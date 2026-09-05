class_name EncounterPhase2D
extends Resource

@export var phase_id: StringName = &"landing"
@export var attacks: Array[EncounterAttack2D] = []

static func make(id: StringName, steps: Array[EncounterAttack2D]) -> EncounterPhase2D:
	var phase := EncounterPhase2D.new()
	phase.phase_id = id
	phase.attacks = steps
	return phase
