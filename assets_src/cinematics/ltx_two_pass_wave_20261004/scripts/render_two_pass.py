"""Bounded source-study Comfy reproduction of the pinned official 2B multiscale recipe."""
from pathlib import Path
import argparse,json,urllib.request,urllib.error,hashlib,shutil,time,uuid,subprocess
from datetime import datetime,timezone
P=Path(__file__).resolve().parents[1];DATA=Path(r"H:\MermaidReefTools\LocalVideo");BASE="http://127.0.0.1:8192"
def request(path,data=None):
 b=None if data is None else json.dumps(data).encode()
 with urllib.request.urlopen(urllib.request.Request(BASE+path,data=b,headers={"Content-Type":"application/json"}),timeout=30) as f:return json.load(f)
def sha(p):
 with Path(p).open("rb") as f:return hashlib.file_digest(f,"sha256").hexdigest()
def add(g,k,typ,**inputs):g[str(k)]={"class_type":typ,"inputs":inputs};return str(k)
def graph(take,strength):
 g={};bindings=[];loads={}
 add(g,1,"CheckpointLoaderSimple",ckpt_name="ltxv-2b-0.9.8-distilled.safetensors")
 add(g,2,"CLIPLoader",clip_name="t5xxl_fp8_e4m3fn.safetensors",type="ltxv",device="cpu")
 prompt=(P/"briefs/wave_prompt.txt").read_text()
 add(g,3,"CLIPTextEncode",clip=["2",0],text=prompt)
 add(g,4,"ConditioningZeroOut",conditioning=["3",0])
 add(g,5,"LTXVConditioning",positive=["3",0],negative=["4",0],frame_rate=24)
 # Official literal0.6666666 floors requested576x832 to352x544 on a32px lattice.
 add(g,6,"EmptyLTXVLatentVideo",width=352,height=544,length=41,batch_size=1)
 if strength>1.0:
  src=P/"inputs/white_attention.png";name="two_pass_"+sha(src)+".png";dst=DATA/"input"/name
  if not dst.exists():shutil.copyfile(src,dst)
  assert sha(dst)==sha(src)
  add(g,28,"LoadImage",image=name);add(g,29,"ImageToMask",image=["28",0],channel="red")
 for n,idx in enumerate([0,3,7,17,22,27,36,40]):
  src=P/f"inputs/guide_{idx:04d}.png";h=sha(src);name="two_pass_"+h+".png";dst=DATA/"input"/name
  if not dst.exists():shutil.copyfile(src,dst)
  assert sha(dst)==h
  bindings.append({"guide_index":idx,"path":src.relative_to(P).as_posix(),"sha256":h,"bound_path":str(dst),"strength":strength if idx==22 else 1.0})
  if h not in loads:
   loads[h]=add(g,20+n,"LoadImage",image=name)
  bindings[-1]["load_node"]=loads[h]
 def guides(base_id,latent,w,h):
  pos=["5",0];neg=["5",1]
  for n,b in enumerate(bindings):
   k=add(g,base_id+n,"LTXVAddGuide",positive=pos,negative=neg,vae=["1",2],latent=latent,image=[b["load_node"],0],frame_idx=b["guide_index"],strength=b["strength"])
   if strength>1.0 and b["guide_index"]==22:g[k]["inputs"]["attention_mask"]=["29",0]
   pos=[k,0];neg=[k,1];latent=[k,2]
  return pos,neg,latent
 add(g,7,"KSamplerSelect",sampler_name="euler")
 add(g,8,"ManualSigmas",sigmas="1,0.9937,0.9875,0.9812,0.9750,0.9094,0.7250,0")
 pos,neg,lat=guides(100,["6",0],352,544)
 add(g,9,"SamplerCustom",model=["1",0],add_noise=True,noise_seed=20261004,cfg=1.0,positive=pos,negative=neg,sampler=["7",0],sigmas=["8",0],latent_image=lat)
 add(g,10,"LTXVCropGuides",positive=pos,negative=neg,latent=["9",0])
 add(g,11,"SaveLatent",samples=["10",2],filename_prefix=f"two_pass/{take}/stage1_latent")
 add(g,12,"VAEDecodeTiled",samples=["10",2],vae=["1",2],tile_size=256,overlap=64,temporal_size=64,temporal_overlap=8)
 add(g,13,"SaveImage",images=["12",0],filename_prefix=f"two_pass/{take}/stage1/frame")
 add(g,14,"LatentUpscaleModelLoader",model_name="ltxv-spatial-upscaler-0.9.8.safetensors")
 add(g,15,"LTXVLatentUpsampler",samples=["10",2],upscale_model=["14",0],vae=["1",2])
 add(g,16,"StudyLTXAdaIN",samples=["15",0],reference=["10",2])
 add(g,17,"ManualSigmas",sigmas="0.9094,0.7250,0.4219,0")
 pos2,neg2,lat2=guides(200,["16",0],704,1088)
 add(g,18,"SamplerCustom",model=["1",0],add_noise=True,noise_seed=20261004,cfg=1.0,positive=pos2,negative=neg2,sampler=["7",0],sigmas=["17",0],latent_image=lat2)
 add(g,19,"LTXVCropGuides",positive=pos2,negative=neg2,latent=["18",0])
 add(g,30,"SaveLatent",samples=["19",2],filename_prefix=f"two_pass/{take}/refined_latent")
 add(g,31,"VAEDecodeTiled",samples=["19",2],vae=["1",2],tile_size=256,overlap=64,temporal_size=64,temporal_overlap=8)
 add(g,32,"SaveImage",images=["31",0],filename_prefix=f"two_pass/{take}/refined_native/frame")
 # Official final whole-canvas post-decode resize; native704x1088 is retained above.
 add(g,33,"ImageScale",image=["31",0],upscale_method="bilinear",width=576,height=832,crop="disabled")
 add(g,34,"SaveImage",images=["33",0],filename_prefix=f"two_pass/{take}/requested_canvas/frame")
 return g,bindings

