from pathlib import Path
import json
r=Path.cwd();s=r/'assets_src/imagegen/job_art_nursery_20261019';p=r/'scripts/nursery_painted_art.gd';t=p.read_text('utf-8');a=t.index('func draw_guide(');t=t[:a]+'''func draw_guide(at: Vector2, pressing: bool) -> void:
	var side := 58.0 if pressing else 54.0
	var rotation := 0.0
	if surface.has_method("_is_nursery_feed_context"):
		var context := String(surface.get("visual_context"))
		if context in ["nursery_bedtime", "push_nursery", "nursery_burp"]:
			# Point from below the cloth/back so the palm never covers a face.
			rotation = PI
		elif context in ["nursery_feed", "pour_nursery"]:
			rotation = PI * 0.5
	else:
		side = 45.0
		rotation = -PI * 0.5 if at.x > surface.size.x * 0.65 else PI * 0.5
	surface.draw_set_transform(at, rotation)
	picture("guide_hand", Rect2(-Vector2(0.436523, 0.986328) * side, Vector2.ONE * side))
	surface.draw_set_transform(Vector2.ZERO)
''';p.write_text(t,encoding='utf-8')
p=r/'scripts/opera_gesture_surface.gd';t=p.read_text('utf-8');old='''				var feed_pose := _nursery_feed_bottle_pose(true)
				at = feed_pose.get("position", center) as Vector2''';assert old in t;t=t.replace(old,'\t\t\t\tat = _nursery_feed_bottle_rect(true).get_center()',1);p.write_text(t,encoding='utf-8')
p=r/'scripts/opera_nursery_catch.gd';t=p.read_text('utf-8');old='painted_art.draw_guide(catch_point, false)';assert old in t;t=t.replace(old,'painted_art.draw_guide(catch_point + Vector2(0, size.y * 0.08), false)',1);p.write_text(t,encoding='utf-8')
p=s/'capture_current03.gd';t=p.read_text('utf-8').replace('review_current03','review_current04').replace('nursery_capture_appdata_current03','nursery_capture_appdata_current04');anchor='"surface_origin": [surface.global_position.x,surface.global_position.y],';assert anchor in t;t=t.replace(anchor,anchor+'''
		"surface_canvas_origin": [surface.get_global_transform_with_canvas().origin.x,surface.get_global_transform_with_canvas().origin.y],
		"surface_size": [surface.size.x,surface.size.y],''',1);(s/'capture_current04.gd').write_text(t,encoding='utf-8')
p=s/'run_capture.py';t=p.read_text('utf-8').replace("['current01','current02','current03']","['current01','current02','current03','current04']");p.write_text(t,encoding='utf-8')
p=s/'current02_visual_diagnosis.json';d=json.loads(p.read_text());d['current03']='Behavior100GUIframesPASS/no source drift/actualsaveunchanged. Whole wash visibly draws once, source mouth correction lands nipple on mouth, older care poses actuallyused. Still visualFAILguide: down-pointing palm covers waiting bedtime face. Current04rotates guide below cloth/back, feed demo indicates actualbottlebody, catchdemo liesbelow safeheads; no state/reward change.';d['current04']='PENDING actual scene review; no4.5assigned yet.';p.write_text(json.dumps(d,indent=2)+'\n')
p=r/'design/audit_impacts/job-art-nursery-20261019.json';d=json.loads(p.read_text());d['scope']+=' Current03 actual scene review finds the down-pointing guide palm covers a waiting bedtime face. Use rigid whole-hand orientation from below cloth/back, indicate the bottle body for feed, and place the small catch hint below settled heads; retain source contours and all existing input targets/verbs.';p.write_text(json.dumps(d,indent=2)+'\n')
print('Guide face-occlusion repair complete; current04 captured separately')
