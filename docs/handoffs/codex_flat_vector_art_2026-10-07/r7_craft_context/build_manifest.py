"""Build the additive delta without changing the frozen R6 representation."""
from pathlib import Path
import json,hashlib,subprocess
P=Path(__file__).resolve().parent;R=P.parents[3];H=P.parent
A="4aceae967de9da7c8f479e358a008188ba1f6304";B="70879a91ddcbba51ba09c7d0be81cc65f340e3b5"
def sha(b):return hashlib.sha256(b).hexdigest()
rows=[]
local=sorted([x for x in P.rglob("*") if x.is_file() and x.name not in ["MANIFEST.json","REMOTE_VERIFICATION.json"] and "__pycache__" not in x.parts]+[H/"CURRENT.json",H/"README.md",R/"ASSET_LICENSES.md",R/"audit/MASTER_AUDIT_2026-08-09.md",R/"audit/MASTER_AUDIT_CHANGELOG_ROLLBACK_2026-08-10.md",R/"design/05_DOC_LEDGER.md",R/"design/audit_impacts/flat-vector-craft-context-20261012.json"])
for x in local:
 b=x.read_bytes();rows.append({"path":x.relative_to(R).as_posix(),"revision":None,"bytes":len(b),"sha256":sha(b),"role":"R7 delta"})
for s in json.loads((P/"SOURCES.json").read_text(encoding="utf-8"))["sources"]:rows.append({"path":s["path"],"revision":s["immutable_revision"],"bytes":s["bytes"],"sha256":s["sha256"],"role":"Exact source/license dependency"})
deps=[(A,"per_piece.json"),(A,"scene_coverage.json"),(A,"tally.json"),(A,"CONGRUENCY_BACKLOG.json"),(A,"CURRENT_SCOPE_CONTEXT_OVERLAY.json"),(A,"FULL_VALIDATION.json"),(A,"MANIFEST.json"),(B,"REMOTE_VERIFICATION.json")]
for rev,n in deps:
 path=(H/ n).relative_to(R).as_posix();b=subprocess.check_output(["git","show",rev+":"+path],cwd=R,stderr=subprocess.PIPE);rows.append({"path":path,"revision":rev,"bytes":len(b),"sha256":sha(b),"role":"Frozen R6 registry/history/probe/public-delivery evidence"})
for n in ["AGENTS.md","design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md","design/AUDIT_DEVELOPMENT_CONTRACT.md","design/02_ART_DIRECTION.md","ART_STYLE_GUIDE.md","audit/findings/ACTIVE_FINDINGS_2026-08-13.md"]:
 b=subprocess.check_output(["git","show",B+":"+n],cwd=R,stderr=subprocess.PIPE);rows.append({"path":n,"revision":B,"bytes":len(b),"sha256":sha(b),"role":"Binding authority"})
rows.extend(json.loads((P/"ORIGIN_DEV_RECONCILIATION.json").read_text(encoding="utf-8"))["required_immutable_files"])
rows.sort(key=lambda x:(x["revision"] or "CURRENT",x["path"]))
data={"schema":"reef.flat_vector_delta_manifest/1","revision":"FV-AUDIT-20261012-R7","repository":"Ebonyks/mermaid-roshan-reef","branch":"codex/flat-vector-r6-20261012","files":rows,"required_file_count":len(rows),"required_bytes":sum(x["bytes"] for x in rows),"payload_sha256":sha("".join((x["revision"] or "CURRENT")+"\t"+x["path"]+"\t"+x["sha256"]+"\t"+str(x["bytes"])+"\n" for x in rows).encode()),"inherited_context_limit":"Unchanged R6 context dependencies were previously fully verified by the exact immutable bound receipt; this revision re-verifies its declared delta/source/history/authority dependencies. No new full-game closure claim.","excluded_post_publication_record":"REMOTE_VERIFICATION.json","accepted_removed":0,"mission_complete":False}
(P/"MANIFEST.json").write_text(json.dumps(data,indent=2)+"\n",encoding="utf-8",newline="\n")
print("R7 MANIFEST",len(rows),data["required_bytes"],data["payload_sha256"])
