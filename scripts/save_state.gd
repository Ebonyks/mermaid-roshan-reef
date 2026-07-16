class_name SaveState
extends RefCounted
# Phase 7.1: mechanical extraction of the save/load helpers from main.gd.
# ALL state stays on main (m.*) — this class owns only the logic, so save
# compatibility and behavior are unchanged. Received main by reference.

var m: ReefMain

func _init(main: ReefMain) -> void:
	m = main

func _read_save_dict(path: String) -> Variant:
	if not FileAccess.file_exists(path):
		return null
	var f: FileAccess = FileAccess.open(path, FileAccess.READ)
	if f == null:
		return null
	var d: Variant = JSON.parse_string(f.get_as_text())
	return d if d is Dictionary else null

func _recover_save_if_needed() -> Variant:
	# Compare transaction generations, not just existence: Android can kill the
	# app after a newer .tmp is flushed but before the older primary is rotated.
	# Ties prefer the primary because it is listed first.
	var candidates: Array[String] = [m.SAVE_PATH, m.SAVE_PATH + ".tmp0", m.SAVE_PATH + ".tmp1", m.SAVE_PATH + ".tmp", m.SAVE_PATH + ".bak"]
	var best_path := ""
	var best_data: Variant = null
	var best_generation := -1
	for candidate: String in candidates:
		var candidate_data: Variant = _read_save_dict(candidate)
		if not (candidate_data is Dictionary):
			continue
		var generation: int = int((candidate_data as Dictionary).get("save_generation", 0))
		if generation > best_generation:
			best_generation = generation
			best_path = candidate
			best_data = candidate_data
	if not (best_data is Dictionary):
		return null
	if best_path != m.SAVE_PATH:
		var save_abs: String = ProjectSettings.globalize_path(m.SAVE_PATH)
		var best_abs: String = ProjectSettings.globalize_path(best_path)
		var can_promote := true
		if FileAccess.file_exists(m.SAVE_PATH):
			can_promote = DirAccess.remove_absolute(save_abs) == OK
		if can_promote:
			# If promotion fails, the validated candidate remains in place and will
			# still win the generation comparison on the next launch.
			DirAccess.rename_absolute(best_abs, save_abs)
	return best_data

func load_save() -> void:
	var loaded: Variant = _recover_save_if_needed()
	if loaded is Dictionary:
		m.save_data = loaded
	m.save_generation = int(m.save_data.get("save_generation", 0))
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
	var saved_critters: Variant = m.save_data.get("critters", {})
	m.critter_collection = saved_critters if saved_critters is Dictionary else {}
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

func write_save() -> bool:
	var won_d := {}
	var found_d := {}
	for f2 in m.friends:
		won_d[String(f2["fname"])] = bool(f2["won"])
		found_d[String(f2["fname"])] = bool(f2["found"])
	var next_generation: int = m.save_generation + 1
	var next_save_data: Dictionary = {"won": won_d, "found": found_d, "finale": m.finale_done, "music": m.music_on, "quality": m.quality, "pearls": m.pearl_count, "skin": m.skin_id, "level2": m.level2_done_once, "plays": m.plays, "custom_fish": m.custom_fish, "custom_friends": m.custom_friends, "crafts": m.craft_unlocks, "galaxy": m.galaxy_unlocked, "bwdone": m.bwd_done, "fairyskin": m.fairy_skin_unlocked, "combat_ice": m.combat_ice_done, "combat_fire": m.combat_fire_done, "dungeon_progress": m.dungeon_progress, "dungeon_done": m.dungeon_done, "stickers": m.stickers, "owned": m.shop_owned, "animals": m.animals_owned, "critters": m.critter_collection, "save_generation": next_generation}
	# Alternate staging slots by generation. A retry never deletes the previous
	# complete temp before its replacement is flushed, so a kill/open failure at
	# any point still leaves at least the last durable generation recoverable.
	var temp_path: String = m.SAVE_PATH + (".tmp%d" % (next_generation & 1))
	var backup_path: String = m.SAVE_PATH + ".bak"
	var temp_abs: String = ProjectSettings.globalize_path(temp_path)
	var save_abs: String = ProjectSettings.globalize_path(m.SAVE_PATH)
	var backup_abs: String = ProjectSettings.globalize_path(backup_path)
	if FileAccess.file_exists(temp_path):
		if DirAccess.remove_absolute(temp_abs) != OK:
			return false
	var f: FileAccess = FileAccess.open(temp_path, FileAccess.WRITE)
	if f == null:
		return false
	f.store_string(JSON.stringify(next_save_data))
	f.flush()
	var write_ok: bool = f.get_error() == OK
	f.close()
	if not write_ok:
		DirAccess.remove_absolute(temp_abs)
		return false
	# Only now may retries advance to the other slot: this generation is fully
	# flushed and remains a recovery candidate even if every later rename fails.
	m.save_generation = next_generation
	m.save_data = next_save_data
	if FileAccess.file_exists(backup_path):
		if DirAccess.remove_absolute(backup_abs) != OK:
			return false
	var had_save: bool = FileAccess.file_exists(m.SAVE_PATH)
	if had_save and DirAccess.rename_absolute(save_abs, backup_abs) != OK:
		return false
	if DirAccess.rename_absolute(temp_abs, save_abs) != OK:
		if had_save and FileAccess.file_exists(backup_path):
			DirAccess.rename_absolute(backup_abs, save_abs)
		return false
	# The new primary is durable. Older transaction artifacts can now be removed;
	# cleanup failure is harmless because generation selection ignores them.
	for stale_path: String in [m.SAVE_PATH + ".tmp0", m.SAVE_PATH + ".tmp1", m.SAVE_PATH + ".tmp", backup_path]:
		if FileAccess.file_exists(stale_path):
			DirAccess.remove_absolute(ProjectSettings.globalize_path(stale_path))
	return true
