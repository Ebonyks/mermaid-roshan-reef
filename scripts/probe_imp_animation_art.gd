extends SceneTree
## Mobile-render review harness for authored imp combat-state sprites.
##
## Examples:
##   IMP_ANIM_CAPTURE_FAMILY=imp_mischief
##   IMP_ANIM_CAPTURE_STATES=windup,charge,slash
##   IMP_ANIM_SHOT_OUT=<absolute directory>
##
## Headless runs still verify that every requested state loads as a 512x512
## texture. Windowed Mobile runs additionally capture the poses through the
## real OperaCareerWorld2D loader and _apply_imp_pose() path.

const DEFAULT_STATES: Array[String] = [
	"windup", "charge", "slash", "recover", "guard", "stagger", "flee",
	"taunt", "hop_a", "hop_b", "bopped", "bow",
]

const BASE_DELIVERY_STATES: Array[String] = [
	"windup", "charge", "slash", "recover", "guard", "stagger", "flee", "taunt",
]
const CAPTAIN_EXTRA_STATES: Array[String] = ["bow"]

const BASE_FAMILIES := ["imp_mischief", "imp_captain"]
const COSTUME_FAMILIES := [
	"rival_chef", "rival_detective", "rival_ballerina", "rival_candymaker",
	"rival_doctor", "rival_farmer", "rival_boxer", "rival_magician",
	"rival_painter", "rival_astronaut", "rival_racer", "rival_popstar",
]
const FX_SPECS := {
	"fx_telegraph_ring": Vector2i(512, 512),
	"fx_telegraph_bang": Vector2i(128, 256),
	"fx_slash_arc": Vector2i(512, 256),
	"fx_dust_puff": Vector2i(256, 256),
	"fx_stolen_sparkle": Vector2i(128, 128),
	"fx_dizzy_stars": Vector2i(256, 256),
}

var bad := 0
var main: ReefMain
var act: OperaAct
var world: OperaCareerWorld2D
var out_dir := ""


func _requested_family() -> String:
	var requested := OS.get_environment("IMP_ANIM_CAPTURE_FAMILY").strip_edges()
	return requested if requested != "" else "imp_mischief"


func _requested_states() -> Array[String]:
	var raw := OS.get_environment("IMP_ANIM_CAPTURE_STATES").strip_edges()
	if raw == "":
		return DEFAULT_STATES.duplicate()
	var states: Array[String] = []
	for part: String in raw.split(","):
		var state := part.strip_edges()
		if state != "":
			states.append(state)
	return states


func _check(label: String, condition: bool) -> void:
	if condition:
		print("IMPANIM|OK|", label)
	else:
		bad += 1
		print("IMPANIM|FAIL|", label)


func _texture_path(family: String, state: String) -> String:
	if state == "idle":
		return "res://assets/opera/worlds/actors/%s.png" % family
	return "res://assets/opera/worlds/actors/%s_%s.png" % [family, state]


func _png_dimensions(path: String) -> Vector2i:
	var file: FileAccess = FileAccess.open(path, FileAccess.READ)
	if file == null:
		return Vector2i.ZERO
	file.big_endian = true
	file.seek(16)
	return Vector2i(file.get_32(), file.get_32())


func _verify_files(family: String, states: Array[String]) -> void:
	for state: String in states:
		var path := _texture_path(family, state)
		_check("%s exists" % path, FileAccess.file_exists(path))
		if not FileAccess.file_exists(path):
			continue
		var dimensions := _png_dimensions(path)
		_check("%s loads at 512x512" % path,
			dimensions == Vector2i(512, 512))


func _verify_delivery() -> void:
	for family: String in BASE_FAMILIES:
		_verify_files(family, BASE_DELIVERY_STATES)
	_verify_files("imp_captain", CAPTAIN_EXTRA_STATES)
	var costume_states: Array[String] = ["idle"]
	costume_states.append_array(DEFAULT_STATES)
	for family: String in COSTUME_FAMILIES:
		_verify_files(family, costume_states)
	for slug: String in FX_SPECS:
		var path := "res://assets/opera/worlds/props/%s.png" % slug
		_check("%s exists" % path, FileAccess.file_exists(path))
		if not FileAccess.file_exists(path):
			continue
		var dimensions := _png_dimensions(path)
		var expected: Vector2i = FX_SPECS[slug]
		_check("%s loads at %dx%d" % [path, expected.x, expected.y],
			dimensions == expected)


func _settle(frames: int) -> void:
	for _index in range(frames):
		await process_frame


func _nursery_config() -> Dictionary:
	for source: Dictionary in OperaHouse.ACTS:
		if String(source.get("costume", "")) == "nursery":
			return source.duplicate(true)
	return {}


func _career_config(career: String) -> Dictionary:
	for source: Dictionary in OperaHouse.ACTS:
		if String(source.get("costume", "")) == career:
			return source.duplicate(true)
	return {}


func _build_world(family: String) -> bool:
	var scene := load("res://scenes/main.tscn") as PackedScene
	main = scene.instantiate() as ReefMain
	get_root().add_child(main)
	await _settle(2)
	if main.intro_active:
		main._skip_intro()
	main.game = "opera"
	var config := _nursery_config()
	if family.begins_with("rival_"):
		config = _career_config(family.trim_prefix("rival_"))
	if config.is_empty():
		_check("career configuration exists for %s" % family, false)
		return false
	act = OperaAct.new()
	get_root().add_child(act)
	act.start(main, config, Callable())
	await _settle(8)
	world = act.career_world_2d
	_check("%s opens the Canvas career world" % family, world != null)
	if world == null:
		return false
	act.set_process(false)
	world.set_process(false)
	for imp: Dictionary in world.combat_imps:
		var old_node := imp.get("node") as TextureRect
		if old_node != null:
			old_node.visible = false
	if world.player_actor != null:
		world.player_actor.visible = false
	if world.rival_actor != null:
		world.rival_actor.visible = false
	return true


