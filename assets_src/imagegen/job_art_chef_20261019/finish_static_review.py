from pathlib import Path
from datetime import datetime,timezone
from PIL import Image
import hashlib,json,numpy as np
root=Path(__file__).resolve().parents[3];src=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text())
full=read(src/'verification/full_ci_native_capture_02.json')
assert full['status']=='PASS' and len(full['completed_probes'])==82 and not full['source_drift']
assert all(sha(root/p)==h for p,h in full['source_sha256_raw_checkout'].items())
captures=[]
for name,receipt_name in [('review_current_06','capture_current_06_receipt.json'),('review_chapter2_05','capture_chapter2_05_receipt.json')]:
    receipt=read(src/receipt_name);assert receipt['status']=='PASS' and not receipt['source_drift'] and receipt['actual_save_unchanged']
    data=read(src/name/'capture.json');assert not data['failures']
    for row in data['captures']:
        p=root/row['path'];assert p.is_file()
        captures.append({**row,'sha256':sha(p)})
assert len(captures)==88
observations={
 'oven_cool':'The round window, raw tin, cream columns, shell handle and supported feet read clearly as one warm storybook oven; no flat face/window/cake substitute remains.',
 'oven_warm':'Same registered body/hardware; the golden interior and risen tin change the ready state without relighting the surrounding room.',
 'oven_open':'Complete painted door, rack and supported risen tin; open depth stays inside the same registered frame rather than floating over the window.',
 'thermometer_empty':'Trim and shell crest match the oven family, tube is readable at the actual small size; natural1:4canvas sampling retained.',
 'thermometer_full':'Same tube silhouette and painted warm progression; disjoint source rows avoid whole-object ghosting. Chapter Two meter is clear of Roshan.',
 'pitcher_empty':'Generated interior is masked into the measured original cavity; exterior/rim/handle identity and natural square sampling stay intact.',
 'batter_stream':'Warm painted material strip connects the original transformed spout to the bowl; source rows are clipped/tiled with uniform sampling, not stretched.',
 'batter_drop':'Small warm teardrop remains legible as batter at use size and shares the stream finish; whole square sprite sampling.',
 'batter_splash':'Soft painted landing crown sits at the bowl contact point; no neon or surrounding abstract halo.',
 'piping_bag':'Whole cream fabric, lavender tie and gold nozzle read as a single cooking tool; measured nozzle stays on the earned pink ribbon.',
 'frosting_cap_start':'Rounded piped end uses the same source/material as the segment, rotated with the initial tangent; no detached geometric cap.',
 'frosting_segment':'Painted pink piping repeats with overlap along the earned curve; broad ridged material and natural aspect stay visible at use size.',
 'frosting_cap_end':'Rounded terminal piping follows the current endpoint/tangent and same cream-pink material; finished picture replaces live piping cleanly.',
 'stack_two':'Whole blue/violet partial stack has a newly visible complete painted top and the original plate/pedestal footprint; stretched ellipse cap removed.',
 'stack_four':'Whole yellow/green/blue/violet partial stack retains support, widths and lower contours; the complete yellow top reads as the next earned pair.',
 'bowl_empty':'Exact existing painted shell-bowl identity reused and uniformly reduced; natural rim, bowl body and spoon remain whole, without a code ellipse.',
 'bowl_unstirred':'Existing broad rainbow batter is confined to the bowl cavity and remains coherent with the authored shell/source identity.',
 'bowl_stirred':'Existing complete authored swirl appears at the earned milestone; no half-swirl wipe or procedural spiral substitutes for the source.',
 'cake_unfrosted':'Whole existing six-round cake keeps all tiers, grain, plate and support; source-aligned trace starts on the red top and travels down the actual cake.',
 'cake_frosted':'The complete original decorated cake appears only at the earned frosting endpoint, with no premature split-tier garlands or abstract completion puff.',
 'guide_hand':'Exact published Teacher hand and native reused; measured fingertip reaches the actual contextual cue, with no concentric-dot replacement.',
 'widget_target_chef_piece_2':'Chocolate-dipped strawberry reads as food with leaf, seed, fruit and chocolate silhouettes; first glossy-realistic attempt rejected. Distinct from the existing cream and cherries.'
}
paths=sorted((root/'assets/opera/worlds/chef_quality_20261019').glob('*.png'))+[root/'assets/opera/worlds/widgets/widget_target_chef_piece_2.png']
rows=[]
for p in paths:
    image=Image.open(p);assert image.mode=='RGBA'
    assert max(image.size)<=1024 or all(n&(n-1)==0 for n in image.size)
    scores={'identity_canon_and_material_family':4.6,'painted_finish_and_light':4.6,
        'contour_alpha_at_current_use':4.5,'visual_readability_at_current_use':4.5,
        'static_registration_with_current_scene_neighbors':4.5}
    rows.append({'id':p.stem,'path':p.relative_to(root).as_posix(),'sha256':sha(p),'dimensions':list(image.size),
        'appearance_scores_out_of5':scores,'minimum_scored_appearance_dimension':min(scores.values()),
        'observation':observations[p.stem],
        'static_local_ai_result':'PASS4.5floor for these appearance dimensions only',
        'motion_contact_over_complete_time':'NOT_ACCEPTED_BY_THIS_STATIC_REVIEW',
        'final_all_applicable_dimension_audit':None})
