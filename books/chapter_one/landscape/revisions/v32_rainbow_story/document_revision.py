"""Publish current navigation and exact manuscript without altering sealed proof pixels."""
from pathlib import Path
import html,json,re
V=Path(__file__).resolve().parent; L=V.parents[1]; R=L.parents[2]
B=json.loads((L/'book.json').read_text('utf8')); M=json.loads((V/'pagination.json').read_text('utf8'))
def write(p,s):p.write_text(s.rstrip()+'\n',encoding='utf8',newline='\n')
write(L.parent/'README.md', '''# Mermaid Roshan — Chapter One picture book

Current edition: **V32 — the magic rainbow pool and a shared welcome**.34 pages including covers;7 ×5 inches landscape;Sniglet. Roshan and her friends clean Pearl Castle and help dusty Grand Puff feel better.

[Before and after, every page](landscape/revisions/v32_rainbow_story/AUDIT_REVIEW.html) · [Reader](landscape/revisions/v32_rainbow_story/complete/READ_BOOK.html) · [Full PDF](landscape/revisions/v32_rainbow_story/complete/Mermaid_Roshan_LANDSCAPE_ROUGH.pdf) · [Versioned package](landscape/revisions/v32_rainbow_story/README.md)

[Design language](DESIGN_LANGUAGE.md), [page plan](landscape/PAGE_PLAN.md), [verification and limits](landscape/REVIEW.md), [story audit](landscape/STORY_COMPREHENSION_AUDIT.md), [independent review](landscape/revisions/v32_rainbow_story/visual_review.json), [local generation evidence](landscape/revisions/v32_rainbow_story/generation_evidence.json) and [manifest](landscape/revisions/v32_rainbow_story/manifest.json) describe current facts.

Existing waterfall colors are restored; Daddy explicitly explains the pool's magic. Puff's reflection, thanks and invitation to rest share one page. The freed page introduces dusty castle belongings through complete contour cutouts. A quiet clean-room result closes the castle work.28 mapped proof pages remain byte-identical to V31, including both covers. V31 and earlier editions are historical evidence. Internal review remains separate from owner, child, professional SLP and physical-print acceptance. No game/runtime or protected-original changes. Resolve/handoff searching remains stopped.
''')
rows=[]
for p,m in zip(B['pages'],M['rows']):
 old='New source-derived insert' if m['baseline_page'] is None else str(m['baseline_page'])
 if p['page']==31:old='30 +31 (combined)'
 rows.append(f"| {p['page']} | {p['mode']} | {old} | {p['text'].replace(chr(10),' / ')} |")
