from pathlib import Path
import argparse,json,urllib.request,urllib.error,uuid,time,hashlib,subprocess,shutil
from datetime import datetime,timezone
R=Path(r'H:\MermaidReefTools\LocalVideo\ltx25');BASE='http://127.0.0.1:8194'
def req(path,data=None):
 b=None if data is None else json.dumps(data).encode()
 with urllib.request.urlopen(urllib.request.Request(BASE+path,data=b,headers={'Content-Type':'application/json'}),timeout=30) as f:return json.load(f)
def sha(p):
 with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def add(g,k,t,**v):g[str(k)]={'class_type':t,'inputs':v};return str(k)
def models(g):
 add(g,1,'UNETLoader',unet_name='ltx-2.5-22b-distilled-transformer-w4a8_convrot.safetensors',weight_dtype='default')
 add(g,2,'CLIPLoader',clip_name='gemma4-12b-with-proj-ltx-2.5-w4a8_convrot.safetensors',type='ltxv',device='default')
 add(g,3,'VAELoader',vae_name='ltx-2.5-video-vae-bf16.safetensors')
 add(g,4,'VAELoader',vae_name='ltx-2.5-audio-vae-bf16.safetensors')
def guides(g,start,latent):
 pos=['7',0];neg=['7',1]
 for n,i in enumerate([0,3,7,17,22,27,36,40]):
  load=add(g,400+n,'LoadImage',image=f'guide_{i:04d}.png')
  k=add(g,start+n,'LTXVAddGuide',positive=pos,negative=neg,vae=['3',0],latent=latent,image=[load,0],frame_idx=i*2,strength=1.0)
  pos=[k,0];neg=[k,1];latent=[k,2]
 return pos,neg,latent
def decode(g,base,latent,label,take):
 k=add(g,base,'VAEDecodeTiled',samples=latent,vae=['3',0],tile_size=256,overlap=64,temporal_size=64,temporal_overlap=8)
 k2=add(g,base+1,'StudyFiniteImages',images=[k,0]);add(g,base+2,'SaveImage',images=[k2,0],filename_prefix=f'{take}/{label}/frame')
 return str(base+2)
def graph(take):
 g={};outputs={};latents={}
 add(g,900,'StudyRuntimeReceipt',label=take)
 if take=='decoder_preflight':
  add(g,3,'VAELoader',vae_name='ltx-2.5-video-vae-bf16.safetensors');add(g,8,'LoadImage',image='guide_0022.png');add(g,9,'VAEEncode',pixels=['8',0],vae=['3',0]);outputs['preflight_frames']=decode(g,40,['9',0],'preflight',take)
  return g,outputs,latents
 models(g);prompt=(R/'wave_prompt.txt').read_text()
 if take=='temporal_retake':prompt+=' During frames17-32, the entire figure lowers her connected open hand slowly through forehead height at frame22. The shoulder and bodice shift with the arm, with small hair and tail follow-through. Keep distinct sharp fingers and painted contours through the whole lowering arc.'
 add(g,5,'CLIPTextEncode',clip=['2',0],text=prompt);add(g,6,'ConditioningZeroOut',conditioning=['5',0]);add(g,7,'LTXVConditioning',positive=['5',0],negative=['6',0],frame_rate=48)
 add(g,10,'KSamplerSelect',sampler_name='euler_ancestral')
 if take in {'base_two_pass','temporal_48fps'}:
  add(g,8,'EmptyLTXVLatentVideo',width=288,height=416,length=81,batch_size=1);add(g,9,'LTXVEmptyLatentAudio',frames_number=81,frame_rate=48,batch_size=1,audio_vae=['4',0])
  add(g,11,'ManualSigmas',sigmas='1.0,0.99375,0.9875,0.98125,0.975,0.909375,0.725,0.421875,0.0')
  pos,neg,lat=guides(g,100,['8',0]);add(g,15,'LTXVConcatAVLatent',video_latent=lat,audio_latent=['9',0]);add(g,16,'SamplerCustom',model=['1',0],add_noise=True,noise_seed=20261004,cfg=1.0,positive=pos,negative=neg,sampler=['10',0],sigmas=['11',0],latent_image=['15',0])
  add(g,17,'LTXVSeparateAVLatent',av_latent=['16',0]);add(g,18,'LTXVCropGuides',positive=pos,negative=neg,latent=['17',0]);add(g,19,'SaveLatent',samples=['18',2],filename_prefix=f'{take}/stage1_video');add(g,20,'SaveLatent',samples=['17',1],filename_prefix=f'{take}/stage1_audio')
  latents={'19':'stage1_video.latent','20':'stage1_audio.latent'};outputs['stage1_frames']=decode(g,40,['18',2],'stage1',take)
  add(g,24,'LatentUpscaleModelLoader',model_name='ltx-2.5-latent-spatial-upscaler-x2-bf16-1.0.safetensors');add(g,25,'LTXVLatentUpsampler',samples=['18',2],upscale_model=['24',0],vae=['3',0])
  pos,neg,lat=guides(g,200,['25',0]);add(g,27,'LTXVConcatAVLatent',video_latent=lat,audio_latent=['17',1]);add(g,26,'ManualSigmas',sigmas='0.85,0.7250,0.4219,0.0')
 else:
  assert take=='temporal_retake'
  for name in ['refined_video.latent','refined_audio.latent']:shutil.copyfile(R/'results/base_two_pass'/name,R/'input'/name)
  add(g,8,'LoadLatent',latent='refined_video.latent');add(g,9,'LoadLatent',latent='refined_audio.latent');add(g,12,'StudyTemporalRetakeMask',samples=['8',0],first_latent=3,last_latent=4)
  pos,neg,lat=guides(g,200,['12',0]);add(g,27,'LTXVConcatAVLatent',video_latent=lat,audio_latent=['9',0]);add(g,26,'ManualSigmas',sigmas='1.0,0.99375,0.9875,0.98125,0.975,0.909375,0.725,0.421875,0.0')
 add(g,28,'SamplerCustom',model=['1',0],add_noise=True,noise_seed=20261004,cfg=1.0,positive=pos,negative=neg,sampler=['10',0],sigmas=['26',0],latent_image=['27',0]);add(g,29,'LTXVSeparateAVLatent',av_latent=['28',0]);add(g,30,'LTXVCropGuides',positive=pos,negative=neg,latent=['29',0]);add(g,31,'SaveLatent',samples=['30',2],filename_prefix=f'{take}/refined_video');add(g,32,'SaveLatent',samples=['29',1],filename_prefix=f'{take}/refined_audio')
 latents.update({'31':'refined_video.latent','32':'refined_audio.latent'});outputs['refined_frames']=decode(g,50,['30',2],'refined',take)

 return g,outputs,latents
