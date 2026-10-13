"""Anonymous byte verification of every declared R7 dependency at exact revisions."""
from pathlib import Path
import json,hashlib,urllib.request,concurrent.futures,argparse,datetime,time,subprocess
P=Path(__file__).resolve().parent;R=P.parents[3]
def sha(b):return hashlib.sha256(b).hexdigest()
a=argparse.ArgumentParser();a.add_argument("--revision",required=True);args=a.parse_args();m=json.loads((P/"MANIFEST.json").read_text(encoding="utf-8"));revision=args.revision
manifest_path=(P/"MANIFEST.json").relative_to(R).as_posix();start=datetime.datetime.now(datetime.timezone.utc).isoformat()
def fetch(url):
 for attempt in range(3):
  try:
   with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"MermaidRoshan-R7-public-evidence"}),timeout=60) as q:return q.status,q.read()
  except Exception:
   if attempt==2:raise
   time.sleep(1)
url="https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/"+revision+"/"+manifest_path;status,raw=fetch(url);assert status==200 and raw==(P/"MANIFEST.json").read_bytes()
def check(x):
 rev=x["revision"] or revision;u="https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/"+rev+"/"+x["path"];status,b=fetch(u);assert status==200 and len(b)==x["bytes"] and sha(b)==x["sha256"],u;return dict(x,verified_revision=rev,http_status=status,url=u)
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:checks=list(pool.map(check,m["files"]))
repo=json.loads(fetch("https://api.github.com/repos/Ebonyks/mermaid-roshan-reef")[1]);assert repo["private"] is False
receipt={"schema":"reef.flat_vector_delta_receipt/1","status":"ALL_DECLARED_DEPENDENCIES_VERIFIED","revision":revision,"manifest_path":manifest_path,"manifest_sha256":sha(raw),"payload_sha256":m["payload_sha256"],"required_file_count":len(checks),"required_bytes":sum(x["bytes"] for x in checks),"started_at_utc":start,"checked_at_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"access_mode":"Anonymous public HTTPS for manifest and every declared required file; public GitHub repo API independently checked; recipient can use the same unauthenticated access mode.","repo_private":False,"checks":checks,"entry_url":"https://github.com/Ebonyks/mermaid-roshan-reef/blob/"+revision+"/"+(P/"README.md").relative_to(R).as_posix(),"immutable_tree_url":"https://github.com/Ebonyks/mermaid-roshan-reef/tree/"+revision+"/"+P.relative_to(R).as_posix(),"direct_manifest_url":url,"creative_acceptance":False,"accepted_removed":0,"mission_complete":False}
(P/"REMOTE_VERIFICATION.json").write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8",newline="\n");print("R7 REMOTE VERIFIED",len(checks),receipt["required_bytes"],receipt["manifest_sha256"])
