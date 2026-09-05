class_name EncounterProfile2D
extends Resource

## Boss content supplies phases and timing; the encounter engine never imports
## characters, voices, rewards, save keys, or a particular scene controller.
@export var encounter_id: StringName = &"encounter"
@export var phases: Array[EncounterPhase2D] = []
@export var counter_seconds: float = 3.2
@export var warning_assist_step: float = 0.18
@export var warning_assist_max: float = 0.9
@export var miss_assist_step: float = 0.45
@export var miss_assist_max: float = 2.4

static func grand_puff() -> EncounterProfile2D:
	var profile := EncounterProfile2D.new()
	profile.encounter_id = &"grand_puff"
	profile.phases = [
		EncounterPhase2D.make(&"puffy", [EncounterAttack2D.circle(5.2, 1.55)]),
		EncounterPhase2D.make(&"dizzy", [EncounterAttack2D.circle(), EncounterAttack2D.circle()]),
		EncounterPhase2D.make(&"angry", [EncounterAttack2D.circle(), EncounterAttack2D.lane()]),
	]
	return profile

static func pepper(rounds: int = 7) -> EncounterProfile2D:
	var profile := EncounterProfile2D.new()
	profile.encounter_id = &"pepper"
	profile.counter_seconds = 4.5
	for index: int in range(maxi(1, rounds)):
		var steps: Array[EncounterAttack2D] = [EncounterAttack2D.circle(4.2, 1.8)]
		if index >= maxi(1, rounds / 3):
			steps.append(EncounterAttack2D.circle(4.2, 1.8) if index < maxi(2, rounds * 2 / 3)
				else EncounterAttack2D.lane(3.4, 1.8))
		profile.phases.append(EncounterPhase2D.make(StringName("shell_%d" % index), steps))
	return profile

func is_valid() -> bool:
	if phases.is_empty() or counter_seconds <= 0.0:
		return false
	for phase: EncounterPhase2D in phases:
		if phase == null or phase.attacks.is_empty():
			return false
		for attack: EncounterAttack2D in phase.attacks:
			if attack == null or attack.warning_seconds < 1.0 or attack.radius <= 0.0 or attack.half_width <= 0.0:
				return false
	return true
