"""Bounded source-study Comfy reproduction of the pinned official 2B multiscale recipe."""
from pathlib import Path
import argparse,json,urllib.request,urllib.error,hashlib,shutil,time,uuid,subprocess
from datetime import datetime,timezone
P=Path(__file__).resolve().parents[1];DATA=Path(r"H:\MermaidReefTools\LocalVideo");BASE="http://127.0.0.1:8193"
def request(path,data=None):
 b=None if data is None else json.dumps(data).encode()
 with urllib.request.urlopen(urllib.request.Request(BASE+path,data=b,headers={"Content-Type":"application/json"}),timeout=30) as f:return json.load(f)
def sha(p):
 with Path(p).open("rb") as f:return hashlib.file_digest(f,"sha256").hexdigest()
def add(g,k,typ,**inputs):g[str(k)]={"class_type":typ,"inputs":inputs};return str(k)
def graph(take,nag):
 g={};bindings=[];loads={}
 add(g,1,"UnetLoaderGGUF",unet_name="ltx-2.3-22b-distilled-Q4_K_S.gguf")
 add(g,2,"DualCLIPLoaderGGUF",clip_name1="gemma-3-12b-it-qat-Q4_K_S.gguf",clip_name2="ltx-2.3-22b-distilled_embeddings_connectors.safetensors",type="ltxv")
 add(g,3,"CLIPTextEncode",clip=["2",0],text=(P/"briefs/wave_prompt.txt").read_text())
 if nag:add(g,4,"CLIPTextEncode",clip=["2",0],text=(P/"briefs/negative_prompt.txt").read_text())
 else:add(g,4,"ConditioningZeroOut",conditioning=["3",0])
 add(g,5,"LTXVConditioning",positive=["3",0],negative=["4",0],frame_rate=24)
 add(g,6,"EmptyLTXVLatentVideo",width=352,height=544,length=41,batch_size=1)
 add(g,7,"VAELoader",vae_name="ltx-2.3-22b-distilled_video_vae.safetensors")
 add(g,8,"KSamplerSelect",sampler_name="euler")
 add(g,9,"ManualSigmas",sigmas="1,0.99375,0.9875,0.98125,0.975,0.909375,0.725,0.421875,0")
 add(g,10,"StudyChunkFeedForward",model=["1",0],chunk_tokens=512)
 model=["10",0]
 if nag:
  add(g,25,"LTX2_NAG",model=model,nag_cond_video=["4",0],nag_scale=5.0,nag_alpha=.25,nag_tau=2.5,inplace=True);model=["25",0]
 pos=["5",0];neg=["5",1];lat=["6",0]
 for n,idx in enumerate([0,3,7,17,22,27,36,40]):
  src=P/f"inputs/guide_{idx:04d}.png";h=sha(src);name="two_pass_"+h+".png";dst=DATA/"input"/name
  if not dst.exists():shutil.copyfile(src,dst)
  assert sha(dst)==h
  if h not in loads:loads[h]=add(g,30+n,"LoadImage",image=name)
  bindings.append({"guide_index":idx,"path":src.relative_to(P).as_posix(),"sha256":h,"bound_path":str(dst),"strength":1.0})
  k=add(g,100+n,"LTXVAddGuide",positive=pos,negative=neg,vae=["7",0],latent=lat,image=[loads[h],0],frame_idx=idx,strength=1.0)
  pos=[k,0];neg=[k,1];lat=[k,2]
 add(g,20,"SamplerCustom",model=model,add_noise=True,noise_seed=20261004,cfg=1.,positive=pos,negative=neg,sampler=["8",0],sigmas=["9",0],latent_image=lat)
 add(g,21,"LTXVCropGuides",positive=pos,negative=neg,latent=["20",0])
 add(g,22,"SaveLatent",samples=["21",2],filename_prefix=f"two_pass/{take}/native_latent")
 add(g,23,"VAEDecodeTiled",samples=["21",2],vae=["7",0],tile_size=256,overlap=64,temporal_size=64,temporal_overlap=8)
 add(g,24,"SaveImage",images=["23",0],filename_prefix=f"two_pass/{take}/native/frame")
 return g,bindings

def main():
 a=argparse.ArgumentParser();a.add_argument("take",choices=["ltx23_chunked","ltx23_chunked_nag"]);args=a.parse_args();take=args.take
 if (P/"results"/take/"receipt.json").exists():raise SystemExit("Existingattempt; no silent repeat or overwrite")
 old=[json.loads(x.read_text()) for x in (P/"results").glob("*/receipt.json")]
 if len(old)>=4 or sum(x.get("backend")=="ltx23" for x in old)>=2:raise SystemExit("Trialcap reached")
 # Readiness/schema checks happen before a model submission; no job queued here.
 schema=request("/object_info");queue=request("/queue");assert not queue["queue_running"] and not queue["queue_pending"],"Existing queue left untouched"
 g,bindings=graph(take,take.endswith("_nag"))
 for k,node in g.items():
  assert node["class_type"] in schema,node["class_type"]
  for name in schema[node["class_type"]]["input"].get("required",{}):assert name in node["inputs"],(k,name)
 out=P/"results"/take;out.mkdir(parents=True,exist_ok=True)
 (out/"workflow.api.json").write_text(json.dumps(g,indent=2)+"\n")
 (out/"input_bindings.json").write_text(json.dumps(bindings,indent=2)+"\n")
 receipt={"take":take,"backend":"ltx23","started_at_utc":datetime.now(timezone.utc).isoformat(),"status":"SUBMITTING","native_canvas":[352,544],"frames":41,"fps":24,"steps":8,"guidance":1.0,"dedicated_nag":take.endswith("_nag"),"nag_settings":{"scale":5.,"alpha":.25,"tau":2.5} if take.endswith("_nag") else None,"chunk_tokens":512,"negative_conditioning_effective_claim":"Dedicated cross-attention NAG; actual execution log required" if take.endswith("_nag") else False,"seed":20261004,"upscaler":False,"source_only":True,"workflow_sha256":sha(out/"workflow.api.json"),"guide_bindings_sha256":sha(out/"input_bindings.json"),"renderer_source_sha256":sha(__file__)}
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
    for node_id,label in [("24","native_frames")]:
     files=history["outputs"][node_id]["images"];assert len(files)==41,(label,len(files));dest=out/label;dest.mkdir(exist_ok=True)
     for n,x in enumerate(files):
      source=DATA/"output"/x["subfolder"]/x["filename"];shutil.copyfile(source,dest/f"{n:04d}.png")
    source=list((DATA/"output"/"two_pass"/take).glob("native_latent*.latent"));assert len(source)==1
    shutil.copyfile(source[0],out/"native.latent")
    receipt["status"]="EXECUTION_PASS";break
   if elapsed-last_progress>=30:print("RENDER_SECONDS",take,round(elapsed),flush=True);last_progress=elapsed
   time.sleep(2)
 except Exception as e:
  receipt["status"]="EXECUTION_FAIL";receipt["error"]=str(e);raise
 finally:
  receipt["elapsed_seconds"]=round(time.monotonic()-start,3);receipt["observed_total_card_peak_mib"]=max((x["total_card_used_mib"] for x in samples),default=None);receipt["memory_sampling_interval_seconds"]=5
  (out/"memory_samples.json").write_text(json.dumps(samples,indent=2)+"\n");(out/"receipt.json").write_text(json.dumps(receipt,indent=2)+"\n");print("RESULT",receipt["status"],receipt["elapsed_seconds"],receipt["observed_total_card_peak_mib"],flush=True)
if __name__=="__main__":main()
