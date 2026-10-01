#!/usr/bin/env python3
"""Compile authored job records; accept only the commissioned JP1 save references."""
from __future__ import annotations
import argparse
from functools import lru_cache
import copy
import hashlib
import json
import math
import re
import subprocess
from pathlib import Path
try:
    from .content_gd_literals import CONSTRUCTORS, GDParser, read_const, read_python_list, opera_rows, mask_source
    from .content_source_refs import baseline_checkpoint_order, read_save_const, read_save_bounds, read_checkpoint_order
except ImportError:
    from content_gd_literals import CONSTRUCTORS, GDParser, read_const, read_python_list, opera_rows, mask_source
    from content_source_refs import baseline_checkpoint_order, read_save_const, read_save_bounds, read_checkpoint_order

BASELINE = "7f068cb80766edd52a110cc1cb3958158f829822"
COMPATIBILITY_CONTRACT = {'schema': 'job_compatibility/1', 'registries': [{'generated': 'PHASES', 'path': 'scripts/opera_career_world_2d.gd', 'source': 'PHASES', 'field': 'phases', 'type': 'Dictionary', 'kind': 'job_dictionary'}, {'generated': 'FINALE_START', 'path': 'scripts/opera_career_world_2d.gd', 'source': 'FINALE_START', 'field': 'finale_start', 'type': 'Dictionary', 'kind': 'job_dictionary'}, {'generated': 'PHASE_STATIONS', 'path': 'scripts/opera_career_world_2d.gd', 'source': 'PHASE_STATIONS', 'field': 'phase_stations', 'type': 'Dictionary', 'kind': 'job_dictionary'}, {'generated': 'HOTSPOT_PHASE_ALIASES', 'path': 'scripts/opera_career_world_2d.gd', 'source': 'HOTSPOT_PHASE_ALIASES', 'field': 'hotspot_aliases', 'type': 'Dictionary', 'kind': 'job_dictionary'}, {'generated': 'GOAL_PROPS', 'path': 'scripts/opera_career_world_2d.gd', 'source': 'GOAL_PROPS', 'field': 'presentation.goal_prop', 'type': 'Dictionary', 'kind': 'job_dictionary'}, {'generated': 'SLUGS', 'path': 'scripts/opera_career_world_2d.gd', 'source': 'SLUGS', 'field': 'legacy.slug', 'type': 'Dictionary', 'kind': 'job_dictionary'}, {'generated': 'LEGACY_PHASES', 'path': 'scripts/opera_career_world_2d.gd', 'source': 'LEGACY_PHASES', 'field': 'legacy.phases', 'type': 'Dictionary', 'kind': 'job_dictionary'}, {'generated': 'LEGACY_FINALE_START', 'path': 'scripts/opera_career_world_2d.gd', 'source': 'LEGACY_FINALE_START', 'field': 'legacy.finale_start', 'type': 'Dictionary', 'kind': 'job_dictionary'}, {'generated': 'COMPETITION_CAREERS', 'path': 'scripts/opera_competition.gd', 'source': 'CAREERS', 'field': 'competition', 'type': 'Dictionary', 'kind': 'job_dictionary'}, {'generated': 'MASTERY_RULES', 'path': 'scripts/opera_mastery.gd', 'source': 'RULES', 'field': 'mastery', 'type': 'Dictionary', 'kind': 'job_dictionary'}, {'generated': 'PRACTICE_COUNTS', 'path': 'scripts/opera_performance_plan.gd', 'source': 'PRACTICE_COUNTS', 'field': 'practice_count', 'type': 'Dictionary', 'kind': 'job_dictionary'}, {'generated': 'CAREER_COLORS', 'path': 'scripts/opera_performance_overlay.gd', 'source': 'CAREER_COLORS', 'field': 'presentation.colors.overlay', 'type': 'Dictionary', 'kind': 'job_dictionary'}, {'generated': 'HOTSPOT_EXPECTED_PHASES', 'path': 'scripts/opera_hotspot_catalog.gd', 'source': 'EXPECTED_PHASES', 'field': 'hotspot_expected_phases', 'type': 'Dictionary', 'kind': 'job_dictionary'}, {'generated': 'HOTSPOT_SPECS', 'path': 'scripts/opera_hotspot_catalog.gd', 'source': 'SPECS', 'field': 'hotspots', 'type': 'Dictionary', 'kind': 'job_dictionary'}, {'generated': 'BACKDROP_PALETTES', 'path': 'scripts/opera_world_backdrop_2d.gd', 'source': 'PALETTES', 'field': 'presentation.backdrop.palette', 'type': 'Dictionary', 'kind': 'job_dictionary'}, {'generated': 'STAGE_PATHS', 'path': 'scripts/opera_stage_paths.gd', 'source': 'PATHS', 'field': 'stage_geometry.paths', 'type': 'Dictionary', 'kind': 'job_dictionary'}, {'generated': 'STAGE_STATION_NAV', 'path': 'scripts/opera_stage_paths.gd', 'source': 'STATION_NAV', 'field': 'stage_geometry.station_nav', 'type': 'Dictionary', 'kind': 'job_dictionary'}, {'generated': 'STAGE_ROAM', 'path': 'scripts/opera_stage_paths.gd', 'source': 'ROAM', 'field': 'stage_geometry.roam', 'type': 'Dictionary', 'kind': 'job_dictionary'}, {'generated': 'STAGE_BLEED', 'path': 'scripts/opera_stage_paths.gd', 'source': 'BLEED', 'field': 'stage_geometry.bleed', 'type': 'Dictionary', 'kind': 'job_dictionary'}, {'generated': 'PHASE_SETS', 'path': 'scripts/chapter_two_career_scene_adapter.gd', 'source': 'PHASE_SETS', 'field': 'chapter2.scene', 'type': 'Dictionary', 'kind': 'job_dictionary'}, {'generated': 'VENUE_LEGACY_PORTAL_RECTS', 'path': 'scripts/opera_house_venue_2d.gd', 'source': 'LEGACY_PORTAL_RECTS', 'field': 'home.venue.legacy_portal', 'type': 'Dictionary', 'kind': 'bit_dictionary'}, {'generated': 'VENUE_CHAPTER2_PORTAL_RECTS', 'path': 'scripts/opera_house_venue_2d.gd', 'source': 'CHAPTER2_PORTAL_RECTS', 'field': 'home.venue.chapter2_portal', 'type': 'Dictionary', 'kind': 'bit_dictionary'}, {'generated': 'VENUE_CHAPTER2_SECOND_WAVE_PORTAL_RECTS', 'path': 'scripts/opera_house_venue_2d.gd', 'source': 'CHAPTER2_SECOND_WAVE_PORTAL_RECTS', 'field': 'home.venue.chapter2_second_wave_portal', 'type': 'Dictionary', 'kind': 'bit_dictionary'}]}
GENERATED = Path("scripts/generated/job_catalog_data.gd")
CAPABILITIES = {"hide_partner", "roshan_actor_atlas", "nursery_catch_overlay", "two_act_show", "uses_room_tiles", "cooperative_win_suffix"}
SHARED = [
 ("ACTS","opera_house","ACTS","Array"),
 ("LIVE_ACT_INDICES","opera_house","LIVE_ACT_INDICES","Array[int]"),
 ("RETIRED_ACT_INDICES","opera_house","RETIRED_ACT_INDICES","Array[int]"),
 ("ACTIVE_STAR_MASK","opera_house","ACTIVE_STAR_MASK","int"),
 ("RETIRED_STAR_MASK","opera_house","RETIRED_STAR_MASK","int"),
 ("ACTIVE_ACT_COUNT","opera_house","ACTIVE_ACT_COUNT","int"),
 ("OPERA_ACTIVE_STAR_MASK","save_state","OPERA_ACTIVE_STAR_MASK","int"),
 ("OPERA_ACTIVE_ACT_COUNT","save_state","OPERA_ACTIVE_ACT_COUNT","int"),
 ("ROOM_ACT_INDICES","castle_career_routes","ROOM_ACT_INDICES","Dictionary"),
 ("CAREER_CREST_FILES","castle_career_routes","CAREER_CREST_FILES","Dictionary"),
 ("MASTERY_CAREERS","opera_mastery","CAREERS","Array[String]"),
 ("PERFORMANCE_ENABLED","opera_performance_plan","ENABLED","Array[String]"),
 ("HOTSPOT_ASSET_META","opera_hotspot_catalog","ASSET_META","Dictionary"),
 ("VENUE_FLOOR_NAMES","opera_house_venue_2d","FLOOR_NAMES","Array[String]"),
 ("VENUE_FLOOR_ACTOR_POSITIONS","opera_house_venue_2d","FLOOR_ACTOR_POSITIONS","Array[Vector2]"),
 ("VENUE_LEGACY_FLOOR_ACT_INDICES","opera_house_venue_2d","LEGACY_FLOOR_ACT_INDICES","Array[int]"),
 ("EXPECTED_STAGE_COUNT","living_world_catalog","EXPECTED_STAGE_COUNT","int"),
 ("LIVE_CAREERS","chapter_two_party_plan","LIVE_CAREERS","Array[Dictionary]"),
 ("ALL_PARTY_MASK","chapter_two_party_plan","ALL_PARTY_MASK","int"),
 ("GUIDE_ORDER","chapter_two_party_plan","GUIDE_ORDER","Array[int]"),
 ("VALID_MODES","chapter_two_career_scene_adapter","VALID_MODES","Array"),
 ("ADAPTER_CAREER_ORDER","chapter_two_career_scene_adapter","CAREER_ORDER","Array"),
]
DIRECTOR = ["ACT_CHEF","ACT_DETECTIVE","ACT_BALLERINA","ACT_CANDY_MAKER",
 "ACT_FARMER","ACT_PAINTER","ACT_ASTRONAUT","ACT_POP_STAR",
 "SKILL_CHEF","SKILL_DETECTIVE","SKILL_BALLERINA","SKILL_CANDY_MAKER",
 "SKILL_FARMER","SKILL_PAINTER","SKILL_ASTRONAUT","SKILL_POP_STAR",
 "INITIAL_TUTORIAL_ACTS","INITIAL_TUTORIAL_MASK","FIRST_WAVE_UNLOCK_MASK",
 "JOB_PHASE_ACTS","JOB_PHASE_MASK_LIMITS"]


