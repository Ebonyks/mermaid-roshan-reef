"""Current scope/provenance bookkeeping; never grants owner or device acceptance."""
from pathlib import Path
from datetime import datetime,timezone
import csv,hashlib,json,shutil,subprocess
root=Path(__file__).resolve().parents[3]
src=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def save(path,data):path.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')

p=src/'prompts.json';prompts=json.loads(p.read_text())
for row in prompts:
    name=row['id']
    if name=='chocolate_strawberry':row['disposition']='REJECTED_STYLE_GLOSSY_REALISM'
    elif name=='frosting_segment':row['disposition']='REJECTED_ROLE_GARLAND_NOT_PIPE_RIBBON'
    elif name=='pitcher_empty_retry':row['disposition']='NOT_SELECTED_WRONG_MANUAL_GUIDE_AND_LOWER_REGISTERED_IOU'
    elif name in ['oven_cool','oven_warm','oven_open','oven_cake_raw','oven_cake_risen']:
        row['disposition']='PRESERVED_INTERMEDIATE_APPEARANCE_INPUT_NOT_RUNTIME_PIXELS'
    else:row['disposition']='SELECTED_CANDIDATE_SOURCE_AND_CURRENT_CONTEXT_REVIEW_REQUIRED'
save(p,prompts)

p=src/'oven_state_job.json';d=json.loads(p.read_text())
d['action']='Existing heat/tap mechanic selects three complete oven-with-supported-tin stills: cool/raw, warm/risen, open/risen. The frame-only states and separate raw/risen tin images are retained as bound intermediate inputs.'
d['method']='ImageGen authored physical cake/window/rack occlusion in the complete state; common-bounds uniform normalization and registered Canvas binary selection only. No local floating cake overlay, interpolated door performance, UV warp or new loop.'
d['native_calls']='6oven-state calls across2three-state candidate sets, plus2separately commissioned raw/risen tin source-object calls;8oven-related calls included in the22total Chef source generations. No paid CLI/API calls.'
d['candidate_sets'][1]['calls_actual']=3
d['reviews'].update(static_context='PENDING final source-bound static review; current GUI checks pass',machine='Focused current runtime probes pending latest fresh-home03; complete82separate',motion_human='PENDING; discrete named state swaps declared, no smooth opening performance claimed')
save(p,d)

reuse=[]
for p in sorted((root/'assets/opera/worlds/backdrops/chef_story_clean_v1').glob('*.png')):
    reuse.append({'path':p.relative_to(root).as_posix(),'sha256':sha(p),'modification':'Exact existing bytes reused by ordinary Chef; original Chapter Two consumer retains same source','authority':'assets_src/imagegen/chef_overdraw_v1_20261003/STATIONS_PROVENANCE.json','native_resolution_gap':'Existing1672x941native/padded2048master debt retained explicitly; no resolution satisfaction or new upscale claimed.'})
save(src/'scene_reuse.json',{'records':reuse,'scope':'Reuse existing painted empty stations to remove repeated bowl/whisk/cake ownership; remove only Chef code spotlights and generic progress dots. Sources unchanged.'})

# Adopt the same six count-only report repairs already proven by Garden/Teacher.
# Compare every CSV cell before writing; actual audio/listening facts must match.
origin=Path('C:/Users/Peter/Documents/mermaid-roshan-reef')
ledger=root/'audit/audio_quality_ledger_2026-08-24.csv'
other=origin/ledger.relative_to(root)
if other.is_file() and ledger.read_bytes()!=other.read_bytes():
    with ledger.open(encoding='utf-8-sig',newline='') as f:before=list(csv.DictReader(f))
    with other.open(encoding='utf-8-sig',newline='') as f:after=list(csv.DictReader(f))
    assert len(before)==len(after)==857
    differences=[]
    for a,b in zip(before,after):
        for key in a:
            if a[key]!=b[key]:
                assert key=='runtime_reference_count',(key,a[key],b[key])
                differences.append({'path':a.get('path',a.get('asset_path','')),'column':key,'before':a[key],'after':b[key]})
    assert len(differences)==6,len(differences)
    shutil.copyfile(other,ledger)
    summary=root/'audit/audio_quality_summary_2026-08-24.json'
    shutil.copyfile(origin/summary.relative_to(root),summary)
    save(src/'audio_ledger_reconciliation.json',{'source':'Garden91b3c005/source-bound baseline reproduction; same six filename-reference counts as Teacher e90c0daa','differences':differences,'audio_bytes_measurements_listening_states':'All857unchanged; no audio or family voice edited.'})

