from pathlib import Path
import hashlib,json,re
r=Path.cwd();f=r/'audit/day_two_boxing_live_refinement_v1_20261001'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
before=(f/'PRODUCTION_SURFACE_PRESENTATION_V1.gd').read_text();after=(r/'scripts/opera_boxing_surface.gd').read_text()
old='\tnext.x = clampf(next.x, 62.0, size.x - 62.0)\n\tnext.y = clampf(next.y, 54.0, size.y - 38.0)'
new='\t# Keep the complete painted card inside the canvas at maximum depth/pulse\n\t# scale and angle. Every authored target remains inside these safe bounds.\n\tnext.x = clampf(next.x, 144.0, size.x - 144.0)\n\tnext.y = clampf(next.y, 152.0, size.y - 128.0)'
assert old in before and new in after and before.replace(old,new)==after
capture=json.loads((f/'native_actions_v1/CAPTURE_RECEIPT.json').read_text())
drags=[x for x in capture['inputs'] if x['type']=='drag'];checks=[]
for x in drags:
    px,py=x['local_xy'];checks.append(dict(width=x['width'],mode=x['mode'],hand=x['hand'],timestamp_us=x['timestamp_us'],local_xy=x['local_xy'],old_clamped=[max(62,min(1218,px)),max(54,min(682,py))],new_clamped=[max(144,min(1136,px)),max(152,min(592,py))]))
assert len(checks)==160 and all(x['old_clamped']==x['new_clamped']==x['local_xy'] for x in checks)
assert all(x['touch_owners']=={} or set(x['touch_owners'].values()).issubset({0,1}) for x in capture['frames'])
edge=json.loads((f/'native_edges_v2/CAPTURE_RECEIPT.json').read_text());assert len(edge['views'])==16 and all(x['inside_action_surface'] for x in edge['views'])
d=dict(status='ONLY_EDGE_CLAMPS_CHANGED_ALL_160_CAPTURED_ACTION_DRAGS_IDENTICAL',previous_production_copy='PRODUCTION_SURFACE_PRESENTATION_V1.gd',previous_sha256=sha(f/'PRODUCTION_SURFACE_PRESENTATION_V1.gd'),current_path='scripts/opera_boxing_surface.gd',current_sha256=sha(r/'scripts/opera_boxing_surface.gd'),captured_action_receipt_sha256=sha(f/'native_actions_v1/CAPTURE_RECEIPT.json'),drag_checks=checks,
    qualification='The20 native action sequences bind the pre-edge production hash. Only the two edge clamps and their explanatory comment differ now; every one of their160 actual drag requests is numerically unchanged by either clamp, including hand ownership and contact path. Source/image/input/phase/processing/render methods otherwise remain literal equals. This bounded equivalence does not relabel a past capture as a new source hash, waive a regression gate or cover other gestures. Current16 boundary drags are independently captured at the new hash.')
(f/'BOUNDARY_REPAIR_EQUIVALENCE_V2.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
for folder,impactname in [('audit/day_one_pool_live_refinement_v2_20261001','day-one-pool-live-refinement-v2-20261001'),('assets_src/imagegen/day1_playroom_sign_v2_20261001','day-one-playroom-sign-v2-20261001'),('audit/day_two_boxing_puff_reuse_v1_20261001','day-two-boxing-puff-reuse-v1-20261001'),('assets_src/imagegen/day2_boxing_single_gloves_v1_20261001','day-two-boxing-single-gloves-v1-20261001'),('audit/day_two_boxing_live_refinement_v1_20261001','day-two-boxing-live-refinement-v1-20261001')]:
    p=r/'design/audit_impacts'/f'{impactname}.json';d=json.loads(p.read_text());d['files']=sorted(set(d['files'])|{x.relative_to(r).as_posix() for x in (r/folder).rglob('*') if x.is_file()});p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
lic=r/'ASSET_LICENSES.md';s=lic.read_text(encoding='utf-8')
for folder in ['audit/day_one_pool_live_refinement_v2_20261001','assets_src/imagegen/day1_playroom_sign_v2_20261001','audit/day_two_boxing_puff_reuse_v1_20261001','assets_src/imagegen/day2_boxing_single_gloves_v1_20261001','audit/day_two_boxing_live_refinement_v1_20261001']:
    for p in sorted((r/folder).rglob('*')):
        if not p.is_file() or p.suffix.lower() not in ['.png','.webp','.mp4']:continue
        rel=p.relative_to(r).as_posix()
        if '`'+rel+'`' in s:continue
        s+=f'| `{rel}` | Mermaid Roshan project artwork / diagnostic evidence capture | Existing project provenance; review-only derivative | Local project | Exact native rendered or browser diagnostic image, complete-canvas review board or native-timed video as applicable; hashes and generation sources retained in review family; no new runtime art or owner approval |\n'
lic.write_text(s,encoding='utf-8',newline='\n')
print('Only clamp delta proved; all160 action drags unchanged;16 current edges enclosed; coverage/licenses refreshed.')
