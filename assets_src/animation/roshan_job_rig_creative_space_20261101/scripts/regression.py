"""Windows orchestration of the unchanged scripts/ci.sh checks and trusted roster."""
from pathlib import Path
import os, re, shlex, subprocess, sys, time, json

ROOT = Path(__file__).resolve().parents[4]
PACKET = Path(__file__).resolve().parents[1]
OUT = PACKET / 'evidence' / 'regression'
OUT.mkdir(parents=True, exist_ok=True)
RUN_ID=str(time.time_ns())
GODOT = subprocess.check_output([sys.executable, '-B', 'tools/resolve_godot.py'], cwd=ROOT, text=True).strip()
ENV = dict(os.environ, GODOT=GODOT, PYTHONUTF8='1', PYTHONIOENCODING='utf-8')
source = (ROOT / 'scripts/ci.sh').read_text(encoding='utf-8')
bad = re.compile(r'FAIL|FAILED|ISSUE|TIMEOUT|STUCK|DID NOT|MISSING|SCRIPT ERROR|Parse Error|Compile Error')
resource_bad = re.compile(r'SCRIPT ERROR|Invalid assignment of property or key|The tweened property .* does not exist|ERROR:.*(Failed loading resource|Cannot open file|No loader found|Resource file not found)')
rows = []

def run(name, args, timeout=480, env=ENV, advisory=False, inspect=False):
    start = time.monotonic()
    try:
        result = subprocess.run(args, cwd=ROOT, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout)
        data, code = result.stdout, result.returncode
    except subprocess.TimeoutExpired as exc:
        data, code = exc.stdout or b'', 124
    (OUT / (name + '.log')).write_bytes(data)
    text = data.decode('utf-8', errors='replace')
    exit_hang = code == 124 and re.search(r'ALL OK|RESULT', '\n'.join(text.splitlines()[-5:]))
    passed = (code == 0 or bool(exit_hang)) and (bool(data) if inspect else True)
    if inspect:
        passed = passed and not bad.search(text) and not resource_bad.search(text)
    row = dict(name=name, command=args, exit=code, passed=bool(passed), advisory=advisory, seconds=round(time.monotonic()-start, 3))
    rows.append(row)
    (OUT / (sys.argv[1] + '_summary.json')).write_text(json.dumps(rows, indent=2)+'\n')
    print(name, 'PASS' if passed else ('ADVISORY' if advisory else 'FAIL'), row['seconds'], flush=True)
    return passed or advisory

if sys.argv[1] == 'probes':
    if not run('import', [GODOT, '--headless', '--path', str(ROOT), '--import'], timeout=720):
        raise SystemExit(1)
    import_text = (OUT/'import.log').read_text(encoding='utf-8',errors='replace')
    if resource_bad.search(import_text) or re.search(r'Parse Error|Compile Error|ERR_FILE_CORRUPT|Error importing|Cannot load resource', import_text):
        print('IMPORT ERRORS', flush=True); raise SystemExit(1)
    names = re.search(r'(?m)^for p in (.+?); do', source).group(1).split()
    all_ok = run('game_2d', [sys.executable, '-B', 'tools/audit_game_2d.py', '--regression-gate'], timeout=None)
    for name in names:
        home = ROOT/'tmp'/('creative-profile-'+RUN_ID+'-'+name)
        for folder in ['appdata','localappdata','data','config']:(home/folder).mkdir(parents=True, exist_ok=True)
        env = dict(ENV, APPDATA=str(home/'appdata'), LOCALAPPDATA=str(home/'localappdata'), XDG_DATA_HOME=str(home/'data'), XDG_CONFIG_HOME=str(home/'config'))
        mode = '--hybrid-touch-test' if name in ['probe_passive','probe_touch_router','probe_touch_stress','probe_interaction','probe_touch_adversary'] else '--classic-touch-test'
        all_ok = run(name, [GODOT,'--headless','-s','scripts/'+name+'.gd','--','--touch',mode], env=env, inspect=True) and all_ok
    print('FULL TRUSTED PROBES ALL OK' if all_ok else 'FULL TRUSTED PROBES FAIL', flush=True)
    raise SystemExit(0 if all_ok else 1)
else:
    logical = source.replace('\\\n',' ')
    commands = [line.strip() for line in logical.splitlines() if line.strip().startswith('python3 ')]
    all_ok = True
    for index, command in enumerate(commands):
        advisory = '|| true' in command
        command = command.split('||')[0].strip()
        if "$(find scripts -name '*.gd')" in command:
            args = shlex.split(command.split('$(find')[0]) + [str(f.relative_to(ROOT)).replace('\\','/') for f in (ROOT/'scripts').rglob('*.gd')]
        else: args = shlex.split(command)
        args = [sys.executable if a=='python3' else (GODOT if a=='$GODOT' else a) for a in args]
        if any('*' in a for a in args):
            expanded=[]
            for a in args:
                expanded.extend([str(f.relative_to(ROOT)).replace('\\','/') for f in ROOT.glob(a)] if '*' in a else [a])
            args=expanded
        all_ok = run('static_%02d'%index,args,timeout=None,advisory=advisory) and all_ok
    print('STATIC ALL OK' if all_ok else 'STATIC FAIL', flush=True)
    raise SystemExit(0 if all_ok else 1)
