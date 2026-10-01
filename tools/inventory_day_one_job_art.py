"""Read-only, explicitly conservative Day One artwork and drawing-source census."""
from pathlib import Path
import fnmatch,hashlib,html,io,json,re,subprocess
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'audit/day_one_job_art_census_20261001'
NAMES=['scripts/day_one_director.gd','scripts/day_one_contact_action_2d.gd',
       'scripts/day_one_art_studio.gd','scripts/arena/day_one_castle_dressing.gd',
       'scripts/arena/castle_rooms_25d.gd','scripts/arena/castle_fixture_rigs.gd',
       'scripts/dust_bunny_sprite.gd','scripts/dust_bunny_boss_sprite.gd',
       'scripts/dust_boss_telegraph_2d.gd','scripts/dust_boss_lesson_2d.gd']

def digest(raw):return hashlib.sha256(raw).hexdigest()

def main():
    if (OUT/'MANIFEST.json').exists():raise SystemExit('Sealed census; use a new revision')
    revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    tracked=subprocess.check_output(['git','ls-tree','-r','--name-only',revision],cwd=ROOT,text=True).splitlines()
    names=set(NAMES)|{n for n in tracked if n.startswith(('scripts/games/day_one_','scripts/games/pool_','scripts/games/stuffie','scripts/games/dust_boss')) and n.endswith('.gd')}
    pending=list(names);sources={}
    while pending:
        name=pending.pop()
        if name in sources:continue
        path=ROOT/name
        raw=path.read_bytes() if path.is_file() else subprocess.check_output(['git','show',revision+':'+name],cwd=ROOT)
        sources[name]=raw
        for dep in re.findall(r'res://(scripts/[^"\s]+\.gd)',raw.decode('utf-8')):
            if dep in tracked and dep!='scripts/main.gd' and dep not in sources:pending.append(dep)
    assets={};unresolved=[];drawings=[]
    for name,raw in sorted(sources.items()):
        text=raw.decode('utf-8')
        for match in re.finditer(r'res://(assets/[^"\s]+\.(?:png|webp|jpg|jpeg|svg))',text):
            reference=match.group(1);line=text.count('\n',0,match.start())+1
            mode='literal';matches=[reference] if reference in tracked else []
            if not matches and '%' in reference:
                pattern=re.sub(r'%[0-9.]*[sdf]','*',reference)
                matches=[n for n in tracked if fnmatch.fnmatchcase(n,pattern)]
                mode='conservative dynamic-template candidate; actual substitution/draw pending'
            if not matches:unresolved.append({'source':name,'line':line,'reference':reference});continue
            for candidate in matches:assets.setdefault(candidate,[]).append({'source':name,'line':line,'reference':reference,'mode':mode})
        functions=list(re.finditer(r'^func ([\w]+)\([^\n]*',text,re.M))
        for i,match in enumerate(functions):
            body=text[match.start():functions[i+1].start() if i+1<len(functions) else len(text)]
            if re.search(r'draw_|Sprite2D|TextureRect|Line2D|Polygon2D|SpriteSheetAnim|AtlasTexture',body):
                drawings.append({'source':name,'function':match.group(1),'line':text.count('\n',0,match.start())+1,
                                 'normalized_function_sha256':digest(body.replace('\r\n','\n').encode()),'visual_score':None,'review':'PENDING native played/context review'})
    process=subprocess.Popen(['git','cat-file','--batch'],cwd=ROOT,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
    items=[]
    prior={r['path']:r for r in json.loads((ROOT/'audit/day2_job_contexts_2026-09-30/inventory.json').read_text())['items']}
    prior_extra=json.loads((ROOT/'audit/day2_job_contexts_2026-09-30/reviews.json').read_text())['assets']
    current_reviews=json.loads((OUT/'reviews.json').read_text(encoding='utf-8')) if (OUT/'reviews.json').is_file() else {'items':{},'atlas_cells':[]}
    for i,(name,consumers) in enumerate(sorted(assets.items()),1):
        path=ROOT/name
        if path.is_file():raw=path.read_bytes();origin='Current local file'
        else:
            process.stdin.write((revision+':'+name+'\n').encode());process.stdin.flush()
            header=process.stdout.readline().decode().split();assert len(header)==3 and header[1]=='blob'
            raw=process.stdout.read(int(header[2]));assert process.stdout.read(1)==b'\n';origin='Exact recorded Git revision'
        dimensions=None
        if not name.endswith('.svg'):
            with Image.open(io.BytesIO(raw)) as image:dimensions=list(image.size)
        item={'id':f'D1A-{i:04}','path':name,'sha256':digest(raw),'bytes':len(raw),'dimensions':dimensions,
                      'byte_origin':origin,'consumers':consumers,'source_score':None,'mounted_score':None,
                      'priority':'UNDETERMINED_UNREVIEWED','acceptance':'Discovery only; no actual draw, mounted quality or owner acceptance'}
        old=prior.get(name)
        if old and old['sha256']==item['sha256']:
            item['source_score']=old.get('draft_source_score',prior_extra.get(old['id'],{}).get('score'))
            item['prior_source_opinion']={'id':old['id'],'revision':'9038246cf9b34005afb8bc28a2f81396930988b6',
                                         'exact_source_sha256_match':True,'lane':'Reused earlier source-only opinion; current Day One mounted/action pending'}
            if item['source_score'] is not None:
                item['priority']='SOURCE_PRIORITY_PRIOR_OPINION' if item['source_score']<=4.5 else 'PRIOR_SOURCE_ABOVE_QUEUE; CURRENT_USE_PENDING'
        opinion=current_reviews['items'].get(item['id'])
        if opinion:
            if opinion['path']!=name or opinion['sha256']!=item['sha256']:
                raise SystemExit('Source review stale: '+name+'; re-review changed bytes before rebuilding')
            item['source_score']=opinion['score']
            item['current_source_opinion']=opinion
            item['priority']='SOURCE_PRIORITY_CURRENT_OPINION' if opinion['score']<=4.5 else 'SOURCE_ABOVE_QUEUE; CURRENT_USE_PENDING'
        items.append(item)
    process.stdin.close();assert process.wait()==0
    OUT.mkdir(exist_ok=True);(OUT/'.gdignore').touch()
    data={'schema':'reef.day-one-job-art-census.v1','production_revision':revision,
          'scope':'Named Day One bathroom/pool/stuffie/art, castle dressing and contact/dust presentation; direct declared script dependencies only. Shared Main helper bodies, runtime node inspection, class-name-only/directory-fragment references, atlas cells and full played phases remain pending.',
          'sources':[{'path':n,'literal_sha256':digest(r),'normalized_lf_sha256':digest(r.replace(b'\r\n',b'\n'))} for n,r in sorted(sources.items())],
          'items':items,'drawing_functions':drawings,'unresolved_literal_or_template_references':unresolved,
          'prior_exact_source_opinions_reused':sum('prior_source_opinion' in r for r in items),
          'new_source_opinions_completed':sum('current_source_opinion' in r for r in items),
          'remaining_source_review_pending':sum(r['source_score'] is None for r in items),
          'individual_source_cells_reviewed':len(current_reviews['atlas_cells']),
          'coverage':'INCOMPLETE; scoped source opinions complete, full discovery/actual use and every current Day One played-context score pending','owner_accepted':False}
    (OUT/'inventory.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    cards=''
    for r in items:
        status='Unreviewed source · score pending' if r['source_score'] is None else f'{"Current source" if "current_source_opinion" in r else "Prior unchanged-source"} opinion: {r["source_score"]}/5 · current Day One mounted/action pending'
        review=r.get('current_source_opinion',{})
        prose=f'<p>{html.escape(review["evaluation"])}</p><p><strong>Next review:</strong> {html.escape(review["next_review_or_refinement"])}</p>' if review else '<p>Reuse attributed to the earlier sealed source opinion; no new mounted/action pass.</p>'
        cards+=f'<article id="{r["id"]}"><h2>{r["id"]}</h2><a href="../../{html.escape(r["path"])}"><img loading="lazy" src="../../{html.escape(r["path"])}" alt="{html.escape(r["path"])}"></a><p><code>{html.escape(r["path"])}</code></p><strong>{status}</strong>{prose}<p>{len(r["consumers"])} source-reference sites; actual drawing/phase use pending.</p></article>'
    cells=''
    by_id={r['id']:r for r in items}
    for cell in current_reviews['atlas_cells']:
        parent=by_id[cell['parent']]; x,y,w,h=cell['source_rect']; iw,ih=parent['dimensions']; factor=200/w
        crop=f'<div class="cell" style="height:{h*factor}px"><img loading="lazy" src="../../{html.escape(parent["path"])}" alt="{html.escape(cell["label"])}" style="width:{iw*factor}px;height:{ih*factor}px;left:{-x*factor}px;top:{-y*factor}px"></div>'
        cells+=f'<article id="{cell["id"]}"><h2>{html.escape(cell["label"])}</h2>{crop}<strong>Source-cell opinion: {cell["score"]}/5</strong><p>{html.escape(cell["evaluation"])}</p><p>Source window {cell["source_rect"]}; actual timing, contact and mounted review pending.</p></article>'
    css='body{font:16px/1.6 system-ui;background:#eef5ff;color:#29324f;margin:0}main{max-width:1180px;margin:auto;padding:24px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:16px}article{background:white;padding:18px;border-radius:16px}img{width:100%;height:260px;object-fit:contain;background:#d6e2ed}code{overflow-wrap:anywhere}.cell{position:relative;width:200px;overflow:hidden;background:#d6e2ed}.cell img{position:absolute;max-width:none;object-fit:fill;background:none}'
    (OUT/'index.html').write_text(f'<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Day One job-art discovery and source reviews</title><style>{css}</style><main><h1>Day One job-art discovery and source reviews</h1><p>Additional read-only coverage for the all-job-days goal: {len(items)} discovered artwork files, {len(sources)} scoped/dependency scripts and {len(drawings)} drawing-related functions. {data["new_source_opinions_completed"]} new native-source opinions and{data["prior_exact_source_opinions_reused"]} earlier byte-identical source opinions are recorded, plus{len(current_reviews["atlas_cells"])} individual source cells. This is an unfinished whole-Day-One census. Discovered references and good source scores do not prove actual drawing or a played action.</p><p>Bathroom, pool, stuffie and art activities plus shared castle/contact/dust presentation are inventoried. Dynamic/class-only references, shared Main helpers, remaining atlas pose cells, all played stages and contact scoring remain open. Existing story clips and protected originals are preserved. Technical water inputs have explicitly technical opinions, not painted-prop acceptance.</p><p><a href="inventory.json">Exact source hashes, consumers, functions and unresolved references</a> · <a href="reviews.json">Written source and cell opinions</a> · <a href="../job_artwork_refinement_live/index.html">All-jobs live entry</a></p><div class="grid">{cards}</div><h2>Individual source atlas cells</h2><p>These exact source windows show artwork only. No interpolation or temporal acceptance is inferred.</p><div class="grid">{cells}</div></main></html>\n',encoding='utf-8')
    print(f'DAY_ONE_ART_CENSUS|DISCOVERED|sources={len(sources)}|images={len(items)}|drawings={len(drawings)}|unresolved={len(unresolved)}|quality review pending')

if __name__=='__main__':main()
