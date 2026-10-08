#!/usr/bin/env python3
"""Owner review video: the game cells of several run-2 takes side by side, plus one outfit.

Each column is a take's 256 px game cells (clip/cells) drawn at 2x with nearest-neighbour scaling over
a flat pale backdrop, so every take is seen at the same size and position whatever canvas it was
generated on. The last column is the party dress baked by the production builder onto the last take.
41 frames at 24 fps, H.264 viewing copy; the PNG cells are authoritative.
Owner-requested image exception for this pilot (previews, 2026-10-07).

    python -I scripts/compare_takes.py [out.mp4]
"""
import subprocess, sys, tempfile
from pathlib import Path
import numpy as np, cv2
from PIL import Image
sys.path.insert(0, str(Path(__file__).resolve().parent))
from pilot_common import PILOT, FRAMES

TAKES = [('a2_endlock', 'a2: rig guides'), ('e1_outward', 'e1: outward path'), ('f1_sidewave', 'f1: side wave'),
         ('g1_slowwave', 'g1: slower, one wave')]
OUTFIT = ('g1_slowwave', 'party', 'g1 + party dress')
BACK = np.array([214, 226, 232], np.float32)


def over(cell):
    a = cell[..., 3:4].astype(np.float32) / 255
    return (cell[..., :3] * a + BACK * (1 - a)).round().astype(np.uint8)


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else PILOT / 'run2' / 'comparison.mp4'
    outfit = np.array(Image.open(PILOT / f'run2/{OUTFIT[0]}/clip/outfits/roshan_wave_{OUTFIT[0]}_{OUTFIT[1]}.png').convert('RGBA'))
    with tempfile.TemporaryDirectory() as t:
        for i in range(FRAMES):
            cols = []
            for job, label in TAKES:
                cols.append((np.array(Image.open(PILOT / f'run2/{job}/clip/cells/{i:04d}.png').convert('RGBA')), label))
            r, c = divmod(i, 8)
            cols.append((outfit[r * 256:(r + 1) * 256, c * 256:(c + 1) * 256], OUTFIT[2]))
            row = []
            for cell, label in cols:
                im = cv2.resize(over(cell), (512, 512), interpolation=cv2.INTER_NEAREST)
                im = np.concatenate([np.full((40, 512, 3), 255, np.uint8), im], 0)
                cv2.putText(im, f'{label}  {i:02d}', (10, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (60, 60, 60), 2, cv2.LINE_AA)
                row.append(im)
            Image.fromarray(np.concatenate(row, 1)).save(f'{t}/{i:04d}.png')
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', '24', '-i', f'{t}/%04d.png', '-c:v', 'libx264', '-crf', '16',
                        '-pix_fmt', 'yuv420p', '-movflags', '+faststart', str(out)], check=True)
    print('wrote', out)


if __name__ == '__main__':
    main()
