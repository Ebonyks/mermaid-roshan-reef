from pathlib import Path
import argparse, collections, copy, functools, hashlib, io, json, re, subprocess, contextlib, xml.etree.ElementTree as ET
from PIL import Image

PACKET = Path(__file__).resolve().parent
ROOT = PACKET.parents[2]
BASE = '92c9fe70319ef46bfaa8f61348a6f51512141ec3'
SCHEMA = 'reef.flat_vector_audit/1'
ART_EXT = {'.png','.webp','.jpg','.jpeg','.svg','.tga','.avif'}
PRIMITIVE = re.compile(r'\b(draw_(?:rect|circle|arc|line|polyline|polygon|colored_polygon|multiline|primitive|style_box))\s*\(|\b(Polygon2D|Line2D|ColorRect|StyleBoxFlat|GradientTexture2D|GradientTexture1D|Image|SphereMesh|CylinderMesh|BoxMesh|PrismMesh|ImmediateMesh|ArrayMesh)\.(?:new|create)\s*\(')
FUNC = re.compile(r'^(\s*)(?:static )?func\s+(\w+)\(')
CLASS = re.compile(r'^(\s*)class\s+(\w+)')
RES = re.compile(r'[\"\'](res://[^\"\'\n]+)[\"\']')
FILE = re.compile(r'[\"\']([^\"\'\n/]+\.(?:png|webp|jpg|jpeg|svg|tga))[\"\']',re.I)


