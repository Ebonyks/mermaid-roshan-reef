from pathlib import Path
import datetime,hashlib,json,subprocess
from PIL import Image
B=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');R=Path('C:/Users/Peter/Documents/mermaid-roshan-reef/tmp');P=B/'audit/job_final_action_consistency_v1_20261003';IP=B/'design/audit_impacts/job-final-action-consistency-20261003.json'
sha=lambda data:hashlib.sha256(data).hexdigest()
obs=json.loads((R/'SHARED_LIBRARY_OBSERVATION_V687.json').read_text());assert not obs['overflow'] and obs['openHistoricalSections']==0 and 'V55: 2,160' in obs['register'] and 'Runtime rollout and acceptance remain pending' in obs['ownerDirection']
dst=P/'SHARED_FORMAT_LIBRARY_V686.jpg';bad=P/'SHARED_FORMAT_LIBRARY_V686.png';raw=(R/'SHARED_FORMAT_LIBRARY_V686.png').read_bytes();assert not dst.exists()
if bad.exists():
 assert bad.resolve().parent==P.resolve() and dst.resolve().parent==P.resolve() and bad.read_bytes()==raw
 oldname=bad.relative_to(B).as_posix()
 assert subprocess.run(['git','cat-file','-e','HEAD:'+oldname],cwd=B,capture_output=True).returncode!=0
 bad.rename(dst)
 subprocess.run(['git','reset','--',oldname],cwd=B,capture_output=True,check=True)
else:dst.write_bytes(raw)
with Image.open(dst) as im:dimensions=list(im.size);assert im.format=='JPEG'
observation=P/'SHARED_LIBRARY_OBSERVATION_V687.json';assert not observation.exists();observation.write_bytes((R/observation.name).read_bytes())
proof=P/'BROWSER_LIBRARY_VERIFY.json';proof.write_text(json.dumps(dict(status='EXISTING_CURRENT_LIBRARY_NOTICE_DIRECTLY_VERIFIED_NEW_REPORT_PREVIEW_PENDING',checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),page='http://127.0.0.1:8880/audit/job_artwork_refinement_live/index.html?revision=owner-format-v1',screenshot=dict(path=dst.relative_to(B).as_posix(),sha256=sha(dst.read_bytes()),dimensions=dimensions),observation=dict(path=observation.relative_to(B).as_posix(),sha256=sha(observation.read_bytes())),new_report_browser_review='PENDING_EXPLICIT_PREVIEW_PERMISSION',scores_changed=False,runtime_changed=False,qualification='Actual current-library browser pixels and DOM. This does not verify the new report page, native background resolution, action or game/owner acceptance.'),indent=2)+'\n',encoding='utf-8',newline='\n')
licenses=B/'ASSET_LICENSES.md';raw=licenses.read_bytes();name=dst.relative_to(B).as_posix();assert name.encode() not in raw
row='\n| `'+name+'` | Actual local-browser screenshot of current artwork library | Original project QA layout; displayed artwork retains inherited attribution | `'+proof.relative_to(B).as_posix()+'` binds exact observed pixels | Review proof only; no game, action, device, child or owner acceptance. |\n'
licenses.write_bytes(raw+row.encode())
helper=P/'review_tools'/Path(__file__).name;helper.write_bytes(Path(__file__).read_bytes())
impact=json.loads(IP.read_text());impact['files']=sorted((set(impact['files'])-{bad.relative_to(B).as_posix()})|{p.relative_to(B).as_posix() for p in [dst,observation,proof,helper,licenses]});impact['validation'].append(dict(command='Actual existing current-library banner and register browser review',result='PASS',evidence=proof.relative_to(B).as_posix()));IP.write_text(json.dumps(impact,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
print('Actual library proof sealed; new report preview remains pending. No opinion or runtime change.')
