"""Bounded local source-only LTX sample; preserves native decoded PNG frames."""
import argparse,json,hashlib,time,urllib.request,shutil,subprocess
from datetime import datetime,timezone
from pathlib import Path
URL='http://127.0.0.1:8190'
def req(route,data=None):
 d=None if data is None else json.dumps(data).encode()
 with urllib.request.urlopen(urllib.request.Request(URL+route,data=d,headers={'Content-Type':'application/json'}),timeout=30) as f:
  b=f.read();return json.loads(b) if b else {}
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
a=argparse.ArgumentParser();a.add_argument('--packet',type=Path,required=True);a.add_argument('--take',default='registered');a.add_argument('--input-series',default='registered_key');a.add_argument('--prompt-file',default='wave.txt');a.add_argument('--frames',type=int,default=41);args=a.parse_args();p=args.packet.resolve();guide_strength=2.0 if args.take=='registered_strong' else 1.0
root=Path(r'H:\MermaidReefTools\LocalVideo');out=p/'results'/args.take;out.mkdir(exist_ok=True);(out/'native_frames').mkdir(exist_ok=True)
if (out/'receipt.json').exists():raise RuntimeError('Existing attempt receipt preserved; do not resubmit')
q=req('/queue')
ahead=[row[1] for rows in q.values() for row in rows]
if ahead:print('SHARED_QUEUE_AHEAD',len(ahead),'existing jobs left untouched',flush=True)
g=json.loads((p/'environment/base_workflow.api.json').read_text())
if args.frames not in [41,81]:raise ValueError('Only bounded declared 41/81-frame studies supported')
g['8']['inputs']['length']=args.frames
indices=[0,14,34,54,72,80] if args.frames==81 else [0,7,17,27,36,40]
bindings=[]
for i,idx in enumerate(indices):
 key=[0,1,2,3,0,0][i];f=p/f'inputs/{args.input_series}_{key:02d}.png';name='ltx_registered_'+sha(f)[:20]+'.png';shutil.copyfile(f,root/'input'/name)
 bindings.append({'frame_index':idx,'path':str(f.relative_to(p)).replace('\\','/'),'sha256':sha(f),'role':'Owned appearance-bearing pose control, not POSITION_GUIDE_ONLY','strength':1.0 if i==0 else guide_strength})
 if i==0:g['4']['inputs']['image']=name;continue
 lid=str(20+i*2);nid=str(21+i*2);g[lid]={'class_type':'LoadImage','inputs':{'image':name}}
 prev='8' if i==1 else str(21+(i-1)*2)
 g[nid]={'class_type':'LTXVAddGuide','inputs':{'positive':[prev,0],'negative':[prev,1],'latent':[prev,2],'vae':['1',2],'image':[lid,0],'frame_idx':idx,'strength':guide_strength}}
