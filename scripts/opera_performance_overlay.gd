class_name OperaPerformanceOverlay
extends Control
## Passive, wordless status for an Opera practice, staged act, and result.
## The owner supplies all state; this surface has no timer or autonomous flow.

const UI := preload("res://scripts/storybook_ui.gd")

const TOP_RECT := Rect2(390.0, 16.0, 500.0, 126.0)
const RESULT_RECT := Rect2(340.0, 70.0, 600.0, 220.0)
const MEDAL_COLORS: Array[Color] = [
	Color("#b96f45"), Color("#cbd6e4"), Color("#f4c64f")]
const CAREER_COLORS := {
	"chef": Color("#ff9385"), "detective": Color("#84b9f0"),
	"ballerina": Color("#ef8fbe"), "candymaker": Color("#f29ab3"),
	"doctor": Color("#6fd4df"), "farmer": Color("#8ed174"),
	"boxer": Color("#f47468"), "magician": Color("#bd91ec"),
	"painter": Color("#f4a15e"), "astronaut": Color("#76bde9"),
	"racer": Color("#ef665f"), "popstar": Color("#ef82ce"),
	"nursery": Color("#91d8c4"), "geologist": Color("#71ceb9"),
	"teacher": Color("#a79de6"),
}

var career_id := ""
var accent := UI.PURPLE
var on_stage := false
var player_progress := 0.0
var rival_progress := 0.0
var result_visible := false
var result_tier := 0
var token_delta := 0
var token_balance := 0
var delta_label: Label = null
var balance_label: Label = null
var _top_style: StyleBoxFlat = null
var _result_style: StyleBoxFlat = null


func _init() -> void:
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	clip_contents = false
	custom_minimum_size = UI.CANVAS_SIZE
	_top_style = UI.panel_style(UI.PURPLE, Color(0.94, 0.98, 1.0, 0.94), 28, 4)
	_result_style = UI.panel_style(UI.GOLD, Color(0.97, 0.95, 1.0, 0.98), 38, 6)
	_ensure_labels()


func configure(career: String) -> void:
	career_id = career
	accent = Color(CAREER_COLORS.get(career, UI.PURPLE))
	_top_style = UI.panel_style(accent, Color(0.94, 0.98, 1.0, 0.94), 28, 4)
	_result_style = UI.panel_style(accent, Color(0.97, 0.95, 1.0, 0.98), 38, 6)
	queue_redraw()


func set_part(next_on_stage: bool) -> void:
	on_stage = next_on_stage
	result_visible = false
	_sync_labels()
	queue_redraw()


func set_progress(player: float, rival: float) -> void:
	player_progress = clampf(player, 0.0, 1.0)
	rival_progress = clampf(rival, 0.0, 1.0)
	queue_redraw()


func show_result(tier: int, earned_delta: int, balance: int) -> void:
	result_tier = clampi(tier, 0, 3)
	token_delta = maxi(0, earned_delta)
	token_balance = maxi(0, balance)
	result_visible = true
	_sync_labels()
	queue_redraw()


func _ensure_labels() -> void:
	if delta_label != null:
		return
	delta_label = Label.new()
	delta_label.name = "EncoreDelta"
	delta_label.position = Vector2(610.0, 194.0)
	delta_label.size = Vector2(118.0, 56.0)
	delta_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	delta_label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	delta_label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	UI.style_hud_label(delta_label, 34, UI.PURPLE_DEEP, 4, UI.ROLE_NUMERIC)
	add_child(delta_label)
	balance_label = Label.new()
	balance_label.name = "EncoreBalance"
	balance_label.position = Vector2(790.0, 194.0)
	balance_label.size = Vector2(108.0, 56.0)
	balance_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	balance_label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	balance_label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	UI.style_hud_label(balance_label, 34, UI.PURPLE_DEEP, 4, UI.ROLE_NUMERIC)
	add_child(balance_label)
	_sync_labels()


func _sync_labels() -> void:
	if delta_label == null or balance_label == null:
		return
	delta_label.visible = result_visible
	balance_label.visible = result_visible
	delta_label.text = "+%d" % token_delta
	balance_label.text = "%d" % token_balance


func _draw() -> void:
	if result_visible:
		_draw_result()
	else:
		_draw_status()


func _draw_status() -> void:
	if career_id == "ballerina":
		draw_set_transform(Vector2(-214.0, 5.4), 0.0, Vector2(0.6, 0.6))
	draw_style_box(_top_style, TOP_RECT)
	if on_stage:
		_draw_curtain(Vector2(438.0, 79.0))
	else:
		_draw_book(Vector2(438.0, 79.0))
	_draw_progress_bar(Rect2(500.0, 48.0, 178.0, 22.0), player_progress,
		accent)
	if on_stage:
		_draw_progress_bar(Rect2(500.0, 88.0, 178.0, 22.0), rival_progress,
			UI.INK_SOFT)
	else:
		_draw_pearl(Vector2(693.0, 59.0), 10.0)
	for index in range(3):
		_draw_medal(Vector2(735.0 + float(index) * 62.0, 78.0), 22.0,
			MEDAL_COLORS[index])

	draw_set_transform(Vector2.ZERO, 0.0, Vector2.ONE)


