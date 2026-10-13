from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil
import subprocess

BASE = Path(__file__).resolve().parent
REPO = Path(r'C:\Users\Peter\.codex\worktrees\flat-vector-art-audit-20261007\mermaid-roshan-reef')
OUT = BASE / 'root_picture_review_20261012'
REV = '6cde8aeae04aaedcc0b1ff22a05ef93ab9bf666f'
ENGINE = r'C:\Users\Peter\AppData\Local\Programs\MermaidReefTools\Godot\4.7.2\godot_console.exe'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')

def copy(source, target):
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    assert sha(source) == sha(target)

OUT.mkdir(exist_ok=True)
runs = [
    ('action', 'root_picture_context_20261013T004837', 'Bounded Garden raw-pointer action context. Reentry and subsequent games retain a legitimate temporary Garden medal; these four states per aspect are not clean ready views. No explicit boot/fade guards in this first harness.'),
    ('rejected_fresh', 'root_picture_fresh_20261013T005252', 'Rejected as a clean-ready evidence batch: no BootSplashHandoff guard. Four inspected frames visibly contain the boot illustration over the game. Passing process exit does not accept presentation.'),
    ('guarded_ready', 'root_picture_guarded_20261013T005623', 'Fresh Main/save per game; explicit boot/menu/intro/fade/medal guards. Eight clean ready stills independently viewed. No action sequence or natural route acceptance.')
]
capture_index = []
for role, run, limit in runs:
    for suffix in ['_receipt.json', '_source_before.json', '_capture.log']:
        copy(BASE / (run + suffix), OUT / 'receipts' / (run + suffix))
    for aspect in ['1280x720', '1600x720']:
        manifest_path = BASE / run / aspect / 'capture_manifest.json'
        m = json.loads(manifest_path.read_text(encoding='utf-8'))
        assert m['source_revision'] == REV and m['errors'] == []
        assert m['normal_save_before'] == m['normal_save_after']
        copy(manifest_path, OUT / 'captures' / role / aspect / 'capture_manifest.json')
        for state in m['states']:
            p = BASE / run / aspect / state['image']['file']
            assert sha(p) == state['image']['sha256']
            target = OUT / 'captures' / role / aspect / p.name
            copy(p, target)
            presentation = state.get('presentation')
            if role == 'guarded_ready':
                assert presentation is not None
                assert all(not value for key, value in presentation.items() if key != 'fade_alpha')
                assert presentation['fade_alpha'] <= 0.02
            capture_index.append({'path': target.relative_to(OUT).as_posix(), 'state_id': state['id'], 'aspect': aspect, 'run_role': role, 'sha256': sha(p), 'source_revision': REV, 'presentation': presentation, 'scope_limit': limit})

harnesses = ['root_capture_picture_context_20261012.gd', 'root_capture_picture_context_fresh_20261012.gd', 'root_capture_picture_context_guarded_20261012.gd']
gates = []
for name in harnesses:
    p = BASE / name
    copy(p, OUT / 'harnesses' / name)
    for command in [
        ['python', '-m', 'gdtoolkit.parser', str(p)],
        ['python', '-B', str(REPO / 'tools/lint_inference.py'), str(p)],
        [ENGINE, '--headless', '--path', str(REPO), '--check-only', '-s', str(p)]
    ]:
        result = subprocess.run(command, cwd=REPO, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=90, creationflags=subprocess.CREATE_NO_WINDOW)
        gates.append({'command': command, 'returncode': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr, 'scope': 'Diagnostic capture harness only; not full game regression or art acceptance.'})
        assert result.returncode == 0, gates[-1]
copy(BASE / 'root_picture_capture_launch.py', OUT / 'harnesses/root_picture_capture_launch.py')
copy(Path(__file__), OUT / 'harnesses' / Path(__file__).name)

reuse = []
for name in ['k_sprout', 'k_flower1', 'flower', 'flower2', 'k_flower2', 'flower3']:
    p = REPO / 'assets/mg' / (name + '.png')
    q = REPO / 'assets/art35/cards/mg' / (name + '_' + name + '.png')
    assert p.read_bytes() == q.read_bytes()
    reuse.append({'role': 'Exact alternate duplicate; no quality improvement', 'runtime': p.relative_to(REPO).as_posix(), 'alternate': q.relative_to(REPO).as_posix(), 'runtime_sha256': sha(p), 'alternate_sha256': sha(q), 'bytes_identical': True, 'authority': 'ASSET_LICENSES.md orthographic Garden render row; existing raster art, not automatically flat-vector debt.'})
