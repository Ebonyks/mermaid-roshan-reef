from pathlib import Path
import datetime, hashlib, json, shutil, subprocess
from PIL import Image

b = Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
q = b/'audit/job_shared_entrance_sources_v1_20261003'
assert q.exists() and not (q/'PLAN_AND_SOURCE_BOUNDARY.json').exists()
assert not (b/'design/audit_impacts/job-shared-entrance-source-review-20261003.json').exists()
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
def write(p, d):
    p.write_text(json.dumps(d, indent=2, ensure_ascii=False)+'\n', encoding='utf-8', newline='\n')
reg = json.loads((b/'audit/job_artwork_refinement_live/ALL_ITEMS.json').read_text(encoding='utf-8'))
ids = ['D2X-'+f'{n:04d}' for n in [1,2,3,4,5,6,7,10,11,24,25,26,27,28,29,30,31,140]]
items = [next(x for x in reg['items'] if x['id']==ident) for ident in ids]
assert len(items)==18 and all(x['current_source_score'] is None for x in items)
old = b/'assets_src/castle/room_backgrounds_2k/castle_live_alpha_baseline_repair.json'
contracts = [b/'assets/flats/castle/interactions_v2/castle_interactions_v2.json', b/'assets/flats/castle/interactions_v4/castle_interactions_v4.json']
def collect(d):
    result={}
    def walk(x):
        if isinstance(x,dict):
            if x.get('sheet') and x.get('grid') and x.get('frame_count'): result[x['sheet']]=x
            for v in x.values(): walk(v)
        elif isinstance(x,list):
            for v in x: walk(v)
    walk(d)
    return result
historical = collect(json.loads(old.read_text(encoding='utf-8')))
bindings={}
for p in contracts:
    for name, data in collect(json.loads(p.read_text(encoding='utf-8'))).items():
        bindings[name]=(p.relative_to(b).as_posix(), data)
rows=[]; stale=[]
for item in items:
    p=b/item['path']; h=sha(p); im=Image.open(p)
    assert h==item['current_checkout_sha256']
    found=bindings.get(item['path']); cells=[]; source_contract=None
    if found:
        origin, data=found
        assert data['sheet_sha256']==h, item['path']
        cols, rr=data['grid']; assert im.width%cols==0 and im.height%rr==0
        for i in range(data['frame_count']):
            rect=[(i%cols)*(im.width//cols),(i//cols)*(im.height//rr),im.width//cols,im.height//rr]
            cell=im.convert('RGBA').crop((rect[0],rect[1],rect[0]+rect[2],rect[1]+rect[3]))
            cells.append(dict(index=i,region=rect,alpha_bbox=cell.getchannel('A').getbbox(),status='DIRECT_REVIEW_PENDING'))
        source_contract=dict(path=origin,sha256=sha(b/origin),binding=data,exact_native_hash_match=True)
    previous=historical.get(item['path'])
    if previous and previous['sheet_sha256']!=h:
        stale.append(dict(path=item['path'],older_hash=previous['sheet_sha256'],current_hash=h,current_manifest=source_contract['path']))
    rows.append(dict(id=item['id'],path=item['path'],sha256=h,bytes=p.stat().st_size,dimensions=list(im.size),mode=im.mode,cells=cells,current_source_contract=source_contract,historical_ownership_binding=previous,source_review_status='PENDING',source_score=None,source_scope='Whole existing native source and each exact authored cell; no mounted-use or complete-action acceptance.'))
assert len(stale)==2 and sum(len(x['cells']) for x in rows)==104
shutil.copyfile(Path(__file__).with_name('prepare_shared_entry_source_review_v530.py'),q/'review_tools/prepare_shared_entry_source_review_v530.py')
shutil.copyfile(__file__,q/'review_tools/prepare_shared_entry_source_review_v531.py')
write(q/'PREPARATION_FAILURE_V530.json',dict(status='PRESERVED_SOURCE_HASH_ASSERTION_FAILURE',error="AssertionError at prior binding['sheet_sha256']==current source hash",effect='Preparation stopped before plan, grades or impact. Only empty review folders and .gdignore existed. No source art or canonical metadata changed.',diagnosis=stale,correction='Current V2/V4 manifests independently match all 13 current atlas natives and their grids. Older alpha-ownership hashes remain historical and unchanged; they are not used as current source evidence.'))
snapshot=dict(status='PLANNED_NATIVE_SOURCE_AND_AUTHORED_CELL_REVIEW',created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),baseline=subprocess.check_output(['git','rev-parse','HEAD'],cwd=b,text=True).strip(),source_files=rows,source_count=18,authored_cells=104,current_contracts=[dict(path=p.relative_to(b).as_posix(),sha256=sha(p)) for p in contracts],historical_ownership_reference=dict(path=old.relative_to(b).as_posix(),sha256=sha(old),stale_hashes=stale),production_change=False,qualification='18 known existing Kitchen/Opera entrance natives, all 104 authored cells and original row sequences must be directly inspected before grading. Current manifests give exact native hashes and grids. No pixel edits, generation or production change; source grades never transfer to rendered contact, ordinary routes, device/child/owner or true2D game-wide acceptance.')
write(q/'PLAN_AND_SOURCE_BOUNDARY.json',snapshot)
impact=dict(id='job-shared-entrance-source-review-20261003',scope='Directly review 18 existing shared Kitchen/Opera entrance natives and individually score 104 authored prop cells. Reuse exact original pixels and current hash-matching V2/V4 manifests; retain two stale hashes in historical ownership metadata. No new art, source alteration, binding or production change. Extend the illustrated library, preserve prior register and rejected drafts, and keep source and complete-action acceptance separate.',baseline=snapshot['baseline'],rules=['DL-AUTH-05','DL-AUTH-06','DL-AUTH-07','DL-VIS-01','DL-VIS-02','DL-VIS-03','DL-VIS-04','DL-VIS-05','DL-VIS-06','DL-VIS-07','DL-READ-01','DL-READ-02','DL-READ-03','DL-MOT-01','DL-MOT-02','DL-MOT-03','DL-MOT-07','DL-ASSET-01','DL-ASSET-03','DL-ASSET-05','DL-ASSET-06'],findings=['MA-VIS-006','MA-PLAY-004','MA-OPERA-012'],files=sorted(p.relative_to(b).as_posix() for p in q.rglob('*') if p.is_file()),validation=[dict(command='Inspect all 18 full native sources and 104 exact authored cells',result='PENDING',evidence='audit/job_shared_entrance_sources_v1_20261003/PLAN_AND_SOURCE_BOUNDARY.json; no grades before review')],acceptance_gaps='Native source/cell review pending. Current mounted appearance, original timeline playback/contact, ordinary routes and target-device/child/owner acceptance remain separate. Source review cannot accept remaining spatial debt. The Candy one-file station repair is separately scoped and remains the only production delta from U. Canonical finding states unchanged.')
write(b/'design/audit_impacts/job-shared-entrance-source-review-20261003.json',impact)
print('PLAN_READY|18 natives|104 cells|13 exact-current manifests|2 stale historical hashes preserved|no bitmap or production edits')
