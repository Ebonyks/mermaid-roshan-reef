from pathlib import Path
import urllib.request,urllib.parse,concurrent.futures,json,hashlib,datetime
R=Path(__file__).resolve().parents[2];rev='cbf8b5b6f9ff4313202d74ca1eafc4ba914bd539';prefix='assets_src/animation/native_rig_costumes_20261031/replacement_v6/';base='https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/'+rev+'/'
def fetch(p):
 u=base+urllib.parse.quote(p,safe='/');q=urllib.request.Request(u,headers={'User-Agent':'MermaidRoshan-SeedVerify/1.0'})
 with urllib.request.urlopen(q,timeout=120) as resp:return resp.read(),resp.status,u
blob,status,url=fetch(prefix+'seed_manifest.json');d=json.loads(blob);rows=[]
def one(x):
 try:
  data,status,u=fetch(x['path']);h=hashlib.sha256(data).hexdigest();return {'path':x['path'],'url':u,'status':status,'sha256':h,'expected_sha256':x['sha256'],'bytes':len(data),'expected_bytes':x['bytes'],'pass':status==200 and h==x['sha256'] and len(data)==x['bytes']}
 except Exception as e:return {'path':x['path'],'pass':False,'error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:rows=list(pool.map(one,d['required_files']))
hashes={x['sha256']:[y['path'] for y in d['required_files'] if y['sha256']==x['sha256']] for x in d['required_files']};local=[]
for p in sorted((R/'seed').rglob('*')):
 if not p.is_file() or p.suffix=='.uid':continue
 h=hashlib.sha256(p.read_bytes()).hexdigest();local.append({'local_path':p.relative_to(R).as_posix(),'sha256':h,'matching_published_paths':hashes.get(h,[]),'exact_content_found':h in hashes,'input_kind':'render_input' if p.parent.name=='art' or p.name in ['rig.json','study.gd','costume.gdshader','costumes.json'] else 'provenance_metadata'})
result={'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'revision':rev,'manifest_url':url,'manifest_sha256':hashlib.sha256(blob).hexdigest(),'access':'anonymous HTTPS; no Authorization header, cookies or account session','candidate':d['candidate'],'parent_status':d['status'],'files':rows,'required_files_checked':len(rows),'remote_required_bytes_pass':all(x['pass'] for x in rows),'local_seed_comparison':local,'local_render_input_match':all(x['exact_content_found'] for x in local if x['input_kind']=='render_input'),'pass':all(x['pass'] for x in rows) and all(x['exact_content_found'] for x in local if x['input_kind']=='render_input'),'limits':d['limits'],'scope':'Corrected replacement architecture source baseline only. Does not accept mixed waist, our new actions, shared join, human/device/child/owner or production adoption.'};(R/'evidence/upstream_seed_remote_verification.json').write_bytes((json.dumps(result,indent=2)+'\n').encode());print('UPSTREAM_SEED_VERIFY',len(rows),result['remote_required_bytes_pass'],result['local_render_input_match'],flush=True)
