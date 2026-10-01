"""Exact RGBA source-window packing for the three infant review candidates."""
from pathlib import Path
import hashlib
import json
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets_src/imagegen/day2_nursery_babies_v2_20261001'
SOURCE=OUT/'attempt-01.png'
EXPECTED='1fb5b34ad4cb7e7fc669f6f075bbff1a82c79f004909c60a7eff4c8c9cd90ea4'

def main():
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==EXPECTED
    native=Image.open(SOURCE).convert('RGBA')
    assert native.size==(1774,887)
    windows=[(0,0,591,887),(591,0,1182,887),(1182,0,1774,887)]
    rebuilt=Image.new('RGBA',native.size)
    rows=[]
    for i,window in enumerate(windows):
        crop=native.crop(window)
        assert crop.getchannel('A').crop((0,0,1,887)).getbbox() is None
        assert crop.getchannel('A').crop((crop.width-1,0,crop.width,887)).getbbox() is None
        offset=((1024-crop.width)//2,(1024-crop.height)//2)
        key=Image.new('RGBA',(1024,1024))
        key.paste(crop,offset)
        path=OUT/f'baby_{i}_review.png'
        key.save(path)
        saved=Image.open(path).convert('RGBA')
        recovered=saved.crop((offset[0],offset[1],offset[0]+crop.width,offset[1]+crop.height))
        assert recovered.tobytes()==crop.tobytes()
        rebuilt.paste(recovered,window[:2])
        bounds=saved.getchannel('A').getbbox()
        painted=saved.getchannel('A').point(lambda a:255 if a>=128 else 0).getbbox()
        assert painted
        assert bounds and min(bounds[0],bounds[1],1024-bounds[2],1024-bounds[3])>14
        rows.append({'index':i,'path':path.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                     'dimensions':[1024,1024],'source_window':list(window),'padding_offset':list(offset),
                     'alpha_bounds':list(bounds),'painted_50pct_bounds':list(painted),'visible_foot_uv':[(painted[0]+painted[2])/2048,painted[3]/1024],
                     'candidate_card_extent_px':80,'candidate_visible_height_px':(painted[3]-painted[1])*80/1024,
                     'source_rgba_window_exact':True,'runtime_bound':False})
    assert rebuilt.tobytes()==native.tobytes()
    report={'schema':'reef.nursery-baby-source-pack.v1','native_sha256':EXPECTED,'method':'Exact nonoverlapping RGBA windows on transparent1024px canvases; no resampling, filtering, alpha repair, recolor or subject modification.',
            'all_native_rgba_pixels_reconstructed':True,'poses':rows,'decoded_review_rgba_bytes':3*1024*1024*4,
            'qualification':'Source-only review PNGs.80px candidate extent approximately matches the original visible infant height; mounted socket, mobile budget and runtime production sizing remain unverified. No new production asset is bound.',
            'owner_accepted':False}
    (OUT/'PACK_REPORT.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print('NURSERY_BABY_PACK|PASS|3 intact candidates|all native RGBA pixels reconstructed')

if __name__=='__main__':
    main()
