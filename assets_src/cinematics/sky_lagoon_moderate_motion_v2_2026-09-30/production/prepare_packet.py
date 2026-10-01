"""Describe and hash the reference archive; never modifies source artwork."""
import hashlib
import json
import struct
import subprocess
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parents[2]
REL = ROOT.relative_to(PROJECT).as_posix()
BRANCH = 'codex/sky-lagoon-moderate-animation-20261001'
BASELINE = 'b65c21fdddd79f272a6854f241faa1441abe6616'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, value):
    path.write_text(json.dumps(value, indent=2), encoding='utf-8')


def describe():
    task = json.loads((ROOT / 'TASK_START.json').read_text())
    samples = json.loads((ROOT / 'SAMPLES.json').read_text())
    lines = ['# Sky Lagoon moderate animation references — v2', '',
             'Owner-requested moderate-resolution examples of all ten previous studies, with a revised importer and a layered Sky Lagoon sample. `MOTION_REFERENCE_ONLY / CANDIDATE`; new visual selection remains open.', '',
             'Open [index.html](index.html) through a local web server for crisp PNG playback, pause, key scrubbing and native-pixel inspection. The running workstation preview is http://127.0.0.1:8191/. GitHub hosts the complete durable archive; local previews are staging only.', '',
             '## Deliverables', '',
             '| Sample | Raster keys | Editable master | PNG board |', '|---|---:|---|---|']
    for s in samples:
        ident = s['id']
        lines.append(f"| {s['title']} | {s['count']} × 512×512 | [{ident}.aseprite](objects/{ident}/{ident}.aseprite) | [All keys](objects/{ident}/spritesheet.png) |")
    lines += ['', 'The set contains 54 fresh generated pose drawings plus 12 authored stained-glass light states: 66 distinct saved raster states. Nine native sheets are 1024×1536, with six 512×512 cells each. Each object has transparent PNG states, a power-of-two atlas, JSON timing and source/authoring receipts. Native sheets and source originals are preserved separately.', '',
              'The [Sky Lagoon sample](scene/sky_lagoon_sample.mp4) is 1920×640, 48 frames at 12 fps (four seconds). Its [layered Aseprite master](scene/sky_lagoon_sample.aseprite) contains the approved v5 panorama, existing slide, current four-tower castle, fresh playground keys and garden/ambient studies. Fixed scenery uses linked cels. [Scene parameters](scene/SCENE_PARAMETERS.json) record every placement and the shared castle anchor.', '',
              '![Sky Lagoon context study](scene/sky_lagoon_sample.png)', '',
              '## What changed', '',
              '- Built-in `image_gen` generated larger new pose drawings from existing identity references. [PROMPT_SET.json](PROMPT_SET.json) contains the exact nine prompts and two padding-repair prompts. No CLI/API-key generation or ComfyUI video job supplied these new keys.',
              '- The Aseprite Lua importer removes disconnected alpha dust, rejects fringe noise, registers anchors and fits the union of poses inside a 512px canvas. It uses native nearest-neighbor raster sampling, not browser/GIF enlargement. The smoke keeps intentional soft alpha; other subject contours are made opaque at alpha ≥192.',
              '- The wide huckleberry uses uniform downsampling to keep every leaf inside the frame. One native edge tip gets a tiny Aseprite-painted closing cap in new padding, recorded in its receipt. This supplies no action pose.',
              '- The swing reuses the larger 1338×1176 approved frame source. Six new detached-seat pitch drawings show near/far cushion and underside changes under two fixed hooks. Ropes are painted between hook and seat sockets; no sideways rotation supplies the action. Contact/perspective polish remains open.',
              '- Seesaw beams/seats/handles have fresh tilted drawings. Axle registration and a small fixed bottom-support region replace the earlier whole-object rotation. Gate leaves open into transparent space while its façade stays fixed.',
              '- Stained glass reuses the 880×1216 owner-supplied artwork, isolates its arch and paints twelve restrained light states. It preserves portrait geometry. In the context sample the existing castle portrait itself gets light; a different portrait is not pasted over it.', '',
              '## Aseprite workflow', '',
              'Open an object `.aseprite` file. The visible layer contains cleaned animation keys; one hidden native-reference cel provides the untouched first input pose. Work at 100% or integer zoom. Add intermediate drawings and revise details on new layers; the native generated sheets remain provenance inputs. The gate master stores the six opening keys; the browser/scene play its recorded forward-and-return order.', '',
              'For the full environment, open `scene/sky_lagoon_sample.aseprite`. The fixed background and slide use linked cels; animated objects retain independent layers. The approved 6144×2048 panorama is uniformly downsampled for this reference sample. Runtime slicing/resolution/import acceptance is not granted by this sample.', '',
              'Rebuild cleaned samples with `python -s -B production/build.py --overwrite`; use `--id 07_swing` to rebuild one. Build/recheck the environment with `python -s -B production/finish.py`; `--verify-only` reopens exports without rebuilding scenery. Use Aseprite 1.3.18.4, Python 3.13, NumPy 2.5.1, Pillow 12.3.0, SciPy 1.18.0 and FFmpeg 8.1.2. Tool paths are explicit workstation defaults near the top of each Python file and can be adjusted for another workstation. Python only reads/analyzes raster data; Aseprite authors all raster edits and composition.', '',
              'Aseprite API references: [Sprite](https://www.aseprite.org/api/sprite/), [Image](https://www.aseprite.org/api/image/), [Layer](https://www.aseprite.org/api/layer/).', '',
              '## Context ownership and review limits', '',
              'The existing panorama is unchanged. Equipment uses current meadow anchors; the castle and bridge use `scripts/arena/sky_lagoon_layout.json`. Garden examples are study placements on open foreground grass. The generated door-leaf region is cropped into the existing castle aperture only for the motion comparison; this composition is not a runtime screenshot or cinematic delivery.', '',
              'The extra fir is delivered as a standalone study and excluded from the context composite because the current shared composition contract disables that tree to protect the scenic mountain path. The painted background fir stays intact. No Roshan character animation, gameplay, save, touch, performance or engine source is changed.', '',
              'These are larger pose studies, not finished smooth loops or a human hand-drawn pixel-art redraw. Six drawings per object still leave visible timing steps, AI detail/topology drift and manually authored contact limits. Owner selection, additional drawings, runtime integration, Mobile/device/child checks and cinematic gates remain open. No finding is closed.', '',
              '## Evidence and delivery', '',
              '[MACHINE_VERIFICATION.json](MACHINE_VERIFICATION.json) records exact native RGBA round trips for all ten masters, 66 distinct states, clear alpha margins and the layered scene first frame. [PROJECT_VERIFICATION.json](PROJECT_VERIFICATION.json) records authority/development/import/source checks. [REVIEW.json](REVIEW.json) distinguishes inspection from owner acceptance. [MANIFEST.json](MANIFEST.json) records each payload file, hash, dimensions, role, provenance and deterministic sorted payload SHA-256.', '',
              f'Authorized public destination: https://github.com/Ebonyks/mermaid-roshan-reef/tree/{BRANCH}/{REL}. The immutable revision and anonymous access/byte verification are recorded in `REMOTE_VERIFICATION.json` after publication. That operational receipt and the manifest itself are excluded from the payload to avoid circular hashes.', '',
              '`ARCHIVE_COMPLETE` requires published exact-revision byte verification. `GENERATION_READY` is false: this is a motion-study archive, not a role-bound video shot card. `DELIVERY_ACCEPTED` is false: none of these sprite/context studies satisfies full-frame cinematic regeneration evidence. Protected originals, prior rejected studies and owner approval states are preserved.', '']
    (ROOT / 'README.md').write_text('\n'.join(lines), encoding='utf-8')
    write(ROOT / 'REVIEW.json', {'status': 'CANDIDATE', 'reviewer': 'Codex visual inspection; not owner acceptance',
          'observations': ['All ten have larger isolated PNG/Aseprite samples.', 'Wide leaves now fit all keys with transparent margins; native padding repairs preserved.',
                           'Swing pitch changes cushion/underside surfaces under fixed hooks; exact rope/socket contacts still need production review.',
                           'Seesaw cleanup no longer clips the angled beam; bottom support fixed only below the action.',
                           'Gate aperture is transparent, with fixed exterior pixels.', 'Stained-glass portrait is preserved; outside checker/signature/sparkle excluded.',
                           'Context preserves panorama and castle/bridge anchors; extra fir stays standalone.'],
          'open_items': ['Six-key cycles need more drawings for smooth production loops.', 'AI rib/leaf/ornament and light continuity needs owner selection and further Aseprite cleanup.',
                         'Context door crop and rope contacts are reference approximations.', 'Runtime/device/child and cinematic acceptance not performed.'],
          'owner_acceptance': False, 'runtime_integration': False, 'findings_closed': []})
    write(ROOT / 'objects/10_glass/METHOD.json', {'method': 'SOURCE_REUSE_ASEPRITE_LIGHT_STATES',
          'source_path': 'assets_src/sky_lagoon/reductive_rebuild_2026-07-28/stained_glass_owner_reference.png',
          'source_sha256': sha(ROOT / 'objects/10_glass/window_identity_source.png'), 'source_dimensions': [880,1216],
          'modification': 'Aseprite isolates existing arch using read-only boundary analysis; uniform nearest-neighbor downsample and painted light band. No portrait redesign or generated identity.',
          'license': 'Owner-supplied project artwork; retain existing ASSET_LICENSES.md provenance, no third-party license inferred.'})
    task['result'] = {'objects': 10, 'raster_states': 66, 'editable_object_masters': 10, 'context_master': [1920, 640, 48], 'status': 'CANDIDATE_MOTION_REFERENCES'}
    # Original task-start decisions remain intact; only append the result.
    write(ROOT / 'TASK_START.json', task)


