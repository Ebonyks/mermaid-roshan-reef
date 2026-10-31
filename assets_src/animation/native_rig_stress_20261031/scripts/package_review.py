"""Retain exact rendered pixels in lossless archives and make portable review movies."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
from PIL import Image,ImageDraw

ROOT=Path(__file__).resolve().parents[1]
CLIPS=['arm_bend','blink','tail_bend']


def run(args):
    subprocess.run(args,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--revision',default='render_v10');parser.add_argument('--rejects',action='store_true');args=parser.parse_args()
    revisions=sorted([p for p in (ROOT/'evidence').glob('render_v*') if p.is_dir()],key=lambda p:int(p.name.split('_v')[-1])) if args.rejects else [ROOT/'evidence'/args.revision]
    for folder in revisions:
        if not (folder/'engine_receipt.json').exists():continue
        for clip in CLIPS:
            frames=sorted((folder/clip).glob('*.png'))
            archive=folder/f'{clip}_rgba.mkv'
            if not archive.exists():
                run(['ffmpeg','-y','-v','error','-framerate','30','-i',str(folder/clip/'%04d.png'),'-filter_complex','[0:v]split=2[c][a];[c]format=rgb24[color];[a]alphaextract[alpha]','-map','[color]','-map','[alpha]','-c:v:0','libx264rgb','-crf:v:0','0','-preset:v:0','veryfast','-c:v:1','ffv1','-level:v:1','3','-pix_fmt:v:1','gray',str(archive)])
            decoded=subprocess.run(['ffmpeg','-v','error','-i',str(archive),'-filter_complex','[0:v:0][0:v:1]alphamerge[out]','-map','[out]','-pix_fmt','rgba','-f','framemd5','-'],capture_output=True,text=True,check=True)
            hashes=[line.split(',')[-1].strip() for line in decoded.stdout.splitlines() if not line.startswith('#') and line.strip()]
            originals=[]
            for p in frames:
                pixels=Image.open(p).convert('RGBA').tobytes()
                originals.append({'frame':int(p.stem),'png_sha256':sha(p),'rgba_sha256':hashlib.sha256(pixels).hexdigest(),'rgba_md5':hashlib.md5(pixels).hexdigest()})
            exact=len(hashes)==len(originals) and all(a==b['rgba_md5'] for a,b in zip(hashes,originals))
            record={'archive':archive.name,'archive_sha256':sha(archive),'codec':'Matroska: lossless H264 RGB stream 0 + lossless FFV1 grayscale alpha stream 1, 30 fps; reconstruct with alphamerge','native_frame_count':len(frames),'decoded_frames':len(hashes),'pixel_roundtrip_exact':exact,'native_pngs_local_preserved':True,'native_png_bytes_in_archive':False,'frames':originals}
            (folder/f'{clip}_archive.json').write_text(json.dumps(record,indent=2)+'\n')
            if not exact:raise RuntimeError(f'LOSSLESS_ROUNDTRIP_FAIL {folder.name}/{clip}')
            print(f'PIXEL_ARCHIVE_OK {folder.name}/{clip} frames={len(frames)} bytes={archive.stat().st_size}',flush=True)
    final=ROOT/'evidence'/args.revision
    review=ROOT/'review';review.mkdir(exist_ok=True)
    for clip in CLIPS:
        archive=final/f'{clip}_rgba.mkv'
        # Flatten once onto a fixed neutral field, with no camera or character edits.
        graph='color=c=0x18202b:s=1280x720:r=30[bg];[0:v:0][0:v:1]alphamerge,scale=720:720:flags=lanczos[fg];[bg][fg]overlay=280:0:shortest=1,format=yuv420p[out]'
        run(['ffmpeg','-y','-v','error','-i',str(archive),'-filter_complex',graph,'-map','[out]','-an','-c:v','libx264','-crf','16','-preset','fast','-movflags','+faststart',str(review/f'{clip}.mp4')])
        run(['ffmpeg','-y','-v','error','-i',str(review/f'{clip}.mp4'),'-vf','setpts=2*PTS','-an','-c:v','libx264','-crf','16','-preset','fast','-movflags','+faststart',str(review/f'{clip}_slow.mp4')])
    # 18-second simultaneous comparison. Source archives include the final sampled endpoint.
    inputs=[]
    for clip in CLIPS:inputs+=['-stream_loop','-1','-i',str(final/f'{clip}_rgba.mkv')]
    graph='color=c=0xe6ebf2:s=1280x720:r=30[bg];[0:v:0][0:v:1]alphamerge,scale=420:420:flags=lanczos[a];[1:v:0][1:v:1]alphamerge,scale=420:420:flags=lanczos[b];[2:v:0][2:v:1]alphamerge,scale=420:420:flags=lanczos[c];[bg][a]overlay=0:140[t1];[t1][b]overlay=430:140[t2];[t2][c]overlay=860:140,format=yuv420p[out]'
    run(['ffmpeg','-y','-v','error',*inputs,'-filter_complex',graph,'-map','[out]','-t','18','-an','-c:v','libx264','-crf','16','-preset','fast','-movflags','+faststart',str(review/'three_studies.mp4')])
    # Every frame is available chronologically on close-up pages for static agent review.
    for clip in CLIPS:
        frames=sorted((final/clip).glob('*.png'))
        crop={'arm_bend':(260,320,545,540),'blink':(470,195,620,295),'tail_bend':(190,450,700,875)}[clip]
        for start in range(0,len(frames),24):
            board=Image.new('RGB',(1440,1120),(225,231,239));draw=ImageDraw.Draw(board)
            for j,p in enumerate(frames[start:start+24]):
                src=Image.open(p).convert('RGBA').crop(crop)
                tile=Image.new('RGBA',src.size,(245,245,245,255));tile.alpha_composite(src)
                tile.thumbnail((350,245),Image.Resampling.LANCZOS)
                x=(j%4)*360;y=(j//4)*185
                if tile.height>160:tile=tile.resize((round(tile.width*160/tile.height),160),Image.Resampling.LANCZOS)
                board.paste(tile.convert('RGB'),(x,y));draw.text((x+5,y+165),f'{clip} frame {p.stem}',fill=(20,25,30))
            board.save(review/f'{clip}_detail_{start//24+1:02}.jpg',quality=95)
    print('REVIEW_PACKAGE_OK',flush=True)


if __name__=='__main__':main()
