"""Build a navigable index from raw agent reports without promoting hypotheses."""
from pathlib import Path
from collections import Counter
import hashlib,json
ROOT=Path(__file__).resolve().parents[4]; CYCLE=ROOT/'audit/cycles/luna-playtest-20261012'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 matrix=json.loads((CYCLE/'matrix.json').read_text()); verified=json.loads((CYCLE/'verification/sessions.json').read_text()); coordinator=json.loads((CYCLE/'coordinator.json').read_text()); rows=[]; classes=Counter(); programs=Counter(); observations=[]
 for row in matrix['sessions']:
  report=CYCLE/'reports'/f"{row['id']}.json"
  if not report.exists(): rows.append({**row,'review_status':'PENDING'});continue
  data=json.loads(report.read_text()); receipt=ROOT/data['runtime_receipt']
  if not receipt.resolve().is_relative_to(CYCLE.resolve()): receipt=report.parent/data['runtime_receipt']
  actual=json.loads(receipt.read_text()); programs[row['probe']]+=1
  rows.append({**row,'review_status':data['verdict'],'runtime_status':actual['status'],'evidence_kind':data['evidence_kind'],'report':report.relative_to(ROOT).as_posix(),'report_sha256':sha(report),'agent_id':data['reviewer']['agent_id'],'play_sequence':data.get('play_sequence'),'timing':data['timing'],'tactile':data['tactile'],'play_appeal':data['play_appeal'],'route_status':data['route_status']})
  for index,item in enumerate(data['observations'],1):
   classes[item['classification']]+=1;observations.append({'intake_id':f"{row['id']}-O{index:02d}",'session_id':row['id'],**item})
 summary={'schema':'luna_gameplay_summary/1','baseline':matrix['baseline'],'status':'REVIEW_COMPLETE' if verified['status']=='PASS' else 'IN_PROGRESS','planned_agent_reviews':len(matrix['sessions']),'verified_valid_reports':verified['completed_valid_sessions'],'coordinator_terminal_completed':coordinator['completed_count'],'runtime_counts':verified['counts'],'unique_existing_probe_programs':len(programs),'probe_invocation_counts':dict(sorted(programs.items())),'observation_counts':dict(classes),'confirmed_new_canonical_findings':['MA-TOUCH-004'],'important_limits':['Repeated probe programs are shared regression anchors, not different autonomous game playthroughs.','Internal calls, routed viewport input, Mobile display, actual device, child observation and owner review are separate lanes.','Agent play_appeal is a hypothesis, without a numeric fun/product score.','Raw report PASS is scoped to its tested assertions; no whole-game or full-route acceptance.'],'sessions':rows,'observations':observations}
 (CYCLE/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 text=(CYCLE/'README.md').read_text();marker='<!-- GENERATED_SESSION_INDEX -->';text=text.split(marker)[0].rstrip()+'\n\n'+marker+'\n\n## Session index\n\n'
 text+=f"Current validated reports: **{verified['completed_valid_sessions']}/{len(matrix['sessions'])}**; terminal agents: **{coordinator['completed_count']}**. Runtime results: **{verified['counts']['runtime_PASS']} PASS**, **{verified['counts']['runtime_FAIL']} FAIL**. Failures are retained. Unique unchanged probe programs so far: **{len(programs)}**; repetitions do not expand unique scenario coverage. [Full structured summary](summary.json) and [count/hash validation](verification/sessions.json) keep every raw observation and source reference.\n\n"
 text+='| Session | Focus | Runtime | Evidence lane | Raw reviewer verdict |\n|---|---|---|---|---|\n'
 for row in rows:
  link=f"[{row['id']}](reports/{row['id']}.json)" if row['review_status']!='PENDING' else row['id']
  text+=f"| {link} | {row['focus']} | {row.get('runtime_status','PENDING')} | {row.get('evidence_kind','PENDING')} | {row['review_status']} |\n"
 (CYCLE/'README.md').write_text(text,encoding='utf-8');print(f"Indexed{len(rows)} planned/{verified['completed_valid_sessions']} valid reports; no hypotheses promoted.")
if __name__=='__main__':main()
