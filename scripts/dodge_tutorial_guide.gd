class_name DodgeTutorialGuide
extends CanvasLayer
# Temporary, non-interactive gesture demonstration for Grand Puff's incoming
# hop. It follows CombatTutorial's 2.4 s ghost-hand rhythm and warm halo, but
# never acts as a button, owns input, or completes the lesson.

const GHOST_HAND_PATH := "res://assets/castle/training/ghost_hand.png"
const CYCLE_T := 2.4

var demo: Control = null
var elapsed := 0.0
# A consistent lower focus band, not a claimed landing marker. The live coral
# flash stays physically attached to Grand Puff above it.
var anchor := Vector2(640.0, 560.0)

class SwipeDemo:
	extends Control
	var ghost: Texture2D = null
	var phase := 0.0
	var rightward := true

	func _draw() -> void:
		# Coral lateral ribbons distinguish MOVE from the boss's radial gold
		# vulnerability strobe. The warm halo matches the shipped tutorial.
		draw_line(Vector2(-150.0, 8.0), Vector2(-48.0, 8.0),
			Color(1.0, 0.34, 0.50, 0.70), 12.0, true)
		draw_line(Vector2(48.0, 8.0), Vector2(150.0, 8.0),
			Color(1.0, 0.34, 0.50, 0.70), 12.0, true)
		var start_x: float = -112.0 if rightward else 112.0
		var end_x: float = 112.0 if rightward else -112.0
		var x: float = lerpf(start_x, end_x, phase)
		var hand_center := Vector2(x, -10.0 - sin(phase * PI) * 18.0)
		draw_circle(hand_center, 48.0, Color(1.0, 0.86, 0.36, 0.20))
		draw_arc(hand_center, 48.0, 0.0, TAU, 40,
			Color(1.0, 0.92, 0.48, 0.86), 6.0, true)
		if ghost != null:
			draw_texture_rect(ghost, Rect2(hand_center - Vector2(44.0, 44.0),
				Vector2(88.0, 88.0)), false)
		else:
			draw_circle(hand_center, 24.0, Color(1.0, 0.96, 0.78, 0.94))

func _ready() -> void:
	layer = 15
	demo = SwipeDemo.new()
	demo.name = "BossSwipeGhostDemo"
	demo.mouse_filter = Control.MOUSE_FILTER_IGNORE
	demo.size = Vector2(360.0, 150.0)
	if ResourceLoader.exists(GHOST_HAND_PATH):
		(demo as SwipeDemo).ghost = load(GHOST_HAND_PATH) as Texture2D
	add_child(demo)
	_update_position()

func _process(delta: float) -> void:
	if not visible or demo == null:
		return
	elapsed += delta
	var cycle_index: int = int(elapsed / CYCLE_T)
	var cycle: float = fmod(elapsed, CYCLE_T)
	var u: float = clampf((cycle - 0.38) / 1.30, 0.0, 1.0)
	(demo as SwipeDemo).rightward = cycle_index % 2 == 0
	(demo as SwipeDemo).phase = 0.5 - 0.5 * cos(u * PI)
	demo.modulate.a = 1.0 if cycle >= 0.22 and cycle <= 1.92 else 0.38
	demo.queue_redraw()
	_update_position()

func set_anchor(screen_position: Vector2) -> void:
	anchor = screen_position
	_update_position()

func restart_demo() -> void:
	elapsed = 0.0
	visible = true

func _update_position() -> void:
	if demo != null:
		demo.position = anchor - demo.size * 0.5
