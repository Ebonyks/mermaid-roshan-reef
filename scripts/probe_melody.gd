extends SceneTree
## Focused shipping contract for Daddy Mermaid's seven-note Canvas theater.
##
## This probe intentionally enters through the Reef friend route and sends
## production Viewport input. It proves that the full-screen activity is
## child-readable, agency-gated, teardown-safe, persistently ranked, and unable
## to touch the normal save while the probe runs.

const InteractionAffordanceLogic = preload(
	"res://scripts/interaction_affordance.gd")

const VIEWPORT_SIZE := Vector2i(1280, 720)
const TALL_PHONE_SIZE := Vector2i(1280, 800)
const TOUCH_INDEX := 71
const PROBE_SAVE_URI := "user://probe_melody_canvas_save.json"
const SAVE_SUFFIXES: Array[String] = [
	"", ".tmp0", ".tmp1", ".tmp", ".old", ".bak", ".bak.tmp", ".bak.old",
]

const MASTER_PATH := \
	"res://assets_src/sky_lagoon/masters/sky_lagoon_panorama_master_v5_hd_3x1.png"
const MASTER_SHA256 := \
	"017532ae864e534d9b356472e2e29150855ede6583a7f63f02f0401d28c7be41"
const TILE_PATHS: Array[String] = [
	"res://assets/flats/sky_lagoon/main/flat_sky_lagoon_main_panorama_v5_tile_r0_c2.png",
	"res://assets/flats/sky_lagoon/main/flat_sky_lagoon_main_panorama_v5_tile_r0_c3.png",
	"res://assets/flats/sky_lagoon/main/flat_sky_lagoon_main_panorama_v5_tile_r1_c2.png",
	"res://assets/flats/sky_lagoon/main/flat_sky_lagoon_main_panorama_v5_tile_r1_c3.png",
]
const TILE_NODE_NAMES: Array[String] = [
	"SkyLagoonBackdrop_r0_c2", "SkyLagoonBackdrop_r0_c3",
	"SkyLagoonBackdrop_r1_c2", "SkyLagoonBackdrop_r1_c3",
]
const TILE_SOURCE_RECTS: Array[Rect2i] = [
	Rect2i(0, 0, 1024, 1024),
	Rect2i(1024, 0, 1024, 1024),
	Rect2i(0, 1024, 1024, 1024),
	Rect2i(1024, 1024, 1024, 1024),
]
const TILE_SHA256: Array[String] = [
	"a5e0dc1e71031ade14059722885bf7905d88f3ea45e9b04e5994cb09ece88850",
	"b423c7c320377e15a38d684d4cec4499c81fa9a31e20bdf4d7dbf051d63c1959",
	"2c095349af8d05bb11e43f2115406ce55f583eb885f2abf5b7b4faf7cb8b1e28",
	"1f84c75cdfc85923b2a18011e50ac60e78145ed6a9703f7c99ae26592bb6edb7",
]
const DADDY_PATH := "res://assets/characters/stickers/daddy.png"
const DADDY_SHA256 := \
	"402024ac72c5365aae8562d422b9f888a6f5cdef7b6539409747e8f965cd0122"
const ROSHAN_PATH := "res://assets/opera/worlds/actors/roshan_popstar.png"
const ROSHAN_SHA256 := \
	"2d7d45ee94bab0adbacb4331461942dd5ba14d20327ed7985945575adbf6d523"
const VOICE_PATH := "res://assets/audio/voices/roshan_op_popstar_rhythm.ogg"
const VOICE_SHA256 := \
	"b8566e49b135e6271e09f6c969af6d8362a8f6582c9c28d93b991741d562b5eb"
const OBJECTIVE := "Tap each rainbow note in the green!"
const EXPECTED_COLORS: Array[Color] = [
	Color(1.0, 0.24, 0.28),
	Color(1.0, 0.54, 0.18),
	Color(1.0, 0.86, 0.24),
	Color(0.30, 0.84, 0.42),
	Color(0.24, 0.68, 0.96),
	Color(0.39, 0.38, 0.88),
	Color(0.72, 0.40, 0.90),
]
const EXPECTED_STAGE_NODES: Array[String] = [
	"ScenicBackcloth",
	"SkyLagoonBackdrop_r0_c2", "SkyLagoonBackdrop_r0_c3",
	"SkyLagoonBackdrop_r1_c2", "SkyLagoonBackdrop_r1_c3",
	"OperaProscenium", "StageFootlights", "StageStar",
	"DaddyGuide", "PopstarRoshan", "TimingZone", "VisualPointer",
]


class CountingAudioDirector:
	extends AudioDirector

	var requests: Array[Dictionary] = []
	var messages: Array[Dictionary] = []

	func show_msg(who: String, txt: String, vo: String = "talk") -> void:
		messages.append({"who": who, "text": txt, "voice": vo})
		super.show_msg(who, txt, vo)

	func _say(speaker: String, event: String = "",
			min_gap: float = 0.0) -> void:
		requests.append({
			"speaker": speaker,
			"event": event,
			"min_gap": min_gap,
		})
		super._say(speaker, event, min_gap)


var main: ReefMain
var melody: MelodyGame
var daddy_friend: Dictionary = {}
var daddy_index := -1
var audio_audit: CountingAudioDirector
var bad := 0
var normal_save_path := ""
var probe_save_path := ""
var normal_before: Array[Dictionary] = []
var first_note_point := Vector2.ZERO
var chime_tuning_before: Dictionary = {}
var texture_alpha_cache: Dictionary = {}


func _init() -> void:
	call_deferred("_run")


func _run() -> void:
	seed(20260813)
	Engine.time_scale = 4.0
	get_root().mode = Window.MODE_WINDOWED
	get_root().size = VIEWPORT_SIZE

	normal_save_path = ProjectSettings.globalize_path("user://reef_save.json")
	probe_save_path = ProjectSettings.globalize_path(PROBE_SAVE_URI)
	# Capture every document SaveState can select or leave behind before the
	# scene exists. This must remain above instantiate()/add_child(): _ready can
	# load, repair, back up, or flush a save.
	normal_before = _artifact_fingerprints(normal_save_path)
	_check("probe save is distinct from the child's normal save",
		probe_save_path != normal_save_path)
	_check("normal primary, backup, and every recovery sidecar are fingerprinted before boot",
		normal_before.size() == SAVE_SUFFIXES.size()
		and SAVE_SUFFIXES == [
			"", ".tmp0", ".tmp1", ".tmp", ".old", ".bak", ".bak.tmp", ".bak.old",
		])
	_check("stale probe-only save artifacts are removed",
		_remove_probe_save_artifacts())
	_check_asset_contract()

	var packed := load("res://scenes/main.tscn") as PackedScene
	main = packed.instantiate() as ReefMain
	main._save_state = SaveState.new(main, probe_save_path)
	get_root().add_child(main)
	await _frames(3)
	if main.intro_active:
		main._skip_intro()
	await _frames(8)
	main._set_touch_mode(main.TOUCH_MODE_HYBRID, false)
	main._apply_quality("speedy")
	await _frames(2)

	_find_daddy_route()
	_check("fresh isolated save starts Daddy and Melody unawarded",
		not daddy_friend.is_empty()
		and not bool(daddy_friend.get("found", false))
		and not bool(daddy_friend.get("won", false))
		and int(main.medals.get("melody", 0)) == 0)
	if daddy_friend.is_empty():
		await _finish()
		return

	# Discovery is the child's real Reef route. Proximity may reveal Daddy and
	# the PLAY affordance, but Hybrid must still wait for an explicit activation.
	var daddy_node: Variant = daddy_friend.get("node")
	main.player.position = daddy_node.position
	main.player.position.x += 3.0
	main.player.vel *= 0.0
	await _frames(10)
	_check("approaching Daddy discovers him without auto-starting Melody",
		bool(daddy_friend.get("found", false)) and main.game == "")
	main._populate_touch_interactables()
	var daddy_target := _touch_target("friend:%d" % daddy_index)
	_check("Daddy exposes the child-facing PLAY plot target",
		not daddy_target.is_empty()
		and String(daddy_target.get("label", "")) == "Daddy Mermaid"
		and String(daddy_target.get("verb", "")) == "PLAY"
		and String(daddy_target.get("affordance_kind", "")) == \
			InteractionAffordanceLogic.PLOT
		and int(daddy_target.get("payload", -1)) == daddy_index)
	var reef_camera: Variant = main.player.cam
	var daddy_screen_point := Vector2(-1.0, -1.0)
	if reef_camera != null:
		daddy_screen_point = reef_camera.unproject_position(daddy_node.global_position)
	_push_touch(daddy_screen_point, true, TOUCH_INDEX - 2)
	_push_touch(daddy_screen_point, false, TOUCH_INDEX - 2)
	await process_frame
	_check("first real one-finger Daddy tap focuses PLAY without launching",
		daddy_screen_point.x >= 0.0 and daddy_screen_point.y >= 0.0
		and main.touch_focus_id == "friend:%d" % daddy_index
		and main.touch_focus_ready and main.game == "")

	# Materialize the speaker card before lifecycle baselines, then install an
	# observing AudioDirector so the production show_msg -> _say path is exact.
	main._flash_speaker_icon("roshan")
	main.clear_dialogue()
	await process_frame
	audio_audit = CountingAudioDirector.new(main)
	main._audio_dir = audio_audit
	main.said_cool.erase("roshan_op_popstar_rhythm")
	audio_audit.requests.clear()
	audio_audit.messages.clear()
	var voice_before: int = main.voice_i
	var direct_baseline: Dictionary = _direct_child_ids()
	var game_nodes_baseline: Array[int] = _game_node_ids()
	var controls_baseline: Dictionary = main.touch_control_blocks.duplicate(true)
	var progress_baseline: Dictionary = _progress_snapshot()
	var route_position := main.player.position
	var route_environment: Variant = main.we_node.environment
	var route_track: String = main.cur_track
	var route_music: Dictionary = _music_context()
	chime_tuning_before = _chime_tuning()
	_check("shared success chime exposes a restorable volume and pitch baseline",
		not chime_tuning_before.is_empty())

	# The second real one-finger tap follows the child-facing focus -> PLAY
	# vocabulary and reaches _fade_cut through the production touch router.
	_push_touch(daddy_screen_point, true, TOUCH_INDEX - 1)
	_push_touch(daddy_screen_point, false, TOUCH_INDEX - 1)
	_check("Daddy PLAY route synchronously enters Melody",
		main.game == "melody" and main.g.get("fr", {}) == daddy_friend)
	melody = main._game_obj("melody", MelodyGame) as MelodyGame
	var first_layer: CanvasLayer = melody.active_layer()
	var first_surface: Node2D = melody.surface()
	first_note_point = melody.active_note_screen_point()
	_check_entry_contract(first_layer, first_surface, direct_baseline,
		game_nodes_baseline, controls_baseline, route_position,
		route_environment, route_track)
	_check_voice_contract(voice_before)

	# A complete tap made beneath the synchronous black reveal may never score,
	# leave a stale latch, or consume the first deliberate post-reveal gesture.
	var first_progress := melody.progress_count()
	_check("entry starts under the production reveal fade",
		main.fade_rect != null and main.fade_rect.modulate.a > 0.02)
	_push_touch(first_note_point, true, TOUCH_INDEX)
	_push_touch(first_note_point, false, TOUCH_INDEX)
	_check("quick press and release wholly under fade make no progress",
		main.fade_rect.modulate.a > 0.02
		and melody.progress_count() == first_progress
		and not bool(melody.audit_snapshot().get("input_down", true)))
	await _wait_for_fade_clear()
	_check_opening_objective_delivery(first_surface)
	await _wait_for_green(true)
	_check("fade tap release clears its neutral latch before fresh input",
		not bool(melody.audit_snapshot().get("blocked_until_release", true)))
	var fresh_point: Vector2 = melody.active_note_screen_point()
	_push_touch(fresh_point, true, TOUCH_INDEX + 1)
	_push_touch(fresh_point, false, TOUCH_INDEX + 1)
	await process_frame
	_check("first fresh green tap after a swallowed fade tap scores exactly once",
		melody.progress_count() == first_progress + 1)
	main.clear_dialogue()
	await _check_rendered_stage_contract(first_surface)

	await _check_tick_and_stage_motion()
	await _exercise_negative_and_neutral_input()
	_check("partial deliberate input reaches exactly six notes before leave",
		melody.progress_count() == 6 and main.game == "melody")

	var first_layer_ref: WeakRef = weakref(first_layer)
	var first_surface_ref: WeakRef = weakref(first_surface)
	var expected_after_leave: Dictionary = _direct_child_ids()
	if first_layer != null:
		expected_after_leave.erase(first_layer.get_instance_id())
	await _leave_through_real_pause_gear()
	print("MELODY|LEAVE_FACTS|game=", main.game,
		"|g_empty=", main.g.is_empty(),
		"|active_layers=", _active_layer_count(),
		"|direct_match=", _direct_child_ids() == expected_after_leave,
		"|game_nodes_match=", _game_node_ids() == game_nodes_baseline,
		"|controls_match=", main.touch_control_blocks == controls_baseline,
		"|world_controls=", main.touch_ui.world_controls_enabled,
		"|position_match=", main.player.position.is_equal_approx(route_position),
		"|environment_match=", main.we_node.environment == route_environment,
		"|track=", main.cur_track, "|expected_track=", route_track,
		"|music_match=", _music_context_matches(route_music),
		"|chime_match=", _chime_tuning_restored())
	_check("neutral pause-menu leave synchronously detaches only Melody",
		main.game == "" and main.g.is_empty()
		and melody.active_layer() == null and melody.surface() == null
		and melody.stage_root() == null and melody.active_note_id() == -1
		and melody.audit_snapshot().is_empty()
		and _active_layer_count() == 0
		and _direct_child_ids() == expected_after_leave
		and _game_node_ids() == game_nodes_baseline
		and main.touch_control_blocks == controls_baseline
		and main.touch_ui.world_controls_enabled
		and main.player.position.is_equal_approx(route_position)
		and main.we_node.environment == route_environment
		and main.cur_track == route_track
		and _music_context_matches(route_music)
		and _chime_tuning_restored())
	_check("neutral leave awards nothing",
		_progress_snapshot() == progress_baseline)
	melody.stage_close()
	melody.stage_close()
	_check("closed Melody teardown is synchronously idempotent",
		melody.active_layer() == null and melody.surface() == null
		and melody.active_note_id() == -1
		and melody.audit_snapshot().is_empty())
	await _frames(2)
	_check("neutral teardown frees the complete Canvas subtree",
		first_layer_ref.get_ref() == null and first_surface_ref.get_ref() == null)
	await _exercise_system_loss_and_paused_census(progress_baseline)

	# Re-entry begins while a real world touch is still held at the deterministic
	# first-note point. The activity must demand its release and then seven new
	# one-finger gestures in red-through-violet order.
	_push_key(KEY_SPACE, true, 5)
	main.notification(Node.NOTIFICATION_APPLICATION_FOCUS_OUT)
	main.notification(Node.NOTIFICATION_APPLICATION_FOCUS_IN)
	_push_pad(JOY_BUTTON_A, true, 6)
	main._forget_melody_pad_device(6)
	_push_touch(first_note_point, true, TOUCH_INDEX + 1)
	var bronze_route_position := main.player.position
	var bronze_route_environment: Variant = main.we_node.environment
	var bronze_route_track: String = main.cur_track
	var bronze_route_music: Dictionary = _music_context()
	var bronze_direct_baseline: Dictionary = _direct_child_ids()
	main._activate_touch_interactable("friend:%d" % daddy_index, daddy_index)
	melody = main._game_obj("melody", MelodyGame) as MelodyGame
	var bronze_layer: CanvasLayer = melody.active_layer()
	var bronze_layer_ref: WeakRef = weakref(bronze_layer)
	_check("re-entry replaces the closed stage with one fresh 0-of-7 layer",
		main.game == "melody" and _active_layer_count() == 1
		and melody.progress_count() == 0 and melody.note_count() == 7
		and melody.active_note_id() == 0
		and _only_layer_added(bronze_direct_baseline, bronze_layer))
	await _wait_for_fade_clear()
	await _wait_for_green(true)
	_push_key(KEY_SPACE, false, 5)
	_push_pad(JOY_BUTTON_A, false, 6)
	_push_touch(melody.active_note_screen_point(), false, TOUCH_INDEX + 2)
	_push_mouse(melody.active_note_screen_point(), false, 4)
	await process_frame
	_check("reset key/pad plus wrong finger/mouse cannot clear the held touch",
		melody.progress_count() == 0
		and bool(melody.audit_snapshot().get(
			"blocked_until_release", false)))
	_push_touch(melody.active_note_screen_point(), false, TOUCH_INDEX + 1)
	await process_frame
	_check("pre-entry held touch cannot become the first note",
		melody.progress_count() == 0
		and not bool(melody.audit_snapshot().get(
			"blocked_until_release", true)))

	var save_before_bronze: int = main.save_generation
	var bronze_run: Dictionary = await _complete_ordered_notes(
		["touch", "touch", "touch", "touch", "touch", "touch", "touch"],
		true, true)
	await _frames(3)
	var bronze_save: Dictionary = _read_probe_save()
	_check("seven fresh direct touch gestures complete red through violet",
		bronze_run.get("ids", []) == [0, 1, 2, 3, 4, 5, 6]
		and _colors_equal(bronze_run.get("colors", []) as Array,
			EXPECTED_COLORS)
		and bool(bronze_run.get("all_armed", false))
		and bool(bronze_run.get("duplicate_exact_once", false)))
	_check("deliberately slow first win awards one bronze medal and one trophy",
		main.game == "" and bool(daddy_friend.get("won", false))
		and main.trophies == int(progress_baseline["trophies"]) + 1
		and int(main.medals.get("melody", 0)) == MedalSystem.BRONZE
		and int((bronze_save.get("medals", {}) as Dictionary).get(
			"melody", 0)) == MedalSystem.BRONZE
		and bool((bronze_save.get("won", {}) as Dictionary).get(
			"Daddy Mermaid", false)))
	_check("bronze upgrade and terminal persistence each write exactly once",
		main.save_generation == save_before_bronze + 2)
	print("MELODY|WIN_RETURN_FACTS|terminal_position_match=",
		bronze_run.get("terminal_position") == bronze_route_position,
		"|environment_match=", main.we_node.environment == bronze_route_environment,
		"|track=", main.cur_track, "|expected_track=", bronze_route_track,
		"|music=", _music_context(), "|expected_music=", bronze_route_music)
	_check("first win restores its exact Reef return context while the shared reward owns fanfare audio",
		bronze_run.get("terminal_position") == bronze_route_position
		and bronze_run.get("terminal_environment") == bronze_route_environment
		and String(bronze_run.get("terminal_track", "")) == bronze_route_track
		and _music_context_values_match(
			bronze_run.get("terminal_music", {}) as Dictionary,
			bronze_route_music)
		and main.we_node.environment == bronze_route_environment
		and main.cur_track == bronze_route_track
		and _music_context_matches(bronze_route_music))
	_check("first win synchronously clears Canvas and controls",
		melody.active_layer() == null and _active_layer_count() == 0
		and _game_node_ids() == game_nodes_baseline
		and main.touch_control_blocks == controls_baseline
		and main.touch_ui.world_controls_enabled)
	await _frames(2)
	_check("first-win layer is freed after synchronous detach",
		bronze_layer_ref.get_ref() == null)

	# Let the first reward layers expire. Hold keyboard and pad actions across
	# the next production fade: neither release may count, and both controls must
	# still work on later fresh presses.
	await _frames(80)
	chime_tuning_before = _chime_tuning()
	_check("replay captures the settled shared-fanfare chime tuning exactly",
		not chime_tuning_before.is_empty())
	var trophy_before_replay: int = main.trophies
	var star_before_replay: Variant = daddy_friend.get("star")
	_push_key(KEY_SPACE, true)
	_push_pad(JOY_BUTTON_A, true)
	var replay_route_position := main.player.position
	var replay_route_environment: Variant = main.we_node.environment
	var replay_route_track: String = main.cur_track
	var replay_route_music: Dictionary = _music_context()
	main._activate_touch_interactable("friend:%d" % daddy_index, daddy_index)
	melody = main._game_obj("melody", MelodyGame) as MelodyGame
	var replay_layer: CanvasLayer = melody.active_layer()
	var replay_layer_ref: WeakRef = weakref(replay_layer)
	await _wait_for_fade_clear()
	await _wait_for_green(true)
	_push_key(KEY_ENTER, false, 0)
	_push_key(KEY_SPACE, false, 1)
	_push_pad(JOY_BUTTON_B, false, 0)
	await process_frame
	_check("unrelated key and pad releases preserve both pre-entry action owners",
		melody.progress_count() == 0
		and bool(melody.audit_snapshot().get(
			"blocked_until_release", false)))
	_push_key(KEY_SPACE, false)
	await process_frame
	_check("releasing one of two pre-entry owners keeps the other owner blocked",
		melody.progress_count() == 0
		and bool(melody.audit_snapshot().get(
			"blocked_until_release", false)))
	_push_pad(JOY_BUTTON_A, false)
	await process_frame
	_check("pre-entry held keyboard/pad actions release neutrally",
		melody.progress_count() == 0
		and not bool(melody.audit_snapshot().get("input_down", true))
		and not bool(melody.audit_snapshot().get(
			"blocked_until_release", true)))

	var save_before_gold: int = main.save_generation
	var gold_run: Dictionary = await _complete_ordered_notes(
		["key", "pad", "touch", "touch", "touch", "touch", "touch"],
		false, false)
	await _frames(3)
	var gold_save: Dictionary = _read_probe_save()
	_check("fresh keyboard, pad, and touch presses all complete the replay",
		gold_run.get("ids", []) == [0, 1, 2, 3, 4, 5, 6]
		and _colors_equal(gold_run.get("colors", []) as Array,
			EXPECTED_COLORS)
		and bool(gold_run.get("all_armed", false)))
	_check("fast replay upgrades only the medal and never duplicates first-win reward",
		main.game == "" and main.trophies == trophy_before_replay
		and daddy_friend.get("star") == star_before_replay
		and int(main.medals.get("melody", 0)) == MedalSystem.GOLD
		and int((gold_save.get("medals", {}) as Dictionary).get(
			"melody", 0)) == MedalSystem.GOLD
		and bool((gold_save.get("won", {}) as Dictionary).get(
			"Daddy Mermaid", false)))
	_check("gold upgrade and terminal persistence each write exactly once",
		main.save_generation == save_before_gold + 2)
	print("MELODY|REPLAY_RETURN_FACTS|terminal_position_match=",
		gold_run.get("terminal_position") == replay_route_position,
		"|environment_match=", main.we_node.environment == replay_route_environment,
		"|track=", main.cur_track, "|expected_track=", replay_route_track,
		"|music=", _music_context(), "|expected_music=", replay_route_music,
		"|chime_match=", _chime_tuning_restored(),
		"|active_layers=", _active_layer_count(),
		"|controls_match=", main.touch_control_blocks == controls_baseline)
	_check("replay restores context and synchronously tears down",
		gold_run.get("terminal_position") == replay_route_position
		and gold_run.get("terminal_environment") == replay_route_environment
		and String(gold_run.get("terminal_track", "")) == replay_route_track
		and _music_context_values_match(
			gold_run.get("terminal_music", {}) as Dictionary,
			replay_route_music)
		and main.we_node.environment == replay_route_environment
		and main.cur_track == replay_route_track
		and _music_context_matches(replay_route_music)
		and _chime_tuning_restored()
		and melody.active_layer() == null and _active_layer_count() == 0
		and main.touch_control_blocks == controls_baseline)
	await _frames(2)
	_check("replay layer is freed after synchronous detach",
		replay_layer_ref.get_ref() == null)

	await _finish()


