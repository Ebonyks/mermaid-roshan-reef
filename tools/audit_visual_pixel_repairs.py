"""Check pixel-preserving native repairs independently of the Aseprite exporters."""
from pathlib import Path
import argparse
import hashlib
import json
import numpy as np
from PIL import Image
ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / 'assets_src/repairs/visual_polish_2026-09-26'
def digest(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
# Keep the September 26 pixel contract immutable against its frozen exports.
# The current runtime successors are checked separately by verify() below.
FOLLOWUP_ORIGINALS = {
    'assets/characters/rumi/rumi_eight_pose_runtime.png': 'rumi_before.png',
    'assets/flats/castle/interactions_v2/craft_room_idea_board_sheet.png': 'board_before.png',
}
def historical_path(path):
    return ('assets_src/repairs/rumi_transparency_2026-09-30/' + FOLLOWUP_ORIGINALS[path]) if path in FOLLOWUP_ORIGINALS else path

def rgba(path):
    return np.array(Image.open(ROOT / historical_path(path)).convert('RGBA'))
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--record',action='store_true');args=parser.parse_args()
    for name in ('PIXEL_EDITS.json','ROSHAN_REPACK.json','FURNITURE_RECOVERY.json'):
        path=PACKET/name;packet=json.loads(path.read_text(encoding='utf-8'))
        if 'source' in packet:assert digest(packet['source'])==packet['source_sha256']
        for e in packet['assets']:
            output=rgba(e['output'])
            if 'source' in e:
                assert digest(e['source'])==e['source_sha256'],e['id']
                original=rgba(e['source'])
                if 'erase_rects' in e:
                    assert original.shape==output.shape
                    allowed=np.zeros(original.shape[:2],bool)
                    for x0,y0,x1,y1 in e['erase_rects']+e['opaque_rects']:allowed[y0:y1,x0:x1]=True
                    for x,y in e.get("force_opaque_pixels",[]):
                        allowed[y,x]=True
                        assert output[y,x,3]==255
                    for pixel in e.get("paint_pixels",[]):
                        x,y=pixel["xy"];allowed[y,x]=True
                        assert output[y,x].tolist()==pixel["rgba"]
                    changed=np.any(original!=output,axis=2)
                    assert not (changed & ~allowed).any(),e['id']+' changes outside reviewed regions'
                    for x0,y0,x1,y1 in e['erase_rects']:assert not output[y0:y1,x0:x1,3].any()
                    rgb_allowed=np.zeros(original.shape[:2],bool)
                    for pixel in e.get("paint_pixels",[]):
                        x,y=pixel["xy"];rgb_allowed[y,x]=True
                    assert np.array_equal(original[:,:,:3][~rgb_allowed],output[:,:,:3][~rgb_allowed]) if not e["erase_rects"] else True
                    e['verification']={'changed_pixels':int(changed.sum()),'changed_pixels_outside_reviewed_regions':0,'unchanged_dimensions':list(output.shape[:2][::-1])}
                else:
                    for f in e['frames']:
                        sx,sy=f['source_xy'];tx,ty=f['target_xy'];before=original[sy:sy+256,sx:sx+256];after=output[ty:ty+256,tx:tx+256];keep=np.ones((256,256),bool)
                        for y,x0,x1 in f['erase_spans']:
                            keep[y,x0:x1]=False
                            assert not after[y,x0:x1,3].any()
                        keep &= before[:,:,3]>0
                        assert np.array_equal(before[keep],after[keep]),e['id']+' owned RGBA pixel changed'
            else:
                assert list(output.shape[:2][::-1])==e['size']
                ys,xs=np.where(output[:,:,3]>8)
                assert min(xs.min(),ys.min(),output.shape[1]-1-xs.max(),output.shape[0]-1-ys.max())>=4,e['id']+' missing gutter'
            for key in ('output','native'):
                value=digest(historical_path(e[key]))
                if args.record:e[key+'_sha256']=value
                else:assert value==e[key+'_sha256'],e['id']+' '+key+' drift'
        if args.record:path.write_text(json.dumps(packet,indent=2)+'\n',encoding='utf-8')
    for name in ('CELL_RECOVERY.json','BLOCKS_RECOVERY.json'):
        path=PACKET/name;packet=json.loads(path.read_text(encoding='utf-8'))
        entries=packet.get('assets',[packet])
        for e in entries:
            assert digest(e['source'])==e['source_sha256']
            output=rgba(e['output'])
            if 'target_cell' in e:
                original=rgba(e['source']);allowed=np.zeros(original.shape[:2],bool)
                x,y,w,h=e['target_cell'];allowed[y:y+h,x:x+w]=True
                for x0,y0,x1,y1 in e['erase_rects']:allowed[y0:y1,x0:x1]=True
                assert np.array_equal(original[~allowed],output[~allowed]),e['id']+' unrelated cell changed'
                cells=[output[y:y+h,x:x+w]]
            else:
                w,h=e['cell_size'];cells=[output[y*h:(y+1)*h,x*w:(x+1)*w] for y in range(2) for x in range(4)]
                assert len({hashlib.sha256(cell.tobytes()).hexdigest() for cell in cells})==8
                assert not output[output[:,:,3]==0,:3].any(), 'blocks hidden RGB residue'
            for cell in cells:
                ys,xs=np.where(cell[:,:,3]>8)
                assert min(xs.min(),ys.min(),cell.shape[1]-1-xs.max(),cell.shape[0]-1-ys.max())>=4
            for key in ('output','native'):
                value=digest(historical_path(e[key]))
                if args.record:e[key+'_sha256']=value
                else:assert value==e[key+'_sha256'],e.get('id','blocks')+' '+key+' drift'
        if args.record:path.write_text(json.dumps(packet,indent=2)+'\n',encoding='utf-8')
    registration=json.loads((PACKET/'REGISTRATION.json').read_text(encoding='utf-8'))
    for e in registration['assets']:
        assert digest(e['source'])==e['source_sha256']
        before=rgba(e['source']);after=rgba(e['output']);w,h=e['cell_size']
        for i,(dx,dy) in enumerate(e['frame_translations']):
            x=i%4*w;y=i//4*h;a=before[y:y+h,x:x+w];b=after[y:y+h,x:x+w]
            ys,xs=np.where(a[:,:,3]>0)
            assert (xs+dx>=0).all() and (xs+dx<w).all() and (ys+dy>=0).all() and (ys+dy<h).all()
            assert np.array_equal(a[ys,xs],b[ys+dy,xs+dx])
            assert int((b[:,:,3]>0).sum())==len(ys)
        for key in ('output','native'):
            assert digest(historical_path(e[key]))==e[key+'_sha256'],e['id']+' registration drift'
    from audit_rumi_transparency import verify
    verify()
    print('VISUAL_PIXEL_REPAIRS|ALL OK')
if __name__=='__main__':main()
