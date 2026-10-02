from pathlib import Path
import datetime,hashlib,json,subprocess

root=next(p for p in Path(__file__).resolve().parents if (p/'project.godot').is_file())
live=root/'audit/job_artwork_refinement_live'
registry=json.loads((live/'ALL_ITEMS.json').read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None
observed={}
items=[]
for item in registry['items']:
 path=item['path'];file=(root/path).resolve()
 assert file.is_relative_to(root.resolve()) and not path.startswith(('.secrets/','.git/','.codex/','.claude/'))
 if path not in observed:observed[path]=sha(file)
 match=observed[path]==item.get('current_checkout_sha256') and observed[path] is not None
 binding=item.get('current_binding');binding_match=None
 if binding and item.get('binding_sha256'):
  binding_match=sha(root/binding)==item['binding_sha256']
 items.append(dict(id=item['id'],path=path,observed_sha256=observed[path],registered_sha256=item.get('current_checkout_sha256'),source_match=match,binding_match=binding_match))
family=root/'audit/job_geode_current_recheck_v1_20261002'
snapshot=json.loads((family/'SOURCE_CURRENT_BEFORE_CAPTURE.json').read_text())
boundary=[dict(path=x['path'],recorded_sha256=x['sha256'],observed_sha256=sha(root/x['path'])) for x in snapshot['source_files']]
changed=[x for x in boundary if x['recorded_sha256']!=x['observed_sha256']]
stamp=dict(schema='reef.current-review-boundary-refresh.v1',status='CURRENT_GEODE_CAPTURE_SOURCE_BOUNDARY_MATCH' if not changed else 'STALE_GEODE_CAPTURE_SOURCE_BOUNDARY_REVIEW_REQUIRED',checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),working_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),registry_items=len(items),unique_registered_paths=len(observed),registered_source_matches=sum(x['source_match'] for x in items),source_changed_or_unavailable=[x for x in items if not x['source_match']],geode_review='audit/job_geode_current_recheck_v1_20261002/DIRECT_REVIEW.json',geode_capture_source_count=len(boundary),geode_capture_boundary_match=not changed,geode_changed_sources=changed,items=items,qualification='Refresh reads known literal sources and recorded binding hashes only. It does not generate art, change opinions, play the game or grant visual/owner acceptance. Changed sources withhold their current opinions in the register display; prior opinions remain in the saved register/history. Any changed member of the recorded geode capture source boundary requires a current rerender before its mounted claims can be displayed as current. All eight dated Doctor/Nursery capture cases remain explicitly historical, not rescued by this refresh.')
nursery=root/'audit/job_nursery_wash_connected_v1_20261002'
nsnapshot=json.loads((nursery/'SOURCE_CURRENT_MACHINE_V3.json').read_text())
nboundary=[dict(path=x['path'],recorded_sha256=x['sha256'],observed_sha256=sha(root/x['path'])) for x in nsnapshot['source_files']]
nchanged=[x for x in nboundary if x['recorded_sha256']!=x['observed_sha256']]
stamp.update(nursery_capture_boundary_match=not nchanged,nursery_capture_source_count=len(nboundary),nursery_changed_sources=nchanged,nursery_review='audit/job_nursery_wash_connected_v1_20261002/DIRECT_REVIEW_CURRENT_V3.json')
stamp['status']='CURRENT_NURSERY_BOUNDARY_MATCH_GEODE_REVIEW_STALE' if not nchanged and changed else ('CURRENT_CAPTURE_BOUNDARIES_MATCH' if not nchanged and not changed else 'NURSERY_CURRENT_CAPTURE_REVIEW_STALE')
stamp['qualification']+=' Current Nursery v3 room/caller captures are separately source-bound; old Doctor/birthday/full-career/device evidence is not promoted by a hash refresh.'
(live/'CURRENT_BOUNDARY_REFRESH.json').write_text(json.dumps(stamp,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
print(stamp['status']+'|'+str(stamp['registered_source_matches'])+'/'+str(len(items))+' registered item hashes match|'+str(len(changed))+' changed geode boundary sources')
