from pathlib import Path
import json
r=Path.cwd();s=r/'assets_src/imagegen/job_art_nursery_20261019';p=r/'scripts/nursery_painted_art.gd';t=p.read_text('utf-8');a=t.index('const GLASS :=');b=t.index('var surface:',a);t=t[:a]+'''const BOTTLE_LABEL := [Vector2(139, 142), Vector2(152, 144), Vector2(163, 151),
	Vector2(170, 162), Vector2(171, 176), Vector2(167, 190), Vector2(157, 200),
	Vector2(144, 204), Vector2(130, 201), Vector2(118, 194), Vector2(110, 181),
	Vector2(109, 167), Vector2(113, 155), Vector2(124, 146)]
'''+t[b:]
old='''	if full != null:
		surface.draw_texture_rect(full, destination, false)
		_draw_empty_glass(destination, float(pose["remaining"]))''';assert old in t;t=t.replace(old,'\tif full != null:\n\t\t_draw_bottle(full, destination, float(pose["remaining"]))',1)
a=t.index('func _draw_empty_glass(');b=t.index('func draw_bedtime()',a);t=t[:a]+'''func _bottle_region(texture: Texture2D, source: Rect2, destination: Rect2) -> void:
	if source.size.x <= 0.0 or source.size.y <= 0.0:
		return
	surface.draw_texture_rect_region(texture,
		Rect2(destination.position + source.position / 256.0 * destination.size,
			source.size / 256.0 * destination.size), source)

func _draw_bottle(full: Texture2D, destination: Rect2, remaining: float) -> void:
	# Disjoint source regions: translucent empty glass must REPLACE milk pixels,
	# never alpha-blend on top of them. The original exterior/nipple stays exact.
	for fixed: Rect2 in [Rect2(0, 0, 256, 112), Rect2(0, 112, 83, 114),
			Rect2(173, 112, 83, 114), Rect2(0, 226, 256, 30)]:
		_bottle_region(full, fixed, destination)
	var split := lerpf(112.0, 226.0, 1.0 - clampf(remaining, 0.0, 1.0))
	_bottle_region(art("bottle_empty"), Rect2(83, 112, 90, split - 112.0), destination)
	_bottle_region(full, Rect2(83, split, 90, 226.0 - split), destination)
	# Only the source-painted medallion is overlaid; the rectangular corners
	# around it must not carry the old milk through the empty state.
	var vertices := PackedVector2Array()
	var uvs := PackedVector2Array()
	for point: Vector2 in BOTTLE_LABEL:
		vertices.append(destination.position + point / 256.0 * destination.size)
		uvs.append(point / 256.0)
	surface.draw_polygon(vertices, PackedColorArray([Color.WHITE]), uvs, full)

'''+t[b:];p.write_text(t,encoding='utf-8')
p=r/'scripts/opera_gesture_surface.gd';t=p.read_text('utf-8');old='at = center.lerp(pat_target, clampf(cycle / 0.9, 0.0, 1.0))';assert old in t;t=t.replace(old,'at = _nursery_burp_hand_point(0.0).lerp(pat_target, clampf(cycle / 0.9, 0.0, 1.0))',1);p.write_text(t,encoding='utf-8')
p=r/'scripts/opera_career_world_2d.gd';t=p.read_text('utf-8');anchor='var career_id := ""';assert anchor in t;t=t.replace(anchor,'var painted_feedback_art: PaintedFeedbackArt = null\n'+anchor,1)
a='\t\tvar colour := Color("#fff1b2") if filled else Color(0.34, 0.55, 0.86, 0.42)';assert a in t;t=t.replace(a,'''		if career_id == "nursery":
			if painted_feedback_art == null:
				painted_feedback_art = PaintedFeedbackArt.new()
			var partial := progress * float(pearl_count) - float(index)
			var state := "full" if filled else ("filling" if partial > 0.0 else "empty")
			painted_feedback_art.pearl(action_panel, at, state)
			continue
'''+a,1)
a='if career_id in ["teacher", "geologist"] \\\n\t\t\tor (career_id == "racer" and mode == "kart_race"):';assert a in t;t=t.replace(a,'if career_id in ["teacher", "geologist", "nursery"] \\\n\t\t\tor (career_id == "racer" and mode == "kart_race"):',1);p.write_text(t,encoding='utf-8')
p=r/'design/audit_impacts/job-art-nursery-20261019.json';d=json.loads(p.read_text());d['scope']+=' Current04 full-use review catches two remaining presentation defects: the initial BURP hint lerps through the face and empty translucent glass was alpha-overlaid on milk. Start the hint beside its own hand; use disjoint full/empty source rows with only the exact painted medallion overlaid. Preserve full exterior/nipple and all fill logic; no RGB redraw or extra bottle generation. Nursery and Boxer consume the same new painted pearl family; Nursery completion holds its actual finished picture without the unrelated Boxer puff/square burst. SharedP8other consumers remain pending.';d['files']=sorted(set(d['files']+['scripts/painted_feedback_art.gd']+[f.relative_to(r).as_posix() for f in s.rglob('*') if f.is_file()]));p.write_text(json.dumps(d,indent=2)+'\n')
p=s/'capture_current04.gd';t=p.read_text('utf-8').replace('review_current04','review_current05').replace('nursery_capture_appdata_current04','nursery_capture_appdata_current05');(s/'capture_current05.gd').write_text(t,encoding='utf-8');p=s/'run_capture.py';t=p.read_text('utf-8').replace("'current03','current04']","'current03','current04','current05']");t=t.replace("'nursery_painted_art.gd','opera_gesture_surface.gd'","'nursery_painted_art.gd','painted_feedback_art.gd','opera_gesture_surface.gd'");t=t.replace("pins={p.relative_to(r)","files+=list((r/'assets/ui').glob('pearl_*.png'))\npins={p.relative_to(r)");p.write_text(t,encoding='utf-8')
p=s/'current02_visual_diagnosis.json';d=json.loads(p.read_text());d['current04']='Behavior100GUIframesPASS/no source drift/actualsaveunchanged; quilts distinct, whole wash and baby-mouth registration draw. VisualFAIL initial BURP hint still lerped through face from panelcentre; translucent empty-glass overlay retained milk, and unrelated completion puff obscured finished work. Current05 uses disjoint source replacement, source-label mask, safe guide entry and painted shared pearls; completion remains clean.';d['current05']='PENDING latest actual scene review; no4.5score yet.';p.write_text(json.dumps(d,indent=2)+'\n')
print('Nursery current04 visual findings repaired; current05 capture pending after shared class/asset import')