def run(take):
 out=R/'results'/take
 assert not (out/'receipt.json').exists(),'Attempt already exists, no silent overwrite/repeat'
 assert not req('/queue')['queue_running'] and not req('/queue')['queue_pending'],'Other queued work'
 model_job=take!='decoder_preflight';old=[json.loads(x.read_text()) for x in (R/'results').glob('*/receipt.json')];assert sum(x.get('model_job',False) for x in old)<5,'Owner-directed five-take total cap'
 g,outputs,latents=graph(take);schema=req('/object_info')
 for k,n in g.items():
  assert n['class_type'] in schema,n['class_type']
  for key in schema[n['class_type']]['input'].get('required',{}):assert key in n['inputs'],(k,key)
 out.mkdir(exist_ok=True);(out/'workflow.api.json').write_text(json.dumps(g,indent=2)+'\n')
 receipt={'take':take,'backend':'ltx25_w4a8','model_job':model_job,'started_at_utc':datetime.now(timezone.utc).isoformat(),'status':'SUBMITTING','native_stage1':[288,416] if take in {'base_two_pass','temporal_48fps'} else None,'native_refined':[576,832],'frames':81 if model_job else 1,'fps':48,'seed':20261004,'guides':[0,6,14,34,44,54,72,80],'negative_conditioning_effective':False,'guidance_method':'StandardCFG1','steps':[8,3] if take in {'base_two_pass','temporal_48fps'} else [8] if model_job else [],'source_only':True,'workflow_sha256':sha(out/'workflow.api.json'),'renderer_sha256':sha(__file__),'retake_temporal_mask':{'first_latent':3,'last_latent':4,'nominal_pixel_frames':[17,32],'spatial_scope':'complete canvas; all figure parts'} if take=='temporal_retake' else None}
 start=time.monotonic();samples=[];last_message=0
 try:
  j=req('/prompt',{'prompt':g,'client_id':str(uuid.uuid4())});(out/'submission_response.json').write_text(json.dumps(j,indent=2)+'\n');assert 'prompt_id' in j and not j.get('node_errors'),j
  pid=j['prompt_id'];receipt.update(prompt_id=pid,status='RUNNING');(out/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');print('QUEUED',take,pid,flush=True)
  while True:
   elapsed=time.monotonic()-start
   if elapsed>1800:
    q=req('/queue')
    if len(q['queue_running'])==1 and q['queue_running'][0][1]==pid:req('/interrupt',{})
    raise TimeoutError('1800-second take cap')
   p=subprocess.run(['nvidia-smi','--query-gpu=memory.used,utilization.gpu','--format=csv,noheader,nounits'],capture_output=True,text=True)
   if p.returncode==0:
    v=p.stdout.strip().split(',');samples.append({'elapsed_seconds':round(elapsed,3),'total_card_used_mib':int(v[0]),'gpu_utilization_percent':int(v[1])})
   history=req('/history/'+pid)
   if pid in history:
    h=history[pid];(out/'history.json').write_text(json.dumps(h,indent=2)+'\n')
    if h['status']['status_str']!='success':raise RuntimeError(str(h['status']['messages'][-2:]))
    for label,k in outputs.items():
     files=h['outputs'][k]['images'];assert len(files)==(81 if model_job else 1),(label,len(files));dest=out/label;dest.mkdir(exist_ok=True)
     for i,x in enumerate(files):shutil.copyfile(R/'output'/x['subfolder']/x['filename'],dest/f'{i:04d}.png')
    for k,label in latents.items():
     prefix=g[k]['inputs']['filename_prefix'].split('/')[-1];found=list((R/'output'/take).glob(prefix+'*.latent'));assert len(found)==1,(label,found);shutil.copyfile(found[0],out/label)
    receipt['status']='EXECUTION_PASS';break
   if elapsed-last_message>=30:print('RENDER_SECONDS',take,round(elapsed),'CARD_MIB',samples[-1]['total_card_used_mib'] if samples else None,flush=True);last_message=elapsed
   time.sleep(5)
 except Exception as e:receipt.update(status='EXECUTION_FAIL',error=str(e));raise
 finally:
  receipt.update(elapsed_seconds=round(time.monotonic()-start,3),observed_total_card_peak_mib=max((x['total_card_used_mib'] for x in samples),default=None),memory_sampling_interval_seconds=5)
  (out/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');(out/'memory_samples.json').write_text(json.dumps(samples,indent=2)+'\n');print('RESULT',receipt['status'],receipt['elapsed_seconds'],receipt['observed_total_card_peak_mib'],flush=True)
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('take',choices=['temporal_48fps']);run(a.parse_args().take)
