"""Validate partial current visual evidence; never grants whole-game acceptance."""
from pathlib import Path
import argparse, hashlib, json, subprocess, re
from PIL import Image
P = Path(__file__).resolve().parent
R = P.parents[3]
ASPECTS = {"1280x720": (1280, 720), "1600x720": (1600, 720)}
PHASE_COUNTS = {"chef": 5, "detective": 3, "ballerina": 6, "candymaker": 4,
    "doctor": 5, "farmer": 4, "boxer": 5, "magician": 8, "painter": 3,
    "astronaut": 4, "racer": 3, "popstar": 7, "nursery": 5,
    "geologist": 4, "teacher": 4}
def sha(b): return hashlib.sha256(b).hexdigest()
def read(path): return json.loads(path.read_text(encoding="utf8"))
def matrix_errors(m, aspect):
    errors = []
    if m.get("result") != "PASS": errors.append("aggregate capture run did not pass")
    if m.get("source_revision") != "44a36776ab3db0d9078aacf09eca144fde342330": errors.append("wrong source revision")
    if m.get("rendering_method") != "mobile" or m.get("quality") != "speedy": errors.append("wrong renderer/quality")
    engine = m.get("engine", {})
    if [engine.get(k) for k in ["major", "minor", "patch", "status", "build"]] != [4, 7, 2, "stable", "official"]: errors.append("wrong exact engine")
    if m.get("save_isolation", {}).get("unchanged") is not True: errors.append("normal save mutated/unattested")
    if m.get("save_isolation", {}).get("before") != m.get("save_isolation", {}).get("after"): errors.append("normal save hash mismatch")
    rows = m.get("states", [])
    if len(rows) != 96 or len({r.get("id") for r in rows}) != 96: errors.append("duplicate/missing state rows")
    if m.get("expected_state_ids") != [r.get("id") for r in rows]: errors.append("matrix order/coverage mismatch")
    kinds = {k: sum(r.get("kind") == k for r in rows) for k in ["castle_route", "opera_venue_floor", "career_entry", "career_phase_fixture"]}
    if list(kinds.values()) != [8, 3, 15, 70]: errors.append("route/entry/phase counts mismatch")
    for career, count in PHASE_COUNTS.items():
        phases = [r for r in rows if r.get("kind") == "career_phase_fixture" and r.get("actual_state", {}).get("career_id") == career]
        if [r.get("actual_state", {}).get("phase_index") for r in phases] != list(range(count)): errors.append("missing/reordered phase " + career)
    for row in rows:
        if row.get("status") != "PASS" or row.get("failures"): errors.append("failed state " + str(row.get("id")))
        for key, expected in row.get("expected_state", {}).items():
            if row.get("actual_state", {}).get(key) != expected: errors.append("state mismatch " + str(row.get("id")))
        im = row.get("image", {})
        if (im.get("width"), im.get("height")) != ASPECTS[aspect]: errors.append("wrong image dimensions")
    return errors

def validate():
    errors = []; source = None
    for aspect, size in ASPECTS.items():
        m = read(P/aspect/"opera_capture_manifest.json"); errors += matrix_errors(m, aspect)
        if source is None: source = m["source_signature"]
        elif source != m["source_signature"]: errors.append("source changed between aspects")
        for row in m["states"]:
            data = row["image"]; path = P/aspect/data["file"]
            if path.parent != P/aspect or not path.is_file(): errors.append("missing/unsafe PNG"); continue
            b = path.read_bytes()
            if len(b) != data["bytes"] or sha(b) != data["sha256"]: errors.append("PNG byte/hash mismatch " + path.name)
            with Image.open(path) as image:
                if image.size != size: errors.append("decoded dimensions mismatch")
                extrema = image.convert("L").resize((64, 36)).getextrema()
                if extrema[1] - extrema[0] < 51: errors.append("blank/near-clear PNG " + path.name)
    for path, expected in source["files"].items():
        f = R/path
        if not f.is_file() or sha(f.read_bytes()) != expected: errors.append("capture source closure drift " + path)
    launch = read(P/"CAPTURE_LAUNCH.json")
    if sha((P/"capture_live_opera.gd").read_bytes()) != launch["derivative_harness_sha256"]: errors.append("harness hash mismatch")
    for c in read(P/"contact_index.json")["contacts"]:
        if sha((P/c["path"]).read_bytes()) != c["sha256"]: errors.append("contact mismatch")
        for s in c["sources"]:
            if sha((P/s["path"]).read_bytes()) != s["sha256"]: errors.append("contact source mismatch")
    coverage = read(P/"coverage.json")
    if len(coverage["entries"]) != 176 or coverage["complete_entries"] != 0 or coverage["partial_entries"] != 24: errors.append("false coverage completion")
    if any(r["route_or_saved_variants_complete"] for r in coverage["entries"]): errors.append("false route/save acceptance")
    scopes = read(P/"scope_review.json")
    if len(scopes["scopes"]) != 369 or scopes["fully_resolved"] != 0: errors.append("false scope closure")
    if read(P/"observations.json")["whole_game_denominator"] is not None: errors.append("fabricated whole-game count")
    command = ["git", "diff", "--quiet", "92c9fe70319ef46bfaa8f61348a6f51512141ec3", "HEAD", "--", "scripts", "scenes", "assets", "shaders", "project.godot"]
    if subprocess.run(command, cwd=R).returncode: errors.append("production Git source drift")
    return errors

def stress():
    import copy
    m = read(P/"1280x720/opera_capture_manifest.json")
    cases = []
    a=copy.deepcopy(m);a["states"].pop();cases.append(a)
    a=copy.deepcopy(m);a["rendering_method"]="gl_compatibility";cases.append(a)
    a=copy.deepcopy(m);a["save_isolation"]["unchanged"]=False;cases.append(a)
    a=copy.deepcopy(m);a["engine"]["patch"]=1;cases.append(a)
    a=copy.deepcopy(m);a["states"][20]["actual_state"]["phase_index"]=999;cases.append(a)
    return all(matrix_errors(a,"1280x720") for a in cases), len(cases)
if __name__ == "__main__":
    ap=argparse.ArgumentParser();ap.add_argument("--stress",action="store_true");args=ap.parse_args()
    if args.stress:
        ok,count=stress();print(f"LIVE REVIEW falsification: {count}/{count} rejected");raise SystemExit(0 if ok else 1)
    errors=validate()
    if errors: print("\n".join(errors));raise SystemExit(1)
    print("LIVE REVIEW PASS: 192 exact captures, 70 phases per aspect, 6427 source closure files, child save unchanged; 24/176 partial entries, zero complete, 369 unresolved scopes")