def _json(path):
    def reject(value): raise ValueError("non-finite JSON number "+value)
    def pairs(items):
        result={}
        for key,value in items:
            if key in result:raise ValueError("duplicate JSON key "+key)
            result[key]=value
        return result
    return json.loads(path.read_text(encoding="utf-8-sig"),parse_constant=reject,object_pairs_hook=pairs)


def load_catalog(root: Path):
    root=Path(root)
    return {"ledger":_json(root/"content/jobs/_ledger.json"),
      "jobs":[_json(p) for p in sorted((root/"content/jobs").glob("*.json")) if not p.name.startswith("_")],
      "config":_json(root/"content/catalog.json"),
      "compatibility":_json(root/"content/compatibility.json")}


def _field(row,path):
    value=row
    for key in path.split("."):
        if not isinstance(value,dict) or key not in value:return None
        value=value[key]
    return value


def _ordered_jobs(catalog):
    return sorted(catalog["jobs"],key=lambda j:(j["star_bit"],j["id"]))


def _table(catalog,name,field,bit_keys=False):
    rows=sorted((j for j in catalog["jobs"] if name in j["compat_order"]),key=lambda j:j["compat_order"][name])
    pairs=[[j["star_bit"] if bit_keys else j["id"],_field(j,field)] for j in rows]
    return {"__dict__":pairs} if bit_keys else dict(pairs)


