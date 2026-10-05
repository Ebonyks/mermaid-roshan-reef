"""Bind exact source-study payload, declared ancestry, licenses and audit coverage."""
import hashlib
import json
import struct
from pathlib import Path
from PIL import Image

PACKET = Path(__file__).resolve().parents[1]
ROOT = PACKET.parents[2]
PREFIX = PACKET.relative_to(ROOT).as_posix()
OLD = 'assets_src/cinematics/ltx25_8gb_wave_20261004'
V2 = 'assets_src/cinematics/ltx25_scale_filter_v2_20261004'
BASELINE = '09f05e529ccaae606eab89d0a9029b968f2137d1'

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def local(name):
    return PREFIX + '/' + name

guides = json.loads((PACKET / 'sources.json').read_text())['source_guides']
controls = [local(f'{scale}/{i:04d}.png') for scale in ('guide_half', 'guide_quarter') for i in range(41)]
full_guides = [local(f'guide_full/{i:04d}.png') for i in range(41)]
prior = [V2 + f'/frames/{i:04d}.png' for i in range(41)]
payload = []
licenses = []
for path in sorted(PACKET.rglob('*')):
    if not path.is_file() or '__pycache__' in path.parts or path.name in {
        'manifest.json', 'remote_verification.json', 'receipt_publication.json'
    }:
        continue
    relative = path.relative_to(PACKET).as_posix()
    parents = []
    role = 'recipe_or_measured_evidence'
    modification = 'Source-only recipe or measured evidence; no runtime or artwork acceptance.'
    if path.parent.name in {'guide_full', 'guide_half', 'guide_quarter'}:
        parents = [local('scripts/guide.lua'), local('guide_plan.json')]
        role = 'structural_control_only'
        modification = 'Aseprite authored complete-figure schematic outline at declared actual grid; motion-only, no appearance authority or delivery pixels.'
    elif path.name in {'sources.json', 'guide_plan.json'}:
        parents = guides
    elif path.name == 'identity_first_frame.png':
        parents = [guides[0], local('scripts/guide.lua')]
        role = 'appearance_reference'
        modification = 'Existing complete opening guide padded32px on whole canvas in Aseprite; no rescale or protected-original edit.'
    elif path.name == 'structural_guide.aseprite':
        parents = full_guides + [local('guide_plan.json'), local('scripts/annotate_guide.lua')]
        role = 'editable_control_master'
        modification = '41 complete authored control frames, 328 landmark slices and41 tags; motion-only guide, not accepted artwork.'
    elif relative.startswith(('take_1/', 'take_2/')):
        take = relative.split('/')[0]
        native = [local(f'{take}/refined_frames/{i:04d}.png') for i in range(41)]
        if path.parent.name in {'stage1_frames', 'refined_frames'}:
            parents = [local(f'{take}/receipt.json'), local(f'{take}/workflow.api.json')]
            role = 'native_complete_generated_frame'
            modification = 'Complete native Union-controlled LTX-2.5 frame; no post-registration, hand replacement, sharpening or frame selection. Rejected/reference only.'
        elif path.name == 'receipt.json':
            parents = controls + [local('identity_first_frame.png'), local('adapter_download.json'), local('prompt.txt'), local('scripts/render.py'), local('scripts/union_nodes.py'), OLD + '/manifest.json']
            role = 'actual_job_and_input_provenance'
        elif path.name in {'native_review.aseprite', 'native_review.mp4'}:
            parents = native + [local('scripts/review.lua')]
            role = 'editable_review_master' if path.suffix == '.aseprite' else 'encoded_review'
            modification = 'Complete41-frame native sequence at24fps; lossless Aseprite master or H264 CRF15 yuv420p viewing copy; rejected/reference only.'
        elif path.name == 'comparison.mp4':
            parents = prior + full_guides + native + [local('scripts/review.lua')]
            role = 'same_timeline_comparison'
            modification = 'Aseprite1:1 prior-v2/authored-guide/native-Union columns at identical41 timeline indices; prior padded8px left/32px top, no crop/scale/time repair; H264 viewing copy.'
        elif path.name == 'verification.json':
            parents = native + [local(f'{take}/native_review.aseprite'), local(f'{take}/receipt.json'), local('scripts/finish.py')]
        elif path.suffix == '.latent':
            parents = [local(f'{take}/receipt.json'), local(f'{take}/workflow.api.json')]
            role = 'native_stage_video_latent'
    elif path.name == 'native_diagnostics.json':
        parents = [local(f'{take}/refined_frames/{i:04d}.png') for take in ('take_1', 'take_2') for i in range(41)] + [local('scripts/measure.py')]
        role = 'read_only_numeric_diagnostics'
    elif path.name == 'runtime_input_binding.json':
        parents = controls + [local('identity_first_frame.png')]
    elif path.name == 'guide_roundtrip.json':
        parents = full_guides + [local('structural_guide.aseprite')]
    row = {
        'path': relative, 'bytes': path.stat().st_size, 'sha256': sha(path),
        'role': role, 'modification_status': modification, 'source_paths': parents,
        'source_sha256': {name: sha(ROOT / name) for name in parents},
        'license_provenance': 'Project-owned Roshan source-study derivatives and authored guides; inherited source attribution and LTX-2.x community model output terms for generated footage; no model weights redistributed.'
    }
    if path.suffix == '.png':
        with Image.open(path) as image:
            row.update(dimensions=list(image.size), mode=image.mode)
    elif path.suffix == '.aseprite':
        header = path.read_bytes()[:14]
        row.update(dimensions=list(struct.unpack_from('<HH', header, 8)), frames=struct.unpack_from('<H', header, 6)[0])
    elif path.suffix == '.mp4':
        row.update(dimensions=[1920 if path.name == 'comparison.mp4' else 640, 896], frames=41, fps='24/1')
    if path.suffix in {'.png', '.mp4', '.aseprite', '.latent'}:
        licenses.append('| `' + local(relative) + '` | ' + row['license_provenance'] + ' | https://github.com/Ebonyks/mermaid-roshan-reef/tree/c51075fff13cfd8f4795b5ef7da232fc7462e7f4/' + OLD + ' | ' + modification + ' |')
    payload.append(row)