def write(name,data):
    (PACKET/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf8', newline='\n')


def sha(data): return hashlib.sha256(data).hexdigest()

@functools.lru_cache(maxsize=None)
def file_sha(path): return sha(path.read_bytes())


@functools.lru_cache(maxsize=None)
def text_sha(path): return sha(path.read_bytes().replace(b'\r\n',b'\n'))

@functools.lru_cache(maxsize=None)
def git(*args): return subprocess.check_output(['git',*args],cwd=ROOT)

def line_refs(path, needle):
    return [i for i,l in enumerate((ROOT/path).read_text(encoding='utf-8-sig').splitlines(),1) if needle in l]


def excluded(path):
    return bool(re.search(r'(?:^|/)(?:probe[^/]*|debug[^/]*|[^/]*test_case|[^/]*test_checks)\.gd$',path) or '/vendor/' in path)


def collect():
    paths = git('ls-tree','-r','--name-only',BASE).decode('utf8').splitlines()
    script_paths = [p for p in paths if p.startswith('scripts/') and p.endswith('.gd')]
    sources = {}
    for p in script_paths:
        sources[p] = (ROOT/p).read_text(encoding='utf-8-sig').replace('\r\n','\n')
    classes = {}
    for p,src in sources.items():
        m = re.search(r'^class_name\s+(\w+)',src,re.M)
        if m: classes[m[1]] = p
    production = [p for p in script_paths if not excluded(p)]
    edges = collections.defaultdict(set)
    for p in production:
        src = sources[p]
        for match in RES.finditer(src):
            q=match[1][6:]
            if q in production: edges[p].add(q)
        for name,q in classes.items():
            if q != p and q in production and re.search(r'\b'+re.escape(name)+r'\b',src): edges[p].add(q)
    reached = {'scripts/main.gd'}
    while True:
        new = reached | {q for p in reached for q in edges[p]}
        if reached == new: break
        reached = new
    inventory, scopes, sites, glyphs, dynamic, fallback, assets_by_name = [],[],[],[],[],[],collections.defaultdict(list)
    asset_paths=[p for p in paths if p.startswith(('assets/','assets_src/')) and Path(p).suffix.lower() in ART_EXT]
    for p in asset_paths: assets_by_name[Path(p).name].append(p)
    consumers=collections.defaultdict(list)
    for p in production:
        src=sources[p]; lines=src.splitlines()
        contexts=[]; current='FILE_SCOPE'; class_stack=[]; functions={}
        for i,l in enumerate(lines,1):
            c=CLASS.match(l)
            if c:
                level=len(c[1]); class_stack=[v for v in class_stack if v[0]<level]; class_stack.append((level,c[2]))
            f=FUNC.match(l)
            if f:
                level=len(f[1]); class_stack=[v for v in class_stack if v[0]<level]
                current='.'.join([v[1] for v in class_stack]+[f[2]])
                functions.setdefault(current,{'name':f[2],'start':i,'end':len(lines),'hits':[]})
                for q,v in functions.items():
                    if q!=current and v['end']==len(lines) and v['start']<i: v['end']=i-1
            for m in PRIMITIVE.finditer(l.split('#',1)[0]):
                kind=m[1] or m[2]+'.new/create'
                site={'id':'FVS-'+sha((p+'|'+current+'|'+str(i)+'|'+str(m.start())).encode())[:12].upper(),'path':p,'line':i,'scope':current,'kind':kind,'source':l.strip(),'evidence':'SOURCE_INSPECTION','visible_piece_count':None}
                sites.append(site)
                if current in functions: functions[current]['hits'].append(site['id'])
            for m in RES.finditer(l):
                q=m[1][6:]
                if Path(q).suffix.lower() in ART_EXT:
                    consumers[q].append({'path':p,'line':i,'scope':current,'binding':'literal_res_path'})
                elif '%' in q or '+' in l or q.endswith('/'):
                    dynamic.append({'path':p,'line':i,'scope':current,'expression':l.strip(),'disposition':'DYNAMIC_BINDING_REQUIRES_RUNTIME_ENUMERATION'})
            for m in FILE.finditer(l):
                for q in assets_by_name[m[1]]:
                    if not any(c['path']==p and c['line']==i for c in consumers[q]):
                        consumers[q].append({'path':p,'line':i,'scope':current,'binding':'filename_match_candidate','ambiguous':len(assets_by_name[m[1]])>1})
            if ('fallback' in l.lower() or 'fail-safe' in l.lower()) and not l.lstrip().startswith('#'):
                fallback.append({'path':p,'line':i,'scope':current,'source':l.strip(),'status':'NEEDS_CONTEXT_REVIEW'})
            if any(ord(ch)>0x2500 for ch in l) and ('"' in l or "'" in l) and not l.lstrip().startswith('#'):
                tokens=[]
                for m in re.finditer(r'\"([^\"\n]*)\"|\x27([^\x27\n]*)\x27',l):
                    value=m[1] or m[2] or ''
                    if any(ord(ch)>0x2500 for ch in value): tokens.append(value)
                if tokens: glyphs.append({'id':'FVG-'+sha((p+'|'+str(i)).encode())[:12].upper(),'path':p,'line':i,'scope':current,'strings':tokens,'disposition':'NEEDS_CONTEXT_REVIEW','note':'Pictogram/emoji or typography candidate. Ordinary text and engine glyph rendering are functional; object/reward icons remain art candidates.'})
        fn_scopes=[]
        for q,v in functions.items():
            if not v['hits']: continue
            entry={'id':'FVF-'+sha((p+'|'+q).encode())[:12].upper(),'path':p,'scope':q,'start_line':v['start'],'end_line':v['end'],'primitive_site_ids':v['hits'],'source_sha256_lf':sha(src.encode()),'reachability':'POTENTIALLY_MAIN_REFERENCED' if p in reached else 'STANDALONE_OR_UNPROVED','status':'NEEDS_CONTEXT_REVIEW','count_unit':'source_function_scope_not_art_piece','individual_piece_count':None,'screen_coverage':None,'required_action':'Trace guard and actual caller, enumerate named visual objects/states in phone-size current Mobile captures; split loops/helper scopes before accepting a piece total.'}
            scopes.append(entry);fn_scopes.append(entry['id'])
        inventory.append({'path':p,'source_sha256_lf':sha(src.encode()),'lines':len(lines),'class_name':next((n for n,q in classes.items() if q==p),None),'reachability':'POTENTIALLY_MAIN_REFERENCED' if p in reached else 'STANDALONE_OR_UNPROVED','primitive_sites':sum(len(v['hits']) for v in functions.values()),'source_scope_ids':fn_scopes,'script_dependencies':sorted(edges[p]),'visual_review':'NOT_CURRENTLY_CAPTURED'})
    assets=[]
    for p in asset_paths:
        f=ROOT/p; data=f.read_bytes(); row={'path':p,'sha256':sha(data),'bytes':len(data),'inventory_role':'runtime_asset' if p.startswith('assets/') else 'source_master_or_review','protected_original':p.startswith(('assets/book/','assets/characters/friends/')),'consumers':consumers[p],'runtime_reachability':'LITERAL_REFERENCE' if any(x['binding']=='literal_res_path' for x in consumers[p]) else ('FILENAME_CANDIDATE' if consumers[p] else 'NO_STATIC_LITERAL_CONSUMER_PROVED'),'visual_disposition':'NEEDS_CONTEXT_REVIEW','origin_method':'PROVENANCE_NOT_YET_DISPOSITIONED','dimensions':None,'mode':None}
        try:
            if f.suffix.lower()=='.svg':
                el=ET.fromstring(data); row['svg_attributes']={k:el.attrib[k] for k in ('width','height','viewBox') if k in el.attrib};row['mode']='vector_xml'
            else:
                with Image.open(f) as im: row['dimensions']=list(im.size);row['mode']=im.mode
        except Exception as exc: row['metadata_error']=type(exc).__name__
        assets.append(row)
    scene_nodes=[]
    for p in paths:
        if p.startswith('scenes/') and p.endswith('.tscn'):
            for i,l in enumerate((ROOT/p).read_text(encoding='utf-8-sig').splitlines(),1):
                if re.search(r'type="(?:Polygon2D|Line2D|ColorRect|MeshInstance3D|Sprite3D|Label3D)"',l):
                    scene_nodes.append({'path':p,'line':i,'node':l,'status':'NEEDS_CONTEXT_REVIEW'})
    producers=[]
    for p in paths:
        if p.startswith('tools/') and Path(p).suffix in {'.py','.gd'} and '/tests/' not in p:
            src=(ROOT/p).read_text(encoding='utf-8-sig',errors='replace')
            if re.search(r'ImageDraw|<svg|\.svg|draw_colored_polygon|draw_polygon|Image\.create|\.polygon\(|\.ellipse\(',src):
                producers.append({'path':p,'sha256_lf':sha(src.replace('\r\n','\n').encode()),'role':'generator_or_validator_candidate','art_production_proved':False,'note':'Retire any obsolete output generator only after its callers and accepted alternative are verified. A validator referencing SVG is not automatically a producer.'})
    shards=[]
    for i in range(0,len(assets),500):
        name='source_images_%02d.json' % (i//500)
        write(name,{'schema':SCHEMA,'baseline':BASE,'images':assets[i:i+500]})
        shards.append({'path':name,'image_records':len(assets[i:i+500])})
    write('source_inventory.json',{'schema':SCHEMA,'baseline':BASE,'scripts':inventory,'image_shards':shards,'image_count':len(assets),'scene_visual_nodes':scene_nodes,'art_producer_candidates':producers,'coverage_limit':'All Git-declared script and image paths at baseline. Ignored/import/export-only local artifacts are not in this Git inventory; supplied baseline scan is checked separately. Static class/type mentions overapproximate reachability; dynamic resource bindings remain open.'})
    write('source_scopes.json',{'schema':SCHEMA,'baseline':BASE,'scopes':scopes,'count_unit':'source_function_scope_not_individual_art'})
    write('primitive_sites.json',{'schema':SCHEMA,'baseline':BASE,'sites':sites,'count_unit':'source_call_site_not_individual_art'})
    write('glyph_inventory.json',{'schema':SCHEMA,'baseline':BASE,'sites':glyphs})
    write('dynamic_bindings.json',{'schema':SCHEMA,'baseline':BASE,'bindings':dynamic,'fallback_mentions':fallback,'note':'This is an overinclusive expression inventory. Neither string roots nor source mentions prove current draw-path visibility.'})
    print('COLLECT',len(production),'scripts',len(assets),'images',len(scopes),'scopes',len(sites),'candidate calls',len(glyphs),'glyph rows')


def check(data=None):
    issues=[]
    if data is None: data={p.stem:json.loads(p.read_text(encoding='utf-8-sig')) for p in PACKET.glob('*.json') if p.name not in {'MANIFEST.json','REMOTE_VERIFICATION.json'}}
    ids=[]
    for r in data['per_piece']['pieces']:
        ids.append(r['id'])
        if not r['source']['sha256'] or not (ROOT/r['source']['path']).is_file(): issues.append('unresolved piece source '+r['id'])
        f=ROOT/r['source']['path']; actual=text_sha(f) if f.suffix in {'.gd','.py','.md','.tscn'} else file_sha(f)
        if actual!=r['source']['sha256']: issues.append('source drift '+r['id'])
        if r['status']=='ACCEPTED_REMOVED' and not all(r['acceptance_evidence'].values()): issues.append('false accepted removal '+r['id'])
        if r['status'] not in data['tally']['status_lanes']: issues.append('unknown status '+r['id'])
        if r['count_unit']!='named_art_role_state_family': issues.append('wrong piece unit '+r['id'])
    if len(ids)!=len(set(ids)): issues.append('duplicate FV IDs')
    if data['tally']['named_piece_records']!=len(ids): issues.append('tally mismatch')
    if data['tally']['accepted_removed']!=sum(r['status']=='ACCEPTED_REMOVED' for r in data['per_piece']['pieces']): issues.append('accepted tally mismatch')
    if set(data['per_piece']['context_brief_ids'])-set(x['id'] for x in data['contextual_briefs']['briefs']): issues.append('missing context brief')
    for f in data['source_inventory']['scripts']:
        if text_sha(ROOT/f['path'])!=f['source_sha256_lf']: issues.append('script hash drift '+f['path'])
    supplemental=data['vector_source_scan']
    if supplemental['baseline']!=BASE: issues.append('supplement baseline drift')
    for f in supplemental['scripts']:
        if text_sha(ROOT/f['path'])!=f['sha256_git_blob_bytes']: issues.append('supplement source drift '+f['path'])
        lines=(ROOT/f['path']).read_text(encoding='utf-8-sig').splitlines()
        for h in f['hits']:
            if lines[h['line']-1].strip()!=h['source']: issues.append('supplement source line drift '+f['path'])
    if sum(f['matches'] for f in supplemental['scripts'])!=supplemental['candidate_primitive_call_sites']: issues.append('supplement call count mismatch')
    for row in data['contact_index']['images']:
        if file_sha(PACKET/row['packet_path'])!=row['sha256']: issues.append('contact hash drift '+row['packet_path'])
    # One complete, source-bound brief for each named role/state family.
    pieces=data['per_piece']['pieces']; briefs=data['per_piece_briefs']['briefs']; tally=data['tally']
    if len(briefs)!=len(pieces) or len({b['id'] for b in briefs})!=len(briefs): issues.append('individual brief total/ID mismatch')
    by_brief={b['id']:b for b in briefs}; scope_ids={s['id'] for s in data['source_scopes']['scopes']}
    for r in pieces:
        b=by_brief.get(r.get('individual_brief_id'))
        if not b or b['piece_id']!=r['id'] or b['parent_brief_id']!=r['context_brief_id']: issues.append('missing or wrong individual brief '+r['id']); continue
        for key in ('scene_route','action_state','proposed_update','palette','material','lighting','scale_perspective','support_contact_occlusion','required_states','output_layer','missing_evidence'):
            if not b.get(key): issues.append('missing individual context '+r['id']+' '+key)
        if b['route_refs']!=r['route_refs'] or not r['route_refs']: issues.append('piece route mismatch '+r['id'])
        if set(r['source_scope_ids'])-scope_ids: issues.append('unknown source scope '+r['id'])
        if r['source']['path'].endswith('.gd'):
            lines=(ROOT/r['source']['path']).read_text(encoding='utf-8-sig').splitlines()
            if not 1<=r['source']['start_line']<=r['source']['end_line']<=len(lines): issues.append('invalid source range '+r['id'])
    counts=dict(collections.Counter(r['status'] for r in pieces))
    if counts!=tally['named_status_counts']: issues.append('status tally mismatch')
    expected={'named_family_count':len({r['family'] for r in pieces}),'source_script_count':len(data['source_inventory']['scripts']),'source_function_scopes':len(data['source_scopes']['scopes']),'primitive_candidate_call_sites':len(data['primitive_sites']['sites']),'glyph_candidate_rows':len(data['glyph_inventory']['sites']),'route_entries':len(data['scene_coverage']['entries']),'unreviewed_current_route_entries':sum(r['capture_status']=='COVERAGE_GAP' for r in data['scene_coverage']['entries'])}
    for key,count in expected.items():
        if tally[key]!=count: issues.append('census tally mismatch '+key)
    actual_accepted=sum(r['status']=='ACCEPTED_REMOVED' for r in pieces)
    for key,allowed in {'integrated':{'INTEGRATED','RUNTIME_VERIFIED','DEVICE_CHILD_OWNER_PENDING','ACCEPTED_REMOVED'},'runtime_verified':{'RUNTIME_VERIFIED','DEVICE_CHILD_OWNER_PENDING','ACCEPTED_REMOVED'}}.items():
        if tally[key]!=sum(r['status'] in allowed for r in pieces): issues.append('unsupported '+key+' tally')
    if tally['replaced']!=sum(r['status'] in {'INTEGRATED','RUNTIME_VERIFIED','DEVICE_CHILD_OWNER_PENDING','ACCEPTED_REMOVED'} for r in pieces): issues.append('unsupported replaced tally')
    non_removal={'VERIFIED_NOT_FLAT_VECTOR_ART','EXEMPT_FUNCTIONAL','INACTIVE_ARCHIVE'}
    resolved_without_removal=sum(r['status'] in non_removal for r in pieces)
    if tally['named_resolved_without_replacement']!=resolved_without_removal: issues.append('unsupported non-removal disposition tally')
    for r in pieces:
        if r['status'] in non_removal and not all(r.get('disposition_evidence',{}).get(k) for k in ('reason','exact_source_and_guard_trace','current_visibility_review','reviewer','check_time')): issues.append('unsupported non-removal disposition '+r['id'])
    if tally['remaining_named_design_records']!=len(pieces)-actual_accepted-resolved_without_removal: issues.append('remaining tally mismatch')
    image_rows=[]
    for shard in data['source_inventory']['image_shards']:
        payload=data[Path(shard['path']).stem]
        if payload['baseline']!=BASE or len(payload['images'])!=shard['image_records']: issues.append('image shard mismatch '+shard['path'])
        image_rows.extend(payload['images'])
    if len(image_rows)!=data['source_inventory']['image_count'] or len(image_rows)!=tally['source_image_count']: issues.append('image census mismatch')
    if len({r['path'] for r in image_rows})!=len(image_rows): issues.append('duplicate source image')
    for r in image_rows:
        f=ROOT/r['path']
        if not f.is_file() or file_sha(f)!=r['sha256'] or f.stat().st_size!=r['bytes']: issues.append('source image drift '+r['path'])
    blob_hashes={}
    for name in ('context_review_observations','garden_context_review'):
        if data[name]['baseline']!=BASE: issues.append('observation baseline drift '+name)
        for r in data[name]['observations']:
            for path,digest in r.get('source_sha256_git_blob_bytes',{}).items():
                if path not in blob_hashes: blob_hashes[path]=sha(git('show',BASE+':'+path))
                if blob_hashes[path]!=digest: issues.append('observation Git blob drift '+path)
    for r in data['contact_index']['images']:
        f=ROOT/r['source_path']
        if not f.is_file() or file_sha(f)!=r['source_sha256']: issues.append('contact source drift '+r['source_path'])
        if r['packet_path'].endswith('.svg') and (PACKET/r['packet_path']).read_bytes()!=f.read_bytes(): issues.append('changed SVG reference copy '+r['packet_path'])
    if 'weak' in ' '.join(tally['zero_acceptance_criteria']).lower(): issues.append('completion scope narrowed by quality qualifier')
    print('FLATVECTOR|RESULT|'+('ALL OK' if not issues else str(len(issues))+' ISSUE(S)'))
    for issue in issues: print('FLATVECTOR|FAIL|'+issue)
    return int(bool(issues))


def stress():
    data={p.stem:json.loads(p.read_text(encoding='utf-8-sig')) for p in PACKET.glob('*.json') if p.name not in {'MANIFEST.json','REMOTE_VERIFICATION.json'}}
    if check(data): return 1
    mutations=[('false functional exemption',lambda d:d['per_piece']['pieces'][0].update(status='EXEMPT_FUNCTIONAL')),('false accepted removal',lambda d:d['per_piece']['pieces'][0].update(status='ACCEPTED_REMOVED')),('missing individual brief',lambda d:d['per_piece_briefs']['briefs'].pop()),('source image hash drift',lambda d:d['source_images_00']['images'][0].update(sha256='0'*64)),('wrong named total',lambda d:d['tally'].update(named_piece_records=1)),('wrong route binding',lambda d:d['per_piece_briefs']['briefs'][0].update(route_refs=['not_a_real_route'])),('narrowed completion criterion',lambda d:d['tally']['zero_acceptance_criteria'].append('Only weak art needs replacement'))]
    passed=0
    for name,mutate in mutations:
        candidate=copy.deepcopy(data); mutate(candidate)
        with contextlib.redirect_stdout(io.StringIO()): result=check(candidate)
        if not result: print('FLATVECTOR|STRESS|FAIL|accepted '+name);return 1
        passed+=1
    print('FLATVECTOR|STRESS|'+str(passed)+'/'+str(len(mutations))+' falsification cases ALL OK')
    return 0


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--collect',action='store_true');parser.add_argument('--check',action='store_true');parser.add_argument('--stress',action='store_true');args=parser.parse_args()
    if args.collect: collect()
    elif args.stress: raise SystemExit(stress())
    else: raise SystemExit(check())
