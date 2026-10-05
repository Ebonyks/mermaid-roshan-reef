"""Fifth bounded take: Aseprite multi-anchor exports, source gate before queue."""
from pathlib import Path
import json,urllib.request,uuid,time,hashlib,subprocess,shutil,sys
from datetime import datetime,timezone
sys.path.insert(0,str(Path(__file__).resolve().parent))
from render import req,sha,graph
from verify_registered_guides import check
P=Path(__file__).resolve().parents[1]
R=Path(r'H:\MermaidReefTools\LocalVideo\ltx25')
def run(take):
 out=R/'results'/take
 assert not (out/'receipt.json').exists(),'Attempt already exists, no silent overwrite/repeat'
 assert not req('/queue')['queue_running'] and not req('/queue')['queue_pending'],'Other queued work'
 model_job=take!='decoder_preflight';old=[json.loads(x.read_text()) for x in (R/'results').glob('*/receipt.json')];assert sum(x.get('model_job',False) for x in old)<5,'Owner-directed five-take task cap'
 preflight=check(write=False)
 for row in preflight['rows']:
  source=P/row['path'];assert sha(source)==row['sha256'];destination=R/'input/scale_registered'/source.name;destination.parent.mkdir(exist_ok=True);shutil.copyfile(source,destination)
 g,outputs,latents=graph('base_two_pass')
 for node in g.values():
  if node['class_type']=='LoadImage':node['inputs']['image']='scale_registered/'+node['inputs']['image']
  if 'filename_prefix' in node['inputs']:node['inputs']['filename_prefix']=node['inputs']['filename_prefix'].replace('base_two_pass/',take+'/')
 g['5']['inputs']['text']+=' Keep the whole figure at the same world scale throughout. The waist remains at pixel (184.5,453) on the 576 by 832 fixed canvas. Head, shoulders, bodice, hair and tail respond continuously to the wave without a camera zoom.'
 g['900']['inputs']['label']=take
 schema=req('/object_info')
 for k,n in g.items():
  assert n['class_type'] in schema,n['class_type']
  for key in schema[n['class_type']]['input'].get('required',{}):assert key in n['inputs'],(k,key)
 out.mkdir(exist_ok=True);(out/'workflow.api.json').write_text(json.dumps(g,indent=2)+'\n')
 receipt={'take':take,'backend':'ltx25_w4a8','model_job':model_job,'started_at_utc':datetime.now(timezone.utc).isoformat(),'status':'SUBMITTING','native_stage1':[288,416] if True else None,'native_refined':[576,832],'frames':41 if model_job else 1,'fps':24,'seed':20261004,'guides':[0,3,7,17,22,27,36,40],'negative_conditioning_effective':take=='anti_blur_nag','guidance_method':'LTX2_NAG5_alpha0.15_tau2.5' if take=='anti_blur_nag' else 'StandardCFG1','steps':[8,3] if True else [8] if model_job else [],'source_only':True,'source_preflight_sha256':sha(P/'scale_continuity/registered_preflight.json'),'guide_hashes':{r['path']:r['sha256'] for r in preflight['rows']},'prompt_sha256':hashlib.sha256(g['5']['inputs']['text'].encode()).hexdigest(),'workflow_sha256':sha(out/'workflow.api.json'),'renderer_sha256':sha(__file__),'retake_temporal_mask':{'first_latent':3,'last_latent':4,'nominal_pixel_frames':[17,32],'spatial_scope':'complete canvas; all figure parts'} if take=='temporal_retake' else None}
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
     files=h['outputs'][k]['images'];assert len(files)==(41 if model_job else 1),(label,len(files));dest=out/label;dest.mkdir(exist_ok=True)
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
if __name__=='__main__':run('scale_registered')
