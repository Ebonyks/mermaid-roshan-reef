from pathlib import Path
import json,hashlib,datetime,shutil
R=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');P=R/'audit/job_geology_painted_invitation_fit_v1_20261003'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
ip=R/'design/audit_impacts/job-geology-painted-invitation-fit-20261003.json';d=read(ip)
assert read(P/'DIRECT_REVIEW_ATTEMPT01.json')['status']=='LAYOUT_REJECTED_ACTOR_OCCLUSION'
original=P/'attempt01/fixture_originals';original.mkdir(exist_ok=False)
records=[]
for name in ['capture.gd','painted_prop_backdrop.gd']:
 dst=original/(name+'.original');shutil.copyfile(P/name,dst);records.append(dict(path=dst.relative_to(R).as_posix(),sha256=sha(dst),role='Exact failedA1 non-runtime fixture source'))
d['scope']+=' Preserve the directly rejected A1 props layout3.5/clearance3.5 and exact helper source; A2 only reserves a lower foreground prop lane below Roshan invitation silhouettes. Candidate remains unbound and counterfactual. No artwork/native pixels or production changes; all58 selected canvases need fresh review.'
d['files']=sorted(set(d['files'])|{x['path'] for x in records}|{(P/'LOWER_FIT_PLAN_V443.json').relative_to(R).as_posix(),(P/'review_tools'/Path(__file__).name).relative_to(R).as_posix(),(P/'review_tools/run_lower_fit_v443.py').relative_to(R).as_posix()});write(ip,d)
write(P/'LOWER_FIT_PLAN_V443.json',dict(status='PLANNED_NO_PREDICTED_PASS',created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),failed_trial='DIRECT_REVIEW_ATTEMPT01.json',preserved_fixture_sources=records,new_rects=dict(fossil_slab=[355,580,180,180*369/889],fossil=[383,543,105,105*674/802],tray_slab=[530,510,430,430*369/889],tray_base_y=625,mineral=[1090,545,130*569/767,130]),reason='A1 later invitations put Roshan over the fossil and trays. Move whole conserved props/supports into reserved lower foreground without moving actors or changing input, pacing, work/completion or source images.',production_changes=False,whole_action_acceptance=False,owner_acceptance=None))
s=(P/'painted_prop_backdrop.gd').read_text();changes={'Rect2(355,485,180':'Rect2(355,580,180','Rect2(383,425,105':'Rect2(383,543,105','Rect2(530,445,430':'Rect2(530,510,430','520.0-tray_height':'625.0-tray_height','Rect2(1090,435':'Rect2(1090,545'}
for a,b in changes.items():assert s.count(a)==1;s=s.replace(a,b)
(P/'painted_prop_backdrop.gd').write_text(s,encoding='utf-8',newline='\n')
s=(P/'capture.gd').read_text();assert s.count('painted_invitation_fit_v1_20261003/attempt01/')==1;s=s.replace('painted_invitation_fit_v1_20261003/attempt01/','painted_invitation_fit_v1_20261003/attempt02/')
s=s.replace('## Actual production surface and all four ordinary career phases. Only entry\n## fixture and isolated test save home are supplied; no phase forcing, source\n## injection, replacement surface, background overlay or completion callback patch.','## NON-RUNTIME COUNTERFACTUAL lower-foreground invitation prop placement.\n## Library backdrop is explicitly replaced by the review-only subclass. Actual\n## work surface/input/completion and developer second entry remain production.')
(P/'capture.gd').write_text(s,encoding='utf-8',newline='\n')
old=(P/'review_tools/run_geology_prop_fit_v439.py').read_text();tail=old[old.index("G=P/'runtime_gate'"):]
tail=tail.replace("G=P/'runtime_gate'","G=P/'runtime_gate_lower_a2'").replace("P/'attempt01'","P/'attempt02'").replace("'_v439'","'_v443'")
prefix=old[:old.index('# The newly generated alpha')]+"ip=R/'design/audit_impacts/job-geology-painted-invitation-fit-20261003.json'\n"
runner=P/'review_tools/run_lower_fit_v443.py';runner.write_text(prefix+tail,encoding='utf-8',newline='\n')
shutil.copyfile(Path(__file__),P/'review_tools'/Path(__file__).name)
exec(compile(runner.read_text(),str(runner),'exec'),{'__file__':str(runner),'__name__':'__main__'})
