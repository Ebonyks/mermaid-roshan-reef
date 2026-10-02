from pathlib import Path
import hashlib,json,shutil
r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');f=r/'audit/job_geode_route_emblem_runtime_v1_20261002';old=r/'audit/job_geode_coherent_runtime_v1_20261002/review_tools'
baseline='c8f88df058434f1fd1b6d7fade712677003c641a'
mp='audit/job_review_v2_20261001/GEOLOGY_GEODE_ROUTE_EMBLEM_SUPPLEMENT_FILES_V10.json'
def replace(s,a,b):assert a in s,a;return s.replace(a,b)
seal=(old/'seal_geology_checkpoint_k_v274.py').read_text(encoding='utf-8')
for a,b in [
 ("work=b/'audit/job_geode_coherent_runtime_v1_20261002'","work=b/'audit/job_geode_route_emblem_runtime_v1_20261002'"),
 ('geology_checkpoint_k_seal_v274','geology_checkpoint_l_seal_v296'),
 ("baseline='c6f03791aee93f1443d423dd50334804e37313fb'","baseline='"+baseline+"'"),
 ('GEOLOGY_COHERENT_GEODE_ROUTE_REVIEW_SUPPLEMENT_FILES_V9.json','GEOLOGY_GEODE_ROUTE_EMBLEM_SUPPLEMENT_FILES_V10.json'),
 ('GEOLOGY_RIVER_GEODE_REVIEW_SUPPLEMENT_FILES_V8.json','GEOLOGY_COHERENT_GEODE_ROUTE_REVIEW_SUPPLEMENT_FILES_V9.json'),
 ('full_ci_v3','full_ci_v1'),('==368','==372'),
 ("['parserv2','inferencev2','authorityv1','developmentv1','2dv1']","['parserv3','inferencev3','importartv1','contractv2','capture1280v1','capture1600v1','authorityv3','developmentv3','audit2dv1']"),
 ("['job-geode-coherent-runtime-20261002.json','job-geology-room-route-review-20261002.json','job-geology-geode-emblem-reuse-20261002.json','job-geology-grotto-native-resolution-20261002.json','job-training-shared-source-review-20261002.json']","['job-geode-route-emblem-runtime-20261002.json','job-wash-root-doctor-sequence-review-20261002.json']"),
 ('geology_checkpoint_k_sealed.json','geology_checkpoint_l_sealed.json'),('and368-source','and372-source')]:seal=replace(seal,a,b)