func _check_asset_contract() -> void:
	var master := Image.load_from_file(MASTER_PATH)
	_check("approved Sky Lagoon v5 master is exact native 6144x2048",
		master != null and master.get_size() == Vector2i(6144, 2048)
		and FileAccess.get_sha256(MASTER_PATH) == MASTER_SHA256)
	var all_tiles_ok := master != null
	for index in range(TILE_PATHS.size()):
		var path: String = TILE_PATHS[index]
		var tile := Image.load_from_file(path)
		var row: int = index / 2
		var column: int = 2 + index % 2
		var crop := master.get_region(Rect2i(
			column * 1024, row * 1024, 1024, 1024)) if master != null else null
		all_tiles_ok = all_tiles_ok and tile != null and crop != null \
			and tile.get_size() == Vector2i(1024, 1024) \
			and FileAccess.get_sha256(path) == TILE_SHA256[index] \
			and tile.get_format() == crop.get_format() \
			and tile.get_data() == crop.get_data()
	_check("four exact lossless center tiles reconstruct one native 2048x2048 screen",
		all_tiles_ok)
	var tile_imports_ok := true
	for tile_path: String in TILE_PATHS:
		var import_text := FileAccess.get_file_as_string(tile_path + ".import")
		tile_imports_ok = tile_imports_ok \
			and import_text.contains("compress/mode=2") \
			and import_text.contains("\"vram_texture\": true") \
			and import_text.contains("mipmaps/generate=false")
	_check("POT background tiles use bounded VRAM import without mip overfetch",
		tile_imports_ok)
	var daddy := Image.load_from_file(DADDY_PATH)
	var roshan := Image.load_from_file(ROSHAN_PATH)
	_check("approved Daddy sticker remains exact protected 750x1024 art",
		daddy != null and daddy.get_size() == Vector2i(750, 1024)
		and FileAccess.get_sha256(DADDY_PATH) == DADDY_SHA256)
	_check("approved Opera popstar Roshan remains exact 512x512 art",
		roshan != null and roshan.get_size() == Vector2i(512, 512)
		and FileAccess.get_sha256(ROSHAN_PATH) == ROSHAN_SHA256)
	var daddy_import := FileAccess.get_file_as_string(DADDY_PATH + ".import")
	var roshan_import := FileAccess.get_file_as_string(ROSHAN_PATH + ".import")
	_check("NPOT Daddy avoids forbidden VRAM mode and POT Roshan is mobile-compressed",
		daddy_import.contains("compress/mode=0")
		and daddy_import.contains("\"vram_texture\": false")
		and roshan_import.contains("compress/mode=2")
		and roshan_import.contains("\"vram_texture\": true"))
	var licenses := FileAccess.get_file_as_string("res://ASSET_LICENSES.md")
	_check("all reused background/actor/voice families retain repository provenance",
		licenses.contains("sky_lagoon_panorama_master_v5_hd_3x1.png")
		and licenses.contains("assets/characters/stickers/*.png")
		and licenses.contains("assets/opera/worlds/actors/roshan_{")
		and licenses.contains("assets/audio/voices/* (all other lines)"))
	_check("exact non-reader objective voice is present and immutable",
		ResourceLoader.exists(VOICE_PATH)
		and FileAccess.get_sha256(VOICE_PATH) == VOICE_SHA256)


func _check_entry_contract(layer: CanvasLayer, surface: Node2D,
		direct_baseline: Dictionary, game_nodes_baseline: Array[int],
		controls_baseline: Dictionary, route_position: Variant,
		route_environment: Variant, route_track: String) -> void:
	var snapshot: Dictionary = melody.audit_snapshot()
	var viewport_rect := Rect2(Vector2.ZERO, Vector2(VIEWPORT_SIZE))
	print("MELODY|ENTRY_FACTS|active_layers=", _active_layer_count(),
		"|direct_before=", direct_baseline.size(),
		"|direct_now=", _direct_child_ids().size(),
		"|only_layer_or_touch_fx_added=",
		_only_layer_and_touch_sparkles_added(direct_baseline, layer),
		"|layer=", layer.layer if layer != null else -999,
		"|pause_layer=", main.pause_layer.layer if main.pause_layer != null else -999)
	_check("entry owns exactly one Canvas layer below the pause sheet",
		layer != null and surface != null and _active_layer_count() == 1
		and layer.name == &"MelodyCanvasLayer"
		and surface.name == &"RainbowTheaterCanvas"
		and melody.stage_root() == surface
		and _only_layer_and_touch_sparkles_added(direct_baseline, layer)
		and layer.layer < main.pause_layer.layer)
	var names_ok := surface != null
	for node_name: String in EXPECTED_STAGE_NODES:
		names_ok = names_ok and _stage_node(surface, node_name) != null
	for index in range(7):
		names_ok = names_ok \
			and _stage_node(surface, "RainbowNote%d" % index) != null \
			and _stage_node(surface, "ProgressPip%d" % index) != null
	_check("Canvas theater exposes every stable stage, note, and progress node",
		names_ok)
	_check("Canvas theater has the exact typed surface tree with no unknown occluder",
		_surface_structure_exact(surface))
	_check("Melody adds no spatial descendants or hidden game-node authority",
		_count_spatial_descendants(layer) == 0
		and _game_node_ids() == game_nodes_baseline)
	var tile_contract: Dictionary = _runtime_tile_contract(surface, viewport_rect)
	_check("runtime binds the exact four native center tiles once in 2x2 order",
		bool(tile_contract.get("paths_exact", false))
		and bool(tile_contract.get("source_2048_square", false)))
	_check("runtime four-tile transforms are seam-free and cover the phone viewport",
		bool(tile_contract.get("seam_free", false))
		and bool(tile_contract.get("covers_viewport", false)))
	_check("attached note geometry exposes all seven ordered colors and the draw path binds the same source color",
		_colors_equal(_actual_note_colors(surface), EXPECTED_COLORS)
		and _note_source_binds_geometry_color()
		and melody.note_count() == 7 and melody.active_note_id() == 0
		and melody.progress_count() == 0)
	_check("stage has no failure state, countdown, or passive completion path",
		bool(snapshot.get("no_fail_state", false))
		and not bool(snapshot.get("has_timer", true))
		and float(main.g.get("timer", 0.0)) < 0.0
		and not bool(snapshot.get("completed", true)))
	_check("opaque Canvas preserves Reef position/environment while owning controls",
		main.player.position.is_equal_approx(route_position)
		and main.return_pos.is_equal_approx(route_position)
		and main.we_node.environment == route_environment
		and main.return_env == route_environment
		and main.return_track == route_track
		and main.touch_control_blocks.size() == controls_baseline.size() + 1
		and main.touch_control_blocks.has("melody")
		and not main.touch_ui.world_controls_enabled)


