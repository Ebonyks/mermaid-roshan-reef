extends SceneTree
## R6 additive current promenade diagnostic extension; original sources and normal saves preserved.
const GODOT_BASELINE_PATH := "res://tools/godot_baseline.json"
const READY_FRAME_LIMIT := 240
const SOURCE_FIXED_FILES: Array[String] = [
	"project.godot",
	"tools/audit_opera_capture.py",
	"tools/audit_godot_baseline.py",
	"tools/godot_baseline.json",
]
const SOURCE_TREE_ROOTS: Array[String] = [
	"assets", "scenes", "scripts", "shaders",
]
const SOURCE_TREE_SUFFIXES := {
	"assets": [
		".bmp", ".dds", ".exr", ".gdshader", ".hdr", ".import", ".jpeg",
		".jpg", ".json", ".ktx", ".mp3", ".ogg", ".ogv", ".png", ".res", ".tres", ".svg", ".tga",
		".uid", ".wav", ".webp",
	],
	"scenes": [".res", ".tres", ".tscn", ".uid"],
	"scripts": [".gd", ".uid", ".json"],
	"shaders": [".gdshader", ".uid"],
}

const EXPECTED_IDS: Array[String] = ["saved_entry", "runway_arrival", "runway_departed", "runway_saved_reentry", "playground_overview", "slide_idle", "slide_pressed", "slide_focus", "slide_focus_late", "slide_ground_cancel", "slide_pause_resumed", "slide_action", "slide_settled", "swing_idle", "swing_pressed", "swing_focus", "swing_focus_late", "swing_ground_cancel", "swing_pause_resumed", "swing_action", "swing_settled", "seesaw_idle", "seesaw_pressed", "seesaw_focus", "seesaw_focus_late", "seesaw_ground_cancel", "seesaw_pause_resumed", "seesaw_action", "seesaw_settled", "castle_idle", "castle_focus", "castle_ground_cancel"]
var failures: int = 0
var capture_root := ""
var aspect_size := Vector2i.ZERO
var run_case := ""
var capture_main: ReefMain
var promenade: SkyLagoonPromenade
var isolated_save := ""
var states: Array[Dictionary] = []
var checks: Array[Dictionary] = []
var capture_source_signature: Dictionary = {}
var normal_save_before: Dictionary = {}
var want_night := false
var want_dayone := false
var setup_trace: Array[Dictionary] = []

func _init() -> void:
	call_deferred("_run")

func _check(label: String, ok: bool, detail: String = "") -> void:
	checks.append({"label": label, "pass": ok, "detail": detail})
	if not ok:
		failures += 1
	print("LIVE6|%s|%s|%s|%s" % [run_case, "PASS" if ok else "FAIL", label, detail])

func _frames(count: int) -> void:
	for _index: int in range(count):
		await process_frame

func _wait(seconds: float) -> void:
	await create_timer(seconds, true).timeout

func _find(name: String) -> Button:
	return capture_main.find_child(name, true, false) as Button

func _pointer(button: Button, pressed: bool, outside: bool = false) -> void:
	if outside:
		var move := InputEventMouseMotion.new()
		move.position = Vector2(1255.0, 710.0)
		move.global_position = move.position
		root.push_input(move, true)
	var event := InputEventMouseButton.new()
	event.button_index = MOUSE_BUTTON_LEFT
	event.pressed = pressed
	event.button_mask = MOUSE_BUTTON_MASK_LEFT if pressed else 0
	event.position = Vector2(1255.0, 710.0) if outside else button.get_global_rect().get_center()
	event.global_position = event.position
	root.push_input(event, true)

func _hover(button: Button) -> void:
	var event := InputEventMouseMotion.new()
	event.position = button.get_global_rect().get_center()
	event.global_position = event.position
	root.push_input(event, true)

func _mouse_point(point: Vector2, pressed: bool) -> void:
	var event := InputEventMouseButton.new()
	event.button_index=MOUSE_BUTTON_LEFT
	event.pressed=pressed
	event.button_mask=MOUSE_BUTTON_MASK_LEFT if pressed else 0
	event.position=point
	event.global_position=point
	root.push_input(event,true)