def _exact_paths(job,event):
    suffix=event.removeprefix("roshan_")
    speaker=job["voice"].get("event_speakers",{}).get(suffix,job["voice"]["speaker"])
    key=speaker+"_"+suffix
    if speaker=="faron":return ["res://assets/audio/voices/"+key+".ogg"]
    if suffix.startswith("teacher_"):
        return ["res://assets/audio/teacher/"+key+".ogg","res://assets/audio/teacher/"+suffix+".ogg"]
    return [folder+key+".ogg" for folder in [job["voice"]["folder"]]+job["voice"]["fallback_folders"]]


def _checkpoint_data(catalog):
    specs={}
    for job in _ordered_jobs(catalog):
        cp=job["save"]["checkpoint"]
        if cp:specs[job["id"]]={**cp,"phase_index_max":len(job["phases"])}
    key_lists={name:[cp["key"] for cp in specs.values() if name in cp["registration_lists"]] for name in ("DICTIONARY_KEYS","KNOWN_KEYS")}
    prefix=catalog["config"]["save_checkpoint_normalization_prefix"]
    return {"SAVE_CHECKPOINTS":specs,"SAVE_CHECKPOINT_KEY_LISTS":key_lists,
        "SAVE_CHECKPOINT_JOB_ORDER":[*prefix,*(jid for jid in specs if jid not in prefix)]}


