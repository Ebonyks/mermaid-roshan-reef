extends SceneTree
## R6 additive current party props diagnostic extension; original sources and normal saves preserved.
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

const EXPECTED_IDS: Array[String] = ["main_hall_before_ballet", "main_hall_after_ballet", "main_hall_ready", "cake_native_00", "cake_native_01", "cake_native_03", "cake_native_07", "cake_native_0f", "cake_native_1f", "cake_native_3f", "cake_native_7f", "cake_fault_00", "cake_fault_01", "cake_fault_03", "cake_fault_07", "cake_fault_0f", "cake_fault_1f", "cake_fault_3f", "cake_fault_7f", "candle_native_unlit", "candle_native_lit", "candle_fault_unlit", "candle_fault_lit", "table_restored", "lawn_ready", "lawn_pause_resumed", "main_hall_returned"]
var failures: int = 0
var capture_root := ""
var aspect_size := Vector2i.ZERO
var run_case := "party_props"
var capture_main: ReefMain
var isolated_save := ""
var states: Array[Dictionary] = []
var checks: Array[Dictionary] = []
var capture_source_signature: Dictionary = {}
var normal_save_before: Dictionary = {}
var fixture_method := "NORMALIZED_SAVED_CHECKPOINT"
var fixture_mask: int = -1
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
		"algorithm": "sha256_runtime_roots_party_props_v1",
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



func _sprite_record(sprite: Sprite2D) -> Dictionary:
	if sprite == null or not is_instance_valid(sprite):
		return {"exists":false}
	return {"exists":true,"path":String(capture_main.get_path_to(sprite)),"visible":sprite.visible,"visible_in_tree":sprite.is_visible_in_tree(),"texture":sprite.texture.resource_path if sprite.texture != null else "","position":sprite.position,"scale":sprite.scale}

func _cake_record(cake: ChapterTwoGiantCake2D) -> Dictionary:
	if cake == null or not is_instance_valid(cake):
		return {"exists":false}
	var ingredient_rows: Array[Dictionary] = []
	for berry: Sprite2D in cake.ingredient_strawberry_sprites:
		ingredient_rows.append(_sprite_record(berry))
	var has_art: bool = cake._has_visible_stage_art()
	var guard := "VECTOR_PROP_FALLBACK"
	if not cake.has_visual_progress():
		guard="NO_PROGRESS"
	elif cake.kitchen_display_layout and (has_art or (cake.cake_piece_mask == 0 and cake.farmer_strawberries_visible)):
		guard="KITCHEN_ART_SUPPRESSED_DRAW"
	elif has_art:
		guard="SHADOW_ONLY"
	return {"exists":true,"path":String(capture_main.get_path_to(cake)),"visible":cake.is_visible_in_tree(),"state":cake.persistent_state(),"stage_id":cake.stage_id(),"phase":cake.visual_phase_id(),"draw_guard":guard,"stage":_sprite_record(cake.stage_art_sprite),"final":_sprite_record(cake.final_cake_sprite),"tray":_sprite_record(cake.candied_tray_sprite),"ingredients":ingredient_rows,"festive":cake.festive,"kitchen_layout":cake.kitchen_display_layout}

func _candle_record(candle: ChapterTwoRainbowCandle2D) -> Dictionary:
	if candle == null or not is_instance_valid(candle):
		return {"exists":false}
	return {"exists":true,"path":String(capture_main.get_path_to(candle)),"visible":candle.is_visible_in_tree(),"lit":candle.lit,"elapsed":candle.elapsed,"draw_guard":"PAINTED_SPRITES_SUPPRESS_VECTOR" if candle.unlit_sprite != null and candle.lit_sprite != null else "VECTOR_CANDLE_FALLBACK","unlit":_sprite_record(candle.unlit_sprite),"lit_sprite":_sprite_record(candle.lit_sprite)}

