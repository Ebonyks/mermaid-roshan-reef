"""Packet manifest: path, role, bytes, SHA-256 (+ image size) for every committed packet file; sorted payload hash."""
import sys,os,hashlib,json; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from paths import *
from PIL import Image
ROLE=[('frames/native/','runtime-candidate whole frame (256 px cell, straight-alpha RGBA); reference-only until accepted'),
      ('wave_master.aseprite','editable master: one whole cel per frame, 24 fps beat tags'),
      ('review/','viewing copy of the same animation (lossy video or GIF)'),('data/','pipeline data (annotations, correspondences, fits, sources)'),
      ('scripts/','reproducible pipeline source'),('README.md','packet guide'),('JOB_CARD.md','animation job card V1'),
      ('verification.json','machine check results'),('.g','repository/engine housekeeping')]
rows=[]
for dp,dn,fn in os.walk(PKT):
    dn[:]=[d for d in dn if d!='__pycache__']
    for f in sorted(fn):
        p=os.path.join(dp,f); rel=os.path.relpath(p,PKT).replace(os.sep,'/')
        if rel=='manifest.json' or f.endswith('.pyc'): continue
        b=open(p,'rb').read(); r={'path':rel,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),
           'role':next((v for k,v in ROLE if rel.startswith(k)),'other')}
        if f.endswith('.png') or f.endswith('.gif'):
            with Image.open(p) as im: r['dimensions']=list(im.size); r['mode']=im.mode
        rows.append(r)
rows.sort(key=lambda r:r['path'])
payload=hashlib.sha256(''.join('%s\t%s\n'%(r['path'],r['sha256']) for r in rows).encode()).hexdigest()
json.dump({'packet':os.path.basename(PKT),'status':'REFERENCE_ONLY',
  'sources':{'atlas':'assets/characters/roshan_25d/roshan_gesture_a.png','atlas_sha256':ATLAS_SHA256,'atlas_cells':'row 0, columns 0-3 (K0 rest, K1 hand at shoulder, K2 overhead, K3 lowering)'},
  'payload_sha256_method':'sha256 of sorted lines "path<TAB>sha256\\n" over files below (manifest.json excluded)',
  'payload_sha256':payload,'file_count':len(rows),'files':rows},open(os.path.join(PKT,'manifest.json'),'w'),indent=1)
print('manifest: %d files, payload %s'%(len(rows),payload))
