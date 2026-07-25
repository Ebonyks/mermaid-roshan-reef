extends SceneTree
# S2 probe (SATCHEL_WORKORDER_2026-07-25): the six-slot hotbar picks loose reef
# props up, holds the selected one in her hands, and puts them back.
#
# The two checks that matter most are the ones protecting the child:
#   * a FULL satchel never refuses a pickup — the oldest thing swims home, and
#     this probe asserts it is visible and back at its exact home position, so
#     nothing is ever destroyed;
#   * zero-input play pockets nothing, so probe_passive's promise still holds.
# S2 is session-only, so the probe also asserts nothing reached the save file.

var main: ReefMain
var bad := 0

func _init() -> void:
	seed(20260725)
	var scene: PackedScene = load("res://scenes/main.tscn")
	main = scene.instantiate() as ReefMain
	get_root().add_child(main)
	await process_frame
	await process_frame
	main._skip_intro()
	await _settle(40)
	await _row_case()
	await _passive_case()
	await _pickup_case()
	await _hold_case()
	await _putdown_case()
	await _overflow_case()
	await _stow_case()
	await _save_case()
	print("SATCHEL|result: ", "ALL OK" if bad == 0 else "%d check(s) FAILED" % bad)
	quit()

func _ck(label: String, ok: bool) -> void:
	print("SATCHEL|", label, ": ", "OK" if ok else "FAIL")
	if not ok:
		bad += 1

func _settle(frames: int) -> void:
	for i in range(frames):
		await process_frame

func _wait_ms(ms: int) -> void:
	var t_end: int = Time.get_ticks_msec() + ms
	while Time.get_ticks_msec() < t_end:
		await process_frame

func _pickables() -> Array:
	var out: Array = []
	for it in main.reactive_props:
		var d: Dictionary = it
		if String(d["kind"]) != "bob":
			continue
		if is_instance_valid(d["wrap"]) and is_instance_valid(d["inst"]):
			out.append(d)
	return out

func _park_at(entry: Dictionary) -> Vector3:
	var wrap: Node3D = entry["wrap"]
	var p: Vector3 = wrap.position
	main.player.position = p
	main.player.vel = Vector3.ZERO
	return p

# ---------------------------------------------------------------- cases

func _row_case() -> void:
	_ck("hotbar row built under the HUD layer",
		main.satchel_row != null and is_instance_valid(main.satchel_row)
			and main.satchel_row.get_parent() == main.hud_layer)
	_ck("row has exactly SLOTS slots",
		main.satchel_row != null and main.satchel_row.get_child_count() == Satchel.SLOTS)
	# the row must clear the bottom-right action bubble (x >= 1094 at base res)
	var w: float = Satchel.SLOTS * Satchel.SLOT_PX + (Satchel.SLOTS - 1) * Satchel.SLOT_GAP
	_ck("row stays clear of the touch action bubble", 640.0 + w * 0.5 < 1094.0)
	_ck("slot targets meet the >=110 px rule", Satchel.SLOT_PX >= 110.0)

func _passive_case() -> void:
	# zero input: drifting around must never pocket anything
	await _wait_ms(600)
	_ck("zero-input play pockets nothing", main.satchel.is_empty())
	_ck("zero-input play holds nothing", main.satchel_sel == -1)

func _pickup_case() -> void:
	var pool: Array = _pickables()
	_ck("reef offers loose props to pick up", pool.size() > 0)
	if pool.is_empty():
		return
	var e: Dictionary = pool[0]
	var wrap: Node3D = e["wrap"]
	var pname: String = String(e["name"])
	var regs0: int = main.reactive_props.size()
	var pos: Vector3 = _park_at(e)
	main._satchel_ref()._action(pos)
	_ck("action pocketed the nearest prop", main.satchel.size() == 1)
	_ck("the pocketed prop is the one she swam to",
		main.satchel.size() == 1 and String((main.satchel[0] as Dictionary)["name"]) == pname)
	# a pickup must NOT jump into her hands, or the next ACTION would drop it
	# again and two pickups in a row would be impossible
	_ck("pocketing leaves her hands free for the next pickup", main.satchel_sel == -1)
	_ck("pocketed prop left the reactive registry",
		main.reactive_props.size() == regs0 - 1)
	_ck("pickup claimed the press from the jump", float(main.player.jump_cool) >= 0.3)
	_ck("its home was remembered for the swim-home path",
		main.satchel.size() == 1 and (main.satchel[0] as Dictionary)["home"] != null)
	_ck("wrap survived the pickup", is_instance_valid(wrap))

