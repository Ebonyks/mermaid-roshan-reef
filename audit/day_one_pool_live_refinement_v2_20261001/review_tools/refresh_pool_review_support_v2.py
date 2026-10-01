from pathlib import Path
import datetime, hashlib, json, shutil

root=Path(__file__).resolve().parents[1];family=root/'audit/day_one_pool_live_refinement_v2_20261001'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
inventory_path=family/'actor_reuse_inventory_v1/INVENTORY.json';inventory=json.loads(inventory_path.read_text())
opinions=[
 (4.0,'Both arms reach toward the work, but the spread fingers and open palms do not wrap a pole. Useful attention/reach source only; not a convincing held-skimmer grasp.'),
 (4.2,'The cupped hands visibly receive an object and preserve approved identity. The fingers remain open and the two hands are not yet shown enclosing the shaft. Purpose candidate, not an accepted tool pose.'),
 (3.9,'The carry hands support a flat object on upward palms. This suggests tray carrying rather than controlling a long skimmer handle. Reject for the named grasp purpose, retain for its original approved use.'),
 (4.6,'The two forward clenched hands visibly supply a grasp shape and a useful concentrating forward lean. This is a provisional source-purpose candidate, not a mounted skimmer or accepted swim action. The original playground use is unchanged.'),
 (4.6,'The second forward closed-hand pose provides another plausible source grasp and a different tail sweep. It merits an in-context tool-fit/anchor test. No neighboring-frame continuity, authored scoop or costume pass follows from this static source opinion.')]
for row,(score,opinion) in zip(inventory['items'],opinions):
 row.update(visual_score=score,score_lane='Provisional suitability for held-skimmer grasp only; existing approved source identity/style retained',
  status='SOURCE_PURPOSE_CANDIDATE_MOUNT_PENDING' if score>4.5 else 'REJECT_FOR_SKIMMER_GRASP_PURPOSE',opinion=opinion)
inventory['status']='FIVE_SOURCE_PURPOSE_OPINIONS_MOUNT_AND_TIMING_PENDING'
inventory['acceptance']='All five exact approved source windows directly inspected. Two closed-hand poses earn provisional4.6 source-purpose opinions; three open/palm-up choices fail the specific grasp purpose3.9–4.2. No pose bound to runtime, no complete motion/wardrobe/device/child/owner approval.'
write(inventory_path,inventory)
page=family/'index.html';text=page.read_text(encoding='utf-8')
marker='<section><h2>Approved source reuse study before character generation</h2>'
assert marker not in text
section=marker+'<p>Five exact approved pose windows were inspected for the specific skimmer grasp gap. Their scores assess this new purpose. No original artwork or runtime actor binding changed.</p><div class="grid">'
for row in inventory['items']:
 rel=str(Path(row['path']).relative_to('audit/day_one_pool_live_refinement_v2_20261001')).replace('\\','/')
 section+=f'<article><h3>{row["role"].replace("_"," ")} · {row["visual_score"]}/5 purpose</h3><img src="{rel}" alt="Exact approved source window: {row["role"]}"><p>{row["opinion"]}</p></article>'
section+='</div><a href="actor_reuse_inventory_v1/INVENTORY.json">Exact source hashes, purpose opinions and unbound wardrobe gaps</a></section>'
text=text.replace('<section><h2>Preserved failures and earlier versions</h2>',section+'<section><h2>Preserved failures and earlier versions</h2>',1)
# Plain-text spacing only; paths, JavaScript identifiers and source hashes stay exact.
for a,b in [('a4.6','a 4.6'),('remain4.2','remain 4.2'),('are4.6','are 4.6'),('in47','in 47'),('all433','all 433'),('all47','all 47'),('All47','All 47'),('and41','and 41'),('Six classic435','Six classic 435'),('native432','native 432'),('six complete40px','six complete 40 px'),('Six individually','Six individually')]:text=text.replace(a,b)
page.write_text(text,encoding='utf-8')
p=family/'REVIEW.json';d=json.loads(p.read_text())
for row in d['shared_items']+d['items']:
 for key in ['opinion','priority_reason']:
  if key not in row:continue
  for a,b in [('a4.6','a 4.6'),('stays4.2','stays 4.2'),('4.6 opinion','4.6 opinion'),('six complete40px','six complete 40 px'),('initial0/catch22/final431','initial 0, catch 22 and final 431'),('initial0/catch21/final431','initial 0, catch 21 and final 431')]:row[key]=row[key].replace(a,b)
