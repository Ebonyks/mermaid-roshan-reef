"""Export-only fast transient limiting; preserve all five native takes/rejects."""
from pathlib import Path
import hashlib
import json
import math
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from tools import audit_audio_quality as aq

HERE = Path(__file__).resolve().parent
SOURCE = HERE / 'generated_delivery'
data = json.loads((SOURCE / 'generation_manifest.json').read_text(encoding='utf-8'))
row = data['attempts'][-1]
assert row['key'] == 'guide_puff_healthy'
command = list(row['review']['encoding_command'])
gain = -16.4 - float(row['initial_encode']['measurement']['input_i'])
command[command.index('-af') + 1] = (
    command[command.index('-af') + 1].rsplit(',volume=', 1)[0]
    + f',volume={gain:.6f}dB'
    + ',alimiter=limit=0.70:attack=1:release=10:level=false:latency=true')
output = HERE / 'guide_puff_healthy_limited01.ogg'
command[-1] = str(output)
subprocess.run(command, check=True, capture_output=True)
meta = aq.probe(output)
signal = aq.decoded_signal(output)
integrated, lra, peak = aq.loudness(output)
passed = (meta.get('decode_ok') and signal.get('decode_ok')
          and meta.get('codec') == 'vorbis' and meta.get('sample_rate_hz') == 48000
          and meta.get('channels') == 1 and float(meta.get('bitrate_kbps', 0)) >= 64
          and integrated is not None and math.isfinite(integrated)
          and abs(integrated + 16) <= 1
          and peak is not None and math.isfinite(peak) and peak <= -1.5
          and signal.get('decoded_clipped_samples') == 0
          and abs(float(signal.get('dc_offset', 1))) < 0.001)
receipt = {'status': 'PASS' if passed else 'FAIL', 'synthesis_calls': 0,
           'native_take_unchanged': True, 'command': command,
           'output': output.relative_to(ROOT).as_posix(),
           'sha256': hashlib.sha256(output.read_bytes()).hexdigest(),
           'meta': meta, 'signal': signal, 'integrated_lufs': integrated,
           'true_peak_dbtp': peak, 'lra': lra}
(HERE / 'healthy_master_receipt.json').write_text(
    json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
print(json.dumps(receipt))
raise SystemExit(0 if passed else 1)