for name in ['flower_coral', 'flower_lavender', 'leaf_broad']:
    p = REPO / 'assets/props/story' / (name + '.png')
    from PIL import Image
    im = Image.open(p).convert('RGBA')
    reuse.append({'role': 'Inspected approved painted reuse candidate; Garden fit not accepted', 'source': p.relative_to(REPO).as_posix(), 'sha256': sha(p), 'dimensions': list(im.size), 'alpha_bbox': list(im.getchannel('A').getbbox()), 'authority': 'ASSET_LICENSES.md Batch04 tropical/flower world-card row; original sheets under assets_src/style_review_batch_04/final.', 'fit_limit': 'Flowers expose roots and differ in contour occupancy/flower species from current Garden outcomes. Whole-art reuse with non-destructive crop/matte and correct soil contact needs exact scene review. Detached leaf alone is not a complete sprout; avoid arbitrary plant assembly.'})

reviewed = [
 'captures/action/1280x720/garden_seed_ready.png',
 'captures/action/1280x720/garden_all_sprouts_settled.png',
 'captures/action/1280x720/garden_complete_settled.png',
 'captures/action/1600x720/garden_complete_settled.png',
 'captures/action/1280x720/garden_sprout_00_active.png',
 *['captures/action/1280x720/garden_flower_%02d_active.png' % i for i in range(5)],
 'captures/action/1280x720/trampoline_ready.png',
 'captures/action/1280x720/xmas_ready.png',
 'captures/rejected_fresh/1280x720/snowman_fresh_ready.png',
 'captures/rejected_fresh/1280x720/trampoline_fresh_ready.png',
 'captures/rejected_fresh/1280x720/xmas_fresh_ready.png',
 'captures/rejected_fresh/1600x720/garden_fresh_ready.png',
 *[c['path'] for c in capture_index if c['run_role'] == 'guarded_ready']
]
assert len(reviewed) == len(set(reviewed)) == 24

def obs(identifier, title, piece_ids, classification, weakness, neighbors, proposal, preserve, evidence, limit):
    return {'id': identifier, 'title': title, 'existing_piece_ids': piece_ids, 'classification': classification, 'observed_weakness': weakness, 'same_scene_comparison': neighbors, 'proposed_update': proposal, 'must_preserve': preserve, 'evidence_paths': evidence, 'limits': limit, 'status': 'CONTEXT_REVIEW_OPEN', 'replacement_pixels': 0, 'runtime_integrations': 0, 'accepted_removals': 0}

garden = ['captures/guarded_ready/1280x720/garden_fresh_ready.png', 'captures/guarded_ready/1600x720/garden_fresh_ready.png']
sprout = ['captures/action/1280x720/garden_all_sprouts_settled.png', 'captures/action/1280x720/garden_sprout_00_active.png']
complete = ['captures/action/1280x720/garden_complete_settled.png', 'captures/action/1600x720/garden_complete_settled.png']
observations = [
 obs('ROOTPIC-01','Garden grass mound',[],'Confirmed visible procedural artwork','A broad uniform green mound with hard rim/highlight has little authored material detail.','Painted sun, seed, butterflies and Roshan carry shaped light, material cues and authored contours. Green palette already belongs to the scene.','Inventory existing calm painted grass/ground first. Reuse a cohesive whole ground strip or commission only the missing grassy base, preserving open negative space around five plants.','Five slots and their unobstructed input envelopes; no added distracting props.',garden,'New named-role registry binding required; not yet a new counted unique design.'),
 obs('ROOTPIC-02','Five Garden clay pots',[],'Confirmed visible procedural artwork','Five repeated flat rounded terracotta shapes with a generic white highlight do not clearly describe an open soil-filled pot.','Brown painted seeds have texture and shaded volume. The plants must root at the same soil line as these containers.','Use one authored clay-pot design repeated five times, with a readable shallow opening/soil and restrained contact shadow. Inventory reusable containers before generation.','150x100 visible envelope and slot spacing; soil/contact line at 615; preserve seed < sprout < flower hierarchy.',garden,'Five instances of one family, not five independently generated designs. Recheck all growth states and occlusion.'),
 obs('ROOTPIC-03','Common Garden sprout',['FV-2A7698EB514E'],'Shaded raster style candidate; not automatically vector','Geometric rod stem and simple elliptical leaves have a simpler surface treatment than Roshan and the sun.','All five plants share this sprout and the same brown seed/pot family. Existing painted flower/leaf cards offer more authored contours but are not exact sprout replacements.','Reuse a suitable complete seedling if found; otherwise draw one common sprout matching the scene’s gentle indigo contours, green family and soil entry. Do not randomly rebuild each sprout.','One shared identity, 148x148 art rect, 0.881 stem-bottom mapping, approximately 105px visible height; root at soil.',sprout,'The art35 alternate is byte-identical; a detached broad leaf is not an accepted whole sprout.'),
]
flower_ids = ['FV-0CE81E2C1213','FV-80696B25F705','FV-712A4ED716EA','FV-D3FF54E92E64','FV-0B0A0AE1B9CF']
flower_names = ['k_flower1','flower','flower2','k_flower2','flower3']
for i,(fid,name) in enumerate(zip(flower_ids,flower_names)):
 observations.append(obs('ROOTPIC-%02d'%(4+i),'Garden mature outcome %d (%s)'%(i+1,name),[fid],'Shaded raster style candidate; not automatically vector','Simple shaded petal/leaf forms and rod stems feel less authored than the adjacent painted world cards.','Compare this exact outcome with the common sprout and the other four flowers as a coherent set, and with painted seed/sun/Roshan. Two approved painted flower cards are available but do not cover all five outcome identities.','Audit whole-card reuse for this specific flower first. Where reuse fails, redraw the named outcome with compatible contours, soft painted surfaces and the same distinct blossom structure; review all five together before integration.','Current slot/order, distinct five outcomes, 228x228 art rect, approximately 170px visible height, stable soil entry, 0.12s 1.2 pop then 0.12s settle.', ['captures/action/1280x720/garden_flower_%02d_active.png'%i,*complete], 'No blanket finding that all raster flowers are flat vector; art35 alternate is byte-identical; identity/fit/phone acceptance still open.'))