d['source_reuse_study']='actor_reuse_inventory_v1/INVENTORY.json'
d['local_delivery']='delivery_http_v2/RECEIPT.json;1376 exact files and18 first/middle/suffix media byte ranges pass. Original whole-file Range failure retained in delivery_http_v1.'
write(p,d)
live=root/'audit/job_artwork_refinement_live/index.html';text=live.read_text(encoding='utf-8')
start=text.index('<section><h2>Current replacement review</h2>');end=text.index('</section>',start)+len('</section>')
text=text[:start]+'<section><h2>Current replacement review</h2><p>The six live pool props now have separate 4.6 drafting opinions for source, mount, contact/carry/drop and stored readability in the current classic capture. All 433 action frames were inspected in 47 ordered boards. Whole actions remain 4.2: body acting is 3.8 and classic/Fairy/Huluu grips are 4.2/4.1/3.5. Initial actor overlap remains 4.3. Earlier shrinking transfers, tiny contents, duplicate basket, incorrect cue and caption-covered return remain preserved at their exact sources. <a href="../day_one_pool_live_refinement_v2_20261001/index.html">Current illustrated individual review and all native frames</a> includes a prospective approved-pose reuse study. Hundreds of other items and the complete owner-approved report remain unfinished.</p></section>'+text[end:]
text=text.replace('The full retry passes all82 trusted probes, with all299 production hashes matching its source snapshot.','The earlier full retry passes all 82 trusted probes, with all 299 production hashes matching that previous source snapshot. The current pool implementation requires its own full run, now in progress with 321 source hashes frozen.')
live.write_text(text,encoding='utf-8')
status=root/'audit/job_artwork_refinement_live/STATUS.json';d=json.loads(status.read_text())
d['current_pool_refinement']={'entry':'audit/day_one_pool_live_refinement_v2_20261001/index.html','review':'audit/day_one_pool_live_refinement_v2_20261001/REVIEW.json',
 'runtime_sources':[{'path':p,'sha256':sha(root/p)} for p in ['scripts/games/day_one_pool_cleanup.gd','scripts/games/pool_skimmer_activity.gd','scripts/games/pool_seahorse_rescue_activity.gd','assets/castle/day_one_pool/activities/refinement_v2/floating_trash_atlas.png','assets/castle/day_one_pool/activities/refinement_v2/pool_skimmer.png']],
 'classic_frames':435,'directly_reviewed_classic_action_frames':433,'classic_boards':47,'props_source_mount_contact_transfer_stored_score':4.6,'whole_played_actions_score':4.2,
 'priority_scores':{'body_acting':3.8,'classic_grip':4.2,'fairy_grip':4.1,'huluu_grip':3.5,'initial_actor_overlap':4.3},
 'wide_visual_scope':'Only initial, first wrapper catch and final in each432-frame capture; no complete wardrobe action pass.',
 'current_full_ci':'In progress at literal321-file source snapshot; prior299-file pass is historical.',
 'qualification':'Refreshable bounded candidate evidence. No all-jobs/global pass, finding closure, device/child/owner/comprehensive report approval, integration or release.'}
write(status,d)
shutil.copyfile(Path(__file__),family/'review_tools'/Path(__file__).name)
impact=root/'design/audit_impacts/day-one-pool-live-refinement-v2-20261001.json';d=json.loads(impact.read_text())
d['files']=sorted(set(d['files'])|{p.relative_to(root).as_posix() for p in family.rglob('*') if p.is_file()}|{'audit/job_artwork_refinement_live/STATUS.json'})
write(impact,d)
print('Five source-purpose opinions saved; illustrated reuse study and current all-jobs entry refreshed. No runtime actor pose selected.')
