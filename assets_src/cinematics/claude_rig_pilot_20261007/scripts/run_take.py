"""Run 2 generation step: one LTX-2.5 Union take on the rig guides. UNTESTED in the cloud session.

Same recipe, seed, adapter, identity opening and stage geometry as
ltx25_union_trial_20261004/scripts/render.py take 1; the only intended change is the structural
guide family (run2/guide_half, run2/guide_quarter) plus one prompt sentence on constant arm length.
That makes the result a controlled comparison with Union take 1.

Prerequisites on the RTX 3060 Ti machine: the Union trial's ComfyUI install (127.0.0.1:8194) with its
study nodes, and scripts/comfy_rig_pilot_nodes.py copied into ComfyUI/custom_nodes (restart after).
    python run_take.py take_1 [--runtime H:\\MermaidReefTools\\LocalVideo\\ltx25]
Two takes per brief (DL-MOT-16), counting failures; results land in run2/<take>/.
"""
from pathlib import Path
import json, urllib.request, uuid, time, hashlib, subprocess, shutil, argparse
from datetime import datetime, timezone

P = Path(__file__).resolve().parents[1] / 'run2'
UNION = Path(__file__).resolve().parents[2] / 'ltx25_union_trial_20261004'
PROMPT_EXTRA = (' The waving arm keeps one constant length and the open hand one constant size in every frame; the arm '
                'bends at the elbow in the picture plane and never points toward the viewer.')


def sha(p):
    with Path(p).open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def req(path, data=None):
    body = json.dumps(data).encode() if data is not None else None
    with urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:8194' + path, data=body, headers={'Content-Type': 'application/json'}), timeout=30) as f:
        return json.load(f)


