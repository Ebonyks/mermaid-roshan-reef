from pathlib import Path
import argparse,json,hashlib,urllib.request,urllib.parse,concurrent.futures,time,datetime,re
def digest(b):return hashlib.sha256(b).hexdigest()
def fetch(url):
 errors=[]
 for attempt in range(4):
  try:
   with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mermaid-Roshan-evidence-verifier','Accept':'application/vnd.github+json'if'api.github.com'in url else'*/*'}),timeout=60)as response:
    data=response.read();assert response.status==200;return data
  except Exception as e:
   errors.append(type(e).__name__+': '+str(e))
   if attempt<3:time.sleep(1+attempt)
 raise RuntimeError(url+' '+str(errors))
def rawurl(rev,path):
 assert re.fullmatch('[0-9a-f]{40}',rev),rev
 assert path and not path.startswith(('/','\\'))and'..'not in path.split('/')and'://'not in path,path
 return 'https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/'+rev+'/'+urllib.parse.quote(path,safe='/')
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--revision',required=True);ap.add_argument('--manifest',required=True);ap.add_argument('--out',required=True);ap.add_argument('--expected-manifest-sha256',required=True);args=ap.parse_args()
 repo=json.loads(fetch('https://api.github.com/repos/Ebonyks/mermaid-roshan-reef'));assert repo['private']is False and repo['full_name']=='Ebonyks/mermaid-roshan-reef'
 payload=fetch(rawurl(args.revision,args.manifest));assert digest(payload)==args.expected_manifest_sha256;manifest=json.loads(payload);assert manifest['schema']=='reef.runtime_trial_delivery/1'
 def one(row):
  rev=row.get('revision')or args.revision;data=fetch(rawurl(rev,row['path']));assert len(data)==row['bytes']and digest(data)==row['sha256'],row['path'];return {'revision':rev,'path':row['path'],'bytes':len(data),'sha256':digest(data),'http_status':200,'verified':True}
 with concurrent.futures.ThreadPoolExecutor(max_workers=6)as pool:rows=list(pool.map(one,manifest['files']))
 out={'schema':'reef.remote_delivery_verification/1','revision':args.revision,'repository':'Ebonyks/mermaid-roshan-reef','public_repository_api_verified':True,'manifest':args.manifest,'manifest_sha256':digest(payload),'manifest_bytes':len(payload),'required_files':len(rows),'required_bytes':sum(x['bytes']for x in rows),'files':rows,'access_mode':'Anonymous HTTPS GET; no authentication. Exact immutable commit, byte length and SHA-256 for every declared required file and manifest.','checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'state':'ALL_REQUIRED_FILES_ANONYMOUSLY_BYTE_VERIFIED','limits':'Transport/provenance receipt only; no image, runtime, device, child, owner or release acceptance. Receipt own metadata is verified separately after its commit.'}
 Path(args.out).write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n');print('REMOTE_VERIFIED',args.revision,len(rows),out['required_bytes'],out['checked_at_utc'],flush=True)
if __name__=='__main__':main()
