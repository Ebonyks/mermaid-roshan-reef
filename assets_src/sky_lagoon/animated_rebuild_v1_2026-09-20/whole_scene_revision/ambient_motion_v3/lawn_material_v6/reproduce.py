from pathlib import Path
import argparse,subprocess,shutil,json,hashlib,io,zipfile,xml.etree.ElementTree as ET
import numpy as np
from PIL import Image
parser=argparse.ArgumentParser(description='Reproduce bounded whole-lawn Aseprite cels in a separate directory.');parser.add_argument('--output',type=Path,required=True);args=parser.parse_args();source=Path(__file__).resolve().parent;out=args.output.resolve();assert out!=source,'Use a separate output directory';out.mkdir(parents=True,exist_ok=True);manifest=json.loads((source/'MANIFEST.json').read_text());results=[]
for region in manifest['regions']:
 ident=region['id'];original=source/ident;dest=out/ident;dest.mkdir(exist_ok=True)
 for name in ['rest.png','motion-mask.png']:shutil.copyfile(original/name,dest/name)
 run=subprocess.run(['C:/Program Files/Aseprite/Aseprite.exe','-b','--script-param','out='+str(dest),'--script',str(source/'author.lua')],capture_output=True,text=True,creationflags=subprocess.CREATE_NO_WINDOW,timeout=180);assert run.returncode==0,run.stderr;(dest/'aseprite.log').write_text(run.stdout+run.stderr)
 mask=Image.open(dest/'motion-mask.png').convert('L');matches=[]
 for k in range(4):
  cel=Image.open(dest/f'cel-{k}.png').convert('RGBA');assert np.array_equal(np.asarray(cel),np.asarray(Image.open(original/f'cel-{k}.png').convert('RGBA')))
  cel.putalpha(mask);cel.save(dest/f'overlay-{k}.png');matches.append(np.array_equal(np.asarray(cel),np.asarray(Image.open(original/f'overlay-{k}.png').convert('RGBA'))))
 with zipfile.ZipFile(original/'lawn-four-pose-groups.ora') as z:
  layers=ET.fromstring(z.read('stack.xml')).findall('.//layer');assert len(layers)==4
  for layer in layers:
   k=int(layer.attrib['src'].split('pose')[-1].split('.')[0]);assert np.array_equal(np.asarray(Image.open(io.BytesIO(z.read(layer.attrib['src']))).convert('RGBA')),np.asarray(Image.open(original/f'overlay-{k}.png').convert('RGBA')))
 assert all(matches);results.append({'id':ident,'four_native_cels_exact':True,'four_masked_overlays_exact':True,'four_krita_pose_layers_match':True});print(ident+' PASS',flush=True)
(out/'RESULT.json').write_text(json.dumps({'status':'SOURCE_REPRODUCTION_PASS','regions':results},indent=2)+'\n')
