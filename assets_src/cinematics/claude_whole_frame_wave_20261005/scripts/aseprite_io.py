"""Minimal Aseprite (.aseprite, RGBA) writer/reader for layered review masters (format spec: aseprite/docs/ase-file-specs.md)."""
import struct, zlib, numpy as np
def _str(s): b=s.encode('utf-8'); return struct.pack('<H',len(b))+b
def _chunk(t,data): return struct.pack('<IH',len(data)+6,t)+data
def write(path, W, H, layers, frames, durations, tags=()):
    """layers: list of (name, visible); frames: list of dict name->uint8 RGBA (straight alpha) HxWx4 or None."""
    out=[]
    for fi,fr in enumerate(frames):
        chunks=[]
        if fi==0:
            chunks.append(_chunk(0x2019, struct.pack('<III',1,0,0)+b'\0'*8+struct.pack('<H',0)+bytes([0,0,0,0])))
            for name,vis in layers:
                chunks.append(_chunk(0x2004, struct.pack('<HHHHHHB3s',(1 if vis else 0)|2,0,0,0,0,0,255,b'\0'*3)+_str(name)))
            if tags:
                d=struct.pack('<H',len(tags))+b'\0'*8
                for a,b,name in tags: d+=struct.pack('<HHBH6s3sB',a,b,0,0,b'\0'*6,b'\0'*3,0)+_str(name)
                chunks.append(_chunk(0x2018,d))
        for li,(name,vis) in enumerate(layers):
            img=fr.get(name)
            if img is None: continue
            a=img[:,:,3]; ys,xs=np.nonzero(a)
            if len(xs)==0: continue
            x0,x1,y0,y1=xs.min(),xs.max()+1,ys.min(),ys.max()+1
            crop=np.ascontiguousarray(img[y0:y1,x0:x1])
            d=struct.pack('<HhhBHh5s',li,int(x0),int(y0),255,2,0,b'\0'*5)+struct.pack('<HH',x1-x0,y1-y0)+zlib.compress(crop.tobytes(),9)
            chunks.append(_chunk(0x2005,d))
        body=b''.join(chunks)
        out.append(struct.pack('<IHHH2sI',16+len(body),0xF1FA,min(len(chunks),0xFFFF),int(durations[fi]),b'\0\0',len(chunks))+body)
    frames_b=b''.join(out)
    hdr=struct.pack('<IHHHHHIHII B3sHBBhhHH84s',128+len(frames_b),0xA5E0,len(frames),W,H,32,1,100,0,0,0,b'\0'*3,1,1,1,0,0,16,16,b'\0'*84)
    assert len(hdr)==128
    open(path,'wb').write(hdr+frames_b)

def read(path):
    b=open(path,'rb').read()
    size,magic,nf,W,H,depth=struct.unpack_from('<IHHHHH',b,0); assert magic==0xA5E0 and depth==32 and size==len(b)
    p=128; layers=[]; frames=[]; durs=[]; tags=[]
    for fi in range(nf):
        fsize,fm,old,dur,_,new=struct.unpack_from('<IHHH2sI',b,p); assert fm==0xF1FA
        q=p+16; n=new if new else old; cels={}
        for _ in range(n):
            csz,ct=struct.unpack_from('<IH',b,q); d=b[q+6:q+csz]
            if ct==0x2004:
                L=struct.unpack_from('<H',d,16)[0]; layers.append((d[18:18+L].decode(),bool(struct.unpack_from('<H',d,0)[0]&1)))
            elif ct==0x2005:
                li,x,y,op,typ,z=struct.unpack_from('<HhhBHh',d,0); assert typ==2
                w,h=struct.unpack_from('<HH',d,16); px=np.frombuffer(zlib.decompress(d[20:]),np.uint8).reshape(h,w,4)
                full=np.zeros((H,W,4),np.uint8); full[y:y+h,x:x+w]=px; cels[layers[li][0]]=full
            elif ct==0x2018:
                nt=struct.unpack_from('<H',d,0)[0]; o=10
                for _t in range(nt):
                    a,bb=struct.unpack_from('<HH',d,o); o+=17; L=struct.unpack_from('<H',d,o)[0]; tags.append((a,bb,d[o+2:o+2+L].decode())); o+=2+L
            q+=csz
        frames.append(cels); durs.append(dur); p+=fsize
    return dict(W=W,H=H,layers=layers,frames=frames,durations=durs,tags=tags)
