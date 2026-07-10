#!/usr/bin/env python3
"""GEN2 overnight batch generation — nano banana 2 (gemini-3-pro-image).

Generates 4 style-bible variants for every visual DISCARD role in
gen2/visual_roles.json via the Gemini Batch API, then analyzes every image
(vision pass) and writes gen2/generated/ + ANALYSIS.md.

Key comes from .secrets/gemini_key or $GEMINI_API_KEY — never committed.
Usage: python3 tools/gen2_batch.py run_all   (logs progress to stdout)
"""
import base64
import json
import os
import sys
import time
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API = "https://generativelanguage.googleapis.com/v1beta"
MODEL = "models/gemini-3-pro-image"
ANALYZE_MODEL = "models/gemini-2.5-flash"
OUT = os.path.join(ROOT, "gen2", "generated")
LEDGER = os.path.join(ROOT, "gen2", "generated", "ledger.json")
VARIANTS = 4
CHUNK = 60  # requests per batch job (defensive against inline size limits)

STYLE = (
    "Mermaid Roshan storybook game-sprite style: flat color anime / modern "
    "cel-shaded webtoon aesthetic, crisp thin black outlines, high-key "
    "vibrant pastel palette (aqua, lavender, coral pink, seafoam green, "
    "sunny gold), toy-like rounded proportions, whimsical and friendly for "
    "a 4-year-old. SINGLE SUBJECT ONLY, fully in frame, centered, 3/4 or "
    "side view suitable as a 2D game sprite. PLAIN SOLID WHITE background - "
    "no scene, no ground shadow, no vignette, no text, no watermark. Clean "
    "sharp edges for cutout extraction. STRICT: no bubbles, no water "
    "droplets, no sparkles, no confetti, no flower/star decals painted on "
    "the subject; no white sticker border; scenery objects (corals, rocks, "
    "plants, buildings, props) must NOT have faces - faces only on actual "
    "creatures; exactly ONE object, never a cluster or group. IDENTITY: "
    "depict ONLY the named subject, plain and instantly readable - do not "
    "blend it with other concepts, and put nothing growing on, attached "
    "to, or merged into it (a rock is just a rock). ABSOLUTELY NO "
    "CHARACTERS: no mermaids, no people, no children, no invented mascots "
    "anywhere in the image - the subject is an empty, unoccupied object."
)
TILE_STYLE = (
    "Seamlessly TILEABLE square texture, hand-painted storybook style, flat "
    "cel-shaded color with soft painterly variation, high-key pastel "
    "palette, no hard directional lighting, no text, edges must wrap "
    "seamlessly left-right and top-bottom. Uniform small-scale detail "
    "only - no large distinct clumps or landmarks that reveal repetition."
)

