class_name RoshanSpriteFrames
extends RefCounted
# Per-frame atlas windows for the Mermaid Roshan 2.5D sheets.
#
# The generated sheets pack their figures on a ~236-250px pitch instead of the
# nominal 256px cell pitch that hframes/vframes assumes, and the error
# accumulates down the sheet. A plain uniform slice therefore does two visible
# things in the lower rows: it cuts the top of Roshan's head off, and it shows
# the head of the NEXT row's figure as a sliver along the bottom edge. The
# worst case measured (play_a "land") loses 36% of her body.
#
# SHIFTS moves each frame's window onto the figure that frame owns. The window
# stays 256x256, so the correction is lossless and conservative: paired with
# offset_correction() every pixel that renders today keeps its exact screen
# position, and the clipped pixels simply come back.
#
# These are measurements of the approved art, not art direction — not one pixel
# of any source PNG is modified. Regenerate the table after any sheet changes:
#     python3 tools/audit_roshan_sprite_clipping.py --emit-table
#
# Measured 2026-08-02 against the sheets landed 2026-08-01. Four frames still
# carry a small unavoidable ghost because the neighbouring figure genuinely
# overlaps the cell; those are listed in ROSHAN_SPRITE_CUTOFF_AUDIT_2026-08-02.md
# for the Codex regeneration pass.

const CELL := 256.0

# frame index -> texture-space translation of that frame's 256x256 window
const SHIFTS := {
	"directional": [
		Vector2(0, 0), Vector2(0, 0), Vector2(0, 0), Vector2(0, 0),
		Vector2(0, 0), Vector2(0, 0), Vector2(0, 0), Vector2(0, 0),
	],
	"swim_front": [
		Vector2(0, 0), Vector2(0, 0), Vector2(-21, 0), Vector2(-21, 0),
		Vector2(0, -5), Vector2(-11, -4), Vector2(-13, -1), Vector2(-13, -4),
		Vector2(0, -26), Vector2(0, -24), Vector2(-2, -23), Vector2(-2, -23),
		Vector2(0, -26), Vector2(-10, -24), Vector2(-22, -23), Vector2(-22, -23),
	],
	"swim_back": [
		Vector2(0, 0), Vector2(0, 0), Vector2(-4, 0), Vector2(-4, 0),
		Vector2(0, -5), Vector2(-10, -5), Vector2(-20, -5), Vector2(-20, -5),
		Vector2(0, -20), Vector2(0, -18), Vector2(-5, -17), Vector2(-5, -17),
		Vector2(0, -20), Vector2(-4, -18), Vector2(-14, -17), Vector2(-14, -17),
	],
	"gesture_a": [
		Vector2(0, 0), Vector2(0, 0), Vector2(0, 0), Vector2(0, 0),
		Vector2(0, -1), Vector2(0, 0), Vector2(0, 0), Vector2(0, 0),
		Vector2(0, -17), Vector2(0, -16), Vector2(0, -18), Vector2(0, -18),
		Vector2(0, -17), Vector2(0, -16), Vector2(0, -18), Vector2(0, -18),
	],
	"gesture_b": [
		Vector2(0, 0), Vector2(0, 0), Vector2(0, 0), Vector2(0, 0),
		Vector2(0, 0), Vector2(0, 0), Vector2(0, 0), Vector2(0, 0),
		Vector2(0, -9), Vector2(0, -10), Vector2(0, -10), Vector2(0, -10),
		Vector2(0, -13), Vector2(0, -12), Vector2(0, -12), Vector2(0, -13),
	],
	"gesture_c": [
		Vector2(0, 0), Vector2(0, 0), Vector2(0, 0), Vector2(0, 0),
		Vector2(0, -20), Vector2(0, -19), Vector2(0, -17), Vector2(0, -16),
		Vector2(0, -30), Vector2(0, -30), Vector2(0, -28), Vector2(0, -26),
		Vector2(0, -30), Vector2(0, -30), Vector2(0, -28), Vector2(0, -26),
	],
	"gesture_d": [
		Vector2(0, 0), Vector2(0, 0), Vector2(13, 0), Vector2(0, 0),
		Vector2(0, 0), Vector2(0, 0), Vector2(0, 0), Vector2(0, 0),
	],
	"play_a": [
		Vector2(0, 0), Vector2(0, 0), Vector2(0, 0), Vector2(0, 0),
		Vector2(0, -8), Vector2(0, -8), Vector2(0, -22), Vector2(0, -38),
		Vector2(0, -65), Vector2(0, -55), Vector2(0, -43), Vector2(0, -60),
		Vector2(0, -65), Vector2(0, -55), Vector2(0, -43), Vector2(0, -60),
	],
	"play_b": [
		Vector2(0, 0), Vector2(0, 0), Vector2(0, 0), Vector2(0, 0),
		Vector2(0, 0), Vector2(0, 0), Vector2(-6, 0), Vector2(-6, 0),
		Vector2(0, -4), Vector2(0, -3), Vector2(0, -21), Vector2(0, 0),
		Vector2(0, -4), Vector2(0, -3), Vector2(0, -21), Vector2(0, 0),
	],
}

static func has_sheet(sheet: String) -> bool:
	return SHIFTS.has(sheet)

static func shift(sheet: String, frame_index: int) -> Vector2:
	if not SHIFTS.has(sheet):
		return Vector2.ZERO
	var frames: Array = SHIFTS[sheet]
	if frames.is_empty():
		return Vector2.ZERO
	return frames[clampi(frame_index, 0, frames.size() - 1)] as Vector2

# The 256x256 texture window this frame should sample, shift included.
static func region(sheet: String, frame_index: int, columns: int) -> Rect2:
	var cols: int = maxi(1, columns)
	var safe: int = maxi(0, frame_index)
	var cell := Vector2(float(safe % cols), float(safe / cols)) * CELL
	return Rect2(cell + shift(sheet, safe), Vector2(CELL, CELL))

# Offset that cancels the window shift, so the pixels that render today keep
# their exact screen position and only the recovered art is new. Texture pixels
# run down the page while Sprite3D.offset.y moves up in world space, so the
# vertical term is negated — the same convention RoshanSpriteAnchors uses.
static func offset_correction(sheet: String, frame_index: int,
		flipped: bool) -> Vector2:
	var s: Vector2 = shift(sheet, frame_index)
	return Vector2(-s.x if flipped else s.x, -s.y)

# Applies the corrected window to a Sprite3D. hframes/vframes are deliberately
# left alone: Sprite3D ignores them once region_enabled is set, and callers
# such as CastleRooms25D still read them to derive the frame size.
static func apply_region(sprite: Sprite3D, sheet: String, frame_index: int,
		columns: int) -> void:
	if sprite == null or not has_sheet(sheet):
		return
	sprite.region_enabled = true
	sprite.region_rect = region(sheet, frame_index, columns)
