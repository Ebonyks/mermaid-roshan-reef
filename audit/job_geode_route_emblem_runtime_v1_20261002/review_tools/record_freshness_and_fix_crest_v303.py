from pathlib import Path
import datetime,hashlib,json,shutil
b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');f=b/'audit/job_geode_route_emblem_runtime_v1_20261002';live=b/'audit/job_artwork_refinement_live';stage=Path('C:/Users/Peter/Documents/mermaid-roshan-reef/tmp')
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
canonical=read(stage/'freshness_canonical_all_v302.json');negative=read(stage/'freshness_negative_all_v302.json');changed=read(stage/'freshness_negative_changed_v302.json')
assert canonical['result'].startswith('4 matching') and len(canonical['uses'])==4 and all(x['imagesLoaded'] for x in canonical['uses'])
assert '676 known' in canonical['summary'] and '547 unique' in canonical['summary'] and '385 source' in canonical['summary']
assert all('Mounted: unassigned' in x['claim'] for x in negative['uses'])
assert next(x for x in negative['uses'] if x['id']=='GEO-USE-LIBRARY')['current'].endswith('review required')
assert changed['ids']==['GEO-USE-LIBRARY'] and changed['result'].startswith('1 matching')
for name in ['freshness_canonical_all_v302.json','freshness_negative_all_v302.json','freshness_negative_changed_v302.json','freshness_canonical_priority_v302.png','freshness_negative_all_v302.png']:shutil.copyfile(stage/name,f/name)
write(f/'FRESHNESS_BROWSER_QA_V303.json',dict(status='PASS_CANONICAL_AND_ISOLATED_INJECTED_STALE_DATA',checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),canonical=canonical,negative=negative,changed_filter=changed,qualification='Browser UI verification, not current gameplay or visual acceptance. Negative data fixture is isolated under ignored tmp and never changes runtime source bytes or the saved register opinions. Canonical1726 source hashes and372 captured boundary hashes matched at the recorded check; source changes after it require another refresh. Counts676 include known source files, pose cells and regions;547 are unique source-file priorities. Three extra mounted geode priorities are counted separately.'))
# Update scope before the production metadata repair.
ip=b/'design/audit_impacts/job-geode-route-emblem-runtime-20261002.json';d=read(ip)
newcrest='assets/opera/worlds/ui/crests/geode_open_painted_v1_20261002.tres'
d['files']=sorted((set(d['files'])-{'assets/opera/ui/crests/geode_open_painted_v1_20261002.tres'})|{newcrest,(f/'review_tools'/Path(__file__).name).relative_to(b).as_posix()})
if 'Full suite1 retained81/82 passing:' not in d['scope']:d['scope']+=' Full suite1 retained81/82 passing: ordinary Opera Library crest assertion rejects an out-of-family metadata location. Restore the existing crest-family path contract using a new metadata-only AtlasTexture in ui/crests, with exact same source pixels, region, aspect and cached atlas; never relax or edit the probe. Recapture both ordinary routes and rerun fresh suite2 after this named repair.'
write(ip,d)
prior=f/'prior_binding_attempt_01';prior.mkdir(exist_ok=True)
for rel in ['scripts/castle_career_routes.gd','audit/job_geode_route_emblem_runtime_v1_20261002/capture.gd','audit/job_geode_route_emblem_runtime_v1_20261002/resource_contract.gd']:
 shutil.copyfile(b/rel,prior/(Path(rel).name+'.txt'))
