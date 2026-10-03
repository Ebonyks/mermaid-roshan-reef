from pathlib import Path
import ast
R=Path('C:/Users/Peter/Documents/mermaid-roshan-reef/tmp')
s=(R/'review_candy_release_v643.py').read_text(encoding='utf-8')
notes=[
'Entry shows two sleeve-owned coral mittens holding the short untwisted gold pleats. One covered oval and both broad fans rest on the table; no torque yet.',
'Both neck contacts retain the entry pose and the same open pleats. This is a stable grip still, not an opposing twist.',
'Hands stay in their original orientations. The central sweet remains opaque and the loose neck pleats remain parallel.',
'Small texture changes occur while both mittens stay on their neck groups; no readable wrist roll or paper winding.',
'Two connected mittens remain at the original contacts. Both fans retain their broad spread with open pleats between them and the body.',
'Entry hold continues. The source hand orientations and open gold neck folds remain unchanged at the intended action start.',
'During the instructed twist interval both hands still face as at entry. Paper pleats have not wound into a short closure.',
'Small painted variation appears on the central body, but each mitten keeps the same near-front orientation and own neck contact.',
'The covered central body remains low. Both untwisted pleat groups and broad fans persist without an opposite rotational consequence.',
'Two principal mittens and their sleeve cuffs remain coherent. The desired left-under/right-over wrist pairing is not visible.',
'Hands continue holding rather than visibly rotating. The short neck pleats stay long and horizontally parallel.',
'The left thumb contour varies slightly, but this does not establish a continuing opposite wrist turn or a paper closure.',
'Both neck grips remain broadly stable. Neither gold neck has acquired the short diagonal winding visible in the target endpoint.',
'Same supported candy and two spread fans remain. The right mitten back has not rolled diagonally across its neck.',
'Left thumb/neck contact changes slightly while the main mitten retains its orientation; right wrist remains near the entry angle.',
'The two hands still hold the pleats without visibly rolling oppositely. Paper folds stay open at both sides of the oval.',
'Small changes in left thumb highlight do not provide a readable torque arc. Both cuffs remain attached and fans conserved.',
'Supported central oval remains covered. No finished short twist or substantial opposite hand orientation appears.',
'Both wrists remain close to the original pose at the middle of the action. Gold neck folds are still parallel and loose.',
'Neck contacts stay intact, but the pictured left-under/right-over endpoint has not been reached. This remains a hold.',
'Hands and fans retain the entry arrangement with minor painted shimmer. No causal contact-to-winding change.',
'Both mittens remain sleeve-owned and touching their own pleats. The parallel gold folds do not close into diagonal twists.',
'Neither wrist shows the specified opposed roll; the covered central body and spread fans remain stable.',
'Late action still contains long open neck pleats. Contact stability is useful but cannot pass the missing twist.',
'Hands continue their hold while the face begins changing and the head lowers. Working material still has no short wound closures.',
'Eye/head acting grows with the same hand and wrapper pose. The generated motion is concentrated in expression rather than the wrists.',
'Eyelids lower and mouth changes. Both neck groups remain untwisted; no clear opposed wrist movement accompanies the acting.',
'Head dips and eyes nearly close while the two mittens keep their original neck positions and orientations.',
'Closed/downward eyes and changed mouth persist. Gold neck folds are still loose parallel lines, not the target short opposite windings.',
'Unrequested facial acting continues while both sleeve-owned mittens remain static at their grips. The candy stays supported.',
'At the intended finished hold, both gold necks remain open. Head/eye acting cannot substitute for physical paper closure.',
'The face is still lowered and partially closed-eyed, but hand orientation and gold pleat structure remain near entry.',
'Both fans stay attached and the central oval stays covered. No finished opposite twist has occurred before the hold.',
'Hands preserve grip ownership without a visible torque trajectory; short diagonal windings are still absent.',
'Head rises slightly and eyes begin reopening. Both wrists and long parallel neck pleats remain effectively unchanged.',
'Eyes reopen with an altered mouth, while the two hands still hold the same loose fold groups rather than two finished twists.',
'Late pose returns toward entry expression. Hand topology remains broadly coherent, but paper closure is still missing.',
'Both mitttens remain at their initial contacts; the right mitten back never rolls across the neck as specified.',
'Near-final canvas retains two attached fans and a supported covered oval. Neither short gold neck is wound closed.',
'Final approach still reads as a steady hold, with minor pose/texture variation. The requested opposite rotational action remains absent.',
'Endpoint returns a nearly unchanged two-hand grip with open parallel neck folds, not two short diagonal twists. Rejected as a twist component despite useful hand/fan conservation.'
];assert len(notes)==41
ops=[
('exactly_two_principal_hand_groups',4.6,'Two principal mittens remain connected to their own sleeves; no extra operator or detached coral hand remnants appear in this bounded study.'),
('sleeve_cuff_mitten_topology',4.4,'Both cuffs and rounded mittens remain broadly coherent. Small thumb/cuff contour changes still require owner and actual-game identity review.'),
('left_short_neck_grip',4.4,'Left hand retains its own loose pleat group throughout. Stable holding does not demonstrate thumb-under wrist rotation or a finished twist.'),
('right_short_neck_grip',4.4,'Right mitten stays with its own pleat group and outside fan. Its quilted back never makes the required across-neck roll.'),
('opposed_wrist_rotation',1.2,'Neither wrist visibly executes the instructed opposite roll. Minor contour variation and head acting cannot count as a contact-driven rotational action.'),
('short_opposite_paper_winding',1.1,'Both gold neck groups remain long parallel open pleats. They do not become the short diagonal opposite windings seen in the source target endpoint.'),
('single_wrapper_fan_conservation',4.3,'Both broad gold fans stay continuously attached outside the hands. Small silhouette/texture variation remains, but the earlier cuff-fan fusion is absent here.'),
('covered_oval_identity',4.4,'One central gold oval stays covered and opaque. No new sweet or exposed red centre appears, though slight size/paint variation remains.'),
('table_support',4.4,'The central body stays low on the same purple worktable; there is no lift/drop. Full contact/body registration in actual gameplay remains unassigned.'),
('character_scene_registration',3.8,'Entry placement mostly holds, but late head/eyes/mouth acting and modest contour changes distract from the absent wrist action.'),
('finished_twist_held_endpoint',1.2,'Final pose still holds loose parallel neck folds with near-entry hand orientations. The required finished short twists are absent.'),
('whole_opposed_twist_component',2.2,'Rejected: coherent grips, fans and table support improve conservation, but the defining opposed wrist motion and paper winding never occur.')
]
s=s.replace("M=P/'release_a1'","M=P/'twist_a1'").replace('v643_next','v644_next')
start=s.index('notes=[');end=s.index("index=read(A/'INDEX.json')",start);s=s[:start]+'notes='+repr(notes)+';assert len(notes)==41\n'+s[end:]
start=s.index('ops=[');end=s.index('\nreview=dict(',start);s=s[:start]+'ops='+repr(ops)+s[end:]
s=s.replace("4.3 if i<10 else (3.8 if i<14 else (2.1 if i<17 else (1.5 if i<25 else 1.2)))","4.3 if i<24 else 3.8")
s=s.replace('REJECTED_DETACHED_CORAL_THUMB_AND_BROKEN_CUFFS_NO_QUIET_REST','REJECTED_STABLE_GRIPS_BUT_NO_OPPOSING_WRIST_ROLL_OR_PAPER_CLOSURE').replace("stage='release'","stage='twist'").replace('whole_component_score=1.7','whole_component_score=2.2').replace("m['component_motion_score']=1.7","m['component_motion_score']=2.2")
s=s.replace('Complete local release reference frame','Complete local twist reference frame').replace('Gold-wrapper supported release — rejected1.7','Gold-wrapper opposite twist — rejected2.2').replace('Supported release component — rejected1.7/5','Opposite wrist-twist component — rejected2.2/5')
s=s.replace('All41 complete decoded896×512 canvases and12 component opinions were directly reviewed. The sweet stays supported and its fans broadly conserved, but withdrawal leaves extra coral thumb material and distorts the cuffs. Late palms rise into a display pose rather than a quiet coherent rest.','All41 complete decoded896×512 canvases and12 component opinions were directly reviewed. Both hands retain their grips and fans remain attached, but neither wrist performs the opposing roll and the neck pleats never wind closed. The principal motion is unrequested facial acting.')
s=s.replace('desired release endpoint','desired twist endpoint').replace('Direct every41 complete native release canvas and12 named components','Direct every41 complete native twist canvas and12 named components').replace('whole release1.7 rejected','whole twist2.2 rejected').replace('RELEASE_REJECTED1_7','TWIST_REJECTED2_2')
ast.parse(s);(R/'review_candy_twist_v644.py').write_bytes(s.encode());print('TWIST_REVIEW_TOOL_PREPARED',flush=True)
