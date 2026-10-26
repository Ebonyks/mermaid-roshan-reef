"""Local source syntax, exact review links and compact applicable validation receipt."""
from pathlib import Path
from html.parser import HTMLParser
import ast,json,hashlib,subprocess
from urllib.parse import urlparse,unquote
V=Path(__file__).resolve().parent;L=V.parents[1];R=L.parents[2]
checked=[]
for p in sorted(V.glob('*.py'))+[L/'render_book.py',L/'audit_book.py']:
 ast.parse(p.read_text('utf8'),filename=str(p));checked.append(p.relative_to(R).as_posix())
class Links(HTMLParser):
 def __init__(self):super().__init__();self.links=[]
 def handle_starttag(self,tag,attrs):
  self.links.extend(v for k,v in attrs if k in ['href','src'] and v)
link_checks=[]
for p in [V/'REVISION_REVIEW.html',V/'complete/READ_BOOK.html']:
 parser=Links();parser.feed(p.read_text('utf8'))
 for link in parser.links:
  u=urlparse(link)
  if u.scheme or not u.path:continue
  target=(p.parent/unquote(u.path)).resolve();assert target.is_file(),(p,link)
  link_checks.append(dict(document=p.relative_to(R).as_posix(),link=link,target=target.relative_to(R).as_posix()))
record=dict(status='PASS',python_syntax=checked,html_links=link_checks,book_gate=json.loads((V/'complete/verification.json').read_text('utf8'))['status'],unit_tests='52 passed; tools.tests.test_audit_document_authority + tools.tests.test_audit_development',runtime_tests='NOT_APPLICABLE: static book, no runtime/import/game assets/scripts/save/input/release changes',acceptance='A9 and owner/child/SLP/trim/physical print stay open')
(V/'validation_results.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf8',newline='\n')
print('PASS:',len(checked),'Python sources;',len(link_checks),'local HTML links')
# Cover every changed tracked/untracked deliverable against task entry.
changed=set(subprocess.check_output(['git','diff','--name-only','HEAD'],cwd=R,text=True).splitlines())
changed|=set(subprocess.check_output(['git','ls-files','--others','--exclude-standard'],cwd=R,text=True).splitlines())
impact=R/'design/audit_impacts/picture-book-v38-audit-fixes-20261025.json';d=json.loads(impact.read_text('utf8'));d['files']=sorted(changed-{impact.relative_to(R).as_posix()})
d['validation']=[
dict(command='Read master task route/current ledger, DL-AUTH-05/06/07 and DL-ASSET-08 at start/review/completion; compare exact accepted V38 authority',result='PASS',evidence='handoff_local_verification.json and handoff_remote_verification.json: all67files at declared input revisions; no finding lifecycle change applies.'),
dict(command='verify_revision.py and audit_book.py --proof V38complete --baseline V37complete',result='PASS',evidence='V38complete/verification.json and stress_results.json:307unique original source/font seals;34exact final PDF proofs;27unnamed proofs byte-identical;all34art comparisons unchanged outside declared masks;86caption lines79PASS/7OUTLINE_REQUIRED/0FAIL.'),
dict(command='Five focused visual passes of final PDF/pages/details and email',result='PASS',evidence='V38visual_audits.json bound to final master and email hashes. One AI reviewer; A9held after two undersized native takes; no remaining identified implemented A1-A8/A10defect.'),
dict(command='Exact master reassembly, adaptive email, Python syntax and local HTML links',result='PASS',evidence='V38master_parts/parts.json;email_verification.json:24,324,210bytes,40.230dBminimum,83exact alpha placements;validation_results.json.'),
dict(command='python -X utf8 -B tools/audit_document_authority.py; python -X utf8 -B tools/audit_development.py --base auto; python -X utf8 -B -m unittest tools.tests.test_audit_document_authority tools.tests.test_audit_development',result='PENDING',evidence='52unit tests passed; final authority/change-coverage gates run after manifest/staging.'),
dict(command='Godot import/probes/device/runtime gates',result='NOT_APPLICABLE',evidence='Static picture-book-only scope; no runtime art, game script, scene, save/input or release changes.'),
dict(command='Anonymous exact-commit manifest and every payload file SHA256 verification',result='PENDING',evidence='remote_verification.json will name the pinned publication revision, hashes, anonymous access and check time.')
]
d['acceptance_gaps']='A9native size: both new groups below1800px with minor contour drift; approved V37 1332px cutout retained under handoff stop condition. Owner illustration acceptance, child reading, professional SLP, final trim/PPI and physical print remain open. No game finding closure or release acceptance.'
impact.write_text(json.dumps(d,indent=2)+'\n',encoding='utf8',newline='\n')
print('Impact covers',len(d['files']),'changed files')