SPECIAL = {
    "galaxy_fruit_apple": "a plain shiny red apple with one leaf - just the fruit, nothing else",
    "galaxy_fruit_banana": "a plain yellow banana - just the fruit, nothing else",
    "galaxy_fruit_melon": "a plain watermelon half showing pink flesh - just the fruit, nothing else",
    "galaxy_fruit_orange": "a plain orange with one leaf - just the fruit, nothing else",
    "galaxy_tray": "a plain empty oval serving plate",
    "galaxy_butterfly1": "a single pretty butterfly with open wings, top-down view",
    "galaxy_butterfly2": "a single pretty butterfly with open wings, side view",
    "kits_swing_a_large": "an empty children's playground swing set: A-frame posts with two hanging swings, no people",
    "kits_swing_b_large": "an empty children's playground swing set with a wide bench swing, no people",
    "kits_slide_a": "an empty children's playground slide with ladder, no people",
    "kits_seesaw_large": "an empty children's playground seesaw, no people",
    "kits_sandbox_round_decorated": "an empty round sandbox with sand and small sandcastles, no people",
    "kits_merry_go_round": "an empty playground merry-go-round spinner, no people",
    "kits_spring_horse_a": "an empty playground spring rider shaped like a pony, no people",
    "ship_ship_ghost": "a friendly rounded ghost pirate ship with softly glowing pastel sails, magical not scary",
    "ship_ship_wreck": "a charming sunken wooden shipwreck, tilted on the seabed, overgrown with pastel coral",
    "ship_cliff_cave_rock": "a large rounded undersea cliff rock with a dark friendly cave opening",
    "galaxy_crystal_castle": "a sparkling fairy-tale crystal castle with rounded spires",
    "castle_bed": "a cozy royal single bed with carved posts and a fluffy pastel quilt",
    "castle_throne": "a golden fairy-tale throne with heart and shell motifs and plush pink cushion",
    "vehicles_gokart": "a cute chunky go-kart, toy-like proportions",
    "vehicles_monstertruck": "a cute chunky monster truck with huge wheels, toy-like",
    "vehicles_motorcycle": "a cute chunky purple cartoon motorcycle, toy-like",
    "kits_wall_narrow_gate": "a chunky pastel castle wall piece with an arched gate opening and crenellated top",
    "terrain_up_water_nrm": None,
}
CATEGORY_HINT = {
    "aquatic": "an underwater reef creature or coral for a mermaid game",
    "nature": "a meadow plant, tree, rock or mushroom for a storybook island",
    "kits": "a chunky modular pastel castle building piece (storybook toy castle)",
    "galaxy": "a garden-world object (do NOT add wings or butterfly parts to it)",
    "ship": "a pirate-sea object for a friendly mermaid reef",
    "terrain": "TILEABLE ground texture",
    "castle": "royal castle furniture",
    "vehicles": "a toy vehicle for a rainbow race",
}


def key():
    p = os.path.join(ROOT, ".secrets", "gemini_key")
    if os.path.exists(p):
        return open(p).read().strip()
    return os.environ["GEMINI_API_KEY"]


def call(method, path, body=None, tries=5):
    for a in range(tries):
        try:
            req = urllib.request.Request(
                API + path,
                data=json.dumps(body).encode() if body is not None else None,
                headers={"x-goog-api-key": key(), "Content-Type": "application/json"},
                method=method,
            )
            with urllib.request.urlopen(req, timeout=300) as r:
                return json.loads(r.read())
        except Exception as e:  # noqa: BLE001 - retry on transient API errors
            print(f"  api retry {a+1}/{tries}: {e}", flush=True)
            time.sleep(60 * (a + 1))
    raise RuntimeError(f"API failed after {tries} tries: {path}")


def describe(role):
    if role in SPECIAL and SPECIAL[role]:
        return SPECIAL[role]
    cat, _, rest = role.partition("_")
    words = rest.replace("up_", "").replace("_col", " tileable surface").replace("_", " ")
    return f"{words} - {CATEGORY_HINT.get(cat, 'a game object')}"


def build_requests():
    roles = json.load(open(os.path.join(ROOT, "gen2", "visual_roles.json")))
    reqs = []
    for role in sorted(roles):
        tile = role.startswith("terrain_")
        big = tile or role.startswith(("kits_", "castle_", "ship_ship"))
        prompt = (TILE_STYLE if tile else STYLE) + "\n\nSubject: " + describe(role) + "."
        for v in range(1, VARIANTS + 1):
            reqs.append({
                "metadata": {"key": f"{role}__v{v}"},
                "request": {
                    "contents": [{"parts": [{"text": prompt + f" (variation {v} of {VARIANTS}: vary the design, keep the style)"}]}],
                    "generationConfig": {
                        "responseModalities": ["TEXT", "IMAGE"],
                        "imageConfig": {"aspectRatio": "1:1", "imageSize": "2K" if big else "1K"},
                    },
                },
            })
    return reqs


def submit_all():
    reqs = build_requests()
    print(f"{len(reqs)} requests -> {((len(reqs)-1)//CHUNK)+1} batch jobs", flush=True)
    jobs = []
    for i in range(0, len(reqs), CHUNK):
        chunk = reqs[i:i + CHUNK]
        body = {"batch": {
            "displayName": f"gen2-art-{i//CHUNK}",
            "inputConfig": {"requests": {"requests": chunk}},
        }}
        r = call("POST", f"/{MODEL}:batchGenerateContent", body)
        jobs.append(r["name"])
        print(f"  submitted {r['name']} ({len(chunk)} reqs)", flush=True)
        time.sleep(5)
    json.dump(jobs, open(os.path.join(OUT, "jobs.json"), "w"))
    return jobs


