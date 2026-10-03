from pathlib import Path
import json,datetime,hashlib,shutil,copy,html
R=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');P=R/'audit/job_geology_painted_invitation_fit_v1_20261003';L=R/'audit/job_artwork_refinement_live'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
now=datetime.datetime.now(datetime.timezone.utc).isoformat();bm=read(P/'QA_BOARD_MANIFEST_A3.json');assert len(bm['boards'])==10
for b in bm['boards']:
 assert sha(R/b['path'])==b['sha256'] and all(sha(R/x['path'])==x['sha256'] for x in b['members'])
 b.update(direct_review=True,reviewed_utc=now)
bm.update(status='ALL58_SELECTED_CANVASES_DIRECTLY_REVIEWED',reviewed_utc=now);write(P/'QA_BOARD_MANIFEST_A3.json',bm)
opinions=copy.deepcopy(read(P/'DIRECT_REVIEW_ATTEMPT02.json')['individual_objects'])
for o in opinions:
 key=o['id'].replace('FIT-A2-','');o['id']='FIT-A3-'+key
 if key=='SUPPORT':o.update(evaluation='Four complete painted supports retain the conserved slab source and correct aspect: one beneath the fossil and one beneath each tray. Each140px tray support leaves a readable border without dominating the invitation.',refinement='Keep conserved source and selected arrangement; review all approach/hide/reveal frames before production binding.')
 elif key=='SUPPORT-SCALE':o.update(score=4.5,priority=True,evaluation='Three140×58.1 stones replace the excessive430×178.5 slab. Each110px tray is centered on one support; all native invitations show clear separation, coherent scale and a shared lower lane.',refinement='Retain the selected arrangement; verify continuous transitions, phone layout and actual production after any future binding.')
 elif key=='WHOLE':o.update(score=4.2,priority=True,evaluation='A3 retains clear painted props and actor clearance, and removes the oversized empty tray support. The broad flat wall bands and angled spotlights still dominate the whole space. Whole action contact remains independently2.7.',refinement='Keep the successful individual prop sources/selected layout. Rebuild the named room weakness and review complete approach/work/return before whole-job acceptance.')
 else:
  o['evaluation']=o['evaluation'].replace('lower support','individual lower support').replace('same flat angular','unchanged flat angular')
  o['refinement']=o['refinement'].replace('Keep the conserved source','Keep the exact conserved source')
 o.update(owner_acceptance=None,lane='nonruntime_counterfactual_selected_fit',reviewed_utc=now)
views=[];details=[]
for w in [1280,1600]:
 rows=read(P/f'attempt03/CAPTURE_{w}.json')['views'];assert len(rows)==29
 for i,x in enumerate(rows):
  assert sha(R/x['path'])==x['sha256'];x=copy.deepcopy(x)
  x.update(direct_review=True,reviewed_utc=now,whole_canvas_score=4.2 if i in [1,4,11,17] else (2.8 if i==27 else 4.0),qualification='Selected whole canvas only. A3 painted props apply to Library invitations; later Opera developer entry remains unchanged production. Work/action/contact and full travel are separate.')
  views.append(x)
  if i in [1,4,11,17]:details.append(dict(path=x['path'],sha256=x['sha256'],viewport=x['viewport'],phase_index=x['phase_index'],direct_review=True,scope='Complete original native canvas inspected, not cropped detail.'))
