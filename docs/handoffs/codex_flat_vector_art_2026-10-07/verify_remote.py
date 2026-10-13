"""Verify every required immutable GitHub byte anonymously;write a separate delivery receipt."""
from pathlib import Path
import argparse,concurrent.futures,datetime,hashlib,json,subprocess,urllib.request,urllib.parse,time
P=Path(__file__).resolve().parent;R=P.parents[2];REPO='Ebonyks/mermaid-roshan-reef'
def sha(b):return hashlib.sha256(b).hexdigest()
def request(url):
 with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'MermaidRoshan-R6-byte-verification'}),timeout=60) as response:
  if response.status!=200:raise ValueError('HTTP '+str(response.status))
  return response.read()
def verify(row):
 url='https://raw.githubusercontent.com/'+REPO+'/'+row['revision']+'/'+urllib.parse.quote(row['path'],safe='/')
 error=None
 for attempt in range(3):
  try:
   raw=request(url)
   if len(raw)!=row['bytes'] or sha(raw)!=row['sha256']:raise ValueError('literal byte/SHA mismatch')
   return {**row,'url':url,'http_status':200,'anonymous_bytes_verified':True}
  except Exception as exc:error=str(exc)
 raise ValueError(row['path']+':'+str(error))
def main():
 a=argparse.ArgumentParser();a.add_argument('--revision',required=True);a.add_argument('--workers',type=int,default=12);args=a.parse_args()
 if len(args.revision)!=40 or any(c not in '0123456789abcdef' for c in args.revision):raise ValueError('exact immutable revision required')
 local=(P/'MANIFEST.json').read_bytes();rel=P.relative_to(R).as_posix();remote=request('https://raw.githubusercontent.com/'+REPO+'/'+args.revision+'/'+rel+'/MANIFEST.json')
 if remote!=local:raise ValueError('manifest bytes differ')
 m=json.loads(remote);rows=[{**x,'path':rel+'/'+x['path'],'revision':args.revision,'lane':'packet'} for x in m['packet_files']]
 rows +=[{**x,'lane':'historical-native'} for x in m['historical_required_files']]
 rows +=[{**x,'lane':'source-provenance'} for x in m['immutable_source_files']]
 rows +=[{**x,'revision':args.revision,'lane':'project-authority'} for x in m['required_project_files']]
 if len({(x['revision'],x['path']) for x in rows})!=len(rows):raise ValueError('duplicate verification target')
 started=datetime.datetime.now(datetime.timezone.utc).isoformat();done=[]
 with concurrent.futures.ThreadPoolExecutor(max_workers=min(16,max(1,args.workers))) as pool:
  for index,result in enumerate(pool.map(verify,rows),1):
   done.append(result)
   if index%100==0:print('REMOTE',index,'/',len(rows),flush=True)
 repo=json.loads(subprocess.check_output(['gh','api','repos/'+REPO],cwd=R,text=True));access=json.loads(subprocess.check_output(['gh','api','repos/'+REPO+'/collaborators/Ebonyks/permission'],cwd=R,text=True))
 if repo['private'] or access.get('permission') not in ['admin','write','maintain']:raise ValueError('required public/owner access mode unavailable')
 receipt={'schema':'reef.remote_verification/2','revision':args.revision,'request_id':m['revision'],'repository':'https://github.com/'+REPO,'branch':m['branch'],'manifest_path':rel+'/MANIFEST.json','manifest_sha256':sha(remote),'payload_sha256':m['payload_sha256'],'started_at_utc':started,'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_EVERY_REQUIRED_BYTE_ANONYMOUSLY_VERIFIED','access_mode':'Public unauthenticated immutable raw HTTP200; owner Ebonyks API permission '+access['permission'],'repo_private':repo['private'],'required_file_count':len(done),'required_bytes':sum(x['bytes'] for x in done),'checks':done,'creative_acceptance':False,'device_child_owner_acceptance':False,'note':'Payload publication is separate from acceptance. This receipt is post-publication;fetch its own exact commit before claiming the receipt delivered.'}
 (P/'REMOTE_VERIFICATION.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n');print('REMOTE|ALL OK|',len(done),'files',receipt['required_bytes'],'bytes',args.revision,flush=True)
if __name__=='__main__':main()
