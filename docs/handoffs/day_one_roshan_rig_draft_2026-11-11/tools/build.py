import json,sys,hashlib,zipfile
src,anims,out=sys.argv[1:4]
zin=zipfile.ZipFile(src)
project=json.loads(zin.read('project.json'))
project['animations']=[a for a in project['animations'] if not a['name'].startswith('D1 ')]+json.load(open(anims))
with zipfile.ZipFile(out,'w') as zout:
    for info in zin.infolist():
        data=zin.read(info.filename)
        if info.filename=='project.json': data=json.dumps(project,separators=(',',':')).encode()
        zout.writestr(info.filename,data,compress_type=info.compress_type)
a,b=zipfile.ZipFile(src),zipfile.ZipFile(out)
assert a.namelist()==b.namelist()
for n in a.namelist():
    if n!='project.json': assert hashlib.sha256(a.read(n)).digest()==hashlib.sha256(b.read(n)).digest(),n
old=json.loads(a.read('project.json')); new=json.loads(b.read('project.json'))
for k in old:
    if k!='animations': assert old[k]==new[k],k
assert new['animations'][:len(old['animations'])]==old['animations']
print('source sha256',hashlib.sha256(open(src,'rb').read()).hexdigest())
print('output sha256',hashlib.sha256(open(out,'rb').read()).hexdigest())
print('animations',len(old['animations']),'->',len(new['animations']),'; textures, bones, slots, skins, weights byte-identical')
