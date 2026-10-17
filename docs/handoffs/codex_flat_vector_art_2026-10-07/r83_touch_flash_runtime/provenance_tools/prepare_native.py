from pathlib import Path
import re,json,hashlib,subprocess,shutil
T=Path.cwd(); P=T/'docs/handoffs/codex_flat_vector_art_2026-10-07/r83_touch_flash_runtime'; R=Path('C:/Users/Peter/.codex/worktrees/flat-vector-r6-20261012/mermaid-roshan-reef'); O=R/'docs/handoffs/codex_flat_vector_art_2026-10-07/r82_touch_flash_reuse'
s=(O/'capture_entry.gd').read_text(encoding='utf-8').replace('R82_','R83_').replace('FLASH82','FLASH83').replace('ORIGINAL_SOURCE','RUNTIME_TRIAL_SOURCE')
s=s.replace('lane = "BOUNDED_CURRENT_ORIGINAL_TOUCH_FLASH" if mode=="RUNTIME_TRIAL_SOURCE" else "EXCLUDED_NONRUNTIME_PAINTED_RING_PROTOTYPE"','lane = "EXCLUDED_WORK_BRANCH_RUNTIME_TRIAL"')
a=s.index('func _touch_child('); b=s.index('func _observe_flash(',a)
s=s[:a]+'''func _touch_child(child: Node) -> void:
	if child is not Panel:
		return
	var panel := child as Panel
	var card := panel.get_node_or_null("PaintedRing") as TextureRect
	if card==null or panel.size!=Vector2(110,110) or not panel.get_theme_stylebox("panel") is StyleBoxEmpty:
		return
	flash_panels.append(panel)
	var id: int = panel.get_instance_id()
	candidate_rects[id]=card
	var original: Dictionary = _panel_data(panel)
	source_blueprints[id]=original
	flash_lifecycle.append({"event":"child_entered_tree","mode":mode,"panel":original,"ticks_msec":Time.get_ticks_msec()})
	panel.tree_exiting.connect(_flash_exit.bind(id))
	card.tree_exiting.connect(_art_exit.bind(id,card.get_instance_id()))
func _art_exit(parent_id: int, id: int) -> void:
	flash_lifecycle.append({"event":"painted_child_tree_exiting","parent_instance_id":parent_id,"instance_id":id,"ticks_msec":Time.get_ticks_msec()})
func _candidate_data(panel: Panel) -> Dictionary:
	var card := candidate_rects.get(panel.get_instance_id()) as TextureRect
	if not is_instance_valid(card):
		return {}
	var p: Vector2 = card.get_global_transform_with_canvas()*Vector2.ZERO
	var finish: Vector2 = card.get_global_transform_with_canvas()*card.size
	var ancestors: Array[Dictionary] = []
	var node: Node = card
	var rgb_preserved := true
	while is_instance_valid(node):
		if node is CanvasItem:
			var item := node as CanvasItem
			ancestors.append({"path":str(item.get_path()),"modulate_rgba":[item.modulate.r,item.modulate.g,item.modulate.b,item.modulate.a],"self_modulate_rgba":[item.self_modulate.r,item.self_modulate.g,item.self_modulate.b,item.self_modulate.a]})
			rgb_preserved=rgb_preserved and item.modulate.r==1.0 and item.modulate.g==1.0 and item.modulate.b==1.0 and item.self_modulate.r==1.0 and item.self_modulate.g==1.0 and item.self_modulate.b==1.0
		node=node.get_parent()
	return {"instance_id":card.get_instance_id(),"texture_path":card.texture.resource_path,"source_dimensions":_v(card.texture.get_size()),"rect_size":_v(card.size),"native_rect":[p.x,p.y,finish.x-p.x,finish.y-p.y],"modulate_rgba":[card.modulate.r,card.modulate.g,card.modulate.b,card.modulate.a],"self_modulate_rgba":[card.self_modulate.r,card.self_modulate.g,card.self_modulate.b,card.self_modulate.a],"ancestor_canvas_items":ancestors,"ancestor_rgb_preserved":rgb_preserved,"parent_panel_alpha":panel.modulate.a,"parent_is_original_panel":card.get_parent()==panel,"original_flat_style_retired":panel.get_theme_stylebox("panel") is StyleBoxEmpty,"mouse_filter_ignored":card.mouse_filter==Control.MOUSE_FILTER_IGNORE,"whole_source_bitmap":true,"work_branch_implementation":true,"visual_override_only":false}
''' +s[b:]
a=s.index('\t_check("source flash exact original blueprint'); b=s.index('\t_check("source flash alpha naturally declines',a)
s=s[:a]+'''	var candidate: Dictionary = onset.candidate as Dictionary
	_check("work-branch whole painted ring exact source bounds "+prefix,candidate.texture_path==RING_PATH and candidate.source_dimensions==[512.0,512.0] and candidate.rect_size==[110.0,110.0] and candidate.original_flat_style_retired and candidate.parent_is_original_panel and candidate.mouse_filter_ignored)
	_check("source RGB across all CanvasItem ancestors "+prefix,candidate.ancestor_rgb_preserved and candidate.modulate_rgba==[1.0,1.0,1.0,1.0] and candidate.self_modulate_rgba==[1.0,1.0,1.0,1.0])
	var child_id: int = int(candidate.instance_id)
''' +s[b:]
s=s.replace('\t_check("source flash naturally queue freed "+kind,not is_instance_valid(panel))','\t_check("source flash naturally queue freed "+kind,not is_instance_valid(panel))\n\t_check("same painted child naturally freed "+kind,not is_instance_id_valid(child_id))')
s=s.replace('"source_controller_unchanged":true,"visual_override":mode!="RUNTIME_TRIAL_SOURCE"','"source_controller_unchanged":true,"visual_override":false,"painted_child_instance_id":child_id,"painted_child_freed":not is_instance_id_valid(child_id)')
old='\tmode="LOCAL_NONRUNTIME_PAINTED_RING"\n\tfor kind: String in ["slide","swing"]:\n\t\tawait _observe_flash(kind)\n'; assert old in s;s=s.replace(old,'')
oldscope='R82 original private entry and actual original touch trials first retain the source StyleBoxFlat. Then LOCAL_NONRUNTIME_PAINTED_RING replaces only exact source flash material in this ignored observer with StyleBoxEmpty plus a whole existing painted-ring TextureRect child, preserving original Panel/controller/tween/fade/free and source RGB/aspect. Candidate frames are explicitly excluded from current source coverage, production replacement and acceptance. No source file, asset, game/phase/actor/timer override or generation/export. Full new-use/style/caller/QA11/device/child/owner/global acceptance remains open.'
newscope='R83 actual work-branch TouchUI implementation after original private NewGame/options/clip/travel and native input. Observer reads Panel/whole bitmap/ancestor RGB/same child natural teardown; no material, game, phase, actor, timer or controller override. Work-branch frames excluded from origin/dev source coverage and acceptance. New-use semantics, remaining callers, QA11/device/child/owner/global gaps open.'
assert oldscope in s;s=s.replace(oldscope,newscope).replace('reef.touch_flash_reuse/1','reef.touch_flash_runtime_trial/1').replace('"production_changes":[]','"production_changes":["scripts/touch_ui.gd"]')
assert 'add_theme_stylebox_override' not in s and 'card.texture='not in s and 'LOCAL_NONRUNTIME_PAINTED_RING'not in s
(P/'capture_entry.gd').write_text(s,encoding='utf-8',newline='\n')
dst=T/'export/flat_vector_r83';dst.mkdir(parents=True,exist_ok=True);shutil.copyfile(P/'capture_entry.gd',dst/'capture_entry.gd')
I=T/'design/audit_impacts/flat-vector-touch-runtime-20261016.json';d=json.loads(I.read_text(encoding='utf-8'));d['files'].append(str((P/'capture_entry.gd').relative_to(T)).replace('\\','/'));I.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
print('R83_OBSERVER_READ_ONLY_NO_VISUAL_OVERRIDES',hashlib.sha256((P/'capture_entry.gd').read_bytes()).hexdigest())
