"""Rebuild the review plan using only files in this book checkout."""
from pathlib import Path
import csv,html,json
P=Path(__file__).resolve().parent/'plan'
with (P/'page_plan.psv').open(encoding='utf-8-sig') as f:rows=list(csv.DictReader(f,delimiter='|'))
for r in rows:r['page']=int(r['page']);r['sources']=[s for s in r['sources'].split(',') if s]
assert [r['page'] for r in rows]==list(range(1,41))
assert rows[11]['sources']==['waterfall'] and not rows[12]['sources']
assert 'ART GAP' in rows[12]['work']
assert all(r['background']=='NONE' for r in rows if r['mode'] in ['F','S'])
C=json.loads((P/'source_catalog.json').read_text(encoding='utf-8'));E=html.escape;cards=[];text=[]
for r in rows:
 cards.append(f'<article class="card" id="p{r["page"]}"><div class="preview">')
 for k in r['sources'][:2]:
  assert (P/C[k]['file']).is_file(),k
  cards.append(f'<div><img loading="lazy" src="{C[k]["file"]}" alt="Existing {E(k)} source"><small>{E(k)}</small></div>')
 if not r['sources']:cards.append('<p class="note"><b>Distinct clearing-action art required</b><br>No repeated obstruction thumbnail. No invented scene.</p>')
 cards.append(f'</div><div><span class="tag">PAGE {r["page"]:02} / {r["mode"]} / {E(r["background"])}</span><h3>{E(r["beat"])}</h3>')
 for k,label in [('composition','Cut and pacing'),('ownership','Background / object ownership'),('work','Production work')]:cards.append(f'<p><b>{label}.</b> {E(r[k])}</p>')
 cards.append('</div></article>')
 text.append(f"### {r['page']:02}. {r['beat']} — {r['mode']} / {r['background']}\n\n**Sources:** {', '.join(r['sources']) or 'ART GAP — distinct clearing-action frame required'}\n\n**Composition:** {r['composition']}\n\n**Border / no duplication:** {r['ownership']}\n\n**Required work:** {r['work']}\n")
(P/'DESIGN_PLAN.html').write_text((P/'design_plan.template.html').read_text(encoding='utf-8').replace('{{PAGE_CARDS}}',''.join(cards)),encoding='utf-8')
(P/'PAGE_BY_PAGE_PLAN.md').write_text((P/'page_plan.template.txt').read_text(encoding='utf-8').replace('{{PAGE_TEXT}}','\n'.join(text)),encoding='utf-8')
(P/'page_plan.json').write_text(json.dumps({'status':'DESIGN_PLAN_NOT_REBUILT_BOOK','story_pages':40,'recto_first':True,'spreads':[[2,3],[14,15],[34,35]],'pages':rows},indent=2),encoding='utf-8')
with (P/'page_plan.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows([{**r,'sources':', '.join(r['sources'])} for r in rows])
print('PASS: 40 page records, existing local sources, no backgrounds on full art, distinct page 12/13 source requirements.')
