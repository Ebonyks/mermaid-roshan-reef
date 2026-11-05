"""Archive every retained run; package the two final costumes with the original exporter."""
from pathlib import Path
import hashlib,json,os,subprocess,sys,importlib.util,shutil
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
os.environ['PATH']='C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/FFmpeg/8.1.2/bin;'+os.environ['PATH']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 for folder in sorted(p for p in (ROOT/'evidence').glob('render_*') if p.is_dir()):
  for clip in ['arm_bend','blink','tail_bend']:
   frames=sorted((folder/clip).glob('*.png'));archive=folder/f'{clip}_rgba.mkv'
   if not frames:continue
   if not archive.exists():
    subprocess.run(['ffmpeg','-y','-v','error','-framerate','30','-i',str(folder/clip/'%04d.png'),'-filter_complex','[0:v]split=2[c][a];[c]format=rgb24[color];[a]alphaextract[alpha]','-map','[color]','-map','[alpha]','-c:v:0','libx264rgb','-crf:v:0','0','-preset:v:0','veryfast','-c:v:1','ffv1','-level:v:1','3','-pix_fmt:v:1','gray',str(archive)],check=True)
   decoded=subprocess.run(['ffmpeg','-v','error','-i',str(archive),'-filter_complex','[0:v:0][0:v:1]alphamerge[out]','-map','[out]','-pix_fmt','rgba','-f','framemd5','-'],capture_output=True,text=True,check=True)
   hashes=[s.split(',')[-1].strip() for s in decoded.stdout.splitlines() if s.strip() and not s.startswith('#')]
   originals=[{'frame':int(p.stem),'png_sha256':sha(p),'rgba_md5':hashlib.md5(Image.open(p).convert('RGBA').tobytes()).hexdigest()} for p in frames]
   exact=len(hashes)==len(originals) and all(a==b['rgba_md5'] for a,b in zip(hashes,originals))
   record={'archive':archive.name,'archive_sha256':sha(archive),'codec':'lossless H264 RGB + FFV1 alpha; reconstruct with alphamerge','native_frame_count':len(frames),'pixel_roundtrip_exact':exact,'frames':originals,'limits':'RGBA pixels exact; native PNG containers retained locally, not in this archive. v1-v7 are partial/intermediate/rejected; v8 is the current actual-garment candidate, not owner acceptance.'}
   (folder/f'{clip}_archive.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
   if not exact:raise RuntimeError('ARCHIVE_PIXEL_MISMATCH '+str(folder))
   print('ARCHIVE_OK',folder.name,clip,len(frames),flush=True)
 spec=importlib.util.spec_from_file_location('review',ROOT/'scripts/package_review.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
 for theme in ['ballet','magician']:
  sys.argv=['package_review.py','--revision',f'render_{theme}_v8'];mod.main()
  target=ROOT/'review'/theme;target.mkdir(exist_ok=True)
  for p in list((ROOT/'review').iterdir()):
   if p.is_file() and p.suffix in ['.mp4','.jpg'] and (p.name=='three_studies.mp4' or any(p.name.startswith(c) for c in ['arm_bend','blink','tail_bend'])):shutil.move(str(p),str(target/p.name))
 print('COSTUME_REVIEW_PACKAGE_OK',flush=True)
if __name__=='__main__':main()
