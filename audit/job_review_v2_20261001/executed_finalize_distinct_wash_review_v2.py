from pathlib import Path
import datetime, hashlib, html, json, os, shutil

r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
out=r/'audit/job_review_v2_20261001'
foam=r/'assets_src/imagegen/day2_wash_foam_v1_20261001'
reuse=r/'audit/day_two_wash_bubble_reuse_v1_20261001'
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,data):p.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
review=json.loads((reuse/'REVIEW.json').read_text())
for row in review['items']:
    if row['direct_full_native_review']:continue
    earlier=next(x for x in review['items'] if x['path']==row['path'].replace('_1600_','_1280_'))
    row['direct_full_native_review']=True
    row['initial_mounted_score']=earlier['initial_mounted_score']
    row['evaluation']=earlier['evaluation']+' The complete1600x720 native view was directly inspected; the wider margins preserve the same subject/anchor defect.'
review['direct_full_native_views']=20
review['remaining_full_native_views_unreviewed']=0
review['additional_direct_review_utc']=now
review['status']='ALL_TWENTY_INITIAL_VIEWS_REVIEWED_COMPLETE_ACTIONS_OPEN'
review['reuse_sink_sources']=[{'path':p,'sha256':sha(r/p),'first_cell_source_score':score,'evaluation':text} for p,score,text in [
 ('assets/flats/castle/interactions_v2/bubble_bath_sink_sheet.png',4.6,'Direct whole-atlas inspection: intact cream-peach shell, gold tap, aqua cabinet and soft painted contour offer suitable established identity for a washing subject. First cell is a reuse candidate; mounted fit, hands and complete washing action are not reviewed.'),
 ('assets/flats/castle/interactions_v2/kitchen_sink_sheet.png',4.5,'Direct whole-atlas inspection: compact clean shell sink retains established identity but thin outer bright pixels and lack of cabinet/water/hand context remain weaker for this task. Reuse candidate only.'),
 ('assets/flats/castle/interactions/bubble_bath_sink_atlas.png',4.2,'Direct whole-atlas inspection: intact established sink identity, but flat straight water and repetitive ring overlays retain schematic motion treatment. No complete-action pass.'),
 ('assets_src/concepts/opera_house_flat/cards/opera_lobby_services_handwashing_bubble_markers.png',3.2,'Direct complete source inspection: two framed sign panels, abstract hand symbol and bubble meter, unsuitable as an isolated literal washing subject. Retired reference only.')]]
write(reuse/'REVIEW.json',review)
native=[]
for p in sorted((foam/'native_fit_v1/native_views').glob('*.webp')):
    fresh='fresh_foam02' in p.name; doctor=p.name.startswith('doctor')
    score=(3.0 if doctor else 3.2) if fresh else 3.0
    native.append({'path':p.relative_to(foam).as_posix(),'sha256':sha(p),'direct_full_native_review':True,'source_variant':'fresh_foam02' if fresh else 'original',
        'individual_display_style_score':4.6 if fresh else 3.0,'mounted_context_score':score,'complete_action_score':None,
        'evaluation':('Fresh matte scallops, broad cream/mint bands and muted purple contour retain the4.6 isolated display-style opinion at the actual220x131 draw size. '+('Foam covers the painted stethoscope rather than the visible shell basin; its wide cream silhouette obscures the clinic object and approaches Roshan’s hair. The doctor anchor remains3.0.' if doctor else 'Foam floats beside and partly overlaps Roshan’s right elbow/hip, with no literal basin at that spot. It does not communicate a washing action; nursery mounted context is3.2.')) if fresh else ('Original broken circular rings remain3.0. '+('They indicate the stethoscope rather than the visible shell basin.' if doctor else 'They float beside Roshan without a basin or washing hands.'))})
assert len(native)==8
fit={'schema':'reef.wash-foam-native-context-review.v2','source_revision':'8e41deaf34f925869395cd8ab0affefe89f89ab5','reviewed_utc':now,'direct_full_native_views':8,'items':native,
 'source_score':4.6,'individual_display_style_score':4.6,'overall_mounted_context_score':None,'complete_action_score':None,
 'status':'SOURCE_SELECTED_UNBOUND_CONTEXT_REPAIRS_REQUIRED','qualification':'All eight complete original/candidate native fixture views directly inspected. Existing invitation dimensions and source bindings preserved. Better source art does not establish a complete object/action4.5 pass, ordinary story/training route, phone/child/owner acceptance.'}
