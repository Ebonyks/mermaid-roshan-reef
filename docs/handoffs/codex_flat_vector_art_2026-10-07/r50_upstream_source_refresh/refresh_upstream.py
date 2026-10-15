"""Full exact upstream AST refresh; no source or runtime mutation."""
from pathlib import Path
import json,hashlib,subprocess,importlib.util,collections,datetime
P=Path(__file__).resolve().parent;R=P.parents[3];H=P.parent;B="4c5c026fd4a3c1ffaded5f13a123a28a2e13f677";D="5120b6d59885dd057937aaf284e73681d8eac9f5"
def sha(b):return hashlib.sha256(b).hexdigest()
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
I=module("inventory50",P/"scan_source_inventory.py");A=module("mutations50",H/"r49_callback_value_domains/audit_callback_domains.py");A.BASE=D
bounded=I._bounded

def rd(p):return bounded.read_document(p)
def wr(n,d):bounded.write_document(P/n,d)
def git(*a):return subprocess.check_output(["git",*a],cwd=R,stderr=subprocess.PIPE)
def batch(paths,rev):
 raw=git("cat-file","--batch") if False else subprocess.check_output(["git","cat-file","--batch"],cwd=R,input="".join(rev+":"+p+"\n"for p in paths).encode(),stderr=subprocess.PIPE);pos=0;out={}
 for path in paths:
  end=raw.index(b"\n",pos);header=raw[pos:end].decode().split();assert header[1]=="blob";size=int(header[2]);pos=end+1;out[path]=raw[pos:pos+size];pos+=size;assert raw[pos:pos+1]==b"\n";pos+=1
 assert pos==len(raw);return out

