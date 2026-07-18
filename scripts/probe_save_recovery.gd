extends SceneTree
# Focused save durability probe. Uses its own user:// files and never touches
# reef_save.json, so it is safe to run beside the normal full-game probes.

const TEST_PATH := "user://reef_save_recovery_probe.json"
const TEST_FILES: Array[String] = [
	TEST_PATH,
	TEST_PATH + ".bak",
	TEST_PATH + ".tmp",
	TEST_PATH + ".tmp0",
	TEST_PATH + ".tmp1",
	TEST_PATH + ".old",
	TEST_PATH + ".bak.tmp",
	TEST_PATH + ".bak.old",
]

var failures := 0

func _init() -> void:
	_cleanup()
	var main: ReefMain = ReefMain.new()
	main.save_data = {
		"future_payload": {"kept": "yes"},
		"future_list": [1, 2, 3],
	}
	main.pearl_count = 17
	main.plays = 4
	main.dungeon_progress = 4
	main.dungeon_done = false
	var state: SaveState = SaveState.new(main, TEST_PATH)
	state.write_save()
	_expect(FileAccess.file_exists(TEST_PATH), "primary created")
	_expect(FileAccess.file_exists(TEST_PATH + ".bak"), "backup created on first write")
	var first: Dictionary = _read_json(TEST_PATH)
	_expect(int(first.get("schema_version", 0)) == SaveState.SCHEMA_VERSION, "schema version added")
	_expect(first.get("future_payload", {}) == {"kept": "yes"}, "unknown dictionary preserved")
	var future_list: Array = first.get("future_list", [])
	_expect(future_list.size() == 3 and int(future_list[0]) == 1 and int(future_list[2]) == 3, "unknown array preserved")
	_expect(int(first.get("dungeon_progress", -1)) == 4 and not bool(first.get("dungeon_done", true)), "dungeon checkpoint serialized")

	main.pearl_count = 33
	main.dungeon_progress = 99   # corrupt/out-of-range runtime state clamps at the ten-room boundary
	main.dungeon_done = true
	state.write_save()
	var second: Dictionary = _read_json(TEST_PATH)
	var previous: Dictionary = _read_json(TEST_PATH + ".bak")
	_expect(int(second.get("pearls", -1)) == 33, "new primary installed")
	_expect(int(previous.get("pearls", -1)) == 17, "backup retains last known-good primary")
	_expect(second.get("future_payload", {}) == {"kept": "yes"}, "unknown key survives another write")
	_expect(int(second.get("dungeon_progress", -1)) == 10 and bool(second.get("dungeon_done", false)), "dungeon completion serialized and clamped")
	var reload_state: SaveState = SaveState.new(main, TEST_PATH)
	var reload_candidate: Dictionary = reload_state._select_load_candidate()
	var reload_data: Dictionary = reload_candidate.get("data", {})
	_expect(int(reload_data.get("dungeon_progress", -1)) == 10 and bool(reload_data.get("dungeon_done", false)), "fresh reader reloads dungeon completion")

	_write_text(TEST_PATH, "{truncated")
	var recovered: Dictionary = state._select_load_candidate()
	_expect(bool(recovered.get("clean", false)), "truncated primary found a clean recovery copy")
	_expect(String(recovered.get("path", "")) == TEST_PATH + ".bak", "backup selected after truncation")
	var recovered_data: Dictionary = recovered.get("data", {})
	_expect(int(recovered_data.get("pearls", -1)) == 17, "backup progress recovered")
	_expect(int(recovered_data.get("dungeon_progress", -1)) == 4 and not bool(recovered_data.get("dungeon_done", true)), "backup dungeon checkpoint recovered")
	_expect(state._repair_primary(recovered_data), "primary repaired from backup")
	_expect(int(_read_json(TEST_PATH).get("pearls", -1)) == 17, "repaired primary is readable")

	# Corrupt critical progression falls back to the rich clean backup.
	_write_text(TEST_PATH, JSON.stringify({
		"schema_version": SaveState.SCHEMA_VERSION,
		"pearls": "not a number",
		"future_payload": {"kept": "yes"},
	}))
	var typed_recovery: Dictionary = state._select_load_candidate()
	_expect(String(typed_recovery.get("path", "")) == TEST_PATH + ".bak", "wrong known type falls back to clean backup")

	# A syntactically valid but incomplete schema document must not beat a
	# complete backup and erase all omitted progress on the next write.
	_write_text(TEST_PATH, JSON.stringify({
		"schema_version": SaveState.SCHEMA_VERSION,
		"music": true,
	}))
	var incomplete_recovery: Dictionary = state._select_load_candidate()
	_expect(String(incomplete_recovery.get("path", "")) == TEST_PATH + ".bak", "incomplete primary falls back to complete backup")

	# A bad preference is repaired field-by-field while newer progression wins.
	var preference_damage: Dictionary = _read_json(TEST_PATH + ".bak")
	preference_damage["pearls"] = 44
	preference_damage["quality"] = 123
	_write_text(TEST_PATH, JSON.stringify(preference_damage))
	var preference_recovery: Dictionary = state._select_load_candidate()
	var preference_data: Dictionary = preference_recovery.get("data", {})
	_expect(String(preference_recovery.get("path", "")) == TEST_PATH, "noncritical damage keeps newer primary")
	_expect(int(preference_data.get("pearls", -1)) == 44, "noncritical repair preserves newer progress")

	# Opening an N+1 save in N is read-only: unknown data and the schema claim
	# survive even if gameplay requests a write — and the disabled write must
	# REPORT failure so main.gd's save_dirty/retry path can see it.
	var future_data: Dictionary = preference_data.duplicate(true)
	future_data["schema_version"] = SaveState.SCHEMA_VERSION + 4
	future_data["future_only_progress"] = {"chapter": 9}
	_write_text(TEST_PATH, JSON.stringify(future_data))
	var future_candidate: Dictionary = state._select_load_candidate()
	_expect(bool(future_candidate.get("future", false)), "future schema recognized")
	var future_text_before := _read_text(TEST_PATH)
	main.save_data = future_data
	main.pearl_count = 99
	var fresh_state := SaveState.new(main, TEST_PATH)
	_expect(not fresh_state.write_save(), "write against a future primary reports failure")
	_expect(_read_text(TEST_PATH) == future_text_before, "fresh writer leaves future schema byte-for-byte untouched")

	# A future BACKUP outranks an older clean temp even when the primary is
	# corrupt; candidate order must never downgrade a newer schema.
	_write_text(TEST_PATH, "{broken")
	var current_temp: Dictionary = preference_data.duplicate(true)
	current_temp["schema_version"] = SaveState.SCHEMA_VERSION
	_write_text(TEST_PATH + ".tmp", JSON.stringify(current_temp))
	_write_text(TEST_PATH + ".bak", JSON.stringify(future_data))
	var future_recovery: Dictionary = fresh_state._select_load_candidate()
	_expect(bool(future_recovery.get("future", false)) and String(future_recovery.get("path", "")) == TEST_PATH + ".bak", "future backup outranks older clean temp")

	# But a stale future-versioned TEMP/sidecar beside a current primary must
	# not hijack selection or silently disable this build's writes — that would
	# make every save a no-op after one visit from a newer dev APK.
	_cleanup()
	main.save_data = {}
	main.pearl_count = 7
	var stale_state := SaveState.new(main, TEST_PATH)
	_expect(stale_state.write_save(), "baseline write succeeds")
	var stale_future: Dictionary = _read_json(TEST_PATH)
	stale_future["schema_version"] = SaveState.SCHEMA_VERSION + 2
	_write_text(TEST_PATH + ".tmp0", JSON.stringify(stale_future))
	main.pearl_count = 8
	var stale_writer := SaveState.new(main, TEST_PATH)
	_expect(stale_writer.write_save(), "stale future temp does not disable writes")
	_expect(int(_read_json(TEST_PATH).get("pearls", -1)) == 8, "write landed despite stale future temp")
	var stale_candidate: Dictionary = stale_writer._select_load_candidate()
	_expect(String(stale_candidate.get("path", "")) == TEST_PATH and not bool(stale_candidate.get("future", false)), "stale future temp does not hijack load selection")

	_cleanup()
	main.free()
	if failures == 0:
		print("SAVE_RECOVERY|RESULT: ALL OK")
		quit()
	else:
		print("SAVE_RECOVERY|RESULT: %d FAIL" % failures)
		quit(1)

