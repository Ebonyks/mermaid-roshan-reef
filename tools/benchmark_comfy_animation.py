"""Bounded same-content ComfyUI benchmark; no runtime asset writes."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import time
import urllib.request

URL = "http://127.0.0.1:8190"
def request(route, payload=None):
    data = None if payload is None else json.dumps(payload).encode()
    req = urllib.request.Request(URL + route, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as response:
        body=response.read()
        return json.loads(body) if body else {}
def sha(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda:f.read(4*1024*1024),b""): h.update(chunk)
    return h.hexdigest()
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--packet",type=Path,required=True)
    ap.add_argument("--tool-root",type=Path,required=True)
    ap.add_argument("--workflow",type=Path,required=True)
    ap.add_argument("--ffmpeg",type=Path,required=True)
    ap.add_argument("--limit",type=int,default=1800)
    ap.add_argument("--engine",choices=("wan22_gguf","ltx_2b","ltx_2b_guided"),default="wan22_gguf")
    ap.add_argument("--steps",type=int,default=24)
    ap.add_argument("--cases",nargs="+",choices=("wave","plant","swing"),default=("wave","plant","swing"))
    args=ap.parse_args()
    for name in args.cases:
        out=args.packet/"results"/args.engine/name
        out.mkdir(parents=True,exist_ok=True)
        receipt=out/"receipt.json"
        if receipt.exists() and json.loads(receipt.read_text())["status"]=="EXECUTION_PASS":
            print(name,"already complete",flush=True);continue
        q=request("/queue")
        if q.get("queue_running") or q.get("queue_pending"): raise RuntimeError("Another job owns the queue; left untouched")
        graph=json.loads(args.workflow.read_text())
        graph.pop("0",None)
        source=args.packet/"inputs"/(name+".png")
        staged="benchmark_"+sha(source)[:16]+".png"
        shutil.copyfile(source,args.tool_root/"input"/staged)
        if args.engine=="ltx_2b_guided":
            bindings=json.loads((args.packet/"environment"/"ltx_controlled_wave_bindings.json").read_text())["bindings"]
            for binding in bindings:
                control=(args.packet/binding["source"]).resolve()
                if not control.is_relative_to(args.packet.resolve()) or sha(control)!=binding["sha256"]:raise RuntimeError("Controlled input binding failed")
                control_name="benchmark_guide_"+binding["sha256"][:16]+".png"
                if not any(n["class_type"]=="LoadImage" and n["inputs"]["image"]==control_name for n in graph.values()):raise RuntimeError("Guide missing from workflow")
                shutil.copyfile(control,args.tool_root/"input"/control_name)
        graph["4"]["inputs"]["image"]=staged
        prompt=(args.packet/"briefs"/(name+".txt")).read_text(encoding="utf-8")
        graph["5"]["inputs"]["text"]=prompt
        graph["8"]["inputs"].update(width=896,height=512,length=41,batch_size=1)
        if graph["9"]["class_type"]=="KSampler":
            graph["9"]["inputs"].update(seed=20261003,steps=args.steps)
        else:
            graph["9"]["inputs"].update(noise_seed=20261003)
        prefix="local_reference/benchmark_20261003_"+args.engine+"_"+name
        graph["11"]["inputs"]["filename_prefix"]=prefix
        (out/"workflow.api.json").write_text(json.dumps(graph,indent=2)+"\n",encoding="utf-8")
        j={"status":"SUBMITTING","acceptance":"REFERENCE_ONLY","engine":args.engine,"source_sha256":sha(source),"prompt_sha256":hashlib.sha256(prompt.encode()).hexdigest(),"workflow_sha256":sha(out/"workflow.api.json"),"started_at_utc":datetime.now(timezone.utc).isoformat(),"settings":{"width":896,"height":512,"frames":41,"fps":24,"steps":args.steps,"seed":20261003},"review":"PENDING","outputs":[]}
        receipt.write_text(json.dumps(j,indent=2)+"\n")
        started=time.monotonic()
        try:
            pid=request("/prompt",{"prompt":graph,"client_id":"benchmark_20261003"})["prompt_id"]
            j["prompt_id"]=pid;j["status"]="RUNNING";receipt.write_text(json.dumps(j,indent=2)+"\n")
            print(name,pid,flush=True)
            while time.monotonic()-started<args.limit:
                history=request("/history/"+pid)
                if pid in history: break
                time.sleep(5)
            else:
                running=request("/queue").get("queue_running",[])
                if any(item[1]==pid for item in running): request("/interrupt",{})
                raise TimeoutError("Owned render reached cap; no unrelated job interrupted")
            result=history[pid]
            (out/"history.json").write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
            if result.get("status",{}).get("status_str")!="success": raise RuntimeError(str(result.get("status")))
            native=[]
            for output in result.get("outputs",{}).values():
                for key in ("videos","images","gifs"):
                    for item in output.get(key,[]):
                        f=(args.tool_root/"output"/item.get("subfolder","")/item["filename"]).resolve()
                        if not f.is_relative_to((args.tool_root/"output").resolve()): raise RuntimeError("Output outside declared root")
                        native.append(f)
            for f in dict.fromkeys(native):
                target=out/("native"+f.suffix)
                shutil.copyfile(f,target)
                j["outputs"].append({"path":target.name,"sha256":sha(target),"bytes":target.stat().st_size})
                if f.suffix==".webm":
                    mp4=out/"preview.mp4"
                    subprocess.run([str(args.ffmpeg),"-hide_banner","-loglevel","error","-y","-i",str(f),"-c:v","libx264","-crf","18","-pix_fmt","yuv420p","-an",str(mp4)],check=True)
                    probe=subprocess.run([str(args.ffmpeg.with_name("ffprobe.exe")),"-v","error","-count_frames","-select_streams","v:0","-show_entries","stream=width,height,r_frame_rate,nb_read_frames","-of","json",str(mp4)],capture_output=True,text=True,check=True)
                    j["outputs"].append({"path":mp4.name,"sha256":sha(mp4),"bytes":mp4.stat().st_size,"media":json.loads(probe.stdout)})
                    stream=j["outputs"][-1]["media"]["streams"][0]
                    if (stream["width"],stream["height"],int(stream["nb_read_frames"]))!=(896,512,41):raise RuntimeError("Native frame mapping failed")
            if not j["outputs"]: raise RuntimeError("No native output")
            j["status"]="EXECUTION_PASS"
        except Exception as e:
            j["status"]="FAILED";j["error"]=str(e)
        j["elapsed_seconds"]=round(time.monotonic()-started,3)
        j["completed_at_utc"]=datetime.now(timezone.utc).isoformat()
        receipt.write_text(json.dumps(j,indent=2)+"\n",encoding="utf-8")
        print(name,j["status"],j["elapsed_seconds"],flush=True)
        q=request("/queue")
        if not q.get("queue_running") and not q.get("queue_pending"): request("/free",{"unload_models":True,"free_memory":True})
if __name__=="__main__":main()
