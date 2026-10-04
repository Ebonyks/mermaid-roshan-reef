#!/usr/bin/env python3
"""Losslessly isolate existing racing source views; never redraw source artwork."""
from pathlib import Path
from collections import deque
import hashlib
import json
from PIL import Image
ROOT = Path(__file__).resolve().parents[1]
SOURCE = "assets_src/concepts/cc0_ocean_replacements_2026-07-22/regen_02_03_vehicles.png"
BOXES = {
 "kart_front": (0,150,277,458), "kart_side": (278,150,675,457),
 "kart_rear": (675,150,947,460), "kart_top": (945,40,1183,461),
 "kart_quarter": (1182,150,1536,465), "moto_front": (0,485,253,939),
 "moto_side": (250,485,681,923), "moto_rear": (681,485,925,931),
 "moto_top": (930,480,1185,944), "moto_quarter": (1180,485,1536,944),
}
def digest(data): return hashlib.sha256(data).hexdigest()
def isolate(image, box):
 crop = image.crop(box).convert("RGBA")
 width,height = crop.size
 pixels = crop.load()
 visited = set()
 queue = deque([(x,0) for x in range(width)] + [(x,height-1) for x in range(width)] + [(0,y) for y in range(height)] + [(width-1,y) for y in range(height)])
 while queue:
  x,y = queue.popleft()
  if (x,y) in visited or not (0 <= x < width and 0 <= y < height): continue
  visited.add((x,y))
  r,g,b,a = pixels[x,y]
  if r < 225 or g < 220 or b < 185 or r-b < 8 or r < g-3: continue
  pixels[x,y] = (r,g,b,0)
  queue.extend([(x-1,y),(x+1,y),(x,y-1),(x,y+1)])
 bbox = crop.getchannel("A").getbbox()
 tight = crop.crop(bbox)
 result = Image.new("RGBA",(512,512))
 result.paste(tight,((512-tight.width)//2,(512-tight.height)//2))
 return result,bbox

def main():
 import argparse
 parser=argparse.ArgumentParser();parser.add_argument("--check",action="store_true");args=parser.parse_args()
 source=ROOT/SOURCE; image=Image.open(source)
 output=ROOT/"assets/kart/canvas";output.mkdir(parents=True,exist_ok=True)
 rows=[]
 for key,box in BOXES.items():
  derived,bbox=isolate(image,box);path=output/(key+".png")
  if args.check:
   if not path.exists() or Image.open(path).convert("RGBA").tobytes()!=derived.tobytes(): raise SystemExit("KARTART|FAIL|"+key)
  else: derived.save(path)
  rows.append({"path":path.relative_to(ROOT).as_posix(),"sha256":digest(path.read_bytes()),"dimensions":[512,512],"source":SOURCE,"source_sha256":digest(source.read_bytes()),"source_crop":list(box),"alpha_bbox_in_crop":list(bbox),"modification":"border-connected cream matte removal; tight crop; centred transparent POT padding; retained RGB source pixels, no redraw or resampling","role":"existing directional vehicle source candidate","acceptance":"source reuse; visual/owner acceptance pending"})
 manifest={"method":"deterministic_source_isolation","source_preserved":True,"files":rows,"gaps":["Truck has no accepted directional 2D source; flat Canvas silhouette is a development candidate only.","Course raster master is 1672x941, below native per-screen 2K; this port uses native Canvas road geometry, not an upscaled raster."]}
 target=ROOT/"assets_src/kart_canvas_2d_20261003/provenance.json"
 if args.check:
  if json.loads(target.read_text())!=manifest: raise SystemExit("KARTART|FAIL|manifest")
 else:
  target.parent.mkdir(parents=True,exist_ok=True);target.write_text(json.dumps(manifest,indent=2)+"\n")
 print("KARTART|ALL OK|10 reused views; no generation")
if __name__=="__main__": main()
