"""Record native art provenance, current page map and review navigation."""
from pathlib import Path
import json,hashlib,html
from PIL import Image
V=Path(__file__).resolve().parent;L=V.parents[1];R=L.parents[2]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
def rel(p):return p.resolve().relative_to(R.resolve()).as_posix()
B=json.loads((L/'book.json').read_text(encoding='utf8'))
jobs=json.loads((V/'generation_jobs.json').read_text(encoding='utf8'))
records=[]
for j in jobs:
 refs=[]
 for f in j['refs']:
  p=Path(f) if Path(f).is_absolute() else R/f
  refs.append(dict(path=rel(p),sha256=sha(p),dimensions=list(Image.open(p).size)))
 p=V/'art'/f"{j['id']}.png"
 records.append(dict(id=j['id'],method='built-in image_gen; bounded source-conditioned edit',prompt=j['prompt'],prompt_sha256=hashlib.sha256(j['prompt'].encode()).hexdigest(),references=refs,output=dict(path=rel(p),sha256=sha(p),dimensions=list(Image.open(p).size)),use=('REJECTED_UNUSED: upper-wall join remained discontinuous; native trial retained as evidence only.' if j['id'] in ['castle_entry_ceiling','castle_entry_join'] else 'Selected: bounded page-layout patches for background edits; full RGBA derivative for reassurance. No full-scene replacement.')))
