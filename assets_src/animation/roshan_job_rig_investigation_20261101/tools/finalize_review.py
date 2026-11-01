"""Refresh review labels, specific asset provenance and exact coverage."""
from pathlib import Path
import json,hashlib,subprocess,sys,datetime,platform
from PIL import Image
R=Path(__file__).resolve().parents[1];REPO=R.parents[2];PREFIX=R.relative_to(REPO).as_posix()
load=lambda p:json.loads(p.read_text(encoding="utf8"))
def save(p,d):p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf8')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
mix=load(R/'evidence/mixed_outline.json');bad=mix['fit_failing_snapshots'];new=mix['new_job_fit_failing_snapshots']
selection=load(R/'evidence/candidate_selection.json');selection.update(preferred_review_candidate='v6',v4_disposition='Superseded: global fin erasure regressed legacy tail choices. Reports and two native examples retained; v6 restores exact seed rendering.',v6_disposition='Conditional legacy anatomy/fin/ownership selection;270 legacy snapshots equal v8,968 complete new-action/regression snapshots equal v4.',mixed_fit_failures=f'{bad}/250;{new} include a new job part')
save(R/'evidence/candidate_selection.json',selection)
prov=load(R/'provenance.json');prov['candidate']='v6_review_only';prov['edits'].append({'method':'Conditional anatomy/fin ownership preservation; no generation or new painting. Exact original_tail restored from immutable seed.','recipe':'tools/legacy_fin_layers.lua; demo/investigation.gd; demo/costume.gdshader','evidence':'evidence/legacy_seed_pixel_comparison.json; evidence/v6_new_action_preservation.json'})
save(R/'provenance.json',prov)
visual=load(R/'evidence/visual_review.json');visual['candidate']='v6';visual['observations']=[x.replace('in65/250',f'in{bad}/250') for x in visual['observations']];save(R/'evidence/visual_review.json',visual)
p=R/'README.md';s=p.read_text(encoding="utf8");start=s.index('Current status:');end=s.index('## Open and inspect',start)
s=s[:start]+f'''Current status: **SOURCE-ONLY REVIEW DRAFT / CANDIDATE v6**. v6 fixes a\nlegacy-fin regression in v4:270 native samples over all27 legacy outfits now\nmatch the immutable v8 seed exactly. All968 complete detective/geologist action\nand regression frames remain pixel-identical to v4. v5's bounded paint repair\nwas rejected for worsening mixed fit65to80. Current strict contour checks still\nfail, and{bad}/250 mixed snapshots fail ({new} include a new job part). The\nshared contract remains unpublished. All82 trusted probes have passing evidence\nafter isolated reruns, with original failures retained. Publication state is in\n`evidence/publication_receipt.json`. Compatible wardrobe and delivery acceptance\nremain blocked; no dev/master integration.\n\nDiagnostic boards (source study, including unresolved poses):\n\n![Detective work samples](review/detective_work_board.jpg)\n\n![Geologist work samples](review/geologist_work_board.jpg)\n\n'''+s[end:]
s=s.replace('grip_parts, repair_parts, repair_seam, final_masters.','grip_parts, repair_parts, repair_seam, legacy_fin_layers, final_masters.')
s=s.replace('The source bindings also expose independent head/body/tail slots.','The source bindings expose independent head/body/tail slots through set_parts and equip_catalog_ids; H/J/K retain the seed legacy-slot cycle.')
s+='\n`tools/legacy_reference.py` compares all27 legacy outfits at ten authored arm,\nblink and tail times with a disposable immutable-v8 actor. Only resource URLs\nare relocated; the reference shader/rest/weights/curves are unchanged. The270\nreference images are in the legacy_seed_preservation ZIPs. New job-only outputs\nare independently compared against v4. These sampled equalities preserve\nbehavior; they do not prove continuous fit or artistic acceptance. CHG-126\nrecords benefits, risks, exact publication binding and rollback scope.\n'
p.write_text(s,encoding="utf8")
for n in ['handoff_status.json']:
 d=load(R/'evidence'/n);d['quality']=f'Candidatev6; legacy preservation restored; strict new contour floors and{bad}/250 mixed samples fail. v5 paint repair rejected.';d['check_time_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();save(R/'evidence'/n,d)
freeze=load(R/'evidence/frozen_inputs_v6.json');drift=[x['path'] for x in freeze['files'] if sha(R/x['path'])!=x['sha256']];assert not drift,drift
save(R/'evidence/preferred_source_restoration.json',{'candidate':'v6','frozen_inputs_drift':drift,'pass':not drift,'reference':'frozen_inputs_v6.json; v4 new-action bytes are independently preserved by v6_new_action_preservation.json'})
save(R/'evidence/review_movie_exports.json',[{'job':j,'candidate':'v6','sha256':sha(R/'review'/f'{j}_work.mp4'),'dimensions':[1280,720],'fps':30,'source':f'evidence/raw_frames_v6/{j}/%04d.png','derivation':'Native RGBA uniformly720/1024 scaled, centered; silent diagnostic; no retiming or artificial acting.'} for j in ['detective','geologist']])
tool={'python':platform.python_version(),'aseprite_file_version':'1.3.18.4','godot':load(R/'evidence/capture_environment.json'),'image_generation':'built-in image_gen; revision/seed/cost unexposed;3 calls','ffmpeg':'8.1.2; command path and export mapping retained in tools/package_native.py'};save(R/'evidence/tool_versions.json',tool)
names=set()
for args in [['git','ls-files','--',PREFIX],['git','ls-files','--others','--exclude-standard','--',PREFIX]]:names.update(subprocess.run(args,cwd=REPO,capture_output=True,text=True,check=True).stdout.splitlines())
frozen=load(R/'contract/frozen_inputs_v8.json')['files'];by_hash={v:k for k,v in frozen.items()}
source=load(R/'source_inventory.json')['sources'];source_hash={x['sha256']:x['path'] for x in source}
native_ids={'detective_take01.png':'exec-3af64ab2-4030-4062-b4ce-49daa8c8d33d','geologist_take01.png':'exec-c850d1f0-edd6-40a4-a3cb-23d3368e091b','grip_take01.png':'exec-5f9d9fa6-18f4-4cde-8999-fe37fb2b3526'}
assets=[]
for name in sorted(names):
 p=REPO/name;rel=p.relative_to(R).as_posix()
 if p.suffix.lower() not in ['.png','.jpg','.jpeg','.mp4','.aseprite','.zip']:continue
 digest=sha(p);sources=[];role='non-runtime source/review derivative';mod='New derived review path; original sources preserved'
 if digest in by_hash:sources=[by_hash[digest]];mod='Literal copy of frozen v8 source'
 elif digest in source_hash:sources=[source_hash[digest]];mod='Literal project-source copy'
 elif rel.startswith('native/'):
  sources=['built-in image_gen:'+native_ids[p.name]];role='Unaccepted native generation; exact prompt in imagegen_prompts.json';mod='Original provider output preserved'
 elif rel.startswith('demo/art/'):
  if p.stem.startswith(('detective_','geologist_')):
   job=p.stem.split('_')[0];sources=['native/'+job+'_take01.png','demo/art/anatomy.png','demo/art/ballet_scalp.png'];role='Registered replacement garment source; complete native contours'
  elif 'grip' in p.stem:sources=['native/grip_take01.png'];role='Provisional isolated front grip'
  elif p.stem=='magnifier_glass':sources=['assets/opera/worlds/ui/magnifier.png'];role='Local lens-alpha derivative'
  else:sources=['demo/art/anatomy.png','demo/art/ownership.png','demo/art/upper_arm.png','demo/art/forearm.png'];role='Declared local anatomy/ownership/arm preservation derivative; Aseprite recipes'
 elif rel.startswith('evidence/rejected_legacy_fin_v4/'):
  sources=['evidence/frozen_inputs_v4.json','evidence/rejected_legacy_fin_v4/frame_index.json','evidence/rejected_legacy_fin_v4/mixed_outline.json'];role='Retained failed v4 native evidence, before conditional fin restoration'
 elif '/rejected_' in rel:
  sources=[q.relative_to(R).as_posix() for q in p.parent.glob('*.json')];role='Retained rejected-candidate diagnostic; source and failures remain in sibling records'
 elif rel.startswith('masters/'):
  sources=['demo/art/'+x for x in ['investigation_anatomy.png','grip_front.png','forearm.png','fore_work.png']]+['tools/final_masters.lua'];role='Editable layered source inspection master, not finished animation'
 elif p.suffix=='.zip':sources=['evidence/native_export.json','evidence/frame_index.json','evidence/legacy_seed_pixel_comparison.json'];role='Literal native Godot PNG archive; exact per-frame sources/hashes in embedded frame_index.json'
 else:sources=['evidence/frame_index.json','evidence/native_export.json','evidence/frozen_inputs_v6.json'];role='Actual engine capture, control or uniformly scaled review derivative; no acceptance'
 dims=list(Image.open(p).size) if p.suffix.lower() in ['.png','.jpg','.jpeg'] else ([1280,720] if p.suffix=='.mp4' else [1024,1024])
 assets.append({'path':name,'sha256':digest,'role':role,'license':'Project-owned source artwork / built-in ImageGen candidate; no external license added','provenance':'; '.join(sources),'source_paths':sources,'modification_status':mod,'dimensions':dims})
save(R/'asset_manifest.json',{'assets':assets,'scope':'Source-only review; provenance does not grant identity/quality acceptance'})
p=REPO/'ASSET_LICENSES.md';s=p.read_text(encoding="utf8");s='\n'.join(line for line in s.splitlines() if not line.startswith('- `'+PREFIX+'/'))+'\n'
s+='\n'.join('- `'+a['path']+'` — '+a['role']+'; project-owned source/derived artwork; source paths: '+a['provenance']+'; source URL: https://github.com/Ebonyks/mermaid-roshan-reef/tree/b700b846d1d2f4b1843279f268e2bb12e4b1f4ec or built-in generation (no external URL); modifications, exact hashes and scope in asset_manifest.json.' for a in assets)+'\n';p.write_text(s,encoding="utf8")
p=REPO/'design/audit_impacts/roshan-job-rig-investigation-20261101.json';d=load(p);d['acceptance_gaps']=f'Source-only review draftv6. Strict new seam floors and{bad}/250 mixed snapshots fail; shared common waist contract unpublished; natural acting/grasp/support/facing, authoritative visual proof, full-speed playback/device/child/owner remain pending. No production adoption, dev/master integration or finding closure.'
for v in d['validation']:
 if 'Same fixed' in v['command']:v['evidence']=PREFIX+'/evidence/strict_regression.json; mixed_outline.json; v6 unaccepted; v5 rejected'
d['validation'].append({'command':'270 exact immutable-v8 legacy samples and968 v4 complete-action/regression preservation samples','result':'PASS','evidence':PREFIX+'/evidence/legacy_seed_pixel_comparison.json; v6_new_action_preservation.json'})
names=set()
for args in [['git','ls-files','--',PREFIX],['git','ls-files','--others','--exclude-standard','--',PREFIX]]:names.update(subprocess.run(args,cwd=REPO,capture_output=True,text=True,check=True).stdout.splitlines())
d['files']=sorted(names|{'ASSET_LICENSES.md','audit/MASTER_AUDIT_2026-08-09.md','audit/MASTER_AUDIT_CHANGELOG_ROLLBACK_2026-08-10.md','design/05_DOC_LEDGER.md'});save(p,d)
print('REFRESHED',len(assets),'assets;',bad,'mixed failures;',len(names),'package files')
