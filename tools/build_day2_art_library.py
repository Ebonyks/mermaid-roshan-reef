"""Source-bound Day Two review library. Scores are authored, never inferred by this tool."""
from __future__ import annotations
import argparse, base64, csv, hashlib, html, io, json, re, subprocess
from collections import Counter
from functools import lru_cache
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'audit/day2_art_library_2026-09-30'
WORK = ROOT / 'tmp/day2_art_contact_sheets'
CAREERS = ['chef','detective','ballerina','candymaker','doctor','farmer','boxer','magician','painter','astronaut','racer','nursery','popstar','geologist','teacher','arborist']
EXTS = {'.png','.webp','.jpg','.jpeg','.svg'}
def sha(data): return hashlib.sha256(data).hexdigest()
def git(*args): return subprocess.check_output(['git',*args],cwd=ROOT)
@lru_cache(maxsize=8)
def source_bytes(path):
    file = ROOT / path
    data = file.read_bytes() if file.exists() else git('show',f'HEAD:{path}')
    return data.replace(b"\r\n", b"\n") if path.endswith(".svg") else data
def image_of(path):
    data = source_bytes(path)
    if path.endswith('.svg'):
        try:
            import cairosvg
            data = cairosvg.svg2png(bytestring=data)
        except (ImportError,OSError):
            # Optional contact-sheet aid only. The HTML uses the original SVG.
            inv = OUT / 'inventory.json'
            if inv.exists():
                matches = [r for r in json.loads(inv.read_text(encoding='utf-8'))['items'] if r['sha256'] == sha(data)]
                for row in matches:
                    png = ROOT / 'tmp/day2_svg_review' / (row['id'] + '.png')
                    if png.exists():
                        candidate = Image.open(png).convert('RGBA')
                        if candidate.getbbox(): return candidate
            return None
    return Image.open(io.BytesIO(data)).convert('RGBA')
