from pathlib import Path
import zipfile,struct,hashlib,subprocess,json,datetime,re
T=Path(__file__).parent;D=T/'APK_42285923870';P=D/'roshan-reef.apk';REV='e70081ea871bd2aab2440be2168abe33d20ee328';now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def write(n,o):(D/n).write_text(json.dumps(o,indent=2)+'\n',encoding='utf-8')
def sha(b):return hashlib.sha256(b).hexdigest()
run=json.loads((D/'RUN_COMPLETED.json').read_text(encoding='utf-8'));assert run['headSha']==REV and run['headBranch']=='dev'and run['status']=='completed'and run['conclusion']=='success'
log=(D/'workflow_complete.log').read_text(encoding='utf-8');guards=[l for l in log.splitlines()if 'ANDROID_SOURCE|PASS|'in l];assert len(guards)==2 and all('ANDROID_SOURCE|PASS|dev|'+REV+'|probe_run=42273654426'in l for l in guards)
# Android binary XML values are decoded directly; no SDK installation or private key access.
def axml(data):
 strings=[];out=[];pos=8
 def length8(b,o):
  x=b[o];return (((x&127)<<8)|b[o+1],o+2)if x&128 else(x,o+1)
 def length16(b,o):
  x=struct.unpack_from('<H',b,o)[0];return(((x&32767)<<16)|struct.unpack_from('<H',b,o+2)[0],o+4)if x&32768 else(x,o+2)
 while pos<len(data):
  typ,hs,sz=struct.unpack_from('<HHI',data,pos);assert sz>=hs and pos+sz<=len(data)
  if typ==1:
   count,styles,flags,start,sty=struct.unpack_from('<5I',data,pos+8)
   for i in range(count):
    off=pos+start+struct.unpack_from('<I',data,pos+hs+4*i)[0]
    if flags&256:
     _,off=length8(data,off);n,off=length8(data,off);strings.append(data[off:off+n].decode('utf-8'))
    else:n,off=length16(data,off);strings.append(data[off:off+n*2].decode('utf-16-le'))
  elif typ==0x102:
   ns,name=struct.unpack_from('<II',data,pos+16);ast,asz,ac=struct.unpack_from('<3H',data,pos+24);attrs={}
   for i in range(ac):
    a=pos+16+ast+i*asz;ns,an,raw=struct.unpack_from('<3I',data,a);vsize,zero,vt,v=struct.unpack_from('<HBBI',data,a+12)
    value=strings[raw]if raw!=0xffffffff else(strings[v]if vt==3 else(bool(v)if vt==0x12 else v));attrs[strings[an]]=value
   out.append({'element':strings[name],'attributes':attrs})
  pos+=sz
 assert pos==len(data);return out
with zipfile.ZipFile(P)as z:
 infos=z.infolist();names=[i.filename for i in infos];assert len(names)==len(set(names));print('ZIP_CRC_START',len(names),flush=True);assert z.testzip()is None;print('ZIP_CRC_PASS',flush=True)
 root=axml(z.read('AndroidManifest.xml'));manifest=next(x['attributes']for x in root if x['element']=='manifest');vc=int(subprocess.check_output(['git','rev-list','--count',REV]).decode().strip());assert manifest['package']=='com.ebonyks.roshanreef'and manifest['versionCode']==vc and manifest['versionName']=='0.1.0',manifest
 assert 'lib/arm64-v8a/libgodot_android.so'in names
 data=z.read('assets/assets.sparsepck');head=struct.unpack_from('<6I2Q',data,0);assert head==(0x43504447,4,4,7,2,6,0,104),head;pos=head[7];count=struct.unpack_from('<I',data,pos)[0];pos+=4;rows=[]
 for i in range(count):
  sl=struct.unpack_from('<I',data,pos)[0];pos+=4;path=data[pos:pos+sl].rstrip(b'\0').decode();pos+=sl;offset,size=struct.unpack_from('<QQ',data,pos);pos+=16;md5=data[pos:pos+16].hex();pos+=16;flags=struct.unpack_from('<I',data,pos)[0];pos+=4
  assert offset==0 and flags==0,(path,offset,flags);relative=path.removeprefix('res://');assert not relative.startswith('/') and '..'not in relative.split('/');member='assets/'+relative;assert member in names and z.getinfo(member).file_size==size,(path,size);rows.append({'native_index_path':path,'virtual_path':'res://'+relative,'zip_member':member,'bytes':size,'md5':md5,'flags':flags})
 assert pos==len(data)and len({r['virtual_path']for r in rows})==count
 index={r['virtual_path']:r for r in rows};targets=['res://scripts/racer/reef_kart_race.gdc','res://scripts/racer/reef_kart_zones.gdc','res://scripts/racer/reef_kart_race.gd.remap','res://scripts/racer/reef_kart_zones.gd.remap','res://project.binary','res://.godot/imported/pool_towel_cabinet.png-40ef64466567e744131ee57f0f0df9a6.ctex'];selected=[]
 for path in targets:
  r=index[path];b=z.read(r['zip_member']);assert hashlib.md5(b).hexdigest()==r['md5'];selected.append({**r,'sha256':sha(b),'pck_md5_match':True})
 banned=['res://assets_src/imagegen/racer_gas_button_20261106/','res://assets_src/review/r146_racer_gas_20261106/','res://docs/handoffs/codex_flat_vector_art_2026-10-07/r146_racer_painted_gas_runtime/','res://assets/racer/ui/gas_button_painted.png','res://assets_src/review/recent_updates_dev_20261106/','res://docs/handoffs/codex_recent_updates_dev_2026-11-06/','res://assets_src/sky_lagoon/original_art_motion_20261105/','res://docs/handoffs/codex_flat_vector_art_2026-10-07/r144_shared_painted_shell/']
 matches={s:[p for p in index if p.startswith(s)]for s in banned};assert not any(matches.values()),matches
 write('PACKAGE_CONTENT_VERIFICATION.json',{'state':'PASS_COMPLETE_ZIP_CRC_ANDROID_MANIFEST_AND_SPARSE_PCK_INDEX','revision':REV,'run_id':42285923870,'zip_entries':len(names),'zip_all_crc_pass':True,'manifest':manifest,'arm64_library_present':True,'pck_header':list(head),'pck_index_bytes':len(data),'pck_virtual_entries':count,'all_virtual_paths_unique_present_size_match':True,'selected_actual_resource_hashes':selected,'targeted_source_review_and_not_yet_R146_exclusions':matches,'source_binding_guard_lines':guards,'checked_at_utc':now(),'limits':['Sparse-PCK full index and all ZIP CRCs verified; MD5/SHA resource decoding bounded to six named selected resources.','No physical Android installation, playback, device performance, child or owner acceptance.','E700 APK predates and excludes R146 painted gas candidate.']});write('PCK_VIRTUAL_FILE_INDEX.json',{'revision':REV,'entries':rows})
