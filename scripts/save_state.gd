class_name SaveState
extends RefCounted
# Phase 7.1: mechanical extraction of the save/load helpers from main.gd.
# ALL state stays on main (m.*) -- this class owns only the logic. Save files
# are versioned and installed transactionally so a killed write cannot erase a
# child's progress.

const SCHEMA_VERSION := 1
const BACKUP_SUFFIX := ".bak"
const TEMP_SUFFIX := ".tmp"
const OLD_SUFFIX := ".old"
const BOOL_KEYS: Array[String] = [
	"finale", "music", "level2", "galaxy", "bwdone", "fairyskin",
	"combat_ice", "combat_fire", "portal_unlocked", "dungeon_done",
	"opera_done",
]
const DICTIONARY_KEYS: Array[String] = [
	"won", "found", "crafts", "stickers", "owned", "animals", "critters",
]
const ARRAY_KEYS: Array[String] = ["custom_fish", "custom_friends"]
const KNOWN_KEYS: Array[String] = [
	"schema_version", "won", "found", "finale", "music", "quality",
	"pearls", "pearls_ever", "portal_unlocked", "skin", "level2", "plays", "custom_fish", "custom_friends",
	"crafts", "galaxy", "bwdone", "fairyskin", "combat_ice", "combat_fire",
	"dungeon_progress", "dungeon_done", "opera_progress", "opera_done",
	"stickers", "owned", "animals",
]

var m: ReefMain
var save_path: String
var future_schema_read_only := false

func _init(main: ReefMain, path_override: String = "") -> void:
	m = main
	save_path = path_override if not path_override.is_empty() else m.SAVE_PATH

func load_save() -> void:
	future_schema_read_only = false
	var selected: Dictionary = _select_load_candidate()
	if bool(selected.get("valid", false)):
		var selected_data: Dictionary = selected.get("data", {})
		m.save_data = selected_data.duplicate(true)
		var source_path: String = String(selected.get("path", ""))
		future_schema_read_only = bool(selected.get("future", false))
		if future_schema_read_only:
			push_warning("SaveState: save schema is newer than this build; preserving it read-only")
		else:
			var backup: Dictionary = _read_save_candidate(_backup_path())
			if not bool(backup.get("clean", false)):
				if not _install_backup(m.save_data):
					push_warning("SaveState: could not establish a last-known-good backup")
			if source_path != save_path or bool(selected.get("changed", false)):
				if source_path != save_path:
					push_warning("SaveState: recovered progress from %s" % source_path)
				if not _repair_primary(m.save_data):
					push_warning("SaveState: recovery loaded in memory but the primary file could not be repaired")
	else:
		m.save_data = _normalise_save({})
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
	m.pearls_ever = maxi(m.pearl_count, int(m.save_data.get("pearls_ever", m.pearl_count)))
	# A completed Level 2 is definitive legacy evidence that the portal opened.
	# The five-friend finale alone never satisfied the original ten-pearl gate.
	m.portal_unlocked = bool(m.save_data.get("portal_unlocked", false)) or m.level2_done_once
	m.custom_fish = m.save_data.get("custom_fish", [])
	m.custom_friends = m.save_data.get("custom_friends", [])
	m.craft_unlocks = m.save_data.get("crafts", {})
	m.stickers = m.save_data.get("stickers", {})
	# legacy cosmetic flags (tail/tiara/pearlskin) may still sit in "owned" from
	# old saves -- kept for save compatibility, no longer applied to the player
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
	m.opera_progress = clampi(int(m.save_data.get("opera_progress", 0)), 0, 14)
	m.opera_done = bool(m.save_data.get("opera_done", false))
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
	# Recheck disk at the write boundary too: callers can construct SaveState and
	# write without calling load_save() first, and a recovery copy may be the only
	# surviving N+1 document.
	if future_schema_read_only or not _find_future_candidate().is_empty():
		future_schema_read_only = true
		push_warning("SaveState: skipped write because a newer save schema is loaded")
		return true
	var won_d: Dictionary = {}
	var found_d: Dictionary = {}
	for f2 in m.friends:
		won_d[String(f2["fname"])] = bool(f2["won"])
		found_d[String(f2["fname"])] = bool(f2["found"])
	# Start with the loaded document so keys from later builds survive a round
	# trip through this one. Known fields are then replaced by current state.
	m.pearls_ever = maxi(m.pearls_ever, m.pearl_count)
	var next_data: Dictionary = _normalise_save(m.save_data)
	var next_generation: int = maxi(m.save_generation, int(next_data.get("save_generation", 0))) + 1
	next_data["schema_version"] = maxi(int(next_data.get("schema_version", SCHEMA_VERSION)), SCHEMA_VERSION)
	next_data["won"] = won_d
	next_data["found"] = found_d
	next_data["finale"] = m.finale_done
	next_data["music"] = m.music_on
	next_data["quality"] = m.quality
	next_data["pearls"] = maxi(m.pearl_count, 0)
	next_data["pearls_ever"] = maxi(m.pearls_ever, 0)
	next_data["portal_unlocked"] = m.portal_unlocked
	next_data["skin"] = m.skin_id
	next_data["level2"] = m.level2_done_once
	next_data["plays"] = maxi(m.plays, 0)
	next_data["custom_fish"] = m.custom_fish
	next_data["custom_friends"] = m.custom_friends
	next_data["crafts"] = m.craft_unlocks
	next_data["galaxy"] = m.galaxy_unlocked
	next_data["bwdone"] = m.bwd_done
	next_data["fairyskin"] = m.fairy_skin_unlocked
	next_data["combat_ice"] = m.combat_ice_done
	next_data["combat_fire"] = m.combat_fire_done
	next_data["dungeon_progress"] = clampi(m.dungeon_progress, 0, 10)
	next_data["dungeon_done"] = m.dungeon_done
	next_data["opera_progress"] = clampi(m.opera_progress, 0, 14)
	next_data["opera_done"] = m.opera_done
	next_data["stickers"] = m.stickers
	next_data["owned"] = m.shop_owned
	next_data["animals"] = m.animals_owned
	next_data["critters"] = m.critter_collection
	next_data["save_generation"] = next_generation
	var normalised: Dictionary = _normalise_save(next_data)
	if not _commit_save(normalised):
		push_error("SaveState: progress remains in memory, but could not be written safely")
		return false
	m.save_data = normalised
	m.save_generation = next_generation
	return true

