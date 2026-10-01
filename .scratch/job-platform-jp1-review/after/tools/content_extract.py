#!/usr/bin/env python3
"""Read-only bootstrap extractor for JP0; output is a reviewable content draft."""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
from pathlib import Path
try:
    from .content_gd_literals import read_const, integer_mapping, opera_rows
    from .content_source_refs import baseline_checkpoint_order
except ImportError:
    from content_gd_literals import read_const, integer_mapping, opera_rows
    from content_source_refs import baseline_checkpoint_order

BASELINE = "7f068cb80766edd52a110cc1cb3958158f829822"
# generated name, source file, source const, record field, native output type
REGISTRIES = [
 ("PHASES","opera_career_world_2d","PHASES","phases","Dictionary"),
 ("FINALE_START","opera_career_world_2d","FINALE_START","finale_start","Dictionary"),
 ("PHASE_STATIONS","opera_career_world_2d","PHASE_STATIONS","phase_stations","Dictionary"),
 ("HOTSPOT_PHASE_ALIASES","opera_career_world_2d","HOTSPOT_PHASE_ALIASES","hotspot_aliases","Dictionary"),
 ("GOAL_PROPS","opera_career_world_2d","GOAL_PROPS","presentation.goal_prop","Dictionary"),
 ("SLUGS","opera_career_world_2d","SLUGS","legacy.slug","Dictionary"),
 ("LEGACY_PHASES","opera_career_world_2d","LEGACY_PHASES","legacy.phases","Dictionary"),
 ("LEGACY_FINALE_START","opera_career_world_2d","LEGACY_FINALE_START","legacy.finale_start","Dictionary"),
 ("COMPETITION_CAREERS","opera_competition","CAREERS","competition","Dictionary"),
 ("MASTERY_RULES","opera_mastery","RULES","mastery","Dictionary"),
 ("PRACTICE_COUNTS","opera_performance_plan","PRACTICE_COUNTS","practice_count","Dictionary"),
 ("CAREER_COLORS","opera_performance_overlay","CAREER_COLORS","presentation.colors.overlay","Dictionary"),
 ("HOTSPOT_EXPECTED_PHASES","opera_hotspot_catalog","EXPECTED_PHASES","hotspot_expected_phases","Dictionary"),
 ("HOTSPOT_SPECS","opera_hotspot_catalog","SPECS","hotspots","Dictionary"),
 ("BACKDROP_PALETTES","opera_world_backdrop_2d","PALETTES","presentation.backdrop.palette","Dictionary"),
 ("STAGE_PATHS","opera_stage_paths","PATHS","stage_geometry.paths","Dictionary"),
 ("STAGE_STATION_NAV","opera_stage_paths","STATION_NAV","stage_geometry.station_nav","Dictionary"),
 ("STAGE_ROAM","opera_stage_paths","ROAM","stage_geometry.roam","Dictionary"),
 ("STAGE_BLEED","opera_stage_paths","BLEED","stage_geometry.bleed","Dictionary"),
 ("PHASE_SETS","chapter_two_career_scene_adapter","PHASE_SETS","chapter2.scene","Dictionary"),
]

def set_field(row, dotted, value):
    parts = dotted.split(".")
    current = row
    for part in parts[:-1]:
        current = current.setdefault(part, {})
    current[parts[-1]] = value