def poll(jobs):
    done = {}
    while len(done) < len(jobs):
        for name in jobs:
            if name in done:
                continue
            st = call("GET", f"/{name}")
            state = st.get("metadata", {}).get("state", st.get("state", "?"))
            print(f"  {name}: {state}", flush=True)
            if "SUCCEEDED" in str(state):
                done[name] = st
            elif "FAILED" in str(state) or "CANCELLED" in str(state):
                done[name] = st
                print(f"  !! {name} ended {state}", flush=True)
        if len(done) < len(jobs):
            time.sleep(180)
    return done


def harvest(done):
    n_ok = 0
    for name, st in done.items():
        resp = st.get("response", {})
        inlined = resp.get("inlinedResponses", {}).get("inlinedResponses", [])
        for item in inlined:
            k = item.get("metadata", {}).get("key", "unknown")
            role, _, ver = k.partition("__")
            parts = (item.get("response", {}).get("candidates", [{}])[0]
                     .get("content", {}).get("parts", []))
            for p in parts:
                blob = p.get("inlineData")
                if blob and blob.get("mimeType", "").startswith("image/"):
                    d = os.path.join(OUT, role)
                    os.makedirs(d, exist_ok=True)
                    open(os.path.join(d, f"{ver}.png"), "wb").write(
                        base64.b64decode(blob["data"]))
                    n_ok += 1
                    break
    print(f"harvested {n_ok} images", flush=True)
    return n_ok


def analyze():
    from PIL import Image
    results = {}
    for role in sorted(os.listdir(OUT)):
        d = os.path.join(OUT, role)
        if not os.path.isdir(d):
            continue
        for f in sorted(os.listdir(d)):
            if not f.endswith(".png"):
                continue
            p = os.path.join(d, f)
            im = Image.open(p)
            im.thumbnail((512, 512))
            import io
            buf = io.BytesIO()
            im.convert("RGB").save(buf, "JPEG", quality=80)
            b64 = base64.b64encode(buf.getvalue()).decode()
            body = {"contents": [{"parts": [
                {"inlineData": {"mimeType": "image/jpeg", "data": b64}},
                {"text": "Score this game-sprite candidate 1-10 on: style (flat "
                         "cel-shaded, thin black outlines, pastel), background "
                         "purity (plain white, single subject), and sprite "
                         "usability (clean silhouette, fully in frame). Reply "
                         "ONLY JSON: {\"style\":n,\"background\":n,\"usable\":n,"
                         "\"note\":\"<10 words\"}"}]}]}
            try:
                r = call("POST", f"/{ANALYZE_MODEL}:generateContent", body, tries=3)
                txt = r["candidates"][0]["content"]["parts"][0]["text"]
                txt = txt[txt.find("{"):txt.rfind("}") + 1]
                results[f"{role}/{f}"] = json.loads(txt)
            except Exception as e:  # noqa: BLE001
                results[f"{role}/{f}"] = {"error": str(e)[:80]}
            time.sleep(1.2)
    json.dump(results, open(os.path.join(OUT, "analysis.json"), "w"), indent=1)
    # best-of-4 summary
    lines = ["# GEN2 batch analysis - best variant per role\n"]
    byrole = {}
    for k, v in results.items():
        if "error" in v:
            continue
        role = k.split("/")[0]
        score = v["style"] + v["background"] + v["usable"]
        if score > byrole.get(role, (0, ""))[0]:
            byrole[role] = (score, k, v.get("note", ""))
    for role, (score, k, note) in sorted(byrole.items()):
        lines.append(f"- **{role}**: {k} ({score}/30) - {note}")
    open(os.path.join(OUT, "ANALYSIS.md"), "w").write("\n".join(lines) + "\n")
    print(f"analyzed {len(results)} images, {len(byrole)} roles ranked", flush=True)




