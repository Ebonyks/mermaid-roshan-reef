extends SceneTree
## Real ReefMain behavioral probe for the opt-in Day One draft-movie seams.
## Run with: --day-one-draft-movies
## This deliberately drives the live event hooks and cancellation boundary; it
## does not replace movie playback with a synthetic director-only fixture.

var main: ReefMain
var failures: int = 0


func _init() -> void:
	call_deferred("_run")


func _run() -> void:
	_check("draft movie flag is enabled", DayOneDraftMovies.enabled())
	if failures > 0:
		quit(1)
		return
	var scene: PackedScene = load("res://scenes/main.tscn") as PackedScene
	main = scene.instantiate() as ReefMain
	root.add_child(main)
	await _frames(3)
	main._skip_intro()
	await _frames(3)
	_manifest_contract()
	await _arrival_and_dirty_castle()
	await _bathroom_boundary()
	await _locked_event_boundaries()
	await _boss_lifecycle()
	await _terminal_day_two()
	main.queue_free()
	await _frames(2)
	print("DAY_ONE_DRAFT_INTEGRATION|RESULT: ",
		"PASS" if failures == 0 else "FAIL failures=%d" % failures)
	quit(1 if failures > 0 else 0)


func _frames(count: int) -> void:
	for _index: int in range(count):
		await process_frame


func _check(label: String, ok: bool, detail: String = "") -> void:
	if not ok:
		failures += 1
	print("DAY_ONE_DRAFT_INTEGRATION|", label, ": ",
		"OK" if ok else "FAIL", (" (" + detail + ")") if detail != "" else "")


func _manifest_contract() -> void:
	for movie_id: String in DayOneDraftMovies.MOVIE_IDS:
		var expected: bool = movie_id not in ["D1-C07", "D1-C08", "D1-C13"]
		_check("manifest runtime eligibility " + movie_id,
			DayOneDraftMovies.runtime_preview_eligible(movie_id) == expected,
			"expected=%s path=%s" % [expected, DayOneDraftMovies.path_for(movie_id)])


func _reset_state(raw: Dictionary) -> void:
	main._day_one_cancel_draft_movies()
	main._clear_day_one_bathroom_movie_handoff()
	main._day_one_bathroom_entry_movie_checked = false
	main._day_one_draft_movie_seen.clear()
	main._day_one_draft_movie_queue.clear()
	main._day_one_ref().restore_state(raw)
	main.g["day_one_last_event"] = ""
	await _frames(2)


func _seen(movie_id: String) -> bool:
	return main._day_one_draft_movie_seen.has(movie_id)


func _arrival_and_dirty_castle() -> void:
	await _reset_state({})
	main._day_one_begin_arrival()
	await _frames(3)
	_check("arrival starts C00", _seen("D1-C00"))
	_check("draft movie is owned by the global Back route",
		main._navigation_ref().top_id() == "day_one_draft_movie"
		and main.global_navigation_button != null
		and main.global_navigation_button.visible)
	main._navigation_ref().press()
	await _frames(4)
	_check("arrival drains queued C01 after C00 skip", _seen("D1-C01"))
	main._day_one_cancel_draft_movies()
	main._day_one_discover_dirty_castle()
	await _frames(3)
	_check("dirty-castle discovery starts C02", _seen("D1-C02"))
	var before: int = main._day_one_draft_movie_seen.size()
	main._day_one_discover_dirty_castle()
	await _frames(2)
	_check("dirty-castle discovery is one-shot",
		main._day_one_draft_movie_seen.size() == before)
	main._day_one_cancel_draft_movies()


func _bathroom_boundary() -> void:
	await _reset_state({
		"day_one_active": true,
		"day_one_current_room": "bathroom",
		"day_one_completed_rooms": [],
		"day_one_bathroom_cleanup_step": 0,
		"day_one_bathroom_supply_hunt_step": 0,
		"day_one_bathroom_tools_authorized": false,
	})
	# Put the live room owner on the actual bathroom stage before asserting its
	# handoff controls; a rootless director fixture would not test ownership.
	main.pearl_count = main.PEARL_TOTAL
	main.level2_done_once = true
	main._enter_level2_now(true, false, false)
	await _frames(8)
	main._enter_castle_interior_now(false)
	await _frames(12)
	main._castle_rooms_ref().show_room("bubble_bath", false)
	await _frames(6)
	_check("bathroom entry is allowed",
		main.day_one_try_enter_castle_room("bubble_bath"))
	main.day_one_activate_castle_room("bubble_bath")
	await _drain_movie_queue_until("D1-C03")
	_check("bathroom entry starts C03", _seen("D1-C03"))
	main._day_one_cancel_draft_movies()
	main.day_one_authorize_bathroom_tools()
	main.day_one_record_bathroom_cleanup_step(2)
	_check("bathroom completion crosses live seam",
		main.day_one_complete_bathroom_scene())
	await _frames(4)
	_check("bathroom advances to pool",
		main._day_one_ref().is_room_completed("bathroom")
		and main._day_one_ref().current_room_id == "pool")
	_check("bathroom completion starts C04", _seen("D1-C04"))
	if main._day_one_draft_movie != null:
		main._day_one_draft_movie.skip()
	await _frames(4)
	_check("bathroom completion exposes one pool route",
		main._day_one_pool_route_button != null
		and is_instance_valid(main._day_one_pool_route_button))
	var bathroom_seen_count: int = int(_seen("D1-C03"))
	main.day_one_activate_castle_room("bubble_bath")
	await _frames(2)
	_check("bathroom re-entry does not duplicate C03",
		int(_seen("D1-C03")) == bathroom_seen_count)
	if main._day_one_pool_route_button != null \
			and is_instance_valid(main._day_one_pool_route_button):
		main._pause_ref().call_deferred("global_navigation_pressed")
		await _frames(10)
		_check("pool room entry starts C05 through room navigation",
			_seen("D1-C05"))
	main._day_one_cancel_draft_movies()


