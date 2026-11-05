"""Verify frozen review exports and make sampled full-figure boards, without changing art."""
from pathlib import Path
import hashlib,json,subprocess
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1]
FF=Path('C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/FFmpeg/8.1.2/bin')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 boards=[]
 for theme in ['ballet','magician']:
  for clip,count in [('arm_bend',97),('blink',73),('tail_bend',121)]:
   indices=[0,(count-1)//4,(count-1)//2,3*(count-1)//4,count-1]
   board=Image.new('RGB',(1800,400),(232,238,246));draw=ImageDraw.Draw(board)
   for j,index in enumerate(indices):
    p=R/f'evidence/render_{theme}_v8'/clip/f'{index:04}.png'
    tile=Image.new('RGBA',(1024,1024),(245,245,245,255));tile.alpha_composite(Image.open(p).convert('RGBA'))
    board.paste(tile.convert('RGB').resize((360,360),Image.Resampling.LANCZOS),(360*j,20));draw.text((360*j+8,382),f'{theme} {clip} {index:04}',fill=(20,30,45))
   p=R/'review'/theme/f'{clip}_full_figure.jpg';board.save(p,quality=97);boards.append({'path':p.relative_to(R).as_posix(),'sha256':sha(p),'frames':indices})
 movies=[]
 for p in sorted((R/'review').rglob('*.mp4')):
  proc=subprocess.run([str(FF/'ffprobe.exe'),'-v','error','-show_streams','-show_format','-of','json',str(p)],capture_output=True,text=True,check=True,timeout=30)
  d=json.loads(proc.stdout);streams=d['streams'];v=next(x for x in streams if x['codec_type']=='video')
  geometry=v['width']==1280 and v['height']==720 and v.get('sample_aspect_ratio')=='1:1' and v.get('display_aspect_ratio')=='16:9'
  no_rotation=not any(x.get('rotation',0)!=0 for x in v.get('side_data_list',[])) and v.get('tags',{}).get('rotate','0')=='0'
  decode=subprocess.run([str(FF/'ffmpeg.exe'),'-v','error','-threads','2','-i',str(p),'-f','null','-'],stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,timeout=180)
  row={'path':p.relative_to(R).as_posix(),'sha256':sha(p),'width':v['width'],'height':v['height'],'sar':v.get('sample_aspect_ratio'),'dar':v.get('display_aspect_ratio'),'duration':d['format'].get('duration'),'frame_rate':v['avg_frame_rate'],'no_rotation':no_rotation,'decode_exit':decode.returncode,'decode_errors':decode.stderr.decode(errors='replace'),'pass':geometry and no_rotation and decode.returncode==0 and not decode.stderr}
  movies.append(row);print('REVIEW_DECODE',row['pass'],row['path'],flush=True)
 archives=[]
 for theme in ['ballet','magician','original']:
  for clip,count in [('arm_bend',97),('blink',73),('tail_bend',121)]:
   folder=R/f'evidence/render_{theme}_v8';d=json.loads((folder/f'{clip}_archive.json').read_text());archive=folder/f'{clip}_rgba.mkv'
   good=d['pixel_roundtrip_exact'] and d['native_frame_count']==count and d['archive_sha256']==sha(archive)
   archives.append({'path':archive.relative_to(R).as_posix(),'pass':good,'frames':d['native_frame_count']})
 swaps=json.loads((R/'evidence/swaps_v8/snapshot_archive.json').read_text());swap_good=swaps['pass'] and swaps['decoded_frames']==81 and swaps['archive_sha256']==sha(R/'evidence/swaps_v8/snapshot_rgba.mkv')
 report={'candidate':'render_v8','pass':all(x['pass'] for x in movies+archives) and len(boards)==6 and swap_good,'movies':movies,'archives':archives,'swap_archive_81_exact':swap_good,'full_figure_boards':boards,'scope':'Machine decode/geometry and exact archive receipts, plus sampled static full-figure boards. No normal-speed human, phone, child or owner acceptance.'}
 (R/'evidence/media_verification_v7.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print('MEDIA_VERIFY',report['pass'],len(movies),flush=True);raise SystemExit(0 if report['pass'] else 1)
if __name__=='__main__':main()