def derive(catalog):
    jobs=_ordered_jobs(catalog)
    ledger=catalog["ledger"]["entries"]
    live=[j for j in jobs if j["status"]=="LIVE"]
    aliases={a:e["id"] for e in ledger for a in e.get("aliases",[])}
    lookup={j["id"]:j for j in jobs}
    runtime_jobs={}
    for job in jobs:
        runtime=copy.deepcopy(job)
        runtime["aliases"]=[a for a,jid in aliases.items() if jid==job["id"]]
        runtime_jobs[job["id"]]=runtime
    result={"JOBS":runtime_jobs,"ALIASES":aliases,"LEDGER":copy.deepcopy(ledger)}
    live_bits=[j["star_bit"] for j in live]
    retired_bits=[e["star_bit"] for e in ledger if e["status"]=="TOMBSTONE"]
    slots=max(e["star_bit"] for e in ledger)+1 if ledger else 0
    result.update({"LIVE_ACT_INDICES":live_bits,"RETIRED_ACT_INDICES":retired_bits,
      "ACTIVE_STAR_MASK":sum(1<<b for b in live_bits),"RETIRED_STAR_MASK":sum(1<<b for b in retired_bits),
      "ACTIVE_ACT_COUNT":len(live),"SLOT_COUNT":slots,"STAR_CEILING":(1<<slots)-1,
      "SHIPPING_PHASE_TOTAL":sum(len(j["phases"]) for j in live)})
    result["ALL_STARS"]=result["ACTIVE_STAR_MASK"]
    result["OPERA_ACTIVE_STAR_MASK"]=result["ACTIVE_STAR_MASK"]
    result["OPERA_ACTIVE_ACT_COUNT"]=result["ACTIVE_ACT_COUNT"]
    acts=[]
    for entry in ledger:
        if entry["status"]=="TOMBSTONE":
            acts.append({"save_bit":entry["star_bit"],"retired":True});continue
        job=lookup[entry["id"]]
        values={"save_bit":job["star_bit"],"name":job["title"],"career":job["career_label"],
          "costume":job["id"],"music":job["music"]["cue"],"voice":job["voice"]["intro_line"],
          "win_line":job["voice"]["win_line"],"floor_col":job["presentation"]["colors"]["floor"],
          "trim":job["presentation"]["colors"]["trim"],"curtain":job["presentation"]["colors"]["curtain"]}
        acts.append({k:values[k] if k in values else job["act_extra"][k] for k in job["act_key_order"]})
    result["ACTS"]=acts
    result["ROOM_ACT_INDICES"]={room:[j["star_bit"] for j in sorted(
        (j for j in live if j["home"]["room"]==room),key=lambda j:j["home"]["room_order"])]
        for room in catalog["config"]["room_order"]}
    result["CAREER_CREST_FILES"]={j["id"]:j["home"]["crest"] for j in sorted(
        (j for j in jobs if "CAREER_CREST_FILES" in j["compat_order"]),key=lambda j:j["compat_order"]["CAREER_CREST_FILES"])}
    for m in catalog["compatibility"]["registries"]:
        result[m["generated"]]=_table(catalog,m["generated"],m["field"],m["kind"]=="bit_dictionary")
    for name in ("MASTERY_CAREERS","PERFORMANCE_ENABLED","ADAPTER_CAREER_ORDER"):
        result[name]=[j["id"] for j in sorted((j for j in jobs if name in j["compat_order"]),key=lambda j:j["compat_order"][name])]
    result["HOTSPOT_ASSET_META"]=catalog["config"]["asset_meta"]
    result["VENUE_FLOOR_NAMES"]=catalog["config"]["venue"]["floor_names"]
    result["VENUE_FLOOR_ACTOR_POSITIONS"]=catalog["config"]["venue"]["floor_actor_positions"]
    venue=sorted((j for j in jobs if "legacy_floor" in j["home"]["venue"]),key=lambda j:j["home"]["venue"]["legacy_floor"])
    result["VENUE_LEGACY_FLOOR_ACT_INDICES"]=[j["star_bit"] for j in venue]
    result["LIVING_WORLD_OPERA_ROWS"]=[["opera.act.%02d" % j["star_bit"],j["living_world"]["name"],
        "scripts/opera_house.gd:ACTS[%d]; scripts/opera_career_world_2d.gd" % j["star_bit"],
        *j["living_world"]["accents"]] for j in jobs]
    result["EXPECTED_STAGE_COUNT"]=catalog["config"]["non_job_stage_count"]+len(live)
    party=sorted((j for j in jobs if j["chapter2"].get("party")),key=lambda j:j["chapter2"]["guide_order"])
    rows=[]
    for j in party:
        values={"act_index":j["star_bit"],**j["chapter2"]["party"]}
        rows.append({k:values[k] for k in j["chapter2"]["party_key_order"]})
    result["LIVE_CAREERS"]=rows
    result["GUIDE_ORDER"]=[j["star_bit"] for j in party]
    result["ALL_PARTY_MASK"]=sum(1<<j["star_bit"] for j in party)
    result["PARTY_MASK"]=result["ALL_PARTY_MASK"]
    result["VALID_MODES"]=catalog["config"]["valid_modes"]
    result.update({"CHAPTER2_"+name:value for name,value in catalog["config"]["chapter2"].items()})
    for job in party:
        name=job["chapter2"]["act_constant"]
        result["CHAPTER2_"+name]=job["star_bit"]
        result["CHAPTER2_"+name.replace("ACT_","SKILL_")]=job["chapter2"]["skill"]
    result["CHAPTER2_JOB_PHASE_ACTS"]=[j["star_bit"] for j in party]
    result["CHAPTER2_JOB_PHASE_MASK_LIMITS"]=[j["chapter2"]["phase_mask_limit"] for j in party]
    result.update(_checkpoint_data(catalog))
    result["ACTOR_ROUTES"]={j["id"]:{**j["presentation"]["actors"],"surface":j["surface"]} for j in jobs}
    result["VOICE_ROUTES"]={j["voice"]["prefix"]:{k:v for k,v in j["voice"].items() if k in (
        "speaker","folder","speaker_prefix","fallback_folders","allow_unprefixed_fallback","exact_required")} for j in jobs}
    routes={}
    for job in jobs:
        for event in job["voice"]["required_keys"]:
            event=event.removeprefix("roshan_")
            route={"speaker":job["voice"].get("event_speakers",{}).get(event,job["voice"]["speaker"]),"event":event,"paths":_exact_paths(job,event)}
            if event in routes and routes[event]!=route:raise ValueError("conflicting exact route "+event)
            routes[event]=route
    result["REQUIRED_VOICE_ROUTES"]=routes
    result["MUSIC_CUES"]=[j["music"]["cue"] for j in jobs]
    result["COSTUME_SHEETS"]={j["id"]:j["art"]["costume_sheet"] for j in jobs}
    result["DIEGETIC_EXPECTED_STATIONS"]={j["id"]:[station["id"] for station in j["stage_geometry"]["paths"]["stations"]] for j in sorted((j for j in jobs if "DIEGETIC_EXPECTED_STATIONS" in j["compat_order"]),key=lambda j:j["compat_order"]["DIEGETIC_EXPECTED_STATIONS"])}
    result["DIEGETIC_PLAYABLE_PHASE_STATIONS"]={j["id"]:list(j["phase_stations"].values()) for j in sorted((j for j in jobs if "DIEGETIC_PLAYABLE_PHASE_STATIONS" in j["compat_order"]),key=lambda j:j["compat_order"]["DIEGETIC_PLAYABLE_PHASE_STATIONS"])}
    result["CHAPTER2_PHASE_TOTAL"]=sum(len(j["chapter2"]["scene"]["phases"]) for j in party)
    result["TRUSTED_PROBE_EXPECTATIONS"]={"live_job_count":len(live),"slot_count":slots,
      "shipping_phase_total":result["SHIPPING_PHASE_TOTAL"],"living_stage_count":result["EXPECTED_STAGE_COUNT"],
      "mastery_job_count":len(result["MASTERY_CAREERS"]),
      "room_job_count":sum(len(bits) for bits in result["ROOM_ACT_INDICES"].values()),
      "legacy_nursery_predecessor_count":sum(1 for j in live if j["star_bit"]<lookup["nursery"]["star_bit"]),
      "diegetic_phase_total":sum(len(v) for v in result["DIEGETIC_PLAYABLE_PHASE_STATIONS"].values()),
      "chapter2_phase_total":result["CHAPTER2_PHASE_TOTAL"],
      "two_act_unit_total":sum(len(j["phases"])+(min(len(j["phases"]),int(j.get("practice_count") or 0)) if j["two_act"] else 0) for j in jobs)}
    return result