def main():
 a=argparse.ArgumentParser();a.add_argument("take",choices=["official_standard","official_mid_strong"]);args=a.parse_args();take=args.take
 if (P/"results"/take/"receipt.json").exists():raise SystemExit("Existingattempt; no silent repeat or overwrite")
 old=[json.loads(x.read_text()) for x in (P/"results").glob("*/receipt.json")]
 if len(old)>=6 or sum(x.get("backend")=="ltxv2b" for x in old)>=2:raise SystemExit("Trialcap reached")
 # Readiness/schema checks happen before a model submission; no job queued here.
 schema=request("/object_info");queue=request("/queue");assert not queue["queue_running"] and not queue["queue_pending"],"Existing queue left untouched"
 g,bindings=graph(take,1.25 if take.endswith("strong") else 1.0)
 for k,node in g.items():
  assert node["class_type"] in schema,node["class_type"]
  for name in schema[node["class_type"]]["input"].get("required",{}):assert name in node["inputs"],(k,name)
 out=P/"results"/take;out.mkdir(parents=True,exist_ok=True)
 (out/"workflow.api.json").write_text(json.dumps(g,indent=2)+"\n")
 (out/"input_bindings.json").write_text(json.dumps(bindings,indent=2)+"\n")
 receipt={"take":take,"backend":"ltxv2b","started_at_utc":datetime.now(timezone.utc).isoformat(),"status":"SUBMITTING","native_stage1":[352,544],"native_refined":[704,1088],"requested_canvas":[576,832],"frames":41,"fps":24,"steps":[7,3],"guidance":1.0,"negative_conditioning_effective":False,"seed":20261004,"source_only":True,"workflow_sha256":sha(out/"workflow.api.json"),"guide_bindings_sha256":sha(out/"input_bindings.json"),"renderer_source_sha256":sha(__file__)}
 (out/"receipt.json").write_text(json.dumps(receipt,indent=2)+"\n");start=time.monotonic();samples=[];next_sample=0;last_progress=0
 try:
  j=request("/prompt",{"prompt":g,"client_id":str(uuid.uuid4())})
  (out/"submission_response.json").write_text(json.dumps(j,indent=2)+"\n")
  if "prompt_id" not in j or j.get("node_errors"):raise RuntimeError(str(j))
  pid=j["prompt_id"];receipt["prompt_id"]=pid;receipt["status"]="RUNNING";(out/"receipt.json").write_text(json.dumps(receipt,indent=2)+"\n");print("QUEUED",take,pid,flush=True)
  while True:
   elapsed=time.monotonic()-start
   if elapsed>1800:
    q=request("/queue")
    if len(q["queue_running"])==1 and q["queue_running"][0][1]==pid:request("/interrupt",{})
    raise TimeoutError("Per-take1800s cap reached")
   if elapsed>=next_sample:
    q=subprocess.run(["nvidia-smi","--query-gpu=memory.used","--format=csv,noheader,nounits"],capture_output=True,text=True)
    if q.returncode==0:samples.append({"elapsed_seconds":round(elapsed,3),"total_card_used_mib":int(q.stdout.strip().splitlines()[0])})
    next_sample=elapsed+5
   h=request("/history/"+pid)
   if pid in h:
    history=h[pid];(out/"history.json").write_text(json.dumps(history,indent=2)+"\n")
    if history["status"]["status_str"]!="success":raise RuntimeError(str(history["status"]["messages"][-2:]))
    for node_id,label in [("13","stage1_frames"),("32","refined_native_frames"),("34","requested_canvas_frames")]:
     files=history["outputs"][node_id]["images"];assert len(files)==41,(label,len(files));dest=out/label;dest.mkdir(exist_ok=True)
     for n,x in enumerate(files):
      source=DATA/"output"/x["subfolder"]/x["filename"];shutil.copyfile(source,dest/f"{n:04d}.png")
    for node_id,label in [("11","stage1.latent"),("30","refined.latent")]:
     data=history["outputs"][node_id].get("latents",[])
     if data:
      x=data[0];shutil.copyfile(DATA/"output"/x["subfolder"]/x["filename"],out/label)
     else:
      source=sorted((DATA/"output"/"two_pass"/take).glob("*latent*.latent"));assert len(source)==2
      shutil.copyfile(next(x for x in source if ("stage1" if node_id=="11" else "refined") in x.name),out/label)
    receipt["status"]="EXECUTION_PASS";break
   if elapsed-last_progress>=30:print("RENDER_SECONDS",take,round(elapsed),flush=True);last_progress=elapsed
   time.sleep(2)
 except Exception as e:
  receipt["status"]="EXECUTION_FAIL";receipt["error"]=str(e);raise
 finally:
  receipt["elapsed_seconds"]=round(time.monotonic()-start,3);receipt["observed_total_card_peak_mib"]=max((x["total_card_used_mib"] for x in samples),default=None);receipt["memory_sampling_interval_seconds"]=5
  (out/"memory_samples.json").write_text(json.dumps(samples,indent=2)+"\n");(out/"receipt.json").write_text(json.dumps(receipt,indent=2)+"\n");print("RESULT",receipt["status"],receipt["elapsed_seconds"],receipt["observed_total_card_peak_mib"],flush=True)
if __name__=="__main__":main()
