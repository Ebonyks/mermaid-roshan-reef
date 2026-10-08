#!/usr/bin/env python3
"""Write manifest.json: SHA-256 and size of every packet file plus the bound sources.

    python -I scripts/manifest.py
"""
import hashlib, sys
sys.path.insert(0, str(__import__('pathlib').Path(__file__).resolve().parent))
from pilot_common import *

RUN2_STATUS = 'EXECUTION_PASS (8 of 8 local takes) / OWNER_REVIEW_PENDING; best candidate g1_slowwave'
SKIP = {'.godot', '__pycache__', 'staging'}


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    files = sorted(p for p in PILOT.rglob('*') if p.is_file() and not SKIP & set(p.relative_to(PILOT).parts)
                   and p.suffix not in ('.import', '.uid') and p.name != 'manifest.json')
    sources = [ATLAS, MEASURE, ROOT / 'tools/build_fashion_outfits.gd', ROOT / 'assets_src/fashion_designer/party_garment_v1/pose_fit.json',
               ROOT / 'assets_src/fashion_designer/party_garment_v1/native.png', UNION / 'scripts/guide.lua', UNION / 'identity_first_frame.png', UNION / 'prompt.txt',
               UNION / 'adapter_download.json'] + [Path(str(TAKE1) % i) for i in range(FRAMES)]
    save_json(PILOT / 'manifest.json', {
        'packet': 'assets_src/cinematics/claude_rig_pilot_20261007', 'status': {
            'run1': 'EXECUTION_PASS / OWNER_REJECTED', 'run2': RUN2_STATUS,
            'cosmetics_on_clips': 'PIPELINE_PASS (Union take 1 and all 8 run-2 takes) / OWNER_REVIEW_PENDING',
            'ARCHIVE_COMPLETE': False, 'GENERATION_READY': 'run2 guides, jobs and PC runner prepared; take budget spent (8 of 8)',
            'DELIVERY_ACCEPTED': False},
        'files': [{'path': p.relative_to(PILOT).as_posix(), 'bytes': p.stat().st_size, 'sha256': sha(p)} for p in files],
        'sources': [{'path': p.relative_to(ROOT).as_posix(), 'bytes': p.stat().st_size, 'sha256': sha(p)} for p in sources]})
    print('manifest:', len(files), 'files,', len(sources), 'sources')


if __name__ == '__main__':
    main()
