class_name WaterMediumState2D
extends RefCounted

## Pure medium-state reducer for authored Canvas water volumes.
##
## Samples use rendered actor landmarks in one consistent coordinate scale:
## body_height, water_column_depth, face_depth, support_acquired,
## contact_inside, normal_velocity_hps, intent, dive_contact_complete, and
## emerge_contact_complete. Positive face_depth is below the surface.

enum State {
	DRY,
	SHALLOW_WADE,
	SURFACE_SWIM,
	SUBMERGED,
}

enum Intent {
	NONE,
	DEEP_TARGET,
	RISE_OR_EXIT,
}

const DRY_ENTER_RATIO: float = 0.12
const DRY_EXIT_RATIO: float = 0.06
const SURFACE_ENTER_RATIO: float = 0.68
const SURFACE_EXIT_RATIO: float = 0.52
const SUBMERGED_ENTER_RATIO: float = 0.18
const SUBMERGED_EXIT_RATIO: float = 0.08

const DRY_WADE_HOLD_SECONDS: float = 0.10
const WADE_SURFACE_HOLD_SECONDS: float = 0.12
const SURFACE_WADE_HOLD_SECONDS: float = 0.16
const SURFACE_SUBMERGED_HOLD_SECONDS: float = 0.12

const _NO_PENDING_STATE: int = -1
const _TIME_EPSILON: float = 0.000001

var current_state: int = State.DRY
var previous_state: int = State.DRY
var transition_count: int = 0
var pending_state: int = _NO_PENDING_STATE
var pending_seconds: float = 0.0


func reset(initial_state: int = State.DRY) -> void:
	current_state = initial_state if _is_valid_state(initial_state) else State.DRY
	previous_state = current_state
	transition_count = 0
	cancel_pending()


func cancel_pending() -> void:
	pending_state = _NO_PENDING_STATE
	pending_seconds = 0.0


func advance(delta_seconds: float, sample: Dictionary) -> int:
	if delta_seconds <= 0.0:
		return current_state
	var body_height: float = float(sample.get("body_height", 0.0))
	if body_height <= 0.0:
		cancel_pending()
		return current_state

	var candidate_state: int = _candidate_for(sample, body_height)
	if candidate_state == current_state:
		cancel_pending()
		return current_state
	if pending_state != candidate_state:
		pending_state = candidate_state
		pending_seconds = 0.0
	pending_seconds += delta_seconds

	var required_seconds: float = _hold_seconds(current_state, candidate_state)
	if pending_seconds + _TIME_EPSILON < required_seconds:
		return current_state

	previous_state = current_state
	current_state = candidate_state
	transition_count += 1
	cancel_pending()
	return current_state


static func state_name(state: int) -> StringName:
	match state:
		State.DRY:
			return &"DRY"
		State.SHALLOW_WADE:
			return &"SHALLOW_WADE"
		State.SURFACE_SWIM:
			return &"SURFACE_SWIM"
		State.SUBMERGED:
			return &"SUBMERGED"
	return &"UNKNOWN"


func _candidate_for(sample: Dictionary, body_height: float) -> int:
	var column_ratio: float = float(sample.get("water_column_depth", 0.0)) / body_height
	var face_ratio: float = float(sample.get("face_depth", -body_height)) / body_height
	var support_acquired: bool = bool(sample.get("support_acquired", false))
	var contact_inside: bool = bool(sample.get("contact_inside", false))
	var intent: int = int(sample.get("intent", Intent.NONE))
	var dive_contact_complete: bool = bool(sample.get("dive_contact_complete", false))
	var emerge_contact_complete: bool = bool(sample.get("emerge_contact_complete", false))

	match current_state:
		State.DRY:
			if contact_inside and column_ratio >= DRY_ENTER_RATIO:
				return State.SHALLOW_WADE
		State.SHALLOW_WADE:
			if not contact_inside and column_ratio <= DRY_EXIT_RATIO:
				return State.DRY
			if contact_inside and column_ratio >= SURFACE_ENTER_RATIO \
					and (not support_acquired or intent == Intent.DEEP_TARGET):
				return State.SURFACE_SWIM
		State.SURFACE_SWIM:
			if contact_inside and dive_contact_complete \
					and face_ratio >= SUBMERGED_ENTER_RATIO:
				return State.SUBMERGED
			if column_ratio <= SURFACE_EXIT_RATIO and support_acquired:
				return State.SHALLOW_WADE
		State.SUBMERGED:
			if intent == Intent.RISE_OR_EXIT and emerge_contact_complete \
					and face_ratio <= SUBMERGED_EXIT_RATIO:
				return State.SURFACE_SWIM
	return current_state


func _hold_seconds(from_state: int, to_state: int) -> float:
	if (from_state == State.DRY and to_state == State.SHALLOW_WADE) \
			or (from_state == State.SHALLOW_WADE and to_state == State.DRY):
		return DRY_WADE_HOLD_SECONDS
	if from_state == State.SHALLOW_WADE and to_state == State.SURFACE_SWIM:
		return WADE_SURFACE_HOLD_SECONDS
	if from_state == State.SURFACE_SWIM and to_state == State.SHALLOW_WADE:
		return SURFACE_WADE_HOLD_SECONDS
	if (from_state == State.SURFACE_SWIM and to_state == State.SUBMERGED) \
			or (from_state == State.SUBMERGED and to_state == State.SURFACE_SWIM):
		return SURFACE_SUBMERGED_HOLD_SECONDS
	return 0.0


func _is_valid_state(state: int) -> bool:
	return state >= State.DRY and state <= State.SUBMERGED
