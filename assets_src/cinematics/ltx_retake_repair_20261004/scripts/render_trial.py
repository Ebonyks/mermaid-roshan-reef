"""Bounded full-frame guide/temporal-retake experiments, with unmodified native outputs."""
from pathlib import Path
import argparse,json,hashlib,time,urllib.request,subprocess,shutil
from datetime import datetime,timezone
ap=argparse.ArgumentParser();ap.add_argument('--take',required=True);ap.add_argument('--backend',choices=['ltxv','ltx23'],required=True);ap.add_argument('--strength',type=float,default=1);ap.add_argument('--port',type=int,default=8190);ap.add_argument('--diagnostic',action='store_true');ap.add_argument('--width',type=int,default=896);ap.add_argument('--height',type=int,default=512);a=ap.parse_args()
p=Path(__file__).resolve().parents[1];out=p/'results'/a.take;out.mkdir(exist_ok=True);(out/'native_frames').mkdir(exist_ok=True)
if (out/'receipt.json').exists():raise SystemExit('Refusing to overwrite an attempt receipt')
existing=[]
for receipt in (p/'results').glob('*/receipt.json'):
 try:
  entry=json.loads(receipt.read_text())
  if entry.get('prompt_id') and not entry.get('diagnostic_only',False):existing.append(entry)
 except (ValueError,OSError):pass
caps=json.loads((p/'briefs/job_card.json').read_text())['caps']
all_submissions=sum(bool(json.loads(x.read_text()).get('prompt_id')) for x in (p/'results').glob('*/receipt.json'))
preflight_path=p/'environment/preflight_failures.json'
preflight_count=sum(x['stage'].startswith('diagnostic_client') for x in json.loads(preflight_path.read_text())) if preflight_path.exists() else 0
if all_submissions+preflight_count>=caps['submissions_including_failed_preflight']:raise SystemExit('Total submission/preflight cap reached, including diagnostics; do not reset by renaming a take.')
if not a.diagnostic and (len(existing)>=caps['additional_generated_takes'] or sum(e.get('backend')==a.backend for e in existing)>=caps['per_backend_takes']):raise SystemExit('Recorded trial take cap reached; do not reset by renaming a take.')
url=f'http://127.0.0.1:{a.port}';root=Path(r'H:\MermaidReefTools\LocalVideo');sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
def req(path,data=None):
 r=urllib.request.Request(url+path,data=None if data is None else json.dumps(data).encode(),headers={'Content-Type':'application/json'})
 with urllib.request.urlopen(r,timeout=90) as s:return json.load(s)
def node(kind,**inputs):return {'class_type':kind,'inputs':inputs}
g=json.loads((p.parent/'ltx_registered_wave_20261004/environment/base_workflow.api.json').read_text())
g.pop('11',None);g['4']['inputs']['image']='retake_trial_original_0040.png';g['5']['inputs']['text']=(p/'briefs/lowering.txt').read_text();g['8']['inputs'].update(length=25,width=a.width,height=a.height)
vae=['1',2];model=['1',0]
if a.backend=='ltx23':
 g['1']=node('UnetLoaderGGUF',unet_name='ltx-2.3-22b-distilled-Q4_K_S.gguf')
 g['2']=node('DualCLIPLoaderGGUF',clip_name1='gemma-3-12b-it-qat-Q4_K_S.gguf',clip_name2='ltx-2.3-22b-distilled_embeddings_connectors.safetensors',type='ltxv')
 g['3']=node('VAELoader',vae_name='ltx-2.3-22b-distilled_video_vae.safetensors');vae=['3',0]
 g['13']['inputs']['sigmas']='1,0.99375,0.9875,0.98125,0.975,0.909375,0.725,0.421875,0'
 g['50']=node('LoadImage',image='retake_trial_source_window.apng');g['52']=node('ImageScale',image=['50',0],upscale_method='area',width=a.width,height=a.height,crop='disabled');g['51']=node('VAEEncode',pixels=['52',0],vae=vae)
 g.pop('8');last=['7',0];negative=['7',1];latent=['51',0]
