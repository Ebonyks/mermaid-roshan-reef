from pathlib import Path
import copy,datetime,hashlib,html,json,shutil
b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');f=b/'audit/job_geode_current_recheck_v1_20261002';live=b/'audit/job_artwork_refinement_live';prefix=f.relative_to(b).as_posix()
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
now=datetime.datetime.now(datetime.timezone.utc).isoformat();snap=read(f/'SOURCE_CURRENT_BEFORE_CAPTURE.json')['source_files'];assert len(snap)==783 and all(sha(b/x['path'])==x['sha256'] for x in snap)
old=read(b/'audit/job_geode_supported_celebration_v1_20261002/REVIEW.json');opinions=copy.deepcopy(old['individual_objects'])
for x in opinions:
 x.update(reviewed_utc=now,qualification='Fresh direct current desktop canvas/ordered-frame drafting opinion. Every selected still was inspected on a complete-canvas board; every captured geode opening/celebration/return frame was inspected. Selected fine details separately inspected at native size. Other phases have selected stills, not complete timed-motion review. Device, child and owner acceptance remain open.',prior_review='audit/job_geode_supported_celebration_v1_20261002/REVIEW.json')
 x['evaluation']=x['evaluation'].replace('The former unsupported4.2 placement is replaced.','This fresh replay confirms the earlier supported placement remains intact.').replace('Every recorded occurrence in both-width sequences was inspected.','Every occurrence in this fresh two-width sequence was inspected.')
opinions.extend([
 dict(id='GEO-RIVER-MOUNT',name='Painted excavated river and earth',score=4.5,artwork_score=4.6,priority=True,evaluation='The cyan water and pebble lips read clearly against the warm painted earth at the selected start and earned endpoints. The angular connected route retains hard turns; no direct hand contact exists. This selected-state opinion does not approve every intervening excavation frame.',refinement='Retain painted material and conserved connected-path mechanics; review all timed excavation frames and replace remote work contact.',owner_acceptance=None,reviewed_utc=now),
 dict(id='GEO-BRUSH-MOUNT',name='Fossil brush material and placement',score=4.5,artwork_score=4.5,priority=True,evaluation='The broad aqua bristles, lilac wrap and golden handle have a readable storybook silhouette. The brush floats above the work away from Roshan; its painting does not establish a grip or meaningful sweeping action.',refinement='Keep this brush source; connect an approved working grip and inspect each contact/clearing transition.',owner_acceptance=None,reviewed_utc=now)
])
views=[];frames=[];states={};checks=[];boards=read(f/'QA_BOARD_MANIFEST_V1.json')['boards']
for board in boards:
 assert sha(b/board['path'])==board['sha256'];board.update(direct_review=True,reviewed_utc=now)
for width in [1280,1600]:
 cap=read(f/f'attempt01/CAPTURE_{width}.json');states[str(width)]={str(i):[] for i in range(7)}
 for v in cap['views']:
  assert sha(b/v['path'])==v['sha256'];v=copy.deepcopy(v);v.update(direct_review=True,reviewed_utc=now,review_method='Whole native canvas inspected on complete-canvas ordered board; specified fine details additionally inspected at native size. Raw capture manifest retained unchanged.')
  views.append(v)
 for row in cap['motion_frames']:
  assert sha(b/row['path'])==row['sha256'];x=copy.deepcopy(row)
  if not x['act_active']:lane='earned_library_return';scores=dict(library_material=4.6,caption_clearance=4.0)
  elif x['celebration_stage']:
   lane='supported_celebration';scores=dict(rooted_crystals=4.6,specimen_mounting=4.5,support_material=4.6,support_mounting=4.5,whole_stage=4.1)
   assert x['goal_anchor']=='painted_geology_display_slab';checks.append(dict(width=width,index=x['index'],position=x['goal_position'],size=x['goal_size'],anchor=x['goal_anchor']))
  else:
   lane='opening_and_completion_hold';scores=dict(rooted_crystals=4.6,opening_progression=4.5,hand_contact=2.7,room_context=2.8,work_to_clap=4.0)
   pull=float(x['surface'].get('pull',0));state=0 if pull<=0 else min(6,1+int(pull/20));states[str(width)][str(state)].append(x['index']);x['observed_authored_state']=state
  x.update(direct_review=True,reviewed_utc=now,review_lane=lane,scores=scores,review_method='Every consecutive frame inspected in row-major complete-canvas ordered boards; selected native details separately inspected.',owner_acceptance=None);frames.append(x)
 for state,occurrences in states[str(width)].items():assert occurrences,(width,state)
 local=[x for x in checks if x['width']==width];assert local and len({x['position'] for x in local})==len({x['size'] for x in local})==1
