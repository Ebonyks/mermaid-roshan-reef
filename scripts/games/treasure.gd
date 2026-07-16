class_name TreasureGame
extends RefCounted
# Phase 7.4: mechanical extraction from main.gd — builder + tick for the
# treasure minigame. All state stays on main (m.*); received by reference.

var m: ReefMain

func _init(main: ReefMain) -> void:
	m = main

func build(fr: Dictionary, origin: Vector3) -> void:
	m.g["timer"] = -1.0
	m.g["checks"] = []
	m.g["chains"] = []
	m._build_cavern(origin)
	m.show_msg(fr["fname"], "Shhh... secret caverns! Follow the sparkles down to the treasure!")
