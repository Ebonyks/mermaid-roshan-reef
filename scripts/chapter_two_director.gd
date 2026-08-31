class_name ChapterTwoDirector
extends RefCounted

## Additive Chapter 2 progression for Mermaid Roshan's birthday party.
##
## The director owns policy only. Mutable state remains on ReefMain so the
## existing save owner can persist it without replacing any legacy key. Each
## ordered story career teaches its own first Opera phase; Ballerina and
## Detective still use their exact matching Castle-room plot objectives.

signal hook_event(event_name: String, payload: Dictionary)

const ACT_CHEF := 0
const ACT_DETECTIVE := 1
const ACT_BALLERINA := 2
const ACT_CANDY_MAKER := 3
const ACT_FARMER := 6
const ACT_PAINTER := 10
const ACT_ASTRONAUT := 11
const ACT_POP_STAR := 13
## Retained as an empty compatibility surface: Chapter 2 no longer has a
## separate four-door tutorial prelude. Each story career teaches its own
## first Opera phase when its ordered milestone becomes available.
const INITIAL_TUTORIAL_ACTS: Array[int] = []
## Retired compatibility constant. Chapter 2 has no standalone tutorial
## prelude and never imports skill bits from the global Opera star mask.
const INITIAL_TUTORIAL_MASK := 0

## Additive Chapter 2 resume state. These masks are deliberately separate
## from `opera_stars`: a party job can be part-way through without awarding a
## free-play Opera star, and the same finished prop must survive re-entry.
const STRAWBERRY_PICK_COUNT := 5
const STRAWBERRY_REQUIRED_MASK := 0x1F
const CAKE_PIECE_REQUIRED_MASK := 0x7F
const CAKE_CHEF_PIECE_MASK := 0x1F
const CAKE_CANDY_PIECE_MASK := 0x60
const PARTY_EVENT_PREP := 0
const PARTY_EVENT_CANDLE_FOUND := 1
const PARTY_EVENT_IGNITION := 2
const PARTY_EVENT_SCOUT_SEEN := 3
const PARTY_EVENT_KING_TAKE_COMPLETE := 4
const PARTY_EVENT_MAX := PARTY_EVENT_KING_TAKE_COMPLETE
const FIRST_WAVE_UNLOCK_MASK := 0x0449
const JOB_PHASE_ACTS: Array[int] = [6, 0, 3, 10, 2, 13, 11, 1]
const JOB_PHASE_MASK_LIMITS: Array[int] = [0x0F, 0x1F, 0x0F, 0x07,
	0x07, 0x0F, 0x0F, 0x07]

const SKILL_CHEF := "chef"
const SKILL_DETECTIVE := "detective"
const SKILL_BALLERINA := "ballerina"
const SKILL_CANDY_MAKER := "candy_maker"
const SKILL_FARMER := "strawberry_gatherer"
const SKILL_PAINTER := "birthday_banner_painter"
const SKILL_ASTRONAUT := "rocket_builder"
const SKILL_POP_STAR := "sound_checker"

const OBJECTIVE_OPERA_TUTORIALS := "opera_tutorials"
const OBJECTIVE_FIND_RAINBOW_CANDLE := "find_rainbow_candle"
const OBJECTIVE_STUFFIE_BALLET := "stuffie_ballet"
const OBJECTIVE_PARTY_PREP := "party_prep"
const OBJECTIVE_MAIN_HALL_PARTY := "main_hall_party"
const OBJECTIVE_EMBER_KING_CRASH := "ember_king_crash"

const PLOT_CONTEXT_STUFFIE_BALLET := "chapter2_stuffie_ballet"
const PLOT_CONTEXT_DETECTIVE_CANDLE := "chapter2_detective_candle"

const ACTION_DETECTIVE_SEARCH := "detective_search"
const ACTION_STUFFIE_BALLET := "stuffie_ballet"
const ACTION_START_BIRTHDAY_PARTY := "start_birthday_party"

const EVENT_CHAPTER_STARTED := "chapter2_started"
const EVENT_SKILL_LEARNED := "chapter2_skill_learned"
const EVENT_OBJECTIVE_CHANGED := "chapter2_objective_changed"
const EVENT_RAINBOW_CANDLE_FOUND := "chapter2_rainbow_candle_found"
const EVENT_STUFFIE_BALLET_COMPLETED := "chapter2_stuffie_ballet_completed"
const EVENT_PARTY_CONTRIBUTION := "chapter2_party_contribution"
const EVENT_PARTY_READY := "chapter2_party_ready"
const EVENT_PARTY_STARTED := "chapter2_main_hall_party_started"
const EVENT_EMBER_SCOUT_SEEN := "chapter2_ember_scout_seen"
const EVENT_EMBER_KING_CRASHED := "chapter2_ember_king_crashed"

var m: ReefMain

var active: bool:
	get:
		return m.chapter2_active
	set(value):
		m.chapter2_active = value
var unlocked_opera_mask: int:
	get:
		return m.chapter2_unlocked_opera_mask
	set(value):
		m.chapter2_unlocked_opera_mask = value
var skill_mask: int:
	get:
		return m.chapter2_skill_mask
	set(value):
		m.chapter2_skill_mask = value
var active_objective: String:
	get:
		return m.chapter2_active_objective
	set(value):
		m.chapter2_active_objective = value
var rainbow_candle_found: bool:
	get:
		return m.chapter2_rainbow_candle_found
	set(value):
		m.chapter2_rainbow_candle_found = value