details=[]
for width,indices in [(1280,[0,2,18,32,42,58,74,112,142]),(1600,[0,74,108])]:
 for n in indices:details.append(prefix+f'/attempt01/native_frames/geode_{width}_{n:04d}.webp')
for width,names in [(1280,['phase0_earned_completion','phase1_partial_brush','phase1_two_pieces','phase2_pan_left','phase2_earned_completion','actual_earned_library_return']),(1600,['phase1_one_piece','phase1_brushed','phase2_pan_right','phase3_invitation','actual_elevator_menu','actual_earned_library_return'])]:
 for name in names:details.append(prefix+f'/attempt01/native_views/geologist_{width}_{name}.webp')
assert len(views)==58 and len(frames)==318 and len(boards)==37 and len(details)==24
def preview(x):
 id=x['id'];name='phase3_full_interior_before_award'
 if id.startswith('GEO-OPEN-STATE-'):return prefix+f'/attempt01/native_frames/geode_1280_{[0,2,18,32,42,58,74][int(id[-1])]:04d}.webp'
 if id in ['GEO-USE-LIBRARY','GEO-LIBRARY-ART']:name='normal_library_card'
 elif id=='GEO-USE-DEV-MENU':name='actual_elevator_menu'
 elif id in ['GEO-USE-INVITATION','GEO-ROOM','GEO-FLAT-FOSSIL','GEO-TRAYS','GEO-HALO']:name='phase3_invitation'
 elif id=='GEO-RETURN-CAPTION':name='actual_earned_library_return'
 elif id=='GEO-FOSSIL-CLEARING':name='phase1_two_pieces'
 elif id=='GEO-PAN-ACTION':name='phase2_pan_left'
 elif id=='GEO-RIVER-MOUNT':name='phase0_earned_completion'
 elif id=='GEO-BRUSH-MOUNT':name='phase1_partial_brush'
 elif id in ['GEO-USE-CELEBRATION','GEO-USE-SUPPORT','GEO-CELEBRATION-CONTEXT']:return prefix+'/attempt01/native_frames/geode_1280_0112.webp'
 elif id=='GEO-CLAP':name='phase3_earned_completion'
 return prefix+'/attempt01/native_views/geologist_1280_'+name+'.webp'
