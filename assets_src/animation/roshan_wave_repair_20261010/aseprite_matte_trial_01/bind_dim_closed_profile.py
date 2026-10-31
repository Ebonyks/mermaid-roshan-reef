"""Bind the source-bound selected whole-cel matte profile. This metadata/script step writes no pixels."""
from pathlib import Path
import sys,json,shutil,hashlib,datetime
packet=Path(__file__).resolve().parent
folder=(packet/sys.argv[1]).resolve()
assert folder.parent==packet and folder.is_dir(), 'Use a newly prepared owned sibling folder'
assert not (folder/'native_rgba').exists(), 'Do not replace a started or frozen candidate'
plan=json.loads((folder/'source_and_seed_plan.json').read_text(encoding='utf-8'))
assert len(plan['sources'])==41 and all(r['source_size']==[768,896] for r in plan['sources'])
reference=packet/'full_wave_matte_03'
reference_plan=json.loads((reference/'source_and_seed_plan.json').read_text(encoding='utf-8'))
for name in ['recover_full_edges.lua','verify_full_matte.py','black_review.lua']:
    destination=folder/name
    if destination.exists(): shutil.copyfile(destination,folder/('prepared_strict_'+name))
    shutil.copyfile(reference/name,destination)
plan['matte_profile']=reference_plan['matte_profile']
plan['mapping']=reference_plan['mapping']
plan['profile_binding']={'reference_folder':reference.name,'bound_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'copied_recipe_sha256':hashlib.sha256((folder/'recover_full_edges.lua').read_bytes()).hexdigest(),'pixel_writes':False,'seed_review_required':'Every newly preserved source crop still requires actual review before the processor assertion passes'}
(folder/'source_and_seed_plan.json').write_text(json.dumps(plan,indent=2)+'\n',encoding='utf-8')
print(json.dumps(plan['profile_binding']))