var stuffie_ballet_done: bool:
	get:
		return m.chapter2_stuffie_ballet_done
	set(value):
		m.chapter2_stuffie_ballet_done = value
var farmer_strawberries_ready: bool:
	get:
		return m.chapter2_farmer_strawberries_ready
	set(value):
		m.chapter2_farmer_strawberries_ready = value
var chef_cake_baked: bool:
	get:
		return m.chapter2_chef_cake_baked
	set(value):
		m.chapter2_chef_cake_baked = value
var candy_cake_finished: bool:
	get:
		return m.chapter2_candy_cake_finished
	set(value):
		m.chapter2_candy_cake_finished = value
var party_piece_mask: int:
	get:
		return m.chapter2_party_piece_mask
	set(value):
		m.chapter2_party_piece_mask = value
var strawberry_mask: int:
	get:
		return m.chapter2_strawberry_mask
	set(value):
		m.chapter2_strawberry_mask = value
var cake_piece_mask: int:
	get:
		return m.chapter2_cake_piece_mask
	set(value):
		m.chapter2_cake_piece_mask = value
var job_phase_masks: Array[int]:
	get:
		return m.chapter2_job_phase_masks
	set(value):
		m.chapter2_job_phase_masks = value
var party_event_phase: int:
	get:
		return m.chapter2_party_event_phase
	set(value):
		m.chapter2_party_event_phase = value
var party_started: bool:
	get:
		return m.chapter2_party_started
	set(value):
		m.chapter2_party_started = value
var ember_scout_seen: bool:
	get:
		return m.chapter2_ember_scout_seen
	set(value):
		m.chapter2_ember_scout_seen = value
var ember_king_crashed: bool:
	get:
		return m.chapter2_ember_king_crashed
	set(value):
		m.chapter2_ember_king_crashed = value
var ember_son_seen: bool:
	get:
		return m.chapter2_ember_son_seen
	set(value):
		m.chapter2_ember_son_seen = value
var candle_lit: bool:
	get:
		return m.chapter2_candle_lit
	set(value):
		m.chapter2_candle_lit = value
var candle_taken: bool:
	get:
		return m.chapter2_candle_taken
	set(value):
		m.chapter2_candle_taken = value
var story_complete: bool:
	get:
		return m.chapter2_story_complete
	set(value):
		m.chapter2_story_complete = value
var event_seen: Dictionary:
	get:
		return m.chapter2_event_seen
	set(value):
		m.chapter2_event_seen = value
var event_history: Array[Dictionary]:
	get:
		return m.chapter2_event_history
	set(value):
		m.chapter2_event_history = value


func _init(main: ReefMain) -> void:
	m = main
	event_seen.clear()
	event_history.clear()
	_normalise_state({})


func start_after_boss() -> bool:
	if active or not m.day_one_giant_dust_bunny_boss_defeated:
		return false
	active = true
	unlocked_opera_mask = FIRST_WAVE_UNLOCK_MASK
	_sync_objective()
	_emit_once(EVENT_CHAPTER_STARTED, {
		"objective": active_objective,
		"unlocked_acts": _acts_for_mask(unlocked_opera_mask),
		"unlocked_opera_mask": unlocked_opera_mask,
	})
	return true


func initial_tutorial_act_indices() -> Array[int]:
	return INITIAL_TUTORIAL_ACTS.duplicate()


func can_start_opera_tutorial(act_index: int) -> bool:
	return active and INITIAL_TUTORIAL_ACTS.has(act_index) \
		and (unlocked_opera_mask & (1 << act_index)) != 0 \
		and (skill_mask & (1 << act_index)) == 0


func tutorial_phase_is_active() -> bool:
	return false


func can_start_chapter2_act(act_index: int) -> bool:
	if not active or not ChapterTwoPartyPlan.is_live_act(act_index):
		return false
	# Detective and Ballerina are authored plot beats, so their normal Opera
	# doors stay closed and the room-owned actions remain the only entry point.
	if act_index in [ACT_DETECTIVE, ACT_BALLERINA]:
		return false
	return active_objective == OBJECTIVE_PARTY_PREP \
		and not party_started and not ember_king_crashed \
		and (unlocked_opera_mask & (1 << act_index)) != 0 \
		and next_party_act() == act_index


func is_opera_priority() -> bool:
	return active and active_objective == OBJECTIVE_OPERA_TUTORIALS


func has_skill(skill_id: String) -> bool:
	var act_index := _act_for_skill(skill_id)
	return act_index >= 0 and (skill_mask & (1 << act_index)) != 0


func record_opera_completion(act_index: int,
		plot_context: String = "") -> bool:
	if not active:
		return false
	if plot_context == PLOT_CONTEXT_STUFFIE_BALLET:
		return complete_stuffie_ballet(act_index)
	if plot_context == PLOT_CONTEXT_DETECTIVE_CANDLE:
		return complete_detective_search()
	if plot_context != "" or not INITIAL_TUTORIAL_ACTS.has(act_index):
		return false
	var bit := 1 << act_index
	var learned_now := (skill_mask & bit) == 0
	skill_mask |= bit
	if learned_now:
		_emit_once(EVENT_SKILL_LEARNED, {
			"act_index": act_index,
			"skill_id": _skill_for_act(act_index),
		})
	var previous_objective := active_objective
	_sync_objective()
	_emit_objective_change(previous_objective)
	return learned_now or previous_objective != active_objective


