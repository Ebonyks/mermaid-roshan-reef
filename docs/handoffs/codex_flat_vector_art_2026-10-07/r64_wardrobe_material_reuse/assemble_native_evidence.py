from pathlib import Path
import json,hashlib,subprocess,datetime,concurrent.futures,urllib.request,io,shutil
from PIL import Image
R=Path.cwd();H=R/'docs/handoffs/codex_flat_vector_art_2026-10-07';P=H/'r64_wardrobe_material_reuse';O=H/'r63_wardrobe_context';S=Path(r'C:/Users/Peter/AppData/Local/Temp/reef-flat-vector-wardrobe-material-reuse-20261015');B='d7703fef32f32c4e2727f43eaecef5ff73d8cdce';D='5120b6d59885dd057937aaf284e73681d8eac9f5'
def rd(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def wr(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(['git',*a],cwd=R,stderr=subprocess.PIPE)
frames=[];cases=[];textures=set();materials=[]
def walk(v):
 if isinstance(v,dict):
  for x in v.values():walk(x)
 elif isinstance(v,list):
  for x in v:walk(x)
 elif isinstance(v,str)and v.startswith('res://assets/'):textures.add(v[6:])
for folder in sorted((P/'native').iterdir()):
 m=rd(folder/'capture_manifest.json');launch=rd(folder/'LAUNCH.json');result=rd(folder/'RESULT.json');failed=result['exit_code']!=0;control=not m['candidate_enabled'];adjunct=launch['early_close_adjunct'];counts={'native':len(m['states']),'bounded':0,'excluded':0}
 assert not result['source_byte_changes'] and not result['script_or_shader_errors'] and result['sidecars_exact'] and result['fixture_dependencies_unchanged'] and result['normal_before']==result['normal_after']
 assert m['source_revision']==D and m['candidate_enabled']==launch['candidate'] and sha((folder/'engine.log').read_bytes())==result['log_sha256']
 assert len(list(folder.glob('*.png')))==len(m['states'])
 for st in m['states']:
  f=folder/st['path'];raw=f.read_bytes();assert sha(raw)==st['sha256'];im=Image.open(io.BytesIO(raw));im.load();assert list(im.size)==m['aspect']
  classification='EXCLUDED_FAILED_OBSERVER_CONTROL'if failed and control else'EXCLUDED_FAILED_V1_CANDIDATE'if failed else'EXCLUDED_ORIGINAL_SOURCE_CONTROL_DIAGNOSTIC'if control else'EXCLUDED_DECLARED_BOOTSTRAP'if st['id']in ['main_hall_checkpoint','fresh_main_checkpoint']else'BOUNDED_V2_REUSE_CANDIDATE_CONTEXT'
  counts['excluded'if classification.startswith('EXCLUDED')else'bounded']+=1
  frames.append({'case':folder.name,'id':st['id'],'path':f.relative_to(P).as_posix(),'sha256':sha(raw),'bytes':len(raw),'dimensions':list(im.size),'pixel_mode':im.mode,'pixel_sha256':sha(im.tobytes()),'classification':classification,'candidate':m['candidate_enabled']})
  snap=st['snapshot'];walk(snap)
  if not failed and snap['r64_materials']['active_legacy_picker']:
   mat=snap['r64_materials'];expected='StyleBoxFlat'if control else'StyleBoxTexture';assert len(mat['panels'])==2 and len(mat['buttons'])==5
   assert all(panel['style']['class']==expected for panel in mat['panels']);assert all(style['class']==expected for button in mat['buttons']for style in button['styles'].values());assert len(mat['ornaments'])==(5 if control else 0)
   if not control:assert mat['heading']['size']=='(430.0, 64.0)' and mat['heading']['line_count']==1 and mat['heading']['font_size']==42
   materials.append({'case':folder.name,'id':st['id'],'candidate':not control,'panel_instances':len(mat['panels']),'button_instances':len(mat['buttons']),'button_style_keys':sum(len(b['styles'])for b in mat['buttons']),'style_class':expected,'ornament_count':len(mat['ornaments']),'heading':mat['heading'],'sha256':sha(json.dumps(mat,sort_keys=True).encode())})
 cases.append({'case':folder.name,'manifest':(folder/'capture_manifest.json').relative_to(P).as_posix(),'manifest_sha256':sha((folder/'capture_manifest.json').read_bytes()),'launch':(folder/'LAUNCH.json').relative_to(P).as_posix(),'result':(folder/'RESULT.json').relative_to(P).as_posix(),'candidate':m['candidate_enabled'],'early_close_adjunct':adjunct,'aspect':m['aspect'],'fairy_unlocked_profile':m['fairy_unlocked_profile'],'checks':len(m['checks']),'failed_checks':[x['label']for x in m['checks']if not x['pass']],'exit_code':result['exit_code'],'counts':counts,'fixture_dependencies':launch['fixture_dependencies']})
assert len(cases)==8 and sum(x['counts']['native']for x in cases)==402 and sum(x['counts']['bounded']for x in cases)==231 and sum(x['counts']['excluded']for x in cases)==171
passed=[x for x in cases if x['exit_code']==0];assert len(passed)==6 and sum(x['checks']for x in passed)==268 and all(not x['failed_checks']for x in passed);assert sum(x['checks']for x in passed if x['candidate'])==219 and sum(x['checks']for x in passed if not x['candidate'])==49
wr(P/'CAPTURE_INDEX.json',{'revision':'FV-AUDIT-20261015-R64','source_revision':D,'cases':cases,'frames':frames,'native_events':402,'bounded_candidate_contexts':231,'excluded_diagnostics':171,'passing_candidate_checks':219,'passing_control_checks':49,'passing_checks':268,'limits':'Count native events, not designs/screens/removals. Failed observer control54 + failedv1candidate54 + passing sourcecontrol54 + candidatebootstrap9 all excluded. New231bounded are candidate-only, no production runtime/replacement or fullQA11/creative acceptance.'})
wr(P/'FRAME_PIXEL_IDENTITY.json',{'mode':'READ_ONLY_ORIGINAL_NATIVE_PNG_AND_DECODED_PIXEL_HASHES','edits_to_capture_pixels':0,'rows':[{k:x[k]for k in ['path','sha256','bytes','dimensions','pixel_mode','pixel_sha256']}for x in frames]})
wr(P/'MATERIAL_STATE_IDENTITY.json',{'rows':materials,'active_candidate_states':sum(x['candidate']for x in materials),'active_source_control_states':sum(not x['candidate']for x in materials),'scope':'All sampled active legacy-picker states in passing cases retain exact2materialPanels/5sourceButtons/6stylekeys and declared material type. Fulltime/focus/disabled/regionprojection/QA11 is not proven from state samples. Card region geometry is bound to exact candidate source and preserved sourcealpha bounding record, not independently decoded liveQA11projection.'})
refs={(x['revision'],x['path'])for x in rd(P/'SOURCE_REFERENCES.json')['files']};tracked=set(git('ls-tree','-r','--name-only',D,'--','assets').decode().splitlines())
for path in textures:
 if path in tracked:refs.add((D,path))
for n in ['per_piece.json','scene_coverage.json','tally.json','source_scopes.json','glyph_inventory.json']:refs.add((B,(H/n).relative_to(R).as_posix()))
def verify(item):
 rev,path=item;raw=git('show',rev+':'+path);u='https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/'+rev+'/'+path
 with urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Reef-R64-candidate-evidence'}),timeout=60)as q:status=q.status;remote=q.read()
 assert status==200 and remote==raw
 row={'revision':rev,'path':path,'bytes':len(raw),'sha256':sha(raw),'url':u,'http_status':status,'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'role':'Exact source/context/canonical dependency; no approval from inclusion'}
 if path.endswith('.png'):
  im=Image.open(io.BytesIO(raw));row['dimensions']=list(im.size)
 return row
with concurrent.futures.ThreadPoolExecutor(max_workers=6)as pool:refrows=list(pool.map(verify,sorted(refs)))
wr(P/'DELIVERY_SOURCE_REFERENCES.json',{'files':refrows,'required_file_count':len(refrows),'required_bytes':sum(x['bytes']for x in refrows),'access_mode':'Anonymous immutable public HTTPS bytes/length/SHA256','scope':'45before-fixture source/contextrefs retained at original time; all direct final reused/current textures and canonical/frozen dependencies verified here. Parent transitive payload retains its original receipt/time.'})
for n in ['CURRENT_PARTIAL_CONTEXT_UNION.json','CURRENT_CATALOGUE_CONTEXT_UNION.json']:shutil.copyfile(O/n,P/n)
marks=rd(P/'native/attempt1_material_candidate_teardown_locked_1280/capture_manifest.json')['states'][-1]['snapshot']['teardown_marks'];assert len(marks)==2 and all(x['source_tween_valid_before']and not x['source_tween_valid_after']and not x['old_burst_valid_after']and x['source_closed']and not x['wardrobe_block_after']for x in marks)
wr(P/'LIFECYCLE.json',{'source_revision':D,'candidate_checks':219,'source_control_checks':49,'candidate_full_cases':4,'candidate_earlyclose_checks':23,'early_close_marks':marks,'runtime_files':4420,'initialized_sidecars':4041,'normal_save_names':8,'normal_save_access':'Hash-only; no actual child data parsed/copied/seeded. Separate synthetic profile on everyrun.','source_pixels_modified':False,'production_changes':[],'scope':'Ignored candidate class original inherited source choices/save/feedback/touch/close. Same-engine Main reload/application handler notifications/Dummy desktopMobile/Speedy, not freshOS/device/audio/performance/QA11/child/owner evidence.'})
summary={'baseline':B,'source_revision':D,'new_native_files':402,'new_bounded_contexts':231,'new_excluded_diagnostics':171,'passing_native_cases':6,'passing_candidate_cases':5,'final_candidate_cases':4,'passing_checks':268,'passing_candidate_checks':219,'passing_control_checks':49,'failed_cases':2,'failed_case_checks':98,'failed_case_failed_checks':8,'new_alias_credits':0,'known_roles':240,'families':32,'existing_partial_roles':74,'existing_partial_families':15,'catalogue_partial':88,'catalogue_without_current_slice':88,'catalogue_complete':0,'retained_bounded':5559,'retained_excluded':2828,'retained_native_events':8387,'generation_calls':0,'new_drawing_samples':0,'approved':0,'integrated':0,'runtime_verified_replacements':0,'accepted_removed':0,'all_game_artwork_total':None,'distinct_screen_total':None,'regression_total':None,'mission_complete':False}
wr(P/'SUMMARY.json',summary);shutil.copyfile(S/'run_native.py',P/'run_native.py');shutil.copyfile(S/'run_remaining_matrix.py',P/'run_remaining_matrix.py');shutil.copyfile(Path(__file__),P/'assemble_native_evidence.py');print('R64_EVIDENCE_READY',len(refrows),sum(x['candidate']for x in materials),sum(not x['candidate']for x in materials),flush=True)
