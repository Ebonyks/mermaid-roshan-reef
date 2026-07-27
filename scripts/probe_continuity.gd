extends SceneTree
# The continuity gate — run LIVE while an asset is being built, not after a
# batch is finished. It answers the two questions that decide whether a model
# can ship at all, before any human looks at it:
#
#   1. Does it satisfy the construction contract (states, budgets, no lights,
#      no skeletons, texture rules, scale)?
#   2. Does it belong next to the objects already in the game — same pastel
#      band, same toy-material language — or is it a beautiful visitor?
#
# It reads the .glb straight from disk with GLTFDocument, so it needs no
# import pass (and therefore cannot hit the NPOT importer deadlock). It is a
# GATE: it prints CONTINUITY| lines and exits 1 if anything FAILs.
#
# Run:  $GODOT --headless -s scripts/probe_continuity.gd -- <path.glb> [more...]
#       $GODOT --headless -s scripts/probe_continuity.gd        # sweep all existing manifest objects
#
# States/paths come from audit/opera_art_manifest.json (regenerate with
# scripts/probe_art_manifest.gd when the fingerprint moves).

const MANIFEST_PATH := "res://audit/opera_art_manifest.json"
const OUT_PATH := "res://audit/continuity_report.json"
const JOBS_ROOT := "res://assets/opera/jobs"

# --- contract budgets (CODEX_NEXTGEN_OBJECTS_2026-07-25.md §4) ---
const MAX_TRIS_PER_STATE := 900
const MAX_TRIS_HERO_TOTAL := 1500
const MAX_MATERIALS := 4
const MAX_TEXTURE_SIDE := 1024
const MAX_NODES := 40
const MIN_TARGET_AXIS := 0.55          # narrowest readable axis for finger targets
const MAX_EXTENT := 10.0               # anything bigger smells like a 100x export
const MIN_EXTENT := 0.05

# --- design-language band (pastel toy playset, matches _toonify output) ---
const SAT_FAIL := 0.70                 # mean saturation above this is not pastel
const SAT_WARN := 0.55
const VAL_FAIL_LOW := 0.30             # mean value below this vanishes on stage
const VAL_WARN_LOW := 0.45
const VAL_WARN_HIGH := 0.965           # near-white clips past ACES/AgX on Android
const DARK_ACCENT_MAX := 0.50          # navy outline accents may not dominate
const ROUGH_FAIL := 0.70               # toonify sets roughness 1.0, metallic 0.0
const METAL_FAIL := 0.10
const TEX_DETAIL_WARN := 0.22          # albedo luminance stddev; toon fills are flat

# --- neighbour continuity (the "visitor" test) ---
const MIN_NEIGHBOURS := 2              # below this, only the absolute band gates
const DELTA_FAIL := 0.22               # |candidate - neighbour median| in S or V
const DELTA_WARN := 0.12

var _stats_cache := {}                 # abs path -> stats dict (sweeps reparse nothing)
var _obj_index := {}                   # "assets/..." rel path -> manifest object info
var _manifest_ok := false
var _fingerprint := ""

func _init() -> void:
	_load_manifest()
	var targets := _targets()
	if targets.is_empty():
		print("CONTINUITY|no targets — pass .glb paths after --, or add assets under %s" % JOBS_ROOT)
		quit(1)
		return
	var report := {}
	var fails := 0
	var warn_only := 0
	for rel: String in targets:
		var entry := _check_object(rel)
		report[rel] = entry
		var verdict := String(entry["verdict"])
		if verdict == "FAIL":
			fails += 1
		elif verdict == "WARN":
			warn_only += 1
	var out := {
		"schema": 1,
		"generated_from": "scripts/probe_continuity.gd",
		"manifest_fingerprint": _fingerprint,
		"objects": report,
	}
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path("res://audit"))
	var f := FileAccess.open(OUT_PATH, FileAccess.WRITE)
	if f != null:
		f.store_string(JSON.stringify(out, "\t", false) + "\n")
		f.close()
	print("CONTINUITY|checked=%d pass=%d warn=%d fail=%d report=%s"
		% [targets.size(), targets.size() - fails - warn_only, warn_only, fails, OUT_PATH])
	print("CONTINUITY|done")
	quit(1 if fails > 0 else 0)