func record_party_contribution(act_index: int) -> bool:
	if not can_start_chapter2_act(act_index) or tutorial_phase_is_active():
		return false
	var bit := 1 << act_index
	if (party_piece_mask & bit) != 0:
		return false
	# Completing a job commits the scene-specific prop milestones as one
	# save-ready snapshot. Partial phase callbacks below remain resumable.
	if act_index == ACT_FARMER:
		strawberry_mask = STRAWBERRY_REQUIRED_MASK
	elif act_index == ACT_CHEF:
		cake_piece_mask |= CAKE_CHEF_PIECE_MASK
	elif act_index == ACT_CANDY_MAKER:
		cake_piece_mask |= CAKE_CANDY_PIECE_MASK
	party_piece_mask |= bit
	_learn_story_skill(act_index)
	if act_index == ACT_PAINTER:
		unlocked_opera_mask = ChapterTwoPartyPlan.ALL_PARTY_MASK
	_sync_job_milestones()
	_sync_party_milestones()
	_emit_once(EVENT_PARTY_CONTRIBUTION, {
		"act_index": act_index,
		"career": String(ChapterTwoPartyPlan.entry_for_act(act_index).get(
			"career", "career")),
		"piece": String(ChapterTwoPartyPlan.entry_for_act(act_index).get(
			"piece", "party_piece")),
		"farmer_strawberries_ready": farmer_strawberries_ready,
		"chef_cake_baked": chef_cake_baked,
		"candy_cake_finished": candy_cake_finished,
	})
	var became_ready := party_is_ready()
	var previous_objective := active_objective
	_sync_objective()
	_emit_objective_change(previous_objective)
	if became_ready:
		_emit_once(EVENT_PARTY_READY, {"piece_mask": party_piece_mask})
	return true


## Record one of the five child-readable strawberry pickups. This is additive
## and safe to call after every touch, so a quit between pickups never loses
## the completed berries. The Farmer party bit is awarded only on job finish.
func record_strawberry_pick(pick_index: int) -> bool:
	if not active or next_party_act() != ACT_FARMER \
			or pick_index < 0 or pick_index >= STRAWBERRY_PICK_COUNT:
		return false
	var bit := 1 << pick_index
	if (strawberry_mask & bit) != 0:
		return false
	strawberry_mask = (strawberry_mask | bit) & STRAWBERRY_REQUIRED_MASK
	return true


## Record the ordered cake construction pieces. Chef owns the five structural
## pieces; Candy Maker owns the final candied berry glaze and placement pieces.
func record_cake_piece(piece_index: int) -> bool:
	if not active or piece_index < 0 or piece_index > 6:
		return false
	var owner_act := ACT_CHEF if piece_index <= 4 else ACT_CANDY_MAKER
	if next_party_act() != owner_act:
		return false
	var bit := 1 << piece_index
	if (cake_piece_mask & bit) != 0:
		return false
	var prior_mask := (1 << piece_index) - 1
	if (cake_piece_mask & prior_mask) != prior_mask:
		return false
	cake_piece_mask = (cake_piece_mask | bit) & CAKE_PIECE_REQUIRED_MASK
	return true


## Generic seam for Opera scene adapters. Phase indices are persisted as a
## compact bitmask; scene-specific callbacks may additionally call the two
## explicit prop methods when a phase contains more than one pickup.
func record_opera_phase_event(act_index: int, phase_index: int,
		phase_name: String = "", completed: bool = true) -> bool:
	if not active or not completed or not ChapterTwoPartyPlan.is_live_act(act_index):
		return false
	if party_started or ember_king_crashed or next_party_act() != act_index:
		return false
	if active_objective not in [OBJECTIVE_PARTY_PREP,
			OBJECTIVE_STUFFIE_BALLET, OBJECTIVE_FIND_RAINBOW_CANDLE]:
		return false
	var slot := JOB_PHASE_ACTS.find(act_index)
	if slot < 0 or phase_index < 0:
		return false
	var limit := JOB_PHASE_MASK_LIMITS[slot]
	if (1 << phase_index) & limit == 0:
		return false
	var phase_mask := job_phase_masks[slot]
	if (phase_mask & (1 << phase_index)) != 0:
		return false
	job_phase_masks[slot] = _ordered_phase_prefix(
		phase_mask | (1 << phase_index), limit)
	if phase_index == 0:
		# The first physical verb is the story tutorial for this career. It
		# teaches the skill without touching the global Opera star mask.
		_learn_story_skill(act_index)
	var changed := true
	if act_index == ACT_CHEF and phase_index <= 4:
		changed = record_cake_piece(phase_index) or changed
	elif act_index == ACT_FARMER and phase_index == 0:
		# The first Farmer phase is the five-touch strawberry harvest. The phase
		# completion callback is authoritative for all five pickups, while direct
		# touch callbacks can still persist them one at a time.
		if strawberry_mask != STRAWBERRY_REQUIRED_MASK:
			strawberry_mask = STRAWBERRY_REQUIRED_MASK
			changed = true
	elif act_index == ACT_CANDY_MAKER:
		# The final Candy Maker phases are the glaze and the placement of the
		# candied strawberries, the two last pieces of the carried cake.
		if phase_index >= 2:
			changed = record_cake_piece(5) or changed
		if phase_index >= 3:
			changed = record_cake_piece(6) or changed
	return changed


func record_opera_phase(act_index: int, phase_index: int,
		phase_name: String = "", completed: bool = true) -> bool:
	return record_opera_phase_event(act_index, phase_index,
		phase_name, completed)


func record_opera_phase_snapshot(act_index: int, snapshot: Dictionary,
		completed: bool = true) -> bool:
	return record_opera_phase_event(act_index,
		int(snapshot.get("phase_index", -1)),
		String(snapshot.get("phase_name", "")), completed)


