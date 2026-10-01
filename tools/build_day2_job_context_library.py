"""Build a source-bound, usage-aware job graphics library; never auto-grade art."""
from __future__ import annotations
import argparse, csv, hashlib, html, io, json, re, subprocess
from collections import Counter, defaultdict
from functools import lru_cache
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'audit/day2_job_contexts_2026-09-30'
OLD = ROOT / 'audit/day2_art_library_2026-09-30'
REV = 'ce0331738970205a5aead4d3e0258eb7873a1642'
DRAW_FILES = ['opera_career_world_2d','opera_gesture_surface','opera_world_backdrop_2d',
 'opera_teacher_surface','opera_geology_surface','opera_ballet_surface','opera_boxing_surface',
 'opera_racer_surface','opera_nursery_catch','opera_tree_book_test','opera_performance_overlay',
 'opera_world_hotspot_2d','chapter_two_giant_cake_2d','chapter_two_rainbow_candle_2d',
 'chapter_two_party_table_2d','chapter_two_room_plot','opera_house_venue_2d','castle_career_routes']

def digest(data): return hashlib.sha256(data).hexdigest()
def read(path): return json.loads(path.read_text(encoding='utf-8'))
def write(path, data): path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
def h(value): return html.escape(str(value))
@lru_cache(maxsize=4096)
def source_hash(path): return digest((ROOT/path).read_bytes())

def load_capture():
    capture=read(OUT/'capture_manifest.json')
    if capture.get('state_files'):
        capture['states']=[state for path in capture['state_files'] for state in read(OUT/path)['states']]
    if (OUT/'output_capture_manifest.json').exists():
        capture['states'].extend(read(OUT/'output_capture_manifest.json')['states'])
    return capture

def load_inventory():
    inv=read(OUT/'inventory.json')
    if inv.get('usage_files'):
        inv['usages']=[row for path in inv['usage_files'] for row in read(OUT/path)['usages']]
    return inv

def save_inventory(inv):
    grouped=defaultdict(list)
    for row in inv['usages']:grouped[row['case']].append(row)
    (OUT/'usages').mkdir(exist_ok=True)
    index=dict(inv);index.pop('usages');index['usage_files']=[]
    for case,rows in grouped.items():
        path='usages/'+case+'.json';write(OUT/path,{'case':case,'usages':rows});index['usage_files'].append(path)
    write(OUT/'inventory.json',index)

def package_captures():
    raw=(OUT/'capture_manifest.json').read_bytes();capture=json.loads(raw)
    if capture.get('state_files'): return
    archive=ROOT/'tmp/job-context-native-capture-manifest.json';archive.write_bytes(raw)
    grouped=defaultdict(list)
    for state in capture.pop('states'):grouped[state['case']].append(state)
    (OUT/'states').mkdir(exist_ok=True)
    capture['state_files']=[]
    capture['raw_manifest_sha256']=digest(raw)
    capture['packaging']='Lossless JSON partition by context; every native state, item, snapshot, image and hash retained. No frame transformation.'
    for case,states in grouped.items():
        path='states/'+case+'.json';write(OUT/path,{'case':case,'states':states});capture['state_files'].append(path)
    write(OUT/'capture_manifest.json',capture)

