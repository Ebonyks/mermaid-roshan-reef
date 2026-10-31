from pathlib import Path
import json,subprocess,hashlib
p=Path(__file__).resolve().parents[1]
a=r"C:\Program Files\Aseprite\Aseprite.exe"
ff=r"C:\Users\Peter\AppData\Local\Programs\MermaidReefTools\FFmpeg\8.1.2\bin\ffmpeg.exe"
for take in sorted((p/"results").iterdir()):
 if not (take/"receipt.json").exists():continue
 receipt=json.loads((take/"receipt.json").read_text())
 if receipt["status"]!="EXECUTION_PASS":continue
 folder="refined_native_frames" if receipt["backend"]=="ltxv2b" else "native_frames"
 subprocess.run([a,"-b","--script-param","take="+str(take),"--script-param","folder="+folder,"--script",str(p/"scripts/export_review.lua")],check=True,timeout=180)
 if receipt["backend"]=="ltx23":subprocess.run([ff,"-v","error","-framerate","24","-i",str(take/folder/"%04d.png"),"-frames:v","41","-c:v","libx264","-crf","18","-pix_fmt","yuv420p","-movflags","+faststart","-y",str(take/"native.mp4")],check=True,timeout=180)
 subprocess.run([ff,"-v","error","-framerate","24","-i",str(take/folder/"%04d.png"),"-vf","select='not(mod(n,2))',setpts=N/(12*TB)","-frames:v","21","-r","12","-c:v","libx264","-crf","18","-pix_fmt","yuv420p","-movflags","+faststart","-y",str(take/"on_twos.mp4")],check=True,timeout=180)
 (take/"cadence.json").write_text(json.dumps({"source_indices":list(range(0,41,2)),"source_fps":24,"selection":"Uniform even-frame sampling; damaged adjacent pairs are failures, no invented anatomy or clean-frame hold used to conceal missing action.","aseprite_total_milliseconds":1708,"video_frames":21,"video_fps":12,"video_duration_seconds":1.75,"video_last_hold_extra_seconds":1/24,"canonical_duration_seconds":41/24,"anatomy_acceptance":False},indent=2)+"\n")
 print("REVIEW_EXPORTED",take.name,flush=True)
