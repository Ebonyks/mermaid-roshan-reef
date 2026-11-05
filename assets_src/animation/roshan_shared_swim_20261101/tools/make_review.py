"""Create labelled QA composites and lossless archives of native RGBA captures.

Pillow only makes review layouts/background instrumentation; it never repairs,
redraws, resamples or changes a source character or exported costume texture.
"""
from __future__ import annotations
import concurrent.futures
import hashlib
import json
import math
from pathlib import Path
import subprocess

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
FFMPEG = Path('C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/FFmpeg/8.1.2/bin/ffmpeg.exe')
JOBS = ['ballet', 'magician', 'live_swaps']
W, H = 1280, 720
FONT = 'C:/Windows/Fonts/segoeui.ttf'


def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def native_path(sample):
    path = ROOT/sample['frame'].removeprefix('res://')
    assert hashlib.sha256(path.read_bytes()).hexdigest() == sample['png_sha256']
    return path


def run(args):
    result = subprocess.run([str(FFMPEG), '-hide_banner', '-loglevel', 'error', '-y', *map(str, args)],
                            capture_output=True, check=False)
    if result.returncode:
        raise RuntimeError(result.stderr.decode('utf-8', errors='replace'))


def review_frame(sample, identity, camera_config):
    zoom=camera_config['camera_zoom']
    root = np.array(sample['root']);camera = root+np.array(camera_config['camera_offset'])
    frame = Image.new('RGBA', (W, H), (19, 39, 55, 255))
    draw = ImageDraw.Draw(frame)
    # Fixed world markers derive solely from recorded native root transforms.
    for x in range(math.floor((camera[0]-W/zoom)/160), math.ceil((camera[0]+W/zoom)/160)):
        sx = round((x*160-camera[0])*zoom+W/2)
        draw.line((sx, 0, sx, H), fill=(30, 57, 73, 255), width=1)
    for y in range(math.floor((camera[1]-H/zoom)/160), math.ceil((camera[1]+H/zoom)/160)):
        sy = round((y*160-camera[1])*zoom+H/2)
        draw.line((0, sy, W, sy), fill=(30, 57, 73, 255), width=1)
    character = Image.open(native_path(sample)).convert('RGBA')
    frame.alpha_composite(character)
    draw = ImageDraw.Draw(frame)
    draw.text((22, 14), 'One native actor | '+sample['skin'].capitalize()+' garment skin', font=ImageFont.truetype(FONT, 27), fill='#F3EFD7')
    draw.text((22, 54), f"Frame {sample['index']:03}/228   Phase {sample['phase']:.3f}s   Actor {sample['actor_id']}", font=ImageFont.truetype(FONT, 19), fill='#C2DBE9')
    speed = float(np.linalg.norm(sample['velocity']));distance = float(np.linalg.norm(root))
    draw.text((22, 84), f'Tail-driven travel {distance:.1f}px   Speed {speed:.1f}px/s   30fps capture', font=ImageFont.truetype(FONT, 18), fill='#9FC4D8')
    draw.text((22, 681), 'SOURCE PROTOTYPE | Character: native Godot RGBA. Grid: recorded world-space markers. Device/owner review pending.', font=ImageFont.truetype(FONT, 17), fill='#C2DBE9')
    return frame


def read_exact(pipe, count):
    chunks = []
    while count:
        chunk = pipe.read(count)
        if not chunk:
            raise RuntimeError('Truncated lossless native decode')
        chunks.append(chunk);count -= len(chunk)
    return b''.join(chunks)