func _check_rendered_stage_contract(surface: Node2D) -> void:
	_check_runtime_texture_census(surface)
	var layer_id: int = melody.active_layer().get_instance_id()
	var progress_before: int = melody.progress_count()
	var note_id_before: int = melody.active_note_id()
	var standard_viewport := Rect2(Vector2.ZERO,
		get_root().get_visible_rect().size)
	var standard: Dictionary = _layout_geometry_contract(surface,
		standard_viewport)
	print("MELODY|LAYOUT_FACTS|standard=", standard)
	_check("actual proscenium polygons visibly dominate the 1280x720 stage",
		bool(standard.get("proscenium_dominant", false)))
	_check("actual Daddy and Roshan alpha bounds are readable at 1280x720",
		bool(standard.get("actors_readable", false)))
	_check("actual note, hit envelope, green zone, and pointer are readable at 1280x720",
		bool(standard.get("note_readable", false)))
	_check("pointer is exactly one attached arrow, line, target, and two rings with no custom-draw duplicate",
		bool(standard.get("pointer_geometry_unique", false))
		and _pointer_source_is_geometry_only())
	_check("actual four-tile Canvas transforms cover 1280x720 seam-free",
		bool(standard.get("backdrop_covers", false)))

	get_root().size = TALL_PHONE_SIZE
	await _frames(4)
	var wide_viewport := Rect2(Vector2.ZERO,
		get_root().get_visible_rect().size)
	var wide: Dictionary = _layout_geometry_contract(surface, wide_viewport)
	print("MELODY|LAYOUT_FACTS|tall=", wide)
	_check("Canvas reflows to the target 1280x800 M11 phone aspect",
		Vector2i(wide_viewport.size) == TALL_PHONE_SIZE
		and bool(wide.get("proscenium_dominant", false))
		and bool(wide.get("actors_readable", false))
		and bool(wide.get("note_readable", false))
		and bool(wide.get("backdrop_covers", false)))
	_check("1280x800 reflow preserves the same live stage and note semantics",
		melody.active_layer() != null
		and melody.active_layer().get_instance_id() == layer_id
		and melody.progress_count() == progress_before
		and melody.active_note_id() == note_id_before)

	get_root().size = VIEWPORT_SIZE
	await _frames(4)
	var restored_viewport := Rect2(Vector2.ZERO,
		get_root().get_visible_rect().size)
	var restored: Dictionary = _layout_geometry_contract(surface,
		restored_viewport)
	print("MELODY|LAYOUT_FACTS|restored=", restored)
	_check("1280x720 restore needs no rebuild and retains readable geometry",
		Vector2i(restored_viewport.size) == VIEWPORT_SIZE
		and melody.active_layer() != null
		and melody.active_layer().get_instance_id() == layer_id
		and melody.progress_count() == progress_before
		and melody.active_note_id() == note_id_before
		and bool(restored.get("proscenium_dominant", false))
		and bool(restored.get("actors_readable", false))
		and bool(restored.get("note_readable", false))
		and bool(restored.get("backdrop_covers", false)))


func _layout_geometry_contract(surface: Node2D,
		viewport_rect: Rect2) -> Dictionary:
	var proscenium: Node = _stage_node(surface, "OperaProscenium")
	var footlights: Node = _stage_node(surface, "StageFootlights")
	var stage_star: Node = _stage_node(surface, "StageStar")
	var proscenium_metrics: Dictionary = _polygon_union_metrics(
		proscenium, viewport_rect)
	var proscenium_rect: Rect2 = proscenium_metrics.get("rect", Rect2())
	var footlights_rect: Rect2 = _node_visual_rect(footlights)
	var stage_star_rect: Rect2 = _node_visual_rect(stage_star)
	var proscenium_dominant: bool = proscenium != null \
		and proscenium.is_visible_in_tree() \
		and float(proscenium_metrics.get("coverage", 0.0)) >= 0.28 \
		and proscenium_rect.size.x >= viewport_rect.size.x * 0.875 \
		and proscenium_rect.size.y >= viewport_rect.size.y * 0.86 \
		and footlights_rect.has_area() \
		and stage_star_rect.has_area() \
		and viewport_rect.encloses(footlights_rect) \
		and viewport_rect.encloses(stage_star_rect)

	var daddy: Node = _stage_node(surface, "DaddyGuide")
	var roshan: Node = _stage_node(surface, "PopstarRoshan")
	var daddy_rect: Rect2 = _node_visual_rect(daddy)
	var roshan_rect: Rect2 = _node_visual_rect(roshan)
	var actors_readable: bool = _direct_actor_contract(
		daddy, surface, DADDY_PATH) \
		and _direct_actor_contract(roshan, surface, ROSHAN_PATH) \
		and viewport_rect.encloses(daddy_rect) \
		and viewport_rect.encloses(roshan_rect) \
		and daddy_rect.size.x >= 150.0 and daddy_rect.size.y >= 220.0 \
		and roshan_rect.size.x >= 120.0 and roshan_rect.size.y >= 160.0

	var note_id: int = melody.active_note_id()
	var note: Node = _stage_node(surface, "RainbowNote%d" % note_id)
	var zone: Node = _stage_node(surface, "TimingZone")
	var pointer: Node = _stage_node(surface, "VisualPointer")
	var note_rect: Rect2 = _node_visual_rect(note)
	var zone_visual_rect: Rect2 = _node_visual_rect(zone)
	var pointer_rect: Rect2 = _node_visual_rect(pointer)
	var hit_rect: Rect2 = melody.active_note_hit_rect()
	var zone_rect: Rect2 = melody.timing_zone_screen_rect()
	var note_center: Vector2 = note_rect.get_center()
	var pointer_target: Variant = pointer.get("target") if pointer != null else null
	var pointer_target_distance := INF
	if pointer_target is Vector2:
		pointer_target_distance = (pointer_target as Vector2).distance_to(note_center)
	var arrow_tip_distance: float = _nearest_named_geometry_point(
		pointer, "Arrow", note_center)
	var pointer_geometry_unique: bool = _pointer_geometry_contract(
		pointer, note_center)
	var expected_note_color: Color = EXPECTED_COLORS[note_id] \
		if note_id >= 0 and note_id < EXPECTED_COLORS.size() else Color.BLACK
	var progress_rects: Array[Rect2] = []
	var progress_clear := true
	for pip_index in range(7):
		var pip: Node = _stage_node(surface, "ProgressPip%d" % pip_index)
		var pip_rect: Rect2 = _node_visual_rect(pip)
		progress_rects.append(pip_rect)
		progress_clear = progress_clear and pip_rect.has_area() \
			and viewport_rect.encloses(pip_rect) \
			and not stage_star_rect.intersects(pip_rect) \
			and not note_rect.intersects(pip_rect) \
			and not zone_visual_rect.intersects(pip_rect) \
			and _effective_canvas_z(pip) > _effective_canvas_z(note)
	var actors_clear: bool = not daddy_rect.intersects(note_rect) \
		and not roshan_rect.intersects(note_rect) \
		and not daddy_rect.intersects(zone_visual_rect) \
		and not roshan_rect.intersects(zone_visual_rect)
	var critical_rects: Array[Rect2] = [
		daddy_rect, roshan_rect, note_rect, zone_visual_rect, pointer_rect,
	]
	critical_rects.append_array(progress_rects)
	var decorations_clear := true
	for critical_rect: Rect2 in critical_rects:
		decorations_clear = decorations_clear \
			and critical_rect.has_area() \
			and not footlights_rect.intersects(critical_rect) \
			and not stage_star_rect.intersects(critical_rect)
	var fill: Node = _stage_node(surface, "OpaqueTheaterFill")
	var scenic: Node = _stage_node(surface, "ScenicBackcloth")
	var first_tile: Node = _stage_node(surface, TILE_NODE_NAMES[0])
	var z_order_valid: bool = _effective_canvas_z(fill) \
			< _effective_canvas_z(scenic) \
		and _effective_canvas_z(scenic) < _effective_canvas_z(first_tile) \
		and _effective_canvas_z(first_tile) < _effective_canvas_z(proscenium) \
		and _effective_canvas_z(proscenium) < _effective_canvas_z(footlights) \
		and _effective_canvas_z(footlights) < _effective_canvas_z(stage_star) \
		and _effective_canvas_z(stage_star) < _effective_canvas_z(daddy) \
		and _effective_canvas_z(stage_star) < _effective_canvas_z(roshan) \
		and _effective_canvas_z(daddy) < _effective_canvas_z(zone) \
		and _effective_canvas_z(roshan) < _effective_canvas_z(zone) \
		and _effective_canvas_z(zone) < _effective_canvas_z(pointer) \
		and _effective_canvas_z(pointer) <= _effective_canvas_z(note) \
		and _effective_canvas_z(note) < _effective_canvas_z(
			_stage_node(surface, "ProgressPip0"))
	var note_readable: bool = note_id >= 0 \
		and note_rect.size.x >= 64.0 and note_rect.size.y >= 64.0 \
		and hit_rect.size.x >= 110.0 and hit_rect.size.y >= 110.0 \
		and hit_rect.grow(6.0).encloses(note_rect) \
		and viewport_rect.encloses(note_rect) \
		and viewport_rect.encloses(hit_rect) \
		and zone_visual_rect.size.x >= 110.0 \
		and zone_visual_rect.size.y >= 110.0 \
		and zone_rect.grow(24.0).encloses(zone_visual_rect) \
		and viewport_rect.encloses(zone_visual_rect) \
		and viewport_rect.encloses(zone_rect) \
		and pointer_rect.size.x >= 48.0 and pointer_rect.size.y >= 48.0 \
		and viewport_rect.encloses(pointer_rect) \
		and pointer_target_distance <= 4.0 \
		and arrow_tip_distance <= 4.0 \
		and pointer_geometry_unique \
		and _subtree_has_green(zone) \
		and _subtree_has_color(note, expected_note_color) \
		and int(pointer.get("target_id")) == note_id \
		and progress_clear and actors_clear and decorations_clear \
		and z_order_valid
	var tile_contract: Dictionary = _runtime_tile_contract(surface,
		viewport_rect)
	return {
		"proscenium_dominant": proscenium_dominant,
		"viewport_rect": viewport_rect,
		"proscenium_rect": proscenium_rect,
		"proscenium_coverage": float(proscenium_metrics.get("coverage", 0.0)),
		"footlights_rect": footlights_rect,
		"stage_star_rect": stage_star_rect,
		"actors_readable": actors_readable,
		"note_readable": note_readable,
		"pointer_geometry_unique": pointer_geometry_unique,
		"critical_regions_clear": progress_clear and actors_clear
			and decorations_clear,
		"z_order_valid": z_order_valid,
		"backdrop_covers": bool(tile_contract.get("paths_exact", false))
			and bool(tile_contract.get("source_2048_square", false))
			and bool(tile_contract.get("seam_free", false))
			and bool(tile_contract.get("covers_viewport", false))
			and _opaque_stage_covers(surface, viewport_rect),
	}


func _opaque_stage_covers(surface: Node2D, viewport_rect: Rect2) -> bool:
	var fill: Node = _stage_node(surface, "OpaqueTheaterFill")
	if not (fill is ColorRect):
		return false
	var color_fill := fill as ColorRect
	return color_fill.is_visible_in_tree() \
		and _effective_canvas_alpha(color_fill) * color_fill.color.a >= 0.98 \
		and color_fill.get_global_rect().grow(1.0).encloses(viewport_rect)


func _runtime_tile_contract(surface: Node2D,
		viewport_rect: Rect2) -> Dictionary:
	var scenic: Node = _stage_node(surface, "ScenicBackcloth")
	if not (scenic is Control):
		return {}
	var scenic_control := scenic as Control
	var rects: Array[Rect2] = []
	var paths: Array[String] = []
	var instance_ids: Dictionary = {}
	var scales: Array[Vector2] = []
	var source_square := true
	var source_geometry_exact := scenic_control.clip_contents
	for index in range(TILE_NODE_NAMES.size()):
		if _count_nodes_named(surface, TILE_NODE_NAMES[index]) != 1:
			return {}
		var node: Node = _stage_node(surface, TILE_NODE_NAMES[index])
		if not (node is Sprite2D) or node.get_parent() != scenic:
			return {}
		var sprite := node as Sprite2D
		var texture: Texture2D = sprite.texture
		if texture == null or texture is AtlasTexture:
			return {}
		paths.append(texture.resource_path)
		var tile_rect: Rect2 = _texture_item_full_rect(sprite)
		rects.append(tile_rect)
		instance_ids[node.get_instance_id()] = true
		scales.append(sprite.scale)
		source_square = source_square \
			and texture.get_size() == Vector2(1024, 1024)
		var tile_scale: Vector2 = sprite.scale
		var global_xform: Transform2D = sprite.get_global_transform_with_canvas()
		var axis_x: Vector2 = global_xform.x
		var axis_y: Vector2 = global_xform.y
		var axis_tolerance: float = maxf(axis_x.length(), axis_y.length()) * 0.001
		source_geometry_exact = source_geometry_exact \
			and String(sprite.get_meta("source_path", "")) == TILE_PATHS[index] \
			and sprite.get_meta("native_source_rect", Rect2i()) \
				== TILE_SOURCE_RECTS[index] \
			and sprite.get_child_count() == 0 \
			and sprite.centered and not sprite.flip_h and not sprite.flip_v \
			and not sprite.region_enabled \
			and sprite.hframes == 1 and sprite.vframes == 1 and sprite.frame == 0 \
			and sprite.offset.is_zero_approx() \
			and tile_scale.x > 0.0 and tile_scale.y > 0.0 \
			and is_equal_approx(tile_scale.x, tile_scale.y) \
			and is_zero_approx(sprite.rotation) and is_zero_approx(sprite.skew) \
			and global_xform.determinant() > 0.0 \
			and absf(axis_x.dot(axis_y)) <= axis_tolerance \
			and is_equal_approx(axis_x.length(), axis_y.length()) \
			and axis_x.x > 0.0 and axis_y.y > 0.0 \
			and absf(axis_x.y) <= axis_tolerance \
			and absf(axis_y.x) <= axis_tolerance \
			and tile_rect.has_area()
	var union_rect: Rect2 = rects[0]
	for index in range(1, rects.size()):
		union_rect = union_rect.merge(rects[index])
	var tolerance := 1.5
	var common_transform := scales.size() == 4
	var common_rect_size := rects.size() == 4
	for index in range(1, scales.size()):
		common_transform = common_transform \
			and scales[index].is_equal_approx(scales[0])
		common_rect_size = common_rect_size \
			and rects[index].size.is_equal_approx(rects[0].size)
	var seam_free: bool = rects.all(func(rect: Rect2) -> bool:
			return rect.has_area()) \
		and common_transform and common_rect_size \
		and absf(rects[0].size.x - rects[0].size.y) <= tolerance \
		and absf(rects[0].end.x - rects[1].position.x) <= tolerance \
		and absf(rects[2].end.x - rects[3].position.x) <= tolerance \
		and absf(rects[0].end.y - rects[2].position.y) <= tolerance \
		and absf(rects[1].end.y - rects[3].position.y) <= tolerance \
		and absf(rects[0].position.y - rects[1].position.y) <= tolerance \
		and absf(rects[2].position.y - rects[3].position.y) <= tolerance \
		and rects[0].position.x < rects[1].position.x \
		and rects[0].position.y < rects[2].position.y \
		and absf(union_rect.size.x - union_rect.size.y) <= tolerance
	var scenic_rect: Rect2 = scenic_control.get_global_rect()
	var scenic_window_exact: bool = scenic_rect.has_area() \
		and viewport_rect.encloses(scenic_rect) \
		and union_rect.grow(tolerance).encloses(scenic_rect) \
		and union_rect.get_center().distance_to(scenic_rect.get_center()) \
			<= tolerance
	return {
		"paths_exact": paths == TILE_PATHS
			and instance_ids.size() == TILE_PATHS.size()
			and source_geometry_exact,
		"source_2048_square": source_square and common_transform
			and common_rect_size,
		"seam_free": seam_free,
		"covers_viewport": scenic_window_exact,
		"union_rect": union_rect,
	}


