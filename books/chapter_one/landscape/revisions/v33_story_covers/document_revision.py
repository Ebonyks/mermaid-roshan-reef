"""Record current cover review and navigation without changing interior evidence."""
from pathlib import Path
import datetime,hashlib,html,json
V=Path(__file__).resolve().parent;L=V.parents[1];R=L.parents[2]
def read(p):return json.loads(p.read_text('utf8'))
def write(p,s):p.write_text(s.rstrip()+'\n',encoding='utf8',newline='\n')
def save(p,d):write(p,json.dumps(d,ensure_ascii=False,indent=2))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ref(p):return dict(path=p.resolve().relative_to(R.resolve()).as_posix(),sha256=sha(p))
b=read(L/'book.json');ver=read(V/'complete/verification.json');e=read(V/'generation_evidence.json')
for q in e['generated']:q['review']='PASS root direct native composed-cover review: semantic correction, identity, complete contours, material joins and bubble detail inspected. Only recorded local polygons delivered. No new independent-agent or clinical sign-off.'
save(V/'generation_evidence.json',e)
open_items=[dict(id='OWNER_PAGE04_REPLACEMENT',pages=[4],issue='Owner rejected the V32 dusty-object insert. A quiet help-request page before the Puff reveal was recommended on2026-10-02 but has not been commissioned for implementation. This cover-only revision deliberately preserves all32 current interiors; that editorial item remains open.')]
save(V/'visual_review.json',dict(revision='V33',revision_verdict='REQUESTED_COVER_CORRECTIONS_REVIEWED; OTHER_EDITORIAL_ACCEPTANCE_OPEN',reviewer='Root direct native review; no additional agent review commissioned',reviewed_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),book=ref(L/'book.json'),pdf=ref(V/'complete/Mermaid_Roshan_LANDSCAPE_ROUGH.pdf'),page_provenance=ref(V/'complete/page_provenance.json'),changed_pages=[dict(page=0,proof=ref(V/'complete/page_00.png'),findings_closed=['Removed front tipped pink paint pot, spilled paint/drops and illustrated craft paper.','Puff now has worried brows/eyes and a downturned unwell mouth, matching his care story.'],observed='All four main characters, original costumes, anatomy, welcoming pose, cleaning bucket/brush/sponge, rainbow waterfall and title remain intact. Marble material joins have no observed cut seam or rectangular repair patch. Exact outside-polygon preservation is separately proved.',internal_verdict='PASS_ROOT_NATIVE_COVER_REVIEW'),dict(page=33,proof=ref(V/'complete/page_33.png'),findings_closed=['Retired the obsolete ensemble craft-table/drawing scene.','Rear now depicts the actual page26 cooperative washing event, using its exact authored scene layers.'],observed='Daddy and Eagle brush Puff; Roshan and Rumi use the existing yellow and pink sponges. Support/contact, faces/tails and original soap/bubble contours remain identical to26 outside its removed caption and tiny shelf cameo. Canonical white Lamma head peeks discreetly behind a shelf teapot; no lettering or extra activity.',internal_verdict='PASS_ROOT_NATIVE_COVER_REVIEW')],retained_interior_evidence=dict(prior_review=ref(V.parent/'v32_rainbow_story/visual_review.json'),retained_only_on_exact_png_identity=list(range(1,33)),no_new_pedagogical_or_art_approval_claim=True),open_findings=open_items,external_acceptance_open=['Owner cover approval','Roshan shared-reading response','Physical print/color/native-density proof','Qualified SLP review remains unperformed; text is unchanged'],scope='Static covers only. No game/runtime, protected-original, clinical or master-audit closure. Prior numeric4.9 judgments do not override owner rejection of page4.'))
save(V/'COMPLETION_AUDIT.json',dict(status='REQUESTED_COVER_REPAIRS_COMPLETE_LOCALLY; REMOTE_BYTES_TO_VERIFY_AFTER_PUSH',baseline='2719d2fcf66afe4cb73b8445087e09dd52319849',requirements=[dict(id='front-promises-current-story',result='PASS',evidence=ref(V/'visual_review.json')),dict(id='rear-actual-cooperative-washing',result='PASS',evidence=ref(V/'complete/verification.json')),dict(id='retain32interiors-and34total',result='PASS',evidence=ref(V/'complete/verification.json')),dict(id='preserve-source-art-and-targeted-edit-scope',result='PASS',evidence=ref(V/'generation_evidence.json'))],open_findings=open_items))
style='body{font:17px/1.5 system-ui;background:#e8f5fa;color:#16364d;margin:0}header,article{max-width:1260px;margin:24px auto;background:white;padding:24px;border-radius:12px}.pair{display:grid;grid-template-columns:1fr 1fr;gap:18px}figure{margin:0}img{width:100%;display:block}figcaption{padding:8px 0;font-weight:600}a{color:#16648f}@media(max-width:760px){.pair{grid-template-columns:1fr}}'
cards=[]
for n in [0,33,*range(1,33)]:
 label='Front cover' if n==0 else 'Rear cover' if n==33 else f'Story{n}'
 note='Removed obsolete painting cues and corrected Puff’s mood.' if n==0 else 'Actual group-washing scene26 replaces the craft gathering; tiny Lamma retained.' if n==33 else 'Exact V32 proof bytes retained.'
 cards.append(f'<article id="page-{n}"><h2>{label}</h2><p>{html.escape(note)}</p><div class="pair"><figure><figcaption>V32</figcaption><img loading="lazy" src="../v32_rainbow_story/complete/page_{n:02}.png"></figure><figure><figcaption>V33</figcaption><img loading="lazy" src="complete/page_{n:02}.png"></figure></div></article>')
