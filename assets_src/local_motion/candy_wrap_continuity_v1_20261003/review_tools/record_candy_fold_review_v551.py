from pathlib import Path
import datetime,hashlib,json,shutil
B=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
P=B/'assets_src/local_motion/candy_wrap_continuity_v1_20261003';Q=P/'comparison_a2';A=Q/'attempt01'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def write(p,d):
 n=p.with_name(p.name+'.v551_next');n.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n');n.replace(p)
idx=read(A/'INDEX.json');assert len(idx['frames'])==41 and len(idx['boards'])==7
assert all(sha(B/x['path'])==x['sha256'] for x in idx['frames']+idx['boards']+idx['outputs'])
notes=[
 'Intact far-edge grip and opposite mitten beside the exposed oval; starting tableau only.',
 'Both hand contacts persist; no flap crosses the sweet.',
 'Head and bow begin tiny contour changes while the grasp stays fixed.',
 'Far flap remains upright at the same grip; red surface wholly exposed.',
 'No forward hand travel or flap rotation toward the viewer.',
 'The gold sheet remains spread flat around the exposed sweet.',
 'Left grip and right support remain readable; no useful fold begins.',
 'Cap and bow shimmer slightly while the task silhouette stays unchanged.',
 'Tiny light smears appear outside the cap; paper still open.',
 'Right mitten continues bracing beside the same uncovered oval.',
 'Head and sleeve contours fluctuate without corresponding work.',
 'Far flap has not advanced beyond its starting raised edge.',
 'No semantic closure is visible at one-half second.',
 'The native detail confirms both mittens hold their initial positions.',
 'Cap/bow perimeter softens; golden paper remains on the tabletop.',
 'Paper highlight flicker does not represent a material fold.',
 'Forearms remain connected; the sweet stays exposed.',
 'Stationary grip continues beyond the intended action midpoint.',
 'No forward travel of the held far-long edge.',
 'Body details vary slightly; no paper covers the red surface.',
 'The left flap crease stays local to the grip.',
 'Right support remains beside the sweet; no fold payoff.',
 'Outer gold-sheet contour is still fully spread and rectangular.',
 'Task contact stays at the same initial far-edge corner.',
 'Native detail at one second confirms the oval remains wholly exposed.',
 'No far-edge-over-belly or final seam is formed.',
 'Mittens remain attached but motion has stalled.',
 'Gold highlights shimmer while the paper geometry remains open.',
 'The model changes incidental costume contour rather than the requested flap.',
 'The sweet remains exposed as the requested closure interval ends.',
 'There is no covering flap across the red oval.',
 'Same raised corner held, opposite mitten remains beside the candy.',
 'Late cap and bow outlines change slightly; no paper sweep.',
 'Left mitten has not moved forward over the same sweet.',
 'No end-state enclosure despite the retained gold-paper material.',
 'The exposed oval and spread sheet still repeat the initial task layout.',
 'No closure exists before the final four frames.',
 'Both grips stay fixed; this is an ineffective hold rather than the specified action.',
 'Paper remains open and costume contours continue minor drift.',
 'Final approach still provides no covering flap or useful payoff.',
 'Final full native confirms the original red oval remains uncovered; far-edge fold fails.'
]
frames=[]
for x,n in zip(idx['frames'],notes):
 i=x['index'];score=4.5 if i==0 else (4.3 if i<=12 else 4.2 if i<=28 else 4.0)
 frames.append(dict(**x,visual_frame_score=score,evaluation=f"Frame {i} at {x['timestamp_seconds']:.3f}s: {n} Individual reference-canvas opinion only; not a useful-action or in-game pass.",direct_native_board_review=True,full_native_detail_review=i in [13,24,40],runtime_bound=False,owner_acceptance=None))
