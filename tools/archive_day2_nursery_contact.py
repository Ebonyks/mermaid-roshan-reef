"""Preserve every native viewport pixel in a verified lossless study archive.

Prepares a guarded list of redundant own WebP files; performs no deletion.
This is diagnostic storage/encoding, never authored cinematic delivery.
"""
import argparse,datetime,hashlib,json,subprocess
from pathlib import Path
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
FFMPEG=Path('C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/FFmpeg/8.1.2/bin/ffmpeg.exe')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def archive(folder):
    base=(ROOT/folder).resolve()
    allowed=(ROOT/'audit/day2_nursery_contact_20261001').resolve()
    assert base==allowed or base.is_relative_to(allowed)
    removals=[]
    for path in sorted(base.glob('*-?*x720.json')):
        data=json.loads(path.read_text())
        if 'frames' not in data:continue
        id=data['id']; rows=data['frames']; width,height=data['dimensions']
        directory=base/'captures'/id
        (base/'movies').mkdir(exist_ok=True)
        lossless=base/'movies'/f'{id}-lossless.mkv'
        browser=base/'movies'/f'{id}.mp4'
        if not lossless.exists():
            subprocess.run([str(FFMPEG),'-v','error','-framerate',str(data['capture_fps']),'-i',str(directory/'%04d.webp'),'-c:v','libx264rgb','-crf','0','-preset','veryfast','-pix_fmt','rgb24',str(lossless)],check=True)
        if not browser.exists():
            subprocess.run([str(FFMPEG),'-v','error','-i',str(lossless),'-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(browser)],check=True)
        decode=subprocess.Popen([str(FFMPEG),'-v','error','-i',str(lossless),'-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
        keep={0,len(rows)-1}
        for index,row in enumerate(rows):
            prior=rows[max(0,index-1)]
            if row['caught']!=prior['caught'] or row['missed']!=prior['missed'] or row['phase']!=prior['phase']:
                keep.update(range(max(0,index-1),min(len(rows),index+8)))
            if bool(row['transfers'])!=bool(prior['transfers']):keep.add(index)
        proof=[]
        for index,row in enumerate(rows):
            source=base/row['image']
            assert source.resolve().is_relative_to(directory.resolve())
            assert sha(source)==row['sha256'],source
            with Image.open(source) as image:
                if image.mode=='RGBA':assert image.getchannel('A').getextrema()==(255,255)
                original=hashlib.sha256(image.convert('RGB').tobytes()).hexdigest()
            required=width*height*3
            raw=bytearray()
            while len(raw)<required:
                chunk=decode.stdout.read(required-len(raw))
                assert chunk,'Missing decoded frame'
                raw.extend(chunk)
            decoded=hashlib.sha256(raw).hexdigest()
            assert original==decoded,(id,index)
            proof.append({'frame':index,'original_webp_sha256':row['sha256'],'rgb_pixel_sha256':original,'decoded_rgb_sha256':decoded,'retained_native_webp':index in keep})
            if index not in keep:removals.append({'path':source.relative_to(ROOT).as_posix(),'sha256':row['sha256']})
        assert not decode.stdout.read(1),'Unexpected archive frame'
        assert decode.wait()==0
        receipt={'id':id,'archive':lossless.relative_to(base).as_posix(),'archive_sha256':sha(lossless),'browser_video':browser.relative_to(base).as_posix(),'browser_sha256':sha(browser),'frames':proof,'method':'Every decoded RGB pixel matches the opaque native viewport. All native byte hashes retained; no interpolation, retiming or subject repair. This diagnostic archive is not cinematic delivery.','checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'cleanup_performed':False}
        (base/f'{id}-archive-proof.json').write_text(json.dumps(receipt,indent=2)+'\n')
        print(f'NURSERY_ARCHIVE|{id}|{len(proof)} exact native frames|{len(keep)} key WebPs',flush=True)
    (ROOT/'tmp/nursery_contact_redundant_frames.json').write_text(json.dumps({'root':str(ROOT),'folder':folder,'files':removals},indent=2)+'\n')
    print(f'Prepared {len(removals)} redundant own frames; no deletion performed.')

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--folder',default='audit/day2_nursery_contact_20261001')
    archive(parser.parse_args().folder)
