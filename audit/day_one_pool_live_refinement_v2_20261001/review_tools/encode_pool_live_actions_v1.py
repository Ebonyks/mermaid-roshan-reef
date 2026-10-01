from pathlib import Path
import datetime, hashlib, json, statistics, subprocess

root = Path(__file__).resolve().parents[1]
folder = root / 'audit/day_one_pool_live_refinement_v2_20261001/native_actions_1280_v1'
assert json.loads((folder / 'PROCESS_RECEIPT.json').read_text(encoding='utf-8'))['exit_code'] == 0
receipt_path = folder / 'ACTION_RECEIPT.json'
receipt = json.loads(receipt_path.read_text(encoding='utf-8'))
assert receipt['checks_failed'] == 0 and len(receipt['actions']) == 6
output = folder / 'ENCODING_RECEIPT.json'
assert not output.exists(), 'Preserve earlier encoding evidence.'
ffmpeg = Path('C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/FFmpeg/8.1.2/bin/ffmpeg.exe')
ffprobe = ffmpeg.with_name('ffprobe.exe')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
rows = []
for action in receipt['actions']:
    item = action['requested_item']
    frames = receipt['frames'][action['start_frame']:action['end_frame_exclusive']]
    lines = ['ffconcat version 1.0']
    for i, frame in enumerate(frames):
        assert sha(folder / frame['path']) == frame['sha256']
        duration_ms = (frames[i + 1]['elapsed_wall_ms'] - frame['elapsed_wall_ms']) if i + 1 < len(frames) else 33
        assert duration_ms > 0
        lines += [f"file '{frame['path']}'", 'option framerate 1000', f'duration {duration_ms / 1000:.3f}']
    concat = folder / f'item_{item:02d}.ffconcat'
    concat.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    video = folder / f'item_{item:02d}_native_timestamps.mp4'
    assert not video.exists()
    command = [str(ffmpeg), '-hide_banner', '-nostdin', '-f', 'concat', '-safe', '0', '-i', str(concat),
               '-fps_mode', 'vfr', '-frames:v', str(len(frames)), '-c:v', 'libx264', '-preset', 'medium',
               '-crf', '16', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', str(video)]
    with (folder / f'item_{item:02d}_encoding.log').open('w', encoding='utf-8') as log:
        result = subprocess.run(command, cwd=folder, stdout=log, stderr=subprocess.STDOUT, check=False)
    assert result.returncode == 0
    probe = json.loads(subprocess.check_output([str(ffprobe), '-v', 'error', '-count_frames', '-select_streams', 'v:0',
        '-show_entries', 'stream=width,height,nb_read_frames,nb_frames,time_base,duration', '-show_entries', 'frame=best_effort_timestamp_time',
        '-of', 'json', str(video)], text=True))
    stream = probe['streams'][0]
    assert int(stream['nb_read_frames']) == len(frames)
    timestamps = [float(f['best_effort_timestamp_time']) for f in probe['frames']]
    expected = [(f['elapsed_wall_ms'] - frames[0]['elapsed_wall_ms']) / 1000 for f in frames]
    errors = [abs(a - b) for a, b in zip(timestamps, expected)]
    assert len(timestamps) == len(expected) and max(errors) < 0.0011, max(errors)
    intervals = [frames[i]['elapsed_wall_ms'] - frames[i-1]['elapsed_wall_ms'] for i in range(1, len(frames))]
    rows.append({'requested_item': item, 'video': video.name, 'sha256': sha(video), 'source_frame_count': len(frames),
        'concat': concat.name, 'concat_sha256': sha(concat), 'command': command, 'process_exit': result.returncode,
        'stream': stream, 'max_timestamp_error_seconds': max(errors),
        'source_intervals_ms': {'minimum': min(intervals), 'median': statistics.median(intervals), 'maximum': max(intervals)}})
    print(f'POOL_ACTION_VIDEO|item{item}|{len(frames)} native frames|timestamp error {max(errors):.6f}s|PASS', flush=True)
output.write_text(json.dumps({'schema': 'reef.native-action-encoding.v1',
    'checked_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'native_receipt_sha256': sha(receipt_path),
    'ffmpeg': str(ffmpeg), 'ffmpeg_binary_sha256': sha(ffmpeg), 'items': rows,
    'qualification': 'Six compressed silent review videos, one per actual native capture span, with recorded variable timestamps. Every encoded frame corresponds to one retained lossless capture; no output frame repeats, interpolation, retiming, subject repair or game/cinematic delivery claim. Real readback cadence includes gaps; video verification is not an action-quality/device/owner pass.'}, indent=2) + '\n', encoding='utf-8')
