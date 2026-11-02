"""Transcode failed opaque ZIP transport to explicit lossless 2D video.

No renamed archive or gate change. Decode every numeric delta, encode actual
video frames, decode again and verify both delta and reconstructed native RGBA.
"""
import hashlib
import json
import zipfile
import numpy as np
from rgba_delta_video import ROOT,encode_rgba,decode_rgba


def main():
    directory=ROOT/'evidence/history/framing_preflight';reports=[]
    for identity in ['ballet','magician','live_swaps']:
        original=directory/(identity+'_rgba_delta.zip');output=directory/(identity+'_rgba_delta.mkv')
        with zipfile.ZipFile(original) as packed:
            old=json.loads(packed.read('manifest.json'));count=len(old['frames'])
            encode_rgba(output,(packed.read(f['entry']) for f in old['frames']),count)
            base=ROOT/old['base_archive'];assert hashlib.sha256(base.read_bytes()).hexdigest()==old['base_sha256']
            verified=[]
            for target,delta,frame in zip(decode_rgba(base,count),decode_rgba(output,count),old['frames'],strict=True):
                assert delta.tobytes()==packed.read(frame['entry'])
                assert hashlib.sha256(np.bitwise_xor(target,delta).tobytes()).hexdigest()==frame['rgba_sha256']
                verified.append({'index':frame['index'],'native_png_sha256':frame['native_png_sha256'],'rgba_sha256':frame['rgba_sha256']})
        manifest={**old,'format':'roshan.rgba-xor-video/1','delta_video':output.relative_to(ROOT).as_posix(),
                  'delta_video_sha256':hashlib.sha256(output.read_bytes()).hexdigest(),'frames':verified,
                  'decode':'Decode base/delta RGB24 and gray alpha tracks to RGBA8; XOR corresponding frames byte-for-byte.',
                  'original_staging_zip_sha256':hashlib.sha256(original.read_bytes()).hexdigest(),
                  'transport_change':'Actual 2D video frames; no opaque archive members; all delta and reconstructed native pixels verified exact.'}
        destination=directory/(identity+'_rgba_delta.json');destination.write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8',newline='\n')
        reports.append({'job':identity,'old_zip':original.name,'old_zip_sha256':manifest['original_staging_zip_sha256'],
                        'video':output.relative_to(ROOT).as_posix(),'bytes':output.stat().st_size,'sha256':manifest['delta_video_sha256'],
                        'manifest':destination.relative_to(ROOT).as_posix(),'all_delta_and_native_pixels_exact':True,'frames':count})
        print('DIAGNOSTIC_2D_VIDEO_EXACT',identity,count,output.stat().st_size,flush=True)
    (directory/'video_conversion.json').write_text(json.dumps({'pass':True,'gates_unchanged':True,'reports':reports},indent=2)+'\n',encoding='utf-8',newline='\n')
    retention=json.loads((directory/'retention.json').read_text());retention['archives']=reports;retention['storage_format']='Explicit lossless RGB/alpha XOR video; native data exact against named base. ZIP staging bytes replaced after verification.';(directory/'retention.json').write_text(json.dumps(retention,indent=2)+'\n',encoding='utf-8',newline='\n')


if __name__=='__main__':main()
