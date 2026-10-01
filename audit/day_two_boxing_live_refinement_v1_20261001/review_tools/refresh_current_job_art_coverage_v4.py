from pathlib import Path
import hashlib, json, shutil, subprocess
r=Path(__file__).resolve().parents[1]
families=[('day-one-pool-live-refinement-v2-20261001','audit/day_one_pool_live_refinement_v2_20261001'),('day-one-playroom-sign-v2-20261001','assets_src/imagegen/day1_playroom_sign_v2_20261001'),('day-two-boxing-puff-reuse-v1-20261001','audit/day_two_boxing_puff_reuse_v1_20261001'),('day-two-boxing-single-gloves-v1-20261001','assets_src/imagegen/day2_boxing_single_gloves_v1_20261001'),('day-two-boxing-live-refinement-v1-20261001','audit/day_two_boxing_live_refinement_v1_20261001')]
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
pool=r/families[0][1];live=r/families[-1][1]
shutil.copyfile(r/'tmp/serve_nursery_review.py',pool/'review_tools/serve_nursery_review_current_v4.py')
shutil.copyfile(Path(__file__),live/'review_tools'/Path(__file__).name)
status=r/'audit/job_artwork_refinement_live/STATUS.json';d=json.loads(status.read_text());d['current_boxing_gloves']['individual_timed_art_scores']=[4.6,4.6];d['current_boxing_gloves']['current_live_review']='audit/day_two_boxing_live_refinement_v1_20261001/REVIEW.json';d['current_boxing_gloves']['complete_actions_accepted']=False;d['current_pool_refinement']['full_ci_in_progress']=True;d['current_pool_refinement']['current_full_ci_retry_v3']='audit/day_one_pool_live_refinement_v2_20261001/full_ci_current_retry_v3/RECEIPT.json';write(status,d)
licenses=r/'ASSET_LICENSES.md';s=licenses.read_text(encoding='utf-8')
for _,prefix in families:
    for p in sorted((r/prefix).rglob('*')):
        if not p.is_file() or p.suffix.lower() not in ('.png','.webp'):continue
        rel=p.relative_to(r).as_posix()
        if '`'+rel+'`' not in s:s+=f'| `{rel}` | Mermaid Roshan project artwork / native diagnostic or review-browser capture | Existing source provenance; review evidence | Local project | Exact diagnostic capture, review-browser screenshot or whole-canvas inspection board; no new delivery artwork or owner acceptance; source records retained |\n'
licenses.write_text(s,encoding='utf-8',newline='\n')
paths=set()
for ident,prefix in families:
    p=r/'design/audit_impacts'/f'{ident}.json';d=json.loads(p.read_text());d['files']=sorted(set(d['files'])|{q.relative_to(r).as_posix() for q in (r/prefix).rglob('*') if q.is_file()});write(p,d);paths.update(d['files']);paths.add(p.relative_to(r).as_posix())
paths=sorted(paths)
assert all((r/p).is_file() for p in paths)
for i in range(0,len(paths),70):
    subprocess.run(['git','add','-f','--sparse','--',*paths[i:i+70]],cwd=r,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
    if i%700==0:print('STAGE_PROGRESS',min(i+70,len(paths)),len(paths),flush=True)
print('Staged current exact coverage:',len(paths),flush=True)
