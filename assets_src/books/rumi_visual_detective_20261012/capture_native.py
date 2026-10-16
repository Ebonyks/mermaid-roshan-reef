"""Preserve one bounded built-in page take byte-for-byte, without image edits."""
from __future__ import annotations
import argparse, hashlib, json, shutil
from datetime import datetime, timezone
from pathlib import Path
from PIL import Image
from validate_selection import FROZEN_SCRIPT, THIRD_TAKE_PAGES, validate_method_change
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--page',type=int,required=True)
    ap.add_argument('--take',type=int,required=True)
    ap.add_argument('--provider-path',required=True)
    ap.add_argument('--prompt-file',required=True)
    ap.add_argument('--references-file',required=True)
    ap.add_argument('--method-change-file',help='Only page8/10 take3: exact root-authorized fresh-layout method-change record')
    args=ap.parse_args()
    if not 1<=args.page<=32 or not 1<=args.take<=(3 if args.page in THIRD_TAKE_PAGES else 2):raise ValueError('Two-take cycle cap; take3 only for named pages8/10 with bound method change')
    script_path=HERE/'story_script.json'
    script=json.loads(script_path.read_text(encoding='utf-8'))
    page=script['pages'][args.page-1]
    if page['number']!=args.page:raise ValueError('Page mapping')
    prompt_path=Path(args.prompt_file).resolve(strict=True)
    refs_path=Path(args.references_file).resolve(strict=True)
    if not prompt_path.is_relative_to(HERE) or not refs_path.is_relative_to(HERE):raise ValueError('Edition-local prompt/reference sidecars required')
    method_change=None
    if args.take==3:
        if not args.method_change_file:raise ValueError('Named third take requires --method-change-file')
        if sha(script_path)!=FROZEN_SCRIPT:raise ValueError('Third take must bind corrected final source')
        method_change=validate_method_change(Path(args.method_change_file),args.page,prompt_path,refs_path)
    elif args.method_change_file:
        raise ValueError('Method-change record applies only to the authorized third take')
    refs=json.loads(refs_path.read_text(encoding='utf-8'))
    actual_refs=[]
    for ref in refs:
        path=(ROOT/ref['path']).resolve(strict=True)
        if not path.is_relative_to(ROOT):raise ValueError('Project-bound reference required')
        actual_refs.append(dict(ref,sha256=sha(path)))
    provider=Path(args.provider_path).resolve(strict=True)
    if provider.suffix.lower()!='.png' or 'generated_images' not in provider.parts:raise ValueError('Native built-in PNG required')
    target=HERE/f'native/page_{args.page:02}_take{args.take}.png'
    receipt=HERE/f'generation/page_{args.page:02}_take{args.take}.json'
    if target.exists() or receipt.exists():raise FileExistsError('No overwriting preserved takes')
    target.parent.mkdir(parents=True,exist_ok=True)
    receipt.parent.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(provider,target)
    if sha(provider)!=sha(target):raise ValueError('Copy changed bytes')
    with Image.open(target) as im:
        if im.mode!='RGB' or im.size!=(1024,1536):raise ValueError('Full native 1024x1536 RGB page required; no conversion allowed')
        rgb_sha=hashlib.sha256(im.tobytes()).hexdigest()
    prompt=prompt_path.read_text(encoding='utf-8')
    row={'page':args.page,'take':args.take,'created_at_utc':datetime.now(timezone.utc).isoformat(),'method':'built-in image_gen.imagegen','provider_path':str(provider),'path':target.relative_to(ROOT).as_posix(),'sha256':sha(target),'provider_sha256':sha(provider),'rgb_pixel_sha256':rgb_sha,'dimensions':[1024,1536],'native_mode':'RGB','script_sha256':sha(script_path),'source_page_sha256':hashlib.sha256(json.dumps(page,ensure_ascii=False,sort_keys=True).encode('utf-8')).hexdigest(),'prompt':prompt,'prompt_sha256':sha(prompt_path),'prompt_file':prompt_path.relative_to(ROOT).as_posix(),'references':actual_refs,'references_file':refs_path.relative_to(ROOT).as_posix(),'modifications':'Native provider PNG copied byte-identically; own-page generated corrections declared by exact prompt; no software crop/resize/sharpening/lettering overlay. Adjacent generated pixels may change.','provider_revision':'not exposed','request_id':'not exposed','seed':'not exposed','reported_cost':'not exposed','call_count':1,'selection':'REVIEW_PENDING','license_provenance':'Owner-commissioned original static-book candidate; existing project identity/setting/prop references retain terms; no film pixels/scene copy.'}
    if method_change:
        row['method_change']=method_change
        row['modifications']='Native provider PNG copied byte-identically; one root-authorized fresh full-page staging call after two failed local repairs, retained in a three-call total cycle. No software crop/resize/sharpening/lettering overlay; no cross-page delivery reuse.'
    receipt.write_text(json.dumps(row,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({'page':args.page,'take':args.take,'native':str(target),'sha256':row['sha256']}))
if __name__=='__main__':main()
