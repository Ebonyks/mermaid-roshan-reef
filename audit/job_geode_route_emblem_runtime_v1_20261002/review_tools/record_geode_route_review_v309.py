from pathlib import Path
import copy, datetime, hashlib, html, json, posixpath, shutil

r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
f=r/'audit/job_geode_route_emblem_runtime_v1_20261002'
prefix=f.relative_to(r).as_posix()
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
snapshot=read(f/'SOURCE_CURRENT_BEFORE_CAPTURES.json')
assert len(snapshot['source_files'])==373
assert all(sha(r/x['path'])==x['sha256'] for x in snapshot['source_files'])
assert (f/'prior_binding_attempt_01/REVIEW.json').is_file()
objects=[]
def obj(id,name,score,evaluation,refinement,proof,art=None,kind='mounted object or relationship'):
 d=dict(id=id,name=name,score=score,artwork_score=art,kind=kind,evaluation=evaluation,refinement=refinement,evidence=proof,priority=score<=4.5,owner_acceptance=None)
 objects.append(d);return d
def view(w,stem):return f'{prefix}/attempt_02/native_views/geologist_{w}_{stem}.webp'
def pair(stem):return [view(w,stem) for w in [1280,1600]]
obj('GEO-USE-LIBRARY','Library geode crest · 50 × 50',4.5,
 'The two plum-outlined halves and cyan/violet interiors remain distinct beneath Geologist Roshan on the pale card. Fine facets reduce at this size, but the painted silhouette and exact open-specimen identity survive at both widths.',
 'Inclusive 4.5 priority. Review on the target tablet and simplify only detail that actually loses clarity; preserve the approved two-half painting.',pair('normal_library_card'),4.5,'current geode presentation')
obj('GEO-USE-INVITATION','Closed invitation · 142 × 126.4146',4.5,
 'Broad lavender and aqua stone bands and one dark plum seam clearly invite opening. The pulse and halo leave the seam readable. This uses the closed state of the same atlas that later opens; the previous acceptable closed source is preserved.',
 'Inclusive 4.5 priority. Refine minor edge/fringe only after device review; the floating invitation and weak flat room are separate context issues.',pair('phase3_invitation'),4.5,'current geode presentation')
obj('GEO-USE-CELEBRATION','Normal earned celebration · 220 × 220 rect',4.2,
 'The painted specimen itself reads 4.6: cream cavity rims surround crystals rooted inside both stone halves, with intact contour and aspect. The mounted emblem remains suspended above three empty outlined trays. Its unsupported placement prevents a 4.5 mounted pass.',
 'Stage the opened specimen on an honest support and resolve the old tray/stage composition. Preserve this exact painted source and rooted crystals.',[f'{prefix}/attempt_02/native_frames/geode_1280_0110.webp',f'{prefix}/attempt_02/native_frames/geode_1600_0108.webp'],4.6,'current geode presentation')
obj('GEO-USE-DEV-MENU','Developer playtest menu · 80 × 80',4.6,
 'At 80 pixels, both stone halves, cavity rims and crystal groups read cleanly against the pale menu. The unchanged shared career-crest caller now gives the adult launcher the same end-state identity as the Library and earned celebration.',
 'Retain provisionally; confirm device rendering. This is the existing owner-directed developer launcher, not a new lesson or chapter route.',pair('actual_elevator_menu'),4.6,'current geode presentation')
