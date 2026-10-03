from pathlib import Path
import datetime,hashlib,json,re
from PIL import Image
B=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');P=B/'assets_src/local_motion/candy_twist_release_components_v1_20261003';L=B/'audit/job_artwork_refinement_live';IP=B/'design/audit_impacts/job-candy-twist-release-components-20261003.json';G=P/'gates_v1';R=Path('C:/Users/Peter/Documents/mermaid-roshan-reef/tmp')
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));sha=lambda raw:hashlib.sha256(raw).hexdigest();now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def put(p,raw):p.parent.mkdir(parents=True,exist_ok=True);t=p.with_name(p.name+'.v650_next');t.write_bytes(raw);t.replace(p)
def write(p,d):put(p,(json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode())
proof=read(R/'BROWSER_OBSERVATIONS_V649.json');assert proof['library']['summary'].startswith('V54: 2,152') and proof['report']['componentRows']==24 and proof['library']['historicalLinks']==83 and not proof['library']['historyOpen'] and not proof['library']['overflow'];assert len(proof['report']['videos'])==2 and all(v['width']==896 and v['height']==512 and v['error'] is None and v['ready']>=1 for v in proof['report']['videos']);assert 'Mounted: unassigned' in proof['register']['item'] and 'Complete action: unassigned' in proof['register']['item'] and '4.5/5' in proof['register']['item']
put(P/'BROWSER_OBSERVATIONS_V649.json',(R/'BROWSER_OBSERVATIONS_V649.json').read_bytes());shots=[]
for name in ['CURRENT_LIBRARY_V646.jpg','COMPONENT_REPORT_V648.jpg','RELEASE_FRAME40_V648.jpg','TWIST_FRAME40_V648.jpg']:
 dst=P/name;put(dst,(R/name).read_bytes())
 with Image.open(dst) as im:assert im.format=='JPEG';size=list(im.size)
 shots.append(dict(path=dst.relative_to(B).as_posix(),sha256=sha(dst.read_bytes()),dimensions=size,role='Actual browser QA proof only'))
write(P/'BROWSER_VERIFY_V650.json',dict(status='ACTUAL_V54_CURRENT_FIRST_LIBRARY_BOTH_MEDIA_AND_ALL82_FRAME_ARTICLES_VERIFIED',checked_utc=now(),observations=P.relative_to(B).as_posix()+'/BROWSER_OBSERVATIONS_V649.json',observations_sha256=sha((P/'BROWSER_OBSERVATIONS_V649.json').read_bytes()),screenshots=shots,component_frames_directly_seen=82,component_opinions=24,source_record_mounted_score=None,source_record_action_score=None,qualification='Actual desktop library/report observation. Full native canvases reviewed independently through14 original-size boards. Saved last-frame browser proofs include the complete rendered896×512 canvas. No game/device/child/owner approval.'))
layout=P/'LIBRARY_LAYOUT_PRESERVATION.json';put(P/'LIBRARY_LAYOUT_FIRST_PHASE.json',layout.read_bytes());d=read(layout)
for name in ['index.html','all_items.html']:
 prior=(P/'previous_v53'/name).read_text(encoding='utf-8');current=(L/name).read_text(encoding='utf-8');oldlinks=re.findall(r'<a\b[^>]*href="([^"]+)"',prior);newlinks=re.findall(r'<a\b[^>]*href="([^"]+)"',current);assert all(newlinks.count(x)>=oldlinks.count(x) for x in set(oldlinks)),name
assert read(L/'ALL_ITEMS.json')['items']==read(P/'previous_v53/ALL_ITEMS.json')['items'] and read(L/'ALL_ITEMS.json')['item_shards']==read(P/'previous_v53/ALL_ITEMS.json')['item_shards']
d.update(status='BROWSER_VERIFIED_CURRENT_FIRST_ALL_HISTORICAL_LINKS_AND_OPINIONS_PRESERVED',final_checked_utc=now(),after={name:dict(bytes=(L/name).stat().st_size,sha256=sha((L/name).read_bytes())) for name in ['index.html','all_items.html']},qualification='Literal prior HTML preserved. All original href multiplicities retained;2064 prior item dictionaries and88-item literal part unchanged. First layout phase left root/stamp literal unchanged;subsequent V54 metadata adds new component review resource and refreshes source stamp without score changes. Verified current counts lead;dated notices remain in labelled disclosures. Actual browser opened/closed historical entry with83 links and no overflow. Existing strict root/part/stamp verification unchanged.');write(layout,d)
licenses=B/'ASSET_LICENSES.md';raw=licenses.read_bytes();rows=[]
for x in shots:
 assert x['path'].encode() not in raw;rows.append('| `'+x['path']+'` | Actual local-browser screenshot of reviewed library/component report | Original project QA layout and inherited displayed-art attribution | `'+P.relative_to(B).as_posix()+'/BROWSER_VERIFY_V650.json` binds exact bytes and observed view | QA proof only;no game,motion,device,child or owner acceptance. |')
put(licenses,raw+('\n'+'\n'.join(rows)+'\n').encode())
authority_paths=['audit/MASTER_AUDIT_2026-08-09.md','design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md','audit/findings/ACTIVE_FINDINGS_2026-08-13.md','design/05_DOC_LEDGER.md','design/AUDIT_DEVELOPMENT_CONTRACT.md','design/animation/ROSHAN_MOVEMENT_LANGUAGE.md','design/animation/ANIMATION_PRODUCTION_PROTOCOL.md'];members=[]
for path in authority_paths:
 p=B/path;members.append(dict(path=path,bytes=p.stat().st_size,sha256=sha(p.read_bytes())))
rules=read(IP)['rules'];language=(B/authority_paths[1]).read_text(encoding='utf-8');assert all(k in language for k in rules)
excerpts=[]
for k in ['DL-VIS-07','DL-INT-03','DL-MOT-11','DL-MOT-13','DL-QA-03','DL-QA-07']:
 pos=language.find(k);excerpts.append(dict(rule=k,text=language[max(0,pos-30):pos+750]))
findings=(B/authority_paths[2]).read_text(encoding='utf-8');finding_lines=[x for x in findings.splitlines() if re.match(r'^#{1,6} .*MA-(VIS-006|PLAY-004)',x)];assert len(finding_lines)==2
write(P/'AUTHORITY_RECHECK_V650.json',dict(status='EXACT_APPLICABLE_AUTHORITY_REFERENCES_RECHECKED_FOR_REVIEW',checked_utc=now(),members=members,rules=rules,related_findings=finding_lines,review_excerpts=excerpts,qualification='Read authority remains binding. No rule/finding lifecycle or release threshold changes. Source/structure/action/device/child/owner evidence stay separate.'))
put(P/'review_tools'/Path(__file__).name,Path(__file__).read_bytes());d=read(IP);d['files']=sorted(set(d['files'])|{p.relative_to(B).as_posix() for p in P.rglob('*') if p.is_file()});d['validation'].append(dict(command='Actual current-first library/report/media/frame browser verification',result='PASS',evidence=P.relative_to(B).as_posix()+'/BROWSER_VERIFY_V650.json;V54 counts,83 historical links,24 report rows,two896x512 videos,all41 articles percomponent,no overflow,source mounted/action lanes unassigned.'));write(IP,d)
members=[]
for path in d['files']:
 p=B/path
 if not p.is_file() or path.startswith(G.relative_to(B).as_posix()+'/'):continue
 members.append(dict(path=path,bytes=p.stat().st_size,sha256=sha(p.read_bytes())))
write(G/'CANDIDATE_COMPONENT_SOURCE_V647.json',dict(status='EXACT82_NATIVE_FRAME106_OPINION_REVIEW_AND_V54_LIBRARY_BYTES_FROZEN',baseline=d['baseline'],frozen_utc=now(),members=members,member_count=len(members),qualification='Exact source/report/browser/library bytes before gates. Later gate/impact/publication metadata separately sealed. No creative/action/owner/integration/release acceptance.'))
allow=B/'tmp/v2_preview_allowed.json';write(allow,sorted(set(read(allow))|{p.relative_to(B).as_posix() for p in P.rglob('*') if p.is_file()}));print('SOURCE_FROZEN',len(members),'browser proof4;all original links/opinions preserved',flush=True);print(json.dumps(dict(finding_lines=finding_lines,review_excerpts=excerpts),ensure_ascii=False),flush=True)
