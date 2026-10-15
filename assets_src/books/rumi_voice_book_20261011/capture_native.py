"""Copy a native built-in output byte-for-byte and record one independent job."""
from __future__ import annotations
import argparse
import hashlib
import json
import shutil
from pathlib import Path
from PIL import Image

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
def sha(path:Path)->str:return hashlib.sha256(path.read_bytes()).hexdigest()
def main()->None:
    ap=argparse.ArgumentParser()
    ap.add_argument('--page',type=int,required=True)
    ap.add_argument('--provider-path',required=True)
    ap.add_argument('--take',type=int,default=1)
    ap.add_argument('--prompt-file',help='Exact corrective prompt saved before the call, inside this edition')
    ap.add_argument('--references-file',help='Actual correction references, edition-local JSON array')
    ap.add_argument('--change-description',default='none; byte-identical copy; no crop, resize, overlay or JPEG conversion')
    args=ap.parse_args()
    if not 1<=args.page<=32 or not 1<=args.take<=3:raise ValueError('bounded page/take required')
    jobs=json.loads((HERE/'illustration_jobs.json').read_text(encoding='utf-8'))
    job=jobs['jobs'][args.page-1]
    prompt=job['prompt']
    if args.prompt_file:
        prompt_path=Path(args.prompt_file).resolve(strict=True)
        if not prompt_path.is_relative_to(HERE.resolve()):raise ValueError('prompt must stay in edition')
        prompt=prompt_path.read_text(encoding='utf-8')
    if args.take>1 and not args.prompt_file:raise ValueError('retake requires its exact recorded prompt')
    refs=job['references']
    if args.references_file:
        refs_path=Path(args.references_file).resolve(strict=True)
        if not refs_path.is_relative_to(HERE.resolve()):raise ValueError('reference list must stay in edition')
        refs=json.loads(refs_path.read_text(encoding='utf-8'))
        for ref in refs:
            if not (ROOT/ref['path']).resolve(strict=True).is_relative_to(ROOT.resolve()):raise ValueError('reference source outside repository')
    src=Path(args.provider_path).resolve(strict=True)
    if src.suffix.lower()!='.png' or 'generated_images' not in src.parts:raise ValueError('native built-in PNG source required')
    dst=HERE/f'native/page_{args.page:02}_take{args.take}.png'
    dst.parent.mkdir(parents=True,exist_ok=True)
    if dst.exists():raise FileExistsError(dst)
    shutil.copyfile(src,dst)
    if sha(src)!=sha(dst):raise ValueError('copy changed bytes')
    with Image.open(dst) as im:
        dims=list(im.size)
        pixels=hashlib.sha256(im.convert('RGB').tobytes()).hexdigest()
        mode=im.mode
    row={'page':args.page,'take':args.take,'method':'built-in image_gen.imagegen','provider_path':str(src),'path':dst.relative_to(ROOT).as_posix(),'sha256':sha(dst),'provider_sha256':sha(src),'rgb_pixel_sha256':pixels,'dimensions':dims,'native_mode':mode,'prompt':prompt,'prompt_sha256':hashlib.sha256(prompt.encode('utf-8')).hexdigest(),'script_sha256':jobs['script_sha256'],'references':[dict(ref,sha256=sha(ROOT/ref['path'])) for ref in refs],'modifications':args.change_description,'provider_revision':'not exposed','request_id':'not exposed','seed':'not exposed','reported_cost':'not exposed','call_count':1,'selection':'REVIEW_PENDING','license_provenance':'Owner-commissioned original project source candidate generated with built-in ImageGen; original project sources used as identity/setting guidance. No copied third-party scene pixels.'}
    receipt=HERE/f'generation/page_{args.page:02}_take{args.take}.json'
    receipt.parent.mkdir(parents=True,exist_ok=True)
    receipt.write_text(json.dumps(row,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({'page':args.page,'take':args.take,'path':str(dst),'dimensions':dims,'sha256':sha(dst)}))
if __name__=='__main__':main()