func _check_runtime_texture_census(surface: Node2D) -> void:
	var counts: Dictionary = {}
	_collect_runtime_texture_paths(surface, counts)
	var expected_paths: Array[String] = TILE_PATHS.duplicate()
	expected_paths.append(DADDY_PATH)
	expected_paths.append(ROSHAN_PATH)
	var exact_once := counts.size() == expected_paths.size()
	var decoded_bytes := 0
	var declared_upload_bytes := 0
	for path: String in expected_paths:
		exact_once = exact_once and int(counts.get(path, 0)) == 1
		var image := Image.load_from_file(path)
		if image == null:
			exact_once = false
			continue
		var pixels: int = image.get_width() * image.get_height()
		decoded_bytes += pixels * 4
		var import_text := FileAccess.get_file_as_string(path + ".import")
		declared_upload_bytes += pixels if import_text.contains(
			"compress/mode=2") else pixels * 4
	_check("live Canvas binds only four tiles, Daddy, and Roshan exactly once each",
		exact_once)
	_check("unique live texture census stays within conservative decoded and declared-upload bounds",
		decoded_bytes > 0 and decoded_bytes <= 23 * 1024 * 1024
		and declared_upload_bytes > 0
		and declared_upload_bytes <= 12 * 1024 * 1024)


func _collect_runtime_texture_paths(node: Node, counts: Dictionary) -> void:
	if node == null:
		return
	var texture: Texture2D = _node_texture(node)
	var source_texture: Texture2D = _source_texture(texture)
	if source_texture != null and not source_texture.resource_path.is_empty():
		counts[source_texture.resource_path] = int(counts.get(
			source_texture.resource_path, 0)) + 1
	for child_value: Variant in node.get_children():
		_collect_runtime_texture_paths(child_value as Node, counts)


func _stage_node(surface: Node, node_name: String) -> Node:
	if surface == null:
		return null
	return surface.find_child(node_name, true, false)


func _surface_structure_exact(surface: Node2D) -> bool:
	if surface == null:
		return false
	var surface_names: Array[String] = [
		"OpaqueTheaterFill", "ScenicBackcloth", "OperaProscenium",
		"StageFootlights", "StageStar", "DaddyGuide", "PopstarRoshan",
		"TimingZone", "VisualPointer",
	]
	for index in range(7):
		surface_names.append("RainbowNote%d" % index)
		surface_names.append("ProgressPip%d" % index)
	if not _exact_direct_child_names(surface, surface_names):
		return false
	var fill: Node = _stage_node(surface, "OpaqueTheaterFill")
	var scenic: Node = _stage_node(surface, "ScenicBackcloth")
	var proscenium: Node = _stage_node(surface, "OperaProscenium")
	var footlights: Node = _stage_node(surface, "StageFootlights")
	var star: Node = _stage_node(surface, "StageStar")
	var zone: Node = _stage_node(surface, "TimingZone")
	var pointer: Node = _stage_node(surface, "VisualPointer")
	if not (fill is ColorRect) or fill.get_child_count() != 0 \
			or not (scenic is ColorRect) \
			or not (proscenium is Control) \
			or not (footlights is Control) or not (star is Control) \
			or not (zone is Control) or not (pointer is Control):
		return false
	if not _exact_direct_child_names(scenic, TILE_NODE_NAMES) \
			or not _exact_typed_geometry_children(proscenium, [
				"LeftCurtainGeometry", "RightCurtainGeometry",
				"CrownHeaderGeometry", "StageApronGeometry",
			], []) \
			or not _exact_typed_geometry_children(
				footlights, [], ["FootlightRailGeometry"]) \
			or not _exact_typed_geometry_children(
				star, ["StageStarGeometry"], []) \
			or not _exact_typed_geometry_children(
				zone, ["GreenWindowGeometry"], []) \
			or not _exact_typed_geometry_children(pointer, [
				"PointerTargetGeometry", "PointerArrowGeometry",
			], [
				"PointerLineGeometry", "PointerInnerRingGeometry",
				"PointerOuterRingGeometry",
			]):
		return false
	for index in range(7):
		var note: Node = _stage_node(surface, "RainbowNote%d" % index)
		var pip: Node = _stage_node(surface, "ProgressPip%d" % index)
		if not (note is Control) or not (pip is Control) \
				or not _exact_typed_geometry_children(
				note, ["NoteColorGeometry"], []) \
				or not _exact_typed_geometry_children(
				pip, ["ProgressPipGeometry"], []):
			return false
	return true


func _exact_direct_child_names(node: Node, expected: Array[String]) -> bool:
	if node == null or node.get_child_count() != expected.size():
		return false
	for index in range(expected.size()):
		if String(node.get_child(index).name) != expected[index]:
			return false
	return true


func _exact_typed_geometry_children(node: Node, polygon_names: Array,
		line_names: Array) -> bool:
	var expected: Array[String] = []
	for name_value: Variant in polygon_names:
		expected.append(String(name_value))
	for name_value: Variant in line_names:
		expected.append(String(name_value))
	if not _exact_direct_child_names(node, expected):
		return false
	for index in range(polygon_names.size()):
		if not (node.get_child(index) is Polygon2D):
			return false
	for index in range(line_names.size()):
		if not (node.get_child(polygon_names.size() + index) is Line2D):
			return false
	return true


func _node_texture(node: Node) -> Texture2D:
	if node is Sprite2D:
		return (node as Sprite2D).texture
	if node is TextureRect:
		return (node as TextureRect).texture
	if node is NinePatchRect:
		return (node as NinePatchRect).texture
	return null


func _direct_actor_contract(actor: Node, surface: Node2D,
		expected_path: String) -> bool:
	if not (actor is Sprite2D) or actor.get_parent() != surface \
			or _count_nodes_named(surface, String(actor.name)) != 1:
		return false
	var sprite := actor as Sprite2D
	var texture: Texture2D = sprite.texture
	if texture == null or texture is AtlasTexture:
		return false
	var xform: Transform2D = sprite.get_global_transform_with_canvas()
	var axis_tolerance: float = maxf(xform.x.length(), xform.y.length()) * 0.001
	return texture.resource_path == expected_path \
		and String(sprite.get_meta("source_path", "")) == expected_path \
		and sprite.get_child_count() == 0 \
		and sprite.centered and not sprite.flip_h and not sprite.flip_v \
		and not sprite.region_enabled \
		and sprite.hframes == 1 and sprite.vframes == 1 and sprite.frame == 0 \
		and sprite.offset.is_zero_approx() \
		and sprite.scale.x > 0.0 and sprite.scale.y > 0.0 \
		and _actor_aspect_preserved(sprite) \
		and is_zero_approx(sprite.rotation) and is_zero_approx(sprite.skew) \
		and xform.determinant() > 0.0 \
		and absf(xform.x.dot(xform.y)) <= axis_tolerance \
		and sprite.is_visible_in_tree() \
		and _effective_canvas_alpha(sprite) > 0.85


func _actor_aspect_preserved(node: Node) -> bool:
	if node is Sprite2D:
		var actor_scale: Vector2 = (node as Sprite2D).scale.abs()
		return absf(actor_scale.x - actor_scale.y) \
			<= maxf(actor_scale.x, actor_scale.y) * 0.02
	if node is TextureRect:
		return (node as TextureRect).stretch_mode \
			== TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	return false


func _source_texture(texture: Texture2D) -> Texture2D:
	var source: Texture2D = texture
	var depth := 0
	while source is AtlasTexture and depth < 8:
		source = (source as AtlasTexture).atlas
		depth += 1
	return source


func _texture_item_full_rect(node: Node) -> Rect2:
	if node is Sprite2D:
		var sprite := node as Sprite2D
		return _transform_rect(sprite.get_rect(),
			sprite.get_global_transform_with_canvas())
	if node is Control:
		return (node as Control).get_global_rect()
	return Rect2()


func _node_visual_rect(node: Node) -> Rect2:
	var rects: Array[Rect2] = []
	_collect_visual_rects(node, rects)
	if rects.is_empty():
		return Rect2()
	var merged: Rect2 = rects[0]
	for index in range(1, rects.size()):
		merged = merged.merge(rects[index])
	if node is Control and _has_geometry_descendant(node):
		var control := node as Control
		var control_rect := _transform_rect(
			Rect2(Vector2.ZERO, control.size),
			control.get_global_transform_with_canvas())
		if String(node.name) == "TimingZone":
			control_rect = control_rect.grow(18.0)
		if String(node.name) in [
			"StageFootlights", "StageStar", "TimingZone",
		] or String(node.name).begins_with("RainbowNote") \
				or String(node.name).begins_with("ProgressPip"):
			merged = merged.merge(control_rect)
	return merged


func _has_geometry_descendant(node: Node) -> bool:
	if node == null:
		return false
	for child_value: Variant in node.get_children():
		var child := child_value as Node
		if child is Polygon2D or child is Line2D \
				or _has_geometry_descendant(child):
			return true
	return false


func _collect_visual_rects(node: Node, rects: Array[Rect2]) -> void:
	if node == null or (node is CanvasItem and (
			not (node as CanvasItem).is_visible_in_tree()
			or _effective_canvas_alpha(node as CanvasItem) <= 0.02)):
		return
	if node is Sprite2D:
		var sprite := node as Sprite2D
		var alpha_rect: Rect2 = _sprite_alpha_rect(sprite)
		if alpha_rect.has_area():
			rects.append(_transform_rect(alpha_rect,
				sprite.get_global_transform_with_canvas()))
	elif node is Polygon2D:
		var polygon := node as Polygon2D
		var points: PackedVector2Array = polygon.polygon
		if points.size() >= 3 and polygon.color.a > 0.02:
			var transformed := PackedVector2Array()
			var xform := polygon.get_global_transform_with_canvas()
			for point: Vector2 in points:
				transformed.append(xform * point)
			rects.append(_points_rect(transformed))
	elif node is TextureRect:
		var texture_rect := node as TextureRect
		if texture_rect.texture != null:
			var alpha_rect: Rect2 = _texture_rect_alpha_rect(texture_rect)
			if alpha_rect.has_area():
				rects.append(alpha_rect)
	elif node is ColorRect:
		var color_rect := node as ColorRect
		if color_rect.color.a > 0.02:
			rects.append(color_rect.get_global_rect())
	elif node is Line2D:
		var line := node as Line2D
		var line_points := PackedVector2Array()
		var line_xform := line.get_global_transform_with_canvas()
		for point: Vector2 in line.points:
			line_points.append(line_xform * point)
		var line_rect: Rect2 = _points_rect(line_points).grow(line.width * 0.5)
		if line_rect.has_area():
			rects.append(line_rect)
	for child_value: Variant in node.get_children():
		_collect_visual_rects(child_value as Node, rects)


func _sprite_alpha_rect(sprite: Sprite2D) -> Rect2:
	if sprite.texture == null:
		return Rect2()
	var source: Texture2D = _source_texture(sprite.texture)
	var used: Rect2i = _texture_alpha_used_rect(source)
	if used.size == Vector2i.ZERO:
		return Rect2()
	var texture_size := source.get_size()
	var full_rect: Rect2 = sprite.get_rect()
	return Rect2(
		full_rect.position + Vector2(used.position) / texture_size * full_rect.size,
		Vector2(used.size) / texture_size * full_rect.size)


func _texture_rect_alpha_rect(item: TextureRect) -> Rect2:
	var source: Texture2D = _source_texture(item.texture)
	if source == null or item.stretch_mode != TextureRect.STRETCH_KEEP_ASPECT_CENTERED:
		return Rect2()
	var used: Rect2i = _texture_alpha_used_rect(source)
	if used.size == Vector2i.ZERO:
		return Rect2()
	var source_size: Vector2 = source.get_size()
	var control_rect: Rect2 = item.get_global_rect()
	var scale_factor: float = minf(
		control_rect.size.x / maxf(source_size.x, 1.0),
		control_rect.size.y / maxf(source_size.y, 1.0))
	var draw_size: Vector2 = source_size * scale_factor
	var draw_position: Vector2 = control_rect.position \
		+ (control_rect.size - draw_size) * 0.5
	return Rect2(
		draw_position + Vector2(used.position) * scale_factor,
		Vector2(used.size) * scale_factor)


func _texture_alpha_used_rect(texture: Texture2D) -> Rect2i:
	if texture == null:
		return Rect2i()
	var key: String = texture.resource_path
	if key.is_empty():
		key = "instance:%d" % texture.get_instance_id()
	if texture_alpha_cache.has(key):
		return texture_alpha_cache[key] as Rect2i
	var image: Image = texture.get_image()
	var used: Rect2i = _image_alpha_rect(image)
	texture_alpha_cache[key] = used
	return used


func _image_alpha_rect(image: Image) -> Rect2i:
	if image == null or image.is_empty():
		return Rect2i()
	var scan: Image = image
	if scan.is_compressed():
		scan = image.duplicate()
		if scan.decompress() != OK:
			return Rect2i()
	var min_point := Vector2i(scan.get_width(), scan.get_height())
	var max_point := Vector2i(-1, -1)
	for y in range(scan.get_height()):
		for x in range(scan.get_width()):
			if scan.get_pixel(x, y).a <= 0.05:
				continue
			min_point.x = mini(min_point.x, x)
			min_point.y = mini(min_point.y, y)
			max_point.x = maxi(max_point.x, x)
			max_point.y = maxi(max_point.y, y)
	if max_point.x < min_point.x or max_point.y < min_point.y:
		return Rect2i()
	return Rect2i(min_point, max_point - min_point + Vector2i.ONE)


func _transform_rect(rect: Rect2, xform: Transform2D) -> Rect2:
	var points := PackedVector2Array([
		xform * rect.position,
		xform * Vector2(rect.end.x, rect.position.y),
		xform * rect.end,
		xform * Vector2(rect.position.x, rect.end.y),
	])
	return _points_rect(points)


func _points_rect(points: PackedVector2Array) -> Rect2:
	if points.is_empty():
		return Rect2()
	var min_point: Vector2 = points[0]
	var max_point: Vector2 = points[0]
	for point: Vector2 in points:
		min_point.x = minf(min_point.x, point.x)
		min_point.y = minf(min_point.y, point.y)
		max_point.x = maxf(max_point.x, point.x)
		max_point.y = maxf(max_point.y, point.y)
	return Rect2(min_point, max_point - min_point)


func _effective_canvas_z(node: Node) -> int:
	if not (node is CanvasItem):
		return -4096
	var total := 0
	var current: Node = node
	while current is CanvasItem:
		var item := current as CanvasItem
		total += item.z_index
		if not item.z_as_relative:
			break
		current = current.get_parent()
	return total


func _nearest_named_geometry_point(node: Node, name_token: String,
		target: Vector2) -> float:
	if node == null:
		return INF
	var best := INF
	if String(node.name).contains(name_token):
		var points := PackedVector2Array()
		if node is Polygon2D:
			var polygon := node as Polygon2D
			var polygon_xform := polygon.get_global_transform_with_canvas()
			for point: Vector2 in polygon.polygon:
				points.append(polygon_xform * point)
		elif node is Line2D:
			var line := node as Line2D
			var line_xform := line.get_global_transform_with_canvas()
			for point: Vector2 in line.points:
				points.append(line_xform * point)
		for point: Vector2 in points:
			best = minf(best, point.distance_to(target))
	for child_value: Variant in node.get_children():
		best = minf(best, _nearest_named_geometry_point(
			child_value as Node, name_token, target))
	return best


