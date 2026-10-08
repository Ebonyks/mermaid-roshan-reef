#!/usr/bin/env python3
"""Write rig-pilot job files for pc_runner/rig_pilot_runner.py (the RTX 3060 Ti ComfyUI install).

Each job is the Union take-1 two-pass recipe (LTX-2.5 W4A8 + Union IC-LoRA, 41 frames at 24 fps,
320x448 x 8 steps then 640x896 x 3 steps, seed 20261004) with named, controlled changes:
  a1_rigguides  rig guides (run2) + the arm-length sentence in run2/prompt.txt; otherwise identical to Union take 1
  a2_endlock    a1 + the approved opening image also locked at frame 40 + a finger-separation sentence
                in place of "Clean connected fingers"
  c1_acting     a2 on the run-3 acting guides (whole-body lean, lift, head tilt, counter-swings, hair
                wave, blink; smoothed arm) + an acting sentence in place of the "small coordinated" one
  d2_occlude    a2 on run-4s guides: the smoothed arm drawn in front (lines under it removed), body still
  d1_act_occl   c1 on run-4 guides: acting + the arm drawn in front + a one-frame blink (c1 shut the eyes 26-36)
  e1_outward    run-5 guides and a 40 px right-shifted opening image: the hand goes out and up at her side,
                waves twice at the top and returns the same way, never crossing the face (the smear zone)
  f1_sidewave   run-6 guides on the same shifted opening: the hand rises out at her side to a top pose beside her
                head, always outside her hair, face and body (the smear zone in e1 too); eyes open in every frame
                (c1, d1 and e1 shut her eyes for 9 to 27 frames when asked for a blink)
  g1_slowwave   f1 on run-7 guides: the same path with a third less peak hand speed (rise 3-15, lower 23-35,
                constant-speed profile) and one wave at the top instead of two (f1 still smeared its fastest frames)
Writes jobs/<job_id>.json (graph, input hashes, output labels) and stages the runtime inputs under
staging/input/rig_pilot/ for the connected-folder copy. Numbers and graphs only.

    python -I scripts/make_jobs.py a1_rigguides a2_endlock [--device-copies <staged ltx25/input>]

The connected-folder copy adds a C2PA content-credentials chunk to PNGs (same pixels, different bytes). With --device-copies the
job's sha256 is the byte hash of the copy actually on the PC (fetched back), after checking that its
pixels equal the source; the source byte hash is kept beside it.
"""
import argparse, hashlib, json, shutil, sys
import numpy as np
from PIL import Image
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
    'd2_occlude': {'guide_set': 'run4s', 'end_lock': True, 'fingers': True, 'seed': 20261004,
                   'note': 'a2 with the smoothed arm drawn in front of hair, face and body lines (occlusion-aware guides), body still'},
    'd1_act_occl': {'guide_set': 'run4', 'end_lock': True, 'fingers': True, 'acting': True, 'quick_blink': True, 'seed': 20261004,
                    'note': 'c1 with the waving arm drawn in front (occlusion-aware acting guides) and a one-frame blink'},
    'e1_outward': {'guide_set': 'run5', 'identity': 'identity_shift40.png', 'shift': 40, 'end_lock': True, 'fingers': True,
                   'acting': True, 'quick_blink': True, 'blink_frame': 36, 'seed': 20261004,
                   'motion': ('One gentle wave: rest at frames0-3, raise her left hand out to her side and up beside her head by '
                              'frame15, wave it gently side to side twice at frames15-24, lower it back down the same way at her '
                              'side by frame35, rest at35-40.'),
                   'note': 'run-5 guides: hand rises and returns outward at her side, waves at the top, never crosses the face; '
                           'figure shifted 40 px right so the arm stays inside the canvas; acting, occlusion, one-frame blink'},
    'f1_sidewave': {'guide_set': 'run6', 'identity': 'identity_shift40.png', 'shift': 40, 'end_lock': True, 'fingers': True,
                    'acting': True, 'eyes_open': True, 'seed': 20261004,
                    'motion': ('One gentle wave: rest at frames0-3, lift her left hand out at her side and up beside her head by '
                               'frame13, the open hand always out beside her hair, never in front of her hair, face or body; wave it '
                               'gently side to side twice at frames13-25, lower it back down the same way at her side by frame35, '
                               'rest at35-40.'),
                    'note': 'run-6 guides: side wave, the hand stays outside the hair, face and body in every frame; eyes open '
                            'throughout (no blink request); acting, occlusion, end lock'},
    'g1_slowwave': {'guide_set': 'run7', 'identity': 'identity_shift40.png', 'shift': 40, 'end_lock': True, 'fingers': True,
                    'acting': True, 'eyes_open': True, 'seed': 20261004,
                    'motion': ('One slow gentle wave: rest at frames0-3, lift her left hand smoothly out at her side and up beside '
                               'her head by frame15, the open hand always out beside her hair, never in front of her hair, face or '
                               'body; wave it once gently side to side at frames15-23, lower it smoothly back down the same way at '
                               'her side by frame35, rest at35-40.'),
                    'note': 'f1 on run-7 guides: same path, peak fingertip speed 15 instead of 20 cell px/frame, one wave at the top'},
    'c1_acting': {'guide_set': 'run3', 'end_lock': True, 'fingers': True, 'acting': True, 'seed': 20261004,
                  'note': 'a2 on the run-3 acting guides (whole body moves with the wave, hair flow, blink) + acting sentence'},
}


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


