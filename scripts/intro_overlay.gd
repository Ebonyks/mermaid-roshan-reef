class_name IntroOverlay
extends RefCounted
# Day One opens with Daddy Mermaid and Mermaid Roshan flying to their kingdom.
# The final authored movie can be dropped at this stable path without code edits.

const OPENING_VIDEO := "res://assets/cinematics/opening/daddy_roshan_flight.ogv"
const OPENING_POSTER := ""  # No ratio-changing fallback plate.

var m: ReefMain

func _init(main: ReefMain) -> void:
	m = main

func _build_intro() -> void:
	m.intro_idx = 0
	m._cinematic_ref().play(OPENING_VIDEO, OPENING_POSTER,
		_opening_finished, "Intro")

func _intro_repeat() -> void:
	m._cinematic_ref().replay()

func _intro_next() -> void:
	if m._cinematic_ref().is_active():
		m._cinematic_ref().finish()
	else:
		_opening_finished()

func _skip_intro() -> void:
	if m._cinematic_ref().is_active():
		m._cinematic_ref().finish()
	else:
		_opening_finished()

func _opening_finished() -> void:
	if m.opening_seen:
		return
	m.opening_seen = true
	m.save_data["opening_seen"] = true
	m._write_save()