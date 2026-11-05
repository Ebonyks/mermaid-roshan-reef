"""Run frozen projects with one motion source, and require fresh native receipts."""
from pathlib import Path
import concurrent.futures, datetime, json, shutil, subprocess, sys, time

ROOT = Path(__file__).resolve().parents[1]
GODOT = Path('C:/Users/Peter/Documents/mermaid-roshan-reef/tmp/godot-4.7.2/editor/Godot_v4.7.2-stable_win64_console.exe')


def run(group, mode):
    project = ROOT/group['project']
    for name in ['swim_motion.gd','capture.gd']:
        shutil.copyfile(ROOT/'shared'/name, project/name)
    output = ROOT/('raw_render' if mode == 'full' else 'raw_preview')/group['group']
    output.mkdir(parents=True, exist_ok=True)
    receipt_path = output/'engine.json'
    before = time.time_ns()
    args = [str(GODOT),'--path',str(project),'--script','capture.gd','--position=-32000,-32000','--',str(output),','.join(group['themes']),mode]
    with (output/'native.log').open('wb') as out, (output/'native.err').open('wb') as err:
        result = subprocess.run(args,stdout=out,stderr=err,timeout=900,creationflags=subprocess.CREATE_NO_WINDOW)
    assert result.returncode == 0, (group['group'],result.returncode)
    assert not any(word in (output/'native.err').read_text(errors='replace') for word in ['ERROR:','SCRIPT ERROR:']), 'NATIVE_RESOURCE_OR_SCRIPT_ERROR '+group['group']
    assert receipt_path.exists() and receipt_path.stat().st_mtime_ns >= before
    receipt = json.loads(receipt_path.read_text())
    assert receipt['completed'] and receipt['renderer'] == 'mobile'
    assert all(receipt['version'][k] == v for k,v in {'major':4,'minor':7,'patch':2,'status':'stable'}.items())
    assert len(receipt['costumes']) == len(group['themes'])
    for item in receipt['costumes']:
        assert item['frames'] == ({'loop':55,'travel':217} if mode == 'full' else {'loop':7,'travel':7})
        assert item['pass'] and item['max_matrix_error'] < 1e-5
    print('NATIVE_GROUP_COMPLETE',group['group'],group['themes'],flush=True)
    return {'group':group['group'],'pass':True,'receipt':str(receipt_path.relative_to(ROOT)),'frames':sum(sum(x['frames'].values()) for x in receipt['costumes'])}


def main():
    mode = sys.argv[1] if len(sys.argv)>1 else 'full'
    groups = json.loads((ROOT/'sources.json').read_text())['groups']
    if len(sys.argv)>2:
        selected = sys.argv[2].split(',')
        groups = [g for g in groups if g['group'] in selected]
    rows = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        for future in concurrent.futures.as_completed([pool.submit(run,g,mode) for g in groups]):
            rows.append(future.result())
    evidence = ROOT/'evidence'
    evidence.mkdir(exist_ok=True)
    (evidence/('native_'+mode+'.json')).write_text(json.dumps({'pass':True,'completed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'rows':rows,'total_frames':sum(x['frames'] for x in rows)},indent=2)+'\n',encoding='utf-8',newline='\n')


if __name__ == '__main__':
    main()