last=str(21+5*2)
g['5']['inputs']['text']=(p/'briefs'/args.prompt_file).read_text(encoding='utf-8')
g['9']['inputs'].update(positive=[last,0],negative=[last,1],latent_image=[last,2])
g['40']={'class_type':'LTXVCropGuides','inputs':{'positive':[last,0],'negative':[last,1],'latent':['9',0]}}
g['10']['inputs']['samples']=['40',2]
g['11']['inputs']['filename_prefix']='local_reference/ltx_registered_wave_20261004_'+args.take
g['14']={'class_type':'SaveImage','inputs':{'images':['10',0],'filename_prefix':'local_reference/ltx_registered_wave_20261004_'+args.take+'/frame'}}
(out/'workflow.api.json').write_text(json.dumps(g,indent=2)+'\n');(out/'bindings.json').write_text(json.dumps(bindings,indent=2)+'\n')
j={'status':'SUBMITTING','acceptance':'REFERENCE_ONLY','model':'LTX-Video 2B 0.9.8 distilled','attempt':5 if args.take=='figure_wide_slow' else (4 if args.take=='figure_wide_root' else (3 if args.take=='figure_wide' else (2 if args.take=='registered_strong' else 1))),'started_at_utc':datetime.now(timezone.utc).isoformat(),'workflow_sha256':sha(out/'workflow.api.json'),'prompt_sha256':sha(p/'briefs'/args.prompt_file),'settings':{'width':896,'height':512,'frames':args.frames,'fps':24,'steps':7,'seed':20261003,'first_frame_strength':1.0,'guide_strength':guide_strength,'refinement_pass':False},'outputs':[],'resource_samples':[],'queue_ahead_prompt_ids':ahead}
(out/'receipt.json').write_text(json.dumps(j,indent=2)+'\n');start=time.monotonic();pid=None
try:
 pid=req('/prompt',{'prompt':g,'client_id':'ltx_registered_wave_20261004'})['prompt_id'];j['prompt_id']=pid;print('SUBMITTED',pid,flush=True)
 while time.monotonic()-start<3600:
  h=req('/history/'+pid)
  if pid in h:break
  running=req('/queue').get('queue_running',[])
  if any(x[1]==pid for x in running):
   if 'sampling_started_elapsed_seconds' not in j:j['sampling_started_elapsed_seconds']=round(time.monotonic()-start,3)
   if time.monotonic()-start-j['sampling_started_elapsed_seconds']>1800:
    req('/interrupt',{});raise TimeoutError('Owned sampling exceeded 1800s cap')
  if not j['resource_samples'] or time.monotonic()-start-j['resource_samples'][-1]['elapsed_seconds']>15:
   sm=subprocess.run(['nvidia-smi','--query-gpu=memory.used,utilization.gpu','--format=csv,noheader,nounits'],capture_output=True,text=True)
   j['resource_samples'].append({'elapsed_seconds':round(time.monotonic()-start,2),'gpu_used_mib_util_percent':sm.stdout.strip()})
  time.sleep(3)
 else:
  if any(x[1]==pid for x in req('/queue').get('queue_running',[])):req('/interrupt',{})
  pending=req('/queue').get('queue_pending',[])
  if any(x[1]==pid for x in pending):req('/queue',{'delete':[pid]})
  raise TimeoutError('Owned queue/render wall cap reached; no unrelated job interrupted')
 result=h[pid];(out/'history.json').write_text(json.dumps(result,indent=2)+'\n')
 if result.get('status',{}).get('status_str')!='success':raise RuntimeError(str(result.get('status')))
 frames=result['outputs']['14']['images']
 if len(frames)!=args.frames:raise RuntimeError('Native decoded frame coverage mismatch')
 for i,v in enumerate(frames):
  f=(root/'output'/v.get('subfolder','')/v['filename']).resolve()
  if not f.is_relative_to((root/'output').resolve()):raise RuntimeError('Output path outside declared root')
  dst=out/'native_frames'/f'{i:04d}.png';shutil.copyfile(f,dst);j['outputs'].append({'path':str(dst.relative_to(out)).replace('\\','/'),'sha256':sha(dst),'bytes':dst.stat().st_size,'native_index':i})
 for v in result['outputs']['11'].get('images',[])+result['outputs']['11'].get('videos',[]):
  f=root/'output'/v.get('subfolder','')/v['filename'];dst=out/('native'+f.suffix);shutil.copyfile(f,dst);j['outputs'].append({'path':dst.name,'sha256':sha(dst),'bytes':dst.stat().st_size})
 j['status']='EXECUTION_PASS'
except Exception as e:j['status']='FAILED';j['error']=str(e)
j['elapsed_seconds']=round(time.monotonic()-start,3);j['completed_at_utc']=datetime.now(timezone.utc).isoformat();(out/'receipt.json').write_text(json.dumps(j,indent=2)+'\n');print(j['status'],j['elapsed_seconds'],j.get('error',''),flush=True)
if not req('/queue').get('queue_running') and not req('/queue').get('queue_pending'):req('/free',{'unload_models':True,'free_memory':True})
if j['status']!='EXECUTION_PASS':raise SystemExit(1)