review=dict(status='SELECTED_PROP_MATERIAL_SCALE_CLEARANCE_AT_FLOOR_WHOLE_ROOM_BELOW',reviewed_utc=now,selected_views=58,boards=10,native_details=details,whole_fit_score=4.2,individual_objects=opinions,views=views,qualification='Every58 selected native full canvas on10 boards and all8 full native invitation canvases directly inspected. Non-runtime Library backdrop only. Source/material and selected scale/clearance floors4.5 remain inclusive priorities; whole room4.2 belowfloor. No continuous approach/device/child/owner/current production acceptance. All783 production sources unchanged. A1 and A2 originals/failures and fixture sources retained.',owner_acceptance=None,runtime_binding=False)
write(P/'DIRECT_REVIEW_ATTEMPT03.json',review)
page=P/'index.html';s=page.read_text();assert s.count('</main></html>')==1
block='<section><h2>A3: three small painted supports</h2><p>Every58 selected full canvas and8 original native invitations reviewed. Tray/support scale4.5, source materials4.5 and selected clearance4.5 provisional; whole composition4.2 remains below the floor because the room is still flat. Current production is unchanged. A1/A2 history stays visible above.</p><a href="DIRECT_REVIEW_ATTEMPT03.json">All12 individual A3 opinions and58 native views</a> · <a href="SMALL_SUPPORT_PLAN_V448.json">Exact conserved-source placement and original A2 fixture hashes</a></section><section><h2>A3 individual evaluations</h2><div class="grid">'
for o in opinions:block+='<article id="'+o['id']+'"><h3>'+html.escape(o['label'])+'</h3><p><strong>'+str(o['score'])+'/5</strong> · selected non-runtime fit</p><p>'+html.escape(o['evaluation'])+'</p><p>'+html.escape(o['refinement'])+'</p></article>'
block+='</div></section><section><h2>All58 selected A3 full canvases</h2><div class="grid">'
for x in views:
 path=x['path'].removeprefix(P.relative_to(R).as_posix()+'/');block+='<article><figure><a href="'+path+'"><img loading="lazy" src="'+path+'" alt="A3 complete '+str(x['viewport'][0])+' canvas '+x['state']+'"></a><figcaption>'+str(x['viewport'][0])+'px · '+x['state']+' · selected view</figcaption></figure><code>'+x['sha256']+'</code></article>'
block+='</div></section>';s=s.replace('</main></html>',block+'</main></html>');s=s.replace('Both trials remain unbound and separately preserved.','A1 and A2 remain separately preserved. A3 small supports now meet selected scale/clearance4.5; whole room4.2 remains below floor and all replacements remain unbound.');page.write_text(s,encoding='utf-8',newline='\n')
d=read(L/'ALL_ITEMS.json');q=next(x for x in d['items'] if x['id']=='GEO-TRAY-SOURCE-01');q['evaluation']+=' All58 A3 selected canvases and8 complete native invitations reviewed: source/selected scale/clearance4.5, whole room4.2. Three small conserved supports remove A2 oversized support3.8. Production unbound; all actual current tray/room/contact/action scores remain separate.';q['refinement']='Retain exact native and selected A3 arrangement. Normalize whole canvas to<=1024 before runtime import; capture complete approach/hide/reveal and actual production after any binding. Whole room/contact/actions remain priorities.';q['original_reports'].append(P.relative_to(R).as_posix()+'/index.html');d['updated_utc']=now;write(L/'ALL_ITEMS.json',d)
for p in [R/'audit/MASTER_AUDIT_2026-08-09.md',R/'audit/findings/ACTIVE_FINDINGS_2026-08-13.md']:
 s=p.read_text();needle='Known572 source-file priorities include570 primary sources and two runtime-source entries.';assert s.count(needle)==1;s=s.replace(needle,needle+' A3 three-small-support trial: all58 selected canvases/8 native invitations inspected; selected materials/support scale/clearance4.5 provisional, whole room4.2 remains weak. All originals and unbound route/continuous-motion boundaries retained.');p.write_text(s,encoding='utf-8',newline='\n')
p=R/'design/05_DOC_LEDGER.md';s=p.read_text();s+='\n| `audit/job_geology_painted_invitation_fit_v1_20261003/DIRECT_REVIEW_ATTEMPT03.json` | 🟢 | `SUPPORTING_CURRENT`; all58 selected A3 canvases/10 boards/8 complete native invitations reviewed, materials/selected support scale/clearance4.5 provisional, whole room4.2. Three small conserved supports; unbound non-runtime fixture, no continuous travel/device/child/owner/current production acceptance. A1/A2 retained. |\n';p.write_text(s,encoding='utf-8',newline='\n')
shutil.copyfile(Path(__file__),P/'review_tools'/Path(__file__).name)
ip=R/'design/audit_impacts/job-geology-painted-invitation-fit-20261003.json';d=read(ip);d['files']=sorted(set(d['files'])|{x.relative_to(R).as_posix() for x in P.rglob('*') if x.is_file()});d['validation'].append(dict(command='Direct review A3 all58 selected canvases/10 ordered boards/8 complete native invitations',result='PASS',evidence='audit/job_geology_painted_invitation_fit_v1_20261003/DIRECT_REVIEW_ATTEMPT03.json: selected material/scale/clearance4.5; whole room4.2 still fails, no production/owner acceptance.'));write(ip,d)
print('A3_ALL58_SELECTED/10BOARDS/8NATIVE_DIRECT|SELECTED_SCALE_CLEARANCE4.5|WHOLE4.2|ROOM2.8|UNBOUND')
