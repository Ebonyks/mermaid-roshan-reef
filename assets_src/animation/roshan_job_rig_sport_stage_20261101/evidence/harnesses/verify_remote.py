from pathlib import Path
import urllib.request,urllib.parse,hashlib,json,sys,datetime,concurrent.futures,time
R=Path(__file__).resolve().parents[2];repo='Ebonyks/mermaid-roshan-reef';revision=sys.argv[1];assert len(revision)==40 and all(c in '0123456789abcdef' for c in revision);prefix=R.relative_to(R.parents[2]).as_posix();base='https://raw.githubusercontent.com/'+repo+'/'+revision+'/'
def fetch(path):
 url=base+urllib.parse.quote(path,safe='/');request=urllib.request.Request(url,headers={'User-Agent':'MermaidRoshan-SourcePacket-Verify/1.0'})
 for attempt in range(3):
  try:
   with urllib.request.urlopen(request,timeout=90) as response:return response.read(),response.status,url
  except Exception:
   if attempt==2:raise
   time.sleep(attempt+1)
data,status,url=fetch(prefix+'/MANIFEST.json');local=(R/'MANIFEST.json').read_bytes();assert data==local,'Remote manifest differs from sealed local manifest';manifest=json.loads(data);rows=[]
def one(row):
 try:
  data,status,url=fetch(row['path']);digest=hashlib.sha256(data).hexdigest();return {'path':row['path'],'url':url,'status':status,'bytes':len(data),'sha256':digest,'expected_sha256':row['sha256'],'pass':status==200 and len(data)==row['bytes'] and digest==row['sha256']}
 except Exception as e:return {'path':row['path'],'pass':False,'error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
 for row in executor.map(one,manifest['files']):rows.append(row)
payload=''.join(x['sha256']+'  '+x['path']+'\n' for x in manifest['files']).encode();result={'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'repository':repo,'revision':revision,'access_mode':'anonymous HTTPS; new urllib requests, no Authorization header, cookies or account session','manifest_url':url,'manifest_sha256':hashlib.sha256(data).hexdigest(),'packet_payload_sha256':hashlib.sha256(payload).hexdigest(),'payload_digest_matches_manifest':hashlib.sha256(payload).hexdigest()==manifest['packet_payload_sha256'],'files_checked':len(rows),'files':rows,'pass':all(x['pass'] for x in rows) and hashlib.sha256(payload).hexdigest()==manifest['packet_payload_sha256'],'acceptance':'Remote byte/access proof only. Source attachment/mixed-fit/restoration, human/owner/device/child and corrected upstream-baseline gates remain separately blocking.'};(R/'evidence/remote_verification.json').write_bytes((json.dumps(result,indent=2)+'\n').encode());print('ANONYMOUS_REMOTE_VERIFY',len(rows),result['pass']);raise SystemExit(0 if result['pass'] else 1)