def census():
    capture = load_capture()
    old = read(OLD/'inventory.json')['items']
    reviews = {x['path']:x for x in read(OLD/'reviews.json')['items']}
    inventory = {x['path']:dict(x, preview='../day2_art_library_2026-09-30/previews/'+x['id']+('.svg' if x['path'].endswith('.svg') else '.webp')) for x in old}
    usages = []
    controls = []
    for state in capture['states']:
        for item in state['items']:
            if item['class'] in ['Button','Label','ProgressBar','ColorRect','Panel','PanelContainer']:
                controls.append({'id':'D2C-%05d' % (len(controls)+1),
                    'state':state['id'],'case':state['case'],'phase_index':state['phase_index'],
                    'beat':state['beat'],'aspect':state['aspect'],'node':item['node'],
                    'class':item['class'],'text':item.get('text',''),'color':item.get('color'),
                    'rect':item.get('rect'),'modulate':item.get('modulate'),
                    'draft_score':None,'runtime_grade':None,'owner_accepted':False})
            for texture in item['textures']:
                path = texture.get('path', '')
                if not path or path=='GENERATED_TEXTURE': continue
                source = ROOT/path
                if not source.exists(): raise ValueError('Missing capture source '+path)
                file_hash = source_hash(path)
                if file_hash != texture['sha256']: raise ValueError('Changed capture source '+path)
                if path not in inventory:
                    data = source.read_bytes()
                    identifier = 'D2X-%04d' % (len(inventory)-len(old)+1)
                    preview = 'art/'+identifier+('.svg' if path.endswith('.svg') else '.webp')
                    (OUT/'art').mkdir(exist_ok=True)
                    if path.endswith('.svg'):
                        (OUT/preview).write_bytes(data)
                        size=[None,None]
                    else:
                        image = Image.open(io.BytesIO(data)).convert('RGBA')
                        size=list(image.size)
                        image.thumbnail((640,640))
                        image.save(OUT/preview, 'WEBP', lossless=True)
                    inventory[path]={'id':identifier, 'path':path, 'sha256':digest(data),
                        'width':size[0], 'height':size[1], 'preview':preview,
                        'role':'Additional entrance/shared/dynamic texture', 'career':'shared'}
                row=inventory[path]
                old_review = reviews.get(path, {})
                review_hash = source_hash(path)
                if path.endswith('.svg'): review_hash=digest(source.read_bytes().replace(b'\r\n',b'\n'))
                source_score=old_review.get('draft_source_score') if old_review.get('sha256')==review_hash else None
                usages.append({'id':'D2U-%05d' % (len(usages)+1), 'state':state['id'],
                    'case':state['case'], 'phase_index':state['phase_index'], 'beat':state['beat'],
                    'aspect':state['aspect'], 'node':item['node'], 'slot':texture['slot'],
                    'source_id':row['id'], 'source_path':path, 'source_sha256':file_hash,
                    'atlas_region':texture.get('region'), 'node_rect':item.get('rect'),
                    'source_score':source_score, 'context_score':None,
                    'runtime_grade':None, 'owner_accepted':False,
                    'binding':'Visible node texture' if item['class'] in ['TextureRect','Sprite2D'] and texture['slot'] in ['texture','normal_map','atlas'] else 'Stored draw input; branch visibility requires pixel review',
                    'review':old_review.get('review','Newly included source; individual visual review required'),
                    'refinement':old_review.get('refinement','Inspect outline, style, phone-scale silhouette and in-context ownership.')})
    components=[]
    for stem in DRAW_FILES:
        path='scripts/'+stem+'.gd'
        text=(ROOT/path).read_text(encoding='utf-8-sig')
        parts=list(re.finditer(r'^func (\w+)\([^\n]*',text,re.M))
        for index,m in enumerate(parts):
            body=text[m.start():parts[index+1].start() if index+1<len(parts) else len(text)]
            calls=[{'line':text[:m.start()].count('\n')+1+n, 'code':line.strip()} for n,line in enumerate(body.splitlines()) if re.search(r'\bdraw_(?:circle|rect|line|polyline|polygon|colored_polygon|arc|style_box|texture|texture_rect|texture_rect_region|string|set_transform)',line)]
            if not calls: continue
            components.append({'id':'D2P-%04d' % (len(components)+1), 'source':path,
                'function':m[1], 'line':text[:m.start()].count('\n')+1,
                'source_sha256':digest((ROOT/path).read_bytes()), 'draw_calls':calls,
                'draft_component_score':None, 'review':'Source drawing component inventoried; actual branch and visual review required.',
                'runtime_grade':None, 'owner_accepted':False})
    sources={p:digest((ROOT/p).read_bytes()) for p in sorted({x['source'] for x in components}|{
        'scripts/opera_house.gd','scripts/chapter_two_party_plan.gd','scripts/chapter_two_career_scene_adapter.gd',
        'scripts/opera_performance_plan.gd','scripts/chapter_two_director.gd','scripts/opera_roshan_actor.gd',
        'scripts/opera_imp_clips.gd','scripts/opera_hotspot_catalog.gd','scripts/teacher_lesson_plan.gd',
        'design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md','design/CHAPTER2_EIGHT_CAREER_PRODUCTION_SPINE_2026-08-30.md',
        'design/OPERA_TREE_BOOK_TEST_2026-09-30.md','tools/capture_day2_job_contexts.gd',
        'tools/capture_day2_job_outputs.gd'})}
    save_inventory({'production_revision':REV,'captured_at_utc':capture['captured_at_utc'],
        'sources':sources,'items':list(inventory.values()),'usages':usages,'drawing_components':components,
        'qualification':'Loaded draw inputs are a conservative inclusion census, not proof that their pixels appear.'})
    (OUT/'.gdignore').write_text('')
    grouped=defaultdict(list)
    for row in controls:grouped[row['case']].append(row)
    (OUT/'controls').mkdir(exist_ok=True)
    control_index=[]
    for case,rows in grouped.items():
        path='controls/'+case+'.json';write(OUT/path,{'case':case,'items':rows});control_index.append(path)
    write(OUT/'control_index.json',{'files':control_index,'instances':len(controls),
        'qualification':'Visible built-in node instances; transparent hit areas and zero-alpha overlays are recorded as non-art, not fabricated defects.'})
    print('JOBLIB|CENSUS|sources=%d usages=%d components=%d states=%d controls=%d' % (len(inventory),len(usages),len(components),len(capture['states']),len(controls)))

