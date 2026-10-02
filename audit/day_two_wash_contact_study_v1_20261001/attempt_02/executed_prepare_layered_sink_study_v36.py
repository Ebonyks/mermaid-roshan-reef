from pathlib import Path
import json,shutil,subprocess,sys
r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');old=Path(__file__).parent
s=(old/'capture_doctor_sink_contact_v34.gd').read_text(encoding='utf-8').replace('doctor_sink_contact_v34','doctor_sink_contact_v36')
s=s.replace('var sink_front := false','var sink_offset := 35.0')
s=s.replace('hand - Vector2(128.0,105.0)*scale_factor','hand + Vector2(sink_offset,0.0) - Vector2(128.0,105.0)*scale_factor')
old_draw='\t\tif not sink_front:\n\t\t\tdraw_texture_rect(sink,sink_rect,false)\n\t\tdraw_texture_rect(character,character_rect,false)\n\t\tif sink_front:\n\t\t\tdraw_texture_rect(sink,sink_rect,false)'
new_draw='\t\tdraw_texture_rect(sink,sink_rect,false)\n\t\tdraw_texture_rect(character,character_rect,false)\n\t\tvar atlas: AtlasTexture = sink as AtlasTexture\n\t\tvar scale_factor := sink_extent/256.0\n\t\tvar front_region := Rect2(0.0,145.0,256.0,111.0)\n\t\tvar front_rect := Rect2(sink_rect.position+Vector2(0.0,145.0)*scale_factor,front_region.size*scale_factor)\n\t\tdraw_texture_rect_region(atlas.atlas,front_rect,front_region)'
assert old_draw in s;s=s.replace(old_draw,new_draw)
s=s.replace('[150.0,180.0,210.0]','[150.0,180.0]').replace('for front: bool in [false,true]:','for offset: float in [35.0,55.0]:').replace('canvas.sink_front=front','canvas.sink_offset=offset')
s=s.replace('"doctor_%d_key%d_sink%d_%s"%[width,source_index,int(extent),"front" if front else "behind"]','"doctor_%d_key%d_sink%d_offset%d"%[width,source_index,int(extent),int(offset)]')
s=s.replace('"sink_in_front":front','"sink_offset_x":offset,"front_region":[0,145,256,111],"draw_order":"whole_sink_behind_character_then_same_sink_front_region"').replace('assert(records.size()==26)','assert(records.size()==18)').replace('26_CAPTURED','18_CAPTURED')
(r/'tmp/capture_doctor_sink_contact_v36.gd').write_text(s,encoding='utf-8',newline='\n')
runner=(old/'prepare_and_run_doctor_contact_v34.py').read_text(encoding='utf-8').replace('doctor_sink_contact_v34','doctor_sink_contact_v36')
runner=runner.replace("shutil.copyfile(Path(__file__).with_name('capture_doctor_sink_contact_v34.gd'),r/'tmp/capture_doctor_sink_contact_v36.gd')",'')
runner=runner.replace("shutil.copyfile(Path(__file__).with_name('capture_doctor_sink_contact_v36.gd'),r/'tmp/capture_doctor_sink_contact_v36.gd')",'')
runner=runner.replace("assert not impact.exists();impact.write_text",'impact.write_text')
runner=runner.replace("Two authored doctor keys, three sink extents150/180/210, behind/front draw order,1280/1600 desktop widths;26 native captures including originals.","Two existing authored doctor keys, two sink extents150/180, hand-to-basin offsets35/55px,1280/1600 desktop widths;18 static views. Original first sink cell drawn behind character, then identical original front-region0,145,256,111 in front. No source-pixel editing or new sink generation.")
runner=runner.replace("'baseline':'c2116877de10202c40e1d939c77eb3646b5f202f'","'baseline':'fb03e0ac3dda1658e9ea188d33cc6e084871642b'")
runner=runner.replace("'files':['audit/day_two_wash_contact_study_v1_20261001/PROFILE.json']","'files':json.loads(impact.read_text(encoding='utf-8'))['files']")
runner=runner.replace("'result':'PENDING','evidence':'tmp/doctor_sink_contact_v36 before archive; exact sources unchanged; each view needs direct review.'","'result':'PENDING','evidence':'tmp/doctor_sink_contact_v36 before archive; first26-view below-floor evidence preserved. Layered same-sink crop/offsets pending individual review.'")
path=r/'tmp/run_layered_sink_contact_v36.py';path.write_text(runner,encoding='utf-8',newline='\n')
print('Prepared18 layered-contact views; first26-view failure preserved.',flush=True)
raise SystemExit(subprocess.run([sys.executable,'-X','utf8','-B',str(path)],cwd=r).returncode)