for x in opinions:x['native_preview']=preview(x)
receipt=b/'audit/job_nursery_wash_connected_v1_20261002/full_ci_v1/RECEIPT.json';assert receipt.is_file()
review=dict(status='CURRENT_GEODE_ALL58_SELECTED_CANVASES_AND318_CAPTURED_FRAMES_DIRECTLY_REVIEWED',reviewed_utc=now,baseline='c2538760639d79b063152ce5530807c04545ba6e',source_files=snap,views=views,frames=frames,boards=boards,individual_objects=opinions,native_details=[dict(path=p,sha256=sha(b/p),direct_review=True) for p in details],authored_state_occurrences=states,stable_celebration_geometry=checks,counts=dict(views=58,frames=318,boards=37,native_details=24,individual_opinions=len(opinions),inclusive_priorities=sum(x['priority'] for x in opinions)),owner_acceptance=None,qualification='Actual Library card and ordinary all-four-phase viewport inputs earn the Library return, then actual Opera elevator developer entry and Back. Isolated entry/save fixtures remain explicit. No separate ChapterTwo story set or two-act Geologist rollout exists. Selected river/fossil/pan states are reviewed, their complete timed action sequences remain open. Native readback is not device FPS. Global audit, strict 2D debt, device, child, owner, integration, release and comprehensive all-job approval remain open.',machine_evidence='audit/job_nursery_wash_connected_v1_20261002/full_ci_v1/RECEIPT.json',machine_qualification='Previously completed current official Godot4.7.2 unmodified82/82 suite on the same783 literal production/machine boundary. Every byte rechecked unchanged before/after these captures. All53 raw diagnostics remain retained; current additional non-runtime fixture separately passes parser/inference/analyzer. No production changes or transferred creative acceptance.')
write(f/'DIRECT_REVIEW.json',review)
write(f/'BOUNDARY_AFTER_DIRECT_REVIEW.json',dict(status='ALL783_LITERAL_SOURCE_MEMBERS_UNCHANGED',source_files=snap,checked_utc=now))
esc=html.escape
def image_block(path,caption):
 rel=Path(path).relative_to(f.relative_to(b)).as_posix();return f'<figure><a href="{esc(rel)}"><img loading="lazy" width="1280" height="720" src="{esc(rel)}" alt="{esc(caption)}"></a><figcaption>{esc(caption)}</figcaption></figure>'
