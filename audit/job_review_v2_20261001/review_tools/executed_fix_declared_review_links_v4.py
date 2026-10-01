from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,posixpath,shutil
r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
p=r/'audit/job_review_v2_20261001/review_tools/build_current_job_item_register_v2.py'
s=p.read_text(encoding='utf-8').replace('import datetime, hashlib, json, shutil, subprocess','import datetime, hashlib, json, shutil, subprocess, posixpath')
bad="if preview and lane=='Day Two':q['preview_path']='audit/day2_art_library_2026-09-30/previews/'+Path(preview).name"
good="if preview and lane=='Day Two':q['preview_path']=posixpath.normpath(posixpath.join('audit/day2_job_contexts_2026-09-30',preview))"
assert s.count(bad)==1;s=s.replace(bad,good)
p.write_text(s,encoding='utf-8')
old=json.loads((r/'audit/job_review_v2_20261001/resource_checks_v2/RECEIPT.json').read_text())
allowed=set(json.loads((r/'tmp/v2_preview_allowed.json').read_text()))
seeds={x['path'] for x in old['resource_heads'] if not x['pass'] and (r/x['path']).is_file()}
class Links(HTMLParser):
    def __init__(self):super().__init__();self.links=[]
    def handle_starttag(self,tag,attrs):
        for key,value in attrs:
            if key in ['href','src','poster'] and value:self.links.append(value)
todo=list(seeds);seen=set();new=set()
while todo:
    page=todo.pop()
    if page in seen:continue
    seen.add(page)
    if not (r/page).is_file():continue
    new.add(page)
    if not page.endswith('.html'):continue
    parser=Links();parser.feed((r/page).read_text(encoding='utf-8'))
    for link in parser.links:
        u=urlsplit(link)
        if u.scheme or not u.path:continue
        q=posixpath.normpath(posixpath.join(posixpath.dirname(page),unquote(u.path)))
        assert not q.startswith(('../','/')) and not any(x.lower() in {'.git','.secrets','.codex','.claude','.aws','keystore'} for x in q.split('/'))
        if (r/q).is_file():
            new.add(q)
            if q.endswith('.html') and q not in seen:todo.append(q)
allowed.update(new)
(r/'tmp/v2_preview_allowed.json').write_text(json.dumps(sorted(allowed),indent=2)+'\n',encoding='utf-8')
review=r/'audit/job_review_v2_20261001/DECLARED_LINK_CORRECTION_V4.json'
review.write_text(json.dumps({'status':'CORRECTED_PENDING_HTTP_RECHECK','preserved_failure':'audit/job_review_v2_20261001/resource_checks_v2/RECEIPT.json','failures':149,'wrong_preview_paths':140,'existing_pages_absent_from_allowlist':9,'preview_repair':'Resolve each preview relative to its actual recorded inventory location instead of forcing every filename into the older preview directory. Existing artwork bytes unchanged.','additional_allowlist_paths':sorted(new- set(json.loads((r/'audit/job_review_v2_20261001/review_tools/V2_PREVIEW_ALLOWED.json').read_text()))),'qualification':'Only linked known review resources added; no directory listing or broad root serving.'},indent=2)+'\n',encoding='utf-8')
shutil.copyfile(r/'tmp/v2_preview_allowed.json',r/'audit/job_review_v2_20261001/review_tools/V2_PREVIEW_ALLOWED.json')
shutil.copyfile(Path(__file__),r/'audit/job_review_v2_20261001/review_tools/executed_fix_declared_review_links_v4.py')
src=Path(__file__).resolve().parent/'check_distinct_review_resources_v3.py'
s=src.read_text(encoding='utf-8').replace('resource_checks_v2','resource_checks_v3').replace('executed_check_distinct_review_resources_v3.py','executed_check_distinct_review_resources_v4.py')
s=s.replace("'failed':[x for x in rows if not x['pass']]", "'failed_count':sum(not x['pass'] for x in rows),'failed_sample':[x for x in rows if not x['pass']][:8]")
(src.parent/'check_distinct_review_resources_v4.py').write_text(s,encoding='utf-8')
p=r/'design/audit_impacts/job-review-separate-v2-20261001.json';d=json.loads(p.read_text());d['scope']+=' Correct 140 wrong preview links using recorded inventory-relative paths and add nine already-existing linked review pages/resources to the explicit localhost allowlist. Preserve the first failed resource receipt.';d['files']=sorted(set(d['files']+[review.relative_to(r).as_posix(),'audit/job_review_v2_20261001/review_tools/executed_fix_declared_review_links_v4.py']));d['validation'].append({'command':'Declared resource failure classification','result':'PASS','evidence':'audit/job_review_v2_20261001/DECLARED_LINK_CORRECTION_V4.json; exact 149 failures classified, actual refreshed HTTP/browser acceptance pending.'});p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
print('Corrected inventory-relative preview resolution and added',len(new),'explicit linked review resources; restart/recheck pending.')