func _expect(condition: bool, label: String) -> void:
	if condition:
		print("SAVE_RECOVERY|OK: ", label)
	else:
		failures += 1
		print("SAVE_RECOVERY|FAIL: ", label)

func _read_json(path: String) -> Dictionary:
	if not FileAccess.file_exists(path):
		return {}
	var file: FileAccess = FileAccess.open(path, FileAccess.READ)
	if file == null:
		return {}
	var parsed: Variant = JSON.parse_string(file.get_as_text())
	file.close()
	if typeof(parsed) == TYPE_DICTIONARY:
		var dictionary: Dictionary = parsed
		return dictionary
	return {}

func _read_text(path: String) -> String:
	if not FileAccess.file_exists(path):
		return ""
	var file: FileAccess = FileAccess.open(path, FileAccess.READ)
	if file == null:
		return ""
	var text: String = file.get_as_text()
	file.close()
	return text

func _write_text(path: String, text: String) -> void:
	var file: FileAccess = FileAccess.open(path, FileAccess.WRITE)
	if file == null:
		failures += 1
		print("SAVE_RECOVERY|FAIL: could not write fixture ", path)
		return
	file.store_string(text)
	file.close()

func _cleanup() -> void:
	for path: String in TEST_FILES:
		if FileAccess.file_exists(path):
			DirAccess.remove_absolute(ProjectSettings.globalize_path(path))
