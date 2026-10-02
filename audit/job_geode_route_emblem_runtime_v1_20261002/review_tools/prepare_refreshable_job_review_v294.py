from pathlib import Path
import json,shutil
r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');f=r/'audit/job_geode_route_emblem_runtime_v1_20261002';live=r/'audit/job_artwork_refinement_live'
tool=live/'review_tools/refresh_current_job_review_v31.py'
assert not tool.exists()
source='''from pathlib import Path
import datetime,hashlib,json,subprocess

root=next(p for p in Path(__file__).resolve().parents if (p/'project.godot').is_file())
live=root/'audit/job_artwork_refinement_live'
registry=json.loads((live/'ALL_ITEMS.json').read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None
observed={}
items=[]
for item in registry['items']:
 path=item['path'];file=(root/path).resolve()
 assert file.is_relative_to(root.resolve()) and not path.startswith(('.secrets/','.git/','.codex/','.claude/'))
 if path not in observed:observed[path]=sha(file)
 match=observed[path]==item.get('current_checkout_sha256') and observed[path] is not None
 binding=item.get('current_binding');binding_match=None
 if binding and item.get('binding_sha256'):
  binding_match=sha(root/binding)==item['binding_sha256']
 items.append(dict(id=item['id'],path=path,observed_sha256=observed[path],registered_sha256=item.get('current_checkout_sha256'),source_match=match,binding_match=binding_match))
family=root/'audit/job_geode_route_emblem_runtime_v1_20261002'
snapshot=json.loads((family/'SOURCE_CURRENT_BEFORE_CAPTURES.json').read_text())
boundary=[dict(path=x['path'],recorded_sha256=x['sha256'],observed_sha256=sha(root/x['path'])) for x in snapshot['source_files']]
changed=[x for x in boundary if x['recorded_sha256']!=x['observed_sha256']]
stamp=dict(schema='reef.current-review-boundary-refresh.v1',status='CURRENT_GEODE_CAPTURE_SOURCE_BOUNDARY_MATCH' if not changed else 'STALE_GEODE_CAPTURE_SOURCE_BOUNDARY_REVIEW_REQUIRED',checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),working_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),registry_items=len(items),unique_registered_paths=len(observed),registered_source_matches=sum(x['source_match'] for x in items),source_changed_or_unavailable=[x for x in items if not x['source_match']],geode_capture_source_count=len(boundary),geode_capture_boundary_match=not changed,geode_changed_sources=changed,items=items,qualification='Refresh reads known literal sources and recorded binding hashes only. It does not generate art, change opinions, play the game or grant visual/owner acceptance. Changed sources withhold their current opinions in the register display; prior opinions remain in the saved register/history. Any changed member of the372-file geode capture boundary requires a current rerender before its mounted claims can be displayed as current. Dated Doctor capture remains explicitly historical, not rescued by this refresh.')
(live/'CURRENT_BOUNDARY_REFRESH.json').write_text(json.dumps(stamp,indent=2,ensure_ascii=False)+'\\n',encoding='utf-8',newline='\\n')
print(stamp['status']+'|'+str(stamp['registered_source_matches'])+'/'+str(len(items))+' registered item hashes match|'+str(len(changed))+' changed geode boundary sources')
'''
compile(source,str(tool),'exec');tool.write_text(source,encoding='utf-8',newline='\n')
reg=live/'ALL_ITEMS.json';d=json.loads(reg.read_text());d['historical_register_rebuild_command']=d['refresh_command'];d['refresh_command']='python -B audit/job_artwork_refinement_live/review_tools/refresh_current_job_review_v31.py';reg.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
p=live/'all_items.html';s=p.read_text(encoding='utf-8')
needle="fetch('ALL_ITEMS.json').then(x=>{if(!x.ok)throw Error(x.status);return x.json()}).then(d=>{"
assert s.count(needle)==1
replacement="""Promise.all([fetch('ALL_ITEMS.json').then(x=>{if(!x.ok)throw Error(x.status);return x.json()}),fetch('CURRENT_BOUNDARY_REFRESH.json').then(x=>{if(!x.ok)throw Error('Run the recorded source-boundary refresh command before viewing current claims');return x.json()})]).then(([d,stamp])=>{const checks=new Map(stamp.items.map(x=>[x.id,x]));for(const q of d.items){const c=checks.get(q.id);if(!c||!c.source_match){q.current_byte_status='CHANGED_SINCE_REGISTER_REFRESH_REVIEW_REQUIRED';q.current_source_score=null;q.current_mounted_score=null;q.current_object_sequence_score=null;q.current_complete_action_score=null;q.priority=false;}else if(c.binding_match===false||(q.id.startsWith('GEO-USE-')&&!stamp.geode_capture_boundary_match)){q.current_mounted_score=null;q.current_object_sequence_score=null;q.current_complete_action_score=null;q.priority=q.current_source_score!=null&&q.current_source_score<=4.5;q.source_qualification+=' Current mounted evidence withheld after a recorded binding/context source change; rerender required.';}}d.counts.inclusive_current_source_priorities=d.items.filter(q=>q.kind==='source'&&q.current_source_score!=null&&q.current_source_score<=4.5).length;d.counts.unreviewed_current_source=d.items.filter(q=>q.kind==='source'&&q.current_source_score==null).length;return d;}).then(d=>{"""
s=s.replace(needle,replacement)
pos=s.index('</h1>')+len('</h1>');s=s[:pos]+'<p>After game developments, run <code>python -B audit/job_artwork_refinement_live/review_tools/refresh_current_job_review_v31.py</code>, then reload this register. Changed sources or recorded bindings withhold current opinions; earlier dated evaluations stay preserved. <a href="CURRENT_BOUNDARY_REFRESH.json">Latest literal source-boundary comparison</a>.</p>'+s[pos:]
p.write_text(s,encoding='utf-8',newline='\n')
shutil.copyfile(Path(__file__),f/'review_tools'/Path(__file__).name)
ip=r/'design/audit_impacts/job-geode-route-emblem-runtime-20261002.json';d=json.loads(ip.read_text());d['files']=sorted(set(d['files'])|{tool.relative_to(r).as_posix(),(live/'CURRENT_BOUNDARY_REFRESH.json').relative_to(r).as_posix(),(f/'review_tools'/Path(__file__).name).relative_to(r).as_posix()});d['scope']+=' Add an explicitly invokable read-only known-source/binding refresh for developments; browser display withholds stale current opinions while all earlier evaluations remain preserved. No generation, automatic gameplay or changed saved scores.';ip.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print('Prepared the source-boundary refresh command and conservative stale-opinion display. Run it before browser reload.')
