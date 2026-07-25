class_name ReactiveProps
extends RefCounted
# S1 of SATCHEL_WORKORDER_2026-07-25: the "casual animation" layer. Every small
# reef prop drifts on its own and answers when Roshan bumps into it — a squash,
# a chime, a puff of sparkle. Nothing here awards anything, gates anything, or
# writes to the save; it is pure world-feel, so probe_passive stays silent.
#
# THE ANIMATION IS LOCAL TO THE PROP'S INNER MESH. _gen2_prop returns a `wrap`
# Node3D holding the fitted `inst`; we only ever touch `inst`'s local transform.
# That is what lets CarrySystem (and, in S2, the Satchel) move the SAME props by
# their wrap without the two systems fighting over one transform.
#
# Perf (Mali-G52): the full registry is only scanned every NEAR_REBUILD seconds
# to rebuild a near list; per-frame work is bounded to props inside the same
# cull radius the creature AnimationPlayers already use (95 m Speedy /
# 160 m Sparkly, DESIGN_3_0.md). Flora sway proper stays in coral_flow.gdshader.

# Corals, sponges and anemones sway from the base like they are rooted.
const SWAY := ["coral", "coral1", "coral2", "coral3", "coral4", "coral5",
	"coral6", "sponge_barrel", "sponge_tubes", "anemone_story"]
# Loose seafloor things bob and turn like they are resting on sand.
const BOB := ["starfish", "spiralshell", "fanshell", "smallfanshell",
	"sanddollar", "urchin_story"]

const NEAR_REBUILD := 0.4      # seconds between full-registry scans
const REACT_TIME := 0.8        # squash-and-stretch decay, matches the singing shell
const REACT_COOL := 1.6        # per-prop, so swimming laps is not a machine gun
const CHIME_GAP := 0.14        # global floor between reaction chimes
const BUMP_PAD := 2.6          # reach past the prop's own footprint

var m: ReefMain
var _t := 0.0
var _near: Array = []          # entries borrowed from m.reactive_props
var _near_t := 0.0
var _chime_t := 0.0

func _init(main: ReefMain) -> void:
	m = main

func register(wrap: Node3D, inst: Node3D, pname: String, target: float) -> void:
	# called from _gen2_prop for whitelisted props only; unknown names are
	# silently ignored so structural flora, rocks, trees and creatures (which
	# own their own animation) never enter the registry.
	var kind := ""
	if pname in SWAY:
		kind = "sway"
	elif pname in BOB:
		kind = "bob"
	else:
		return
	m.reactive_props.append({
		"wrap": wrap, "inst": inst, "kind": kind,
		"base": inst.position, "scale": inst.scale,
		"phase": randf() * TAU, "r": target * 0.5 + BUMP_PAD,
		"cool": 0.0, "react": 0.0,
	})

func release(wrap: Node3D) -> void:
	# S2 hook: a prop that has been picked up stops being world furniture. Its
	# inner mesh is restored to the authored rest pose on the way out so it
	# never freezes mid-squash inside a satchel slot.
	for i in range(m.reactive_props.size() - 1, -1, -1):
		var it: Dictionary = m.reactive_props[i]
		if it["wrap"] != wrap:
			continue
		var inst: Node3D = it["inst"]
		if is_instance_valid(inst):
			inst.position = it["base"]
			inst.scale = it["scale"]
			inst.rotation = Vector3.ZERO
		m.reactive_props.remove_at(i)
		_near_t = 0.0   # force a rebuild; the near list may hold this entry

func tick(delta: float, ppos: Vector3) -> void:
	_t += delta
	_chime_t = maxf(0.0, _chime_t - delta)
	_near_t -= delta
	if _near_t <= 0.0:
		_near_t = NEAR_REBUILD
		_rebuild_near(ppos)
	for it in _near:
		_animate(it as Dictionary, delta, ppos)

func _rebuild_near(ppos: Vector3) -> void:
	# one pass: drop registry entries whose node died with its world, and
	# collect the ones close enough to be worth animating this interval.
	var lim: float = 95.0 if m.quality == "speedy" else 160.0
	_near.clear()
	for i in range(m.reactive_props.size() - 1, -1, -1):
		var it: Dictionary = m.reactive_props[i]
		var wrap: Node3D = it["wrap"]
		if not is_instance_valid(wrap) or not is_instance_valid(it["inst"]):
			m.reactive_props.remove_at(i)
			continue
		if not wrap.is_visible_in_tree():
			continue   # another world is up; keep the entry, skip the work
		if wrap.position.distance_to(ppos) < lim:
			_near.append(it)

func _animate(it: Dictionary, delta: float, ppos: Vector3) -> void:
	var wrap: Node3D = it["wrap"]
	var inst: Node3D = it["inst"]
	if not is_instance_valid(wrap) or not is_instance_valid(inst):
		return
	it["cool"] = maxf(0.0, float(it["cool"]) - delta)
	var ph: float = float(it["phase"])
	var base: Vector3 = it["base"]
	var bscale: Vector3 = it["scale"]

	# ---- bump: she swam into it ----
	if float(it["cool"]) <= 0.0 and wrap.position.distance_to(ppos) < float(it["r"]):
		it["cool"] = REACT_COOL
		it["react"] = REACT_TIME
		_ring(wrap.position, String(it["kind"]))

	# ---- idle drift ----
	match String(it["kind"]):
		"sway":
			inst.rotation.z = sin(_t * 0.6 + ph) * 0.05
			inst.rotation.x = cos(_t * 0.47 + ph) * 0.04
			inst.position = base
		"bob":
			inst.position = base + Vector3(0.0, sin(_t * 1.3 + ph) * 0.09, 0.0)
			inst.rotation.y = sin(_t * 0.31 + ph) * 0.18

	# ---- reaction: the singing shell's squash-and-stretch, shared ----
	var rt: float = float(it["react"])
	if rt > 0.0:
		rt = maxf(0.0, rt - delta)
		it["react"] = rt
		var amp: float = rt / REACT_TIME
		var pulse: float = sin((REACT_TIME - rt) * 18.0) * 0.09 * amp
		inst.scale = bscale * (1.0 + pulse)
		if String(it["kind"]) == "sway":
			inst.rotation.z += pulse * 2.2
		else:
			inst.position += Vector3(0.0, maxf(0.0, pulse) * 1.6, 0.0)
	elif inst.scale != bscale:
		inst.scale = bscale

func _ring(pos: Vector3, kind: String) -> void:
	# Audio and particles are rate-limited; the squash never is. A tap that
	# does nothing would break the one promise this whole pass makes, so the
	# visual reaction always fires even when the sound is being throttled.
	if _chime_t > 0.0:
		return
	_chime_t = CHIME_GAP
	if m.chime != null:
		# pitch only — volume_db is shared with the pearl and carry chimes and
		# must not be re-tuned behind their backs.
		var step: int = ReefMain.PENT[randi() % ReefMain.PENT.size()]
		m.chime.pitch_scale = (1.35 if kind == "bob" else 0.95) * pow(2.0, float(step) / 12.0)
		m.chime.play()