opinions=[
 ('identity_and_costume',4.3,'Recognizable child/costume persist. Cap, bows, face and costume contours shimmer; attractive individual frames do not establish useful work.'),
 ('connected_mittens',4.4,'Exactly two mittened hands remain connected through sleeves. Their stationary topology is stronger than the missing action.'),
 ('starting_far_edge_grip',4.4,'Left mitten holds a raised far-paper crease; right mitten supports beside the oval. This is a useful starting pose only.'),
 ('far_edge_forward_fold',1.5,'No continuous forward/downward sweep. Every frame leaves the same red oval exposed; the prescribed verb is absent.'),
 ('sweet_support',4.4,'Same sweet remains supported on the paper/worktop; it is not lifted or dropped. Support alone cannot pass wrapping.'),
 ('closed_belly_payoff',1.5,'The endpoint repeats an open sheet. No gold flap covers the oval and no enclosing seam exists.'),
 ('contact_and_prop_stability',4.1,'Broad grip/support layout remains stable, but tiny outline/highlight changes are not measured anchor compliance or a material fold.'),
 ('attention',3.8,'Eyes remain generally open with a fixed expression; no sustained task-specific attention beat explains a meaningful hand change.'),
 ('gold_paper_and_table',4.3,'Warm gold crinkled sheet and lavender support agree broadly with the wrapper style. Material resemblance is insufficient when the sheet never wraps.'),
 ('whole_far_fold_component',1.8,'Rejected: required far-edge fold and closed-belly payoff are absent throughout all 41 native canvases. Do not average the stronger identity/support scores into action acceptance.')
]
review=dict(status='ALL41_NATIVE_FRAMES_REVIEWED_FAR_FOLD_COMPONENT_REJECTED',reviewed_utc=now(),prompt_id=idx['prompt_id'],native_frame_count=41,boards_reviewed=[x['path'] for x in idx['boards']],full_native_details=[13,24,40],individual_frames=frames,component_opinions=[dict(item=i,score=s,evaluation=e,runtime_bound=False,owner_acceptance=None) for i,s,e in opinions],whole_component_score=1.8,runtime_integration=False,owner_approval=None,qualification='All seven original-size boards inspected in order and three full native details inspected separately. This is a local motion reference substep only. No useful fold occurs; neck grip, counter-twist and release were outside this component and remain required for the original complete wrapping goal. No cinematic delivery, source-score transfer, ordinary game/route/device/child/owner acceptance.')
write(A/'DIRECT_REVIEW.json',review)
write(Q/'REVIEW_STATUS.json',dict(status=review['status'],whole_component_score=1.8,native_frames_reviewed=41,review_path=(A/'DIRECT_REVIEW.json').relative_to(B).as_posix(),runtime_integration=False,owner_approval=None))
s=read(P/'REVIEW_STATUS.json');s.update(native_frames_reviewed=82,far_fold_component_score=1.8,far_fold_component_status='REJECTED_NO_FOLD',far_fold_review=(A/'DIRECT_REVIEW.json').relative_to(B).as_posix());write(P/'REVIEW_STATUS.json',s)
shutil.copyfile(__file__,P/'review_tools'/Path(__file__).name)
ip=B/'design/audit_impacts/job-candy-local-wrap-continuity-20261003.json';d=read(ip)
wrong=d['validation'][-1]
assert wrong['command']=='Developed local quiet-idle FIFO Candy A1 and exact native output archival'
write(Q/'ARCHIVER_METADATA_CORRECTION.json',dict(corrected_utc=now(),original_entry=wrong,reason='A2 archiver inherited an A1 validation label/evidence pointer. Native A2 bytes and all 41 outputs are independently verified; metadata correction does not rerender or change pixels.'))
d['validation'][-1]=dict(command='Developed local quiet-idle FIFO Candy far-fold A2 and exact native output archival',result='PASS',evidence=(A/'RENDER_RECEIPT.json').relative_to(B).as_posix())
d['validation'].append(dict(command='Direct original-size review of all 82 A1/A2 native canvases, 14 boards and six full native details',result='FAIL',evidence='A1 whole2.4 and A2 far-fold1.8 rejected; both DIRECT_REVIEW.json registers retained. No production binding.'))
d['files']=sorted(set(d['files'])|{x.relative_to(B).as_posix() for x in P.rglob('*') if x.is_file()});write(ip,d)
L=B/'audit/job_artwork_refinement_live';reg=read(L/'ALL_ITEMS.json')
print(json.dumps({'a2_reviewed':41,'component_score':1.8,'registry_counts':reg['counts'],'registry_refresh':reg['refresh_command'],'source_row_example':next(x for x in reg['items'] if x['id']=='CANDY-M-A10-STATE-1'),'M_summary_example':read(B/'assets_src/imagegen/candy_wrap_contact_v1_20261003/COMPLETE_SOURCE_REVIEW.json')['sources'][-1]},ensure_ascii=False))