func _snapshot() -> Dictionary:
	var m: ReefMain = capture_main
	var canvas: Array[Dictionary] = []
	_collect_visible(m,canvas)
	var table: ChapterTwoPartyTable2D = null
	if is_instance_valid(m._chapter_two_room_plot):
		table=m._chapter_two_room_plot.party_table
	var table_row := {"exists":is_instance_valid(table)}
	if is_instance_valid(table):
		table_row.merge({"cake":_cake_record(table.giant_cake),"candle":_candle_record(table.party_candle),"scout_exists":table.ember_scout_actor != null,"king_exists":table.ember_king_actor != null,"prince_exists":table.ember_son_actor != null,"north_arrow_exists":table.north_star_clue != null})
	var hats: Array[Dictionary] = []
	if is_instance_valid(m.chapter2_lawn_view):
		for hat: Node in m.chapter2_lawn_view.find_children("*","Polygon2D",true,false):
			var poly: Polygon2D = hat as Polygon2D
			var lines: Array[Dictionary] = []
			for child: Node in poly.get_children():
				if child is Line2D:
					var line: Line2D = child as Line2D
					lines.append({"points":line.points,"width":line.width,"color":line.default_color})
			hats.append({"path":String(m.get_path_to(poly)),"points":poly.polygon,"color":poly.color,"position":poly.position,"scale":poly.scale,"visible":poly.is_visible_in_tree(),"lines":lines})
	return {"fixture_method":fixture_method,"fixture_cake_mask":fixture_mask,"game":m.game,"phase":String(m.g.get("phase","")),"room":m.castle_room_id,"chapter_active":m.chapter2_is_active(),"party_mask":m.chapter2_party_piece_mask,"story_cake_mask":m.chapter2_cake_piece_mask,"candle_lit":m.chapter2_candle_lit,"candle_taken":m.chapter2_candle_taken,"party_started":m.chapter2_party_started,"lawn_beat":m.chapter2_lawn_beat,"table":table_row,"hats":hats,"lawn_exists":is_instance_valid(m.chapter2_lawn_view),"hud_visible":m.hud_layer.visible if m.hud_layer != null else false,"tree_paused":paused,"source_normal_navigation":m.game == "chapter2_lawn" and m.chapter2_lawn_view.uses_global_navigation(),"visible_canvas":canvas}

func _capture(id: String, expected: Dictionary) -> void:
	await _frames(4)
	await RenderingServer.frame_post_draw
	var actual := _snapshot()
	var valid := true
	for key: String in expected:
		valid=valid and actual.get(key)==expected[key]
	var image: Image = root.get_texture().get_image()
	valid=valid and image.get_size()==aspect_size
	var path := capture_root.path_join(id+".png")
	var fresh_path := not FileAccess.file_exists(path)
	var save_result := image.save_png(path)
	valid=valid and fresh_path and save_result==OK
	var file := FileAccess.open(path,FileAccess.READ)
	states.append({"id":id,"sequence":states.size(),"expected":expected,"actual":actual,"status":"PASS" if valid else "FAIL","image":{"file":id+".png","width":image.get_width(),"height":image.get_height(),"bytes":file.get_length(),"sha256":FileAccess.get_sha256(path)}})
	_check("native state/image "+id,valid)

func _checkpoint(mask: int) -> void:
	var m: ReefMain = capture_main
	m._day_one_ref().restore_state({"day_one_active":false,"day_one_completed_rooms":DayOneDirector.ROOM_ORDER.duplicate(),"day_one_giant_dust_bunny_boss_triggered":true,"day_one_giant_dust_bunny_boss_defeated":true,"day_one_arrival_plane_media_seen":true})
	m._chapter_two_ref().restore_state({"day_one_giant_dust_bunny_boss_defeated":true,"chapter2_active":true,"chapter2_party_piece_mask":mask,"chapter2_lawn_started":false,"chapter2_party_started":false,"chapter2_ember_king_crashed":false})
	m._write_save()
	m._save_state.load_save()
	m._chapter_two_sync_room_plot()
	await _frames(5)
	_check("normalized story checkpoint",m.chapter2_is_active() and m.chapter2_party_piece_mask==mask,"boss=%s active=%s mask=%d" % [m.day_one_giant_dust_bunny_boss_defeated,m.chapter2_is_active(),m.chapter2_party_piece_mask])

func _fault_cake(cake: ChapterTwoGiantCake2D) -> void:
	for sprite: Sprite2D in [cake.stage_art_sprite,cake.final_cake_sprite,cake.candied_tray_sprite]:
		if sprite != null:
			sprite.texture=null
			sprite.visible=false
	for sprite: Sprite2D in cake.ingredient_strawberry_sprites:
		sprite.queue_free()
	cake.ingredient_strawberry_sprites.clear()
	cake.queue_redraw()