def source_snapshot(root: Path,catalog=None):
    catalog=catalog if catalog is not None else load_catalog(root)
    data=derive(catalog)
    result={name:(read_save_const(root,source,data,BASELINE) if file=="save_state" else read_const(root/f"scripts/{file}.gd",source)) for name,file,source,_ in SHARED}
    for m in catalog["compatibility"]["registries"]:
        result[m["generated"]]=read_const(root/m["path"],m["source"])
    for source in DIRECTOR:result["CHAPTER2_"+source]=read_const(root/"scripts/chapter_two_director.gd",source)
    result["DIEGETIC_EXPECTED_STATIONS"]=read_const(root/"scripts/probe_opera_diegetic_paths.gd","EXPECTED_STATIONS")
    result["DIEGETIC_PLAYABLE_PHASE_STATIONS"]=read_const(root/"scripts/probe_opera_diegetic_paths.gd","PLAYABLE_PHASE_STATIONS")
    text=mask_source((root/"scripts/probe_chapter2.gd").read_text(encoding="utf-8"))
    matches=list(re.finditer(r"(?m)^\t_check\(\s*,\s*count == (\d+)\b(?=\s*\))",text))
    if len(matches)!=1:raise ValueError("expected one real Chapter Two phase-count assertion")
    result["CHAPTER2_PHASE_TOTAL"]=int(matches[0].group(1))
    result["LIVING_WORLD_OPERA_ROWS"]=opera_rows(root)
    result.update(read_save_bounds(root,data))
    result["SAVE_CHECKPOINT_JOB_ORDER"]=read_checkpoint_order(root,data)
    text=mask_source((root/"scripts/probe_opera_2d.gd").read_text(encoding="utf-8"))
    matches=list(re.finditer(r"(?m)^\t_check\(\s*,\s*shipping_phase_count == (\d+)\b(?=\s+and\s+missing_specs\.is_empty\(\)\))",text))
    if len(matches)!=1:raise ValueError("expected one real shipping phase-count assertion")
    result["SHIPPING_PHASE_TOTAL"]=int(matches[0].group(1))
    return result


@lru_cache(maxsize=32)
def _first_declaration(root_name,jid):
    result=subprocess.check_output(["git","log","--reverse","--format=%H|%cs","-S",
        chr(34)+"costume"+chr(34)+": "+chr(34)+jid+chr(34),"--","scripts/opera_house.gd"],
        cwd=root_name,text=True).splitlines()
    if not result:raise ValueError("baseline allocation evidence missing for "+jid)
    commit,date=result[0].split("|")
    return {"first_declaration_commit":commit,"first_declaration_date":date}


def baseline_entries(root: Path,catalog):
    """Pinned initial allocation, extended only by the Git integration baseline."""
    def blob(ref,path):
        return subprocess.check_output(["git","show",ref+":"+path],cwd=root,text=True,encoding="utf-8",stderr=subprocess.DEVNULL)
    text=blob(BASELINE,"scripts/opera_house.gd")
    match=re.search(r"(?m)^const\s+ACTS\b[^=\n]*=",text)
    acts=GDParser(text,match.end()).value()
    initial=[{"star_bit":i,"id":None if a.get("retired") else a["costume"],
        "status":"TOMBSTONE" if a.get("retired") else "LIVE",
        "aliases":["candy_maker","candy"] if a.get("costume")=="candymaker" else []} for i,a in enumerate(acts)]
    observed_date=subprocess.check_output(["git","show","-s","--format=%cs",BASELINE],cwd=root,text=True).strip()
    for entry in initial:
        entry["allocated"]={"observed_commit":BASELINE,"observed_date":observed_date,
            "source":"scripts/opera_house.gd:ACTS[%d]" % entry["star_bit"]}
        if entry["id"] is not None:
            entry["allocated"].update(_first_declaration(str(root.resolve()),entry["id"]))
        else:
            entry["reason"]="Owner cut 3d1236fe; raw bit preserved permanently (DL-SAVE-06)"
    integration=subprocess.check_output(["git","merge-base","HEAD","origin/dev"],cwd=root,text=True).strip()
    exists=subprocess.run(["git","cat-file","-e",integration+":content/jobs/_ledger.json"],cwd=root,capture_output=True)
    if exists.returncode==0:
        previous=json.loads(blob(integration,"content/jobs/_ledger.json"))["entries"]
        if len(previous)<len(initial) or any(any(a.get(k)!=b.get(k) for k in ("star_bit","id","status","aliases","allocated","reason")) for a,b in zip(initial,previous)):
            raise ValueError("baseline integration allocation contradicts initial ledger")
        return previous
    return initial


def _strict_equal(a,b):
    if type(a) is not type(b):return False
    if isinstance(a,dict):return list(a)==list(b) and all(_strict_equal(a[k],b[k]) for k in a)
    if isinstance(a,list):return len(a)==len(b) and all(_strict_equal(x,y) for x,y in zip(a,b))
    return a==b



def _schema_validate(value,schema,path,errors):
    types={"object":dict,"array":list,"string":str,"integer":int,"number":(int,float),"boolean":bool,"null":type(None)}
    wanted=schema.get("type")
    if wanted:
        allowed=wanted if isinstance(wanted,list) else [wanted]
        if not any(isinstance(value,types[t]) and not (t in ("integer","number") and isinstance(value,bool)) for t in allowed):
            errors.append("E01 "+path+": invalid type");return
    if "const" in schema and value!=schema["const"]:errors.append("E01 "+path+": invalid schema/value")
    if "enum" in schema and value not in schema["enum"]:errors.append("E01 "+path+": unsupported value")
    if isinstance(value,dict):
        props=schema.get("properties",{})
        for key in schema.get("required",[]):
            if key not in value:errors.append("E01 "+path+"."+key+": missing field")
        if schema.get("additionalProperties") is False:
            for key in value.keys()-props.keys():errors.append("E01 "+path+"."+key+": unknown field")
        for key,child in props.items():
            if key in value:_schema_validate(value[key],child,path+"."+key,errors)
    if isinstance(value,list):
        if len(value)<schema.get("minItems",0):errors.append("E01 "+path+": too few items")
        if "items" in schema:
            for i,child in enumerate(value):_schema_validate(child,schema["items"],f"{path}[{i}]",errors)
    if isinstance(value,(int,float)) and not isinstance(value,bool):
        if not math.isfinite(value):errors.append("E01 "+path+": nonfinite number")
        if value<schema.get("minimum",value):errors.append("E01 "+path+": below minimum")
    if isinstance(value,str) and "pattern" in schema and not re.fullmatch(schema["pattern"],value):errors.append("E01 "+path+": invalid string")


