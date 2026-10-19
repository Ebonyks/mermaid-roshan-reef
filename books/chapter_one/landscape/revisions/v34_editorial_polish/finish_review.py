"""Bind the completed root visual review and owner-authorized Downloads copy."""
from pathlib import Path
import datetime, hashlib, json, shutil
V = Path(__file__).resolve().parent
C = V / 'complete'
R = V.parents[4]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p): return json.loads(p.read_text('utf8'))
def save(p, d): p.write_text(json.dumps(d, ensure_ascii=False, indent=2)+'\n', encoding='utf8', newline='\n')
master = C/'Mermaid_Roshan_LANDSCAPE_ROUGH.pdf'
email = C/'Mermaid_Roshan_Book_V34_Email.pdf'
v = read(C/'verification.json'); e = read(C/'email_verification.json')
assert v['status'] == e['status'] == 'PASS'
assert sha(master) == v['pdf_sha256'] == e['source_sha256']
assert sha(email) == e['output_sha256']
record = dict(
    reviewer='Root Codex visual/editorial review, 2026-10-18',
    checked_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    status='REVIEW_CANDIDATE_ACCEPTED_FOR_OWNER_REVIEW',
    master_sha256=sha(master), email_sha256=sha(email),
    page_proofs=[dict(page=i, sha256=sha(C/f'page_{i:02}.png')) for i in range(34)],
    scope=['All 34 pages inspected using contact sheets and full page proofs; selected source/character/style comparisons and native details inspected.',
           'Final pages 1, 23, 24 and 25 rechecked at native proof scale after header rejection and little-puff correction.',
           'Final email front/rear native samples inspected; per-page pixel comparison, native dimensions, alpha masks and editable type verified independently.',
           'Only little puffs in low marginal banks; Grand Puff retains his main narrative role. No new full narrative-scene redraw used.'],
    rejected=['Grand-Puff-shaped bank studies', 'oversized marginal figures', 'extra door knob',
              'entry/floor inpaints with visible joins', 'both aircraft header extensions with visible joins'],
    open=['Owner and child reading/creative acceptance', 'Qualified SLP review',
          'Final restoration/upsampling, trim/reflow, crown headroom, bleed and physical print',
          'Source ear identity held; literal bath-drain and waterfall-action source gaps not invented'],
    scoring='No unmeasured 4.9/5 or clinical approval claim.'
)
save(V/'visual_review.json', record)
e['visual_review']='Root native final email front/rear samples: PASS for owner-review delivery. Clinical, final-resolution and print acceptance remain open.'
save(C/'email_verification.json', e)
dest=Path('C:/Users/Peter/Downloads/Mermaid_Roshan_Book_V34_Email.pdf')
if dest.exists() and sha(dest)!=sha(email):
    dest=dest.with_name('Mermaid_Roshan_Book_V34_Editorial_20261018_Email.pdf')
assert not dest.exists() or sha(dest)==sha(email), 'Preserve existing differing download'
if not dest.exists(): shutil.copyfile(email, dest)
assert sha(dest)==sha(email)
save(V/'downloads_receipt.json', dict(path=dest.as_posix(), bytes=dest.stat().st_size, sha256=sha(dest), source=email.relative_to(R).as_posix(), checked_at_utc=record['checked_at_utc']))
print(json.dumps(dict(visual_review='recorded', download=dest.as_posix(), bytes=dest.stat().st_size)))
