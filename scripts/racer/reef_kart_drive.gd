extends RefCounted
## Fixed-step PC kart motion. The heading describes the body. The velocity
## vector retains momentum so the tires can grip, slide and regain traction.

const DEFAULTS := {
	"steer_rate": 22.0,
	"turn": 3.0,
	"crawl_grip": 0.24,
	"grip": 18.0,
	"drift_grip": 5.5,
	"coast": 112.0,
	"accel": 350.0,
	"rail_rebound": 0.12,
	"camera": 18.0,
	"charge": 0.68,
}
const BRAKE := 660.0
const REVERSE := 82.0
const DRIFT_MIN_SPEED := 108.0


static func forward(heading: float) -> Vector2:
	return Vector2(sin(heading), -cos(heading))


static func reset(kart: Dictionary) -> void:
	kart["velocity"] = Vector2.ZERO
	kart["wheel"] = 0.0
	cancel_drift(kart)


static func cancel_drift(kart: Dictionary) -> void:
	kart["drift_dir"] = 0.0
	kart["drift_charge"] = 0.0


static func step(kart: Dictionary, controls: Dictionary, terrain: int, top: float,
		tune: Dictionary, delta: float) -> void:
	var heading := float(kart["heading"])
	var velocity: Vector2 = kart["velocity"]
	var speed := velocity.dot(forward(heading))
	var throttle := clampf(float(controls.get("throttle", 0.0)), 0.0, 1.0)
	var brake := bool(controls.get("brake", false))
	var stick := clampf(float(controls.get("steer", 0.0)), -1.0, 1.0)
	var spin := float(kart["spin_t"]) > 0.0
	if spin:
		stick = 0.0
		kart["spin_vis"] = float(kart["spin_vis"]) + delta * 11.0
	else:
		kart["spin_vis"] = 0.0
	var drift := _drift(kart, controls, stick, speed, brake or spin, tune, delta)
	var wheel := move_toward(float(kart["wheel"]), stick, float(tune["steer_rate"]) * delta)
	kart["wheel"] = wheel
	var powered := throttle > 0.0 or float(kart["boost_t"]) > 0.0
	if spin:
		speed = move_toward(speed, 0.0, BRAKE * 0.5 * delta)
	elif brake:
		var target := -REVERSE if not powered and speed <= 8.0 else 0.0
		speed = move_toward(speed, target, BRAKE * delta)
	elif powered:
		var boost := 2.05 if float(kart["boost_t"]) > 0.0 else 1.0
		var traction := 0.62 if terrain == ReefKartTrack.Terrain.APRON else 1.0
		var accel := float(tune["accel"]) * boost * traction * maxf(throttle, 0.5 if boost > 1.0 else 0.0)
		var engine_pull := 1.0 - 0.48 * clampf(speed / maxf(top, 1.0), 0.0, 1.0)
		speed = move_toward(speed, top, (accel * engine_pull if speed < top else 330.0) * delta)
	else:
		speed = move_toward(speed, 0.0, float(tune["coast"]) * delta)
	var turn_grip := smoothstep(2.0, 64.0, absf(speed))
	if absf(speed) > 1.0:
		turn_grip = maxf(turn_grip, float(tune["crawl_grip"]))
	turn_grip *= lerpf(1.07, 0.79, clampf(absf(speed) / 360.0, 0.0, 1.0))
	var yaw := wheel
	if drift != 0.0:
		yaw = drift * (0.63 + wheel * drift * 0.43)
	heading = wrapf(heading + yaw * float(tune["turn"]) * float(kart["turn_rate"])
		* turn_grip * signf(speed) * delta, -PI, PI)
	var ahead := forward(heading)
	var right := Vector2(-ahead.y, ahead.x)
	# Rotation keeps the velocity from the preceding step. The changed tire
	# axes produce side slip even when the driver holds a steady steering angle.
	var slip := velocity.dot(right)
	var grip := float(tune["drift_grip"] if drift != 0.0 else tune["grip"])
	if terrain == ReefKartTrack.Terrain.APRON:
		grip *= 0.76
	if not bool(kart["player"]):
		grip = maxf(24.0, grip)
	slip *= exp(-grip * delta)
	kart["heading"] = heading
	kart["velocity"] = ahead * speed + right * slip
	kart["speed"] = (kart["velocity"] as Vector2).length()
	kart["steer_vis"] = clampf(yaw, -1.0, 1.0)


static func _drift(kart: Dictionary, controls: Dictionary, stick: float, speed: float,
		cancelled: bool, tune: Dictionary, delta: float) -> float:
	if cancelled or speed < DRIFT_MIN_SPEED * 0.72:
		cancel_drift(kart)
		return 0.0
	var drift := float(kart["drift_dir"])
	if not bool(controls.get("drift", false)):
		if drift != 0.0 and float(kart["drift_charge"]) >= float(tune["charge"]):
			kart["boost_t"] = maxf(float(kart["boost_t"]), 0.72)
		cancel_drift(kart)
		return 0.0
	if drift == 0.0 and absf(stick) >= 0.24 and speed >= DRIFT_MIN_SPEED:
		drift = signf(stick)
		kart["drift_dir"] = drift
	if drift != 0.0:
		kart["drift_charge"] = minf(1.0, float(kart["drift_charge"]) + delta * (0.7 + 0.3 * absf(stick)))
	return drift
