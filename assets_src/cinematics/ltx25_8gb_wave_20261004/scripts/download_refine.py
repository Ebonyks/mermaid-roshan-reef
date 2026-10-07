from pathlib import Path
import getpass,json,time,hashlib,datetime,os,sys
sys.path.insert(0,r'H:\MermaidReefTools\LocalVideo\ltx25\python_deps')
from huggingface_hub import hf_hub_download
p=Path(r'H:\MermaidReefTools\LocalVideo\ltx25')
repo='Lightricks/LTX-2.5-22b-IC-LoRA-Refine-Details';rev='4912c478b35dd96b6cdcc5f7c7ff9d72c2c57929';name='ltx-2.5-22b-ic-lora-refine-details-1.0.safetensors';size=1308787534;expected='771a84f70e143af89867fc714ebbf7bd6edcaa4974c0360cba4a2d292a99f0e6'
j={'repo':repo,'revision':rev,'filename':name,'expected_bytes':size,'expected_sha256':expected,'credential_persisted':False,'weights_redistributed':False}
token=getpass.getpass('Hugging Face token (hidden; session only): ')
start=time.monotonic()
try:
 f=Path(hf_hub_download(repo,name,revision=rev,local_dir=p/'models/loras',token=token))
 with f.open('rb') as s:h=hashlib.file_digest(s,'sha256').hexdigest()
 assert h==expected and f.stat().st_size==size
 j.update(status='PASS',path=str(f),bytes=size,sha256=h,elapsed_seconds=round(time.monotonic()-start,3))
except Exception as e:
 j.update(status='BLOCKED',exception_type=type(e).__name__)
finally:
 token=None;j['checked_at_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();(p/'logs/download_refine_details.json').write_text(json.dumps(j,indent=2)+'\n');print(json.dumps(j),flush=True)
