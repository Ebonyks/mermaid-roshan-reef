from pathlib import Path
import json,hashlib,subprocess,struct,uuid
from PIL import Image
p=Path(__file__).resolve().parents[1];tmp=Path(r"H:\MermaidReefTools\LocalVideo\verification")/uuid.uuid4().hex;tmp.mkdir(parents=True)
a=r"C:\Program Files\Aseprite\Aseprite.exe"
ff=r"C:\Users\Peter\AppData\Local\Programs\MermaidReefTools\FFmpeg\8.1.2\bin\ffprobe.exe"
def pixels(f):
 with Image.open(f) as im:return im.size,hashlib.sha256(im.convert("RGBA").tobytes()).hexdigest()
def export(master):
 folder=tmp/master.parent.name/master.stem;folder.mkdir(parents=True,exist_ok=True)
 subprocess.run([a,"-b","--script-param","master="+str(master),"--script-param","destination="+str(folder),"--script",str(p/"scripts/export_native_frames.lua")],check=True,timeout=180)
 return folder
rows=[]
keys=[0,3,7,17,22,27,36,40];d=export(p/"inputs/wave_guides.aseprite")
for n,i in enumerate(keys):assert pixels(d/f"{n:04d}.png")==pixels(p/f"inputs/guide_{i:04d}.png"),(n,i)
rows.append({"artifact":"inputs/wave_guides.aseprite","native_roundtrip_frames":8,"status":"PASS"})
for take in sorted((p/"results").iterdir()):
 if not (take/"receipt.json").exists():continue
 rec=json.loads((take/"receipt.json").read_text());g=json.loads((take/"workflow.api.json").read_text())
 for b in json.loads((take/"input_bindings.json").read_text()):
  h=hashlib.sha256((p/b["path"]).read_bytes()).hexdigest();assert b["sha256"]==h
 assert len([v for v in g.values() if v["class_type"]=="LTXVAddGuide"])==(16 if rec["backend"]=="ltxv2b" else 8)
 if rec["backend"]=="ltxv2b":
  assert g["6"]["inputs"]["width"]==352 and g["6"]["inputs"]["height"]==544
  assert len(g["8"]["inputs"]["sigmas"].split(","))-1==7 and len(g["17"]["inputs"]["sigmas"].split(","))-1==3
  assert g["15"]["class_type"]=="LTXVLatentUpsampler" and g["16"]["class_type"]=="StudyLTXAdaIN"
 if rec["status"]!="EXECUTION_PASS":rows.append({"take":take.name,"execution":rec["status"],"footage":"Absent; no fabricated output"});continue
 folder="refined_native_frames" if rec["backend"]=="ltxv2b" else "native_frames"
 variants=[("native_review.aseprite",folder,list(range(41))),("on_twos.aseprite",folder,list(range(0,41,2)))]
 if rec["backend"]=="ltxv2b":variants += [(v+".aseprite",v+"_frames",list(range(41))) for v in ["stage1","refined_native","requested_canvas"]]
 for master,source,indices in variants:
  out=export(take/master);files=sorted(out.glob("*.png"));assert len(files)==len(indices)
  for n,i in enumerate(indices):assert pixels(files[n])==pixels(take/source/f"{i:04d}.png"),(take.name,master,n)
  rows.append({"artifact":(take/master).relative_to(p).as_posix(),"native_roundtrip_frames":len(indices),"status":"PASS"})
 for video in take.glob("*.mp4"):
  data=json.loads(subprocess.run([ff,"-v","error","-show_streams","-of","json",str(video)],capture_output=True,text=True,check=True).stdout);v=next(x for x in data["streams"] if x["codec_type"]=="video")
  twos=video.stem=="on_twos";assert int(v["nb_frames"])==(21 if twos else 41);assert v["avg_frame_rate"]==("12/1" if twos else "24/1")
  rows.append({"artifact":video.relative_to(p).as_posix(),"frames":int(v["nb_frames"]),"dimensions":[v["width"],v["height"]],"fps":v["avg_frame_rate"],"status":"PASS"})
result={"status":"PASS","checks":rows,"qa_resolution":"Native pixels only; 1:1 contacts; output recipe normalization remains declared separately.","visual_quality_acceptance":False,"runtime_device_child_owner_acceptance":False,"reexport_directory_not_published":str(tmp)}
(p/"environment/trial_verification.json").write_text(json.dumps(result,indent=2)+"\n");print("TRIAL_MACHINE_PASS",len(rows),"checks",flush=True)