def file_role(path):
    name = path.relative_to(ROOT).as_posix()
    if name.startswith('context/'):
        source = {'approved_clean_panorama.png': 'assets_src/sky_lagoon/masters/sky_lagoon_panorama_master_v5_hd_3x1.png',
                  'current_castle.png': 'assets/sprites/sky_lagoon/sky_lagoon_castle_four_tower_v4.png',
                  'current_slide.png': 'assets/sprites/sky_lagoon/sky_lagoon_slide_v3_compact.png'}[path.name]
        return 'approved context reference', [source], 'Unmodified byte copy; original retained', 'Existing project artwork; retain source ASSET_LICENSES.md row'
    if name.startswith('objects/'):
        ident = name.split('/')[1]
        task = json.loads((ROOT / 'TASK_START.json').read_text())
        source = next(s['source_path'] for s in task['objects'] if s['id'] == ident)
        if path.name == 'identity_source.png':
            return 'approved identity/style reference', [source], 'Unmodified byte copy', 'Existing project artwork; retain source ASSET_LICENSES.md row'
        if path.name == 'window_identity_source.png':
            return 'owner high-resolution window reference', ['assets_src/sky_lagoon/reductive_rebuild_2026-07-28/stained_glass_owner_reference.png'], 'Unmodified byte copy', 'Owner-supplied project artwork; retain source provenance'
        if path.name in ('generated_native.png', 'padded_native.png'):
            return 'native built-in ImageGen pose/padding sheet', [source, f'{REL}/objects/{ident}/GENERATION.json'], 'Fresh reference drawings; native output preserved', 'OpenAI-generated output based on project identity artwork; https://openai.com/policies/terms-of-use/'
        if path.suffix in ('.png', '.aseprite'):
            input_name = 'window_identity_source.png' if ident == '10_glass' else ('padded_native.png' if (path.parent / 'padded_native.png').exists() or (ROOT / 'objects' / ident / 'padded_native.png').exists() else 'generated_native.png')
            return 'Aseprite cleaned raster state / atlas / editable master', [f'{REL}/objects/{ident}/{input_name}', source], 'Aseprite isolation, edge cleanup, registration and recorded fixture/light edits; original inputs retained', 'Project reference derivative; generated-output or owner-source rights as recorded'
        return 'generation/authoring/timing metadata', [source], 'Authored JSON evidence; reference only', 'Project-authored reference metadata'
    if name.startswith('scene/'):
        return 'layered context motion study / encoded preview', [f'{REL}/context/approved_clean_panorama.png', f'{REL}/scene/SCENE_PARAMETERS.json'], 'Aseprite review composition; uniform scale, fixed approved fixtures, fresh object keys, local light/door study; FFmpeg MP4 encode', 'Project reference derivative; source-specific rights retained'
    return 'tool / archive metadata / operator index', [], 'Project-authored reference archive content', 'Project-authored content; no external source code copied'


