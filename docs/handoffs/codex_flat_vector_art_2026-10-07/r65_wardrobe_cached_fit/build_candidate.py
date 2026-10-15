from pathlib import Path
import json,shutil
R=Path.cwd();H=R/'docs/handoffs/codex_flat_vector_art_2026-10-07';P=H/'r65_wardrobe_cached_fit';O=H/'r64_wardrobe_material_reuse';W=Path(r'C:/Users/Peter/.codex/worktrees/flat-vector-dev-context-20261015/mermaid-roshan-reef');S=Path(r'C:/Users/Peter/AppData/Local/Temp/reef-flat-vector-wardrobe-cached-fit-20261015')
old=(O/'wardrobe_material_candidate.gd').read_text(encoding='utf-8-sig');opening=old[old.index('func _open_wardrobe()'):]
opening=opening.replace('var replacement := StyleBoxTexture.new()\n\t\t\t\treplacement.texture = texture','var replacement: StyleBoxTexture = _r65_parent_style')
opening=opening.replace('replacement = _card_style("normal")','replacement = _r65_frames["white"] as StyleBoxTexture')
header='''extends "res://scripts/wardrobe_ui.gd"
# R65 ignored refinement; original source pixels, input targets and portrait rectangles stay unchanged.
const PANEL_ART: Texture2D = preload("res://assets/fashion/skin_engine_v2/ui/wardrobe_panel.png")
const CARD_ART: Texture2D = preload("res://assets/fashion/skin_engine_v2/ui/wardrobe_card.png")
var r64_shell_binding: Dictionary = {}
var r64_open_count: int = 0
var r64_refresh_count: int = 0
var _r65_frames: Dictionary = {}
var _r65_empty: StyleBoxEmpty
var _r65_parent_style: StyleBoxTexture
var _r65_style_creations: int = 0
var _r65_source_refreshes: int = 0
var _r65_paint_skips: int = 0
var _r65_frame_nodes_created: int = 0
var _r65_sync_writes: int = 0
var _r65_last_key: String = ""

func _init(main: ReefMain) -> void:
	super(main)
	for mode: String in ["white", "hover", "warm"]:
		var painted := StyleBoxTexture.new()
		painted.texture = CARD_ART
		painted.region_rect = Rect2(9, 8, 223, 224)
		painted.texture_margin_left = 36
		painted.texture_margin_right = 36
		painted.texture_margin_top = 36
		painted.texture_margin_bottom = 36
		painted.modulate_color = Color.WHITE if mode == "white" else (Color(1.0, 0.95, 0.83) if mode == "hover" else Color(1.0, 0.86, 0.64))
		_r65_frames[mode] = painted
		_r65_style_creations += 1
	_r65_empty = StyleBoxEmpty.new()
	_r65_empty.content_margin_left = 12
	_r65_empty.content_margin_right = 36
	_r65_empty.content_margin_top = 12
	_r65_empty.content_margin_bottom = 12
	_r65_style_creations += 1
	_r65_parent_style = StyleBoxTexture.new()
	_r65_parent_style.texture = PANEL_ART
	_r65_style_creations += 1

func r65_stats() -> Dictionary:
	var resources: Dictionary = {"empty": _r65_empty.get_instance_id(), "parent": _r65_parent_style.get_instance_id()}
	for key: String in _r65_frames:
		resources[key] = (_r65_frames[key] as StyleBoxTexture).get_instance_id()
	return {"style_creations": _r65_style_creations, "source_refreshes": _r65_source_refreshes, "paint_scans": r64_refresh_count, "duplicate_paint_skips": _r65_paint_skips, "frame_nodes_created": _r65_frame_nodes_created, "sync_writes": _r65_sync_writes, "resource_ids": resources, "inherited_open_allocations_not_removed_or_profiled": true}

func _wardrobe_refresh() -> void:
	if m.wardrobe_layer == null:
		return
	_r65_source_refreshes += 1
	if m.wd.has("preview"):
		(m.wd["preview"] as TextureRect).texture = FashionOutfitRenderer.portrait(m, "roshan") if m.skin_id == "classic" else load(String(m._skin_def(m.skin_id)["preview"]))
	for entry in m.wd.get("btns", []):
		var sel: bool = String(entry["id"]) == m.skin_id
		var eid := String(entry["id"])
		var locked: bool = eid.begins_with("fairy") and not m.fairy_skin_unlocked
		var bt: Button = entry["btn"]
		# Preserve all typography/role metadata effects of the old allocating style helper.
		StorybookUI._apply_button_typography(bt, StorybookUI.ROLE_CHILD_CONTROL, 28)
		var token: Dictionary = StorybookUI.typography_role(StorybookUI.ROLE_CHILD_CONTROL)
		bt.add_theme_color_override("font_hover_pressed_color", token["hover_pressed_color"])
		bt.set_meta("storybook_kind", "picture")
		bt.set_meta("picture_first", true)
		bt.set_meta("touch_target", true)
		bt.alignment = HORIZONTAL_ALIGNMENT_RIGHT
		bt.set_meta("selected", sel)
		bt.set_meta("locked", locked)
		bt.text = "🔒 " + String(m._skin_def(eid)["label"]) if locked else ("✔ " if sel else "    ") + String(m._skin_def(eid)["label"])
		bt.modulate = Color(0.75, 0.75, 0.8) if locked else Color.WHITE
	_paint_picker_buttons()

func _sync_frame(button: Button) -> void:
	if not is_instance_valid(button) or not button.is_inside_tree() or button.is_queued_for_deletion():
		return
	var frame: Panel = button.get_node_or_null("R65PaintedFrame") as Panel
	if frame == null:
		return
	var mode: String = "white"
	if not button.disabled:
		if button.is_pressed() or button.has_focus():
			mode = "warm"
		elif button.is_hovered():
			mode = "hover"
		elif bool(button.get_meta("selected", false)):
			mode = "warm"
	var wanted: StyleBoxTexture = _r65_frames[mode] as StyleBoxTexture
	if frame.get_theme_stylebox("panel") != wanted:
		frame.add_theme_stylebox_override("panel", wanted)
		_r65_sync_writes += 1
	frame.set_meta("r65_frame_mode", mode)

func _paint_picker_buttons() -> void:
	if m.wardrobe_layer == null or not m.wd.has("btns"):
		return
	var stage: Control = m.wd.get("stage") as Control
	if stage == null or stage.find_child("WardrobeLook_classic", true, false) == null:
		return
	var key: String = str(stage.get_instance_id()) + ":" + m.skin_id + ":" + str(m.fairy_skin_unlocked)
	if key == _r65_last_key:
		_r65_paint_skips += 1
		return
	_r65_last_key = key
	r64_refresh_count += 1
	for name: String in ["WardrobeLook_classic", "WardrobeLook_fairy", "WardrobeLook_huluu", "WardrobeFinishButton", "FashionWardrobeButton"]:
		var button: Button = stage.find_child(name, true, false) as Button
		if button == null:
			continue
		for state: String in ["normal", "hover", "pressed", "hover_pressed", "focus", "disabled"]:
			if button.get_theme_stylebox(state) != _r65_empty:
				button.add_theme_stylebox_override(state, _r65_empty)
		var frame: Panel = button.get_node_or_null("R65PaintedFrame") as Panel
		if frame == null:
			frame = Panel.new()
			frame.name = "R65PaintedFrame"
			frame.mouse_filter = Control.MOUSE_FILTER_IGNORE
			frame.show_behind_parent = true
			frame.position = Vector2(0, -7)
			frame.size = Vector2(button.size.x * 3.0, (button.size.y + 14.0) * 3.0)
			frame.scale = Vector2.ONE / 3.0
			frame.add_theme_stylebox_override("panel", _r65_frames["white"] as StyleBoxTexture)
			button.add_child(frame)
			_r65_frame_nodes_created += 1
			button.mouse_entered.connect(_sync_frame.bind(button))
			button.mouse_exited.connect(_sync_frame.bind(button))
			button.focus_entered.connect(_sync_frame.bind(button))
			button.focus_exited.connect(_sync_frame.bind(button))
			button.button_down.connect(_sync_frame.bind(button))
			button.button_up.connect(_sync_frame.bind(button))
		_sync_frame(button)

'''
(P/'wardrobe_cached_fit_candidate.gd').write_text(header+opening,encoding='utf-8',newline='\n')
shutil.copyfile(O/'wardrobe_material_candidate.gd',P/'wardrobe_previous_candidate.gd');shutil.copyfile(O/'base_capture.gd',P/'base_capture.gd')
print('R65_CANDIDATE_BUILT')
