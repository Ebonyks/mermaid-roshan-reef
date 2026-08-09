extends Node
class_name HairSim
# ---------------------------------------------------------------------------
# Light, deterministic underwater spring motion for Roshan's hair strand rig.
#
# Strand bones follow the contract from tools/fit_roshan_rig.py:
#   hair_<SS>_<J>   SS = strand 00..N-1, J = segment 0..segs-1
#
# This stays deliberately smaller than SpringBoneSimulator3D: 24 Vector2
# springs, no collision bodies, and a bounded substep loop. Translation makes
# the locks trail through the water, turning fans them sideways, and a slow
# current keeps the free tips alive while Roshan is hovering. Roots remain
# close to the scalp; damping and travel loosen gradually toward each tip.
# ---------------------------------------------------------------------------

const ROOT_STIFFNESS := 34.0
const TIP_STIFFNESS := 12.0
const ROOT_DAMPING := 9.0
const TIP_DAMPING := 5.2
const TRAIL := 0.012
const TURN_TRAIL := 0.035
const IDLE_SWAY := 0.025
const CURRENT_SWAY := 0.035
const ROOT_MAX_ANGLE := 0.08
const TIP_MAX_ANGLE := 0.22
const MAX_DRIVE := 0.18
const MAX_WATER_SPEED := 25.0
const MAX_TURN_SPEED := 4.0
const VELOCITY_RESPONSE := 3.2
const TURN_RESPONSE := 4.0
const MAX_STEP := 1.0 / 60.0
const MAX_FRAME_DELTA := 0.1
const TELEPORT_DISTANCE := 4.0

var _player: Node3D = null
var _skel: Skeleton3D = null
# Per-segment state, parallel arrays indexed by entry.
var _bone: PackedInt32Array = []
var _rest: Array[Quaternion] = []
var _global_rest: Array[Quaternion] = []
var _ang: PackedVector2Array = []
var _vel: PackedVector2Array = []
var _phase: PackedFloat32Array = []
var _stiff: PackedFloat32Array = []
var _damp: PackedFloat32Array = []
var _depth: PackedFloat32Array = []
var _limit: PackedFloat32Array = []
var _last_pos := Vector3.ZERO
var _last_basis := Basis.IDENTITY
var _smoothed_local_v := Vector3.ZERO
var _smoothed_turn := 0.0
var _t := 0.0

func setup(player: Node3D) -> bool:
	_player = player
	_skel = _find_skel(player)
	if _skel == null:
		return false
	_bone.clear()
	_rest.clear()
	_global_rest.clear()
	_ang.clear()
	_vel.clear()
	_phase.clear()
	_stiff.clear()
	_damp.clear()
	_depth.clear()
	_limit.clear()
	# Discover and sort strand chains: bones named hair_SS_J.
	var strands := {} # SS -> [ {idx, j} ... ]
	for bi in range(_skel.get_bone_count()):
		var nm: String = _skel.get_bone_name(bi)
		if not nm.begins_with("hair_"):
			continue
		var parts: PackedStringArray = nm.substr(5).split("_")
		if parts.size() != 2:
			continue
		var ss := int(parts[0])
		var j := int(parts[1])
		if not strands.has(ss):
			strands[ss] = []
		strands[ss].append({"idx": bi, "j": j})
	if strands.is_empty():
		return false
	var keys: Array = strands.keys()
	keys.sort()
	for ss in keys:
		var segs: Array = strands[ss]
		segs.sort_custom(func(a, b): return a["j"] < b["j"])
		var n: int = segs.size()
		for k in range(n):
			var bi: int = segs[k]["idx"]
			var depth: float = float(k) / float(maxi(n - 1, 1))
			_bone.append(bi)
			_rest.append(_skel.get_bone_pose_rotation(bi))
			_global_rest.append(_skel.get_bone_global_rest(bi).basis.get_rotation_quaternion())
			_ang.append(Vector2.ZERO)
			_vel.append(Vector2.ZERO)
			_phase.append(float(ss) / float(keys.size()) * TAU)
			_depth.append(depth)
			# Roots stay deliberate; tips are softer and travel farther. A small
			# deterministic variation stops the eight locks moving as one sheet.
			var jitter: float = lerpf(0.90, 1.10, _hash01(int(ss) * 7 + k))
			_stiff.append(lerpf(ROOT_STIFFNESS, TIP_STIFFNESS, depth) * jitter)
			_damp.append(lerpf(ROOT_DAMPING, TIP_DAMPING, depth))
			_limit.append(lerpf(ROOT_MAX_ANGLE, TIP_MAX_ANGLE, depth))
	_last_pos = _player.global_position
	_last_basis = _player.global_transform.basis.orthonormalized()
	_smoothed_local_v = Vector3.ZERO
	_smoothed_turn = 0.0
	_t = 0.0
	return not _bone.is_empty()

