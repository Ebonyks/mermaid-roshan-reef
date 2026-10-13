"""Verify exact source evidence, stable units and unchanged acceptance for R17."""
from pathlib import Path
import json,hashlib,subprocess,re
P=Path(__file__).resolve().parent;R=P.parents[3];V=P.parent/'r16_pointer_candidate';BASE='182f2e522a330b89bf7329b26516583160f343e0'
def get(n):return json.loads((P/n).read_text(encoding='utf-8'))
def sha(b):return hashlib.sha256(b).hexdigest()
def blob(p):return subprocess.check_output(['git','show',BASE+':'+p],cwd=R,stderr=subprocess.PIPE)
c=get('SCRIPT_CENSUS.json');paths=subprocess.check_output(['git','ls-tree','-r','--name-only',BASE,'scripts'],cwd=R,text=True).splitlines();paths=sorted(p for p in paths if p.endswith('.gd') and not Path(p).name.startswith('probe'));assert paths==[x['path'] for x in c['files']]
raw={p:blob(p) for p in paths}
for x in c['files']:assert len(raw[x['path']])==x['bytes'] and sha(raw[x['path']])==x['sha256']
for x in get('SOURCES.json')['sources']:
 b=blob(x['path']);assert x['revision']==BASE and len(b)==x['bytes'] and sha(b)==x['sha256']
 checkout=(R/x['path']).read_bytes();assert checkout.replace(b'\r\n',b'\n')==b.replace(b'\r\n',b'\n') if x['path'].endswith('.gd') else checkout==b
for x in get('SOURCE_EXCERPTS.json')['entries']:
 lines=raw[x['path']].decode('utf-8-sig').splitlines();t='\n'.join(lines[x['start_line']-1:x['end_line']])+'\n';assert t==x['text_lf'] and sha(t.encode())==x['sha256_excerpt_lf']
a=get('SOURCE_AUDIT.json');assert len(a['rows'])==15 and sum(len(x['source_phase_rows']) for x in a['rows'])==61
assert sum(x['uses_shared_helper'] for x in a['rows'])==12 and sum(len(x['source_phase_rows']) for x in a['rows'] if x['uses_shared_helper'])==49
acts=raw['scripts/opera_house.gd'].decode().split('const ACTS := [',1)[1].split('\n]',1)[0];pairs=[];retired=[]
for b in re.findall(r'\{([^{}]+)\}',acts):
 m=re.search(r'"save_bit": (\d+)',b)
 if not m:continue
 slot=int(m[1]);career=re.search(r'"costume": "([^"]+)"',b)
 if career:pairs.append((slot,career[1]))
 elif '"retired": true' in b:retired.append(slot)
assert pairs==[(int(x['route_id'].rsplit('.',1)[1]),x['career']) for x in a['rows']] and retired==[4,9,14]
for x in a['rows']:
 t=raw[x['surface_path']].decode();assert x['source_only'] and not x['runtime_context_complete']
 if not x['uses_shared_helper']:assert '_draw_demo_finger(' not in t and 'super._draw(' not in t
refs=[(p,i,l) for p,b in raw.items() for i,l in enumerate(b.decode('utf-8-sig').splitlines(),1) if 'assets/castle/training/ghost_hand.png' in l];assert refs==[(x['path'],x['line'],x['text']) for x in a['old_hand_path_references']]
assert len({x[0] for x in refs})==16
for n in ['per_piece.json','scene_coverage.json','tally.json','CONGRUENCY_BACKLOG.json']:
 old=json.loads((V/n).read_text());new=get(n)
 if n=='per_piece.json':
  assert [(x['id'],x['status']) for x in old['pieces']]==[(x['id'],x['status']) for x in new['pieces']]
  assert old['supplemental_piece_records']==new['supplemental_piece_records']
 if n=='scene_coverage.json':assert [(x['id'],x['status'],x['captures']) for x in old['entries']]==[(x['id'],x['status'],x['captures']) for x in new['entries']]
 if n=='tally.json':
  for k in ['named_piece_records','named_family_count','named_status_counts','all_game_individual_piece_total','current_distinct_screen_total','accepted_removed','integrated','runtime_verified','remaining_source_scopes_to_disposition','current_context_sample_lanes']:assert old[k]==new[k],k
  for k in ['exact_capture_count','retained_native_capture_count','retained_native_captures','partial_overlapping_entries','complete_entries','entries_without_current_slice']:assert old['current_context'][k]==new['current_context'][k],k
assert not subprocess.check_output(['git','diff',BASE,'--','scripts','scenes','assets','assets_src','project.godot','tools'],cwd=R,stderr=subprocess.PIPE)
assert get('SOURCE_AUDIT.json')['accepted_removed']==0 and get('SOURCE_AUDIT.json')['native_captures_added']==0
print('R17 PASS: exact171-script census/29 sources,source ranges,15 live routes/61 constant phases/12 shared49/3 independent12; stable IDs,statuses,counts,captures and runtime unchanged; all acceptance open')