func _select_load_candidate() -> Dictionary:
	var paths: Array[String] = _candidate_paths()
	var candidates: Array[Dictionary] = []
	for path: String in paths:
		candidates.append(_read_save_candidate(path))
	# Never choose an older clean fallback before discovering an N+1 recovery
	# copy later in the list. Preserving the newest schema outranks repair order.
	for candidate: Dictionary in candidates:
		if bool(candidate.get("valid", false)) and bool(candidate.get("future", false)):
			return candidate
	var primary: Dictionary = candidates[0]
	var newest_clean: Dictionary = {}
	var newest_generation: int = -1
	for candidate: Dictionary in candidates:
		if not bool(candidate.get("clean", false)):
			continue
		var candidate_data: Dictionary = candidate.get("data", {})
		var generation: int = int(candidate_data.get("save_generation", 0))
		if newest_clean.is_empty() or generation > newest_generation:
			newest_clean = candidate
			newest_generation = generation
	if bool(primary.get("clean", false)):
		return newest_clean
	# Normalise a damaged preference/config field in place instead of rolling
	# all newer progress back. Critical progression corruption still falls
	# through to a known-good recovery copy.
	if bool(primary.get("valid", false)) and bool(primary.get("complete", false)) and bool(primary.get("progress_clean", false)):
		var primary_data: Dictionary = primary.get("data", {})
		if newest_clean.is_empty() or int(primary_data.get("save_generation", 0)) >= newest_generation:
			return primary
		return newest_clean
	if not newest_clean.is_empty():
		return newest_clean
	var salvage: Dictionary = primary if bool(primary.get("valid", false)) else {}
	for i in range(1, candidates.size()):
		var candidate: Dictionary = candidates[i]
		if salvage.is_empty() and bool(candidate.get("valid", false)):
			salvage = candidate
	return salvage

func _recover_save_if_needed() -> Variant:
	# Compatibility entry point used by the kart durability probe and older
	# callers. Selection compares transaction generations and repairs the primary
	# from a newer fully validated staging slot without deleting the source first.
	var selected: Dictionary = _select_load_candidate()
	if not bool(selected.get("valid", false)):
		return null
	var data: Dictionary = selected.get("data", {})
	var source_path: String = String(selected.get("path", ""))
	if source_path != save_path and not bool(selected.get("future", false)):
		if not _repair_primary(data):
			push_warning("SaveState: newer recovery data remains staged because primary promotion failed")
	return data

