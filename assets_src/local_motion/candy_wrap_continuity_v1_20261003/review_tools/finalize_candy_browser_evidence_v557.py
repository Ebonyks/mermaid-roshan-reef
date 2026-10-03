from pathlib import Path
import datetime,hashlib,json,shutil
B=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');P=B/'assets_src/local_motion/candy_wrap_continuity_v1_20261003';T=Path('C:/Users/Peter/Documents/mermaid-roshan-reef/tmp');IP=B/'design/audit_impacts/job-candy-local-wrap-continuity-20261003.json'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):
 n=p.with_name(p.name+'.v557_next');n.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8');n.replace(p)
for name in ['BROWSER_A2_REFERENCE_V555.png','BROWSER_SOURCE_GALLERY_V555.png','BROWSER_VERIFY_V555.json']:
 assert not (P/name).exists();shutil.copyfile(T/name,P/name);assert sha(T/name)==sha(P/name)
q=read(P/'BROWSER_VERIFY_V555.json');assert q['native_video_observation']['ended'] and q['sources_loaded']==[627,1254,1254,1254] and q['native_frame_articles']==82 and q['component_rows']==20 and not q['horizontal_overflow']
licenses=(B/'ASSET_LICENSES.md').read_bytes()
for name in ['BROWSER_A2_REFERENCE_V555.png','BROWSER_SOURCE_GALLERY_V555.png']:
 path=(P/name).relative_to(B).as_posix();assert ('| `'+path+'` |').encode() not in licenses;licenses+=('\n| `'+path+'` | Exact cua browser QA screenshot of project review report | Project artwork and generated-source notices retained | Browser verification JSON and report source paths | Review-only UI evidence, unchanged screenshot bytes; no production art or creative acceptance. |\n').encode()
f=B/'ASSET_LICENSES.md';n=f.with_name(f.name+'.v557_next');n.write_bytes(licenses);n.replace(f)
shutil.copyfile(__file__,P/'review_tools'/Path(__file__).name)
ip=read(IP);ip['files']=sorted(set(ip['files'])|{p.relative_to(B).as_posix() for p in P.rglob('*') if p.is_file()});ip['validation'].append(dict(command='Browser exact native playback, end-frame selection and whole source gallery decoding',result='PASS',evidence='BROWSER_VERIFY_V555.json;82 frame articles/20 component rows, decoded whole sources, native A2 ended without error, no horizontal overflow. Initial whitelist preview failure preserved; machine/UI verification only.'));write(IP,ip)
print('Three browser evidence originals archived and all new artwork licensing/impact coverage recorded.')