# ---------------------------------------------------------------- targets ---

func _targets() -> Array:
	var out: Array = []
	var args := OS.get_cmdline_user_args()
	for a: String in args:
		var rel := a.replace("\\", "/").trim_prefix("res://")
		if rel.ends_with(".glb"):
			out.append(rel)
	if out.is_empty():
		for rel in _glbs_under(JOBS_ROOT):
			out.append(rel)
	return out

func _glbs_under(root: String) -> Array:
	var out: Array = []
	var stack: Array = [root]
	while not stack.is_empty():
		var dir_path: String = stack.pop_back()
		var d := DirAccess.open(dir_path)
		if d == null:
			continue
		d.list_dir_begin()
		var name := d.get_next()
		while name != "":
			if d.current_is_dir():
				if not name.begins_with("."):
					stack.append(dir_path.path_join(name))
			elif name.ends_with(".glb"):
				out.append(dir_path.path_join(name).trim_prefix("res://"))
			name = d.get_next()
		d.list_dir_end()
	out.sort()
	return out

# --------------------------------------------------------------- manifest ---

func _load_manifest() -> void:
	if not FileAccess.file_exists(MANIFEST_PATH):
		print("CONTINUITY|manifest missing — state checks will be skipped; run scripts/probe_art_manifest.gd")
		return
	var parsed: Variant = JSON.parse_string(FileAccess.get_file_as_string(MANIFEST_PATH))
	if not (parsed is Dictionary):
		print("CONTINUITY|manifest unreadable — state checks will be skipped")
		return
	var manifest: Dictionary = parsed
	_fingerprint = String(manifest.get("fingerprint", ""))
	var acts: Dictionary = manifest.get("acts", {})
	for costume in acts.keys():
		var act: Dictionary = acts[costume]
		for b: Dictionary in act.get("beats", []):
			var objs: Dictionary = b.get("objects", {})
			for oname in objs.keys():
				var od: Dictionary = objs[oname]
				_obj_index[String(od.get("path", ""))] = {
					"costume": String(costume),
					"object": String(oname),
					"beat": String(b.get("beat", "")),
					"gesture": String(b.get("gesture", "")),
					"states": od.get("states", []),
				}
	_manifest_ok = true

# ------------------------------------------------------------- the checks ---

