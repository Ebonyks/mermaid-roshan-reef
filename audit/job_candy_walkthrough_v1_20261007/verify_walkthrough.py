"""Verify review-package closure and source fidelity; never run the game."""
from pathlib import Path
from html.parser import HTMLParser
import base64, datetime, hashlib, json, re, subprocess, sys
import xml.etree.ElementTree as ET
from PIL import Image

P=Path(__file__).resolve().parent
R=P.parents[1]
REL=P.relative_to(R).as_posix()
BASE='6238934447cf28834874396dfbaff65effafda46'
H=lambda b:hashlib.sha256(b).hexdigest()
def dump(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def runtime_diff():
    changed=subprocess.check_output(['git','diff','--name-only',BASE],cwd=R).decode().splitlines()
    new=subprocess.check_output(['git','ls-files','--others','--exclude-standard'],cwd=R).decode().splitlines()
    all_paths=set(changed+new)
    unexpected=sorted(x for x in all_paths if not x.startswith(REL+'/') and x not in [
        'ASSET_LICENSES.md','design/05_DOC_LEDGER.md','design/audit_impacts/candymaker-visual-walkthrough-20261007.json'])
    assert not unexpected,unexpected
    return sorted(all_paths)

steps=json.loads((P/'STEPS.json').read_text(encoding='utf-8'))['steps']
assets=json.loads((P/'ASSET_PROVENANCE.json').read_text(encoding='utf-8'))['assets']
binding=json.loads((P/'SOURCE_BINDING.json').read_text(encoding='utf-8'))
assert len(steps)==33 and len({s['id'] for s in steps})==33
assert len(binding['image_bindings'])==25
assert H((P/'sources/world-captured-480.gd.txt').read_bytes())==binding['captured_world_raw_sha256']
assert H((P/'sources/world-current-a319.gd.txt').read_bytes())==binding['current_uncommitted_world_raw_sha256']
assert (P/'.gdignore').exists()
licenses=(R/'ASSET_LICENSES.md').read_text(encoding='utf-8')
for a in assets:
    path=P/a['path'];raw=path.read_bytes()
    assert H(raw)==a['sha256'],a['path']
    assert '`'+REL+'/'+a['path']+'`' in licenses,a['path']
    if path.suffix=='.png':
        with Image.open(path) as im:
            assert list(im.size)==a['dimensions'];im.verify()
    else:
        tree=ET.fromstring(raw)
        image=tree.find('{http://www.w3.org/2000/svg}image')
        assert image is not None
        embedded=base64.b64decode(image.attrib['href'].split(',',1)[1])
        assert H(embedded)==a['source_sha256'],a['path']
        assert H((P/a['source_path']).read_bytes())==H(embedded),a['path']
        if not a['role'].startswith('native'):
            assert 'NO NATIVE SCREENSHOT' in raw.decode('utf-8')
for b in binding['image_bindings']:
    assert H((P/b['local']).read_bytes())==b['capture_record']['sha256']
    with Image.open(P/b['local']) as im:assert im.size==(1280,720)
for b in binding['receipt_bindings']:
    assert H((P/b['path']).read_bytes())==b['sha256']
for s in steps:
    assert all(s[x] for x in ['title','gesture','see','roshan','result','next'])
    assert (P/s['annotation']).exists()
    if not s['image']:assert s['gap'] and s['reference']
    else:assert s['status']=='FROZEN_480_NATIVE_PREVIEW'
    if s['voice']:
        source=(P/'sources/chapter_two_career_scene_adapter.gd.txt' if s['group']=='birthday' else P/'sources/world-captured-480.gd.txt').read_text(encoding='utf-8')
        assert s['voice'] in source,s['id']
        if s['group']=='birthday':
            assert s['spoken'] in (P/'sources/chapter_two_voice_catalog.gd.txt').read_text(encoding='utf-8'),s['id']
lookup={s['id']:s for s in steps}
for step,idx,count in [('B16',25,1),('B17',33,2),('B18',41,3),('B19',49,4),('B20',57,5)]:
    b=next(b for b in binding['image_bindings'] if b['capture_kind']=='motion_frame' and b['capture_index']==idx)
    assert b['capture_record']['state']['phase_progress']==count
    assert lookup[step]['image']==b['local']

class Links(HTMLParser):
    def __init__(self):super().__init__();self.links=[];self.ids=[]
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if 'id' in d:self.ids.append(d['id'])
        for x in ['href','src']:
            if x in d:self.links.append(d[x])
page=Links();page.feed((P/'index.html').read_text(encoding='utf-8'))
assert len(page.ids)==len(set(page.ids))
def check_link(url):
    if url.startswith('#'):assert url[1:] in page.ids;return
    if '://' in url or url.startswith('data:'):return
    target=(P/url.split('#')[0]).resolve()
    assert target.is_relative_to(P),url
    assert target.exists(),url
for url in page.links:check_link(url)
for url in re.findall(r'\]\(([^)]+)\)',(P/'README.md').read_text(encoding='utf-8')):check_link(url)
for name in ['NATIVE_TERMINAL_A5AH.json','PLACE_ENDPOINT_CAP_OVERRUN_A5AT.json']:
    original=json.loads((P/'evidence'/name).read_text(encoding='utf-8'))
    assert original['status'].startswith('FAIL'),name
changed_paths=runtime_diff()
assert REL+'/README.md' in changed_paths, 'Review package must be explicitly staged; root audit directory is ignored'
out=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),status='PASS_PACKAGE_SOURCE_IMAGE_LINK_AND_INPUT_CLOSURE',
    steps=33,native_originals=25,asset_provenance_rows=len(assets),native_size=[1280,720],
    exact_original_hashes=True,embedded_original_bytes=True,source_reconstruction=True,
    voices_match_snapshot_source=True,placement_counts_match_capture=True,
    links_resolve=True,original_failures_preserved=True,runtime_diff='NONE',
    runtime_validation='Exact green baseline Probe suite37609978581 with unchanged runtime bytes; no new engine/import/capture run',
    browser_review='Desktop1280x720 hero, sorting arrows, raw-toggle and ordinary source-only card inspected; responsive/physical-device acceptance not claimed',
    visual_acceptance='NOT_ESTABLISHED; no numeric grading or fresh-runtime/device/child/owner acceptance')
if '--verify-only' not in sys.argv:
    dump(P/'VALIDATION.json',out)
print(json.dumps(out))