p=root/'design/05_DOC_LEDGER.md';text=p.read_text('utf-8')
old='`PROVENANCE_ONLY` / `SUPPORTING_CURRENT` for minigame-sheet derivation and review notes. It grants no 5/5 or runtime acceptance; owner/context/device review remains separate.'
new='`PROVENANCE_ONLY` / `SUPPORTING_CURRENT` for minigame-sheet derivation and review notes, including the2026-10-19 hash-bound painted Chef chocolate-strawberry revision. It grants no5/5 or runtime acceptance; current source/context/device/owner review remains separate.'
assert old in text or new in text
p.write_text(text.replace(old,new),encoding='utf-8')

paragraph='Owner-requested [Chef painted object candidate](../design/audit_impacts/job-art-chef-20261019.json) (2026-10-19) replaces flat acted-on art with22runtimePNG uses from22builtin ImageGen calls plus declared existing painted sources. The available tool does not expose its model revision. Whole oven/tin states, a registered empty-cup cavity, painted batter/piping/thermometer, chocolate strawberry and whole partial-stack keys preserve source identity and gesture/save ownership. Ordinary Chef reuses the existing empty-station kitchen; its native-resolution debt remains explicit. Current configured desktop Mobile/GUI evidence, minimum4.5per applicable object dimension, exact human motion, canonicalQA11, physical-device/child/owner and complete local/remote82gates are separate. The desktop-save capture-launcher incident and preserved files are recorded honestly; no guessed restore is performed. No master finding is closed.'
p=root/'audit/MASTER_AUDIT_2026-08-09.md';text=p.read_text('utf-8')
if 'Chef painted object candidate' not in text:
    text=text.replace('### Development task index',paragraph+'\n\n### Development task index',1)
p.write_text(text,encoding='utf-8')

p=root/'audit/findings/ACTIVE_FINDINGS_2026-08-13.md';text=p.read_text('utf-8')
for finding in ['MA-OPERA-001','MA-VIS-010']:
    start=text.index('## '+finding+'\n');end=text.find('\n## ',start+4)
    if end<0:end=len(text)
    section=text[start:end]
    lines=section.splitlines()
    for i,line in enumerate(lines):
        if line.startswith('| history |') and 'job-art-chef-20261019.json' not in line:
            lines[i]=line[:-1]+' 2026-10-19: scoped Chef painted-object candidate, whole partial-stack keys, original-cup cavity emptying and registered work-object placement are tracked in design/audit_impacts/job-art-chef-20261019.json. Current local object/GUI checks do not close full motion, canonicalQA11, native-background/device/child/owner or game-wide evidence; lifecycle remains CONFIRMED_OPEN. |'
    text=text[:start]+'\n'.join(lines)+ ('\n' if section.endswith('\n') else '')+text[end:]
p.write_text(text,encoding='utf-8')

