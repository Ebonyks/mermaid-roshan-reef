"""Build the two-treatment editorial plan; source frames remain reference-only."""
from pathlib import Path
import csv,html,json
P=Path(__file__).resolve().parent/'plan';E=html.escape
with (P/'page_plan.psv').open(encoding='utf-8-sig') as f:rows=list(csv.DictReader(f,delimiter='|'))
for r in rows:r['page']=int(r['page']);r['sources']=[s for s in r['sources'].split(',') if s]
assert [r['page'] for r in rows]==list(range(1,41))
assert rows[11]['sources']==['waterfall'] and not rows[12]['sources']
assert all(r['mode'] in ['C','F','S'] for r in rows)
assert all(r['background']=='NONE' for r in rows if r['mode']!='C')
assert all(all(r[k] for k in ['foreground_cutouts','background_left','background_right','remove_from_source','placement','extraction_status']) for r in rows)
C=json.loads((P/'source_catalog.json').read_text(encoding='utf-8'))
for r in rows:
 for k in r['sources']:assert (P/C[k]['file']).is_file(),k
cut=[r['page'] for r in rows if r['mode']=='C'];full=[r['page'] for r in rows if r['mode']!='C']
intro='''# Chapter One: cutout or full-art layout plan

This replaces the previous vignette/cropped-panel layout. It is a production plan, not a rebuilt book. Exactly two image treatments are allowed: **CUTOUT** (complete figures, objects or connected action groups with transparent contours on the blue stationery background) and **FULL ART** (existing scene fills the page or facing spread, without stationery). Spread halves are full art, not a third treatment.

No scene rectangles, rounded screenshot boxes, circular scene windows, torn-edge room patches or softly masked scenery on reduced pages. A real paper sheet or window frame may retain its physical shape; the room around it may not. Sticker means a true silhouette, not an added white stroke. Preserve natural holes between limbs and through net mesh, source identity and contact. Never crop a person into isolated hands or heads to avoid extraction work.

Every cutout page below assigns: foreground silhouettes, left-mound decoration, right-mound decoration, context to remove, scale/text placement and extraction status. Border integrations preserve exact supplied pixels and obey the original Gemini contract: top 85% clear of integrated assets, <=12% width AND height, slopes only, central gap clear, bottom 10% hidden by mound texture and low-opacity grounding shadow. These small-decoration rules do not shrink the separate foreground story illustrations. All stationery panels stay blue; no foreground/border prop duplication.

Full-art pages use NONE for both background mounds and for decorative overlays. Crop to the outer page/spread edges only while retaining essential action; use authorized peripheral outpainting where needed, never a full-scene redraw. Story page 1 is recto. Facing spreads are 2-3, 14-15 and 34-35. Sniglet text occupies natural quiet space without solid caption bars.

Page 12 depicts the blockage. Page 13 still requires a distinct existing clearing-action source; it cannot reuse page 12 or invent action. Existing backgrounds remain studies until the exact-asset, geometry and publication checks pass. Missing extractions remain explicit jobs; no screenshot may fill their place. No handoff polling resumes.
'''
intro+='\n**CUTOUT pages:** '+', '.join(map(str,cut))+'.\n\n**FULL-ART pages:** '+', '.join(map(str,full))+'.\n\n'
md=[intro];cards=[]
for r in rows:
 treatment='CUTOUT' if r['mode']=='C' else ('FULL ART — spread half' if r['mode']=='S' else 'FULL ART')
 md.append(f"## {r['page']:02}. {r['beat']} — {treatment}\n\n")
 fields=[('foreground_cutouts','Foreground artwork'),('background_left','Left mound'),('background_right','Right mound'),('remove_from_source','Remove / retain'),('placement','Placement and text'),('extraction_status','Production status'),('work','Source constraints')]
 cards.append(f'<article id="p{r["page"]}" class="card"><header><span class="tag {"cut" if r["mode"]=="C" else "full"}">{r["page"]:02} · {treatment}</span><h2>{E(r["beat"])}</h2></header><dl>')
 for k,label in fields:
  md.append(f"**{label}:** {r[k]}\n\n");cards.append(f'<dt>{label}</dt><dd>{E(r[k])}</dd>')
 md.append('**Source keys:** '+(', '.join(r['sources']) or 'MISSING — distinct clearing-action source required')+'\n\n')
 cards.append('</dl>')
 if r['sources']:
  cards.append('<details class="source"><summary>Source material only — not the proposed layout</summary><p>These unprocessed source frames are extraction/composition inputs. Rectangular source previews never count as delivered cutout artwork.</p><div class="sources">')
  for k in r['sources']:cards.append(f'<figure><img loading="lazy" src="{C[k]["file"]}" alt="Reference only: {E(k)}"><figcaption>{E(k)}</figcaption></figure>')
  cards.append('</div></details>')
 else:cards.append('<p class="gap">Source gap: clearing-action artwork required. No repeated obstruction image.</p>')
 cards.append('</article>')