def graph(take):
    g = {}
    def n(i, kind, **args):
        g[str(i)] = {'class_type': kind, 'inputs': args}; return str(i)
    n(1, 'UNETLoader', unet_name='ltx-2.5-22b-distilled-transformer-w4a8_convrot.safetensors', weight_dtype='default')
    n(2, 'CLIPLoader', clip_name='gemma4-12b-with-proj-ltx-2.5-w4a8_convrot.safetensors', type='ltxv', device='default')
    n(3, 'VAELoader', vae_name='ltx-2.5-video-vae-bf16.safetensors'); n(4, 'VAELoader', vae_name='ltx-2.5-audio-vae-bf16.safetensors')
    n(80, 'LTXICLoRALoaderModelOnly', model=['1', 0], lora_name='ltx-2.3-22b-ic-lora-union-control-ref0.5.safetensors', strength_model=1.0)
    n(81, 'UnionModelProof', model=['80', 0], downscale=['80', 1])
    prompt = (UNION / 'prompt.txt').read_text().strip() + PROMPT_EXTRA
    (P / 'prompt.txt').write_text(prompt + '\n')
    n(5, 'CLIPTextEncode', clip=['2', 0], text=prompt); n(6, 'ConditioningZeroOut', conditioning=['5', 0]); n(7, 'LTXVConditioning', positive=['5', 0], negative=['6', 0], frame_rate=24)
    n(8, 'EmptyLTXVLatentVideo', width=320, height=448, length=41, batch_size=1)
    n(9, 'LTXVEmptyLatentAudio', frames_number=41, frame_rate=24, batch_size=1, audio_vae=['4', 0])
    n(10, 'KSamplerSelect', sampler_name='euler_ancestral'); n(11, 'ManualSigmas', sigmas='1.0,0.99375,0.9875,0.98125,0.975,0.909375,0.725,0.421875,0.0')
    n(12, 'LoadImage', image='rig_pilot/identity_first_frame.png')
    n(13, 'LTXVAddGuide', positive=['7', 0], negative=['7', 1], vae=['3', 0], latent=['8', 0], image=['12', 0], frame_idx=0, strength=1.0)
    n(14, 'RigPilotGuideBatch', lane='quarter', frames=41)
    def control(i, image, latent, pos, neg):
        n(i, 'LTXAddVideoICLoRAGuide', positive=pos, negative=neg, vae=['3', 0], latent=latent, image=image, frame_idx=0, strength=1.0,
          latent_downscale_factor=['80', 1], crop='disabled', use_tiled_encode=True, tile_size=256, tile_overlap=64, use_streaming=False, tile_frames=41)
    control(15, ['14', 0], ['13', 2], ['13', 0], ['13', 1])
    n(16, 'LTXVConcatAVLatent', video_latent=['15', 2], audio_latent=['9', 0])
    n(17, 'SamplerCustom', model=['81', 0], add_noise=True, noise_seed=20261004, cfg=1.0, positive=['15', 0], negative=['15', 1], sampler=['10', 0], sigmas=['11', 0], latent_image=['16', 0])
    n(18, 'LTXVSeparateAVLatent', av_latent=['17', 0]); n(19, 'LTXVCropGuides', positive=['15', 0], negative=['15', 1], latent=['18', 0])
    n(20, 'SaveLatent', samples=['19', 2], filename_prefix=f'rig_pilot/{take}/stage1_video')
    n(21, 'LatentUpscaleModelLoader', model_name='ltx-2.5-latent-spatial-upscaler-x2-bf16-1.0.safetensors'); n(22, 'LTXVLatentUpsampler', samples=['19', 2], upscale_model=['21', 0], vae=['3', 0])
    n(23, 'LTXVAddGuide', positive=['7', 0], negative=['7', 1], vae=['3', 0], latent=['22', 0], image=['12', 0], frame_idx=0, strength=1.0)
    n(24, 'RigPilotGuideBatch', lane='half', frames=41); control(25, ['24', 0], ['23', 2], ['23', 0], ['23', 1])
    n(26, 'LTXVConcatAVLatent', video_latent=['25', 2], audio_latent=['18', 1]); n(27, 'ManualSigmas', sigmas='0.85,0.7250,0.4219,0.0')
    n(28, 'SamplerCustom', model=['81', 0], add_noise=True, noise_seed=20261004, cfg=1.0, positive=['25', 0], negative=['25', 1], sampler=['10', 0], sigmas=['27', 0], latent_image=['26', 0])
    n(29, 'LTXVSeparateAVLatent', av_latent=['28', 0]); n(30, 'LTXVCropGuides', positive=['25', 0], negative=['25', 1], latent=['29', 0])
    n(31, 'SaveLatent', samples=['30', 2], filename_prefix=f'rig_pilot/{take}/refined_video')
    n(40, 'VAEDecodeTiled', samples=['19', 2], vae=['3', 0], tile_size=256, overlap=64, temporal_size=64, temporal_overlap=8)
    n(41, 'StudyFiniteImages', images=['40', 0]); n(42, 'SaveImage', images=['41', 0], filename_prefix=f'rig_pilot/{take}/stage1/frame')
    n(50, 'VAEDecodeTiled', samples=['30', 2], vae=['3', 0], tile_size=256, overlap=64, temporal_size=64, temporal_overlap=8)
    n(51, 'UnionOutputProof', images=['50', 0]); n(52, 'SaveImage', images=['51', 0], filename_prefix=f'rig_pilot/{take}/refined/frame')
    n(90, 'StudyRuntimeReceipt', label=take)
    return g


def stage_inputs(RT):
    dst = RT / 'input/rig_pilot'; pairs = [(UNION / 'identity_first_frame.png', dst / 'identity_first_frame.png')]
    for lane in ('half', 'quarter'):
        pairs += [(P / f'guide_{lane}/{i:04d}.png', dst / f'guide_{lane}/{i:04d}.png') for i in range(41)]
    for src, d in pairs:
        d.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(src, d)
        assert sha(src) == sha(d), f'Runtime input mismatch {d}'
    return [src for src, _ in pairs]


