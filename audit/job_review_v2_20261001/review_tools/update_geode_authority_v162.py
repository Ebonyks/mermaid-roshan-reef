from pathlib import Path
import hashlib, json, shutil

b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
ip=b/'design/audit_impacts/job-geode-painted-runtime-20261001.json'
ledger=b/'design/05_DOC_LEDGER.md'
s=ledger.read_text(encoding='utf-8')
lines=s.splitlines()
lines=[('| `assets_src/imagegen/geologist_painted_rebuild_v1_20261001/index.html` | 🟣 | `CANDIDATE`;18 native ImageGen originals/34 neutral fields/13 whole-canvas derivatives individually inspected. REVIEW_V7 retains source opinions and binds four selected geode derivatives in the topic runtime candidate. All36 current ordinary four-phase viewport-input native views at1280/1600 directly reviewed: rooted interior4.6/sampled opening4.5 provisional/current visible clapping4.6. Actual room2.8/contact2.7 and flat fossil/pan/invitations remain priorities. Earlier source/302-view evidence is preserved as history, not current runtime acceptance; other painted drafts remain unbound. Castle/story entry, full timed action/device/child/owner/final all-job report remain open. |' if '`assets_src/imagegen/geologist_painted_rebuild_v1_20261001/index.html`' in x else x) for x in lines]
ledger.write_text('\n'.join(lines)+'\n',encoding='utf-8',newline='\n')
finding=b/'audit/findings/ACTIVE_FINDINGS_2026-08-13.md'
s=finding.read_text(encoding='utf-8')
old='[New source-bound ordinary-route/full-suite evidence](../job_geode_runtime_v1_20261001/index.html) pending. Remote actor and other geology surfaces remain priorities; no lifecycle closure/integration/owner approval.'
new='[All36 current source-bound native views](../job_geode_runtime_v1_20261001/index.html) directly inspected across ordinary four-phase viewport-input career progression at1280/1600. Rooted interior4.6/sampled opening4.5 provisional; actual first-run celebration actor disappearance preserved and task-rest position repaired. Current visible clapping4.6 keeps the crystals inside their cavities. Every90 native archive exposed honestly:36 current and7 earlier directly reviewed,43 total; other47 older views unscored. Actual room2.8/contact2.7 and flat fossil/pan/invitations remain priorities. Fresh334-source full suite pending; prior325-source suite cannot validate changed runtime. Castle/story entry, full timed action/device/child/owner/final all-job report open; no lifecycle closure/integration/owner approval.'
assert old in s
finding.write_text(s.replace(old,new,1),encoding='utf-8',newline='\n')
target=b/'audit/job_review_v2_20261001/review_tools/update_geode_authority_v162.py'
shutil.copyfile(__file__,target)
d=json.loads(ip.read_text())
d['files']=sorted(set(d['files'])|{target.relative_to(b).as_posix()})
d['acceptance_gaps']='Bound geode source/rooted reveal4.6 and sampled opening4.5 provisional; current clapping4.6. Actual room2.8, contact2.7, invitations2.9–3.4, flat fossil/pan and full timed actions remain priorities. Current ordinary four-phase input capture uses a direct career-entry fixture with main HUD hidden, so complete castle/story entry, device, child, owner and final comprehensive all-job acceptance remain open. No integration/release or finding closure.'
ip.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
# Existing service reloads this exact allowlist for each request. Add only the
# explicit new review payload and four runtime-source images, never directories.
allow=b/'tmp/v2_preview_allowed.json'
paths=set(json.loads(allow.read_text(encoding='utf-8')))
for prefix in ['audit/job_geode_runtime_v1_20261001','audit/job_review_v2_20261001/opening_motion_remote_verified_v5','assets/opera/worlds/geology/painted_geode_v1_20261001']:
 paths.update(p.relative_to(b).as_posix() for p in (b/prefix).rglob('*') if p.is_file())
paths.update(['assets_src/imagegen/geologist_painted_rebuild_v1_20261001/REVIEW_V7.json'])
allow.write_text(json.dumps(sorted(paths),indent=2)+'\n',encoding='utf-8',newline='\n')
print('Current source/actual-native authority and finding history updated; explicit preview allowlist refreshed.')
