from pathlib import Path
import json,datetime,hashlib,shutil,copy
R=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');P=R/'audit/job_geology_painted_invitation_fit_v1_20261003'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
boards=read(P/'QA_BOARD_MANIFEST_A2.json');assert len(boards['boards'])==10
for b in boards['boards']:
 assert sha(R/b['path'])==b['sha256']
 assert all(sha(R/x['path'])==x['sha256'] for x in b['members'])
 b.update(direct_review=True,reviewed_utc=now)
boards.update(status='ALL58_SELECTED_CANVASES_DIRECTLY_REVIEWED',reviewed_utc=now)
write(P/'QA_BOARD_MANIFEST_A2.json',boards)
old=read(P/'DIRECT_REVIEW_ATTEMPT01.json');opinions=copy.deepcopy(old['individual_objects'])
notes={
'TRAY-LEFT':(4.5,'At native110px width, the shallow aqua floor, cream rim and lavender front wall remain clear; the complete contour sits on the lower support and stays away from Roshan in all four selected invitations.','Keep the conserved source; review continuous approach and phone size before binding.'),
'TRAY-MIDDLE':(4.5,'The exact shared tray is visibly separated from its neighbors and no longer crosses Roshan at the selected pan invitation in either width.','Retain source; selected clearance is not continuous travel acceptance.'),
'TRAY-RIGHT':(4.5,'The right reuse keeps a complete rim and matches the other two at native size. It clears the rival and back control.','Keep the exact reusable tray; confirm the complete approach and device composition.'),
'FOSSIL':(4.5,'The conserved golden spiral and lavender stone remain legible at105px and clear Roshan in all four selected invitations at both widths.','Retain exact source; full fossil action remains independently3.2.'),
'SUPPORT':(4.5,'Both supports retain the source painting and complete contour. Their material fits the props, but the large tray support has excessive empty area, scored separately.','Keep the painted support source; refine its scale and contents relationship.'),
'MINERAL':(4.5,'The complete cyan/lavender mineral cluster reads cleanly at130px height below the rival; no flat crystal ring remains in the substituted Library backdrop.','Preserve source; confirm continuous visibility and actual production binding later.'),
'DUPLICATION':(4.6,'Each named replacement prop has one drawing owner in this non-runtime substituted Library backdrop; no duplicate flat drawing is visible. The later Opera developer entry is unchanged production.','Keep exclusive ownership and the explicit route boundary.'),
'CLEARANCE':(4.5,'All eight native invitations show a clear gap between Roshan and the lower fossil, trays and crystal. This improves A1 overlap without changing the actor or gameplay.','Review all intervening approach frames before transferring the selected-state clearance result to production.'),
'WORK-HIDE':(4.5,'All selected working canvases hide the invitation props when the actual work surface opens. The fossil, pan and opened rooted geode remain unobscured.','Continuous hide/reveal and action contact require their own review.'),
'ROOM':(2.8,'The same flat angular wall bands, navy field and triangular spotlights remain. Painted props cannot pass this room composition.','Rebuild the named room weakness using compliant native coverage after inventory; do not claim upsampled resolution as native.'),
'WHOLE':(4.0,'A2 improves actor clearance and retains readable painted props. The oversized empty support and flat room still weaken the whole invitation; current work contact and actions remain below floor.','Preserve A2 and refine the support arrangement; do not bind or approve the whole job from this trial.')}
for o in opinions:
 key=o['id'].replace('FIT-A1-','');score,evaluation,refinement=notes[key]
 o.update(id='FIT-A2-'+key,score=score,priority=score<=4.5,evaluation=evaluation,refinement=refinement,owner_acceptance=None,lane='nonruntime_counterfactual_selected_fit')
opinions.append(dict(id='FIT-A2-SUPPORT-SCALE',label='Large support versus three small trays',score=3.8,priority=True,evaluation='At both native widths, the trays use only the lower band of a430×178.5 slab. Its broad empty upper field dominates these small specimens and makes the invitation feel oversized.',refinement='Try three small conserved stone supports, one per tray, with a shared baseline and unchanged tray sources. Capture and review again without altering production.',owner_acceptance=None,lane='nonruntime_counterfactual_selected_fit'))
views=[];details=[]
for w in [1280,1600]:
 rows=read(P/f'attempt02/CAPTURE_{w}.json')['views'];assert len(rows)==29
 for i,x in enumerate(rows):
  assert sha(R/x['path'])==x['sha256']
  x=copy.deepcopy(x);x.update(direct_review=True,reviewed_utc=now,whole_canvas_score=4.0 if i in [1,4,11,17] else (2.8 if i==27 else 4.0),qualification='Selected full canvas only. Improved lower props apply to Library invitations; Opera developer entry remains unchanged production. Actual work contact/action scores stay separately below floor.')
  views.append(x)
  if i in [1,4,11,17]:details.append(dict(path=x['path'],sha256=x['sha256'],viewport=x['viewport'],phase_index=x['phase_index'],direct_review=True,scope='Complete original native canvas, not a cropped detail.'))
write(P/'DIRECT_REVIEW_ATTEMPT02.json',dict(status='SELECTED_CLEARANCE_IMPROVED_WHOLE_ROOM_AND_SUPPORT_BELOW_FLOOR',reviewed_utc=now,selected_views=58,boards=10,native_details=details,whole_fit_score=4.0,individual_objects=opinions,views=views,qualification='All58 selected full canvases on10 complete boards and all8 original native invitation canvases directly inspected. Non-runtime Library backdrop only; no intervening motion/device/child/owner/current production approval. Later Opera developer entry is actual unchanged flat production. All783 production hashes remain unchanged. A1 exact failed layout is preserved.',owner_acceptance=None,runtime_binding=False))
shutil.copyfile(Path(__file__),P/'review_tools'/Path(__file__).name)
ip=R/'design/audit_impacts/job-geology-painted-invitation-fit-20261003.json';d=read(ip);d['files']=sorted(set(d['files'])|{x.relative_to(R).as_posix() for x in P.rglob('*') if x.is_file()});write(ip,d)
print('A2_ALL58_SELECTED/10BOARDS/8NATIVE_DIRECT|CLEARANCE4.5|SUPPORT_SCALE3.8|WHOLE4.0|UNBOUND')