func _pointer_geometry_contract(pointer: Node, note_center: Vector2) -> bool:
	if not (pointer is Control) or not pointer.is_visible_in_tree() \
			or _effective_canvas_alpha(pointer as CanvasItem) <= 0.85:
		return false
	var target_geometry: Node = _stage_node(pointer, "PointerTargetGeometry")
	var arrow_geometry: Node = _stage_node(pointer, "PointerArrowGeometry")
	var line_geometry: Node = _stage_node(pointer, "PointerLineGeometry")
	var inner_geometry: Node = _stage_node(pointer, "PointerInnerRingGeometry")
	var outer_geometry: Node = _stage_node(pointer, "PointerOuterRingGeometry")
	var expected_nodes: Array[Node] = [
		target_geometry, arrow_geometry, line_geometry,
		inner_geometry, outer_geometry,
	]
	var expected_names: Array[String] = [
		"PointerTargetGeometry", "PointerArrowGeometry", "PointerLineGeometry",
		"PointerInnerRingGeometry", "PointerOuterRingGeometry",
	]
	if _count_geometry_descendants(pointer) != expected_nodes.size():
		return false
	for index in range(expected_nodes.size()):
		var geometry: Node = expected_nodes[index]
		if geometry == null or geometry.get_parent() != pointer \
				or _count_nodes_named(pointer, expected_names[index]) != 1 \
				or not geometry.is_visible_in_tree() \
				or _effective_canvas_alpha(geometry as CanvasItem) <= 0.10:
			return false
	if not (target_geometry is Polygon2D) \
			or not (arrow_geometry is Polygon2D) \
			or not (line_geometry is Line2D) \
			or not (inner_geometry is Line2D) \
			or not (outer_geometry is Line2D):
		return false
	var target_polygon := target_geometry as Polygon2D
	var arrow_polygon := arrow_geometry as Polygon2D
	var pointer_line := line_geometry as Line2D
	var inner_ring := inner_geometry as Line2D
	var outer_ring := outer_geometry as Line2D
	return target_polygon.polygon.size() == 4 \
		and _points_rect(target_polygon.polygon).has_area() \
		and target_polygon.color.a >= 0.15 \
		and arrow_polygon.polygon.size() == 3 \
		and _points_rect(arrow_polygon.polygon).has_area() \
		and arrow_polygon.color.a >= 0.85 \
		and _nearest_named_geometry_point(pointer, "Arrow", note_center) <= 4.0 \
		and pointer_line.points.size() >= 2 and pointer_line.width >= 7.0 \
		and pointer_line.default_color.a >= 0.85 \
		and inner_ring.points.size() >= 24 and inner_ring.width >= 7.0 \
		and inner_ring.default_color.a >= 0.85 \
		and outer_ring.points.size() >= 24 and outer_ring.width >= 4.0 \
		and outer_ring.default_color.a >= 0.75


func _count_geometry_descendants(node: Node) -> int:
	if node == null:
		return 0
	var count := 1 if node is Polygon2D or node is Line2D else 0
	for child_value: Variant in node.get_children():
		count += _count_geometry_descendants(child_value as Node)
	return count


func _count_nodes_named(node: Node, exact_name: String) -> int:
	if node == null:
		return 0
	var count := 1 if String(node.name) == exact_name else 0
	for child_value: Variant in node.get_children():
		count += _count_nodes_named(child_value as Node, exact_name)
	return count


func _pointer_source_is_geometry_only() -> bool:
	var source := FileAccess.get_file_as_string("res://scripts/games/melody.gd")
	var block_start: int = source.find("class PointerCanvas extends Control:")
	var block_end: int = source.find("class RainbowNoteCanvas extends Control:",
		block_start + 1)
	if block_start < 0 or block_end <= block_start:
		return false
	var block: String = source.substr(block_start, block_end - block_start)
	return block.count("PointerTargetGeometry") == 1 \
		and block.count("PointerArrowGeometry") == 1 \
		and block.count("PointerLineGeometry") == 1 \
		and block.count("PointerInnerRingGeometry") == 1 \
		and block.count("PointerOuterRingGeometry") == 1 \
		and not block.contains("func _draw") \
		and not block.contains("draw_")


func _note_source_binds_geometry_color() -> bool:
	var source := FileAccess.get_file_as_string("res://scripts/games/melody.gd")
	var block_start: int = source.find("class RainbowNoteCanvas extends Control:")
	var block_end: int = source.find("class ProgressPipCanvas extends Control:",
		block_start + 1)
	if block_start < 0 or block_end <= block_start:
		return false
	var block: String = source.substr(block_start, block_end - block_start)
	return block.count("color_geometry.color = note_color") == 1 \
		and block.count("draw_circle(center, 35.0, note_color") == 1


func _polygon_union_metrics(node: Node, viewport_rect: Rect2) -> Dictionary:
	var polygons: Array[PackedVector2Array] = []
	_collect_polygons(node, polygons)
	if polygons.is_empty():
		return {}
	var union_rect: Rect2 = _points_rect(polygons[0])
	for index in range(1, polygons.size()):
		union_rect = union_rect.merge(_points_rect(polygons[index]))
	var columns := 200
	var rows := 90
	var covered := 0
	for row in range(rows):
		for column in range(columns):
			var point := viewport_rect.position + Vector2(
				(float(column) + 0.5) * viewport_rect.size.x / float(columns),
				(float(row) + 0.5) * viewport_rect.size.y / float(rows))
			for polygon: PackedVector2Array in polygons:
				if Geometry2D.is_point_in_polygon(point, polygon):
					covered += 1
					break
	return {
		"rect": union_rect.intersection(viewport_rect),
		"coverage": float(covered) / float(columns * rows),
	}


func _collect_polygons(node: Node,
		polygons: Array[PackedVector2Array]) -> void:
	if node == null or (node is CanvasItem and (
			not (node as CanvasItem).is_visible_in_tree()
			or _effective_canvas_alpha(node as CanvasItem) <= 0.02)):
		return
	if node is Polygon2D:
		var item := node as Polygon2D
		if item.polygon.size() >= 3 and item.color.a > 0.02:
			var transformed := PackedVector2Array()
			var xform := item.get_global_transform_with_canvas()
			for point: Vector2 in item.polygon:
				transformed.append(xform * point)
			polygons.append(transformed)
	for child_value: Variant in node.get_children():
		_collect_polygons(child_value as Node, polygons)


func _subtree_has_green(node: Node) -> bool:
	return _subtree_has_color_predicate(node, func(color: Color) -> bool:
		return color.a > 0.25 and color.g >= 0.45 \
			and color.g > color.r * 1.12 and color.g > color.b * 1.05)


func _subtree_has_color(node: Node, expected: Color) -> bool:
	return _subtree_has_color_predicate(node, func(color: Color) -> bool:
		return color.a > 0.25 and Color(color.r, color.g, color.b).is_equal_approx(
			Color(expected.r, expected.g, expected.b)))


func _subtree_has_color_predicate(node: Node, predicate: Callable) -> bool:
	if node == null:
		return false
	if node is CanvasItem and (not (node as CanvasItem).is_visible_in_tree()
			or _effective_canvas_alpha(node as CanvasItem) <= 0.02):
		return false
	var colors: Array[Color] = []
	if node is Polygon2D:
		colors.append((node as Polygon2D).color)
	elif node is ColorRect:
		colors.append((node as ColorRect).color)
	elif node is Line2D:
		colors.append((node as Line2D).default_color)
	for color: Color in colors:
		if bool(predicate.call(color)):
			return true
	for child_value: Variant in node.get_children():
		if _subtree_has_color_predicate(child_value as Node, predicate):
			return true
	return false


func _effective_canvas_alpha(item: CanvasItem) -> float:
	if item == null:
		return 0.0
	var alpha: float = item.modulate.a * item.self_modulate.a
	var ancestor: Node = item.get_parent()
	while ancestor != null:
		if ancestor is CanvasItem:
			var canvas_ancestor := ancestor as CanvasItem
			alpha *= canvas_ancestor.modulate.a \
				* canvas_ancestor.self_modulate.a
		ancestor = ancestor.get_parent()
	return alpha


func _check_voice_contract(voice_before: int) -> void:
	var matching := 0
	for request: Dictionary in audio_audit.requests:
		if String(request.get("speaker", "")) == "roshan" \
				and String(request.get("event", "")) == "op_popstar_rhythm":
			matching += 1
	var player := _last_voice_player()
	var request: Dictionary = audio_audit.requests[0] \
		if audio_audit.requests.size() == 1 else {}
	var message: Dictionary = audio_audit.messages[0] \
		if audio_audit.messages.size() == 1 else {}
	_check("Daddy entry sends the exact target+verb objective and voice exactly once",
		audio_audit.requests.size() == 1 and matching == 1
		and audio_audit.messages.size() == 1
		and String(message.get("who", "")) == "Roshan"
		and String(message.get("text", "")) == OBJECTIVE
		and String(message.get("voice", "")) == "op_popstar_rhythm"
		and String(request.get("speaker", "")) == "roshan"
		and String(request.get("event", "")) == "op_popstar_rhythm"
		and is_equal_approx(float(request.get("min_gap", -1.0)), 0.5)
		and main.voice_i == voice_before + 1)
	_check("requested voice resolves to the exact immutable OGG",
		player != null and player.stream != null and player.playing
		and player.stream.resource_path == VOICE_PATH
		and FileAccess.get_sha256(VOICE_PATH) == VOICE_SHA256)


func _check_opening_objective_delivery(surface: Node2D) -> void:
	var note: Node = _stage_node(surface,
		"RainbowNote%d" % melody.active_note_id())
	var pointer: Node = _stage_node(surface, "VisualPointer")
	var note_rect: Rect2 = _node_visual_rect(note)
	var layer: CanvasLayer = melody.active_layer()
	_check("shared objective text remains semantic state occluded below the opaque stage",
		main.hud_msg.text == OBJECTIVE and main.hud_msg.visible
		and main.hud_layer != null and layer != null
		and main.hud_layer.layer < layer.layer
		and _opaque_stage_covers(surface,
			Rect2(Vector2.ZERO, get_root().get_visible_rect().size)))
	_check("opening non-reader objective is carried by the sole live attached visual pointer",
		note_rect.has_area()
		and _pointer_geometry_contract(pointer, note_rect.get_center()))


func _check_tick_and_stage_motion() -> void:
	var before: Dictionary = melody.audit_snapshot()
	var tick_before := int(before.get("tick_count", -1))
	var elapsed_before := float(before.get("elapsed", -1.0))
	var game_time_before := float(main.g.get("t", -1.0))
	await process_frame
	var after: Dictionary = melody.audit_snapshot()
	var tick_after := int(after.get("tick_count", -1))
	var elapsed_after := float(after.get("elapsed", -1.0))
	var game_time_after := float(main.g.get("t", -1.0))
	var elapsed_delta := elapsed_after - elapsed_before
	var game_delta := game_time_after - game_time_before
	var direct_frame_delta: float = main.get_process_delta_time()
	print("MELODY|TICK_FACTS|game_delta=", game_delta,
		"|elapsed_delta=", elapsed_delta,
		"|reported_frame_delta=", direct_frame_delta,
		"|tick_delta=", tick_after - tick_before)
	_check("one rendered frame produces exactly one Melody controller tick",
		tick_before >= 0 and tick_after == tick_before + 1)
	_check("shared ranking clock advances by exactly the one delivered frame delta",
		game_delta > 0.0 and elapsed_delta > 0.0
		and is_equal_approx(game_delta, elapsed_delta))
	_check("runtime motion consumes that same frame delta exactly once",
		game_delta > 0.0 and is_equal_approx(elapsed_delta, game_delta))