write(foam/'NATIVE_CONTEXT_REVIEW_V2.json',fit)
attempt=json.loads((foam/'ATTEMPT_02_REVIEW.json').read_text())
attempt['selection']='SOURCE_DRAFT_SELECTED_UNBOUND_CONTEXT_REPAIRS_REQUIRED'
attempt['native_fit_score']=None
attempt['individual_display_style_score']=4.6
attempt['native_context_review']='NATIVE_CONTEXT_REVIEW_V2.json'
attempt['mounted_context_scores']={'doctor':3.0,'nursery':3.2}
attempt['complete_action_score']=None
write(foam/'ATTEMPT_02_REVIEW.json',attempt)

css='body{margin:0;background:#eef0fa;color:#25304c;font:17px/1.5 system-ui}main{max-width:1180px;margin:auto;padding:24px}a{color:#3856a3}section,article{background:white;padding:20px;border-radius:12px;margin:20px 0}img{max-width:100%;height:auto}figure{margin:10px 0}figcaption{margin:8px 0}.source{background:repeating-conic-gradient(#ebedf6 0% 25%,#dce0ec 0% 50%) 0/24px 24px}table{border-collapse:collapse;width:100%}th,td{padding:10px;text-align:left;border-bottom:1px solid #dce0ec}.notice{border-left:5px solid #cb826b;padding:15px;background:#fff4ef}code{overflow-wrap:anywhere}nav{display:flex;gap:20px;flex-wrap:wrap}'
esc=html.escape
def imgcard(src,title,text,source=False):return '<article><h3>'+esc(title)+'</h3><figure><img loading="lazy" '+('class="source" ' if source else '')+'src="'+esc(src,quote=True)+'" alt="'+esc(title,quote=True)+'"><figcaption>'+esc(text)+'</figcaption></figure></article>'
body='<h1>Washing artwork: source and context review</h1><nav><a href="../job_review_v2_20261001/index.html">Distinct review revision2</a><a href="../job_artwork_refinement_live/all_items.html">Individual job library</a><a href="REVIEW.json">Twenty-view evaluations and reuse inventory</a><a href="../../assets_src/imagegen/day2_wash_foam_v1_20261001/NATIVE_CONTEXT_REVIEW_V2.json">Eight fresh-foam native evaluations</a></nav>'
body+='<p class="notice">First-pass refinement remains incomplete. Twenty original/reuse invitation and initial activity views, plus eight original/fresh-foam views, were directly reviewed. Foam source/display style4.6 is a drafting opinion. Doctor context3.0, nursery context3.2, doctor washing subject2.9 and nursery missing subject2.2 remain priorities. Complete washing actions, ordinary played training/story routes, owner/phone/child acceptance are pending.</p>'
body+='<section><h2>Individual decisions</h2><table><tr><th>Item</th><th>Score</th><th>Decision</th></tr><tr><td>Original doctor and nursery ring sources</td><td>3.0</td><td>Replace the schematic rings; preserve originals.</td></tr><tr><td>Existing bubble-burst cells0/2</td><td>4.4 source;4.0/3.7 mounted</td><td>Reuse test below target: too glossy and blue for soap.</td></tr><tr><td>Fresh foam attempt1</td><td>4.4</td><td>Retained rejected draft: bright teal contour fringe.</td></tr><tr><td>Fresh foam attempt2</td><td>4.6 source/display style</td><td>Selected unbound source; placement/action are separate.</td></tr><tr><td>Doctor fresh-foam context</td><td>3.0</td><td>Over the stethoscope rather than the painted wash basin.</td></tr><tr><td>Nursery fresh-foam context</td><td>3.2</td><td>Floating beside and overlapping Roshan without a basin.</td></tr><tr><td>Doctor initial washing activity</td><td>2.9</td><td>Schematic sink and detached circle hands, away from Roshan.</td></tr><tr><td>Nursery initial washing activity</td><td>2.2</td><td>Generic widget draw branch returns before nursery wash subject.</td></tr><tr><td>Existing bubble-bath sink first cell</td><td>4.6 source</td><td>Suitable established reuse candidate; mounted/contact/action pending.</td></tr></table></section>'
for n,score,text in [('attempt_01_native.png',4.4,'Rejected and preserved: mint/teal outer fringe and oversized bright highlights.'),('attempt_02_native.png',4.6,'Selected unbound matte source. Native1635x962 alpha is preserved; runtime derivative uses only whole-canvas uniform scaling and transparent padding.')]:
    body+=imgcard('../../assets_src/imagegen/day2_wash_foam_v1_20261001/'+n,'Fresh foam '+n+' — '+str(score)+'/5',text,True)
