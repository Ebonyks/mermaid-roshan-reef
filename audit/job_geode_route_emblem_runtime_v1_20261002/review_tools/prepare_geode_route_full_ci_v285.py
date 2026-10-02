from pathlib import Path
import hashlib, json, shutil

r = Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
f = r / 'audit/job_geode_route_emblem_runtime_v1_20261002'
old = r / 'audit/job_geode_coherent_runtime_v1_20261002/review_tools/run_coherent_geode_full_ci_v261.py'
new = f / 'review_tools/run_geode_route_full_ci_v285.py'
text = old.read_text(encoding='utf-8')
text = text.replace("family=root/'audit/job_geode_coherent_runtime_v1_20261002'", "family=root/'audit/job_geode_route_emblem_runtime_v1_20261002'")
text = text.replace("folder=family/'full_ci_v3'", "folder=family/'full_ci_v1'")
text = text.replace('job-geode-coherent-runtime-20261002.json', 'job-geode-route-emblem-runtime-20261002.json')
start = text.index(' previous=json.loads(')
end = text.index(" wrapper='''", start)
replacement = ''' snapshot=json.loads((family/'SOURCE_CURRENT_BEFORE_CAPTURES.json').read_text())
 assert len(snapshot['source_files'])==372
 assert all(sha(root/r['path'])==r['sha256'] for r in snapshot['source_files'])
 snapshot['status']='CURRENT_LITERAL_SOURCE_SNAPSHOT'
 snapshot['created_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
 snapshot['qualification']='Fresh current literal 372-file boundary, including current Library/goal/invitation bindings and actual route/resource review fixtures. Existing trusted scripts/ci.sh remains unmodified. All hashes frozen throughout the run; no inherited pass, hosted result or visual/device/owner acceptance.'
 assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()==snapshot['baseline']
 paths={r['path'] for r in snapshot['source_files']}
 write(folder/'SOURCE_BEFORE.json',snapshot)
'''
text = text[:start] + replacement + text[end:]
text = text.replace('audit/job_geode_coherent_runtime_v1_20261002/full_ci_v3/process.exit', 'audit/job_geode_route_emblem_runtime_v1_20261002/full_ci_v1/process.exit')
text = text.replace('Official Godot4.7.2 unmodified coherent-geode production full suite3 scripts/ci.sh', 'Official Godot4.7.2 unmodified current geode route-emblem full suite1 scripts/ci.sh')
assert not new.exists()
new.write_text(text, encoding='utf-8', newline='\n')
shutil.copyfile(Path(__file__), f/'review_tools'/Path(__file__).name)
impact=r/'design/audit_impacts/job-geode-route-emblem-runtime-20261002.json'
d=json.loads(impact.read_text())
d['files']=sorted(set(d['files'])|{p.relative_to(r).as_posix() for p in [new, f/'review_tools'/Path(__file__).name]})
impact.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print('Prepared exact-current full suite runner. No production source change.')
