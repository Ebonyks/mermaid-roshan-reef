extends SceneTree
# Arm calibration probe: freezes the player in open ground and steps through
# raw arm angles + the actual toy poses, shooting front/side/back per pose.
# Isolates left/right arm mapping from toy occlusion. Dev-only.

const OUT := "C:/Users/Peter/AppData/Local/Temp/claude/C--Users-Peter-Documents-Claude-Projects-Book-layout-ocean-game/22c09d23-46ce-44d9-974a-d6891729ae81/scratchpad/armcal"

var main: Node
var cam: Camera3D
var pl: Node3D

func _shot(cpos: Vector3, look: Vector3, fname: String) -> void:
	cam.position = cpos
	cam.look_at(look)
	await process_frame
	await RenderingServer.frame_post_draw
	var img: Image = get_root().get_viewport().get_texture().get_image()
	img.save_png(OUT + "/" + fname)

func _pose_shots(label: String) -> void:
	var pp: Vector3 = pl.position
	var fc := Vector3(0, 0, -1)   # yaw locked to 0, model faces -Z
	var sd := Vector3(1, 0, 0)
	await _shot(pp + fc * 5.0 + Vector3(0, 1.6, 0), pp + Vector3(0, 1.2, 0), "c_%s_front.png" % label)
	await _shot(pp + sd * 5.0 + Vector3(0, 1.6, 0), pp + Vector3(0, 1.2, 0), "c_%s_right.png" % label)
	await _shot(pp - sd * 5.0 + Vector3(0, 1.6, 0), pp + Vector3(0, 1.2, 0), "c_%s_left.png" % label)
	print("  pose: " + label)

func _init() -> void:
	DirAccess.make_dir_recursive_absolute(OUT)
	var ms: PackedScene = load("res://scenes/main.tscn")
	main = ms.instantiate()
	get_root().add_child(main)
	await process_frame
	if main.has_method("_skip_intro"):
		main._skip_intro()
	await process_frame
	main.pearl_count = main.PEARL_TOTAL
	for f in main.friends:
		f["found"] = true
		f["won"] = true
	main.trophies = 5
	main._enter_level2()
	for i in range(10):
		await process_frame
	pl = main.player
	# freeze every other bone writer: no swim, no physics, no toy tick
	pl.set_process(false)
	pl.set_physics_process(false)
	# open ground in front of the sandbox
	var toys: Array = main.g.get("toys", [])
	for td in toys:
		if String(td["kind"]) == "sandbox":
			pl.position = (td["anchor"] as Vector3) + (td["fwd"] as Vector3) * 8.0 + Vector3(0, 1.2, 0)
			break
	pl.rotation = Vector3.ZERO
	pl.set("vel", Vector3.ZERO)
	cam = Camera3D.new()
	cam.fov = 45.0
	get_root().add_child(cam)
	cam.make_current()
	print("=== ARM CALIB ===")
	# raw symmetry: identical angle on both upper arms, no bend
	for amt: float in [0.65, 1.1, 1.5, 2.3]:
		pl._rot_bone("armU", Vector3.RIGHT, amt)
		pl._rot_bone("armU2", Vector3.RIGHT, amt)
		pl._rot_bone("armF", Vector3.RIGHT, 0.0)
		pl._rot_bone("armF2", Vector3.RIGHT, 0.0)
		await _pose_shots("sym%d" % int(amt * 100))
	# forearm bend on top of a mid raise: is the bend direction right?
	pl._rot_bone("armU", Vector3.RIGHT, 1.1)
	pl._rot_bone("armU2", Vector3.RIGHT, 1.1)
	pl._rot_bone("armF", Vector3.RIGHT, 0.55)
	pl._rot_bone("armF2", Vector3.RIGHT, 0.55)
	await _pose_shots("bend55")
	pl._rot_bone("armF", Vector3.RIGHT, -0.55)
	pl._rot_bone("armF2", Vector3.RIGHT, -0.55)
	await _pose_shots("bendneg55")
	# the actual toy poses, exactly as the choreography drives them
	pl.toy_pose("seat", 1.0, 0.5)
	await _pose_shots("seat")
	pl.toy_pose("swing", 1.0, 0.4)
	await _pose_shots("swing")
	pl.toy_pose("ride", 1.0, 1.0)
	await _pose_shots("wheee")
	pl.toy_pose("dig", 1.0, PI * 0.5)
	await _pose_shots("digL")
	pl.toy_pose("dig", 1.0, -PI * 0.5)
	await _pose_shots("digR")
	print("=== DONE ===")
	quit()