func _check_object(rel: String) -> Dictionary:
	var reasons: Array = []
	var warns: Array = []
	var stats := _stats_for(rel)
	if stats.is_empty():
		print("CONTINUITY|obj=%s verdict=FAIL reasons=unreadable_glb" % rel)
		return {"verdict": "FAIL", "reasons": ["unreadable_glb"]}

	var info: Dictionary = _obj_index.get(rel, {})
	if _manifest_ok and info.is_empty() and rel.begins_with("assets/opera/jobs/"):
		# Outfits and pre-manifest props live here legitimately; a NEW beat
		# object at a path the manifest does not know is the real hazard —
		# check the name you were told, not the name you invented.
		warns.append("not_a_manifest_object_states_unchecked")

	# 1. states are child nodes, exactly one visible
	if not info.is_empty():
		var expected: Array = []
		for s: String in info["states"]:
			expected.append("State" + s.to_pascal_case())
		var have: Array = stats["state_nodes"]
		for e: String in expected:
			if not have.has(e):
				reasons.append("missing_state:" + e)
		for h: String in have:
			if not expected.has(h):
				warns.append("extra_state:" + h)
		if expected.size() > 0:
			var vis: int = stats["visible_states"]
			if vis != 1:
				reasons.append("default_visible_states=%d_want_1" % vis)

	# 2. forbidden node types
	if stats["lights"] > 0:
		reasons.append("lights=%d" % stats["lights"])
	if stats["skeletons"] > 0:
		reasons.append("skeletons=%d" % stats["skeletons"])
	if stats["anim_players"] > 0:
		reasons.append("animation_players=%d" % stats["anim_players"])
	if stats["nodes"] > MAX_NODES:
		reasons.append("nodes=%d_max_%d" % [stats["nodes"], MAX_NODES])

	# 3. budgets
	var worst_state_tris: int = stats["worst_state_tris"]
	if worst_state_tris > MAX_TRIS_PER_STATE:
		reasons.append("tris_per_state=%d_max_%d" % [worst_state_tris, MAX_TRIS_PER_STATE])
	if stats["total_tris"] > MAX_TRIS_HERO_TOTAL:
		warns.append("total_tris=%d_over_hero_budget_%d" % [stats["total_tris"], MAX_TRIS_HERO_TOTAL])
	if stats["materials"] > MAX_MATERIALS:
		reasons.append("materials=%d_max_%d" % [stats["materials"], MAX_MATERIALS])
	for t: Dictionary in stats["textures"]:
		var w: int = t["w"]
		var h: int = t["h"]
		var pot: bool = _is_pot(w) and _is_pot(h)
		if maxi(w, h) > MAX_TEXTURE_SIDE and not pot:
			reasons.append("texture_%dx%d_npot_and_over_%d" % [w, h, MAX_TEXTURE_SIDE])
		elif not pot:
			warns.append("texture_%dx%d_npot_no_vram_compress" % [w, h])

	# 4. scale and pivot
	var size: Vector3 = stats["aabb_size"]
	var max_ext: float = maxf(size.x, maxf(size.y, size.z))
	if max_ext > MAX_EXTENT:
		reasons.append("extent=%.1fm_smells_like_100x_export" % max_ext)
	elif max_ext < MIN_EXTENT and max_ext > 0.0:
		reasons.append("extent=%.3fm_too_small_to_exist" % max_ext)
	var narrow: float = minf(size.x, minf(size.y, size.z))
	var readable: float = maxf(narrow, _mid(size))
	if readable < MIN_TARGET_AXIS and max_ext >= MIN_EXTENT:
		warns.append("readable_axis=%.2fm_under_%.2fm_check_if_finger_target" % [readable, MIN_TARGET_AXIS])
	if stats["below_origin_frac"] > 0.45:
		warns.append("origin_looks_centred_want_contact_point")

	# 5. material language (toonify contract)
	if stats["normal_maps"] > 0:
		reasons.append("normal_maps=%d_toonify_strips_these" % stats["normal_maps"])
	if stats["max_metallic"] > METAL_FAIL:
		reasons.append("metallic=%.2f_toy_language_is_matte" % stats["max_metallic"])
	if stats["min_roughness"] < ROUGH_FAIL:
		reasons.append("roughness=%.2f_toy_language_is_matte" % stats["min_roughness"])
	if stats["overbright_albedo"]:
		reasons.append("albedo_over_1.0_clips_past_tonemap")
	if stats["shader_materials"] > 0:
		warns.append("shader_materials=%d_gate_cannot_read_them" % stats["shader_materials"])

	# 6. palette: absolute pastel band
	var sat: float = stats["mean_sat"]
	var val: float = stats["mean_val"]
	if sat > SAT_FAIL:
		reasons.append("saturation=%.2f_not_pastel" % sat)
	elif sat > SAT_WARN:
		warns.append("saturation=%.2f_hot_for_the_set" % sat)
	if val < VAL_FAIL_LOW:
		reasons.append("value=%.2f_too_dark_for_stage" % val)
	elif val < VAL_WARN_LOW:
		warns.append("value=%.2f_dim_for_the_set" % val)
	elif val > VAL_WARN_HIGH:
		warns.append("value=%.2f_will_clip_white_on_android" % val)
	if stats["dark_frac"] > DARK_ACCENT_MAX:
		warns.append("dark_share=%.2f_outline_navy_dominates" % stats["dark_frac"])
	if stats["tex_detail"] > TEX_DETAIL_WARN:
		warns.append("texture_detail=%.2f_reads_photographic_not_toy" % stats["tex_detail"])

	# 7. palette: neighbours — the visitor test
	var neighbours := _neighbour_stats(rel)
	var d_sat := 0.0
	var d_val := 0.0
	if neighbours.size() >= MIN_NEIGHBOURS:
		d_sat = sat - _median(neighbours.map(func(n: Dictionary) -> float: return n["mean_sat"]))
		d_val = val - _median(neighbours.map(func(n: Dictionary) -> float: return n["mean_val"]))
		if absf(d_sat) > DELTA_FAIL:
			reasons.append("visitor_saturation_delta=%+.2f_vs_%d_neighbours" % [d_sat, neighbours.size()])
		elif absf(d_sat) > DELTA_WARN:
			warns.append("saturation_delta=%+.2f_vs_neighbours" % d_sat)
		if absf(d_val) > DELTA_FAIL:
			reasons.append("visitor_value_delta=%+.2f_vs_%d_neighbours" % [d_val, neighbours.size()])
		elif absf(d_val) > DELTA_WARN:
			warns.append("value_delta=%+.2f_vs_neighbours" % d_val)

	# 8. stage contrast, reported not gated: props must read AGAINST their set
	var stage_note := ""
	if not info.is_empty():
		stage_note = _stage_contrast(String(info["costume"]), val)

	var verdict := "PASS"
	if not reasons.is_empty():
		verdict = "FAIL"
	elif not warns.is_empty():
		verdict = "WARN"
	var line := "CONTINUITY|obj=%s verdict=%s tris=%d/%d mats=%d sat=%.2f val=%.2f dsat=%+.2f dval=%+.2f" \
		% [rel, verdict, worst_state_tris, stats["total_tris"], stats["materials"], sat, val, d_sat, d_val]
	if not reasons.is_empty():
		line += " fail=" + ",".join(reasons)
	if not warns.is_empty():
		line += " warn=" + ",".join(warns)
	if stage_note != "":
		line += " " + stage_note
	print(line)
	return {
		"verdict": verdict, "reasons": reasons, "warnings": warns,
		"tris_worst_state": worst_state_tris, "tris_total": stats["total_tris"],
		"materials": stats["materials"], "nodes": stats["nodes"],
		"mean_sat": sat, "mean_val": val, "dark_frac": stats["dark_frac"],
		"tex_detail": stats["tex_detail"], "aabb_size": [size.x, size.y, size.z],
		"delta_sat_vs_neighbours": d_sat, "delta_val_vs_neighbours": d_val,
		"neighbours": neighbours.size(),
	}