def _native_validate(value,path,errors):
    if isinstance(value,float) and not math.isfinite(value):errors.append("E01 "+path+": nonfinite number")
    if isinstance(value,dict):
        tags=[k for k in value if k.startswith("__")]
        if tags:
            if set(value)=={"__call__","args"}:
                name,args=value["__call__"],value["args"]
                good=isinstance(args,list) and name in CONSTRUCTORS
                if good:
                    numeric=lambda xs:all(type(x) in (int,float) and math.isfinite(x) for x in xs)
                    if name=="Color":
                        good=(len(args)==1 and isinstance(args[0],str) and bool(re.fullmatch(r"#[0-9A-Fa-f]{6}(?:[0-9A-Fa-f]{2})?",args[0]))) or (len(args) in (3,4) and numeric(args))
                    elif name in ("Vector2","Vector2i"):good=len(args)==2 and numeric(args) and (name!="Vector2i" or all(type(x) is int for x in args))
                    elif name=="Rect2":good=(len(args)==4 and numeric(args)) or (len(args)==2 and all(isinstance(x,dict) and x.get("__call__")=="Vector2" for x in args))
                    else:
                        good=len(args)==1 and isinstance(args[0],list)
                        if good and name=="PackedStringArray":good=all(isinstance(x,str) for x in args[0])
                        elif good and name=="PackedInt32Array":good=all(type(x) is int and -(1<<31)<=x<(1<<31) for x in args[0])
                        elif good and name=="PackedFloat32Array":good=numeric(args[0])
                if not good:errors.append("E01 "+path+": forbidden constructor or arguments")
            elif set(value)=={"__stringname__"}:
                if not isinstance(value["__stringname__"],str):errors.append("E01 "+path+": invalid StringName")
            elif set(value)=={"__dict__"}:
                pairs=value["__dict__"]
                if not isinstance(pairs,list) or any(not isinstance(p,list) or len(p)!=2 for p in pairs):
                    errors.append("E01 "+path+": invalid native dictionary");return
                keys=[json.dumps(p[0],sort_keys=True) for p in pairs]
                if len(set(keys))!=len(keys):errors.append("E01 "+path+": duplicate native dictionary key")
            else:errors.append("E01 "+path+": forbidden literal tag")
        for key,child in value.items():_native_validate(child,path+"."+key,errors)
    elif isinstance(value,list):
        for i,child in enumerate(value):_native_validate(child,f"{path}[{i}]",errors)


def _repo_path(root,value):
    if not isinstance(value,str) or not value:return None
    path=(root/value.removeprefix("res://")).resolve()
    return path if path.is_relative_to(root.resolve()) else None


def diagnostics(root: Path,catalog):
    music=set(read_python_list(root/"tools/build_area_music.py","EXPECTED_IDS"))
    atlas=set(read_python_list(root/"tools/audit_opera_roshan_animation.py","CAREERS"))
    return [f"JP4_DEFERRED music_catalog:{j['id']}" for j in _ordered_jobs(catalog) if j["music"]["cue"] not in music]+[
        f"JP4_DEFERRED atlas_gate:{j['id']}" for j in _ordered_jobs(catalog) if j["id"] not in atlas]