func _candidate_paths() -> Array[String]:
	return [
		save_path,
		save_path + ".tmp0",
		save_path + ".tmp1",
		_temp_path(save_path),
		_old_path(save_path),
		_backup_path(),
		_temp_path(_backup_path()),
		_old_path(_backup_path()),
	]

func _find_future_candidate() -> Dictionary:
	for path: String in _candidate_paths():
		var candidate: Dictionary = _read_save_candidate(path)
		if bool(candidate.get("valid", false)) and bool(candidate.get("future", false)):
			return candidate
	return {}

func _read_save_candidate(path: String) -> Dictionary:
	var result: Dictionary = {
		"valid": false,
		"clean": false,
		"complete": false,
		"progress_clean": false,
		"future": false,
		"changed": false,
		"path": path,
		"data": {},
	}
	if not FileAccess.file_exists(path):
		return result
	var file: FileAccess = FileAccess.open(path, FileAccess.READ)
	if file == null:
		return result
	var text: String = file.get_as_text()
	file.close()
	if text.strip_edges().is_empty():
		return result
	var json: JSON = JSON.new()
	var parse_error: Error = json.parse(text)
	if parse_error != OK:
		return result
	var parsed: Variant = json.data
	if typeof(parsed) != TYPE_DICTIONARY:
		return result
	var raw: Dictionary = parsed
	if not _looks_like_save(raw):
		return result
	var normalised: Dictionary = _normalise_save(raw)
	var version: int = _schema_version(raw)
	var future: bool = version > SCHEMA_VERSION
	var complete: bool = _has_complete_schema(raw)
	result["valid"] = true
	result["clean"] = _known_types_are_valid(raw) and complete
	result["complete"] = complete
	result["progress_clean"] = _progress_types_are_valid(raw)
	result["future"] = future
	result["changed"] = raw != normalised
	result["data"] = normalised
	return result

func _looks_like_save(data: Dictionary) -> bool:
	for key: String in KNOWN_KEYS:
		if data.has(key):
			return true
	return false

func _schema_version(data: Dictionary) -> int:
	if not data.has("schema_version") or not _is_nonnegative_integer(data["schema_version"]):
		return 0
	return int(data["schema_version"])

func _has_complete_schema(data: Dictionary) -> bool:
	var version: int = _schema_version(data)
	if version > SCHEMA_VERSION:
		return true
	if data.has("schema_version"):
		for key: String in KNOWN_KEYS:
			if not data.has(key):
				return false
		return true
	# Legacy releases had no schema marker, but every genuine save contained
	# these core progression fields. A one-key JSON fragment is not a save.
	return data.has("won") and data.has("found") and data.has("pearls") and data.has("plays")

func _progress_types_are_valid(data: Dictionary) -> bool:
	for key: String in BOOL_KEYS:
		if key == "music":
			continue
		if data.has(key) and typeof(data[key]) != TYPE_BOOL:
			return false
	for key: String in DICTIONARY_KEYS:
		if data.has(key) and typeof(data[key]) != TYPE_DICTIONARY:
			return false
	for key: String in ARRAY_KEYS:
		if data.has(key) and typeof(data[key]) != TYPE_ARRAY:
			return false
	for key: String in ["schema_version", "pearls", "pearls_ever", "dungeon_progress", "opera_progress", "save_generation"]:
		if data.has(key) and not _is_nonnegative_integer(data[key]):
			return false
	return true

func _known_types_are_valid(data: Dictionary) -> bool:
	for key: String in BOOL_KEYS:
		if data.has(key) and typeof(data[key]) != TYPE_BOOL:
			return false
	for key: String in DICTIONARY_KEYS:
		if data.has(key) and typeof(data[key]) != TYPE_DICTIONARY:
			return false
	for key: String in ARRAY_KEYS:
		if data.has(key) and typeof(data[key]) != TYPE_ARRAY:
			return false
	for key: String in ["schema_version", "pearls", "pearls_ever", "dungeon_progress", "opera_progress", "plays", "save_generation"]:
		if data.has(key) and not _is_nonnegative_integer(data[key]):
			return false
	if data.has("quality"):
		if typeof(data["quality"]) != TYPE_STRING or not (String(data["quality"]) in ["speedy", "sparkly"]):
			return false
	if data.has("skin") and (typeof(data["skin"]) != TYPE_STRING or String(data["skin"]).is_empty()):
		return false
	return true