func _exercise_negative_and_neutral_input() -> void:
	var before := melody.progress_count()
	await _wait_for_green(false)
	var early_point: Vector2 = melody.active_note_screen_point()
	_push_touch(early_point, true, TOUCH_INDEX + 2)
	_push_touch(early_point, false, TOUCH_INDEX + 2)
	await process_frame
	_check("early note tap makes no progress and carries no penalty",
		melody.progress_count() == before and main.game == "melody")

	await _wait_for_green(true)
	var wrong_point := Vector2(72.0, 110.0)
	_check("wrong-point fixture is outside the active hit and pause zones",
		not melody.active_note_hit_rect().has_point(wrong_point)
		and not (main.touch_ui.pause_zone() as Rect2).has_point(wrong_point))
	_push_touch(wrong_point, true, TOUCH_INDEX + 3)
	_push_touch(wrong_point, false, TOUCH_INDEX + 3)
	await process_frame
	_check("wrong-point tap in the green window makes no progress or fail state",
		melody.progress_count() == before
		and not bool(melody.audit_snapshot().get("completed", true)))

	# Let the same note traverse a complete missed green opportunity and return.
	# Motion is allowed; progress, failure, and note identity are not.
	var missed_id: int = melody.active_note_id()
	await _wait_for_green(false)
	await _wait_for_green(true)
	_check("one complete passive miss recycles forever without progress or penalty",
		melody.progress_count() == before
		and melody.active_note_id() == missed_id
		and main.game == "melody"
		and not bool(melody.audit_snapshot().get("completed", true)))

	await _wait_for_green(false)
	var held_point: Vector2 = melody.active_note_screen_point()
	_push_touch(held_point, true, TOUCH_INDEX + 4)
	_check("early held touch is down but never armed",
		bool(melody.audit_snapshot().get("input_down", false))
		and not bool(melody.audit_snapshot().get("touch_armed", true)))
	await _wait_for_green(true)
	_push_touch(held_point, false, TOUCH_INDEX + 4)
	await process_frame
	_check("holding from early into green cannot smuggle a hit",
		melody.progress_count() == before)

	# Real PauseCornerButton route, held note touch first.
	await _wait_for_green(false)
	var pause_touch_point: Vector2 = melody.active_note_screen_point()
	_push_touch(pause_touch_point, true, TOUCH_INDEX + 5)
	_check("touch press reaches the held controller before pause",
		bool(melody.audit_snapshot().get("input_down", false)))
	await _open_pause_gear(TOUCH_INDEX + 6)
	_check("real pause gear cancels the held touch neutrally",
		paused
		and not bool(melody.audit_snapshot().get("input_down", true))
		and bool(melody.audit_snapshot().get("blocked_until_release", false))
		and melody.progress_count() == before)
	_resume_from_pause_button()
	await _wait_for_green(true)
	_push_touch(pause_touch_point, false, TOUCH_INDEX + 60)
	_push_mouse(pause_touch_point, false, 6)
	_push_touch(pause_touch_point, true, TOUCH_INDEX + 61)
	_push_touch(pause_touch_point, false, TOUCH_INDEX + 61)
	await process_frame
	_check("wrong sources cannot clear or score the touch held across pause",
		melody.progress_count() == before
		and bool(melody.audit_snapshot().get(
			"blocked_until_release", false)))
	_push_touch(pause_touch_point, false, TOUCH_INDEX + 5)
	await process_frame
	_check("held touch release after pause cannot score",
		melody.progress_count() == before
		and not bool(melody.audit_snapshot().get(
			"blocked_until_release", true)))

	# The child may lift the original finger while the Pause sheet is still up.
	# That exact release must reach the neutral latch without touching the sheet,
	# so resume is immediately ready for a wholly fresh gesture.
	await _wait_for_green(false)
	var paused_release_point: Vector2 = melody.active_note_screen_point()
	_push_touch(paused_release_point, true, TOUCH_INDEX + 62)
	await _open_pause_gear(TOUCH_INDEX + 63)
	_push_touch(paused_release_point, false, TOUCH_INDEX + 62)
	await process_frame
	_check("the original source may clear its own neutral latch while still paused",
		paused and melody.progress_count() == before
		and not bool(melody.audit_snapshot().get(
			"blocked_until_release", true))
		and not main._melody_held_sources.has(StringName(
			"touch:0:%d" % (TOUCH_INDEX + 62))))
	_resume_from_pause_button()
	await _wait_for_green(true)
	var after_paused_release_point: Vector2 = melody.active_note_screen_point()
	_push_touch(after_paused_release_point, true, TOUCH_INDEX + 64)
	_push_touch(after_paused_release_point, false, TOUCH_INDEX + 64)
	await process_frame
	_check("first fresh gesture after an in-pause lift scores exactly once",
		melody.progress_count() == before + 1)

	# Same real overlay route, held keyboard.
	before = melody.progress_count()
	await _wait_for_green(false)
	_push_key(KEY_SPACE, true)
	_check("keyboard press reaches the same held controller",
		bool(melody.audit_snapshot().get("input_down", false)))
	await _open_pause_gear(TOUCH_INDEX + 7)
	_check("real pause gear cancels the held keyboard neutrally",
		paused
		and not bool(melody.audit_snapshot().get("input_down", true))
		and bool(melody.audit_snapshot().get("blocked_until_release", false))
		and melody.progress_count() == before)
	_resume_from_pause_button()
	await _wait_for_green(true)
	_push_key(KEY_ENTER, false, 0)
	_push_key(KEY_SPACE, false, 1)
	_push_pad(JOY_BUTTON_A, false, 0)
	await process_frame
	_check("wrong key, device, and pad releases cannot clear paused Space",
		melody.progress_count() == before
		and bool(melody.audit_snapshot().get(
			"blocked_until_release", false)))
	_push_key(KEY_SPACE, false)
	await process_frame
	_check("held keyboard release after pause cannot score",
		melody.progress_count() == before)
	await _wait_for_green(true)
	_push_key(KEY_SPACE, true)
	_push_key(KEY_ENTER, false, 0)
	_push_key(KEY_SPACE, false, 1)
	_push_pad(JOY_BUTTON_A, false, 0)
	await process_frame
	_check("only the exact keyboard owner may finish an armed note",
		melody.progress_count() == before
		and bool(melody.audit_snapshot().get("input_down", false)))
	_push_key(KEY_SPACE, false)
	await process_frame
	_check("fresh keyboard press/release scores exactly one note",
		melody.progress_count() == before + 1)

	# Real PauseCornerButton route again, held pad action on the next note.
	before = melody.progress_count()
	await _wait_for_green(false)
	_push_pad(JOY_BUTTON_A, true)
	await _open_pause_gear(TOUCH_INDEX + 8)
	_check("real pause gear cancels the held pad action neutrally",
		paused
		and not bool(melody.audit_snapshot().get("input_down", true))
		and bool(melody.audit_snapshot().get("blocked_until_release", false))
		and melody.progress_count() == before)
	_resume_from_pause_button()
	await _wait_for_green(true)
	_push_pad(JOY_BUTTON_B, false, 0)
	_push_pad(JOY_BUTTON_A, false, 1)
	_push_key(KEY_SPACE, false, 0)
	await process_frame
	_check("wrong pad button, device, and key cannot clear paused pad A",
		melody.progress_count() == before
		and bool(melody.audit_snapshot().get(
			"blocked_until_release", false)))
	_push_pad(JOY_BUTTON_A, false)
	await process_frame
	_check("held pad release after pause cannot score",
		melody.progress_count() == before)
	await _wait_for_green(true)
	_push_pad(JOY_BUTTON_A, true)
	_push_pad(JOY_BUTTON_B, false, 0)
	_push_pad(JOY_BUTTON_A, false, 1)
	_push_key(KEY_SPACE, false, 0)
	await process_frame
	_check("only the exact pad owner may finish an armed note",
		melody.progress_count() == before
		and bool(melody.audit_snapshot().get("input_down", false)))
	_push_pad(JOY_BUTTON_A, false)
	await process_frame
	_check("fresh pad press/release scores exactly one note",
		melody.progress_count() == before + 1)

	before = melody.progress_count()
	await _wait_for_green(false)
	_push_pad(JOY_BUTTON_A, true, 3)
	main._forget_melody_pad_device(3)
	await process_frame
	_check("controller disconnect neutralizes only its unreleasable held source",
		melody.progress_count() == before
		and not bool(melody.audit_snapshot().get("input_down", true))
		and not bool(melody.audit_snapshot().get(
			"blocked_until_release", true)))

	# A pause raised with no held action must not invent a stale release latch or
	# consume the next entirely fresh note tap.
	before = melody.progress_count()
	await _open_pause_gear(TOUCH_INDEX + 9)
	_check("no-held real pause leaves the controller neutral",
		paused
		and not bool(melody.audit_snapshot().get("input_down", true))
		and not bool(melody.audit_snapshot().get(
			"blocked_until_release", true)))
	_resume_from_pause_button()
	await _wait_for_green(true)
	var post_pause_point: Vector2 = melody.active_note_screen_point()
	_push_touch(post_pause_point, true, TOUCH_INDEX + 10)
	_push_touch(post_pause_point, false, TOUCH_INDEX + 10, 0, true)
	await process_frame
	_check("Android-cancelled touch is neutral and clears only its own source",
		melody.progress_count() == before
		and not bool(melody.audit_snapshot().get("input_down", true))
		and not bool(melody.audit_snapshot().get(
			"blocked_until_release", true)))
	_push_touch(post_pause_point, true, TOUCH_INDEX + 10)
	_push_touch(post_pause_point, false, TOUCH_INDEX + 10, 1)
	_push_touch(post_pause_point, false, TOUCH_INDEX + 70)
	_push_touch(post_pause_point, false, TOUCH_INDEX + 72, 0, true)
	_push_mouse(post_pause_point, false, 7)
	_push_touch(post_pause_point, true, TOUCH_INDEX + 71)
	_push_touch(post_pause_point, false, TOUCH_INDEX + 71)
	await process_frame
	_check("only the exact touch owner may finish an armed note",
		melody.progress_count() == before
		and bool(melody.audit_snapshot().get("input_down", false)))
	_push_touch(post_pause_point, false, TOUCH_INDEX + 10)
	await process_frame
	_check("first fresh tap after no-held pause scores exactly once",
		melody.progress_count() == before + 1)

	# The pause sheet's real Sticker doorway raises a higher Canvas overlay while
	# Melody remains the live game. Its GUI must receive taps, while the note
	# controller consumes only the neutral release of the source held at pause.
	before = melody.progress_count()
	await _wait_for_green(false)
	var overlay_held_point: Vector2 = melody.active_note_screen_point()
	_push_touch(overlay_held_point, true, TOUCH_INDEX + 12)
	_check("touch source is genuinely held before opening the Sticker overlay",
		bool(melody.audit_snapshot().get("input_down", false)))
	await _open_pause_gear(TOUCH_INDEX + 13)
	var sticker_button := main.find_child("PauseStickerButton", true, false) as Button
	_check("real pause sheet exposes its visible Sticker Book doorway",
		sticker_button != null and sticker_button.is_visible_in_tree())
	if sticker_button == null:
		_resume_from_pause_button()
		_push_touch(overlay_held_point, false, TOUCH_INDEX + 12)
		return
	var sticker_point: Vector2 = sticker_button.get_global_rect().get_center()
	_push_touch(sticker_point, true, TOUCH_INDEX + 14)
	_push_touch(sticker_point, false, TOUCH_INDEX + 14)
	await process_frame
	var sticker_back: Button = null
	if main.stickers_layer != null:
		sticker_back = main.stickers_layer.find_child(
			"StickerBookBackButton", true, false) as Button
	_check("real Sticker button opens the higher-layer book without touching progress",
		not paused and main.game == "melody"
		and main.stickers_layer != null and main.stickers_layer.layer > \
			melody.active_layer().layer
		and sticker_back != null and sticker_back.is_visible_in_tree()
		and melody.progress_count() == before
		and not bool(melody.audit_snapshot().get("input_down", true))
		and bool(melody.audit_snapshot().get("blocked_until_release", false)))
	if sticker_back == null:
		if paused:
			_resume_from_pause_button()
		elif main.stickers_layer != null:
			main._close_stickers()
		_push_touch(overlay_held_point, false, TOUCH_INDEX + 12)
		return
	_push_touch(overlay_held_point, false, TOUCH_INDEX + 80)
	_push_mouse(overlay_held_point, false, 8)
	_push_touch(overlay_held_point, true, TOUCH_INDEX + 81)
	_push_touch(overlay_held_point, false, TOUCH_INDEX + 81)
	await process_frame
	_check("overlay traffic cannot clear or score another held touch source",
		main.stickers_layer != null and melody.progress_count() == before
		and bool(melody.audit_snapshot().get(
			"blocked_until_release", false)))
	_push_touch(overlay_held_point, false, TOUCH_INDEX + 12)
	await process_frame
	_check("held source release clears neutrally through the higher overlay",
		melody.progress_count() == before
		and not bool(melody.audit_snapshot().get("input_down", true))
		and not bool(melody.audit_snapshot().get(
			"blocked_until_release", true)))
	var back_point: Vector2 = sticker_back.get_global_rect().get_center()
	var pause_zone: Rect2 = main.touch_ui.pause_zone()
	_check("Sticker Back deliberately exercises its real pause-corner overlap",
		sticker_back.get_global_rect().intersects(pause_zone)
		and pause_zone.has_point(back_point))
	_push_touch(back_point, true, TOUCH_INDEX + 15)
	_push_touch(back_point, false, TOUCH_INDEX + 15)
	await process_frame
	_check("TouchUI yields the overlapping real Back tap to the higher Sticker GUI",
		main.stickers_layer == null and main.game == "melody"
		and not paused
		and main.touch_control_blocks.has("melody")
		and not main.touch_control_blocks.has("stickers")
		and melody.progress_count() == before
		and not bool(melody.audit_snapshot().get("input_down", true))
		and not bool(melody.audit_snapshot().get(
			"blocked_until_release", true)))
	if main.stickers_layer != null:
		main._close_stickers()
		return
	await _wait_for_green(true)
	var post_overlay_point: Vector2 = melody.active_note_screen_point()
	_push_mouse(post_overlay_point, true, 0)
	_push_mouse(post_overlay_point, false, 0, true)
	await process_frame
	_check("cancelled owner mouse is neutral and clears only its own source",
		melody.progress_count() == before
		and not bool(melody.audit_snapshot().get("input_down", true))
		and not bool(melody.audit_snapshot().get(
			"blocked_until_release", true)))
	_push_mouse(post_overlay_point, true, 0)
	_push_mouse(post_overlay_point, false, 1, true)
	_push_mouse(post_overlay_point, false, 1)
	_push_touch(post_overlay_point, false, TOUCH_INDEX + 16)
	await process_frame
	_check("mouse ownership distinguishes device and touch source tokens",
		melody.progress_count() == before
		and bool(melody.audit_snapshot().get("input_down", false)))
	_push_mouse(post_overlay_point, false, 0)
	await process_frame
	_check("first fresh green mouse gesture after Sticker Book scores exactly once",
		melody.progress_count() == before + 1)

	# A standalone focus loss retains its source-free guard through arbitrarily
	# many lost-context frames. Only the matching focus restoration permits the
	# next active tick to retire it; the missing old release is never synthesized.
	before = melody.progress_count()
	await _wait_for_green(false)
	var focus_point: Vector2 = melody.active_note_screen_point()
	_push_touch(focus_point, true, TOUCH_INDEX + 11)
	main.notification(Node.NOTIFICATION_APPLICATION_FOCUS_OUT)
	_check("standalone focus loss neutrally forgets the held touch owner",
		not bool(melody.audit_snapshot().get("input_down", true))
		and bool(melody.audit_snapshot().get("blocked_until_release", false))
		and (melody.audit_snapshot().get("blocked_sources", {}) as Dictionary).is_empty()
		and melody.input_context_lost())
	await _frames(3)
	_check("lost focus cannot clear its neutral guard on background frames",
		melody.progress_count() == before
		and bool(melody.audit_snapshot().get("blocked_until_release", false)))
	main.notification(Node.NOTIFICATION_APPLICATION_FOCUS_IN)
	_check("matching focus restoration retains the guard until an active tick",
		not melody.input_context_lost()
		and bool(melody.audit_snapshot().get("blocked_until_release", false)))
	await process_frame
	_check("first active focus-restored tick needs no missing old release",
		melody.progress_count() == before
		and not bool(melody.audit_snapshot().get(
			"blocked_until_release", true)))


