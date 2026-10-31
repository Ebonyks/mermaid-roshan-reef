"""Freeze a job-specific profile and validate bound source hashes before Aseprite.

This prepares metadata/code only; it does not create or edit any image.
"""
from pathlib import Path
import argparse,hashlib,json,shutil,re
base=Path(__file__).resolve().parent
root=base.parents[3]
parser=argparse.ArgumentParser()
parser.add_argument('--profile',required=True,help='Existing source-bound JSON profile, relative to this study or absolute')
parser.add_argument('--output',required=True,help='Fresh child study directory name')
parser.add_argument('--sample-frame',type=int,action='append',help='Bound single-cell reproduction proof; never a complete-performance claim')
args=parser.parse_args()
out=(base/args.output).resolve()
assert out.parent==base,'Output must be a new direct study child'
assert not out.exists(), 'Use a fresh immutable draft directory'
profile=Path(args.profile)
if not profile.is_absolute():profile=base/profile
profile=profile.resolve();assert profile.is_relative_to(base),'Profile must remain within this study'
cfg=json.loads(profile.read_text(encoding='utf-8-sig'))
assert not ({'arm_template','hand_template','rig','skeleton','part_images','appearance_parts'}&set(cfg)), 'No rig or part appearance inputs'
schema_path=base/'recipe_profile.schema.json'
schema=json.loads(schema_path.read_text(encoding='utf-8'))
def validate(value,rule,path='$'):
    """Validate the declared local schema subset using only the stdlib."""
    if '$ref' in rule:
        target=schema
        for name in rule['$ref'].removeprefix('#/').split('/'):target=target[name]
        return validate(value,target,path)
    if 'const' in rule:assert value==rule['const'],f'{path}: wrong constant'
    kind=rule.get('type')
    tests={'object':lambda: isinstance(value,dict),'array':lambda:isinstance(value,list),
        'string':lambda:isinstance(value,str),'number':lambda:isinstance(value,(int,float)) and not isinstance(value,bool),
        'integer':lambda:isinstance(value,int) and not isinstance(value,bool)}
    if kind:assert tests[kind](),f'{path}: expected {kind}'
    if kind=='object':
        for name in rule.get('required',[]):assert name in value,f'{path}.{name}: required'
        for name,sub in rule.get('properties',{}).items():
            if name in value:validate(value[name],sub,f'{path}.{name}')
    elif kind=='array':
        assert len(value)>=rule.get('minItems',0) and len(value)<=rule.get('maxItems',float('inf')),f'{path}: invalid array length'
        for n,item in enumerate(value):validate(item,rule.get('items',{}),f'{path}[{n}]')
    elif kind in ('number','integer'):
        assert value>=rule.get('minimum',-float('inf')) and value<=rule.get('maximum',float('inf')),f'{path}: bounds'
        assert value>rule.get('exclusiveMinimum',-float('inf')),f'{path}: exclusive bound'
    elif kind=='string' and 'pattern' in rule:assert re.search(rule['pattern'],value),f'{path}: pattern'
if cfg['schema']=='reef.aseprite-whole-cel-paint-profile.v2':validate(cfg,schema)
mask_path=(root/cfg['head_boundary_masks']).resolve()
assert mask_path.is_relative_to(base),'Masks must be inspectable within the source study'
masks=json.loads(mask_path.read_text(encoding='utf-8-sig'))
assert cfg['frame_count']==41 and cfg['fps']==24 and cfg['duration_ms']==1708,'Preserve this wave action contract'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
sources=[]
source_dir=(root/cfg['source_dir']).resolve()
assert source_dir.is_relative_to(root/'assets_src/animation'),'Sources must be non-runtime animation sources'
assert len(masks['frames'])==cfg['frame_count'],'Every source needs a bound mask record'
assert [f['index'] for f in masks['frames']]==list(range(cfg['frame_count'])),'Source-mask indices must be exact ordered0..40'
for f in masks['frames']:
    p=source_dir/f"{f['index']:04d}.png"
    assert sha(p)==f['source_sha256'],f'Bound source changed: {p}'
    sources.append({'frame':f['index'],'path':p.relative_to(root).as_posix(),'sha256':sha(p)})
cfg['head_boundary_masks']=(out/'head_boundary_masks.json').relative_to(root).as_posix()
cfg.pop('sample_frames',None)
cfg['master_name']='wave_native_rgb.aseprite'
if args.sample_frame:
    assert all(0<=n<cfg['frame_count'] for n in args.sample_frame),'Sample index outside action'
    assert len(set(args.sample_frame))==len(args.sample_frame),'Duplicate sample index'
    cfg['sample_frames']=args.sample_frame;cfg['master_name']='sample_proof.aseprite'
cfg['profile_parent']={'path':profile.relative_to(root).as_posix(),'sha256':sha(profile)}
out.mkdir()
def save(name,data):
    (out/name).write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8',newline='\n')
save('recipe_profile.json',cfg)
save('head_boundary_masks.json',masks)
shutil.copyfile(base/'paint_connected.lua',out/'paint_connected.lua')
shutil.copyfile(Path(__file__),out/'prepare_full_draft.executed.py')
if cfg['schema']=='reef.aseprite-whole-cel-paint-profile.v2':shutil.copyfile(schema_path,out/schema_path.name)
save('source_and_recipe_binding.json',{'schema':'reef.aseprite-source-recipe-binding.v1','sources':sources,
    'recipe_sha256':sha(out/'paint_connected.lua'),'profile_sha256':sha(out/'recipe_profile.json'),
    'preparation_script_sha256':sha(Path(__file__)),'profile_parent_sha256':sha(profile),
    'preparation_script_snapshot':'prepare_full_draft.executed.py','preparation_execution_context':Path(__file__).relative_to(root).as_posix(),
    'profile_schema_sha256':sha(schema_path),'schema_validation':'stdlib validator of the exact local declared JSON Schema subset for v2; legacy profiles retain scoped defaults',
    'mask_sha256':sha(out/'head_boundary_masks.json'),'method':'Aseprite whole-native-cel local direct paint',
    'generated_api_calls':0,'gpu_jobs':0,'external_cost':0,'human_acceptance':False,
    'pending':['all native contours after full rendering','final RGBA every frame and normal-speed loop','W2/W3 final exact bytes','device','owner']})
print(out)