p=root/'audit/MASTER_AUDIT_CHANGELOG_ROLLBACK_2026-08-10.md';text=p.read_text('utf-8')
if 'Chef painted object candidate (CHG-106)' not in text:
    text+='\n\n## Chef painted object candidate (CHG-106)\n\nBaseline6fb96aeb441952c1053cc5ce18435fc57fc1d1ab. The [impact](../design/audit_impacts/job-art-chef-20261019.json) enumerates every changed file and retained attempt.22runtimePNG uses replace acted-on flat art, preserve original sources and introduce whole source-aligned partial cake states. New rendering helper owns no gameplay/save progress. Existing input verbs/counts, rewards, phase/save keys and the six-round/five-strawberry Chapter Two story remain. FROST/TOP coordinates follow the actual cake; bowl/thermometer/actor placement and Chef-only empty-station backdrop reuse remove duplicate/occluded work objects. The strict deterministic builder now derives the chocolate slot from its hash-bound native; comparator unchanged,11tests and42derivatives pass. Six inherited audio filename-reference counts are reconciled without changing857audio hashes/measurements/listening facts. Failed fixtures/checks, the unsupported capture save-path flag incident and exact preserved-file hashes remain evidence. Complete82local/remote gates and exact visual/motion/device/child/owner acceptance are separately tracked; no master closure. Rollback: manual_reconstruction, restore only scoped code/consumer paths from this baseline while preserving native/rejected artwork, provenance, all save keys, original/protected art and later unrelated work; rerun exact-engine focused/full gates. Never guess a desktop-save restore.\n'
p.write_text(text,encoding='utf-8')

license_path=root/'ASSET_LICENSES.md';text=license_path.read_text('utf-8')
for image in sorted(src.rglob('*.png')):
    name=image.relative_to(root).as_posix()
    if '| `'+name+'` |' not in text:
        text+='\n| `'+name+'` | Chef source/technical review derivative2026-10-19 | Existing source licenses/OpenAI output terms retained | https://openai.com/policies/terms-of-use/ | SHA256 '+sha(image)+'; source roles/prompts/normalization or configured runtime capture retained in same package; no owner/device acceptance. |'
license_path.write_text(text+'\n' if not text.endswith('\n') else text,encoding='utf-8')

p=root/'design/audit_impacts/job-art-chef-20261019.json';d=json.loads(p.read_text())
d['scope']+=' Actual current-scene review also moves the Chapter Two thermometer clear of Roshan, keeps the FROST picture coherent until its earned endpoint, and stages her aside from the cake. Ordinary Chef reuses the existing source-preserved empty-station kitchen (native-resolution debt unchanged), keeps the original empty-hand actor pose and removes Chef-only code spotlights/progress/abstract completion overlays. No game state, verb/count/reward/save schema change. Record the unsupported GUI capture --user-data-dir incident; preserve remaining desktop files, use verified APPDATA isolation and before/after real-save hashes for every later capture; restore only from an established known-good backup. Adopt six count-only inherited audio-report corrections with all857audio source facts unchanged.' if 'unsupported GUI capture --user-data-dir incident' not in d['scope'] else ''
changed=subprocess.run(['git','diff','--name-only'],cwd=root,capture_output=True,text=True,check=True).stdout.splitlines()
extra=[x.relative_to(root).as_posix() for x in src.rglob('*') if x.is_file()]
extra += [x.relative_to(root).as_posix() for x in (root/'assets/opera/worlds/chef_quality_20261019').rglob('*') if x.is_file()]
extra += ['scripts/chef_painted_art.gd']
uid=root/'scripts/chef_painted_art.gd.uid'
if uid.exists():extra.append(uid.relative_to(root).as_posix())
d['files']=sorted(set(d['files']+changed+extra+[p.relative_to(root).as_posix()]))
d['acceptance_gaps']='Implementation/local configured art review in progress; complete82CI, final object scores, exact full-speed human motion/contact, canonicalQA11, physical-device, child, owner and all remaining campaign packages remain separate. Existing native-background coverage debt remains. Desktop save recovery requires known-good pre-capture backup; preserved live files remain untouched, no guessed restoration.'
save(p,d)
print('Chef authority/provenance/license/coverage records refreshed; no visual acceptance inferred')