def validate(root: Path,catalog):
    root=Path(root)
    errors=[]
    try:
        schema=_json(root/"content/job_record.schema.json")
        for i,job in enumerate(catalog["jobs"]):
            _schema_validate(job,schema,f"job[{i}]",errors)
            _native_validate(job,f"job[{i}]",errors)
        _native_validate(catalog["config"],"config",errors)
        _native_validate(catalog["ledger"],"ledger",errors)
        if catalog.get("compatibility")!=COMPATIBILITY_CONTRACT:
            errors.append("E01 compatibility metadata differs from fixed JP0 contract")
            return errors
        entries=catalog["ledger"]["entries"]
        if catalog["config"].get("runtime_baseline")!=BASELINE:errors.append("E02 immutable runtime allocation baseline changed")
        try:old=baseline_entries(root,catalog)
        except (OSError,ValueError,subprocess.SubprocessError,RuntimeError) as exc:
            errors.append("E02 baseline history unavailable: "+str(exc));return errors
        if len(entries)<len(old) or any(any(a.get(k)!=b.get(k) for k in ("star_bit","id","status","aliases")) for a,b in zip(old,entries)):
            errors.append("E02 ledger removed, reordered, repointed or reused baseline allocation")
        if old and "allocated" in old[0] and any(a!=b for a,b in zip(old,entries)):errors.append("E02 allocation evidence changed")
        for entry in entries:
            evidence=entry.get("allocated",{})
            if not isinstance(evidence,dict) or not re.fullmatch(r"[0-9a-f]{40}",str(evidence.get("observed_commit",""))) or not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}",str(evidence.get("observed_date",""))) or not evidence.get("source"):
                errors.append("E02 allocation requires dated immutable Git evidence")
        bits=[e["star_bit"] for e in entries]
        if any(type(b) is not int or b<0 for b in bits) or bits!=list(range(len(entries))):
            errors.append("E02 star allocation must be unique contiguous append order")
        ids=[e["id"] for e in entries if e["id"] is not None]
        aliases=[a for e in entries for a in e.get("aliases",[])]
        if len(set(ids))!=len(ids) or len(set(aliases))!=len(aliases) or set(ids)&set(aliases):errors.append("E01 duplicate identity or alias")
        # This namespace object is pinned JP0 evidence, not an authoring bound.
        # Future appended entries grow STAR_CEILING from max(bit) with no edits
        # to this sealed baseline evidence.
        namespace=catalog["ledger"]["star_namespace"]
        if namespace!={"save_key":"opera_stars","highest_allocated_bit":17,"derived_ceiling":262143,"next_free_bit":18}:
            errors.append("E10 baseline star ceiling evidence changed")
        jobs=catalog["jobs"]
        jids=[j["id"] for j in jobs]
        if len(set(jids))!=len(jids):errors.append("E01 duplicate job id")
        if set(jids)!=set(ids):errors.append("E02 unregistered act or missing allocated job")
        data=_checkpoint_data(catalog)
        prefix=catalog["config"].get("save_checkpoint_normalization_prefix")
        if prefix!=baseline_checkpoint_order(root,BASELINE,data):errors.append("E09 checkpoint normalization prefix differs from immutable baseline order")
        checkpoint_keys=[spec["key"] for spec in data["SAVE_CHECKPOINTS"].values()]
        if len(checkpoint_keys)!=len(set(checkpoint_keys)):errors.append("E09 duplicate checkpoint key")
        for spec in data["SAVE_CHECKPOINTS"].values():
            lists=spec["registration_lists"]
            if not lists or len(lists)!=len(set(lists)) or any(name not in ("DICTIONARY_KEYS","KNOWN_KEYS") for name in lists):errors.append("E09 unknown or duplicate checkpoint registration list")
        allocations={e["id"]:e for e in entries if e["id"] is not None}
        rooms={r["id"] for r in read_const(root/"scripts/arena/castle_rooms_25d.gd","ROOMS")}
        room_orders=set()
        local=(root/"scripts/ci.sh").read_text(encoding="utf-8")
        remote=(root/".github/workflows/probes.yml").read_text(encoding="utf-8")
        local_roster=set(re.search(r"for p in (probe_\w+.*?)\s*;\s*do",local,re.S).group(1).split())
        remote_roster=set(re.search(r"for p in (probe_\w+.*?)\s*;\s*do",remote,re.S).group(1).split())
        ledger_text=(root/"design/05_DOC_LEDGER.md").read_text(encoding="utf-8")
        for job in jobs:
            jid=job["id"]
            allocation=allocations.get(jid,{})
            if allocation.get("star_bit")!=job["star_bit"] or allocation.get("status")!=job["status"]:errors.append("E02 "+jid+": job contradicts allocation")
            if job["two_act"] != ("PERFORMANCE_ENABLED" in job["compat_order"]):errors.append("E01 "+jid+": two_act differs from ordered enabled membership")
            home=job["home"]
            marker=(home["room"],home["room_order"])
            if home["room"] not in rooms or marker in room_orders:errors.append("E03 "+jid+": unknown room or duplicate room order")
            room_orders.add(marker)
            phases=job["phases"]
            if not phases or type(job["finale_start"]) is not int or not 0<=job["finale_start"]<len(phases):errors.append("E04 "+jid+": empty phases or invalid finale index")
            stations={s["id"] for s in job.get("stage_geometry",{}).get("paths",{}).get("stations",[])}
            for station in job.get("phase_stations",{}).values():
                if station not in stations:errors.append("E04 "+jid+": missing station "+str(station))
            for phase in phases:
                if "station" in phase and phase["station"] not in stations:errors.append("E04 "+jid+": unknown phase station")
            voice=job["voice"]
            if isinstance(voice.get("required_keys"),list):
                for event in voice["required_keys"]:
                    paths=_exact_paths(job,event)
                    if not any((_repo_path(root,p) or Path("__missing__")).is_file() for p in paths):errors.append("E05 "+jid+": missing exact voice "+event)
                if not {p["vo"] for p in phases}.issubset(set(voice["required_keys"])):errors.append("E05 "+jid+": phase voice not required")
            cue=_repo_path(root,"res://assets/audio/music/"+job["music"]["cue"]+".ogg")
            if not cue or not cue.is_file():errors.append("E06 "+jid+": missing music cue")
            art=job["art"]
            sheet=_repo_path(root,art["costume_sheet"])
            if not sheet or not sheet.is_file():errors.append("E07 "+jid+": missing costume sheet")
            elif hashlib.sha256(sheet.read_bytes()).hexdigest()!=art["costume_sheet_sha256"]:errors.append("E07 "+jid+": costume hash mismatch")
            crest=home["crest"] if str(home["crest"]).startswith("res://") else "res://assets/opera/worlds/ui/crests/"+str(home["crest"])
            goal=job["presentation"]["goal_prop"]
            goal="res://assets/opera/worlds/props/"+goal+("" if Path(goal).suffix else ".png")
            references=[crest,goal,job["surface"],*art["props"],*art["tiles"],job["presentation"]["actors"]["player"],job["presentation"]["actors"]["partner"]]
            for reference in references:
                path=_repo_path(root,reference)
                if not path or not path.is_file():errors.append("E08 "+jid+": missing reference "+str(reference))
            checkpoint=job["save"]["checkpoint"]
            if checkpoint:
                for name in checkpoint["registration_lists"]:
                    if checkpoint["key"] not in read_save_const(root,name,data,BASELINE):errors.append("E09 "+jid+": checkpoint missing from "+name)
            if job["chapter2"].get("party") and not 0<=job["star_bit"]<16:errors.append("E11 "+jid+": party bit exceeds present namespace")
            if not job["probes"] or any(p not in local_roster&remote_roster or not (root/"scripts"/(p+".gd")).is_file() for p in job["probes"]):errors.append("E13 "+jid+": no trusted probe coverage")
            for doc in job["docs"]:
                path=_repo_path(root,doc)
                if not path or not path.is_file() or ("| \x60"+doc+"\x60 |") not in ledger_text:errors.append("E14 "+jid+": missing or unclassified document "+doc)
        measured=diagnostics(root,catalog)
        expected={"music_catalog":["geologist"],"atlas_gate":["geologist","teacher"]}
        actual={"music_catalog":[x.split(":")[1] for x in measured if "music_catalog:" in x],
                "atlas_gate":[x.split(":")[1] for x in measured if "atlas_gate:" in x]}
        if catalog["config"].get("deferred_jp4")!=expected:errors.append("E01 JP4 evidence cannot create a waiver")
        if actual["music_catalog"]!=expected["music_catalog"]:errors.append("E06 music tool coverage differs from JP0 baseline")
        if actual["atlas_gate"]!=expected["atlas_gate"]:errors.append("E07 atlas tool coverage differs from JP0 baseline")
        if not errors:
            derived=derive(catalog)
            for name,literal in source_snapshot(root,catalog).items():
                if name not in derived or not _strict_equal(literal,derived[name]):errors.append("E16 source compatibility differs: "+name)
    except (OSError,ValueError,KeyError,TypeError,IndexError,AttributeError,subprocess.SubprocessError) as exc:
        errors.append("E01 validation failed closed: "+str(exc))
    return errors