func _click(button: Button) -> void:
	_check("pointer target exists", is_instance_valid(button))
	if not is_instance_valid(button):
		return
	# Capture coordinates before input: callbacks can remove/rebuild this control.
	var point: Vector2 = button.get_global_rect().get_center()
	_hover(button)
	await _frames(1)
	_mouse_point(point,true)
	await _frames(2)
	_mouse_point(point,false)
	await _frames(3)

func _style(style: StyleBox) -> Dictionary:
	var out := {"class": style.get_class(), "path": style.resource_path}
	if style is StyleBoxFlat:
		var flat: StyleBoxFlat = style as StyleBoxFlat
		out["bg_color"] = flat.bg_color
		out["border_color"] = flat.border_color
		out["border_widths"] = [flat.border_width_left, flat.border_width_top, flat.border_width_right, flat.border_width_bottom]
		out["corner_radii"] = [flat.corner_radius_top_left, flat.corner_radius_top_right, flat.corner_radius_bottom_left, flat.corner_radius_bottom_right]
		out["shadow_size"] = flat.shadow_size
	elif style is StyleBoxTexture:
		var textured: StyleBoxTexture = style as StyleBoxTexture
		if textured.texture != null:
			out["texture"] = textured.texture.resource_path
		out["modulate"] = textured.modulate_color
		out["texture_margins"] = [textured.texture_margin_left, textured.texture_margin_top, textured.texture_margin_right, textured.texture_margin_bottom]
	return out

func _collect_visible(node: Node, rows: Array[Dictionary], layer: int = 0, layer_visible: bool = true) -> void:
	if node is CanvasLayer:
		layer = (node as CanvasLayer).layer
		layer_visible = layer_visible and (node as CanvasLayer).visible
	if node is CanvasItem and (node as CanvasItem).is_visible_in_tree() and layer_visible:
		var item: CanvasItem = node as CanvasItem
		var row: Dictionary = {"path": String(capture_main.get_path_to(node)), "class": String(node.get_class()), "modulate": item.modulate, "self_modulate": item.self_modulate, "z_index": item.z_index, "canvas_layer": layer}
		var script: Script = node.get_script() as Script
		if script != null:
			row["script"] = script.resource_path
		if node is Control:
			var control: Control = node as Control
			row["rect"] = control.get_global_rect()
			row["mouse_filter"] = control.mouse_filter
			row["clip_contents"] = control.clip_contents
			var styles: Dictionary = {}
			for key: String in ["normal", "hover", "pressed", "hover_pressed", "disabled", "focus", "panel"]:
				if control.has_theme_stylebox(key):
					styles[key] = _style(control.get_theme_stylebox(key))
			row["styles"] = styles
			row["font"] = _font_record(control.get_theme_font("font"))
			row["font_size"] = control.get_theme_font_size("font_size")
			row["typography_role"] = String(control.get_meta("typography_role", ""))
			row["properties"] = {}
			for property: Dictionary in node.get_property_list():
				if String(property["name"]) in ["selected", "choice_color", "choice_effect", "choice_texture", "atlas_grid", "atlas_frame", "color_id", "symbol_id"]:
					var value: Variant = node.get(String(property["name"]))
					row["properties"][String(property["name"])] = value.resource_path if value is Resource else value
		if node is Label:
			row["text"] = (node as Label).text
		if node is Button:
			var button: Button = node as Button
			row["text"] = button.text
			row["disabled"] = button.disabled
			row["pressed"] = button.button_pressed
			row["draw_mode"] = button.get_draw_mode()
			row["focus"] = button.has_focus()
			row["selected"] = button.get_meta("selected", false)
			row["locked"] = button.get_meta("locked", false)
			var callbacks: Array[Dictionary] = []
			for connection: Dictionary in button.get_signal_connection_list("pressed"):
				var callback: Callable = connection["callable"] as Callable
				var target: Object = callback.get_object()
				callbacks.append({"method":String(callback.get_method()),"valid":callback.is_valid(),"target_id":callback.get_object_id(),"target_class":target.get_class() if is_instance_valid(target) else "missing"})
			row["pressed_callbacks"] = callbacks
		if node is TextureRect:
			var tr: TextureRect = node as TextureRect
			if tr.texture != null:
				row["texture"] = tr.texture.resource_path
		if node is Sprite2D:
			var sprite: Sprite2D = node as Sprite2D
			if sprite.texture != null:
				row["texture"] = sprite.texture.resource_path
		if node is ColorRect:
			row["color"] = (node as ColorRect).color
		if node is Polygon2D:
			var polygon: Polygon2D = node as Polygon2D
			row["polygon"] = polygon.polygon
			row["color"] = polygon.color
			row["position"] = polygon.position
			row["scale"] = polygon.scale
			row["rotation"] = polygon.rotation
		if item.material is ShaderMaterial:
			var material: ShaderMaterial = item.material as ShaderMaterial
			if material.shader != null:
				row["shader"] = material.shader.resource_path
				row["shader_code_sha256"] = material.shader.code.sha256_text()
		rows.append(row)
	for child: Node in node.get_children():
		_collect_visible(child, rows, layer, layer_visible)