video=R/'assets_src/cinematics/day_one_davinci_draft_2026-09-04/sources/C02_S01_v1_door_open.mp4'
save(V/'generation_evidence.json',dict(baseline='4eb7c58bd81ac820949d122e97052e3b76213997',owner_direction='Approve preview changes except oversized19; replace unrelated23 with early dirty-castle exploration;26 offers cleaning supply and reassurance. Book-only cooperative cleaning.',generated=records,extraction=dict(source=rel(video),source_sha256=sha(video),fps='24/1',timestamp_seconds=4,frame_index_zero_based=96,command='ffmpeg -ss4 -i C02_S01_v1_door_open.mp4 -frames:v1 castle_entry_source.png',output=rel(V/'art/castle_entry_source.png'),output_sha256=sha(V/'art/castle_entry_source.png'),dimensions=[1264,720]),reuse=dict(preview_manifest='books/chapter_one/previews/2026-09-30/manifest.json',selected=['sink_action','lamba_bath','fountain_clear_v2','hug_cutout_v2','hug_stationery_v2','rescue_release','scrub_ceiling','rainbow_puff_cutout'],excluded={'apology_canvas':'owner rejected oversized speaking bunnies','art_caption_space':'craft-making beat removed','old26_copy':'superseded by new cleaning plot'}),inventory_rejections=[dict(path='assets_src/cinematics/d1_c02_first_dirty_castle_discovery_visual_v1/first_frames/S02_FIRST_FRAME.png',reason='Upper duplicated architecture; pending first-frame review is not acceptance.'),dict(path='assets_src/cinematics/day_one_davinci_draft_2026-09-04/sources/C02_S02_v1_dirty_hall.mp4',reason='Reviewed1s/4s; duplicated upper strip and character drift.'),dict(path='assets_src/cinematics/day_one_davinci_draft_2026-09-04/sources/C02_S03_v1_dirty_hall_evidence_REGEN.mp4',reason='Literal rabbits and EVIDENCE signs; unsuitable narrative art.')],hidden_appearances=dict(adult_only=True,story_pages=[9,31],unprompted=True,note='Bath-towel peek and tiny toy peek. No child-facing clue, label, arrow or instruction.'),scope='Static picture book. No game-canon, gameplay, cinematic-delivery or protected-original change.'))
# Store portable paths in the executable prompt archive.
for j in jobs:j['refs']=[rel(Path(f) if Path(f).is_absolute() else R/f) for f in j['refs']]
save(V/'generation_jobs.json',jobs)
table=['| New story page | V27 page | Treatment | Caption |','|---|---|---|---|']
for p in B['pages']:table.append('| '+str(p['page'])+' | '+str(p['original_page'] or 'new')+' | '+p['mode']+' | '+p['text'].replace('\n',' / ')+' |')
intro='''# V28 — helping Grand Puff

Status: `SUPPORTING_CURRENT`; full 34-page review proof, not final owner, child or print acceptance. 32 story pages plus both covers; 7 × 5 inches, Sniglet. Page numbers below are story numbers; PDF page numbers are one higher because of the front cover.

The new early castle-entry beat uses an existing Grok door-opening frame. The separate craft-making page is removed. Sorting and scrubbing the craft room remain part of the castle cleanup. The former play invitation now bridges the rainbow reflection into the final bubble nap.

Grand Puff is an uncomfortable friend. Roshan offers a soapy star sponge and says, “Hold on, we’ll make you feel clean and better!” Daddy, Rumi and Baby Eagle help wash him. The same Puff emerges rainbow bright and feels like himself again. The shell attack, dizziness and combat reading are removed. This owner decision governs the book only.

The prior preview approvals are applied, except oversized apology bunnies and the removed craft page. The apology now has two small bank bunnies and editable rounded capsules. Two unprompted Lamb-a appearances are integrated locally; their locations remain in adult production evidence only.

The door is on23 and Puff on24; bubbles are on27 and the rainbow reveal on28. These page-turn placements assume story1 begins on a right-hand page. A physical print dummy must confirm cover/endpaper and binding choices.

## Current page assignments

'''
(L/'PAGE_PLAN.md').write_text(intro+'\n'.join(table)+'\n\nFull-art pages have no stationery frame. Reduced pages retain contour cutouts and event-specific low blue banks; exact sources, layouts and bounded patches are in book.json and revisions/v28_kindness/complete/page_provenance.json. Prior page plans remain available in Git history.\n',encoding='utf8',newline='\n')
review='''# V28 revision review

Status: `SUPPORTING_CURRENT`. Implemented owner corrections are reviewable in the [full book](revisions/v28_kindness/complete/READ_BOOK.html), [revision comparison](revisions/v28_kindness/REVISION_REVIEW.html) and [current page plan](PAGE_PLAN.md).

## What changed

- Former19 →20: reject enlarged preview bunnies; use locally reduced, grounded versions, about9.8% of page height. Eagle remains the foreground focus. Rounded speech capsules keep both exact apologies.
- Former23: remove disconnected craft-making. New3 opens the actual castle doors to reveal the dirty interior. A left-anchored full-art trim preserves both source characters and the threshold. The unsuccessful wall-extension studies are excluded.
- Former26 →25: soapy star sponge in Roshan’s hand, caring expression from Puff, exact owner reassurance. No projectile trail or dizzy eyes.
- Former27 →26: four friends wash Puff together; approved upper-wall extension replaces the compressed strip above the unchanged source scene.
- Approved sink action, bath wording/hidden visitor, fountain action, isolated hug, Eagle release and rainbow-Puff reflection are applied.
- Former20 →31: gentle play before everyone sleeps. Two page turns protect the final reveals.34total pages retained.

## Review and limits

Rendered page review checks seams, visible character features, caption placement and the complete story. Mechanical verification checks34pages,7×5trim,18pt minimum story type, safe placement, source hashes, transparent reduced art, selected-source exclusions, owner wording, page-turn order and two hidden appearances. Neither check establishes child comprehension or print acceptance.

Native sources remain mixed density. The new entrance frame is1264×720, 144ppi at full-page trim; existing restored scene art is often about212ppi. Lossless PDF stream optimization changes storage only, never decoded pixels. The last three finale ceiling strips remain a known lower-density exception. No300ppi print-master claim.

The accepted hug preview’s tiny fountain crest begins above the strict lower15% target. The small apology ears also reach above that line, within the earlier speaking-character margin; their heights now meet12%. The play-border ear has its existing two-pixel exception. These are explicit review limits, not hidden automatic passes.

The comprehensive V27 review’s waterfall-clearing action and rescue-room continuity questions remain open. Original cover, rear H, exact rainbow landing and protected project art remain unchanged. Resolve/handoff searching stays stopped. No runtime or game-canon changes, finding closure, device test or child acceptance is claimed.

See [native generation provenance](revisions/v28_kindness/generation_evidence.json), [visual review](revisions/v28_kindness/visual_review.json), [machine results](revisions/v28_kindness/complete/stress_results.json), and [delivery manifest](revisions/v28_kindness/manifest.json). Earlier detailed review history is preserved in Git and the dated V27 review.
'''
(L/'REVIEW.md').write_text(review,encoding='utf8',newline='\n')
story='''# V28 whole-story comprehension audit

Status: `SUPPORTING_CURRENT`; editorial review, not an observed child reading test. The owner’s latest book-only kindness plot supersedes prior fight/dodge/shell directions.

| Pages | Narrative job | Evidence and review |
|---|---|---|
|1–4|Destination, arrival, entry, reason to clean|Added open-door source frame makes crossing into a dirty castle explicit before the shared plan.|
|5–9|Tools, playful dust bunny, bath cleanup and payoff|Connected sponge contact replaces a tool inventory; concrete verbs and repeated scrub/splash invite participation.|
|10–16|Rumi needs help; remove gunk, clear water, free and hug her|Rumi’s hundreds of years describe residence, never entrapment. Waterfall clearing remains partially carried by narration; distinct rainbow payoff and pulled cup are visible.|
|17–20|Hear a chirp; two bunnies trap Eagle; brush them away; apologize|Exactly two cloud bunnies, no blanket. Their intent is playful but the trap is real. Small speaking bunnies remain secondary to freed Eagle. Rescue-room architectural continuity is still imperfect.|
|21–22|Finish another castle room|Sorting and table scrubbing advance cleanup. The unrelated making-art pause is removed.|
|23–25|Last door, unwell friend, reassurance|Door23 precedes the page-turn reveal. Sponge and exact owner reassurance show care rather than attack.|
|26–29|Friends wash Puff; bubbles; rainbow reveal; landing|Four helpers make the cause clear. Grand Puff remains one individual. Exact original jump/landing retained. Reveal28 follows page turn from27.|
|30–32|Name the change, play gently, rest together|Roshan addresses rainbow Puff; play resolves the earlier apology and softens the transition to sleep.|

Language uses short clauses, concrete actions, named referents and useful repetition. Rumi, reassurance and transformation retain a few richer words supported by pictures. This is a shared-reading picture book, not a controlled phonics program or certified reading level. Nothing prompts Roshan to look for Lamb-a.

Read-aloud and print-dummy checks remain: pacing of the extra entry beat, whether the final play invitation interrupts the settling rhythm, understanding that dust obscured Puff’s own colors, and spontaneous recognition of the small apology speakers. Do not call these accepted without observing the child/owner.

Current manuscript/page mapping: [PAGE_PLAN.md](PAGE_PLAN.md). Art, geometry and source limits: [REVIEW.md](REVIEW.md). Previous comprehension cycles remain in Git history.
'''
(L/'STORY_COMPREHENSION_AUDIT.md').write_text(story,encoding='utf8',newline='\n')
cards=[]
for old,new,title in [(19,20,'Smaller apology bunnies'),(23,3,'Craft-making replaced by castle entry'),(26,25,'A sponge and reassurance'),(6,7,'The sponge touches the sink'),(8,9,'Clearer bath payoff'),(13,14,'The fountain action'),(15,16,'A quieter hug'),(18,19,'Freeing Baby Eagle'),(27,26,'Friends clean Grand Puff'),(31,30,'Roshan speaks to Puff')]:
 before=f'../../../previews/2026-09-30/{"after" if old in [19,23,26] else "before"}/story_{old:02}.png'
 cards.append(f'<section><h2>{html.escape(title)}</h2><div class="pair"><figure><figcaption>Previous {"proposal" if old in [19,23,26] else "book"} · story {old}</figcaption><img loading="lazy" src="{before}"></figure><figure><figcaption>V28 · story {new}</figcaption><img loading="lazy" src="complete/page_{new:02}.png"></figure></div></section>')
