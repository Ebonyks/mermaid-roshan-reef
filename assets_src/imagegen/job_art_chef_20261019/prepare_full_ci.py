from pathlib import Path
import json,sys
root=Path(__file__).resolve().parents[3]
out=Path(__file__).resolve().parent/'verification'
out.mkdir(exist_ok=True)
original=Path('C:/Users/Peter/Documents/mermaid-roshan-reef/assets_src/imagegen/artwork_quality_20261018/verification')
revision=sys.argv[1] if len(sys.argv)>1 else '01'
assert revision.isdigit()
adapter=(original/'windows_native_capture_05.py').read_text().replace('native_capture_05_events.jsonl','native_capture_'+revision+'_events.jsonl')
adapter_path=out/('windows_native_capture_'+revision+'.py')
assert not adapter_path.exists(),'Preserve original transport source'
adapter_path.write_text(adapter)
script=(original/'run_ci_native_capture_05.sh').read_text()
script=script.replace("cd '/c/Users/Peter/Documents/mermaid-roshan-reef'", "cd '/c/Users/Peter/.codex/worktrees/art-chef-20261019/mermaid-roshan-reef'")
script=script.replace('C:/Users/Peter/Documents/mermaid-roshan-reef/assets_src/imagegen/artwork_quality_20261018/verification/windows_native_capture_05.py',adapter_path.as_posix())
(out/('run_ci_native_capture_'+revision+'.sh')).write_text(script)
runner=(original/'run_full_ci_native_capture_05.py').read_text()
runner=runner.replace("'assets/mg/painted_quality_20261018'", "'assets/opera/worlds/chef_quality_20261019','assets/opera/worlds/widgets'")
runner=runner.replace("pins = {", "sources += [root/'tools/prepare_opera_minigame_art.py',root/'tools/tests/test_prepare_opera_minigame_art.py']\npins = {")
runner=runner.replace('run_ci_native_capture_05.sh','run_ci_native_capture_'+revision+'.sh').replace('full_ci_native_capture_05','full_ci_native_capture_'+revision)
runner=runner.replace('e31864fb904b0e1192b90a2b577516864497bb10','6fb96aeb441952c1053cc5ce18435fc57fc1d1ab')
(out/('run_full_ci_'+revision+'.py')).write_text(runner)
for name in ['native_capture_'+revision+'_events.jsonl','full_ci_native_capture_'+revision+'.log']:
    path=out/name
    assert not path.exists(),'Never overwrite an earlier CI transcript'
    path.touch()
(out/('full_ci_native_capture_'+revision+'.json')).write_text(json.dumps({'status':'PENDING','baseline':'6fb96aeb441952c1053cc5ce18435fc57fc1d1ab','scope':'Unchanged complete scripts/ci.sh;82ordered native probes; no retries; original deadlines/classifiers; exact approved Godot4.7.2'},indent=2)+'\n')
print('Prepared complete CI with native output transport; runtime frozen')