func _exercise_system_loss_and_paused_census(
		progress_baseline: Dictionary) -> void:
	# Main is pausable, while TouchUI is the always-processing release relay.
	# Prove that sources which lift under an ordinary Reef pause cannot survive
	# in Melody's process-wide pre-entry census and poison a later Canvas stage.
	var census_point := Vector2(420.0, 260.0)
	var held_touch := StringName("touch:31:%d" % (TOUCH_INDEX + 201))
	var held_mouse := StringName("mouse:32:left")
	var held_key := StringName("key:33:%d" % KEY_SPACE)
	var held_pad := StringName("pad:34:%d" % JOY_BUTTON_A)
	_push_touch(census_point, true, TOUCH_INDEX + 201, 31)
	_push_mouse(census_point, true, 32)
	_push_key(KEY_SPACE, true, 33)
	_push_pad(JOY_BUTTON_A, true, 34)
	_check("ordinary Reef input populates the complete Melody entry-source census",
		main.game == ""
		and main._melody_held_sources.has(held_touch)
		and main._melody_held_sources.has(held_mouse)
		and main._melody_held_sources.has(held_key)
		and main._melody_held_sources.has(held_pad))
	main.toggle_pause()
	_check("ordinary non-Melody pause suspends Main while TouchUI stays live",
		paused and main.game == "" and main.pause_panel.visible)
	_push_touch(census_point, false, TOUCH_INDEX + 201, 31)
	_push_mouse(census_point, false, 32)
	_push_key(KEY_SPACE, false, 33)
	_push_pad(JOY_BUTTON_A, false, 34)
	await process_frame
	_check("paused terminal touch, mouse, key, and pad releases retire the census",
		main._melody_held_sources.is_empty())
	main.pause_resume_btn.pressed.emit()
	await process_frame
	_check("ordinary pause resumes without creating a Melody activity",
		not paused and not main.pause_panel.visible and main.game == "")

	main._activate_touch_interactable("friend:%d" % daddy_index, daddy_index)
	melody = main._game_obj("melody", MelodyGame) as MelodyGame
	var recovery_layer: CanvasLayer = melody.active_layer()
	var recovery_layer_ref: WeakRef = weakref(recovery_layer)
	_check("clean census cannot poison the next Melody entry",
		main.game == "melody" and recovery_layer != null
		and (melody.audit_snapshot().get("blocked_sources", {}) as Dictionary).is_empty())
	await _wait_for_fade_clear()
	await _wait_for_green(true)

	# Real Android ordering may be focus-out -> application-paused, followed by
	# resumed -> focus-in. Neither the first restore nor arbitrary lost-context
	# traffic may thaw the stage, repopulate the census, or clear its guard.
	var before := melody.progress_count()
	var lost_touch_point: Vector2 = melody.active_note_screen_point()
	_push_touch(lost_touch_point, true, TOUCH_INDEX + 202, 41)
	_check("ordered context-loss fixture holds a concrete touch owner",
		bool(melody.audit_snapshot().get("input_down", false)))
	var lost_game_time := float(main.g.get("t", -1.0))
	var lost_elapsed := float(melody.audit_snapshot().get("elapsed", -1.0))
	main.notification(Node.NOTIFICATION_APPLICATION_FOCUS_OUT)
	main.notification(Node.NOTIFICATION_APPLICATION_PAUSED)
	var runtime_reasons: Array = melody.audit_snapshot().get(
		"input_context_loss_reasons", []) as Array
	_check("focus-out then application-paused tracks both reasons behind one guard",
		not bool(melody.audit_snapshot().get("input_down", true))
		and bool(melody.audit_snapshot().get("blocked_until_release", false))
		and (melody.audit_snapshot().get("blocked_sources", {}) as Dictionary).is_empty()
		and main._melody_held_sources.is_empty()
		and main._melody_input_context_lost() and melody.input_context_lost()
		and main._melody_input_context_losses.size() == 2
		and main._melody_input_context_losses.has(&"focus")
		and main._melody_input_context_losses.has(&"application")
		and runtime_reasons.size() == 2
		and runtime_reasons.has(&"focus")
		and runtime_reasons.has(&"application"))
	await _frames(4)
	var lost_pause_point: Vector2 = main.touch_ui.pause_zone().get_center()
	_push_touch(lost_pause_point, true, TOUCH_INDEX + 250, 46)
	_push_touch(lost_pause_point, false, TOUCH_INDEX + 250, 46)
	_push_mouse(lost_pause_point, true, 47)
	_push_mouse(lost_pause_point, false, 47)
	await process_frame
	_check("lost context consumes the real touch and mouse Pause-corner target",
		not paused and not main.pause_panel.visible
		and main.game == "melody" and melody.progress_count() == before)
	_push_lost_context_traffic(Vector2(80.0, 680.0), 45, true)
	await process_frame
	_check("lost-context touch, mouse, key, and pad presses cannot claim census state",
		melody.progress_count() == before
		and is_equal_approx(float(main.g.get("t", -2.0)), lost_game_time)
		and is_equal_approx(float(melody.audit_snapshot().get(
			"elapsed", -2.0)), lost_elapsed)
		and main._melody_held_sources.is_empty()
		and bool(melody.audit_snapshot().get("blocked_until_release", false))
		and (melody.audit_snapshot().get("blocked_sources", {}) as Dictionary).is_empty()
		and not bool(melody.audit_snapshot().get("input_down", true)))
	_push_lost_context_traffic(Vector2(80.0, 680.0), 45, false)
	await process_frame
	_check("lost-context touch, mouse, key, and pad releases are also inert",
		melody.progress_count() == before
		and is_equal_approx(float(main.g.get("t", -2.0)), lost_game_time)
		and is_equal_approx(float(melody.audit_snapshot().get(
			"elapsed", -2.0)), lost_elapsed)
		and main._melody_held_sources.is_empty()
		and bool(melody.audit_snapshot().get("blocked_until_release", false))
		and (melody.audit_snapshot().get("blocked_sources", {}) as Dictionary).is_empty()
		and not bool(melody.audit_snapshot().get("input_down", true)))
	main.notification(Node.NOTIFICATION_APPLICATION_RESUMED)
	await _frames(2)
	runtime_reasons = melody.audit_snapshot().get(
		"input_context_loss_reasons", []) as Array
	_check("resumed alone cannot override the still-lost focus reason",
		main._melody_input_context_lost() and melody.input_context_lost()
		and melody.progress_count() == before
		and main._melody_held_sources.is_empty()
		and bool(melody.audit_snapshot().get("blocked_until_release", false))
		and main._melody_input_context_losses.size() == 1
		and main._melody_input_context_losses.has(&"focus")
		and runtime_reasons.size() == 1 and runtime_reasons.has(&"focus"))
	_push_lost_context_traffic(Vector2(80.0, 680.0), 55, true)
	await process_frame
	_check("partially restored context still rejects every fresh source press",
		melody.progress_count() == before
		and main._melody_held_sources.is_empty()
		and bool(melody.audit_snapshot().get("blocked_until_release", false)))
	_push_lost_context_traffic(Vector2(80.0, 680.0), 55, false)
	await process_frame
	_check("partially restored context still rejects every terminal release",
		melody.progress_count() == before
		and main._melody_held_sources.is_empty()
		and bool(melody.audit_snapshot().get("blocked_until_release", false)))
	main.notification(Node.NOTIFICATION_APPLICATION_FOCUS_IN)
	_check("full ordered restoration keeps a source-free guard until its tick",
		not main._melody_input_context_lost() and not melody.input_context_lost()
		and main._melody_input_context_blocks_input()
		and melody.input_context_blocks_input()
		and main._melody_held_sources.is_empty()
		and bool(melody.audit_snapshot().get("blocked_until_release", false)))
	_push_lost_context_traffic(lost_pause_point, 65, true)
	_check("pre-tick restored presses cannot enter Main census, arm Melody, or score",
		not paused and not main.pause_panel.visible
		and melody.progress_count() == before
		and main._melody_held_sources.is_empty()
		and not bool(melody.audit_snapshot().get("input_down", true))
		and bool(melody.audit_snapshot().get("blocked_until_release", false)))
	await process_frame
	_check("first restored tick clears only the guard, never preserves pre-tick presses",
		melody.progress_count() == before
		and not main._melody_input_context_blocks_input()
		and not melody.input_context_blocks_input()
		and main._melody_held_sources.is_empty()
		and not bool(melody.audit_snapshot().get("input_down", true))
		and not bool(melody.audit_snapshot().get("blocked_until_release", true)))
	# Deliberately never send any of the four old releases. A neutral exit and
	# rebuild must still start source-clean rather than carrying phantom owners.
	await _leave_through_real_pause_gear()
	_check("unreleased pre-tick sources cannot poison a neutral Melody leave",
		main.game == "" and _progress_snapshot() == progress_baseline
		and main._melody_held_sources.is_empty() and melody.active_layer() == null)
	await _wait_for_fade_clear()
	_check("pre-tick-source recovery teardown frees its first Canvas subtree",
		recovery_layer_ref.get_ref() == null)
	main._populate_touch_interactables()
	var recovery_daddy_node: Variant = daddy_friend.get("node")
	var recovery_camera: Variant = main.player.get("cam")
	var recovery_daddy_point := Vector2(-1.0, -1.0)
	if recovery_camera != null and recovery_daddy_node != null:
		recovery_daddy_point = recovery_camera.unproject_position(
			recovery_daddy_node.global_position)
	var recovery_viewport: Rect2 = main.get_viewport().get_visible_rect()
	_check("missing-release recovery exposes Daddy through the real Reef camera",
		recovery_camera != null and recovery_daddy_node != null
		and recovery_viewport.has_point(recovery_daddy_point)
		and not _touch_target("friend:%d" % daddy_index).is_empty())
	var recovery_touch_index := TOUCH_INDEX + 251
	_push_touch(recovery_daddy_point, true, recovery_touch_index)
	_push_touch(recovery_daddy_point, false, recovery_touch_index)
	await process_frame
	_check("first recovery one-finger Daddy tap focuses PLAY without launching",
		main.game == "" and main.touch_focus_id == "friend:%d" % daddy_index
		and main.touch_focus_ready)
	_push_touch(recovery_daddy_point, true, recovery_touch_index)
	_push_touch(recovery_daddy_point, false, recovery_touch_index)
	_check("second recovery one-finger Daddy PLAY tap enters through production routing",
		main.game == "melody" and main.g.get("fr", {}) == daddy_friend)
	melody = main._game_obj("melody", MelodyGame) as MelodyGame
	recovery_layer = melody.active_layer()
	recovery_layer_ref = weakref(recovery_layer)
	_check("reentry after missing releases has no inherited census or exact owner",
		main.game == "melody" and recovery_layer != null
		and main._melody_held_sources.is_empty()
		and (melody.audit_snapshot().get(
			"blocked_sources", {}) as Dictionary).is_empty())
	await _wait_for_fade_clear()
	await _wait_for_green(true)
	before = melody.progress_count()
	_push_key(KEY_SPACE, true, 42)
	_push_key(KEY_SPACE, false, 42)
	await process_frame
	_check("different fresh gesture scores exactly once after source-clean reentry",
		melody.progress_count() == before + 1)

	# Reverse both halves: application-paused -> focus-out, then focus-in ->
	# resumed. The remaining application reason must be independently binding.
	before = melody.progress_count()
	await _wait_for_green(true)
	_push_pad(JOY_BUTTON_A, true, 43)
	_check("reverse-order context-loss fixture holds a concrete pad owner",
		bool(melody.audit_snapshot().get("input_down", false)))
	main.notification(Node.NOTIFICATION_APPLICATION_PAUSED)
	main.notification(Node.NOTIFICATION_APPLICATION_FOCUS_OUT)
	runtime_reasons = melody.audit_snapshot().get(
		"input_context_loss_reasons", []) as Array
	_check("application-paused then focus-out also retains both exact reasons",
		main._melody_input_context_losses.size() == 2
		and main._melody_input_context_losses.has(&"focus")
		and main._melody_input_context_losses.has(&"application")
		and runtime_reasons.size() == 2
		and runtime_reasons.has(&"focus")
		and runtime_reasons.has(&"application"))
	await _frames(3)
	_push_lost_context_traffic(Vector2(80.0, 680.0), 75, true)
	await process_frame
	_check("reverse loss ordering also ignores all traffic and forgets its owner",
		not bool(melody.audit_snapshot().get("input_down", true))
		and bool(melody.audit_snapshot().get("blocked_until_release", false))
		and (melody.audit_snapshot().get("blocked_sources", {}) as Dictionary).is_empty()
		and main._melody_held_sources.is_empty()
		and melody.progress_count() == before)
	_push_lost_context_traffic(Vector2(80.0, 680.0), 75, false)
	await process_frame
	_check("reverse-order terminal traffic cannot mutate the empty census",
		not bool(melody.audit_snapshot().get("input_down", true))
		and bool(melody.audit_snapshot().get("blocked_until_release", false))
		and main._melody_held_sources.is_empty()
		and melody.progress_count() == before)
	main.notification(Node.NOTIFICATION_APPLICATION_FOCUS_IN)
	await process_frame
	runtime_reasons = melody.audit_snapshot().get(
		"input_context_loss_reasons", []) as Array
	_check("focus-in alone cannot override the still-paused application reason",
		main._melody_input_context_lost() and melody.input_context_lost()
		and bool(melody.audit_snapshot().get("blocked_until_release", false))
		and melody.progress_count() == before
		and main._melody_input_context_losses.size() == 1
		and main._melody_input_context_losses.has(&"application")
		and runtime_reasons.size() == 1
		and runtime_reasons.has(&"application"))
	main.notification(Node.NOTIFICATION_APPLICATION_RESUMED)
	_check("reverse full restoration also retains its pre-tick guard",
		not main._melody_input_context_lost() and not melody.input_context_lost()
		and bool(melody.audit_snapshot().get("blocked_until_release", false)))
	await process_frame
	_check("reverse restoration clears the guard on its first active tick",
		not bool(melody.audit_snapshot().get("blocked_until_release", true)))
	var fresh_touch_point: Vector2 = melody.active_note_screen_point()
	_push_touch(fresh_touch_point, true, TOUCH_INDEX + 203, 44)
	_push_touch(fresh_touch_point, false, TOUCH_INDEX + 203, 44)
	await process_frame
	_check("reverse-order different-source touch gesture scores exactly once",
		melody.progress_count() == before + 1)

	# Nest OS loss inside the real Pause sheet. Context loss supersedes the normal
	# exact-source latch, but full OS restoration while SceneTree is still paused
	# cannot clear the guard; only a subsequent unpaused Melody tick may do so.
	before = melody.progress_count()
	await _wait_for_green(false)
	_push_key(KEY_SPACE, true, 51)
	await _open_pause_gear(TOUCH_INDEX + 204)
	_check("nested fixture starts with a normal exact-source Pause latch",
		paused and bool(melody.audit_snapshot().get("blocked_until_release", false))
		and not (melody.audit_snapshot().get(
			"blocked_sources", {}) as Dictionary).is_empty())
	_check("real Pause accessibility keeps Resume focused for lost-input testing",
		main.pause_resume_btn.has_focus())
	main.notification(Node.NOTIFICATION_APPLICATION_FOCUS_OUT)
	main.notification(Node.NOTIFICATION_APPLICATION_PAUSED)
	var resume_point: Vector2 = main.pause_resume_btn.get_global_rect().get_center()
	var leave_point: Vector2 = main.pause_leave_btn.get_global_rect().get_center()
	_push_touch(resume_point, true, TOUCH_INDEX + 205, 85)
	_push_mouse(leave_point, true, 86)
	_push_key(KEY_ENTER, true, 87)
	_push_pad(JOY_BUTTON_A, true, 88)
	_push_action(&"ui_accept", true)
	await process_frame
	_check("lost-context presses cannot activate real Resume/Leave or focused actions",
		paused and main.pause_panel.visible and main.game == "melody"
		and melody.active_layer() != null
		and main._melody_held_sources.is_empty()
		and melody.progress_count() == before)
	_push_touch(resume_point, false, TOUCH_INDEX + 205, 85)
	_push_mouse(leave_point, false, 86)
	_push_key(KEY_ENTER, false, 87)
	_push_pad(JOY_BUTTON_A, false, 88)
	_push_action(&"ui_accept", false)
	await _frames(3)
	_check("lost-context releases also leave real Pause GUI and Melody untouched",
		paused and melody.input_context_lost()
		and main.pause_panel.visible and main.game == "melody"
		and main._melody_held_sources.is_empty()
		and (melody.audit_snapshot().get("blocked_sources", {}) as Dictionary).is_empty()
		and bool(melody.audit_snapshot().get("blocked_until_release", false))
		and melody.progress_count() == before)
	main.notification(Node.NOTIFICATION_APPLICATION_RESUMED)
	main.notification(Node.NOTIFICATION_APPLICATION_FOCUS_IN)
	await process_frame
	_check("full OS restore cannot clear the guard while Pause remains open",
		paused and not melody.input_context_lost()
		and main._melody_input_context_blocks_input()
		and melody.input_context_blocks_input()
		and bool(melody.audit_snapshot().get("blocked_until_release", false))
		and melody.progress_count() == before
		and main.pause_resume_btn.has_focus())
	_push_action(&"ui_accept", true)
	_push_action(&"ui_accept", false)
	_check("real focused ui_accept resumes without clearing the restored context guard",
		not paused and bool(melody.audit_snapshot().get(
			"blocked_until_release", false)))
	await process_frame
	_check("first active unpaused nested-restoration tick clears the guard",
		not main._melody_input_context_blocks_input()
		and not melody.input_context_blocks_input()
		and not bool(melody.audit_snapshot().get("blocked_until_release", true)))
	await _wait_for_green(true)
	_push_pad(JOY_BUTTON_A, true, 52)
	_push_pad(JOY_BUTTON_A, false, 52)
	await process_frame
	_check("fresh pad gesture after nested restoration scores exactly once",
		melody.progress_count() == before + 1)

	await _leave_through_real_pause_gear()
	_check("system-loss recovery stage leaves neutrally with no reward or save progress",
		main.game == "" and _progress_snapshot() == progress_baseline
		and melody.active_layer() == null and main._melody_held_sources.is_empty())
	await _frames(2)
	_check("system-loss recovery teardown frees its complete Canvas subtree",
		recovery_layer_ref.get_ref() == null)


