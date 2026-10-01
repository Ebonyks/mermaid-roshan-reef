"""Read-only expanded Day One source graph; potential references are not actual use."""
from pathlib import Path
import fnmatch
import hashlib
import html
import io
import json
import re
import subprocess
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'audit/day_one_job_art_census_v2_20261001'

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def main():
    assert not (OUT / 'MANIFEST.json').exists(), 'Sealed output; use a new revision'
    revision = subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    tracked = set(subprocess.check_output(['git','ls-tree','-r','--name-only',revision],cwd=ROOT,text=True).splitlines())
    batch = subprocess.Popen(['git','cat-file','--batch'],cwd=ROOT,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
    def raw(name):
        p=ROOT/name
        if p.is_file():return p.read_bytes()
        batch.stdin.write((revision+':'+name+'\n').encode());batch.stdin.flush()
        header=batch.stdout.readline().split();assert len(header)==3 and header[1]==b'blob',name
        data=batch.stdout.read(int(header[2]));assert batch.stdout.read(1)==b'\n';return data
    scripts={n:raw(n).decode('utf-8') for n in sorted(tracked) if n.startswith('scripts/') and n.endswith('.gd') and not Path(n).name.startswith('probe') and '/tests/' not in n}
    classes={}
    for name,text in scripts.items():
        match=re.search(r'^class_name\s+(\w+)',text,re.M)
        if match:classes.setdefault(match[1],[]).append(name)
    prior=json.loads((ROOT/'audit/day_one_job_art_census_20261001/inventory.json').read_text())
    seeds={s['path'] for s in prior['sources']}|{n for n in scripts if Path(n).name.startswith('day_one_')}
    sources={};edges=[];pending=list(sorted(seeds));main_requests=set();main_parts={}
    main_text=scripts['scripts/main.gd'];functions=list(re.finditer(r'^func\s+(\w+)\(',main_text,re.M))
    main_functions={m.group(1):(m.start(),main_text[m.start():functions[i+1].start() if i+1<len(functions) else len(main_text)]) for i,m in enumerate(functions)}
    main_header=main_text[:functions[0].start()]
    while pending or main_requests-set(main_parts):
        while pending:
            name=pending.pop()
            if name in sources or name=='scripts/main.gd':continue
            text=scripts[name];sources[name]=text
            for dep in re.findall(r'res://(scripts/[^"\s]+\.gd)',text):
                if dep in scripts and dep!='scripts/main.gd':
                    edges.append({'from':name,'to':dep,'kind':'explicit script resource'});pending.append(dep)
            for cls in set(re.findall(r'\b([A-Z]\w*)\b',text)) & set(classes):
                if cls=='ReefMain':continue
                for dep in classes[cls]:
                    edges.append({'from':name,'to':dep,'kind':'class-name candidate; semantic/runtime use unverified','class_name':cls})
                    if dep not in sources:pending.append(dep)
            main_requests.update(re.findall(r'\bm\.(\w+)\s*\(',text))
            main_requests.update(re.findall(r'\bm\.call\(\s*"(\w+)"',text))
        for method in sorted(main_requests-set(main_parts)):
            if method not in main_functions:
                main_parts[method]=None;continue
            pos,body=main_functions[method];main_parts[method]={'line':main_text.count('\n',0,pos)+1,'text':body,'normalized_lf_sha256':sha(body.replace('\r\n','\n').encode())}
            main_requests.update(c for c in re.findall(r'(?<![.\w])([_a-z]\w*)\s*\(',body) if c in main_functions)
            main_requests.update(c for c in re.findall(r'(?:call_deferred|Callable)\([^\n]*?"(\w+)"',body) if c in main_functions)
            for cls in set(re.findall(r'\b([A-Z]\w*)\b',body)) & set(classes):
                if cls=='ReefMain':continue
                for dep in classes[cls]:
                    edges.append({'from':'scripts/main.gd::'+method,'to':dep,'kind':'shared Main callback class candidate; actual job use unverified'})
                    if dep not in sources:pending.append(dep)
    sources['scripts/main.gd']=main_header+'\n'.join(v['text'] for v in main_parts.values() if v)
    images=sorted(n for n in tracked if n.startswith('assets/') and Path(n).suffix.lower() in ['.png','.jpg','.jpeg','.webp','.svg'])
    image_set=set(images);assets={};unresolved=[];drawing=[];directory_fragments=[]
    for name,text in sorted(sources.items()):
        bases=set(re.findall(r'"(res://assets/[^"\n]*/)["\s]',text))
        # Resolve only literal string/constant concatenations; never execute GDScript.
        expressions={}
        lines=text.splitlines()
        for index,line in enumerate(lines):
            match=re.match(r'^const\s+(\w+)(?:\s*:\s*[^=]+)?\s*(?::=|=)\s*(.*)$',line)
            if not match:continue
            expression=match.group(2)
            next_line=index+1
            while expression.rstrip().endswith('\\') and next_line<len(lines):
                expression=expression.rstrip()[:-1]+lines[next_line].strip();next_line+=1
            expressions[match.group(1)]=expression
        resolved={}
        for _pass in range(len(expressions)+1):
            changed=False
            for constant,expression in expressions.items():
                if constant in resolved:continue
                parts=re.split(r'\s*\+\s*',expression.strip())
                if not parts or not all(re.fullmatch(r'"[^"\n]*"|[A-Z_][A-Z_0-9]*',p) for p in parts):continue
                if not all(p.startswith('"') or p in resolved for p in parts):continue
                resolved[constant]=''.join(p[1:-1] if p.startswith('"') else resolved[p] for p in parts);changed=True
            if not changed:break
        bases.update(v for v in resolved.values() if v.startswith('res://assets/') and v.endswith('/'))
        literals=list(re.finditer(r'"([^"\n]+\.(?:png|jpg|jpeg|webp|svg))"',text))
        for m in literals:
            value=m.group(1);line=text.count('\n',0,m.start())+1
            candidates=[];kind=''
            if value.startswith('res://'):
                pattern=re.sub(r'%[0-9.]*[sdf]','*',value.removeprefix('res://'))
                candidates=[n for n in images if fnmatch.fnmatchcase(n,pattern)]
                kind='literal resource' if '%' not in value else 'dynamic-template candidate; substitution unverified'
            else:
                for base in bases:
                    pattern=re.sub(r'%[0-9.]*[sdf]','*',base.removeprefix('res://')+value)
                    candidates.extend(n for n in images if fnmatch.fnmatchcase(n,pattern))
                kind='directory/filename-fragment candidate; actual binding unverified'
            candidates=sorted(set(candidates))
            if not candidates:
                unresolved.append({'source':name,'line_in_scoped_text':line,'fragment':value,'reason':'No exact or declared-directory match; concatenation/runtime dictionary substitution needs review'})
            else:
                for candidate in candidates:assets.setdefault(candidate,[]).append({'source':name,'line_in_scoped_text':line,'reference':value,'mode':kind,'scope':'Named scoped source' if name in seeds else 'Shared dependency candidate; may be outside Day One jobs'})
            if not value.startswith('res://'):directory_fragments.append({'source':name,'fragment':value,'candidate_count':len(candidates)})
        fn=list(re.finditer(r'^func\s+(\w+)\(',text,re.M))
        for i,m in enumerate(fn):
            body=text[m.start():fn[i+1].start() if i+1<len(fn) else len(text)]
            if re.search(r'draw_|Sprite2D|Sprite3D|TextureRect|Line2D|Polygon2D|AtlasTexture|SpriteSheetAnim',body):drawing.append({'source':name,'function':m.group(1),'normalized_lf_sha256':sha(body.replace('\r\n','\n').encode()),'actual_use':'PENDING native context/played route','visual_score':None})
    earlier={x['path']:x for x in prior['items']}
    day2=json.loads((ROOT/'audit/day2_job_contexts_2026-09-30/inventory.json').read_text())
    earlier.update({x['path']:x for x in day2['items'] if x['path'] not in earlier})
    items=[]
    for i,(name,consumers) in enumerate(sorted(assets.items()),1):
        data=raw(name);dims=None
        if Path(name).suffix!='.svg':
            with Image.open(io.BytesIO(data)) as im:dims=list(im.size)
        item={'id':f'D1V2-{i:04}','path':name,'sha256':sha(data),'bytes':len(data),'dimensions':dims,'consumers':consumers,'source_score':None,'actual_draw':'UNVERIFIED','mounted_score':None,'action_score':None}
        old=earlier.get(name)
        if old and old['sha256']==item['sha256']:
            item['source_score']=old.get('source_score',old.get('draft_source_score'))
            item['prior_opinion']={'id':old['id'],'source_sha256_matches':True,'archive':'audit/day_one_job_art_census_20261001' if name in {x['path'] for x in prior['items']} else 'audit/day2_job_contexts_2026-09-30','qualification':'Exact-byte source-only opinion; no new actual-use/mounted/action acceptance.'}
        item['priority']='UNREVIEWED_SOURCE' if item['source_score'] is None else ('PRIOR_SOURCE_PRIORITY' if item['source_score']<=4.5 else 'PRIOR_SOURCE_ABOVE_QUEUE; USE_PENDING')
        items.append(item)
    inventory={'schema':'reef.day-one-expanded-source-census.v2','production_revision':revision,'scope':'Conservative class-name/Main-callback/directory-fragment discovery supplement. Shared source graphs include possible non-job branches; references do not prove drawing. This does not complete the actual-use or played-action audit.','seed_sources':sorted(seeds),'sources':[{'path':n,'whole_source_sha256':sha(raw(n)),'scoped_text_normalized_lf_sha256':sha(t.replace('\r\n','\n').encode())} for n,t in sorted(sources.items())],'class_dependency_edges':edges,'shared_main_methods':[{'name':n,**{k:v for k,v in d.items() if k!='text'}} for n,d in sorted(main_parts.items()) if d],'unresolved_main_method_names':sorted(n for n,v in main_parts.items() if not v),'items':items,'drawing_functions':drawing,'directory_fragment_candidates':directory_fragments,'unresolved_image_fragments':unresolved,'new_source_candidates':sum(x['path'] not in {y['path'] for y in prior['items']} for x in items),'remaining_new_source_opinions':sum(x['source_score'] is None for x in items),'actual_use_complete':False,'owner_accepted':False}
    OUT.mkdir(exist_ok=True);(OUT/'.gdignore').touch();(OUT/'inventory.json').write_text(json.dumps(inventory,indent=2)+'\n',encoding='utf-8')
    cards=[]
    for x in items:
        score='Unreviewed source' if x['source_score'] is None else f'Earlier exact-byte source opinion {x["source_score"]}/5'
        cards.append(f'<article id="{x["id"]}"><h2>{x["id"]}</h2><img loading="lazy" src="../../{html.escape(x["path"])}" alt="{html.escape(x["path"])}"><code>{html.escape(x["path"])}</code><p>{score}. Actual drawing, mounted quality and action review pending.</p><p>{len(x["consumers"])} declared/candidate reference sites; shared dependency branches may be outside the Day One jobs.</p></article>')
    css='body{margin:0;background:#eef5ff;color:#26304e;font:16px/1.6 system-ui}main{max-width:1200px;margin:auto;padding:24px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px}article{background:white;border-radius:16px;padding:18px}img{width:100%;height:250px;object-fit:contain;background:#dce7ef}code{overflow-wrap:anywhere}h2{font-size:18px}'
    (OUT/'index.html').write_text(f'<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Expanded Day One source discovery</title><style>{css}</style><main><h1>Expanded Day One source discovery</h1><p>{len(items)} conservative image candidates from {len(sources)} source scopes, {len(inventory["shared_main_methods"])} shared Main methods and {len(drawing)} drawing-related functions. {inventory["new_source_candidates"]} image candidates are additional to the earlier48-image census; {inventory["remaining_new_source_opinions"]} source opinions remain pending. This is a discovery supplement, not an actual-use or whole-jobs pass.</p><p>Class references, Main callbacks and directory/filename fragments expose assets omitted by direct full-path searches. Shared dispatch branches may include other areas. Every reused source score requires an exact SHA match. Dynamic substitutions, dictionary bindings, all native played contexts, remaining atlas cells and individual weak-object refinement remain open.</p><p><a href="inventory.json">Exact graph, references, hashes and unresolved expressions</a> · <a href="../day_one_job_art_census_20261001/index.html">Earlier individual source and30-cell opinions</a> · <a href="../job_artwork_refinement_live/index.html">All-jobs live entry</a></p><div class="grid">{"".join(cards)}</div></main></html>\n',encoding='utf-8')
    batch.stdin.close();assert batch.wait()==0
    print(f'DAY_ONE_EXPANDED|sources={len(sources)}|main_methods={len(inventory["shared_main_methods"])}|images={len(items)}|additional={inventory["new_source_candidates"]}|unreviewed={inventory["remaining_new_source_opinions"]}|actual-use NOT COMPLETE')

if __name__=='__main__':main()