func _pose_time(state: String) -> float:
	match state:
		"windup": return 0.72
		"charge": return 0.20
		"slash": return 0.14
		"recover": return 0.58
		"guard": return 0.40
		"stagger": return 0.25
		"flee": return 0.55
		"taunt": return 0.42
		_: return 0.25


func _capture_page(family: String, states: Array[String], page: int) -> void:
	var review_nodes: Array[TextureRect] = []
	var page_start := page * 4
	var page_end := mini(states.size(), page_start + 4)
	var positions := [
		Vector2(180.0, 555.0), Vector2(490.0, 555.0),
		Vector2(800.0, 555.0), Vector2(1110.0, 555.0),
	]
	for local_index in range(page_end - page_start):
		var state := states[page_start + local_index]
		var node := TextureRect.new()
		node.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		node.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		node.mouse_filter = Control.MOUSE_FILTER_IGNORE
		node.size = Vector2(150.0, 150.0) if family == "imp_captain" else Vector2(118.0, 118.0)
		world.combat_layer.add_child(node)
		var imp := {
			"node": node,
			"captain": family == "imp_captain",
			"seed": local_index,
			"state_t": _pose_time(state),
		}
		var expected := _texture_path(family, state)
		world._apply_imp_pose(imp, node, positions[local_index], state, 1.0)
		_check("%s resolves through the live state loader" % expected,
			node.texture != null and node.texture.resource_path == expected)
		_check("%s reports exact same-family resolution" % expected,
			String(imp.get("texture_resolution", "")) == "exact"
			and String(imp.get("texture_family", "")) == family
			and String(imp.get("texture_state", "")) == state)
		if state in ["windup", "recover", "guard"]:
			var sole: Vector2 = imp.get("sole", Vector2.ZERO)
			_check("%s keeps its grounded sole registered" % expected,
				absf(sole.y - (positions[local_index].y + 8.0)) <= 3.0)
		review_nodes.append(node)
	await _settle(4)
	await RenderingServer.frame_post_draw
	var image: Image = get_root().get_viewport().get_texture().get_image()
	var target := out_dir.path_join("%s_page_%02d.png" % [family, page + 1])
	var error := image.save_png(target)
	_check("saved %s" % target, error == OK)
	for node: TextureRect in review_nodes:
		node.queue_free()
	await _settle(2)


func _capture_fx(family: String) -> void:
	_check("telegraph ring loaded by the live world", world.fx_telegraph_ring_texture != null)
	_check("telegraph bang loaded by the live world", world.fx_telegraph_bang_texture != null)
	_check("slash arc loaded by the live world", world.fx_slash_arc_texture != null)
	_check("dust puff loaded by the live world", world.fx_dust_puff_texture != null)
	_check("stolen sparkle loaded by the live world", world.fx_stolen_sparkle_texture != null)
	_check("dizzy stars loaded by the live world", world.fx_dizzy_stars_texture != null)
	world.combat_marks = [
		{"kind": "ring", "pos": Vector2(210.0, 540.0), "t": 0.15, "life": 0.9},
		{"kind": "arc", "pos": Vector2(485.0, 520.0), "t": 0.05, "life": 0.3},
		{"kind": "dust", "pos": Vector2(755.0, 520.0), "t": 0.08, "life": 0.4},
		{"kind": "dizzy", "pos": Vector2(1010.0, 545.0), "t": 0.12, "life": 0.62},
	]
	world.combat_imps.append({
		"popped": false,
		"carrying": true,
		"center": Vector2(1160.0, 500.0),
		"seed": 2,
	})
	world.combat_fx.queue_redraw()
	await _settle(4)
	await RenderingServer.frame_post_draw
	var image: Image = get_root().get_viewport().get_texture().get_image()
	var target := out_dir.path_join("%s_fx.png" % family)
	var error := image.save_png(target)
	_check("saved %s" % target, error == OK)


func _init() -> void:
	var family := _requested_family()
	var states := _requested_states()
	if OS.get_environment("IMP_ANIM_CAPTURE_STATES").strip_edges().is_empty():
		var delivered: Array[String] = []
		for state: String in states:
			if FileAccess.file_exists(_texture_path(family, state)):
				delivered.append(state)
		states = delivered
	_verify_delivery()
	if DisplayServer.get_name() == "headless":
		_finish()
		return
	call_deferred("_run_windowed", family, states)


func _run_windowed(family: String, states: Array[String]) -> void:
	var requested_out := OS.get_environment("IMP_ANIM_SHOT_OUT").strip_edges()
	out_dir = requested_out if requested_out != "" \
		else ProjectSettings.globalize_path("res://tmp/imp_animation_shots")
	DirAccess.make_dir_recursive_absolute(out_dir)
	if not await _build_world(family):
		_finish()
		return
	var page_count := ceili(float(states.size()) / 4.0)
	for page in range(page_count):
		await _capture_page(family, states, page)
	await _capture_fx(family)
	_finish()


func _finish() -> void:
	if bad == 0:
		print("IMPANIM|result: ALL OK")
		quit()
	else:
		print("IMPANIM|result: %d FAIL" % bad)
		quit(1)
