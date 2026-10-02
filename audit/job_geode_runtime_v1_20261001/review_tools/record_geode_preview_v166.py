from pathlib import Path
import datetime,hashlib,json,shutil
b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');out=b/'audit/job_geode_runtime_v1_20261001'
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
write(out/'LIBRARY_QA.json',{'status':'PASS_OBSERVED_REPORT_LAYOUT','checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'url':'http://127.0.0.1:8880/audit/job_geode_runtime_v1_20261001/index.html?revision=production-v3',
 'report_sha256':hashlib.sha256((out/'index.html').read_bytes()).hexdigest(),
 'checks':[{'check':'exact HTTP bytes for report/current JSON/final native view/open source','result':'PASS'},
 {'check':'browser DOM exposes all36 scored current views, four source items, six embedded components via JSON and preserved archive disclosures','result':'PASS'},
 {'check':'phone-size preview control responds','result':'PASS'},
 {'check':'current browser viewport1265px content width1265px after long-identifier wrap repair','result':'PASS'},
 {'check':'visible loaded artwork broken-image count0','result':'PASS'}],
 'qualification':'Browser report usability and selected loaded images only; no artwork, touch-device or owner acceptance. Full local suite was still running at this check.'})
p=out/'PROVENANCE.json';d=json.loads(p.read_text());d['status']='EXACT_COPIED_PAINTED_GEODE_SOURCES_WITH_CURRENT_NATIVE_REVIEW'
d['current_native_review']='audit/job_geode_runtime_v1_20261001/REVIEW.json'
d['current_native_views_directly_reviewed']=36
for q in d['items']:
 q['runtime_score']=None
 q['sampled_mounted_object_finish']=4.6
 q['qualification']='Exact intact source state appears in reviewed current production captures. Object finish4.6; full timed action, room/contact, device/child/owner acceptance remain separate and incomplete.'
write(p,d)
target=out/'review_tools/record_geode_preview_v166.py';shutil.copyfile(__file__,target)
ip=b/'design/audit_impacts/job-geode-painted-runtime-20261001.json';d=json.loads(ip.read_text());d['files']=sorted(set(d['files'])|{p.relative_to(b).as_posix() for p in out.rglob('*') if p.is_file()});d['validation'].append({'command':'Browser report DOM, responsive overflow and selected exact HTTP artwork bytes','result':'PASS','evidence':'audit/job_geode_runtime_v1_20261001/LIBRARY_QA.json; report usability only.'});write(ip,d)
print('Recorded current source-bound review and observed library layout/HTTP evidence.')