manifest = {
    'schema': 'source-study-payload-v1', 'status': 'REJECTED_REFERENCE_ONLY',
    'baseline': BASELINE, 'payload': payload,
    'payload_sha256': hashlib.sha256('\n'.join(row['path'] + ' ' + row['sha256'] for row in payload).encode()).hexdigest(),
    'new_transformer_jobs': 2, 'new_imagegen_calls': 0, 'paid_api_calls': 0,
    'model_weights_redistributed': False, 'accepted': False,
    'previous_source_manifest': OLD + '/manifest.json',
    'prior_registration_manifest': V2 + '/manifest.json',
    'union_adapter_execution': 'PASS_ON_8GB_BOTH_TAKES',
    'refine_details_execution': 'NOT_RUN',
    'archive_complete_requires': 'Actual anonymous remote receipt at exact published revision; not inferred from this manifest'
}
(PACKET / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
marker = '\n## LTX-2.5 Union structural-control trial — 2026-10-04\n'
license_path = ROOT / 'ASSET_LICENSES.md'
text = license_path.read_text(encoding='utf-8')
if marker in text:
    start = text.index(marker)
    end = text.find('\n## ', start + len(marker))
    text = text[:start] + (text[end:] if end >= 0 else '')
text += marker + '\n| Asset | Source/license | Source URL | Modifications |\n|---|---|---|---|\n' + '\n'.join(licenses) + '\n'
license_path.write_text(text, encoding='utf-8', newline='')
impact_path = ROOT / 'design/audit_impacts/ltx25-union-trial-20261004.json'
impact = json.loads(impact_path.read_text())
docs = ['ASSET_LICENSES.md', 'audit/MASTER_AUDIT_2026-08-09.md', 'audit/animation/README.md',
        'design/05_DOC_LEDGER.md', 'design/animation/ANIMATION_PRODUCTION_PROTOCOL.md',
        'design/reference/owner_decisions.json', 'design/reference/OWNER_DECISIONS.md']
impact['files'] = sorted(set(docs + [path.relative_to(ROOT).as_posix() for path in PACKET.rglob('*') if path.is_file() and '__pycache__' not in path.parts]))
impact_path.write_text(json.dumps(impact, indent=2) + '\n', encoding='utf-8')
assert all(row['bytes'] < 104857600 for row in payload), 'GitHub per-file limit'
print('PAYLOAD', len(payload), 'LICENSE_ROWS', len(licenses), 'BYTES', sum(row['bytes'] for row in payload), 'MAX_FILE', max(row['bytes'] for row in payload))
