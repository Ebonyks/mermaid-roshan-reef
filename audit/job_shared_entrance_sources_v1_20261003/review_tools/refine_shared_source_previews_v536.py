from pathlib import Path
import datetime, hashlib, json, shutil, subprocess
b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');q=b/'audit/job_shared_entrance_sources_v1_20261003';l=b/'audit/job_artwork_refinement_live';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d,compact=False):
 n=p.with_name(p.name+'.new');n.write_text(json.dumps(d,ensure_ascii=False,**({'separators':(',',':')} if compact else {'indent':2}))+'\n',encoding='utf-8',newline='\n');n.replace(p)
r=json.loads((l/'ALL_ITEMS.json').read_text(encoding='utf-8'));before=sha(l/'ALL_ITEMS.json');review=json.loads((q/'DIRECT_NATIVE_REVIEW.json').read_text());changes=[]
for x in review['source_files']:
 for c in x['cells']:
  it=next(z for z in r['items'] if z['id']==c['id']);assert 'preview_display_region' not in it
  rx,ry,rw,rh=c['region'];bx,by,ex,ey=c['alpha_bbox'];bx=max(0,bx-8);by=max(0,by-8);ex=min(rw,ex+8);ey=min(rh,ey+8)
  it['preview_display_region']=[rx+bx,ry+by,ex-bx,ey-by];changes.append(dict(id=it['id'],exact_authored_cell=c['region'],read_only_display_window=it['preview_display_region']))
assert len(changes)==104
r['updated_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();write(l/'ALL_ITEMS.json',r,True);assert (l/'ALL_ITEMS.json').stat().st_size<4194304
p=l/'all_items.html';t=p.read_text(encoding='utf-8')
old="const regionStyle=q=>{const s=220/Math.max(q.region[2],q.region[3]),d=q.source_dimensions;return 'position:absolute;max-width:none;max-height:none;width:'+(d[0]*s)+'px;height:'+(d[1]*s)+'px;left:'+(-q.region[0]*s)+'px;top:'+(-q.region[1]*s)+'px;object-fit:fill'};"
new="const previewRegion=q=>q.preview_display_region||q.region;const regionStyle=q=>{const r=previewRegion(q),s=220/Math.max(r[2],r[3]),d=q.source_dimensions;return 'position:absolute;max-width:none;max-height:none;width:'+(d[0]*s)+'px;height:'+(d[1]*s)+'px;left:'+(-r[0]*s)+'px;top:'+(-r[1]*s)+'px;object-fit:fill'};"
assert t.count(old)==1;t=t.replace(old,new)
old="'style=\"height:'+(220*q.region[3]/Math.max(q.region[2],q.region[3]))+'px;width:'+(220*q.region[2]/Math.max(q.region[2],q.region[3]))"
new="'style=\"height:'+(220*previewRegion(q)[3]/Math.max(previewRegion(q)[2],previewRegion(q)[3]))+'px;width:'+(220*previewRegion(q)[2]/Math.max(previewRegion(q)[2],previewRegion(q)[3]))"
assert t.count(old)==1;t=t.replace(old,new);p.write_text(t,encoding='utf-8',newline='\n')
for p in [l/'index.html',l/'all_items.html']:
 t=p.read_text(encoding='utf-8').replace('V44 has 1934 known entries/772 source-cell-region priorities/48 current Candy priorities/377 source reviews remaining.','The earlier V44 checkpoint had 1934 entries/772 source-cell-region priorities/377 pending source reviews. V45 now has 2038 entries/888 source-cell-region priorities/602 unique source priorities/359 pending source reviews, plus the same 48 current Candy priorities.')
 t=t.replace('All 8 connected sources','All 10 connected sources').replace('missing bridgeA8 source 4.1 rejected','bridges A8/A9/A10 score 4.1/4.1/4.2 and remain rejected');p.write_text(t,encoding='utf-8',newline='\n')
shutil.copyfile(__file__,q/'review_tools/refine_shared_source_previews_v536.py')
shutil.copyfile(Path('C:/Users/Peter/Documents/mermaid-roshan-reef/tmp/SharedEntranceReportV536.png'),q/'SharedEntranceReportV536.png')
write(q/'NATIVE_CSS_PREVIEW_REFINEMENT_V536.json',dict(status='READ_ONLY_SOURCE_WINDOWS_REFINED',before_register_sha256=before,after_register_sha256=sha(l/'ALL_ITEMS.json'),windows=changes,qualification='Exact authored cell regions remain unchanged. Preview CSS uses original alpha bounds plus8px native padding so tiny lamps can be inspected. No bitmap crop file, resampling, repair pixels or source edits; existing other-region previews retain their exact previous geometry. Source scores and production boundary unchanged.'))
write(q/'BROWSER_QA_V536_INITIAL.json',dict(status='REPORT_RENDERING_PASS_LIBRARY_DETAIL_REFINEMENT_PENDING_RECHECK',report_articles=18,authored_cell_sections=104,images=122,all122_original_images_decoded=True,horizontal_overflow=False,report_screenshot=dict(path=(q/'SharedEntranceReportV536.png').relative_to(b).as_posix(),sha256=sha(q/'SharedEntranceReportV536.png')),library_search='D2X-0027-CELL',eight_matching_cells=True,library_2038_summary=True,qualification='Temporary in-app browser rendering and search only. Native CSS windows subsequently enlarged for tiny original props; final library recheck is pending. No game, browser persistence/status or creative acceptance claim.'))
ip=b/'design/audit_impacts/job-shared-entrance-source-review-20261003.json';d=json.loads(ip.read_text());d['files']=sorted(set(d['files'])|{p.relative_to(b).as_posix() for p in q.rglob('*') if p.is_file()});write(ip,d)
refresh=subprocess.run(['C:/Users/Peter/AppData/Local/Python/bin/python.exe','-X','utf8','-B',str(l/'review_tools/refresh_current_job_review_v45.py')],cwd=b,capture_output=True,text=True);assert refresh.returncode==0,refresh.stderr;print(refresh.stdout)
ap=b/'tmp/v2_preview_allowed.json';write(ap,sorted(set(json.loads(ap.read_text()))|set(d['files'])))
print('104 read-only native preview windows refined; exact cell definitions, scores and all source bitmap hashes unchanged.')
