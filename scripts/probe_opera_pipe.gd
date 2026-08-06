extends SceneTree
## Focused gate for the pipe-dream grammar (astronaut PIPES): placement,
## conservation, recovery. Born from the 2026-08-05 release audit, which
## found the tray duplicating a tile on every tap, fueled tiles permanently
## un-liftable (one-move dead ends in rounds 2 and 3), and the help twinkle
## pointing at the napping imp. No other probe places a single tile.

var checks := 0
var failed := 0


func _ck(name: String, ok: bool) -> void:
	checks += 1
	if not ok:
		failed += 1
		print("PIPE|FAIL|%s" % name)


func _tap(surface: OperaGestureSurface, at: Vector2) -> void:
	surface._press(at)
	surface._release(at)


func _drag_place(surface: OperaGestureSurface, slot: int, cell: int) -> void:
	surface._press(surface._pipe_tray_rect(slot).get_center())
	surface._release(surface._pipe_cell_rect(cell).get_center())


func _tile_census(surface: OperaGestureSurface) -> int:
	# every tile in the round, wherever it is: tray + carried + placed loose
	var count := surface.pipe_tray.size()
	if surface.pipe_drag_tile != "":
		count += 1
	for cell in range(surface.PIPE_COLS * surface.PIPE_ROWS):
		if surface.PIPE_MOUTHS.has(String(surface.pipe_grid[cell])) and not surface.pipe_fixed[cell]:
			count += 1
	return count


func _flow(surface: OperaGestureSurface, seconds: float) -> void:
	var t := 0.0
	while t < seconds:
		surface._process(0.1)
		t += 0.1


func _init() -> void:
	var surface := OperaGestureSurface.new()
	surface.size = Vector2(852, 560)
	get_root().add_child(surface)
	surface.configure("pipe", Color.WHITE, 1, "")
	surface.armed_only = false
	surface.set_block_signals(true)

	# ---- round 1: the one-finger path (tap the tile, tap the cell)
	var census := _tile_census(surface)
	_ck("round 1 tray starts with its two authored tiles", surface.pipe_tray.size() == 2)
	_tap(surface, surface._pipe_tray_rect(0).get_center())
	_ck("a tray tap never duplicates a tile", _tile_census(surface) == census)
	_ck("a tray tap remembers the selection", surface.pipe_tray_sel >= 0)
	surface._press(surface._pipe_cell_rect(5).get_center())
	_ck("tap-tap places the remembered tile", String(surface.pipe_grid[5]) == "H")
	_ck("placement conserves the tile census", _tile_census(surface) == census)
	_drag_place(surface, 0, 6)
	_ck("drag placement lands the second pipe", String(surface.pipe_grid[6]) == "H")
	_flow(surface, 9.0)
	_ck("round 1 fuel reaches the rocket", surface.pipe_round >= 1)
	_flow(surface, 1.5)

	# ---- round 2: the audit's dead end — SW into cell 0 gets fuel, and the
	# child must be able to LIFT the fueled mistake and fix her own plan
	var sw_slot: int = surface.pipe_tray.find("SW")
	_ck("round 2 tray holds the audit's trap tile", sw_slot >= 0)
	if sw_slot >= 0:
		_drag_place(surface, sw_slot, 0)
	_flow(surface, 4.0)
	_ck("the trap tile gets fuel (the audit's dead end)", 0 in surface._pipe_flow_cells())
	surface._press(surface._pipe_cell_rect(0).get_center())
	_ck("a fueled tile can be LIFTED and the fuel drains back",
		surface.pipe_drag_tile == "SW" and not (0 in surface._pipe_flow_cells()))
	surface._release(surface._pipe_tray_rect(0).get_center())
	_ck("the lifted tile returns to the tray", surface.pipe_tray.has("SW"))
	for pair: Array in [["SE", 0], ["H", 1], ["SW", 2], ["NE", 6]]:
		var slot: int = surface.pipe_tray.find(String(pair[0]))
		if slot >= 0:
			_drag_place(surface, slot, int(pair[1]))
	_flow(surface, 14.0)
	_ck("round 2 completes after the recovery", surface.pipe_round >= 2)
	_flow(surface, 1.5)

	# ---- round 3: block the flow into the napping imp on purpose
	var h_slot: int = surface.pipe_tray.find("H")
	if h_slot >= 0:
		_drag_place(surface, h_slot, 5)
	_flow(surface, 4.0)
	surface.pipe_wait_t = 9.0
	var hint := surface._pipe_hint_cell()
	_ck("the help twinkle never marks the napping imp",
		hint >= 0 and String(surface.pipe_grid[hint]) != "IMP")
	# the kind auto-recovery: fuel that has waited far past the hint window
	# pops the wrong pipe back to the tray by itself
	surface.pipe_wait_t = 15.9
	surface.pipe_flow_t = 1.19
	surface._pipe_tick(0.2)
	_ck("long-waiting fuel kindly returns the wrong pipe to the tray",
		not (5 in surface._pipe_flow_cells()) and String(surface.pipe_grid[5]) == "")

	print("PIPE|result: %s" % ("ALL OK" if failed == 0 else "%d FAIL" % failed))
	quit(0 if failed == 0 else 1)
