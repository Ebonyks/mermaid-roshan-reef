"""Apply the same bounded Aseprite matte bridge to raw reference footage."""
import argparse,json,hashlib,subprocess,time,tempfile
from pathlib import Path
from PIL import Image
import numpy as np

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
 a=argparse.ArgumentParser();a.add_argument("--packet",type=Path,required=True);a.add_argument("--ffmpeg",type=Path,required=True);a.add_argument("--aseprite",type=Path,required=True);a.add_argument("--scratch",type=Path,required=True);args=a.parse_args()
 args.packet=args.packet.resolve();args.scratch=args.scratch.resolve()
 for receipt in sorted((args.packet/"results").glob("*/*/receipt.json")):
  j=json.loads(receipt.read_text())
  native=next((f for f in [receipt.parent/"native.webm",receipt.parent/"native_0.mp4",receipt.parent/"preview.mp4"] if f.exists()),receipt.parent/"preview.mp4")
  if j.get("status")!="EXECUTION_PASS" or not native.exists():continue
  out=receipt.parent/"aseprite";out.mkdir(exist_ok=True)
  if (out/"bridge_receipt.json").exists():continue
  start=time.monotonic();scratch=args.scratch/receipt.parent.parent.name/receipt.parent.name;scratch.mkdir(parents=True,exist_ok=True)
  subprocess.run([str(args.ffmpeg),"-hide_banner","-loglevel","error","-y","-i",str(native),str(scratch/"raw_%04d.png")],check=True)
  frames=len(list(scratch.glob("raw_*.png")))
  width,height=Image.open(scratch/"raw_0001.png").size
  canvas_width=1<<((width*2-1).bit_length());canvas_height=1<<((height*4-1).bit_length())
  dimensions=["--script-param","width="+str(width),"--script-param","height="+str(height)]
  subprocess.run([str(args.aseprite),"-b","--script-param","directory="+scratch.as_posix(),"--script-param","output="+out.as_posix(),"--script-param","count="+str(frames),*dimensions,"--script",str(args.packet/"cleanup_bridge.lua")],check=True,timeout=900)
  if not (out/"bridge.aseprite").exists() or len(list(scratch.glob("clean_*.png")))!=frames:raise RuntimeError("Aseprite bridge did not preserve frame coverage")
  subprocess.run([str(args.aseprite),"-b","--script-param","directory="+scratch.as_posix(),"--script-param","output="+out.as_posix(),"--script-param","count="+str(frames),*dimensions,"--script-param","canvas_width="+str(canvas_width),"--script-param","canvas_height="+str(canvas_height),"--script",str(args.packet/"pack_bridge.lua")],check=True,timeout=120)
  for page,first in enumerate(range(0,frames,8)):
   cells=[{"native_index":index,"frame":{"x":((index-first)%2)*width,"y":((index-first)//2)*height,"w":width,"h":height},"rotated":False,"trimmed":False,"duration":round((index+1)*1000/24)-round(index*1000/24)} for index in range(first,min(frames,first+8))]
   (out/f"atlas_{page:02d}.json").write_text(json.dumps({"frames":cells,"meta":{"image":f"atlas_{page:02d}.png","size":{"w":canvas_width,"h":canvas_height},"format":"RGBA8888","scale":1,"lane":"REFERENCE_ONLY"}},indent=2)+"\n")
  indices=[]
  for page,first in enumerate(range(0,frames,8)):
   atlas=Image.open(out/f"atlas_{page:02d}.png").convert("RGBA")
   if atlas.size!=(canvas_width,canvas_height):raise RuntimeError("Atlas page is not the declared POT canvas")
   for index in range(first,min(frames,first+8)):
    x=((index-first)%2)*width;y=((index-first)//2)*height
    cell=np.array(atlas.crop((x,y,x+width,y+height)))
    clean=np.array(Image.open(scratch/f"clean_{index+1:04d}.png").convert("RGBA"))
    cell[cell[:,:,3]==0,:3]=0;clean[clean[:,:,3]==0,:3]=0
    if not np.array_equal(cell,clean):raise RuntimeError(f"Atlas altered frame {index}")
    indices.append(index)
  if indices!=list(range(frames)):raise RuntimeError("Atlas duplicated or omitted native indices")
  reopened=Path(tempfile.mkdtemp(prefix="reopen_",dir=scratch))
  subprocess.run([str(args.aseprite),"-b","--script-param","input="+str(out/"bridge.aseprite"),"--script-param","output="+str(reopened),"--script",str(args.packet/"reopen_bridge.lua")],check=True,timeout=120)
  pixel_hashes=[]
  for index in range(frames):
   clean=np.array(Image.open(scratch/f"clean_{index+1:04d}.png").convert("RGBA"))
   restored=np.array(Image.open(reopened/f"reopened_{index+1:04d}.png").convert("RGBA"))
   clean[clean[:,:,3]==0,:3]=0;restored[restored[:,:,3]==0,:3]=0
   if not np.array_equal(clean,restored):raise RuntimeError(f"Master round-trip altered visible pixels at index {index}")
   pixel_hashes.append(hashlib.sha256(clean.tobytes()).hexdigest())
  subprocess.run([str(args.ffmpeg),"-hide_banner","-loglevel","error","-y","-f","lavfi","-i",f"color=c=0xd1d5db:s={width}x{height}:r=24","-framerate","24","-i",str(scratch/"clean_%04d.png"),"-filter_complex","[0:v][1:v]overlay=shortest=1","-frames:v",str(frames),"-c:v","libx264","-crf","18","-pix_fmt","yuv420p",str(out/"bridge_preview.mp4")],check=True)
  data={"status":"DERIVATION_COMPLETE_REFERENCE_ONLY","source_video":native.name,"source_video_sha256":sha(native),"reopen_verification":{"status":"PASS","frames":frames,"method":"Reopen/editable-master native-canvas export vs original cleaned RGBA; fully transparent RGB ignored. Native visible pixels only; filtered sampling not accepted."},"source_frame_count":frames,"atlas_verification":{"pages_pot":True,"unique_native_indices":indices,"visible_rgba_pixel_equality":True},"native_fps":24,"master_timing":"Millisecond boundary rounding: durations 41/42 ms; MP4 re-export samples one cleaned frame per original frame at exact 24 fps.","method":"Aseprite Lua border-connected removal of pixels within 12 RGB levels of shared 238 gray; no crop, registration, geometry repair, motion repair or interpolation","matte_limits":"Residual edge halos and generated shadows require visual review; interior light-painted details preserved by connectivity. Do not accept rejected motion through cleanup.","native_dimensions":[width,height],"canvas_reference_pivot":[width/2,height/2],"runtime_socket_acceptance":False,"elapsed_seconds":round(time.monotonic()-start,3),"source_to_output":[{"index":i-1,"raw_sha256":sha(scratch/f"raw_{i:04d}.png"),"clean_rgba_sha256":sha(scratch/f"clean_{i:04d}.png"),"visible_rgba_pixel_sha256":pixel_hashes[i-1]} for i in range(1,frames+1)],"outputs":[{"path":p.name,"sha256":sha(p),"bytes":p.stat().st_size} for p in sorted(out.iterdir()) if p.is_file()]}
  (out/"bridge_receipt.json").write_text(json.dumps(data,indent=2)+"\n")
  print(receipt.parent.parent.name,receipt.parent.name,"ASEPRITE_BRIDGE",data["elapsed_seconds"],flush=True)
if __name__=="__main__":main()