start=seal.index("'qualification':'Additive canonical Git-blob checkpoint:");end=seal.index("'}\nwrite(b/mp,m)",start)
qualification='Additive reversible current painted-geode Library50px/invitation142px4.5 provisional, shared developer80px4.6 and normal celebration artwork4.6 but placement4.2/composition3.3. Same source atlas pixels; three production bindings and one AtlasTexture resource, function bodies/mechanics/save/reward preserved. All58 current stills/316 current consecutive frames/27 motion boards/10 still boards/eight native details/23 current object-state-context opinions reviewed. Room2.8/contact2.7/fossil clearing3.9/pan3.8/caption4.0 and native-background coverage remain open. Fresh unmodified officialGodot4.7.2 full suite1 82/82 on372 frozen literal files, raw diagnostics retained; no inherited or visual pass. V31 known register1726 entries/1245 sources/49 runtime regions retains676 source priorities/385 unassigned; four old technical labels now distinct, aliases/oldV30 bytes preserved. Separately all256 preservedOctober1 Doctor1280 training WASH frames/22 boards/eight native details/12 opinions reviewed; workflow2.7/contact2.3/subject2.2/basin2.9 remain weak. Other1818 case frames/current rerender/story/device/child/owner/all-job acceptance remain open. Verify required unchanged native references at this exact remote revision as well as every new payload. Earlier closed maps immutable; no finding lifecycle change, dev/master integration or release.'
seal=seal[:start]+"'qualification':"+repr(qualification)+seal[end+1:]
needle='write(b/mp,m);git('
pos=seal.index(needle)
extra="""refs=json.loads((b/'audit/job_wash_root_doctor_sequence_v1_20261002/REQUIRED_UNCHANGED_REFERENCES.json').read_text())['files']
for ref in ['assets/opera/worlds/geology/coherent_geode_v1_20261002/opening_six_states.png','assets/opera/worlds/geology/coherent_geode_v1_20261002/opening_bridge.png','assets/opera/worlds/geology/painted_work_v1_20261001/work_slab.png']:
 raw_ref=git('show','HEAD:'+ref);refs[ref]=[len(raw_ref),hashlib.sha256(raw_ref).hexdigest()]
for ref,v in refs.items():
 raw_ref=git('show','HEAD:'+ref);assert [len(raw_ref),hashlib.sha256(raw_ref).hexdigest()]==v,ref
assert not set(refs)&set(files)
m['required_unchanged_files']=len(refs);m['unchanged_required_files']=dict(sorted(refs.items()))
"""
seal=seal[:pos]+extra+seal[pos:]
seal=replace(seal,"'payload_bytes':m['required_payload_bytes'],'checked_utc'","'payload_bytes':m['required_payload_bytes'],'unchanged_required_files':len(refs),'checked_utc'")
(f/'review_tools/seal_geology_checkpoint_l_v296.py').write_text(seal,encoding='utf-8',newline='\n')
pub=(old/'publish_geology_checkpoint_k_v259.py').read_text(encoding='utf-8')
for a,b in [('geology_checkpoint_k_publish_v259','geology_checkpoint_l_publish_v297'),('geology_checkpoint_k_remote_v259','geology_checkpoint_l_remote_v297'),('geology_checkpoint_k_sealed.json','geology_checkpoint_l_sealed.json'),('publish_geology_checkpoint_k_v259.py','publish_geology_checkpoint_l_v297.py'),('audit/job_geode_coherent_runtime_v1_20261002/full_ci_v3/','audit/job_geode_route_emblem_runtime_v1_20261002/full_ci_v1/'),('==368','==372'),("'source_count':368","'source_count':372"),('/audit/job_geology_room_route_v1_20261002/index.html','/audit/job_geode_route_emblem_runtime_v1_20261002/index.html')]:pub=replace(pub,a,b)
start=pub.index('msg.write_text(');end=pub.index("\nrun('commit'",start)
message='Reuse painted geode throughout its actual job route\n\nThe end specimen opens into two stone halves with crystals rooted inside. Reuse that same unchanged source for Library crest, closed invitation, normal earned celebration and existing shared developer menu; preserve input, progress, save and rewards. Three production script bindings and one new AtlasTexture resource. Strict catalog/cache check and exact function-body preservation recorded; initial unused-metadata failure retained and repaired without weakening validators.\n\nEvery58 current native stills/316 consecutive frames/37 complete boards/eight native details and23 individual opinions reviewed. Library/invitation4.5 provisional; developer80px4.6; celebration material4.6 but unsupported placement4.2/composition3.3. Room2.8/contact2.7/fossil clearing3.9/pan3.8/caption4.0 and native-resolution background gap remain. V31 known register1726 entries,676 source priorities/385 unassigned, with material/mounting separated and earlierV30 bytes/labels preserved.\n\nAlso review every256 preservedOctober1 Doctor1280 training WASH frames on22 complete boards plus eight native details and12 individual opinions. Workflow2.7/contact2.3/subject2.2/basin2.9 remain weak; dated capture freshness470/475, not a new current rerender. Other1818 captured case frames and ordinary story/device/child/owner acceptance remain open.\n\nFresh officialGodot4.7.2 unmodified full suite1 82/82 on372 unchanged literal source files, raw diagnostics retained. Topic review candidate; no all-job acceptance, finding closure, dev/master integration or release. Every new payload and259 required unchanged native reference files anonymously verified at immutable revision. Earlier closed maps unchanged.\n'
pub=pub[:start]+'msg.write_text('+repr(message)+",encoding='utf-8')"+pub[end:]
pub=replace(pub,"rows=[];fail=[]","targets=dict(m['files']);targets.update(m.get('unchanged_required_files',{}))\nrows=[];fail=[]")
pub=replace(pub,'[pool.submit(fetch,p) for p in m[\'files\']]','[pool.submit(fetch,p) for p in targets]')
pub=replace(pub,"m['files'][row['path']]","targets[row['path']]")
pub=replace(pub,"'payload_files':len(rows),'files_including_manifest':len(rows)+1","'payload_files':len(m['files']),'required_unchanged_files':len(m.get('unchanged_required_files',{})),'files_including_manifest':len(rows)+1")
(f/'review_tools/publish_geology_checkpoint_l_v297.py').write_text(pub,encoding='utf-8',newline='\n')
compile(seal,'seal_l','exec');compile(pub,'publish_l','exec')
assert not (r/mp).exists();(r/mp).write_text(json.dumps({'status':'UNSEALED_CURRENT_CHECKPOINT_L_PENDING_FULL_CI'},indent=2)+'\n',encoding='utf-8')
shutil.copyfile(Path(__file__),f/'review_tools'/Path(__file__).name)
ip=r/'design/audit_impacts/job-geode-route-emblem-runtime-20261002.json';d=json.loads(ip.read_text());d['files']=sorted(set(d['files'])|{p.relative_to(r).as_posix() for p in f.rglob('*') if p.is_file()}|{mp});ip.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print('Prepared exact topic-only checkpointL sealer/publisher; no stage/commit/push until current82-probe/372-source full suite passes.')
