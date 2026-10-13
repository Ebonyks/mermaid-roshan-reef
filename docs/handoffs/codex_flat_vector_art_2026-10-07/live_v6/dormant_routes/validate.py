"""Fail-closed source-only route evidence checks; grants no visual acceptance."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from immutable_source import source_bytes
import argparse,copy,hashlib,json,re,subprocess
from functools import lru_cache
P=Path(__file__).resolve().parent
R=P.parents[4]
H="6cde8aeae04aaedcc0b1ff22a05ef93ab9bf666f"
IDS={"FVF-3F1F73EDCAD1","FVF-3F9F842B7BA3","FVF-8A1564966D4B","FVF-535EDBF3F803","FVF-F5F7A8DE4736","FVF-355A4498233C"}
TOKENS="_open_craft_studio _craft_ref CraftStudio _style_swatch _mg2d_open _mg_build_slide _mg_circle _mg2d_feedback_burst PictureGames _build_pearl_castle _hang_portrait _touch_open_picture _l2_start_slide _start_game _start_game_now wall_pics PIC_GAME DollsNurserySurface DollsGame FetchGame MelodyGame SeekGame ShopGame SlideRaceGame TreasureGame ProsceniumCanvas FishSteerCueCanvas FishStageTrimCanvas SeekMeadowSurface".split()
PAT=re.compile(r"\b(?:"+"|".join(map(re.escape,TOKENS))+r")\b")
@lru_cache(maxsize=None)
def git_original(name):return source_bytes(R,H,name)
def sha(b):return hashlib.sha256(b).hexdigest()
def read(n):return json.loads((P/n).read_text(encoding="utf-8"))
def safe(base,name):
 p=(base/name).resolve()
 assert p.is_relative_to(base.resolve()),"unsafe evidence path"
 return p
def check(overrides=None,byte_overrides=None):
 overrides=overrides or {};byte_overrides=byte_overrides or {}
 def get(n):return copy.deepcopy(overrides[n]) if n in overrides else read(n)
 m=get("MACHINE.json")
 for k,v in {"source_revision":H,"method":"SOURCE_ONLY_NO_NATIVE_RUN","native_frames_added":0,"cumulative_staged_frames":1178,"R6_total_staged_new_frames":574,"overlapping_entries":176,"partial_entries":62,"complete_entries":0,"source_route_reviewed_scopes":6,"friend_scope_backlog":27,"classified_visual_scopes":10,"unresolved_scopes":359,"source_role_briefs":37,"affected_overlapping_catalogue_entries":26,"flat_role_contexts_prior_native_slices":119,"replacements":0,"accepted_removals":0,"visual_device_child_owner_acceptance":False,"DL_QA_11":False,"publication":"UNPUBLISHED_HANDOFF_BLOCKED","all_game_individual_piece_total":None,"current_visible_new_art_instances":None}.items():assert m[k]==v,(k,"source-only claim drift")
 scan=get("REFERENCE_SCAN.json");assert scan["tokens"]==TOKENS
 tracked=subprocess.check_output(["git","ls-files","-z"],cwd=R).decode().split("\0")
 corpus=[];refs=[]
 for name in sorted(tracked):
  p=R/name
  if not p.is_file() or name.startswith(("docs/","audit/","design/","assets_src/","disabled_addons/")) or p.suffix not in {".gd",".tscn",".tres",".godot",".gdshader"}:continue
  b=p.read_bytes();corpus.append({"path":name,"working_sha256":sha(b),"bytes":len(b)})
  for i,line in enumerate(b.decode("utf-8-sig").splitlines(),1):
   found=sorted(set(PAT.findall(line)))
   if found:refs.append({"path":name,"line":i,"tokens":found,"text":line,"lane":"HISTORICAL_BACKUP_REFERENCE" if name.startswith("backups/") else ("TEST_PROBE" if "/probe" in "/"+name else "PRODUCTION_SOURCE")})
 assert scan["corpus_count"]==len(corpus)==349 and scan["corpus"]==corpus,"source corpus drift"
 assert scan["references"]==refs and len(refs)==382,"reference closure drift"
 source=get("SOURCE_PROOFS.json");assert source["revision"]==H and len(source["sources"])==46
 paths=set();source_text={}
 for row in source["sources"]:
  name=row["path"];assert name not in paths;paths.add(name)
  original=git_original(name)
  archived=byte_overrides.get(row["packet_path"],safe(P,row["packet_path"]).read_bytes())
  assert sha(original)==row["git_lf_sha256"] and archived==original,"archived source mismatch"
  current=safe(R,name).read_bytes();assert sha(current)==row["working_tree_sha256"],"working source drift"
  assert current.replace(b"\r\n",b"\n")==original,"production source changed"
  source_text[name]=archived.decode("utf-8-sig")
 assert {r["path"] for r in refs}.issubset(paths),"unbound reference file"
 # Independently require the critical concrete control flow; route prose is insufficient.
 picture=source_text["scripts/games/picture_games.gd"]
 assert re.search(r'if kind == "slide":\s+.*?m\._l2_start_slide\(\).*?\n\t\treturn',picture,re.S),"slide diversion missing"
 assert picture.index('if kind == "slide":')<picture.index('elif kind == "slide": _mg_build_slide()')
 main=source_text["scripts/main.gd"]
 entry=main[main.index("func _enter_level2_now("):main.index("func _enter_northern_kingdom(")]
 assert '_lagoon_promenade_ref().build(' in entry and '_build_pearl_castle(' not in entry
 assert entry.rstrip().endswith("return"),"current entry early return missing"
 assert 'm.g["phase"] = "promenade"' in source_text["scripts/arena/sky_lagoon_promenade.gd"]
 assert 'call_deferred("_start_game", fairy_fr)' in main and '"game": "fairyshoot"' in main,"deferred launcher missing"
 craft_refs=[r for r in refs if "_open_craft_studio" in r["tokens"] and r["lane"]=="PRODUCTION_SOURCE"]
 assert [(r["path"],r["line"]) for r in craft_refs]==[("scripts/craft_studio.gd",40),("scripts/main.gd",7288),("scripts/main.gd",7289)]
 routes=get("ROUTE_REVIEW.json");assert routes["native_frames_added"]==0
 assert {r["id"] for r in routes["routes"]}=={"craft_studio","picture_suite","retired_picture_slide_builder","retained_friend_games"}
 for row in routes["routes"]:
  for name,a,b in row["source_anchors"]:
   assert name in paths and 0<a<=b<=len(source_text[name].splitlines()),"unbound source anchor"
 friend=next(r for r in routes["routes"] if r["id"]=="retained_friend_games")
 assert "fairy_fr(game=fairyshoot)" in friend["retained_api"],"deferred launch erased from route summary"
 assert next(r for r in routes["routes"] if r["id"]=="retired_picture_slide_builder")["normal_route"]=="BYPASSED_BY_EARLY_RETURN_IN_ORDINARY_OPENER"
 scopes=get("SCOPE_ROUTE_REVIEW.json");assert scopes["visual_classification_added"]==0 and scopes["no_dormancy_exemption"] is True
 assert len(scopes["scopes"])==6 and {r["scope_id"] for r in scopes["scopes"]}==IDS
 original_scopes=json.loads((P.parent.parent/"source_scopes.json").read_text(encoding="utf-8"))["scopes"]
 for row in scopes["scopes"]:
  old=next(r for r in original_scopes if r["id"]==row["scope_id"])
  assert (row["path"],row["function"],row["lines"])==(old["path"],old["scope"],[old["start_line"],old["end_line"]])
  assert row["fully_dispositioned_for_inventory"] is False and row["individual_piece_count"] is None and row["current_visible_piece_count"] is None
  assert row["status"]=="SOURCE_ROUTE_REVIEW_ONLY_VISUAL_UNRESOLVED","dormancy visual exemption"
 backlog=get("FRIEND_SCOPE_BACKLOG.json");assert backlog["scope_count"]==len(backlog["scopes"])==27
 assert len({r["scope_id"] for r in backlog["scopes"]})==27
 assert all(r["fully_dispositioned"] is False and r["individual_piece_count"] is None for r in backlog["scopes"])
 briefs=get("SOURCE_ROLE_BRIEFS.json");assert len(briefs["role_briefs"])==37 and briefs["all_game_individual_piece_total"] is None
 assert len({r["id"] for r in briefs["role_briefs"]})==37
 assert len([r for r in briefs["role_briefs"] if r["id"].startswith("craft.swatch.")])==8
 assert len([r for r in briefs["role_briefs"] if r["id"].startswith("picture.retired_slide.band.")])==6
 assert all(r["source_only"] is True and r["replacement_or_acceptance"] is False and r["current_visible_individual_piece_count"] is None for r in briefs["role_briefs"])
 baseline=P.parent/"room_routes"
 for n,key in [("CUMULATIVE_COVERAGE.json","entries"),("CUMULATIVE_SCOPES.json","scopes")]:
  old=json.loads((baseline/n).read_text(encoding="utf-8"));new=get(n)
  assert len(old[key])==len(new[key])
  for a,b in zip(old[key],new[key]):
   assert all(b[k]==v for k,v in a.items()),"prior native status/capture altered"
  for k,v in old.items():
   if k not in {key,"note"}:assert new[k]==v,"scope/coverage tally drift"
 cov=get("CUMULATIVE_COVERAGE.json");assert sum(r["status"].startswith("PARTIAL") for r in cov["entries"])==62
 assert sum(bool(r.get("route_or_saved_variants_complete")) for r in cov["entries"])==0
 return {"status":"PASS","measured_source_files":349,"identifier_occurrences":382,"exact_source_proofs":46,"source_route_reviews":6,"retained_friend_scope_backlog":27,"source_role_briefs":37,"new_frames":0,"visual_classifications_added":0,"acceptance":False}
def stress():
 cases=[]
 def mutate(name,label,change):
  d=read(name);change(d);cases.append((label,{name:d},{}))
 mutate("MACHINE.json","inflated_native_frames",lambda d:d.update(native_frames_added=1))
 mutate("MACHINE.json","false_visual_classification",lambda d:d.update(classified_visual_scopes=16,unresolved_scopes=353))
 mutate("MACHINE.json","false_all_game_total",lambda d:d.update(all_game_individual_piece_total=37))
 mutate("REFERENCE_SCAN.json","omitted_deferred_launch",lambda d:d["references"].__setitem__(slice(None),[r for r in d["references"] if not (r["path"]=="scripts/main.gd" and r["line"]==2349)]))
 mutate("REFERENCE_SCAN.json","archive_mislabeled_production",lambda d:next(r for r in d["references"] if r["path"].startswith("backups/")).update(lane="PRODUCTION_SOURCE"))
 mutate("REFERENCE_SCAN.json","missing_source_corpus_file",lambda d:d["corpus"].pop())
 mutate("SCOPE_ROUTE_REVIEW.json","dormancy_exemption",lambda d:d["scopes"][0].update(fully_dispositioned_for_inventory=True))
 mutate("FRIEND_SCOPE_BACKLOG.json","accepted_child_via_parent",lambda d:d["scopes"][0].update(fully_dispositioned=True))
 mutate("SOURCE_ROLE_BRIEFS.json","source_bands_claimed_visible",lambda d:next(r for r in d["role_briefs"] if r["id"]=="picture.retired_slide.band.0").update(current_visible_individual_piece_count=1))
 mutate("CUMULATIVE_COVERAGE.json","dormant_entry_complete",lambda d:next(r for r in d["entries"] if r["id"]=="game.pic_slide").update(route_or_saved_variants_complete=True))
 b=(P/"sources/scripts/games/picture_games.gd").read_bytes().replace(b'\t\treturn',b'\t\tpass',1)
 cases.append(("archive_early_return_changed",{},{"sources/scripts/games/picture_games.gd":b}))
 results=[]
 for label,overrides,raw in cases:
  try:check(overrides,raw)
  except (AssertionError,KeyError,ValueError) as e:results.append({"control":label,"rejected":True,"reason":str(e)[:180]})
  else:raise RuntimeError("accepted falsification "+label)
 return results
if __name__=="__main__":
 ap=argparse.ArgumentParser();ap.add_argument("--stress",action="store_true");args=ap.parse_args()
 result=check()
 if args.stress:result["falsification_controls"]=stress()
 print(json.dumps(result,ensure_ascii=False,indent=2))
