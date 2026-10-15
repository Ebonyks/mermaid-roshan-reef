from pathlib import Path
import json,hashlib,subprocess,importlib.util
P=Path(__file__).resolve().parent;R=P.parents[3];H=P.parent;O=H/"r49_callback_value_domains";B="4c5c026fd4a3c1ffaded5f13a123a28a2e13f677";D="5120b6d59885dd057937aaf284e73681d8eac9f5"
s=importlib.util.spec_from_file_location("bounded50manifest",P/"bounded_json.py");A=importlib.util.module_from_spec(s);s.loader.exec_module(A)
def rd(p):return A.read_document(p)
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(["git",*a],cwd=R,stderr=subprocess.PIPE)
rows={}
def add(path,rev=None,role="R50 source evidence; all art/runtime acceptance open"):
 b=(R/path).read_bytes()if rev is None else git("show",rev+":"+path);rows[(rev,path)]={"path":path,"revision":rev,"bytes":len(b),"sha256":sha(b),"role":role}
for name,oldrev in [("MANIFEST.json","3f191462fddfa7052587eb1e2a16fba8e0722708"),("AMENDMENT_MANIFEST.json","2be771150729043791dc194149ea456c5192a495")]:
 for x in rd(O/name)["files"]:
  rev=x["revision"]or oldrev;rows[(rev,x["path"])]=dict(x,revision=rev,role="Inherited exact evidence")
post={"MANIFEST.json","REMOTE_VERIFICATION.json","RECEIPT_GATES.json","receipt_gates.log","FINAL_BYTE_RECEIPT.json"}
def excluded(path):return Path(path).name in post or Path(path).name.startswith(("MANIFEST.fragment","REMOTE_VERIFICATION.fragment"))
changed=git("diff","--name-only",B).decode().splitlines()+git("ls-files","--others","--exclude-standard").decode().splitlines()
for path in sorted(set(changed)):
 if path.startswith(P.relative_to(R).as_posix()+"/")and excluded(path):continue
 add(path)
for x in rd(P/"CONTEXT_PREREQUISITE.json")["checks"]:add(x["path"],x["revision"],"Verified public prerequisite before collection")
for x in rd(P/"CURRENT_SOURCE_INVENTORY.json")["input_files"]:add(x["path"],D,"Exact declared source/UID/import input")
for x in rd(P/"RUNTIME_PATHS_AND_JSON.json")["json_catalogs"]:add(x["path"],D,"Exact parsed JSON catalogue; no visual or runtime credit")
for path in git("ls-tree","-r","--name-only",B,"--",O.relative_to(R).as_posix()).decode().splitlines():add(path,B,"Prior R49 packet")
for name in ["source_scopes.json","glyph_inventory.json","per_piece.json","scene_coverage.json","tally.json"]:add((H/name).relative_to(R).as_posix(),B,"Preserved frozen source register/readers")
for name in ["classify_dispatch.py","test_dispatch_semantics.py","engine/evidence/NATIVE_CLASS_INDEX.json"]:add((H/"r45_dispatch_semantics_audit"/name).relative_to(R).as_posix(),B,"Retained actual4.7.2 semantic helper/evidence")
idx=rd(H/"r45_dispatch_semantics_audit/engine/evidence/NATIVE_CLASS_INDEX.json")
for x in idx["classes"]:add((H/"r45_dispatch_semantics_audit/engine/evidence"/x["file"]).relative_to(R).as_posix(),B,"Retained exact native ClassDB query; no new engine run")
add((O/"test_callback_domains.py").relative_to(R).as_posix(),B,"Retained mutation adversarial tests")
rows=sorted(rows.values(),key=lambda x:(x["revision"]or"CURRENT",x["path"]));m={"schema":"reef.flat_vector_delta_manifest/1","revision":"FV-AUDIT-20261015-R50","repository":"Ebonyks/mermaid-roshan-reef","branch":"codex/flat-vector-r6-20261012","audited_source_revision":D,"topic_baseline":B,"files":rows,"required_file_count":len(rows),"required_bytes":sum(x["bytes"]for x in rows),"payload_sha256":sha("".join((x["revision"]or"CURRENT")+"\t"+x["path"]+"\t"+x["sha256"]+"\t"+str(x["bytes"])+"\n"for x in rows).encode()),"scope":"Complete required audit dependencies. Enumerated runtime media paths are metadata,not generation/context inputs; unreviewed media/native/resource/route/visual closure remains open. Source and historical context records retain exact revisions.","post_publication_records":"Receipt index/allparts,gates/log/final byte proof separately bound. This manifest index/allparts are verified separately from its dependency list,avoiding selfhash recursion.","new_generation_calls":0,"new_captures":0,"accepted_removed":0,"mission_complete":False};files=A.write_document(P/"MANIFEST.json",m);print("R50_MANIFEST",len(rows),m["required_bytes"],len(files),"physical manifest files",m["payload_sha256"],flush=True)