def manifest():
    rows = []
    for path in sorted(ROOT.rglob('*')):
        if not path.is_file() or path.name in ('MANIFEST.json', 'REMOTE_VERIFICATION.json'): continue
        rel = path.relative_to(ROOT).as_posix()
        dimensions = None
        if path.suffix == '.png': dimensions = list(Image.open(path).size)
        elif path.suffix == '.aseprite': dimensions = list(struct.unpack_from('<HH', path.read_bytes(), 8))
        elif path.suffix == '.mp4': dimensions = [1920, 640]
        role, sources, change, license_info = file_role(path)
        sources = [{'path': src, 'sha256': sha(PROJECT / src)} for src in sources if (PROJECT / src).is_file()]
        rows.append({'path': rel, 'sha256': sha(path), 'bytes': path.stat().st_size,
                     'dimensions': dimensions, 'role': role, 'sources': sources,
                     'modification': change, 'license_provenance': license_info,
                     'runtime_asset': False, 'accepted_keyframe': False})
    payload = hashlib.sha256(''.join(r['path'] + '\t' + r['sha256'] + '\n' for r in rows).encode()).hexdigest()
    write(ROOT / 'MANIFEST.json', {'id': 'sky_lagoon_moderate_motion_v2_2026-09-30', 'status': 'CANDIDATE_MOTION_REFERENCE_ARCHIVE',
          'baseline': BASELINE, 'branch': BRANCH, 'repository': 'https://github.com/Ebonyks/mermaid-roshan-reef',
          'packet_path': REL, 'owner_requested_objects': 10, 'frame_canvas': [512, 512], 'raster_states': 66,
          'generation_mode': 'built-in image_gen, nine pose sheets plus two padding repairs; owner-source reuse for glass',
          'ARCHIVE_COMPLETE': 'PENDING_REMOTE_BYTE_VERIFICATION', 'GENERATION_READY': False, 'DELIVERY_ACCEPTED': False,
          'packet_payload_sha256': payload, 'payload_hash_method': 'SHA256 UTF-8 sorted path + TAB + file SHA256 + LF, relative to packet root',
          'excluded_from_payload': ['MANIFEST.json', 'REMOTE_VERIFICATION.json'], 'files': rows,
          'limits': 'New moderate object/scene motion references. Not human hand-drawn pixel art, final loops, accepted game integration or full-frame cinematic delivery.'})
    print(f'Manifest: {len(rows)} files, {sum(r["bytes"] for r in rows) / 1024**2:.1f} MiB, {payload}', flush=True)


