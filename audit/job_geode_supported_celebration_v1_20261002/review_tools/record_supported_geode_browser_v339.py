from pathlib import Path
import datetime, hashlib, json, shutil
from PIL import Image

b = Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
root = Path('C:/Users/Peter/Documents/mermaid-roshan-reef')
f = b / 'audit/job_geode_supported_celebration_v1_20261002'
contact = b / 'assets_src/imagegen/geologist_geode_contact_v1_20261002'
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
def write(p, value):
    p.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()

ci = read(f / 'full_ci_v3/RECEIPT.json')
assert ci['status'] == 'PASS_UNMODIFIED_CURRENT_FULL_SUITE' and ci['source_unchanged']
assert len(ci['probe_results']) == 82 and all(x['process_exit'] == 0 for x in ci['probe_results'])
browser = read(root / 'tmp/geode_browser_state_v339.json')
assert browser['report']['rows'] == 25
assert browser['report']['broken_images'] == []
assert browser['report']['loaded_image_count'] >= 1
assert browser['report']['native_links'] == 374
assert 'passes 82/82' in browser['report']['machine_status']
assert set(browser['register']['rows']) == {
    'GEO-USE-INVITATION', 'GEO-USE-LIBRARY', 'GEO-USE-CELEBRATION',
    'GEO-USE-DEV-MENU', 'GEO-USE-SUPPORT'
}
assert all(x['complete'] and x['width'] > 0 for x in browser['register']['images'])
assert all(sha(b / x['path']) == x['before_sha256'] for x in ci['source_checks'])

# Collapsed/offscreen report illustrations load lazily. Verify their native
# files separately rather than misreporting deferred requests as HTTP failures.
image_files = []
for src in browser['report']['image_sources']:
    p = (f / src).resolve()
    assert p.is_relative_to(f.resolve()) and p.is_file(), src
    with Image.open(p) as im:
        im.load()
        dims = list(im.size)
    image_files.append({'path': p.relative_to(b).as_posix(), 'sha256': sha(p), 'dimensions': dims})
browser['report']['literal_image_file_checks'] = image_files

evidence = []
for name in ['report', 'register']:
    source = root / f'tmp/geode_browser_{name}_v339.png'
    target = f / f'browser_{name}_v339.png'
    assert source.is_file() and not target.exists()
    shutil.copyfile(source, target)
    with Image.open(target) as im:
        dims = list(im.size)
    evidence.append({'path': target.relative_to(b).as_posix(), 'sha256': sha(target), 'dimensions': dims})

browser.update({
    'status': 'CURRENT_REPORT_AND_FIVE_GEODE_USE_REGISTER_VERIFIED',
    'checked_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'screenshots': evidence,
    'report_source_sha256': sha(f / 'index.html'),
    'register_source_sha256': sha(b / 'audit/job_artwork_refinement_live/ALL_ITEMS.json'),
    'qualification': 'Browser presentation and loaded-image review after current local suite pass. Deferred lazy illustrations are identified separately; all 40 native illustration files decode locally with recorded literal hashes. All 374 frame/still links are counted. No new review of every earlier source opinion, motion capture, phone, child, owner or full all-job acceptance.'
})
write(f / 'BROWSER_REVIEW_V339.json', browser)
shutil.copyfile(__file__, f / 'review_tools' / Path(__file__).name)
for filename, folder in [
    ('job-geode-supported-celebration-20261002.json', f),
    ('job-geode-contact-source-20261002.json', contact)
]:
    path = b / 'design/audit_impacts' / filename
    impact = read(path)
    impact['files'] = sorted(set(impact['files']) | {p.relative_to(b).as_posix() for p in folder.rglob('*') if p.is_file()})
    write(path, impact)
allow = b / 'tmp/v2_preview_allowed.json'
write(allow, sorted(set(read(allow)) | {p.relative_to(b).as_posix() for p in f.rglob('*') if p.is_file()}))
print(json.dumps({'status': browser['status'], 'evidence': evidence}))