func resume_phase_index_for_act(act_index: int) -> int:
	# Opera phase masks store a contiguous completed prefix. Resume at the first
	# unfinished phase so a re-entry never replays a completed physical task.
	var slot := JOB_PHASE_ACTS.find(act_index)
	if slot < 0 or slot >= job_phase_masks.size():
		return 0
	var phase_mask := int(job_phase_masks[slot]) & JOB_PHASE_MASK_LIMITS[slot]
	var phase_index := 0
	while phase_index < 8:
		var bit := 1 << phase_index
		if (JOB_PHASE_MASK_LIMITS[slot] & bit) == 0 \
				or (phase_mask & bit) == 0:
			break
		phase_index += 1
	return phase_index


func party_is_ready() -> bool:
	return active \
		and (party_piece_mask & ChapterTwoPartyPlan.ALL_PARTY_MASK) \
		== ChapterTwoPartyPlan.ALL_PARTY_MASK


func next_party_act() -> int:
	var entry := ChapterTwoPartyPlan.next_incomplete_entry(party_piece_mask)
	return int(entry.get("act_index", -1))


func can_start_main_hall_party(room_id: String = "main_hall") -> bool:
	return room_id == "main_hall" and party_is_ready() \
		and not party_started and not ember_king_crashed


func start_main_hall_party(room_id: String = "main_hall") -> bool:
	if not can_start_main_hall_party(room_id):
		return false
	party_started = true
	party_event_phase = PARTY_EVENT_IGNITION
	candle_lit = true
	candle_taken = false
	var previous_objective := active_objective
	_sync_objective()
	_emit_once(EVENT_PARTY_STARTED, {
		"room_id": room_id,
		"candle_lit": true,
		"candle_lighter": "astronaut_party_rocket",
		"rocket_built_by": "astronaut_roshan",
		"cake": "gigantic_birthday_cake",
	})
	_emit_objective_change(previous_objective)
	return true


func can_trigger_ember_king_crash(room_id: String = "main_hall") -> bool:
	return room_id == "main_hall" and party_started and party_is_ready() \
		and candle_lit and party_event_phase >= PARTY_EVENT_SCOUT_SEEN \
		and not ember_king_crashed


func trigger_ember_king_crash(room_id: String = "main_hall") -> bool:
	if not can_trigger_ember_king_crash(room_id):
		return false
	# The King takes the newly lit rainbow candle because he wants it for his
	# own birthday party. Roshan's cake, rocket, stuffies, and other completed
	# preparations remain safe.
	ember_king_crashed = true
	# The runtime uses a deliberately non-identifying, code-native child-sized
	# silhouette. Final transparent identity art remains owner-acceptance work.
	ember_son_seen = true
	party_event_phase = PARTY_EVENT_KING_TAKE_COMPLETE
	candle_lit = false
	candle_taken = true
	story_complete = true
	var previous_objective := active_objective
	_sync_objective()
	_emit_once(EVENT_EMBER_KING_CRASHED, {
		"room_id": room_id,
		"actor": "ember_king",
		"son": "ember_prince_identity_placeholder",
		"son_visible": true,
		"son_identity_art_approved": false,
		"next_arc_seed": "north_star_clue",
		"candle": "rainbow_candle",
		"candle_lit_before_crash": true,
		"candle_departed_lit": true,
		"local_candle_present": false,
		"candle_lit": false,
		"candle_taken": true,
		"stolen_thing": "rainbow_candle",
		"taken_for": "ember_king_birthday_party",
		"motive": "wants_the_candle_for_his_own_birthday",
	})
	_emit_objective_change(previous_objective)
	return true


func record_ember_scout() -> bool:
	if not active or not party_started or ember_king_crashed \
		or ember_scout_seen:
		return false
	ember_scout_seen = true
	party_event_phase = PARTY_EVENT_SCOUT_SEEN
	_emit_once(EVENT_EMBER_SCOUT_SEEN, {"safe": true})
	return true


func room_plot_action(room_id: String) -> String:
	if not active:
		return ""
	match active_objective:
		OBJECTIVE_FIND_RAINBOW_CANDLE:
			if room_id == "library" and next_party_act() == ACT_DETECTIVE:
				return ACTION_DETECTIVE_SEARCH
		OBJECTIVE_STUFFIE_BALLET:
			if room_id == "playroom" and next_party_act() == ACT_BALLERINA:
				return ACTION_STUFFIE_BALLET
		OBJECTIVE_MAIN_HALL_PARTY:
			if room_id == "main_hall":
				return ACTION_START_BIRTHDAY_PARTY
	return ""


func should_show_party_table(room_id: String) -> bool:
	return active and room_id == "main_hall" \
		and stuffie_ballet_done


func complete_detective_search() -> bool:
	if room_plot_action("library") != ACTION_DETECTIVE_SEARCH:
		return false
	rainbow_candle_found = true
	party_piece_mask |= 1 << ACT_DETECTIVE
	_learn_story_skill(ACT_DETECTIVE)
	_sync_party_milestones()
	_sync_job_milestones()
	party_event_phase = PARTY_EVENT_CANDLE_FOUND
	# Discovery never lights the candle. Only the authored party-start beat may
	# ignite it after Astronaut Roshan has built the lighting rocket.
	var previous_objective := active_objective
	_sync_objective()
	_emit_once(EVENT_RAINBOW_CANDLE_FOUND, {
		"room_id": "library",
		"hiding_place": "magic_storybook",
		"lit": false,
	})
	_emit_objective_change(previous_objective)
	return true