def main(take, RT):
    existing = list(P.glob('take_*/receipt.json')); assert len(existing) < 2, 'Two-take cap includes failures'
    out = P / take; out.mkdir(exist_ok=True); assert not (out / 'receipt.json').exists(), 'No silent repeated take'
    q = req('/queue'); assert not q['queue_running'] and not q['queue_pending'], 'Other queued work'
    sources = stage_inputs(RT)
    g = graph(take); schema = req('/object_info')
    for node in g.values():
        assert node['class_type'] in schema, f"Missing node {node['class_type']} (install comfy_rig_pilot_nodes.py and restart)"
        assert not set(schema[node['class_type']]['input'].get('required', {})) - set(node['inputs']), node
    (out / 'workflow.api.json').write_text(json.dumps(g, indent=2) + '\n')
    j = {'status': 'SUBMITTING', 'started_at_utc': datetime.now(timezone.utc).isoformat(), 'take': take, 'engine': 'LTX-2.5 W4A8',
         'adapter': 'Union Control 2.3-trained official 2.5 route', 'control_strength': 1.0, 'identity_first_frame_strength': 1.0,
         'adapter_sha256': json.loads((UNION / 'adapter_download.json').read_text())['sha256'],
         'source_hashes': {str(f.relative_to(P.parents[3])).replace('\\', '/'): sha(f) for f in sources},
         'workflow_sha256': sha(out / 'workflow.api.json'), 'seed': 20261004, 'stages': [[320, 448, 8], [640, 896, 3]], 'frames': 41, 'fps': 24,
         'new_imagegen_calls': 0, 'controlled_change_vs_union_take_1': 'guide family (rig guides) + one prompt sentence'}
    start = time.monotonic(); memory = []; last = 0; pid = None
    try:
        submit = req('/prompt', {'prompt': g, 'client_id': str(uuid.uuid4())}); (out / 'submission.json').write_text(json.dumps(submit, indent=2) + '\n')
        assert 'prompt_id' in submit and not submit.get('node_errors'), submit
        pid = submit['prompt_id']; j.update(status='RUNNING', prompt_id=pid); print('QUEUED_RIG_PILOT', pid, flush=True)
        while time.monotonic() - start < 1200:
            elapsed = time.monotonic() - start
            sample = subprocess.run(['nvidia-smi', '--query-gpu=memory.used,utilization.gpu', '--format=csv,noheader,nounits'], capture_output=True, text=True)
            if sample.returncode == 0:
                x = sample.stdout.strip().split(','); memory.append({'elapsed_seconds': elapsed, 'card_used_mib': int(x[0]), 'utilization_percent': int(x[1])})
            h = req('/history/' + pid)
            if pid in h:
                h = h[pid]; (out / 'history.json').write_text(json.dumps(h, indent=2) + '\n'); assert h['status']['status_str'] == 'success', h['status']['messages'][-2:]
                for label, key in [('stage1_frames', '42'), ('refined_frames', '52')]:
                    imgs = h['outputs'][key]['images']; assert len(imgs) == 41
                    dest = out / label; dest.mkdir(exist_ok=True)
                    for i, x in enumerate(imgs): shutil.copyfile(RT / 'output' / x['subfolder'] / x['filename'], dest / f'{i:04d}.png')
                for label in ['stage1_video', 'refined_video']:
                    files = list((RT / 'output/rig_pilot' / take).glob(label + '*.latent')); assert len(files) == 1
                    shutil.copyfile(files[0], out / (label + '.latent'))
                for f in ['patch_install.json', 'patch_execution.json']: shutil.copyfile(RT / 'results/union_trial' / f, out / f)
                j['status'] = 'EXECUTION_PASS'; break
            if elapsed - last >= 30:
                print('RIG_PILOT_SECONDS', round(elapsed), 'CARD_MIB', memory[-1]['card_used_mib'] if memory else None, flush=True); last = elapsed
            time.sleep(5)
        else:
            raise TimeoutError('20-minute take cap')
    except Exception as e:
        j.update(status='EXECUTION_FAIL', error=str(e))
        if pid:
            q = req('/queue')
            if len(q['queue_running']) == 1 and q['queue_running'][0][1] == pid: req('/interrupt', {})
        raise
    finally:
        j.update(elapsed_seconds=time.monotonic() - start, sampled_card_peak_mib=max((x['card_used_mib'] for x in memory), default=None))
        (out / 'receipt.json').write_text(json.dumps(j, indent=2) + '\n'); (out / 'memory_samples.json').write_text(json.dumps(memory, indent=2) + '\n')
        print('RIG_PILOT_RESULT', j['status'], j['elapsed_seconds'], j['sampled_card_peak_mib'], flush=True)


if __name__ == '__main__':
    a = argparse.ArgumentParser(); a.add_argument('take', choices=['take_1', 'take_2'])
    a.add_argument('--runtime', default=r'H:\MermaidReefTools\LocalVideo\ltx25'); v = a.parse_args(); main(v.take, Path(v.runtime))
