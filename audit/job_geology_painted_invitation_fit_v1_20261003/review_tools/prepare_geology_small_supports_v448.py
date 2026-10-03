from pathlib import Path
import json,hashlib,datetime,shutil
R=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');P=R/'audit/job_geology_painted_invitation_fit_v1_20261003'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
ip=R/'design/audit_impacts/job-geology-painted-invitation-fit-20261003.json';d=read(ip)
assert read(P/'DIRECT_REVIEW_ATTEMPT02.json')['whole_fit_score']==4.0
original=P/'attempt02/fixture_originals';original.mkdir(exist_ok=False);records=[]
for name in ['capture.gd','painted_prop_backdrop.gd']:
 dst=original/(name+'.original');shutil.copyfile(P/name,dst);records.append(dict(path=dst.relative_to(R).as_posix(),sha256=sha(dst),role='Exact A2 reviewed lower-lane non-runtime fixture source'))
d['scope']+=' Preserve exact A2 selected clearance4.5/support scale3.8/whole4.0 and all58 views. A3 reuses three small aspect-preserved supports instead of one oversized empty slab, with unchanged tray sources, actor/work/input/save and production. All58 selected A3 views require fresh review; no predicted pass.'
d['files']=sorted(set(d['files'])|{x['path'] for x in records}|{(P/'SMALL_SUPPORT_PLAN_V448.json').relative_to(R).as_posix(),(P/'review_tools'/Path(__file__).name).relative_to(R).as_posix(),(P/'review_tools/run_small_supports_v448.py').relative_to(R).as_posix()});write(ip,d)
write(P/'SMALL_SUPPORT_PLAN_V448.json',dict(status='PLANNED_NO_PREDICTED_PASS',created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),prior_review='DIRECT_REVIEW_ATTEMPT02.json',preserved_fixture_sources=records,new_support_rects=[[535+i*145,603,140,140*369/889] for i in range(3)],unchanged_tray_base_y=625,reason='A2 tray support scale3.8: one430×178.5 slab overwhelms three110px trays. Reuse the same approved slab three times at140×58.1, preserving aspect and original pixels. Each tray rests on one small stone support. Keep lower clearance and source identity.',production_changes=False,whole_action_acceptance=False,owner_acceptance=None))
s=(P/'painted_prop_backdrop.gd').read_text();line='\t_draw_geology_prop("slab",Rect2(530,510,430,430.0*369.0/889.0))\n';assert s.count(line)==1;s=s.replace(line,'');needle='\tfor index in range(3):\n';assert s.count(needle)==1;s=s.replace(needle,needle+'\t\t_draw_geology_prop("slab",Rect2(535.0+float(index)*145.0,603,140,140.0*369.0/889.0))\n');(P/'painted_prop_backdrop.gd').write_text(s,encoding='utf-8',newline='\n')
s=(P/'capture.gd').read_text();assert s.count('painted_invitation_fit_v1_20261003/attempt02/')==1;s=s.replace('painted_invitation_fit_v1_20261003/attempt02/','painted_invitation_fit_v1_20261003/attempt03/');(P/'capture.gd').write_text(s,encoding='utf-8',newline='\n')
s=(P/'review_tools/run_lower_fit_v443.py').read_text();assert s.count("G=P/'runtime_gate_lower_a2'")==1;s=s.replace("G=P/'runtime_gate_lower_a2'","G=P/'runtime_gate_small_a3'").replace("G.mkdir(exist_ok=True)","G.mkdir(exist_ok=False)").replace("P/'attempt02'","P/'attempt03'").replace("'_v443'","'_v448'");runner=P/'review_tools/run_small_supports_v448.py';runner.write_text(s,encoding='utf-8',newline='\n')
shutil.copyfile(Path(__file__),P/'review_tools'/Path(__file__).name)
exec(compile(runner.read_text(),str(runner),'exec'),{'__file__':str(runner),'__name__':'__main__'})