func can_start_stuffie_ballet() -> bool:
	return room_plot_action("playroom") == ACTION_STUFFIE_BALLET


func complete_stuffie_ballet(act_index: int) -> bool:
	if act_index != ACT_BALLERINA or not can_start_stuffie_ballet() \
			or stuffie_ballet_done:
		return false
	stuffie_ballet_done = true
	party_piece_mask |= 1 << ACT_BALLERINA
	_learn_story_skill(ACT_BALLERINA)
	_sync_party_milestones()
	_sync_job_milestones()
	var previous_objective := active_objective
	_sync_objective()
	_emit_once(EVENT_STUFFIE_BALLET_COMPLETED, {
		"room_id": "playroom",
		"act_index": act_index,
	})
	_emit_objective_change(previous_objective)
	return true


func should_show_candle(room_id: String) -> bool:
	return active and not party_started and room_id == "library" \
		and rainbow_candle_found


func can_launch_plot_act(room_id: String, act_index: int,
		plot_context: String) -> bool:
	if plot_context == PLOT_CONTEXT_STUFFIE_BALLET:
		return room_id == "playroom" and act_index == ACT_BALLERINA \
			and can_start_stuffie_ballet()
	if plot_context == PLOT_CONTEXT_DETECTIVE_CANDLE:
		return room_id == "library" and act_index == ACT_DETECTIVE \
			and room_plot_action(room_id) == ACTION_DETECTIVE_SEARCH
	return false


func opera_config_overrides(plot_context: String,
		act_index: int = -1) -> Dictionary:
	# Story careers use their complete authored phase set. `reward_policy` is
	# consumed by OperaHouse to suppress the global free-play star while the
	# first phase still teaches the career skill through the director callback.
	if plot_context == "" and can_start_chapter2_act(act_index):
		return {
			"reward_policy": "chapter2_story",
			"chapter2_story_career": true,
			"chapter2_tutorial": false,
			"run_context": _story_run_context(),
			"win_line": "Roshan finished the next birthday-party job!",
		}
	if plot_context == PLOT_CONTEXT_STUFFIE_BALLET \
			and can_launch_plot_act("playroom", ACT_BALLERINA,
				plot_context):
		return {
			"reward_policy": "chapter2_story",
			"chapter2_tutorial": false,
			"chapter2_story_career": true,
			"chapter2_context": PLOT_CONTEXT_STUFFIE_BALLET,
			"chapter2_scene": "stuffie_room",
			"run_context": _story_run_context(),
			"name": "The Stuffies Dance Together",
			"voice": "Ballerina Roshan! Teach your stuffie friends to dance and play together!",
			"win_line": "Roshan taught every stuffie to dance and play together!",
		}
	if plot_context == PLOT_CONTEXT_DETECTIVE_CANDLE \
			and can_launch_plot_act("library", ACT_DETECTIVE,
				plot_context):
		return {
			"reward_policy": "chapter2_story",
			"chapter2_tutorial": false,
			"chapter2_story_career": true,
			"chapter2_context": PLOT_CONTEXT_DETECTIVE_CANDLE,
			"chapter2_scene": "magic_storybook",
			"run_context": _story_run_context(),
			"name": "Find the Unlit Rainbow Candle",
			"voice": "Detective Roshan! Search the magic storybook for the last party piece!",
			"win_line": "Roshan found the rainbow candle. It is still unlit!",
		}
	return {}


func _story_run_context() -> Dictionary:
	return {
		"chapter": "chapter2",
		"reward_policy": "chapter2_story",
		"callbacks": {
			"phase_completed": Callable(m,
				"chapter2_on_opera_phase_snapshot"),
		},
	}


func serialize_state() -> Dictionary:
	return {
		"chapter2_active": active,
		"chapter2_unlocked_opera_mask": unlocked_opera_mask,
		"chapter2_skill_mask": skill_mask,
		"chapter2_active_objective": active_objective,
		"chapter2_rainbow_candle_found": rainbow_candle_found,
		"chapter2_stuffie_ballet_done": stuffie_ballet_done,
		"chapter2_farmer_strawberries_ready": farmer_strawberries_ready,
		"chapter2_chef_cake_baked": chef_cake_baked,
		"chapter2_candy_cake_finished": candy_cake_finished,
		"chapter2_party_piece_mask": party_piece_mask,
		"chapter2_strawberry_mask": strawberry_mask,
		"chapter2_cake_piece_mask": cake_piece_mask,
		"chapter2_job_phase_masks": job_phase_masks.duplicate(),
		"chapter2_party_event_phase": party_event_phase,
		"chapter2_party_started": party_started,
		"chapter2_ember_scout_seen": ember_scout_seen,
		"chapter2_ember_king_crashed": ember_king_crashed,
		"chapter2_ember_son_seen": ember_son_seen,
		"chapter2_candle_lit": candle_lit,
		"chapter2_candle_taken": candle_taken,
		"chapter2_story_complete": story_complete,
	}


func restore_state(raw: Variant) -> void:
	_normalise_state(raw as Dictionary if raw is Dictionary else {})
	event_seen.clear()
	event_history.clear()


