"""Retain a failed preflight as explicit lossless 2D RGBA XOR video."""
from pathlib import Path
import hashlib,json,shutil
import numpy as np
from PIL import Image
from make_review import ROOT,load,native_path
from rgba_delta_video import encode_rgba,decode_rgba


def main():
    destination=ROOT/'evidence/history/framing_preflight'
    destination.mkdir(parents=True,exist_ok=True)
    native=load(ROOT/'evidence/native_capture_receipt.json')
    for name,digest in native['inputs'].items():
        source=ROOT/name;assert hashlib.sha256(source.read_bytes()).hexdigest()==digest,name
        target=destination/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,target)
    for name in ['native_capture_receipt.json','native_capture_complete.json','native_capture.log','native_swap_tests.json','native_geometry_audit.json','ballet_samples.json','magician_samples.json','live_swaps_samples.json']:
        target=destination/'evidence'/name;target.parent.mkdir(exist_ok=True);shutil.copy2(ROOT/'evidence'/name,target)
    reports=[]
    for identity in ['ballet','magician','live_swaps']:
        base=ROOT/'evidence/history/candidate02_component_bug/masters'/(identity+'_native_rgba.mkv')
        samples=load(ROOT/'evidence'/(identity+'_samples.json'))['samples'];proof=[]
        output=destination/(identity+'_rgba_delta.mkv')
        def deltas():
            for sample,baseline in zip(samples,decode_rgba(base,len(samples)),strict=True):
                original=np.asarray(Image.open(native_path(sample)).convert('RGBA'))
                proof.append({'index':sample['index'],'native_png_sha256':sample['png_sha256'],'rgba_sha256':hashlib.sha256(original.tobytes()).hexdigest()})
                yield np.bitwise_xor(original,baseline)
        encode_rgba(output,deltas(),len(samples))
        for baseline,delta,record in zip(decode_rgba(base,len(samples)),decode_rgba(output,len(samples)),proof,strict=True):
            assert hashlib.sha256(np.bitwise_xor(baseline,delta).tobytes()).hexdigest()==record['rgba_sha256']
        manifest={'format':'roshan.rgba-xor-video/1','base_archive':base.relative_to(ROOT).as_posix(),
                  'base_sha256':hashlib.sha256(base.read_bytes()).hexdigest(),'delta_video':output.relative_to(ROOT).as_posix(),
                  'delta_video_sha256':hashlib.sha256(output.read_bytes()).hexdigest(),'frames':proof,'width':1280,'height':720,
                  'channels':'RGBA8','base_streams':{'rgb':0,'alpha':1},'all_frames_recovered_exact':True,
                  'decode':'Decode RGB24 and gray alpha tracks from base/delta to RGBA; XOR corresponding frames.'}
        file=destination/(identity+'_rgba_delta.json');file.write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8',newline='\n')
        reports.append({'job':identity,'video':output.relative_to(ROOT).as_posix(),'sha256':manifest['delta_video_sha256'],'native_rgba_exact':True,'frames':len(samples)})
        print('DIAGNOSTIC_RGBA_VIDEO_RETAINED',identity,flush=True)
    (destination/'retention.json').write_text(json.dumps({'status':'REJECTED_TECHNICAL_FRAMING','all_original_rgba_preserved':True,'archives':reports},indent=2)+'\n',encoding='utf-8',newline='\n')


if __name__=='__main__':main()
