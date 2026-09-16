"""Split oversized native review masters without changing any pixels or timing."""
from pathlib import Path
import json,subprocess,struct,zlib,hashlib,numpy as np
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'assets_src/characters/grand_puff_additional_cels_2026-09-15';TMP=ROOT/'tmp/puff-native-split';TMP.mkdir(exist_ok=True)
ASE='C:/Program Files/Aseprite/Aseprite.exe'
def q(p):return json.dumps(str(p).replace('\\','/'))
def verify_native(p,rows):
 b=p.read_bytes();size,magic,n,w,h,depth=struct.unpack_from('<IHHHHH',b);assert magic==0xA5E0 and n==len(rows) and w==944 and h==944 and depth==32
 offset=128
 for index,row in enumerate(rows):
  fsize,fmagic,nchunks,duration=struct.unpack_from('<IHHH',b,offset);assert fmagic==0xF1FA and duration==row['duration_ms'];pos=offset+16;found=False
  for _ in range(nchunks):
   csize,ctype=struct.unpack_from('<IH',b,pos);payload=b[pos+6:pos+csize]
   if ctype==0x2005:
    layer,x,y,opacity,kind=struct.unpack_from('<HhhBH',payload)
    if layer==1:
     assert kind==2 and opacity==255
     cw,ch=struct.unpack_from('<HH',payload,16);pixels=np.frombuffer(zlib.decompress(payload[20:]),dtype=np.uint8).reshape(ch,cw,4);canvas=np.zeros((944,944,4),dtype=np.uint8);canvas[y:y+ch,x:x+cw]=pixels
     assert hashlib.sha256(canvas.tobytes()).hexdigest()==row['cel_rgba_sha256'];found=True
   pos+=csize
  assert found,(p,index)
  offset+=fsize
 assert offset==len(b)
 return {'path':p.name,'sha256':hashlib.sha256(b).hexdigest(),'frame_count':n,'first_source_index':rows[0]['source_frame_index'],'last_source_index':rows[-1]['source_frame_index'],'all_pixels_and_durations_match':True}
for name in ['idle','flinch','prowl','giggle','bounce']:
 manifest=OUT/(name+'_CEL_MANIFEST.json')
 if not manifest.exists():continue
 m=json.loads(manifest.read_text());clip=m['clips'][0]
 if not clip.get('native_path'):continue
 source=OUT/clip['native_path']
 if not source.exists():continue
 rows=clip['frames'];parts=[];lines=[f'local original=app.open({q(source)})']
 for part,start in enumerate(range(0,len(rows),80),1):
  stop=min(start+80,len(rows));dest=OUT/f'grand_puff_{name}_part{part:02d}.aseprite';parts.append((dest,rows[start:stop]));lines += ['do local s=Sprite(944,944,ColorMode.RGB)','s.layers[1].name=original.layers[1].name','local reference=original.layers[1]:cel(1);if reference then s:newCel(s.layers[1],1,reference.image,reference.position) end','s.layers[1].isVisible=false','s.layers[1].isEditable=false','local actor=s:newLayer();actor.name=original.layers[2].name','local cleanup=s:newLayer();cleanup.name=original.layers[3].name']
  for i,idx in enumerate(range(start,stop),1):
   if i>1:lines.append('s:newEmptyFrame()')
   lines += [f's.frames[{i}].duration=original.frames[{idx+1}].duration',f'local c=original.layers[2]:cel({idx+1});s:newCel(actor,{i},c.image,c.position)']
  lines += [f'local t=s:newTag(1,{stop-start});t.name={q(name+" source frames "+str(start)+"-"+str(stop-1))}',f's:saveAs({q(dest)})','s:close() end']
 lines+=['original:close()'];script=TMP/(name+'.lua');script.write_bytes(('\n'.join(lines)+'\n').encode());subprocess.run([ASE,'--batch','--script',str(script)],check=True,capture_output=True)
 records=[verify_native(p,fr) for p,fr in parts]
 assert all(p.stat().st_size<100*1024*1024 for p,_ in parts)
 clip['native_parts']=records;clip['native_path']=None;manifest.write_bytes((json.dumps(m,indent=2)+'\n').encode())
 # The unsplit task-generated file is redundant only after all part pixels verify.
 assert source.resolve().parent==OUT.resolve();source.unlink()
 (OUT/(name+'_SPLIT_VERIFICATION.json')).write_bytes((json.dumps({'method':'Native cel copy preserving pixels, positions and timing; parsed RGBA every frame after native save','parts':records},indent=2)+'\n').encode())
 print('Split and verified',name,len(rows),'frames across',len(parts),'native documents',flush=True)