def analyze_batch():
    """Batch-API analysis: no interactive rate limits."""
    import io
    from PIL import Image
    reqs = []
    for role in sorted(os.listdir(OUT)):
        d = os.path.join(OUT, role)
        if not os.path.isdir(d):
            continue
        for f in sorted(os.listdir(d)):
            if not f.endswith((".png", ".webp")):
                continue
            im = Image.open(os.path.join(d, f))
            im.thumbnail((384, 384))
            buf = io.BytesIO()
            im.convert("RGB").save(buf, "JPEG", quality=75)
            reqs.append({
                "metadata": {"key": f"{role}/{f}"},
                "request": {"contents": [{"parts": [
                    {"inlineData": {"mimeType": "image/jpeg",
                                    "data": base64.b64encode(buf.getvalue()).decode()}},
                    {"text": "Score this game-sprite candidate 1-10 on: style "
                             "(flat cel-shaded, thin black outlines, pastel), "
                             "background purity (plain white, single subject), "
                             "and sprite usability (clean silhouette, fully in "
                             "frame). Reply ONLY JSON: {\"style\":n,"
                             "\"background\":n,\"usable\":n,\"note\":\"<10 words\"}"}]}]},
            })
    print(len(reqs), "analysis requests", flush=True)
    ckpt = os.path.join(OUT, "analysis_jobs.json")
    jobs = json.load(open(ckpt)) if os.path.exists(ckpt) else []
    AC = 50
    for i in range(len(jobs) * AC, len(reqs), AC):
        body = {"batch": {"displayName": f"gen2-analysis-{i//AC}",
                          "inputConfig": {"requests": {"requests": reqs[i:i+AC]}}}}
        r = call("POST", f"/{ANALYZE_MODEL}:batchGenerateContent", body, tries=10)
        jobs.append(r["name"])
        json.dump(jobs, open(ckpt, "w"))
        print("  submitted", r["name"], flush=True)
        time.sleep(60)   # the key is quota-tight after the overnight run
    done = poll(jobs)
    results = {}
    for name, st in done.items():
        for item in st.get("response", {}).get("inlinedResponses", {}).get("inlinedResponses", []):
            k = item.get("metadata", {}).get("key", "?")
            try:
                txt = item["response"]["candidates"][0]["content"]["parts"][0]["text"]
                txt = txt[txt.find("{"):txt.rfind("}") + 1]
                results[k] = json.loads(txt)
            except Exception as e:  # noqa: BLE001
                results[k] = {"error": str(e)[:80]}
    json.dump(results, open(os.path.join(OUT, "analysis.json"), "w"), indent=1)
    lines = ["# GEN2 batch analysis - best variant per role\n"]
    byrole = {}
    for k, v in results.items():
        if "error" in v:
            continue
        role = k.split("/")[0]
        score = v["style"] + v["background"] + v["usable"]
        if score > byrole.get(role, (0, "", ""))[0]:
            byrole[role] = (score, k, v.get("note", ""))
    for role, (score, k, note) in sorted(byrole.items()):
        lines.append(f"- **{role}**: {k} ({score}/30) - {note}")
    open(os.path.join(OUT, "ANALYSIS.md"), "w").write("\n".join(lines) + "\n")
    print(f"analyzed {len(results)}, ranked {len(byrole)} roles", flush=True)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    mode = sys.argv[1] if len(sys.argv) > 1 else "run_all"
    if mode == "run_all":
        t0 = time.time()
        jobs = submit_all()
        done = poll(jobs)
        n = harvest(done)
        json.dump({"jobs": len(jobs), "images": n,
                   "wall_minutes": round((time.time() - t0) / 60, 1)},
                  open(LEDGER, "w"))
        analyze()
        print("ALL DONE", flush=True)
    elif mode == "analyze_batch":
        analyze_batch()
        print("ALL DONE", flush=True)
    elif mode == "resume":
        jobs = json.load(open(os.path.join(OUT, "jobs.json")))
        done = poll(jobs)
        harvest(done)
        analyze()
        print("ALL DONE", flush=True)
