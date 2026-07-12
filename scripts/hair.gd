extends Node
class_name HairSim
# ---------------------------------------------------------------------------
# SCAFFOLD (2026-06-25) — light spring physics for Roshan's rainbow hair.
#
# Drives 10-15+ independent hair-strand bone chains with a per-segment spring so
# each rainbow streak sways and trails on its own as she swims/turns. Pairs with
# the rainbow hair shader (assets/characters/hair_rainbow.gdshader), which colours
# each streak by strand index (stored in vertex-colour R) and cycles hue via TIME
# — so colour is the shader's job, motion is this script's.
#
# Strand bones follow the contract from tools/build_roshan_base.py:
#   hair_<SS>_<J>   SS = strand 00..N-1,  J = segment 0..segs-1   (chain off 'head')
#
# DESIGN
#   * Independent: each strand gets its own phase + slight stiffness jitter, so no
#     two streaks move alike. The spring also lags behind the player's velocity, so
#     the whole mane trails when she accelerates.
#   * Built on the same primitive as player.gd's procedural swim
#     (Skeleton3D.set_bone_pose_rotation relative to the rest pose) — no engine
#     node dependency. (Godot's SpringBoneSimulator3D is the built-in alternative;
#     this custom solver is used so behaviour is deterministic and tunable here.)
#   * Guarded: if no hair_* bones exist (e.g. the current 5-bone model), setup()
#     finds nothing and the node is a no-op. Safe to add before the re-rig lands.
#
# NOT yet wired in. To enable (after the strand-rigged model exists):
#     var hs := HairSim.new(); player.add_child(hs); hs.setup(player)
#   and drop the per-strand hair1/hair2/hair3 lines from player.gd's swim.
# ---------------------------------------------------------------------------

const STIFFNESS := 42.0          # spring constant (toward rest)
const DAMPING := 7.0             # velocity damping
const TRAIL := 0.16              # how strongly hair lags the player's motion
const IDLE_SWAY := 0.06          # ambient float amplitude (radians)
const MAX_ANGLE := 0.6           # clamp so streaks never fold through the head

var _player: Node3D = null
var _skel: Skeleton3D = null
# per-segment state, parallel arrays indexed by entry
var _bone: PackedInt32Array = []
var _rest: Array[Quaternion] = []
var _ang := PackedVector2Array()     # current sway (x = pitch, y = yaw), radians
var _vel := PackedVector2Array()     # angular velocity
var _phase: PackedFloat32Array = []  # per-strand phase (independence)
var _stiff: PackedFloat32Array = []  # per-segment stiffness (jittered)
var _depth: PackedFloat32Array = []  # 0..1 along the strand (tips move more)
var _last_pos := Vector3.ZERO
var _t := 0.0

func setup(player: Node3D) -> bool:
	_player = player
	_skel = _find_skel(player)
	if _skel == null:
		return false
	# discover strand chains: bones named hair_SS_J
	var strands := {}   # SS -> [ {idx, j} ... ]
	for bi in range(_skel.get_bone_count()):
		var nm := _skel.get_bone_name(bi)
		if not nm.begins_with("hair_"):
			continue
		var parts := nm.substr(5).split("_")
		if parts.size() != 2:
			continue
		var ss := int(parts[0]); var j := int(parts[1])
		if not strands.has(ss):
			strands[ss] = []
		strands[ss].append({"idx": bi, "j": j})
	if strands.is_empty():
		return false
	var keys := strands.keys(); keys.sort()
	for ss in keys:
		var segs: Array = strands[ss]
		segs.sort_custom(func(a, b): return a["j"] < b["j"])
		var n := segs.size()
		for k in range(n):
			var bi: int = segs[k]["idx"]
			_bone.append(bi)
			_rest.append(_skel.get_bone_pose_rotation(bi))
			_ang.append(Vector2.ZERO)
			_vel.append(Vector2.ZERO)
			_phase.append(float(ss) / float(keys.size()) * TAU)
			# tips (higher j) are floppier; small per-strand jitter for independence
			_depth.append(float(k + 1) / float(n))
			_stiff.append(STIFFNESS * (0.8 + 0.4 * _hash01(ss * 7 + k)))
	_last_pos = _player.global_position
	return _bone.size() > 0

func _process(delta: float) -> void:
	if _skel == null or _bone.is_empty() or delta <= 0.0:
		return
	_t += delta
	# player motion this frame, in the player's local frame -> drives the trail
	var world_v := (_player.global_position - _last_pos) / delta
	_last_pos = _player.global_position
	var local_v: Vector3 = _player.global_transform.basis.inverse() * world_v
	var drive := Vector2(-local_v.z, -local_v.x) * TRAIL   # trail opposite motion

	for e in range(_bone.size()):
		var depth := _depth[e]
		var phase := _phase[e]
		# target = motion trail (scaled by depth) + ambient float (per-strand phase)
		var target := drive * depth
		target.x += sin(_t * 1.7 + phase) * IDLE_SWAY * depth
		target.y += cos(_t * 1.3 + phase * 1.3) * IDLE_SWAY * depth
		# damped spring toward target
		var a := _ang[e]
		var acc := (target - a) * _stiff[e] - _vel[e] * DAMPING
		_vel[e] += acc * delta
		a += _vel[e] * delta
		a.x = clampf(a.x, -MAX_ANGLE, MAX_ANGLE)
		a.y = clampf(a.y, -MAX_ANGLE, MAX_ANGLE)
		_ang[e] = a
		# apply relative to rest, about MODEL-space axes (the v3 strand bones
		# carry Blender rest orientations; raw local axes would sway each
		# strand in a different arbitrary direction)
		var rq: Quaternion = _rest[e]
		var ax_pitch: Vector3 = (rq.inverse() * Vector3.RIGHT).normalized()
		var ax_yaw: Vector3 = (rq.inverse() * Vector3.BACK).normalized()
		var q := rq * Quaternion(ax_pitch, a.x) * Quaternion(ax_yaw, a.y)
		_skel.set_bone_pose_rotation(_bone[e], q)

func _find_skel(n: Node) -> Skeleton3D:
	if n == null:
		return null
	if "skel" in n and n.skel is Skeleton3D:
		return n.skel
	return _scan_skel(n)

func _scan_skel(n: Node) -> Skeleton3D:
	if n is Skeleton3D:
		return n
	for c in n.get_children():
		var r := _scan_skel(c)
		if r != null:
			return r
	return null

func _hash01(i: int) -> float:
	var x := sin(float(i) * 127.1) * 43758.5453
	return x - floor(x)