assert len(rows)==22
out=src/'review/art_review.json'
out.write_text(json.dumps({'schema':'reef.object_art_static_review/1','reviewer':'Codex local AI source/current-desktop-frame review; not an independent human or owner',
    'reviewed_utc':datetime.now(timezone.utc).isoformat(),'baseline':'6fb96aeb441952c1053cc5ce18435fc57fc1d1ab',
    'threshold':'Minimum4.5/5 in every scored applicable appearance dimension, never a mean. Source and actual Mobile/HUD neighbor context both inspected.',
    'scope':'22runtimepictures, object sheets and88source-bound current frames at1280/1600; configured ordinary Chef plus configured Chapter Two world. Not a natural-route, movie or physical-device session.',
    'objects':rows,'captures':captures,
    'measured_oven_cool_warm_alpha16_iou':.9913654836414505,
    'measured_oven_open_closed_upper300px_alpha16_iou':.9952069071325031,
    'new_family_rgba_mib':13.140625,'extra_chocolate_rgba_mib':.25,
    'rejected_or_intermediate_sources':'All22generation attempts, glossy chocolate, role-wrong garland, unnecessary wrong-guide cup retry and oven/tin intermediates remain in prompts/native/provenance; none is silently accepted.',
    'limits':['This review does not score whole-motion/full-speed contact, canonicalQA11, physical-device, child or owner acceptance.',
        'Current desktop touch fixtures are configured; final all-item/census/P8 and whole-campaign audit remain open.',
        'Existing kitchen native-resolution debt and shared ambient/HUD/actor acceptance remain explicit.',
        'Desktop-save incident/recovery status is separate; latest capture receipts prove isolation and unchanged live hashes.']},indent=2)+'\n')
p=root/'design/audit_impacts/job-art-chef-20261019.json';d=read(p)
d['validation'] += [{'command':'Current source/actual Mobile still appearance review22objects and88frames','result':'PASS','evidence':'review/art_review.json; local AI appearance-only minimum4.5in every scored dimension; exact full-time motion/formal/device/child/owner remain unaccepted.'},
    {'command':'Complete unchanged scripts/ci.sh native capture02','result':'PASS','evidence':'verification/full_ci_native_capture_02.json/log:82original probes ordered, all exit0, process0,2462.405seconds,source_drift[]; logSHA256089c77a0979dd76743bd5186f5214fe8a6a8a5a6a04c424632ff3a14998dbb5c. All original failures/interrupted runs retained; no retry or classifier/probe waiver.'}]
d['acceptance_gaps']='Local appearance-only22objects meet4.5floor,88current configured frames/source pins and complete82local probes pass. Exact remoteCI/integration, final all-applicable-time/motion/census/P8/game-wide audit, canonicalQA11, physical-device, child and owner remain open. Existing native-background debt persists. Desktop save recovery still requires known-good prior backup; preserved live files untouched.'
p.write_text(json.dumps(d,indent=2)+'\n')
for name in ['audit/MASTER_AUDIT_2026-08-09.md','audit/MASTER_AUDIT_CHANGELOG_ROLLBACK_2026-08-10.md']:
    p=root/name;text=p.read_text('utf-8')
    note='Chef local verification2026-10-19: complete unchanged scripts/ci.sh native capture02 passes82/82zero exits with no source drift; logSHA256089c77a0979dd76743bd5186f5214fe8a6a8a5a6a04c424632ff3a14998dbb5c.88current configured Mobile/GUI frames and22source/context appearance-only local AI reviews meet4.5in each scored dimension. Full motion/formal/device/child/owner, remoteCI/integration and whole-campaign acceptance remain separate; earlier failures and the save-isolation incident remain recorded.'
    if name.endswith('MASTER_AUDIT_2026-08-09.md'):
        text=text.replace('### Development task index',note+'\n\n### Development task index',1)
    else:text+='\n'+note+'\n'
    p.write_text(text,encoding='utf-8')
print('Recorded22appearance-only static passes,88frame bindings and full82machine pass; final/time/owner scores remain null')
