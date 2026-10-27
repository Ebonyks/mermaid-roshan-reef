"""Check recorded visual-review bindings without manufacturing review or rewriting docs.

A changed PDF requires a new explicit review record written after inspection.
This helper never copies old observations onto a fresh artifact.
"""
from pathlib import Path
import hashlib,json
V=Path(__file__).resolve().parent;C=V/'complete'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
review=json.loads((V/'visual_audits.json').read_text('utf8'))
assert review['pdf_sha256']==sha(C/'Mermaid_Roshan_LANDSCAPE_ROUGH.pdf'),'Master changed; explicit visual re-review required'
assert review['email_sha256']==sha(C/'Mermaid_Roshan_Book_V41_Email.pdf'),'Email changed; explicit visual re-review required'
assert len(review['passes'])==5
for p in review['passes']:
 assert p['result']=='PASS_PART1_REVIEW' and not p['remaining_in_scope_defects']
 assert p['inspected'] and p['observations']
 for path in p['inspected']:
  assert (V/path).is_file(),path
  assert sha(V/path)==p['inspected_sha256'][path],('Stale inspected artifact',path)
print('Existing five-pass record matches the exact artifacts. No review claim or file was created.')
