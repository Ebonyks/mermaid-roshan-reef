"""Install only five new Guide files after independent strict artifact checks."""
from pathlib import Path
import hashlib
import json
import math
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from tools import audit_audio_quality as aq

HERE = Path(__file__).resolve().parent
SOURCE = HERE / 'generated_delivery'
producer = json.loads((SOURCE / 'generation_manifest.json').read_text(encoding='utf-8'))
repair = json.loads((HERE / 'healthy_master_receipt.json').read_text(encoding='utf-8'))
assert repair['status'] == 'PASS' and repair['synthesis_calls'] == 0
assert producer['synthesis_calls'] + producer['previous_run']['synthesis_calls'] == 5
protected = subprocess.check_output([
    'git','diff','--name-only','1a4e8a1ceae29b401d63900a57a531b2f4442ba8','--',
    'assets/book','assets/audio/voices','assets/characters/friends'],cwd=ROOT,text=True)
if protected.strip():
    raise RuntimeError('Protected original changes must be resolved before installation')
manifest_path = ROOT / aq.OBJECTIVE_GUIDE_MANIFEST_REL
runtime_manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
old_entries = list(runtime_manifest['entries'])
old_keys = {entry['key'] for entry in old_entries}
assert len(old_keys) == 2 and runtime_manifest['synthesis_calls'] == 2
new_entries = []
receipts = []
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
for row in producer['attempts']:
    key = row['key']
    if key not in aq.OBJECTIVE_GUIDE_TEXT or not key.startswith('guide_puff_'):
        raise RuntimeError('Unexpected care cue: ' + key)
    if row['text'] != aq.OBJECTIVE_GUIDE_TEXT[key]:
        raise RuntimeError('Care transcript mismatch')
    native = SOURCE / row['native']['path']
    if sha(native) != row['native']['sha256']:
        raise RuntimeError('Native take hash mismatch')
    source = ROOT / repair['output'] if key == 'guide_puff_healthy' else SOURCE / row['review']['path']
    expected_hash = repair['sha256'] if key == 'guide_puff_healthy' else row['review']['sha256']
    if sha(source) != expected_hash:
        raise RuntimeError('Review source hash mismatch')
    meta, signal = aq.probe(source), aq.decoded_signal(source)
    integrated,lra,peak = aq.loudness(source)
    passed = (meta.get('decode_ok') and signal.get('decode_ok')
              and meta.get('codec') == 'vorbis' and meta.get('sample_rate_hz') == 48000
              and meta.get('channels') == 1 and float(meta.get('bitrate_kbps',0)) >= 64
              and integrated is not None and math.isfinite(integrated)
              and abs(integrated+16) <= 1 and peak is not None and math.isfinite(peak)
              and peak <= -1.5 and signal.get('decoded_clipped_samples') == 0
              and abs(float(signal.get('dc_offset',1))) < 0.001)
    if not passed:
        raise RuntimeError('Strict artifact verification failed: ' + key)
    output = ROOT / aq.OBJECTIVE_GUIDE_ROOT_REL / (key+'.ogg')
    if output.exists():
        raise RuntimeError('No-overwrite guard: ' + str(output))
    verification = {**meta,'integrated_lufs':integrated,'true_peak_dbtp':peak,
                    'decoded_sample_peak':signal['decoded_peak_linear'],
                    'decoded_clipped_samples':signal['decoded_clipped_samples'],
                    'decoded_dc_mean':signal['dc_offset']}
    new_entries.append({'key':key,'speaker':'guide','text':row['text'],
        'native_source_path':native.relative_to(ROOT).as_posix(),
        'native_source_sha256':sha(native),
        'source_review_path':source.relative_to(ROOT).as_posix(),
        'output_path':output.relative_to(ROOT).as_posix(),'output_sha256':sha(source),
        'trigger':'Grand Puff cold introduction, intentional cleaning opening, earned relief or completion',
        'visual_pointer':'Sympathetic whole-character acting, forehead star and soap-bubble cleaning contact',
        'historical_family_recording_gap':'New owner-directed cold/care narration; old bonk, enraged and burst takes remain untouched and are not substituted',
        'historical_family_gap_preserved':True,'verification':verification,
        'human_listening':'NOT_MEASURED','device':'NOT_MEASURED','child':'NOT_MEASURED','owner':'NOT_MEASURED'})
    receipts.append({'key':key,'source':str(source.relative_to(ROOT)),
                     'output':str(output.relative_to(ROOT)),'sha256':sha(source),'status':'PASS'})
assert len(new_entries) == 5 and len({row['key'] for row in new_entries}) == 5
for entry in new_entries:
    shutil.copyfile(ROOT/entry['source_review_path'],ROOT/entry['output_path'])
    assert sha(ROOT/entry['output_path']) == entry['output_sha256']
runtime_manifest['entries'] = old_entries + new_entries
runtime_manifest['synthesis_calls'] = 7
runtime_manifest['additional_source_bundles'] = [{
    'owner_scope_date':'2026-10-17','scope':'Grand Puff cold/care rework; neutral adult Guide, no family imitation',
    'generation_manifest_path':(SOURCE/'generation_manifest.json').relative_to(ROOT).as_posix(),
    'generation_manifest_sha256':sha(SOURCE/'generation_manifest.json'),
    'generation_status':'FAILED final-cue export retained; four entries passed. Export-only repair completes fifth.',
    'repair_receipt_path':(HERE/'healthy_master_receipt.json').relative_to(ROOT).as_posix(),
    'repair_receipt_sha256':sha(HERE/'healthy_master_receipt.json'),
    'synthesis_calls':5,'reencode_synthesis_calls':0,'protected_original_changes':0}]
manifest_path.write_text(json.dumps(runtime_manifest,indent=2)+'\n',encoding='utf-8')
result = aq.validate_objective_guides(ROOT)
receipt = {'status':'PASS' if not result['blocking'] else 'FAIL','artifacts':receipts,
    'guide_validation':result,'new_synthesis_calls':5,'paid_api_calls':0,
    'old_entries_preserved':runtime_manifest['entries'][:2] == old_entries,
    'protected_original_diff':protected,'external_acceptance':'OPEN_DEVICE_LISTENING_CHILD_OWNER'}
(HERE/'INSTALL_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
print(json.dumps(receipt))
raise SystemExit(1 if result['blocking'] else 0)