def inventory():
    tracked = git('ls-files').decode().splitlines()
    paths = {p for p in tracked if p.startswith('assets/opera/') and Path(p).suffix.lower() in EXTS}
    paths.update(p for p in tracked if p.startswith('assets/chapter2/birthday/') and Path(p).suffix.lower() in EXTS)
    extra = [
        'assets/characters/roshan_25d/roshan_base.png',
        'assets/castle/training/ghost_hand.png',
        'assets/castle/day_one_art_studio/magic_cleaning_brush.png',
        'assets/minigames/seek/lamma_animation.png', 'assets/kart/boost_ribbon.png',
        'assets/mg/seed.png','assets/flats/castle/logo_studio_v2/castle_banner_rainbow.png',
        'assets/flats/castle/rooms/room_playroom_item_stuffie_nook.png',
    ]
    paths.update(p for p in extra if p in tracked)
    # Close over literal image references in every related production controller.
    related = [p for p in tracked if p.startswith('scripts/') and p.endswith('.gd') and (Path(p).name.startswith('opera_') or 'chapter_two' in p or 'day_two' in p)]
    for script in related:
        text = source_bytes(script).decode('utf-8-sig')
        paths.update(p for p in re.findall(r'res://([^"\s]+\.(?:png|webp|jpg|svg))',text) if p in tracked)
    # Direct dynamic backdrop families consumed by the story adapters and venue.
    for p in tracked:
        if Path(p).suffix.lower() not in EXTS: continue
        if (p.startswith('assets/flats/castle/opera_house_venue_2d/background_tiles/')
            or p.startswith('assets/flats/castle/interactions_v4/background_tiles/room_library_')
            or p.startswith('assets/flats/castle/rooms/background_tiles/room_playroom_')
            or (p.startswith('assets/flats/sky_lagoon/main/') and re.search(r'_tile_r[01]_c[23]\.png$',p))): paths.add(p)
    scripts = {p:source_bytes(p).decode('utf-8-sig').replace('\r\n','\n') for p in tracked if p.startswith('scripts/') and p.endswith('.gd') and not Path(p).name.startswith('probe')}
    previous = json.loads((OUT/'inventory.json').read_text(encoding='utf-8'))['items'] if (OUT/'inventory.json').exists() else []
    old = {r['path']:r for r in previous}
    next_id = max([int(r['id'].split('-')[1]) for r in previous] or [0]) + 1
    rows = []
    for p in sorted(paths,key=lambda p:(p not in old,old[p]['id'] if p in old else p)):
        # Inventory needs headers, not a second full raster decode.
        im=Image.open(io.BytesIO(source_bytes(p))) if not p.endswith('.svg') else None
        consumer=[{'path':s,'line':text[:text.find('res://'+p)].count('\n')+1} for s,text in scripts.items() if 'res://'+p in text]
        career=next((c for c in CAREERS if re.search(r'(^|[_/])'+c+r'([_/.]|$)',p)), 'shared')
        if career=='shared':
            for alias,owner in {'candy':'candymaker','engineer':'astronaut','singer':'popstar'}.items():
                if re.search(r'(^|[_/])'+alias+r'([_/.]|$)',p):career=owner;break
        if 'tree_book_test' in p: career='arborist'
        role=Path(p).parent.name
        if 'backdrops' in p or 'background_tiles' in p or 'flat_sky_lagoon' in p or '/stage/' in p: role='background'
        if '/actors/animation/' in p: role='actor atlas'
        if 'retired' in p or re.search(r'(dragon|phantom|maestro)',p): state='retired content'
        elif '/widgets/' in p and re.fullmatch(r'widget_(gauge|track|pour|basin|charge|crank|trace|push|target|lanes)_[a-z]+',Path(p).stem) and 'pour_candymaker' not in p: state='retired widget base'
        elif '/actors/' in p and not '/animation/' in p and Path(p).name.startswith('roshan_'): state='fallback / reference'
        else: state='current family / verify phase binding'
        item_id=old[p]['id'] if p in old else f'D2A-{next_id:04}'
        if p not in old: next_id+=1
        if p.endswith('.svg'):
            svg=source_bytes(p).decode();w=re.search(r'width="(\d+)"',svg);h=re.search(r'height="(\d+)"',svg)
            dimensions=(int(w[1]),int(h[1])) if w and h else (None,None)
        else: dimensions=(im.width,im.height) if im else (None,None)
        rows.append({'id':item_id,'path':p,'sha256':sha(source_bytes(p)),'width':dimensions[0],'height':dimensions[1],'career':career,'role':role,'usage':state,'literal_consumers':consumer,'dynamic_binding_note':'Literal-reference census is supporting evidence only; filename templates and per-phase alternatives require controller review.','draft_source_score':None,'review':None,'rule_ids':[],'acceptance':'NOT_ACCEPTED: source-only drafting score; current runtime/device/child/owner review separate','priority':False})
    return rows
