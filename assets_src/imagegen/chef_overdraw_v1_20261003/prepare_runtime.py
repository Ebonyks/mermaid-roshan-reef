"""Reproduce the selected static Chef backdrop's existing POT promotion.

The source edit is the preserved native imagegen output. This script only
applies the project's established whole-canvas normalization and tile split.
"""
from pathlib import Path
import argparse,io,sys
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT))
sys.path.insert(0,str(ROOT/"tools"))
from tools.build_opera_codex_art import native_master
PACKET=Path(__file__).resolve().parent
def main():
    args=argparse.ArgumentParser()
    args.add_argument('--check',action='store_true')
    check=args.parse_args().check
    source=PACKET/'world_chef_stations_native.png'
    master=native_master(source)
    targets={PACKET/'world_chef_stations_master.png':master}
    directory=ROOT/'assets/opera/worlds/backdrops/chef_story_clean_v1'
    for row in range(2):
        for col in range(2):
            targets[directory/f'world_chef_c{col}r{row}.png']=master.crop(
                (col*1024,row*1024,(col+1)*1024,(row+1)*1024))
    for target,image in targets.items():
        data=io.BytesIO()
        image.save(data,format='PNG')
        if check:
            if target.read_bytes()!=data.getvalue():
                raise SystemExit('CHEF_RUNTIME|DRIFT|'+target.relative_to(ROOT).as_posix())
        else:
            target.parent.mkdir(parents=True,exist_ok=True)
            target.write_bytes(data.getvalue())
    print('CHEF_RUNTIME|ALL OK|five deterministic derivatives; original native unchanged')
if __name__=='__main__':
    main()