func _normalise_save(raw: Dictionary) -> Dictionary:
	var data: Dictionary = raw.duplicate(true)
	var qdef: String = "speedy" if OS.has_feature("mobile") else "sparkly"
	var version: int = _nonnegative_int_or_default(raw, "schema_version", SCHEMA_VERSION)
	data["schema_version"] = maxi(version, SCHEMA_VERSION)
	data["won"] = _dictionary_or_default(raw, "won")
	data["found"] = _dictionary_or_default(raw, "found")
	data["finale"] = _bool_or_default(raw, "finale", false)
	data["music"] = _bool_or_default(raw, "music", true)
	data["quality"] = _quality_or_default(raw, qdef)
	var pearls: int = _nonnegative_int_or_default(raw, "pearls", 0)
	data["pearls"] = pearls
	data["pearls_ever"] = maxi(pearls, _nonnegative_int_or_default(raw, "pearls_ever", pearls))
	data["portal_unlocked"] = _bool_or_default(raw, "portal_unlocked", false)
	data["skin"] = _string_or_default(raw, "skin", "classic")
	data["level2"] = _bool_or_default(raw, "level2", false)
	data["plays"] = _nonnegative_int_or_default(raw, "plays", 0)
	data["custom_fish"] = _array_or_default(raw, "custom_fish")
	data["custom_friends"] = _array_or_default(raw, "custom_friends")
	data["crafts"] = _dictionary_or_default(raw, "crafts")
	data["galaxy"] = _bool_or_default(raw, "galaxy", false)
	data["bwdone"] = _bool_or_default(raw, "bwdone", false)
	data["fairyskin"] = _bool_or_default(raw, "fairyskin", false)
	data["combat_ice"] = _bool_or_default(raw, "combat_ice", false)
	data["combat_fire"] = _bool_or_default(raw, "combat_fire", false)
	data["dungeon_progress"] = clampi(_nonnegative_int_or_default(raw, "dungeon_progress", 0), 0, 10)
	data["dungeon_done"] = _bool_or_default(raw, "dungeon_done", false)
	data["opera_progress"] = clampi(_nonnegative_int_or_default(raw, "opera_progress", 0), 0, 14)
	data["opera_done"] = _bool_or_default(raw, "opera_done", false)
	data["stickers"] = _dictionary_or_default(raw, "stickers")
	data["owned"] = _dictionary_or_default(raw, "owned")
	data["animals"] = _dictionary_or_default(raw, "animals")
	data["critters"] = _dictionary_or_default(raw, "critters")
	data["save_generation"] = _nonnegative_int_or_default(raw, "save_generation", 0)
	return data

func _bool_or_default(data: Dictionary, key: String, default_value: bool) -> bool:
	var value: Variant = data.get(key, default_value)
	return bool(value) if typeof(value) == TYPE_BOOL else default_value

func _dictionary_or_default(data: Dictionary, key: String) -> Dictionary:
	var value: Variant = data.get(key, {})
	if typeof(value) == TYPE_DICTIONARY:
		var dictionary: Dictionary = value
		return dictionary.duplicate(true)
	return {}

func _array_or_default(data: Dictionary, key: String) -> Array:
	var value: Variant = data.get(key, [])
	if typeof(value) == TYPE_ARRAY:
		var array: Array = value
		return array.duplicate(true)
	return []

func _string_or_default(data: Dictionary, key: String, default_value: String) -> String:
	var value: Variant = data.get(key, default_value)
	if typeof(value) == TYPE_STRING and not String(value).is_empty():
		return String(value)
	return default_value

func _quality_or_default(data: Dictionary, default_value: String) -> String:
	var value: Variant = data.get("quality", default_value)
	if typeof(value) == TYPE_STRING and String(value) in ["speedy", "sparkly"]:
		return String(value)
	return default_value

func _nonnegative_int_or_default(data: Dictionary, key: String, default_value: int) -> int:
	var value: Variant = data.get(key, default_value)
	return int(value) if _is_nonnegative_integer(value) else default_value

func _is_nonnegative_integer(value: Variant) -> bool:
	if typeof(value) == TYPE_INT:
		return int(value) >= 0
	if typeof(value) == TYPE_FLOAT:
		var number: float = float(value)
		return is_finite(number) and number >= 0.0 and number == floorf(number)
	return false

