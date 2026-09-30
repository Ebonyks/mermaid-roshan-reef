"""Read-only verification for the native Aseprite Rumi/craft follow-up."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
PACKET=ROOT/'assets_src/repairs/rumi_transparency_2026-09-30'
def rgba(path):return np.array(Image.open(path).convert('RGBA'))
def verify():
    spec=json.loads((PACKET/'REPAIR.json').read_text())
    for group in ('sources','outputs'):
        for name,digest in spec[group].items():
            data=(ROOT/name).read_bytes()
            if name.endswith('.lua'):data=data.replace(b'\r\n',b'\n')
            assert hashlib.sha256(data).hexdigest()==digest,name+' provenance drift'
    atlas=rgba(ROOT/'assets/characters/rumi/rumi_eight_pose_runtime.png')
    assert atlas.shape==(768,1024,4)
    for i in range(8):
        frame=atlas[i//4*384:(i//4+1)*384,i%4*256:(i%4+1)*256]
        y,x=np.where(frame[:,:,3]>8)
        assert min(x.min(),y.min(),255-x.max(),383-y.max())>=7,('Rumi gutter',i)
    before=rgba(PACKET/'rumi_pool_before.png');after=rgba(ROOT/'assets/characters/rumi/rumi_pool_idle_swim_atlas.png')
    assert before.shape==after.shape==(512,1024,4)
    assert np.array_equal(before[256:],after[256:]),'Swimming row changed'
    for i in range(4):
        cell=after[:256,i*256:(i+1)*256]
        y,x=np.where(cell[:,:,3]>8)
        assert min(x.min(),y.min(),255-x.max(),255-y.max())>=7,('Pool idle gutter',i)
        assert 225<=y.max()-y.min()+1<=242,('Pool idle scale',i)
    before=rgba(PACKET/'board_before.png');after=rgba(ROOT/'assets/flats/castle/interactions_v2/craft_room_idea_board_sheet.png')
    for i in range(8):
        a=before[i//4*188:(i//4+1)*188,i%4*256:(i%4+1)*256].copy()
        b=after[i//4*188:(i//4+1)*188,i%4*256:(i%4+1)*256]
        if i in spec['board']['frames']:
            for x0,y0,x1,y1 in spec['board']['erase_rects']:a[y0:y1,x0:x1]=0
            expected=np.zeros_like(a);expected[:,:252]=a[:,4:]
        else:expected=a
        polygon=spec['board']['backing_polygon']
        for y in range(36,132):
            for x in range(42,216):
                inside=False;j=len(polygon)-1
                for k,pa in enumerate(polygon):
                    pb=polygon[j]
                    if ((pa[1]>y)!=(pb[1]>y)) and x<(pb[0]-pa[0])*(y-pa[1])/(pb[1]-pa[1])+pa[0]:inside=not inside
                    j=k
                if inside:
                    sample=expected[113,47,:3].copy()
                    t=expected[y,x,3]/255
                    expected[y,x,:3]=np.floor(expected[y,x,:3]*t+sample*(1-t)+0.5)
                    expected[y,x,3]=255
        visible=(expected[:,:,3]>0)|(b[:,:,3]>0)
        assert np.array_equal(expected[visible],b[visible]),('Unowned board edit',i)
    print('RUMI_TRANSPARENCY|ALL OK')
if __name__=='__main__':verify()
