from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,re,sys
from PIL import Image
D=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((D/'manifest.json').read_text(encoding='utf-8'));errors=[]
assert len(m['steps'])==16
for s in m['steps']:
 for k in ['child_sees','gesture','configured_instruction','embodied_action_and_contact','before_action_after','next','panel','public_baseline_refs']:assert s[k]
 if 'native' in s:assert sha(D/s['native'])==s['native_sha256'] and Image.open(D/s['native']).size==(1280,720)
 else:assert 'COVERAGE_GAP' in s['evidence_status']
for x in m['media']:
 p=D/x['path'];assert p.is_file()
 if x['role'] in ['unmodified_native_capture','existing_asset_reference_not_gameplay','lossless_native_action_sequence']:assert sha(p)==x['source_sha256']
h=(D/'index.html').read_text(encoding='utf-8')
for target in re.findall(r'(?:href|src|data-native|data-panel)="([^"]+)"',h):
 if target.startswith('#'):assert 'id="'+target[1:]+'"' in h
 elif not target.startswith(('http:','https:','data:')):assert (D/target).is_file()
assert 'href="source/' not in h
receipt=json.loads((D/'SOURCE_CAPTURE_RECEIPT.json').read_text(encoding='utf-8'));seq=Image.open(D/'native/wash_full_action.webp');assert seq.n_frames==248
for k,row in enumerate(receipt['runs']):
 seq.seek(k);assert hashlib.sha256(seq.convert('RGB').tobytes()).hexdigest()==row['rgb_sha256']
v=json.loads((D/'VERIFICATION.json').read_text(encoding='utf-8'))
for row in v['files']:assert sha(D/row['path'])==row['sha256']
print('PUBLIC_WALKTHROUGH|PASS|16steps|8native_views|248canvases|'+str(len(v['files']))+'sealed_files')
