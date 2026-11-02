"""Fetch every required file anonymously from an immutable GitHub revision."""
from pathlib import Path
import argparse
import concurrent.futures
import datetime
import hashlib
import json
import re
import time
import urllib.parse
import urllib.request

ROOT=Path(__file__).resolve().parents[1]
REPO=ROOT.parents[2]
ORIGIN='https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/'


def fetch(url, expected_size=None, expected_hash=None):
    for attempt in range(3):
        try:
            request=urllib.request.Request(url,headers={'User-Agent':'Roshan-Source-Integrity/1','Accept-Encoding':'identity'})
            digest=hashlib.sha256();count=0;chunks=[]
            with urllib.request.urlopen(request,timeout=120) as response:
                status=response.status
                while True:
                    data=response.read(1024*1024)
                    if not data:break
                    digest.update(data);count+=len(data)
                    if expected_size is None:chunks.append(data)
            assert status==200
            if expected_size is not None:assert count==expected_size,(url,'byte count',count,expected_size)
            if expected_hash is not None:assert digest.hexdigest()==expected_hash,(url,'hash mismatch')
            return {'status':status,'bytes':count,'sha256':digest.hexdigest()},b''.join(chunks)
        except Exception:
            if attempt==2:raise
            time.sleep(attempt+1)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--revision',required=True)
    parser.add_argument('--receipt',type=Path,required=True)
    args=parser.parse_args()
    assert re.fullmatch('[0-9a-f]{40}',args.revision),'Immutable full revision required'
    local=(ROOT/'manifest.json').read_bytes()
    name=(ROOT/'manifest.json').relative_to(REPO).as_posix()
    base=ORIGIN+args.revision+'/'
    manifest_fetch,remote=fetch(base+name,expected_hash=hashlib.sha256(local).hexdigest())
    manifest=json.loads(remote)
    def check(entry):
        result,_=fetch(base+urllib.parse.quote(entry['path'],safe='/'),entry['bytes'],entry['sha256'])
        return {'path':entry['path'],**result}
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        results=list(pool.map(check,manifest['required_files']))
    payload=''.join(f"{f['path']}\0{f['bytes']}\0{f['sha256']}\n" for f in sorted(results,key=lambda x:x['path'])).encode()
    assert hashlib.sha256(payload).hexdigest()==manifest['payload_sha256']
    receipt={'status':'REMOTE_SOURCE_PACKET_VERIFIED','revision':args.revision,
        'repository':'https://github.com/Ebonyks/mermaid-roshan-reef','branch':manifest['branch'],
        'access_mode':'Anonymous HTTPS to immutable raw GitHub revision; no Authorization header, cookies or GitHub credentials.',
        'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'manifest':{'path':name,**manifest_fetch},'payload_sha256':manifest['payload_sha256'],
        'required_file_count':len(results),'required_payload_bytes':sum(f['bytes'] for f in results),
        'all_required_files_verified':True,'files':results,
        'entry_url':'https://github.com/Ebonyks/mermaid-roshan-reef/tree/'+manifest['branch']+'/'+ROOT.relative_to(REPO).as_posix(),
        'immutable_tree_url':'https://github.com/Ebonyks/mermaid-roshan-reef/tree/'+args.revision+'/'+ROOT.relative_to(REPO).as_posix(),
        'direct_manifest_url':base+name,'master_audit_changed':False,'master_audit_writeback_authorized':False,
        'acceptance':'Integrity/access verification only. No human identity/style/natural-motion, device, child/owner, production or finding-closure acceptance.'}
    args.receipt.parent.mkdir(parents=True,exist_ok=True)
    args.receipt.write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8',newline='\n')
    print('ANONYMOUS_REMOTE_PACKET_VERIFIED',len(results),'files',receipt['required_payload_bytes'],'bytes',args.revision,flush=True)


if __name__=='__main__':main()
