class_name KartDriving
extends RefCounted
## Shared scalar handling from KartGame. Presenters own track geometry, input,
## effects and rewards; both races use these same driving calculations.

const LAPS := 2
const BOOST_MUL := 0.5
const TURBO_TIME := 1.4
const DRIFT_TIERS := [0.0, 0.8, 1.6, 2.4]
const DRIFT_BOOST := [0.0, 0.55, 0.95, 1.4]
const KART_HANDLING := {
	"label": "Rainbow Kart", "blurb": "PRO: turbo champ - pickups charge extra! / CON: no muscle",
	"vmax": 1.0, "steer": 22.0, "wall": 0.82, "mass": 1.0, "mcharge": 1.3,
	"turbo": 1.35, "slip": 0.12, "size": 6.0, "yaw_fix": -PI * 0.5,
	"lean": 0.15,
}


static func advance(kart: Dictionary, curvature: float, delta: float) -> void:
	# The inside of a bend covers less distance. Preserve the original 18% cap.
	var line: float = clampf(float(kart["lat"]) * curvature, -0.18, 0.18)
	kart["s"] = float(kart["s"]) + float(kart["speed"]) * (1.0 - line) * delta


static func charge(kart: Dictionary, vehicle: Dictionary, amount: float) -> void:
	kart["meter"] = minf(1.0,
		float(kart["meter"]) + amount * float(vehicle.get("mcharge", 1.0)))


static func tick_turbo(kart: Dictionary, vehicle: Dictionary, fired: bool,
		touch_live: bool, delta: float) -> bool:
	kart["boost_t"] = maxf(0.0, float(kart["boost_t"]) - delta)
	var want_fire := fired
	if float(kart["meter"]) >= 0.99 and float(kart["boost_t"]) <= 0.0:
		kart["full_t"] = float(kart.get("full_t", 0.0)) + delta
		if float(kart["full_t"]) >= (0.2 if touch_live else 2.5):
			want_fire = true
	else:
		kart["full_t"] = 0.0
	if not want_fire or float(kart["meter"]) < 0.5 or float(kart["boost_t"]) > 0.0:
		return false
	kart["boost_t"] = TURBO_TIME * float(vehicle["turbo"])
	kart["meter"] = maxf(0.0, float(kart["meter"]) - 0.5)
	kart["full_t"] = 0.0
	kart["squash"] = 0.3
	return true


static func accelerate(kart: Dictionary, target: float, boosting: bool,
		delta: float) -> void:
	# Original strong low-end pull, relaxing near cruising speed.
	var acceleration: float = 60.0 if boosting else 40.0
	if float(kart["speed"]) < target * 0.6:
		acceleration *= 1.8
	kart["speed"] = move_toward(float(kart["speed"]), target, acceleration * delta)


static func steer_velocity(kart: Dictionary, want_velocity: float,
		slip: float, delta: float) -> void:
	kart["latv"] = lerpf(float(kart["latv"]), want_velocity,
		minf(1.0, (1.0 - slip * 0.7) * 30.0 * delta + 0.14))


static func drift_tier(seconds: float) -> int:
	for tier in range(DRIFT_TIERS.size() - 1, 0, -1):
		if seconds >= float(DRIFT_TIERS[tier]):
			return tier
	return 0


static func tick_drift(kart: Dictionary, steer: float, curvature: float,
		delta: float) -> Dictionary:
	var event := {"entered": false, "tier_up": false, "release": false}
	var bend := absf(curvature) > 0.006
	var into_bend := bend and absf(steer) >= 0.6 and steer * curvature < 0.0
	kart["drift_arm"] = float(kart.get("drift_arm", 0.0)) + delta if into_bend else 0.0
	if not bool(kart.get("drift", false)) and float(kart["drift_arm"]) >= 0.25:
		kart["drift"] = true
		kart["drift_t"] = 0.0
		kart["drift_dir"] = signf(steer)
		kart["hop"] = 0.22
		event["entered"] = true
	if bool(kart.get("drift", false)):
		var keep := bend and absf(steer) >= 0.25 \
			and signf(steer) == float(kart["drift_dir"]) and steer * curvature < 0.0
		if keep:
			kart["drift_t"] = float(kart["drift_t"]) + delta
			var tier := drift_tier(float(kart["drift_t"]))
			if tier > int(kart.get("drift_tier_seen", 0)):
				kart["drift_tier_seen"] = tier
				event["tier_up"] = true
		else:
			event["release"] = true
	return event


static func release_drift(kart: Dictionary) -> int:
	var tier := drift_tier(float(kart.get("drift_t", 0.0)))
	cancel_drift(kart)
	if tier > 0:
		kart["boost_t"] = maxf(float(kart["boost_t"]), float(DRIFT_BOOST[tier]))
		kart["squash"] = 0.3
	return tier


static func cancel_drift(kart: Dictionary) -> void:
	kart["drift"] = false
	kart["drift_arm"] = 0.0
	kart["drift_t"] = 0.0
	kart["drift_tier_seen"] = 0


static func steering_target(kart: Dictionary, vehicle: Dictionary, steer: float,
		rail: float, touch_live: bool) -> float:
	var rate := float(vehicle["steer"])
	var velocity := steer * rate
	if bool(kart.get("drift", false)):
		var carve := float(kart["drift_dir"]) * rail * 0.6
		velocity = clampf((carve - float(kart["lat"])) * 3.0, -rate * 1.4, rate * 1.4)
	if touch_live:
		var room := rail - absf(float(kart["lat"]))
		var toward_wall := float(kart["lat"]) * steer > 0.3
		if room < 3.5 and not toward_wall:
			var aid := clampf((3.5 - room) / 3.5, 0.0, 1.0) * 0.7
			velocity = lerpf(velocity, -signf(float(kart["lat"])) * rate * 0.6, aid)
	if float(kart.get("air_t", 0.0)) > 0.0:
		velocity *= 0.5
	return velocity


static func apply_lateral(kart: Dictionary, vehicle: Dictionary,
		new_lateral: float, wall: float) -> bool:
	var bounced := absf(new_lateral) > wall
	if bounced:
		new_lateral = clampf(new_lateral, -wall, wall) * 0.8
		kart["latv"] = -float(kart["latv"]) * 0.85
		kart["speed"] = float(kart["speed"]) * float(vehicle["wall"])
		kart["squash"] = 0.3
		kart["hop"] = 0.22
	kart["lat"] = new_lateral
	return bounced