func _font_record(font: Font, depth: int = 0) -> Dictionary:
	if font == null or depth > 4:
		return {}
	var out := {"class": font.get_class(), "path": font.resource_path, "family": font.get_font_name(), "style": font.get_font_style_name(), "fallbacks": []}
	if font.resource_path.begins_with("res://") and FileAccess.file_exists(font.resource_path):
		out["source_sha256"] = FileAccess.get_sha256(font.resource_path)
	else:
		out["source_limit"] = "Embedded/OS runtime font; no standalone source path exposed; Android fallback and exact font licensing unresolved."
	for fallback: Font in font.fallbacks:
		out["fallbacks"].append(_font_record(fallback, depth + 1))
	return out

func _touch_record() -> Dictionary:
	var t: CanvasLayer = capture_main.touch_ui
	var circles: Array[Dictionary] = []
	for role: String in ["hint", "base", "knob"]:
		var p: Panel = t._stick_hint if role == "hint" else (t._base if role == "base" else t._knob)
		circles.append({"role": role, "path": String(capture_main.get_path_to(p)), "visible": p.visible, "in_tree": p.is_visible_in_tree(), "size": p.size, "style": _style(p.get_theme_stylebox("panel"))})
	var flashes: Array[Dictionary] = []
	for child: Node in t._root.get_children():
		if child is Panel and child not in [t._stick_hint,t._base,t._knob]:
			var p: Panel = child as Panel
			flashes.append({"path": String(capture_main.get_path_to(p)), "visible": p.is_visible_in_tree(), "rect": p.get_global_rect(), "alpha": p.modulate.a, "style": _style(p.get_theme_stylebox("panel"))})
	return {"mode": t.control_mode, "world_enabled": t.world_controls_enabled, "touch_idx": t._touch_idx, "press_elapsed_ms": Time.get_ticks_msec() - t._press_ms, "owners": t.touch_owners.duplicate(), "stick_vec": t.stick_vec, "action_down": t.action_down, "circles": circles, "flashes": flashes}

func _set_aspect(size: Vector2i) -> bool:
	get_root().mode = Window.MODE_WINDOWED
	DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_WINDOWED)
	await process_frame
	for _frame: int in range(READY_FRAME_LIMIT):
		# Windows applies a maximized-to-windowed transition asynchronously.
		# Reassert the requested client size after that transition instead of
		# accepting the monitor-sized backing texture as capture evidence.
		DisplayServer.window_set_position(Vector2i(-2400, 0))
		get_root().size = size
		DisplayServer.window_set_size(size)
		await process_frame
		var image: Image = get_root().get_viewport().get_texture().get_image()
		if image != null and image.get_size() == size:
			return true
	return false