func _complete_ordered_notes(modes: Array, force_bronze: bool,
		duplicate_first_press: bool) -> Dictionary:
	var result := {
		"ids": [],
		"colors": [],
		"all_armed": true,
		"duplicate_exact_once": not duplicate_first_press,
	}
	for expected_id in range(7):
		if main.game != "melody":
			break
		var green := await _wait_for_green(true)
		if not green or melody.active_note_id() != expected_id:
			break
		(result["ids"] as Array).append(melody.active_note_id())
		(result["colors"] as Array).append(_active_note_actual_color())
		if force_bronze and expected_id == 6:
			main.g["t"] = 151.0
		var before := melody.progress_count()
		var mode := String(modes[expected_id])
		if mode == "key":
			_push_key(KEY_SPACE, true)
			result["all_armed"] = bool(result["all_armed"]) \
				and bool(melody.audit_snapshot().get("touch_armed", false))
			_push_key(KEY_SPACE, false)
		elif mode == "pad":
			_push_pad(JOY_BUTTON_A, true)
			result["all_armed"] = bool(result["all_armed"]) \
				and bool(melody.audit_snapshot().get("touch_armed", false))
			_push_pad(JOY_BUTTON_A, false)
		else:
			var point: Vector2 = melody.active_note_screen_point()
			_push_touch(point, true, TOUCH_INDEX + 20 + expected_id)
			result["all_armed"] = bool(result["all_armed"]) \
				and bool(melody.audit_snapshot().get("touch_armed", false))
			if duplicate_first_press and expected_id == 0:
				_push_touch(point, true, TOUCH_INDEX + 20 + expected_id)
				result["duplicate_exact_once"] = \
					melody.progress_count() == before
			_push_touch(point, false, TOUCH_INDEX + 20 + expected_id)
		if expected_id == 6 and main.game == "":
			# Capture the synchronous return seam before normal Reef physics gets
			# its next frame and is free to move the player again.
			result["terminal_position"] = main.player.position
			result["terminal_environment"] = main.we_node.environment
			result["terminal_track"] = main.cur_track
			result["terminal_music"] = _music_context()
		await process_frame
		if expected_id < 6:
			_check("ordered note %d scores once on a fresh %s release" \
				% [expected_id, mode],
				main.game == "melody"
				and melody.progress_count() == before + 1
				and melody.active_note_id() == expected_id + 1)
		else:
			_check("seventh ordered note completes without a fail/timer branch",
				main.game == "" and bool(daddy_friend.get("won", false)))
	return result


func _leave_through_real_pause_gear() -> void:
	await _open_pause_gear(TOUCH_INDEX + 8)
	_check("real pause sheet exposes its neutral BACK doorway",
		paused and main.pause_panel.visible
		and main.pause_leave_btn.visible
		and bool(main.pause_leave_btn.get_meta("neutral_exit", false)))
	main.pause_leave_btn.grab_focus()
	_check("neutral BACK doorway owns real focused Pause GUI input",
		main.pause_leave_btn.has_focus())
	_push_action(&"ui_accept", true)
	_push_action(&"ui_accept", false)


func _open_pause_gear(_index: int) -> void:
	var navigation := main.find_child(
		"GlobalNavigationButton", true, false) as Button
	_check("Melody exposes only the global Back control",
		navigation != null and navigation.visible
		and String(navigation.get_meta("global_navigation_mode", "")) == "back"
		and main.find_child("PauseCornerButton", true, false) == null)
	# Pause-cancellation semantics are still exercised through the internal Menu
	# command; pressing the visible global control now correctly leaves Melody.
	main.toggle_pause()
	await process_frame
	_check("internal Menu command raises the production Menu sheet",
		paused and main.pause_panel.visible)


func _resume_from_pause_button() -> void:
	main.pause_resume_btn.pressed.emit()
	_check("real resume button restores the live Melody stage",
		not paused and not main.pause_panel.visible
		and main.game == "melody")


func _wait_for_green(wanted: bool, limit: int = 900) -> bool:
	for _index in range(limit):
		if main.game != "melody" or melody.active_note_id() < 0:
			return false
		var in_green: bool = melody.timing_zone_screen_rect().has_point(
			melody.active_note_screen_point())
		if in_green == wanted:
			return true
		await process_frame
	return false


func _wait_for_fade_clear(limit: int = 120) -> bool:
	for _index in range(limit):
		if main.fade_rect == null or (main.fade_rect.modulate.a <= 0.02 \
				and main.fade_rect.mouse_filter == Control.MOUSE_FILTER_IGNORE):
			return true
		await process_frame
	_check("entry fade clears visually and restores input within its bounded reveal",
		false)
	return false


func _push_touch(position: Vector2, pressed: bool, index: int,
		device: int = 0, canceled: bool = false) -> void:
	var event := InputEventScreenTouch.new()
	event.device = device
	event.index = index
	event.position = position
	event.pressed = pressed
	event.canceled = canceled
	main.get_viewport().push_input(event, false)


func _push_mouse(position: Vector2, pressed: bool, device: int = 0,
		canceled: bool = false) -> void:
	var event := InputEventMouseButton.new()
	event.device = device
	event.button_index = MOUSE_BUTTON_LEFT
	event.position = position
	event.pressed = pressed
	event.canceled = canceled
	main.get_viewport().push_input(event, false)


func _push_key(keycode: Key, pressed: bool, device: int = 0) -> void:
	var event := InputEventKey.new()
	event.device = device
	event.physical_keycode = keycode
	event.pressed = pressed
	event.echo = false
	main.get_viewport().push_input(event, false)


func _push_pad(button: JoyButton, pressed: bool, device: int = 0) -> void:
	var event := InputEventJoypadButton.new()
	event.device = device
	event.button_index = button
	event.pressed = pressed
	main.get_viewport().push_input(event, false)


func _push_action(action: StringName, pressed: bool) -> void:
	var event := InputEventAction.new()
	event.action = action
	event.pressed = pressed
	main.get_viewport().push_input(event, false)


func _push_lost_context_traffic(position: Vector2, seed_value: int,
		pressed: bool) -> void:
	# Every supported gameplay vocabulary is deliberately exercised while the OS
	# context is absent. Presses and releases are separate real Viewport phases so
	# transient census repopulation cannot hide behind a back-to-back erase.
	_push_touch(position, pressed, TOUCH_INDEX + seed_value, seed_value)
	_push_mouse(position, pressed, seed_value + 1)
	_push_key(KEY_ENTER, pressed, seed_value + 2)
	_push_pad(JOY_BUTTON_X, pressed, seed_value + 3)


func _find_daddy_route() -> void:
	var melody_routes := 0
	for index in range(main.friends.size()):
		var friend := main.friends[index] as Dictionary
		if String(friend.get("game", "")) == "melody":
			melody_routes += 1
			if daddy_friend.is_empty():
				daddy_friend = friend
				daddy_index = index
	_check("Daddy Mermaid owns the sole Melody friend route at the canonical slot",
		melody_routes == 1 and daddy_index == 3 and String(daddy_friend.get(
			"fname", "")) == "Daddy Mermaid")


func _touch_target(target_id: String) -> Dictionary:
	for target_value: Variant in main.touch_interactables:
		var target := target_value as Dictionary
		if String(target.get("id", "")) == target_id:
			return target
	return {}


func _active_layer_count() -> int:
	var count := 0
	for child_value: Variant in main.get_children():
		var child := child_value as Node
		if child != null and child.name == &"MelodyCanvasLayer":
			count += 1
	return count


func _count_spatial_descendants(node: Node) -> int:
	if node == null:
		return 0
	var total := 0
	for child_value: Variant in node.get_children():
		var child := child_value as Node
		if child is Node3D:
			total += 1
		total += _count_spatial_descendants(child)
	return total


func _direct_child_ids() -> Dictionary:
	var ids: Dictionary = {}
	for child_value: Variant in main.get_children():
		var child := child_value as Node
		if child != null:
			ids[child.get_instance_id()] = true
	return ids


func _only_layer_added(baseline: Dictionary, layer: CanvasLayer) -> bool:
	if layer == null or baseline.has(layer.get_instance_id()):
		return false
	var current := _direct_child_ids()
	if current.size() != baseline.size() + 1 \
			or not current.has(layer.get_instance_id()):
		return false
	for instance_id: Variant in baseline:
		if not current.has(instance_id):
			return false
	return true


func _only_layer_and_touch_sparkles_added(baseline: Dictionary,
		layer: CanvasLayer) -> bool:
	if layer == null or baseline.has(layer.get_instance_id()):
		return false
	var layer_seen := false
	for child_value: Variant in main.get_children():
		var child := child_value as Node
		if child == null or baseline.has(child.get_instance_id()):
			continue
		if child == layer:
			layer_seen = true
			continue
		# The production focus/activate router adds one short, one-shot sparkle
		# for each real tap. It is not Melody stage ownership and frees itself.
		if not (child is Node3D) or not bool(child.get("one_shot")) \
				or int(child.get("amount")) != 36 \
				or not is_equal_approx(float(child.get("lifetime")), 1.1):
			return false
	for instance_id: Variant in baseline:
		if not _direct_child_ids().has(instance_id):
			return false
	return layer_seen


func _game_node_ids() -> Array[int]:
	var ids: Array[int] = []
	for node_value: Variant in main.game_nodes:
		var node := node_value as Node
		if node != null and is_instance_valid(node):
			ids.append(node.get_instance_id())
	return ids


func _progress_snapshot() -> Dictionary:
	return {
		"won": bool(daddy_friend.get("won", false)),
		"trophies": main.trophies,
		"medals": main.medals.duplicate(true),
		"stickers": main.stickers.duplicate(true),
	}


func _music_context() -> Dictionary:
	if main.music == null:
		return {}
	return {
		"track": main.cur_track,
		"stream_path": main.music.stream.resource_path \
			if main.music.stream != null else "",
		"playing": main.music.playing,
		"volume_db": main.music.volume_db,
		"pitch_scale": main.music.pitch_scale,
	}


func _music_context_matches(expected: Dictionary) -> bool:
	if expected.is_empty():
		return main.music == null
	var actual: Dictionary = _music_context()
	return _music_context_values_match(actual, expected)


func _music_context_values_match(actual: Dictionary,
		expected: Dictionary) -> bool:
	# Volume is a live speech-duck envelope, not durable route state. Exact
	# objective/win voices legitimately move it while the track is restored.
	return String(actual.get("track", "")) == String(expected.get("track", "")) \
		and String(actual.get("stream_path", "")) == String(
			expected.get("stream_path", "")) \
		and bool(actual.get("playing", false)) == bool(
			expected.get("playing", false)) \
		and is_equal_approx(float(actual.get("pitch_scale", 0.0)),
			float(expected.get("pitch_scale", 0.0)))


func _chime_tuning() -> Dictionary:
	if main.chime == null:
		return {}
	return {
		"volume_db": main.chime.volume_db,
		"pitch_scale": main.chime.pitch_scale,
	}


func _chime_tuning_restored() -> bool:
	if chime_tuning_before.is_empty() or main.chime == null:
		return false
	var actual: Dictionary = _chime_tuning()
	return is_equal_approx(float(actual.get("volume_db", 0.0)),
		float(chime_tuning_before.get("volume_db", 0.0))) \
		and is_equal_approx(float(actual.get("pitch_scale", 0.0)),
			float(chime_tuning_before.get("pitch_scale", 0.0)))


func _last_voice_player() -> AudioStreamPlayer:
	if main.voice_pool.is_empty() or main.voice_i <= 0:
		return null
	return main.voice_pool[(main.voice_i - 1) % main.voice_pool.size()] \
		as AudioStreamPlayer


func _colors_equal(actual: Array, expected: Array[Color]) -> bool:
	if actual.size() != expected.size():
		return false
	for index in range(expected.size()):
		if not (actual[index] as Color).is_equal_approx(expected[index]):
			return false
	return true


func _actual_note_colors(surface: Node) -> Array:
	var colors: Array = []
	for note_index in range(7):
		var note: Node = _stage_node(surface, "RainbowNote%d" % note_index)
		colors.append(_note_geometry_color(note,
			note_index == melody.active_note_id()))
	return colors


func _active_note_actual_color() -> Color:
	var surface: Node2D = melody.surface()
	var note: Node = _stage_node(surface,
		"RainbowNote%d" % melody.active_note_id())
	return _note_geometry_color(note, true)


func _note_geometry_color(note: Node, expected_visible: bool) -> Color:
	if not (note is CanvasItem):
		return Color.BLACK
	var note_item := note as CanvasItem
	var geometry: Node = _stage_node(note, "NoteColorGeometry")
	if not (geometry is Polygon2D) \
			or geometry.get_parent() != note \
			or _count_nodes_named(note, "NoteColorGeometry") != 1:
		return Color.BLACK
	var polygon := geometry as Polygon2D
	if note_item.visible != expected_visible \
			or polygon.visible == false \
			or polygon.is_visible_in_tree() != expected_visible \
			or polygon.polygon.size() < 20 \
			or not _points_rect(polygon.polygon).has_area() \
			or polygon.color.a <= 0.85:
		return Color.BLACK
	return polygon.color


func _read_probe_save() -> Dictionary:
	var file := FileAccess.open(probe_save_path, FileAccess.READ)
	if file == null:
		return {}
	var parsed: Variant = JSON.parse_string(file.get_as_text())
	return parsed as Dictionary if parsed is Dictionary else {}


func _file_fingerprint(path: String) -> Dictionary:
	var exists := FileAccess.file_exists(path)
	return {
		"path": path.get_file(),
		"exists": exists,
		"sha256": FileAccess.get_sha256(path) if exists else "",
		"modified_time": FileAccess.get_modified_time(path) if exists else 0,
	}


func _artifact_fingerprints(base_path: String) -> Array[Dictionary]:
	var result: Array[Dictionary] = []
	for suffix: String in SAVE_SUFFIXES:
		result.append(_file_fingerprint(base_path + suffix))
	return result


func _same_fingerprints(before: Array[Dictionary],
		after: Array[Dictionary]) -> bool:
	if before.size() != after.size():
		return false
	for index in range(before.size()):
		if before[index] != after[index]:
			return false
	return true


func _remove_probe_save_artifacts() -> bool:
	var all_removed := true
	for suffix: String in SAVE_SUFFIXES:
		var path := probe_save_path + suffix
		if FileAccess.file_exists(path):
			all_removed = DirAccess.remove_absolute(path) == OK and all_removed
	return all_removed


func _frames(count: int) -> void:
	for _index in range(count):
		await process_frame


func _check(label: String, condition: bool) -> void:
	if condition:
		print("MELODY|OK|", label)
	else:
		bad += 1
		print("MELODY|FAIL|", label)


func _finish() -> void:
	paused = false
	if main != null and is_instance_valid(main):
		main.process_mode = Node.PROCESS_MODE_DISABLED
		main.get_parent().remove_child(main)
		main.free()
	await process_frame
	var normal_after := _artifact_fingerprints(normal_save_path)
	_check("normal save and all recovery artifacts retain exact hash/mtime",
		_same_fingerprints(normal_before, normal_after))
	_check("isolated probe save and recovery artifacts clean up exactly",
		_remove_probe_save_artifacts()
		and not _artifact_fingerprints(probe_save_path).any(
			func(entry: Dictionary) -> bool:
				return bool(entry.get("exists", false))))
	if bad == 0:
		print("MELODY|result: ALL OK")
		quit()
	else:
		print("MELODY|result: %d FAIL" % bad)
		quit(1)
