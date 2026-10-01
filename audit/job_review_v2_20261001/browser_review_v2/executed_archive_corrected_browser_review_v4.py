from pathlib import Path
import datetime,hashlib,json,shutil
r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
out=r/'audit/job_review_v2_20261001/browser_review_v2';assert not out.exists();out.mkdir()
rows=[]
for name in ['wash_register_v2_browser_corrected.png','wash_register_v2_browser_source_fixed.png']:
    source=Path(__file__).resolve().parent/name;dst=out/name
    shutil.copyfile(source,dst)
    rows.append({'path':dst.relative_to(r).as_posix(),'sha256':hashlib.sha256(dst.read_bytes()).hexdigest(),'source':str(source),'modifications':'Exact screenshot bytes; no crop or pixel modification.','visual_review':'DIRECT'})
result={'status':'PASS_SCOPED_DESKTOP_BROWSER_LAYOUT_AND_SOURCE_PREVIEW','checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'screenshots':rows,'observed_width':1265,'observed_scroll_width':1265,'foam_search_matches':3,'shared_sink_search':'D2X-0001: one visible loaded image using audit/day2_job_contexts_2026-09-30/art/D2X-0001.webp','broken_observed_images':0,'resource_receipt':'audit/job_review_v2_20261001/resource_checks_v3/RECEIPT.json','preserved_failures':['audit/job_review_v2_20261001/browser_review_v1/REVIEW.json','audit/job_review_v2_20261001/resource_checks_v1/FAILURE.json','audit/job_review_v2_20261001/resource_checks_v2/RECEIPT.json'],'qualification':'Only refreshed desktop layout, relevant searches, declared resource reachability and native-video byte ranges checked. All registered source/native/action, ordinary game routes, phone, child and owner acceptance remain separate.'}
(out/'REVIEW.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
shutil.copyfile(Path(__file__),out/'executed_archive_corrected_browser_review_v4.py')
p=r/'ASSET_LICENSES.md';s=p.read_text(encoding='utf-8')
for row in rows:
    if row['path'] not in s:s+='\n| `'+row['path']+'` | Mermaid Roshan local browser review screenshot | Project review evidence; underlying artwork rights unchanged | Local V2 review http://127.0.0.1:8880/; SHA-256 `'+row['sha256']+'` | Exact screenshot; no pixel changes; corrected scoped desktop review; not runtime art |\n'
p.write_text(s,encoding='utf-8')
p=r/'design/audit_impacts/job-review-separate-v2-20261001.json';d=json.loads(p.read_text());d['files']=sorted(set(d['files']+[x.relative_to(r).as_posix() for x in out.rglob('*') if x.is_file()]));d['validation'].append({'command':'Direct refreshed V2 desktop browser review','result':'PASS','evidence':'audit/job_review_v2_20261001/browser_review_v2/REVIEW.json; width=scrollWidth=1265; three foam source records and repaired D2X-0001 image loaded. Scoped browser usability only, not all artwork acceptance.'});p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
print('Archived two directly reviewed corrected browser screenshots and scoped evidence.')
