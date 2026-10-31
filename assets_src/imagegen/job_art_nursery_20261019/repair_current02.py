from pathlib import Path
import json,hashlib
r=Path.cwd();s=r/'assets_src/imagegen/job_art_nursery_20261019';p=r/'scripts/opera_gesture_surface.gd';t=p.read_text('utf-8')
a='func _draw_causal_context(center: Vector2) -> bool:\n';assert a in t;t=t.replace(a,a+'\tif visual_context == "nursery_wash":\n\t\t_nursery_art().draw_wash()\n\t\treturn true\n',1)
old='var mouth := _nursery_baby_center(baby_index) + Vector2(size.x * 0.025, -size.y * 0.055)';assert old in t;t=t.replace(old,'var mouth := _nursery_baby_mouth(baby_index)',1)
a='func _nursery_feed_bottle_pose(active: bool) -> Dictionary:';assert a in t;t=t.replace(a,'''func _nursery_baby_mouth(index: int) -> Vector2:
	# Measured from each unchanged320-square painted baby, not its head box.
	var points := [Vector2(164, 132), Vector2(156, 134), Vector2(161, 133)]
	var side := minf(size.x, size.y) * 0.29
	return _nursery_baby_center(index) + (points[clampi(index, 0, 2)] / 320.0
		- Vector2.ONE * 0.5) * side


'''+a,1);t=t.replace('"remaining": 1.0 - fill,\n\t\t"baby": baby_index,','"remaining": 1.0 - fill,\n\t\t"approach": approach,\n\t\t"baby": baby_index,',1);p.write_text(t,encoding='utf-8')
p=r/'scripts/nursery_painted_art.gd';t=p.read_text('utf-8');t=t.replace('func draw_wash() -> void:\n','func draw_wash() -> void:\n\tsurface.set_meta("nursery_painted_draw_route", "whole_connected_wash")\n',1)
for name,route in [('draw_feed','registered_bottle_and_crib'),('draw_bedtime','three_whole_quilt_keys'),('draw_burp','painted_hand_on_swaddle')]:t=t.replace('func '+name+'() -> void:\n','func '+name+'() -> void:\n\tsurface.set_meta("nursery_painted_draw_route", "'+route+'")\n',1)
p.write_text(t,encoding='utf-8')
p=r/'scripts/opera_career_world_2d.gd';t=p.read_text('utf-8');old='in ["FEED", "BURP"]:';assert t.count(old)==2;t=t.replace(old,'in ["CATCH BABIES", "FEED", "BURP", "BEDTIME"]:');p.write_text(t,encoding='utf-8')
p=r/'scripts/opera_nursery_catch.gd';t=p.read_text('utf-8');t=t.replace('size.y * PILLOW_Y - extent * 0.43','size.y * PILLOW_Y - extent * 0.47',1);old='''		_draw_baby(int(entry.get("texture", 0)),
			Vector2(float(entry.get("x", 0.5)) * size.x,
				float(entry.get("y", 0.0)) * size.y - extent * 0.27), extent)''';new='''		# The completed-care hold shows any already-spawned extra baby safe on
		# a pillow, with no sixth catch/reward or airborne frozen recipient.
		var center_y := size.y * PILLOW_Y - extent * 0.47 if not active and caught >= goal \
			else float(entry.get("y", 0.0)) * size.y - extent * 0.315
		_draw_baby(int(entry.get("texture", 0)),
			Vector2(float(entry.get("x", 0.5)) * size.x, center_y), extent)''';assert old in t;t=t.replace(old,new,1);p.write_text(t,encoding='utf-8')
# Preserve diagnosed failed visual versions. The latest fixture verifies the
# wash draw route as well as state, and records registration geometry.
p=s/'capture_current02.gd';t=p.read_text('utf-8').replace('review_current02','review_current03').replace('nursery_capture_appdata_current02','nursery_capture_appdata_current03')
a='func _shot(state: String) -> void:\n';assert a in t;t=t.replace(a,a+'''	if phase_id != "wash-hands":
		world._update_nursery_care_pose(world.phases[world.phase_index] as Dictionary)
''',1)
a='"partner_visible":world.rival_actor.visible,';assert a in t;t=t.replace(a,a+'''
		"surface_visible":surface.visible,"context":surface.visual_context,
		"widget_template":surface.widget_template,
		"painted_draw_route":String(surface.get_meta("nursery_painted_draw_route","")),
		"action_panel": [world.action_panel.position.x,world.action_panel.position.y,world.action_panel.size.x,world.action_panel.size.y],
		"surface_origin": [surface.global_position.x,surface.global_position.y],''',1)
a='\t\t\t\t\t_ck("connected wash owns the sole Roshan picture",not world.player_actor.visible)';assert a in t;t=t.replace(a,a+'\n\t\t\t\t\t_ck("whole wash source actually reaches Canvas",String(surface.get_meta("nursery_painted_draw_route","")) == "whole_connected_wash")',1)
(s/'capture_current03.gd').write_text(t,encoding='utf-8')
p=s/'run_capture.py';t=p.read_text('utf-8').replace("['current01','current02']","['current01','current02','current03']");p.write_text(t,encoding='utf-8')
p=r/'design/audit_impacts/job-art-nursery-20261019.json';d=json.loads(p.read_text());d['scope']+=' Current02 confirms correct framing/cloth roles but exposes an unreachable wash draw behind generic widget selection and inaccurate old fixed mouth offset. Route whole connected wash before generic widgets; keep sole-Roshan hiding/restoration, and measure each unchanged baby mouth in native320coordinates for literal nipple contact. Apply the approved8care poses to catch/feed/burp/bedtime; no generic atlas prop duplicates. Completed-catch still depicts any already-spawned extra baby safe on pillows without awarding a sixth catch; runtime motion/contact review remains explicit.';d['files']=sorted(set(d['files']+[f.relative_to(r).as_posix() for f in s.rglob('*') if f.is_file()]));p.write_text(json.dumps(d,indent=2)+'\n')
(s/'current02_visual_diagnosis.json').write_text(json.dumps({'current01':'Behavior100framesPASS but visualFAIL: padded room, cloth keys too similar, wash route unreachable and bottle tip offset.','current02':'Behavior100framesPASS/no source drift/actual-save unchanged; same1024x576sharp region nowfillsframe, full quilt clearly drapes. VisualFAIL remains wash route (empty picture despite hidden stageRoshan) and bottle tip oldoffset on cheek; captured source-derived coordinate correction in nextsource.','current03':'PENDING; no4.5score assigned before actual picture review.','source_baby_mouth_pixels320':[[164,132],[156,134],[161,133]],'limits':'LocalAI source measurement, not independent human/device/owner motion acceptance.'},indent=2)+'\n')
print('Current02 diagnosis recorded; unreachable wash and source mouth registration repaired, latest GUI review pending')
