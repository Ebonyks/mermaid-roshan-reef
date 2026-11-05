"""Measure actual per-mesh material coverage, rather than a full-figure union proxy."""
from pathlib import Path
import concurrent.futures,json,shutil,subprocess,time

ROOT=Path(__file__).resolve().parents[1]
GODOT=Path('C:/Users/Peter/Documents/mermaid-roshan-reef/tmp/godot-4.7.2/editor/Godot_v4.7.2-stable_win64_console.exe')


def one(group):
    project=ROOT/group['project'];shutil.copyfile(ROOT/'shared/capture_surfaces.gd',project/'capture_surfaces.gd')
    folder=ROOT/'raw_surfaces'/group['group'];folder.mkdir(parents=True,exist_ok=True)
    before=time.time_ns()
    with (folder/'native.log').open('wb') as out,(folder/'native.err').open('wb') as err:
        result=subprocess.run([str(GODOT),'--path',str(project),'--script','capture_surfaces.gd','--position=-32000,-32000','--',str(folder),','.join(group['themes'])],stdout=out,stderr=err,timeout=300,creationflags=subprocess.CREATE_NO_WINDOW)
    assert result.returncode==0 and 'ERROR:' not in (folder/'native.err').read_text(errors='replace')
    p=folder/'surfaces_receipt.json';assert p.stat().st_mtime_ns>=before
    d=json.loads(p.read_text());assert d['completed'] and d['renderer']=='mobile'
    published=ROOT/'evidence/material_surfaces'/group['group']
    for theme in group['themes']:
        shutil.copytree(folder/theme,published/theme,dirs_exist_ok=True)
    shutil.copyfile(p,published/'surfaces_receipt.json')
    print('ISOLATED_SURFACES_CAPTURED',group['group'],sum(x['meshes'] for x in d['rows']),flush=True)
    return {'group':group['group'],'receipt':str(p.relative_to(ROOT)),'pass':True}


def main():
    groups=json.loads((ROOT/'sources.json').read_text())['groups'];rows=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        for future in concurrent.futures.as_completed([pool.submit(one,g) for g in groups]):rows.append(future.result())
    (ROOT/'evidence/isolated_surface_capture.json').write_text(json.dumps({'pass':True,'rows':rows},indent=2)+'\n',encoding='utf-8',newline='\n')


if __name__=='__main__':main()