func _draw_result() -> void:
	draw_style_box(_result_style, RESULT_RECT)
	var medal_color := MEDAL_COLORS[clampi(result_tier - 1, 0, 2)] \
		if result_tier > 0 else UI.MUTED
	_draw_medal(Vector2(470.0, 175.0), 62.0, medal_color)
	_draw_pearl(Vector2(585.0, 222.0), 22.0)
	_draw_pearl(Vector2(765.0, 222.0), 22.0)
	# A small shell divider makes “earned now” and “kept total” readable without
	# words: the left pearl points to +delta, the right pearl to the purse total.
	draw_line(Vector2(742.0, 197.0), Vector2(742.0, 247.0),
		UI.INK_SOFT, 3.0, true)
	for index in range(3):
		var filled := index < result_tier
		_draw_medal(Vector2(628.0 + float(index) * 54.0, 139.0), 17.0,
			MEDAL_COLORS[index] if filled else Color(0.68, 0.69, 0.78, 0.42))


func _draw_progress_bar(rect: Rect2, progress: float, color: Color) -> void:
	draw_rect(rect, Color(0.24, 0.18, 0.46, 0.18), true)
	draw_rect(Rect2(rect.position, Vector2(rect.size.x * progress, rect.size.y)),
		color, true)
	draw_rect(rect, UI.INK_SOFT, false, 3.0)
	_draw_pearl(Vector2(rect.position.x + rect.size.x * progress,
		rect.get_center().y), 8.0)


func _draw_book(center: Vector2) -> void:
	var left := PackedVector2Array([
		center + Vector2(-38.0, -28.0), center + Vector2(-3.0, -20.0),
		center + Vector2(-3.0, 30.0), center + Vector2(-38.0, 20.0)])
	var right := PackedVector2Array([
		center + Vector2(3.0, -20.0), center + Vector2(38.0, -28.0),
		center + Vector2(38.0, 20.0), center + Vector2(3.0, 30.0)])
	draw_colored_polygon(left, UI.PEARL)
	draw_colored_polygon(right, UI.PEARL_BLUE)
	draw_polyline(left, UI.INK, 4.0)
	draw_polyline(right, UI.INK, 4.0)
	draw_line(center + Vector2(0.0, -20.0), center + Vector2(0.0, 30.0),
		UI.INK, 4.0, true)


func _draw_curtain(center: Vector2) -> void:
	draw_line(center + Vector2(-42.0, -31.0), center + Vector2(42.0, -31.0),
		UI.GOLD, 6.0, true)
	draw_colored_polygon(PackedVector2Array([
		center + Vector2(-39.0, -27.0), center + Vector2(-5.0, -27.0),
		center + Vector2(-14.0, 31.0), center + Vector2(-43.0, 25.0)]),
		Color("#e86f91"))
	draw_colored_polygon(PackedVector2Array([
		center + Vector2(5.0, -27.0), center + Vector2(39.0, -27.0),
		center + Vector2(43.0, 25.0), center + Vector2(14.0, 31.0)]),
		Color("#e86f91"))
	draw_circle(center + Vector2(0.0, 2.0), 10.0, UI.GOLD)


func _draw_medal(center: Vector2, radius: float, color: Color) -> void:
	var ribbon_width := radius * 0.46
	draw_colored_polygon(PackedVector2Array([
		center + Vector2(-ribbon_width, radius * 0.52),
		center + Vector2(-radius * 0.08, radius * 1.55),
		center + Vector2(0.0, radius * 0.93)]), accent.darkened(0.14))
	draw_colored_polygon(PackedVector2Array([
		center + Vector2(ribbon_width, radius * 0.52),
		center + Vector2(radius * 0.08, radius * 1.55),
		center + Vector2(0.0, radius * 0.93)]), accent)
	draw_circle(center, radius, color)
	draw_arc(center, radius, 0.0, TAU, 32, UI.INK, maxf(3.0, radius * 0.12), true)
	draw_circle(center + Vector2(-radius * 0.28, -radius * 0.30),
		maxf(2.0, radius * 0.13), Color(1.0, 1.0, 1.0, 0.66))


func _draw_pearl(center: Vector2, radius: float) -> void:
	draw_circle(center, radius, UI.PEARL_BLUE)
	draw_arc(center, radius, 0.0, TAU, 24, UI.PURPLE_DEEP,
		maxf(2.0, radius * 0.15), true)
	draw_circle(center + Vector2(-radius * 0.30, -radius * 0.32),
		maxf(1.5, radius * 0.22), Color(1.0, 1.0, 1.0, 0.86))