func _fault_candle(candle: ChapterTwoRainbowCandle2D) -> void:
	if candle.unlit_sprite != null:
		candle.unlit_sprite.queue_free()
	if candle.lit_sprite != null:
		candle.lit_sprite.queue_free()
	candle.unlit_sprite=null
	candle.lit_sprite=null
	candle.set_lit(candle.lit)

func _matrix() -> void:
	var m: ReefMain = capture_main
	await _checkpoint(0x449)
	await _capture("main_hall_before_ballet",{"game":"level2","chapter_active":true})
	_check("normal table absent before Ballet",not is_instance_valid(m._chapter_two_room_plot.party_table))
	await _checkpoint(0x44D)
	await _capture("main_hall_after_ballet",{"game":"level2","chapter_active":true})
	_check("normal table appears after Ballet",is_instance_valid(m._chapter_two_room_plot.party_table))
	await _checkpoint(ChapterTwoPartyPlan.ALL_PARTY_MASK)
	await _capture("main_hall_ready",{"game":"level2","candle_lit":false})
	for fault: bool in [false,true]:
		for mask: int in [0,1,3,7,15,31,63,127]:
			m._chapter_two_sync_room_plot()
			await _frames(2)
			var table: ChapterTwoPartyTable2D = m._chapter_two_room_plot.party_table
			table.party_candle.hide()
			table.giant_cake.apply_milestone_masks(31,mask)
			table.giant_cake.show()
			fixture_mask=mask
			fixture_method="SOURCE_PROP_API_MILESTONE_WITH_PERSISTENT_READY_CHECKPOINT"
			if fault:
				fixture_method="SOURCE_PROP_API_AND_DECLARED_IN_MEMORY_RESOURCE_FAILURE"
				_fault_cake(table.giant_cake)
			await _capture(("cake_fault_" if fault else "cake_native_")+"%02x" % mask,{"game":"level2","story_cake_mask":127})
	for fault: bool in [false,true]:
		for lit: bool in [false,true]:
			m._chapter_two_sync_room_plot()
			await _frames(2)
			var table: ChapterTwoPartyTable2D = m._chapter_two_room_plot.party_table
			table.party_candle.show()
			table.party_candle.set_lit(lit)
			fixture_mask=-1
			fixture_method="SOURCE_CANDLE_STATE_API_WITH_PERSISTENT_UNLIT_CHECKPOINT"
			if fault:
				fixture_method="SOURCE_CANDLE_API_AND_DECLARED_IN_MEMORY_RESOURCE_FAILURE"
				_fault_candle(table.party_candle)
			await _capture(("candle_fault_" if fault else "candle_native_")+("lit" if lit else "unlit"),{"game":"level2","candle_lit":false})
	fixture_method="NORMALIZED_SAVED_CHECKPOINT"
	await _checkpoint(ChapterTwoPartyPlan.ALL_PARTY_MASK)
	await _capture("table_restored",{"game":"level2"})
	FashionDesigner.refresh_unlocks(m)
	_check("explicit saved dress fixture equipped",FashionDesigner.equip(m,"roshan",FashionDesigner.PARTY_DRESS,true))
	m.chapter2_party_dress_done=true
	m._write_save()
	m._save_state.load_save()
	_check("party dress survives real isolated reload",FashionDesigner.party_dressed(m))
	var table_touch: Control = m._chapter_two_room_plot.party_touch_surface
	_check("normal table hotspot exists",is_instance_valid(table_touch))
	if is_instance_valid(table_touch):
		var point := table_touch.get_global_rect().get_center()
		_mouse_point(point,true)
		await _frames(2)
		_mouse_point(point,false)
	await _frames(8)
	fixture_method="RAW_TABLE_HOTSPOT_FROM_NORMALIZED_READY_DRESS_CHECKPOINT"
	await _capture("lawn_ready",{"game":"chapter2_lawn","lawn_beat":0})
	_check("all eleven hat instances present",(_snapshot()["hats"] as Array).size()==11)
	m.toggle_pause()
	await _frames(2)
	m.toggle_pause()
	await _frames(3)
	await _capture("lawn_pause_resumed",{"game":"chapter2_lawn","tree_paused":false})
	m._end_chapter2_lawn()
	await _frames(18)
	fixture_method="SOURCE_OWNER_EXIT_TO_MAIN_HALL"
	await _capture("main_hall_returned",{"game":"level2","room":"main_hall"})

