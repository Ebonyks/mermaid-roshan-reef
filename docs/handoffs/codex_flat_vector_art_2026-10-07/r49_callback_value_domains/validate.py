"""Current R49 exact evidence, stable-ID, frozen-array and acceptance-lane integrity."""
from pathlib import Path
import json,hashlib,subprocess,importlib.util
P=Path(__file__).resolve().parent;R=P.parents[3];O=P.parent/"r48_grand_puff_context";BASE="61d12c5b7d29cd106a817d8d0064aa60f48f3ed2"
def rd(p):return json.loads(p.read_text(encoding="utf-8"))
def sha(b):return hashlib.sha256(b).hexdigest()
def raw(path,rev=BASE):return subprocess.check_output(["git","show",rev+":"+path],cwd=R,stderr=subprocess.PIPE)
def main():
 w=rd(P/"engine/attempt1/WRAPPER_PROVENANCE.json");assert sha((P/w["path"]).read_bytes())==w["sha256"]
 c=rd(P/"MUTATION_CENSUS.json");a=P/"audit_callback_domains.py";assert c["analyzer_sha256"]==sha(a.read_bytes());assert c["counts"]=={"COMPUTED_INDEX_WRITE":523,"DISPATCH_INVOCATION_CANDIDATE":338,"PROPERTY_MUTATOR":25,"NAMED_WRITE":11,"API_CALLER":15,"PORT_OR_OWNER_DECLARATION":10}
 assert len(c["rows"])==len({x["id"] for x in c["rows"]})==922
 for x in c["rows"]:assert sha(x["source"].encode())==x["source_sha256"]
 sources=rd(P/"SOURCE_EQUIVALENCE.json")["files"];assert len(sources)==312
 for x in sources:
  b=raw(x["path"]);assert sha(b)==x["sha256"]==x["r44_sha256"] and len(b)==x["bytes"] and x["parse"]=="PASS"
 dom=rd(P/"CALLBACK_DOMAINS.json");chains=rd(P/"NAMED_SOURCE_PATH_CHAINS.json");ports=dom["ports"];assert len(ports)==len(chains["chains"])==9
 plan=rd(P/"PLAN.json");assert {x["port_id"]for x in ports}==set(plan["selected_port_ids"]);assert {i for x in ports for i in x["invocation_ids"]}==set(plan["selected_invocation_ids"]) and len(plan["selected_invocation_ids"])==14
 assert dom["full_runtime_domains_still_open"]==57 and dom["R45_sites_outside_this_traced_subset"]==43
 assert all(not x["full_write_caller_value_closure"] and not x["native_alias_resource_runtime_closure"] for x in ports)
 inv={x["r45_binding_id"]for x in c["rows"]if x["kind"]=="DISPATCH_INVOCATION_CANDIDATE"};old=rd(P.parent/"r45_dispatch_semantics_audit/DISPATCH_SEMANTICS.json")["records"];assert inv=={x["binding_id"]for x in old if x["classification"]["invocation_expression"]}
 for x in chains["source_order_evidence"]:
  b=raw(x["path"]);assert sha(b)==x["file_sha256"] and sha(x["body"].encode())==x["body_sha256"] and x["body"] in b.decode("utf-8-sig")
 rs=rd(P/"RESOURCE_SYMBOL_SCAN.json");assert len(rs["resources"])==rs["resource_count"]==17 and rs["literal_hit_rows"]==rs["opaque_binary_count"]==0
 for x in rs["resources"]:b=raw(x["path"]);assert sha(b)==x["sha256"] and len(b)==x["bytes"]
 for x in rd(P/"CONTEXT_PREREQUISITE.json")["checks"]+rd(P/"REVIEW.json")["source_references"]:
  b=raw(x["path"],x["revision"]);assert sha(b)==x["sha256"] and len(b)==x["bytes"]
 proof=rd(P/"engine/attempt1/COMPONENT_PROOF.json");result=rd(P/"engine/attempt1/RESULT.json");assert len(proof["checks"])==21 and all(x["pass"]for x in proof["checks"])
 assert proof["engine"]["string"]=="4.7.2-stable (official)" and proof["engine"]["hash"]=="ed1daf0bf001b61586d9930840f2f1394092c079" and proof["display"]=="headless" and not proof["game_instantiated"]
 assert proof["fixture_sha256"]==sha((P/"probe_callback_domains.gd").read_bytes())==sha((P/"engine/attempt1/fixture_source.gd").read_bytes());assert result["log_sha256"]==sha((P/"engine/attempt1/engine.log").read_bytes())
 assert result["exit_code"]==0 and result["sidecars_exact"] and result["sidecars_before_count"]==result["sidecars_after_count"]==4039 and result["fixture_unchanged"] and not result["script_or_shader_errors"]
 assert result["normal_before"]==result["normal_after"]==proof["normal_before"]==proof["normal_after"] and len(proof["normal_before"])==8
 for name in ["per_piece.json","scene_coverage.json","tally.json"]:
  d=rd(P/name);prior=rd(O/name);assert d["inherited_r48_reference_base"]==BASE and d["callback_value_domains"]["all_R45_full_runtime_domains_still_open"]==57
  if name=="per_piece.json":assert d["pieces"]==prior["pieces"] and d["supplemental_piece_records"]==prior["supplemental_piece_records"] and len(d["pieces"])+len(d["supplemental_piece_records"])==240
  if name=="scene_coverage.json":assert d["entries"]==prior["entries"] and d["effective_partial_entries"]==83 and d["effective_entries_without_current_slice"]==93 and d["complete_entries"]==0
  if name=="tally.json":
   assert d["historical_totals"][:-1]==prior["historical_totals"] and d["historical_totals"][-1]["immutable_final_byte_proof_revision"]==BASE
   for k in ["current_context","current_partial_context_counts","current_context_sample_lanes","known_named_design_records_including_supplemental","known_family_count_including_supplemental","remaining_source_scopes_to_disposition"]:assert d[k]==prior[k],k
   assert d["known_named_design_records_including_supplemental"]==240 and d["known_family_count_including_supplemental"]==32 and d["accepted_removed"]==d["integrated"]==d["runtime_verified"]==0 and d["all_game_individual_piece_total"] is None and d["regression_count"] is None
 # Old frozen roots and all prior revision evidence stay byte-identical.
 changed=subprocess.check_output(["git","diff","--name-only",BASE],cwd=R,text=True).splitlines()
 for path in changed:
  assert not path.startswith(("scripts/","assets/","assets_src/","scenes/","shaders/","addons/")) and path!="project.godot",path
 for n in ["per_piece.json","scene_coverage.json","tally.json"]:assert (P.parent/n).read_bytes()==raw((P.parent/n).relative_to(R).as_posix())
 cur=rd(P.parent/"CURRENT.json");assert cur["current_tally"]==P.name+"/tally.json" and cur["revision"]==plan["revision"]
 assert not rd(P/"WORK_IN_PROGRESS.json")["mission_complete"] and not rd(P/"REVIEW.json")["mission_complete"]
 print("R49_INTEGRITY_PASS 312exact scripts/922rows/338IDs/9paths14sites/full57open;21headless checks;240roles32families;frozen/history/zeroacceptance preserved",flush=True)
if __name__=="__main__":main()