ACTING = ('Her whole body moves with the wave as one piece: she lifts slightly and leans away from the raised arm, tilts '
          'her head toward her hand, her free arm and tail sway in counter-motion, her rainbow hair flows gently in the water, '
          'and she blinks once as she settles, eyes closed at frames34-35.')
ACTING_QUICK = ACTING.replace('and she blinks once as she settles, eyes closed at frames34-35.',
                              'and she blinks once, quickly, as she settles: her eyes are shut only at frame34 and open in every '
                              'other frame.')


def prompt_for(r):
    base = (UNION / 'prompt.txt').read_text().strip()
    if r.get('acting'):
        old = 'The complete figure responds with small coordinated shoulder, torso, clothing, hair and tail movement.'
        assert old in base
        acting = ACTING_QUICK if r.get('quick_blink') else ACTING
        if r.get('eyes_open'):
            acting = ACTING.replace('and she blinks once as she settles, eyes closed at frames34-35.',
                                    'and her eyes stay open, looking at the viewer, in every frame.')
            assert acting != ACTING
        if r.get('blink_frame'):
            acting = acting.replace('frame34', f"frame{r['blink_frame']}")
        base = base.replace(old, acting)
        old = 'fixed waist at(216.5,485) in the640x896 canvas.'
        assert old in base
        base = base.replace(old, f"the waist stays within a few pixels of ({216.5 + r.get('shift', 0)},485) in the640x896 canvas.")
    if r.get('motion'):
        old = ('One gentle connected wave: rest at frames0-3, raise her left hand near face at7, above head at17, lower through face '
               'height at22 and chest at27, settle to the same rest at36-40.')
        assert old in base
        base = base.replace(old, r['motion'])
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
    n(12, 'LoadImage', image='rig_pilot/' + r.get('identity', 'identity_first_frame.png'))

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


def same_pixels(a, b):
    A, B = Image.open(a), Image.open(b)
    return A.size == B.size and np.array_equal(np.array(A.convert('RGBA')), np.array(B.convert('RGBA')))


def stage_inputs(guide_set, device=None, identity='identity_first_frame.png'):
    src = UNION / identity if identity == 'identity_first_frame.png' else PILOT / guide_set / identity
    pairs = [(src, 'rig_pilot/' + identity)]
    for lane in ('half', 'quarter'):
        pairs += [(PILOT / guide_set / f'guide_{lane}/{i:04d}.png', f'rig_pilot/{guide_set}/guide_{lane}/{i:04d}.png') for i in range(41)]
    rows = []
    for src, rel in pairs:
        dst = STAGE / 'input' / rel; dst.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(src, dst)
        row = {'path': rel, 'sha256': sha(src), 'source': str(src.relative_to(PILOT.parents[2])).replace('\\', '/')}
        if device:
            copy = Path(device) / rel
            assert same_pixels(src, copy), f'PC copy differs in pixels: {rel}'
            row.update(sha256=sha(copy), source_sha256=sha(src), pixel_identical_to_source=True)
        rows.append(row)
    return rows


def main(ids, device=None):
    (PILOT / 'jobs').mkdir(exist_ok=True)
    for jid in ids:
        r = RECIPES[jid]
        job = {'job_id': jid, 'note': r['note'], 'recipe': r, 'prompt': prompt_for(r), 'timeout_s': 1800,
               'inputs': stage_inputs(r['guide_set'], device, r.get('identity', 'identity_first_frame.png')), 'graph': graph(jid, r),
               'outputs': {'42': 'stage1_frames', '52': 'refined_frames', '20': 'stage1_latent', '31': 'refined_latent'},
               'controlled_baseline': 'assets_src/cinematics/ltx25_union_trial_20261004/take_1 (workflow c027567040d2588c)',
               'used_as_delivery_pixels': False}
        p = PILOT / 'jobs' / f'{jid}.json'
        p.write_text(json.dumps(job, indent=2) + '\n')
        print(jid, sha(p), len(job['graph']), 'nodes')


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('ids', nargs='*'); ap.add_argument('--device-copies')
    v = ap.parse_args(); main(v.ids or list(RECIPES), v.device_copies)