observations += [
 obs('ROOTPIC-09','Garden watering can',['FV-74CBBFCFD63F'],'Raster finish/contact-fit candidate','The small pink can has a rougher contour/resolution than Roshan and floats nearby as a watching/watering cue.','Existing sun and seed have finer painted shaping. Palette already matches the pink/purple family.','Preserve this can’s identity; check its best source master and non-destructive cleanup before requesting new pixels. Review readable spout orientation and intentional relation to Roshan/flowers.','272x286 transparent raster; runtime 130x137 rect and 0.32 rotation; do not claim or fake a hand-held contact. Protected book art remains untouched.',garden,'Alpha exterior is transparent; no white-background contamination defect was found.'),
 obs('ROOTPIC-10','Picture-game gradient fields',['FV-BBB50149283E'],'Confirmed generated flat field; material/context candidate','Large smooth gradients supply calm negative space but no authored scene material.','Garden uses warm painted props; Snowman needs snow; Trampoline uses Roshan/star; Xmas has a detailed cool tree/ornaments. Each needs its own environmental/paper context.','Inventory calm existing backgrounds per game. Reuse or draw a context-specific painted field with restrained depth, keeping targets clear; do not put a random busy landscape behind every activity.','HUD and all input envelopes; native background coverage/import/overdraw rules; source-specific scene identity.',garden+['captures/guarded_ready/1280x720/snowman_fresh_ready.png','captures/guarded_ready/1280x720/trampoline_fresh_ready.png','captures/guarded_ready/1280x720/xmas_fresh_ready.png'],'Per-game callers require separate resolution; this is not coverage of Slide or every aspect/state.'),
 obs('ROOTPIC-11','Picture growth/win sparkle polygons',['FV-E96CD69662D1'],'Confirmed visible procedural ornament','Growth and win bursts are flat eight-point stars.','Nearby butterflies/sun and the large Trampoline star are authored raster art; a simple painted sparkle may fit without imitating the large objective star.','Inspect reusable painted sparkles and share a small authored family; preserve palette and effect limits. Review the burst at full speed, settles and close/reentry.','Action max three concurrent bursts; win replaces old bursts; 4..18 elements; 0.35..0.9s lifetime; existing one-owner feedback layer.',['captures/action/1280x720/garden_sprout_00_active.png','captures/action/1280x720/garden_complete_payoff.png'],'Stills do not validate complete motion/seams/phone overdraw.'),
 obs('ROOTPIC-12','Snowman snow field',['FV-55B5EF60A12C'],'Confirmed visible procedural artwork','Huge flattened/translucent rounded panels create grey bands and a large white highlight rather than a snowy ground surface.','The smaller rolling ball has the same generic style; future carrot/coal and action need a coherent snow family.','Reuse a quiet painted snow ground if suitable; otherwise supply one snowy base with local snow grain and gentle cool shadows, preserving the rolling workspace.','Rolling gestures, CTA/hint, stacking area and phase behavior.',['captures/guarded_ready/1280x720/snowman_fresh_ready.png','captures/guarded_ready/1600x720/snowman_fresh_ready.png'],'Ready stage only; no face/stack/chase source comparison accepted here.'),
 obs('ROOTPIC-13','Snowball rolling/stacked family',['FV-C99F706798D3'],'Confirmed visible procedural artwork','The ready ball is a generic flat white disc with border/shadow; growth and stacking need one coherent snow material.','Snow field currently shares generic panel treatment. Later face props are separate approved candidates, not substitutes for the child’s rolling action.','Inspect existing complete snowball assets, otherwise draw one reusable snowball family compatible with snowy field; preserve dynamic size and contact.','Start radius26; final radii124/98/72; circles accumulate3/2.5/2 turns; grow/stack/face/chase states and no automatic zero-input win.',['captures/guarded_ready/1280x720/snowman_fresh_ready.png','captures/guarded_ready/1600x720/snowman_fresh_ready.png'],'Growing/stacked family is source-bound only in this slice; full interaction capture remains required.'),
 obs('ROOTPIC-14','Trampoline mat/frame and detached highlight',['FV-C6F64FAA2F32'],'Confirmed visible procedural artwork/contact defect','Flat blue capsule lacks readable mat/frame material. Its large white child highlight hangs below the pad after the parent height is reduced to56.','Roshan and the objective star already have authored contours/lighting. Their palette can guide the mat without redrawing them.','Inventory complete trampoline art; replace the capsule/highlight with one context-matched painted mat/frame with readable spring surface/support. Align Roshan’s intended rest/landing relationship and review each bounce.','400x140 touch target at440,430; visible mat envelope440,492/400x56; current bounce input/rhythm, Roshan identity and large star objective.',['captures/guarded_ready/1280x720/trampoline_fresh_ready.png','captures/guarded_ready/1600x720/trampoline_fresh_ready.png'],'Rest/ready observations only. Star overlaps instruction panel in both aspects; solve spacing within existing objective behavior, not by deleting the target.'),
 obs('ROOTPIC-15','Xmas ornament card material',['FV-E1D26D3057A3'],'Confirmed visible flat frame; whole caller remains open','Uniform white rounded cards and dark rims are materially plainer than the detailed tree and ornaments.','Five ornaments share polished jewel/shell forms; the sixth flower is protected source artwork and disabled initially.','Reuse one compatible painted card material across the five active ornaments and locked flower state while preserving distinct feedback states. Retain the existing undecorated tree and detachable components.','110x110 ornament cards, protected friendship flower, disabled/enabled distinction, precise placement/one-finger input.',['captures/guarded_ready/1280x720/xmas_fresh_ready.png','captures/guarded_ready/1600x720/xmas_fresh_ready.png'],'No predecorated replacement tree; ready stills do not close placement/topper/payoff states.'),
 obs('ROOTPIC-16','Picture header and shell crest',['FV-E9E82E0C6703','FV-AB474EF3699E'],'Visible flat UI ornament/material; caller classification open','Pale rounded panel and line-only fan crest are plainer than the authored picture props. At1280 the fixed Back disc covers the crest; expanded width separates them.','All four picture games share the same header language and approved indigo palette.','Audit a reusable painted paper/shell-header family and distinct Back presentation; test safe-area spacing at both aspects with exact actionable content and voice cues.','Readable touch/navigation semantics, accessible contrast, current text/voice goals and non-overlapping input.',['captures/guarded_ready/1280x720/garden_fresh_ready.png','captures/guarded_ready/1600x720/garden_fresh_ready.png'],'Do not exempt all StyleBoxFlat callers as functional or redesign lesson content.'),
 obs('ROOTPIC-17','Garden medal card and starburst',[],'Confirmed visible procedural/glyph reward art','The cream tier card, bronze medal glyph, star row and radial flat stars use a different material treatment from nearby painted flowers.','Reward hierarchy should remain clearly distinguishable from plant-growth feedback and the large Trampoline objective star.','Inventory existing painted medal/sparkle assets; preserve tier distinctions, a single bounded celebration owner and reward timing. Review the exact0..2.2s lifecycle and reentry.','CELEBRATION_SECONDS=2.2; one Canvas celebration; bronze/silver/gold/perfect states and safe input.',['captures/action/1280x720/garden_complete_settled.png','captures/action/1600x720/garden_complete_settled.png'],'Immediate reentry after0.7s can legitimately show this still-live medal. No stale indefinite-overlay defect asserted. Bind medal source roles before adding new unique-design counts.')
]

