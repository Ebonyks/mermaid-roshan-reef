"""Package already-isolated garments and explicit bindings; never invent a character or weights."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import tempfile
try:
    from tools.validate_costume_skin import fields, require, validate_skin
except ModuleNotFoundError:
    from validate_costume_skin import fields, require, validate_skin


def reference(root: Path, name: str) -> dict:
    require(isinstance(name,str) and name and '\\' not in name and ':' not in name, 'recipe paths must be repository-relative POSIX')
    path=PurePosixPath(name)
    require(not path.is_absolute() and '..' not in path.parts and not any(p.lower() in {'.git','.secrets','.aws','.codex','.claude'} for p in path.parts), 'unsafe recipe path')
    source=(root/name).resolve()
    require(source.is_relative_to(root.resolve()) and source.is_file(), 'missing/escaping recipe asset: '+name)
    return {'path':name,'sha256':hashlib.sha256(source.read_bytes()).hexdigest()}


def prepare(recipe: dict, rig_path: Path, root: Path) -> tuple[dict,dict]:
    fields(recipe, {'skin_id','views','attachments','coverage','sources','edits','generator_calls'}, set(), 'recipe')
    rig=json.loads(rig_path.read_text(encoding='utf-8'))
    attachments=[]
    for item in recipe['attachments']:
        fields(item, {'id','view','slot','texture'}, {'template_id','geometry','binding'}, 'recipe attachment')
        out={k:item[k] for k in ['id','view','slot']}
        out['texture']=reference(root,item['texture'])
        if 'binding' in item:
            require('template_id' not in item and 'geometry' not in item, 'ambiguous rigid/weighted recipe')
            out.update(mode='rigid',binding=item['binding'])
        elif 'template_id' in item:
            require('geometry' not in item and item['template_id'] in rig['templates'], 'unknown/ambiguous binding template')
            out.update(mode='weighted',template_id=item['template_id'],geometry=rig['templates'][item['template_id']])
        else:
            require('geometry' in item, 'garment lacks binding/template; do not guess weights')
            out.update(mode='weighted',geometry=reference(root,item['geometry']))
        attachments.append(out)
    sources=[]
    for item in recipe['sources']:
        fields(item, {'path','license','role','acceptance_scope'}, set(), 'recipe source')
        sources.append({'asset':reference(root,item['path']),'license':item['license'],'role':item['role'],'acceptance_scope':item['acceptance_scope']})
    skin={'format':'roshan.skin/1','skin_id':recipe['skin_id'],'rig':{'id':rig['rig_id'],'version':rig['version'],'contract_sha256':hashlib.sha256(rig_path.read_bytes()).hexdigest()},'views':recipe['views'],'attachments':attachments,'coverage':recipe['coverage'],'provenance':{'sources':sources,'edits':recipe['edits'],'generator_calls':recipe['generator_calls']}}
    with tempfile.TemporaryDirectory(prefix='roshan_skin_format_') as temporary:
        path=Path(temporary)/'skin.json'
        path.write_text(json.dumps(skin,indent=2)+'\n',encoding='utf-8',newline='\n')
        report=validate_skin(path,rig_path,root)
    return skin,report


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--recipe',type=Path,required=True)
    parser.add_argument('--rig',type=Path,required=True)
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1])
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    try:
        require(not args.out.exists(), 'output already exists; choose a new versioned path')
        require(args.out.suffix.lower()=='.json', 'skin output must be a JSON data file')
        require(args.out.resolve().is_relative_to(args.root.resolve()), 'output must stay inside asset root')
        skin,report=prepare(json.loads(args.recipe.read_text(encoding='utf-8')),args.rig,args.root.resolve())
        args.out.parent.mkdir(parents=True,exist_ok=True)
        args.out.write_text(json.dumps(skin,indent=2)+'\n',encoding='utf-8',newline='\n')
        print(json.dumps({'output':str(args.out),**report},indent=2))
        return 0
    except (ValueError,OSError,KeyError,TypeError) as error:
        print(json.dumps({'format_and_bindings_pass':False,'error':str(error),'production_accepted':False},indent=2))
        return 1


if __name__=='__main__':raise SystemExit(main())
