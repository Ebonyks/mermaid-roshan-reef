class_name EncounterGestureGuide2D
extends Control

## Reusable, noninteractive picture demonstration for a live screen target.
const HAND_PATH := "res://assets/castle/training/ghost_hand.png"
const TAP_CHIP_PATH := "res://assets/castle/training/verb_chip_tap.png"
const HOLD_CHIP_PATH := "res://assets/castle/training/verb_chip_hold.png"

var mode := "press"
var t := 0.0
var anchor := Vector2.ZERO
var hand_texture: Texture2D = null
var tap_chip: Texture2D = null
var hold_chip: Texture2D = null
var show_chip: bool = true
var cue_color := Color(1.0, 0.95, 0.6)
var _redraw_elapsed: float = 0.0
var _redraw_interval: float = 1.0 / 30.0

func configure_quality(quality: String) -> void:
	_redraw_interval = 1.0 / 30.0 if quality == "speedy" else 1.0 / 60.0

func _ready() -> void:
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	if ResourceLoader.exists(HAND_PATH):
		hand_texture = load(HAND_PATH) as Texture2D
	if ResourceLoader.exists(TAP_CHIP_PATH):
		tap_chip = load(TAP_CHIP_PATH) as Texture2D
	if ResourceLoader.exists(HOLD_CHIP_PATH):
		hold_chip = load(HOLD_CHIP_PATH) as Texture2D

func _process(delta: float) -> void:
	if not is_visible_in_tree():
		return
	t += delta
	_redraw_elapsed += delta
	if _redraw_elapsed >= _redraw_interval:
		_redraw_elapsed = 0.0
		queue_redraw()

func _pressing() -> bool:
	if mode == "hold":
		var full_t: float = float(HitEngine.CHARGE_STAGE_T[2])
		var hold_cycle: float = fmod(t, full_t + 1.1)
		return hold_cycle >= 0.7 and hold_cycle <= full_t + 0.85
	var cycle: float = fmod(t, 2.4)
	if mode == "drum":
		return (cycle > 0.9 and cycle < 1.1) or (cycle > 1.3 and cycle < 1.5) \
			or (cycle > 1.7 and cycle < 1.9)
	return cycle > 1.1

func _draw() -> void:
	if anchor == Vector2.ZERO:
		return
	var pressing: bool = _pressing()
	var halo: float = 30.0 if pressing else 20.0
	draw_circle(anchor, halo, Color(cue_color, 0.28))
	if hand_texture != null:
		var hand_size := Vector2(82.0, 82.0)
		var hand_origin: Vector2 = anchor - hand_size * Vector2(0.435, 0.875)
		hand_origin.y -= 0.0 if pressing else 10.0
		draw_texture_rect(hand_texture, Rect2(hand_origin, hand_size), false)
	else:
		draw_circle(anchor, 13.0, Color(1.0, 0.98, 0.88, 0.95))
	if pressing:
		var ring: float = 18.0 + fmod(t * 46.0, 26.0)
		draw_arc(anchor, ring, 0.0, TAU, 32, Color(cue_color, 0.7), 3.0, true)
	if mode == "hold" and pressing:
		var full_t: float = float(HitEngine.CHARGE_STAGE_T[2])
		var cycle: float = fmod(t, full_t + 1.1)
		var grow: float = clampf((cycle - 0.7) / full_t, 0.0, 1.0)
		var stage_col: Color = HitEngine.CHARGE_COLORS[clampi(int(grow * 3.0), 0, 2)]
		draw_arc(anchor, 34.0 + grow * 26.0, -PI * 0.5,
			-PI * 0.5 + TAU * maxf(grow, 0.06), 40,
			Color(stage_col.r, stage_col.g, stage_col.b, 0.85), 5.0, true)
	var chip: Texture2D = hold_chip if mode == "hold" else tap_chip
	if show_chip and chip != null and mode != "":
		var chip_size := Vector2(82.0, 82.0)
		draw_texture_rect(chip, Rect2(anchor + Vector2(54.0, -105.0), chip_size), false)