sources = []
for path in ['scripts/games/picture_games.gd','scripts/medal_system.gd','scripts/storybook_ui.gd','ASSET_LICENSES.md']:
    p = REPO / path
    if p.exists():
        sources.append({'path': path, 'raw_sha256': sha(p), 'lf_text_sha256': hashlib.sha256(p.read_text(encoding='utf-8').encode('utf-8')).hexdigest()})

review = {
 'schema': 'reef.root_picture_context_review/1', 'recorded_at_utc': datetime.now(timezone.utc).isoformat(),
 'reviewer': 'Root Codex independent visual inspection; not owner/child/device acceptance', 'source_revision': REV,
 'runtime_baseline_revision': '92c9fe70319ef46bfaa8f61348a6f51512141ec3',
 'task_scope': 'Oct12 point-by-point same-scene art congruency review; Garden raw-pointer growth and four fresh picture ready states. No replacement pixels or production changes.',
 'rules': ['DL-AUTH-05','DL-AUTH-06','DL-AUTH-07','DL-VIS-01','DL-VIS-02','DL-VIS-03','DL-VIS-04','DL-VIS-05','DL-VIS-06','DL-VIS-07','DL-VIS-08','DL-READ-01','DL-READ-02','DL-READ-03','DL-READ-04','DL-READ-05','DL-READ-06','DL-ASSET-01','DL-ASSET-02','DL-ASSET-03','DL-ASSET-04','DL-ASSET-05','DL-ASSET-06'],
 'related_findings': ['MA-VIS-006','MA-VIS-007','MA-VIS-008','MA-DOC-008'],
 'capture_counts': {'retained_native':52,'initial_action_native':36,'rejected_fresh_native':8,'guarded_ready_native':8,'actually_independently_viewed_unique':24},
 'reviewed_capture_paths': reviewed, 'captures': capture_index, 'source_files': sources, 'reuse_inventory': reuse,
 'observations': observations, 'observation_count':len(observations),
 'piece_ids_bound': sorted({i for o in observations for i in o['existing_piece_ids']}),
 'evidence_lanes': {'implementation':'UNCHANGED','machine':'Three harnesses parser/inference/engine checks pass; three execution receipts zero exit and6452 runtime sources unchanged; ordinary saves unchanged.', 'visual':'Bounded root inspection only;17 observations and24 unique viewed native captures.', 'device':'PENDING','child':'PENDING','owner':'PENDING','full_game_inventory':'PENDING','accepted_removals':0},
 'scope_limits': ['Synthetic direct API routes with fresh isolated profiles, not natural child play.', 'The first action run lacks explicit presentation guards; clean cross-game ready contexts use guarded run.', 'No complete motion, save/resume, fallback, all phase, phone performance or zero-art closure claim.', 'Images retain exact captured bytes; no creative image edits or generated replacements.', 'This directory is local staging only; publishing and exact anonymous GitHub verification are required before a delivered handoff claim.']
}
write(OUT/'review.json',review)
write(OUT/'harness_validation.json',{'schema':1,'gates':gates,'all_pass':all(g['returncode']==0 for g in gates)})
files = []
for p in sorted(OUT.rglob('*')):
    if p.is_file() and p.name != 'manifest.json':
        files.append({'path':p.relative_to(OUT).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size,'role':'review native capture' if p.suffix=='.png' else 'diagnostic source/evidence'})
payload = ''.join(f"{x['path']}\t{x['sha256']}\t{x['bytes']}\n" for x in files).encode('utf-8')
write(OUT/'manifest.json',{'schema':'reef.root_picture_review_packet/1','source_revision':REV,'files':files,'payload_hash_definition':'UTF-8 sorted path TAB SHA256 TAB bytes LF, excluding manifest','packet_payload_sha256':hashlib.sha256(payload).hexdigest(),'delivery':'LOCAL_STAGING_NOT_DELIVERED','acceptance':'NO_REPLACEMENT_ACCEPTANCE'})
print(json.dumps({'out':str(OUT),'files':len(files),'native':52,'viewed':24,'observations':len(observations),'piece_ids':len(review['piece_ids_bound']),'review_sha256':sha(OUT/'review.json'),'manifest_sha256':sha(OUT/'manifest.json'),'payload_sha256':hashlib.sha256(payload).hexdigest(),'maximum_file_bytes':max(x['bytes'] for x in files)}))