func _process(delta: float) -> void:
	if _skel == null or _bone.is_empty() or delta <= 0.0:
		return
	var frame_delta: float = minf(delta, MAX_FRAME_DELTA)
	_t += frame_delta
	var current_position: Vector3 = _player.global_position
	var displacement: Vector3 = current_position - _last_pos
	_last_pos = current_position
	var current_basis: Basis = _player.global_transform.basis.orthonormalized()
	var local_v := Vector3.ZERO
	if displacement.length() < TELEPORT_DISTANCE:
		local_v = current_basis.inverse() * (displacement / maxf(delta, 0.0001))
		if local_v.length() > MAX_WATER_SPEED:
			local_v = local_v.normalized() * MAX_WATER_SPEED
	var velocity_blend: float = 1.0 - exp(-VELOCITY_RESPONSE * frame_delta)
	_smoothed_local_v = _smoothed_local_v.lerp(local_v, velocity_blend)

	var previous_forward: Vector3 = -_last_basis.z.normalized()
	var current_forward: Vector3 = -current_basis.z.normalized()
	var turn_angle: float = atan2(
		previous_forward.cross(current_forward).dot(Vector3.UP),
		previous_forward.dot(current_forward),
	)
	_last_basis = current_basis
	var turn_speed: float = clampf(turn_angle / maxf(delta, 0.0001), -MAX_TURN_SPEED, MAX_TURN_SPEED)
	var turn_blend: float = 1.0 - exp(-TURN_RESPONSE * frame_delta)
	_smoothed_turn = lerpf(_smoothed_turn, turn_speed, turn_blend)

	var drive := Vector2(-_smoothed_local_v.z, -_smoothed_local_v.x) * TRAIL
	drive.y -= _smoothed_turn * TURN_TRAIL
	if drive.length() > MAX_DRIVE:
		drive = drive.normalized() * MAX_DRIVE
	var steps: int = clampi(ceili(frame_delta / MAX_STEP), 1, 6)
	var step: float = frame_delta / float(steps)
	for _substep in range(steps):
		_integrate(step, drive)
	_apply_pose()

func _integrate(step: float, drive: Vector2) -> void:
	for entry in range(_bone.size()):
		var depth: float = _depth[entry]
		var response: float = lerpf(0.18, 1.0, pow(depth, 1.45))
		var phase: float = _phase[entry]
		var target: Vector2 = drive * response
		# A slow shared current gives the water direction; independent phase and
		# frequency supply the smaller lock-to-lock float around it.
		target.x += sin(_t * 0.52 + 0.4) * CURRENT_SWAY * response
		target.y += cos(_t * 0.43 - 0.2) * CURRENT_SWAY * response
		target.x += sin(_t * 1.10 + phase) * IDLE_SWAY * response
		target.y += cos(_t * 0.86 + phase * 1.3) * IDLE_SWAY * response
		var angle: Vector2 = _ang[entry]
		var velocity: Vector2 = _vel[entry]
		var acceleration: Vector2 = (target - angle) * _stiff[entry] - velocity * _damp[entry]
		velocity += acceleration * step
		angle += velocity * step
		var limit: float = _limit[entry]
		angle.x = clampf(angle.x, -limit, limit)
		angle.y = clampf(angle.y, -limit, limit)
		_ang[entry] = angle
		_vel[entry] = velocity

func _apply_pose() -> void:
	for entry in range(_bone.size()):
		var angle: Vector2 = _ang[entry]
		var rest_rotation: Quaternion = _rest[entry]
		var global_rest_rotation: Quaternion = _global_rest[entry]
		# Convert MODEL-space water axes through the full accumulated rest basis.
		# Using only the local rest quaternion made child chains disagree about
		# which way was "through the water".
		var pitch_axis: Vector3 = (global_rest_rotation.inverse() * Vector3.RIGHT).normalized()
		var yaw_axis: Vector3 = (global_rest_rotation.inverse() * Vector3.BACK).normalized()
		var pose: Quaternion = rest_rotation * Quaternion(pitch_axis, angle.x) * Quaternion(yaw_axis, angle.y)
		_skel.set_bone_pose_rotation(_bone[entry], pose)

func _find_skel(node: Node) -> Skeleton3D:
	if node == null:
		return null
	if "skel" in node and node.skel is Skeleton3D:
		return node.skel
	return _scan_skel(node)

func _scan_skel(node: Node) -> Skeleton3D:
	if node is Skeleton3D:
		return node
	for child in node.get_children():
		var result: Skeleton3D = _scan_skel(child)
		if result != null:
			return result
	return null

func _hash01(value: int) -> float:
	var hashed: float = sin(float(value) * 127.1) * 43758.5453
	return hashed - floor(hashed)
