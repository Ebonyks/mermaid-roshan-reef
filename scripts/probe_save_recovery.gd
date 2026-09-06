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
	TEST_PATH + ".before_new_game",
	TEST_PATH + ".before_new_game.tmp",
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
	main.opera_stars = 0x4211
	main.opera_progress = 16
	main.touch_mode = main.TOUCH_MODE_CLASSIC
	var state: SaveState = SaveState.new(main, TEST_PATH)
	state.write_save()
	_expect(FileAccess.file_exists(TEST_PATH), "primary created")
	_expect(FileAccess.file_exists(TEST_PATH + ".bak"), "backup created on first write")
	var first: Dictionary = _read_json(TEST_PATH)
	_expect(int(first.get("schema_version", 0)) == SaveState.SCHEMA_VERSION, "schema version added")
	_expect(first.get("future_payload", {}) == {"kept": "yes"}, "unknown dictionary preserved")
	_expect(String(first.get("touch_mode", "")) == "classic", "Classic touch preference serialized")
	var future_list: Array = first.get("future_list", [])
	_expect(future_list.size() == 3 and int(future_list[0]) == 1 and int(future_list[2]) == 3, "unknown array preserved")
	_expect(int(first.get("dungeon_progress", -1)) == 4 and not bool(first.get("dungeon_done", true)), "dungeon checkpoint serialized")
	_expect(int(first.get("opera_stars", -1)) == 0x4211, "raw sparse Opera mask serialized")
	_expect(int(first.get("opera_progress", -1)) == 1, "Opera progress counts only live bits")

	main.pearl_count = 33
	main.dungeon_progress = 99   # corrupt/out-of-range runtime state clamps at the ten-room boundary
	main.dungeon_done = true
	main.opera_stars = 0xFFFF
	main.opera_progress = 0
	main.touch_mode = main.TOUCH_MODE_HYBRID
	state.write_save()
	var second: Dictionary = _read_json(TEST_PATH)
	var previous: Dictionary = _read_json(TEST_PATH + ".bak")
	_expect(int(second.get("pearls", -1)) == 33, "new primary installed")
	_expect(int(previous.get("pearls", -1)) == 17, "backup retains last known-good primary")
	_expect(String(second.get("touch_mode", "")) == "hybrid", "Hybrid touch preference serialized")
	_expect(String(previous.get("touch_mode", "")) == "classic", "touch rollback preference survives in backup")
	_expect(second.get("future_payload", {}) == {"kept": "yes"}, "unknown key survives another write")
	_expect(int(second.get("dungeon_progress", -1)) == 10 and bool(second.get("dungeon_done", false)), "dungeon completion serialized and clamped")
	_expect(int(second.get("opera_stars", -1)) == 0xFFFF, "retired Opera bits survive a rewrite")
	_expect(int(second.get("opera_progress", -1)) == 13, "complete Opera progress is thirteen live careers")
	_expect(int(previous.get("opera_stars", -1)) == 0x4211 and int(previous.get("opera_progress", -1)) == 1, "Opera backup retains prior sparse mask semantics")
	var reload_state: SaveState = SaveState.new(main, TEST_PATH)
	var reload_candidate: Dictionary = reload_state._select_load_candidate()
	var reload_data: Dictionary = reload_candidate.get("data", {})
	_expect(int(reload_data.get("dungeon_progress", -1)) == 10 and bool(reload_data.get("dungeon_done", false)), "fresh reader reloads dungeon completion")
	_expect(int(reload_data.get("opera_stars", -1)) == 0xFFFF and int(reload_data.get("opera_progress", -1)) == 13, "fresh reader reloads effective Opera completion")
	_expect(String(reload_data.get("touch_mode", "")) == "hybrid", "fresh reader reloads touch preference")
	var teacher_default: Dictionary = state._normalise_save({})
	_expect((teacher_default.get("teacher_learning_progress", {}) as Dictionary).get(
		"version", 0) == 1, "old save receives additive Teacher learning defaults")
	_expect(teacher_default.get("teacher_lesson_checkpoint", {"bad": true}) == {},
		"old save receives empty Teacher lesson checkpoint")
	var teacher_raw := {
		"teacher_learning_progress": {"version": 1, "kinds": {
			"pattern": {"tier": 2, "clean_successes": 1, "rounds": 9}}},
		"teacher_lesson_checkpoint": {"version": 1, "phase_index": 2,
			"mechanic": {"kind": "add", "choices": [2, 3, 4]},
			"future_note": "keep"},
		"teacher_neighbor": {"kept": true},
	}
	var teacher_normalised: Dictionary = state._normalise_save(teacher_raw)
	var pre_teacher_primary := _read_text(TEST_PATH)
	var pre_teacher_backup := _read_text(TEST_PATH + ".bak")
	main.save_data = teacher_normalised
	state.write_save()
	var teacher_disk: Dictionary = _read_json(TEST_PATH)
	var teacher_progress: Dictionary = teacher_disk.get("teacher_learning_progress", {})
	var teacher_kinds: Dictionary = teacher_progress.get("kinds", {})
	var teacher_pattern: Dictionary = teacher_kinds.get("pattern", {})
	var teacher_checkpoint: Dictionary = teacher_disk.get("teacher_lesson_checkpoint", {})
	var teacher_mechanic: Dictionary = teacher_checkpoint.get("mechanic", {})
	var teacher_choices: Array = teacher_mechanic.get("choices", [])
	_expect(int(teacher_pattern.get("tier", -1)) == 2
		and int(teacher_pattern.get("rounds", -1)) == 9,
		"Teacher learning progress survives JSON disk round-trip")
	_expect(int(teacher_checkpoint.get("phase_index", -1)) == 2
		and String(teacher_mechanic.get("kind", "")) == "add"
		and teacher_choices.size() == 3 and int(teacher_choices[0]) == 2
		and int(teacher_choices[2]) == 4,
		"Teacher lesson checkpoint survives JSON disk round-trip")
	_expect(String(teacher_checkpoint.get("future_note", "")) == "keep"
		and teacher_disk.get("teacher_neighbor", {}) == {"kept": true},
		"Teacher save normalization preserves unrelated keys")
	for invalid_checkpoint: Variant in ["bad", {"version": 2,
			"phase_index": 1, "mechanic": {}}, {"version": 1,
			"phase_index": 1.5, "mechanic": {}}, {"version": 1,
			"phase_index": 1, "mechanic": []}]:
		var healed: Dictionary = state._normalise_save({
			"teacher_lesson_checkpoint": invalid_checkpoint,
			"teacher_neighbor": {"kept": true}})
		_expect(healed.get("teacher_lesson_checkpoint", {"bad": true}) == {}
			and healed.get("teacher_neighbor", {}) == {"kept": true},
			"invalid Teacher checkpoint heals without losing unrelated keys")
	_write_text(TEST_PATH, pre_teacher_primary)
	_write_text(TEST_PATH + ".bak", pre_teacher_backup)
	main.save_data = reload_data

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
	preference_damage["touch_mode"] = 123
	_write_text(TEST_PATH, JSON.stringify(preference_damage))
	var preference_recovery: Dictionary = state._select_load_candidate()
	var preference_data: Dictionary = preference_recovery.get("data", {})
	_expect(String(preference_recovery.get("path", "")) == TEST_PATH, "noncritical damage keeps newer primary")
	_expect(int(preference_data.get("pearls", -1)) == 44, "noncritical repair preserves newer progress")
	_expect(String(preference_data.get("touch_mode", "")) == "hybrid", "invalid touch preference repairs to Hybrid")

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

	# A save missing a key that a NEWER build added (schema growth) must stay
	# clean: completeness is judged against the frozen core quartet, so the
	# missing key just gets its default instead of demoting every existing
	# save to the salvage path on first launch.
	_cleanup()
	main.save_data = {}
	main.pearl_count = 12
	var core_state := SaveState.new(main, TEST_PATH)
	_expect(core_state.write_save(), "core-quartet fixture written")
	var trimmed: Dictionary = _read_json(TEST_PATH)
	trimmed.erase("stickers")   # stands in for any key a later build adds
	trimmed.erase("critters")   # real case: saves from before the Critter Book
	trimmed.erase("touch_mode")   # pre-touch-mode save defaults safely
	_write_text(TEST_PATH, JSON.stringify(trimmed))
	var older_backup: Dictionary = _read_json(TEST_PATH + ".bak")
	older_backup["pearls"] = 1   # a demotion to the backup would visibly roll progress back
	older_backup["save_generation"] = 0
	_write_text(TEST_PATH + ".bak", JSON.stringify(older_backup))
	var core_candidate: Dictionary = core_state._select_load_candidate()
	_expect(bool(core_candidate.get("clean", false)) and String(core_candidate.get("path", "")) == TEST_PATH, "save missing a newly-added key is still clean")
	var core_data: Dictionary = core_candidate.get("data", {})
	_expect(core_data.get("stickers") is Dictionary, "missing key restored with its default")
	_expect(core_data.get("critters") is Dictionary, "pre-Critter-Book save defaults critters without demotion")
	_expect(String(core_data.get("touch_mode", "")) == "hybrid", "pre-touch-mode save defaults to Hybrid")
	_expect(int(core_data.get("pearls", -1)) == 12, "no demotion: newest progress kept")

	# The optional Geologist checkpoint is additive: old saves get an empty
	# checkpoint, valid partial work survives a real JSON write/read, and a bad
	# checkpoint heals locally without discarding unrelated future data.
	_expect(core_data.get("opera_geology_checkpoint", {"bad": true}) == {},
		"pre-Geologist save defaults geology checkpoint to empty")
	_cleanup()
	var geology_checkpoint := {
		"version": 1,
		"phase_index": 1,
		"mechanic": {
			"version": 1,
			"mode": "geology_fossil",
			"cleared": [0, 3, 11, 24],
			"snapped": [false, false, false],
		},
		"future_checkpoint_note": "keep",
	}
	main.save_data = {
		"opera_geology_checkpoint": geology_checkpoint,
		"geology_neighbor_key": {"kept": true},
	}
	var geology_state := SaveState.new(main, TEST_PATH)
	_expect(geology_state.write_save(), "Geologist checkpoint fixture written")
	var geology_disk: Dictionary = _read_json(TEST_PATH)
	var geology_disk_checkpoint: Dictionary = geology_disk.get(
		"opera_geology_checkpoint", {})
	var geology_disk_mechanic: Dictionary = geology_disk_checkpoint.get(
		"mechanic", {})
	var geology_disk_cleared: Array = geology_disk_mechanic.get("cleared", [])
	_expect(int(geology_disk_checkpoint.get("phase_index", -1)) == 1
		and String(geology_disk_mechanic.get("mode", "")) == "geology_fossil"
		and geology_disk_cleared.size() == 4
		and int(geology_disk_cleared[2]) == 11,
		"valid Geologist checkpoint survives JSON disk round-trip")
	_expect(String(geology_disk_checkpoint.get("future_checkpoint_note", "")) == "keep"
		and geology_disk.get("geology_neighbor_key", {}) == {"kept": true},
		"checkpoint and save preserve unrelated keys")
	var invalid_checkpoints: Array = [
		"wrong top type",
		{"version": 2, "phase_index": 1, "mechanic": {}},
		{"version": "1", "phase_index": 1, "mechanic": {}},
		{"version": 1, "phase_index": {}, "mechanic": {}},
		{"version": 1, "phase_index": NAN, "mechanic": {}},
		{"version": 1, "phase_index": 1.5, "mechanic": {}},
		{"version": 1, "phase_index": 5, "mechanic": {}},
		{"version": 1, "phase_index": 1, "mechanic": []},
	]
	for invalid_checkpoint: Variant in invalid_checkpoints:
		var damaged := {
			"opera_geology_checkpoint": invalid_checkpoint,
			"geology_neighbor_key": {"kept": true},
		}
		var healed: Dictionary = geology_state._normalise_save(damaged)
		_expect(healed.get("opera_geology_checkpoint", {"bad": true}) == {},
			"invalid Geologist checkpoint schema heals to empty")
		_expect(healed.get("geology_neighbor_key", {}) == {"kept": true},
			"invalid checkpoint healing retains unrelated key")

	# New Game archives the complete current document through a checked temp
	# rename. Restoring it must preserve unknown fields and outrank the fresh
	# post-reset .bak by generation, even if the process is killed mid-restore.
	_cleanup()
	main.save_data = {"archive_unknown": {"kept": true}}
	main.pearl_count = 23
	main.plays = 2
	var archive_state: SaveState = SaveState.new(main, TEST_PATH)
	_expect(archive_state.write_save(), "archive fixture baseline write succeeds")
	var archived_generation: int = int(
		_read_json(TEST_PATH).get("save_generation", 0))
	_expect(archive_state.start_new_game(), "New Game installs a fresh save")
	var archive_path: String = TEST_PATH + ".before_new_game"
	var archived: Dictionary = _read_json(archive_path)
	_expect(archived.get("archive_unknown", {}) == {"kept": true},
		"before-New-Game archive preserves unknown fields")
	_expect(int(archived.get("pearls", -1)) == 23
		and int(archived.get("save_generation", 0)) == archived_generation,
		"before-New-Game archive keeps the prior generation")
	var fresh_generation: int = int(_read_json(TEST_PATH + ".bak").get(
		"save_generation", 0))
	_expect(fresh_generation > archived_generation,
		"fresh New Game backup is newer than the archive")
	_write_text(archive_path, "{broken archive")
	_expect(not archive_state.restore_new_game_archive(),
		"corrupt before-New-Game archive is refused")
	_write_text(archive_path, JSON.stringify(archived))
	_expect(archive_state.restore_new_game_archive(),
		"clean before-New-Game archive restores transactionally")
	var restored: Dictionary = _read_json(TEST_PATH)
	_expect(restored.get("archive_unknown", {}) == {"kept": true}
		and int(restored.get("pearls", -1)) == 23,
		"archive restore keeps progress and unknown fields")
	_expect(int(restored.get("save_generation", 0)) > fresh_generation,
		"archive restore generation outranks the fresh backup")

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