body+='<h2>Fresh foam in the actual invitation nodes</h2>'
for row in native:body+=imgcard('../../assets_src/imagegen/day2_wash_foam_v1_20261001/'+row['path'],Path(row['path']).name+' — context'+str(row['mounted_context_score'])+'/5',row['evaluation'])
body+='<h2>Existing-art reuse inventory</h2>'
for row in review['reuse_sink_sources']:body+=imgcard('../../'+row['path'],Path(row['path']).name+' — source'+str(row['first_cell_source_score'])+'/5',row['evaluation'],True)
body+='<h2>All twenty original and bubble-atlas native views</h2>'
for row in review['items']:body+=imgcard(row['path'],Path(row['path']).name+' — '+str(row['initial_mounted_score'])+'/5',row['evaluation'])
(reuse/'index.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Washing source and context review</title><style>'+css+'</style><main>'+body+'</main></html>\n',encoding='utf-8',newline='\n')

overview='<h1>Mermaid Roshan job artwork review — revision2</h1><p class="notice">The comprehensive goal remains active. This is a separately versioned review from clean baseline5b8bfb, carrying forward source8e41 artwork/evidence. The five original sealed manifests remain unchanged at their original immutable revision. No all-items4.5 pass, owner approval, finding closure, integration or release is claimed.</p><nav><a href="../job_artwork_refinement_live/all_items.html">Search1,386 known source/pose/prop entries</a><a href="../job_artwork_refinement_live/index.html">Read-through job library</a><a href="../day_two_wash_bubble_reuse_v1_20261001/index.html">New washing source/context audit</a><a href="MANIFEST_V2.json">Compact sourceA manifest representation</a><a href="SOURCE_A_REMOTE_VERIFICATION.json">SourceA anonymous verification receipt</a><a href="HOSTED_A_FAILURE_STATE.json">SourceA hostedCI failure</a><a href="CARRY_FORWARD_RECEIPT.json">Distinct-workspace and file-map proof</a></nav><section><h2>Current qualifications</h2><p>The existing register contains481 source priorities at or below4.5 and463 unassigned current source opinions. It catalogues1140 source files,240 pose cells and6 pool regions; shared candidates do not prove exhaustive actual job use. Whole pool actions4.2, boxing guard/imp4.2 and belt4.0 remain open even where individual replacement art is4.6. New washing evidence adds28 direct native initial views and two fresh generated foam attempts; complete washing sequences are unreviewed.</p><p>SourceA was anonymously fetched with normal TLS: all9583 unique declared files,3606378193 bytes and five original manifests matched exact hashes. Its local82/82 full suite preceded manifest sealing. Hosted run36921926232 then failed the existing2D scan because five large JSON manifests exceeded the4MiB scan limit. The new separately named manifest is3714044 bytes and preserves all sourceA file/dependency records. Current V2 gates and publication remain pending; the scanner and baseline have not been weakened.</p></section><section><h2>Reversible refinement</h2><p>Original art, failed attempts, earlier native captures and source hashes remain inspectable. Washing foam attempt1 is4.4 and retained rejected; attempt2 source/display style is4.6 but doctor context3.0 and nursery context3.2 require placement and literal-subject repairs. Existing painted shell-sink art is a source reuse candidate. Refreshing source fingerprints requests re-review and never assigns acceptance.</p><p><code>python -B tools/refresh_job_artwork_status.py</code></p></section>'
(out/'index.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Jobs artwork review revision2</title><style>'+css+'</style><main>'+overview+'</main></html>\n',encoding='utf-8',newline='\n')