func _stage_contrast(costume: String, val: float) -> String:
	if not (OperaAct.STAGE_SETS is Dictionary) or not OperaAct.STAGE_SETS.has(costume):
		return ""
	var set_cfg: Dictionary = OperaAct.STAGE_SETS[costume]
	var backdrop: Color = set_cfg.get("backdrop", Color.WHITE)
	return "stage_contrast=%.2f" % absf(val - backdrop.v)

# --------------------------------------------------------- neighbour pool ---

func _neighbour_stats(rel: String) -> Array:
	var pool: Array = []
	var folder := ("res://" + rel).get_base_dir()
	for other in _glbs_under(folder):
		if other != rel:
			pool.append(other)
	if pool.size() < MIN_NEIGHBOURS:
		for other in _glbs_under(JOBS_ROOT):
			if other != rel and not pool.has(other):
				pool.append(other)
	var out: Array = []
	for other: String in pool:
		var s := _stats_for(other)
		if not s.is_empty():
			out.append(s)
	return out

# ---------------------------------------------------------- glb -> stats ----

func _stats_for(rel: String) -> Dictionary:
	if _stats_cache.has(rel):
		return _stats_cache[rel]
	var abs_path := ProjectSettings.globalize_path("res://" + rel)
	var stats := {}
	if FileAccess.file_exists(abs_path):
		var doc := GLTFDocument.new()
		var state := GLTFState.new()
		if doc.append_from_file(abs_path, state) == OK:
			var root := doc.generate_scene(state)
			if root != null:
				stats = _measure(root)
				root.free()
	_stats_cache[rel] = stats
	return stats

