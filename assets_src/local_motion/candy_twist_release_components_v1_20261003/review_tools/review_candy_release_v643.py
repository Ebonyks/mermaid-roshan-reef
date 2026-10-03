from pathlib import Path
import datetime,hashlib,html,json
B=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');P=B/'assets_src/local_motion/candy_twist_release_components_v1_20261003';M=P/'release_a1';A=M/'attempt01'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,raw):t=p.with_name(p.name+'.v643_next');t.write_bytes(raw);t.replace(p)
def write(p,d):put(p,(json.dumps(d,indent=2,ensure_ascii=False)+'\n').encode())
notes=[
'Initial two sleeve-owned coral mittens grip the finished short gold necks. One covered oval and two broad fans rest on the purple table; this is an entry still, not proof of release.',
'Entry pose remains nearly identical: both hands contact their own necks and both fans remain attached. No separation yet.',
'Both mittens and short neck contacts remain legible. The candy stays supported with the same opaque central body.',
'Small painted texture variation occurs while the hands retain the finished-neck grips; release has not started.',
'Two rounded mittens remain at the gold necks. The fans and central oval keep their entry arrangement.',
'Hold ends with both neck contacts still present and table support intact. No clean withdrawal has occurred.',
'At the instructed release interval the pose still holds both short necks. The gold paper remains broadly conserved.',
'Both palms continue gripping; no visible purple gap opens between either mitten and its neck.',
'Supported covered oval and two attached broad fans remain clear, but the release is delayed.',
'The two connected coral mittens still own their neck contacts. This remains a hold, not a completed disengagement.',
'Hands stay at the necks while the face begins changing expression and painted facial detail; no withdrawal yet.',
'Both mittens retain the grip and the head lowers slightly. Paper remains supported but the intended simple release is not visible.',
'Eyelids and mouth visibly change while both neck contacts remain. Unrequested facial acting competes with the small working action.',
'Head and eyes continue changing. The two palms still hold, and a reliable visible release seam is absent.',
'Rapid hand withdrawal begins with smeared cuff/mitten contours. A coral thumb-like oval is left beside the left neck; the right neck grows a separate bulb.',
'Both departing hand silhouettes smear and stretch. The coral left-neck remnant stays on the table and the right gold bulb persists.',
'Main mittens begin separating above the wrapper, but the left coral lobe remains at the neck. Separation does not conserve the whole hand topology.',
'Both palms rise sharply into a display pose. The left cuff/mitten outline breaks into separate shapes and the leftover coral neck lobe remains.',
'Raised palms are distinct from the supported wrapper, but the left hand has a second coral/cuff-associated wedge below it and another coral lobe at the neck.',
'Two principal palms are upright. The extra left coral shapes remain; the right neck contains a newly enlarged bulb rather than the original short-paper winding.',
'Raised left palm, lower coral/cuff wedge and coral neck remnant are all visible together. The hand has not withdrawn as one coherent owned shape.',
'The display pose persists with the same extra coral left-hand remnants. The candy body stays covered and table-supported.',
'Both hands remain raised rather than quietly resting outside the fan tips. The left cuff and coral remnants still violate topology.',
'Upright palms hold with an extra lower left coral wedge. Fans remain attached, but clean sleeve-to-hand ownership has failed.',
'Left palm becomes taller while the lower coral wedge and neck remnant persist. Right palm remains raised; no calm supported-release endpoint.',
'Left upright mitten elongates and its cuff changes shape. Right hand begins folding down; extra left coral pieces remain beside the wrapper.',
'The left hand still reads as a tall vertical oval with a second coral wedge beneath the cuff. The right cuff turns downward outside its fan.',
'Right palm shrinks into a bent coral shape while the left upright oval and separate lower remnants remain. Coherent two-hand settle is absent.',
'Asymmetric raised-left/bent-right pose persists; the left neck still has a detached coral lobe. Wrapper fan contours remain broadly continuous.',
'Left palm stays upright with a broken lower cuff shape; the right mitten is curled down. This does not match the quiet released source endpoint.',
'Late intended rest still shows a tall raised left mitten, lower coral wedge and left-neck remnant. The right hand remains bent outside the fan.',
'No clean settle: the left glove stays vertical and overextended, while the right glove/cuff contour contracts. The central gold body stays low.',
'Right wrist and mitten show motion smearing as they lower toward the right fan. The left detached coral remnants remain unchanged.',
'Right hand rolls down close to the outer fan; left hand remains upright and split around its cuff. Both hands cannot receive a topology pass.',
'Right palm now lies low beside the fan but the left remains a tall raised oval with extra coral material at the neck.',
'The asymmetric near-hold continues. Left cuff bands and lower coral wedge fail the original simple sleeve-owned mitten design.',
'Left hand remains elongated and raised; right cuff is stretched into a low bent position. Left-neck coral remnant remains on the table.',
'Late source placement varies slightly while the same malformed glove/cuff silhouettes persist. The candy stays covered but release quality fails.',
'Right mitten moves near the right fan, while the left raised palm and separate lower remnants remain. There is no matching calm two-hand rest.',
'Final approach retains the left neck coral lobe and deformed upright glove. The right hand is low, close to the fan edge.',
'Endpoint contains one covered table-supported gold sweet, but a raised elongated left mitten, extra coral left-neck material and altered cuffs. Rejected: clean whole-hand disengagement and quiet two-hand rest are missing.'
];assert len(notes)==41
index=read(A/'INDEX.json');frames=[]
for row,note in zip(index['frames'],notes):
 assert sha(B/row['path'])==row['sha256'];i=row['index'];frames.append(dict(**row,direct_complete_native_review=True,pose_graphics_score=4.3 if i<10 else (3.8 if i<14 else (2.1 if i<17 else (1.5 if i<25 else 1.2))),evaluation=note,priority=True,whole_component_motion_score=None,current_game_score=None,owner_acceptance=None))
