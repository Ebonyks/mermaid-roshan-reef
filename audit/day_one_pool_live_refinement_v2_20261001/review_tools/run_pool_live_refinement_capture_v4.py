from pathlib import Path
import hashlib, json, os, shutil, subprocess, time

root = Path(__file__).resolve().parents[1]
family = root / 'audit/day_one_pool_live_refinement_v2_20261001'
out = family / 'native_actions_1280_v4'
assert not out.exists(), 'Do not overwrite a capture attempt.'
out.mkdir(parents=True)
env = os.environ.copy()
home = root / 'tmp/pool_live_refinement_native_v4'
for key, folder in [('APPDATA','Roaming'), ('LOCALAPPDATA','Local')]:
    p = home / folder
    p.mkdir(parents=True, exist_ok=True)
    env[key] = str(p)
env['DAY_ONE_POOL_CAPTURE_OUT'] = str(out)
chain = ['project.godot', 'scenes/main.tscn', 'scripts/main.gd', 'scripts/day_one.gd',
         'scripts/arena/castle_rooms_25d.gd', 'scripts/games/day_one_pool_cleanup.gd',
         'scripts/games/pool_skimmer_activity.gd', 'scripts/games/pool_waterfall_activity.gd',
         'scripts/games/pool_seahorse_rescue_activity.gd', 'tools/capture_day_one_pool_live_refinement_actions.gd',
         'assets/castle/day_one_pool/activities/refinement_v2/floating_trash_atlas.png',
         'assets/castle/day_one_pool/activities/refinement_v2/pool_skimmer.png']
chain = [p for p in chain if (root/p).is_file()]
def hashes():
    return {p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in chain}
before=hashes()
for p in chain:
    target = out/'source_chain'/p
    target.parent.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(root/p,target)
cmd=['C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/Godot/4.7.2/godot_console.exe',
     '--path',str(root),'--windowed','--resolution','1280x720',
     '--script','res://tools/capture_day_one_pool_live_refinement_actions.gd','--','--touch','--classic-touch-test']
started=time.time()
with (out/'capture.stdout.log').open('wb') as stdout,(out/'capture.stderr.log').open('wb') as stderr:
    result=subprocess.run(cmd,cwd=root,env=env,stdout=stdout,stderr=stderr)
after=hashes()
receipt={'command':cmd,'exit_code':result.returncode,'elapsed_seconds':round(time.time()-started,3),
         'source_before':before,'source_after':after,'source_unchanged':before==after}
(out/'PROCESS_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'exit_code':result.returncode,'source_unchanged':before==after,'elapsed_seconds':receipt['elapsed_seconds']}),flush=True)
raise SystemExit(result.returncode if before==after else 2)
