"""Fresh immutable upstream inventory integrity; no runtime/art acceptance."""
from pathlib import Path
import json,hashlib,subprocess,importlib.util,collections
P=Path(__file__).resolve().parent;R=P.parents[3];H=P.parent;B="4c5c026fd4a3c1ffaded5f13a123a28a2e13f677";D="5120b6d59885dd057937aaf284e73681d8eac9f5";O=H/"r49_callback_value_domains"
s=importlib.util.spec_from_file_location("bound50validate",P/"bounded_json.py");A=importlib.util.module_from_spec(s);s.loader.exec_module(A)
def rd(p):return A.read_document(p)
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(["git",*a],cwd=R,stderr=subprocess.PIPE)
def batch(rows):
 request="".join(rev+":"+path+"\n"for rev,path in rows).encode();raw=subprocess.check_output(["git","cat-file","--batch"],cwd=R,input=request,stderr=subprocess.PIPE);pos=0;out={}
 for rev,path in rows:
  end=raw.index(b"\n",pos);parts=raw[pos:end].decode().split();assert parts[1]=="blob";size=int(parts[2]);pos=end+1;out[(rev,path)]=raw[pos:pos+size];pos+=size+1
 assert pos==len(raw);return out

def main():
 inv=rd(P/"CURRENT_SOURCE_INVENTORY.json");summary=rd(P/"SOURCE_SUMMARY.json");assert inv["baseline"]==D and inv["parsed_gd_files"]==312 and inv["parse_failures"]==0 and len(inv["input_files"])==1510
 inputs=[(D,x["path"])for x in inv["input_files"]];raws=batch(inputs)
 for x in inv["input_files"]:b=raws[(D,x["path"])];assert sha(b)==x["raw_sha256"]and len(b)==x["bytes"]
 for x in inv["scripts"]:assert sha(raws[(D,x["path"])])==x["raw_sha256"]
 scopes=rd(P/"SOURCE_SCOPE_RECONCILIATION.json");root=rd(H/"source_scopes.json")["scopes"];assert {x["id"]for x in scopes["rows"]}=={x["id"]for x in root}and len(root)==369 and all(x["binding_status"]=="CURRENT_FUNCTION_REBOUND"for x in scopes["rows"])and len(scopes["additional_source_candidates"])==825
 glyph=rd(P/"GLYPH_SCOPE_GAPS.json");assert {x["id"]for x in glyph["rows"]}=={x["id"]for x in rd(H/"glyph_inventory.json")["sites"]}and len(glyph["rows"])==348
 sem=rd(P/"DISPATCH_SEMANTICS.json");assert len(sem["records"])==506 and sem["R45_original_records_retained"]==493 and sem["R45_exact_key_excerpt_matches"]==489 and not sem["R45_raw_keys_not_in_current_source"]
 non=sem["summary"]["non_test_source_candidates"];assert(non["constructors"],non["invocations"],non["unresolved_invocations"])==(102,157,57)
 for x in sem["records"]:
  assert x["audited_source_revision"]==D and sha(raws[(D,x["path"])])==x["file_sha256"]and sha(x["source_excerpt"].encode())==x["full_excerpt_sha256"]
  if x["classification"]["category"].startswith("CALLABLE_"):assert "data"in x["classification"]["first_argument_role"]
 mut=rd(P/"MUTATION_CENSUS.json");assert len(mut["rows"])==927 and mut["counts"]=={"COMPUTED_INDEX_WRITE":525,"DISPATCH_INVOCATION_CANDIDATE":341,"PROPERTY_MUTATOR":25,"NAMED_WRITE":11,"API_CALLER":15,"PORT_OR_OWNER_DECLARATION":10};assert collections.Counter(x["status"]for x in mut["R49_correspondence"])=={"EXACT_KEY_AND_EXCERPT":921,"SAME_KEY_CHANGED_EXCERPT_REVIEW_REQUIRED":1}
 for x in mut["rows"]:assert sha(x["source"].encode())==x["source_sha256"]
 tr=rd(P/"R49_SELECTED_CALLBACK_TRANSFER.json");assert tr["source_sites"]==14 and tr["original_R45_runtime_domains_still_open"]==57 and tr["full_runtime_domains_closed"]==0
 delta=rd(P/"UPSTREAM_DELTA.json");assert delta["changed_script_count"]==25 and delta["qualified_function_changes"]=={"BODY_CHANGED":71,"NEW_QUALIFIED_FUNCTION":62,"PRIOR_FUNCTION_NOT_IN_THIS_SOURCE_NO_RETIREMENT_INFERRED":4};assert len(delta["candidate_scopes_not_in_R37"])==13 and len(delta["prior_candidate_scopes_not_in_current"])==2
 decl=rd(P/"TOP_LEVEL_DECLARATION_DELTA.json");assert decl["file_count"]==9 and decl["main_audio_guide_field_added"]
 for f in decl["files"]:
  for row in f["prior_nodes_not_exactly_rebound"]+f["new_or_changed_current_nodes"]:assert sha(row["source"].encode())==row["sha256"]
 catalog=rd(P/"RUNTIME_PATHS_AND_JSON.json");assert catalog["runtime_root_tracked_path_count"]==len(catalog["tracked_paths"])==4420 and len(catalog["json_catalogs"])==18
 extras=[(D,x["path"])for x in catalog["json_catalogs"]];raws.update(batch(extras))
 for x in catalog["json_catalogs"]:assert sha(raws[(D,x["path"])])==x["sha256"]and x["json_parse"]=="PASS"and x["http_status"]==200
 prereq=rd(P/"CONTEXT_PREREQUISITE.json")["checks"];assert len(prereq)==330;proofraw=batch([(x["revision"],x["path"])for x in prereq])
 for x in prereq:assert sha(proofraw[(x["revision"],x["path"])] )==x["sha256"]and x["http_status"]==200
 prov=rd(P/"SCAN_PROVENANCE.json");assert prov["driver_sha256"]==sha((P/"refresh_upstream.py").read_bytes())and prov["current_inventory_scanner_sha256"]==sha((P/"scan_source_inventory.py").read_bytes())
 for name in ["per_piece.json","scene_coverage.json","tally.json"]:
  d=rd(P/name);prior=rd(O/name);assert d["upstream_source_refresh"]["audited_source_revision"]==D
  if name=="per_piece.json":assert d["pieces"]==prior["pieces"]and d["supplemental_piece_records"]==prior["supplemental_piece_records"]and len(d["pieces"])+len(d["supplemental_piece_records"])==240
  if name=="scene_coverage.json":assert d["entries"]==prior["entries"]and d["effective_partial_entries"]==83 and d["effective_entries_without_current_slice"]==93 and d["complete_entries"]==0
  if name=="tally.json":
   assert d["historical_totals"][:-1]==prior["historical_totals"]and d["historical_totals"][-1]["immutable_final_byte_proof_revision"]==B
   for k in ["current_context","current_context_sample_lanes","current_partial_context_counts"]:assert d[k]==prior[k]
   assert(d["known_named_design_records_including_supplemental"],d["known_family_count_including_supplemental"],d["accepted_removed"],d["integrated"],d["runtime_verified"])==(240,32,0,0,0)and d["all_game_individual_piece_total"]is None and d["regression_count"]is None
 assert not git("diff","--name-only",B,"--","scripts","assets","assets_src","scenes","shaders","addons","project.godot").strip()
 for n in ["per_piece.json","scene_coverage.json","tally.json"]:assert(H/n).read_bytes()==git("show",B+":"+(H/n).relative_to(R).as_posix())
 assert rd(H/"CURRENT.json")["current_tally"]==P.name+"/tally.json"
 assert all(x.stat().st_size<4194304 for x in P.rglob("*")if x.is_file())
 assert not rd(P/"WORK_IN_PROGRESS.json")["mission_complete"]and not rd(P/"REVIEW.json")["mission_complete"]
 print("R50_INTEGRITY_PASS exactD312scripts/1510inputs/369frozen/348glyphs/506dispatch/927mutation/25files137functions9declarations/4420paths18JSON;240roles32families/0accepted/globalunknown;runtimeunchanged",flush=True)
if __name__=="__main__":main()
