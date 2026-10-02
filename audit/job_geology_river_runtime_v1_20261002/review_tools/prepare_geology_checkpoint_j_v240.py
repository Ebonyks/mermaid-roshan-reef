from pathlib import Path
import datetime,json,hashlib,shutil,subprocess,sys
b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
f=b/'audit/job_geology_river_runtime_v1_20261002';p=b/'audit/job_geode_coherent_pilot_v1_20261002'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
qa=dict(status='PASS_OBSERVED_BROWSER_LOADING',checked_utc=now,browser='Codex in-app browser4/tab36',viewport=1280,document_width=1265,checks=[
 dict(path='audit/job_geology_river_runtime_v1_20261002/network.html?revision=current-ci-pass',images=28,loaded=28,broken=0),
 dict(path='audit/job_geology_river_runtime_v1_20261002/timed.html?revision=actual-timed-v1',images=26,loaded=26,broken=0,frame_evaluations=312),
 dict(path='audit/job_geode_coherent_pilot_v1_20261002/index.html?revision=pilot-v1',images=26,loaded=26,broken=0,frame_evaluations=312),
 dict(path='assets_src/imagegen/geologist_geode_coherent_states_v1_20261002/index.html',images=65,loaded=65,broken=0),
 dict(path='audit/job_artwork_refinement_live/all_items.html?revision=geode-timed-v1&q=GEO-RIVER-RUNTIME-',filter='GEO-RIVER-RUNTIME-',lane='All known items',images=6,loaded=6,broken=0),
 dict(path='audit/job_artwork_refinement_live/all_items.html?revision=v27-pilot',filter='GEO-COHERENT',lane='All known items',matched=65,page_images=[30,30,5],page_loaded=[30,30,5],broken=0,first_region_style='position:absolute;max-width:none;max-height:none;width:660px;height:440px;left:-220px;top:-220px;object-fit:fill')],
 qualification='Browser DOM loading/layout/navigation verification only; every1712 register entry is not claimed loaded, and loading is not creative or owner acceptance.')
