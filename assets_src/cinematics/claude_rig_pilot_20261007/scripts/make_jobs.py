#!/usr/bin/env python3
"""Write rig-pilot job files for pc_runner/rig_pilot_runner.py (the RTX 3060 Ti ComfyUI install).

Each job is the Union take-1 two-pass recipe (LTX-2.5 W4A8 + Union IC-LoRA, 41 frames at 24 fps,
320x448 x 8 steps then 640x896 x 3 steps, seed 20261004) with named, controlled changes:
  a1_rigguides  rig guides (run2) + the arm-length sentence in run2/prompt.txt; otherwise identical to Union take 1
  a2_endlock    a1 + the approved opening image also locked at frame 40 + a finger-separation sentence
                in place of "Clean connected fingers"
Writes jobs/<job_id>.json (graph, input hashes, output labels) and stages the runtime inputs under
staging/input/rig_pilot/ for the connected-folder copy. Numbers and graphs only.

    python -I scripts/make_jobs.py a1_rigguides a2_endlock
"""
import hashlib, json, shutil, sys
from pathlib import Path

PILOT = Path(__file__).resolve().parents[1]
UNION = PILOT.parent / 'ltx25_union_trial_20261004'
STAGE = PILOT / 'pc_runner' / 'staging'
ARM = (' The waving arm keeps one constant length and the open hand one constant size in every frame; the arm '
       'bends at the elbow in the picture plane and never points toward the viewer.')
FINGERS = ('Five clearly separated fingers on the open hand and crisp hands in every frame, without motion blur, '
           'smearing or fused fingers,')
RECIPES = {
    'a1_rigguides': {'guide_set': 'run2', 'end_lock': False, 'fingers': False, 'seed': 20261004,
                     'note': 'Controlled change vs Union take 1: rig guides (W3 0.0%) + arm-length sentence'},
    'a2_endlock': {'guide_set': 'run2', 'end_lock': True, 'fingers': True, 'seed': 20261004,
                   'note': 'a1 + approved opening image also at frame 40 (loop lock) + finger-separation sentence'},
}


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def prompt_for(r):
    base = (UNION / 'prompt.txt').read_text().strip()
    if r['fingers']:
        assert 'Clean connected fingers,' in base
        base = base.replace('Clean connected fingers,', FINGERS)
    return base + ARM