state_notes=[
 'A single rounded closed stone with a centered plum seam rests at the stable center/base.',
 'The narrow first crack reveals a sliver of interior without releasing a crystal.',
 'The opening grows around the stable base; the cream cavity rim becomes readable.',
 'Both halves reveal coherent cyan and violet mineral groups inside the cavity.',
 'The cavities widen while the shell contours and crystal roots remain consistent.',
 'Two calm mineral clusters stay within their cream rims; width increases without whole-object translation.',
 'Both fully opened halves sit on the same slab; crystals remain embedded through completion.'
]
frames=[];views=[];boards=[];ranges={};caps={}
for w,total,first_goal,first_return in [(1280,162,110,141),(1600,155,108,134)]:
 cap=read(f/f'attempt_02/CAPTURE_{w}.json');caps[w]=cap
 assert len(cap['motion_frames'])==total and len(cap['views'])==29
 assert read(f/f'runtime_gate/capture{w}v2.receipt.json')['status']=='PASS'
 for x in cap['motion_frames']:
  assert sha(r/x['path'])==x['sha256']
  x['direct_review']=True;x['reviewed_utc']=now;x['review_method']='Direct inspection of every cell on the complete ordered whole-frame boards; selected full native details also inspected.'
  index=x['index'];phase=x['phase_index']
  if index<first_goal:
   assert phase==3
   pull=float(x['surface'].get('pull',0));state=min(6,int(pull/20))
   x['visible_review_lane']='actual geode task';x['authored_state_index']=state
   x['scores']={'geode_artwork':4.5,'object_opening_sequence':4.5,'rooted_crystals':4.6,'work_slab':4.6,'actor_work_contact':2.7,'room':2.8}
   x['evaluation']=state_notes[state]+' Minor edge/reveal remains at the inclusive 4.5 threshold. Roshan works remotely rather than reaching the slab; room/contact opinions stay separate.'
  elif index<first_return:
   assert phase==4
   x['visible_review_lane']='ordinary earned celebration'
   x['scores']={'painted_geode_artwork':4.6,'emblem_placement':4.2,'celebration_composition':3.3,'room':2.8,'clap_acting':4.0}
   x['evaluation']='Normal celebration retains the two painted cavities and rooted crystals, but the emblem hangs above empty outlined trays. The flat stage and distant actor remain weak. Allocated task metadata does not mean the old slab is visibly mounted here.'
  else:
   assert phase==-1
   x['visible_review_lane']='actual earned Library return'
   x['scores']={'library_artwork':4.6,'return_caption_placement':4.0}
   x['evaluation']='The ordinary OperaAct callback returns to the Library with the earned star. The first return frame is dim during the fade; the later caption covers Roshan lower tail, and Daddy bottom at the wide layout. Repeated held states are actual captured game states; no missing motion is filled by synthesized images.'
  frames.append(x)
 for x in cap['views']:
  assert sha(r/x['path'])==x['sha256']
  x['direct_review']=True;x['reviewed_utc']=now
  stem=Path(x['path']).stem;phase=x.get('phase_index')
  if x['state'] in ['normal_library_card','actual_earned_library_return']:
   x['scores']={'library_artwork':4.6,'geode_crest':4.5,'caption_placement':4.0}
   x['evaluation']='Actual Library scene and career card use the painted open-geode crest. Warm room art remains coherent; broad caption overlaps the actor lower body. Return still shows the earned star.'
  elif x['state'] in ['actual_elevator_menu','actual_dev_back_menu']:
   x['scores']={'geode_menu_icon':4.6};x['evaluation']='Existing adult developer launcher and Back show the same readable painted 80-pixel geode. Other menu icons remain unchanged; no whole-menu reapproval is inferred.'
  elif x['state']=='actual_opera_venue':
   x['scores']={'caption_placement':4.0};x['evaluation']='Actual separate Opera venue is shown to establish the existing elevator route. This capture does not newly approve the whole venue; prior object evaluations remain separately linked.'
  elif phase==3:
   is_inv=x['state']=='invitation'
   x['scores']={'closed_invitation' if is_inv else 'geode_artwork':4.5,'rooted_crystals':4.6,'room':2.8,'actor_work_contact':2.7}
   x['evaluation']='Current closed/open authored family reads consistently. The completed geode reveals crystals inside the halves, with stable base and center. Room and reaching/contact remain weak; this still is not a whole-action pass.'
  elif phase==1:
   x['scores']={'fossil_artwork':4.6,'clearing_and_piece_geometry':3.9,'actor_work_contact':2.7,'room':2.8}
   x['evaluation']='Painted fossil identity improves material quality, but dirt removal cuts straight rectangular cells and puzzle thirds retain straight strips/ghost targets. Remote brushing and flat room remain unresolved.'
  elif phase==2:
   x['scores']={'pan_artwork':4.6,'pan_action':3.8,'actor_work_contact':2.7,'room':2.8}
   x['evaluation']='Painted pan contains cyan minerals while orange grains leave during rocking. The surface makes the verb legible, but actor contact is remote and the grain/action finish remains below 4.5.'
  else:
   x['scores']={'painted_river_artwork':4.6,'room':2.8,'actor_work_contact':2.7}
   x['evaluation']='Current painted river work is visible in the actual normal route. Its earlier dedicated detailed material/junction opinions remain linked separately; this still does not approve natural timing or complete actor contact.'
  views.append(x)
 write(f/f'attempt_02/CAPTURE_{w}_REVIEWED.json',cap)
 bm=read(f/f'BOARD_MANIFEST_V2_{w}.json')
 bm['status']='EVERY_CAPTURED_FRAME_AND_STILL_DIRECTLY_REVIEWED';bm['reviewed_utc']=now
 bm['frames']=cap['motion_frames'];bm['views']=cap['views']
 for b in bm['boards']:
  assert sha(r/b['path'])==b['sha256'];b['direct_review']=True;b['reviewed_utc']=now;boards.append(b)
 write(f/f'BOARD_MANIFEST_V2_{w}.json',bm)
 ranges[str(w)]={'task':[0,first_goal-1],'normal_celebration':[first_goal,first_return-1],'actual_Library_return':[first_return,total-1],'caption_starts':first_return+1}