func _normalise_state(source: Dictionary) -> void:
	var normalised := normalise_save_patch(source, m.opera_stars)
	active = bool(normalised.get("chapter2_active", false))
	unlocked_opera_mask = int(normalised.get(
		"chapter2_unlocked_opera_mask", 0))
	skill_mask = int(normalised.get("chapter2_skill_mask", 0))
	active_objective = String(normalised.get(
		"chapter2_active_objective", ""))
	rainbow_candle_found = bool(normalised.get(
		"chapter2_rainbow_candle_found", false))
	stuffie_ballet_done = bool(normalised.get(
		"chapter2_stuffie_ballet_done", false))
	party_piece_mask = int(normalised.get("chapter2_party_piece_mask", 0))
	strawberry_mask = int(normalised.get("chapter2_strawberry_mask", 0))
	cake_piece_mask = int(normalised.get("chapter2_cake_piece_mask", 0))
	job_phase_masks = _phase_masks_from_variant(
		normalised.get("chapter2_job_phase_masks", []))
	party_event_phase = int(normalised.get("chapter2_party_event_phase", 0))
	farmer_strawberries_ready = bool(normalised.get(
		"chapter2_farmer_strawberries_ready", false))
	chef_cake_baked = bool(normalised.get(
		"chapter2_chef_cake_baked", false))
	candy_cake_finished = bool(normalised.get(
		"chapter2_candy_cake_finished", false))
	party_started = bool(normalised.get("chapter2_party_started", false))
	ember_scout_seen = bool(normalised.get("chapter2_ember_scout_seen", false))
	ember_king_crashed = bool(normalised.get(
		"chapter2_ember_king_crashed", false))
	ember_son_seen = bool(normalised.get("chapter2_ember_son_seen", false))
	candle_lit = bool(normalised.get("chapter2_candle_lit", false))
	candle_taken = bool(normalised.get("chapter2_candle_taken", false))
	story_complete = bool(normalised.get("chapter2_story_complete", false))