func _locked_event_boundaries() -> void:
	await _reset_state({
		"day_one_active": true,
		"day_one_current_room": "bathroom",
		"day_one_completed_rooms": [],
	})
	_check("locked pool rejects the real entry guard",
		not main.day_one_try_enter_castle_room("mermaid_pool"))
	if main.day_one_can_enter_castle_room("mermaid_pool"):
		main.day_one_activate_castle_room("mermaid_pool")
	await _frames(2)
	_check("locked pool does not start C05", not _seen("D1-C05"))
	_check("locked stuffie does not start C07", not _seen("D1-C07"))
	_check("locked art does not start C09", not _seen("D1-C09"))
	_check("pre-defeat does not start C13", not _seen("D1-C13"))
	main._day_one_cancel_draft_movies()
	await _reset_state({
		"day_one_active": true,
		"day_one_current_room": "art",
		"day_one_completed_rooms": ["bathroom", "pool", "stuffie"],
	})
	main._castle_rooms_ref().show_room("craft_room", false)
	await _frames(6)
	_check("art room entry starts C09 through room navigation",
		_seen("D1-C09"))
	main._day_one_cancel_draft_movies()


func _drain_movie_queue_until(target_id: String) -> void:
	for _attempt: int in range(12):
		await _frames(2)
		var active_id: String = ""
		if main._day_one_draft_movie != null \
				and is_instance_valid(main._day_one_draft_movie):
			active_id = main._day_one_draft_movie.movie_id
		print("DAY_ONE_DRAFT_INTEGRATION|movie diagnostic id=%s queue=%s "
			% [active_id, main._day_one_draft_movie_queue])
		if _seen(target_id):
			return
		if main._day_one_draft_movie != null \
				and is_instance_valid(main._day_one_draft_movie):
			main._day_one_draft_movie.skip()
	await _frames(3)


func _boss_lifecycle() -> void:
	await _reset_state({
		"day_one_active": true,
		"day_one_current_room": "",
		"day_one_completed_rooms": ["bathroom", "pool", "stuffie", "art"],
		"day_one_giant_dust_bunny_boss_triggered": false,
	})
	var director: DayOneDirector = main._day_one_ref()
	_check("all rooms arm boss door", director.boss_door_glow)
	_check("boss trigger enters real event seam",
		director.trigger_giant_dust_bunny_boss())
	await _frames(3)
	_check("boss entry starts C11", _seen("D1-C11"))
	main.notification(NOTIFICATION_APPLICATION_FOCUS_OUT)
	await _frames(3)
	_check("focus loss cancels boss trigger", not director.giant_dust_bunny_boss_triggered)
	_check("focus loss re-arms boss door", main.day_one_boss_door_ready())
	main._day_one_cancel_draft_movies()
	_check("boss can be retriggered after lifecycle cancel",
		director.trigger_giant_dust_bunny_boss())
	await _frames(3)
	if main._day_one_draft_movie != null:
		main._day_one_draft_movie.skip()
	await _frames(30)
	_check("skipping C11 starts the real Dust Boss",
		main.game == "dustboss")
	main.notification(NOTIFICATION_APPLICATION_FOCUS_OUT)
	await _frames(4)
	_check("focus loss cancels active Dust Boss", main.game != "dustboss")


func _terminal_day_two() -> void:
	await _reset_state({
		"day_one_active": true,
		"day_one_current_room": "",
		"day_one_completed_rooms": ["bathroom", "pool", "stuffie", "art"],
		"day_one_giant_dust_bunny_boss_triggered": true,
	})
	var director: DayOneDirector = main._day_one_ref()
	director.giant_dust_bunny_boss_triggered = true
	_check("boss completion owns terminal transition",
		main.day_one_complete_boss_and_begin_day_two())
	await _frames(4)
	_check("boss defeat starts Chapter 2 independently",
		main.chapter2_active and not main.day_one_is_active())
	_check("ineligible boss-defeat C13 never starts", not _seen("D1-C13"))
	_check("Day Two transition queues C12", _seen("D1-C12"))
	if main._day_one_draft_movie != null:
		main._day_one_draft_movie.skip()
	await _frames(8)
	_check("skipping C12 presents Day Two",
		main.day_two_transition_active
		or bool(main.g.get("day_two_started", false)))
	main._day_one_cancel_draft_movies()
	_check("Day Two event is idempotent",
		not director.complete_day_one_after_boss())
