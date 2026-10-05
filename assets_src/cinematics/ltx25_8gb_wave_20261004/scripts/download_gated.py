from pathlib import Path
import getpass,json,time,hashlib,datetime,concurrent.futures
from huggingface_hub import hf_hub_download
root=Path(r'H:\MermaidReefTools\LocalVideo\ltx25')
repo='Lightricks/LTX-2.5';revision='2356ce76915d6c48d313d7e8b25900e1dd3abaa8'
files={
 'video_vae':('vae/ltx-2.5-video-vae-bf16.safetensors',1472223346,'847e14ca7f3355debca0cea4eaa24ac0fbcdf0061da054ac89ca638a869ddba3'),
 'upscaler':('latent_upscale_models/ltx-2.5-latent-spatial-upscaler-x2-bf16-1.0.safetensors',995778752,'eb5a71fe4068ee87ccdb1c3aa635e547ca76bd2d30ae20ae889f2c325c0677e8'),
 'audio_vae':('vae/ltx-2.5-audio-vae-bf16.safetensors',364866540,'c52733d37f6a7fb7949c3dc0fb468c6cb2169e4d836983a73babb9f0d54837a5')}
token=getpass.getpass('Hugging Face token (hidden, download-session only): ')
def download(kind,entry):
 name,size,expected=entry;start=time.monotonic()
 print(json.dumps({'stage':'DOWNLOAD','kind':kind,'filename':name,'bytes_expected':size,'authenticated':True}),flush=True)
 try:path=Path(hf_hub_download(repo,name,revision=revision,local_dir=root/'models',token=token))
 except Exception as e:
  print(json.dumps({'stage':'FAIL','kind':kind,'exception_type':type(e).__name__}),flush=True);raise RuntimeError(type(e).__name__) from None
 with path.open('rb') as stream:actual=hashlib.file_digest(stream,'sha256').hexdigest()
 assert path.stat().st_size==size and actual==expected,'Size or hash mismatch'
 receipt={'kind':kind,'repo':repo,'revision':revision,'path':str(path),'bytes':size,'sha256':actual,'expected_sha256':expected,'status':'PASS','download_and_hash_seconds':round(time.monotonic()-start,3),'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'credential_persisted':False,'weights_redistributed':False}
 (root/'logs'/f'download_{kind}.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8');print(json.dumps(receipt),flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 for f in [pool.submit(download,k,v) for k,v in files.items()]:f.result()
token=None
print('ALL THREE MATCHED OFFICIAL COMPONENTS HASH-VERIFIED',flush=True)
