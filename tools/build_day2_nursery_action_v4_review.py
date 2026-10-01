"""Build the versioned, source-qualified nursery review without changing artwork."""
from pathlib import Path
import hashlib
import html
import json

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "audit/day2_nursery_action_v4_20261001"
SOURCE = ROOT / "assets_src/imagegen/day2_nursery_motionkeys_20261001"
LOWER = ROOT / "assets_src/imagegen/day2_nursery_lower_bridge_20261001"
STYLE = """body{margin:0;background:#eef5ff;color:#26304e;font:17px/1.55 system-ui}main{max-width:1180px;margin:auto;padding:24px}a{color:#504296}h1,h2,h3{line-height:1.2}.notice,article,section{background:white;border-radius:18px;padding:20px;margin:18px 0}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px}.grid article{margin:0}.art{background:repeating-conic-gradient(#dce5ed 0% 25%,#f8fbff 0% 50%) 50%/24px 24px;border-radius:12px}img{max-width:100%;height:auto;display:block}small{display:block;color:#4a5264}table{width:100%;border-collapse:collapse}td,th{text-align:left;padding:9px;border-bottom:1px solid #dce1eb}input[type=range]{width:100%}button,select{font:inherit;padding:8px;border:1px solid #adbad2;border-radius:8px}.frame{width:100%;background:#182149}details{margin:18px 0}code{overflow-wrap:anywhere}pre{white-space:pre-wrap;overflow-wrap:anywhere}nav{display:flex;gap:18px;flex-wrap:wrap}@media(max-width:520px){main{padding:12px}table{font-size:14px}td,th{padding:5px}}"""
NAMES = ["Anticipation / available", "Receive", "Lift", "Hold / carry", "First lower", "Lower", "Reach down", "Set down"]
NOTES = [
    "The open palms, warm face and complete fin establish a connected care body. Loaded but not sampled by the current receiving controller.",
    "Cupped palms, sleeves, elbows and torso belong to one complete silhouette; the source contains no baked baby. Actual catch requires the visible palms to arrive.",
    "Hands rise close to the face while the apron and rainbow hair remain recognizable. The same separate baby stays on the measured palm socket.",
    "Support near the chest reads clearly at the fitted extent. The short whole-body carry keeps the baby attached to the authored palms.",
    "Forward palms and connected elbows communicate lowering. The preceding hold-to-lower boundary still has a 28.32px vertical palm jump.",
    "The next downward pose retains costume and tail identity. Its similarity to the preceding key requires temporal review rather than assuming motion quality.",
    "Downward attention and a longer connected reach prepare placement. Native pixels remain complete through the packing window.",
    "Low palms approach painted cushion support. This held final state is visible before feeding; empty return still needs acting review.",
]

