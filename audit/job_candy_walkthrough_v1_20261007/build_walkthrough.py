"""Build an owner walkthrough from preserved bytes. No engine or generation.
Run: python -B build_walkthrough.py --source-root PATH
"""
from pathlib import Path
from html import escape
import argparse, base64, hashlib, json
from PIL import Image

PKG = Path(__file__).resolve().parent
REPO = PKG.parents[1]
BASE = '6238934447cf28834874396dfbaff65effafda46'
OLD = '480d83ab0b79bed7679bea17838e8b915f4189f9992741e7580d061894980446'
NEW = 'a319c9155529e8dbc1355dd79c1e8e169917fb6703137e53a103dd7a113c3ab6'
REL = PKG.relative_to(REPO).as_posix()
parser = argparse.ArgumentParser()
parser.add_argument('--source-root', required=True)
SRC = Path(parser.parse_args().source_root).resolve()
E = SRC / 'audit/candymaker_clearance_20261006'
CAP = json.loads((E/'candidate_a5ad_1280/CAPTURE_candidate_a5ad_1280.json').read_text(encoding='utf-8'))
H = lambda b: hashlib.sha256(b).hexdigest()
def save_json(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
for name in ['native', 'annotations', 'references', 'evidence', 'sources', 'gates']:
    (PKG/name).mkdir(exist_ok=True)
(PKG/'.gdignore').write_text('', encoding='utf-8')
(PKG/'.gitignore').write_text('__pycache__/\npreview-*.png\nlocal-server.log\n', encoding='utf-8')
(PKG/'.gitattributes').write_text('* -text\n', encoding='utf-8')
assets, bindings = [], []
def copy_image(src, dst, role, source):
    raw = src.read_bytes()
    dst.write_bytes(raw)
    with Image.open(dst) as im:
        im.verify()
    with Image.open(dst) as im:
        size = list(im.size)
    assets.append(dict(path=dst.relative_to(PKG).as_posix(), source_path=source,
        source_sha256=H(raw), sha256=H(raw), dimensions=size, role=role,
        modifications='Byte-identical copy; no pixel edits',
        license='Project-owned original/derivative; inherits exact source ASSET_LICENSES.md scope; review only', url='none; repository source'))
for i, v in enumerate(CAP['views']):
    src = SRC/v['path']
    assert H(src.read_bytes()) == v['sha256']
    dst = PKG/'native'/f'view-{i:02d}.png'
    copy_image(src, dst, 'original_native_checkpoint', v['path'])
    bindings.append(dict(local=dst.relative_to(PKG).as_posix(), capture_kind='view', capture_index=i, capture_record=v))
for i in [25, 33, 41, 49, 57, 72, 87, 88]:
    v = CAP['motion_frames'][i]
    src = SRC/v['path']
    assert H(src.read_bytes()) == v['sha256']
    dst = PKG/'native'/f'frame-{i:04d}.png'
    copy_image(src, dst, 'original_sparse_native_frame', v['path'])
    bindings.append(dict(local=dst.relative_to(PKG).as_posix(), capture_kind='motion_frame', capture_index=i, capture_record=v))
refs = {
    'ladle':'assets/opera/worlds/widgets/widget_pour_candymaker_mover.png',
    'candy':'assets/opera/worlds/widgets/widget_target_candymaker_piece_0.png',
    'goal':'assets/opera/worlds/props/goal_candymaker.png',
    'share':'assets/opera/worlds/widgets/widget_target_candymaker_mover.png',
    'frosted':'assets/chapter2/birthday/chapter2_chef_frosted_rainbow_cake.png',
    'final-cake':'assets/chapter2/birthday/chapter2_grand_five_strawberry_cake.png',
    'berry':'assets/chapter2/birthday/sky_lagoon_strawberry_single.png',
}
for name, path in refs.items():
    copy_image(SRC/path, PKG/'references'/f'{name}.png', 'approved_source_reference_only', path)
receipt_paths = [
    'candidate_a5ad_1280/CAPTURE_candidate_a5ad_1280.json',
    'NATIVE_TERMINAL_A5AH.json', 'NATIVE_ARTIFACT_VERIFICATION_A5AI.json',
    'NATIVE_PNG_INDEX_A5AI.json', 'CURRENT_VARIANT_ROUTE_INVENTORY_A5AF.json',
    'CURRENT_MACHINE_VARIANTS_A5AA.json', 'restart_a5z_birthday.json',
    'restart_a5z_ordinary.json', 'partial_a5ab_birthday_1280/PARTIAL_COAT_BACK_RESUME.json',
    'CURRENT_ENDPOINT_REPAIR_CHECKPOINT_A5AS.json', 'PLACE_ENDPOINT_CAP_OVERRUN_A5AT.json',
    'PLACE_ENDPOINT_PATCH_A5AO.json', 'PLACE_GEOMETRY_CPU_A5AP.json',
    'INDEPENDENT_SEQUENCE_INTAKE_A5AU.json', 'gates/candidate_a5ad_1280.receipt.json',
]
receipt_bindings = []
for path in receipt_paths:
    src = E/path
    dst = PKG/'evidence'/src.name
    dst.write_bytes(src.read_bytes())
    receipt_bindings.append(dict(path=dst.relative_to(PKG).as_posix(),
        original_path='audit/candymaker_clearance_20261006/'+path, sha256=H(dst.read_bytes())))
world = (SRC/'scripts/opera_career_world_2d.gd').read_bytes()
assert H(world) == NEW
start = world.index(b'func _draw_chapter2_candy_place(')
end = world.index(b'func ', start+5)
oldbody = (E/'draw_chapter2_candy_place_before_a5ao.gd.txt').read_bytes()
frozen = world[:start]+oldbody+world[end:]
assert H(frozen) == OLD, ('reconstruction hash mismatch', H(frozen))
(PKG/'sources/world-captured-480.gd.txt').write_bytes(frozen)
(PKG/'sources/world-current-a319.gd.txt').write_bytes(world)
for path in ['scripts/opera_candy_story_surface.gd', 'scripts/chapter_two_career_scene_adapter.gd',
             'scripts/chapter_two_voice_catalog.gd', 'scripts/opera_hotspot_catalog.gd',
             'scripts/opera_performance_plan.gd', 'scripts/chapter_two_director.gd', 'scripts/castle_career_routes.gd']:
    (PKG/'sources'/(Path(path).name+'.txt')).write_bytes((SRC/path).read_bytes())
(PKG/'sources/capture_birthday.gd.txt').write_bytes((E/'capture_birthday.gd').read_bytes())
save_json(PKG/'SOURCE_BINDING.json', dict(
    documentation_baseline=BASE, captured_preview_baseline='96274aab9cebd563b10846a4a48de5d017588563',
    captured_branch='codex/candymaker-46-20261006', captured_world_raw_sha256=OLD,
    current_uncommitted_world_raw_sha256=NEW, current_world_native_evidence='NONE; prior native frames do not validate changed endpoints',
    reconstruction='Replace only current PLACE function with preserved pre-A5AO bytes; exact frozen480 SHA verified',
    capture_manifest_original_sha256=H((E/receipt_paths[0]).read_bytes()), capture_profile=CAP['events'][0],
    fixture='Valid prior DayOne/Farmer/Chef isolated save loaded before Main READY; actual Kitchen explicitly mounted. No fresh-save preceding-story or foyer travel proof. Candy starts at zero and earns all four phases via173 real touch/drag events.',
    selected_original_count=len(bindings), original_capture_total_count=130,
    published_subset_limit='Only listed25 selected originals are shipped. Historical receipts describe original owning-checkout paths, not extra required packet files. Every displayed image dependency is included.',
    image_bindings=bindings, receipt_bindings=receipt_bindings,
    no_new_engine_runs=True, no_new_generation=True, no_saved_userdata_mutation=True))

steps = json.loads((PKG/'STEP_TEXT.json').read_text(encoding='utf-8'))['steps']
def uri(path):
    return 'data:image/png;base64,'+base64.b64encode(path.read_bytes()).decode()
def mark(o):
    x, y = o['x'], o['y']
    if o['type'] == 'drag':
        d = f'M{x},{y} L{o["x2"]},{o["y2"]}'
    elif o['type'] == 'circle':
        d = f'M{x+40},{y} A40,40 0 1,1 {x},{y-40}'
    else:
        return f'<circle cx="{x}" cy="{y}" r="29" fill="none" stroke="#17294d" stroke-width="10"/><circle cx="{x}" cy="{y}" r="29" fill="none" stroke="#fff479" stroke-width="4"/>'
    return f'<path d="{d}" fill="none" stroke="#17294d" stroke-width="9"/><path d="{d}" fill="none" stroke="#fff479" stroke-width="4" marker-end="url(#arrow)"/>'
svghead = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 800"><defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6" fill="#fff479"/></marker></defs>'
for s in steps:
    if s['image']:
        src = PKG/s['image']
        extra = ''.join(mark(o) for o in s['overlay'])
        legend = ' · '.join(o['label'] for o in s['overlay']) or 'Observe the actual earned result'
        text = svghead+f'<image width="1280" height="720" href="{uri(src)}"/>'+extra+f'<rect y="720" width="1280" height="80" fill="#17294d"/><text x="24" y="750" fill="#fff479" font-family="sans-serif" font-size="22">{s["id"]} · REVIEW ANNOTATION · CAPTURED PREVIEW480</text><text x="24" y="782" fill="white" font-family="sans-serif" font-size="21">{escape(legend)}</text></svg>'
    else:
        src = PKG/'references'/f'{s["reference"]}.png'
        text = svghead+f'<rect width="1280" height="800" fill="#edf0f8"/><rect x="28" y="28" width="1224" height="92" rx="20" fill="#17294d"/><text x="56" y="86" font-family="sans-serif" font-size="34" fill="#fff479">{s["id"]} · SOURCE ONLY · NO NATIVE SCREENSHOT</text><image x="420" y="140" width="440" height="440" href="{uri(src)}"/><text x="640" y="625" text-anchor="middle" font-family="sans-serif" font-size="32" fill="#17294d">{escape(s["title"])}</text><text x="640" y="681" text-anchor="middle" font-family="sans-serif" font-size="23" fill="#435471">Approved source reference; room, motion and contact are not shown.</text><text x="640" y="757" text-anchor="middle" font-family="sans-serif" font-size="22" fill="#435471">Read the separate gesture / result / next-step caption.</text></svg>'
    f = PKG/'annotations'/f'{s["id"]}.svg'
    f.write_text(text, encoding='utf-8')
    s['annotation'] = 'annotations/'+f.name
    s['status'] = 'FROZEN_480_NATIVE_PREVIEW' if s['image'] else 'SOURCE_ONLY_GAP'
    assets.append(dict(path=s['annotation'], source_path=s['image'] or 'references/'+s['reference']+'.png',
        source_sha256=H(src.read_bytes()), sha256=H(f.read_bytes()), dimensions=[1280,800],
        role='native_vector_review_annotation' if s['image'] else 'source_only_coverage_gap_illustration',
        modifications='Original PNG embedded byte-identically with separate vector marks and an outside-canvas ribbon' if s['image'] else 'Unchanged approved reference on a neutral NO NATIVE SCREENSHOT card; no invented scene/runtime pixels',
        license='Project-original review annotation; underlying art retains source license/provenance', url='none; repository source'))
save_json(PKG/'STEPS.json', dict(steps=steps, annotation_coordinate_space='Observed1280x720 input trace anchors; diagram overlays are review instructions only', native_selected_count=len(bindings), unscored=True))
save_json(PKG/'ASSET_PROVENANCE.json', dict(assets=assets, protected_originals_modified=False, new_generation_calls=0, no_character_or_scene_redraw=True))

intro = 'This walkthrough shows Candy Maker’s recorded birthday preview, plus ordinary play and save/resume steps. Native images are preserved; source-only panels identify missing screenshots. The unpublished recorded preview predates a held placement drawing change. This packet documents preview behavior; it does not certify the shipping build or establish 4.6/5 clearance.'
limits = 'Godot 4.7.2-stable · Mobile renderer · Speedy · Desktop 1280×720. Prior story used an isolated prerequisite fixture; Candy itself was earned with 173 real touch/drag events. Ordinary and reload results have headless evidence only. Sparse PLACE/reward frames are not full-speed or 30 fps coverage. Action audio is scripted, not recorded.'
status = 'Machine logic and capture checks are separate from visual/contact, device, child and owner acceptance. No scores or findings change. Cake support and tool choice remain pending. The original native-supervisor filename failure and the later 600 s preparation-cap failure are preserved.'
sections = {
    'birthday':('Birthday: five strawberries for one persistent cake','Entry, station invitations, earned activity checkpoints, placement intermediates, result, reward and return.'),
    'lifecycle':('Leave, save and resume','What the machine tests established, with explicit native-image gaps.'),
    'current':('Held current source: uncaptured placement repair','The newer drawing change. No repaired screenshot, new staging, animation or acceptance is claimed.'),
    'ordinary':('Ordinary play: syrup, sort, wrap and share','A distinct post-story variant with four generic candy phases. Approved source artwork explains each uncaptured step.'),
}
def card(s):
    orig = f'<a href="{s["image"]}" target="_blank" rel="noopener">Full-size original PNG</a> · ' if s['image'] else ''
    prompt = ''
    if s['voice']:
        spoken = s.get('spoken', s['voice'])
        caption_kind = 'Voice-catalog caption' if s['group']=='birthday' else 'Scripted voice cue from phase source'
        prompt = f'<div class="voice"><strong>Scripted instruction</strong><p>“{escape(s["voice"])}”</p><small>{caption_kind}: “{escape(spoken)}” · audio unverified</small></div>'
    fields = ''.join(f'<dt>{k}</dt><dd>{escape(s[v])}</dd>' for k,v in [('See','see'),('One-finger action','gesture'),('Roshan / contact','roshan'),('Visible or saved result','result'),('Next','next')])
    gap = f'<p class="gap"><strong>Evidence gap</strong> · {escape(s["gap"])}</p>' if s['gap'] else ''
    raw = f'<img class="original" src="{s["image"]}" alt="Original native frame" loading="lazy" width="1280" height="720"/>' if s['image'] else ''
    kind = 'Source-only gap' if not s['image'] else 'Native preview · World 480d83…'
    return f'<article class="step" id="{s["id"]}"><header><span class="num">{s["id"]}</span><div><span class="type">{kind}</span><h3>{escape(s["title"])}</h3></div></header><div class="cardbody"><figure><img class="annotated" src="{s["annotation"]}" alt="{escape(s["title"])}; {s["status"]}" loading="lazy" width="1280" height="800"/>{raw}<figcaption>{orig}<a href="{s["annotation"]}" target="_blank" rel="noopener">Separate annotation / reference</a></figcaption></figure><div class="caption">{prompt}<dl>{fields}</dl></div></div>{gap}</article>'
body = ''.join(f'<section id="{g}"><div class="sectiontitle"><h2>{title}</h2><p>{desc}</p></div>'+''.join(card(s) for s in steps if s['group']==g)+'</section>' for g,(title,desc) in sections.items())
css = (PKG/'walkthrough.css').read_text(encoding='utf-8')
tail = (PKG/'COVERAGE.html').read_text(encoding='utf-8')
html = '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Candy Maker · Step-by-step walkthrough</title><style>'+css+'</style></head><body><nav aria-label="Walkthrough sections"><strong>Candy Maker</strong><a href="#birthday">Birthday</a><a href="#lifecycle">Save &amp; resume</a><a href="#current">Current change</a><a href="#ordinary">Ordinary play</a><a href="#coverage">Evidence &amp; gaps</a><button type="button" id="toggle" aria-pressed="false">Show original screenshots</button></nav><main><div class="hero"><div class="eyebrow">OWNER REVIEW · 7 OCTOBER2026</div><h1>Candy Maker,<br>one step at a time.</h1><p class="lead">'+escape(intro)+'</p><p class="limits">'+escape(limits)+'</p><p class="status">'+escape(status)+'</p><div class="overview"><span>Coat → Sort → Glaze → Place</span><span>25 preserved native originals</span><span>33 numbered panels</span></div></div>'+body+tail+'</main><script>document.getElementById("toggle").addEventListener("click",function(){var raw=document.body.classList.toggle("raw");this.textContent=raw?"Show gesture annotations":"Show original screenshots";this.setAttribute("aria-pressed",String(raw));});</script></body></html>'
(PKG/'index.html').write_text(html, encoding='utf-8')
md = ['# Candy Maker — step-by-step visual walkthrough','',intro,'',limits,'',status,'','[Browser version](index.html) · [Step manifest](STEPS.json) · [Source binding](SOURCE_BINDING.json) · [Payload hashes](MANIFEST.json)','', 'Native originals below are from the frozen480 preview. Open the separate SVG annotation for gesture marks. Every source-only panel says NO NATIVE SCREENSHOT. The action prompt is scripted; actual audio playback is unverified.','']
for g,(title,desc) in sections.items():
    md += ['## '+title,'',desc,'']
    for s in steps:
        md += ['### '+s['id']+' — '+s['title'],'',f'![{s["status"]}: {s["title"]}]({s["image"] or s["annotation"]})','',f'[Separate annotation / full reference]({s["annotation"]})'+(f' · [Full-size native original]({s["image"]})' if s['image'] else ''),'',f'**See:** {s["see"]}','',f'**Touch:** {s["gesture"]}','']
        if s['voice']:
            caption_kind = 'Voice-catalog caption' if s['group']=='birthday' else 'Scripted voice cue from phase source'
            md += [f'**Scripted instruction:** “{s["voice"]}” {caption_kind}: “{s.get("spoken",s["voice"])}” (audio not recorded).','']
        md += [f'**Roshan / contact:** {s["roshan"]}','',f'**Result:** {s["result"]}','',f'**Next:** {s["next"]}','']
        if s['gap']:
            md += [f'**Evidence gap:** {s["gap"]}','']
md += ['## Coverage and provenance','', 'No Candy-only initial tutorial or two-act practice is naturally enabled. The Chapter2 foyer guides into the same Kitchen rather than supplying a separate Candy game. Legacy six-phase combat is excluded.','', 'Captured: Kitchen → COAT5 → SORT5 → GLAZE2turns → PLACE5 → saved five-fruit cake → stage reward → Kitchen. Ordinary: SYRUP5 → SORT6 → WRAP1.8turns → SHARE6 → ordinary star → return/replay.','', '[Source binding](SOURCE_BINDING.json) · [Asset provenance](ASSET_PROVENANCE.json) · [Local validation](VALIDATION.json) · [Remote verification](REMOTE_VERIFICATION.json). Historical receipts describe130 original images; this review ships only25 selected originals. All displayed image dependencies are included.','', 'The native-supervisor filenameFAIL and later preparation-wall-capFAIL remain preserved under evidence/. Re-verification does not overwrite failures. Machine checks do not establish contact, nativeA319, full-speed motion, device, child, owner or≥4.6 clearance.','', 'Documentation baseline: '+BASE+'. Runtime clearance remains blocked; pending support/tool decisions are unchanged.','']
(PKG/'README.md').write_text('\n'.join(md), encoding='utf-8')
ledger = REPO/'design/05_DOC_LEDGER.md'
txt = ledger.read_text(encoding='utf-8')
row = f'| `{REL}/README.md` | 🟡 | `SOURCE_ONLY_REVIEW` owner-commissioned Candy Maker walkthrough; frozen480 native preview and explicit currentA319/ordinary/lifecycle gaps. Source/input provenance bound in adjacent manifest; no numeric clearance, accepted live-runtime, artistic/device/child/owner authority or finding closure. |'
if row not in txt:
    ledger.write_text(txt.rstrip()+'\n'+row+'\n', encoding='utf-8')
licenses = REPO/'ASSET_LICENSES.md'
txt = licenses.read_text(encoding='utf-8')
heading = '## Candy Maker visual walkthrough2026-10-07'
if heading not in txt:
    entries = ['', heading, '', 'Project-owned diagnostic screenshots and approved references, preserved byte-identically. Separate vector annotations/gap cards are review-only and excluded from runtime imports. Per-file hashes and sources: `'+REL+'/ASSET_PROVENANCE.json`.','']
    for a in assets:
        entries.append('- `'+REL+'/'+a['path']+'` — '+a['license']+'; source: `'+a['source_path']+'`; URL: none (repository source); modifications: '+a['modifications']+'.')
    licenses.write_text(txt.rstrip()+'\n'+'\n'.join(entries)+'\n', encoding='utf-8')
impact = REPO/'design/audit_impacts/candymaker-visual-walkthrough-20261007.json'
d = json.loads(impact.read_text(encoding='utf-8'))
d['files'] = sorted([p.relative_to(REPO).as_posix() for p in PKG.rglob('*') if p.is_file() and not p.name.startswith('preview-')]+['ASSET_LICENSES.md','design/05_DOC_LEDGER.md'])
d['source_binding'] = REL+'/SOURCE_BINDING.json'
d['facts_changed'] = 'Adds one source-only ledger classification and exact license/provenance rows for review copies/annotations. No canonical finding lifecycle or master task route changes.'
save_json(impact, d)
size = sum(p.stat().st_size for p in PKG.rglob('*') if p.is_file())
assert size < 128*1024*1024, ('walkthrough allocation exceeds128MiB',size)
print(json.dumps(dict(steps=len(steps), native_originals=len(bindings), assets=len(assets), package_bytes=size, frozen_source_sha256=H(frozen), runtime_changes=0)))
