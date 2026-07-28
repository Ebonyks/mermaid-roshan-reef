class_name TreasureGame
extends RefCounted
# Secret Cave route builder. The no-fail checkpoint logic still lives in the
# shared course tick; this file now supplies only authored 2D runtime art.

const BACKGROUND := "res://assets/minigames/treasure/background.png"
const CHEST_SPRITE := "res://assets/minigames/treasure/chest.png"
const CHECKPOINT_SPRITE := "res://assets/minigames/treasure/checkpoint.svg"
const ROSHAN_EXPLORE := "res://assets/minigames/shared/roshan_catch.png"

var m: ReefMain

func _init(main: ReefMain) -> void:
	m = main

func build(fr: Dictionary, origin: Vector3) -> void:
	m.g["timer"] = -1.0
	m.g["checks"] = []
	m.g["chains"] = []
	m.player.set_skin("__minigame_2d", ROSHAN_EXPLORE)
	var gy: float = m.ARENA_POS.y
	var route: Array[Vector3] = [
		Vector3(origin.x, gy + 8.0, origin.z + 14.0),
		Vector3(origin.x - 10.0, gy + 6.0, origin.z + 4.0),
		Vector3(origin.x - 6.0, gy + 4.2, origin.z - 8.0),
		Vector3(origin.x + 6.0, gy + 3.4, origin.z - 12.0),
		Vector3(origin.x + 12.0, gy + 3.0, origin.z - 2.0),
	]
	_add_cavern_plate(origin, gy)
	for i in range(route.size()):
		var kind: String = "chest" if i == route.size() - 1 else "way"
		var checkpoint := _standee(CHECKPOINT_SPRITE, 2.4, route[i])
		(m.g["checks"] as Array).append({"node": checkpoint, "hit": false, "kind": kind})
	var chest := _standee(CHEST_SPRITE, 6.8,
		route[route.size() - 1] + Vector3(0, -3.0, 0))
	m.g["treasure_chest"] = chest
	m.show_msg(fr["fname"], "Shhh... secret caverns! Follow the sparkles down to the treasure!")

func _add_cavern_plate(origin: Vector3, ground_y: float) -> void:
	var plate := Sprite3D.new()
	plate.texture = load(BACKGROUND)
	plate.pixel_size = 1.0 / maxf(1.0, float(plate.texture.get_height()))
	plate.rotation_degrees.x = -90.0
	plate.position = Vector3(origin.x, ground_y + 0.12, origin.z)
	var base_width: float = float(plate.texture.get_width()) * plate.pixel_size
	plate.scale = Vector3(50.0 / base_width, 30.0, 1.0)
	plate.billboard = BaseMaterial3D.BILLBOARD_DISABLED
	plate.shaded = false
	plate.alpha_cut = SpriteBase3D.ALPHA_CUT_DISABLED
	m.add_child(plate)
	m.game_nodes.append(plate)

func _standee(path: String, height: float, pos: Vector3) -> Node3D:
	var holder := Node3D.new()
	holder.position = pos
	m.add_child(holder)
	m.game_nodes.append(holder)
	var sprite := Sprite3D.new()
	sprite.texture = load(path)
	sprite.pixel_size = height / maxf(1.0, float(sprite.texture.get_height()))
	sprite.position.y = height * 0.5
	sprite.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	sprite.shaded = false
	sprite.alpha_cut = SpriteBase3D.ALPHA_CUT_DISCARD
	holder.add_child(sprite)
	return holder
