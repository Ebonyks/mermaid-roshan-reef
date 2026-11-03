"""Prove the first rendered swap frame matches its standalone skin/phase."""
from pathlib import Path
import hashlib
import json

import numpy as np
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]


def load(path):return json.loads(Path(path).read_text(encoding='utf-8'))


def pixels(sample):
    path=ROOT/sample['frame'].removeprefix('res://')
    assert hashlib.sha256(path.read_bytes()).hexdigest()==sample['png_sha256']
    return np.asarray(Image.open(path).convert('RGBA'))


def main():
    data={name:load(ROOT/'evidence'/(name+'_samples.json'))['samples'] for name in ['ballet','magician','live_swaps']}
    actual=[];worst=0;passed=True
    for i,sample in enumerate(data['live_swaps']):
        expected=data[sample['skin']][i]
        difference=np.abs(pixels(sample).astype(np.int16)-pixels(expected).astype(np.int16))
        maximum=int(difference.max());count=int(np.count_nonzero(difference))
        same_pose=sample['bones']==expected['bones'] and sample['phase']==expected['phase'] and sample['root']==expected['root']
        same_actor=sample['actor_id']==expected['actor_id'] and sample['animator_id']==expected['animator_id']
        passed &= maximum==0 and same_pose and same_actor
        worst=max(worst,maximum)
        actual.append({'index':i,'skin':sample['skin'],'rgba_max_difference':maximum,'different_channels':count,
                       'same_native_pose_phase_root':same_pose,'same_actor_animator':same_actor})
    seam=[]
    for name in ['ballet','magician']:
        a,b=data[name][57],data[name][114]
        difference=np.abs(pixels(a).astype(np.int16)-pixels(b).astype(np.int16))
        seam.append({'skin':name,'indices':[57,114],'logical_times':[a['time'],b['time']],
                     'fin_turn_delta':abs(a['fin_turn_degrees']-b['fin_turn_degrees']),
                     'max_channel_difference':int(difference.max()),'mean_channel_difference':float(difference.mean()),
                     'note':'Actual rendered one-cycle endpoints at steady strength. Small subpixel camera/GPU rounding is recorded; human seam review remains separate.'})
    result={'pass':bool(passed),'frames_compared':len(actual),'maximum_rgba_difference':worst,
            'swap_boundary_frames':[37,76,113,154,187],'first_drawable_swap_pixels_exact':bool(passed),
            'frames':actual,'cycle_seam_observations':seam,
            'scope':'Each live capture follows the first RenderingServer.frame_post_draw after the synchronous swap; no settling frames skipped. Native data/output equality, not a simulated animation counter.',
            'human_motion_accepted':False,'device_verified':False,'owner_accepted':False}
    (ROOT/'evidence/swap_pixel_audit.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
    print('ACTUAL_FIRST_DRAW_SWAP_PIXELS',bool(passed),'frames',len(actual),'max_rgba_difference',worst,flush=True)
    return 0 if passed else 1


if __name__=='__main__':raise SystemExit(main())