for name in ['SOURCE_CURRENT_BEFORE_CAPTURES.json','REVIEW.json','PLAN.json','RESOURCE_CONTRACT.json','MECHANIC_UNCHANGED.json']:shutil.copyfile(f/name,prior/name)
shutil.copyfile(b/'assets/opera/worlds/geology/coherent_geode_v1_20261002/open_geode.tres',b/newcrest)
p=b/'scripts/castle_career_routes.gd';s=p.read_text(encoding='utf-8');old='"geologist": "res://assets/opera/worlds/geology/coherent_geode_v1_20261002/open_geode.tres"';assert s.count(old)==1
s=s.replace(old,'"geologist": "geode_open_painted_v1_20261002.tres"');p.write_text(s,encoding='utf-8',newline='\n')
p=f/'resource_contract.gd';s=p.read_text(encoding='utf-8');needle='\tassert(direct.region == relative.region)';assert s.count(needle)==1
s=s.replace(needle,needle+'\n\tvar crest: AtlasTexture = load("res://assets/opera/worlds/ui/crests/geode_open_painted_v1_20261002.tres") as AtlasTexture\n\tassert(crest != null and crest.atlas == source and crest.region == direct.region)\n\tassert(crest.resource_path.contains("/ui/crests/"))\n\tassert(CastleCareerRoutes.CAREER_CREST_FILES["geologist"] == "geode_open_painted_v1_20261002.tres")')
s=s.replace('"same_cached_texture":direct.atlas == source and relative.atlas == source,','"same_cached_texture":direct.atlas == source and relative.atlas == source and crest.atlas == source, "crest_resource_path":crest.resource_path, "crest_atlas_rid":crest.atlas.get_rid().get_id(),')
p.write_text(s,encoding='utf-8',newline='\n')
p=f/'capture.gd';s=p.read_text(encoding='utf-8');old='const OUT := "res://audit/job_geode_route_emblem_runtime_v1_20261002/attempt_01/"';assert s.count(old)==1;s=s.replace(old,old.replace('attempt_01','attempt_02'));p.write_text(s,encoding='utf-8',newline='\n')
snapshot=read(prior/'SOURCE_CURRENT_BEFORE_CAPTURES.json');snapshot['source_files'].append(dict(path=newcrest,sha256=sha(b/newcrest),bytes=(b/newcrest).stat().st_size))
for x in snapshot['source_files']:x['sha256']=sha(b/x['path']);x['bytes']=(b/x['path']).stat().st_size
snapshot['created_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();snapshot['status']='FROZEN_CURRENT_CREST_FAMILY_LOCATION_REPAIR_RECAPTURE_PENDING';snapshot['qualification']='Fresh373-file literal boundary, same unchanged painted atlas pixels and crop geometry. Source metadata location now obeys the existing unchanged ordinary route probe. Earlier372-file captured source, opinions and failed suite1 are preserved; no inherited current route acceptance.';assert len(snapshot['source_files'])==373
write(f/'SOURCE_CURRENT_BEFORE_CAPTURES.json',snapshot)
plan=read(f/'PLAN.json');plan['status']='CREST_FAMILY_LOCATION_FIXED_FRESH_BOTH_WIDTH_RECAPTURE_AND_FULL_CI2_PENDING';plan['bindings']['crest']['path']=newcrest;plan['bindings']['developer_menu']['path']=newcrest;plan['full_ci_failed_attempt']='full_ci_v1/RECEIPT.json';write(f/'PLAN.json',plan)
write(f/'CREST_LOCATION_REPAIR_V303.json',dict(status='IMPLEMENTED_REVALIDATION_PENDING',failure=dict(suite='full_ci_v1/RECEIPT.json',probe='probe_opera_2d',failed_assertions=['library route uses its exact diegetic entrances and approved art','nine room route sets cover all fifteen live sparse slots once'],probe_sha256=sha(b/'scripts/probe_opera_2d.gd')),fix=newcrest,original_goal_metadata='assets/opera/worlds/geology/coherent_geode_v1_20261002/open_geode.tres',source_sha256=sha(b/'assets/opera/worlds/geology/coherent_geode_v1_20261002/opening_six_states.png'),same_metadata_bytes=(b/newcrest).read_bytes()==(b/'assets/opera/worlds/geology/coherent_geode_v1_20261002/open_geode.tres').read_bytes(),qualification='Keep the unchanged existing /ui/crests/ family assertion. No probe edits, relaxed art gates, atlas pixel edits, region/size changes, input/progress/save/reward changes. Earlier failed run and earlier captures remain preserved. New metadata copy shares one cached atlas.'))
licenses=b/'ASSET_LICENSES.md';s=licenses.read_text(encoding='utf-8');s+='\n| `'+newcrest+'` | Existing Codex ImageGen painted geode; metadata reuse | Project-generated; source provenance preserved | `assets/opera/worlds/geology/coherent_geode_v1_20261002/opening_six_states.png` | New AtlasTexture metadata in the existing crest family; exact unchanged source and open region, filter_clip; no pixel edits. Original goal metadata preserved. |\n';licenses.write_text(s,encoding='utf-8',newline='\n')
shutil.copyfile(Path(__file__),f/'review_tools'/Path(__file__).name)
d=read(ip);d['files']=sorted(set(d['files'])|{p.relative_to(b).as_posix() for p in f.rglob('*') if p.is_file()});d['validation'].append(dict(command='Canonical and isolated negative browser freshness review',result='PASS',evidence=(f/'FRESHNESS_BROWSER_QA_V303.json').relative_to(b).as_posix()));write(ip,d)
print('Freshness QA recorded; crest-family location repaired with exact unchanged artwork. Probe unchanged.373-source recapture and fullCI2 pending.')