ops=[
('two_coherent_owned_mittens',1.3,'Two main palms rise, but additional coral shapes remain below the left cuff and at the left neck. Principal hand count alone conceals broken hand ownership.'),
('left_thumb_conservation',0.8,'From frame14 onward a coral thumb-like lobe stays at the left neck while the main mitten departs. It does not remain attached to the withdrawing hand.'),
('right_neck_material_conservation',2.5,'The right neck develops a bulb as the mitten lifts. Its former hand-contact region is not conserved as the same short flexible paper winding.'),
('sleeve_cuff_mitten_topology',1.6,'Withdrawal smears and separates the left glove/cuff contour. Late left hand becomes a long oval with a lower coral wedge; right cuff also deforms.'),
('clean_disengagement_before_withdrawal',1.8,'Both palms eventually move away, but the movement leaves coral material at the wrapper and lacks a coherent whole-hand separation seam.'),
('quiet_two_hand_rest',1.4,'Hands rise into an unrequested display pose, then settle asymmetrically. Tall upright left glove does not match the quiet relaxed endpoint.'),
('single_wrapper_and_broad_fans',4.1,'Both broad gold fans remain attached to the central wrapper throughout. Local neck bulbs and changing contours prevent a stronger material-conservation opinion.'),
('covered_oval_identity',4.3,'A single opaque gold central oval remains covered with no visible red candy reveal or extra central sweet. Modest silhouette/texture variation remains.'),
('table_support',4.2,'The central sweet remains low on the purple work surface during withdrawal. Local hand remnants and small footprint changes undermine the complete supported release.'),
('character_scene_registration',3.5,'Unrequested head/expression change and late cuff/silhouette/working-footprint drift weaken continuity against the fixed room.'),
('painted_style_and_readability',4.0,'Entry retains broad painted colour and contours; blurred withdrawal and malformed late mittens reduce clarity. The inherited busy room remains a separate4.4 source priority.'),
('whole_supported_release_component',1.7,'Rejected: preserved table support and fans do not compensate for detached thumb material, broken cuffs, elongated palms and absent quiet coherent two-hand rest.')
]
review=dict(status='REJECTED_DETACHED_CORAL_THUMB_AND_BROKEN_CUFFS_NO_QUIET_REST',reviewed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),reviewer='Codex direct complete native-frame drafting review',stage='release',native_frames_reviewed=41,boards_directly_reviewed=7,individual_frame_opinions=41,component_opinions=len(ops),frames=frames,components=[dict(id=k,score=s,evaluation=e,priority=s<=4.5) for k,s,e in ops],whole_component_score=1.7,source_still_score=4.5,current_game_wrap_score=2.8,complete_wrapping_score=None,acceptance='LOCAL_MOTION_REFERENCE_ONLY',runtime_integration=False,device_acceptance=None,child_acceptance=None,owner_acceptance=None,submitted_manifest_sha256=index['submitted_manifest_sha256'],endpoint_conditioned=False)
write(A/'DIRECT_REVIEW.json',review);write(M/'REVIEW_STATUS.json',{k:review[k] for k in ['status','reviewed_utc','stage','native_frames_reviewed','component_opinions','whole_component_score','source_still_score','current_game_wrap_score','complete_wrapping_score','acceptance','runtime_integration','owner_acceptance','submitted_manifest_sha256','endpoint_conditioned']})
m=read(M/'MANIFEST.json');m['status']=review['status'];m['visual_review']=(A/'DIRECT_REVIEW.json').relative_to(B).as_posix();m['component_motion_score']=1.7;m['complete_action_score']=None;write(M/'MANIFEST.json',m)
esc=lambda x:html.escape(str(x));rows=''.join('<tr><td>'+esc(k.replace('_',' '))+'</td><td>'+str(s)+'/5</td><td>'+esc(e)+'</td></tr>' for k,s,e in ops)
movie=next(x['path'] for x in index['outputs'] if x['path'].endswith('.mp4'));rel=lambda p:Path(p).relative_to(M.relative_to(B)).as_posix()
articles=''.join('<article id="frame%02d"><h2>Frame %d · %.3fs · pose graphics %s/5</h2><img loading="lazy" src="%s" alt="Complete local release reference frame %d"><p>%s</p><p>Complete action, current game and owner acceptance unassigned for this individual canvas.</p></article>'%(x['index'],x['index'],x['timestamp_seconds'],x['pose_graphics_score'],rel(x['path']),x['index'],esc(x['evaluation'])) for x in frames)
css='body{max-width:1120px;margin:auto;padding:24px;background:#edf3fb;color:#25334b;font:17px/1.55 system-ui}article{background:white;padding:18px;border-radius:16px;margin:24px 0}img,video{width:100%;height:auto;display:block;aspect-ratio:7/4}td,th{padding:10px;text-align:left;vertical-align:top;border-bottom:1px solid #d5e0ef}table{width:100%;border-collapse:collapse}td,p{overflow-wrap:anywhere}a{color:#164c83}'
page='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Gold-wrapper supported release — rejected1.7</title><style>'+css+'</style><h1>Supported release component — rejected1.7/5</h1><p>All41 complete decoded896×512 canvases and12 component opinions were directly reviewed. The sweet stays supported and its fans broadly conserved, but withdrawal leaves extra coral thumb material and distorts the cuffs. Late palms rise into a display pose rather than a quiet coherent rest.</p><p>Source endpoint4.5 provisional; actual in-game WRAP2.8 unchanged. This is a local motion reference with one conditioned start image. The desired release endpoint was a human QC reference, not a conditioned end image. No runtime or cinematic acceptance.</p><p><a href="../index.html">Component overview and full remaining objective</a> · <a href="attempt01/DIRECT_REVIEW.json">Every frame/component opinion</a> · <a href="checks/SUBMITTED_MANIFEST.exact.json">Exact manifest saved before dispatch</a> · <a href="attempt01/RENDER_RECEIPT.json">Actual render receipt</a></p><video controls preload="metadata" src="'+rel(movie)+'"></video><table><thead><tr><th>Component</th><th>Draft score</th><th>Evaluation</th></tr></thead><tbody>'+rows+'</tbody></table>'+articles+'</html>'
put(M/'index.html',page.encode());put(P/'review_tools'/Path(__file__).name,Path(__file__).read_bytes())
ip=B/'design/audit_impacts/job-candy-twist-release-components-20261003.json';d=read(ip);d['files']=sorted(set(d['files'])|{p.relative_to(B).as_posix() for p in P.rglob('*') if p.is_file()});d['validation'].append(dict(command='Direct every41 complete native release canvas and12 named components',result='FAIL',evidence=(A/'DIRECT_REVIEW.json').relative_to(B).as_posix()+';whole release1.7 rejected. Source4.5/current WRAP2.8 unchanged.'));write(ip,d)
print('RELEASE_REJECTED1_7|41 individually scored frames|12 components|originals preserved',flush=True)
