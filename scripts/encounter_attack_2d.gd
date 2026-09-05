class_name EncounterAttack2D
extends Resource

## Content data only. An attack locks its target when its warning starts.
enum Shape { CIRCLE, LANE }

@export var shape: Shape = Shape.CIRCLE
@export var radius: float = 5.2
@export var half_width: float = 4.4
@export var warning_seconds: float = 1.4

static func circle(size: float = 5.2, warning: float = 1.4) -> EncounterAttack2D:
	var attack := EncounterAttack2D.new()
	attack.radius = size
	attack.warning_seconds = warning
	return attack

static func lane(width: float = 4.4, warning: float = 1.4) -> EncounterAttack2D:
	var attack := EncounterAttack2D.new()
	attack.shape = Shape.LANE
	attack.half_width = width
	attack.warning_seconds = warning
	return attack
