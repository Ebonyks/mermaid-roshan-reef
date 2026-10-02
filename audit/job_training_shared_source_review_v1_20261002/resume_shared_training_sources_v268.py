from pathlib import Path
import datetime, json, shutil

b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');f=b/'audit/job_training_shared_source_review_v1_20261002';live=b/'audit/job_artwork_refinement_live'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
d=read(live/'ALL_ITEMS.json');assert d['counts']['registered_items']==1722 and d['counts']['unreviewed_current_source']==385
r=read(f/'REVIEW.json');baseline=r['baseline'];source_rows=[(x['id'],x['path'],x['score'],x['evaluation'],x['binding_trace']) for x in r['sources']]
assert not (b/'design/audit_impacts/job-training-shared-source-review-20261002.json').exists()
write(f/'PREPARATION_FAILURE.json',dict(status='PRESERVED_REVIEW_HELPER_FAILURE_NOT_GAME_FAILURE',recorded_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),helper='record_shared_training_sources_v267.py',failed_step='Live index insertion expected explicit<body>; this existing HTML uses implicit body and<main>.',already_completed=['Three direct source opinions and11 components','V29 register preserved, V30 counts1722/385 written','Additive master/finding note and scoped ledger update'],repair='Resume only live-index insertion, exact impact coverage and local allowlist at observed<main>. No repeated register append or rewrite of dated facts.',qualification='No production/input/save/asset image changed; this is a report-preparation failure, not a test or art pass.'))
shutil.copyfile(__file__,f/Path(__file__).name)
original=Path('C:/Users/Peter/Documents/mermaid-roshan-reef/tmp/record_shared_training_sources_v267.py').read_text(encoding='utf-8');tail=original[original.index("p=live/'index.html'"):].replace("needle='<body>'","needle='<main>'")
exec(compile(tail,str(f/Path(__file__).name),'exec'))