def extract(root: Path, out: Path):
    def const(file, name):
        return read_const(root / f"scripts/{file}.gd", name)
    acts = const("opera_house", "ACTS")
    rooms = const("castle_career_routes","ROOM_ACT_INDICES")
    crests = const("castle_career_routes","CAREER_CREST_FILES")
    party = const("chapter_two_party_plan","LIVE_CAREERS")
    enabled = const("opera_performance_plan","ENABLED")
    career_order = const("chapter_two_career_scene_adapter","CAREER_ORDER")
    mastery_order = const("opera_mastery","CAREERS")
    world_rows = opera_rows(root)
    jobs, entries = [], []
    observed_date = subprocess.check_output(["git","show","-s","--format=%cs",BASELINE],cwd=root,text=True).strip()
    for slot, act in enumerate(acts):
        if act.get("retired"):
            entries.append({"star_bit":slot,"id":None,"status":"TOMBSTONE","aliases":[],
              "allocated":{"observed_commit":BASELINE,"source":f"scripts/opera_house.gd:ACTS[{slot}]"},
              "reason":"Owner cut 3d1236fe; raw bit preserved permanently (DL-SAVE-06)"})
            entries[-1]["allocated"]["observed_date"] = observed_date
            continue
        jid = act["costume"]
        aliases = ["candy_maker","candy"] if jid == "candymaker" else []
        entry = {"star_bit":slot,"id":jid,"status":"LIVE","aliases":aliases,
          "allocated":{"observed_commit":BASELINE,"source":f"scripts/opera_house.gd:ACTS[{slot}]"}}
        # The first exact allocation declaration visible in this file's Git
        # history is evidence, not a claim about earlier authoring outside it.
        history = subprocess.run(["git","log","--reverse","--format=%H|%cs",
            "-S",f'"costume": "{jid}"',"--","scripts/opera_house.gd"],
            cwd=root, text=True, capture_output=True, check=True).stdout.splitlines()
        if history:
            commit,date = history[0].split("|")
            entry["allocated"].update({"first_declaration_commit":commit,"first_declaration_date":date})
        entry["allocated"]["observed_date"] = observed_date
        entries.append(entry)
        room = next(r for r, bits in rooms.items() if slot in bits)
        row = {"schema":"job_record/1","id":jid,"status":"LIVE","family":"opera_career",
           "title":act["name"],"career_label":act["career"],"star_bit":slot,"progress_key":None,
           "home":{"room":room,"room_order":rooms[room].index(slot),"crest":crests.get(jid),"venue":{}},
           "presentation":{"colors":{"floor":act["floor_col"],"trim":act["trim"],"curtain":act["curtain"]},
               "actors":{},"backdrop":{}},
           "voice":{"engine":"Parler-TTS Mini v1.1 provisional preferred Roshan route; Kokoro-82M exact legacy fallback (ASSET_LICENSES.md)",
               "speaker":"roshan","folder":"res://assets/audio/teacher/" if jid == "teacher" else "res://assets/audio/voices/filler_v1/",
               "prefix":"teacher_" if jid == "teacher" else "op_"+jid+"_",
               "fallback_folders":[] if jid == "teacher" else ["res://assets/audio/voices/"],
               "speaker_prefix":True,"allow_unprefixed_fallback":jid == "teacher","exact_required":jid == "teacher",
               "intro_line":act["voice"],"win_line":act["win_line"],"required_keys":[]},
           "music":{"cue":act["music"]},"art":{},"save":{"checkpoint":None},
           "competition":{},"mastery":{},"two_act":jid in enabled,
           "capabilities":[],"surface":"res://scripts/opera_gesture_surface.gd",
           "chapter2":{"party":None,"scene":None},"legacy":{},
           "living_world":world_rows[[int(w[0].split(".")[-1]) for w in world_rows].index(slot)],
           "stage_inventory_id":None,
           "probes":["probe_opera","probe_opera_2d"],"docs":["design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md"],
           "compat_order":{},"act_key_order":list(act),
           "act_extra":{k:v for k,v in act.items() if k not in {"save_bit","name","career","costume","music","voice","win_line","floor_col","trim","curtain"}}}
        for name,order in [("MASTERY_CAREERS",mastery_order),("PERFORMANCE_ENABLED",enabled),("ADAPTER_CAREER_ORDER",career_order)]:
            if jid in order: row["compat_order"][name] = order.index(jid)
        matching = next((p for p in party if p["act_index"] == slot),None)
        if matching:
            row["chapter2"]["party"] = {k:v for k,v in matching.items() if k != "act_index"}
            row["chapter2"]["party_key_order"] = list(matching)
            row["chapter2"]["guide_order"] = party.index(matching)
        sheet = f"res://assets/opera/worlds/actors/animation/roshan_{jid}_sheet_a.png"
        row["art"] = {"costume_sheet":sheet,"costume_sheet_sha256":hashlib.sha256((root/sheet[6:]).read_bytes()).hexdigest(),
            "provenance":"ASSET_LICENSES.md","props":[],"tiles":[]}
        partner = "faron_nursery" if jid == "nursery" else ("rival_doctor" if jid == "teacher" else ("rival_detective" if jid == "geologist" else "rival_"+jid))
        row["presentation"]["actors"] = {
            "player":sheet if jid == "geologist" else f"res://assets/opera/worlds/actors/roshan_{jid}.png",
            "partner":f"res://assets/opera/worlds/actors/{partner}.png",
            "partner_visible_solo":jid not in ("teacher","ballerina"),
            "player_size":{"__call__":"Vector2","args":[280,280] if jid == "ballerina" else [250,250]},
            "partner_size":{"__call__":"Vector2","args":[190,190]}}
        special = {"boxer":"boxing","ballerina":"ballet","teacher":"teacher","geologist":"geology","racer":"racer"}
        if jid in special: row["surface"]=f"res://scripts/opera_{special[jid]}_surface.gd"
        if jid in ("teacher","ballerina"): row["capabilities"].append("hide_partner")
        if jid == "geologist": row["capabilities"].append("roshan_actor_atlas")
        if jid == "nursery": row["capabilities"].append("nursery_catch_overlay")
        if row["two_act"]: row["capabilities"].append("two_act_show")
        if jid == "teacher":
            row["capabilities"].append("uses_room_tiles")
            row["presentation"]["backdrop"].update({"mode":"room_tiles","room":"library"})
            row["art"]["tiles"] = [f"res://assets/flats/castle/interactions_v4/background_tiles/room_library_background_r{r}_c{c}.png" for r in range(2) for c in range(4)]
            row["voice"]["engine"]="Kokoro af_heart; assets_src/teacher_learning_2026-09-05/audio_manifest.json"
            row["docs"].append("design/TEACHER_LEARNING_ENGINE_2026-09-05.md")
            row["save"]["checkpoint"]={"key":"teacher_lesson_checkpoint","schema_version":1,"registration_lists":["DICTIONARY_KEYS"]}
        else:
            row["presentation"]["backdrop"]["mode"]="career_tiles"
            row["presentation"]["backdrop"]["painting"]=f"res://assets/opera/worlds/backdrops/world_{jid}.png"
            row["art"]["tiles"]=[f"res://assets/opera/worlds/backdrops/{kind}_{jid}_c{c}r{r}.png" if not (jid=="ballerina" and kind=="stage") else f"res://assets/opera/worlds/stage/finale_stage_c{c}r{r}.png" for kind in ("world","stage") for r in range(2) for c in range(2)]
        if jid=="geologist":
            row["save"]["checkpoint"]={"key":"opera_geology_checkpoint","schema_version":1,"registration_lists":["KNOWN_KEYS"]}
        if jid=="geologist":
            row["art"]["tiles"]=[]
            row["presentation"]["backdrop"].update({"mode":"vector"})
            row["presentation"]["backdrop"].pop("painting",None)
        if jid=="nursery":row["voice"]["engine"]+="; Faron uses protected exact legacy cues"
        old_world=row["living_world"]
        row["living_world"]={"name":old_world[1],"accents":old_world[3:]}
        row["compat_order"]["CAREER_CREST_FILES"]=list(crests).index(jid)
        jobs.append(row)
    byid = {j["id"]:j for j in jobs}
    registry_manifest=[]
    for generated,file,source,field,native_type in REGISTRIES:
        values=const(file,source)
        for order,(jid,value) in enumerate(values.items()):
            set_field(byid[jid],field,value)
            byid[jid]["compat_order"][generated]=order
        registry_manifest.append({"generated":generated,"path":f"scripts/{file}.gd","source":source,"field":field,"type":native_type,"kind":"job_dictionary"})
    asset_meta=const("opera_hotspot_catalog","ASSET_META")
    config={"schema":"job_catalog/1","runtime_baseline":BASELINE,
      "room_order":list(rooms),"asset_meta":asset_meta,
      "valid_modes":const("chapter_two_career_scene_adapter","VALID_MODES"),
      "non_job_stage_count":const("living_world_catalog","EXPECTED_STAGE_COUNT")-len(jobs),
      "venue":{"floor_names":const("opera_house_venue_2d","FLOOR_NAMES"),"floor_actor_positions":const("opera_house_venue_2d","FLOOR_ACTOR_POSITIONS")},
      "chapter2":{},"deferred_jp4":{"music_catalog":["geologist"],"atlas_gate":["geologist","teacher"]}}
    for source,field in [("LEGACY_PORTAL_RECTS","legacy_portal"),("CHAPTER2_PORTAL_RECTS","chapter2_portal"),("CHAPTER2_SECOND_WAVE_PORTAL_RECTS","chapter2_second_wave_portal")]:
        for order,(bit,rect) in enumerate(integer_mapping(const("opera_house_venue_2d",source)).items()):
            row=next(j for j in jobs if j["star_bit"]==bit)
            row["home"]["venue"][field]=rect
            row["compat_order"]["VENUE_"+source]=order
        registry_manifest.append({"generated":"VENUE_"+source,"path":"scripts/opera_house_venue_2d.gd","source":source,"field":"home.venue."+field,"type":"Dictionary","kind":"bit_dictionary"})
    for floor,bit in enumerate(const("opera_house_venue_2d","LEGACY_FLOOR_ACT_INDICES")):
        next(j for j in jobs if j["star_bit"]==bit)["home"]["venue"]["legacy_floor"]=floor
    direct=["ACT_CHEF","ACT_DETECTIVE","ACT_BALLERINA","ACT_CANDY_MAKER","ACT_FARMER","ACT_PAINTER","ACT_ASTRONAUT","ACT_POP_STAR"]
    skill=["SKILL_CHEF","SKILL_DETECTIVE","SKILL_BALLERINA","SKILL_CANDY_MAKER","SKILL_FARMER","SKILL_PAINTER","SKILL_ASTRONAUT","SKILL_POP_STAR"]
    for name in direct+skill:
        val=const("chapter_two_director",name)
        bit=val if name in direct else const("chapter_two_director",name.replace("SKILL_","ACT_"))
        row=next(j for j in jobs if j["star_bit"]==bit)
        if name in direct: row["chapter2"]["act_constant"]=name
        else: row["chapter2"]["skill"]=val
    order=const("chapter_two_director","JOB_PHASE_ACTS")
    limits=const("chapter_two_director","JOB_PHASE_MASK_LIMITS")
    for bit,limit in zip(order,limits):
        row=next(j for j in jobs if j["star_bit"]==bit)
        row["chapter2"]["phase_mask_limit"]=limit
    for name in ["INITIAL_TUTORIAL_ACTS","INITIAL_TUTORIAL_MASK","FIRST_WAVE_UNLOCK_MASK"]:
        config["chapter2"][name]=const("chapter_two_director",name)
    inventory=json.loads((root/"audit/stage_pathfinding/stage_inventory.json").read_text(encoding="utf-8"))
    def find_id(value,bit):
        if isinstance(value,dict):
            for k,v in value.items():
                if k=="id" and isinstance(v,str) and v.startswith(f"opera.act.{bit:02}."): return v
                found=find_id(v,bit)
                if found:return found
        elif isinstance(value,list):
            for v in value:
                found=find_id(v,bit)
                if found:return found
    for name,source in [("DIEGETIC_EXPECTED_STATIONS","EXPECTED_STATIONS"),("DIEGETIC_PLAYABLE_PHASE_STATIONS","PLAYABLE_PHASE_STATIONS")]:
        order=list(const("probe_opera_diegetic_paths",source))
        for row in jobs:
            if row["id"] in order:row["compat_order"][name]=order.index(row["id"])
    for row in jobs:
        jid=row["id"]
        row["stage_inventory_id"]=find_id(inventory,row["star_bit"])
        if row["competition"].get("cooperative"):row["capabilities"].append("cooperative_win_suffix")
        # Explicit required file inventory includes phase cues and the exact
        # currently authored per-career Roshan clips. It never fabricates clips.
        keys=[p["vo"] for p in row["phases"]]
        keys += [p["vo"] for p in (row["chapter2"].get("scene") or {}).get("phases",[])]
        if jid=="teacher":
            keys += [p.stem for p in sorted((root/"assets/audio/teacher").glob("*.ogg"))]
        else:
            keys += [p.stem.removeprefix("roshan_") for p in sorted((root/"assets/audio/voices").glob("roshan_op_"+jid+"_*.ogg"))]
        row["voice"]["required_keys"]=list(dict.fromkeys(keys))
        if jid=="nursery":row["voice"]["event_speakers"]={p["vo"]:p["speaker"].lower() for p in row["phases"] if "speaker" in p}
        row["art"]["props"]=list(dict.fromkeys(spec["path"] for spec in row["hotspots"].values()))
    config["save_checkpoint_normalization_prefix"]=baseline_checkpoint_order(root,BASELINE,{"SAVE_CHECKPOINTS":{j["id"]:j["save"]["checkpoint"] for j in jobs if j["save"]["checkpoint"]}})
    namespace={"save_key":"opera_stars","highest_allocated_bit":max(e["star_bit"] for e in entries),
      "derived_ceiling":(1<<len(entries))-1,"next_free_bit":len(entries)}
    out.mkdir(parents=True,exist_ok=True)
    (out/".gdignore").write_bytes(b"")
    (out/"jobs").mkdir(exist_ok=True)
    for name,value in [("catalog.json",config),("compatibility.json",{"schema":"job_compatibility/1","registries":registry_manifest}),("jobs/_ledger.json",{"schema":"job_ledger/1","star_namespace":namespace,"entries":entries})]:
        (out/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    for row in jobs:
        (out/"jobs"/(row["id"]+".json")).write_text(json.dumps(row,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    schema=root/"content/job_record.schema.json"
    if schema.is_file() and schema.resolve()!=(out/"job_record.schema.json").resolve():
        (out/"job_record.schema.json").write_bytes(schema.read_bytes())
    print(f"Extracted {len(jobs)} jobs, {len(entries)} allocations, {len(registry_manifest)} mapped registries.")

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out",required=True,type=Path)
    ap.add_argument("--root",type=Path,default=Path(__file__).resolve().parents[1])
    args=ap.parse_args()
    extract(args.root,args.out)
    return 0

if __name__=="__main__":raise SystemExit(main())