ref=json.loads((P/'reference_audit.json').read_text(encoding='utf-8'))
md.append('## Reference audit\n\nOriginal PDF page numbers; layouts examined previously, not new approved book art.\n\n')
for r in ref:md.append(f"- **{r['pdf_page']:02}:** {r['observation']}\n")
md.append('''\n## Production order and acceptance

1. Extract representative foregrounds for pages 4, 7, 11, 24, 32, 33 and 38; inspect transparent edges, complete silhouettes and natural holes. Existing cutouts on 8/20/22/28/29/37/40 still need final edge review.
2. Compose cutout-page proofs with named mound assets. If an extra decorative asset is not cleanly extractable, leave that slope with its base-native shell/coral rather than draw a new object or duplicate a foreground prop.
3. Compose full-art proofs with no stationery. Resolve peripheral aspect-ratio needs without moving characters or inventing scenes; verify whole-spread continuity before splitting.
4. Inspect all 40 page treatments together. Reject any reduced scenic patch, clipped body part, duplicate prop, invented action or opaque caption strip. Validate the 85%/12%/10% background constraints separately from foreground scale.
5. Only then rebuild the book PDF. This plan does not assert finished cutout production, print suitability, final Resolve delivery or owner visual acceptance.
''')
(P/'PAGE_BY_PAGE_PLAN.md').write_text(''.join(md),encoding='utf-8')
style='''body{margin:0;background:#eef5fa;color:#19364a;font:16px/1.55 system-ui,sans-serif}main{max-width:1100px;margin:auto;padding:32px}h1{font-size:38px;line-height:1.12}h2{font-size:23px;margin:12px 0}a{color:#16668b}.intro,.card{background:white;border:1px solid #bbd4e4;border-radius:12px;padding:26px;margin:22px 0}.intro{background:#dfedf7}.rhythm{display:flex;flex-wrap:wrap;gap:5px;margin:25px 0}.rhythm a{padding:7px;text-decoration:none;min-width:32px;text-align:center}.cut{background:#cee7f5;color:#16445e}.full{background:#235977;color:white}.tag{display:inline-block;padding:6px 12px;border-radius:5px;font-weight:700}dl{display:grid;grid-template-columns:180px 1fr;gap:12px 20px}dt{font-weight:700}dd{margin:0}summary{cursor:pointer;font-weight:600;padding:12px;background:#edf3f7}.source{margin-top:20px;border-top:1px solid #cadde9}.sources{display:flex;flex-wrap:wrap;gap:18px}.sources figure{margin:10px 0;max-width:310px}.sources img{max-width:100%;max-height:260px;object-fit:contain}.gap{border-left:4px solid #ad8037;padding:12px;background:#fff3db}.refgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}.refgrid img{width:100%}@media(max-width:700px){main{padding:14px}.card,.intro{padding:18px}dl{grid-template-columns:1fr;gap:3px}dd{margin-bottom:14px}.refgrid{grid-template-columns:1fr 1fr}}'''
h=[f'<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Chapter One — cutout or full-art plan</title><style>{style}</style><main><h1>Cutout or full art.<br>One clear choice for every page.</h1><p>40-page layout revision · 23 cutout pages · 17 full-art pages · production plan, not a rebuilt book</p><p><a href="../DESIGN_LANGUAGE.md">Binding book rules</a> · <a href="PAGE_BY_PAGE_PLAN.md">Written plan</a> · <a href="page_plan.csv">Editable table</a></p><section class="intro"><h2>Two treatments only</h2><p><b>Cutout:</b> whole figures, objects or connected action groups, isolated along their actual silhouettes and placed on blue stationery. No rectangular screenshots, rounded scene boxes, torn-edge room fragments or scenic blobs.</p><p><b>Full art:</b> the existing scene fills the page or facing spread. No blue stationery, decorative mounds, floating inset or extra sticker.</p><p>Each cutout-page card specifies foreground art, left and right mound decoration, removal instructions and placement. Small background assets obey the Gemini limits; large foreground story illustrations do not inherit the 12% cap. Source frames are collapsed below each card and are not proposed layouts.</p><p><b>Key changes:</b> page 10 is full art; page 29 is a large boss silhouette; page 32 uses whole tools; page 38 uses whole objects, not room thumbnails. Page 13 remains a distinct clearing-action source gap.</p></section><nav class="rhythm">']
for r in rows:h.append(f'<a class="{"cut" if r["mode"]=="C" else "full"}" href="#p{r["page"]}">{r["page"]}<br>{"C" if r["mode"]=="C" else "F"}</a>')
h+=['</nav><p>Full-art facing spreads: <b>2–3 · 14–15 · 34–35</b>. All other full-art choices occupy one page. Covers remain separate.</p>',*cards,'<details><summary>Original book — page-by-page reference analysis</summary><p>Layout evidence only; held-IP imagery is not new-book source art.</p><div class="refgrid">']
for r in ref:h.append(f'<div><img loading="lazy" src="reference/page_{r["pdf_page"]:02}.jpg" alt="Original reference page {r["pdf_page"]}"><p><b>{r["pdf_page"]:02}.</b> {E(r["observation"])}</p></div>')
h.append('</div></details><p>Production remains pending: exact alpha extractions, compliant mound integrations, full-art fitting and final book export. No new scene redraws or handoff polling.</p></main></html>')
(P/'DESIGN_PLAN.html').write_text(''.join(h),encoding='utf-8')
(P/'page_plan.json').write_text(json.dumps({'status':'CUTOUT_OR_FULL_ART_PLAN; NOT_REBUILT_BOOK','story_pages':40,'cutout_pages':cut,'full_art_pages':full,'spreads':[[2,3],[14,15],[34,35]],'pages':rows},indent=2),encoding='utf-8')
with (P/'page_plan.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows([{**r,'sources':', '.join(r['sources'])} for r in rows])
print(f'PASS: 40 assigned pages; {len(cut)} cutout, {len(full)} full art; explicit layer/removal/placement fields; full-art backgrounds NONE; page 13 gap retained.')