def save_json(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

def page(path, title, content):
    path.write_text(f'<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)}</title><style>{STYLE}</style><main><h1>{html.escape(title)}</h1>{content}</main></html>\n', encoding="utf-8")

def link(path, text):
    return f'<a href="{html.escape(path)}">{html.escape(text)}</a>'

def image(path, caption):
    return f'<a href="{html.escape(path)}"><img class="art" loading="lazy" src="{html.escape(path)}" alt="{html.escape(caption)}"></a>'

def main():
    if (OUT / "MANIFEST.json").exists():
        raise SystemExit("This review packet is sealed. Start a new revision instead of rebuilding.")
    pack = json.loads((SOURCE / "PACK_REPORT.json").read_text())
    rows = [{"id": f"N4-CARE-{i:02}", "name": NAMES[i], "source_style_score": 4.6,
             "review": NOTES[i], "runtime_observed": i != 0, "owner_accepted": False,
             "source_path": pose["path"], "sha256": pose["sha256"]} for i, pose in enumerate(pack["poses"])]
    originals = [{"id": f"D2A-{391+i:04}", "name": color + " baby", "source_path": f"assets/opera/worlds/nursery/baby_{i}.png",
                  "source_style_score": 4.5, "mounted_score": 4.3, "priority": True,
                  "review": "Constant 72px extent preserves this baby's identity through falling, support and resting. The fine facial and swaddle treatment remains static and more naturalistic than the new care body. Refine individually; keep this original recoverable."}
                 for i, color in enumerate(["Aqua", "Pink", "Violet"])]
    originals.append({"id": "D2A-0078", "name": "Faron", "source_path": "assets/opera/worlds/actors/faron_nursery.png",
                      "source_style_score": 4.4, "mounted_score": 4.1, "priority": True,
                      "review": "The complete nursery costume and silhouette remain clear. The more adult, detailed treatment and static baked baby differ from the simplified care body; safe pickup and return are not shown."})
    reviews = {"schema": "reef.job-artwork.nursery-v4.v1", "baseline": "10fd9ff3b7bc8fbbcc5e82aa63db00bbaaf41b64",
               "reviewer": "Codex drafting review", "owner_accepted": False, "source_items": rows,
               "original_items": originals, "action_score": 4.2, "connected_assembly_score": 4.3,
               "cushion_score": 4.6, "safe_return_score": 3.4,
               "inclusive_priority_threshold": 4.5,
               "acceptance": "Incomplete. Source-style opinions are separate from mounted interaction, device, child and owner acceptance."}
    save_json(OUT / "reviews.json", reviews)
    contract = {"schema": "reef.interactive-action-contract.v1", "character": "Roshan",
                "profile": "design/animation/ROSHAN_MOVEMENT_LANGUAGE.md", "intent": "Receive, support, carry and gently place one baby on a cushion",
                "lane": "interactive_gameplay_authored_states", "progress_owner": "OperaNurseryCatch / OperaCareerWorld2D",
                "presentation_owner": "OperaNurseryCare", "clip_duration_seconds": 1.42,
                "body_card_extent_px": 250, "baby_extent_px": 72,
                "states": [{"index": i, "name": NAMES[i]} for i in range(8)],
                "contact": "One retained transfer; the baby bottom follows the measured authored palm socket until fixed cushion support. Other fallers wait during care.",
                "trigger": "Fresh intentional one-finger input and arrival of the visible palms; no passive catch or reward",
                "exit": "Final transfer settles before FEED; normal route actor becomes visible in its retained room rest",
                "known_failure": "Hold-to-first-lower hip-relative palm change: [2.9296875,28.3203125] screen pixels. Action remains 4.2.",
                "safe_return": "Separate unresolved 3.4 action: existing safe fade does not show pickup and return.",
                "evidence": "body_v3/capture_index.json", "device": "PENDING", "child": "PENDING", "owner": "PENDING"}
    save_json(OUT / "ACTION_CONTRACT.json", contract)
    cards = ''.join(f'<article id="{r["id"]}"><h3>{r["id"]} · {r["name"]}</h3>{image("../../"+r["source_path"],r["name"])}<strong>4.6/5 source style</strong><p>{r["review"]}</p><small>Owner acceptance pending. '+('Not sampled in this action.' if not r['runtime_observed'] else 'Action quality is separately scored below.')+'</small></article>' for r in rows)
    oldcards = ''.join(f'<article id="{r["id"]}"><h3>{r["id"]} · {r["name"]}</h3>{image("../../"+r["source_path"],r["name"])}<strong>{r["mounted_score"]}/5 mounted; {r["source_style_score"]}/5 source</strong><p>{r["review"]}</p></article>' for r in originals)
    histories = [('body_v3', 'Current source: repaired feeding layout'), ('body_v2', 'Earlier source: before feeding overlap repair'), ('body', 'Qualified history: source edited during capture'), ('contact', 'Contact-only history: before connected body')]
    gallery = ''
    traces = []
    for folder, title in histories:
        cases = []
        for aspect in ['1280x720', '1600x720']:
            capture = json.loads((OUT / folder / f'catch-{aspect}.json').read_text())
            frames = capture['frames']
            for f in frames:
                raw = (OUT / folder / f['image']).read_bytes()
                assert hashlib.sha256(raw).hexdigest() == f['sha256']
            cases.append({"folder": folder, "title": title, "id": capture['id'], "dimensions": capture['dimensions'], "frames": frames})
            gallery += f'<details><summary>{title} · {aspect} · {len(frames)} native samples</summary><div class="grid">'
            for f in frames:
                caption = f'{f["driver_t"]:.3f}s · '+(f'care key {f["care_key"]} · ' if 'care_key' in f else '')+f'{f["caught"]} caught, {f["missed"]} missed'
                gallery += '<article>'+image(folder+'/'+f['image'], caption)+f'<small>{caption}</small></article>'
            gallery += '</div></details>'
        traces.extend(cases)
    save_json(OUT / 'trace_library.json', traces)
    options = ''.join(f'<option value="{i}">{html.escape(t["title"])} · {t["id"]}</option>' for i, t in enumerate(traces))
    player = f'<section><h2>Inspect actual sampled frames</h2><label for="trace">Trace</label> <select id="trace">{options}</select><p id="state"></p><img id="frame" class="frame" alt="Native sampled nursery frame"><label for="position">Sample index</label><input id="position" type="range" min="0" value="0"><p>Processing was fixed 30 fps. The current trace records regular 2 fps samples plus every authored-key change; intervals vary. These samples do not prove every frame of motion. No frame interpolation is used.</p></section>'
    script = """<script>fetch('trace_library.json').then(r=>r.json()).then(data=>{const trace=document.querySelector('#trace'),pos=document.querySelector('#position'),frame=document.querySelector('#frame'),state=document.querySelector('#state');function show(){const t=data[+trace.value],f=t.frames[+pos.value];frame.src=t.folder+'/'+f.image;state.textContent=`Sample ${+pos.value+1}/${t.frames.length} · ${f.driver_t.toFixed(3)}s · key ${f.care_key??'detached arms'} · ${f.caught} caught · ${f.missed} missed · phase ${f.phase}`;}function choose(){pos.max=data[+trace.value].frames.length-1;pos.value=0;show();}trace.addEventListener('change',choose);pos.addEventListener('input',show);choose();}).catch(e=>document.querySelector('#state').textContent='Trace data failed to load: '+e.message);</script>"""
    header = '<div class="notice"><strong>Draft revision · incomplete all-jobs goal</strong><p>Connected care body and painted support improve the nursery. Receiving/carrying/lowering remains 4.2/5, below the requested bar; twelve new source candidates have individual 4.6 opinions. No global 4.5 pass, owner approval or final report is claimed.</p></div><nav>'+link('REPORT.md','Written report')+link('reviews.json','Individual scores')+link('ACTION_CONTRACT.json','Action contract')+link('../job_artwork_refinement_live/index.html','Live all-jobs entry')+link('../../assets_src/imagegen/day2_nursery_lower_bridge_20261001/index.html','Four next bridge candidates')+'</nav>'
    summary = '<section><h2>Mounted/action priorities</h2><table><tr><th>Item</th><th>Score</th><th>Next work</th></tr><tr><td>Painted receiving cushions</td><td>4.6</td><td>Keep pixels; verify physical contact at every slot.</td></tr><tr><td>Connected care assembly</td><td>4.3</td><td>Complete action and empty return.</td></tr><tr><td>Receiving/carry/lowering</td><td>4.2</td><td>Audit additional lowering in-betweens.</td></tr><tr><td>Miss and safe return</td><td>3.4</td><td>Show a truthful supported pickup and return.</td></tr></table><p>Original trusted Opera2D failure and repaired three-probe rerun are retained in machine/. A probe pass does not change a visual score. Current source hashes are stable across body_v3; body/ preserves its source-edit qualification.</p></section>'
    page(OUT/'index.html','Nursery care revision4 — individual artwork and action review',header+summary+'<h2>Eight individually scored source keys</h2><div class="grid">'+cards+'</div><h2>Original live items still prioritized</h2><div class="grid">'+oldcards+'</div>'+player+'<h2>Every retained sample</h2>'+gallery+script)
    page(SOURCE/'index.html','Eight connected nursery care source keys', '<p>Each source key has a provisional4.6 style opinion. Runtime action remains4.2. Native source pixels and earlier evidence remain preserved.</p>'+image('candidates/attempt-01.png','Complete native eight-key generation')+'<p>'+link('PROMPT.txt','Prompt')+' · '+link('SOURCE_GAP.json','Inventory and named gap')+' · '+link('PACK_REPORT.json','Exact RGBA reconstruction and socket estimates')+' · '+link('../../../audit/day2_nursery_action_v4_20261001/index.html','Individual fitted/action review')+'</p>')
    page(LOWER/'index.html','Four lowering bridge source candidates', '<p>Four provisional4.6 source-style opinions. Native geometry, fitted sockets and runtime integration remain pending. These keys are not part of the8-key action.</p>'+image('candidates/attempt-01.png','Complete native four-key bridge generation')+'<p>'+link('REPORT.md','Four individual written reviews')+' · '+link('PROMPT.txt','Prompt')+' · '+link('SOURCE_GAP.json','Measured named gap')+' · '+link('../../../audit/day2_nursery_action_v4_20261001/index.html','Current action4.2 review')+'</p>')
    live = ROOT/'audit/job_artwork_refinement_live'
    live.mkdir(exist_ok=True)
    (live/'.gdignore').touch()
    page(live/'index.html','Mermaid Roshan jobs artwork — live review entry','<div class="notice"><strong>Reversible refinement in progress</strong><p>The sealed first pass contains777 source items,240 pose cells and35 job/context families. Hundreds of weak items and played actions remain. Day One cleaning census is pending. Final owner approval follows a complete report.</p></div><nav>'+link('../day2_nursery_action_v4_20261001/index.html','Latest nursery revision')+link('../day2_job_contexts_2026-09-30/index.html','All777 sources and contexts')+link('../day2_action_continuity_20261001/index.html','Eleven timed action pilots')+link('../../assets_src/local_motion/day2_batch1_20260930/index.html','Five ComfyUI reference studies')+'</nav><section><h2>Underlying development trigger</h2><p>Refresh source fingerprints with <code>python -B tools/refresh_job_artwork_status.py</code>. A changed hash requests re-review; it never assigns a pass or changes scores.</p><pre id="status">Loading saved status…</pre></section><script>fetch("STATUS.json").then(r=>r.json()).then(d=>{document.querySelector("#status").textContent=JSON.stringify({checked_utc:d.checked_utc,capture_freshness:d.capture_freshness,coverage:d.coverage},null,2)}).catch(e=>document.querySelector("#status").textContent=e.message)</script>')
    # Follow-up sources stay separate from the unchanged current runtime score.
    followup = '<p>'+link('../../assets_src/imagegen/day2_nursery_babies_v2_20261001/index.html','Three new infant alternatives and native held fits')+' · source/held-fit4.6 only; original infants remain bound. '+link('../day_one_job_art_census_20261001/index.html','Day One source discovery and individual opinions')+' · complete played-context coverage remains open.</p>'
    current_page=(OUT/'index.html').read_text(encoding='utf-8')
    (OUT/'index.html').write_text(current_page.replace('</main>',followup+'</main>'),encoding='utf-8')
    live_page=(live/'index.html').read_text(encoding='utf-8')
    live_page=live_page.replace('Day One cleaning census is pending.','Day One has an additional48-file/179-drawing-function discovery census,36 new source opinions,12 earlier byte-identical opinions and30 individually scored source cells. Full discovery and all played-context review remain open.')
    live_links=link('../../assets_src/imagegen/day2_nursery_babies_v2_20261001/index.html','Three new infant alternatives and native held fits')+link('../day_one_job_art_census_20261001/index.html','Day One source discovery and individual opinions')
    (live/'index.html').write_text(live_page.replace('</nav>',live_links+'</nav>',1),encoding='utf-8')
    print('NURSERY_V4_REVIEW|PASS|8 source opinions,4 original live items,all retained native samples; follow-up sources separate')

if __name__ == '__main__':
    main()
