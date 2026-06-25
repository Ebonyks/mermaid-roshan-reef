extends Node
class_name CosmeticManager
# ---------------------------------------------------------------------------
# SCAFFOLD (2026-06-25) — the cosmetic "engine" for Roshan.
#
# Replaces the old mutually-exclusive billboard skins (player.set_skin) with a
# COMPOSABLE, data-driven cosmetic system on the ONE shared rigged base model.
# A loadout (e.g. "fairy") is a stack of cosmetics applied together; the Fairy
# variant is therefore a *loadout*, not a separate model.
#
# Three cosmetic types (see assets/characters/cosmetics/catalog.json):
#   socket   -> instantiate a part GLB, attach to a named bone socket
#   material -> override material / params on matching mesh surfaces
#   morph    -> drive a blend-shape (morph target) 0..1
#
# DESIGN RULES
#   * Pure-additive & safe: every step is guarded. Missing asset / bone / morph /
#     surface => that cosmetic is skipped with a push_warning, never a crash. So
#     this can ship before any cosmetic art or socket bones exist (applying the
#     "classic" loadout is a clean no-op).
#   * Re-applying a loadout first fully reverts the previous one (sockets freed,
#     materials/morphs restored), so swaps don't accumulate.
#   * NOT yet wired into the game. To enable, see CHARACTER_CUSTOMIZATION.md §8:
#       var cm := CosmeticManager.new(); add_child(cm); cm.setup(player)
#       cm.apply_loadout("fairy")
# ---------------------------------------------------------------------------

const CATALOG_PATH := "res://assets/characters/cosmetics/catalog.json"

var _player: Node3D = null
var _catalog: Dictionary = {}
var _spawned: Array[Node] = []                 # socket nodes we created (for cleanup)
var _mat_backup: Array = []                    # [{mi, surface, original_material}]
var _morph_backup: Array = []                  # [{mi, blend_idx, original_value}]
var current_loadout := "classic"

func setup(player: Node3D, catalog_path: String = CATALOG_PATH) -> bool:
	_player = player
	_catalog = _load_catalog(catalog_path)
	return not _catalog.is_empty()

func _load_catalog(path: String) -> Dictionary:
	if not ResourceLoader.exists(path) and not FileAccess.file_exists(path):
		push_warning("CosmeticManager: catalog not found at %s" % path)
		return {}
	var f := FileAccess.open(path, FileAccess.READ)
	if f == null:
		push_warning("CosmeticManager: cannot open %s" % path)
		return {}
	var parsed: Variant = JSON.parse_string(f.get_as_text())
	if typeof(parsed) != TYPE_DICTIONARY:
		push_warning("CosmeticManager: catalog is not valid JSON object")
		return {}
	return parsed

# --- public API -----------------------------------------------------------

func list_loadouts() -> Array:
	return (_catalog.get("loadouts", {}) as Dictionary).keys()

func apply_loadout(loadout_id: String) -> void:
	_revert()
	current_loadout = loadout_id
	var loadouts: Dictionary = _catalog.get("loadouts", {})
	if not loadouts.has(loadout_id):
		push_warning("CosmeticManager: unknown loadout '%s'" % loadout_id)
		return
	# resolve to cosmetics, keeping only the last entry per layer (mutual exclusion)
	var cosmetics: Dictionary = _catalog.get("cosmetics", {})
	var by_layer: Dictionary = {}
	var order: Array = []
	for cid in loadouts[loadout_id]:
		if not cosmetics.has(cid):
			push_warning("CosmeticManager: loadout '%s' references unknown cosmetic '%s'" % [loadout_id, cid])
			continue
		var c: Dictionary = cosmetics[cid]
		var layer: String = String(c.get("layer", cid))
		if by_layer.has(layer):
			order.erase(layer)
		by_layer[layer] = c
		order.append(layer)
	for layer in order:
		_apply_one(by_layer[layer])

func apply_cosmetic_by_id(cid: String) -> void:
	var cosmetics: Dictionary = _catalog.get("cosmetics", {})
	if cosmetics.has(cid):
		_apply_one(cosmetics[cid])
	else:
		push_warning("CosmeticManager: unknown cosmetic '%s'" % cid)

# --- application ----------------------------------------------------------

func _apply_one(c: Dictionary) -> void:
	match String(c.get("type", "")):
		"socket":   _apply_socket(c)
		"material": _apply_material(c)
		"morph":    _apply_morph(c)
		_:          push_warning("CosmeticManager: cosmetic with unknown type: %s" % c)

