"""Verify the Aseprite-exported Eagle and reject the retired game crop."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image
ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / 'assets_src/characters/baby_eagle_2026-09-26/RUNTIME.json'
SOURCE_HASH = '166461427017b2624dcf1c342bde658c63a8247b522ad113c92f6ec1bb084bd9'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true', help='Compatibility alias; verification is always read-only')
    parser.parse_args()
    record = json.loads(RECORD.read_text(encoding='utf-8'))
    assert hashlib.sha256((ROOT / record['source']).read_bytes()).hexdigest() == SOURCE_HASH
    for key in ('output', 'native'):
        assert hashlib.sha256((ROOT / record[key]).read_bytes()).hexdigest() == record[key + '_sha256']
    with Image.open(ROOT / record['output']) as image:
        assert image.size == (290, 512) and image.mode == 'RGBA', 'Runtime placement canvas changed'
    assert not (ROOT / 'assets/book/baby_eagle.png').exists(), 'Retired backpack crop returned'
    for directory in ('scripts', 'scenes'):
        for path in (ROOT / directory).rglob('*'):
            if path.suffix in ('.gd', '.tscn', '.tres'):
                assert 'res://assets/book/baby_eagle.png' not in path.read_text(encoding='utf-8'), str(path)
    print('EAGLE|ALL OK')

if __name__ == '__main__':
    main()