def roundtrip(archive, samples):
    common = [str(FFMPEG), '-hide_banner', '-loglevel', 'error', '-threads', '2', '-i', str(archive)]
    rgb = subprocess.Popen(common+['-map', '0:v:0', '-pix_fmt', 'rgb24', '-f', 'rawvideo', 'pipe:1'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    alpha = subprocess.Popen(common+['-map', '0:v:1', '-pix_fmt', 'gray', '-f', 'rawvideo', 'pipe:1'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    proofs = []
    try:
        for sample in samples:
            original = np.asarray(Image.open(native_path(sample)).convert('RGBA'))
            color = np.frombuffer(read_exact(rgb.stdout, W*H*3), np.uint8).reshape(H, W, 3)
            matte = np.frombuffer(read_exact(alpha.stdout, W*H), np.uint8).reshape(H, W)
            assert np.array_equal(color, original[:, :, :3]), ('RGB mismatch', sample['index'])
            assert np.array_equal(matte, original[:, :, 3]), ('Alpha mismatch', sample['index'])
            proofs.append({'index': sample['index'], 'native_png_sha256': sample['png_sha256'],
                           'rgba_pixels_sha256': hashlib.sha256(original.tobytes()).hexdigest()})
        assert not rgb.stdout.read(1) and not alpha.stdout.read(1), 'Unexpected extra archive frame'
        assert rgb.wait(timeout=120) == 0 and alpha.wait(timeout=120) == 0
    finally:
        for process in [rgb, alpha]:
            if process.poll() is None:
                process.terminate();process.wait(timeout=10)
    return proofs


def make_job(identity):
    camera_config = load(ROOT/'evidence'/(identity+'_samples.json'))
    samples = camera_config['samples']
    output = ROOT/'raw_review'/identity
    output.mkdir(parents=True, exist_ok=True)
    for sample in samples:
        review_frame(sample, identity, camera_config).convert('RGB').save(output/f"frame_{sample['index']:04}.png")
    native_pattern = str(native_path(samples[0])).replace('frame_0000.png', 'frame_%04d.png')
    review_pattern = str(output/'frame_%04d.png')
    review = ROOT/'review'/(identity+'.mp4')
    run(['-framerate', 30, '-i', review_pattern, '-frames:v', len(samples), '-c:v', 'libx264', '-threads', 2,
         '-preset', 'medium', '-crf', 17, '-pix_fmt', 'yuv420p', '-movflags', '+faststart', review])
    archive = ROOT/'masters'/(identity+'_native_rgba.mkv')
    run(['-framerate', 30, '-i', native_pattern, '-filter_complex', '[0:v]split[r][a];[r]format=rgb24[rgb];[a]alphaextract[alpha]',
         '-map', '[rgb]', '-map', '[alpha]', '-frames:v', len(samples), '-c:v:0', 'libx264rgb', '-threads:v:0', 2,
         '-preset', 'medium', '-crf', 0, '-pix_fmt:v:0', 'rgb24', '-c:v:1', 'ffv1', '-threads:v:1', 2,
         '-level:v:1', 3, '-pix_fmt:v:1', 'gray', '-metadata:s:v:0', 'title=Native RGB lossless',
         '-metadata:s:v:1', 'title=Native alpha lossless', archive])
    assert archive.stat().st_size < 99_000_000, 'Native archive exceeds the project GitHub single-file budget'
    proofs = roundtrip(archive, samples)
    print('REVIEW_ARCHIVED_RGBA_EXACT', identity, len(samples), round(archive.stat().st_size/1e6, 2), 'MB', flush=True)
    return {'job': identity, 'native_frames': len(samples), 'logical_action_seconds': 7.6,
            'encoded_duration_seconds': len(samples)/30, 'fps': 30, 'archive': archive.relative_to(ROOT).as_posix(),
            'archive_bytes': archive.stat().st_size, 'sha256': hashlib.sha256(archive.read_bytes()).hexdigest(),
            'native_rgba_exact_all_frames': True, 'frames': proofs, 'review': review.relative_to(ROOT).as_posix(),
            'review_sha256': hashlib.sha256(review.read_bytes()).hexdigest()}


def contact_sheet(samples, indices, path, columns=4, cell=(320, 210)):
    sheet = Image.new('RGB', (columns*cell[0], math.ceil(len(indices)/columns)*cell[1]), '#132737')
    draw = ImageDraw.Draw(sheet)
    for i, index in enumerate(indices):
        sample = samples[index]
        picture = Image.open(native_path(sample)).convert('RGBA')
        background = Image.new('RGBA', picture.size, '#203B4B');background.alpha_composite(picture)
        background.thumbnail((cell[0], cell[1]-30))
        x, y = i % columns*cell[0], i//columns*cell[1]
        sheet.paste(background.convert('RGB'), (x, y))
        draw.text((x+6, y+cell[1]-26), f"{sample['skin']} f{index:03} {sample['time']:.2f}s", font=ImageFont.truetype(FONT, 16), fill='#F3EFD7')
    sheet.save(path)


def fin_sheet(samples, camera_config):
    transitions = [i for i in range(1, len(samples)) if samples[i]['fin_state'] != samples[i-1]['fin_state']]
    sheet = Image.new('RGB', (5*240, len(transitions)*250), '#132737')
    draw = ImageDraw.Draw(sheet)
    for row, transition in enumerate(transitions):
        for column, index in enumerate(range(transition-2, transition+3)):
            sample = samples[index];x, y = sample['bones']['Fin'][4:]
            zoom=camera_config['camera_zoom'];offset=camera_config['camera_offset']
            sx, sy = (x-offset[0])*zoom+W/2, (y-offset[1])*zoom+H/2
            original = Image.open(native_path(sample)).convert('RGBA')
            crop = original.crop((round(sx-190), round(sy-120), round(sx+50), round(sy+100)))
            tile = Image.new('RGBA', crop.size, '#203B4B');tile.alpha_composite(crop)
            px, py = column*240, row*250
            sheet.paste(tile.convert('RGB'), (px, py))
            draw.text((px+5, py+223), f"f{index:03} {sample['fin_state']}", font=ImageFont.truetype(FONT, 16), fill='#F3EFD7')
    sheet.save(ROOT/'review/fin_transitions.png')
    return transitions


def main():
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(make_job, JOBS))
    ballet_config=load(ROOT/'evidence/ballet_samples.json')
    magician_config=load(ROOT/'evidence/magician_samples.json')
    ballet = ballet_config['samples']
    magician = magician_config['samples']
    swaps = load(ROOT/'evidence/live_swaps_samples.json')['samples']
    contact_sheet(ballet, [0, 15, 30, 48, 75, 96, 114, 138, 165, 183, 207, 228], ROOT/'review/ballet_action.png')
    contact_sheet(magician, [0, 15, 30, 48, 75, 96, 114, 138, 165, 183, 207, 228], ROOT/'review/magician_action.png')
    contact_sheet(swaps, [j for i in [37, 76, 113, 154, 187] for j in [i-1, i, i+1]], ROOT/'review/swap_boundaries.png', 3, (426, 270))
    comparison = Image.new('RGB', (2560, 720), '#132737')
    comparison.paste(review_frame(ballet[48], 'ballet',ballet_config).convert('RGB'), (0, 0))
    comparison.paste(review_frame(magician[48], 'magician',magician_config).convert('RGB'), (1280, 0))
    comparison.save(ROOT/'review/two_costumes.png')
    transitions = fin_sheet(ballet,ballet_config)
    version = subprocess.check_output([str(FFMPEG), '-version'], text=True, encoding='utf-8').splitlines()[0]
    record = {'pass': True, 'native_rgba_exact': True, 'ffmpeg': version, 'jobs': results,
              'fin_transition_frames': transitions, 'composite_scope': 'QA layouts only. Unmodified native character RGB/alpha preserved bit-exact in paired-track lossless archives. Grid derives from native root; labelled reviews are not runtime footage.',
              'human_accepted': False, 'device_accepted': False, 'owner_accepted': False, 'production_accepted': False}
    (ROOT/'evidence/media_roundtrip.json').write_text(json.dumps(record, indent=2)+'\n', encoding='utf-8', newline='\n')
    print('REVIEW_MEDIA_ALL_OK', flush=True)


if __name__ == '__main__':
    main()
