extends RefCounted
## One authored in-plane phrase for every candidate. No new view is implied.
const PERIOD: float = 1.8
const DURATION: float = 7.2


func smooth(value: float) -> float:
	var v: float = clampf(value, 0.0, 1.0)
	return v * v * v * (v * (v * 6.0 - 15.0) + 10.0)


func pulse(t: float, offset: float = 0.0) -> float:
	var p: float = fposmod(t, PERIOD) - offset
	if p < 0.08:
		return 0.0
	if p < 0.40:
		return smooth((p - 0.08) / 0.32)
	if p < 0.48:
		return 1.0
	return 1.0 - smooth((p - 0.48) / 0.90)


func pose(t: float) -> Dictionary:
	var effort: float = pulse(t)
	var answer: float = pulse(t, 0.08)
	var distal: float = pulse(t, 0.16)
	return {
		"Torso": -2.0 * effort, "Head": 0.0,
		"LeftUpper": 3.5 * effort, "LeftFore": 6.0 * answer,
		"LeftHand": -1.0 * answer, "RightUpper": -2.5 * effort,
		"RightFore": -4.0 * answer, "RightHand": 0.5 * answer,
		"TailA": 3.3 * effort, "TailB": 5.0 * answer,
		"TailC": -4.2 * distal, "TailD": -3.0 * distal,
		"Fin": 2.4 * pulse(t, 0.20)
	}


func apply(scene: Node2D, t: float, clip: String) -> void:
	var bones: Dictionary = scene.get("bones")
	var local_time: float = t
	var envelope: float = 1.0
	if clip == "travel":
		local_time = maxf(t - 0.30, 0.0)
		envelope = smooth(t / 0.30) * (1.0 - smooth((t - 5.65) / 0.45))
	var angles: Dictionary = pose(local_time)
	for bone_name: String in bones:
		var bone: Bone2D = bones[bone_name]
		bone.transform = bone.rest
		bone.rotation += deg_to_rad(float(angles.get(bone_name, 0.0)) * envelope)
	var half: Sprite2D = scene.get("eye_half")
	var closed: Sprite2D = scene.get("eye_closed")
	half.visible = false
	closed.visible = false
	# A discrete authored blink during recovery, never over the propulsion peak.
	if clip == "travel" and t >= 3.58 and t < 3.78:
		closed.visible = t >= 3.63 and t < 3.71
		half.visible = not closed.visible
	var actor: Node2D = scene.get("actor")
	actor.position = Vector2.ZERO
	actor.scale = Vector2.ONE
	if clip == "travel":
		var progress: float = smooth((t - 0.15) / 5.65)
		actor.position = Vector2(-95.0 + 190.0 * progress, -3.0 * envelope * pulse(local_time))


func phase(t: float, clip: String) -> String:
	if clip == "travel":
		if t < 0.3:
			return "attention / immediate departure"
		if t > 6.1:
			return "quiet supported arrival"
		if t > 5.65:
			return "brake and settle"
	var p: float = fposmod(t if clip == "loop" else maxf(t - 0.3, 0.0), PERIOD)
	if p < 0.4:
		return "gather / push"
	if p < 0.7:
		return "fin follows propulsion"
	return "glide / recovery"