def graph(job_id, r):
    g = {}
    def n(i, kind, **args):
        g[str(i)] = {'class_type': kind, 'inputs': args}; return str(i)
    n(1, 'UNETLoader', unet_name='ltx-2.5-22b-distilled-transformer-w4a8_convrot.safetensors', weight_dtype='default')
    n(2, 'CLIPLoader', clip_name='gemma4-12b-with-proj-ltx-2.5-w4a8_convrot.safetensors', type='ltxv', device='default')
    n(3, 'VAELoader', vae_name='ltx-2.5-video-vae-bf16.safetensors'); n(4, 'VAELoader', vae_name='ltx-2.5-audio-vae-bf16.safetensors')
    n(80, 'LTXICLoRALoaderModelOnly', model=['1', 0], lora_name='ltx-2.3-22b-ic-lora-union-control-ref0.5.safetensors', strength_model=1.0)
    n(81, 'UnionModelProof', model=['80', 0], downscale=['80', 1])
    n(5, 'CLIPTextEncode', clip=['2', 0], text=prompt_for(r)); n(6, 'ConditioningZeroOut', conditioning=['5', 0])
    n(7, 'LTXVConditioning', positive=['5', 0], negative=['6', 0], frame_rate=24)
    n(8, 'EmptyLTXVLatentVideo', width=320, height=448, length=41, batch_size=1)
    n(9, 'LTXVEmptyLatentAudio', frames_number=41, frame_rate=24, batch_size=1, audio_vae=['4', 0])
    n(10, 'KSamplerSelect', sampler_name='euler_ancestral'); n(11, 'ManualSigmas', sigmas='1.0,0.99375,0.9875,0.98125,0.975,0.909375,0.725,0.421875,0.0')
    n(12, 'LoadImage', image='rig_pilot/identity_first_frame.png')

    def identity(i, latent, pos, neg):
        """Opening image at frame 0; with end_lock the same image again at frame 40. Returns the last node id."""
        a = n(i, 'LTXVAddGuide', positive=pos, negative=neg, vae=['3', 0], latent=latent, image=['12', 0], frame_idx=0, strength=1.0)
        if r['end_lock']:
            a = n(i + 100, 'LTXVAddGuide', positive=[a, 0], negative=[a, 1], vae=['3', 0], latent=[a, 2], image=['12', 0], frame_idx=40, strength=1.0)
        return a

    def control(i, image, src):
        n(i, 'LTXAddVideoICLoRAGuide', positive=[src, 0], negative=[src, 1], vae=['3', 0], latent=[src, 2], image=image, frame_idx=0,
          strength=1.0, latent_downscale_factor=['80', 1], crop='disabled', use_tiled_encode=True, tile_size=256, tile_overlap=64,
          use_streaming=False, tile_frames=41)
    s1 = identity(13, ['8', 0], ['7', 0], ['7', 1])
    n(14, 'RigPilotGuideBatch', guide_set=r['guide_set'], lane='quarter', frames=41)
    control(15, ['14', 0], s1)
    n(16, 'LTXVConcatAVLatent', video_latent=['15', 2], audio_latent=['9', 0])
    n(17, 'SamplerCustom', model=['81', 0], add_noise=True, noise_seed=r['seed'], cfg=1.0, positive=['15', 0], negative=['15', 1],
      sampler=['10', 0], sigmas=['11', 0], latent_image=['16', 0])
    n(18, 'LTXVSeparateAVLatent', av_latent=['17', 0]); n(19, 'LTXVCropGuides', positive=['15', 0], negative=['15', 1], latent=['18', 0])
    n(20, 'SaveLatent', samples=['19', 2], filename_prefix=f'rig_pilot/{job_id}/stage1_video')
    n(21, 'LatentUpscaleModelLoader', model_name='ltx-2.5-latent-spatial-upscaler-x2-bf16-1.0.safetensors')
    n(22, 'LTXVLatentUpsampler', samples=['19', 2], upscale_model=['21', 0], vae=['3', 0])
    s2 = identity(23, ['22', 0], ['7', 0], ['7', 1])
    n(24, 'RigPilotGuideBatch', guide_set=r['guide_set'], lane='half', frames=41)
    control(25, ['24', 0], s2)
    n(26, 'LTXVConcatAVLatent', video_latent=['25', 2], audio_latent=['18', 1]); n(27, 'ManualSigmas', sigmas='0.85,0.7250,0.4219,0.0')
    n(28, 'SamplerCustom', model=['81', 0], add_noise=True, noise_seed=r['seed'], cfg=1.0, positive=['25', 0], negative=['25', 1],
      sampler=['10', 0], sigmas=['27', 0], latent_image=['26', 0])
    n(29, 'LTXVSeparateAVLatent', av_latent=['28', 0]); n(30, 'LTXVCropGuides', positive=['25', 0], negative=['25', 1], latent=['29', 0])
    n(31, 'SaveLatent', samples=['30', 2], filename_prefix=f'rig_pilot/{job_id}/refined_video')
    n(40, 'VAEDecodeTiled', samples=['19', 2], vae=['3', 0], tile_size=256, overlap=64, temporal_size=64, temporal_overlap=8)
    n(41, 'StudyFiniteImages', images=['40', 0]); n(42, 'SaveImage', images=['41', 0], filename_prefix=f'rig_pilot/{job_id}/stage1/frame')
    n(50, 'VAEDecodeTiled', samples=['30', 2], vae=['3', 0], tile_size=256, overlap=64, temporal_size=64, temporal_overlap=8)
    n(51, 'UnionOutputProof', images=['50', 0]); n(52, 'SaveImage', images=['51', 0], filename_prefix=f'rig_pilot/{job_id}/refined/frame')
    n(90, 'StudyRuntimeReceipt', label=job_id)
    return g


def stage_inputs(guide_set):
    pairs = [(UNION / 'identity_first_frame.png', 'rig_pilot/identity_first_frame.png')]
    for lane in ('half', 'quarter'):
        pairs += [(PILOT / guide_set / f'guide_{lane}/{i:04d}.png', f'rig_pilot/{guide_set}/guide_{lane}/{i:04d}.png') for i in range(41)]
    rows = []
    for src, rel in pairs:
        dst = STAGE / 'input' / rel; dst.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(src, dst)
        rows.append({'path': rel, 'sha256': sha(src), 'source': str(src.relative_to(PILOT.parents[2])).replace('\\', '/')})
    return rows


def main(ids):
    (PILOT / 'jobs').mkdir(exist_ok=True)
    for jid in ids:
        r = RECIPES[jid]
        job = {'job_id': jid, 'note': r['note'], 'recipe': r, 'prompt': prompt_for(r), 'timeout_s': 1800,
               'inputs': stage_inputs(r['guide_set']), 'graph': graph(jid, r),
               'outputs': {'42': 'stage1_frames', '52': 'refined_frames', '20': 'stage1_latent', '31': 'refined_latent'},
               'controlled_baseline': 'assets_src/cinematics/ltx25_union_trial_20261004/take_1 (workflow c027567040d2588c)',
               'used_as_delivery_pixels': False}
        p = PILOT / 'jobs' / f'{jid}.json'
        p.write_text(json.dumps(job, indent=2) + '\n')
        print(jid, sha(p), len(job['graph']), 'nodes')


if __name__ == '__main__':
    main(sys.argv[1:] or list(RECIPES))