func _engine_contract() -> Dictionary:
	var version := Engine.get_version_info()
	return {
		"major": int(version.get("major", -1)),
		"minor": int(version.get("minor", -1)),
		"patch": int(version.get("patch", -1)),
		"status": String(version.get("status", "")),
		"build": String(version.get("build", "")),
		"version_string": String(version.get("string", "")),
	}

func _exact_engine() -> bool:
	var engine := _engine_contract()
	if not FileAccess.file_exists(GODOT_BASELINE_PATH):
		return false
	var parsed: Variant = JSON.parse_string(FileAccess.get_file_as_string(GODOT_BASELINE_PATH))
	if not parsed is Dictionary:
		return false
	var baseline: Dictionary = parsed
	var parts: PackedStringArray = String(baseline.get("version", "")).split(".")
	if parts.size() != 3:
		return false
	for part: String in parts:
		if not part.is_valid_int():
			return false
	var status: String = String(baseline.get("status", ""))
	var release: String = String(baseline.get("release", ""))
	if status != "stable" or release != "%s-%s" % [String(baseline.get("version", "")), status]:
		return false
	return int(engine["major"]) == int(parts[0]) and int(engine["minor"]) == int(parts[1]) \
		and int(engine["patch"]) == int(parts[2]) and String(engine["status"]) == status \
		and String(engine["build"]) == "official" \
		and String(engine["version_string"]) == "%s (official)" % release

func _source_suffixes(root_name: String) -> Array[String]:
	var suffixes: Array[String] = []
	var raw_suffixes: Array = SOURCE_TREE_SUFFIXES.get(root_name, []) as Array
	for value: Variant in raw_suffixes:
		suffixes.append(String(value))
	return suffixes

func _source_file_matches(file_name: String, suffixes: Array[String]) -> bool:
	var lower_name := file_name.to_lower()
	for suffix: String in suffixes:
		if lower_name.ends_with(suffix):
			return true
	return false

func _collect_source_tree(relative_dir: String, suffixes: Array[String],
		paths: Array[String], missing: Array[String]) -> void:
	var resource_dir := "res://" + relative_dir
	if not DirAccess.dir_exists_absolute(resource_dir):
		missing.append(relative_dir + "/")
		return
	var file_names := DirAccess.get_files_at(resource_dir)
	file_names.sort()
	for file_name: String in file_names:
		if _source_file_matches(file_name, suffixes):
			paths.append(relative_dir + "/" + file_name)
	var directory_names := DirAccess.get_directories_at(resource_dir)
	directory_names.sort()
	for directory_name: String in directory_names:
		_collect_source_tree(
			relative_dir + "/" + directory_name, suffixes, paths, missing)

func _source_path_contract() -> Dictionary:
	var paths: Array[String] = SOURCE_FIXED_FILES.duplicate()
	var missing: Array[String] = []
	var tree_rules: Array[Dictionary] = []
	for root_name: String in SOURCE_TREE_ROOTS:
		var suffixes := _source_suffixes(root_name)
		tree_rules.append({"root": root_name, "suffixes": suffixes})
		_collect_source_tree(root_name, suffixes, paths, missing)
	paths.sort()
	missing.sort()
	return {
		"paths": paths,
		"missing": missing,
		"tree_rules": tree_rules,
	}

func _source_signature() -> Dictionary:
	var contract := _source_path_contract()
	var source_paths: Array = contract.get("paths", []) as Array
	var file_hashes: Dictionary = {}
	var missing: Array = contract.get("missing", []) as Array
	var entries: Array[String] = []
	for relative_value: Variant in source_paths:
		var relative := String(relative_value)
		var resource_path := "res://" + relative
		var digest := ""
		if FileAccess.file_exists(resource_path):
			digest = FileAccess.get_sha256(resource_path)
		if digest.is_empty():
			missing.append(relative)
		else:
			file_hashes[relative] = digest
		entries.append("%s:%s" % [relative, digest])
	missing.sort()
	return {
		"algorithm": "sha256_runtime_roots_promenade_v1",
		"tree_rules": contract.get("tree_rules", []),
		"paths": source_paths,
		"files": file_hashes,
		"missing": missing,
		"sha256": "\n".join(entries).sha256_text(),
	}

