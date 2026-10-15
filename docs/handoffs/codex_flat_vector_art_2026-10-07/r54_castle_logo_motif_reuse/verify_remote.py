from pathlib import Path
import json,hashlib,urllib.request,concurrent.futures,argparse,datetime,time,importlib.util
P=Path(__file__).resolve().parent;R=P.parents[3]
s=importlib.util.spec_from_file_location("bounded50remote",P/"bounded_json.py");A=importlib.util.module_from_spec(s);s.loader.exec_module(A)
def sha(b):return hashlib.sha256(b).hexdigest()
ap=argparse.ArgumentParser();ap.add_argument("--revision",required=True);revision=ap.parse_args().revision;start=datetime.datetime.now(datetime.timezone.utc).isoformat()
def fetch(u):
 for attempt in range(3):
  try:
   with urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":"MermaidRoshan-R54-public-audit-evidence"}),timeout=60)as q:return q.status,q.read()
  except Exception:
   if attempt==2:raise
   time.sleep(1)
def verify_manifest_file(path):
 u="https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/"+revision+"/"+path.relative_to(R).as_posix();status,b=fetch(u);assert status==200 and b==path.read_bytes();return {"path":path.relative_to(R).as_posix(),"revision":revision,"bytes":len(b),"sha256":sha(b),"http_status":status,"url":u}
manifest_path=P/"MANIFEST.json";manifest_checks=[verify_manifest_file(manifest_path)];idx=json.loads(manifest_path.read_text(encoding="utf-8"))
if idx.get("schema")==A.INDEX_SCHEMA:manifest_checks.extend(verify_manifest_file(P/x["path"])for x in idx["fragments"])
m=A.read_document(manifest_path)
def check(x):
 rev=x["revision"]or revision;u="https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/"+rev+"/"+x["path"];status,b=fetch(u);assert status==200 and len(b)==x["bytes"]and sha(b)==x["sha256"],u;return dict(x,verified_revision=rev,http_status=status,url=u)
with concurrent.futures.ThreadPoolExecutor(max_workers=10)as pool:
 checks=[]
 for i,row in enumerate(pool.map(check,m["files"]),1):
  checks.append(row)
  if i%500==0:print("R54_ANONYMOUS_FILES_VERIFIED",i,flush=True)
repo=json.loads(fetch("https://api.github.com/repos/Ebonyks/mermaid-roshan-reef")[1]);assert repo["private"]is False
receipt={"schema":"reef.flat_vector_delta_receipt/1","status":"ALL_DECLARED_DEPENDENCIES_VERIFIED","revision":revision,"manifest_path":manifest_path.relative_to(R).as_posix(),"manifest_sha256":sha(manifest_path.read_bytes()),"manifest_logical_sha256":sha(A.logical_bytes(manifest_path)),"manifest_files_verified":manifest_checks,"payload_sha256":m["payload_sha256"],"required_file_count":len(checks),"required_bytes":sum(x["bytes"]for x in checks),"checks":checks,"started_at_utc":start,"checked_at_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"access_mode":"Anonymous public immutable HTTPS GET for every required file plus manifest index/allparts; exact byte/length/SHA256. Public repo API independently checked.","repo_private":False,"entry_url":"https://github.com/Ebonyks/mermaid-roshan-reef/blob/"+revision+"/"+(P/"README.md").relative_to(R).as_posix(),"immutable_tree_url":"https://github.com/Ebonyks/mermaid-roshan-reef/tree/"+revision+"/"+P.relative_to(R).as_posix(),"direct_manifest_url":manifest_checks[0]["url"],"audited_source_revision":m["audited_source_revision"],"creative_acceptance":False,"accepted_removed":0,"mission_complete":False};A.write_document(P/"REMOTE_VERIFICATION.json",receipt);print("R54_REMOTE_VERIFIED",len(checks),receipt["required_bytes"],receipt["manifest_sha256"],flush=True)
