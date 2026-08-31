class_name PartnerAssist
extends RefCounted
# Combat wing 2026-08 (owner 2026-08-01: partner powers "should have
# cool-down and be a super move, depending on which partner you have").
# You never fight alone: Daddy Mermaid in the castle, the following stuffie
# everywhere else. A portrait bubble sits mid-left; READY = glow ring +
# idle wiggle + one chirp; one tap fires that partner's SUPER; then the
# partner rests behind a radial refill ring. The child's own pops shave the
# rest, so her effort still matters.
#
# Agency: the bubble acts ONLY on a tap — a zero-input run can never fire a
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
const READY_PULSE := 0.045         # the shared idle-pulse idiom

var m: ReefMain
var kind := ""                     # "daddy" | "stuffie"
var cool := 0.0                    # seconds until READY (0 = ready)
var uses := 0                      # rotates Daddy's three recorded lines
var announced := false
var elapsed := 0.0
var on_super: Callable = Callable()
var layer: CanvasLayer = null
var bubble: Button = null
var ring: PartnerRing = null

# The no-numerals cooldown ring: a gold full circle when ready, a soft blue
# arc refilling clockwise while the partner rests.
class PartnerRing:
	extends Control
	var progress := 1.0
	func _draw() -> void:
		var center: Vector2 = size * 0.5
		var radius: float = size.x * 0.5 - 5.0
		if progress >= 1.0:
			draw_arc(center, radius, 0.0, TAU, 48, Color(1.0, 0.95, 0.55, 0.9), 7.0, true)
		elif progress > 0.01:
			draw_arc(center, radius, -PI * 0.5, -PI * 0.5 + TAU * progress, 48, Color(0.75, 0.85, 1.0, 0.8), 7.0, true)

func _init(main: ReefMain) -> void:
	m = main

func attach(partner_kind: String, super_cb: Callable) -> void:
	if bubble != null:
		return
	kind = partner_kind
	on_super = super_cb
	cool = 0.0
	announced = false
	layer = CanvasLayer.new()
	layer.layer = 15
	m.add_child(layer)
	bubble = Button.new()
	bubble.flat = true
	bubble.focus_mode = Control.FOCUS_NONE
	var vs: Vector2 = m.get_viewport().get_visible_rect().size
	bubble.position = Vector2(26.0, vs.y * 0.40 - 88.0)
	bubble.size = Vector2(176.0, 176.0)
	bubble.pivot_offset = Vector2(88.0, 88.0)
	bubble.pressed.connect(on_bubble_tap)
	layer.add_child(bubble)
	var tex_path: String = _portrait_path()
	if tex_path != "" and ResourceLoader.exists(tex_path):
		var portrait := TextureRect.new()
		portrait.texture = load(tex_path)
		portrait.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		portrait.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		portrait.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
		portrait.mouse_filter = Control.MOUSE_FILTER_IGNORE
		bubble.add_child(portrait)
	else:
		StorybookUI.style_icon_button(bubble, "🧸" if kind == "stuffie" else "💙",
			"secondary", Vector2(176.0, 176.0), "Partner power!")
	ring = PartnerRing.new()
	ring.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	ring.mouse_filter = Control.MOUSE_FILTER_IGNORE
	bubble.add_child(ring)

func detach() -> void:
	if layer != null and is_instance_valid(layer):
		layer.queue_free()
	layer = null
	bubble = null
	ring = null

func ready() -> bool:
	return bubble != null and cool <= 0.0

# The bubble rides CanvasLayer 15, ABOVE full-screen modals on the base
# canvas — while the elevator book (or any room menu) is open the bubble
# would still catch taps and waste the super into a covered screen. It
# steps aside whenever a castle menu is up (alpha audit 2026-08-05).
func _blocked() -> bool:
	if m.castle_room_menu_open:
		return true
	# Daddy's SPLASH only herds the MAIN HALL's dust bunnies — in any other
	# castle room it was a silent no-op that still spent the whole 18s
	# cooldown. The bubble steps aside outside the hall instead of tempting
	# a wasted tap (alpha audit 2026-08-05).
	if kind == "daddy" and String(m.castle_room_id) != "main_hall":
		return true
	return false

func tick(delta: float) -> void:
	if bubble == null:
		return
	bubble.visible = not _blocked()
	elapsed += delta
	if cool > 0.0:
		cool = maxf(0.0, cool - delta)
		bubble.modulate = Color(0.62, 0.68, 0.80)   # resting: dimmed, no wiggle
		bubble.scale = Vector2.ONE
		ring.progress = 1.0 - cool / float(COOLDOWNS.get(kind, 12.0))
	else:
		bubble.modulate = Color(1, 1, 1)
		bubble.scale = Vector2.ONE * (1.0 + sin(elapsed * 2.2) * READY_PULSE)
		ring.progress = 1.0
		if not announced:
			announced = true
			_chirp_ready()
	ring.queue_redraw()

# Her own pops hurry the partner back — cause and effect she can feel.
func note_child_pop() -> void:
	if cool > 0.0:
		cool = maxf(0.0, cool - POP_SHAVE)

func on_bubble_tap() -> void:
	if bubble == null or cool > 0.0 or _blocked():
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

func _portrait_path() -> String:
	if kind == "daddy":
		return String(ReefMain.SPEAKER_PORTRAIT.get("daddy", ""))
	match String(m.companion_id):
		"eagle":
			return "res://assets/book/baby_eagle.png"
		"lamma":
			return "res://assets/sprites/stuffie_studio/lamma.png"
	return ""   # unknown stuffie: cozy 🧸 icon fallback
