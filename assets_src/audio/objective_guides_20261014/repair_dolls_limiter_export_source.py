"""Export-only bounded mastering repair; never imports or calls a TTS model."""
from __future__ import annotations
import hashlib
import json
import shutil
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path
import numpy as np

OUT = Path(__file__).resolve().parent / "candidates"
MANIFEST = OUT / "generation_manifest.json"
FFMPEG = shutil.which("ffmpeg")
FFPROBE = shutil.which("ffprobe")

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def stamp():
    return datetime.now(timezone.utc).isoformat()

def run(command):
    return subprocess.run(command, check=True, capture_output=True)

def measure(path):
    command = [FFMPEG,"-hide_banner","-nostats","-i",str(path),"-af",
               "loudnorm=I=-16:TP=-1.7:LRA=7:print_format=json","-f","null","-"]
    output=run(command).stderr.decode("utf-8","replace")
    return json.JSONDecoder().raw_decode(output[output.rfind("{"):])[0], command

def save(manifest):
    MANIFEST.write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")

start=time.perf_counter()
m=json.loads(MANIFEST.read_text(encoding="utf-8"))
assert m["synthesis_calls"]==2 and len(m["attempts"])==2
assert m["attempts"][0]["status"]=="CANDIDATE_MACHINE_PASS"
record=m["attempts"][1]
assert record["key"]=="guide_dolls_catch_three" and record["status"]=="CANDIDATE_MACHINE_FAIL"
native=OUT/record["native"]["path"]
derived=OUT/record["native_to_review"]["derivative_path"]
assert sha(native)==record["native"]["sha256"] and sha(derived)==record["native_to_review"]["derivative_sha256"]
snapshot=OUT/"repair_dolls_limiter_export_source.py"
assert not snapshot.exists()
shutil.copyfile(__file__,snapshot)
failed=record["review"]
failed_path=OUT/failed["path"]
assert sha(failed_path)==failed["sha256"]
rejected=OUT/"rejected_encodes"/(record["key"]+"_encode04.ogg")
assert not rejected.exists()
shutil.move(str(failed_path),str(rejected))
failed["path"]=rejected.relative_to(OUT).as_posix()
record.setdefault("preserved_export_attempts",[]).append(failed)
m.setdefault("preserved_postprocess_failures",[]).append({
    "status":m["status"],"failure":m.get("failure"),"finished_utc":m.get("finished_utc"),
    "synthesis_calls_at_failure":2,
    "repair":"Dolls export-only lookahead limiter addresses speech peaks missed by compressor attack before measured normalization; no additional synthesis",
})
m["status"]="EXPORT_ONLY_MASTERING"
m["export_only_repair_source_sha256"]=sha(snapshot)
save(m)
compressed=OUT/"derived"/(record["key"]+"_limited.wav")
compressor="alimiter=limit=0.15:attack=5:release=50:level=false,highpass=f=40"
command=[FFMPEG,"-hide_banner","-nostats","-n","-i",str(derived),"-af",compressor,
         "-c:a","pcm_f32le",str(compressed)]
run(command)
measured,measure_command=measure(compressed)
filt=("loudnorm=I=-16:TP=-1.7:LRA=7:measured_I="+measured["input_i"]
      +":measured_TP="+measured["input_tp"]+":measured_LRA="+measured["input_lra"]
      +":measured_thresh="+measured["input_thresh"]+":offset="+measured["target_offset"]
      +":linear=true:print_format=json")
export=OUT/"review"/(record["key"]+".ogg")
encode=[FFMPEG,"-hide_banner","-nostats","-n","-i",str(compressed),"-af",filt,
        "-ar","48000","-ac","1","-c:a","libvorbis","-b:a","96k",str(export)]
run(encode)
post,post_command=measure(export)
probe_command=[FFPROBE,"-v","error","-show_streams","-show_format","-of","json",str(export)]
probe=json.loads(run(probe_command).stdout)
stream=probe["streams"][0]
decoded=np.frombuffer(run([FFMPEG,"-hide_banner","-loglevel","error","-i",str(export),
                          "-f","f32le","-acodec","pcm_f32le","-"]).stdout,dtype="<f4")
v={"codec":stream["codec_name"],"sample_rate_hz":int(stream["sample_rate"]),
   "channels":int(stream["channels"]),"bitrate_kbps":int(stream.get("bit_rate",0))/1000,
   "duration_seconds":float(stream.get("duration",probe["format"]["duration"])),
   "integrated_lufs":float(post["input_i"]),"true_peak_dbtp":float(post["input_tp"]),
   "decoded_finite":bool(np.isfinite(decoded).all()),"decoded_sample_peak":float(np.max(np.abs(decoded))),
   "decoded_dc_mean":float(decoded.mean())}
passed=(v["codec"]=="vorbis" and v["sample_rate_hz"]==48000 and v["channels"]==1
        and v["bitrate_kbps"]>=64 and v["decoded_finite"] and v["decoded_sample_peak"]<1
        and abs(v["decoded_dc_mean"])<0.001 and abs(v["integrated_lufs"]+16)<=1
        and v["true_peak_dbtp"]<=-1.5)
record["native_to_review"]["compression"]={"filter":compressor,"path":compressed.relative_to(OUT).as_posix(),
    "sha256":sha(compressed),"command":command,"measured_loudness":measured,"measurement_command":measure_command,
    "reason":"Declared lookahead limiter supplies crest headroom; 40 Hz highpass removes DC offset; native take unchanged"}
record["review"]={"path":export.relative_to(OUT).as_posix(),"sha256":sha(export),"bytes":export.stat().st_size,
    "verification":v,"encoding_command":encode,"measurement_command":post_command,
    "ffprobe_command":probe_command,"machine_pass":passed}
record["status"]="CANDIDATE_MACHINE_PASS" if passed else "CANDIDATE_MACHINE_FAIL"
record["finished_utc"]=stamp()
m["status"]="CANDIDATE_MACHINE_PASS" if passed else "CANDIDATE_MACHINE_FAIL"
m["acceptance"]["machine"]="PASS" if passed else "FAIL"
m["finished_utc"]=stamp()
m["export_only_mastering_seconds"]=round(time.perf_counter()-start,6)
if passed:
    m.pop("failure",None)
save(m)
receipt={"schema":"reef.objective-guide-machine-receipt.v1","status":m["status"],
         "manifest_sha256":sha(MANIFEST),"checked_utc":stamp(),"synthesis_calls":m["synthesis_calls"],
         "cues":[{"key":a["key"],"native_sha256":a["native"]["sha256"],
                  "review_sha256":a["review"]["sha256"],"verification":a["review"]["verification"]}
                 for a in m["attempts"]],"acceptance":m["acceptance"]}
(OUT/"MACHINE_RECEIPT.json").write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
print(json.dumps(receipt),flush=True)
if not passed:
    raise SystemExit(1)
