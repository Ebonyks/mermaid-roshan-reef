from pathlib import Path
import json,subprocess,hashlib,importlib.util,os
P=Path(__file__).resolve().parent;R=P.parents[3];H=P.parent;D='dd799b2d43871b29d1d6e0503646308a194dad1e'
spec=importlib.util.spec_from_file_location('retained78scanner',H/'r78_game_payload_closure/scan_game_payload.py');A=importlib.util.module_from_spec(spec);spec.loader.exec_module(A)
A.TARGETS={'_flash','_circle','pulse_context_action'};A.FIELDS=set();A.BODIES=A.TARGETS|{'_ready','_process','_release_stick','_unhandled_input','_hybrid_unhandled_input','_classic_unhandled_input','_on_touch_world'}
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*args):return subprocess.check_output(['git',*args],cwd=R,stderr=subprocess.PIPE)
def scan(text,path):return A.scan(text,path)
def main():
 source=json.loads((H/'r78_game_payload_closure/SOURCE_PAYLOAD_GRAPH.json').read_text(encoding='utf-8'));keys=['named_calls','literal_reflective_calls','ambiguous_literal_dispatch_arguments','target_references','field_references','field_literal_property_access','declarations','function_bodies'];rows={k:[]for k in keys};files=[]
 owners={'scripts/main.gd','scripts/touch_ui.gd'}
 for i,old in enumerate(source['files'],1):
  raw=git('show',D+':'+old['path']);assert sha(raw)==old['sha256'];out=scan(raw.decode('utf-8-sig'),old['path']);files.append(old)
  for k,rr in out.items():
   if k=='function_bodies'and old['path']not in owners:continue
   rows[k].extend(dict(x,probe_or_test_filename=old['probe_or_test_filename'])for x in rr)
  if i%100==0:print('R81_PARSED',i,'of',len(source['files']),flush=True)
 prod=[x for x in rows['named_calls']if not x['probe_or_test_filename']];fields=[x for x in rows['field_references']if not x['probe_or_test_filename']]
 summary={'parsed_scripts':len(files),'named_target_calls':len(rows['named_calls']),'non_test_named_target_calls':len(prod),'non_test_touch_ui_flash_calls':len([x for x in prod if x['path']=='scripts/touch_ui.gd' and x['method']=='_flash']),'allcaller_closure':False,'global_legacy_unreachability_proved':False}
 doc={'schema':'reef.touch_flash_owner_graph/1','source_revision':D,'scanner_sha256':sha(Path(__file__).read_bytes()),'retained_scanner_path':str((H/'r78_game_payload_closure/scan_game_payload.py').relative_to(R)).replace('\\','/'),'retained_scanner_revision':'ce4a454f65fc5b61f915ce41176af866fdf633ab','retained_scanner_sha256':sha((H/'r78_game_payload_closure/scan_game_payload.py').read_bytes()),'files':files,'target_names':sorted(A.TARGETS),**rows,'summary':summary,'limits':'Exact AST named calls only. Same method basename across unrelated receiver classes is not the same flash design. Current TouchUI local calls are bounded separately; variable/native/reflective/resource/debug routes remain open. Source construction and flash lifetime do not accept artwork, whole modes, device/child/owner or zero-art.'}
 dest=Path(os.environ.get('R81_ANALYSIS_OUTPUT',str(P)));dest.mkdir(exist_ok=True,parents=True);(dest/'SOURCE_OWNER_GRAPH.json').write_text(json.dumps(doc,indent=2)+'\n',encoding='utf-8',newline='\n');print('R81_SOURCE_SUMMARY',json.dumps(summary),flush=True)
if __name__=='__main__':main()