func _measure(root: Node) -> Dictionary:
	var s := {
		"nodes": 0, "lights": 0, "skeletons": 0, "anim_players": 0,
		"state_nodes": [], "visible_states": 0,
		"total_tris": 0, "base_tris": 0, "state_tris": {},
		"materials": 0, "textures": [], "normal_maps": 0,
		"max_metallic": 0.0, "min_roughness": 1.0,
		"shader_materials": 0, "overbright_albedo": false,
		"aabb_size": Vector3.ZERO, "below_origin_frac": 0.0,
		"mean_sat": 0.0, "mean_val": 0.0, "dark_frac": 0.0, "tex_detail": 0.0,
	}
	# top-level State* children (glTF roots wrap everything in one scene node)
	var scan_root := root
	if root.get_child_count() == 1 and not _has_state_child(root):
		if _has_state_child(root.get_child(0)):
			scan_root = root.get_child(0)
	for c in scan_root.get_children():
		if String(c.name).begins_with("State"):
			s["state_nodes"].append(String(c.name))
			if c is Node3D and (c as Node3D).visible:
				s["visible_states"] = int(s["visible_states"]) + 1
	var mats := {}       # material -> true
	var weights: Array = []   # [color: Color, weight: float]
	var bounds := AABB()
	var have_bounds := false
	var stack: Array = [[root, Transform3D.IDENTITY, ""]]
	while not stack.is_empty():
		var item: Array = stack.pop_back()
		var node: Node = item[0]
		var xf: Transform3D = item[1]
		var state_name: String = item[2]
		s["nodes"] = int(s["nodes"]) + 1
		if node is Node3D:
			xf = xf * (node as Node3D).transform
		if node.get_parent() == scan_root and String(node.name).begins_with("State"):
			state_name = String(node.name)
		if node is Light3D:
			s["lights"] = int(s["lights"]) + 1
		if node is Skeleton3D:
			s["skeletons"] = int(s["skeletons"]) + 1
		if node is AnimationPlayer:
			s["anim_players"] = int(s["anim_players"]) + 1
		if node is MeshInstance3D:
			var mi := node as MeshInstance3D
			if mi.mesh != null:
				var local: AABB = xf * mi.mesh.get_aabb()
				bounds = local if not have_bounds else bounds.merge(local)
				have_bounds = true
				for si in range(mi.mesh.get_surface_count()):
					var tris := _surface_tris(mi.mesh, si)
					s["total_tris"] = int(s["total_tris"]) + tris
					if state_name == "":
						s["base_tris"] = int(s["base_tris"]) + tris
					else:
						var st: Dictionary = s["state_tris"]
						st[state_name] = int(st.get(state_name, 0)) + tris
					var m: Material = mi.get_surface_override_material(si)
					if m == null:
						m = mi.mesh.surface_get_material(si)
					if m == null:
						continue
					mats[m] = true
					_measure_material(m, float(tris), s, weights)
		for c in node.get_children():
			stack.append([c, xf, state_name])
	s["materials"] = mats.size()
	var worst: int = int(s["base_tris"])
	if (s["state_tris"] as Dictionary).is_empty():
		worst = int(s["total_tris"])
	else:
		for k in (s["state_tris"] as Dictionary).keys():
			worst = maxi(worst, int(s["base_tris"]) + int(s["state_tris"][k]))
	s["worst_state_tris"] = worst
	if have_bounds:
		s["aabb_size"] = bounds.size
		if bounds.size.y > 0.001:
			s["below_origin_frac"] = clampf(-bounds.position.y / bounds.size.y, 0.0, 1.0)
	# weighted palette
	var tw := 0.0
	var sat := 0.0
	var val := 0.0
	var dark := 0.0
	for pair: Array in weights:
		var c: Color = pair[0]
		var w: float = pair[1]
		tw += w
		sat += c.s * w
		val += c.v * w
		if c.v < 0.35:
			dark += w
	if tw > 0.0:
		s["mean_sat"] = sat / tw
		s["mean_val"] = val / tw
		s["dark_frac"] = dark / tw
	return s

