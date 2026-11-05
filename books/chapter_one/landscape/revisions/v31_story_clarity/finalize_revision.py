"""Build the V31 review and synchronize only changed current book facts."""
from pathlib import Path
import hashlib,html,json,re
V=Path(__file__).resolve().parent;L=V.parents[1];R=L.parents[2]
def read(p):return json.loads(p.read_text(encoding='utf8'))
def save(p,q):p.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
def write(p,s):p.write_text(s,encoding='utf8',newline='\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
B=read(L/'book.json');old=read(V/'BOOK_BASELINE.json');E=read(V/'generation_evidence.json')
changes={
 12:('The caption claimed completed/countable streams; only partial progress was visible, and the warm lane resembled a premature reward.','Ordinary clear aqua replaces the colored lane/reflection. The caption explicitly describes ongoing clearing, little by little; the remaining green gunk is intentionally present.'),
 13:('The follow-up still relied on an unsupported three-stream count.','Clean water flow and the existing full rainbow picture supply the finished payoff, without requiring the child to identify invisible divisions.'),
 23:('Rainbow arch and candy-pink door looked inviting before the uncomfortable dusty Puff.','The same shell door is closed and shadowed violet, with a faint seam glow; Roshan looks cautiously curious. All completed room doors, floor route lights and original stairs remain.'),
 31:('A second Baby Eagle play invitation reopened an already resolved subplot near the ending.','Grand Puff says thank you, and Roshan invites him to rest. A local grateful facial expression differentiates the Puff cutout. Tiny bunnies yawn/rest beside settled toys; the old toy-chest Lamma peek is removed.'),
 33:('No Lamma cameo appeared on the accepted rear cover.','A tiny partially concealed canonical Lamma face peeks among background books. All cast, cover composition and V30 identity corrections remain intact.')}
cards=[]
for n in list(changes)+[q for q in range(34) if q not in changes]:
 label='Front cover' if n==0 else 'Rear cover' if n==33 else f'Story page {n} (PDF position {n+1})'
 prior,after=changes.get(n,('No new owner finding on this page.','Byte-identical V30 proof image retained; previous evidence stays at its exact recorded baseline.'))
 cards.append(f'<article id="page-{n}"><h2>{label}</h2><p><b>Before:</b> {html.escape(prior)}</p><div class="pair"><figure><figcaption>V30</figcaption><img loading="lazy" src="../v30_identity/complete/page_{n:02}.png"></figure><figure><figcaption>V31</figcaption><img loading="lazy" src="complete/page_{n:02}.png"></figure></div><p><b>After:</b> {html.escape(after)}</p></article>')
doc='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Mermaid Roshan - V31 story clarity</title><style>body{margin:0;background:#e5f2f8;color:#153047;font:17px/1.5 system-ui}header,article{max-width:1360px;margin:25px auto;padding:24px;background:white;border-radius:12px}.pair{display:grid;grid-template-columns:1fr 1fr;gap:20px}figure{margin:0}img{width:100%;display:block}figcaption{font-weight:bold;margin-bottom:8px}a{color:#175bb0}.note{background:#eef7fc;padding:16px}@media(max-width:850px){.pair{grid-template-columns:1fr}header,article{margin:14px;padding:16px}}</style><header><h1>V31 - clearer progress, mystery and belonging</h1><p>34 authored pages including covers;32 interiors;7 x5 inches landscape;Sniglet. Story numbering is unchanged. The five changed pages appear first below, followed by29 retained pages.</p><p><a href="complete/READ_BOOK.html">Read the complete book</a> · <a href="complete/Mermaid_Roshan_LANDSCAPE_ROUGH.pdf">Full PDF</a> · <a href="PRINT_DUMMY.html">Bound spreads</a> · <a href="SLP_REVIEW_PACKET.html">Language packet</a> · <a href="visual_review.json">Independent audit</a> · <a href="generation_evidence.json">Prompts and native provenance</a></p><p class="note">Page31 now closes Grand Puff's story: thanks, welcome, shared rest. An extra early dirty-castle page was considered, using existing source material. Simply moving31 to the front would put door/Puff and bubble/rainbow reveals on shared spreads; combining two bath-action pages to compensate would crowd those actions. This narrower revision preserves both reveal turns and uses31 to resolve the main encounter.</p><p>Five native local candidates supply bounded regions only. First composed mask trials showed waterfall-color remnants and a stair join; revised contour scope removes the remnants and retains the original complete stairs. Original full scene bases, accepted covers and exact landing are preserved. Two unprompted Lamma appearances remain: bath9 and rear cover. Professional SLP, owner/child reading and physical print acceptance remain open.</p></header>'''+''.join(cards)+'</html>'
write(V/'AUDIT_REVIEW.html',doc)
readme='''# V31 - story clarity and belonging

Status: `SUPPORTING_CURRENT`; complete review proof awaiting owner/child/qualified SLP/physical-print acceptance.34 pages including both covers;32 interiors;7 x5 inches landscape;Sniglet. Exact V30 baseline: `19ee6ce8ec4c20c05714f101d0d222a33477e400`.

[All-page before/after](AUDIT_REVIEW.html) · [Reader](complete/READ_BOOK.html) · [Full PDF](complete/Mermaid_Roshan_LANDSCAPE_ROUGH.pdf) · [Bound spread dummy](PRINT_DUMMY.html) · [Language review packet](SLP_REVIEW_PACKET.html) · [Manifest](manifest.json)

Page12 now describes partial progress with clear aqua water, reserving the rainbow for13. Both captions avoid the unsupported stream count. Page23 retains the correct castle hall, completed doors, route lights and source stairs, but replaces the welcoming rainbow door with closed shadowed violet and a narrow mysterious glow. Roshan's cautious expression matches the rumble. Page31 gives Grand Puff thanks and an invitation to rest; it resolves the main encounter before32's inclusive nap instead of reopening the Eagle subplot. Tiny sleepy bunnies support that settling rhythm. A discreet canonical Lamma peek joins the rear cover, while the old31 cameo is removed; two sightings remain.

An additional early exploration page was analyzed but not selected: a simple insert/delete spoils both reveal turns, and compensating by merging bath actions would reduce their visual clarity. The existing castle-entry/dirty-hall setup remains. This is an editorial choice available for owner review, not a new scene invention.

Five built-in image-generation calls produce local candidate pixels only. Exact [prompts, references, native hashes and delivered masks](generation_evidence.json) are durable project assets. The initial composed mask errors were caught and revised: waterfall lane/reflection scope follows material boundaries, and the original stair artwork remains unchanged. Complete full-scene bases, V30 character repairs, strong21 and exact landing29 are retained.

[Independent audit](visual_review.json), [PDF/pixel/source verification](complete/verification.json) and [stress checks](complete/stress_results.json) separate observations from machine evidence.29 page PNGs remain byte-identical to V30. The lossless PDF uses embedded editable Sniglet; native artwork remains approximately212ppi at trim, not a certified300ppi press master. No professional SLP approval, child test, print approval or game-wide master-audit satisfaction is claimed.

## Rebuild and delivery

```text
python -B books/chapter_one/landscape/render_book.py --output books/chapter_one/landscape/revisions/v31_story_clarity/complete
python -B books/chapter_one/landscape/revisions/v31_story_clarity/optimize_pdf_lossless.py books/chapter_one/landscape/revisions/v31_story_clarity/complete/Mermaid_Roshan_LANDSCAPE_ROUGH.pdf
python -B books/chapter_one/landscape/revisions/v31_story_clarity/verify_revision.py
python -B books/chapter_one/landscape/audit_book.py --proof books/chapter_one/landscape/revisions/v31_story_clarity/complete --baseline books/chapter_one/landscape/revisions/v30_identity/complete
```

Rebuilds require reconciliation of actual proof/audit hashes. Established destination: `Ebonyks/mermaid-roshan-reef`, branch `codex/mermaid-roshan-picture-book`; anonymous HTTPS recipient access. After push, `verify_remote.py <exact-commit> --receipt <outside-repo-output>` fetches the exact remote manifest and every required file without credentials. Publication and byte identity do not grant creative acceptance. No dev/master integration or game release is commissioned.
'''
write(V/'README.md',readme)
plan=['# V31 current page plan','','Status: `SUPPORTING_CURRENT`.34 total pages, including covers;32 interiors;7 x5 inches landscape;Sniglet. F = full art; C = true contour cutout on contextual low blue stationery. No reduced scenic rectangles.','','Door23 precedes Puff24 across a page turn; bubbles27 precede rainbow28 across a page turn. Story1 starts on a right-hand page. The physical print dummy still requires printer review.','','| Story page | Treatment | Caption |','|---|---|---|']
plan += [f"| {p['page']} | {p['mode']} | "+p['text'].replace('\n',' / ')+' |' for p in B['pages']]
plan+=['','The waterfall progress12 and complete rainbow13 now form an explicit before/completion pair without a stream count. The closed violet door23 is uncertain rather than celebratory. Grand Puff replies with thanks and is invited to rest31, leading directly into32. Two subtle Lamma sightings are unprompted.','','Exact source/placement/mask/type data: [book.json](book.json) and [provenance](revisions/v31_story_clarity/complete/page_provenance.json). [Before/after](revisions/v31_story_clarity/AUDIT_REVIEW.html) and [independent audit](revisions/v31_story_clarity/visual_review.json) retain the observations and alternatives.']
write(L/'PAGE_PLAN.md','\n'.join(plan)+'\n')
main=R/'books/chapter_one/README.md';s=main.read_text('utf8').replace('V30 - comprehensive polish','V31 - story clarity and belonging').replace('v30_identity','v31_story_clarity')
s=s[:s.index('V29 and earlier')]+'V30 and earlier dated proofs remain historical evidence. V31 corrects ambiguous waterfall progress and the inviting final door, connects Grand Puff’s gratitude and welcome to the group nap, and adds a tiny rear-cover Lamma.29 unchanged page PNGs retain their exact V30 bytes. Internal craft judgments remain separate from owner, child, print and qualified SLP acceptance. No game/runtime or protected-original change. Resolve/handoff searching remains stopped.\n'
write(main,s)
p=L/'STORY_COMPREHENSION_AUDIT.md';s=p.read_text('utf8').replace('V30','V31').replace('v30_identity','v31_story_clarity').replace('one stream then the other two clear; rainbow payoff','partial gunk removal is explicitly ongoing, followed by clear water and the rainbow payoff').replace('Glow/rumble create curiosity','A closed shadowed-violet door and low rumble create cautious curiosity').replace('|31–32|Gentle play and shared rest|Play answers the apology; inclusive bubble nap settles the rhythm.|','|31–32|Gratitude, welcome and shared rest|Puff thanks Roshan; she invites him to rest with the friends. The inclusive bubble nap completes his belonging arc.|')
write(p,s)
review='''# V31 story-clarity review

Status: `SUPPORTING_CURRENT`; complete owner-review proof, external acceptance pending.

The [all-page comparison](revisions/v31_story_clarity/AUDIT_REVIEW.html) records the owner's new comprehension/mood findings, even though the previous internal V30 craft scores had met the target. Those scores did not establish owner acceptance or guarantee that every plot ambiguity had been found.

The four changed story pages12/13/23/31 now show ongoing clearing, a completed rainbow payoff without unsupported counting, a mysterious closed castle door, and Grand Puff's thanks/welcome before the shared nap. The rear cover adds a tiny unprompted Lamma; old31's cameo is removed. Two small tired-bunny performances support31.29 other page PNGs are exactly unchanged. The early-castle alternative and its reveal-pacing cost are documented rather than silently shifting page numbers.

Five built-in local candidates, exact masks, source references/hashes and inspected revisions are in [generation evidence](revisions/v31_story_clarity/generation_evidence.json). Only bounded regions are delivered over the existing source bases. First composed mask trials exposed color remnants and a staircase join; both were corrected before final verification. The original stairs and route cues remain, alongside the shadowed door.

Native bubble contours and final export quality remain explicit review lanes. [Verification](revisions/v31_story_clarity/complete/verification.json) compares all34 final PDF renders with the proof PNGs, protects unchanged source/art/font bytes and tests exact outside-scope preservation. [Stress checks](revisions/v31_story_clarity/complete/stress_results.json) cover trim/type, source hashes, full-art/cutout treatment, contextual low-bank bounds and canon/reveal order. These checks do not infer identity, clinical or physical-print acceptance.

[Independent character/style/language judgments](revisions/v31_story_clarity/visual_review.json) are internal editorial evidence. Owner/child reading, a qualified SLP and the physical printer proof remain open. Native images are approximately212ppi at7x5 trim; no300ppi press-master claim. No game/runtime/master-finding closure, cinematic delivery change or protected-original modification.
'''
write(L/'REVIEW.md',review)
design=R/'books/chapter_one/DESIGN_LANGUAGE.md';s=design.read_text('utf8')
heading='## V31 owner corrections: comprehension, mystery and belonging (2026-09-30)'
if heading in s:s=s[:s.index(heading)].rstrip()+'\n'
s+='\n'+heading+'\n\nThe owner rejects the unclear waterfall count/completion claim, the inviting rainbow doorway and the weak former31 play beat, and requests a tiny rear-cover Lamma. Use ongoing partial clearing12, full rainbow completion13, the same castle door shadowed violet23, and Puff’s thanks/rest invitation31. Keep the correct completed doors and route lights; uncertainty belongs to the dusty friend behind the door, not a new villain or combat plot. Preserve source scene bases, existing bodies/staging, exact landing and both reveal turns. The extra early exploration alternative remains documented; no numbering shift is required for this narrower correction.\n\nOnly five local candidates supply bounded water/reflection, door/face, low-bank acting, Puff face and shelf-cameo pixels. No full-scene replacement or protected-original edit. Remove old31’s cameo when adding the rear cameo, preserving two subtle unprompted sightings. [V31](landscape/revisions/v31_story_clarity/README.md) owns current review facts; V30 is the unchanged-image baseline. Source/pixel checks and internal editorial judgments do not grant owner, child, professional SLP or print acceptance.\n'
write(design,s)
# Preserve existing professional-review guidance while updating exact manuscript and scope.
packet=(V.parent/'v30_identity/SLP_REVIEW_PACKET.html').read_text('utf8')
packet=packet.replace('Final V30 book','Current V31 book').replace('V29 baseline reader','V30 baseline reader').replace('../v29_polish/complete/READ_BOOK.html','../v30_identity/complete/READ_BOOK.html').replace('Exact V30 manuscript','Exact V31 manuscript')
start=packet.index('<p class="small">The final frozen V30 proof');end=packet.index('</p>',start)+4
packet=packet[:start]+'<p class="small">V31 binds the five changed page proofs and29 retained V30 screenshots to exact hashes. Waterfall progress12/13, mysterious door23 and Grand Puff’s gratitude/rest31 have been reread against their visible pictures. The rear gains a tiny silent cameo. These corrections do not claim professional SLP sign-off or a measured literacy outcome.</p>'+packet[end:]
packet=packet.replace('The frozen V30 digital proof passes this editorial shared-reading review.','The V31 digital proof is under exact editorial review.').replace('new identity derivatives retain the same story, staging and caption regions.','local V31 derivatives retain the existing scene bases and caption regions; page31 closes the Puff encounter with gratitude and a rest invitation.')
for p in B['pages']:
 pattern=r'<tr><td>'+str(p['page'])+r'</td><td>.*?</td></tr>'
 line='<tr><td>'+str(p['page'])+'</td><td>'+html.escape(p['text']).replace('\n','<br>')+'</td></tr>'
 packet,count=re.subn(pattern,lambda _:line,packet,flags=re.S);assert count==1,p['page']
write(V/'SLP_REVIEW_PACKET.html',packet)
scope=read(V/'REVISION_SCOPE.json');scope['source_inventory']['lamma']='Canonical assets/sprites/stuffie_studio/lamma.png (949x1024 RGBA); tiny head behind existing shelf books. Only local pixels; no foreground cast changes.'
scope['source_inventory']['waterfall']='The original partial-progress frame remains base. Aqua lane plus contiguous lower-pool reflection is a bounded material repair, avoiding colored remnants and a cut reflection seam. All gunk and architecture outside remain unchanged.'
scope['chosen_ending']='31 Puff thanks Roshan and is invited to rest. Early exploration considered but rejected here because simple insertion spoils reveal parity and compensated bath compression weakens action clarity.'
save(V/'REVISION_SCOPE.json',scope)
print('Wrote current review, exact manuscript, authority-facing navigation and scope facts.')