func _run() -> void:
	capture_root=OS.get_environment("LIVE6PP_OUT")
	var aspect := OS.get_environment("LIVE6PP_ASPECT").split("x")
	if aspect.size()!=2 or capture_root.is_empty():
		quit(1)
		return
	aspect_size=Vector2i(int(aspect[0]),int(aspect[1]))
	if aspect_size not in [Vector2i(1280,720),Vector2i(1600,720)] or not _exact_engine() or DisplayServer.get_name()=="headless" or RenderingServer.get_current_rendering_method()!="mobile" or DirAccess.dir_exists_absolute(capture_root):
		quit(1)
		return
	DirAccess.make_dir_recursive_absolute(capture_root)
	isolated_save=capture_root.get_base_dir().path_join("profiles").path_join(capture_root.get_file()).path_join("reef_save.json")
	DirAccess.make_dir_recursive_absolute(isolated_save.get_base_dir())
	normal_save_before=_normal_save_fingerprints()
	capture_source_signature=_source_signature()
	_check("fresh isolated profile",not FileAccess.file_exists(isolated_save))
	var scene: PackedScene = load("res://scenes/main.tscn") as PackedScene
	capture_main=scene.instantiate() as ReefMain
	capture_main._save_state=SaveState.new(capture_main,isolated_save)
	root.add_child(capture_main)
	capture_main._apply_quality("speedy")
	await _frames(6)
	_check("native aspect",await _set_aspect(aspect_size))
	var m: ReefMain = capture_main
	m._start_menu_ref()._dismiss_menu()
	await _frames(3)
	m._day_one_cancel_story_clips()
	m.day_one_active=false
	m.chapter2_active=false
	m._enter_level2_now(true,false,false)
	await _frames(18)
	await _checkpoint(0x449)
	m._enter_castle_interior_now(false)
	await _frames(24)
	m._castle_rooms_ref().show_room("main_hall",false)
	await _frames(18)
	await _matrix()
	paused=false
	capture_main.queue_free()
	capture_main=null
	await _frames(8)
	var normal_after := _normal_save_fingerprints()
	var source_after := _source_signature()
	_check("normal saves unchanged",normal_save_before==normal_after)
	_check("measured sources unchanged",capture_source_signature==source_after)
	var ids: Array[String] = []
	for r: Dictionary in states:
		ids.append(String(r["id"]))
	_check("ordered matrix complete",ids==EXPECTED_IDS)
	var manifest := {"schema":"reef.flat_vector.party_props.v1","source_revision":OS.get_environment("GITHUB_SHA"),"run_case":run_case,"engine":_engine_contract(),"renderer":RenderingServer.get_current_rendering_method(),"display_server":DisplayServer.get_name(),"quality":"speedy","aspect":[aspect_size.x,aspect_size.y],"harness_sha256":FileAccess.get_sha256(get_script().resource_path),"source_signature":capture_source_signature,"source_unchanged":capture_source_signature==source_after,"save_isolation":{"before":normal_save_before,"after":normal_after,"unchanged":normal_save_before==normal_after,"fresh_fixture_save":isolated_save,"normal_save_file":ProjectSettings.globalize_path("user://reef_save.json")},"checks":checks,"expected_ids":EXPECTED_IDS,"states":states,"failures":failures,"result":"PASS" if failures==0 else "FAIL","scope":"Diagnostic normalized saved MainHall table route and source-owner raw entry/exit to lawn ready;private in-memory resource faults and component milestone/lit API fixtures are explicitly NOT natural gameplay/saved progression. All originals unchanged. No full motion/contact/device/child/owner or independentQA11 acceptance."}
	var out := FileAccess.open(capture_root.path_join("capture_manifest.json"),FileAccess.WRITE)
	out.store_string(JSON.stringify(manifest,"\t",true)+"\n")
	out.close()
	print("LIVE6|RESULT|%s|states=%d" %[manifest["result"],states.size()])
	quit(0 if failures==0 else 1)
