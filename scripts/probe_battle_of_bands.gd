extends SceneTree

func _initialize() -> void:
	call_deferred("_run")

func _run() -> void:
	if "--capture" in OS.get_cmdline_user_args():
		root.mode = Window.MODE_WINDOWED
		root.size = Vector2i(1280, 720)
	var packed := load("res://scenes/battle_of_bands_prototype.tscn") as PackedScene
	var stage: Control = packed.instantiate()
	stage.persist_progress = false
	root.add_child(stage)
	await process_frame
	for frame: int in range(8):
		await process_frame
	if "--capture" in OS.get_cmdline_user_args():
		await RenderingServer.frame_post_draw
		root.get_texture().get_image().save_png("res://build/bands/prototype.png")
	assert(stage.hits == 0, "Passive input must not complete music")
	assert(not stage.strike(2) and stage.hits == 0, "Wrong drum cannot progress")
	stage._set_suspended(true)
	assert(not stage.strike(0), "Focus loss blocks stale input")
	stage._set_suspended(false)
	for index: int in stage.PATTERN:
		assert(stage.strike(index), "Intentional sequence progresses")
	assert(stage.story_step == 0 and stage.candle.visible, "Success precedes theft")
	stage._advance_story()
	assert(stage.story_step == 0, "Song must finish before theft")
	stage._on_song_finished()
	stage.touch_owner = 1
	stage._advance_story()
	assert(stage.story_step == 0, "Held drum touch cannot hand story to another finger")
	stage.touch_owner = -1
	stage._advance_story()
	assert(stage.story_step == 1 and stage.candle.position.x == 1040, "King visibly takes candle")
	stage._advance_story()
	stage._advance_story()
	assert(not stage.king.visible and not stage.prince.visible and stage.hits == 12, "Departure preserves success")
	stage._replay()
	assert(stage.hits == 0 and stage.story_step == 0 and stage.king.visible, "Replay restores band")
	var touch := InputEventScreenTouch.new()
	touch.index = 1
	touch.pressed = true
	touch.position = stage.DRUMS[0]
	stage._gui_input(touch)
	assert(stage.hits == 1, "First finger owns hit")
	touch.index = 2
	touch.position = stage.DRUMS[1]
	stage._gui_input(touch)
	assert(stage.hits == 1, "Second finger cannot steal input")
	stage.progress_path = "user://bands_probe_isolated.cfg"
	stage.persist_progress = true
	stage._checkpoint()
	stage.strike(1)
	var restored: Control = packed.instantiate()
	restored.progress_path = stage.progress_path
	root.add_child(restored)
	await process_frame
	assert(restored.hits == 2, "Save reload preserves phrase progress")
	restored.queue_free()
	for suffix: String in ["", ".bak", ".tmp"]:
		var path: String = ProjectSettings.globalize_path(stage.progress_path + suffix)
		if FileAccess.file_exists(path):
			DirAccess.remove_absolute(path)
	stage.persist_progress = false
	stage.queue_free()
	await process_frame
	print("BANDS|ALL OK|passive wrong-input focus-loss completion theft departure replay second-finger save-reload")
	quit()
