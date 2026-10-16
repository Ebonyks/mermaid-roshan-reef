from pathlib import Path
import json,subprocess,hashlib,importlib.util,os
P=Path(__file__).resolve().parent;R=P.parents[3];H=P.parent;D='dd799b2d43871b29d1d6e0503646308a194dad1e'
spec=importlib.util.spec_from_file_location('retained78scanner',H/'r78_game_payload_closure/scan_game_payload.py');A=importlib.util.module_from_spec(spec);spec.loader.exec_module(A)
A.TARGETS={'_enter_level2','_enter_level2_now','_build_pearl_castle','_hang_portrait','_tick_level2','_populate_touch_interactables','_populate_courtyard_touch_interactables','_touch_open_picture','_mg2d_open','_start_playground_animation'};A.FIELDS={'wall_pics'};A.BODIES=A.TARGETS|{'_process','_lagoon_ref','_lagoon_promenade_ref','_register_target','_target_at','handle_touch','_activate','build','tick','_build_playground_screen','_tick_playground_animation','_tick_slide_animation'}
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*args):return subprocess.check_output(['git',*args],cwd=R,stderr=subprocess.PIPE)
def scan(text,path):return A.scan(text,path)
def main():
 source=json.loads((H/'r78_game_payload_closure/SOURCE_PAYLOAD_GRAPH.json').read_text(encoding='utf-8'));keys=['named_calls','literal_reflective_calls','ambiguous_literal_dispatch_arguments','target_references','field_references','field_literal_property_access','declarations','function_bodies'];rows={k:[]for k in keys};files=[]
 owners={'scripts/main.gd','scripts/arena/sky_lagoon.gd','scripts/arena/sky_lagoon_promenade.gd','scripts/games/picture_games.gd','scripts/arena/castle_rooms_25d.gd'}
 for i,old in enumerate(source['files'],1):
  raw=git('show',D+':'+old['path']);assert sha(raw)==old['sha256'];out=scan(raw.decode('utf-8-sig'),old['path']);files.append(old)
  for k,rr in out.items():
   if k=='function_bodies'and old['path']not in owners:continue
   rows[k].extend(dict(x,probe_or_test_filename=old['probe_or_test_filename'])for x in rr)
  if i%100==0:print('R79_PARSED',i,'of',len(source['files']),flush=True)
 prod=[x for x in rows['named_calls']if not x['probe_or_test_filename']];fields=[x for x in rows['field_references']if not x['probe_or_test_filename']]
 summary={'parsed_scripts':len(files),'named_target_calls':len(rows['named_calls']),'non_test_named_target_calls':len(prod),'non_test_wall_array_references':len(fields),'allcaller_closure':False,'global_legacy_unreachability_proved':False}
 doc={'schema':'reef.promenade_picture_owner_graph/1','source_revision':D,'scanner_sha256':sha(Path(__file__).read_bytes()),'retained_scanner_path':str((H/'r78_game_payload_closure/scan_game_payload.py').relative_to(R)).replace('\\','/'),'retained_scanner_revision':'ce4a454f65fc5b61f915ce41176af866fdf633ab','retained_scanner_sha256':sha((H/'r78_game_payload_closure/scan_game_payload.py').read_bytes()),'files':files,'target_names':sorted(A.TARGETS),**rows,'summary':summary,'limits':'Exact named source ownership/caller/property evidence only. Current entry/tick/touch selection does not globally retire reflected/native/alias/debug paths. Wall-array refs/loops, protected image occurrence or constructor presence are not artwork counts, child-route verification or accepted removals.'}
 dest=Path(os.environ.get('R79_ANALYSIS_OUTPUT',str(P)));dest.mkdir(exist_ok=True,parents=True);(dest/'SOURCE_OWNER_GRAPH.json').write_text(json.dumps(doc,indent=2)+'\n',encoding='utf-8',newline='\n');print('R79_SOURCE_SUMMARY',json.dumps(summary),flush=True)
if __name__=='__main__':main()