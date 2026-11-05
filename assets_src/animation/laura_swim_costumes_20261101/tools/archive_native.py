"""Preserve every native source pixel as lossless RGB plus lossless alpha."""
from pathlib import Path
import concurrent.futures, hashlib, json, subprocess
import numpy as np
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
FFMPEG=Path('C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/FFmpeg/8.1.2/bin/ffmpeg.exe')


def execute(args):
    result=subprocess.run([str(FFMPEG),'-y','-v','error',*args],capture_output=True,timeout=600,creationflags=subprocess.CREATE_NO_WINDOW)
    assert result.returncode==0,result.stderr.decode(errors='replace')


def read_exact(stream,count):
    result=bytearray()
    while len(result)<count:
        chunk=stream.read(count-len(result))
        if not chunk:
            raise EOFError('Short decoded native frame')
        result.extend(chunk)
    return bytes(result)


def one(row):
    group,theme,clip,count=row
    source=ROOT/f'raw_render/{group}/{theme}/{clip}'
    dest=ROOT/'archives'/theme
    dest.mkdir(parents=True,exist_ok=True)
    rgb=dest/(clip+'_rgb.mkv');alpha=dest/(clip+'_alpha.mkv')
    common=['-framerate','30','-i',str(source/'%04d.png'),'-frames:v',str(count)]
    execute(common+['-c:v','libx264rgb','-crf','0','-preset','fast','-threads','1','-pix_fmt','rgb24',str(rgb)])
    execute(common+['-vf','alphaextract','-c:v','ffv1','-threads','1','-pix_fmt','gray',str(alpha)])
    processes=[]
    for path,pix in [(rgb,'rgb24'),(alpha,'gray')]:
        processes.append(subprocess.Popen([str(FFMPEG),'-v','error','-i',str(path),'-f','rawvideo','-pix_fmt',pix,'pipe:1'],stdout=subprocess.PIPE,stderr=subprocess.PIPE,creationflags=subprocess.CREATE_NO_WINDOW))
    hashes=[]
    for index in range(count):
        color=np.frombuffer(read_exact(processes[0].stdout,1024*1024*3),dtype=np.uint8).reshape(1024,1024,3)
        matte=np.frombuffer(read_exact(processes[1].stdout,1024*1024),dtype=np.uint8).reshape(1024,1024,1)
        decoded=np.concatenate([color,matte],axis=2).tobytes()
        original=Image.open(source/f'{index:04}.png').convert('RGBA').tobytes()
        assert original==decoded,(theme,clip,index)
        hashes.append(hashlib.sha256(decoded).hexdigest())
    for process in processes:
        assert process.stdout.read()==b''
        error=process.stderr.read()
        assert process.wait()==0,error.decode(errors='replace')
    files=[{'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in [rgb,alpha]]
    assert max(x['bytes'] for x in files)<100*1048576
    record={'theme':theme,'clip':clip,'frames':count,'fps':30,'pass':True,'exact_rgba_decode':True,'rgba_sha256':hashes,'files':files}
    (dest/(clip+'_receipt.json')).write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
    print('NATIVE_ARCHIVE_EXACT',theme,clip,count,flush=True)
    return record


def main():
    groups=json.loads((ROOT/'sources.json').read_text())['groups']
    jobs=[(g['group'],theme,clip,count) for g in groups for theme in g['themes'] for clip,count in [('loop',55),('travel',217)]]
    records=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        for future in concurrent.futures.as_completed([pool.submit(one,row) for row in jobs]):
            records.append(future.result())
    (ROOT/'evidence/native_archives.json').write_text(json.dumps({'pass':True,'clips':len(records),'frames':sum(x['frames'] for x in records),'receipts':['archives/'+r['theme']+'/'+r['clip']+'_receipt.json' for r in records]},indent=2)+'\n',encoding='utf-8',newline='\n')
    print('NATIVE_ARCHIVES_COMPLETE',len(records),flush=True)


if __name__=='__main__':
    main()