for state,note in enumerate(state_notes):
 proof=[x['path'] for x in frames if x.get('authored_state_index')==state]
 assert proof,state
 obj(f'GEO-OPEN-STATE-{state}',f'Authored opening state {state} of 6',4.5,note+' All occurrences on both-width complete sequences were directly inspected.',
  'Refine minor contour/reveal only; preserve center, base, cavity topology and rooted minerals. Remote actor contact remains 2.7.',[proof[0],proof[-1]],4.5,'opening state')
obj('GEO-CAVITIES','Rooted crystal groups and cream cavity rims',4.6,'Cyan and violet minerals remain attached inside both stone cavities, including the normal celebration. No detached loot crystals appear. Broad facets preserve the storybook material language.','Retain provisionally; target-device and owner approval remain separate.',pair('phase3_full_interior_before_award'),4.6)
obj('GEO-SLAB','Painted work slab',4.6,'The cream top and lavender side planes of the painted support has an authored contour and an honest resting surface during the opening. Stable stone base avoids earlier whole-object drift.','Retain provisionally; celebration does not currently preserve this support.',pair('phase3_middle_open'),4.6)
obj('GEO-CONTACT','Roshan hand/tool contact with work',2.7,'Roshan changes pose but remains beside the task instead of visibly reaching its working surface. Remote seam/pull, brush and pan handling do not satisfy visible local work.','Use matching authored contact poses and stage her at the work; do not award the contact claim from a crouch alone.',pair('phase3_middle_open'))
obj('GEO-CLAP','Work-to-clap transition',4.0,'The cheerful authored clapping pose reads clearly, but the change from remote crouching to clap is abrupt and does not supply the missing work contact.','Repair arrival/contact/resting action before transition polish.',pair('phase3_earned_completion'),4.6)
obj('GEO-ROOM','Geologist flat room backdrop',2.8,'Uniform polygon strata and broad flat wedges remain visibly unlike the painted character and new specimen. The new props do not repair the environment.','Replace the named weak background with a painted native-resolution solution; retain originals. The current 1254-square generation fails required coverage.',pair('phase3_invitation'))
obj('GEO-TRAYS','Three outlined display trays',2.9,'Empty cyan rectangular outlines provide neither material nor honest support; the celebration specimen floats above them.','Rebuild or reuse child-readable painted supports and bind the opened specimen to its actual resting surface.',[f'{prefix}/attempt_02/native_frames/geode_1280_0110.webp'])
obj('GEO-HALO','Flat crystal cluster and ring',2.9,'Sharp polygon crystals and a thin cyan ring remain unrelated to the more specific painted geode material.','Replace this named live vector defect with a compatible painted formation or appropriate reused art.',pair('phase3_invitation'))
obj('GEO-CELEBRATION-CONTEXT','Normal celebration composition',3.3,'The specimen identity now survives the win, improving the former flat emblem. The flat proscenium, empty trays and suspended placement still interrupt the visual world.','Resolve support and painted stage hierarchy; source 4.6 cannot grant composition 4.5.',[f'{prefix}/attempt_02/native_frames/geode_1280_0110.webp',f'{prefix}/attempt_02/native_frames/geode_1600_0108.webp'])
obj('GEO-FOSSIL-CLEARING','Fossil dirt clearing and puzzle thirds',3.9,'Straight brush-grid gaps and rectangular source strips are visible across partial clearing and piece placement. The fossil painting itself is coherent, but the cut geometry feels mechanical.','Develop a reversible organic clearing/assembly treatment while preserving conserved pieces, input and saved progress.',pair('phase1_partial_brush')+pair('phase1_one_piece'),4.6)
obj('GEO-PAN-ACTION','Pan rocking and contained minerals',3.8,'The bowl rocks and orange grains move away while cyan minerals stay inside. The action communicates sorting but still lacks Roshan hand contact and a polished quiet return.','Refine actual contact, grain release and calm ending; local motion studies remain separate unbound references.',pair('phase2_pan_right')+pair('phase2_partial_pan'),4.6)
obj('GEO-RETURN-CAPTION','Library return caption placement',4.0,'The large pale caption covers Roshan lower tail; at the wide layout it also cuts into Daddy bottom. Earned star and real return remain correct.','Refine this shared caption placement with both actors and the supported aspect ratios in view.',pair('actual_earned_library_return'))
obj('GEO-LIBRARY-ART','Library painted room art',4.6,'The warm lavender stone, aqua windows and rounded shell furniture support the approved storybook world. The icon fits its pale career card.','Retain; caption and protected actor identity stay separately evaluated.',pair('normal_library_card'),4.6)
sm=read(f/'STILL_BOARD_MANIFEST_V2.json');sm['status']='EVERY58_NATIVE_STILL_DIRECTLY_REVIEWED';sm['reviewed_utc']=now
by_path={x['path']:x for x in views}
for b in sm['boards']:
 assert sha(r/b['path'])==b['sha256'];b['direct_review']=True;b['reviewed_utc']=now;b['views']=[by_path[x['path']] for x in b['views']]
