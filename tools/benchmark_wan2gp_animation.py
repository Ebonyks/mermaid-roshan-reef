"""Run bounded Wan2GP action studies; public/restricted output routing is explicit."""
import argparse
from datetime import datetime,timezone
import hashlib,json,sys,time,shutil
from pathlib import Path

def sha(p):
 h=hashlib.sha256()
 with Path(p).open("rb") as f:
  for b in iter(lambda:f.read(8388608),b""):h.update(b)
 return h.hexdigest()
def main():
 a=argparse.ArgumentParser()
 a.add_argument("--runner",type=Path,required=True)
 a.add_argument("--packet",type=Path,required=True)
 a.add_argument("--engine",choices=("scail2_14B","hunyuan_1_5_480_i2v_step_distilled"),required=True)
 a.add_argument("--output",type=Path,required=True)
 a.add_argument("--limit",type=int,default=1800)
 a.add_argument("--resolution",default="896x512")
 a.add_argument("--steps",type=int)
 args=a.parse_args();args.packet=args.packet.resolve();args.output=args.output.resolve()
 args.output.mkdir(parents=True,exist_ok=True)
 setup_start=time.monotonic()
 setup={"status":"INITIALIZING","started_at_utc":datetime.now(timezone.utc).isoformat(),"engine":args.engine,"method":"Shared API import/init before task submit; independent from per-task model-load/generation timer"}
 (args.output/"setup_receipt.json").write_text(json.dumps(setup,indent=2)+"\n")
 print("Initializing",args.engine,flush=True)
 sys.path.insert(0,str(args.runner.resolve()))
 from shared.api import init
 s=init(root=args.runner.resolve(),cli_args=["--attention","sdpa","--profile","5"],output_dir=args.output/"native",console_output=True)
 setup.update(status="INITIALIZED",elapsed_seconds=round(time.monotonic()-setup_start,3))
 (args.output/"setup_receipt.json").write_text(json.dumps(setup,indent=2)+"\n")
 cases=("wave",) if args.engine=="scail2_14B" else ("wave","plant","swing")
 for name in cases:
  d=args.output/name;d.mkdir(parents=True,exist_ok=True)
  receipt=d/"receipt.json"
  if receipt.exists() and json.loads(receipt.read_text())["status"]=="EXECUTION_PASS":continue
  settings=s.get_default_settings(args.engine)
  settings.update(prompt=(args.packet/"briefs"/(name+".txt")).read_text(encoding="utf-8"),resolution=args.resolution,video_length=41,force_fps=24,seed=20261003,repeat_generation=1,image_start=str(args.packet/"inputs"/(name+".png")),num_inference_steps=args.steps or (40 if args.engine=="scail2_14B" else 8))
  if args.engine=="scail2_14B":
   settings.update(video_guide=str(args.packet/"inputs"/"wave_driver.mp4"),video_mask=str(args.packet/"inputs"/"wave_mask.mp4"),video_prompt_type="V1",image_refs=None)
   settings["custom_settings"].update(scail2_animate_preprocessing="raw",image_ref_keyword_content="cartoon mermaid character")
  exported=s.prepare_settings_for_export(settings)
  (d/"settings.json").write_text(json.dumps(exported,indent=2,default=str)+"\n")
  j={"engine":args.engine,"status":"SUBMITTING","lane":"REFERENCE_ONLY","review":"PENDING","started_at_utc":datetime.now(timezone.utc).isoformat(),"source_sha256":sha(args.packet/"inputs"/(name+".png")),"settings_sha256":sha(d/"settings.json"),"runner_revision":"b8b18f8114e432eea8f3d7e853a51dd91fa99571","attention":"sdpa","profile":5,"resolution":args.resolution,"steps":settings["num_inference_steps"],"outputs":[]}
  receipt.write_text(json.dumps(j,indent=2)+"\n")
  start=time.monotonic();job=None
  try:
   job=s.submit_task(settings)
   result=job.result(timeout=args.limit)
   (d/"result.json").write_text(json.dumps({"success":result.success,"errors":[str(e) for e in result.errors],"generated_files":result.generated_files},indent=2)+"\n")
   if not result.success:raise RuntimeError("; ".join(str(e) for e in result.errors))
   for i,p in enumerate(result.generated_files):
    source=Path(p).resolve()
    if not source.is_relative_to((args.output/"native").resolve()):raise RuntimeError("Generated output is outside the declared task directory")
    target=d/("native_"+str(i)+source.suffix);shutil.copyfile(source,target)
    j["outputs"].append({"path":target.name,"sha256":sha(target),"bytes":target.stat().st_size})
   if not j["outputs"]:raise RuntimeError("No output returned")
   j["status"]="EXECUTION_PASS"
  except Exception as e:
   if job is not None:job.cancel()
   j["status"]="FAILED";j["error"]=str(e)
  j["elapsed_seconds"]=round(time.monotonic()-start,3);j["completed_at_utc"]=datetime.now(timezone.utc).isoformat()
  receipt.write_text(json.dumps(j,indent=2)+"\n")
  print(name,j["status"],j["elapsed_seconds"],flush=True)
  if j["status"]=="FAILED":break
if __name__=="__main__":main()
