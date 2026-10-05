"""Read-only sharpness diagnostics; cannot establish identity or artwork acceptance."""
import hashlib,json
from pathlib import Path
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parents[1];ROOT=P.parents[2]
OLD=ROOT/'assets_src/cinematics/ltx25_8gb_wave_20261004'
V2=ROOT/'assets_src/cinematics/ltx25_scale_filter_v2_20261004'
def metric(path,xoff=0):
    a=np.asarray(Image.open(path).convert('RGB'),dtype=np.float32)
    roi=a[165:250,145+xoff:285+xoff];g=roi@np.array([.2126,.7152,.0722],dtype=np.float32)
    lap=4*g[1:-1,1:-1]-g[:-2,1:-1]-g[2:,1:-1]-g[1:-1,:-2]-g[1:-1,2:]
    dx=g[1:-1,2:]-g[1:-1,:-2];dy=g[2:,1:-1]-g[:-2,1:-1]
    bg=a[20:60,520:560]@np.array([.2126,.7152,.0722],dtype=np.float32)
    bg_lap=4*bg[1:-1,1:-1]-bg[:-2,1:-1]-bg[2:,1:-1]-bg[1:-1,:-2]-bg[1:-1,2:]
    return {'path':path.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'laplacian_variance':float(lap.var()),'gradient_energy':float(np.mean(dx*dx+dy*dy)),
            'empty_background_laplacian_variance':float(bg_lap.var()),'empty_background_std':float(bg.std()),
            'roi_xyxy':[145+xoff,165,285+xoff,250]}
def main():
    rows=[]
    for i in range(41):
        row={'index':i,'native':metric(OLD/f'results/scale_registered/refined_frames/{i:04d}.png'),
             'registered':metric(V2/f'frames/{i:04d}.png',24)}
        if (P/f'decoder_2_frames/{i:04d}.png').is_file():row['decoder_2']=metric(P/f'decoder_2_frames/{i:04d}.png')
        rows.append(row)
    guides=[{'index':i,**metric(OLD/f'scale_continuity/registered_guides/guide_{i:04d}.png')} for i in [0,3,7,17,22,27,36,40]]
    summaries=[]
    for lane in [n for n in rows[0] if n!='index']:
        vals=[r[lane]['laplacian_variance'] for r in rows];energy=[r[lane]['gradient_energy'] for r in rows]
        summaries.append({'lane':lane,'laplacian_min':min(vals),'laplacian_max':max(vals),'laplacian_max_min_ratio':max(vals)/min(vals),
                          'gradient_min':min(energy),'gradient_max':max(energy),'gradient_max_min_ratio':max(energy)/min(energy),
                          'empty_background_laplacian_median':float(np.median([r[lane]['empty_background_laplacian_variance'] for r in rows])),
                          'softest_laplacian_index':int(np.argmin(vals)),'sharpest_laplacian_index':int(np.argmax(vals))})
    report={'status':'DIAGNOSTIC_ONLY','frames':rows,'registered_guides':guides,'summaries':summaries,
            'interpretation_limits':'ROI edge content, pose, colour and small registration changes affect these numbers. They are supporting native focus observations, not a stand-alone sharpness gate. No image pixels edited by Python.',
            'focus_inference':'Large edge-energy changes are already present in native frames before Aseprite/MP4; guide sharpness heterogeneity is a plausible contributor, not isolated causality.'}
    (P/'focus_metrics.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print('FOCUS',json.dumps(summaries))
    print('GUIDE_LAPLACIAN',[(r['index'],round(r['laplacian_variance'],2)) for r in guides])
if __name__=='__main__':main()