def cells():
    """Expose every current career atlas cell as a reversible inspection crop."""
    folder=OUT/'cells';folder.mkdir(exist_ok=True)
    rows=[]
    for source in sorted((ROOT/'assets/opera/worlds/actors/animation').glob('roshan_*_sheet_a.png')):
        im=Image.open(source).convert('RGBA');career=source.stem[7:-8]
        if im.size!=(1024,1024):raise ValueError('Unexpected current atlas '+str(source))
        for row,pose in enumerate(['idle','travel','work','cheer']):
            for col in range(4):
                identifier='D2F-%04d'%(len(rows)+1);region=[col*256,row*256,256,256]
                preview='cells/'+identifier+'.webp'
                im.crop((region[0],region[1],region[0]+256,region[1]+256)).save(OUT/preview,'WEBP',lossless=True)
                rows.append({'id':identifier,'career':career,'pose':pose,'frame':col,
                    'source':source.relative_to(ROOT).as_posix(),'source_sha256':digest(source.read_bytes()),
                    'region':region,'preview':preview,'preview_sha256':digest((OUT/preview).read_bytes()),
                    'draft_score':None,'runtime_grade':None,'owner_accepted':False,
                    'qualification':'All 16 cells individually inspected; source pose opinion, not proof of a motion sequence or active phase binding.'})
    write(OUT/'atlas_cells.json',{'items':rows})

