from pathlib import Path
import datetime,json,shutil,subprocess
R=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
L=R/'audit/job_artwork_refinement_live';S=R/'assets_src/imagegen/nursery_scrub_attention_fresh_v1_20261002'
ip=R/'design/audit_impacts/job-nursery-fresh-attention-20261002.json'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
d=read(L/'ALL_ITEMS.json');assert len(d['items'])==1802 and d['display_revision']=='V36_FRESH_NURSERY_ATTENTION_AND_REJECTED_A2'
old=d['scope'];assert old.startswith('V34 known union:')
h=L/'history_v36_before_metadata';assert not h.exists();h.mkdir()
for name in ('ALL_ITEMS.json','all_items.html'):shutil.copyfile(L/name,h/(name+'.original'))
d['updated_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
d['scope']='V36 known register:1263 unique source files,328 pose cells,85 runtime state/use/action entries and126 source object regions =1802 entries. Adds two fresh Nursery native source paintings and22 individual component opinions: A1 continuity4.1 rejected; A2 unbound static4.5/gaze-style4.6/palm4.5 provisional. Every41 local prompt-only A2 motion frame reviewed; action3.0 rejected. Current source-bound Geologist review separately covers58 selected complete canvases/318 opening-to-earned-return frames; rooted opening4.5/material4.6 and23 inclusive current priorities. Current Nursery complete wash3.9/attention3.8/room2.9 and10 inclusive current priorities remain unchanged. All783 recorded current production source bytes unchanged. Known source/cell/region priorities706;385 source reviews still required. Complete timed pan/fossil phases, ordinary full career/training breadth, device, child and owner acceptance remain separate; this register is not exhaustive live-use or all-job acceptance. Individual opinion dates and every historical register remain preserved.'
d['qualification']='Literal registered source continuity retains only qualified source opinions. Exact current captures establish separately named mounted/object/action opinions; still materials never pass embodied actions. 706 counts known source/cell/region opinions at the inclusive<=4.5 priority threshold, not706 weak live objects. 23 current Geologist and10 Nursery priorities remain separately counted. A score of4.5 meets the provisional source floor and remains an inclusive refinement priority. Two fresh Nursery natives/22 components are unbound; local A2 motion3.0 rejected. 385 source file reviews and broad live-route/device/child/owner/all-job acceptance remain open. Originals, rejected candidates and dated history are preserved; neither pending reference upload nor browser persistence action is authorized by this update.'
write(L/'ALL_ITEMS.json',d)
p=L/'all_items.html';raw=p.read_text(encoding='utf-8');assert 'register.created_utc' in raw or 'data.created_utc' in raw or 'd.created_utc' in raw
for name in ('register','data','d'):raw=raw.replace(name+'.created_utc','('+name+'.updated_utc || '+name+'.created_utc)')
p.write_text(raw,encoding='utf-8',newline='\n')
shutil.copyfile(__file__,S/'review_tools'/Path(__file__).name)
impact=read(ip);impact['files']=sorted(set(impact['files'])|{x.relative_to(R).as_posix() for x in h.rglob('*') if x.is_file()}|{(S/'review_tools'/Path(__file__).name).relative_to(R).as_posix()});write(ip,impact)
subprocess.run(['C:/Users/Peter/AppData/Local/Python/bin/python.exe','-X','utf8','-B',str(L/'review_tools/refresh_current_job_review_v35.py')],cwd=R,check=True)
print('CURRENT_METADATA_V36_CORRECTED|old V34 summary preserved|no scores changed|updated stamp accurate')
