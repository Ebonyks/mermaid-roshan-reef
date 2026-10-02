from pathlib import Path
import datetime,hashlib,json,shutil,subprocess
R=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
F=R/'audit/job_geode_current_recheck_v1_20261002';assert not F.exists()
baseline=subprocess.run(['git','rev-parse','HEAD'],cwd=R,capture_output=True,check=True).stdout.decode().strip();assert baseline=='c2538760639d79b063152ce5530807c04545ba6e'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
old=R/'audit/job_geode_supported_celebration_v1_20261002/capture.gd'
current=read(R/'audit/job_nursery_wash_connected_v1_20261002/SOURCE_CURRENT_MACHINE_V3.json')
assert len(current['source_files'])==783 and all(sha(R/r['path'])==r['sha256'] for r in current['source_files'])
prior_imp=read(R/'design/audit_impacts/job-nursery-wash-connected-20261002.json')
paths=['PLAN.json','.gdignore','capture.gd','SOURCE_CURRENT_BEFORE_CAPTURE.json','review_tools/'+Path(__file__).name]
ip=R/'design/audit_impacts/job-geode-current-recheck-20261002.json'
impact={'id':'job-geode-current-recheck-20261002','scope':'Fresh current Geologist visual/context replay after shared CareerWorld Nursery changes made old mounted evidence stale. Preserve exact production artwork and mechanics. Copy only the established actual Library-card/all-four-phase/earned-return/Opera-elevator capture fixture with a new non-runtime output directory. Verify every current source byte before/after, inspect every native selected canvas and all opening/celebration/earned-return frames, and assign fresh bounded component/action opinions only after direct review. Keep older Geologist reviews, user rooted-crystal direction, individual weaknesses, all finding states, device/child/owner/integration/release gates. No new or edited production/source artwork, input/progress/save/reward owners, protected originals or cinematic delivery.','baseline':baseline,'rules':prior_imp['rules'],'findings':prior_imp['findings'],'files':[(F/p).relative_to(R).as_posix() for p in paths],'validation':[{'command':'Current unchanged Geologist capture/individual visual recheck','result':'PENDING','evidence':(F/'PLAN.json').relative_to(R).as_posix()}]}
write(ip,impact)
(F/'review_tools').mkdir(parents=True);(F/'.gdignore').write_text('',encoding='utf-8')
s=old.read_text(encoding='utf-8');needle='res://audit/job_geode_supported_celebration_v1_20261002/attempt_02/';assert s.count(needle)==1
s=s.replace(needle,'res://audit/job_geode_current_recheck_v1_20261002/attempt01/');(F/'capture.gd').write_text(s,encoding='utf-8',newline='\n')
write(F/'PLAN.json',{'status':'CURRENT_SOURCE_REPLAY_PREPARED','baseline':baseline,'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'named_gap':'Old M mounted/action claims automatically withheld after shared CareerWorld Nursery change. Source paintings remain preserved; current production context needs direct rerendering before any current mounted opinion.','reuse':'Exact existing capture fixture and exact current production art; no regeneration or production edits.','fixture_original':old.relative_to(R).as_posix(),'fixture_original_sha256':sha(old),'fixture_copy_sha256':sha(F/'capture.gd'),'fixture_change':'Output directory only. All input/entry/completion/source-owner code identical.','source_boundary_count':783,'contexts':'Actual Library card/caller all four ordinary phases and earned room return, then actual Opera elevator Geologist developer entry and Back. Neither separate ChapterTwo story phases nor two-act Geologist stage rollout exists.','views':[1280,1600],'required_review':'All selected native canvases and every native opening/celebration/return frame, fine details at native size; rooted crystals inside halves, stable supporting slab, no loot drops, actor visibility, true contacts, other phase material/action defects, clearing and actual return. Source/static/mounted/action/device/child/owner opinions remain distinct.','owner_acceptance':None,'integration':False,'release':False})
write(F/'SOURCE_CURRENT_BEFORE_CAPTURE.json',current)
shutil.copyfile(Path(__file__),F/'review_tools'/Path(__file__).name)
print('CURRENT_GEODE_RECHECK_PREPARED|783 unchanged source hashes|new output only|older evidence preserved')