def _gd(value,indent=0):
    if value is None:return "null"
    if type(value) is bool:return "true" if value else "false"
    if type(value) in (int,float):return repr(value)
    if isinstance(value,str):return json.dumps(value,ensure_ascii=False)
    if isinstance(value,dict):
        if "__call__" in value:return value["__call__"]+"("+", ".join(_gd(a) for a in value["args"])+")"
        if "__stringname__" in value:return "&"+_gd(value["__stringname__"])
        pairs=value["__dict__"] if "__dict__" in value else list(value.items())
        if not pairs:return "{}"
        if indent>0:return "{"+", ".join(_gd(k,indent+1)+": "+_gd(v,indent+1) for k,v in pairs)+"}"
        return "{\n"+"\n".join("\t"*(indent+1)+_gd(k)+": "+_gd(v,indent+1)+"," for k,v in pairs)+"\n"+"\t"*indent+"}"
    if isinstance(value,list):
        if not value:return "[]"
        if indent>0:return "["+", ".join(_gd(v,indent+1) for v in value)+"]"
        if all(type(v) in (str,int,float,bool) or v is None or (isinstance(v,dict) and "__call__" in v) for v in value):return "["+", ".join(_gd(v) for v in value)+"]"
        return "[\n"+"\n".join("\t"*(indent+1)+_gd(v,indent+1)+"," for v in value)+"\n"+"\t"*indent+"]"
    raise ValueError("cannot emit native value")


def render(catalog):
    data=derive(catalog)
    types={name:kind for name,_,_,kind in SHARED}
    types.update({m["generated"]:m["type"] for m in catalog["compatibility"]["registries"]})
    types.update({"LEDGER":"Array[Dictionary]","LIVING_WORLD_OPERA_ROWS":"Array","MUSIC_CUES":"Array[String]",
        "SLOT_COUNT":"int","STAR_CEILING":"int","SHIPPING_PHASE_TOTAL":"int","PARTY_MASK":"int",
        "SAVE_CHECKPOINT_JOB_ORDER":"Array[String]"})
    for name,value in data.items():
        if name not in types:
            types[name]="Dictionary" if isinstance(value,dict) else ("Array[int]" if isinstance(value,list) and all(type(v) is int for v in value) else ("Array" if isinstance(value,list) else ("int" if type(value) is int else "String")))
    lines=["# GENERATED by tools/content_build.py - do not edit.",
      "# Authored records compile to native constants; no runtime JSON.","class_name JobCatalogData","extends RefCounted",""]
    for name,value in data.items():lines.extend(["const "+name+": "+types[name]+" = "+_gd(value),""])
    return "\n".join(lines)


def issues(root: Path):
    try:
        catalog=load_catalog(root)
        found=validate(root,catalog)
        if found:return found
        output=Path(root)/GENERATED
        if not output.is_file() or output.read_bytes()!=render(catalog).encode("utf-8"):
            return ["E15 generated catalogue missing/stale; run python -B tools/content_build.py --write"]
        return []
    except (OSError,ValueError,KeyError,TypeError) as exc:return ["E01 content load failed closed: "+str(exc)]


def write(root: Path):
    catalog=load_catalog(root)
    found=validate(root,catalog)
    if found:return found
    path=Path(root)/GENERATED
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_bytes(render(catalog).encode("utf-8"))
    return []


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    group=ap.add_mutually_exclusive_group(required=True)
    group.add_argument("--write",action="store_true")
    group.add_argument("--check",action="store_true")
    group.add_argument("--explain",metavar="ID")
    ap.add_argument("--root",type=Path,default=Path(__file__).resolve().parents[1])
    args=ap.parse_args()
    if args.explain:
        catalog=load_catalog(args.root)
        aliases={a:e["id"] for e in catalog["ledger"]["entries"] for a in e.get("aliases",[])}
        jid=aliases.get(args.explain,args.explain)
        job=next((j for j in catalog["jobs"] if j["id"]==jid),None)
        if not job:ap.error("unknown job "+args.explain)
        print(json.dumps({"job":job,
          "registries":[m["generated"] for m in catalog["compatibility"]["registries"] if m["generated"] in job["compat_order"]],
          "voice_paths":{k:_exact_paths(job,k) for k in job["voice"]["required_keys"]},
          "checkpoint":derive(catalog)["SAVE_CHECKPOINTS"].get(jid),
          "deferred_jp4":[x for x in diagnostics(args.root,catalog) if x.endswith(":"+jid)]},ensure_ascii=True,indent=2))
        return 0
    found=write(args.root) if args.write else issues(args.root)
    for problem in found:print(problem)
    if found:return 1
    catalog=load_catalog(args.root)
    for diagnostic in diagnostics(args.root,catalog):print(diagnostic)
    print("CONTENT|OK|catalogue-current")
    return 0

if __name__=="__main__":raise SystemExit(main())

