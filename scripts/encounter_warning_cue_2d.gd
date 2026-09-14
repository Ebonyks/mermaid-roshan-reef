class_name EncounterWarningCue2D
extends RefCounted

## Shared boss grammar: aim visibly, flash a fixed commitment, then launch.
## Presentation samples the attack clock; it cannot finish or award an attack.
const AIM_FRACTION: float = 0.35
const LOCK_FLASHES: int = 3
const MIN_WARNING_SECONDS: float = 2.2

static func aim_progress(progress: float) -> float:
	return smoothstep(0.0, AIM_FRACTION, progress)

static func is_locked(progress: float) -> bool:
	return progress >= AIM_FRACTION

static func lock_brightness(progress: float, launched: bool = false) -> float:
	if launched:
		return 1.0
	if not is_locked(progress):
		return 0.0
	var phase: float = clampf((progress - AIM_FRACTION) / (1.0 - AIM_FRACTION), 0.0, 1.0)
	# Three deliberate local flashes; the footprint never disappears entirely.
	return 0.22 + 0.78 * pow(sin(phase * PI * float(LOCK_FLASHES)), 2.0)

static func imminence(progress: float, launched: bool = false) -> float:
	if launched:
		return 1.0
	var last_flash: float = AIM_FRACTION + (1.0 - AIM_FRACTION) * float(LOCK_FLASHES - 1) / float(LOCK_FLASHES)
	return smoothstep(last_flash, last_flash + 0.035, progress)
