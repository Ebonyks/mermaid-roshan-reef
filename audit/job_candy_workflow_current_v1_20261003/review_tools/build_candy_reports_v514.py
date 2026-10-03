from pathlib import Path
import json, hashlib, datetime, html, shutil

B=Path(r'C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
C=B/'audit/job_candy_workflow_current_v1_20261003'
D=B/'audit/job_candy_wrap_contact_runtime_v1_20261003'
M=B/'assets_src/imagegen/candy_wrap_contact_v1_20261003'
N=B/'assets_src/imagegen/candy_wrap_states_v1_20261003'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
def write(p,v):p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')

for name in ['QA_BOARD_MANIFEST_TRAINING_A2.json','QA_BOARD_MANIFEST_REPAIRED_A3.json']:
 q=read(C/name);q['status']='ALL_ORDERED_BOARDS_DIRECTLY_REVIEWED';q['reviewed_utc']=now
 for board in q['boards']:
  assert sha(B/board['path'])==board['sha256'];board['direct_review']=True
  for row in board['members']:
   assert sha(B/row['path'])==row['sha256'];row['direct_review']=True;row['review_scope']='Complete canvas inspected in this ordered QA board. Original-size details named separately.'
 write(C/name,q)

rows=[
 ('factory composition',3.8,'Rounded painted confectionery architecture is coherent, but dense trim competes with work and oversized UI. Refine hierarchy in actual game, conserving the source painting.', 'training',8),
 ('blurred perimeter backing',3.1,'Broad soft border washes the stage and looks like a blurred rectangular reproduction. Clarify explicit canvas layers and preserve crisp authored edges.', 'training',8),
 ('large dark activity oval',3.0,'Large translucent lens obscures physical stations and frames flat icons as a separate interface. Replace its weak use with a supported child-readable work composition.', 'training',8),
 ('progress star strip',4.0,'Earned feedback works, but generic glowing dots sit apart from the physical result. Retain intentional progress and make the visual change support the action.', 'training',11),
 ('SYRUP shell-mold painting in use',4.5,'Complete painted shell and warm syrup preserve material at the current dock size. Static visible opinion; full pouring action and hand contact are separate.', 'training',3),
 ('SYRUP ladle painting in use',4.5,'Gold/red ladle belongs to the painted workstation. Roshan does not hold it in the captured panel; do not transfer this prop score to acting.', 'training',2),
 ('SYRUP rectangular workstation frame',3.8,'The complete painted card is a hard rectangular inset over another factory. It needs scene ownership and a measured transition into useful work.', 'training',2),
 ('SYRUP actor-to-ladle contact',2.7,'Room Roshan holds a whisk away from the pictured ladle/mold. Named hand contact remains absent.', 'training',2),
 ('SORT coral flower bin',3.3,'Flat outline rectangle and coral icon function as a box, but fall below painted rounded-prop material.', 'training',5),
 ('SORT aqua shell bin',3.3,'Aqua icon is recognizable, but the container is a flat translucent rectangle. Reuse the approved shape identity and paint the actual support.', 'training',5),
 ('SORT plum wrapped-candy bin',3.2,'Flat purple silhouette repeats the wrapper problem and lacks painted folds/support.', 'training',5),
 ('SORT moving candy piece in use',3.8,'Silhouette is recognizable at touch size, but appears as a detached icon against the lens. Static readability does not prove physical sorting contact.', 'training',5),
 ('SORT room-actor contact',2.7,'Four whisk poses do not collect or place any candy into the bins.', 'training',5),
 ('WRAP exposed sweet',3.4,'Flat coral oval remains uncovered through progress. It does not visibly become the golden-paper sweet requested by the owner.', 'training',11),
 ('WRAP left end triangle',2.8,'Detached flat fan turns around an uncovered sweet. No attached paper neck or pinch contact.', 'training',9),
 ('WRAP right end triangle',2.8,'Independent rotating triangle has no connected wrapping sheet or material folding.', 'training',10),
 ('WRAP golden motion arcs',3.0,'Arcs signify motion but do not fold paper or twist attached necks. Cosmetic feedback cannot establish wrapping.', 'training',11),
 ('WRAP supporting pink rectangle',3.2,'Flat translucent platform has no painted table/support relationship and competes with the lens.', 'training',8),
 ('WRAP four work-row hand poses',2.7,'Each current work key holds a whisk away from the sweet. None represents edge fold, neck pinch or opposing twist.', 'training',8),
 ('WRAP whole action',2.8,'All consecutive ordinary wrapping frames inspected at both native sizes. Progress succeeds while the sweet remains uncovered; hand contact and material causality fail.', 'training',11),
 ('SHARE painted gift-bag invitation',4.5,'Complete painted tied gift bag is coherent and visible. Invitation opinion only; giving/receiving action is separate.', 'training',12),
 ('SHARE coral recipient portrait in use',3.8,'Recipient is recognizable but appears as an icon inside the old lens instead of a receiving character.', 'training',13),
 ('SHARE aqua recipient portrait in use',3.8,'Icon identity survives; receiving hand/object relationship is not shown.', 'training',13),
 ('SHARE plum recipient portrait in use',3.8,'Readable color identity, but remote tapping cannot demonstrate giving a wrapped sweet.', 'training',13),
 ('SHARE rival/actor relationship',3.6,'Large rival and remote Roshan compete with the small gifts and recipient symbols. Current composition is below the floor.', 'training',14),
 ('normal Kitchen return composition',4.0,'Actual earned callback restores the room and saved star. Large reading caption is supplemental; phone/child and full route acceptance remain separate.', 'training',15),
 ('COAT physical invitation binding',4.5,'Scoped route repair now arms the intended existing station and opens the task through real input. This score is selected invitation fit, not art/action closure.', 'story',1),
 ('COAT cream flat tray',3.0,'Flat rounded rectangle has no painted rim/depth or useful hand support.', 'story',2),
 ('COAT purple pitcher silhouette',2.8,'Flat jug is partly covered by the persistent cake; it is weaker than the existing painted pitcher source.', 'story',2),
 ('COAT five berries in use',3.8,'Painted berry identities are reused, but crowding/overlap with the cake obscures one side of the work.', 'story',2),
 ('COAT cake overlap with work',2.5,'Large persistent cake covers the activity area before the berries are worked. Preserve cake identity while fixing mounted ownership/scale.', 'story',2),
 ('SORT STRAWBERRIES coral bin',3.0,'Flat story bin sits below a berry row that crosses its upper edge. No painted support/contact.', 'story',5),
 ('SORT STRAWBERRIES gold bin',3.0,'Color target is recognizable but remains a flat rectangle with unsupported berries.', 'story',5),
 ('SORT STRAWBERRIES aqua bin',3.0,'Aqua target lacks painted volume and physical berry placement.', 'story',5),
 ('SORT STRAWBERRIES five-berry layout',3.4,'Five visible berries straddle the bin tops while inherited sorting earns six placements. Visible item sequencing needs its own truthful review.', 'story',5),
 ('GLAZE five berry paintings in use',4.0,'Five consistent red source berries remain recognizable. Their mounted flat tray and unchanged surface do not communicate glaze.', 'story',8),
 ('GLAZE flat pink tray',3.1,'Unpainted rectangle under the berries fails the painted support language.', 'story',8),
 ('GLAZE gold shaft/control',2.8,'Generic shaft and circular control do not represent a nozzle/brush/pour contacting berries.', 'story',9),
 ('GLAZE golden arcs',2.7,'Gold feedback brightens as progress advances; no visible physical glazing contact or material change.', 'story',11),
 ('GLAZE hand contact',2.7,'Room Roshan keeps the remote whisk. New candy-wrapper hands must never be bound to this different birthday task.', 'story',8),
 ('GLAZE cake result semantics',2.2,'At cake mask0x3F the game already shows five berries on the violet base. Binding cake protocol requires cake unchanged and glazed berries on their separate tray.', 'story',11),
 ('GLAZE whole action',2.6,'Complete consecutive action inspected at both sizes. Earned progress and stable berry count do not repair missing glaze contact or premature wrong-tier result.', 'story',11),
 ('PLACE moving-berry column',2.5,'Task berries move into a vertical column at the right edge instead of visibly settling one per upper tier.', 'story',13),
 ('PLACE visible berry accounting',2.0,'Five task berries remain visible together with five painted base berries. Ten visible berries contradict the required five-object assembly.', 'story',14),
 ('final cake upper-tier placement',2.0,'Cake mask0x7F still shows five berries along violet base and none on the five upper tiers. Canon requires one per upper tier, none on violet base.', 'story',14),
 ('final cake/Roshan occlusion',2.6,'Large cake covers Roshan head/body in the actual1600 finale. Source beauty does not pass mounted hierarchy.', 'story',14),
 ('birthday finale rival relationship',3.3,'Imp spectacle competes with the birthday-preparation result. Actual intent and object accounting need to remain primary.', 'story',14),
 ('birthday Kitchen return composition',4.0,'Ordinary callback returns with cake127 and party bit8 earned. Correct save/return does not accept the preceding visual construction.', 'story',15),
]
caps={}
for lane in ('training','story'):
 for width in (1280,1600):caps[(lane,width)]=read(C/f'attempt03/CAPTURE_{lane}_{width}.json')
opinions=[]
for i,(item,score,evaluation,lane,index) in enumerate(rows,1):
 evidence=[]
 for width in (1280,1600):
  v=caps[(lane,width)]['views'][index];assert sha(B/v['path'])==v['sha256'];evidence.append({'path':v['path'],'sha256':v['sha256'],'requested_and_native_width':width,'tag':v['tag']})
 opinions.append({'id':f'CANDY-USE-{i:03d}','item':item,'score':score,'evaluation':evaluation,'refinement':evaluation.split('. ')[-1],'scope':'Current production drawing after exactly four station bindings and ingredient invitation reuse; actual isolated Kitchen caller, '+lane,'evidence':evidence,'current_binding':'scripts/opera_career_world_2d.gd','binding_sha256':sha(B/'scripts/opera_career_world_2d.gd'),'owner_acceptance':None,'priority':score<=4.5})

details=[]
for lane,width,indices in [('training',1280,[8,11]),('training',1600,[9,13]),('story',1280,[8,11,14,15]),('story',1280,[2,5]),('story',1600,[8,14])]:
 for i in indices:
  v=caps[(lane,width)]['views'][i];details.append({'path':v['path'],'sha256':v['sha256'],'direct_original_native_review':True,'width':width,'tag':v['tag']})
boundary=read(C/'SOURCE_CURRENT_A3_BEFORE_CAPTURE.json');assert all(sha(B/x['path'])==x['sha256'] for x in boundary['source_files'])
review={'status':'ALL_CURRENT_CIRCLE_FRAMES_AND_SELECTED_VIEWS_REVIEWED_MULTIPLE_VISUAL_PRIORITIES_OPEN','reviewed_utc':now,'reviewer':'Codex visual drafting review','baseline':boundary['baseline'],'production_changes':boundary['declared_changes_from_U'],'coverage':{'current_consecutive_canvases':626,'current_phase2_canvases':622,'current_phase3_endpoints':4,'current_selected_views':64,'current_ordered_boards':66,'current_original_native_details':len(details),'earlier_training_canvases':304,'earlier_training_views':32,'earlier_training_boards':32},'opinions':opinions,'direct_native_details':details,'all783_sources_unchanged_during_capture_and_review':True,'machine_evidence':'Four current route/capture processes and nine focused route/parser/inference checks pass; failure and diagnostics preserved. New uncommitted source not covered by previous-U hosted success.','source_boundary':'SOURCE_CURRENT_A3_BEFORE_CAPTURE.json','qualification':read(C/'QA_BOARD_MANIFEST_REPAIRED_A3.json')['qualification'],'missing_evidence':['Other phases complete timed actions','Separate Opera elevator training traversal','Full preceding Farmer/Chef story travel','Natural timing','Target device','Child','Owner','Full all-job final report acceptance'],'owner_acceptance':None,'finding_lifecycles_changed':False}
write(C/'DIRECT_REVIEW_CURRENT_A3.json',review)

style='body{margin:auto;max-width:1500px;padding:24px;background:#f6f0ff;color:#292043;font:17px/1.5 system-ui}h1,h2{color:#38265e}a{color:#423784}img{max-width:100%;height:auto;background:repeating-conic-gradient(#ded4ea 0% 25%,#f6f0ff 0% 50%) 0/24px 24px}figure{margin:12px 0}figcaption{font-size:14px;overflow-wrap:anywhere}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(360px,1fr));gap:18px}article,details{background:white;border:1px solid #d7c6e5;border-radius:12px;padding:16px;margin:12px 0}.score{font-weight:800}.weak{color:#953522}pre{white-space:pre-wrap;overflow-wrap:anywhere;font-size:13px}summary{cursor:pointer;font-weight:700}'
esc=html.escape
def rel(base,path):
 import os
 return Path(__import__('os').path.relpath(B/path,base)).as_posix()
def fig(base,v):
 p=rel(base,v['path']);return '<figure><a href="'+esc(p)+'"><img loading="lazy" src="'+esc(p)+'"></a><figcaption>'+esc(v.get('tag',v['path']))+' · '+esc(v['sha256'])+'</figcaption></figure>'
def page(title,body):return '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+esc(title)+'</title><style>'+style+'</style><main><h1>'+esc(title)+'</h1>'+body+'</main></html>\n'

body='<p><strong>Current wrapping does not match the new golden-paper wrapper.</strong> Its work row holds a remote whisk; the flat sweet stays uncovered. Current whole wrapping2.8/5. New connected source attempts and the actual-input contact study are explicitly separate below.</p>'
body+='<p>All626 current consecutive wrapping/glaze canvases and64 selected views directly reviewed on66 ordered boards at native1280×720 and1600×720. All304 earlier training canvases/32 views also reviewed. Four missing birthday station bindings repaired with existing invitation art; no new wrapper is bound to production.</p>'
body+='<p><strong>Birthday priorities:</strong> premature berries on cake0x3F; five berries on violet base instead of upper tiers at0x7F; five extra task berries still visible; cake obscures Roshan. These are actual mounted/result defects, separate from the source paintings.</p>'
body+='<p>Actual Kitchen callback and all four phases earned. Explicit isolated entry and seeded preceding Farmer/Chef prerequisites; full earlier story travel, other complete timed phases, natural timing, phone/child/owner and all-job acceptance remain open.</p><nav><a href="../../assets_src/imagegen/candy_wrap_states_v1_20261003/index.html">All wrapper sources</a> · <a href="../../assets_src/imagegen/candy_wrap_contact_v1_20261003/index.html">All contact redraws</a> · <a href="../job_candy_wrap_contact_runtime_v1_20261003/index.html">Contact study and failures</a> · <a href="DIRECT_REVIEW_CURRENT_A3.json">Exact evaluations</a> · <a href="../job_artwork_refinement_live/all_items.html">All-item library</a></nav>'
body+='<div class="grid">'+''.join(fig(C,caps[k]['views'][i]) for k,i in [(('training',1280),8),(('training',1280),11),(('story',1600),11),(('story',1600),14)])+'</div><h2>Individual mounted objects and relationships</h2>'
for o in opinions:
 body+='<article id="'+o['id']+'"><h3>'+esc(o['item'])+' · <span class="score weak">'+str(o['score'])+'/5</span></h3><p>'+esc(o['evaluation'])+'</p><p>'+esc(o['scope'])+'</p><details><summary>Exact native evidence at both sizes</summary><div class="grid">'+''.join(fig(C,v) for v in o['evidence'])+'</div></details></article>'
body+='<h2>All current selected canvases</h2>'
for k,cap in caps.items():body+='<details><summary>'+esc(str(k))+' · all16 native selected views</summary><div class="grid">'+''.join(fig(C,v) for v in cap['views'])+'</div></details>'
for name in ['QA_BOARD_MANIFEST_REPAIRED_A3.json','QA_BOARD_MANIFEST_TRAINING_A2.json']:
 q=read(C/name);body+='<details><summary>'+esc(name)+' · every ordered board reviewed</summary>'+''.join(fig(C,v) for v in q['boards'])+'</details>'
body+='<h2>Source, machine and acceptance boundaries</h2><p>783 declared literal production sources stay unchanged during captures/review except the separately frozen one-file route repair from U. Raw failures, obsolete phase-count fixture, absent station reproduction and earlier snapshots remain preserved. Scores are Codex drafting opinions, not owner approval.</p><p><a href="SOURCE_CURRENT_A3_BEFORE_CAPTURE.json">Exact boundary</a> · <a href="DIMENSIONS_RECHECK_LINK.txt">Native-size recheck</a> · <a href="../../design/audit_impacts/job-candy-workflow-current-20261003.json">Impact</a></p>'
(C/'DIMENSIONS_RECHECK_LINK.txt').write_text('../job_candy_wrap_contact_runtime_v1_20261003/DIMENSIONS_RECHECK_V513.json\n',encoding='utf-8')
(C/'index.html').write_text(page('Candy Maker · current workflow and wrapper contact audit',body),encoding='utf-8',newline='\n')

# Each native contact sheet gets a separate whole-source opinion and four addressable state opinions.
scores=[[4.5,4.5,4.2,4.2],[4.5,4.5,4.5,4.1],[4.5]*4,[4.5]*4,[4.5,4.5,4.5,4.6],[4.5,4.5,4.5,4.6],[4.5,4.5,4.5,4.6]]
whole=[4.2,4.1,4.2,4.1,4.1,4.3,4.5]
sources=[]
for i in range(1,8):
 a=M/f'attempt{i:02d}';s=read(a/'SOURCE.json');r=read(a/'DIRECT_REVIEW.json');assert sha(a/'native.png')==s['sha256']
 entry={'attempt':i,'source':s,'whole_source_score':whole[i-1],'source_review':r,'state_opinions':[{'state':state,'region':[j%2*627,j//2*627,627,627],'score':scores[i-1][j],'scope':'Native static hand-and-paper state only; motion/mounted/device/owner separate.'} for j,state in enumerate(['open sheet','long-edge fold','neck pinch','opposite wrist twist'])],'production_binding':False,'owner_acceptance':None};sources.append(entry)
write(M/'COMPLETE_SOURCE_REVIEW.json',{'reviewed_utc':now,'sources':sources,'qualification':'All7 native sources directly viewed. A1–A6 rejected as complete matching sheets; A7 static provisional4.5, actual action separate. Preserve original natives and exact prompts. 1254RGBA NPOT source masters remain outside runtime; no technical-ready/owner pass.'})
body='<p>Seven separately preserved built-in ImageGen attempts. Each native source and each of its four hand/paper states has its own opinion. Static endpoints never grant an animation pass. A7 awaits exact actual-input review.</p><p><a href="../../../audit/job_candy_wrap_contact_runtime_v1_20261003/index.html">Actual-input study</a> · <a href="COMPLETE_SOURCE_REVIEW.json">All source and state opinions</a></p>'
for e in sources:
 p=e['source']['native_path'];body+='<article id="attempt'+str(e['attempt'])+'"><h2>Attempt'+str(e['attempt'])+' · complete source '+str(e['whole_source_score'])+'/5</h2>'+fig(M,{'path':p,'sha256':e['source']['sha256']})+'<p>'+esc(' · '.join(x['state']+':'+str(x['score'])+'/5' for x in e['state_opinions']))+'</p>'+''.join('<p><strong>'+esc(o['item'])+' '+str(o['score'])+'/5.</strong> '+esc(o['evaluation'])+'</p>' for o in e['source_review']['opinions'])+'<details><summary>Exact prompt/source record</summary><pre>'+esc((M/f"PROMPT_A{e['attempt']}.txt").read_text())+'</pre><a href="attempt'+f"{e['attempt']:02d}"+'/SOURCE.json">Native provenance</a></details></article>'
(M/'index.html').write_text(page('Candy Maker · connected wrapping-contact source iterations',body),encoding='utf-8',newline='\n')

shutil.copyfile(Path(__file__),C/'review_tools'/Path(__file__).name)
ip=B/'design/audit_impacts/job-candy-workflow-current-20261003.json';impact=read(ip);impact['files']=sorted(set(impact['files'])|{p.relative_to(B).as_posix() for root in (C,D,M,N) for p in root.rglob('*') if p.is_file()});impact['acceptance_gaps']+=' Current Candy wrapping2.8/glaze2.6; wrong-tier/duplicate birthday berries and cake occlusion require repair. All48 current use opinions and626 circle canvases reviewed separately from generated source contact. Native physical size inventory checked; A04 maximized-window change preserved as failed fixture.';write(ip,impact)
print(json.dumps({'current_opinions':len(opinions),'current_native_details':len(details),'source_attempts':len(sources),'current_source_unchanged':True,'report':str(C/'index.html')}))