def project_docs():
    licenses = PROJECT / 'ASSET_LICENSES.md'
    start = '<!-- SKY_LAGOON_MODERATE_MOTION_V2_START -->';end = '<!-- SKY_LAGOON_MODERATE_MOTION_V2_END -->'
    text = licenses.read_text(encoding='utf-8')
    if start in text: text = text[:text.index(start)] + text[text.index(end) + len(end):]
    rows = [start, '', '## Sky Lagoon moderate animation references v2 — 2026-09-30', '',
            'Reference samples only; source originals retained. New pose drawings use built-in ImageGen; isolation, edge cleanup, registration and context composition use Aseprite. Full-frame cinematic and runtime acceptance remain open.', '',
            '| Asset | Source / provenance | License / URL | Modifications |', '|---|---|---|---|']
    for path in sorted(ROOT.rglob('*')):
        if not path.is_file() or path.suffix not in ('.png', '.aseprite', '.mp4'): continue
        role, sources, change, license_info = file_role(path)
        rows.append(f'| `{path.relative_to(PROJECT).as_posix()}` | {role}; '+ '; '.join(f'`{s}`' for s in sources) + f' | {license_info} | {change} |')
    licenses.write_text(text.rstrip() + '\n\n' + '\n'.join(rows) + '\n\n' + end + '\n', encoding='utf-8')
    ledger = PROJECT / 'design/05_DOC_LEDGER.md'
    text = ledger.read_text(encoding='utf-8')
    if f'`{REL}/README.md`' not in text:
        text = text.rstrip() + f'\n| `{REL}/README.md` | 🟣 | `CANDIDATE / MOTION_REFERENCE_ONLY`; owner-requested ten moderate-resolution object samples, native generated pose sheets, Aseprite cleanup/masters and a layered Sky Lagoon context study. Source pixels/provenance preserved; six-key polish and owner/runtime/device/child/cinematic acceptance remain open. Exact remote byte verification is separate. |\n'
        ledger.write_text(text, encoding='utf-8')
    master = PROJECT / 'audit/MASTER_AUDIT_2026-08-09.md'
    text = master.read_text(encoding='utf-8')
    entry = f'Sky Lagoon moderate animation supplement (2026-09-30): [ten larger samples and layered context study](../{REL}/README.md), with [impact record](../design/audit_impacts/sky-lagoon-moderate-animation-20260930.json). Nine six-pose sheets and twelve reused-portrait light states supply 512px Aseprite references; source originals and prior rejected archive are preserved. No runtime, cinematic, owner, device, child or finding-closure acceptance.\n\n'
    if f'../{REL}/README.md' not in text: master.write_text(text.replace('## 0. Planning entry\n\n', '## 0. Planning entry\n\n' + entry, 1), encoding='utf-8')
    attrs = PROJECT / '.gitattributes';text = attrs.read_text(encoding='utf-8')
    rule = REL + '/** -text whitespace=cr-at-eol'
    if rule not in text: attrs.write_text(text.rstrip() + '\n\n# Literal moderate-reference packet hashes survive every checkout.\n' + rule + '\n', encoding='utf-8')
    impact = PROJECT / 'design/audit_impacts/sky-lagoon-moderate-animation-20260930.json'
    record = json.loads(impact.read_text())
    paths = {'.gitattributes', 'ASSET_LICENSES.md', 'audit/MASTER_AUDIT_2026-08-09.md', 'design/05_DOC_LEDGER.md'}
    paths.update(p.relative_to(PROJECT).as_posix() for p in ROOT.rglob('*') if p.is_file())
    paths.add(REL + '/REMOTE_VERIFICATION.json')
    record['files'] = sorted(paths)
    record['validation'][0] = {'command': 'Codex native sheets, cleaned contours and scene review', 'result': 'PASS', 'evidence': REL + '/REVIEW.json; bounded reference inspection only; owner/contact/continuity acceptance open.'}
    record['validation'][1] = {'command': 'production/finish.py --verify-only', 'result': 'PASS', 'evidence': REL + '/MACHINE_VERIFICATION.json; ten native masters, 66 distinct RGBA states, alpha margins and layered scene round trip.'}
    impact.write_text(json.dumps(record, indent=2), encoding='utf-8')


if __name__ == '__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--hash-only', action='store_true');args=parser.parse_args()
    if not args.hash_only: describe();project_docs()
    manifest()