func _normal_save_fingerprints() -> Dictionary:
	var values: Dictionary = {}
	var normal := ProjectSettings.globalize_path("user://reef_save.json")
	for suffix: String in ["", ".tmp0", ".tmp1", ".tmp", ".old", ".bak", ".bak.tmp", ".bak.old"]:
		var path := normal + suffix
		values[suffix] = FileAccess.get_sha256(path) if FileAccess.file_exists(path) else "absent"
	return values


func _v(v: Vector2) -> Array[float]:
	return [v.x,v.y]

func _c(c: Color) -> Array[float]:
	return [c.r,c.g,c.b,c.a]

func _cue_record(target: Dictionary) -> Dictionary:
	var node: Node2D = target.get("node") as Node2D
	var glow: Sprite2D = target.get("highlight") as Sprite2D
	var tex: Texture2D = glow.texture
	var texture := {"class":tex.get_class(),"path":tex.resource_path,"width":tex.get_width(),"height":tex.get_height()}
	if tex is GradientTexture2D:
		var gradient: GradientTexture2D = tex as GradientTexture2D
		var colors: Array = []
		var offsets: Array = []
		for color: Color in gradient.gradient.colors:
			colors.append(_c(color))
		for value: float in gradient.gradient.offsets:
			offsets.append(value)
		texture.merge({"fill":gradient.fill,"fill_from":_v(gradient.fill_from),"fill_to":_v(gradient.fill_to),"gradient_colors":colors,"gradient_offsets":offsets})
	var children: Array[Dictionary] = []
	for child: Node in glow.get_children():
		if child is Polygon2D:
			var poly: Polygon2D = child as Polygon2D
			var points: Array = []
			var screen: Array = []
			for point: Vector2 in poly.polygon:
				points.append(_v(point))
				screen.append(_v(poly.get_global_transform_with_canvas()*point))
			children.append({"name":String(poly.name),"path":String(capture_main.get_path_to(poly)),"points":points,"screen_points":screen,"color":_c(poly.color),"visible":poly.is_visible_in_tree(),"role":String(poly.get_meta("canvas_layer_role",""))})
	return {"id":String(target.get("id","")),"kind":String(target.get("kind","")),"node_path":String(capture_main.get_path_to(node)),"node_master":_v(node.position),"node_screen":_v(promenade.screen_from_master(node.position)),"hit_radius_px":float(target.get("radius_px",0)),"glow_path":String(capture_main.get_path_to(glow)),"glow_master":_v(glow.position),"glow_modulate":_c(glow.modulate),"glow_scale":_v(glow.scale),"glow_visible":glow.is_visible_in_tree(),"texture":texture,"children":children,"focus_cue_role":String(glow.get_meta("focus_cue_role","")),"pointer_tip":_v(glow.get_meta("pointer_tip_local",Vector2.ZERO) as Vector2)}

