"""Bounded R7 integrity and no-acceptance verification; no runtime edits."""
from pathlib import Path
import json,hashlib,subprocess,copy
from PIL import Image
P=Path(__file__).resolve().parent;H=P.parent;R=P.parents[3]
def read(n):return json.loads((P/n).read_text(encoding="utf-8"))
def sha(b):return hashlib.sha256(b).hexdigest()
def req(v,m):
 if not v:raise ValueError(m)
def guard(t,pc,c,rv):
 req(t["all_game_individual_piece_total"] is None,"unknown denominator")
 req(all(t[k]==0 for k in ["replaced","integrated","runtime_verified","accepted_removed"]),"no removals")
 req(len(pc["pieces"])==224 and len(pc["supplemental_piece_records"])==1,"frozen/supplemental units")
 req(pc["known_named_design_records_including_supplemental"]==225 and t["known_named_design_records_including_supplemental"]==225,"known records")
 req(pc["known_family_count_including_supplemental"]==30,"families")
 req(len(pc["supplemental_piece_records"][0]["component_roles"])==3,"whole design versus layers")
 req(t["remaining_source_scopes_to_disposition"]==351 and t["supplemental_texture_compositor_scopes"]==2,"scope units")
 req(len(c["entries"])==176 and len({x["id"] for x in c["entries"]})==176,"stable routes")
 req(sum("PARTIAL" in x["status"] for x in c["entries"])==77 and c["partial_entries"]==77 and c["entries_without_current_slice"]==99,"partial route counts")
 req(c["complete_entries"]==0 and not any(x.get("route_or_saved_variants_complete") for x in c["entries"]),"no complete route")
 req(rv["native_captures"]==80 and len(rv["capture_bindings"])==80 and sum(x["independently_viewed"] for x in rv["capture_bindings"])==5,"native/review units")
 req(rv["acceptance"]["owner"] is None and rv["acceptance"]["accepted_removed"]==0 and not rv["acceptance"]["full_context_review_complete"],"no acceptance")
 req(t["current_context"]["exact_capture_count"]==1664 and t["current_context"]["retained_native_capture_count"]==1766,"historical native counts")
 for ob in rv["observations"]:
  req(ob["piece_ids"]==[rv["piece_id"]] and len(ob["comparison"])==10,"point-by-point binding")
def main():
 t=read("tally.json");pc=read("per_piece.json");c=read("scene_coverage.json");rv=read("REVIEW.json");guard(t,pc,c,rv)
 old=json.loads((H/"per_piece.json").read_text(encoding="utf-8"));req(pc["pieces"]==old["pieces"],"frozen IDs/history changed")
 expected="FVR-"+sha(rv["identity_key"].encode())[:12].upper();req(rv["piece_id"]==expected and pc["supplemental_piece_records"][0]["id"]==expected,"stable semantic ID")
 req(len({x["path"] for x in rv["capture_bindings"]})==80,"duplicate file binding")
 for b in rv["capture_bindings"]:
  q=P/b["path"];raw=q.read_bytes();req(sha(raw)==b["sha256"] and len(raw)==b["bytes"],"native bytes")
  with Image.open(q) as im:req(list(im.size)==b["dimensions"],"native dimensions")
 for a in ["1280x720","1600x720"]:
  m=read("captures/"+a+"/capture_manifest.json");req(len(m["states"])==40 and not m["errors"] and m["normal_save_before"]==m["normal_save_after"],"capture/save scope")
  req(m["renderer"]=="mobile" and m["quality"]=="speedy" and m["engine"]["hash"].startswith("ed1daf0bf") and m["source_revision"]=="e2b3c73789707aa49a91b4f42e2a9dd4b68225df","exact engine/source")
 orig=read("original_launch_receipt.json");req(orig["returncode"]==0 and not orig["changed_runtime_sources"] and orig["harness_sha256"]==sha((P/"capture_craft.gd").read_bytes()),"original launch binding")
 parity=read("SOURCE_PARITY.json");req(parity["matched_raw"]==5350 and parity["newline_only_import_sidecars"]==1102 and not parity["unresolved"],"raw versus semantic parity")
 for x in parity["raw_mismatches"]:req(x["path"].endswith(".import") and x["lf_canonical_matches_recorded"],"sidecar limit")
 req(not subprocess.check_output(["git","diff","e2b3c73789707aa49a91b4f42e2a9dd4b68225df","--","scripts","scenes","assets","shaders","project.godot"],cwd=R,stderr=subprocess.PIPE),"runtime change")
 base=[t,pc,c,rv];controls=[("fake_total",0,lambda x:x.update(all_game_individual_piece_total=225)),("fake_removal",0,lambda x:x.update(accepted_removed=1)),("count_layers_as_designs",1,lambda x:x.update(known_named_design_records_including_supplemental=227)),("complete_route",2,lambda x:x.update(complete_entries=1)),("owner_acceptance",3,lambda x:x["acceptance"].update(owner="ACCEPTED")),("source_scope_closure",0,lambda x:x.update(remaining_source_scopes_to_disposition=0))]
 for n,i,f in controls:
  vals=copy.deepcopy(base);f(vals[i]);caught=False
  try:guard(*vals)
  except ValueError:caught=True
  req(caught,"missed negative control "+n)
 print("R7|ALL OK|80native/5viewed/4observations;224frozen+1whole fish;77partial/0complete;unknown denominator;0accepted;6negative controls")
if __name__=="__main__":main()
