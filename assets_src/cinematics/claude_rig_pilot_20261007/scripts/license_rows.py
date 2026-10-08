#!/usr/bin/env python3
"""Append ASSET_LICENSES.md rows for a pilot clip folder (frames, cells, atlases, outfits, videos).

Adds one row per image/video file under the folder that ASSET_LICENSES.md does not list yet, at the
end of the rig-pilot section (the last section of the file). Text only.

    python -I scripts/license_rows.py <folder relative to the pilot> <source kind: union_take1|rig_take|guides>
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from pilot_common import PILOT, ROOT

BASE = 'https://github.com/Ebonyks/mermaid-roshan-reef/tree/6238934447cf28834874396dfbaff65effafda46/'
SRC = {
    'union_take1': ('LTX-2.5 Union take 1 frames', BASE + 'assets_src/cinematics/ltx25_union_trial_20261004'),
    'rig_take': ('a rig-guided LTX-2.5 take of this pilot (RTX 3060 Ti, run2)', BASE + 'assets_src/cinematics/ltx25_union_trial_20261004'),
    'guides': ('', BASE + 'assets_src/cinematics/ltx25_union_trial_20261004/scripts/guide.lua'),
}
GUIDE_TERMS = ('Project-owned authored structural guide; contours ported from the project\'s Union `guide.lua`; arm pose authored '
               'on the fixed-length rig (scripts/animate_run*.py or the revision-2 solve); no model output pixels.')
SHIFT_TERMS = ('Project-owned derivative of the Union trial opening image (approved Roshan K0 cell, upscaled); no model output '
               'pixels.')
TERMS = ('Project-owned Roshan derivative of {src} (LTX-2.x community model output terms) and, for outfits, the project '
         'party garment and procedural bows; no model weights redistributed.')


def describe(rel):
    name = rel.split('/')[-1]
    if name == 'identity_shift40.png':
        return ('The Union opening image moved 40 px right as a whole, the uncovered strip filled with its flat background; '
                'opening and end-lock image for takes e1, f1 and g1. Generator input only, not runtime.')
    for lane, size in (('guide_full', '640x896'), ('guide_half', '320x448'), ('guide_quarter', '160x224')):
        if f'/{lane}/' in rel:
            return (f'Structural outline at {size}: Union contours moved by rigid region turns (whole-body acting) plus the rig arm '
                    'at the W3 contract lengths; motion-only, no appearance authority or delivery pixels.')
    if '/refined_frames/' in rel or '/stage1_frames/' in rel:
        return 'Complete native frame as generated (640x896); no registration, repair or selection. Reference only, not runtime.'
    if '/cells/' in rel:
        return ('Whole frame matted on its flat background, one uniform 2.5 px edge erosion, mapped to the approved 256 px cell '
                '(scripts/clip_cells.py); no part edits. Reference only, not runtime.')
    if name == 'atlas.png':
        return 'The 41 cells above in an 8-column atlas (scripts/clip_cells.py). Reference only, not runtime.'
    if '/outfits/' in rel:
        kind = name.rsplit('_', 1)[1][:-4]
        return (f'Game outfit "{kind}" baked onto every cell by tools/build_fashion_outfits.gd --fit/--out with the clip fit '
                '(constant K0 bodice box moved with the tracked bodice). Outfit test, not runtime.')
    if name.endswith('.mp4'):
        return 'H.264 viewing copy, 41 frames at 24 fps; the PNGs are authoritative.'
    return 'Pilot evidence derivative. Reference only, not runtime.'


def main():
    folder, kind = sys.argv[1], sys.argv[2]
    src, url = SRC[kind]
    lic = ROOT / 'ASSET_LICENSES.md'; text = lic.read_text(encoding='utf-8')
    rows = []
    for f in sorted((PILOT / folder).rglob('*')):
        if f.suffix.lower() not in ('.png', '.mp4') or not f.is_file():
            continue
        rel = str(f.relative_to(ROOT)).replace('\\', '/')
        if f'`{rel}`' in text:
            continue
        terms = (SHIFT_TERMS if rel.endswith('identity_shift40.png') else GUIDE_TERMS) if kind == 'guides' else TERMS.format(src=src)
        rows.append(f'| `{rel}` | {terms} | {url} | {describe(rel)} |')
    if rows:
        lic.write_text(text.rstrip('\n') + '\n' + '\n'.join(rows) + '\n', encoding='utf-8')
    print(len(rows), 'rows added')


if __name__ == '__main__':
    main()