func _snapshot() -> Dictionary:
	var m: ReefMain = capture_main
	var canvas: Array[Dictionary] = []
	_collect_visible(m,canvas)
	var targets: Array[Dictionary] = []
	for value: Variant in m.g.get("lagoon_promenade_targets",[]):
		targets.append(_cue_record(value as Dictionary))
	var play: Dictionary = m.g.get("lagoon_play_anim",{}) as Dictionary
	return {"save_path":m._save_state.save_path,"game":m.game,"phase":String(m.g.get("phase","")),"tree_paused":paused,"start_menu_active":m.start_menu_active,"intro_active":m.intro_active,"story_clip_present":is_instance_valid(m._day_one_story_clip),"fade_alpha":m.fade_rect.color.a*m.fade_rect.modulate.a*m.fade_rect.self_modulate.a if m.fade_rect!=null and m.fade_rect.visible else 0.0,"night":m.is_night,"plays":m.plays,"day_one_active":m.day_one_is_active(),"plane_departed_save":bool(m.save_data.get("lagoon_plane_departed",false)),"route_master_x":promenade.master_route_x(),"focus":String(m.g.get("lagoon_promenade_focus","")),"focus_t":float(m.g.get("lagoon_promenade_focus_t",0)),"action_label":promenade.action_label(),"play_kind":String(play.get("kind","")),"play_phase":String(play.get("phase","")),"play_t":float(play.get("t",0)),"targets":targets,"visible_canvas":canvas,"touch":_touch_record(),"normal_hud_visible":m.hud_layer.visible,"player_hidden":not m.player.visible,"camera2d_current":root.get_viewport().get_camera_2d()==promenade.camera_2d(),"camera3d_current":root.get_viewport().get_camera_3d()!=null,"save_generation":m.save_generation,"firefly_count":(m.g.get("lagoon_night_fireflies",[]) as Array).size(),"castle_armed":bool(m.g.get("lagoon_castle_armed",false))}

func _capture(id: String,expect: Dictionary) -> void:
	await _frames(3)
	await RenderingServer.frame_post_draw
	var actual := _snapshot()
	var valid: bool = actual["save_path"]==isolated_save and actual["game"]=="level2" and actual["phase"]=="promenade" and not actual["tree_paused"] and not actual["start_menu_active"] and not actual["intro_active"] and not actual["story_clip_present"] and float(actual["fade_alpha"])<=0.001 and actual["night"]==want_night and actual["day_one_active"]==want_dayone and actual["camera2d_current"] and not actual["camera3d_current"] and actual["player_hidden"]
	for key: String in expect:
		valid = valid and actual.get(key)==expect[key]
	var image: Image = root.get_viewport().get_texture().get_image()
	var path := capture_root.path_join(id+".png")
	_check("capture path fresh "+id,not FileAccess.file_exists(path))
	var err: Error = image.save_png(path)
	valid = valid and not image.is_empty() and image.get_size()==aspect_size and err==OK
	_check("native state/image "+id,valid,str(expect))
	var file: FileAccess = FileAccess.open(path,FileAccess.READ)
	states.append({"id":id,"sequence":states.size(),"expected":expect,"actual":actual,"status":"PASS" if valid else "FAIL","image":{"file":id+".png","width":image.get_width(),"height":image.get_height(),"bytes":file.get_length(),"sha256":FileAccess.get_sha256(path)}})
	file.close()

func _tap(point: Vector2) -> void:
	var motion := InputEventMouseMotion.new()
	motion.position=point
	motion.global_position=point
	root.push_input(motion,true)
	await _frames(1)
	_mouse_point(point,true)
	await _frames(2)
	_mouse_point(point,false)
	await _frames(3)

func _target(id: String) -> Dictionary:
	for value: Variant in capture_main.g.get("lagoon_promenade_targets",[]):
		var target: Dictionary = value as Dictionary
		if String(target.get("id",""))==id:
			return target
	return {}

func _place(master_x: float) -> void:
	promenade.set_master_route_x(master_x)
	setup_trace.append({"operation":"production set_master_route_x","declared_programmatic_fixture":true,"master_x":master_x})
	await _frames(3)

func _saved_reentry(departed: bool) -> void:
	var m: ReefMain = capture_main
	m.save_data["lagoon_plane_departed"]=departed
	m.plays=1 if want_night else 0
	m._write_save()
	m._save_state.load_save()
	m._apply_quality("speedy")
	m._set_touch_mode("hybrid",false)
	_check("saved play parity/dayone/plane",m.is_night==want_night and m.day_one_is_active()==want_dayone and bool(m.save_data.get("lagoon_plane_departed",false))==departed)
	m._enter_level2_now(false,false,false)
	promenade=m._lagoon_promenade_ref()
	await _frames(12)
	setup_trace.append({"operation":"isolated write/load and production current Sky entry","declared_programmatic_fixture":true,"plays_input":1 if want_night else 0,"night_loaded":m.is_night,"plane_saved":departed,"dayone_loaded":m.day_one_is_active(),"generation":m.save_generation})

