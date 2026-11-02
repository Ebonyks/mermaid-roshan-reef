"""Non-destructively copy actual identity/design inputs with role-bound hashes."""
from pathlib import Path
import hashlib
import json
import shutil

ROOT=Path(__file__).resolve().parents[1]
REPO=ROOT.parents[2]


def main():
    paths=[('roshan_base.png','assets/characters/roshan_25d/roshan_base.png','identity'),
           ('roshan_swim_front.png','assets/characters/roshan_25d/roshan_swim_front.png','existing_view_only')]
    for theme in ['ballet','magician']:
        for piece in ['body','tail','head']:
            paths.append((theme+'_'+piece+'.png',f'assets_src/fashion_designer/beta_20261025/native/{theme}_{piece}.png','wardrobe_design'))
    sources=[]
    for name,original,role in paths:
        target=ROOT/'references'/name;source=REPO/original
        before=hashlib.sha256(source.read_bytes()).hexdigest();shutil.copy2(source,target)
        assert before==hashlib.sha256(source.read_bytes()).hexdigest()==hashlib.sha256(target.read_bytes()).hexdigest()
        sources.append({'path':target.relative_to(ROOT).as_posix(),'original':original,'sha256':before,'role':role,
                        'modifications':'None; exact byte copy. Original unchanged.',
                        'acceptance_scope':'Existing static character identity/design reference only; does not accept generated derivatives or a new performance.',
                        'license':'Existing project asset provenance/rights retained; see root ASSET_LICENSES.md. No relicense.'})
    roles={
        'shared_view':{'IMAGE_1':'references/roshan_base.png','IMAGE_2':'references/roshan_swim_front.png'},
        'ballet':{'IMAGE_1':'art_source/shared_view_parts_take01.png','IMAGE_2':'references/ballet_body.png','IMAGE_3':'references/ballet_tail.png','IMAGE_4':'references/ballet_head.png'},
        'magician':{'IMAGE_1':'art_source/shared_view_parts_take01.png','IMAGE_2':'references/magician_body.png','IMAGE_3':'references/magician_tail.png','IMAGE_4':'references/magician_head.png','IMAGE_5':'art_source/ballet_parts_take01.png'},
        'neck':{'IMAGE_1':'art_source/shared_view_parts_take01.png'}}
    for inputs in roles.values():
        for name,path in list(inputs.items()):
            inputs[name]={'path':path,'sha256':hashlib.sha256((ROOT/path).read_bytes()).hexdigest()}
    result={'sources':sources,'generation_input_bindings':roles,
            'bound_roles':'Shared: identity and existing view only. Ballet/Magician: shared part geometry/style plus original costume designs; Magician IMAGE_5 supplies sheet layout/relative scale only. Neck: shared joint/style repair.',
            'reviews_used_as_generation_pixels':False,'position_guides_used_as_delivery_pixels':False,
            'generated_candidates_accepted':False,'master_audit_writeback_authorized':False}
    (ROOT/'references/source_manifest.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
    print('REFERENCE_COPIES_EXACT',len(sources),flush=True)


if __name__=='__main__':main()
