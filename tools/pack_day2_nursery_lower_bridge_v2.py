"""Lossless review windows and declared manual landmarks; never edits sealed sources."""
from pathlib import Path
import hashlib,json
from PIL import Image

R=Path(__file__).resolve().parents[1]
FOLDER='assets_src/imagegen/day2_nursery_lower_bridge_v2_20261001'
SOURCE='assets_src/imagegen/day2_nursery_lower_bridge_20261001/candidates/attempt-01.png'
EXPECTED='464e9d3c4791c87a50103d645363ff70f191ff7905b7feebbc06e3f8cded5957'
WINDOWS=[(0,0,655,627),(655,0,1254,627),(0,627,655,1254),(655,627,1254,1254)]
# Manual native apron/tail center and supporting palm estimates, +/-5 source pixels.
# These are diagnostic measurements, not approved runtime contacts.
HIPS=[(273,475),(899,478),(307,1088),(925,1089)]
PALMS=[(184,345),(795,369),(161,1018),(753,1039)]

def main():
    out=R/FOLDER
    assert not (out/'MANIFEST.json').exists(), 'Review packet is sealed'
    raw=(R/SOURCE).read_bytes()
    assert hashlib.sha256(raw).hexdigest()==EXPECTED
    native=Image.open(R/SOURCE).convert('RGBA');assert native.size==(1254,1254)
    out.mkdir(parents=True,exist_ok=True);(out/'.gdignore').write_text('')
    reconstructed=Image.new('RGBA',native.size);rows=[]
    for index,window in enumerate(WINDOWS):
        crop=native.crop(window);offset=((1024-crop.width)//2,(1024-crop.height)//2)
        padded=Image.new('RGBA',(1024,1024));padded.paste(crop,offset)
        path=out/f'lower_{index:02}_review.png';padded.save(path)
        decoded=Image.open(path).convert('RGBA')
        restored=decoded.crop((offset[0],offset[1],offset[0]+crop.width,offset[1]+crop.height))
        assert restored.tobytes()==crop.tobytes();reconstructed.paste(restored,window[:2])
        painted=decoded.getchannel('A').point(lambda n:255 if n>=128 else 0).getbbox()
        rows.append({'index':index,'path':path.relative_to(R).as_posix(),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'dimensions':[1024,1024],'source_window':list(window),'padding_offset':list(offset),'painted_50pct_bounds':list(painted),'hip_xy':[HIPS[index][j]-window[j]+offset[j] for j in range(2)],'palm_xy':[PALMS[index][j]-window[j]+offset[j] for j in range(2)],'landmark_uncertainty_native_px':5,'pixel_copy_exact':True,'runtime_bound':False})
    assert reconstructed.tobytes()==native.tobytes()
    # Normalize the first new pose's painted full-body height to old hold key3.
    old=json.loads((R/'assets/opera/worlds/nursery/refinement_v2/care_keys.json').read_text())['poses'][3]
    old_image=Image.open(R/old['path']).convert('RGBA');old_box=old_image.getchannel('A').point(lambda n:255 if n>=128 else 0).getbbox()
    old_height=(old_box[3]-old_box[1])*250.0/512.0
    new_height=rows[0]['painted_50pct_bounds'][3]-rows[0]['painted_50pct_bounds'][1]
    extent=old_height/new_height*1024.0
    report={'schema':'reef.lowering-review-pack.v1','source':SOURCE,'source_sha256':EXPECTED,'method':'Exact nonoverlapping native RGBA windows on1024px transparent review canvases; all pixels reconstructed; no resampling, alpha repair, color change or subject modification.','all_native_rgba_pixels_reconstructed':True,'native_rgba_sha256':hashlib.sha256(native.tobytes()).hexdigest(),'poses':rows,'old_hold_50pct_bounds':list(old_box),'reference_painted_height_screen_px':old_height,'common_new_review_card_extent_px':extent,'scale_method':'One common whole-image display scale for all four new keys, set by painted full-body height of first source versus old held key3. No per-key scale, artificial socket adjustment or body translation hides displacement. Hip origin aligned across independently held comparisons.','owner_accepted':False,'runtime_contact_accepted':False}
    (out/'PACK_REPORT.json').write_text(json.dumps(report,indent=2)+'\n')
    print(f'LOWER_BRIDGE_REVIEW_PACK|4 exact keys|extent={extent:.6f}|no runtime binding')

if __name__=='__main__':main()
