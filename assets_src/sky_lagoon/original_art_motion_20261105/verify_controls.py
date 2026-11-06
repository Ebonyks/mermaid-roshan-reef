from pathlib import Path
from PIL import Image
import subprocess,json,hashlib
p=Path(__file__).resolve().parent
command=['python','-B',str(p/'verify_original.py')]
baseline=subprocess.run(command,capture_output=True,text=True,encoding='utf-8')
assert baseline.returncode==0,('Positive baseline must pass before corruption controls',baseline.stderr[-1000:])
results=[]
expected_messages={'non-original appearance pixel':'Runtime appearance differs','wrong original placement':'Unexpected target/placement','excessive sway':'Excessive motion requested','root support motion':'Root support field must be zero','incorrect GIF duration':'GIF timing differs','stale native playback evidence':'Stale native evidence'}
def check(name,files,mutate):
 backups={f:f.read_bytes() for f in files}
 try:
  mutate()
  run=subprocess.run(command,capture_output=True,text=True,encoding='utf-8')
  assert run.returncode!=0,('Corruption passed',name)
  details=(run.stderr+run.stdout).strip().splitlines()
  assert expected_messages[name] in '\n'.join(details),('Rejected for unrelated reason',name,details[-3:])
  results.append({'case':name,'result':'REJECTED_AS_REQUIRED','exit_code':run.returncode,'last_message':details[-1] if details else 'nonzero'})
 finally:
  for f,raw in backups.items():f.write_bytes(raw)
  assert all(hashlib.sha256(f.read_bytes()).digest()==hashlib.sha256(raw).digest() for f,raw in backups.items())
source=p/'demo_project/patches/lake_foxtails.png'
def poison_pixel():
 im=Image.open(source).convert('RGB');im.putpixel((10,10),(255,0,255));im.save(source)
check('non-original appearance pixel',[source],poison_pixel)
target=p/'demo_project/targets.json'
def bad_position():
 d=json.loads(target.read_text(encoding='utf-8'));d[0]['xy'][0]-=16;target.write_text(json.dumps(d),encoding='utf-8')
check('wrong original placement',[target],bad_position)
def bad_motion():
 d=json.loads(target.read_text(encoding='utf-8'));d[0]['amplitude']=12;target.write_text(json.dumps(d),encoding='utf-8')
check('excessive sway',[target],bad_motion)
fields=[p/'fields/lake_foxtails.png',p/'demo_project/patches/lake_foxtails_field.png']
def bad_root():
 for f in fields:
  im=Image.open(f).convert('L');im.putpixel((200,490),255);im.save(f)
check('root support motion',[*fields],bad_root)
gif=p/'lake_foxtails.gif'
def bad_delay():
 raw=bytearray(gif.read_bytes());index=raw.index(b'\x21\xf9\x04');raw[index+4]=10;raw[index+5]=0;gif.write_bytes(raw)
check('incorrect GIF duration',[gif],bad_delay)
shader=p/'demo_project/breeze.gdshader'
def stale_runtime():shader.write_bytes(shader.read_bytes()+b'\n// corruption control: evidence must not transfer\n')
check('stale native playback evidence',[shader],stale_runtime)
(p/'evidence/negative-controls.json').write_text(json.dumps({'status':'PASS','positive_baseline':'PASS before all mutations','cases':results,'restoration':'Every mutated derivative restored byte-for-byte in finally; protected master never modified.'},indent=2)+'\n',encoding='utf-8')
print(json.dumps(results,indent=2))
