extends "res://scripts/probe_day_one_pool_shots.gd"
const ART_TRACE := preload("res://tools/job_art_scene_trace.gd")

func _capture(name: String) -> void:
	var was_paused: bool = paused
	paused = true
	await _frames(3)
	await RenderingServer.frame_post_draw
	ART_TRACE.save_frame_receipt(root, name, capture_root,
		"res://tools/capture_day_one_pool_art_inventory.gd", "res://scripts/probe_day_one_pool_shots.gd")
	paused = was_paused
