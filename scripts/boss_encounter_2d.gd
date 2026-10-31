class_name BossEncounter2D
extends RefCounted

## Shared no-death encounter rules. Hosts advance authored animation and call
## resolve_impact only at visible contact. Completed rounds are monotonic;
## rewards, checkpoint persistence and presentation remain host-owned.
enum State { IDLE, TELL, STRIKE, COUNTER_READY, OPENING, RECOVERY, CELEBRATE, COMPLETE }
enum Impact { HIT, NEXT_TELL, COUNTER_READY, IGNORED }

var profile: EncounterProfile2D = null
var patterns: EncounterPatterns2D = null
var state: State = State.IDLE
var completed_rounds: int = 0
var completed_attacks: int = 0
var damage_taken: int = 0
var opening_misses: int = 0
var avoids: int = 0
var counter_elapsed: float = 0.0

func configure(content: EncounterProfile2D, rounds: int = 0,
		damage: int = 0, misses: int = 0, attacks: int = 0) -> void:
	profile = content
	patterns = EncounterPatterns2D.new(content)
	completed_rounds = clampi(rounds, 0, content.phases.size()) if content != null else 0
	completed_attacks = clampi(attacks, 0, content.phases[completed_rounds].attacks.size()) \
		if content != null and not finished() and content.preserve_combo_progress else 0
	damage_taken = maxi(0, damage)
	opening_misses = maxi(0, misses)
	avoids = 0
	counter_elapsed = 0.0
	state = State.COMPLETE if finished() else State.IDLE

func finished() -> bool:
	return profile != null and profile.is_valid() and completed_rounds >= profile.phases.size()

func begin_attack(player: Vector2, boss: Vector2, radius: float) -> void:
	if profile == null or not profile.is_valid() or finished():
		return
	if profile.preserve_combo_progress \
			and completed_attacks >= profile.phases[completed_rounds].attacks.size():
		state = State.COUNTER_READY
		return
	patterns.begin_phase(completed_rounds, player, boss, radius, completed_attacks)
	_assist_warning()
	state = State.TELL

func tick_tell(delta: float) -> bool:
	if state != State.TELL:
		return false
	patterns.tick(delta)
	return patterns.tell_finished()

func begin_strike() -> void:
	if state == State.TELL and patterns.tell_finished():
		patterns.resolved = true
		state = State.STRIKE

func resolve_impact(player: Vector2, boss: Vector2, radius: float) -> Impact:
	if state != State.STRIKE:
		return Impact.IGNORED
	if patterns.contains(player):
		damage_taken += 1
		state = State.RECOVERY
		return Impact.HIT
	avoids += 1
	if profile.preserve_combo_progress:
		completed_attacks += 1
	if patterns.advance_combo(player, boss, radius):
		_assist_warning()
		state = State.TELL
		return Impact.NEXT_TELL
	state = State.COUNTER_READY
	return Impact.COUNTER_READY

func _assist_warning() -> void:
	patterns.tell_time += minf(float(damage_taken + opening_misses)
		* profile.warning_assist_step, profile.warning_assist_max)

func patient_warning() -> bool:
	return profile != null and profile.patient_after_attempts > 0 \
		and damage_taken >= profile.patient_after_attempts


func counter_window() -> float:
	# A patient opening still needs a fresh, targeted input edge. Waiting wins nothing.
	if profile != null and profile.patient_after_attempts > 0 \
			and opening_misses >= profile.patient_after_attempts:
		return INF
	return profile.counter_seconds + minf(float(opening_misses)
		* profile.miss_assist_step, profile.miss_assist_max) if profile != null else 0.0

func open_counter() -> void:
	if state != State.COUNTER_READY:
		return
	counter_elapsed = 0.0
	state = State.OPENING

func tick_counter(delta: float, visual_open: bool) -> bool:
	if state != State.OPENING:
		return false
	# The host reports the real animation window, including its closing frame.
	# Before the first visible frame, a delayed animation cannot consume mercy.
	if visual_open or counter_elapsed > 0.0:
		counter_elapsed += maxf(0.0, delta)
	if counter_elapsed < counter_window():
		return false
	opening_misses += 1
	state = State.RECOVERY
	return true

func try_counter(fresh_edge: bool, target_hit: bool, visual_open: bool) -> bool:
	if state != State.OPENING or not fresh_edge or not target_hit or not visual_open:
		return false
	completed_rounds += 1
	completed_attacks = 0
	state = State.COMPLETE if finished() else State.CELEBRATE
	return true