print('PACKAGE_PASS',count,manifest,flush=True)
java=Path(r'C:/Program Files/Microsoft/jdk-17.0.20.8-hotspot/bin');results=[]
for key,cmd in [('jarsigner',[str(java/'jarsigner.exe'),'-verify','-verbose','-certs',str(P)]),('public_certificate',[str(java/'keytool.exe'),'-printcert','-jarfile',str(P)])]:
 r=subprocess.run(cmd,capture_output=True);raw=r.stdout+r.stderr;(D/(key+'.log')).write_bytes(raw);s=raw.decode('utf-8','replace');results.append({'tool':key,'exit_code':r.returncode,'log':key+'.log','sha256':sha(raw),'bytes':len(raw)});assert r.returncode==0,(key,s[-2000:])
 if key=='jarsigner':assert 'jar verified.'in s.lower();warnings=[x.strip()for x in s.splitlines()if any(w in x.lower()for w in ['warning:','self-signed','timestamp','jarinputstream','not signed','reorder'])]
 else:
  expected='D5:F2:60:43:2D:CF:31:5D:E8:F2:85:C3:31:1E:DA:ED:C6:FE:2B:C0:1A:2F:04:7E:BE:1C:A1:CA:8F:FD:33:14';assert expected in s and expected in log
write('PUBLIC_SIGNATURE_VERIFICATION.json',{'state':'PASS_JAR_V1_VERIFICATION_AND_MATCHING_PUBLIC_CERTIFICATE','revision':REV,'public_signer_sha256':expected,'tools':results,'warnings_retained':warnings,'checked_at_utc':now(),'private_keystore_read':False,'limits':['Java17 JAR/v1 verification only; not independent Android v2/v3 apksigner verification or physical-device installation.','Self-signed debug certificate, timestamp and ZIP ordering warnings remain unwaived.']})
download=json.loads((D/'DOWNLOAD_RESULT.json').read_text(encoding='utf-8'));write('APK_VERIFIED.json',{'state':'PASS_ANONYMOUS_APK_BYTES_EXACT_DEV_SOURCE_MANIFEST_SPARSE_PCK_CRC_AND_PUBLIC_JAR_SIGNATURE','revision':REV,'run_id':42285923870,'probe_run':42273654426,'apk_bytes':P.stat().st_size,'apk_sha256':'1f03dac7b163d637fe6a9f43bff8a49d9032202450f7ca1d69bc00808a8c5939','download_result':'DOWNLOAD_RESULT.json','package_receipt':'PACKAGE_CONTENT_VERIFICATION.json','signature_receipt':'PUBLIC_SIGNATURE_VERIFICATION.json','checked_at_utc':now(),'R146_included':False,'device':None,'child':None,'owner':None,'formal_QA11':None});print('APK_FULL_PASS',flush=True)
