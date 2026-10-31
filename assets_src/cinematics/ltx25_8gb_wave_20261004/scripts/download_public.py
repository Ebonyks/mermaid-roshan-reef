from pathlib import Path
import sys,time,json,hashlib,datetime
from huggingface_hub import hf_hub_download
repo='Winnougan/ltx-2.5-w4a8-convrot-int4-convrot-Winnougan-Blessing'
revision='d27e4b9248e93b982f5c92e713a8f5cbdde76a45'
files={
 'transformer':('diffusion_models/ltx-2.5-22b-distilled-transformer-w4a8_convrot.safetensors',12520292200,'19ee13bf3a156f11b62ede47449fba8e02f775549d22598e1ffa9d874acf46a3'),
 'encoder':('text_encoders/gemma4-12b-with-proj-ltx-2.5-w4a8_convrot.safetensors',10604323186,'720a028bed0b776a31ceacbdfcf52edb54a9a4ab203c9a3b148299d147d0b4d5')}
kind=sys.argv[1];name,size,expected=files[kind];root=Path(r'H:\MermaidReefTools\LocalVideo\ltx25');start=time.monotonic()
print(json.dumps({'stage':'DOWNLOAD','kind':kind,'filename':name,'bytes_expected':size,'repo_revision':revision,'authenticated':False}),flush=True)
path=Path(hf_hub_download(repo,name,revision=revision,local_dir=root/'models',token=False))
print(json.dumps({'stage':'HASH_VERIFY','kind':kind,'path':str(path)}),flush=True)
with path.open('rb') as stream:actual=hashlib.file_digest(stream,'sha256').hexdigest()
assert path.stat().st_size==size and actual==expected,(kind,'Size or hash mismatch')
receipt={'kind':kind,'repo':repo,'revision':revision,'path':str(path),'bytes':path.stat().st_size,'sha256':actual,'expected_sha256':expected,'status':'PASS','download_and_hash_seconds':round(time.monotonic()-start,3),'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'credentials_printed':False,'publication':'Weights remain local, not redistributed.'}
(root/'logs'/f'download_{kind}.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8');print(json.dumps(receipt),flush=True)