write(f/'STILL_BOARD_MANIFEST_V2.json',sm)
details=[view(w,stem) for w in [1280,1600] for stem in ['normal_library_card','phase3_invitation','actual_elevator_menu']]+[f'{prefix}/attempt_02/native_frames/geode_1280_0110.webp',f'{prefix}/attempt_02/native_frames/geode_1600_0108.webp']
review=dict(status='CURRENT_ROUTE_USES_REVIEWED_ART_IMPROVED_CONTEXT_PRIORITIES_REMAIN',reviewed_utc=now,baseline=snapshot['baseline'],source_files=snapshot['source_files'],views=views,frames=frames,boards=boards,still_boards=sm['boards'],individual_objects=objects,native_details=[dict(path=p,sha256=sha(r/p),direct_review=True) for p in details],frame_ranges=ranges,counts=dict(native_stills=58,consecutive_frames=317,ordered_motion_boards=27,ordered_still_boards=10,native_details=8,individual_current_opinions=len(objects)),scores=dict(opening=4.5,rooted_crystals=4.6,library_crest=4.5,invitation=4.5,developer_menu_geode=4.6,celebration_geode_artwork=4.6,celebration_placement=4.2,celebration_composition=3.3,room=2.8,work_contact=2.7,fossil_clearing=3.9,pan_action=3.8,return_caption=4.0),owner_acceptance=None,
 scope_trace={'new_shared_caller':'scripts/opera_job_playtest_menu.gd uses CastleCareerRoutes.CAREER_CREST_FILES at 80x80; unchanged existing developer menu was captured and reviewed. Four current presentations are individually recorded.', 'route':'Actual Library picture card -> shipping OperaAct -> four intentional tasks -> normal celebration -> ordinary earned Library return/star; separate actual Opera venue/elevator developer replay/Back.', 'not_a_new_route':'Current ChapterTwo career order excludes Geologist; no Geologist lesson, two-act rollout or invented chapter entry is claimed.'},
 review_method='Directly inspected every cell on 27 complete ordered motion boards and 10 complete native-still boards before this record, plus eight whole native detail images. Captured originals and hash provenance remain intact. Current opinions are individually scoped; the prior 86-object report remains historical detail, not a claim of 86 fresh object re-reviews.',
 qualification='Codex first-pass drafting opinions only. Entry fixture initializes isolated Main/Castle/save state, but actual actions use touch/drag and normal callbacks; no injected artwork, forced phases/results or completion callback changes. Readback slows wall-clock motion; desktop capture is not device fps evidence. Full CI is separately pending on 373 frozen literal files; cache identity is engine-verified, device VRAM/fps/child/owner and broad all-job acceptance remain open. Inclusive <=4.5 remains a refinement priority.')
