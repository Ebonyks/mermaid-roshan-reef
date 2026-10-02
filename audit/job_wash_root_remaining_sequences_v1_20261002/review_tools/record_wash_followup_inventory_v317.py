from pathlib import Path
import datetime, hashlib, json, shutil
r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
f=r/'audit/job_wash_root_remaining_sequences_v1_20261002'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
def record(rel):
 p=r/rel;return dict(path=rel,bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
sources=[
 ('assets_src/imagegen/day2_doctor_wash_pose_v1_20261001/attempt_06_native.png',4.5,'Readable painted Doctor identity and soapy clasped hands. Standalone static source is a useful provisional rub pose, but supplies no basin contact or completed washing sequence.'),
 ('assets_src/imagegen/day2_doctor_wash_reach_clean_v1_20261001/attempt01_native.png',4.4,'Identity remains coherent, but one hand presses the opposite wrist while the lowered hand hangs. A useful pose study, not proof of reaching to or contacting the basin.'),
 ('assets_src/imagegen/day2_doctor_wash_motion_v1_20261001/motion_key01_attempt01_native.png',4.5,'A clear alternate soapy-hand pose with the same character material. Its difference from the clasp pose needs actual motion/contact review; two source keys do not prove rubbing action.'),
 ('assets_src/imagegen/day2_doctor_wash_clean_result_v1_20261001/attempt01_native.png',4.5,'Separated clean palms provide a useful readable rest study. No basin, faucet stream or water-off transition establishes a complete rinse. Alpha edges and in-game scale require mounted review.')
]
inventory=[dict(**record(p),direct_source_review=True,reviewed_utc=now,standalone_source_opinion=score,priority=score<=4.5,evaluation=note,current_binding=None,owner_acceptance=None) for p,score,note in sources]
d=dict(status='READ_ONLY_REUSE_INVENTORY_AND_ROUTING_HYPOTHESIS',checked_utc=now,baseline=read(f/'PLAN.json')['baseline'],current_code=[record(p) for p in ['scripts/opera_gesture_surface.gd','scripts/opera_career_world_2d.gd']],routing_observations=[
 'Nursery WASH HANDS declares widget empty with visual_context nursery_wash.',
 'CareerWorld _bind_widget passes the phase visual_context to the surface.',
 'GestureSurface _load_widget_set derives widget_template from the first visual_context word; nursery_wash therefore produces nonempty nursery.',
 'GestureSurface drawing returns from the nonempty-widget branch before the later nursery-context branch. The generic widget-family match has no nursery case.',
 'The later _draw_nursery_context nursery_wash branch contains only code-native basin/bubble symbols. Simply exposing it would not satisfy the requested painted washing subject, coherent contact, rub, rinse and clean rest.'
 ],diagnosis='Likely current source cause of the absent Nursery washing subject, pending fresh current native route capture. No runtime change made; this is not a repaired action or a current visual pass.',reuse_inventory=inventory,generation_gap='Reuse suitable approved identity/material sources first. Doctor has useful unbound static pose studies but still lacks audited basin contact and a literal water-on rinse. Doctor-costume poses do not authorize substituting the Nursery profession design. Inspect Nursery approved source masters and current mounted route before generating its missing connected wash gestures.',qualification='Direct static source review of these four existing unchanged native files only. No newly generated source, local motion, production binding, synthesized action frames, save/input/reward change, device/child/owner acceptance or completed repair. This follow-up source inventory is separate from the dated 1818-frame visual review.')
write(f/'NEXT_REPAIR_REUSE_INVENTORY_V317.json',d)
shutil.copyfile(__file__,f/'review_tools'/Path(__file__).name)
ip=r/'design/audit_impacts/job-wash-root-remaining-sequences-review-20261002.json';x=read(ip);x['files']=sorted(set(x['files'])|{p.relative_to(r).as_posix() for p in f.rglob('*') if p.is_file()});write(ip,x)
allow=r/'tmp/v2_preview_allowed.json';write(allow,sorted(set(read(allow))|set(x['files'])))
print('Recorded read-only Nursery routing hypothesis and four existing Doctor source reuse studies; no current repair/pass.')