else:last=['8',0];negative=['8',1];latent=['8',2]
for n,(idx,file) in enumerate([(8,'corrected_0048.png'),(24,'original_0064.png')]):
 lid=str(20+n*2);nid=str(21+n*2);g[lid]=node('LoadImage',image='retake_trial_'+file)
 g[nid]=node('LTXVAddGuide',positive=last,negative=negative,latent=latent,vae=vae,image=[lid,0],frame_idx=idx,strength=a.strength if n==0 else 1.0)
 last=[nid,0];negative=[nid,1];latent=[nid,2]
if a.backend=='ltx23':
 # Four native latent frames plus two appended guide frames: preserve first/last and guides.
 # Both middle temporal blocks are regenerated across the entire canvas, never only a limb.
 g['60']=node('LoadImage',image='retake_trial_mask_black.png');g['61']=node('LoadImage',image='retake_trial_mask_white.png')
 sources=[['60',0],['61',0],['61',0],['60',0],['60',0],['60',0]]
 acc=sources[0]
 for i,source in enumerate(sources[1:]):
  nid=str(62+i);g[nid]=node('ImageBatch',image1=acc,image2=source);acc=[nid,0]
 g['68']=node('ImageToMask',image=acc,channel='red');g['69']=node('SetLatentNoiseMask',samples=latent,mask=['68',0]);latent=['69',0]
g['9']['inputs'].update(model=model,positive=last,negative=negative,latent_image=latent,noise_seed=20261004)
g['40']=node('LTXVCropGuides',positive=last,negative=negative,latent=['9',0]);g['10']['inputs'].update(samples=['40',2],vae=vae)
g['14']=node('SaveImage',images=['10',0],filename_prefix='local_reference/ltx_retake_repair_20261004_'+a.take+'/frame')
if a.backend=='ltx23' and not a.diagnostic:
 g['80']=node('SaveLatent',samples=['51',0],filename_prefix='local_reference/ltx_retake_repair_20261004_'+a.take+'/encoded_source')
 g['81']=node('SaveLatent',samples=['40',2],filename_prefix='local_reference/ltx_retake_repair_20261004_'+a.take+'/retake_latent')
if a.diagnostic:
 g={'1':node('CheckpointLoaderSimple',ckpt_name='ltxv-2b-0.9.8-distilled.safetensors')} if a.backend=='ltxv' else {'3':node('VAELoader',vae_name='ltx-2.3-22b-distilled_video_vae.safetensors')}
 g['20']=node('LoadImage',image='retake_trial_corrected_0048.png');g['21']=node('VAEEncode',pixels=['20',0],vae=vae);g['10']=node('VAEDecodeTiled',samples=['21',0],vae=vae,tile_size=256,overlap=64,temporal_size=64,temporal_overlap=8);g['14']=node('SaveImage',images=['10',0],filename_prefix='local_reference/ltx_retake_repair_20261004_'+a.take+'/frame')
if a.backend=='ltx23' and not a.diagnostic:
 g['80']=node('SaveLatent',samples=['51',0],filename_prefix='local_reference/ltx_retake_repair_20261004_'+a.take+'/encoded_source')
 g['81']=node('SaveLatent',samples=['40',2],filename_prefix='local_reference/ltx_retake_repair_20261004_'+a.take+'/retake_latent')
bindings=[]
for graph_node in g.values():
 if graph_node['class_type']=='LoadImage':
  original=root/'input'/graph_node['inputs']['image'];immutable=root/'input'/('retake_sha_'+sha(original)[:20]+'_'+original.name)
  if immutable.exists() and sha(immutable)!=sha(original):raise RuntimeError('Existing immutable input differs')
  if not immutable.exists():shutil.copyfile(original,immutable)
  bindings.append({'model_input_name':immutable.name,'sha256':sha(immutable),'bytes':immutable.stat().st_size})
  graph_node['inputs']['image']=immutable.name