func _apply_socket(c: Dictionary) -> void:
	var path: String = String(c.get("asset", ""))
	if not ResourceLoader.exists(path):
		push_warning("CosmeticManager: socket asset missing: %s" % path); return
	var ps: PackedScene = load(path)
	if ps == null:
		return
	for sock_key in ["socket", "mirror_socket"]:
		if not c.has(sock_key):
			continue
		var bone: String = String(c[sock_key])
		var inst: Node3D = ps.instantiate()
		var off: Dictionary = c.get("offset", {})
		if off.has("scale"):
			inst.scale = Vector3.ONE * float(off["scale"])
		if off.has("pos"):
			var p: Array = off["pos"]
			inst.position = Vector3(p[0], p[1], p[2])
		if sock_key == "mirror_socket":
			inst.scale.x *= -1.0   # mirror for the opposite side (e.g. second wing)
		if _player != null and _player.has_method("attach_bone") and _player.attach_bone(inst, bone):
			_spawned.append(inst)
		else:
			push_warning("CosmeticManager: could not attach to bone '%s' (missing socket?)" % bone)
			inst.queue_free()

func _apply_material(c: Dictionary) -> void:
	var match_str: String = String(c.get("surface_match", "")).to_lower()
	for mi in _iter_mesh_instances():
		var mesh: Mesh = mi.mesh
		if mesh == null:
			continue
		for si in range(mesh.get_surface_count()):
			var src: Material = mi.get_active_material(si)
			var sname: String = (src.resource_name if src != null else "").to_lower()
			if match_str != "" and match_str not in sname and match_str not in mi.name.to_lower():
				continue
			_mat_backup.append({"mi": mi, "surface": si, "mat": mi.get_surface_override_material(si)})
			var new_mat: Material = _build_material(c, src)
			mi.set_surface_override_material(si, new_mat)

func _build_material(c: Dictionary, src: Material) -> Material:
	if c.has("shader"):
		var sm := ShaderMaterial.new()
		var sh: Shader = load(String(c["shader"]))
		if sh != null:
			sm.shader = sh
		return sm
	# else a tweaked copy of the existing material
	var m: BaseMaterial3D = (src.duplicate() if src is BaseMaterial3D else StandardMaterial3D.new())
	var params: Dictionary = c.get("params", {})
	if params.has("albedo_color"):
		var a: Array = params["albedo_color"]
		m.albedo_color = Color(a[0], a[1], a[2], a[3] if a.size() > 3 else 1.0)
	if params.has("emission_energy"):
		m.emission_enabled = true
		m.emission_energy_multiplier = float(params["emission_energy"])
	return m

func _apply_morph(c: Dictionary) -> void:
	var morph: String = String(c.get("morph", ""))
	var value := float(c.get("value", 1.0))
	for mi in _iter_mesh_instances():
		var mesh: Mesh = mi.mesh
		if mesh == null or mesh.get_blend_shape_count() == 0:
			continue
		var bi := -1
		for k in range(mesh.get_blend_shape_count()):
			if String(mesh.get_blend_shape_name(k)) == morph:
				bi = k; break
		if bi < 0:
			continue
		_morph_backup.append({"mi": mi, "idx": bi, "val": mi.get_blend_shape_value(bi)})
		mi.set_blend_shape_value(bi, value)

# --- revert ---------------------------------------------------------------

func _revert() -> void:
	for n in _spawned:
		if is_instance_valid(n):
			var p := n.get_parent()      # the BoneAttachment3D attach_bone created
			n.queue_free()
			if p is BoneAttachment3D and p.get_child_count() <= 1:
				p.queue_free()
	_spawned.clear()
	for b in _mat_backup:
		if is_instance_valid(b["mi"]):
			(b["mi"] as MeshInstance3D).set_surface_override_material(b["surface"], b["mat"])
	_mat_backup.clear()
	for b in _morph_backup:
		if is_instance_valid(b["mi"]):
			(b["mi"] as MeshInstance3D).set_blend_shape_value(b["idx"], b["val"])
	_morph_backup.clear()

# --- helpers --------------------------------------------------------------

func _iter_mesh_instances() -> Array:
	var out: Array = []
	var root: Node = _player.model_root if (_player != null and "model_root" in _player) else _player
	if root != null:
		_collect_meshes(root, out)
	return out

func _collect_meshes(n: Node, out: Array) -> void:
	if n is MeshInstance3D:
		out.append(n)
	for c in n.get_children():
		_collect_meshes(c, out)