static func normalise_save_patch(raw: Variant, opera_star_mask: int) -> Dictionary:
	var source: Dictionary = raw as Dictionary if raw is Dictionary else {}
	var boss_defeated := _bool_static(
		source, "day_one_giant_dust_bunny_boss_defeated", false)
	# Chapter 2 activation is derived from the real boss defeat boundary. Heal a
	# save written between boss defeat and the chapter-start event instead of
	# trusting an arbitrary active flag.
	var chapter_active := boss_defeated
	var unlocked_mask := _nonnegative_int_static(source,
		"chapter2_unlocked_opera_mask",
		FIRST_WAVE_UNLOCK_MASK if chapter_active else 0) \
		& ChapterTwoPartyPlan.ALL_PARTY_MASK
	if chapter_active:
		unlocked_mask |= FIRST_WAVE_UNLOCK_MASK
	var learned_mask := _nonnegative_int_static(
		source, "chapter2_skill_mask", 0) \
		& ChapterTwoPartyPlan.ALL_PARTY_MASK
	# No standalone tutorials remain; a live chapter always begins at Farmer.
	var all_tutorials_done := chapter_active
	var party_mask := _nonnegative_int_static(
		source, "chapter2_party_piece_mask", 0) \
		& ChapterTwoPartyPlan.ALL_PARTY_MASK
	var strawberry_mask := _nonnegative_int_static(
		source, "chapter2_strawberry_mask", 0) & STRAWBERRY_REQUIRED_MASK
	var cake_piece_mask := _nonnegative_int_static(
		source, "chapter2_cake_piece_mask", 0) & CAKE_PIECE_REQUIRED_MASK
	# Legacy saves only carried the completed party bit; backfill the additive
	# prop mask so the visible cake/strawberry state is not lost on upgrade.
	if (party_mask & (1 << ACT_FARMER)) != 0:
		strawberry_mask = STRAWBERRY_REQUIRED_MASK
	if (party_mask & (1 << ACT_CHEF)) != 0:
		cake_piece_mask |= CAKE_CHEF_PIECE_MASK
	if (party_mask & (1 << ACT_CANDY_MAKER)) != 0:
		cake_piece_mask |= CAKE_CANDY_PIECE_MASK
	var phase_masks := _normalise_phase_masks_static(
		source.get("chapter2_job_phase_masks", []))
	# A complete scene-specific prop is safe evidence for its legacy party bit;
	# the causal prefix below still prevents a skipped job.
	if strawberry_mask == STRAWBERRY_REQUIRED_MASK:
		party_mask |= 1 << ACT_FARMER
	if cake_piece_mask & CAKE_CHEF_PIECE_MASK == CAKE_CHEF_PIECE_MASK:
		party_mask |= 1 << ACT_CHEF
	if cake_piece_mask & CAKE_CANDY_PIECE_MASK == CAKE_CANDY_PIECE_MASK:
		party_mask |= 1 << ACT_CANDY_MAKER
	# Chapter 2 is a causal chain rather than a checklist. Heal malformed or
	# hand-edited saves by retaining only the contiguous earned prefix.
	party_mask = _ordered_party_prefix_static(party_mask)
	# A phase mask is only meaningful for the current contiguous job. Any later
	# job mask without every earlier party contribution is impossible progress;
	# discard it while preserving a valid partial prefix for the current job.
	for slot in range(JOB_PHASE_ACTS.size()):
		if slot == 0:
			continue
		var prerequisite_act := JOB_PHASE_ACTS[slot - 1]
		if (party_mask & (1 << prerequisite_act)) == 0:
			phase_masks[slot] = 0
	if (party_mask & (1 << ACT_PAINTER)) != 0:
		unlocked_mask = ChapterTwoPartyPlan.ALL_PARTY_MASK
	else:
		unlocked_mask = FIRST_WAVE_UNLOCK_MASK
	if (party_mask & (1 << ACT_FARMER)) == 0:
		# Partial Farmer pickups are valid resume state; later cake work is not.
		cake_piece_mask = 0
	if (party_mask & (1 << ACT_CHEF)) == 0:
		# Partial Chef construction is valid after Farmer; Candy cannot precede it.
		cake_piece_mask &= CAKE_CHEF_PIECE_MASK
	# Chef phases have one-to-one physical cake-piece milestones. A malformed
	# save may claim a phase without its visible piece; heal that claim while
	# preserving the valid in-progress prefix for re-entry.
	phase_masks[1] = int(phase_masks[1]) \
		& (cake_piece_mask & CAKE_CHEF_PIECE_MASK)
	learned_mask |= party_mask
	var raw_event_phase := _nonnegative_int_static(
		source, "chapter2_party_event_phase", PARTY_EVENT_PREP)
	var farmer_ready := strawberry_mask == STRAWBERRY_REQUIRED_MASK
	var chef_baked := cake_piece_mask & CAKE_CHEF_PIECE_MASK \
		== CAKE_CHEF_PIECE_MASK
	var candy_finished := cake_piece_mask & CAKE_CANDY_PIECE_MASK \
		== CAKE_CANDY_PIECE_MASK
	var candle_found := (party_mask & (1 << ACT_DETECTIVE)) != 0
	var ballet_done := (party_mask & (1 << ACT_BALLERINA)) != 0
	var party_ready := party_mask == ChapterTwoPartyPlan.ALL_PARTY_MASK
	var legacy_party_started := _bool_static(
		source, "chapter2_party_started", false)
	var legacy_scout_seen := _bool_static(
		source, "chapter2_ember_scout_seen", false)
	var legacy_king_crashed := _bool_static(
		source, "chapter2_ember_king_crashed", false)
	var legacy_candle_found := _bool_static(
		source, "chapter2_rainbow_candle_found", false)
	var event_phase := clampi(raw_event_phase, PARTY_EVENT_PREP,
		PARTY_EVENT_MAX)
	if legacy_king_crashed:
		event_phase = PARTY_EVENT_KING_TAKE_COMPLETE
	elif legacy_scout_seen:
		event_phase = maxi(event_phase, PARTY_EVENT_SCOUT_SEEN)
	elif legacy_party_started:
		event_phase = maxi(event_phase, PARTY_EVENT_IGNITION)
	elif legacy_candle_found or candle_found:
		event_phase = maxi(event_phase, PARTY_EVENT_CANDLE_FOUND)
	if not party_ready:
		event_phase = PARTY_EVENT_PREP
	var party_started := party_ready and event_phase >= PARTY_EVENT_IGNITION
	var scout_seen := party_started and event_phase >= PARTY_EVENT_SCOUT_SEEN
	var king_crashed := party_started \
		and event_phase >= PARTY_EVENT_KING_TAKE_COMPLETE
	# The saved beat means the code-native child-sized silhouette was shown;
	# it does not grant owner acceptance to the pending identity concept.
	var son_seen := king_crashed
	candle_found = party_ready and event_phase >= PARTY_EVENT_CANDLE_FOUND
	var candle_lit := party_started and event_phase >= PARTY_EVENT_IGNITION \
		and not king_crashed
	var candle_taken := king_crashed
	var story_complete := king_crashed
	var objective := _derived_objective_static(
		chapter_active, all_tutorials_done, party_mask,
		party_ready, party_started, king_crashed)
	return {
		"chapter2_active": chapter_active,
		"chapter2_unlocked_opera_mask": unlocked_mask,
		"chapter2_skill_mask": learned_mask,
		"chapter2_active_objective": objective,
		"chapter2_rainbow_candle_found": candle_found,
		"chapter2_stuffie_ballet_done": ballet_done,
		"chapter2_farmer_strawberries_ready": farmer_ready,
		"chapter2_chef_cake_baked": chef_baked,
		"chapter2_candy_cake_finished": candy_finished,
		"chapter2_party_piece_mask": party_mask,
		"chapter2_strawberry_mask": strawberry_mask,
		"chapter2_cake_piece_mask": cake_piece_mask,
		"chapter2_job_phase_masks": phase_masks,
		"chapter2_party_event_phase": event_phase,
		"chapter2_party_started": party_started,
		"chapter2_ember_scout_seen": scout_seen,
		"chapter2_ember_king_crashed": king_crashed,
		"chapter2_ember_son_seen": son_seen,
		"chapter2_candle_lit": candle_lit,
		"chapter2_candle_taken": candle_taken,
		"chapter2_story_complete": story_complete,
	}


static func _ordered_party_prefix_static(raw_mask: int) -> int:
	var prefix := 0
	for act_index: int in ChapterTwoPartyPlan.GUIDE_ORDER:
		var bit := 1 << act_index
		if (raw_mask & bit) == 0:
			break
		prefix |= bit
	return prefix


static func _ordered_phase_prefix(raw_mask: int, limit: int) -> int:
	var prefix := 0
	for bit_index in range(8):
		var bit := 1 << bit_index
		if (limit & bit) == 0 or (raw_mask & bit) == 0:
			break
		prefix |= bit
	return prefix


static func _normalise_phase_masks_static(raw: Variant) -> Array[int]:
	var result: Array[int] = []
	var source: Array = raw as Array if raw is Array else []
	for slot in range(JOB_PHASE_ACTS.size()):
		var value: Variant = source[slot] if slot < source.size() else 0
		var candidate := 0
		if typeof(value) == TYPE_INT:
			candidate = maxi(int(value), 0)
		elif typeof(value) == TYPE_FLOAT:
			var number := float(value)
			if is_finite(number) and number >= 0.0 and number == floorf(number):
				candidate = int(number)
		var limit := JOB_PHASE_MASK_LIMITS[slot]
		result.append(_ordered_phase_prefix(candidate & limit, limit))
	return result