families=['audit/day_one_pool_live_refinement_v2_20261001','assets_src/imagegen/day1_playroom_sign_v2_20261001','audit/day_two_boxing_puff_reuse_v1_20261001','assets_src/imagegen/day2_boxing_single_gloves_v1_20261001','audit/day_two_boxing_live_refinement_v1_20261001']
changed=[]
for prefix in families:
    p=r/prefix/'index.html';text=p.read_text(encoding='utf-8');link=os.path.relpath(out/'MANIFEST_V2.json',p.parent).replace('\\','/')
    updated=text.replace('href="MANIFEST.json"','href="'+link+'"').replace("href='MANIFEST.json'","href='"+link+"'")
    if updated!=text:p.write_text(updated,encoding='utf-8',newline='\n');changed.append(p.relative_to(r).as_posix())
p=r/'audit/job_artwork_refinement_live/index.html';text=p.read_text(encoding='utf-8')
needle='<h1>Mermaid Roshan jobs artwork — live review entry</h1>'
addition='<p><a href="../job_review_v2_20261001/index.html">Distinct review revision2 and preserved sourceA verification/hosted failure</a> · <a href="../day_two_wash_bubble_reuse_v1_20261001/index.html">Washing: all28 native initial views, fresh foam4.6 source and unresolved context/subject priorities</a></p>'
assert needle in text and addition not in text
p.write_text(text.replace(needle,needle+addition),encoding='utf-8',newline='\n');changed.append(p.relative_to(r).as_posix())

ledger=r/'design/05_DOC_LEDGER.md';text=ledger.read_text(encoding='utf-8')
old='current full321-source retry has81/82 green processes: pool passes after helper-only repair, picture-games exits127; exact unchanged direct retry passes but a fresh fullsuite remains required.'
new='sourceA full325-source retry passes82/82 with literal source hashes unchanged before manifest sealing; all54 raw engine diagnostics and earlier81/82 failures remain inspectable. SourceA hosted run36921926232 subsequently fails the2D scanner on five oversized review JSON manifests; distinctV2 metadata gates and exact-head hosted evidence remain pending.'
assert old in text;text=text.replace(old,new)
text+='\n| `audit/job_review_v2_20261001/index.html` | 🟣 | `CANDIDATE`; distinct review representation from clean5b8bfb, retaining immutable8e41 artwork/evidence and untouched original sealed manifests. Compact V2 preserves all9583 sourceA file/dependency records; normal-TLS anonymous original-byte receipt is separate from original hosted-red and pending current V2 gates. Comprehensive source/context/action and owner/device/child acceptance remain open. |\n| `audit/day_two_wash_bubble_reuse_v1_20261001/index.html` | 🟣 | `CANDIDATE`; all28 complete initial native doctor/nursery views directly reviewed. Existing bubble reuse below target, fresh foam1 rejected4.4 and fresh foam2 source/display4.6 unbound. Doctor context3.0, nursery context3.2, doctor subject2.9 and nursery skipped subject2.2 remain priorities. Existing painted sink first cell4.6 is a reuse source opinion, not mounted/action acceptance. Complete wash, ordinary routes, phone/child/owner acceptance pending. |\n'
ledger.write_text(text,encoding='utf-8',newline='\n');changed.append(ledger.relative_to(r).as_posix())
master=r/'audit/MASTER_AUDIT_2026-08-09.md';text=master.read_text(encoding='utf-8');needle='## 0. Planning entry\n'
assert needle in text
para='\nDistinct job-art review revision2 (2026-10-01): [new review entry](job_review_v2_20261001/index.html) preserves the immutable8e41 packet and its all9583-file anonymous verification. HostedA failed on five oversized review JSON manifests; new compact representation is separately named and keeps the complete original file maps, with current gates pending. [Washing source/context audit](day_two_wash_bubble_reuse_v1_20261001/index.html) directly evaluates28 initial native views, retains rejected foam4.4 and unbound fresh matte foam4.6 source/display art, and names doctor anchor3.0, nursery context3.2, doctor subject2.9 and missing nursery wash subject2.2. Existing painted sink source reuse4.6 is not complete-action approval. [Impact](../design/audit_impacts/job-review-separate-v2-20261001.json). All-job/source/action, ordinary-route, device/child/owner and final comprehensive report remain incomplete; no finding closure.\n'
master.write_text(text.replace(needle,needle+para,1),encoding='utf-8',newline='\n');changed.append(master.relative_to(r).as_posix())
active=r/'audit/findings/ACTIVE_FINDINGS_2026-08-13.md';text=active.read_text(encoding='utf-8')
for finding,event in [('MA-VIS-006','2026-10-01: distinct [V2 job-art review](../job_review_v2_20261001/index.html) preserves sourceA hashes and original hosted-red evidence; all28 initial washing views directly reviewed, source/display foam4.6 remains unbound, and doctor/nursery placement/subject scores stay below target. Full actions, all-jobs/ordinary routes and external acceptance remain open.'),('MA-2D-002','2026-10-01: sourceA hosted run36921926232 rejects five oversized review JSON manifests as scan-coverage debt. Distinct [V2 representation](../job_review_v2_20261001/index.html) preserves original immutableA manifests and all file maps at a separately named path below the existing scan limit; new current inventory/gates pending. No scanner/manifest waiver, strict satisfaction or lifecycle closure.')]:
    start=text.index('## '+finding+'\n');end=text.find('\n## ',start+4);end=len(text) if end<0 else end
    section=text[start:end];lines=section.splitlines(True);found=False
    for i,line in enumerate(lines):
        if line.startswith('| history |'):
            lines[i]=line.rstrip('\n').rstrip().rstrip('|').rstrip()+' '+event+' |\n';found=True;break
    assert found;text=text[:start]+''.join(lines)+text[end:]
