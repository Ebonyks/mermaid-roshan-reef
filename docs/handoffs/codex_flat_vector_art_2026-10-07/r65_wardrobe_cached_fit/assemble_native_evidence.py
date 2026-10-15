from pathlib import Path
import json,hashlib,subprocess,datetime,concurrent.futures,urllib.request,io,shutil,re,sys
from PIL import Image
sys.stdout.reconfigure(encoding='utf-8')
R=Path.cwd();H=R/'docs/handoffs/codex_flat_vector_art_2026-10-07';P=H/'r65_wardrobe_cached_fit';O=H/'r64_wardrobe_material_reuse';S=Path(r'C:/Users/Peter/AppData/Local/Temp/reef-flat-vector-wardrobe-cached-fit-20261015');B='6647c56cb0c05f0130557f022abf5d421b4cc871';D='5120b6d59885dd057937aaf284e73681d8eac9f5';REV='FV-AUDIT-20261015-R65'
def rd(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def wr(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(['git',*a],cwd=R,stderr=subprocess.PIPE)
frames=[];cases=[];materials=[];textures=set();cache_epochs=[];retirements=[];diagnostics=[];mode_gaps=[]
def walk(v):
 if isinstance(v,dict):
  for x in v.values():walk(x)
 elif isinstance(v,list):
  for x in v:walk(x)
 elif isinstance(v,str)and v.startswith('res://assets/'):textures.add(v[6:])
for folder in sorted((P/'native').iterdir()):
 m=rd(folder/'capture_manifest.json');launch=rd(folder/'LAUNCH.json');result=rd(folder/'RESULT.json');refined=m['refined_enabled'];adjunct=launch['early_close_adjunct'];counts={'native':len(m['states']),'bounded':0,'excluded':0};epochs={}
 assert result['exit_code']==0 and not m['errors'] and all(x['pass']for x in m['checks'])
 assert not result['source_byte_changes']and not result['script_or_shader_errors']and result['sidecars_exact']and result['fixture_dependencies_unchanged']and result['normal_before']==result['normal_after']==m['normal_before']==m['normal_after']
 assert m['source_revision']==D and refined==launch['refined_candidate']and sha((folder/'engine.log').read_bytes())==result['log_sha256']
 assert m['engine']['hash']=='ed1daf0bf001b61586d9930840f2f1394092c079'and m['renderer']=='mobile'and m['display']=='Windows'and m['time_scale']==1 and m['quality_requested']=='speedy'and not m['actual_child_data']and not m['normal_route_proved']
 assert result['sidecar_before_count']==result['sidecar_after_count']==4041 and len(result['normal_before'])==8
 assert len(list(folder.glob('*.png')))==len(m['states'])
 for name,digest in launch['fixture_dependencies'].items():assert sha((folder/name).read_bytes())==digest==sha((P/name).read_bytes())
 for st in m['states']:
  raw=(folder/st['path']).read_bytes();assert sha(raw)==st['sha256'];im=Image.open(io.BytesIO(raw));im.load();assert list(im.size)==m['aspect']
  excluded=not refined or st['id']in ['main_hall_checkpoint','fresh_main_checkpoint'];classification='EXCLUDED_R64_CANDIDATE_CONTROL'if not refined else'EXCLUDED_DECLARED_BOOTSTRAP'if excluded else'BOUNDED_R65_CACHED_FIT_CANDIDATE';counts['excluded'if excluded else'bounded']+=1
  frames.append({'case':folder.name,'id':st['id'],'path':(folder/st['path']).relative_to(P).as_posix(),'sha256':sha(raw),'bytes':len(raw),'dimensions':list(im.size),'pixel_mode':im.mode,'pixel_sha256':sha(im.tobytes()),'classification':classification,'refined':refined})
  snap=st['snapshot'];walk(snap);assert snap['quality']=='speedy'and snap['time_scale']==1 and snap['r65_refined_enabled']==refined
  fit=snap['r65_fit'];mat=snap['r64_materials']
  if fit['active']:
   assert len(fit['buttons'])==5 and len(mat['panels'])==2 and not mat['ornaments']and mat['heading']['size']=='(430.0, 64.0)'and mat['heading']['line_count']==1
   assert all(p['style']['class']=='StyleBoxTexture'for p in mat['panels'])
   for bt in fit['buttons']:
    assert len(bt['styles'])==6 and bt['pressed_connections']>=1
    assert all(v['class']==('StyleBoxEmpty'if refined else'StyleBoxTexture')for v in bt['styles'].values())
    if bt['name'].startswith('WardrobeLook_'):assert bt['size']=='(480.0, 110.0)'and bt['portrait']['size']=='(96.0, 94.0)'and bt['portrait']['position']=='(10.0, 8.0)'
    else:assert bt['size']==('(330.0, 132.0)'if bt['name']=='WardrobeFinishButton'else'(132.0, 132.0)')
    if refined:
     frame=bt['frame'];assert frame['behind_parent']and frame['mouse_filter']==2 and frame['position']=='(0.0, -7.0)'and frame['style']['class']=='StyleBoxTexture'and frame['style']['region_rect']=='[P: (9.0, 8.0), S: (223.0, 224.0)]'
     wanted='warm'if bt['pressed']or bt['focus']else'hover'if bt['hovered']else'warm'if bt['selected']else'white'
     if frame['mode']!=wanted:mode_gaps.append({'case':folder.name,'id':st['id'],'button':bt['name'],'observed':frame['mode'],'expected_from_sampled_flags':wanted})
   if refined:
    cache=snap['r65_cache'];assert cache['style_creations']==5 and len(set(cache['resource_ids'].values()))==5
    key=cache['resource_ids']['empty'];epochs.setdefault(key,cache['resource_ids']);assert epochs[key]==cache['resource_ids']
    for bt in fit['buttons']:assert all(x['resource_id']==key for x in bt['styles'].values())and bt['frame']['style']['resource_id']==cache['resource_ids'][bt['frame']['mode']]
   materials.append({'case':folder.name,'id':st['id'],'refined':refined,'snapshot_sha256':sha(json.dumps(fit,sort_keys=True).encode()),'button_count':5,'candidate_style_creations':5 if refined else None,'button_style_class':'StyleBoxEmpty'if refined else'StyleBoxTexture'})
  if st['id'].startswith('native_'):diagnostics.append({'case':folder.name,'id':st['id'],'refined':refined,'picker_focus':[b['name']for b in fit['buttons']if b['focus']],'picker_hover':[b['name']for b in fit['buttons']if b['hovered']],'scope':'Native mouse move/Tab events only. No picker focus means focus appearance is unexercised; no direct state writes.'})
 for retired in m['r65_retired_owners']:
  assert not retired['owner_valid_after_3frames'];retirements.append({'case':folder.name,**retired})
 for resources in epochs.values():cache_epochs.append({'case':folder.name,'resource_ids':resources})
 cases.append({'case':folder.name,'manifest':(folder/'capture_manifest.json').relative_to(P).as_posix(),'manifest_sha256':sha((folder/'capture_manifest.json').read_bytes()),'refined':refined,'early_close_adjunct':adjunct,'aspect':m['aspect'],'fairy_unlocked_profile':m['fairy_unlocked_profile'],'checks':len(m['checks']),'counts':counts,'exit_code':0,'fixture_dependencies':launch['fixture_dependencies']})
assert len(cases)==6 and {(x['fairy_unlocked_profile'],x['aspect'][0])for x in cases if x['refined']and not x['early_close_adjunct']}=={(False,1280),(False,1600),(True,1280),(True,1600)}
counts={k:sum(x['counts'][k]for x in cases)for k in ['native','bounded','excluded']};candidate_checks=sum(x['checks']for x in cases if x['refined']);control_checks=sum(x['checks']for x in cases if not x['refined'])
assert counts=={'native':304,'bounded':239,'excluded':65}and(candidate_checks,control_checks)==(225,50)
wr(P/'CAPTURE_INDEX.json',{'revision':REV,'source_revision':D,'cases':cases,'frames':frames,'native_events':counts['native'],'bounded_candidate_contexts':counts['bounded'],'excluded_diagnostics':counts['excluded'],'passing_candidate_checks':candidate_checks,'passing_control_checks':control_checks,'passing_checks':candidate_checks+control_checks,'limits':'Event evidence, not art designs/screens/removals; all R64control56 and declared candidatebootstrap9 excluded. No production or QA11/creative acceptance.'})
wr(P/'FRAME_PIXEL_IDENTITY.json',{'mode':'READ_ONLY_NATIVE_PNG_AND_DECODED_PIXEL_HASHES','edits_to_capture_pixels':0,'rows':[{k:x[k]for k in ['path','sha256','bytes','dimensions','pixel_mode','pixel_sha256']}for x in frames]})
wr(P/'MATERIAL_STATE_IDENTITY.json',{'rows':materials,'active_candidate_states':sum(x['refined']for x in materials),'active_control_states':sum(not x['refined']for x in materials),'cache_epochs':cache_epochs,'mode_gaps':mode_gaps,'native_gui_diagnostics':diagnostics,'limits':'Five shared candidate style resources per owner, stable IDs across sampled refresh/reopen. No total allocation, CPU/GPU/overdraw/FPS, focus/disabled or target device acceptance. Inherited source open still allocates styles/ornaments before replacement.'})
assert not mode_gaps,mode_gaps
refs={(x['revision'],x['path'])for x in rd(P/'SOURCE_REFERENCES.json')['files']};tracked=set(git('ls-tree','-r','--name-only',D,'--','assets').decode().splitlines())
for path in textures:
 if path in tracked:refs.add((D,path))
for n in ['per_piece.json','scene_coverage.json','tally.json','source_scopes.json','glyph_inventory.json']:refs.add((B,(H/n).relative_to(R).as_posix()))
def verify(item):
 rev,path=item;raw=git('show',rev+':'+path);u='https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/'+rev+'/'+path
 with urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Reef-R65-evidence'}),timeout=60)as q:status=q.status;remote=q.read()
 assert status==200 and remote==raw
 row={'revision':rev,'path':path,'bytes':len(raw),'sha256':sha(raw),'url':u,'http_status':status,'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'role':'Exact source/context/canonical dependency; no approval from inclusion'}
 if path.endswith('.png'):row['dimensions']=list(Image.open(io.BytesIO(raw)).size)
 return row
with concurrent.futures.ThreadPoolExecutor(max_workers=6)as pool:refrows=list(pool.map(verify,sorted(refs)))
wr(P/'DELIVERY_SOURCE_REFERENCES.json',{'files':refrows,'required_file_count':len(refrows),'required_bytes':sum(x['bytes']for x in refrows),'access_mode':'Anonymous immutable public HTTPS exactbytes/SHA256','scope':'42beforefixture references retain original times; direct source/current textures/canonical verified here. Historical transitive payload retains prior receipt/time.'})
for n in ['CURRENT_PARTIAL_CONTEXT_UNION.json','CURRENT_CATALOGUE_CONTEXT_UNION.json']:shutil.copyfile(O/n,P/n)
early=next(x for x in cases if x['early_close_adjunct']);earlym=rd(P/early['manifest']);marks=earlym['states'][-1]['snapshot']['teardown_marks'];assert len(marks)==2 and all(len(x['owned_frame_ids'])==5 and not x['surviving_frame_ids_after_12frames']and not x['source_tween_valid_after']and x['source_closed']and not x['old_burst_valid_after']and not x['wardrobe_block_after']for x in marks)
wr(P/'LIFECYCLE.json',{'source_revision':D,'candidate_checks':candidate_checks,'control_checks':control_checks,'early_close_marks':marks,'retired_owner_observations':retirements,'cache_epochs':cache_epochs,'runtime_files':4420,'initialized_sidecars':4041,'normal_save_names':8,'normal_save_access':'Hash-only; no actual child data copied/read/seeded. Synthetic private profiles only.','production_changes':[],'scope':'Observed original-input disposal of five frame nodes at Back/Done and weak owner lifetime after same-engine retirement. Not a global leak/profile/performance proof, freshOS or physical device evidence.'})
source=(P/'wardrobe_cached_fit_candidate.gd').read_text(encoding='utf-8');original=git('show',D+':scripts/wardrobe_ui.gd').decode('utf-8');refresh=original.split('func _wardrobe_refresh()')[1].split('\nfunc ')[0];candidate=source.split('func _wardrobe_refresh()')[1].split('\nfunc ')[0]
start=refresh.index('\t\tStorybookUI.style_picture_button(');end=refresh.index('\t\tbt.alignment',start);helper=candidate[candidate.index('\t\t# Preserve all typography'):candidate.index('\t\tbt.alignment')];normalized=candidate.replace('\t_r65_source_refreshes += 1\n','').replace(helper,refresh[start:end]).replace('\t_paint_picker_buttons()\n','');assert normalized.strip()==refresh.strip()
wr(P/'FIXTURE_LINEAGE.json',{'baseline':B,'source_revision':D,'base_capture_identical_to_R64':(P/'base_capture.gd').read_bytes()==(O/'base_capture.gd').read_bytes(),'previous_owner_exact_published_R64':(P/'wardrobe_previous_candidate.gd').read_bytes()==(O/'wardrobe_material_candidate.gd').read_bytes(),'current_source_refresh_preserved_except_declared_style_helper':True,'removed_helper_nonstyle_effects_retained':['typography role/size','font_hover_pressed_color','storybook_kind','picture_first','touch_target'],'candidate_methods':re.findall(r'^func (\w+)\(',source,re.M),'inherited_unmodified_behavior':['pick','apply_skin','skin_sprite_path','feedback','done','close','toast','open_shell'],'source_png_edits':0,'generation_calls':0,'accepted_removed':0,'candidate_script_sha256':sha((P/'wardrobe_cached_fit_candidate.gd').read_bytes()),'scope':'Mechanical refresh style allocation substitution plus cache/owned frame and prior R64open body. Original pressed connections, private profiles, choices, save keys and behavior assertions retained. Native mouse/Tab diagnosis added; no direct flag writes.'})
summary={'baseline':B,'source_revision':D,'new_native_files':304,'new_bounded_contexts':239,'new_excluded_diagnostics':65,'passing_native_cases':6,'passing_candidate_cases':5,'final_candidate_cases':4,'passing_checks':275,'passing_candidate_checks':225,'passing_control_checks':50,'failed_cases':0,'new_alias_credits':0,'known_roles':240,'families':32,'existing_partial_roles':74,'existing_partial_families':15,'catalogue_partial':88,'catalogue_without_current_slice':88,'catalogue_complete':0,'retained_bounded':5798,'retained_excluded':2893,'retained_native_events':8691,'generation_calls':0,'new_drawing_samples':0,'approved':0,'integrated':0,'runtime_verified_replacements':0,'accepted_removed':0,'all_game_artwork_total':None,'distinct_screen_total':None,'regression_total':None,'mission_complete':False};wr(P/'SUMMARY.json',summary)
for n in ['run_native.py','run_remaining_matrix.py','build_fixture.py','build_candidate.py']:shutil.copyfile(S/n,P/n)
shutil.copyfile(Path(__file__),P/'assemble_native_evidence.py');print('R65_EVIDENCE_READY',counts,candidate_checks,control_checks,'refs',len(refrows),'active',sum(x['refined']for x in materials),sum(not x['refined']for x in materials),flush=True)
