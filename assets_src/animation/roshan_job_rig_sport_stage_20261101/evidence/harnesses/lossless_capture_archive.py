from pathlib import Path
import subprocess,json,hashlib,time
from PIL import Image
R=Path(__file__).resolve().parents[2];raw=R/'evidence/verification_v3/action_repeatability_raw';out=R/'review/frozen_v3';ff='C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/FFmpeg/8.1.2/bin/ffmpeg.exe';rows=[]
for theme in ['boxer','racer','popstar']:
 dest=out/(theme+'_native_rgba.mkv');args=[ff,'-hide_banner','-y','-framerate','30','-start_number','0','-i',str(raw/(theme+'_%04d.png')),'-filter_complex','[0:v]split=2[a][b];[a]format=rgb24[rgb];[b]alphaextract,format=gray[alpha]','-map','[rgb]','-map','[alpha]','-frames:v:0','241','-frames:v:1','241','-c:v:0','libx264rgb','-preset:v:0','medium','-crf:v:0','0','-pix_fmt:v:0','rgb24','-threads:v:0','2','-c:v:1','libx264','-preset:v:1','medium','-crf:v:1','0','-pix_fmt:v:1','gray','-threads:v:1','2','-metadata:s:v:0','title=Native RGB bytes','-metadata:s:v:1','title=Native alpha bytes; reconstruction track','-an',str(dest)];start=time.monotonic();p=subprocess.run(args,capture_output=True,text=True,timeout=300);(out/(theme+'_lossless_encode.log')).write_text(p.stdout+p.stderr);row={'path':dest.relative_to(R).as_posix(),'encoder_args':args,'encode_exit':p.returncode,'encoding_seconds':round(time.monotonic()-start,2),'frames':[]}
 if p.returncode==0:
  decode=[ff,'-hide_banner','-loglevel','error','-i',str(dest),'-filter_complex','[0:v:0][0:v:1]alphamerge,format=rgba[v]','-map','[v]','-f','rawvideo','-pix_fmt','rgba','pipe:1'];err=out/(theme+'_lossless_decode.log')
  with err.open('wb') as stream:
   proc=subprocess.Popen(decode,stdout=subprocess.PIPE,stderr=stream)
   for i in range(241):
    data=proc.stdout.read(1024*1024*4);source=Image.open(raw/f'{theme}_{i:04d}.png').convert('RGBA').tobytes();row['frames'].append({'frame':i,'source_rgba_sha256':hashlib.sha256(source).hexdigest(),'decoded_rgba_sha256':hashlib.sha256(data).hexdigest(),'pass':data==source})
   extra=proc.stdout.read(1);proc.stdout.close();code=proc.wait(timeout=60)
  row['decode_exit']=code;row['extra_decoded_bytes']=len(extra);row['decoder_args']=decode;row['sha256']=hashlib.sha256(dest.read_bytes()).hexdigest();row['bytes']=dest.stat().st_size;row['pass']=code==0 and not extra and all(x['pass'] for x in row['frames']) and row['bytes']<50*1024*1024
 else:row['pass']=False
 rows.append(row);(out/'lossless_archive_receipt.json').write_text(json.dumps({'scope':'Two archival video tracks hold original8bit RGB and alpha. Acceptance requires reconstruction of ALL native RGBA bytes in ALL241frames per action; no colour/range or hidden-alpha difference waived. Review MP4 is separate.','rows':rows,'complete':len(rows)==3,'pass':len(rows)==3 and all(x['pass'] for x in rows)},indent=2)+'\n');print(theme,'RGBA archive',row['pass'],row.get('bytes'),flush=True)