(out/'bindings.json').write_text(json.dumps(bindings,indent=2)+'\n')
(out/'workflow.api.json').write_text(json.dumps(g,indent=2)+'\n')
queue=req('/queue');j={'status':'SUBMITTING','started_at_utc':datetime.now(timezone.utc).isoformat(),'backend':a.backend,'diagnostic_only':a.diagnostic,'source_window_inclusive':[40,64],'native_frames_expected':1 if a.diagnostic else 25,'fps':24,'guide_strength':a.strength,'width':a.width,'height':a.height,'server_port':a.port,'seed':20261004,'workflow_sha256':sha(out/'workflow.api.json'),'native_outputs':[],'resources':[],'queue_ahead_prompt_ids':[x[1] for key in ['queue_running','queue_pending'] for x in queue[key]],'acceptance':'REFERENCE_ONLY'}
start=time.monotonic();pid=None
try:
 submission=req('/prompt',{'prompt':g,'client_id':'ltx_retake_repair_20261004'});pid=submission['prompt_id'];j['prompt_id']=pid;print('SUBMITTED',a.take,pid,flush=True)
 while time.monotonic()-start<7200:
  h=req('/history/'+pid)
  if pid in h:break
  running=req('/queue')['queue_running']
  if any(x[1]==pid for x in running):
   j.setdefault('active_start_elapsed_seconds',time.monotonic()-start)
   if time.monotonic()-start-j['active_start_elapsed_seconds']>1800:
    req('/interrupt',{});raise TimeoutError('Owned rendering exceeded 1800s cap')
  if not j['resources'] or time.monotonic()-start-j['resources'][-1]['elapsed_seconds']>10:
   r=subprocess.run(['nvidia-smi','--query-gpu=memory.used,utilization.gpu','--format=csv,noheader,nounits'],capture_output=True,text=True)
   j['resources'].append({'elapsed_seconds':round(time.monotonic()-start,3),'gpu_used_mib_util_percent':r.stdout.strip()})
   (out/'receipt.json').write_text(json.dumps(j,indent=2)+'\n')
  time.sleep(2)
 else:raise TimeoutError('Queue wait cap reached')
 h=h[pid];(out/'history.json').write_text(json.dumps(h,indent=2)+'\n')
 if h.get('status',{}).get('status_str')!='success':raise RuntimeError(str(h.get('status')))
 images=h['outputs']['14']['images'];assert len(images)==j['native_frames_expected'],len(images)
 for i,item in enumerate(images):
  source=(root/'output'/item.get('subfolder','')/item['filename']).resolve();assert source.is_relative_to((root/'output').resolve())
  dst=out/'native_frames'/f'{i:04d}.png';shutil.copyfile(source,dst);j['native_outputs'].append({'index':i,'path':str(dst.relative_to(out)).replace('\\','/'),'sha256':sha(dst),'bytes':dst.stat().st_size})
 for node_id in ['80','81']:
  for item in h.get('outputs',{}).get(node_id,{}).get('latents',[]):
   source=root/'output'/item.get('subfolder','')/item['filename'];dst=out/('encoded_source.latent' if node_id=='80' else 'retake.latent');shutil.copyfile(source,dst)
 j['status']='EXECUTION_PASS'
except Exception as e:
 j['status']='FAILED';j['error']=str(e)
 if pid and any(x[1]==pid for x in req('/queue')['queue_running']):req('/interrupt',{})
j['elapsed_seconds']=round(time.monotonic()-start,3);j['completed_at_utc']=datetime.now(timezone.utc).isoformat();(out/'receipt.json').write_text(json.dumps(j,indent=2)+'\n');print(a.take,j['status'],j['elapsed_seconds'],j.get('error',''),flush=True)
if j['status']!='EXECUTION_PASS':raise SystemExit(1)
