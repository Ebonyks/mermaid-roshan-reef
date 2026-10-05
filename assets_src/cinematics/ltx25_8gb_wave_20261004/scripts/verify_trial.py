from pathlib import Path
import json,hashlib,struct,subprocess,tempfile,ast
from PIL import Image
p=Path(__file__).resolve().parents[1]
a=r"C:\Program Files\Aseprite\Aseprite.exe"
checks=[]
def sha(f):
 with Path(f).open("rb") as s:return hashlib.file_digest(s,"sha256").hexdigest()
for f in p.glob("scripts/*.py"):ast.parse(f.read_text(encoding="utf-8-sig"));checks.append("source syntax "+f.name)
for t in sorted((p/"results").iterdir()):
 if not (t/"receipt.json").exists():continue
 j=json.loads((t/"receipt.json").read_text());g=json.loads((t/"workflow.api.json").read_text());assert sha(t/"workflow.api.json")==j["workflow_sha256"]
 assert j["renderer_sha256"] in [sha(p/"scripts/render.py"),sha(p/"scripts/render_base_retake.py"),sha(p/'scripts/render_temporal48.py')]
 checks.append("immutable graph and generator source "+t.name)
 if j["status"]!="EXECUTION_PASS":continue
 if not j["model_job"]:continue
 assert [g[str(200+i)]["inputs"]["frame_idx"] for i in range(8)]==([0,6,14,34,44,54,72,80] if t.name=='temporal_48fps' else [0,3,7,17,22,27,36,40])
 expected=[288,416] if t.name in ["base_two_pass","anti_blur_nag","temporal_48fps"] else None
 for folder,dims in [("refined_frames",[576,832])]+([("stage1_frames",expected)] if expected else []):
  files=sorted((t/folder).glob("*.png"));assert len(files)==j['frames']
  for f in files:
   with Image.open(f) as im:assert list(im.size)==dims
 checks.append("complete native frames and eight whole-figure guides "+t.name)
 if expected:
  assert len(g["11"]["inputs"]["sigmas"].split(','))==9 and len(g["26"]["inputs"]["sigmas"].split(','))==4
  assert g["25"]["class_type"]=="LTXVLatentUpsampler"
  checks.append("8-step first pass, learned2x upscale and3-step refinement "+t.name)
 master=t/"native_review.aseprite";header=master.read_bytes()[:14];assert struct.unpack_from('<H',header,6)[0]==j['frames']
 with tempfile.TemporaryDirectory(prefix='ltx25-ase-verify-') as tmp:
  subprocess.run([a,'-b','--script-param','master='+str(master),'--script-param','output='+tmp,'--script',str(p/'scripts/export_roundtrip.lua')],check=True,timeout=180)
  for i in range(j['frames']):
   with Image.open(t/f'refined_frames/{i:04d}.png') as x,Image.open(Path(tmp)/f'{i:04d}.png') as y:assert x.convert('RGBA').tobytes()==y.convert('RGBA').tobytes(),(t.name,i)
 checks.append(str(j["frames"])+"-frame lossless native Aseprite roundtrip "+t.name)
 if t.name=='anti_blur_nag':
  n=json.loads((t/'nag_hook_proof.json').read_text());assert n['status']=='ACTUAL_GPU_HOOK_PASS' and n['calls']>0 and n['first_call']['positive_negative_mean_absolute_difference']>0
  checks.append("negative attention actually executed on GPU")
c=json.loads((p/'environment/runner_effective_configuration.json').read_text());assert c['dynamic_vram_effective'] and c['allocator']=='cudaMallocAsync' and c['async_offload_streams']==2 and c['bf16_vae_requested'];checks.append('actual dynamic offload/BF16/runtime configuration')
r=json.loads((p/'environment/retake_preservation_check.json').read_text());assert r['outside_latent_mask_exact'];checks.append('retake mask preserved four of six video latent frames exactly; decoded pixel preservation NOT asserted')
j={'status':'PASS','checks':checks,'assertions':len(checks),'visual_acceptance':False,'owner_device_child_acceptance':False}
(p/'environment/trial_verification.json').write_text(json.dumps(j,indent=2)+'\n');print(json.dumps(j),flush=True)