write(f/'REVIEW.json',review)
plan=read(f/'PLAN.json');plan['status']='CURRENT_ROUTE_DIRECT_REVIEW_RECORDED_FRESH_FULL_CI_PENDING';plan['bindings']['developer_menu']=dict(path=plan['bindings']['crest']['path'],rect=[80,80],caller='scripts/opera_job_playtest_menu.gd',score=4.6);plan['current_review']='REVIEW.json';write(f/'PLAN.json',plan)
esc=html.escape
url=lambda p:posixpath.relpath(p,prefix)
def figure(p,caption):return f'<figure><a href="{esc(url(p))}"><img loading="lazy" src="{esc(url(p))}" alt="{esc(caption)}"></a><figcaption>{esc(caption)}</figcaption></figure>'
css='''body{margin:0;background:#edf3f7;color:#253449;font:17px/1.6 system-ui,sans-serif}main{max-width:1220px;margin:auto;padding:24px}h1,h2,h3{color:#423079;line-height:1.25}a{color:#3e328b}section,article,details{background:#fff;padding:22px;margin:20px 0;border-radius:18px;border:1px solid #ccd8e4}figure{margin:16px 0;background:#eff5fb;border-radius:12px;overflow:hidden}img{display:block;width:100%;height:auto}figcaption{padding:10px 14px;color:#253449;background:#f6f9ff;overflow-wrap:anywhere}table{border-collapse:collapse;width:100%;font-size:16px}th,td{text-align:left;vertical-align:top;border-bottom:1px solid #d4deeb;padding:10px}code{overflow-wrap:anywhere}button,select{font:inherit;padding:9px 15px;background:#f5f1ff;border:1px solid #8775bd;border-radius:12px}.priority{border-left:6px solid #bc7641}.good{border-left:6px solid #468679}.facts{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px}.facts p{margin:0;background:#eaf3f7;padding:14px;border-radius:12px}.controls{position:sticky;top:0;background:#eaf1f9;padding:10px;z-index:2}summary{cursor:pointer;font-weight:650}.native-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(460px,1fr));gap:14px}@media(max-width:600px){main{padding:12px}.native-grid{display:block}td,th{padding:5px;font-size:14px}}'''
parts=[f'<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Geologist geode · actual route review</title><style>{css}</style><main><h1>The geode opens to reveal crystals inside</h1>',
 '<p>The same painted specimen now appears on the Library card, closed invitation, normal earned celebration and shared developer menu. It opens into two stone halves; crystals remain rooted inside both cavities. This is a reversible runtime candidate with original art preserved.</p>',
 '<div class="facts"><p>58 native stills<br>317 consecutive frames</p><p>27 motion boards<br>10 still boards · all reviewed</p><p>Opening 4.5 provisional<br>Rooted crystals 4.6</p><p>Celebration placement 4.2<br>Room 2.8 · contact 2.7</p></div>',
 '<p>Scores are individual first-pass opinions. A source score does not approve its staging or the whole activity. Items at or below 4.5 remain priorities. Owner, child and target-device approval remain pending; this is not the final all-jobs report.</p>',
 '<nav><a href="../job_artwork_refinement_live/all_items.html">All known job items</a> · <a href="../job_geology_room_route_v1_20261002/index.html">Prior 86-object route review</a> · <a href="../job_geode_coherent_runtime_v1_20261002/index.html">Seven-state rebuild and rejected mounting</a> · <a href="../../assets_src/imagegen/geologist_grotto_native2k_v1_20261002/index.html">Failed native-resolution backdrop attempt</a> · <a href="REVIEW.json">Exact current evaluations</a></nav>',
 '<section><h2>Four current presentations</h2><p>The 80-pixel developer menu is an additional shared caller discovered during this review. Its existing code did not change. The ordinary celebration uses the painted open specimen, but its support and surrounding stage remain weak.</p><table><tr><th>Use</th><th>Artwork</th><th>Mounted opinion</th></tr>']
for x in objects[:4]:parts.append(f'<tr><td>{esc(x["name"])}</td><td>{x["artwork_score"]}/5</td><td>{x["score"]}/5</td></tr>')
parts.append('</table></section>')
for x in objects[:4]:
 parts.append(f'<article id="{x["id"]}" class="{"priority" if x["priority"] else "good"}"><h2>{esc(x["name"])} · {x["score"]}/5</h2><p>{esc(x["evaluation"])}</p><p>Next refinement: {esc(x["refinement"])}</p>')
 for p in x['evidence']:parts.append(figure(p,Path(p).name+' · complete captured native canvas'))
 parts.append('</article>')
