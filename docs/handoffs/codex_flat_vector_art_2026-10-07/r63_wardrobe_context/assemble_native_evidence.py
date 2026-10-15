from pathlib import Path
import json,hashlib,subprocess,datetime,urllib.request,concurrent.futures,io,re,shutil
from PIL import Image
R=Path.cwd();H=R/'docs/handoffs/codex_flat_vector_art_2026-10-07';P=H/'r63_wardrobe_context';O=H/'r62_catalogue_origin';S=Path(r'C:/Users/Peter/AppData/Local/Temp/reef-flat-vector-wardrobe-context-20261015');B='db43af9e46f0b7f718225ffc03dd40206b8cc2de';D='5120b6d59885dd057937aaf284e73681d8eac9f5';REV='FV-AUDIT-20261015-R63'
def rd(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def wr(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(['git',*a],cwd=R,stderr=subprocess.PIPE)
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
for n in ['run_native.py','run_teardown.py']:
 shutil.copyfile(S/n,P/n)
# Every event remains an event: none is a unique-screen or accepted-art count.
cases=[];frames=[];textures=set()
def walk(v):
 if isinstance(v,dict):
  for x in v.values():walk(x)
 elif isinstance(v,list):
  for x in v:walk(x)
 elif isinstance(v,str) and v.startswith('res://') and v.endswith('.png'):textures.add(v[6:])
for folder in sorted((P/'native').iterdir()):
 m=rd(folder/'capture_manifest.json');result=rd(folder/'RESULT.json');launch=rd(folder/'LAUNCH.json');failed=result['exit_code']!=0
 assert not result['timed_out'] and not result['script_or_shader_errors'] and not result['source_byte_changes'] and result['normal_before']==result['normal_after'] and result['sidecars_exact'] and result['fixture_unchanged']
 assert result['log_sha256']==sha((folder/'engine.log').read_bytes());assert len(list(folder.glob('*.png')))==len(m['states'])
 counts={'native':len(m['states']),'bounded':0,'excluded':0}
 for st in m['states']:
  f=folder/Path(st['path']).name;b=f.read_bytes();assert sha(b)==st['sha256'];im=Image.open(io.BytesIO(b));im.load();assert list(im.size)==m['aspect']
  excluded=failed or st['id'] in ['main_hall_checkpoint','fresh_main_checkpoint'];counts['excluded' if excluded else 'bounded']+=1
  frames.append({'case':folder.name,'id':st['id'],'path':f.relative_to(P).as_posix(),'sha256':sha(b),'bytes':len(b),'dimensions':list(im.size),'pixel_mode':im.mode,'pixel_sha256':sha(im.tobytes()),'role':st['role'],'classification':'EXCLUDED_FIXTURE_READER_RUN' if failed else 'EXCLUDED_DECLARED_BOOTSTRAP' if excluded else 'BOUNDED_CURRENT_ORIGINAL_CONTEXT'})
  walk(st['snapshot'])
 cases.append({'case':folder.name,'manifest':(folder/'capture_manifest.json').relative_to(P).as_posix(),'manifest_sha256':sha((folder/'capture_manifest.json').read_bytes()),'launch':(folder/'LAUNCH.json').relative_to(P).as_posix(),'result':(folder/'RESULT.json').relative_to(P).as_posix(),'fixture_sha256':sha((folder/'fixture_source.gd').read_bytes()),'aspect':m['aspect'],'fairy_unlocked_profile':m['fairy_unlocked_profile'],'checks':len(m['checks']),'failed_checks':[x['label'] for x in m['checks'] if not x['pass']],'exit_code':result['exit_code'],'counts':counts,'scope':'Excluded whole first reader-error run' if failed else 'Original full-skin native inputs; earlyclose adjunct only' if 'teardown' in folder.name else 'Original full-skin native inputs plus same-engine reload and Fashion entry/Back only'})
assert len(cases)==6 and sum(x['counts']['native'] for x in cases)==294 and sum(x['counts']['bounded'] for x in cases)==231 and sum(x['counts']['excluded'] for x in cases)==63
assert sum(x['checks'] for x in cases if x['exit_code']==0)==147 and all(not x['failed_checks'] for x in cases if x['exit_code']==0)
wr(P/'CAPTURE_INDEX.json',{'revision':REV,'source_revision':D,'cases':cases,'frames':frames,'native_events':294,'bounded_contexts':231,'excluded_diagnostics':63,'passing_cases':5,'passing_checks':147,'limits':'4full matrix54frames33checks each;24frame15check earlyclose adjunct;54first reader-error frames excluded,9declared bootstrap/reload frames excluded. Repeated events/instances are not unique screens/designs/removals.'})
wr(P/'FRAME_PIXEL_IDENTITY.json',{'mode':'READ_ONLY_ORIGINAL_NATIVE_PNG_BYTES_AND_DECODED_PIXELS','image_edits':0,'rows':[{k:x[k] for k in ['path','sha256','bytes','dimensions','pixel_mode','pixel_sha256']} for x in frames]})
# All direct exact current art/caller dependencies are anonymously reverified; source refs before fixture stay immutable.
refs={(x['revision'],x['path']):x for x in rd(P/'SOURCE_REFERENCES.json')['files']}
for x in rd(O/'CATALOGUE_ORIGINS.json')['rows']:
 if x['id'] in ['game.wardrobe','game.pearl_castle']:
  for path in x.get('declared_sources',[])+x.get('declared_hosts',[]):refs.setdefault((D,path),None)
for path in textures:refs.setdefault((D,path),None)
for n in ['CATALOGUE_ORIGINS.json','CURRENT_CATALOGUE_CONTEXT_UNION.json','CURRENT_PARTIAL_CONTEXT_UNION.json']:
 refs.setdefault((B,(O/n).relative_to(R).as_posix()),None)
for path in ['AGENTS.md','audit/MASTER_AUDIT_2026-08-09.md','design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md','audit/findings/ACTIVE_FINDINGS_2026-08-13.md','design/05_DOC_LEDGER.md','design/AUDIT_DEVELOPMENT_CONTRACT.md']:
 refs.setdefault((B,path),None)
def verify(key):
 rev,path=key;b=git('show',rev+':'+path);u='https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/'+rev+'/'+path
 with urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Reef-R63-audit-evidence'}),timeout=60) as q:status=q.status;remote=q.read()
 assert status==200 and remote==b,(rev,path)
 d={'revision':rev,'path':path,'bytes':len(b),'sha256':sha(b),'url':u,'http_status':status,'checked_at_utc':now(),'role':'Exact current source/same-scene or immutable canonical dependency; source inclusion grants no new-use acceptance'}
 if path.endswith('.png'):
  im=Image.open(io.BytesIO(b));d['dimensions']=list(im.size);d['mode']=im.mode
 return d
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:allrefs=list(pool.map(verify,sorted(refs)))
wr(P/'DELIVERY_SOURCE_REFERENCES.json',{'status':'EXACT_ANONYMOUS_HTTP200_BYTES_SHA256','files':allrefs,'required_file_count':len(allrefs),'required_bytes':sum(x['bytes'] for x in allrefs),'initial_prerequisite':'SOURCE_REFERENCES.json and CONTEXT_PREREQUISITE.json retain exact before-fixture45refs/time. Later current source/texture refs verified here; no historical transitive re-review.'})
# Record explicit consumers and exact function bodies as evidence, without claiming graph exhaustion.
functions={'scripts/wardrobe_ui.gd':['_open_wardrobe_shell','_open_wardrobe','_wardrobe_refresh','_wardrobe_pick','_wardrobe_feedback_burst','_wardrobe_done','_wardrobe_toast','_close_wardrobe','_apply_skin','skin_sprite_path'],'scripts/main.gd':['_wardrobe_ref','_open_wardrobe'],'scripts/arena/castle_rooms_25d.gd':['_activate_room_item','_open_roleplay_wardrobe','_finish_open_roleplay_wardrobe','_enter_gallery_room'],'scripts/fashion_wardrobe.gd':['open']}
slices=[]
for path,names in functions.items():
 b=git('show',D+':'+path);s=b.decode('utf-8-sig');matches=list(re.finditer(r'^func\s+([A-Za-z_][A-Za-z_0-9]*)\(',s,re.M))
 for name in names:
  hit=next((i for i,x in enumerate(matches) if x.group(1)==name),None)
  assert hit is not None,(path,name)
  m=matches[hit];end=matches[hit+1].start() if hit+1<len(matches) else len(s);body=s[m.start():end]
  slices.append({'revision':D,'path':path,'source_sha256':sha(b),'function':name,'line':s[:m.start()].count('\n')+1,'body':body,'body_sha256':sha(body.encode())})
wr(P/'SOURCE_CALLER_BINDINGS.json',{'revision':REV,'source_revision':D,'functions':slices,'route':'Declared private originalSaveState beforeMain + actual Continue, private Castle bootstrap; original HallDoor_family_gallery -> gallery_royal_bedroom_door -> current shell_wardrobe roleplay dress_up with native_pack empty/source glint -> Main._open_wardrobe -> WardrobeUI original shell/picker. Native touch original Button callbacks; no direct callback emission.','fallback_limits':'Current loaded texture paths and original callbacks only; missing texture, native override/value domains, all callers/resources/ordinary launch/full routes and other Fashion variants remain open.','functional_geometry':'Touch rectangles, target positions, player foot and control blocking are invisible functional geometry, separately retained; no visible-flat exemption inferred.'})
orig=rd(O/'CATALOGUE_ORIGINS.json');games=json.loads(git('show',D+':design/reference/games.json'));bindings=[]
for name in ['wardrobe','pearl_castle']:
 row=next(x for x in games['games'] if x['id']==name);origin=next(x for x in orig['rows'] if x['id']=='game.'+name)
 assert row['name']==origin['declared_name'] and row['sources']==origin['declared_sources'] and row['host']==origin['declared_hosts']
 bindings.append({'id':'game.'+name,'original_origin':origin,'current_catalogue_row':row,'current_catalogue_sha256':next(x['sha256'] for x in allrefs if x['revision']==D and x['path']=='design/reference/games.json'),'native_cases':[x['case'] for x in cases if x['exit_code']==0],'proved_partial_subset':'Original full-skin Wardrobe consumer from actual Royal Bedroom item, locked/unlocked selections, feedback, save/reload/close and Fashion entry only' if name=='wardrobe' else 'Original CastleRooms MainHall/DreamHouseWing/RoyalBedroom interior subset reached after declared private Castle bootstrap, with source props/door/UI item; no courtyard/lagoon/ordinary launch/full-room route claim','accepted_removed':0,'complete':False})
prior=rd(O/'CURRENT_CATALOGUE_CONTEXT_UNION.json');new=['game.pearl_castle','game.wardrobe'];assert not set(new)&set(prior['current_partial_ids']);ids=sorted(prior['current_partial_ids']+new);assert len(ids)==88
wr(P/'CATALOGUE_BINDINGS.json',{'revision':REV,'bindings':bindings,'retained_overlapping_ids':['ui.wardrobe','overlay.wardrobe'],'standalone.main':'Not credited: private bootstrap does not prove unforced project-entry path.','no_historical_score_refresh':True,'no_unique_screen_or_art_credit':True})
union=dict(prior);union.update(prior_revision=B,prior_partial_ids=prior['current_partial_ids'],new_partial_ids=new,new_evidence='CATALOGUE_BINDINGS.json and SOURCE_CALLER_BINDINGS.json + original source-input matrix. Existing ui.wardrobe/overlay.wardrobe retained, not merged.',current_partial_ids=ids,current_partial_count=88,without_current_slice_count=88,new_native_files=294)
wr(P/'CURRENT_CATALOGUE_CONTEXT_UNION.json',union);shutil.copyfile(O/'CURRENT_PARTIAL_CONTEXT_UNION.json',P/'CURRENT_PARTIAL_CONTEXT_UNION.json')
# All facts derived from native events; no synthetic creative/owner acceptance.
marks=rd(P/'native/attempt1_wardrobe_teardown_locked_1280/capture_manifest.json')['states'][-1]['snapshot']['teardown_marks']
assert len(marks)==2 and all(x['source_tween_valid_before'] and not x['source_tween_valid_after'] and not x['old_burst_valid_after'] and x['source_closed'] and not x['wardrobe_block_after'] for x in marks)
wr(P/'LIFECYCLE.json',{'source_revision':D,'full_matrix_checks':132,'early_close_checks':15,'early_close_marks':marks,'case_records':cases,'normal_save_access':'8names hash-only; actual child data never parsed/copied/seeded','runtime_file_count':4420,'initialized_sidecar_count':4041,'source_byte_changes':[],'native_scope':'Exact approved4.7.2 Windows Forward Mobile, actualSpeedy,time1,Dummy audio/maxfps30. Private originalSaveState; same-engine freshMain reload/application notifications, not fresh OS/real platform pause/QA11/device performance/audio/child/owner.','historical_import_limit':'R51 historical1102trackedLFCRLF rewrites restored/2043ignored created; current4041before/after exact. No claim of zero historical import writes.'})
wr(P/'SOURCE_PARITY.json',{'baseline':B,'source_revision':D,'source_before_after_guards':[{'case':x['case'],'result':x['result'],'runtime_files':4420,'sidecars':4041,'normal_names':8} for x in cases],'historical_helper_source':'R55capture_comfy.gd at immutableB;20helper bodies copied, _go_room RoyalBedroom branch extension and read-only_disk skin/fairyskin additions declared. First54frames reader-error retained/excluded. No production change.','current_fixture_sha256':sha((P/'capture_wardrobe.gd').read_bytes()),'teardown_fixture_sha256':sha((P/'capture_teardown.gd').read_bytes()),'frozen5':[{'path':(H/n).relative_to(R).as_posix(),'sha256':sha(git('show',B+':'+(H/n).relative_to(R).as_posix()))} for n in ['per_piece.json','scene_coverage.json','tally.json','source_scopes.json','glyph_inventory.json']]})
print('R63_ASSEMBLED_NATIVE_AND_SOURCE',len(allrefs),len(frames),len(slices),flush=True)
