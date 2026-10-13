"""Fail-closed native/source inventory checks; never grants visual acceptance."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from immutable_source import source_bytes
from functools import lru_cache
import argparse, copy, hashlib, json, re, subprocess
from PIL import Image
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from json_evidence import read_json
P = Path(__file__).resolve().parent
R = P.parents[4]
H = "6cde8aeae04aaedcc0b1ff22a05ef93ab9bf666f"
HARNESS = "b80324413d0bea97aff9b56b039eb13169fdcb98209dc1f7c2934d13f162a0b3"
CASES = ["post_day", "post_night", "dayone_day", "dayone_night"]
ASPECTS = ["1280x720", "1600x720"]
TOYS = ["slide", "swing", "seesaw"]
SUFFIXES = ["idle", "pressed", "focus", "focus_late", "ground_cancel", "pause_resumed", "action", "settled"]
MATRIX = ["saved_entry", "runway_arrival", "runway_departed", "runway_saved_reentry", "playground_overview"] + [t+"_"+s for t in TOYS for s in SUFFIXES] + ["castle_idle", "castle_focus", "castle_ground_cancel"]
RING = "FVF-3D0E22645108"
POINTER = "FVF-CE72B2B6035D"
ARCH = "assets/sprites/sky_lagoon/sky_lagoon_castle_door_focus_v1.png"
TOKENS = ["_affordance_diamond_texture", "_add_affordance_pointer", "_register_target"]
RULES = [
 {"root":"assets","suffixes":[".bmp",".dds",".exr",".gdshader",".hdr",".import",".jpeg",".jpg",".json",".ktx",".mp3",".ogg",".ogv",".png",".res",".tres",".svg",".tga",".uid",".wav",".webp"]},
 {"root":"scenes","suffixes":[".res",".tres",".tscn",".uid"]},
 {"root":"scripts","suffixes":[".gd",".uid",".json"]},
 {"root":"shaders","suffixes":[".gdshader",".uid"]}]
def sha(b): return hashlib.sha256(b).hexdigest()
def read(n): return read_json(P/n)
def safe(base, name):
 p = (base/name).resolve()
 assert p.is_relative_to(base.resolve()), "unsafe evidence path"
 return p
@lru_cache(maxsize=None)
def original(n): return source_bytes(R,H,n)
@lru_cache(maxsize=None)
def artifact(n):
 p=safe(P,n); b=p.read_bytes()
 with Image.open(p) as im:
  im.load(); dims=list(im.size)
 return sha(b),len(b),dims
@lru_cache(maxsize=None)
def current_signature():
 paths=["project.godot","tools/audit_opera_capture.py","tools/audit_godot_baseline.py","tools/godot_baseline.json"]
 for rule in RULES:
  paths += [p.relative_to(R).as_posix() for p in (R/rule["root"]).rglob("*") if p.is_file() and p.suffix in rule["suffixes"]]
 paths.sort(); files={n:sha(safe(R,n).read_bytes()) for n in paths}
 return {"algorithm":"sha256_runtime_roots_promenade_v1","files":files,"paths":paths,"missing":[],"tree_rules":RULES,"sha256":sha("\n".join(n+":"+files[n] for n in paths).encode())}
@lru_cache(maxsize=None)
def caller_scan():
 names=subprocess.check_output(["git","ls-files","-z"],cwd=R).decode().split("\0")
 corpus=[]; refs=[]; pattern=re.compile(r"\b(?:"+"|".join(map(re.escape,TOKENS))+r")\b")
 for n in sorted(names):
  p=R/n
  if not p.is_file() or n.startswith(("docs/","audit/","design/","assets_src/","disabled_addons/")) or p.suffix not in {".gd",".tscn",".tres",".godot",".gdshader"}: continue
  b=p.read_bytes();corpus.append({"path":n,"working_sha256":sha(b),"bytes":len(b)})
  for i,line in enumerate(b.decode("utf-8-sig").splitlines(),1):
   tokens=sorted(set(pattern.findall(line)))
   if tokens: refs.append({"path":n,"line":i,"tokens":tokens,"text":line,"lane":"HISTORICAL_BACKUP_REFERENCE" if n.startswith("backups/") else ("TEST_PROBE" if "/probe" in "/"+n else "PRODUCTION_SOURCE")})
 return corpus,refs
@lru_cache(maxsize=None)
def raw_native(n): return read(n)
def near(a,b):
 if isinstance(b,list): return isinstance(a,list) and len(a)==len(b) and all(near(x,y) for x,y in zip(a,b))
 if isinstance(b,(float,int)): return isinstance(a,(float,int)) and abs(a-b)<1e-5
 return a==b

def check(overrides=None):
 overrides=overrides or {}
 def get(n): return copy.deepcopy(overrides[n]) if n in overrides else read(n)
 m=get("MACHINE.json")
 exact={"source_revision":H,"engine":"4.7.2.stable.official.ed1daf0bf","renderer":"mobile","quality":"speedy","aspects":ASPECTS,"saved_variants":CASES,"native_processes":8,"new_native_frames":256,"boards":16,"cumulative_staged_frames":1434,"R6_total_staged_new_frames":830,"partial_entries":66,"complete_entries":0,"classified_scopes":12,"unresolved_scopes":357,"new_scope_classifications":2,"finite_named_flat_cue_roles":10,"flat_caller_roles_in_new_scopes":9,"new_visible_raster_role_outside_primitive_scopes":1,"cumulative_flat_named_role_contexts":129,"all_game_individual_piece_total":None,"source_fingerprint_files":6444,"source_fingerprint_algorithm":"sha256_runtime_roots_promenade_v1","normal_child_saves_unchanged":True,"production_unchanged":True,"replacements":0,"accepted_removals":0,"DL_QA_11":False,"visual_device_child_owner_acceptance":False,"publication":"UNPUBLISHED_HANDOFF_BLOCKED"}
 for k,v in exact.items(): assert m[k]==v,(k,"claim drift")
 assert get("EXPECTED_MATRIX.json")=={c:MATRIX for c in CASES},"native matrix drift"
 assert sha((P.parent/"capture_promenade.gd").read_bytes())==HARNESS,"executed harness drift"
 sp=get("SOURCE_PROOFS.json"); assert sp["revision"]==H and len(sp["sources"])==14
 assert {r["path"] for r in sp["sources"]}=={'scripts/chapter_two_director.gd', 'scripts/arena/sky_lagoon_layout.json', 'scripts/arena/sky_lagoon_promenade.gd', 'scripts/probe_sky_lagoon_art.gd', 'scripts/living_world_catalog.gd', 'scripts/day_one_flow.gd', 'scripts/main.gd', 'scripts/interaction_affordance.gd', 'scripts/touch_ui.gd', 'scripts/save_state.gd', 'scripts/pause_menu.gd', 'scripts/probe_sky_lagoon_animals.gd', 'scripts/day_one_director.gd', 'scripts/probe_start_menu_routing.gd'}
 texts={}
 for r in sp["sources"]:
  n=r["path"]; b=original(n);assert sha(b)==r["git_lf_sha256"] and safe(P,r["packet_path"]).read_bytes()==b,"source archive mismatch"
  current=safe(R,n).read_bytes();assert sha(current)==r["working_tree_sha256"] and current.replace(b"\r\n",b"\n")==b,"source changed"
  texts[n]=b.decode("utf-8-sig")
 assert "scripts/arena/sky_lagoon_layout.json" in texts
 scan=get("CALLER_PROOFS.json"); corpus,refs=caller_scan()
 assert scan["tokens"]==TOKENS and scan["corpus"]==corpus and scan["references"]==refs
 assert scan["measured_corpus_count"]==len(corpus)==349 and len(refs)==11,"caller corpus drift"
 code=texts["scripts/arena/sky_lagoon_promenade.gd"]
 concrete=[r for r in refs if r["lane"]=="PRODUCTION_SOURCE" and '_register_target("' in r["text"]]
 assert [r["line"] for r in concrete]==[549,550,551,602]
 assert [re.search(r'_register_target\("(.*?)"',r["text"]).group(1) for r in concrete]==TOYS+["castle_gate"]
 assert 'var pointer_tip := Vector2(0.0, 128.0)' in code and '_add_affordance_pointer(glow, pointer_tip)' in code
 signature=current_signature();assert len(signature["files"])==6444 and signature["missing"]==[]
 launch=get("CAPTURE_LAUNCH.json"); runs=launch["runs"]
 assert len(runs)==8 and {(r["case"],r["aspect"]) for r in runs}=={(c,a) for c in CASES for a in ASPECTS}
 assert all(r["source_revision"]==H and r["harness_sha256"]==HARNESS and r["exit_code"]==0 and r["parent_normal_save_unchanged_after_exit"] is True and r["ended_at_utc"]>r["started_at_utc"] for r in runs)
 caps=get("CAPTURES.json");assert caps["native_count"]==len(caps["frames"])==256 and len(caps["manifests"])==8
 assert {(r["case"],r["aspect"]) for r in caps["manifests"]}=={(c,a) for c in CASES for a in ASPECTS},"duplicate/missing native matrix manifest"
 frame_map={(r["case"],r["aspect"],r["state"]):r for r in caps["frames"]}
 assert len(frame_map)==256 and set(frame_map)=={(c,a,s) for c in CASES for a in ASPECTS for s in MATRIX}
 states={}; total=0
 for row in caps["manifests"]:
  c=row["case"]; aspect=row["aspect"]; dims=[int(x) for x in aspect.split("x")];path=row["path"]
  b=safe(P,path).read_bytes();assert sha(b)==row["sha256"] and len(b)==row["bytes"]<4*1024**2,"native metadata hash/cap"
  n=copy.deepcopy(overrides[path]) if path in overrides else raw_native(path)
  assert n["schema"]=="reef.flat_vector.promenade.v1" and n["source_revision"]==H and n["run_case"]==c and n["harness_sha256"]==HARNESS
  assert n["engine"]=={"build":"official","major":4,"minor":7,"patch":2,"status":"stable","version_string":"4.7.2-stable (official)"}
  assert n["renderer"]=="mobile" and n["quality"]=="speedy" and n["display_server"]!="headless" and n["aspect"]==dims
  assert n["result"]=="PASS" and n["failures"]==0 and all(x["pass"] is True for x in n["checks"])
  assert n["expected_ids"]==MATRIX and [r["id"] for r in n["states"]]==MATRIX
  assert n["source_signature"]==signature and n["source_unchanged"] is True,"native source fingerprint missing/drift"
  si=n["save_isolation"];assert si["unchanged"] is True and si["before"]==si["after"] and len(si["before"])==8
  assert si["fresh_fixture_save"]!=si["normal_save_file"] and "/profiles/" in si["fresh_fixture_save"],"save isolation drift"
  for i,s in enumerate(n["states"]):
   sid=s["id"];a=s["actual"];f=frame_map[(c,aspect,sid)];states[(c,aspect,sid)]=s
   assert s["status"]=="PASS" and s["sequence"]==f["sequence"]==i
   assert f["path"]==f"native/{c}/{aspect}/{sid}.png" and f["dimensions"]==dims
   digest,size,image_dims=artifact(f["path"]);total+=size
   assert digest==f["sha256"]==s["image"]["sha256"] and image_dims==dims and size==s["image"]["bytes"]
   assert s["image"]["file"]==sid+".png" and [s["image"]["width"],s["image"]["height"]]==dims
   for k,v in s["expected"].items(): assert a[k]==v,(sid,k,"expected-state mismatch")
   for k,v in {"game":"level2","phase":"promenade","tree_paused":False,"start_menu_active":False,"intro_active":False,"story_clip_present":False,"fade_alpha":0,"normal_hud_visible":True,"player_hidden":True,"camera2d_current":True,"camera3d_current":False,"night":c.endswith("night"),"day_one_active":c.startswith("dayone"),"plays":2 if c.endswith("night") else 1,"firefly_count":18 if c.endswith("night") else 0,"save_path":si["fresh_fixture_save"]}.items(): assert a[k]==v,(sid,k,"fixture drift")
   assert a["plane_departed_save"]==(sid not in {"saved_entry","runway_arrival"}),"departure/reload not bound"
   assert [t["id"] for t in a["targets"]]==TOYS+["castle_gate"]
   for t in a["targets"]:
    assert t["glow_visible"] is True
    if t["id"] in TOYS:
     texture=t["texture"]
     for k,v in {"class":"GradientTexture2D","width":192,"height":192,"fill":1,"fill_from":[.5,.5],"fill_to":[1,.5],"gradient_offsets":[0,.5,1],"gradient_colors":[[1,1,1,0],[1,1,1,.98],[1,1,1,0]]}.items():assert near(texture[k],v),"gradient shape drift"
     assert t["kind"]=="playground" and t["pointer_tip"]==[0,128] and len(t["children"])==2
     for child,name,points,color in zip(t["children"],["PointerOutline","PointerFill"],[[[-32,70],[32,70],[18,101],[0,128],[-18,101]],[[-22,75],[22,75],[11,99],[0,119],[-11,99]]],[[.1,.16,.34,.96],[1,1,1,1]]):
      assert child["name"]==name and child["points"]==points and near(child["color"],color) and child["visible"] is True and len(child["screen_points"])==5,"pointer topology/color drift"
    else:
     assert t["texture"]=={"class":"CompressedTexture2D","height":228,"path":"res://"+ARCH,"width":199} and t["children"]==[],"visible raster role drift"
    alpha=t["glow_modulate"][3]
    if a["focus"]==t["id"]: assert .82-1e-5<=alpha<=1.00001,"selected cue absent"
    elif t["id"]!="castle_gate" or not c.startswith("dayone"): assert abs(alpha-.055)<1e-5,"idle cue drift"
    else: assert .45-1e-5<=alpha<=1.00001,"Day One castle idle emphasis absent"
 assert total==472095862,"native bytes changed"
 obs=get("EXACT_OBSERVATIONS.json");assert len(obs["observations"])==256 and obs["full_natural_child_progression"] is False
 assert {(o["case"],o["aspect"],o["state"]) for o in obs["observations"]}==set(states),"duplicate/missing native observation"
 for o in obs["observations"]:
  key=(o["case"],o["aspect"],o["state"]);s=states[key];a=s["actual"]
  assert o["native_sha256"]==s["image"]["sha256"] and o["targets"]==a["targets"],"observation/native detached"
  for k in ["focus","focus_t","plays","night","day_one_active","plane_departed_save","firefly_count","play_kind","play_phase","camera2d_current","camera3d_current"]:assert o[k]==a[k]
  assert o["hud_visible"]==a["normal_hud_visible"]
 boards=get("BOARDS.json");assert len(boards["boards"])==16 and boards["preview_only"] is True and boards["native_source_edits"] is False
 assert {(b["case"],b["aspect"],b["part"]) for b in boards["boards"]}=={(c,a,p) for c in CASES for a in ASPECTS for p in [1,2]},"duplicate/missing review board"
 for b in boards["boards"]:
  digest,size,dims=artifact(b["path"]);assert digest==b["sha256"] and dims==b["dimensions"]==[1280,904]
  assert [x["state"] for x in b["cells"]]==MATRIX[(b["part"]-1)*16:b["part"]*16]
  for cell in b["cells"]:
   f=frame_map[(b["case"],b["aspect"],cell["state"])];assert cell["source"]==f["path"] and cell["source_sha256"]==f["sha256"] and cell["source_dimensions"]==f["dimensions"]
   box=cell["thumbnail_bounds"];assert box[2:]==([320,180] if b["aspect"]=="1280x720" else [320,144]),"whole-canvas mapping drift"
 review=get("VISUAL_REVIEW.json");assert review["boards_inspected"]==len(review["boards"])==16 and len(review["full_native_spots"])==4 and review["DL_QA_11"] is False and review["device_child_owner_acceptance"] is False
 assert {(r["path"],r["sha256"]) for r in review["boards"]}=={(b["path"],b["sha256"]) for b in boards["boards"]}
 for s in review["full_native_spots"]: assert artifact(s["path"])[0]==s["sha256"] and s["replacement_or_acceptance"] is False
 reuse=get("REUSE_INVENTORY.json");assert len(reuse["sources"])==reuse["inspected_originals"]==5 and reuse["new_art"]==0
 for s in reuse["sources"]:
  b=safe(R,s["path"]).read_bytes();assert sha(b)==s["sha256"] and s["modified"] is False and s["new_pixels"] is False and s["manual_source_inspected"] is True
  with Image.open(safe(R,s["path"])) as im: assert list(im.size)==s["dimensions"]
 assert reuse["sources"][0]["status"]=="REJECTED_VECTOR_STYLE_RASTER_LOOKALIKE","PNG art exemption"
 with Image.open(R/ARCH) as im: assert im.mode=="RGBA" and im.size==(199,228) and im.getextrema()[:3]==((255,255),)*3
 briefs=get("INSTANCE_BRIEFS.json");roles=briefs["roles"]
 assert len(roles)==briefs["finite_named_cue_roles"]==10 and briefs["all_game_individual_piece_total"] is None and briefs["replacements"]==briefs["accepted_removals"]==0
 assert {r["id"] for r in roles}=={"promenade."+t+"."+r for t in TOYS for r in ["ring","pointer_outline","pointer_fill"]}|{"promenade.castle_gate.focus_arch"}
 for r in roles:
  assert r["named_context_instance_count"]==1 and r["unique_design_count"] is None
  assert r["status"].endswith("REQUIRES_PAINTED_REPLACEMENT"),"functional mask art exemption"
  expected_states=["castle_idle","castle_focus","castle_ground_cancel"] if r["target"]=="castle_gate" else [r["target"]+"_"+s for s in SUFFIXES]
  assert {(x["case"],x["aspect"],x["state"]) for x in r["bindings"]}=={(c,a,s) for c in CASES for a in ASPECTS for s in expected_states}
  assert len(r["bindings"])==8*len(expected_states),"duplicate role binding"
  for x in r["bindings"]:
   f=frame_map[(x["case"],x["aspect"],x["state"])];assert x["native_path"]==f["path"] and x["native_sha256"]==f["sha256"]
  if r["target"]=="castle_gate": assert r["source_scope"] is None and r["texture"]==ARCH
  else: assert r["source_scope"]==(RING if r["role"]=="ring" else POINTER)
 scopes=get("SCOPE_DISPOSITIONS.json");assert scopes["classification_only"] is True and len(scopes["scopes"])==2
 original_scopes=json.loads((P.parent.parent/"source_scopes.json").read_text(encoding="utf-8"))["scopes"]
 for s in scopes["scopes"]:
  assert s["scope_id"] in {RING,POINTER} and s["fully_dispositioned_for_inventory"] is True and s["acceptance"] is False and s["individual_unique_design_count"] is None
  assert s["status"]=="SOURCE_SCOPE_INVENTORY_CLASSIFIED_NOT_REMOVED","functional helper art exemption"
  original_scope=next(x for x in original_scopes if x["id"]==s["scope_id"])
  assert (s["source"],s["function"],s["lines"])==(original_scope["path"],original_scope["scope"],[original_scope["start_line"],original_scope["end_line"]]),"scope source authority detached"
  assert s["finite_named_flat_role_instances"]==(3 if s["scope_id"]==RING else 6)
  assert set(s["bindings"])=={r["id"] for r in roles if r["source_scope"]==s["scope_id"]}
 cov=get("CUMULATIVE_COVERAGE.json");assert len(cov["entries"])==cov["declared_overlapping_entries"]==176
 assert cov["partial_entries"]==sum(r["status"].startswith("PARTIAL") for r in cov["entries"])==66 and cov["complete_entries"]==0
 assert all(r["route_or_saved_variants_complete"] is False for r in cov["entries"]),"false complete entry"
 prior=json.loads((P.parent/"dormant_routes/CUMULATIVE_COVERAGE.json").read_text(encoding="utf-8"))
 changed={"sky.promenade_runway","sky.promenade_playground","sky.promenade_castle","game.sky_lagoon"}
 for old,new in zip(prior["entries"],cov["entries"]):
  assert old["id"]==new["id"]
  if old["id"] not in changed: assert old==new,"historical coverage changed"
  else: assert old["status"]=="COVERAGE_GAP" and new["status"].startswith("PARTIAL")
 cs=get("CUMULATIVE_SCOPES.json");assert len(cs["scopes"])==cs["source_scope_count"]==369 and cs["fully_resolved"]==sum(bool(s["fully_dispositioned"]) for s in cs["scopes"])==12
 prior=json.loads((P.parent/"dormant_routes/CUMULATIVE_SCOPES.json").read_text(encoding="utf-8"))
 for old,new in zip(prior["scopes"],cs["scopes"]):
  assert old["scope_id"]==new["scope_id"]
  if old["scope_id"] not in {RING,POINTER}:assert old==new,"historical scope changed"
  else: assert new["fully_dispositioned"] is True and new["individual_piece_count"] is None and new["instance_count"]==(3 if new["scope_id"]==RING else 6)
 return {"status":"PASS","native_processes":8,"native_frames":256,"boards":16,"source_files":6444,"caller_corpus":349,"caller_refs":11,"source_proofs":14,"flat_cue_roles":10,"inventory_classified_scopes":2,"cumulative_frames":1434,"partial_entries":66,"classified_scopes":12,"unresolved_scopes":357,"acceptance":False}

def stress():
 cases=[]
 def mutate(n,label,fn):
  d=read(n);fn(d);cases.append((label,{n:d}))
 mutate("MACHINE.json","unique_total_inflation",lambda d:d.update(all_game_individual_piece_total=129))
 mutate("MACHINE.json","false_accepted_removal",lambda d:d.update(accepted_removals=10))
 mutate("MACHINE.json","false_QA11_closure",lambda d:d.update(DL_QA_11=True))
 mutate("INSTANCE_BRIEFS.json","omit_visible_raster_role",lambda d:d["roles"].pop())
 mutate("INSTANCE_BRIEFS.json","functional_mask_exemption",lambda d:d["roles"][-1].update(status="FUNCTIONAL_MASK_ACCEPTED"))
 mutate("INSTANCE_BRIEFS.json","detach_native_binding",lambda d:d["roles"][0]["bindings"][0].update(native_sha256="0"*64))
 mutate("SCOPE_DISPOSITIONS.json","old_helper_instance_count",lambda d:d["scopes"][0].update(finite_named_flat_role_instances=1))
 mutate("CUMULATIVE_COVERAGE.json","partial_to_complete",lambda d:next(r for r in d["entries"] if r["id"]=="game.sky_lagoon").update(route_or_saved_variants_complete=True))
 mutate("REUSE_INVENTORY.json","PNG_style_exemption",lambda d:d["sources"][0].update(status="ACCEPTED_PAINTED_REUSE"))
 mutate("VISUAL_REVIEW.json","detach_board_review",lambda d:d["boards"][0].update(sha256="0"*64))
 mutate("EXACT_OBSERVATIONS.json","detach_native_observation",lambda d:d["observations"][0].update(native_sha256="0"*64))
 mutate("CAPTURES.json","duplicate_native_matrix",lambda d:d["manifests"].__setitem__(1,copy.deepcopy(d["manifests"][0])))
 mutate("EXACT_OBSERVATIONS.json","duplicate_observation_hides_state",lambda d:d["observations"].__setitem__(1,copy.deepcopy(d["observations"][0])))
 mutate("BOARDS.json","duplicate_board_hides_context",lambda d:d["boards"].__setitem__(1,copy.deepcopy(d["boards"][0])))
 mutate("SCOPE_DISPOSITIONS.json","wrong_scope_source_authority",lambda d:d["scopes"][0].update(function="_register_target"))
 mutate("SCOPE_DISPOSITIONS.json","functional_helper_exemption",lambda d:d["scopes"][0].update(status="FUNCTIONAL_MASK"))
 n="native/post_day/1280x720/capture_manifest.json"
 mutate(n,"active_layout_missing",lambda d:d["source_signature"]["files"].pop("scripts/arena/sky_lagoon_layout.json"))
 mutate(n,"story_parity_drift",lambda d:d["states"][0]["actual"].update(plays=2))
 mutate(n,"3D_current_camera",lambda d:d["states"][0]["actual"].update(camera3d_current=True))
 mutate(n,"hidden_normal_HUD",lambda d:d["states"][0]["actual"].update(normal_hud_visible=False))
 mutate(n,"wrong_pointer_vertices",lambda d:d["states"][0]["actual"]["targets"][0]["children"][0]["points"].pop())
 mutate(n,"normal_save_mutation",lambda d:d["save_isolation"]["after"].update({"":"0"*64}))
 results=[]
 for label,changes in cases:
  try: check(changes)
  except (AssertionError,KeyError,ValueError):results.append({"case":label,"result":"REJECTED"})
  else: raise AssertionError("falsification accepted: "+label)
 return results
if __name__=="__main__":
 parser=argparse.ArgumentParser();parser.add_argument("--stress",action="store_true");args=parser.parse_args()
 result=check()
 if args.stress:result["falsifications"]=stress();result["rejected_falsifications"]=len(result["falsifications"])
 print(json.dumps(result,indent=2))
