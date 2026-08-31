class_name DodgeTutorialGuide
extends CanvasLayer
# Picture-first companion to CombatTutorial.DemoFinger. It uses the same
# approved ghost hand, warm halo, 2.4-second loop and quiet re-demonstration
# language, but acts out a left/right swipe around a landing marker.

const GHOST_HAND_PATH := "res://assets/castle/training/ghost_hand.png"
const CYCLE_T := 2.4

var root: Control = null
var hand: TextureRect = null
var left_arrow: Label = null
var right_arrow: Label = null
var landing_ring: Control = null
var t := 0.0

class LandingRing:
	extends Control
	var pulse := 0.0
	func _process(delta: float) -> void:
		pulse += delta
		queue_redraw()
	func _draw() -> void:
		var r: float = 58.0 + sin(pulse * 5.0) * 7.0
		draw_circle(Vector2.ZERO, r, Color(1.0, 0.72, 0.38, 0.16))
		draw_arc(Vector2.ZERO, r, 0.0, TAU, 48,
			Color(1.0, 0.90, 0.48, 0.88), 7.0, true)
		draw_circle(Vector2.ZERO, 13.0, Color(1.0, 0.96, 0.72, 0.92))

func _ready() -> void:
	layer = 13
	root = Control.new()
	root.name = "DodgeTutorialGuideRoot"
	root.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	root.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(root)
	landing_ring = LandingRing.new()
	landing_ring.name = "LandingMarker"
	landing_ring.position = Vector2(640.0, 430.0)
	landing_ring.mouse_filter = Control.MOUSE_FILTER_IGNORE
	root.add_child(landing_ring)
	left_arrow = _arrow("←", Vector2(395.0, 380.0))
	right_arrow = _arrow("→", Vector2(805.0, 380.0))
	hand = TextureRect.new()
	hand.name = "SwipeGhostHand"
	hand.texture = load(GHOST_HAND_PATH) as Texture2D
	hand.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	hand.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	hand.custom_minimum_size = Vector2(96.0, 96.0)
	hand.size = Vector2(96.0, 96.0)
	hand.pivot_offset = hand.size * 0.5
	hand.mouse_filter = Control.MOUSE_FILTER_IGNORE
	root.add_child(hand)

func _arrow(glyph: String, pos: Vector2) -> Label:
	var arrow := Label.new()
	arrow.text = glyph
	arrow.position = pos
	arrow.size = Vector2(80.0, 100.0)
	arrow.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	arrow.add_theme_font_size_override("font_size", 82)
	arrow.add_theme_color_override("font_color", Color(1.0, 0.94, 0.55))
	arrow.add_theme_color_override("font_outline_color", Color(0.20, 0.12, 0.34))
	arrow.add_theme_constant_override("outline_size", 12)
	arrow.mouse_filter = Control.MOUSE_FILTER_IGNORE
	root.add_child(arrow)
	return arrow

func _process(delta: float) -> void:
	t += delta
	var cycle: float = fmod(t, CYCLE_T)
	var rightward: bool = int(t / CYCLE_T) % 2 == 0
	var u: float = clampf((cycle - 0.55) / 1.15, 0.0, 1.0)
	var eased: float = 0.5 - 0.5 * cos(u * PI)
	var start_x: float = 640.0
	var end_x: float = 850.0 if rightward else 430.0
	hand.position = Vector2(lerpf(start_x, end_x, eased) - 48.0,
		430.0 - 48.0 + sin(eased * PI) * -18.0)
	var live_alpha: float = 0.95 if cycle >= 0.40 and cycle <= 1.95 else 0.35
	hand.modulate = Color(1.0, 1.0, 1.0, live_alpha)
	left_arrow.modulate.a = 1.0 if not rightward else 0.28
	right_arrow.modulate.a = 1.0 if rightward else 0.28

func restart_demo() -> void:
	t = 0.0
	visible = true
