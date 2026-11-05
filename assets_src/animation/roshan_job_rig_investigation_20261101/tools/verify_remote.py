"""Anonymous exact-revision byte verification; does not use Codex credentials."""
from pathlib import Path
import subprocess,sys,json,hashlib,urllib.request,urllib.parse,datetime,concurrent.futures,time
R=Path(__file__).resolve().parents[1];PREFIX=R.relative_to(R.parents[2]).as_posix();REV=sys.argv[1]
REPORT=Path(sys.argv[2]) if len(sys.argv)>2 else R/'evidence/remote_verification.json'
BASE='https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/'+REV+'/'
def fetch(path):
    for attempt in range(3):
        try:
            response=urllib.request.urlopen(urllib.request.Request(BASE+urllib.parse.quote(path,safe='/'),headers={'User-Agent':'Codex-anonymous-packet-verifier','Accept-Encoding':'identity'}),timeout=180)
            digest=hashlib.sha256();count=0
            while True:
                chunk=response.read(1024*1024)
                if not chunk:break
                digest.update(chunk);count+=len(chunk)
            return {'path':path,'sha256':digest.hexdigest(),'bytes':count,'status':response.status,'access_mode':'anonymous HTTPS; no auth header/token'}
        except Exception:
            if attempt==2:raise
            time.sleep(2)
def main():
    manifest_path=PREFIX+'/manifest.json';raw=urllib.request.urlopen(urllib.request.Request(BASE+manifest_path,headers={'User-Agent':'Codex-anonymous-packet-verifier'}),timeout=60).read();manifest=json.loads(raw)
    rows=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        for expected,actual in zip(manifest['files'],pool.map(fetch,[x['path'] for x in manifest['files']])):
            actual['matches']=actual['sha256']==expected['sha256'] and actual['bytes']==expected['bytes'];rows.append(actual)
            if len(rows)%40==0:print('REMOTE_VERIFIED',len(rows),flush=True)
    metadata=[]
    for name in manifest['metadata_files_outside_payload_hash']:
        if name=='manifest.json':continue
        p=R/name;actual=fetch(PREFIX+'/'+name);actual['matches']=actual['sha256']==hashlib.sha256(p.read_bytes()).hexdigest();metadata.append(actual)
    root_files=[]
    for name in ['ASSET_LICENSES.md','audit/MASTER_AUDIT_2026-08-09.md','audit/MASTER_AUDIT_CHANGELOG_ROLLBACK_2026-08-10.md','design/05_DOC_LEDGER.md','design/audit_impacts/roshan-job-rig-investigation-20261101.json']:
        actual=fetch(name);actual['matches']=actual['sha256']==hashlib.sha256(subprocess.run(['git','show',REV+':'+name],cwd=R.parents[2],capture_output=True,check=True).stdout).hexdigest();root_files.append(actual)
    report={'required_repository_files':root_files,'revision':REV,'repository':'Ebonyks/mermaid-roshan-reef','check_time_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'access_mode':'anonymous public HTTPS; no credentials supplied','manifest_url':BASE+manifest_path,'manifest_sha256':hashlib.sha256(raw).hexdigest(),'sorted_packet_payload_sha256':manifest['sorted_packet_payload_sha256'],'files':rows,'metadata_files':metadata,'all_literal_bytes_match':all(x['matches'] for x in rows+metadata+root_files),'scope':'Archive review publication only; no compatible wardrobe, generation readiness or delivery acceptance.'}
    REPORT.write_text(json.dumps(report,indent=2)+'\n');print('REMOTE_RECEIPT',len(rows),report['all_literal_bytes_match']);raise SystemExit(0 if report['all_literal_bytes_match'] else 1)
if __name__=='__main__':main()
