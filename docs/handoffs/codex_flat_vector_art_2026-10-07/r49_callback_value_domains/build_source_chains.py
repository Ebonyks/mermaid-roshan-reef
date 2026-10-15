"""Validate finite callback bindings on named source paths, without global closure."""
from pathlib import Path
import json,hashlib,subprocess
P=Path(__file__).resolve().parent;R=P.parents[3];BASE="61d12c5b7d29cd106a817d8d0064aa60f48f3ed2"
def rd(p):return json.loads(p.read_text(encoding="utf-8"))
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 c=rd(P/"MUTATION_CENSUS.json");domains=rd(P/"CALLBACK_DOMAINS.json");rows=c["rows"];byid={x["id"]:x for x in rows};assert len(byid)==len(rows)==922
 old=rd(P.parent/"r45_dispatch_semantics_audit/DISPATCH_SEMANTICS.json")["records"]
 inv=[x for x in rows if x["kind"]=="DISPATCH_INVOCATION_CANDIDATE"]
 assert {x["r45_binding_id"] for x in inv}=={x["binding_id"] for x in old if x["classification"]["invocation_expression"]}
 assert len(inv)==338 and all(x["target_method_inferred"] is False for x in inv)
 def one(**criteria):
  found=[x for x in rows if all(x.get(k)==v for k,v in criteria.items())];assert len(found)==1,criteria;return found[0]
 owner=one(kind="NAMED_WRITE",field="touch_ui",path="scripts/main.gd",function="_ready")
 assert owner["value_AST"]=='getattr_call\n  getattr\n    standalone_call\n      preload\n      string\t"res://scripts/touch_ui.gd"\n    .\n    new'
 open_=one(kind="API_CALLER",path="scripts/games/dust_boss.gd",function="_stage_open");reset=one(kind="API_CALLER",path="scripts/games/dust_boss.gd",function="stage_close")
 assert open_["arguments_AST"]==["on_world_tap","_cancel_world_move","on_world_drag"] and reset["arguments_AST"]==[]
 royal=one(kind="API_CALLER",path="scripts/day_one_flow.gd",function="_day_one_arm_boss_door")
 assert royal["arguments_AST"]==['string\t"day_one_giant_dust_bunny"',"_day_one_trigger_boss"]
 def method(path,name):
  raw=subprocess.check_output(["git","show",BASE+":"+path],cwd=R,stderr=subprocess.PIPE);s=raw.decode("utf-8-sig");a=s.index("func "+name+"(");b=s.find("\nfunc ",a+1);b=len(s) if b<0 else b;body=s[a:b]
  return {"path":path,"revision":BASE,"function":name,"file_sha256":sha(raw),"body_sha256":sha(body.encode()),"start_line":s[:a].count("\n")+1,"end_line":s[:b].count("\n")+1,"body":body}
 setter=method("scripts/touch_ui.gd","set_encounter_controls");assert setter["body"].index("_clear_touch_state()")<setter["body"].index("encounter_press = press")
 for param in ["press","cancel","motion"]:assert param+": Callable = Callable()" in setter["body"]
 activate=method("scripts/arena/castle_rooms_25d.gd","_activate_royal_hall_event")
 assert activate["body"].index("var entry: Callable = m.castle_royal_hall_event_entry")<activate["body"].index("clear_royal_hall_event(event_id, expected_event_generation)")<activate["body"].index("entry.call()")
 arm=method("scripts/arena/castle_rooms_25d.gd","arm_royal_hall_event");clear=method("scripts/arena/castle_rooms_25d.gd","_force_clear_royal_hall_event")
 assert "m.castle_royal_hall_event_entry = entry" in arm["body"] and "m.castle_royal_hall_event_entry = Callable()" in clear["body"]
 chains=[]
 for d in domains["ports"]:
  field=d["stored_field"];target=d["standard_target"];ids=[];steps=[]
  if field.startswith("world_"):
   write=one(kind="NAMED_WRITE",field=field,path="scripts/main.gd",function="_init_touch_experiment")
   assert write["value_AST"]=='standalone_call\n  Callable\n  self\n  string\t"'+target["function"]+'"'
   ids=[owner["id"],write["id"]];steps=["Main._ready explicitly constructs the TouchUI component", "Main._init_touch_experiment directly stores Callable(self, named Main method) on that source path", "TouchUI invokes the selected field only if valid"]
  elif field.startswith("encounter_"):
   param=field.removeprefix("encounter_");write=one(kind="NAMED_WRITE",field=field,path="scripts/touch_ui.gd",function="set_encounter_controls");assert write["value_AST"]==param
   slot={"press":0,"cancel":1,"motion":2}[param];assert open_["arguments_AST"][slot]==target["function"]
   ids=[owner["id"],open_["id"],write["id"],reset["id"]];steps=["DustBoss._stage_open passes three named bound methods to the shared component", "Setter clears the prior input owner before storing parameters", "DustBoss.stage_close uses empty Callable defaults to reset the three fields", "Actual headless component protocol proof uses synthetic receivers; it does not execute DustBoss/Main"]
  else:
   ids=[royal["id"],one(kind="NAMED_WRITE",path="scripts/arena/castle_rooms_25d.gd",function="arm_royal_hall_event",field=field)["id"],one(kind="NAMED_WRITE",path="scripts/arena/castle_rooms_25d.gd",function="_force_clear_royal_hall_event",field=field)["id"]]
   steps=["DayOneFlow passes its bound _day_one_trigger_boss method with the named event ID", "CastleRooms validates and stores the passed Callable on the referenced Main field", "Default activation copies the callback locally, clears the one-shot hook, then invokes the local", "Source relation only in this revision; no new Royal Hall runtime test"]
  assert set(d["invocation_ids"])<={x["r45_binding_id"] for x in inv}
  chains.append({"port_id":d["port_id"],"invocation_ids":d["invocation_ids"],"stored_field":field,"named_target":target,"write_caller_evidence_ids":ids,"steps":steps,"conditional_scope":"Only when the shown receiver/owner path is the active path and no intervening alternate mutation changes it", "all_alias_write_caller_resource_runtime_domains_closed":False})
 callers=[x for x in rows if x["kind"]=="API_CALLER"];probe=[x["id"] for x in callers if x["path"]=="scripts/probe_throne.gd"];assert len(callers)==15 and len(probe)==12
 mutators=[x for x in rows if x["kind"]=="PROPERTY_MUTATOR"];assert len(mutators)==25 and sum(x["property"] is None for x in mutators)==6
 out={"baseline":BASE,"status":"NINE_NAMED_SOURCE_PATHS_BOUND_FULL_CLOSURE_OPEN","chains":chains,"source_order_evidence":[setter,arm,clear,activate],"all_API_caller_evidence_ids":[x["id"] for x in callers],"probe_only_API_caller_ids":probe,"probe_limit":"12 probe_throne API sites include arbitrary synthetic bindings, invalid IDs/defaults and rearm; kept as alternate callers, not normal gameplay or closed domains.","mutation_risks":{"computed_index_writes":523,"indirect_invocations":338,"mutator_shaped_calls":25,"unknown_property_names":6,"unknown_property_groups":["FairyConservatoryDoor._set_flag key","DungeonLevel progress_field/done_field","probe_passive snapshot keys"],"limits":"Literal selected callback/resource symbol absence is not alias/native/generated-string absence. Receiver overrides, setter method values, external scripts/resources and save/input route states remain open."},"R45_invocation_ID_parity":338,"selected_invocation_sites":14,"outside_selected_subset":43,"full_runtime_domains_open":57,"new_artwork_credit":0,"accepted_removed":0}
 (P/"NAMED_SOURCE_PATH_CHAINS.json").write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8",newline="\n");print("R49_NAMED_CHAINS",len(chains),"14 sites;338 R45 invocation IDs preserved;57 full runtime domains open",flush=True)
if __name__=="__main__":main()