func _run_matrix() -> void:
	var m: ReefMain = capture_main
	await _capture("saved_entry",{})
	await _place(610.0)
	await _capture("runway_arrival",{"plane_departed_save":false})
	# The production plane controller earns and writes its ordinary7second departure.
	await _wait(7.3)
	await _capture("runway_departed",{"plane_departed_save":true})
	await _saved_reentry(true)
	await _place(610.0)
	await _capture("runway_saved_reentry",{"plane_departed_save":true})
	await _place(3072.0)
	await _capture("playground_overview",{})
	for id: String in ["slide","swing","seesaw"]:
		var target: Dictionary = _target(id)
		var node: Node2D = target.get("node") as Node2D
		await _place(node.position.x)
		promenade.cancel_navigation()
		await _capture(id+"_idle",{"focus":"","play_kind":""})
		var point: Vector2 = promenade.screen_from_master(node.position)
		var move := InputEventMouseMotion.new()
		move.position=point
		move.global_position=point
		root.push_input(move,true)
		_mouse_point(point,true)
		await _frames(2)
		await _capture(id+"_pressed",{"focus":""})
		_mouse_point(point,false)
		await _frames(3)
		await _capture(id+"_focus",{"focus":id,"action_label":"PLAY"})
		await _wait(0.45)
		await _capture(id+"_focus_late",{"focus":id,"action_label":"PLAY"})
		await _tap(Vector2(aspect_size.x*0.70,690))
		await _capture(id+"_ground_cancel",{"focus":"","action_label":"JUMP"})
		point=promenade.screen_from_master(node.position)
		await _tap(point)
		_check("raw refocus before pause "+id,String(m.g.get("lagoon_promenade_focus",""))==id)
		m.toggle_pause()
		await _frames(2)
		m.toggle_pause()
		await _frames(3)
		await _capture(id+"_pause_resumed",{"focus":"","action_label":"JUMP"})
		point=promenade.screen_from_master(node.position)
		await _tap(point)
		await _tap(point)
		await _wait(0.2)
		await _capture(id+"_action",{"focus":"","play_kind":id,"play_phase":"action"})
		var deadline: int = Time.get_ticks_msec()+12000
		while not (m.g.get("lagoon_play_anim",{}) as Dictionary).is_empty() and Time.get_ticks_msec()<deadline:
			await process_frame
		_check("ordinary action naturally settled "+id,(m.g.get("lagoon_play_anim",{}) as Dictionary).is_empty())
		await _capture(id+"_settled",{"focus":"","play_kind":""})
	await _place(4905.0)
	promenade.cancel_navigation()
	await _capture("castle_idle",{"focus":""})
	var gate: Dictionary = _target("castle_gate")
	var gate_node: Node2D = gate.get("node") as Node2D
	await _tap(promenade.screen_from_master(gate_node.position))
	await _capture("castle_focus",{"focus":"castle_gate","action_label":"ENTER"})
	await _tap(Vector2(aspect_size.x*0.25,690))
	await _capture("castle_ground_cancel",{"focus":"","action_label":"JUMP"})

