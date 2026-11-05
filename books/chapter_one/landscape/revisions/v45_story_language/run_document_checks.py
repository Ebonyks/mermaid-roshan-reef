"""Capture mandatory project gates without inferring their result from output text."""
import datetime,subprocess,sys,time
from build_revision import V,R,C,read,save,sha

commands=[['tools/audit_document_authority.py'],['tools/audit_development.py','--base','auto'],
          ['-m','unittest','tools.tests.test_audit_document_authority','tools.tests.test_audit_development']]
checks=[]
for tail in commands:
    command=[sys.executable,'-X','utf8','-B']+tail
    start=time.monotonic();r=subprocess.run(command,cwd=R,capture_output=True,text=True,encoding='utf8')
    q=dict(command=command,exit_code=r.returncode,seconds=round(time.monotonic()-start,3),stdout=r.stdout,stderr=r.stderr)
    checks.append(q);print('exit',r.returncode,':',' '.join(tail),flush=True)
    print(r.stdout,flush=True);print(r.stderr,flush=True)
record=dict(status='PASS' if all(q['exit_code']==0 for q in checks) else 'FAIL',checked_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),checks=checks,
    book_verification=dict(path='complete/verification.json',status=read(C/'verification.json')['status'],sha256=sha(C/'verification.json')),
    source_baseline='550a0b86216dee020d5070428ab4ddcfe0da4dc1',
    earlier_checks='Initial document-navigation gate failed only because manifest.json was not yet created. QA/preflight01 retains initial six contrast failures and two margin failures. These are not current acceptance.',
    runtime_scope='Book-only files; game/runtime/protected/workflow files unchanged. No new Godot/device/child/release claim.')
save(V/'validation_results.json',record)
impact=R/'design/audit_impacts/picture-book-v45-language-20261031.json';d=read(impact)
d['scope']='Critique and implement V45 as a review draft:24exact proposed captions, exact page21 bubbles and one declared concise page11 editorial adaptation to preserve fixed-size readability/clear action; unchanged artwork/covers/order/type sizes. Publish on established picture-book branch with anonymous verification.'
d['validation'][0]=dict(command='Existing audit_book.py V45 route: source/applied manuscript, art/image/alpha/vector preservation, nine complete unchanged entries, outside-caption pixels, actual glyph geometry and unchanged V37 composed contrast',result='PASS' if read(C/'verification.json')['status']=='PASS_TEXT_ART_EXPORT_AND_CONTRAST' else 'FAIL',evidence='books/chapter_one/landscape/revisions/v45_story_language/complete/verification.json; exact PDF '+sha(C/'Mermaid_Roshan_and_the_Dust_Bunnies_V45.pdf')+';24source-exact changed captions and explicit page11 adaptation. Actual V44 counts77PASS/7outline/0FAIL; V45 counts93PASS/9outline/0FAIL.')
d['validation'][1]=dict(command='Authority/development audits and two audit unit-test modules',result=record['status'],evidence='books/chapter_one/landscape/revisions/v45_story_language/validation_results.json; exact commands, exits, output and elapsed times retained.')
d['acceptance_gaps']='Owner review of V45/new story facts/page11 concise adaptation, actual oral reading/read-aloud with Roshan, qualifiedSLP, inherited BK44-O01/O02 continuity, physical print/arrival binding and V41Part2 remain open. No game/release change. Publication evidence is recorded separately after payload commit.'
save(impact,d)
if record['status']!='PASS':raise SystemExit(1)