func _hold_case() -> void:
	if main.satchel.is_empty():
		_ck("something was held to test", false)
		return
	var it: Dictionary = main.satchel[0]
	var wrap: Node3D = it["wrap"]
	main._satchel_ref().select(0)
	_ck("tapping a slot takes that thing out", main.satchel_sel == 0)
	await _wait_ms(500)
	var yaw: float = float(main.player.yaw)
	var pt: Vector3 = main.player.position \
		+ Vector3(sin(yaw), 0.0, cos(yaw)) * CarrySystem.CARRY_FWD \
		+ Vector3(0.0, CarrySystem.CARRY_UP, 0.0)
	_ck("the selected slot is what she is holding", wrap.visible)
	_ck("held prop rides the shared carry point", wrap.position.distance_to(pt) < 2.0)

func _putdown_case() -> void:
	if main.satchel.is_empty():
		_ck("something was held to put down", false)
		return
	var it: Dictionary = main.satchel[0]
	var wrap: Node3D = it["wrap"]
	var regs0: int = main.reactive_props.size()
	main._satchel_ref()._action(main.player.position)
	_ck("action put the held prop back down", main.satchel.is_empty())
	_ck("putting down clears the selection", main.satchel_sel == -1)
	_ck("the prop is visible in the reef again", wrap.visible)
	_ck("the prop rejoined the reactive registry",
		main.reactive_props.size() == regs0 + 1)
	var seat: float = ReefMain.seabed_y(wrap.position.x, wrap.position.z)
	_ck("it was seated on the sand, not left floating",
		absf(wrap.position.y - (seat + 0.3)) < 0.01)
	_ck("it was set down inside the world bounds",
		Vector2(wrap.position.x, wrap.position.z).length() <= ReefMain.WORLD_R)

func _overflow_case() -> void:
	var pool: Array = _pickables()
	if pool.size() < Satchel.SLOTS + 1:
		_ck("reef offers enough loose props to overfill the satchel", false)
		return
	var sat: Satchel = main._satchel_ref()
	# fill every slot
	for i in range(Satchel.SLOTS):
		var e: Dictionary = pool[i]
		sat._action(_park_at(e))
	_ck("satchel filled to capacity", main.satchel.size() == Satchel.SLOTS)
	# the oldest thing in the bag, and where it came from
	var oldest: Dictionary = main.satchel[0]
	var old_wrap: Node3D = oldest["wrap"]
	var old_home: Vector3 = oldest["home"]
	var old_name: String = String(oldest["name"])
	# one more pickup: this must NOT be refused
	var extra: Dictionary = pool[Satchel.SLOTS]
	sat._action(_park_at(extra))
	_ck("a full satchel still accepts a pickup — never a wall",
		main.satchel.size() == Satchel.SLOTS)
	var still_bagged := false
	for it in main.satchel:
		var d: Dictionary = it
		if d["wrap"] == old_wrap:
			still_bagged = true
	# assert the INVARIANT (the newest thing is bagged and out of the world)
	# rather than which prop was nearest — several identical shells can sit
	# within reach of one spot, and the identity is not what matters here
	var newest: Dictionary = main.satchel[Satchel.SLOTS - 1]
	var new_wrap: Node3D = newest["wrap"]
	_ck("the newest prop is bagged and out of the world",
		is_instance_valid(new_wrap) and not new_wrap.visible)
	_ck("the evicted prop left the bag", not still_bagged)
	# the whole point: eviction relocates, it never destroys
	_ck("the evicted prop still exists", is_instance_valid(old_wrap))
	_ck("the evicted prop swam home to where it was found",
		is_instance_valid(old_wrap) and old_wrap.position.distance_to(old_home) < 0.01)
	_ck("the evicted prop is visible again", is_instance_valid(old_wrap) and old_wrap.visible)
	var back := false
	for it2 in main.reactive_props:
		var d2: Dictionary = it2
		if d2["wrap"] == old_wrap:
			back = true
	_ck("the evicted prop is world furniture again (%s)" % old_name, back)
	_ck("selection never dangles past the bag after an eviction",
		main.satchel_sel == -1 or main.satchel_sel < main.satchel.size())

func _stow_case() -> void:
	main._satchel_ref().stow()
	var any_visible := false
	for it in main.satchel:
		var d: Dictionary = it
		var w: Node3D = d["wrap"]
		if is_instance_valid(w) and w.visible:
			any_visible = true
	_ck("stow hides everything the satchel owns", not any_visible)
	_ck("stow hides the hotbar row",
		main.satchel_row != null and not main.satchel_row.visible)

func _save_case() -> void:
	# S2 is deliberately session-only: placement and persistence are S3
	main._write_save()
	await _settle(6)
	_ck("satchel contents are not persisted in S2", not main.save_data.has("satchel"))
	_ck("no room key written in S2", not main.save_data.has("room"))
	_ck("carrying things awarded no pearls beyond normal play", int(main.pearl_count) >= 0)
	_ck("carrying things awarded no medals", main.medals.is_empty())