write(V/'AUDIT_REVIEW.html',f'<!doctype html><meta charset="utf-8"><title>V33 story-faithful covers</title><style>{style}</style><header><h1>V33 · Covers match the cleaning story</h1><p>Only the front and rear change. All32 interiors retain exact V32 bytes;34 pages including covers.</p><p><a href="complete/READ_BOOK.html">Reader</a> · <a href="complete/Mermaid_Roshan_Book_V33_Email.pdf">Email PDF under25MB</a> · <a href="complete/Mermaid_Roshan_LANDSCAPE_ROUGH.pdf">Lossless master</a> · <a href="visual_review.json">Native review</a> · <a href="complete/verification.json">Mechanical evidence</a></p><p>Root inspected both changed native covers; no new independent or professional review is claimed. Owner/child/print acceptance and the previously rejected interior4 remain open.</p></header>'+''.join(cards))
spreads=['<article><h2>Exterior covers</h2><div class="pair"><img src="complete/page_33.png"><img src="complete/page_00.png"></div></article>','<article><h2>Inside front / Story1</h2><div class="pair"><p>Inside front cover</p><img src="complete/page_01.png"></div></article>']
for left in range(2,32,2):spreads.append(f'<article><h2>Story{left}–{left+1}</h2><div class="pair"><img loading="lazy" src="complete/page_{left:02}.png"><img loading="lazy" src="complete/page_{left+1:02}.png"></div></article>')
spreads.append('<article><h2>Story32 / Inside rear</h2><div class="pair"><img src="complete/page_32.png"><p>Inside rear cover</p></div></article>')
write(V/'PRINT_DUMMY.html',f'<!doctype html><meta charset="utf-8"><title>V33 bound spread dummy</title><style>{style}</style><header><h1>V33 · Bound spread dummy</h1><p>Covers separate from32 interiors; story1 right. Door23→Puff24 and bubbles27→rainbow28 remain across page turns. Physical printer/binding approval pending.</p></header>'+''.join(spreads))
save(V/'print_pagination.json',dict(revision='V33',total_authored_pages=34,interiors=32,book_sha256=sha(L/'book.json'),pdf_sha256=sha(V/'complete/Mermaid_Roshan_LANDSCAPE_ROUGH.pdf'),first_story_side='right',reveals=[dict(setup=23,reveal=24),dict(setup=27,reveal=28)],interior_pagination_unchanged=True))
write(V/'README.md','''# V33 — covers match the cleaning story

Status: `SUPPORTING_CURRENT`; requested cover correction review complete, owner/child/physical-print acceptance open.34 total pages,32 interiors,7 ×5 inches landscape,Sniglet. Exact V32 baseline: `2719d2fcf66afe4cb73b8445087e09dd52319849`.

[Before/after](AUDIT_REVIEW.html) · [Reader](complete/READ_BOOK.html) · [Email PDF under25MB](complete/Mermaid_Roshan_Book_V33_Email.pdf) · [Lossless master](complete/Mermaid_Roshan_LANDSCAPE_ROUGH.pdf) · [Spread dummy](PRINT_DUMMY.html) · [Manifest](manifest.json)

The front no longer promises a painting activity: the tipped pink pot, spill/drops and illustrated paper are removed through a bounded floor inpaint. The hidden lavender Puff has the worried/unwell expression appropriate to a friend needing care. The original ensemble, cleaning supplies, rainbow waterfall, title and prior identity repairs remain unchanged outside those two polygons.

The rear retires the obsolete craft-table gathering and uses the actual story26 cooperative washing scene. Original source layers, transforms, fixtures, anatomy and brush/sponge contacts are reused exactly; the interior caption is omitted. A tiny canonical Lamma head is locally added behind a rear-shelf teapot. This retains two silent appearances, story10 and rear33, without a child-facing clue. No full-scene generation or invented scene is delivered.

Two built-in ImageGen local candidates supply only declared polygons. [Prompts, reference roles/hashes, native outputs and scope](generation_evidence.json) are preserved alongside originals. The caption-free reference PNGs are PDF-derived inputs only; final delivery reuses original art layers, never a flattened reference screenshot. All230 baseline source/font files remain Git-identical.

[Root native review](visual_review.json) and [mechanical verification](complete/verification.json) are separate evidence. All32 interior PNGs are byte-identical to V32; all34 lossless PDF renders match current PNGs; title/manuscript text, font, trim and reveal turns are unchanged. Front pixels outside two added polygons are exact. Rear pixels equal story26 outside its omitted caption and tiny shelf polygon. The email derivative preserves native image sizes, vector text, geometry and lossless alpha while recompressing RGB streams; see [email verification](complete/email_verification.json).

The owner's rejected V32 dusty-object page4 remains an open editorial item. The quiet request-for-help replacement was recommended, but not commissioned for implementation. This cover-only repair does not claim whole-book acceptance or carry forward a numeric score over that rejection. Qualified SLP review remains unperformed; current words are unchanged. Native print density, paper/color/binding and actual child response remain separate from digital checks. No game/runtime/master-finding, device or release work.

## Rebuild and publication

Use `render_book.py --output .../v33_story_covers/complete`, then this folder's `optimize_pdf_lossless.py`, `verify_revision.py` and `email_export.py`. New renders require fresh native review and exact audit bindings. `document_revision.py` records navigation/review, `package_revision.py` records the exact manifest/coverage, and `run_project_gates.py` records applicable authority/coverage tests. See [project gates](project_gates.json).

Established destination: `Ebonyks/mermaid-roshan-reef`, branch `codex/mermaid-roshan-picture-book`. After push, `verify_remote.py <exact-commit> --receipt <outside-repo-path>` fetches the manifest and every required file through anonymous HTTPS. Publication and byte identity do not grant creative acceptance. No dev/master integration or release is commissioned.
''')
write(L.parent/'README.md','''# Mermaid Roshan — Chapter One picture book

Current edition: **V33 — covers match the cleaning story**.34 pages including both covers;32 interiors;7 ×5 inches landscape;Sniglet.

[Before/after](landscape/revisions/v33_story_covers/AUDIT_REVIEW.html) · [Reader](landscape/revisions/v33_story_covers/complete/READ_BOOK.html) · [Email PDF under25MB](landscape/revisions/v33_story_covers/complete/Mermaid_Roshan_Book_V33_Email.pdf) · [Lossless master](landscape/revisions/v33_story_covers/complete/Mermaid_Roshan_LANDSCAPE_ROUGH.pdf) · [Versioned package](landscape/revisions/v33_story_covers/README.md)

The front removes the obsolete paint spill/drawing paper and gives Puff a worried expression. The rear uses the book's actual cooperative washing scene, with a tiny hidden Lamma. All32 interiors remain byte-identical to V32. Original art/font files remain unchanged. [Design language](DESIGN_LANGUAGE.md), [page plan](landscape/PAGE_PLAN.md), [review](landscape/REVIEW.md), [story audit](landscape/STORY_COMPREHENSION_AUDIT.md), [current cover audit](landscape/revisions/v33_story_covers/visual_review.json) and [manifest](landscape/revisions/v33_story_covers/manifest.json) record scope.

The previously rejected interior4 and its proposed quiet-request replacement remain open; this commission repairs covers only. Owner/child/physical-print and professional SLP acceptance remain separate. Earlier dated editions preserve their original evidence. No game/runtime, protected-original or release change; Resolve/handoff searching remains stopped.
''')
p=L/'PAGE_PLAN.md';s=p.read_text('utf8').replace('# V32 current page plan','# V33 current page plan')
s=s.replace('Status: `SUPPORTING_CURRENT`.','Status: `SUPPORTING_CURRENT`. Interior pagination and exact caption table below are unchanged from V32. V33 changes only covers; see [cover comparison](revisions/v33_story_covers/AUDIT_REVIEW.html).',1)
s=s.replace('Front and rear covers retain V31 artwork; rear has no text.','Front retains its original rendering with bounded painting-debris removal and unwell Puff expression. Rear reuses the actual story26 washing scene without text and adds a tiny shelf Lamma.')
s=s.replace('[book.json](book.json); [pagination](revisions/v32_rainbow_story/pagination.json) records the map.','[book.json](book.json); [V32 pagination](revisions/v32_rainbow_story/pagination.json) retains the interior map. The owner-rejected page4 and proposed quiet-request replacement remain unimplemented and open.')
write(p,s)
write(L/'REVIEW.md','''# V33 current review

Status: `SUPPORTING_CURRENT`. [V33](revisions/v33_story_covers/README.md) corrects the two covers over V32 baseline `2719d2fcf66afe4cb73b8445087e09dd52319849`; all32 interiors retain exact V32 PNG bytes and caption/source configurations.

Front: remove the tipped paint pot, paint spill/drops and illustrated craft paper; locally replace Puff's mischievous expression with worried/unwell features. Rear: replace the obsolete craft gathering with the exact existing scene26 group washing. Only one tiny shelf Lamma is inpainted into that scene; the full scene is not regenerated. Prior files, identity repairs, font, text, trim and both reveal turns are preserved.

[Root native review](revisions/v33_story_covers/visual_review.json), [machine verification](revisions/v33_story_covers/complete/verification.json), [generation evidence](revisions/v33_story_covers/generation_evidence.json), [email verification](revisions/v33_story_covers/complete/email_verification.json), [stress checks](revisions/v33_story_covers/complete/stress_results.json) and [project gates](revisions/v33_story_covers/project_gates.json) bind the actual outputs. Root reviewed both covers directly; no new independent agent, clinical or child approval is claimed. All230 original source/font files remain exact; all34 lossless PDF renders match native PNGs; bounded source/text preservation checks pass. The separate email derivative preserves text and image sizes under25MB.

Owner rejection of the V32 dusty-object insert4 remains open. Its recommended quiet help-request replacement was analysis, not an implementation commission; covers-only work does not close it or establish whole-book4.9 acceptance. Professional SLP review, child enjoyment/comprehension and physical print/color/paper/binding/native-density acceptance remain open. Native full-art density is unchanged (many frames roughly212ppi at trim). No game/runtime, device, master-finding or release acceptance.
''')
p=L/'STORY_COMPREHENSION_AUDIT.md';s=p.read_text('utf8').replace('# V32 story comprehension and shared-reading audit','# V33 story comprehension and shared-reading audit')
s=s.replace('Status: `SUPPORTING_CURRENT`.','Status: `SUPPORTING_CURRENT`. V33 leaves all V32 interior text and pictures exact; only cover promises are corrected. The owner rejected the dusty-object insert4 after the V32 review. A quiet request from behind Puff’s door was recommended but remains unimplemented; this editorial item stays open. The unchanged sequence below describes the actual proof, not acceptance of that insert.',1)
write(p,s)
p=L.parent/'DESIGN_LANGUAGE.md';s=p.read_text('utf8');marker='## V33 owner correction: cover story truth (2026-10-17)'
if marker in s:s=s[:s.index(marker)].rstrip()
write(p,s+'\n\n'+marker+'''

The owner rejects cover elements representing events absent from the current story. Remove the front's paint-making spill and drawing paper through bounded floor repair; give Puff his unwell, care-seeking expression. Retire rear H's obsolete craft gathering. Reuse the exact existing story26 cooperative washing scene for the rear, omitting its caption and retaining one tiny canonical shelf Lamma through a local patch. Preserve original source artwork, identity, contact, fixtures, all32 interiors, title/font/trim and both reveal turns. No full-scene redraw is authorized or needed. V33 owns current cover facts; earlier cover approvals are superseded only for these named deficiencies. The rejected interior4 remains a separate open editorial item. Publication and machine checks do not establish owner/child, professional SLP or physical-print approval.
''')
p=V.parent/'v32_rainbow_story/README.md';s=p.read_text('utf8').replace('Status: `SUPPORTING_CURRENT`;','Status: `HISTORICAL_EVIDENCE`; original published V32 proof; [V33](../v33_story_covers/README.md) supersedes its cover facts.');write(p,s)
p=R/'design/05_DOC_LEDGER.md';lines=p.read_text('utf8').splitlines()
changes={
'books/chapter_one/README.md':('🔵','`SUPPORTING_CURRENT`; V33 cover continuity repair and current34-page reader/email/master navigation; all32 V32 interiors preserved, owner-rejected4 remains open.'),
'books/chapter_one/landscape/PAGE_PLAN.md':('🔵','`SUPPORTING_CURRENT`; V33 cover treatments and unchanged V32 exact32-page interior table/reveals; rejected interior4 remains open.'),
'books/chapter_one/landscape/REVIEW.md':('🔵','`SUPPORTING_CURRENT`; V33 source-faithful cover repairs,32 byte-identical interior proofs, exact masks/source/master and email checks; owner/child/print/SLP acceptance and rejected4 remain open.'),
'books/chapter_one/landscape/STORY_COMPREHENSION_AUDIT.md':('🔵','`SUPPORTING_CURRENT`; V33 cover promises match actual cleaning; V32 interior descriptions retained with owner rejection of4 and unimplemented replacement explicit; no clinical/child acceptance.'),
'books/chapter_one/landscape/revisions/v32_rainbow_story/README.md':('⚪','`HISTORICAL_EVIDENCE`; original V32 magical rainbow story/pagination/proof and audits; V33 repairs covers and retains32 exact interiors. Rejected insert4 remains open.'),
}
for i,line in enumerate(lines):
 for key,(icon,desc) in changes.items():
  if line.startswith('| `'+key+'` |'):lines[i]=f'| `{key}` | {icon} | {desc} |'
new=f'| `{V.relative_to(R).as_posix()}/README.md` | 🔵 | `SUPPORTING_CURRENT`; V33 removes obsolete front painting cues/mischievous Puff and replaces rear craft gathering with actual scene26 washing; bounded native art, unchanged32 interiors, email/master proofs and source/remote evidence; owner/child/print/SLP and rejected4 remain open. |'
if new not in lines:lines.append(new)
write(p,'\n'.join(lines))
if not (V/'project_gates.json').exists():save(V/'project_gates.json',dict(status='PENDING',checks=[]))
print('Current review/navigation and honest remaining editorial scope recorded.')
