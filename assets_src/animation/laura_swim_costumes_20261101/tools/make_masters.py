"""Retain exact editable RGBA loops and prove pixel-exact Aseprite reopening."""
from pathlib import Path
import hashlib,json,subprocess
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
ASEPRITE=Path('C:/Program Files/Aseprite/Aseprite.exe')


def main():
    groups=json.loads((ROOT/'sources.json').read_text())['groups']
    (ROOT/'masters').mkdir(exist_ok=True)
    for group in groups:
        for theme in group['themes']:
            (ROOT/'raw_masters'/theme).mkdir(parents=True,exist_ok=True)
    for mode in ['import','reopen']:
        with (ROOT/'evidence'/('aseprite_'+mode+'.log')).open('wb') as out:
            subprocess.run([str(ASEPRITE),'--batch','--script-param','root='+ROOT.as_posix(),'--script-param','mode='+mode,'--script',str(ROOT/'tools/masters.lua')],stdout=out,stderr=subprocess.STDOUT,check=True,timeout=1200,creationflags=subprocess.CREATE_NO_WINDOW)
    rows=[]
    for group in groups:
        for theme in group['themes']:
            for index in range(54):
                original=Image.open(ROOT/f'raw_render/{group["group"]}/{theme}/loop/{index:04}.png').convert('RGBA').tobytes()
                reopened=Image.open(ROOT/f'raw_masters/{theme}/{index:04}.png').convert('RGBA').tobytes()
                assert original==reopened,(theme,index)
            p=ROOT/'masters'/(theme+'.aseprite')
            rows.append({'theme':theme,'frames':54,'duration_ms':1800,'pass':True,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
    result={'pass':True,'frames_reopened':len(rows)*54,'masters':rows,'rgba_pixel_equality':True,'source_editable_action':'shared/swim_motion.gd plus frozen native meshes and painted parts; Aseprite loops are the pixel cleanup bridge.','extra_endpoint':'Native frame54 is QA-only and excluded from the54-frame loop master.'}
    (ROOT/'evidence/aseprite_roundtrip.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
    print('EXACT_ASEPRITE_MASTERS',len(rows),result['frames_reopened'],flush=True)


if __name__=='__main__':
    main()