def contacts(rows):
    WORK.mkdir(parents=True,exist_ok=True)
    f=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',15)
    grouped={}
    for r in rows: grouped.setdefault(r['role'],[]).append(r)
    manifest=[]
    for role,items in grouped.items():
        for start in range(0,len(items),20):
            chunk=items[start:start+20]
            canvas=Image.new('RGB',(1440,1100),'#e5e2ec'); d=ImageDraw.Draw(canvas)
            for k,r in enumerate(chunk):
                x=(k%5)*288; y=(k//5)*275
                d.rectangle((x+4,y+4,x+283,y+231),fill='#c8c2cf')
                im=image_of(r['path'])
                if im:
                    im.thumbnail((272,217)); canvas.paste(im,(x+8+(272-im.width)//2,y+8+(217-im.height)//2),im)
                d.text((x+8,y+234),r['id']+' '+Path(r['path']).stem[:29],font=f,fill='#19203d')
                d.text((x+8,y+254),Path(r['path']).stem[29:60],font=f,fill='#19203d')
            filename=f'{role.replace(" ","-")}-{start//20+1:02}.jpg'
            canvas.save(WORK/filename,quality=92)
            manifest.append({'file':filename,'items':[r['id'] for r in chunk]})
    (WORK/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    print(json.dumps({'items':len(rows),'roles':Counter(r['role'] for r in rows),'sheets':manifest},indent=2))

def watched_sources():
    paths=git('ls-files').decode().splitlines()
    chosen=[p for p in paths if p.startswith('scripts/') and p.endswith('.gd') and (Path(p).name.startswith('opera_') or 'chapter_two' in p or 'day_two' in p)]
    chosen += [p for p in paths if p.startswith('scripts/') and p.endswith('.gd') and (Path(p).name.startswith('castle_') or Path(p).name in ['main.gd','save_state.gd','audio_director.gd','storybook_ui.gd','player.gd','flat_sky_lagoon_2d.gd'])]
    chosen += ['design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md','design/ARBORIST_TREE_BOOK_HANDOFF_2026-09-29.md','design/CHAPTER2_EIGHT_CAREER_PRODUCTION_SPINE_2026-08-30.md','design/OPERA_TWO_ACT_PERFORMANCES_2026-09-05.md','design/OPERA_TREE_BOOK_TEST_2026-09-30.md']
    chosen += [p for p in paths if p.startswith('docs/handoffs/codex_opera_imp_contest_2026-09-30/') and Path(p).name in ['CONTEST_DESIGN.md','CURRENT_STATE_ANALYSIS.md','contest_spec.json','imp_art_inventory.json']]
    return {p:sha(source_bytes(p).decode("utf-8-sig").replace("\r\n","\n").encode("utf-8")) for p in sorted(chosen)}

def preview(path):
    data=source_bytes(path)
    if path.endswith('.svg'):return 'data:image/svg+xml;base64,'+base64.b64encode(data).decode()
    im=Image.open(io.BytesIO(data)).convert('RGBA');im.thumbnail((768,768))
    buf=io.BytesIO();im.save(buf,format='WEBP',quality=88)
    return 'data:image/webp;base64,'+base64.b64encode(buf.getvalue()).decode()

def markdown_prose(document):
    def inline(text):
        text=html.escape(text)
        text=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',r'<a href="\2">\1</a>',text)
        text=re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',text)
        return re.sub(r'`([^`]+)`',r'<code>\1</code>',text)
    blocks=[]
    for part in document.split('\n\n'):
        if part.startswith('#'):
            match=re.match(r'(#{1,6}) (.*)',part);level=len(match[1]);blocks.append(f'<h{level}>{inline(match[2])}</h{level}>')
        elif re.match(r'\d+\. ',part):
            blocks.append('<ol>'+''.join('<li>'+inline(re.sub(r'^\d+\. ','',line))+'</li>' for line in part.splitlines())+'</ol>')
        else:blocks.append('<p>'+inline(part)+'</p>')
    return ''.join(blocks)

def render(rows,reviews,baseline):
    evaluations=json.loads((OUT/'evaluations.json').read_text(encoding='utf-8'))
    cached={}
    existing=OUT/'index.html'
    if existing.exists():
        match=re.search(r'<script id="library-data" type="application/json">(.*?)</script>',existing.read_text(encoding='utf-8'),re.S)
        if match:cached={r['path']:r for r in json.loads(match[1])['items']}
    data=[]
    for r in rows:
        item=dict(r);old=cached.get(r['path'])
        item['preview']=old['preview'] if old and old['sha256']==r['sha256'] else preview(r['path']);data.append(item)
    document=(OUT/'REPORT.md').read_text(encoding='utf-8')
    # Markdown remains the canonical written companion; HTML embeds readable prose.
    intro=markdown_prose(document)
    payload=json.dumps({'items':data,'evaluations':evaluations},ensure_ascii=False).replace('</','<\\/')
    page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Day Two · Artwork review library</title>
<style>:root{color-scheme:light;--ink:#242745;--paper:#fffaf0;--mint:#d8eee4}*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.6 system-ui}header,main{max-width:1460px;margin:auto;padding:28px}header{background:var(--mint);border-radius:0 0 32px 32px}h1{font:600 40px/1.15 Georgia}h2{font:600 29px Georgia;margin-top:32px}h3{font:600 22px Georgia}a{color:#303b85}p{max-width:1050px}.notice{padding:15px;background:#fff0d4;border-left:5px solid #ce8733}nav,form{display:flex;gap:12px;flex-wrap:wrap;align-items:center}select,input,button{font:inherit;padding:9px;border:1px solid #aaa4ba;border-radius:8px;background:white;color:var(--ink)}input{min-width:220px}button{cursor:pointer}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:18px}.card,.evaluation{border:1px solid #d2cbd4;border-radius:16px;background:white;padding:18px}.art{width:100%;height:248px;object-fit:contain;background:repeating-conic-gradient(#d5cfdb 0% 25%,#eee9f0 0% 50%) 50%/24px 24px;border-radius:10px}.score{float:right;font-weight:750}.priority{color:#9a3e1f}.path{font:12px/1.5 ui-monospace;overflow-wrap:anywhere}.meta{font-size:13px;color:#60576c}.card button{margin-top:8px}details{margin:20px 0}summary{cursor:pointer;font-weight:700}dialog{border:0;border-radius:20px;max-width:1100px;width:92vw;max-height:94vh;overflow:auto;padding:26px;box-shadow:0 10px 60px #25223666}dialog::backdrop{background:#161423aa}dialog img{width:100%;height:min(55vh,650px);object-fit:contain;background:#c9c3d1}table{border-collapse:collapse;width:100%;font-size:14px}td,th{padding:10px;text-align:left;border-bottom:1px solid #ddd;vertical-align:top}.phases td:first-child{width:20%}.close{float:right}.shot{height:auto;max-height:500px;width:100%;object-fit:contain;background:#ece8ed}.sticky{position:sticky;top:0;background:var(--paper);padding:12px 0;z-index:5}#count{font-weight:700}.evaluation{margin-bottom:22px}.summary-links a{margin-right:15px}@media(max-width:600px){header,main{padding:16px}h1{font-size:32px}select,input{max-width:100%}.phases,.phases tbody,.phases tr,.phases td{display:block;width:100%;overflow-wrap:anywhere}.phases thead{display:none}.phases tr{margin-bottom:18px;border-bottom:2px solid #d2cbd4}.phases td{border:0;padding:6px 0}.phases td:first-child{width:100%;font-weight:700}.phases td:nth-child(2)::before{content:"Visual review: ";font-weight:700}.phases td:nth-child(3)::before{content:"Next evidence: ";font-weight:700}}</style>
<header><p>Mermaid Roshan · First pass · 30 September 2026</p><h1>Day Two artwork<br>and game sequence library</h1><p>Every source image has its own score, observations and next review action. Browse all careers, the Opera training/show paths, the birthday jobs and Tree Book.</p><p class="notice">Draft source scores are design opinions. A score at or below 4.5/5 is a refinement priority. No score here establishes current gameplay, animation, device, child or owner acceptance.</p><nav><a href="#written">Written review</a><a href="#games">Games and phases</a><a href="#artwork">Artwork gallery</a><a href="#evidence">Historical compositions</a></nav><p class="meta">Source baseline BASELINE · Thumbnails preserve whole source composition; originals and full hashes are linked per item.</p></header><main><details id="written"><summary>Read the complete first-pass report and refresh instructions</summary>INTRO</details><section id="games"><h2>Every game and its visual sequence</h2><div id="game-list"></div></section><section id="artwork"><h2>Individual artwork reviews</h2><form class="sticky" onsubmit="return false"><input id="search" placeholder="Search ID, filename or review" aria-label="Search artwork"><select id="career" aria-label="Career"><option value="">All careers and shared art</option></select><select id="role" aria-label="Art role"><option value="">All art roles</option></select><select id="filter" aria-label="Review filter"><option value="all">All images</option><option value="priority">Refinement: score ≤4.5</option><option value="retain">Retain: score &gt;4.5</option><option value="retired">Retired/inactive/reference alternatives</option><option value="pending">Pending new review</option></select><select id="sort" aria-label="Sort"><option value="id">Inventory order</option><option value="weak">Lowest scores first</option><option value="strong">Highest scores first</option></select><span id="count"></span></form><div class="grid" id="gallery"></div></section><section id="evidence"><h2>Recorded composition examples</h2><p class="notice">These are earlier diagnostic captures, labeled with their own manifests. They illustrate composition concerns and are not fresh captures of the source baseline.</p><div id="shots"></div></section></main><dialog id="detail"><button class="close" onclick="this.closest('dialog').close()">Close</button><div id="detail-content"></div></dialog><script id="library-data" type="application/json">PAYLOAD</script><script>
const data=JSON.parse(document.getElementById('library-data').textContent),items=data.items;
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const raw=p=>'https://github.com/Ebonyks/mermaid-roshan-reef/blob/BASELINE/'+p.split('/').map(encodeURIComponent).join('/');
for(const key of ['career','role'])for(const val of [...new Set(items.map(x=>x[key]))].sort()){const o=document.createElement('option');o.value=val;o.textContent=val;document.getElementById(key).append(o)}
function show(id){const x=items.find(x=>x.id===id);document.getElementById('detail-content').innerHTML=`<h2>${esc(x.id)} · ${esc(x.path.split('/').pop())}</h2><img src="${x.preview}" alt="${esc(x.path)}"><p><b>${x.draft_source_score??'Pending'}/5</b> · ${esc(x.usage)}</p><p>${esc(x.review)}</p><p><b>Next action:</b> ${esc(x.refinement)}</p><p class="path">${esc(x.path)}<br>SHA-256 ${esc(x.sha256)}<br>${x.width} × ${x.height}</p><p>${esc(x.rule_ids.join(', '))}</p><p>${esc(x.review_basis)}</p><p class="notice">${esc(x.acceptance)}</p><a href="${raw(x.path)}" target="_blank" rel="noopener">Inspect original at the exact source revision</a>`;document.getElementById('detail').showModal()}
function draw(){const q=document.getElementById('search').value.toLowerCase(),career=document.getElementById('career').value,role=document.getElementById('role').value,f=document.getElementById('filter').value;
let visible=items.filter(x=>(!career||x.career===career)&&(!role||x.role===role)&&(!q||[x.id,x.path,x.review,x.refinement].join(' ').toLowerCase().includes(q))&&(f==='all'||f==='priority'&&x.priority||f==='retain'&&x.draft_source_score>4.5||f==='retired'&&/retired|reference|superseded|inactive/.test(x.usage)||f==='pending'&&x.draft_source_score==null));const s=document.getElementById('sort').value;if(s!=='id')visible.sort((a,b)=>(s==='weak'?1:-1)*((a.draft_source_score??-1)-(b.draft_source_score??-1)));document.getElementById('count').textContent=visible.length+' / '+items.length+' images';document.getElementById('gallery').innerHTML=visible.map(x=>`<article class="card"><span class="score ${x.priority?'priority':''}">${x.draft_source_score??'Pending'}/5</span><h3>${esc(x.id)}</h3><img class="art" loading="lazy" src="${x.preview}" alt="${esc(x.path)}"><p class="path">${esc(x.path)}</p><p class="meta">${esc(x.career)} · ${esc(x.role)} · ${esc(x.usage)}</p><p>${esc(x.review)}</p><p><b>Refine:</b> ${esc(x.refinement)}</p><button onclick="show('${x.id}')">Details and original</button></article>`).join('')}
for(const id of ['search','career','role','filter','sort'])document.getElementById(id).addEventListener(id==='search'?'input':'change',draw);draw();
document.getElementById('game-list').innerHTML=data.evaluations.games.map(g=>`<article class="evaluation"><h3>${esc(g.title)} <span class="score">${g.draft_design_score==null?'Pending':g.draft_design_score+'/5'}</span></h3><p class="meta">${esc(g.status)} · Provisional design/sequence score, not a current runtime grade</p><p>${esc(g.evaluation)}</p><p><b>Refinement:</b> ${esc(g.refinement)}</p><p><b>Artwork:</b> ${g.artwork_ids.map(id=>`<button onclick="show('${id}')">${id}</button>`).join(' ')}</p><details><summary>${g.phases.length} phase evaluations</summary><table class="phases"><thead><tr><th>Phase / interaction</th><th>Graphic interaction and continuity review</th><th>Required next evidence</th></tr></thead><tbody>${g.phases.map(p=>`<tr><td>${esc(p.name)}<br><span class="meta">${esc(p.mode)}</span></td><td>${esc(p.review)}</td><td>${esc(p.next_evidence)}</td></tr>`).join('')}</tbody></table></details></article>`).join('');
document.getElementById('shots').innerHTML=data.evaluations.captures.map(c=>`<article class="evaluation"><h3>${esc(c.caption)}</h3><img class="shot" loading="lazy" src="${c.preview}" alt="${esc(c.caption)}"><p>${esc(c.review)}</p><p class="path">${esc(c.path)}<br>${esc(c.sha256)}</p><p class="meta">${esc(c.evidence_limit)} · Manifest: ${esc(c.manifest)}</p></article>`).join('');
</script></html>'''.replace('BASELINE',baseline).replace('INTRO',intro).replace('PAYLOAD',payload)
    (OUT/'index.html').write_text(page,encoding='utf-8')
    with (OUT/'priority_queue.csv').open('w',newline='',encoding='utf-8-sig') as f:
        writer=csv.DictWriter(f,fieldnames=['id','path','career','role','usage','draft_source_score','review','refinement','sha256']);writer.writeheader()
        writer.writerows({k:r.get(k,'') for k in writer.fieldnames} for r in sorted(rows,key=lambda r:(r['draft_source_score'] is None,r['draft_source_score'] or 0,r['id'])) if r['priority'])
    print(json.dumps({'images':len(rows),'priority_at_or_below_4_5':sum(r['priority'] for r in rows),'games':len(evaluations['games']),'phases':sum(len(g['phases']) for g in evaluations['games']),'html_bytes':(OUT/'index.html').stat().st_size}))
def main():
    p=argparse.ArgumentParser(); p.add_argument('--inventory',action='store_true'); p.add_argument('--contacts',action='store_true'); p.add_argument('--render',action='store_true');p.add_argument('--refresh',action='store_true');p.add_argument('--check',action='store_true');args=p.parse_args()
    OUT.mkdir(parents=True,exist_ok=True)
    rows=inventory()
    review_file=OUT/'reviews.json'
    reviews=json.loads(review_file.read_text(encoding='utf-8')) if review_file.exists() else {'items':[]}
    authored={r['path']:r for r in reviews['items']}
    for r in rows:
        a=authored.get(r['path'])
        if a and a['sha256']==r['sha256']:
            for key in ['draft_source_score','review','rule_ids','usage','refinement','review_basis']:r[key]=a[key]
            for key in ['imp_binding_evidence','reviewed_checkout_sha256']:
                if key in a:r[key]=a[key]
            r['priority']=r['draft_source_score'] is not None and r['draft_source_score']<=4.5
        else:r['review']='PENDING_REVIEW: new or changed bytes; prior score invalidated.'
    watch=watched_sources()
    previous=json.loads((OUT/'inventory.json').read_text(encoding='utf-8')) if (OUT/'inventory.json').exists() else {'items':[],'watched_sources':{}}
    if args.refresh:
        old={r['path']:r for r in previous['items']};now={r['path']:r for r in rows}
        old_watch=previous.get('watched_sources',{})
        delta={'source_revision':git('rev-parse','HEAD').decode().strip(),'added':sorted(set(now)-set(old)),'removed':sorted(set(old)-set(now)),'changed':[p for p in now if p in old and now[p]['sha256']!=old[p]['sha256']],'changed_controllers_or_authority':[p for p in sorted(set(watch)|set(old_watch)) if old_watch.get(p)!=watch.get(p)], 'required_action':'Human review new/changed images and all affected phase/composition evaluations. No scores are inferred or promoted.'}
        (OUT/'refresh_delta.json').write_text(json.dumps(delta,indent=2)+'\n',encoding='utf-8')
        if any(delta[k] for k in ['added','removed','changed','changed_controllers_or_authority']):
            reviews['composition_status']='STALE: changed source requires a new context/sequence review'
            review_file.write_text(json.dumps(reviews,indent=2)+'\n',encoding='utf-8')
    if args.check:
        errors=[]
        if len(rows)!=len(previous['items']):errors.append('Inventory count changed; run --refresh')
        if {r['path']:r['sha256'] for r in rows}!={r['path']:r['sha256'] for r in previous['items']}:errors.append('Image census/bytes changed; run --refresh')
        if watch!=previous.get('watched_sources'):errors.append('Controller/authority bytes changed; run --refresh')
        for r in rows:
            if r['draft_source_score'] is None:errors.append(r['id']+' missing current human source review')
            elif not 0<=r['draft_source_score']<5:errors.append(r['id']+' invalid drafting score')
            elif r['priority']!=(r['draft_source_score']<=4.5):errors.append(r['id']+' threshold mismatch')
        ids={r['id'] for r in rows}
        if len(ids)!=len(rows):errors.append('Duplicate image identifiers')
        evaluations=json.loads((OUT/'evaluations.json').read_text(encoding='utf-8'))
        game_ids=[g['id'] for g in evaluations['games']]
        if len(set(game_ids))!=len(game_ids):errors.append('Duplicate context identifiers')
        for game in evaluations['games']:
            missing=set(game['artwork_ids'])-ids
            if missing:errors.append(game['id']+' has unresolved artwork IDs: '+', '.join(sorted(missing)))
            if not game.get('evaluation'):errors.append(game['id']+' lacks context review')
            if not game.get('phases') and game.get('draft_design_score') is not None:errors.append(game['id']+' scores an unreviewed sequence')
            for phase in game['phases']:
                if not all(phase.get(k) for k in ['name','mode','review','next_evidence']):errors.append(game['id']+' has incomplete phase review')
        if reviews.get('composition_status','').startswith('STALE'):errors.append('Composition review stale')
        if errors:raise SystemExit('\n'.join(errors))
        print(f'PASS: {len(rows)} individually source-bound reviews; inclusive <=4.5 threshold; controller/authority fingerprints current; no acceptance promotion')
        return
    baseline=previous.get('baseline',git('rev-parse','HEAD').decode().strip())
    (OUT/'inventory.json').write_text(json.dumps({'baseline':baseline,'source_revision':git('rev-parse','HEAD').decode().strip(),'watched_sources':watch,'items':rows},indent=2)+'\n',encoding='utf-8')
    if args.contacts: contacts(rows)
    elif args.render: render(rows,reviews,baseline)
    else: print(json.dumps({'items':len(rows),'roles':Counter(r['role'] for r in rows)}))
if __name__=='__main__': main()