def contacts():
    capture=load_capture()
    groups=defaultdict(list)
    for state in capture['states']:
        if state['aspect']=='1280x720' and state['beat'] in ['open','foyer','entrance','output-fixture']:
            groups[state['case']].append(state)
    folder=ROOT/'tmp/job-context-contact-sheets';folder.mkdir(exist_ok=True)
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',16)
    for case,states in groups.items():
        columns=2; width=1280; height=((len(states)+1)//2)*392
        board=Image.new('RGB',(width,height),'#eee9e0');draw=ImageDraw.Draw(board)
        for index,state in enumerate(states):
            x=(index%2)*640;y=(index//2)*392
            im=Image.open(OUT/state['image']).convert('RGB');im.thumbnail((640,360));board.paste(im,(x,y))
            label=state['id'].split('--')[0]+' / '+str(state.get('phase',{}).get('name',state['beat']))
            draw.text((x+8,y+364),label,fill='#243e52',font=font)
        board.save(folder/(case+'.jpg'),quality=92)
    extra=[x for x in load_inventory()['items'] if x['id'].startswith('D2X')] if (OUT/'inventory.json').exists() else []
    for start in range(0,len(extra),24):
        rows=extra[start:start+24];board=Image.new('RGB',(1200,((len(rows)+3)//4)*240),'#dcd4e9');draw=ImageDraw.Draw(board)
        for n,row in enumerate(rows):
            if row['path'].endswith('.svg'):continue
            im=Image.open(OUT/row['preview']).convert('RGBA');im.thumbnail((292,196));x=n%4*300;y=n//4*240
            board.paste(im,(x+(300-im.width)//2,y),im)
            draw.text((x+5,y+198),row['id']+' '+Path(row['path']).name[:30],font=font,fill='#241636')
        board.save(folder/('extra-%03d.jpg'%start),quality=92)

def render():
    inv=load_inventory();capture=load_capture();rev=read(OUT/'reviews.json')
    asset_reviews=rev.get('assets',{});component_reviews=rev.get('components',{});phase_reviews=rev.get('phases',{})
    old_reviews={x['path']:x for x in read(OLD/'reviews.json')['items']}
    assets={x['id']:x for x in inv['items']}
    usages=inv['usages']
    for usage in usages:
        key=usage['case']+'/%d'%usage['phase_index'];review=phase_reviews.get(key,{})
        usage['context_score']=review.get('score')
        usage['context_review']=review.get('review','Current state review still required')
        usage['context_refinement']=review.get('refinement','Collect remaining state/input evidence')
        extra=asset_reviews.get(usage['source_id'])
        if extra: usage['source_score']=extra.get('score');usage['review']=extra['review'];usage['refinement']=extra['refinement']
        usage['priority']=usage['source_score'] is None or usage['source_score']<=4.5 or usage['context_score'] is None or usage['context_score']<=4.5
    for component in inv['drawing_components']:
        if component['id'] in component_reviews: component.update(component_reviews[component['id']])
    save_inventory(inv)
    summary={'source_items':len(assets),'additional_sources':len(asset_reviews),
        'diagnostic_states':len(capture['states']),'cases':len({x['case'] for x in capture['states']}),
        'phases':len({(x['case'],x['phase_index']) for x in capture['states'] if x['phase_index']>=0 and x['beat']!='reward-fixture'}),
        'usages':len(usages),'priority_usages':sum(x['priority'] for x in usages),
        'drawing_components':len(inv['drawing_components']),
        'scored_components':sum(x['draft_component_score'] is not None for x in inv['drawing_components']),
        'phase_reviews':len(phase_reviews),'acceptance':'DRAFT; OWNER_APPROVAL_PENDING'}
    write(OUT/'summary.json',summary)
    with (OUT/'priority_queue.csv').open('w',newline='',encoding='utf-8') as f:
        fields=['id','case','phase_index','beat','aspect','source_id','source_path','source_score','context_score']
        writer=csv.DictWriter(f,fields,extrasaction='ignore');writer.writeheader();writer.writerows(x for x in usages if x['priority'])
    grouped=defaultdict(list)
    for state in capture['states']:grouped[state['case']].append(state)
    cards=[]
    for case,states in grouped.items():
        phase_groups=defaultdict(list)
        for state in states:phase_groups[state['phase_index']].append(state)
        inner=[]
        for phase,examples in phase_groups.items():
            review=phase_reviews.get(case+'/%d'%phase,{})
            title=next((s.get('phase',{}).get('name') for s in examples if s.get('phase',{}).get('name')), 'Entrance / return controls' if phase<0 else 'Tree Book page %d'%phase)
            pictures=''.join('<a href="%s" target="_blank"><figure><img loading="lazy" width="%d" height="%d" src="%s"><figcaption>%s · %s</figcaption></figure></a>'%(h(s['image']),s['dimensions'][0],s['dimensions'][1],h(s['image']),h(s['beat']),h(s['aspect'])) for s in examples)
            rows=[x for x in usages if x['case']==case and x['phase_index']==phase]
            # Distinct texture slots remain independent usage IDs. Collapse only
            # the screenshot/aspect repetition for the reading interface.
            distinct={}
            for row in rows: distinct.setdefault((row['node'],row['slot'],row['source_id']),row)
            table=''.join('<tr><td><a href="#%s">%s</a></td><td>%s<br><small>%s / %s</small></td><td>%s</td><td>%s</td><td>%s</td></tr>'%(h(x['source_id']),h(x['id']),h(Path(x['source_path']).name),h(x['node'].split('/')[-1]),h(x['slot']),h(x['source_score']),h(x['context_score']),h(x['binding'])) for x in distinct.values())
            inner.append('<article><h3>%s · draft %s/5</h3><p>%s</p><p><b>Refinement:</b> %s</p><div class="shots">%s</div><details><summary>%d distinct item slots; every beat/aspect usage in inventory and CSV</summary><div class="scroll"><table><tr><th>ID</th><th>Item / node slot</th><th>Source</th><th>Context</th><th>Visibility evidence</th></tr>%s</table></div></details></article>'%(h(title),h(review.get('score','UNREVIEWED')),h(review.get('review','')),h(review.get('refinement','')),pictures,len(distinct),table))
        seq=rev.get('sequences',{}).get(case,{})
        cards.append('<section class="case" data-search="%s"><h2>%s</h2><p>%s</p>%s</section>'%(h(case),h(case.replace('-',' ').title()),h(seq.get('review','')),''.join(inner)))
    source_cards=[]
    for identifier,row in assets.items():
        review=asset_reviews.get(identifier,old_reviews.get(row['path'],{}));score=review.get('score',review.get('draft_source_score'))
        source_cards.append('<article class="source" id="%s" data-search="%s"><h3>%s · %s/5</h3><img loading="lazy" src="%s"><p>%s</p><p>%s</p><small>%s</small></article>'%(h(identifier),h(identifier+' '+row['path']),h(identifier),h(score if score is not None else 'UNREVIEWED'),h(row['preview']),h(review.get('review','Additional source awaiting review')),h(review.get('refinement','')),h(row['path'])))
    components=[]
    for row in inv['drawing_components']:
        code='\n'.join('%d: %s'%(x['line'],x['code']) for x in row['draw_calls'])
        components.append('<article class="component" data-search="%s"><h3>%s · %s · %s/5</h3><p>%s</p><p>%s</p><details><summary>%s:%d · %d draw calls</summary><pre>%s</pre></details></article>'%(h(row['source']+' '+row['function']),h(row['id']),h(row['function']),h(row['draft_component_score'] if row['draft_component_score'] is not None else 'UNREVIEWED'),h(row['review']),h(row.get('refinement','')),h(row['source']),row['line'],len(row['draw_calls']),h(code)))
    control_cards=[];control_rows=[]
    for path in read(OUT/'control_index.json')['files']:
        data=read(OUT/path)
        for row in data['items']:
            key=row['case']+'/'+row['node'].split('/')[-1]+'/'+row['class']
            row.update(rev.get('controls',{}).get(key,{}));control_rows.append(row)
        write(OUT/path,data)
    for key,row in {(x['case'],x['node'].split('/')[-1],x['class']):x for x in control_rows}.items():
        control_cards.append('<article class="component" data-search="%s"><h3>%s · %s · %s/5</h3><p>%s</p><p>%s</p><small>%s · %s · %s</small></article>'%(h(' '.join(key)),h(row['id']),h(key[1]),h(row.get('draft_score') if row.get('draft_score') is not None else row.get('status','UNREVIEWED')),h(row.get('review','')),h(row.get('refinement','')),h(key[0]),h(key[2]),h(row.get('rect'))))
    cell_data=read(OUT/'atlas_cells.json');cell_cards=[]
    for row in cell_data['items']:
        row.update(rev.get('cells',{}).get(row['id'],{}))
        cell_cards.append('<article class="source" id="%s" data-search="%s"><h3>%s · %s/5</h3><img loading="lazy" src="%s"><p>%s %s %s</p><p>%s</p><p>%s</p></article>'%(h(row['id']),h(row['career']+' '+row['pose']+' '+row['id']),h(row['id']),h(row.get('draft_score','UNREVIEWED')),h(row['preview']),h(row['career']),h(row['pose']),row['frame'],h(row.get('review','')),h(row.get('refinement',''))))
    write(OUT/'atlas_cells.json',cell_data)
    summary.update({'control_instances':len(control_rows),'atlas_cells':len(cell_cards),
        'unscored_nonvisual_controls':sum(x.get('draft_score') is None for x in control_rows)})
    write(OUT/'summary.json',summary)
    with (OUT/'detail_priorities.csv').open('w',newline='',encoding='utf-8') as f:
        fields=['id','category','career','case','phase_index','node','source','pose','frame','draft_score','draft_component_score','status','review','refinement']
        writer=csv.DictWriter(f,fields,extrasaction='ignore');writer.writeheader()
        writer.writerows(dict(x,category='atlas_cell') for x in cell_data['items'] if x['draft_score'] is not None and x['draft_score']<=4.5)
        writer.writerows(dict(x,category='code_draw') for x in inv['drawing_components'] if x['draft_component_score'] is not None and x['draft_component_score']<=4.5)
        writer.writerows(dict(x,category='control') for x in control_rows if x.get('draft_score') is not None and x['draft_score']<=4.5)
    payload=f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Every job · artwork in context</title><style>
body{{margin:0;background:#f4f1e9;color:#263d4c;font:17px/1.5 system-ui}}header,main{{max-width:1440px;margin:auto;padding:24px}}header{{background:#dceff0}}nav{{position:sticky;top:0;background:#e3e8ee;padding:12px;z-index:100}}button,input{{font:inherit;padding:10px;margin:4px;border:1px solid #8191aa;border-radius:8px}}article{{background:white;border:1px solid #c1cad8;padding:18px;margin:16px 0;border-radius:12px}}h2{{margin-top:40px}}.shots{{display:grid;grid-template-columns:repeat(auto-fit,minmax(270px,1fr));gap:12px}}figure{{margin:0}}img{{display:block;width:100%;height:auto}}figcaption,small{{font-size:13px;overflow-wrap:anywhere}}a{{color:#345c94}}.sources{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:18px}}.source img{{height:260px;object-fit:contain;background:#e5dcec}}.scroll{{overflow:auto}}table{{border-collapse:collapse;width:100%;font-size:13px}}td,th{{border-bottom:1px solid #ccd;padding:8px;text-align:left}}pre{{overflow:auto;font-size:12px}}[hidden]{{display:none!important}}.notice{{background:#fff3d9;border-left:5px solid #b99441;padding:16px}}.source:target{{outline:4px solid #dc9d43}}
</style><header><p>Mermaid Roshan · draft graphics audit</p><h1>Every job, in context</h1><p>{summary['cases']} activity contexts · {summary['phases']} phases/pages · {summary['diagnostic_states']} fresh diagnostic frames · {len(assets)} source images · {len(usages)} texture usages · {len(inv['drawing_components'])} code-drawn components</p><p class="notice">All scores are drafting opinions. ≤4.5/5 is a refinement priority. Native captures use Godot 4.7.2 Mobile at two widths; direct state selection and hidden global HUD limit acceptance. Stored draw inputs may be absent from a frame. Nursery v4 remains owner-rejected as too lifelike. Owner, played motion, actual input, device and child acceptance remain open.</p><p><a href="REPORT.md">Written report</a> · <a href="priority_queue.csv">Individual priority queue</a> · <a href="inventory.json">Full usage inventory</a> · <a href="capture_manifest.json">Capture evidence</a> · <a href="../day2_art_library_2026-09-30/index.html">Earlier source and planned-contest library</a></p></header><nav><button data-tab="contexts">Jobs and sequences</button><button data-tab="sources">Every source image</button><button data-tab="components">Code-drawn items</button><input id="search" aria-label="Search" placeholder="Search career, item or function"></nav><main><div id="contexts">{''.join(cards)}</div><div id="sources" class="sources" hidden>{''.join(source_cards)}</div><div id="components" hidden>{''.join(components)}</div></main><script>
const panels=['contexts','sources','components'];function select(id){{panels.forEach(p=>document.getElementById(p).hidden=p!==id);document.querySelector('#search').value='';document.querySelectorAll('[data-search]').forEach(x=>x.hidden=false)}}document.querySelectorAll('[data-tab]').forEach(b=>b.onclick=()=>select(b.dataset.tab));document.querySelector('#search').oninput=e=>{{let q=e.target.value.toLowerCase();document.querySelectorAll('[data-search]').forEach(x=>x.hidden=!x.dataset.search.toLowerCase().includes(q))}};document.querySelectorAll('a[href^="#D2"]').forEach(a=>a.onclick=()=>select('sources'));if(location.hash.startsWith('#D2'))select('sources');
</script></html>'''
    payload=payload.replace('Earlier source and planned-contest library</a>', 'Earlier source and planned-contest library</a> · <a href="motion/index.html">Five completed local motion studies</a> · <a href="../../assets_src/imagegen/day2_refinement_20261001/index.html">Fresh reversible replacements</a> · <a href="../day2_action_continuity_20261001/index.html">Timed action reviews</a>')
    payload=payload.replace("['contexts','sources','components']","['contexts','sources','components','cells','controls']")
    payload=payload.replace('<input id="search"','<button data-tab="cells">All 240 actor cells</button><button data-tab="controls">Controls and panels</button><input id="search"')
    payload=payload.replace('</main>','<div id="cells" class="sources" hidden>'+''.join(cell_cards)+'</div><div id="controls" hidden>'+''.join(control_cards)+'</div></main>')
    payload=payload.replace("if(location.hash.startsWith('#D2'))select('sources');","if(location.hash.startsWith('#D2F'))select('cells');else if(location.hash.startsWith('#D2'))select('sources');")
    payload=payload.replace('Source drawing component inventoried; actual branch and visual review required.','Source drawing component inventoried; actual branch and visual review required.')
    (OUT/'index.html').write_text(payload,encoding='utf-8')
    print('JOBLIB|RENDER|'+json.dumps(summary))

def check():
    inv=load_inventory();capture=load_capture();review=read(OUT/'reviews.json')
    failures=[]
    for path,sha in inv['sources'].items():
        if digest((ROOT/path).read_bytes())!=sha:failures.append('stale controller '+path)
    for state in capture['states']:
        if digest((OUT/state['image']).read_bytes())!=state['sha256']:failures.append('stale capture '+state['id'])
        if state['save_error']!=0 or state['dimensions']!=list(map(int,state['aspect'].split('x'))):failures.append('invalid render '+state['id'])
    phases={(x['case'],x['phase_index']) for x in capture['states']}
    for case,phase in phases:
        if case+'/%d'%phase not in review['phases']:failures.append('unreviewed phase '+case+'/%d'%phase)
    for row in inv['items']:
        if not (OUT/row['preview']).exists():failures.append('missing art '+row['id'])
        source=ROOT/row['path']
        if not source.exists():failures.append('missing source '+row['id'])
        else:
            data=source.read_bytes()
            if source.suffix=='.svg':data=data.replace(b'\r\n',b'\n')
            if digest(data)!=row['sha256']:failures.append('stale source opinion '+row['id'])
    for usage in inv['usages']:
        if usage['source_score'] is None or usage['context_score'] is None:failures.append('missing draft opinion '+usage['id'])
    for row in inv['drawing_components']:
        if row['draft_component_score'] is None and row.get('status')!='SOURCE_ONLY_NOT_OBSERVED':failures.append('unqualified drawing component '+row['id'])
    for row in read(OUT/'atlas_cells.json')['items']:
        if row['draft_score'] is None:failures.append('unreviewed cell '+row['id'])
        if digest((OUT/row['preview']).read_bytes())!=row['preview_sha256']:failures.append('stale cell '+row['id'])
    for path in read(OUT/'control_index.json')['files']:
        for row in read(OUT/path)['items']:
            if row.get('draft_score') is None and row.get('status')!='NONVISUAL_NODE':failures.append('unqualified control '+row['id'])
    for path in OUT.rglob('*'):
        if path.is_file() and path.suffix in ['.json','.html','.csv','.md'] and path.stat().st_size>=4*1024*1024:failures.append('text scanner limit '+str(path.relative_to(OUT)))
    write(OUT/'verification.json',{'failures':failures,'source_count':len(inv['items']),'states':len(capture['states']),
        'qualification':'Completeness/freshness checks; no automatic visual, input, device, child or owner approval.'})
    print('JOBLIB|CHECK|'+ ('ALL OK' if not failures else str(len(failures))+' GAP(S) '+str(failures[:12])))
    return 1 if failures else 0

def delta():
    """Read-only comparison with the frozen evidence; do not carry grades forward."""
    inv=load_inventory();controllers=[];art=[]
    for path,sha in inv['sources'].items():
        current=digest((ROOT/path).read_bytes()) if (ROOT/path).exists() else None
        if current!=sha:controllers.append({'path':path,'recorded':sha,'current':current})
    for row in inv['items']:
        source=ROOT/row['path'];data=source.read_bytes() if source.exists() else None
        if data is not None and source.suffix=='.svg':data=data.replace(b'\r\n',b'\n')
        current=digest(data) if data is not None else None
        if current!=row['sha256']:art.append({'id':row['id'],'path':row['path'],'recorded':row['sha256'],'current':current})
    catalog_path=OUT/'image_catalog_snapshot.json'
    directories=sorted({str(Path(row['path']).parent).replace('\\','/') for row in inv['items']})
    current_catalog=sorted({p.relative_to(ROOT).as_posix() for directory in directories
        for p in (ROOT/directory).rglob('*') if p.is_file() and p.suffix.lower() in ['.png','.jpg','.jpeg','.webp','.svg']})
    if not catalog_path.exists():
        write(catalog_path,{'production_revision':inv['production_revision'],'directories':directories,
            'paths':current_catalog,'qualification':'Image-file discovery baseline only; inclusion is not a visual opinion or active-use claim.'})
    prior_catalog=read(catalog_path)['paths']
    value={'production_revision':inv['production_revision'],'controller_changes':controllers,
        'source_changes':art,'new_image_paths':sorted(set(current_catalog)-set(prior_catalog)),
        'removed_image_paths':sorted(set(prior_catalog)-set(current_catalog)),
        'action':'Recapture catalog/node census to discover new items and re-author affected opinions; preserve score/rejection history. New files require relevance and active-use review. No automatic approval or grade migration.'}
    write(OUT/'refresh_delta.json',value)
    print('JOBLIB|DELTA|controllers=%d art=%d'%(len(controllers),len(art)))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--package',action='store_true');parser.add_argument('--census',action='store_true');parser.add_argument('--contacts',action='store_true');parser.add_argument('--cells',action='store_true');parser.add_argument('--render',action='store_true');parser.add_argument('--check',action='store_true');parser.add_argument('--delta',action='store_true');args=parser.parse_args()
    if args.package:package_captures()
    if args.census:census()
    if args.contacts:contacts()
    if args.cells:cells()
    if args.render:render()
    if args.delta:delta()
    if args.check:raise SystemExit(check())
