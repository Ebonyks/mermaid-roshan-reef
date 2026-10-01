from pathlib import Path
import hashlib, json, os, subprocess, time

root = Path(__file__).resolve().parents[1]
out = root / 'audit/day_one_pool_live_refinement_v2_20261001/focused_pointer_v6'
out.mkdir(parents=True, exist_ok=True)
assert not (out / 'RECEIPT.json').exists(), 'Preserve this attempt; use a new directory for retries.'
python = 'C:/Users/Peter/AppData/Local/Python/bin/python.exe'
godot = 'C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/Godot/4.7.2/godot_console.exe'
scripts = ['scripts/games/pool_skimmer_activity.gd', 'scripts/games/day_one_pool_cleanup.gd',
           'tools/pack_day_one_pool_refinement_atlas.gd', 'tools/capture_day_one_pool_live_refinement_actions.gd', 'tools/probe_day_one_pool_refinement.gd', 'scripts/games/pool_seahorse_rescue_activity.gd']
env = os.environ.copy()
home = root / 'tmp/pool_live_refinement_focused_pointer_v6'
for key, folder in [('APPDATA', 'Roaming'), ('LOCALAPPDATA', 'Local')]:
    target = home / folder
    target.mkdir(parents=True, exist_ok=True)
    env[key] = str(target)
env['PYTHONUTF8'] = '1'
env['POOL_REFINEMENT_PROBE_OUT'] = str(out / 'INDEPENDENT_TRANSFER_CHECKS.json')
commands = [('parser', [python, '-X', 'utf8', '-B', '-m', 'gdtoolkit.parser', *scripts]),
            ('inference', [python, '-X', 'utf8', '-B', 'tools/lint_inference.py', *scripts]),
            ('import', [godot, '--headless', '--path', str(root), '--import'])]
commands += [(f'analyzer_{i}', [godot, '--headless', '--path', str(root), '--check-only', '--script', p]) for i,p in enumerate(scripts)]
commands += [('pool_trusted', [godot, '--headless', '--path', str(root), '--script', 'scripts/probe_day_one_pool_cleanup.gd']), ('contextual_voice', [godot, '--headless', '--path', str(root), '--script', 'scripts/probe_day_one_contextual_voice.gd']), ('independent_transfer', [godot, '--headless', '--path', str(root), '--script', 'tools/probe_day_one_pool_refinement.gd', 'scripts/games/pool_seahorse_rescue_activity.gd'])]
rows = []
before = {p: hashlib.sha256((root / p).read_bytes()).hexdigest() for p in scripts}
for name, cmd in commands:
    started = time.time()
    with (out / f'{name}.stdout.log').open('wb') as stdout, (out / f'{name}.stderr.log').open('wb') as stderr:
        result = subprocess.run(cmd, cwd=root, env=env, stdout=stdout, stderr=stderr)
    rows.append({'name': name, 'command': cmd, 'exit_code': result.returncode, 'elapsed_seconds': round(time.time()-started,3)})
    print(name, result.returncode, flush=True)
    if result.returncode: break
receipt = {'schema':'reef.pool-live-focused-checks.v1', 'source_before':before,
           'source_after':{p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in scripts},
           'commands':rows, 'pass':len(rows)==len(commands) and all(r['exit_code']==0 for r in rows)}
(out / 'RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
raise SystemExit(0 if receipt['pass'] else 1)
