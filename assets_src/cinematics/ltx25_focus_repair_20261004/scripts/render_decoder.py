"""One controlled 1-vs2-step decoder ablation from the existing fifth take."""
import json,urllib.request,uuid,time,hashlib,shutil,subprocess
from pathlib import Path
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parents[1];ROOT=P.parents[2]
OLD=ROOT/'assets_src/cinematics/ltx25_8gb_wave_20261004'
R=Path(r'H:\MermaidReefTools\LocalVideo\ltx25');BASE='http://127.0.0.1:8194'
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def request(path,data=None):
    body=json.dumps(data).encode() if data is not None else None
    with urllib.request.urlopen(urllib.request.Request(BASE+path,data=body,headers={'Content-Type':'application/json'}),timeout=30) as f:return json.load(f)
def main():
    assert not (P/'receipt.json').exists(),'One ablation only; retain failures'
    queue=request('/queue');assert not queue['queue_running'] and not queue['queue_pending'],'Other queued work'
    src=OLD/'results/scale_registered/refined_video.latent';name='focus_registered_video.latent'
    shutil.copyfile(src,R/'input'/name)
    g={'1':{'class_type':'VAELoader','inputs':{'vae_name':'ltx-2.5-video-vae-bf16.safetensors'}},
       '2':{'class_type':'LoadLatent','inputs':{'latent':name}}}
    for steps in [1,2]:
        key=str(steps+2)
        g[key]={'class_type':'FocusDecoderAblation','inputs':{'samples':['2',0],'vae':['1',0],'steps':steps}}
        g[str(steps+4)]={'class_type':'SaveImage','inputs':{'images':[key,0],'filename_prefix':f'focus_decoder_ablation/steps_{steps}/frame'}}
    assert all(n['class_type'] in request('/object_info') for n in g.values())
    (P/'workflow.api.json').write_text(json.dumps(g,indent=2)+'\n',encoding='utf-8')
    receipt={'status':'SUBMITTING','method':'Saved identical video latent, publisher1-step vs experimental2-step decoder; no transformer resampling',
             'new_transformer_jobs':0,'new_imagegen_calls':0,'new_decoder_ablation_jobs':1,'source_latent':src.relative_to(ROOT).as_posix(),
             'source_latent_sha256':sha(src),'workflow_sha256':sha(P/'workflow.api.json'),'frames':41,'fps':24,'source_only':True}
    start=time.monotonic();memory=[];(P/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    try:
        submission=request('/prompt',{'prompt':g,'client_id':str(uuid.uuid4())});assert 'prompt_id' in submission and not submission.get('node_errors'),submission
        pid=submission['prompt_id'];receipt.update(prompt_id=pid,status='RUNNING');print('QUEUED_DECODER_ABLATION',pid,flush=True)
        while time.monotonic()-start<900:
            n=subprocess.run(['nvidia-smi','--query-gpu=memory.used','--format=csv,noheader,nounits'],capture_output=True,text=True)
            if n.returncode==0:memory.append({'elapsed_seconds':time.monotonic()-start,'card_used_mib':int(n.stdout.strip())})
            history=request('/history/'+pid)
            if pid in history:
                h=history[pid];(P/'history.json').write_text(json.dumps(h,indent=2)+'\n',encoding='utf-8')
                assert h['status']['status_str']=='success',h['status']['messages'][-2:]
                for steps in [1,2]:
                    out=P/f'decoder_{steps}_frames';out.mkdir(exist_ok=True)
                    files=h['outputs'][str(steps+4)]['images'];assert len(files)==41
                    for i,x in enumerate(files):shutil.copyfile(R/'output'/x['subfolder']/x['filename'],out/f'{i:04d}.png')
                    shutil.copyfile(R/f'results/focus_decoder_ablation/steps_{steps}.json',P/f'decoder_{steps}_proof.json')
                exact=[]
                for i in range(41):
                    a=np.array(Image.open(OLD/f'results/scale_registered/refined_frames/{i:04d}.png').convert('RGBA'))
                    b=np.array(Image.open(P/f'decoder_1_frames/{i:04d}.png').convert('RGBA'))
                    exact.append(bool(np.array_equal(a,b)))
                receipt.update(status='DECODE_EXECUTION_PASS',baseline_pixel_identical_frames=sum(exact),baseline_per_frame_exact=exact)
                assert all(exact),'Baseline re-decode does not reproduce original pixels; interpretation requires diagnosis'
                # Baseline files duplicate already published originals; retain only the parity proof.
                for f in sorted((P/'decoder_1_frames').glob('*.png')):f.unlink()
                (P/'decoder_1_frames').rmdir()
                break
            time.sleep(3)
        else:
            q=request('/queue')
            if len(q['queue_running'])==1 and q['queue_running'][0][1]==pid:request('/interrupt',{})
            raise TimeoutError('900-second decoder ablation ceiling')
    except Exception as e:receipt.update(status='DECODE_EXECUTION_FAIL',error=str(e));raise
    finally:
        receipt.update(elapsed_seconds=time.monotonic()-start,observed_card_peak_mib=max((r['card_used_mib'] for r in memory),default=None))
        (P/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
        (P/'memory_samples.json').write_text(json.dumps(memory,indent=2)+'\n',encoding='utf-8')
        print('DECODER_RESULT',receipt['status'],receipt.get('baseline_pixel_identical_frames'),receipt['elapsed_seconds'],receipt['observed_card_peak_mib'],flush=True)
if __name__=='__main__':main()