func _run() -> void:
	run_case=OS.get_environment("LIVE6P_CASE")
	capture_root=OS.get_environment("LIVE6P_OUT")
	var aspect := OS.get_environment("LIVE6P_ASPECT").split("x")
	if aspect.size()!=2 or run_case not in ["post_day","post_night","dayone_day","dayone_night"] or capture_root.is_empty():
		quit(1)
		return
	want_night=run_case.ends_with("night")
	want_dayone=run_case.begins_with("dayone")
	aspect_size=Vector2i(int(aspect[0]),int(aspect[1]))
	if aspect_size not in [Vector2i(1280,720),Vector2i(1600,720)] or not _exact_engine() or DisplayServer.get_name()=="headless" or RenderingServer.get_current_rendering_method()!="mobile" or DirAccess.dir_exists_absolute(capture_root):
		quit(1)
		return
	DirAccess.make_dir_recursive_absolute(capture_root)
	isolated_save=capture_root.get_base_dir().path_join("profiles").path_join(capture_root.get_file()).path_join("reef_save.json")
	DirAccess.make_dir_recursive_absolute(isolated_save.get_base_dir())
	_check("fresh profile",not FileAccess.file_exists(isolated_save))
	normal_save_before=_normal_save_fingerprints()
	capture_source_signature=_source_signature()
	var scene: PackedScene = load("res://scenes/main.tscn") as PackedScene
	capture_main=scene.instantiate() as ReefMain
	capture_main._save_state=SaveState.new(capture_main,isolated_save)
	root.add_child(capture_main)
	capture_main._apply_quality("speedy")
	await _frames(6)
	_check("exact native viewport",await _set_aspect(aspect_size))
	var m: ReefMain = capture_main
	m._start_menu_ref()._dismiss_menu()
	await _frames(3)
	m._day_one_cancel_story_clips()
	m.intro_active=false
	if not want_dayone:
		m.day_one_giant_dust_bunny_boss_defeated=true
		m._chapter_two_ref().restore_state({"day_one_giant_dust_bunny_boss_defeated":true,"chapter2_party_piece_mask":ChapterTwoPartyPlan.ALL_PARTY_MASK,"chapter2_ember_king_crashed":true,"chapter2_party_started":true,"chapter2_lawn_started":false})
	m._day_one_ref().restore_state({"day_one_active":want_dayone,"day_one_giant_dust_bunny_boss_defeated":not want_dayone,"day_one_arrival_plane_media_seen":true})
	await _saved_reentry(false)
	await _run_matrix()
	paused=false
	capture_main.queue_free()
	capture_main=null
	await _frames(8)
	var normal_after := _normal_save_fingerprints()
	var source_after := _source_signature()
	_check("normal saves unchanged",normal_save_before==normal_after)
	_check("measured source list unchanged",capture_source_signature["sha256"]==source_after["sha256"])
	var actual_ids: Array[String] = []
	for row: Dictionary in states:
		actual_ids.append(String(row["id"]))
	_check("exact ordered matrix",actual_ids==EXPECTED_IDS)
	var manifest := {"schema":"reef.flat_vector.promenade.v1","source_revision":OS.get_environment("GITHUB_SHA"),"run_case":run_case,"engine":_engine_contract(),"renderer":RenderingServer.get_current_rendering_method(),"display_server":DisplayServer.get_name(),"quality":"speedy","aspect":[aspect_size.x,aspect_size.y],"harness_sha256":FileAccess.get_sha256(get_script().resource_path),"source_signature":capture_source_signature,"source_unchanged":capture_source_signature["sha256"]==source_after["sha256"],"save_isolation":{"before":normal_save_before,"after":normal_after,"unchanged":normal_save_before==normal_after,"fresh_fixture_save":isolated_save,"normal_save_file":ProjectSettings.globalize_path("user://reef_save.json")},"setup_trace":setup_trace,"checks":checks,"expected_ids":EXPECTED_IDS,"states":states,"failures":failures,"result":"PASS" if failures==0 else "FAIL","scope":"Diagnostic current promenade source-native context only. Programmatic normalized saved checkpoints and camera route positions;actual raw focus/cancel/play,source-owned pause and natural plane departure/ride settle. Normal HUD preserved. No QA11 independent active closure,complete animation/contact,device/child/owner acceptance."}
	var out := FileAccess.open(capture_root.path_join("capture_manifest.json"),FileAccess.WRITE)
	out.store_string(JSON.stringify(manifest,"\t",true)+"\n")
	out.close()
	print("LIVE6|RESULT|%s|states=%d" %[manifest["result"],states.size()])
	quit(0 if failures==0 else 1)
