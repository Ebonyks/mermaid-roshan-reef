from pathlib import Path
import json,subprocess,shutil
p=Path(__file__).resolve().parents[1]
a=r"C:\Program Files\Aseprite\Aseprite.exe"
ff=r"C:\Users\Peter\AppData\Local\Programs\MermaidReefTools\FFmpeg\8.1.2\bin\ffmpeg.exe"
for take in sorted((p/"results").iterdir()):
 if not (take/"receipt.json").exists():continue
 receipt=json.loads((take/"receipt.json").read_text())
 if not receipt.get("model_job") or receipt["status"]!="EXECUTION_PASS":continue
 count=receipt['frames'];fps=receipt['fps']
 subprocess.run([a,"-b","--script-param","take="+str(take),"--script-param","count="+str(count),"--script-param","fps="+str(fps),"--script",str(p/"scripts/export_review.lua")],check=True,timeout=180)
 subprocess.run([ff,"-v","error","-framerate",str(fps),"-i",str(take/"refined_frames/%04d.png"),"-frames:v",str(count),"-c:v","libx264","-crf","18","-pix_fmt","yuv420p","-movflags","+faststart","-y",str(take/"native.mp4")],check=True,timeout=180)
 indices=list(range(count));duration=round(count*1000/fps)
 (take/"cadence.json").write_text(json.dumps({"source_indices":indices,"source_fps":fps,"aseprite_total_milliseconds":duration,"canonical_duration_seconds":count/fps,"video_frames":count,"video_fps":fps,"whole_canvas_scale":False,"frame_repair":False,"cadence_selection":"Every original native frame retained; no blur hidden by holds."},indent=2)+"\n")
 if fps==48:
  selected=list(range(0,count,2));folder=take/'comparison24_frames';folder.mkdir(exist_ok=True)
  for i,src in enumerate(selected):shutil.copyfile(take/f'refined_frames/{src:04d}.png',folder/f'{i:04d}.png')
  subprocess.run([ff,'-v','error','-framerate','24','-i',str(folder/'%04d.png'),'-frames:v','41','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-y',str(take/'comparison24.mp4')],check=True,timeout=180)
  (take/'comparison24_cadence.json').write_text(json.dumps({'source_indices':selected,'source_fps':48,'output_fps':24,'output_frames':41,'action_last_frame_time_seconds':80/48,'native_display_duration_seconds':81/48,'comparison_display_duration_seconds':41/24,'last_frame_display_difference_seconds':1/48,'interpolation':False,'pixel_repair':False,'purpose':'Exact equal action timestamps for same-content comparison; all81 native frames separately retained.'},indent=2)+'\n')
 print("REVIEW_EXPORTED",take.name,count,fps,flush=True)
