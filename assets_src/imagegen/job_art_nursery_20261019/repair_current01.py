from pathlib import Path
from PIL import Image
import json,hashlib,shutil
r=Path.cwd();s=r/'assets_src/imagegen/job_art_nursery_20261019';p=r/'design/audit_impacts/job-art-nursery-20261019.json';d=json.loads(p.read_text());d['files']=sorted(set(d['files']+['scripts/opera_stage_paths.gd']));d['scope']+=' Current01 visual review rejects undersized/padded room framing and indistinct cloth states despite100GUI checks passing. Restore only the exact sharp native1024x576portion of the same existing Nursery painting, pixel-equal to current tiles, retaining native-resolution debt; remap Nursery-only station coordinates to the whole sharp frame. Use final2quilt calls within6aggregate cap, preserve both earlier candidates, choose whole cloth keys at the same natural width/top and draw draped cloth in front of its own rail.';p.write_text(json.dumps(d,indent=2)+'\n')
p=r/'scripts/opera_world_backdrop_2d.gd';t=p.read_text('utf-8');anchor='\tif racer_driving and career_id == "racer" and world_tiles.size() == 4:';assert anchor in t
t=t.replace(anchor,'\tif career_id == "nursery" and world_tiles.size() == 4:\n\t\t_draw_nursery_sharp_room()\n\t\treturn\n'+anchor,1)
anchor='func _draw_racer_circuit() -> void:';assert anchor in t
t=t.replace(anchor,'''func _draw_nursery_sharp_room() -> void:
	# Exact native1024x576 sharp region, verified against source bytes.
	# Framing repair only: native2K-per-screen coverage remains unmet.
	var native_rect := Rect2(512, 731, 1024, 576)
	for row in range(2):
		for column in range(2):
			var tile_origin := Vector2(column * 1024, row * 1024)
			var overlap := native_rect.intersection(Rect2(tile_origin, Vector2(1024, 1024)))
			var source := Rect2(overlap.position - tile_origin, overlap.size)
			var destination := Rect2((overlap.position - native_rect.position) / native_rect.size * size,
				overlap.size / native_rect.size * size)
			draw_texture_rect_region(world_tiles[row * 2 + column], destination, source)


'''+anchor,1);p.write_text(t,encoding='utf-8')
p=r/'scripts/opera_stage_paths.gd';t=p.read_text('utf-8');old='"nursery": [0.0947, 0.9077],';assert old in t;t=t.replace(old,'"nursery": [0.0, 1.0], # Same sharp painting now fills the whole canvas.',1);p.write_text(t,encoding='utf-8')
# Preserve attempt01 normalization/provenance and source bytes before changing derivatives.
shutil.copyfile(s/'prepare_runtime.py',s/'prepare_runtime_attempt01.py');shutil.copyfile(s/'runtime_provenance.json',s/'runtime_provenance_attempt01.json');old=s/'review/retired_quilts01';old.mkdir(parents=True,exist_ok=True)
for name in ['folded','half','tucked']:shutil.copyfile(r/('assets/opera/worlds/nursery_quality_20261019/quilt_'+name+'.png'),old/('quilt_'+name+'.png'))
p=s/'prepare_runtime.py';t=p.read_text('utf-8-sig');a=t.index('for name in [\'folded\',\'half_retry\',\'tucked\']:');b=t.index('# Uniformly register the empty source',a)
t=t[:a]+'''for name,native in [('folded','quilt_folded_native'),('half','quilt_half_long_native'),('tucked','quilt_tucked_long_native')]:
 p=s/(native+'.png');im=Image.open(p).convert('RGBA');b=im.getchannel('A').point(lambda a:255 if a>=16 else 0).getbbox();b=(max(0,b[0]-4),max(0,b[1]-4),min(im.width,b[2]+4),min(im.height,b[3]+4));c=im.crop(b);c.thumbnail((504,504),Image.Resampling.LANCZOS);place=((512-c.width)//2,4)
 emit('quilt_'+name,p,(504,504),b,(512,512),place)
'''+t[b:];p.write_text(t,encoding='utf-8')
p=r/'scripts/nursery_painted_art.gd';t=p.read_text('utf-8');a=t.index('func draw_bedtime()');b=t.index('func draw_burp()',a);part=t[a:b];part=part.replace('\t\tvar progress: Array =','\t\tcrib_front(crib)\n\t\tvar progress: Array =',1).replace('var width := crib.size.x * 0.84','var width := crib.size.x * 0.54').replace('Vector2(width, width * 0.5)','Vector2.ONE * width');last=part.rfind('\n\t\tcrib_front(crib)');assert last>=0;part=part[:last]+part[last:].replace('\n\t\tcrib_front(crib)','',1);t=t[:a]+part+t[b:];p.write_text(t,encoding='utf-8')
# A new capture version, never overwrite current01 or its preserved failure-by-appearance.
p=s/'capture_current01.gd';t=p.read_text('utf-8-sig').replace('review_current01','review_current02').replace('nursery_capture_appdata_current01','nursery_capture_appdata_current02');(s/'capture_current02.gd').write_text(t,encoding='utf-8')
p=s/'run_capture.py';t=p.read_text('utf-8-sig').replace("assert name=='current01'","assert name in ['current01','current02']");t=t.replace("'opera_world_backdrop_2d.gd']","'opera_world_backdrop_2d.gd','opera_stage_paths.gd']");p.write_text(t,encoding='utf-8')
p=s/'job_cards.json';d=json.loads(p.read_text());d['actual_call_accounting'].update(total=13,quilt_all_keys_including_reject=6);d['quilt_generation_closed']='Aggregate6calls exhausted. Final source/current context review still pending; no more quilt generations under this card. Current01 prior source selection explicitly failed actual-use readability; all native and prior runtime/provenance preserved.';p.write_text(json.dumps(d,indent=2)+'\n')
print('Nursery attempt02: exact native room crop/station remap and distinct natural cloth keys; earlier attempt retained')
