"""Build an honest all-page review and current book navigation from final audits."""
from pathlib import Path
import hashlib, html, json

V=Path(__file__).resolve().parent; L=V.parents[1]; R=L.parents[2]
def read(p):return json.loads(p.read_text(encoding='utf8'))
def save(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
def write(p,s):p.write_text(s,encoding='utf8',newline='\n')
def rel(p):return p.resolve().relative_to(R.resolve()).as_posix()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def esc(s):return html.escape(str(s))
def index(report):return {p.get('page_index',p.get('page')):p for p in report['pages']}
def score(row):
 if 'object_min_score' in row:return row['object_min_score']
 if row.get('objects') and all('internal_craft_score' in q for q in row['objects']):return min(q['internal_craft_score'] for q in row['objects'])
 for key in ['final_internal_visual_craft_score','internal_visual_craft_score','baseline_internal_visual_craft_score','internal_craft_score']:
  if row.get(key) is not None:return row[key]
 raise ValueError('No real reviewed score in '+str(row.keys()))

B=read(L/'book.json'); configs={p['page']:p for p in B['pages']}
S=read(V/'style_final.json'); C=read(V/'character_final.json'); language=read(V/'language_final.json')
assert C['book_json_sha256']==S['frozen_evidence']['book']['sha256']==language['evidence']['book_json_sha256']==sha(L/'book.json')
assert C['page_provenance_sha256']==S['frozen_evidence']['page_provenance']['sha256']==language['evidence']['page_provenance_sha256']==sha(V/'complete/page_provenance.json')
assert S['frozen_evidence']['pdf_snapshot']['sha256']==sha(V/'complete/Mermaid_Roshan_LANDSCAPE_ROUGH.pdf')
si=index(S);ci=index(C);sb=index(read(V/'style_baseline.json'));cb=index(read(V/'character_baseline.json'))
assert set(si)==set(ci)==set(sb)==set(cb)==set(range(34))
rows=[];open_findings=[]
for n in range(34):
 current=min(score(si[n]),score(ci[n]));base=min(score(sb[n]),score(cb[n]))
 cp=configs.get(n,{})
 character_notes=[dict(object=q['object'],score=q['internal_craft_score'],observation=q['observed']) for q in ci[n].get('objects',[])]
 row=dict(page=n,label='Front cover' if n==0 else 'Rear cover' if n==33 else f'Story page {n}',baseline_internal_craft_min=base,final_internal_craft_min=current,all_reviewed_objects_at_target=current>=4.9,character_objects=character_notes,style_review=si[n],before=dict(path=f'../v28_kindness/complete/page_{n:02}.png',sha256=sha(V.parent/'v28_kindness/complete'/f'page_{n:02}.png')),after=dict(path=f'complete/page_{n:02}.png',sha256=sha(V/'complete'/f'page_{n:02}.png')),image_treatment=cp.get('mode','F'),caption=cp.get('text',''),background=cp.get('background_theme','Complete rendered composition'),motifs=cp.get('integrated_motifs',[]))
 rows.append(row)
 if current<4.9:
  remaining=ci[n].get('observed_remaining_failures',[])
  detail=' '.join(remaining) if isinstance(remaining,list) else str(remaining)
  open_findings.append(dict(id=f'BOOK-CRAFT-{n:02}',pages=[n],issue='Sub-target internal judgment. '+str(si[n].get('findings',''))+(' '+detail if detail else ''),objects=[q for q in character_notes if q['score']<4.9],status='OWNER_SOURCE_VARIANT_OR_EDITORIAL_LIMIT; see independent final reviews, not a fabricated master finding'))
summary=dict(pages=34,minimum=min(q['final_internal_craft_min'] for q in rows),mean_page_minimum=sum(q['final_internal_craft_min'] for q in rows)/34,pages_at_internal_target=sum(q['all_reviewed_objects_at_target'] for q in rows),all_objects_target_met=all(q['all_reviewed_objects_at_target'] for q in rows))
review=dict(revision='V29',revision_verdict='COMPLETE_ITERATED_REVIEW_PROOF; EXTERNAL_ACCEPTANCE_PENDING',method='Independent native all34-page character/style/language passes, original-book comparison, all-object notes, final selective reinspection after composition repairs, plus all34 PDF pixel and font checks.',book_json_sha256=sha(L/'book.json'),page_provenance_sha256=sha(V/'complete/page_provenance.json'),internal_scale='Subjective editorial craft1–5;4.9 near-final screen craft. Not the master-audit release-proven scale or SLP approval.',summary=summary,pages=rows,open_findings=open_findings,external_gates=['Owner art and wording approval','Roshan read-aloud/comprehension observation','Professional SLP review before SLP-approved claim','Physical7×5 print dummy, paper/color/gutter and native-density acceptance'],generation_evidence='generation_evidence.json',bubble_review='bubble_baseline_review.json')
save(V/'visual_review.json',review)

cards=[]
for q in rows:
 n=q['page'];style=q['style_review']
 notes=''.join('<li><b>'+esc(o['object'])+'</b> · '+esc(o['score'])+'/5: '+esc(o['observation'])+'</li>' for o in q['character_objects'])
 cards.append(f'''<article id="page-{n}"><h2>{esc(q['label'])} <small>{q['image_treatment']} · internal minimum {q['baseline_internal_craft_min']:.1f} → {q['final_internal_craft_min']:.1f}/5</small></h2><div class="pair"><figure><figcaption>Before · frozen V28</figcaption><a href="{q['before']['path']}" target="_blank"><img loading="lazy" src="{q['before']['path']}" alt="Before {esc(q['label'])}"></a></figure><figure><figcaption>After · current V29</figcaption><a href="{q['after']['path']}" target="_blank"><img loading="lazy" src="{q['after']['path']}" alt="After {esc(q['label'])}"></a></figure></div><p><b>Style:</b> {esc(style.get('findings','See full independent audit.'))}</p><p><b>Words:</b> {esc(q['caption'])}</p><p><b>Background:</b> {esc(q['background'])}</p><details><summary>Object-by-object review and source evidence</summary><ul>{notes}</ul><p>Before SHA256: <code>{q['before']['sha256']}</code><br>After SHA256: <code>{q['after']['sha256']}</code></p></details></article>''')
 studies=read(V/'generation_evidence.json')
 rejects=''.join('<figure><img loading="lazy" src="art/'+esc(j['id'])+'.png" alt="Rejected '+esc(j['id'])+'"><figcaption><b>'+esc(j['id'])+'</b> · '+esc(j['selection_reason'])+'</figcaption></figure>' for j in studies['generated'] if j['selection']=='REJECTED_UNUSED')
 doc='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Mermaid Roshan V29 · complete audit and before/after</title><style>body{margin:0;background:#173449;color:#eff8ff;font:17px/1.55 system-ui}header,main,footer{max-width:1500px;margin:auto;padding:24px}article{padding:22px;margin:0 0 28px;background:#e9f3f8;color:#183346;border-radius:14px}.pair{display:grid;grid-template-columns:1fr 1fr;gap:22px}figure{margin:0}img{width:100%;display:block}figcaption{padding:8px 0}a{color:#aae8ff}article a{color:#126999}h1{line-height:1.15}small{font-size:15px;font-weight:normal}details{background:#d9eaf4;padding:14px;border-radius:8px}code{overflow-wrap:anywhere;font-size:12px}.studies{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}.notice{background:#254c65;padding:18px;border-radius:12px}.nav{position:sticky;top:0;background:#173449;padding:12px;z-index:10}@media(max-width:850px){.pair,.studies{grid-template-columns:1fr}}</style><header><h1>V29 · Complete book audit</h1><p>34 pages including covers · 7 × 5 inches · Sniglet · finished kindness plot</p><p>''' +str(studies['generated_count'])+' native generation candidates; '+str(studies['selected_candidate_count'])+' selected derivatives; '+str(studies['rejected_candidate_count'])+''' rejected studies retained. Every page is compared below, including unchanged accepted art.</p><p class="notice">Internal near-final craft target is4.9/5. '''+str(summary['pages_at_internal_target'])+' of34 pages meet it across both independent visual reviews; minimum '+str(summary['minimum'])+'''. This report does not inflate accepted source differences into a perfect score. Owner, child, print and actual SLP approval remain open.</p><p><a href="complete/READ_BOOK.html">Read the book</a> · <a href="complete/Mermaid_Roshan_LANDSCAPE_ROUGH.pdf">Full PDF</a> · <a href="SLP_REVIEW_PACKET.html">Language review packet</a> · <a href="visual_review.json">Combined object audit</a> · <a href="generation_evidence.json">Prompts and provenance</a> · <a href="complete/verification.json">PDF verification</a> · <a href="manifest.json">Delivery manifest</a></p><p>Bubble audit: closed perimeter rings, clean highlights and dense lather are inspected at native scale. Painted grain is distinguished from corruption; unknown upstream compression is not diagnosed from a PNG container. Export is lossless and checked pixel-for-pixel on all34 pages.</p><p>Click either page image to inspect it at full rendered size. Story numbering begins after the front cover.</p></header><div class="nav"><label>Jump to page <select onchange="location.hash='page-'+this.value">'''+''.join('<option value="'+str(n)+'">'+esc(rows[n]['label'])+'</option>' for n in range(34))+'''</select></label></div><main>'''+''.join(cards)+'''<h2>Rejected studies · production evidence</h2><p>These images are excluded from delivered page artwork. Their failures shaped the smaller grounded banks, the coherent ceiling reuse and natural local repairs.</p><div class="studies">'''+rejects+'''</div></main><footer>Static-book scope only. No game runtime, cinematic acceptance, protected original or master finding changed.</footer></html>'''
write(V/'AUDIT_REVIEW.html',doc)

table=['| Story page | Treatment | Caption |','|---|---|---|']
for p in B['pages']:table.append('| '+str(p['page'])+' | '+p['mode']+' | '+p['text'].replace('\n',' / ')+' |')
write(L/'PAGE_PLAN.md','# V29 current page plan\n\nStatus: `SUPPORTING_CURRENT`.34 total pages, including both covers;32 story pages;7 × 5 in landscape; Sniglet. F means full art; C means authored-contour cutout on low blue event stationery. No reduced scenic rectangles. The story and page order are finished.\n\nDoor23 precedes Puff24; bubble27 precedes rainbow28. These intended reveals assume story1 begins on a right-hand page; a physical print dummy must confirm binding/endpapers.\n\n'+'\n'.join(table)+'\n\nExact sources, masks, placements, typography and measured marginal bounds are in [book.json](book.json) and [page provenance](revisions/v29_polish/complete/page_provenance.json). The [all-page before/after review](revisions/v29_polish/AUDIT_REVIEW.html) records the final independent object judgments.\n')
write(L/'REVIEW.md','''# V29 comprehensive polish review

Status: `SUPPORTING_CURRENT`; complete iterated proof for owner review, not final acceptance.

The [all-page before/after package](revisions/v29_polish/AUDIT_REVIEW.html) compares every V28 page with V29. Three independent reviewers examine character identity, composition/backgrounds and age4–5 wording. Native source studies, rejected candidates and exact masks remain inspectable.

The selected repairs restore castle-entry clarity, plain Roshan costume details, the listening gesture, canonical two-bunny Eagle rescue, naturally rounded speech capsules and the sleeping bunnies. Event banks now vary supply gathering, cleaning, towel drying, apology, frightened hiding, cheering/popcorn, friendship and gentle toy play. Two tiny unprompted visitors have canonical identities. The strong page21 foreground, accepted covers and exact landing remain unchanged.

The bubble lane checks broken contours, mottling/block patterns, halos and export degradation. Entire coherent11/21 stationery derivatives replace the old broken perimeter rings; rectangular patch seams are rejected. Existing approved26 ceiling is reused27–29 after generated extensions failed their composed joins. Dirty-bath and rainbow-waterfall caption surfaces receive bounded material-preserving calm edits. All white story type uses a fine editable navy contour, no opaque caption bars.

All34 PDF pages are rendered and compared to proof PNGs after lossless image-stream optimization. Mechanical checks cover native source hashes, full-art/cutout treatment, minimum18pt story type, margins, actual bound annotations, foreground/text separation, exact commissioned wording, cooperative cleaning and reveal order. Generated occlusion/shadow opacity and exact source prop pixels are not claimed measurable.

The internal4.9 craft target and actual remaining sub-target observations are in the [combined audit](revisions/v29_polish/visual_review.json). Accepted source variations are recorded rather than arbitrarily redesigned. Native artwork is generally1484×1060, about212ppi at7×5; it is not a300ppi press master. Owner/child/physical-print review and professional SLP review remain outstanding. No game/master finding, runtime, cinematic delivery or protected original is changed.
''')
write(L/'STORY_COMPREHENSION_AUDIT.md','''# V29 story and language review

Status: `SUPPORTING_CURRENT`; developmental editorial review, not an observed child test or professional SLP approval.

| Pages | Narrative purpose | Current evidence |
|---|---|---|
|1–4|Arrive, enter, see dirt, agree to help|Actual source doorway and dirty hall establish entry before cleaning. Roshan's quotation has an explicit speaker.|
|5–9|Tools, playful bunny, bath cleaning and payoff|Brush/sponge, contact scrubbing, drain and clean water support concrete verbs and playful repetition.|
|10–16|Meet and help Rumi|Rumi's residence lasted hundreds of years, not her entrapment. Strainer removes rubbish; one stream then the other two clear; rainbow payoff, freed cup, released friend and hug complete the cause chain.|
|17–20|Hear, find, help Eagle; bunnies apologize|The playroom cue bridges the approach and toy hall. Exactly two playful cloud bunnies trap Eagle. Brushing is gentle, each speaker apologizes and Roshan models gentle play.|
|21–22|Finish craft-room cleanup|Sorting and scrubbing advance restoration; no disconnected craft-making pause.|
|23–25|Last door, uncomfortable Puff, reassurance|Glow/rumble create curiosity; Roshan holds cleaning supply and offers the owner's exact caring words.|
|26–30|Friends wash Puff; rainbow reveal|Helpers wash together. Dirt hid the same friend's own colors. Bubble/reveal page turn, exact landing and reflection preserve continuity.|
|31–32|Gentle play and shared rest|Play answers the apology; inclusive bubble nap settles the rhythm.|

Short concrete clauses, named referents, supported richer words and recurrent sounds invite participation as reading develops. This remains a shared-reading picture book, not a controlled phonics course or certified reading level. No hidden-character search instruction appears in the manuscript.

The [language packet](revisions/v29_polish/SLP_REVIEW_PACKET.html) gives the exact manuscript, language-development rationale and review questions. Relevant ASHA and IES guidance is cited there. Actual SLP sign-off requires a qualified professional. Observe Roshan's understanding of the rescue, apology and same-Puff transformation; allow enjoyable reading without turning each page into a test. A print dummy must confirm all caption placements and reveal turns.
''')
write(L.parent/'README.md','''# Mermaid Roshan - Chapter One picture book

Current edition: **V29 - comprehensive polish**.34 pages including covers;7 × 5 in landscape; Sniglet. The finished story follows friends cleaning Pearl Castle and helping the dusty Grand Puff feel better.

[Review every before/after page](landscape/revisions/v29_polish/AUDIT_REVIEW.html) · [Read the book](landscape/revisions/v29_polish/complete/READ_BOOK.html) · [Full PDF](landscape/revisions/v29_polish/complete/Mermaid_Roshan_LANDSCAPE_ROUGH.pdf) · [Versioned package](landscape/revisions/v29_polish/README.md)

Current authority and evidence: [design language](DESIGN_LANGUAGE.md), [page plan](landscape/PAGE_PLAN.md), [checks and limitations](landscape/REVIEW.md), [story review](landscape/STORY_COMPREHENSION_AUDIT.md), [object audit](landscape/revisions/v29_polish/visual_review.json), [native prompts/provenance](landscape/revisions/v29_polish/generation_evidence.json) and [manifest](landscape/revisions/v29_polish/manifest.json).

V28 and earlier dated reviews remain historical evidence. V29 adds independent whole-book audits, selective source-preserving repairs, varied grounded bank performances, subtler hidden visitors, bubble-quality checks and clearer editable typography/language. The4.9 internal target is reported honestly. Owner, child, print and qualified SLP acceptance remain open. No game/runtime, cinematic or protected-original change. Resolve/handoff searching remains stopped.
''')
write(V/'README.md',f'''# V29 - comprehensive book polish

Status: `SUPPORTING_CURRENT`; complete iterated review proof.34 pages including covers;32 story pages;7 × 5 in landscape; Sniglet. Baseline `{read(V/'generation_evidence.json')['baseline']}`.

[Before/after of all34 pages](AUDIT_REVIEW.html) · [Reader](complete/READ_BOOK.html) · [Full PDF](complete/Mermaid_Roshan_LANDSCAPE_ROUGH.pdf) · [Current page plan](../../PAGE_PLAN.md) · [Language review packet](SLP_REVIEW_PACKET.html)

{studies['generated_count']} built-in image-generation candidates were made for recorded gaps;{studies['selected_candidate_count']} selected derivatives and{studies['rejected_candidate_count']} rejected studies are preserved. The [full prompt/reference/native-hash evidence](generation_evidence.json) records actual delivery layers and masks. Source originals are unchanged. Rejected ceiling/scale/floor studies are excluded; the approved coherent ceiling is reused.

Independent final [character](character_final.json), [style](style_final.json) and [language](language_final.json) audits bind to the current proof. [Combined audit](visual_review.json):{summary['pages_at_internal_target']}/34 page minima meet internal4.9; overall minimum{summary['minimum']:.1f}, mean{summary['mean_page_minimum']:.3f}. These are subjective editorial judgments, not master-audit or SLP acceptance. Sub-target details are retained openly.

Bubble quality is audited at native size and in final PDF renders. [Verification](complete/verification.json) checks all34 page pixels, manuscript, embedded font, source preservation and trim; [encoding evidence](complete/lossless_pdf_encoding.json) proves unchanged decoded image data. Native images are generally~212ppi at this trim, not300ppi.

Owner art/wording, Roshan's read-aloud/comprehension, physical print dummy and professional SLP review remain outstanding. The SLP packet applies developmental guidance without claiming sign-off.

## Build and delivery

From repository root, use the bundled Python runtime with Pillow, ReportLab, pypdf and pypdfium2:

```text
python -B books/chapter_one/landscape/render_book.py --output books/chapter_one/landscape/revisions/v29_polish/complete
python -B books/chapter_one/landscape/revisions/v29_polish/optimize_pdf_lossless.py books/chapter_one/landscape/revisions/v29_polish/complete/Mermaid_Roshan_LANDSCAPE_ROUGH.pdf
python -B books/chapter_one/landscape/revisions/v29_polish/verify_revision.py
python -B books/chapter_one/landscape/audit_book.py --proof books/chapter_one/landscape/revisions/v29_polish/complete --baseline books/chapter_one/landscape/revisions/v28_kindness/complete
```

Rebuilding changes proof metadata/hash and requires final audit reconciliation. Optional native-copy scripts are staging helpers; the committed native PNGs are the durable project assets.

Established repository: `Ebonyks/mermaid-roshan-reef`; branch: `codex/mermaid-roshan-picture-book`; recipient access: anonymous HTTPS. [Manifest](manifest.json) lists exact source/build/review files and hashes. After push, `verify_remote.py <exact-commit> --receipt <output-path>` anonymously verifies the remote manifest and every required file. Remote byte verification proves delivery only. No dev/master integration or release is commissioned.
''')
print(json.dumps(summary))
