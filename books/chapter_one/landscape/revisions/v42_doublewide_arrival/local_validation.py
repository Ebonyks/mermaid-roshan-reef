"""Execute local checks and preserve observed results; never invent test success or edit impacts."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse,unquote
import argparse,ast,datetime,hashlib,json,subprocess,sys
V=Path(__file__).resolve().parent;L=V.parents[1];R=L.parents[2]
ap=argparse.ArgumentParser();ap.add_argument('--run-contract-gates',action='store_true');a=ap.parse_args()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
checked=[]
for p in sorted(V.glob('*.py'))+[L/'render_book.py',L/'audit_book.py']:
 ast.parse(p.read_text('utf8'),filename=str(p));checked.append(p.relative_to(R).as_posix())
class Links(HTMLParser):
 def __init__(self):super().__init__();self.links=[]
 def handle_starttag(self,tag,attrs):self.links.extend(v for k,v in attrs if k in ['href','src'] and v)
links=[]
for p in [V/'REVISION_REVIEW.html',V/'complete/READ_BOOK.html']:
 parser=Links();parser.feed(p.read_text('utf8'))
 for link in parser.links:
  u=urlparse(link)
  if u.scheme or not u.path:continue
  target=(p.parent/unquote(u.path)).resolve();assert target.is_file(),(p,link)
  links.append(dict(document=p.relative_to(R).as_posix(),link=link,target=target.relative_to(R).as_posix()))
gate=json.loads((V/'complete/verification.json').read_text('utf8'))
assert gate['status']=='PASS_DOUBLEWIDE_REVIEW' and not gate['issues'],'Book gate has not passed for final review'
assert gate['pdf_sha256']==sha(V/'complete/Mermaid_Roshan_LANDSCAPE_ROUGH.pdf'),'Run book gate for current master'
book=json.loads((L/'book.json').read_text('utf8'))
assert book==json.loads((V/'BOOK_CURRENT.json').read_text('utf8'))
canonical=hashlib.sha256(json.dumps(book,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
assert gate.get('book_canonical_sha256')==canonical,'Run book gate for current controls; prior result is stale'
assert gate['provenance_sha256']==sha(V/'complete/page_provenance.json'),'Run book gate for current composition'
email=json.loads((V/'complete/email_verification.json').read_text('utf8'))
assert email['status']=='PASS' and email['source_sha256']==gate['pdf_sha256']
assert email['output_sha256']==sha(V/'complete/Mermaid_Roshan_Book_V42_Email.pdf')
assert gate['standalone_sha256']==sha(V/'complete/Sky_Lagoon_Doublewide_V42.pdf')
assert (V/'complete/READ_BOOK.html').read_text('utf8').count('<figure class="wide">')==1
runs=[]
if a.run_contract_gates:
 for args in [['tools/audit_document_authority.py'],['tools/audit_development.py','--base','auto'],['-m','unittest','tools.tests.test_audit_document_authority','tools.tests.test_audit_development']]:
  command=[sys.executable,'-X','utf8','-B']+args
  r=subprocess.run(command,cwd=R,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf8',errors='replace')
  runs.append(dict(command=command,returncode=r.returncode,output=r.stdout))
  print(r.stdout,end='',flush=True)
record=dict(status='PASS' if all(q['returncode']==0 for q in runs) else 'FAIL',scope='Syntax/local links and exact existing book-gate binding; contract gates only if explicitly executed',checked_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),python_syntax=checked,html_links=links,book_gate=gate['status'],book_verification_sha256=sha(V/'complete/verification.json'),contract_gate_runs=runs,unit_test_status='Executed; see observed unittest output' if a.run_contract_gates else 'NOT_RUN_IN_THIS_INVOCATION',runtime_tests='NOT_APPLICABLE: static book; no runtime/import/game/save/input/release changes',acceptance='B2/A9 closed as not needed at11in; owner illustration/child/SLP/physical print remain separate')
(V/'validation_results.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf8',newline='\n')
print('PASS local syntax/links' if record['status']=='PASS' else 'FAIL observed contract check')
if record['status']=='FAIL':raise SystemExit(1)