write(f/'BROWSER_QA_V27_PILOT.json',qa)
shutil.copyfile(__file__,f/'review_tools'/Path(__file__).name)
old=b/'audit/job_geology_painted_work_v1_20261001/review_tools'
s=(old/'seal_geology_work_v191.py').read_text()
s=s.replace("work=b/'audit/job_geology_painted_work_v1_20261001'","work=b/'audit/job_geology_river_runtime_v1_20261002'")
s=s.replace('geology_work_seal_v191','geology_checkpoint_j_seal_v241').replace('geology_work_v182_sealed.json','geology_checkpoint_j_sealed.json')
s=s.replace("baseline='e1b431f49258eef1d293b11a732353f0a3aa12e9'","baseline='40b1c7bfe025f284507c586fea61b9dd76b61423'")
s=s.replace('GEOLOGY_PAINTED_WORK_REVIEW_SUPPLEMENT_FILES_V7.json','GEOLOGY_RIVER_GEODE_REVIEW_SUPPLEMENT_FILES_V8.json')
s=s.replace('==349','==362').replace("['parserv5','inferencev5','authorityv2','developmentv2','2dv1']","['parserv3','inferencev3','authorityv2','developmentv2','2dv1']")
s=s.replace("['job-geology-painted-work-20261001.json','job-geology-river-painted-source-20261001.json']","['job-geology-river-join-study-20261001.json','job-geology-river-junction-source-20261001.json','job-geology-river-bed-source-20261002.json','job-geology-river-painted-runtime-20261002.json','job-geode-coherent-opening-20261002.json']")
s=s.replace('GEOLOGY_RUNTIME_REVIEW_SUPPLEMENT_FILES_V6.json','GEOLOGY_PAINTED_WORK_REVIEW_SUPPLEMENT_FILES_V7.json')
start=s.index("'qualification':'Additive exact canonical")
end=s.index("'}\nwrite(b/mp,m)",start)
s=s[:start]+"'qualification':'Additive exact canonical Git-blob map for painted river sources, every162 isolated join studies, every46 actual four-phase stills and28 actual network views, current312 actual geode frames and312 unbound seven-state pilot frames with complete ordered boards, every geode generation/rejection and65 source opinions, V27 register1712 entries. Current officialGodot4.7.2 unmodified full suite82/82 with362 unchanged source hashes and57 raw diagnostics retained applies to current painted-river production only. Actual four-state geode opening4.2 is retained; unbound pilot opening4.5 provisional does not grant actual-production or owner acceptance. Earlier closed maps remain immutable. Training/story/return/device/child/owner/all-job/integration/release remain open."+s[end:]
s=s.replace('and349-source','and362-source')
(b/'tmp/seal_geology_checkpoint_j_v241.py').write_text(s,encoding='utf-8',newline='\n')
# Publisher is made reviewable and included before sealing.
s=(old/'executed_publish_geology_work_v183.py').read_text()
s=s.replace('geology_work_publish_v183','geology_checkpoint_j_publish_v242').replace('geology_work_remote_v183','geology_checkpoint_j_remote_v242').replace('geology_work_v182_sealed.json','geology_checkpoint_j_sealed.json').replace('executed_publish_geology_work_v183.py','publish_geology_checkpoint_j_v242.py')
s=s.replace('audit/job_geology_painted_work_v1_20261001/full_ci_v1/','audit/job_geology_river_runtime_v1_20261002/full_ci_v1/').replace('==349','==362').replace("'source_count':349","'source_count':362")
start=s.index('msg.write_text(');end=s.index("\nrun('commit'",start)
message='Audit painted river runtime and seven-state geode pilot\\n\\nBind six complete painted river images at reversible new paths; preserve actual input/path/flow/save methods. Include every162 isolated join studies and all46 current ordinary four-phase views/28 production network views. Current unmodified officialGodot4.7.2 full suite82/82 preserves362 literal source hashes and57 raw diagnostics.\\n\\nReview every312 actual continuous geode frame: opening4.2 exposes silhouette swaps. Preserve every failed regeneration, native original and exact reference hash; selected seven-state unbound pilot reaches provisional opening4.5, materials/rooted crystals4.6 after every312 frames on26 boards and8 native transition details. Current production geode remains unchanged. Room2.8/contact2.7/clap4.0 remain weak. V27 library has1712 individually addressable entries,666 inclusive priorities and388 unassigned.\\n\\nQualified reversible topic review checkpoint only; no complete training/story/return/device/child/owner/all-job acceptance, dev/master integration or release. Prior immutable source and review maps remain unchanged.\\n'
s=s[:start]+"msg.write_text("+repr(message.replace('\\n','\n'))+",encoding='utf-8')"+s[end:]
s=s.replace('/audit/job_geology_painted_work_v1_20261001/index.html','/audit/job_geode_coherent_pilot_v1_20261002/index.html')
(b/'tmp/publish_geology_checkpoint_j_v242.py').write_text(s,encoding='utf-8',newline='\n')
shutil.copyfile(b/'tmp/publish_geology_checkpoint_j_v242.py',f/'review_tools/publish_geology_checkpoint_j_v242.py')
ipaths=[b/'design/audit_impacts'/n for n in ['job-geology-river-join-study-20261001.json','job-geology-river-junction-source-20261001.json','job-geology-river-bed-source-20261002.json','job-geology-river-painted-runtime-20261002.json','job-geode-coherent-opening-20261002.json']]
extra={x.relative_to(b).as_posix() for root in [f,p,b/'assets_src/imagegen/geologist_geode_coherent_states_v1_20261002'] for x in root.rglob('*') if x.is_file()}
mp=b/'audit/job_review_v2_20261001/GEOLOGY_RIVER_GEODE_REVIEW_SUPPLEMENT_FILES_V8.json'
assert not mp.exists(),'Preserve any existing immutable map.'
write(mp,dict(status='UNSEALED_LOCAL_PLACEHOLDER_NOT_DELIVERY'))
extra|={mp.relative_to(b).as_posix()}
extra|={f.relative_to(b).as_posix()+'/runtime_gate/'+label+ext for label in ['authorityv2','developmentv2'] for ext in ['.stdout.log','.stderr.log','.receipt.json']}
d=read(ipaths[3]);d['files']=sorted(set(d['files'])|extra)
d['validation'].append(dict(command='Unmodified full officialGodot4.7.2 suite',result='PASS',evidence='audit/job_geology_river_runtime_v1_20261002/full_ci_v1/RECEIPT.json:82/82,362 unchanged literal sources,57 raw diagnostics; frozen painted-river production only.'))
write(ipaths[3],d)
for label,args in [('authorityv2',[sys.executable,'-X','utf8','-B','tools/audit_document_authority.py']),('developmentv2',[sys.executable,'-X','utf8','-B','tools/audit_development.py','--base','auto'])]:
 t=datetime.datetime.now(datetime.timezone.utc);q=subprocess.run(args,cwd=b,capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW)
 (f/'runtime_gate'/f'{label}.stdout.log').write_bytes(q.stdout);(f/'runtime_gate'/f'{label}.stderr.log').write_bytes(q.stderr)
 write(f/'runtime_gate'/f'{label}.receipt.json',dict(status='PASS' if q.returncode==0 else 'FAIL',command=args,process_exit=q.returncode,started_utc=t.isoformat(),finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat()))
 print(label,q.returncode,q.stdout.decode(errors='replace')[-1800:],flush=True);assert q.returncode==0
print('CheckpointJ review and publication helpers prepared; no production geode binding changed.',flush=True)