func _measure_material(m: Material, weight: float, s: Dictionary, weights: Array) -> void:
	if not (m is BaseMaterial3D):
		s["shader_materials"] = int(s["shader_materials"]) + 1
		return
	var bm := m as BaseMaterial3D
	if bm.normal_enabled and bm.normal_texture != null:
		s["normal_maps"] = int(s["normal_maps"]) + 1
	s["max_metallic"] = maxf(float(s["max_metallic"]), bm.metallic)
	s["min_roughness"] = minf(float(s["min_roughness"]), bm.roughness)
	var c := bm.albedo_color
	if c.r > 1.001 or c.g > 1.001 or c.b > 1.001:
		s["overbright_albedo"] = true
	if bm.albedo_texture != null:
		var tex := bm.albedo_texture
		var found := false
		for t: Dictionary in s["textures"]:
			if t["tex"] == tex:
				found = true
		if not found:
			var sample := _sample_texture(tex)
			(s["textures"] as Array).append({
				"tex": tex, "w": tex.get_width(), "h": tex.get_height()})
			s["tex_detail"] = maxf(float(s["tex_detail"]), float(sample["stddev"]))
		var mean: Color = _sample_texture(tex)["mean"]
		c = Color(c.r * mean.r, c.g * mean.g, c.b * mean.b)
	weights.append([c, maxf(weight, 1.0)])

var _tex_cache := {}

func _sample_texture(tex: Texture2D) -> Dictionary:
	if _tex_cache.has(tex):
		return _tex_cache[tex]
	var out := {"mean": Color.WHITE, "stddev": 0.0}
	var img := tex.get_image()
	if img != null:
		if img.is_compressed():
			img.decompress()
		var n := 16
		var sum := Vector3.ZERO
		var lums: Array = []
		for iy in range(n):
			for ix in range(n):
				var px := img.get_pixel(
					int((ix + 0.5) * img.get_width() / n),
					int((iy + 0.5) * img.get_height() / n))
				sum += Vector3(px.r, px.g, px.b)
				lums.append(px.get_luminance())
		var count := float(n * n)
		out["mean"] = Color(sum.x / count, sum.y / count, sum.z / count)
		var mean_l := 0.0
		for l: float in lums:
			mean_l += l
		mean_l /= count
		var variance := 0.0
		for l: float in lums:
			variance += (l - mean_l) * (l - mean_l)
		out["stddev"] = sqrt(variance / count)
	_tex_cache[tex] = out
	return out

# ------------------------------------------------------------------ misc ----

func _surface_tris(mesh: Mesh, si: int) -> int:
	var arrays := mesh.surface_get_arrays(si)
	if arrays.is_empty():
		return 0
	var idx: Variant = arrays[Mesh.ARRAY_INDEX]
	if idx != null and (idx as PackedInt32Array).size() > 0:
		return (idx as PackedInt32Array).size() / 3
	var verts: Variant = arrays[Mesh.ARRAY_VERTEX]
	if verts != null:
		return (verts as PackedVector3Array).size() / 3
	return 0

func _has_state_child(node: Node) -> bool:
	for c in node.get_children():
		if String(c.name).begins_with("State"):
			return true
	return false

func _is_pot(v: int) -> bool:
	return v > 0 and (v & (v - 1)) == 0

func _mid(v: Vector3) -> float:
	var a: Array = [v.x, v.y, v.z]
	a.sort()
	return a[1]

func _median(values: Array) -> float:
	if values.is_empty():
		return 0.0
	var a := values.duplicate()
	a.sort()
	return a[a.size() / 2]
