class_name ChapterTwoEmberEncounter
extends RefCounted

## Chapter 2's protection encounter uses Grand Puff's shared rules. The host
## owns visible impacts, fresh touch edges, presentation and persistence.
## Every mutable field lives on ReefMain; this satellite owns policy only.
const ROUNDS := 3
const RADIUS := 26.0
const ENGINE_KEY := "chapter2_ember_encounter"

var m: ReefMain

func _init(main: ReefMain) -> void:
	m = main

static func content() -> EncounterProfile2D:
	var profile := EncounterProfile2D.new()
	profile.encounter_id = &"ember_king_protect_friends"
	profile.counter_seconds = 4.5
	profile.warning_assist_max = 2.0
	profile.miss_assist_max = 5.0
	profile.phases = [
		EncounterPhase2D.make(&"royal_stomp", [EncounterAttack2D.circle(5.2, 2.1)]),
		EncounterPhase2D.make(&"double_demand", [
			EncounterAttack2D.circle(5.2, 2.1), EncounterAttack2D.circle(5.2, 2.1)]),
		EncounterPhase2D.make(&"make_way", [
			EncounterAttack2D.circle(5.2, 2.1), EncounterAttack2D.lane(4.4, 2.4)]),
	]
	return profile

func begin() -> BossEncounter2D:
	var engine := BossEncounter2D.new()
	engine.configure(content(), m.chapter2_protection_rounds,
		m.chapter2_protection_bumps, m.chapter2_protection_misses)
	m.g[ENGINE_KEY] = engine
	return engine

func engine() -> BossEncounter2D:
	return m.g.get(ENGINE_KEY) as BossEncounter2D

func accept_counter(fresh_edge: bool, target_hit: bool, visible_open: bool) -> bool:
	var current := engine()
	if current == null or not m.chapter2_party_started \
			or m.chapter2_candle_taken or not m.chapter2_candle_lit:
		return false
	if not current.try_counter(fresh_edge, target_hit, visible_open):
		return false
	m.chapter2_protection_rounds = maxi(m.chapter2_protection_rounds,
		current.completed_rounds)
	checkpoint_assistance()
	return true

func checkpoint_assistance() -> void:
	var current := engine()
	if current == null:
		return
	m.chapter2_protection_bumps = maxi(m.chapter2_protection_bumps,
		current.damage_taken)
	m.chapter2_protection_misses = maxi(m.chapter2_protection_misses,
		current.opening_misses)

func friends_are_safe() -> bool:
	return m.chapter2_protection_rounds == ROUNDS

func teardown() -> void:
	checkpoint_assistance()
	m.g.erase(ENGINE_KEY)

static func normalise_checkpoint(source: Dictionary, party_ready: bool,
		party_started: bool, legacy_complete: bool) -> Dictionary:
	var rounds := _counter(source, "chapter2_protection_rounds", ROUNDS)
	var bumps := _counter(source, "chapter2_protection_bumps", 100000)
	var misses := _counter(source, "chapter2_protection_misses", 100000)
	if not party_ready or not party_started:
		rounds = 0
		bumps = 0
		misses = 0
	# Preserve completed old saves without inventing battle mastery for them.
	var lawn_started: bool = source.get("chapter2_lawn_started", false) is bool \
		and bool(source.get("chapter2_lawn_started", false)) and party_ready
	var beat := _counter(source, "chapter2_lawn_beat", 8)
	if not lawn_started or not party_started:
		beat = 0
	elif legacy_complete:
		beat = maxi(beat, 6)
	elif rounds == ROUNDS:
		beat = 5
	else:
		beat = clampi(beat, 1, 4)
	return {
		"chapter2_lawn_beat": beat,
		"chapter2_protection_rounds": rounds,
		"chapter2_protection_bumps": bumps,
		"chapter2_protection_misses": misses,
		"chapter2_lawn_started": lawn_started,
	}

static func _counter(source: Dictionary, key: String, maximum: int) -> int:
	var value: Variant = source.get(key, 0)
	if value is int:
		return clampi(int(value), 0, maximum)
	if value is float and is_finite(float(value)) and float(value) == floorf(float(value)):
		return clampi(int(value), 0, maximum)
	return 0