cards=''.join(f'<article id="{esc(x["id"])}"><h2>{esc(x["id"])} · {esc(x["name"])}</h2><p><strong>Current use / relationship {x["score"]}/5</strong> · material {str(x["artwork_score"])+"/5" if x["artwork_score"] is not None else "separate / unassigned"} · {"refinement priority" if x["priority"] else "retain provisionally"}</p>{image_block(x["native_preview"],x["name"])}<p>{esc(x["evaluation"])}</p><p>Refinement: {esc(x["refinement"])}</p></article>' for x in opinions)
galleries=''.join('<details><summary>'+str(width)+'px · '+kind+' · every declared member</summary>'+''.join(image_block(x['path'],f'{width} {kind}: {x["first"]}–{x["last"]}, row-major ({x["count"]} images)') for x in boards if x['width']==width and x['kind']==kind)+'</details>' for width in [1280,1600] for kind in ['views','motion_frames'])
native=''.join(f'<li><a href="{esc(Path(x["path"]).relative_to(f.relative_to(b)).as_posix())}">{esc(Path(x["path"]).name)}</a> · {esc(x["sha256"])}</li>' for x in views+frames)
page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Current Geologist — rooted crystals and complete route recheck</title><style>body{background:#eef5fb;color:#26304a;font:18px/1.55 system-ui;margin:0}main{max-width:1250px;margin:auto;padding:24px}article,header,details{background:white;padding:24px;margin:22px 0;border-radius:16px}img{width:100%;height:auto;display:block}figure{margin:16px 0}a{color:#51418c}code{overflow-wrap:anywhere}h1,h2{line-height:1.25}figcaption{font-size:14px}li{overflow-wrap:anywhere;font-size:13px}</style><main><header><a href="../job_artwork_refinement_live/all_items.html">All-item review library</a><h1>Current Geologist: crystals stay inside the opened stone</h1><p>Fresh current replay after the shared Nursery renderer change. The same painted stone opens around rooted cyan/violet crystal groups and stays on its slab through the earned celebration. Opening and specimen/support mounting score4.5 provisionally; rooted material4.6. Whole stage4.1, room2.8, hands/work contact2.7, fossil clearing3.9 and panning action3.8 remain weaknesses.</p><p>All58 selected complete native canvases and all318 consecutive opening/celebration/earned-return frames at1280/1600 inspected on37 complete ordered boards;24 fine details additionally inspected at native size. The four ordinary tasks are earned through the actual Library caller. Actual Opera elevator and developer Geologist entry/Back are included. Other task animations still need their own complete timed captures. This is not a Geologist birthday story route.</p><p>No artwork or production code changed in this recheck. All783 current source bytes remain unchanged; official Godot4.7.2 local full suite82/82 remains the scoped machine evidence, with53 raw diagnostics retained. This does not approve visuals, target-device performance, child/owner acceptance, integration or release.</p><p><a href="DIRECT_REVIEW.json">Written evaluations and every frame record</a> · <a href="SOURCE_CURRENT_BEFORE_CAPTURE.json">Literal source boundary</a> · <a href="../job_geode_supported_celebration_v1_20261002/index.html">Preserved previous review and rejected room trial</a> · <a href="../job_nursery_wash_connected_v1_20261002/remote_verified_v1/index.html">Published Nursery checkpoint remote verification</a></p></header>'''+cards+galleries+'<details><summary>All376 unchanged native originals and SHA-256</summary><ol>'+native+'</ol></details><details><summary>24 additionally inspected full native details</summary>'+''.join(image_block(p,Path(p).name+' — original native detail') for p in details)+'</details><p>Inclusive4.5 refinement remains visible even when the required4.5 drafting floor is met. Originals and earlier failures stay preserved. Owner acceptance remains pending.</p></main></html>'
(f/'index.html').write_text(page,encoding='utf-8',newline='\n')
# Freeze the exact prior registry/display/refresh before replacing current claims.
history=live/'history_v34_1_before_current_geode';history.mkdir(exist_ok=False)
for name in ['ALL_ITEMS.json','all_items.html','CURRENT_BOUNDARY_REFRESH.json']:
 shutil.copyfile(live/name,history/(name+'.original'))
registry=read(live/'ALL_ITEMS.json');known={x['id']:x for x in registry['items']}
for opinion in opinions:
 id=opinion['id'];p=opinion['native_preview']
 if id in known:
  x=known[id];x.setdefault('mounted_review_history',[]).append({k:copy.deepcopy(x.get(k)) for k in ['current_mounted_score','current_source_score','evaluation','refinement','current_capture_review','current_reviewed_utc','binding_sha256','image_path','image_scope']})
 else:
  x=dict(id=id,aliases=[id],kind='runtime use/action',path=p,source_dimensions=[1280,720],earlier_sha256=sha(b/p),historical_source_score=None,current_source_score=None,families=['Geologist','Current actual Library / Opera caller'],original_reports=[],native_reference_observations=[],current_checkout_sha256=sha(b/p),current_byte_status='EXACT_CURRENT_CAPTURE',protected_original=False,current_mounted_score=None,current_complete_action_score=None,owner_acceptance=None);registry['items'].append(x)
 x.update(evaluation=opinion['evaluation'],refinement=opinion['refinement'],current_mounted_score=opinion['score'],capture_family='geode_current_v1',current_capture_review=prefix+'/DIRECT_REVIEW.json',current_reviewed_utc=now,priority=opinion['priority'],image_path=p,image_scope='Fresh actual complete native gameplay canvas; use/action opinion is separate from material and source acceptance.',source_qualification=opinion.get('qualification',review['qualification']),latest_refinement=dict(report=prefix+'/index.html#'+id,note=opinion['evaluation']))
 if id in ['GEO-CONTACT','GEO-CLAP','GEO-PAN-ACTION','GEO-FOSSIL-CLEARING']:x['current_complete_action_score']=opinion['score']
 if x.get('current_binding'):x['binding_sha256']=sha(b/x['current_binding'])
 x['original_reports'].append(prefix+'/index.html#'+id)
registry['counts']['additional_runtime_prop_regions']=sum(x['kind'] not in ['source','pose cell','source object region'] for x in registry['items'])
registry['counts']['registered_items']=len(registry['items']);registry['counts']['current_geode_mounted_priorities']=sum(x.get('capture_family')=='geode_current_v1' and x['priority'] for x in registry['items'])
assert len(registry['items'])==1778 and registry['counts']['additional_runtime_prop_regions']==85 and registry['counts']['current_geode_mounted_priorities']==23
registry.update(display_revision='V35_CURRENT_GEODE_RECHECK',created_utc=now,refresh_command='python -B audit/job_artwork_refinement_live/review_tools/refresh_current_job_review_v35.py');write(live/'ALL_ITEMS.json',registry)
s=(live/'all_items.html').read_text();s=s.replace('refresh_current_job_review_v34.py','refresh_current_job_review_v35.py')
s=s.replace("q.capture_family==='nursery_wash_v3'?q.current_mounted_score:q.current_source_score","['nursery_wash_v3','geode_current_v1'].includes(q.capture_family)?q.current_mounted_score:q.current_source_score")
s=s.replace("const scoreLabel=q=>q.capture_family==='nursery_wash_v3'?","const scoreLabel=q=>q.capture_family==='geode_current_v1'?'Current mounted use / action':q.capture_family==='nursery_wash_v3'?")
s=s.replace("q.id.startsWith('GEO-USE-')&&!stamp.geode_capture_boundary_match","q.capture_family==='geode_current_v1'&&!stamp.geode_capture_boundary_match")
s=s.replace("!q.id.startsWith('GEO-USE-')&&q.capture_family!=='nursery_wash_v3'","q.capture_family!=='geode_current_v1'&&q.capture_family!=='nursery_wash_v3'")
s=s.replace("q.id.startsWith('GEO-USE-')&&q.current_mounted_score!=null","q.capture_family==='geode_current_v1'&&q.current_mounted_score!=null")
s=s.replace('runtime prop regions +','runtime prop/use/action entries +').replace('current geode mounted priorities','current Geologist state/use/action priorities')
at=s.index('</header>');s=s[:at]+f'<p><a href="../job_geode_current_recheck_v1_20261002/index.html">Fresh current Geologist review: all58 selected canvases/318 opening-to-return frames;27 individual opinions</a>.23 inclusive state/use/action priorities remain; flat room2.8/contact2.7 are not approved by the improved geode.</p>'+s[at:];(live/'all_items.html').write_text(s,encoding='utf-8',newline='\n')
refresh=(live/'review_tools/refresh_current_job_review_v34.py').read_text().replace("audit/job_geode_supported_celebration_v1_20261002","audit/job_geode_current_recheck_v1_20261002").replace("SOURCE_CURRENT_BEFORE_CAPTURES.json","SOURCE_CURRENT_BEFORE_CAPTURE.json")
refresh=refresh.replace("geode_capture_source_count=len(boundary)","geode_review='audit/job_geode_current_recheck_v1_20261002/DIRECT_REVIEW.json',geode_capture_source_count=len(boundary)")
(live/'review_tools/refresh_current_job_review_v35.py').write_text(refresh,encoding='utf-8',newline='\n')
# Ledger authority of the old mounted report changes; preserve its exact old row.
lp=b/'design/05_DOC_LEDGER.md';s=lp.read_text();rows=[line for line in s.splitlines() if line.startswith('| `audit/job_geode_supported_celebration_v1_20261002/')];write(f/'PREVIOUS_LEDGER_ROWS.json',dict(rows=rows,reason='Current mounted source boundary now freshly reviewed in separate current report. Old report unchanged and retained as historical evidence.'))
for row in rows:s=s.replace(row,row.replace('SUPPORTING_CURRENT','SUPPORTING_HISTORICAL'))
s+='\n| `audit/job_geode_current_recheck_v1_20261002/index.html` | 🔵 | `SUPPORTING_CURRENT`: fresh unchanged-source actual Library all-four-phase route and earned return/Opera elevator developer entry;58 selected canvases and318 consecutive geode frames on37 boards plus24 native details directly reviewed.27 individual opinions: opening/mounting4.5, rooted material4.6;23 inclusive priorities include room2.8/contact2.7/clearing3.9/pan3.8. V35 library1778 entries preserves exact V34.1 originals. Same783 current literal sources unchanged; local82/82 scoped machine receipt/53 raw diagnostics separate. Other timed phases, separate ordinary training/story where applicable, device/child/owner/all-job acceptance remain open. |\n';lp.write_text(s,encoding='utf-8',newline='\n')
mp=b/'audit/MASTER_AUDIT_2026-08-09.md';s=mp.read_text();note='\nCurrent Geologist recheck (2026-10-02): [fresh actual Library route/earned return and Opera elevator entry](job_geode_current_recheck_v1_20261002/index.html) directly reviews58 selected canvases/318 consecutive opening-celebration-return frames,37 boards/24 native details; all783 literal current sources unchanged.27 opinions retain opening/mounting4.5/rooted material4.6 and23 inclusive priorities including flat room2.8/contact2.7/clearing3.9/pan3.8. V35 registry1778 entries preserves V34.1 and binds current opinions to the new complete boundary. Old mounted Geologist report is historical. Other complete timed tasks, device/child/owner/all-job acceptance and finding lifecycles remain open. [Impact](../design/audit_impacts/job-geode-current-recheck-20261002.json).\n'
for marker in ['## 0. Planning entry','### Development task index']:assert marker in s;s=s.replace(marker,marker+'\n'+note,1)
mp.write_text(s,encoding='utf-8',newline='\n')
ap=b/'audit/findings/ACTIVE_FINDINGS_2026-08-13.md';s=ap.read_text();s+='\n### Current Geologist source recheck — 2026-10-02\n\n[Fresh actual caller review](../job_geode_current_recheck_v1_20261002/index.html) inspects58 complete selected canvases and318 consecutive geode opening/celebration/earned Library-return frames at both widths. Crystals stay rooted inside the supported halves; static opening/mounting4.5 and material4.6 remain provisional. Room2.8/contact2.7/clearing3.9/pan3.8 and other complete timed phases/device/child/owner/comprehensive acceptance remain open. All783 literal current source hashes remain unchanged; the current local82/82 machine receipt does not close MA-VIS-006, MA-PLAY-004 or MA-OPERA-012 or strict2D debt. Existing lifecycle states remain unchanged.\n';ap.write_text(s,encoding='utf-8',newline='\n')
shutil.copyfile(__file__,f/'review_tools'/Path(__file__).name)
ip=b/'design/audit_impacts/job-geode-current-recheck-20261002.json';d=read(ip);d['files']=sorted(set(d['files'])|{p.relative_to(b).as_posix() for p in f.rglob('*') if p.is_file()}|{p.relative_to(b).as_posix() for p in history.rglob('*') if p.is_file()}|{'audit/job_artwork_refinement_live/ALL_ITEMS.json','audit/job_artwork_refinement_live/all_items.html','audit/job_artwork_refinement_live/CURRENT_BOUNDARY_REFRESH.json','audit/job_artwork_refinement_live/review_tools/refresh_current_job_review_v35.py','design/05_DOC_LEDGER.md','audit/MASTER_AUDIT_2026-08-09.md','audit/findings/ACTIVE_FINDINGS_2026-08-13.md'})
d['validation'][0]=dict(command='Fresh direct current Geologist selected-canvas/every-captured-frame/individual review',result='PASS',evidence=prefix+'/DIRECT_REVIEW.json;27 bounded individual opinions,23 inclusive priorities; weak relationships and owner acceptance remain open.')
d['acceptance_gaps']=review['qualification'];write(ip,d)
allow=b/'tmp/v2_preview_allowed.json';write(allow,sorted(set(read(allow))|set(d['files'])|{p.relative_to(b).as_posix() for p in (b/'audit/job_nursery_wash_connected_v1_20261002/remote_verified_v1').rglob('*') if p.is_file()}))
print(json.dumps(dict(status=review['status'],counts=review['counts'],registry=1778,source_unchanged=783)))