func _phase_masks_from_variant(raw: Variant) -> Array[int]:
	return _normalise_phase_masks_static(raw)


static func _bool_static(source: Dictionary, key: String,
		default_value: bool) -> bool:
	var value: Variant = source.get(key, default_value)
	return bool(value) if typeof(value) == TYPE_BOOL else default_value


static func _nonnegative_int_static(source: Dictionary, key: String,
		default_value: int) -> int:
	var value: Variant = source.get(key, default_value)
	if typeof(value) == TYPE_INT:
		return int(value) if int(value) >= 0 else default_value
	if typeof(value) == TYPE_FLOAT:
		var number := float(value)
		if is_finite(number) and number >= 0.0 and number == floorf(number):
			return int(number)
	return default_value


static func _derived_objective_static(chapter_active: bool,
		all_tutorials_done: bool, party_mask: int, party_ready: bool,
		party_started: bool, king_crashed: bool) -> String:
	if not chapter_active:
		return ""
	if not all_tutorials_done:
		return OBJECTIVE_OPERA_TUTORIALS
	var next_act := _next_party_act_static(party_mask)
	if next_act == ACT_DETECTIVE:
		return OBJECTIVE_FIND_RAINBOW_CANDLE
	if next_act == ACT_BALLERINA:
		return OBJECTIVE_STUFFIE_BALLET
	if not party_ready:
		return OBJECTIVE_PARTY_PREP
	if not party_started:
		return OBJECTIVE_MAIN_HALL_PARTY
	if not king_crashed:
		return OBJECTIVE_EMBER_KING_CRASH
	return ""


static func _next_party_act_static(party_mask: int) -> int:
	for act_index: int in ChapterTwoPartyPlan.GUIDE_ORDER:
		if (party_mask & (1 << act_index)) == 0:
			return act_index
	return -1


static func _acts_for_mask(mask: int) -> Array[int]:
	var result: Array[int] = []
	for act_index: int in ChapterTwoPartyPlan.all_act_indices():
		if (mask & (1 << act_index)) != 0:
			result.append(act_index)
	return result


func _sync_party_milestones() -> void:
	_sync_job_milestones()


func _sync_job_milestones() -> void:
	farmer_strawberries_ready = strawberry_mask == STRAWBERRY_REQUIRED_MASK
	chef_cake_baked = cake_piece_mask & CAKE_CHEF_PIECE_MASK \
		== CAKE_CHEF_PIECE_MASK
	candy_cake_finished = cake_piece_mask & CAKE_CANDY_PIECE_MASK \
		== CAKE_CANDY_PIECE_MASK


func _learn_story_skill(act_index: int) -> void:
	if not ChapterTwoPartyPlan.is_live_act(act_index):
		return
	var bit := 1 << act_index
	if (skill_mask & bit) != 0:
		return
	skill_mask |= bit
	_emit_once(EVENT_SKILL_LEARNED, {
		"act_index": act_index,
		"skill_id": _skill_for_act(act_index),
		"chapter2_story_career": true,
	})


func _sync_objective() -> void:
	active_objective = _derived_objective_static(
		active,
		true,
		party_piece_mask,
		party_is_ready(), party_started, ember_king_crashed)


func _all_tutorials_done() -> bool:
	return (skill_mask & INITIAL_TUTORIAL_MASK) == INITIAL_TUTORIAL_MASK


func _emit_objective_change(previous_objective: String) -> void:
	if previous_objective == active_objective:
		return
	_emit_once(EVENT_OBJECTIVE_CHANGED, {
		"from": previous_objective,
		"objective": active_objective,
	})


func _skill_for_act(act_index: int) -> String:
	match act_index:
		ACT_CHEF:
			return SKILL_CHEF
		ACT_DETECTIVE:
			return SKILL_DETECTIVE
		ACT_BALLERINA:
			return SKILL_BALLERINA
		ACT_CANDY_MAKER:
			return SKILL_CANDY_MAKER
		ACT_FARMER:
			return SKILL_FARMER
		ACT_PAINTER:
			return SKILL_PAINTER
		ACT_ASTRONAUT:
			return SKILL_ASTRONAUT
		ACT_POP_STAR:
			return SKILL_POP_STAR
	return ""


func _act_for_skill(skill_id: String) -> int:
	match skill_id:
		SKILL_CHEF:
			return ACT_CHEF
		SKILL_DETECTIVE:
			return ACT_DETECTIVE
		SKILL_BALLERINA:
			return ACT_BALLERINA
		SKILL_CANDY_MAKER:
			return ACT_CANDY_MAKER
		SKILL_FARMER:
			return ACT_FARMER
		SKILL_PAINTER:
			return ACT_PAINTER
		SKILL_ASTRONAUT:
			return ACT_ASTRONAUT
		SKILL_POP_STAR:
			return ACT_POP_STAR
	return -1


func _emit_once(event_name: String, payload: Dictionary) -> void:
	var discriminator := str(payload.get(
		"skill_id", payload.get("act_index", payload.get("objective",
			payload.get("flame", payload.get("room_id", ""))))))
	var event_id := "%s:%s" % [event_name, discriminator]
	if bool(event_seen.get(event_id, false)):
		return
	event_seen[event_id] = true
	var record := {
		"event": event_name,
		"payload": payload.duplicate(true),
	}
	event_history.append(record)
	hook_event.emit(event_name, payload.duplicate(true))
