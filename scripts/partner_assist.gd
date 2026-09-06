class_name PartnerAssist
extends RefCounted
# Combat wing 2026-08 (owner 2026-08-01: partner powers "should have
# cool-down and be a super move, depending on which partner you have").
# You never fight alone: Daddy Mermaid in the castle, the following stuffie
# everywhere else. The former portrait control, readiness ring and prompt are
# retired. The optional ability state remains dormant for a future in-world
# interaction; no overlay asks the child to find a missing control.
#
# Agency: the ability acts ONLY on explicit activation — a zero-input run can never fire a
# super (probe_partner proves it). Supers may defeat FODDER (the child
# triggered them) but never bosses, and they never touch the pop-chain:
# note_hit is never called from here — the combo is her verbs alone.
# The super EFFECT belongs to the hosting encounter via on_super(kind), so
# enemy-shape knowledge stays out of this satellite.

const COOLDOWNS := {"daddy": 18.0, "stuffie": 12.0}
const POP_SHAVE := 1.0             # seconds each of her own pops shaves off
const STAMPEDE_POPS := 4           # stuffie super: nearest fodder popped
const STUN_T := 3.0                # dizzy time for everything else
const BIG_TAPS := 3                # post-stampede empowered taps

var m: ReefMain
var kind := ""                     # "daddy" | "stuffie"
var cool := 0.0                    # seconds until READY (0 = ready)
var uses := 0                      # rotates Daddy's three recorded lines
var announced := false
var elapsed := 0.0
var on_super: Callable = Callable()
var attached := false

func _init(main: ReefMain) -> void:
	m = main

func attach(partner_kind: String, super_cb: Callable) -> void:
	if attached:
		return
	attached = true
	kind = partner_kind
	on_super = super_cb
	cool = 0.0
	announced = false
	# Partner presentation remains in-world. A future diegetic interaction may
	# expose this optional super without adding another screen control.

func detach() -> void:
	attached = false

func ready() -> bool:
	return attached and cool <= 0.0

func _blocked() -> bool:
	if m.castle_room_menu_open:
		return true
	# Daddy's SPLASH only herds the MAIN HALL's dust bunnies — in any other
	# castle room it was a silent no-op that still spent the whole 18s
	# cooldown. The dormant ability stays unavailable outside the hall.
	if kind == "daddy" and String(m.castle_room_id) != "main_hall":
		return true
	return false

func tick(delta: float) -> void:
	if not attached:
		return
	elapsed += delta
	if cool > 0.0:
		cool = maxf(0.0, cool - delta)
	else:
		announced = true

# Her own pops hurry the partner back — cause and effect she can feel.
func note_child_pop() -> void:
	if cool > 0.0:
		cool = maxf(0.0, cool - POP_SHAVE)

func activate() -> void:
	if not attached or cool > 0.0 or _blocked():
		return
	cool = float(COOLDOWNS.get(kind, 12.0))
	announced = false
	Juice.haptic(40)
	m._audio_ref().pop(4)
	m._audio_ref()._fanfare()
	if kind == "daddy":
		# his three real recorded lines take turns (never generated audio)
		uses += 1
		m._say("daddy" + str((uses - 1) % 3 + 1), "", 0.0)
	else:
		m._say(_stuffie_speaker(), "talk", 0.0)
	if on_super.is_valid():
		on_super.call(kind)

func _chirp_ready() -> void:
	m._say("daddy" if kind == "daddy" else _stuffie_speaker(),
		"assist_ready" if kind == "daddy" else "talk", 3.0)

func _stuffie_speaker() -> String:
	match String(m.companion_id):
		"eagle":
			return "sparkle"
		"mewsha":
			return "mewsha"
		"lamma":
			return "evie"
	return "roshan"
