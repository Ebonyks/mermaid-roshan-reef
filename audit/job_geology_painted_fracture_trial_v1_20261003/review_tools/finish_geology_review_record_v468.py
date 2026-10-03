from pathlib import Path
import datetime,hashlib,json,shutil,subprocess
R=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');J=R/'audit/job_geology_painted_fracture_trial_v1_20261003';L=R/'audit/job_artwork_refinement_live'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
reg=read(L/'ALL_ITEMS.json');boundary=read(J/'SOURCE_CURRENT_BEFORE_CAPTURE.json')['source_files'];checks=read(J/'QA_CELL_SPOT_CHECK_V466.json')['rows']
assert reg['display_revision']=='V41_PAINTED_FOSSIL_FRACTURE_CANDIDATE_HISTORY'
assert sum(len(x.get('candidate_reviews',[])) for x in reg['items'])==24
assert (L/'ALL_ITEMS_V40.original.json').exists() and (J/'DIRECT_REVIEW_ATTEMPT02.json').exists()
oldcounts=read(L/'ALL_ITEMS_V40.original.json')['counts']
assert reg['counts']==oldcounts
ids={q['id']:q['id'] for q in reg['items'] if q.get('candidate_reviews')}
assert len(ids)==12
# The first tail retry wrote only HTML before missing the proof-only ids variable.
# Rebuild that derivative from the exact preserved V40 page to avoid duplicate links.
shutil.copyfile(L/'all_items_V40.original.html',L/'all_items.html')
source=Path(__file__).with_name('record_geology_fracture_review_v467.py')
script=source.read_text(encoding='utf-8')
# Continue only the interrupted HTML/impact tail. Do not repeat capture/review writes,
# immutable V40 archival or candidate-history append already completed successfully.
tail=script[script.index("html=(L/'all_items.html')"):]
scope=dict(globals());scope['__file__']=str(source)
exec(compile(tail,str(source),'exec'),scope)
write(J/'REPORT_HELPER_V467.json',{'status':'REPORT_TAIL_RESUMED_WITHOUT_REPEATING_RECORD_OR_HISTORY','failure':'First assertion required an explicit body tag; the existing valid library uses HTML implicit body. First tail retry omitted the proof-only ids variable after writing HTML. Neither failure changed production or captures.','correction':'Require the observed closing header only and derive the12 candidate ids from the recorded register. Rebuild derivative HTML from exact preserved V40 and resume tail once without repeated links, captures, source scores or history append.','scope':'Report helper errors, not game or visual failures.'})
shutil.copyfile(Path(__file__),J/'review_tools'/Path(__file__).name)
ip=R/'design/audit_impacts/job-geology-painted-fracture-trial-20261003.json';d=read(ip);d['files']=sorted(set(d['files'])|{x.relative_to(R).as_posix() for x in J.rglob('*') if x.is_file()});write(ip,d)