parts.append('<section><h2>Individual objects, states and relationships</h2><p>The previous 86-object index is linked for unchanged historical detail. The following opinions name exactly what was freshly assessed in these current captures; they do not turn that earlier index into 86 fresh re-reviews.</p><div class="controls"><label><input id="weak" type="checkbox"> Show priorities at or below 4.5 only</label></div>')
for x in objects[4:]:
 parts.append(f'<article class="opinion {"priority" if x["priority"] else "good"}" data-priority="{str(x["priority"]).lower()}" id="{x["id"]}"><h3>{esc(x["name"])} · {x["score"]}/5</h3><p>{esc(x["evaluation"])}</p><p>{esc(x["refinement"])}</p><details><summary>Open captured evidence</summary>')
 for p in x['evidence']:parts.append(figure(p,Path(p).name))
 parts.append('</details></article>')
parts.append('</section><section><h2>Every consecutive opening, celebration and return frame</h2><p>Each ordered board contains complete captured canvases, left to right and top to bottom. Native originals are linked separately. These are actual recorded frames, including unchanged held gameplay states. No interpolated, synthesized or repaired frames were substituted. The phase index determines the visible celebration, even while old task metadata remains allocated.</p>')
for w in [1280,1600]:
 rr=ranges[str(w)];parts.append(f'<h3>{w} × 720</h3><p>Task frames {rr["task"]}; normal celebration {rr["normal_celebration"]}; actual Library return {rr["actual_Library_return"]}. Caption starts frame {rr["caption_starts"]} after the initial dim return.</p>')
 for b in boards:
  if b['width']==w:parts.append(figure(b['path'],f'{w}: frames {b["first_frame"]}–{b["last_frame"]} · all {b["count"]} directly reviewed'))
parts.append('<details><summary>Every native frame and its individual recorded evaluation</summary>')
for x in frames:parts.append(f'<p><a href="{esc(url(x["path"]))}">{x["width"]} frame {x["index"]:04d}</a> · {esc(x["visible_review_lane"])} · {esc(x["evaluation"])} <code>{esc(json.dumps(x["scores"]))}</code></p>')
parts.append('</details></section><section><h2>Every native still across all four tasks and real routes</h2>')
for b in sm['boards']:parts.append(figure(b['path'],f'{b["width"]} still board {b["index"]} · {b["count"]} whole captured canvases · all directly reviewed'))
parts.append('<details><summary>Open all 58 native stills and evaluations</summary><div class="native-grid">')
for x in views:parts.append(figure(x['path'],x['evaluation']+' Scores: '+json.dumps(x['scores'])))
parts.append('</div></details></section><section><h2>Implementation and evidence limits</h2><p>Three production scripts change only the crest/goal/invitation resource binding and exact catalog metadata. All 24 Castle route functions and 182 career-world functions stay literally unchanged; catalog validators remain unchanged. The source atlas pixels and hashes are unchanged. Godot confirms one cached atlas texture for these uses; its nominal RGBA8 footprint is 8 MiB, which can load earlier than the former 4 MiB invitation source. This is not device VRAM or frame-rate acceptance.</p><p>The actual picture card, four intentional tasks, ordinary win callback and earned Library star are captured at both widths. The existing adult elevator replay and Back are separate. The isolated entry fixture and slowed readback do not prove a natural full chapter launch or device timing.</p><p id="ci-status">Fresh full regression suite: pending on 373 frozen literal source files.</p><p><a href="full_ci_v2/RECEIPT.json">Full current suite receipt</a> · <a href="full_ci_v1/RECEIPT.json">Preserved failed first suite: 81 of 82 probes passed</a> · <a href="MECHANIC_UNCHANGED.json">Exact function-body preservation</a> · <a href="RESOURCE_CONTRACT.json">Unrelaxed catalog/cache check</a> · <a href="SOURCE_CURRENT_BEFORE_CAPTURES.json">373 source hashes</a></p><p>Weak backdrop, work contact, fossil clearing, panning, celebration support, caption placement, native background coverage and the broad all-jobs backlog remain open. No finding lifecycle closure, integration or release is granted.</p></section></main><script>document.getElementById("weak").onchange=e=>document.querySelectorAll(".opinion").forEach(x=>x.hidden=e.target.checked&&x.dataset.priority!=="true");fetch("full_ci_v2/RECEIPT.json").then(r=>r.json()).then(d=>{document.getElementById("ci-status").textContent="Fresh full regression suite: "+d.status+(d.probe_results?" · "+d.probe_results.length+" probes · "+(d.source_checks||[]).length+" literal source checks":"")+". Machine verification remains separate from visual/device/owner acceptance.";});</script></html>')
(f/'index.html').write_text(''.join(parts),encoding='utf-8',newline='\n')
shutil.copyfile(Path(__file__),f/'review_tools'/Path(__file__).name)
for rel in ['audit/MASTER_AUDIT_2026-08-09.md','audit/findings/ACTIVE_FINDINGS_2026-08-13.md']:
 p=r/rel;s=p.read_text(encoding='utf-8')
 old_line=next(x for x in s.splitlines() if x.startswith('Painted geode route continuation (2026-10-02):'))
 link=('../' if '/findings/' in rel else '')+prefix.split('/',1)[1]+'/index.html'
 note=f'Painted geode route continuation (2026-10-02): [Current four mounted presentations and every58 native stills/317 consecutive real route frames]({link}) directly reviewed at1280/1600. Same authored source now binds Library50px4.5, closed invitation142px4.5, normal celebration art4.6/unsupported placement4.2, and unchanged shared developer menu80px4.6. Seven-state opening4.5/rooted crystals4.6 remain provisional; celebration composition improves to3.3 but remains weak. Room2.8/contact2.7/fossil clearing3.9/pan3.8/caption4.0 and failed native-background coverage remain open. Fresh unmodified fullCI pending on373 frozen literal sources; strict catalog/cache passes separately. Prior86-object review remains historical detail, not86 fresh re-reviews. No all-job/device/child/owner acceptance, finding lifecycle change, integration or release.'
 s=s.replace(old_line,note)
 for a,b in [('job_training_shared_source_review_v 1_20261002','job_training_shared_source_review_v1_20261002'),('geology_geode_emblems_v 1_20261002','geology_geode_emblems_v1_20261002'),('geologist_grotto_native 2k_v 1_20261002','geologist_grotto_native2k_v1_20261002')]:s=s.replace(a,b)
 p.write_text(s,encoding='utf-8',newline='\n')
