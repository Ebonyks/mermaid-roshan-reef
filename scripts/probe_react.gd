extends SceneTree
# S1 probe (SATCHEL_WORKORDER_2026-07-25): the reactive-prop layer registers
# small props, drifts them, answers a bump with a squash — and awards nothing.
# The last point is the important one: this whole layer is cosmetic, so it must
# be invisible to progression. CarrySystem's four props must stay OUT of the
# registry or a held starfish would chime in Roshan's hands forever.

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
	await _settle(30)
	await _registry_case()
	await _bump_case()
	await _no_reward_case()
	await _release_case()
	print("REACT|result: ", "ALL OK" if bad == 0 else "%d check(s) FAILED" % bad)
	quit()

func _ck(label: String, ok: bool) -> void:
	print("REACT|", label, ": ", "OK" if ok else "FAIL")
	if not ok:
		bad += 1

func _settle(frames: int) -> void:
	for i in range(frames):
		await process_frame

func _wait_ms(ms: int) -> void:
	var t_end: int = Time.get_ticks_msec() + ms
	while Time.get_ticks_msec() < t_end:
		await process_frame

func _registry_case() -> void:
	_ck("registry populated by the reef build", main.reactive_props.size() > 0)
	# only whitelisted kinds ever get in
	var kinds_ok := true
	for it in main.reactive_props:
		var d: Dictionary = it
		if not (String(d["kind"]) in ["sway", "bob"]):
			kinds_ok = false
	_ck("every entry is a known kind", kinds_ok)
	# CarrySystem's two stars and two shells were handed back out
	var carry: CarrySystem = main._carry_ref()
	var owned: Array = []
	for s in carry.stars:
		var sd: Dictionary = s
		owned.append(sd["node"])
	for sh in carry.shells:
		var hd: Dictionary = sh
		owned.append(hd["node"])
	var leaked := false
	for it2 in main.reactive_props:
		var d2: Dictionary = it2
		if d2["wrap"] in owned:
			leaked = true
	_ck("carry props excluded from the registry", owned.size() == 4 and not leaked)

func _bump_case() -> void:
	var target: Dictionary = _first_entry()
	if target.is_empty():
		_ck("a prop was available to bump", false)
		return
	var wrap: Node3D = target["wrap"]
	var inst: Node3D = target["inst"]
	var rest: Vector3 = target["scale"]
	var wrap0: Vector3 = wrap.position
	# park Roshan inside the prop's bump radius and let one rebuild+tick land
	main.player.position = wrap.position
	main.player.vel = Vector3.ZERO
	main._react_ref()._near_t = 0.0
	await _settle(4)
	_ck("bump started a reaction", float(target["react"]) > 0.0)
	_ck("bump armed the per-prop cooldown", float(target["cool"]) > 0.0)
	_ck("the squash scaled the inner mesh", inst.scale != rest)
	_ck("the wrap transform was left alone for CarrySystem/Satchel",
		wrap.position == wrap0)
	# and it decays back to the authored rest pose on its own. REACT_TIME is in
	# seconds, and headless frames are far faster than wall-clock, so this waits
	# on the clock rather than on a frame count (the probe_carry pattern).
	await _wait_ms(900)
	_ck("reaction decays to rest", float(target["react"]) == 0.0 and inst.scale == rest)

func _no_reward_case() -> void:
	# swim through a crowd of props: nothing may be earned, won or unlocked
	var pearls0: int = int(main.pearl_count)
	var medals0: int = main.medals.size()
	var won0: int = main.save_data.get("won", {}).size()
	var n := 0
	for it in main.reactive_props:
		var d: Dictionary = it
		var w: Node3D = d["wrap"]
		if not is_instance_valid(w):
			continue
		main.player.position = w.position
		main._react_ref()._near_t = 0.0
		await process_frame
		n += 1
		if n >= 25:
			break
	_ck("bumped a crowd of props", n > 0)
	_ck("no pearls awarded by reactions", int(main.pearl_count) == pearls0)
	_ck("no medals awarded by reactions", main.medals.size() == medals0)
	_ck("no game marked won by reactions", main.save_data.get("won", {}).size() == won0)

func _release_case() -> void:
	var target: Dictionary = _first_entry()
	if target.is_empty():
		_ck("a prop was available to release", false)
		return
	var wrap: Node3D = target["wrap"]
	var inst: Node3D = target["inst"]
	var base: Vector3 = target["base"]
	var rest: Vector3 = target["scale"]
	var before: int = main.reactive_props.size()
	main._react_ref().release(wrap)
	_ck("release drops exactly one entry", main.reactive_props.size() == before - 1)
	_ck("release restores the authored rest pose",
		inst.position == base and inst.scale == rest and inst.rotation == Vector3.ZERO)
	# a released prop must stay still even while Roshan sits on top of it
	main.player.position = wrap.position
	main._react_ref()._near_t = 0.0
	await _settle(10)
	_ck("released prop no longer animates",
		inst.position == base and inst.scale == rest)

func _first_entry() -> Dictionary:
	for it in main.reactive_props:
		var d: Dictionary = it
		if is_instance_valid(d["wrap"]) and is_instance_valid(d["inst"]):
			return d
	return {}