def main():
 assert git("rev-parse","HEAD").decode().strip()==B
 I.run()
 inv=rd(P/"CURRENT_SOURCE_INVENTORY.json");assert inv["baseline"]==D and inv["parse_failures"]==0
 paths=[x["path"]for x in inv["scripts"]];assert len(paths)==312
 current=batch(paths,D);oldraw=batch(paths,B);facts=[]
 for path in paths:facts.append(A.Facts(current[path].decode("utf-8-sig"),path))
 sf=[x.sf for x in facts];indexpath=H/"r45_dispatch_semantics_audit/engine/evidence/NATIVE_CLASS_INDEX.json";index=rd(indexpath);native={}
 for x in index["classes"]:
  raw=(indexpath.parent/x["file"]).read_bytes();assert sha(raw)==x["sha256"];native[x["class_name"]]=json.loads(raw)
 resolver=A.D.Resolver(sf,native);oldsem=rd(H/"r45_dispatch_semantics_audit/DISPATCH_SEMANTICS.json");oldmap={x["binding_id"]:x for x in oldsem["records"]};sem=[];seen=set();classcollisions={}
 for f in sf:
  for info in f.classes.values():
   if info["name"]:classcollisions.setdefault(info["name"],[]).append(f.path)
 classcollisions={k:v for k,v in classcollisions.items()if len(v)>1}
 assert not classcollisions,"Duplicate global class names require conservative resolution before semantic credit"
 for f in sf:
  for row in f.calls:
   key=row["binding_id"];old=oldmap.get(key);equal=bool(old and old["r44_record"]["full_excerpt_sha256"]==row["full_excerpt_sha256"] and old["r44_record"]["path"]==row["path"] and old["r44_record"]["function"]==row["function"] and old["r44_record"]["method"]==row["method"])
   rec={k:v for k,v in row.items()if k in ["binding_id","path","function","line","end_line","method","receiver_AST","full_excerpt_sha256"]};rec["source_expression_id"]="FVE50-"+sha((key+"|"+row["full_excerpt_sha256"]).encode())[:12].upper();rec["audited_source_revision"]=D;rec["file_sha256"]=sha(current[f.path]);rec["source_excerpt"]=f.excerpt(row["node"]);rec["probe_label"]=Path(f.path).name.startswith("probe")or Path(f.path).stem.endswith("_test_case");rec["classification"]=resolver.classify(f,row);rec["R45_source_site_match"]="RAW_KEY_AND_EXACT_EXCERPT"if equal else("SAME_RAW_KEY_CHANGED_EXCERPT_IDENTITY_REVIEW_REQUIRED"if old else"NEW_RAW_KEY_IN_THIS_SOURCE_SNAPSHOT");rec["prior_R45_binding_id"]=key if equal else None;sem.append(rec);seen.add(key)
 stats={}
 for label,probe in [("non_test_source_candidates",False),("probe_or_test",True)]:
  selected=[x for x in sem if x["probe_label"]==probe];stats[label]={"raw_expressions":len(selected),"categories":dict(collections.Counter(x["classification"]["category"]for x in selected)),"constructors":sum(not x["classification"]["invocation_expression"]for x in selected),"invocations":sum(x["classification"]["invocation_expression"]for x in selected),"unresolved_invocations":sum(x["classification"]["invocation_expression"]and x["classification"]["method_selector"]is None for x in selected)}
 wr("DISPATCH_SEMANTICS.json",{"baseline":D,"topic_baseline":B,"records":sem,"summary":stats,"R45_original_records_retained":len(oldmap),"R45_exact_key_excerpt_matches":sum(x["prior_R45_binding_id"]is not None for x in sem),"R45_raw_keys_not_in_current_source":sorted(set(oldmap)-seen),"class_alias_collisions":classcollisions,"native_metadata":{"path":indexpath.relative_to(R).as_posix(),"revision":B,"sha256":sha(indexpath.read_bytes()),"engine":index["engine"],"scope":"Retained actual97-class exact4.7.2 ClassDB query; no new query/game/scene run. Missing types remain unresolved."},"helper_sha256":A.D.EXECUTION_SOURCE_SHA,"no_historical_ID_or_disposition_rewritten":True,"limits":"Raw-key/excerpt match is source correspondence only, not all intervening writes/callers or runtime closure. New source-expression IDs do not become artwork IDs. Literal Callable data never becomes a target edge.","accepted_removed":0})
 mut=[r for f in facts for r in f.rows];oldmut=rd(H/"r49_callback_value_domains/MUTATION_CENSUS.json")["rows"];oldby={x["id"]:x for x in oldmut};nowby={x["id"]:x for x in mut};assert len(nowby)==len(mut)
 wr("MUTATION_CENSUS.json",{"baseline":D,"rows":mut,"counts":dict(collections.Counter(x["kind"]for x in mut)),"helper_reference":(H/"r49_callback_value_domains/audit_callback_domains.py").relative_to(R).as_posix(),"helper_revision":B,"helper_sha256":sha((H/"r49_callback_value_domains/audit_callback_domains.py").read_bytes()),"configuration_override":{"BASE":D,"main_called":False,"reason":"Reuse exact tested Facts extractor on the actual new source revision; no old equality assertions or old output writers executed."},"R49_correspondence":[{"prior_id":x["id"],"status":"EXACT_KEY_AND_EXCERPT"if x["id"]in nowby and nowby[x["id"]]["source_sha256"]==x["source_sha256"]else("SAME_KEY_CHANGED_EXCERPT_REVIEW_REQUIRED"if x["id"]in nowby else"KEY_NOT_REBOUND_NO_RETIREMENT_INFERRED")}for x in oldmut],"limits":"Computed index/property/alias/native/resource domains remain open; risk rows are not callback writers or artwork pieces by default."})
 oldports=rd(H/"r49_callback_value_domains/CALLBACK_DOMAINS.json")["ports"];semby={x["binding_id"]:x for x in sem};selected=[]
 for port in oldports:
  for key in port["invocation_ids"]:
   row=semby[key];assert row["prior_R45_binding_id"]==key and row["classification"]["invocation_expression"]
   selected.append({"port_id":port["port_id"],"binding_id":key,"line":row["line"],"file_sha256":row["file_sha256"],"excerpt_sha256":row["full_excerpt_sha256"],"audited_source_revision":D,"scope":"Exact current invocation correspondence; R49 named-chain and18-method body evidence retained. All write/native/alias/resource/runtime domains stay open."})
 wr("R49_SELECTED_CALLBACK_TRANSFER.json",{"baseline":D,"sites":selected,"source_sites":14,"full_runtime_domains_closed":0,"original_R45_runtime_domains_still_open":57,"new_current_unknowns_separate":"DISPATCH_SEMANTICS.json","current_upstream_runtime_or_art_acceptance":False})
 bypath={x["path"]:x for x in inv["scripts"]};deltas=[]
 oldscope=rd(H/"r37_current_source_inventory/SOURCE_SCOPE_RECONCILIATION.json");oldcurrent=rd(H/"r37_current_source_inventory/CURRENT_SOURCE_INVENTORY.json");prior_scopes={(x["path"],x["scope"]):x for x in oldscope["additional_source_candidates"]};newscope=rd(P/"SOURCE_SCOPE_RECONCILIATION.json");new_scopes={(x["path"],x["scope"]):x for x in newscope["additional_source_candidates"]}
 for path in paths:
  if sha(current[path])==sha(oldraw[path]):continue
  old=I.parse_script(path,oldraw[path]);new=bypath[path];of={x["name"]:x for x in old["functions"]};nf={x["name"]:x for x in new["functions"]};assert len(of)==len(old["functions"]) and len(nf)==len(new["functions"])
  functions=[]
  for name in sorted(set(of)|set(nf)):
   a,b=of.get(name),nf.get(name)
   if a and b and a["source_sha256_lf"]==b["source_sha256_lf"]:continue
   funcs={"function":name,"status":"BODY_CHANGED"if a and b else("NEW_QUALIFIED_FUNCTION"if b else"PRIOR_FUNCTION_NOT_IN_THIS_SOURCE_NO_RETIREMENT_INFERRED"),"old":a,"current":b,"current_candidate_categories":sorted({cat for c in new["calls"]if c["scope"]==name for cat in I.categories(c)}),"full_route_or_art_disposition":None};functions.append(funcs)
  deltas.append({"path":path,"topic_revision":B,"topic_sha256":sha(oldraw[path]),"upstream_revision":D,"upstream_sha256":sha(current[path]),"probe_label":Path(path).name.startswith("probe"),"changed_functions":functions,"source_context_review_pending":True})
 added=[new_scopes[k]for k in sorted(new_scopes.keys()-prior_scopes.keys())];missing=[prior_scopes[k]for k in sorted(prior_scopes.keys()-new_scopes.keys())]
 wr("UPSTREAM_DELTA.json",{"baseline":D,"topic_baseline":B,"changed_script_count":len(deltas),"script_changes":deltas,"qualified_function_changes":dict(collections.Counter(x["status"]for f in deltas for x in f["changed_functions"])),"candidate_scopes_not_in_R37":added,"prior_candidate_scopes_not_in_current":missing,"original_R37_candidate_ids_retained_in_historical_packet":True,"all_frozen_scope_ids_preserved":369,"all_frozen_glyph_ids_preserved":348,"new_artwork_role_count":None,"regression_count":None,"accepted_removed":0,"limits":"Qualified function/API/symbol/reference deltas choose the next current scene/state audit. They do not classify an art piece, exempt geometry, prove route reachability or accept incoming gameplay repairs."})
 wr("SCAN_PROVENANCE.json",{"audited_source_revision":D,"topic_baseline":B,"current_inventory_scanner_sha256":sha((P/"scan_source_inventory.py").read_bytes()),"driver_sha256":sha(Path(__file__).read_bytes()),"R45_semantic_helper_sha256":A.D.EXECUTION_SOURCE_SHA,"R49_mutation_helper_sha256":sha((H/"r49_callback_value_domains/audit_callback_domains.py").read_bytes()),"current_source_parse_files":len(paths),"source_prerequisite":"CONTEXT_PREREQUISITE.json","runtime_code_changed":False,"runtime_or_engine_executions":0,"generation_calls":0,"accepted_removed":0,"mission_complete":False})
 print("R50_DISPATCH",len(sem),json.dumps(stats),"MUTATIONS",len(mut),"SOURCE_DELTA",len(deltas),"functions",sum(len(x["changed_functions"])for x in deltas),"new candidate scopes",len(added),"missing",len(missing),flush=True)
if __name__=="__main__":main()