active.write_text(text,encoding='utf-8',newline='\n');changed.append(active.relative_to(r).as_posix())

licenses=r/'ASSET_LICENSES.md';text=licenses.read_text(encoding='utf-8')
for p in sorted(set([*foam.rglob('*.png'),*foam.rglob('*.webp'),*reuse.rglob('*.webp')])):
    rel=p.relative_to(r).as_posix();assert '| '+rel+' |' not in text
    if p.suffix=='.png':source='Built-in Codex image_gen fresh text-only foam generation; exact prompt/review and original native preserved';mods='Whole-canvas uniform normalization/padding only' if 'whole_canvas' in p.name else 'Native generator pixels preserved; unbound draft'
    else:source='Project-owned native Godot4.7.2 Mobile fixture capture; existing source identity/provenance unchanged';mods='Lossless WebP screenshot; diagnostic fixture, no complete played-route or owner approval'
    text+='\n| '+rel+' | '+source+' | Project-owned review derivative; underlying source licenses remain in their original rows | Local review provenance | '+mods+'; SHA256 '+sha(p)+' |'
text+='\n';licenses.write_text(text,encoding='utf-8',newline='\n');changed.append(licenses.relative_to(r).as_posix())
impact_path=r/'design/audit_impacts/job-review-separate-v2-20261001.json';impact=json.loads(impact_path.read_text())
newfiles=[p.relative_to(r).as_posix() for d in [out,foam,reuse] for p in d.rglob('*') if p.is_file()]
impact['files']=sorted(set(impact['files']+newfiles+changed))
impact['validation'].append({'command':'Direct complete initial-native wash and fresh-foam source/context review','result':'PENDING','evidence':'audit/day_two_wash_bubble_reuse_v1_20261001/REVIEW.json and assets_src/imagegen/day2_wash_foam_v1_20261001/NATIVE_CONTEXT_REVIEW_V2.json record28 directly inspected views and honest individual scores. Source/display4.6 is partial evidence; context/subjects and complete actions remain below target or unreviewed.'})
write(impact_path,impact)
print(json.dumps({'new_initial_views_reviewed':28,'fresh_source':4.6,'doctor_context':3.0,'nursery_context':3.2,'source_a_preserved':True,'changed_control_files':changed,'impact_files':len(impact['files'])}),flush=True)
