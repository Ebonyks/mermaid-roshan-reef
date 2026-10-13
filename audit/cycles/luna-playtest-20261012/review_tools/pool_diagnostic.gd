extends "res://scripts/probe_day_one_pool_shots.gd"
## Diagnostic adapter only: existing scene/state probe with declared story-clip
## cancellation and exact window size. This bypass is not visible-route proof.

func _run() -> void:
	DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_WINDOWED)
	DisplayServer.window_set_size(Vector2i(1280, 720))
	root.size = Vector2i(1280, 720)
	process_frame.connect(_cancel_fixture_clips)
	print("LUNA_DIAGNOSTIC|window=1280x720|clips=cancelled_fixture_only")
	await super._run()

func _cancel_fixture_clips() -> void:
	for child: Node in root.get_children():
		var main: ReefMain = child as ReefMain
		if main != null and main._day_one_story_clip != null:
			print("LUNA_DIAGNOSTIC|cancel_clip|" + main._day_one_story_clip.movie_id)
			main._day_one_cancel_story_clips()
