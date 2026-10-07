"""Check the review packet without treating synthetic/reference panels as acceptance."""
from pathlib import Path
from hashlib import sha256
from html.parser import HTMLParser
from datetime import datetime, timezone
import json, re, subprocess
from PIL import Image

root = Path(__file__).resolve().parents[4]
out = Path(__file__).resolve().parents[1]
assert (root / 'project.godot').is_file(), root
def digest(p): return sha256(p.read_bytes()).hexdigest()
checks=[]
def passed(label): checks.append({'check':label,'result':'PASS'})
bindings=json.loads((out/'source_bindings.json').read_text(encoding='utf-8'))
for path, row in bindings.items():
    target=out/path
    assert target.is_file(), path
    source=root/row['source_path']
    if source.is_file():
        assert digest(source)==row['source_sha256'], path
        if row['modification'].startswith('Byte-identical'):
            assert target.read_bytes()==source.read_bytes(), path
    elif row['source_path'].startswith('native/'):
        assert digest(out/row['source_path'])==row['source_sha256'], path
    elif row['role']=='NATURAL_INPUT_ENTRY_CAPTURE':
        assert digest(target)==row['source_sha256'], path
    else:
        raise AssertionError('Unbound source '+path)
    if row.get('comparison_source'):
        assert digest(out/row['comparison_source'])==row['comparison_sha256'], path
passed('66 exact source bindings and preserved native copies; annotation sources match')
old=json.loads((out/'evidence/original_capture_manifest.json').read_text())
for cap in old['captures']:
    p=out/'native'/Path(cap['path']).name
    assert digest(p)==cap['sha256']
    assert list(Image.open(p).size)==cap['dimensions']
passed('All ten historical synthetic capture hashes and dimensions match original manifest')

class Links(HTMLParser):
    def __init__(self): super().__init__(); self.links=[]; self.ids=set()
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if 'id' in a: self.ids.add(a['id'])
        for key in ['src','href']:
            if key in a:self.links.append(a[key])
parser=Links(); parser.feed((out/'index.html').read_text(encoding='utf-8'))
for link in parser.links:
    if link.startswith('#'): assert link[1:] in parser.ids, link
    elif link not in ['manifest.json','evidence/verification.json']: assert (out/link).is_file(), link
for link in re.findall(r'\]\(([^)]+)\)',(out/'README.md').read_text(encoding='utf-8')):
    if not link.startswith('https://') and link not in ['manifest.json','evidence/verification.json']:assert (out/link).is_file(),link
passed('All local HTML, full-size image, voice, navigation and Markdown links resolve')
steps=json.loads((out/'steps.json').read_text(encoding='utf-8'))['steps']
assert len(steps)==25 and len({s['id'] for s in steps})==25
assert len([s for s in steps if s['status'].startswith('PROPOSED')])==4
for s in steps:
    for key in ['see','do','action','next','status']: assert s[key],(s['id'],key)
    if s['status'].startswith('ASSET') or s['status'].startswith('PROPOSED'):assert s['gap'],s['id']
    assert Image.open(out/s['annotation']).size==(1280,880)
    for ref in s['source_refs']:assert (root/ref.split(':')[0]).is_file(),ref
passed('21 current process panels / 4 proposed panels, required captions and gap classifications')
observation=json.loads((out/'native/natural_input_observation.json').read_text())
assert observation['renderer']=='mobile'
assert observation['engine']['string']=='4.7.2-stable (official)'
assert len(observation['events'])==1
assert observation['events'][0]['target']=='StartMenuNewGameButton'
script=(out/'evidence/capture_natural.gd').read_text()
for forbidden in ['complete_disguise_phase','_skip_intro','_dismiss_menu','FashionDesigner.equip','chapter2_story_complete =','_pick(','store_string(JSON.stringify(save']:
    assert forbidden not in script,forbidden
passed('Approved engine/renderer and single real UI entry event; no phase setters in bounded harness')
baseline='6238934447cf28834874396dfbaff65effafda46'
changed=subprocess.check_output(['git','diff','--name-only',baseline],cwd=root,text=True).splitlines()
assert all(not p.startswith(('scripts/','scenes/','assets/','tools/')) and p!='project.godot' for p in changed),changed
passed('No runtime, protected-source, scene, save, tool or project configuration change from baseline')
report={'schema':'reef.fashion_walkthrough_check/1','checked_at_utc':datetime.now(timezone.utc).isoformat(),
        'runtime_baseline':baseline,'checks':checks,'agent_visual_inspection':'Asset comparisons, original chooser, party-dress after and bow-stage annotations inspected at full frame. Text-only arrows/banners; no acceptance of art/acting claimed.',
        'natural_input_scope':'Fresh New Game and castle introduction only; all later route, action, completion and reload capture gaps retained.',
        'device_child_owner':'PENDING; none performed','redesign':'PROPOSED / NOT YET PLAYABLE'}
(out/'evidence/verification.json').write_text(json.dumps(report,indent=2)+'\n')
entries=[]
for p in sorted(out.rglob('*')):
    if not p.is_file() or p.name=='manifest.json':continue
    rel=p.relative_to(out).as_posix()
    e={'path':rel,'sha256':digest(p),'bytes':p.stat().st_size}
    if p.suffix=='.png':e['dimensions']=list(Image.open(p).size)
    if rel in bindings:e.update(bindings[rel])
    entries.append(e)
payload=''.join(e['path']+'\t'+e['sha256']+'\n' for e in entries).encode()
manifest={'schema':'reef.fashion_walkthrough_packet/1','runtime_source_commit':baseline,
          'status':'OWNER_REVIEW_WITH_EXPLICIT_COVERAGE_GAPS','packet_scope':'Non-runtime process reference and proposed redesign; no art or game changes',
          'payload_sha256':sha256(payload).hexdigest(),'payload_algorithm':'SHA-256 of UTF-8 sorted relative-path TAB file-SHA256 LF records; manifest excludes itself',
          'native_capture_method':'Ten old synthetic captures, three new natural-input entry-only captures, nine source-asset references; annotated derivatives preserved separately',
          'steps':25,'proposed_steps':4,'files':entries,
          'acceptance_gaps':['Natural wardrobe entry and state transitions','Embodied dressing/garment contact acting','Natural disguise completion/reload','Birthday-to-lawn handoff','Device/child/owner acceptance']}
(out/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
print('FASHION WALKTHROUGH | ALL OK |',len(checks),'checks |',len(entries),'payload files |',manifest['payload_sha256'])
