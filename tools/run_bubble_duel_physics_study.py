"""Paired original-mechanics tuning: 25 broad designs, then 25 local refinements."""
from pathlib import Path
import argparse, hashlib, json, os, subprocess, sys, tempfile, statistics, time

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "assets_src/bubble_duel_physics_20261105"
BASE = dict(gravity=.25, strength_scale=1., lateral=.75, softcap=.9,
            ceiling_bounce=.8, ceiling_drag=.8, speed_scale=1., pop_hop=2.)

def score(row):
    bouts = row["bouts"]
    completion = sum(b["complete"] for b in bouts) / len(bouts)
    median = statistics.median(b["seconds"] for b in bouts)
    fidelity = 1 / (1 + row["source_rms_error"])
    pacing = max(0, 1 - abs(median - 35) / 120)
    return .65 * fidelity + .25 * completion + .10 * pacing

def run(engine, env, name, variants):
    config = ART / (name + "-config.json")
    output = ART / (name + "-results.json")
    config.write_text(json.dumps({"variants": variants}, indent=2) + "\n", encoding="utf-8")
    child = env.copy()
    child["DUEL_STUDY_CONFIG"] = str(config)
    child["DUEL_STUDY_REPORT"] = str(output)
    with (ART / (name + ".log")).open("w", encoding="utf-8") as log:
        proc = subprocess.run([engine, "--headless", "--path", str(ROOT),
            "-s", "scripts/probe_bubble_duel_study.gd"], cwd=ROOT, env=child,
            stdout=log, stderr=subprocess.STDOUT, timeout=1200)
    if proc.returncode or not output.exists():
        raise RuntimeError((ART / (name + ".log")).read_text(encoding="utf-8")[-8000:])
    data = json.loads(output.read_text(encoding="utf-8"))
    if data["failures"]: raise RuntimeError(data["failures"])
    return data

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bouts", type=int, default=12)
    args = parser.parse_args()
    engine = subprocess.check_output([sys.executable, "-B", "tools/resolve_godot.py"],
        cwd=ROOT, text=True).strip()
    start = time.monotonic()
    locked_path = ART / "phase2-config.json"
    locked_refinements = json.loads(locked_path.read_text(encoding="utf-8"))["variants"] if locked_path.exists() else None
    broad = [{"id": "01-source", "params": {}, "bouts": args.bouts, "require_complete": False}]
    values = {
        "gravity": [.20, .225, .275], "strength_scale": [.85, 1.1, 1.2],
        "lateral": [.5, .6, .9], "softcap": [.84, .88, .94],
        "ceiling_bounce": [.65, .9, 1.], "ceiling_drag": [.65, .9, 1.],
        "speed_scale": [.85, 1.1, 1.2], "pop_hop": [1.5, 2.5, 3.]
    }
    for key, choices in values.items():
        for value in choices:
            broad.append({"id": f"{len(broad)+1:02d}-{key}-{value}",
                "params": {key:value}, "bouts":args.bouts, "require_complete":False})
    with tempfile.TemporaryDirectory(prefix="duel-50-study-") as folder:
        env = os.environ.copy()
        for key in ["APPDATA","LOCALAPPDATA","XDG_DATA_HOME","XDG_CONFIG_HOME"]:
            target = Path(folder) / key
            target.mkdir()
            env[key] = str(target)
        phase1 = run(engine, env, "phase1", broad)
        ranked = sorted(phase1["variants"], key=score, reverse=True)
        winner = ranked[0]
        anchor = BASE | winner["params"]
        if locked_refinements is not None:
            refinements = locked_refinements
        else:
            refinements = []
            # Unique paired two-parameter refinements around the measured winner.
            axes = [("gravity",.0125),("strength_scale",.04),("lateral",.04),
                    ("ceiling_bounce",.04),("pop_hop",.2)]
            for a,(key,step) in enumerate(axes):
                for sign in [-1,1]:
                    for factor in [.5,1.]:
                        params = {k:v for k,v in anchor.items() if v != BASE[k]}
                        params[key] = round(anchor[key] + sign * step * factor, 6)
                        second,second_step = axes[(a+1)%len(axes)]
                        params[second] = round(anchor[second] - sign * second_step * .5,6)
                        refinements.append({"id":f"{26+len(refinements):02d}-refine-{key}-{sign}-{factor}",
                            "params":params, "bouts":args.bouts, "require_complete":False})
            for sign in [-2,-1,0,1,2]:
                refinements.append({"id":f"{26+len(refinements):02d}-rebound-balance-{sign}",
                    "params": winner["params"] | {"gravity":round(anchor["gravity"] + sign*.005,6),
                    "ceiling_bounce":round(anchor["ceiling_bounce"] + .015 + sign*.005,6)},
                    "bouts":args.bouts, "require_complete":False})
        configs = broad + refinements
        assert len(configs)==50 and len({json.dumps(BASE|v["params"],sort_keys=True) for v in configs})==50
        phase2 = run(engine,env,"phase2",refinements)
    ranked = sorted(phase1["variants"]+phase2["variants"],key=score,reverse=True)
    compact = [{"id":v["id"],"params":v["params"],"score":score(v),
        "source_rms_error":v["source_rms_error"],
        "completed":sum(b["complete"] for b in v["bouts"]),"bouts":len(v["bouts"]),
        "median_seconds":statistics.median(b["seconds"] for b in v["bouts"]),
        "pops":sum(b["pops"] for b in v["bouts"]),
        "bump_contacts":sum(b["bump_contacts"] for b in v["bouts"])} for v in ranked]
    report = {"selection":ranked[0]["id"],"params":ranked[0]["params"],
        "rule":"65% source trace fidelity 1/(1+RMS), 25% natural bout completion, 10% proximity to35-second bot bout; measured proxy only, not human fun.",
        "iterations":50,"bouts":sum(len(v["bouts"]) for v in ranked),
        "completed":sum(b["complete"] for v in ranked for b in v["bouts"]),
        "ranked":compact,"wall_seconds":time.monotonic()-start,
        "source_sha256":{p.name:hashlib.sha256(p.read_bytes()).hexdigest()
            for p in [ROOT/"scripts/bubble_duel_motion.gd",ROOT/"scripts/bubble_duel_arena.gd",
                      ROOT/"scripts/bubble_duel_brain.gd",ROOT/"scripts/bubble_duel_geometry.gd",
                      ROOT/"scripts/bubble_duel_test_policy.gd"]},
        "limits":"Existing phase2-config.json is locked and reused on revalidation; delete nothing silently to create a new design bank. Same paired seeds/policies across designs. Phase2 depends on measured phase1 winner. Exploratory timeouts retained and penalized. Independent complete UI bouts, physical touch, visual/child/owner review remain separate."}
    (ART/"selection.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:report[k] for k in ["selection","params","iterations","bouts","completed","wall_seconds"]}))
    return 0

if __name__=="__main__": raise SystemExit(main())
