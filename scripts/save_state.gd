class_name SaveState
extends RefCounted
# Phase 7.1: mechanical extraction of the save/load helpers from main.gd.
# ALL state stays on main (m.*) — this class owns only the logic, so save
# compatibility and behavior are unchanged. Received main by reference.

var m: ReefMain

func _init(main: ReefMain) -> void:
	m = main

func load_save() -> void:
	if FileAccess.file_exists(m.SAVE_PATH):
		var f = FileAccess.open(m.SAVE_PATH, FileAccess.READ)
		if f != null:
			var d: Variant = JSON.parse_string(f.get_as_text())
			if d is Dictionary:
				m.save_data = d
	m.finale_done = bool(m.save_data.get("finale", false))
	m.level2_done_once = bool(m.save_data.get("level2", false))
	m.plays = int(m.save_data.get("plays", 0)) + 1   # each launch flips day <-> night
	m.is_night = (m.plays % 2) == 0
	m._apply_time_of_day()
	m.music_on = bool(m.save_data.get("music", true))
	var qdef: String = "speedy" if OS.has_feature("mobile") else "sparkly"
	m._apply_quality(String(m.save_data.get("quality", qdef)))
	m.music.volume_db = -8.0 if m.music_on else -60.0
	if m.music_btn != null:
		m.music_btn.text = "Music: On" if m.music_on else "Music: Off"
	m.pearl_count = int(m.save_data.get("pearls", 0))
	m.custom_fish = m.save_data.get("custom_fish", [])
	m.custom_friends = m.save_data.get("custom_friends", [])
	m.craft_unlocks = m.save_data.get("crafts", {})
	m.stickers = m.save_data.get("stickers", {})
	# legacy cosmetic flags (tail/tiara/pearlskin) may still sit in "owned" from
	# old saves — kept for save compatibility, no longer applied to the player
	m.shop_owned = m.save_data.get("owned", {})
	m.animals_owned = m.save_data.get("animals", {})
	if bool(m.shop_owned.get("tail", false)):
		m.player.set_rainbow_trail(true)
	if bool(m.shop_owned.get("tiara", false)):
		m.player.set_tiara(true)
	m.galaxy_unlocked = bool(m.save_data.get("galaxy", false))
	m.bwd_done = bool(m.save_data.get("bwdone", false))
	m.combat_ice_done = bool(m.save_data.get("combat_ice", false))
	m.combat_fire_done = bool(m.save_data.get("combat_fire", false))
	m.dungeon_progress = clampi(int(m.save_data.get("dungeon_progress", 0)), 0, 10)
	m.dungeon_done = bool(m.save_data.get("dungeon_done", false))
	m.skin_id = String(m.save_data.get("skin", "classic"))
	# Fairy Roshan is the Butterfly World prize (grandfathered if already worn)
	m.fairy_skin_unlocked = bool(m.save_data.get("fairyskin", false)) or m.skin_id == "fairy"
	m._apply_skin()
	var won_d: Dictionary = m.save_data.get("won", {})
	var found_d: Dictionary = m.save_data.get("found", {})
	for f2 in m.friends:
		var nm := String(f2["fname"])
		if bool(found_d.get(nm, false)):
			m.first_session = false
			f2["found"] = true
			(f2["beacon"] as OmniLight3D).light_energy = 1.0
			((f2["pillar"] as MeshInstance3D).material_override as StandardMaterial3D).albedo_color.a = 0.035
		if bool(won_d.get(nm, false)):
			f2["won"] = true
			m.trophies += 1
			m._add_won_star(f2)
	m._update_hud()

func write_save() -> void:
	var won_d := {}
	var found_d := {}
	for f2 in m.friends:
		won_d[String(f2["fname"])] = bool(f2["won"])
		found_d[String(f2["fname"])] = bool(f2["found"])
	m.save_data = {"won": won_d, "found": found_d, "finale": m.finale_done, "music": m.music_on, "quality": m.quality, "pearls": m.pearl_count, "skin": m.skin_id, "level2": m.level2_done_once, "plays": m.plays, "custom_fish": m.custom_fish, "custom_friends": m.custom_friends, "crafts": m.craft_unlocks, "galaxy": m.galaxy_unlocked, "bwdone": m.bwd_done, "fairyskin": m.fairy_skin_unlocked, "combat_ice": m.combat_ice_done, "combat_fire": m.combat_fire_done, "dungeon_progress": m.dungeon_progress, "dungeon_done": m.dungeon_done, "stickers": m.stickers, "owned": m.shop_owned, "animals": m.animals_owned}
	var f = FileAccess.open(m.SAVE_PATH, FileAccess.WRITE)
	if f != null:
		f.store_string(JSON.stringify(m.save_data))
