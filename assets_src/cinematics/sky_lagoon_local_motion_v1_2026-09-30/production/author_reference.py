import argparse,json,subprocess,hashlib
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parent
ASE=Path('C:/Program Files/Aseprite/Aseprite.exe')
def run(id):
 folder=ROOT/'authored'/id;(folder/'frames').mkdir(exist_ok=True)
 p=subprocess.run([str(ASE),'--batch','--script-param','root='+folder.as_posix(),'--script-param','id='+id,'--script',str(ROOT/'author_motion.lua')],capture_output=True,text=True,check=True)
 print(p.stdout,flush=True)
 master=folder/(id+'.aseprite')
 subprocess.run([str(ASE),'--batch',str(master),'--sheet',str(folder/'spritesheet.png'),'--sheet-type','rows','--sheet-columns','8','--sheet-width','2048','--sheet-height','1024','--data',str(folder/'spritesheet.json'),'--format','json-array'],capture_output=True,text=True,check=True)
 images=[Image.open(p).convert('RGBA') for p in sorted((folder/'frames').glob('*.png'))]
 preview=[]
 for im in images:
  bg=Image.new('RGBA',im.size,(231,238,242,255));bg.alpha_composite(im);preview.append(bg.convert('RGB'))
 # GIF uses its native centisecond precision; timings alternate 80/90 ms to preserve the 12fps cycle.
 times=[80 if n%3!=2 else 90 for n in range(32)]
 preview[0].save(folder/'preview.gif',save_all=True,append_images=preview[1:],duration=times,loop=0,disposal=2)
 selected=[0,4,8,12,16,20,24,28]
 board=Image.new('RGB',(1024,576),(231,238,242));d=ImageDraw.Draw(board);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',16)
 for j,n in enumerate(selected):
  x=j%4*256;y=j//4*288;board.paste(images[n],(x,y),images[n]);d.text((x+8,y+263),f'Pose {n:02d}',font=font,fill=(36,48,70))
 board.save(folder/'pose_board.png')
 # Reopen and export the editable file: independent exact pixel round trip.
 rt=folder/'roundtrip';rt.mkdir(exist_ok=True)
 subprocess.run([str(ASE),'--batch',str(master),'--save-as',str(rt/'pose{frame}.png')],capture_output=True,text=True,check=True)
 exported=sorted(rt.glob('*.png'),key=lambda p:int(p.stem.replace('pose','')))
 assert len(exported)==32
 for n,p in enumerate(exported):assert Image.open(p).convert('RGBA').tobytes()==images[n].tobytes(),(id,n)
 receipt=json.loads((folder/'AUTHORING_RECEIPT.json').read_text());receipt['exact_round_trip']='PASS'
 receipt['authoring_script_sha256']=hashlib.sha256((ROOT/'author_motion.lua').read_bytes()).hexdigest()
 receipt['source_derivative_sha256']=hashlib.sha256((folder/'source.png').read_bytes()).hexdigest()
 (folder/'AUTHORING_RECEIPT.json').write_text(json.dumps(receipt,indent=2),encoding='utf-8')
 print(id+' editable 32-pose Aseprite exact round trip PASS',flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('id');run(p.parse_args().id)