doc='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Mermaid Roshan · V28 revision review</title><style>body{margin:0;background:#17344a;color:#ecf7ff;font:17px/1.55 system-ui}header,main{max-width:1500px;margin:auto;padding:24px}section{background:#e8f3f9;color:#18344a;padding:20px;border-radius:14px;margin-bottom:28px}.pair{display:grid;grid-template-columns:1fr 1fr;gap:20px}figure{margin:0}img{display:block;width:100%}a{color:#a9e4ff}figcaption{padding:8px}h1{line-height:1.2}@media(max-width:800px){.pair{grid-template-columns:1fr}}</style><header><h1>V28 · Helping Grand Puff</h1><p>Full34-page revision with a source-based castle entrance, smaller speaking bunnies and collaborative cleaning. Story numbering has changed; the map below each comparison identifies both versions.</p><p><a href="complete/READ_BOOK.html">Read the complete book</a> · <a href="complete/Mermaid_Roshan_LANDSCAPE_ROUGH.pdf">Full review PDF</a> · <a href="../../PAGE_PLAN.md">Every page and its words</a> · <a href="../../REVIEW.md">Checks and remaining limits</a></p><p>Review proof. Native art density and three older finale ceiling strips remain print limitations. The new book is ready for owner review, not declared finished.</p></header><main>'''+''.join(cards)+'</main></html>'
(V/'REVISION_REVIEW.html').write_text(doc,encoding='utf8',newline='\n')
print('Provenance, page plan, comprehension review and comparisons recorded.')