func _commit_save(data: Dictionary) -> bool:
	var primary_temp: String = _temp_path(save_path)
	if not _write_checked_file(primary_temp, data):
		return false
	var primary_before: Dictionary = _read_save_candidate(save_path)
	var backup_before: Dictionary = _read_save_candidate(_backup_path())
	var backup_ready: bool = bool(backup_before.get("clean", false))
	if bool(primary_before.get("clean", false)):
		var previous_data: Dictionary = primary_before.get("data", {})
		backup_ready = _install_backup(previous_data)
		if not backup_ready and bool(backup_before.get("clean", false)):
			backup_ready = true
			push_warning("SaveState: keeping the existing valid backup because it could not be refreshed")
	elif not backup_ready:
		backup_ready = _install_backup(data)
	if not backup_ready:
		_remove_temporary(primary_temp)
		return false
	if not _replace_file(primary_temp, save_path):
		return false
	var installed: Dictionary = _read_save_candidate(save_path)
	if not bool(installed.get("clean", false)):
		push_error("SaveState: primary verification failed after installation; backup was retained")
		return false
	return true

func _install_backup(data: Dictionary) -> bool:
	var backup_path: String = _backup_path()
	var backup_temp: String = _temp_path(backup_path)
	if not _write_checked_file(backup_temp, data):
		return false
	if not _replace_file(backup_temp, backup_path):
		return false
	var installed: Dictionary = _read_save_candidate(backup_path)
	return bool(installed.get("clean", false))

func _repair_primary(data: Dictionary) -> bool:
	var primary_temp: String = _temp_path(save_path)
	if not _write_checked_file(primary_temp, data):
		return false
	return _replace_file(primary_temp, save_path)

func _write_checked_file(path: String, data: Dictionary) -> bool:
	var file: FileAccess = FileAccess.open(path, FileAccess.WRITE)
	if file == null:
		push_error("SaveState: could not open %s for writing" % path)
		return false
	file.store_string(JSON.stringify(data))
	file.flush()
	var write_error: Error = file.get_error()
	file.close()
	if write_error != OK:
		push_error("SaveState: write failed for %s (error %d)" % [path, write_error])
		return false
	var checked: Dictionary = _read_save_candidate(path)
	if not bool(checked.get("clean", false)):
		push_error("SaveState: refused an invalid temporary save at %s" % path)
		return false
	return true

func _replace_file(source_path: String, target_path: String) -> bool:
	var source_absolute: String = ProjectSettings.globalize_path(source_path)
	var target_absolute: String = ProjectSettings.globalize_path(target_path)
	# POSIX rename replaces the destination atomically. Windows may reject that
	# form, so retain the old target until the new file has landed.
	var direct_error: Error = DirAccess.rename_absolute(source_absolute, target_absolute)
	if direct_error == OK:
		return true
	if not FileAccess.file_exists(target_path):
		push_error("SaveState: could not install %s (error %d)" % [target_path, direct_error])
		return false
	var old_path: String = _old_path(target_path)
	if FileAccess.file_exists(old_path):
		var stale_remove_error: Error = DirAccess.remove_absolute(ProjectSettings.globalize_path(old_path))
		if stale_remove_error != OK:
			push_error("SaveState: preserved target because stale recovery file could not be removed")
			return false
	var move_old_error: Error = DirAccess.rename_absolute(target_absolute, ProjectSettings.globalize_path(old_path))
	if move_old_error != OK:
		push_error("SaveState: preserved target because it could not be staged (error %d)" % move_old_error)
		return false
	var install_error: Error = DirAccess.rename_absolute(source_absolute, target_absolute)
	if install_error != OK:
		var restore_error: Error = DirAccess.rename_absolute(ProjectSettings.globalize_path(old_path), target_absolute)
		if restore_error != OK:
			push_error("SaveState: install and rollback both failed; recovery copies remain on disk")
		else:
			push_error("SaveState: install failed; the previous file was restored")
		return false
	var remove_error: Error = DirAccess.remove_absolute(ProjectSettings.globalize_path(old_path))
	if remove_error != OK:
		push_warning("SaveState: new file installed; an extra recovery copy remains at %s" % old_path)
	return true

func _remove_temporary(path: String) -> void:
	if not FileAccess.file_exists(path):
		return
	var remove_error: Error = DirAccess.remove_absolute(ProjectSettings.globalize_path(path))
	if remove_error != OK:
		push_warning("SaveState: could not remove temporary file %s" % path)

func _backup_path() -> String:
	return save_path + BACKUP_SUFFIX

func _temp_path(path: String) -> String:
	return path + TEMP_SUFFIX

func _old_path(path: String) -> String:
	return path + OLD_SUFFIX