write(L/'PAGE_PLAN.md','''# V32 current page plan

Status: `SUPPORTING_CURRENT`.34 total pages, both covers included;32 interiors;7 ×5 inches landscape;Sniglet. F = full art. C = complete irregular contour cutouts on contextual low blue stationery. Reduced scenic rectangles are excluded.

New4 expands dusty-castle inspection. Old4–21 shift forward one place; old22 becomes the quiet clean-room result30.23–29 remain in place. Old30 and31 combine into31;32 and both covers remain unchanged. Door23→Puff24 and bubbles27→rainbow28 still cross page turns. Story1 starts on the right. See [mapped comparison](revisions/v32_rainbow_story/AUDIT_REVIEW.html) and [spread dummy](revisions/v32_rainbow_story/PRINT_DUMMY.html).

| Story | Treatment | V31 source page | Exact caption |
|---|---|---|---|
'''+ '\n'.join(rows)+'''

Front and rear covers retain V31 artwork; rear has no text. Hidden Lamma appearances remain on new10 and the rear cover, unprompted. Source assignments, low-bank motifs, caption geometry and derivative masks are exact in [book.json](book.json); [pagination](revisions/v32_rainbow_story/pagination.json) records the map.
''')
write(L/'REVIEW.md','''# V32 current review

Status: `SUPPORTING_CURRENT`. V32 implements the owner's rainbow-pool clarification and consolidated Puff ending over exact V31 baseline `07734bb43018ffdefef3644f337db8fa46038d5b`.

Rainbow colors emerge through the remaining gunk on13, using the original rainbow artwork.14 shows the full rainbow waterfall and explicitly explains the swimming pool's magic.31 combines Roshan's reflection, Puff's thanks and the invitation to rest. The freed page4 gives complete dusty chest and cobweb cutouts a contextual low blue bank.22 now narrates sorting and table cleaning together;30 uses the existing clean room as a quiet closing result, with only the actor and brush footprint locally filled. Door23, kindness episode24–29, nap32 and both covers remain fixed.

Five built-in image-generation calls address named extraction/background gaps. Four components are delivered: a chest contour source, a shell-and-web alpha extraction, a small lower-bank edit and the bounded empty-room fill. Both chest candidates fail clean standalone alpha; the first is used only through an explicit PDF contour clip, preserving its original raster bytes. No full-scene regeneration or scene invention. Exact prompts, native hashes, source paths and delivered polygons are in [generation evidence](revisions/v32_rainbow_story/generation_evidence.json).

[Independent character, style and language review](revisions/v32_rainbow_story/visual_review.json) separates visual observations from [machine verification](revisions/v32_rainbow_story/complete/verification.json). All34 PDF renders equal their PNG proofs;28 mapped V31 pages are byte-identical.224 registered baseline source files and the font retain exact original bytes. Sniglet is embedded and captions have at least18pt type and24pt trim clearance. Lossless export contains no JPEG/JPX image streams. [Stress checks](revisions/v32_rainbow_story/complete/stress_results.json), [project gates](revisions/v32_rainbow_story/project_gates.json) and [completion audit](revisions/v32_rainbow_story/COMPLETION_AUDIT.json) record exact scope.

Internal near-final craft judgments do not establish professional SLP, owner/child or physical-print acceptance. Existing art retains its native density (many full frames approximately212ppi at trim); this is a review PDF, not a certified300ppi press master. Actual paper, color, binding, gutter and reading response remain to be reviewed. No game runtime, master finding, device, cinematic delivery or release acceptance is claimed.
''')
write(L/'STORY_COMPREHENSION_AUDIT.md','''# V32 story comprehension and shared-reading audit

Status: `SUPPORTING_CURRENT`. Internal editorial review for a shared-reading picture book, ages4–5. Professional SLP endorsement and child evidence remain open.

The opening now moves from arrival and invitation3 to concrete cobweb/chest observations4, dusty-floor problem5, shared goal and visible supplies6. This uses existing castle material and preserves the setting. The bath supplies simple repeated actions. The pool sequence12–16 connects gunk clearing, rainbow water, the magic swimming pool, the obstructing cup and Rumi's freedom;17 keeps the immediate hug. Daddy's named speech on14 explains why the waterfall is rainbow. No unsupported stream count or ordinary-water substitution remains.

Rumi has lived in the castle for hundreds of years; the text does not assign that duration to her trap.18–21 identify Baby Eagle's chirp, exactly two playful bunnies, an accidental trap, gentle brushing, apology and gentle play. The chirp and trapped-Eagle picture now share a spread, providing immediate identification rather than a concealed danger. The quiet bank bunnies remain secondary to the rescue.

22 combines sorting paints and cleaning the table before the last door.23→24 still uses a page turn to reveal dusty, uncomfortable Grand Puff.25–29 keep reassurance, cooperative washing, concealed colors, rainbow emergence and the exact landing. The quiet clean-room30 records the castle result;31 gives Roshan's rainbow reflection, Puff's thanks and a shared invitation.32 delivers the inclusive bubble nap. No renewed cleaning job, second transformation or unrelated Eagle subplot is introduced at the end.

All32 captions have been reread against current pictures. Named speakers, concrete nouns, short breath groups and familiar helping/scrubbing refrains support adult read-aloud and later participation. New 'cobwebs' and 'rainbow-colored' have direct pictorial support. Useful vocabulary remains natural; no measured decoding level or clinical developmental outcome is asserted. Two silent Lamma appearances remain optional discoveries and are not explained in child-facing text.

Exact text is in [page plan](PAGE_PLAN.md) and [language review packet](revisions/v32_rainbow_story/SLP_REVIEW_PACKET.html); [independent language audit](revisions/v32_rainbow_story/language_final.json) binds the current manuscript and proof hashes. [Spread dummy](revisions/v32_rainbow_story/PRINT_DUMMY.html) preserves right-side story1 and both23→24/27→28 reveals. A physical dummy and natural adult reading remain separate from digital checks.
''')
p=L.parent/'DESIGN_LANGUAGE.md';s=p.read_text('utf8')
s=s.replace('V31 below owns the current review proof.','V32 below owns the current review proof.')
s=s.replace('[V31](landscape/revisions/v31_story_clarity/README.md) owns current review facts; V30 is the unchanged-image baseline.','[V31](landscape/revisions/v31_story_clarity/README.md) preserves historical review facts; V30 was its unchanged-image baseline.')
marker='## V32 owner clarification: magical rainbow water and consolidated welcome (2026-10-01)'
if marker in s:s=s[:s.index(marker)].rstrip()
write(p,s+'\n\n'+marker+'''

Water from the magic swimming pool is rainbow-colored. Restore the original partial rainbow13; explicitly explain the pool's magic on14. Combine Puff's reflection, gratitude and invitation to rest into31, freeing a page for complete dusty-castle object cutouts early in the story. Use old22 as a quiet clean-room result30 after locally removing the actor/held brush;22 narrates both sorting and table cleaning. Preserve32 interiors plus covers and the23→24/27→28 reveal turns.

Continue full-art/true contour alternation, blue stationery, clear upper85%, empty central bottom gap, grounded low assets ≤12%, source character contours and subtle page-specific details. New local bank/extraction work grants no full-scene redraw authority. Both native chest candidates retain backing haze; use the first only as a document-clipped exact contour source, never declare it a clean-alpha master. Preserve all originals, prompt/source hashes and rejected attempts. [V32](landscape/revisions/v32_rainbow_story/README.md) owns current facts;28 mapped V31 proofs remain unchanged. Internal quality judgments never supply owner/child/SLP/print or game-wide approval.
''')
p=V.parent/'v31_story_clarity/README.md';s=p.read_text('utf8').replace('Status: `SUPPORTING_CURRENT`;','Status: `HISTORICAL_EVIDENCE`;')
s=s.replace('Status: `HISTORICAL_EVIDENCE`; complete review proof awaiting owner/child/qualified SLP/physical-print acceptance.','Status: `HISTORICAL_EVIDENCE`; original published V31 review proof. Current edition: [V32](../v32_rainbow_story/README.md). Its water treatment and separate ending have been superseded; original artwork and audits remain evidence.')
write(p,s)
write(V/'README.md','''# V32 — the magic rainbow pool and a shared welcome

Status: `SUPPORTING_CURRENT`; complete review proof, external owner/child/qualified SLP/physical-print acceptance pending.34 pages including both covers;32 interiors;7 ×5 inches landscape;Sniglet. Exact V31 baseline: `07734bb43018ffdefef3644f337db8fa46038d5b`.

[All-page before/after](AUDIT_REVIEW.html) · [Reader](complete/READ_BOOK.html) · [Full PDF](complete/Mermaid_Roshan_LANDSCAPE_ROUGH.pdf) · [Spread dummy](PRINT_DUMMY.html) · [Language packet](SLP_REVIEW_PACKET.html) · [Manifest](manifest.json)

The waterfall remains rainbow:13 restores the existing colors emerging through gunk, and14 adds Daddy's dialogue that the swimming pool's magic makes the water rainbow-colored.31 combines the former30 reflection and31 gratitude/rest invitation. This frees4 for dusty-castle inspection, using complete chest and shell/cobweb contours.22 narrates sorting and table cleaning; the existing clean room becomes quiet closing result30. Both reveal turns, helping plot, exact landing, inclusive nap and covers remain unchanged. [Pagination](pagination.json) records old-to-new mapping;28 page proofs retain exact mapped V31 bytes.

Five built-in image-generation calls address specific extraction and small local-background gaps. Four components are delivered. Both chest candidates retain diffuse backing and are rejected as standalone alpha assets; the first supplies only a precise document-level contour extraction. The second is not delivered. The shell/web silhouette is complete. Bank/empty-room pixels enter only the declared lower regions or actor/brush footprint over the intact scene base. No full-scene redraw, invented scene or protected-original edit. [Exact prompts, sources, native hashes, masks and selections](generation_evidence.json) preserve the distinction.

[Independent character/style/language review](visual_review.json), [source/PDF verification](complete/verification.json), [stress checks](complete/stress_results.json), [completion audit](COMPLETION_AUDIT.json) and [project gates](project_gates.json) cover the current proof. All34 lossless PDF renders equal native PNG proofs.224 registered V31 source files and the font remain exact. Embedded Sniglet captions are18pt or larger, with24pt trim clearance. Native art density is unchanged; many full frames are approximately212ppi at trim. Internal near-final craft ratings are editorial observations, not professional SLP, owner/child, physical-print or game-wide master-audit acceptance.

## Rebuild and delivery

```text
python -B books/chapter_one/landscape/render_book.py --output books/chapter_one/landscape/revisions/v32_rainbow_story/complete
python -B books/chapter_one/landscape/revisions/v32_rainbow_story/optimize_pdf_lossless.py books/chapter_one/landscape/revisions/v32_rainbow_story/complete/Mermaid_Roshan_LANDSCAPE_ROUGH.pdf
python -B books/chapter_one/landscape/revisions/v32_rainbow_story/verify_revision.py
python -B books/chapter_one/landscape/audit_book.py --proof books/chapter_one/landscape/revisions/v32_rainbow_story/complete --baseline books/chapter_one/landscape/revisions/v31_story_clarity/complete
```

Rebuilds require new exact audit bindings. Established publication destination: `Ebonyks/mermaid-roshan-reef`, branch `codex/mermaid-roshan-picture-book`; anonymous HTTPS recipient access. After push, `verify_remote.py <exact-commit> --receipt <outside-repo-output>` fetches the remote manifest and every required file without credentials. Remote byte identity does not grant creative acceptance. No dev/master integration or game release is commissioned.
''')
packet=(V.parent/'v31_story_clarity/SLP_REVIEW_PACKET.html').read_text('utf8')
packet=packet.replace('Current V31 book','Current V32 book').replace('../v30_identity/complete/READ_BOOK.html','../v31_story_clarity/complete/READ_BOOK.html').replace('V30 baseline reader','V31 baseline reader')
packet=re.sub(r'<p class="small">V31 binds.*?</p>','<p class="small">V32 binds six changed pages and28 mapped byte-identical V31 proofs. Daddy explains the magic rainbow pool on14;31 combines reflection, gratitude and a rest invitation. The freed opening page4 shows dusty castle belongings, and30 quietly records the clean result. No SLP endorsement or measured literacy outcome is claimed.</p>',packet,flags=re.S)
packet=packet.replace('clear-stream progression','rainbow-water progression').replace('18–20 pt','18–20 pt').replace('the concealed rainbow reveal','the concealed Puff rainbow reveal')
packet=re.sub(r'<p>All 34 pages are covered.*?</p>','<p>All34 proofs and32 current captions have hash-bound editorial review. Embedded Sniglet captions are18pt or larger; every story caption and speech glyph retains24pt trim clearance, with18pt minimum cover clearance. Quiet caption regions, named dialogue and clear speaker tails have been inspected.14 uses three20pt lines below the focal actors;31 separates three named dialogue turns from both faces. The original supply caption now appears on6, the cup on15, Rumi residence on12 and gentle-play/apology page on21. Physical print, natural adult read-aloud, actual SLP review and owner/child acceptance remain separate.</p>',packet,flags=re.S)
packet=re.sub(r'<h2>Revision evidence and remaining checks</h2>.*?<h2>Print pagination','''<h2>Revision evidence and remaining checks</h2>
<ul>
<li>6 names a brush and sponges, with the existing complete supplies visible.</li>
<li>12 distinguishes Rumi's long castle residence from her current trap.</li>
<li>13 shows rainbow colors through remaining gunk.14 explicitly explains the magic swimming pool; no stream count is imposed.</li>
<li>15 shows Roshan holding the freed cup beside the seahorse fountain.</li>
<li>21 preserves rounded apology bubbles, explicit gentle-play language and small speaker figures.</li>
<li>22 narrates sorting and table scrubbing before the final door. The quiet room30 records the completed castle, then31 combines reflection, gratitude and rest.</li>
<li>28 mapped V31 proofs remain byte-identical, including the accepted ceiling-join repair27 and both covers. Retained evidence does not grant fresh owner/print acceptance.</li>
</ul>
<h2>Print pagination''',packet,flags=re.S)
table='<h2>Exact V32 manuscript</h2>\n<table><thead><tr><th>Page</th><th>Exact text</th></tr></thead><tbody>\n'
table+='<tr><td>Front cover</td><td>'+html.escape(B['title'])+'</td></tr>\n'
for p in B['pages']:table+=f"<tr><td>{p['page']}</td><td>{html.escape(p['text']).replace(chr(10),'<br>')}</td></tr>\n"
table+='<tr><td>Rear cover</td><td>No text</td></tr>\n</tbody></table>'
packet=re.sub(r'<h2>Exact V31 manuscript</h2>.*?</tbody></table>',table,packet,flags=re.S)
assert 'V31 binds' not in packet and 'Exact V31 manuscript' not in packet
write(V/'SLP_REVIEW_PACKET.html',packet)
p=R/'design/05_DOC_LEDGER.md';lines=p.read_text('utf8').splitlines()
descriptions={
'books/chapter_one/README.md':('🔵','`SUPPORTING_CURRENT`; V32 current34-page review navigation, magic rainbow pool, consolidated Puff welcome and mapped source/proof evidence; external acceptance remains open.'),
'books/chapter_one/landscape/PAGE_PLAN.md':('🔵','`SUPPORTING_CURRENT`; V32 exact32-page map, dusty-castle insert4, rainbow pool dialogue13–14, combined cleanup22, quiet result30 and merged welcome31; both reveal turns preserved.'),
'books/chapter_one/landscape/REVIEW.md':('🔵','`SUPPORTING_CURRENT`; V32 six changed proofs and28 exact mapped V31 reuses; native extraction/local-mask limits, lossless PDF/source checks and external acceptance gaps.'),
'books/chapter_one/landscape/STORY_COMPREHENSION_AUDIT.md':('🔵','`SUPPORTING_CURRENT`; V32 magic pool dialogue, concrete early dust observations, completed cleanup before the final door and consolidated Puff gratitude/rest; all32 captions reread, not professional SLP or child-test evidence.'),
'books/chapter_one/landscape/revisions/v31_story_clarity/README.md':('⚪','`HISTORICAL_EVIDENCE`; published V31 mystery-door/rear-cameo and ending evidence. V32 restores rainbow water and consolidates the ending; original art/proofs/audits preserved.'),
}
for i,line in enumerate(lines):
 for key,(icon,desc) in descriptions.items():
  if line.startswith('| `'+key+'` |'):lines[i]=f'| `{key}` | {icon} | {desc} |'
new=f'| `{V.relative_to(R).as_posix()}/README.md` | 🔵 | `SUPPORTING_CURRENT`; V32 magical rainbow pool, consolidated Puff page, freed early dusty-castle inspection and quiet clean-room closing; exact34-page proof, five bounded candidates, four delivered components, independent audits and anonymous remote manifest; owner/child/SLP/print acceptance remain open. |'
if new not in lines:lines.append(new)
write(p,'\n'.join(lines))
print('Current V32 docs, exact manuscript packet and ledger updated.')
