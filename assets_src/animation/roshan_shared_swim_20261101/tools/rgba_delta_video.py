"""Explicit 2D, lossless RGB/alpha numeric-difference video I/O."""
import subprocess
import tempfile
import numpy as np
from make_review import FFMPEG,ROOT,W,H,read_exact


def encode_rgba(path,frames,count):
    with tempfile.TemporaryFile() as errors:
        command=[str(FFMPEG),'-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgba','-s',f'{W}x{H}','-r','30','-i','pipe:0',
                 '-filter_complex','[0:v]split[r][a];[r]format=rgb24[rgb];[a]alphaextract[alpha]',
                 '-map','[rgb]','-map','[alpha]','-frames:v',str(count),'-c:v:0','libx264rgb','-threads:v:0','2','-preset','medium','-crf','0',
                 '-pix_fmt:v:0','rgb24','-c:v:1','ffv1','-threads:v:1','2','-level:v:1','3','-pix_fmt:v:1','gray',
                 '-metadata:s:v:0','title=RGBA XOR RGB numeric differences','-metadata:s:v:1','title=RGBA XOR alpha numeric differences',str(path)]
        process=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.DEVNULL,stderr=errors)
        written=0
        try:
            for frame in frames:
                data=frame.tobytes() if isinstance(frame,np.ndarray) else frame
                assert len(data)==W*H*4
                process.stdin.write(data);written+=1
            process.stdin.close();code=process.wait(timeout=180);errors.seek(0)
            assert code==0,errors.read().decode(errors='replace')
            assert written==count
        finally:
            if process.poll() is None:process.terminate();process.wait(timeout=15)


def decode_rgba(path,count):
    common=[str(FFMPEG),'-hide_banner','-loglevel','error','-threads','2','-i',str(path)]
    rgb=subprocess.Popen(common+['-map','0:v:0','-pix_fmt','rgb24','-f','rawvideo','pipe:1'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    alpha=subprocess.Popen(common+['-map','0:v:1','-pix_fmt','gray','-f','rawvideo','pipe:1'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    try:
        for _ in range(count):
            frame=np.empty((H,W,4),np.uint8)
            frame[:,:,:3]=np.frombuffer(read_exact(rgb.stdout,W*H*3),np.uint8).reshape(H,W,3)
            frame[:,:,3]=np.frombuffer(read_exact(alpha.stdout,W*H),np.uint8).reshape(H,W)
            yield frame
        assert not rgb.stdout.read(1) and not alpha.stdout.read(1)
        assert rgb.wait(timeout=60)==0 and alpha.wait(timeout=60)==0
    finally:
        for process in [rgb,alpha]:
            if process.poll() is None:process.terminate();process.wait(timeout=15)
