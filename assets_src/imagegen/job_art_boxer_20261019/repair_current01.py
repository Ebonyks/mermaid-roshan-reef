from pathlib import Path
import json,hashlib,shutil
r=Path.cwd();s=r/'assets_src/imagegen/job_art_boxer_20261019';p=s/'prepare_runtime.py';t=p.read_text('utf-8-sig');marker="(s/'runtime_provenance.json').write_text";assert marker in t
extra='''for name in ['focus_mitt','impact_puff']:
 p=s/(name+'_native.png');im=Image.open(p).convert('RGBA');im.thumbnail((512,512),Image.Resampling.LANCZOS);emit(im,o/(name+'.png'),p,'Whole native canvas uniformly downsampled to512; transparent margins and all authored contours retained. No crop/paint/warp.')
'''
t=t.replace(marker,extra+marker,1).replace("'7new calls:2ring/open,5pearl states including first empty/filling readability rejects.","'9new calls:2ring/open,5pearl states including first empty/filling readability rejects,1focusmitt and1cleanpuff.");p.write_text(t,encoding='utf-8')
p=r/'scripts/opera_boxing_surface.gd';t=p.read_text('utf-8');old='res://assets/opera/worlds/widgets/widget_track_boxer_mover.png';assert old in t;t=t.replace(old,'res://assets/opera/worlds/boxer_quality_20261019/focus_mitt.png',1);old='res://assets/opera/worlds/props/fx_bop_puff.png';assert old in t;t=t.replace(old,'res://assets/opera/worlds/boxer_quality_20261019/impact_puff.png',1)
a=t.index('func _draw_mitts()');b=t.index('func _draw_target(',a);t=t[:a]+'''func _draw_mitts() -> void:
	if _mitts_texture == null:
		return
	var side := minf(180.0, size.y * 0.26)
	var targets: Array[Vector2] = [active_target_position()]
	if mode == "boxing_guide":
		targets = [guide_target_position(0), guide_target_position(1)]
	for target: Vector2 in targets:
		# The authored shell medallion is the actual existing hit centre.
		draw_texture_rect(_mitts_texture,
			Rect2(target - Vector2(0.5, 0.516) * side, Vector2.ONE * side), false)


'''+t[b:];p.write_text(t,encoding='utf-8')
p=r/'scripts/opera_world_backdrop_2d.gd';t=p.read_text('utf-8');(s/'backdrop_before_boxer_framing.gd').write_text(t,encoding='utf-8')
a='\tif racer_driving and career_id == "racer" and world_tiles.size() == 4:';assert a in t;t=t.replace(a,'\tif career_id == "boxer" and not stage_mode and world_tiles.size() == 4:\n\t\t_draw_boxer_native_room()\n\t\treturn\n'+a,1)
a='func _draw_racer_circuit() -> void:';assert a in t;t=t.replace(a,'''func _draw_boxer_native_room() -> void:
	# Recover the complete existing1672x941 native frame from the same tiles;
	# retain original outer feather. This does not meet native2K coverage.
	var native_rect := Rect2(188, 553, 1672, 941)
	for row in range(2):
		for column in range(2):
			var tile_origin := Vector2(column * 1024, row * 1024)
			var overlap := native_rect.intersection(Rect2(tile_origin, Vector2(1024, 1024)))
			var source := Rect2(overlap.position - tile_origin, overlap.size)
			var destination := Rect2((overlap.position - native_rect.position) / native_rect.size * size,
				overlap.size / native_rect.size * size)
			draw_texture_rect_region(world_tiles[row * 2 + column], destination, source)


'''+a,1);t=t.replace('if career_id != "nursery" and (stage_mode or not _is_chapter2_clean_kitchen()):','if career_id not in ["nursery", "boxer"] and (stage_mode or not _is_chapter2_clean_kitchen()):',1).replace('if stage_mode and career_id != "nursery":','if stage_mode and career_id not in ["nursery", "boxer"]:',1);p.write_text(t,encoding='utf-8')
p=s/'capture_current01.gd';t=p.read_text('utf-8-sig').replace('review_current01','review_current02').replace('boxer_capture_appdata_current01','boxer_capture_appdata_current02');(s/'capture_current02.gd').write_text(t,encoding='utf-8');p=s/'run_capture.py';t=p.read_text('utf-8').replace("assert name=='current01'","assert name in ['current01','current02']");p.write_text(t,encoding='utf-8')
n=r/'assets_src/imagegen/job_art_nursery_20261019';p=n/'capture_current05.gd';t=p.read_text('utf-8').replace('review_current05','review_current06').replace('nursery_capture_appdata_current05','nursery_capture_appdata_current06');(n/'capture_current06.gd').write_text(t,encoding='utf-8');p=n/'run_capture.py';t=p.read_text('utf-8').replace("'current04','current05']","'current04','current05','current06']");p.write_text(t,encoding='utf-8')
p=r/'design/audit_impacts/job-art-nursery-20261019.json';d=json.loads(p.read_text());d['scope']+=' Boxer current02 retains original ring effect under an accurately positioned single focus mitt, a new clean puff, and exact existing native-framing repair of its world only; stage choice/current state unchanged. Nursery current06 refreshes exact shared-backdrop source pins after this unrelated Boxer-only branch; its previously reviewed render/inputs are unchanged.';d['files']=sorted(set(d['files']+[f.relative_to(r).as_posix() for f in s.rglob('*') if f.is_file()]+[f.relative_to(r).as_posix() for f in n.rglob('*') if f.is_file()]));p.write_text(json.dumps(d,indent=2)+'\n')
(s/'current01_visual_diagnosis.json').write_text(json.dumps({'current01':'152GUIframesPASS/no drift/live save unchanged; current art contextFAIL for fixed paired-mitt positioning/hidden halo, line-tailed puff, broad blurred surround/code spotlights. Original source/captures retained.','current02':'PENDING after new source-matched single mitt, cleanpuff and existing nativeframe repair; no4.5score before actual current review.','method':'Original ring remains under props, no over-object paint. Focus mitt medallion follows unchanged logical target, source contour fits existing156px interaction circle. All behavior functions retain exact integrated bytes.'},indent=2)+'\n')
print('Current02 Boxer context repair wired; fresh source-bound captures and full gates pending')