ledger=r/'design/05_DOC_LEDGER.md';s=ledger.read_text(encoding='utf-8')
s='\n'.join(x for x in s.split('\n') if not x.startswith('| `'+prefix+'/index.html`'))
s+='\n| `'+prefix+'/index.html` | 🔵 | `SUPPORTING_CURRENT` reversible four-use actual route review: all58 native stills/317 frames/27 motion boards/10 still boards/eight native details and'+str(len(objects))+' named current object/state/context opinions. Library50px and closed142px4.5 provisional; developer80px4.6; celebration painting4.6 but unsupported placement4.2/composition3.3. Strict catalog/cache passes; fresh373-source full suite pending separately. Prior86-object detail remains historical, originals preserved, room/contact/native-resolution/all-job/device/child/owner gates and finding lifecycles remain open. |\n'
ledger.write_text(s,encoding='utf-8',newline='\n')
ip=r/'design/audit_impacts/job-geode-route-emblem-runtime-20261002.json';d=read(ip)
d['scope']+=' Fresh actual-use review includes the fourth shared developer menu caller; all58 native stills/317 frames directly inspected and separately scored. Four new presentation opinions keep celebration material4.6 separate from unsupported mounting4.2. Correct three malformed existing continuation navigation paths without changing dated evidence.'
d['files']=sorted(set(d['files'])|{p.relative_to(r).as_posix() for p in f.rglob('*') if p.is_file()})
d['validation'].append(dict(command='Direct complete current Library/OperaAct/elevator route artwork review',result='PASS',evidence=prefix+'/REVIEW.json; direct visual inspection completed, not a claim that all artwork passes4.5.'))
d['acceptance_gaps']='Opening/Library/invitation4.5 provisional; celebration material4.6 but placement4.2/composition3.3, room2.8/contact2.7/fossil clearing3.9/pan3.8/caption4.0 remain weak. Fresh fullCI pending373 source files; native background coverage/device/child/owner/all-job acceptance and finding lifecycle remain open.'
write(ip,d)
allow=r/'tmp/v2_preview_allowed.json';write(allow,sorted(set(read(allow))|{p.relative_to(r).as_posix() for p in f.rglob('*') if p.is_file()}))
print('Recorded current four uses,',len(objects),'individual opinions, every58 stills/317 frames/37 boards/eight native details; no global approval.')
