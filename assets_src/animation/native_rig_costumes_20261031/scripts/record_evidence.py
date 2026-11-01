"""Refresh exact task coverage, provenance and honest machine/acceptance summary."""
from pathlib import Path
import json,hashlib,subprocess,re
ROOT=Path(__file__).resolve().parents[1];REPO=ROOT.parents[2];REL=ROOT.relative_to(REPO).as_posix()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def files():return sorted({s.decode() for s in subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard','-z','--',REL],cwd=REPO).split(b'\0') if s and (REPO/s.decode()).is_file()})
def read(p):return json.loads(p.read_text(encoding='utf-8-sig')) if p.exists() else None
def main():
 summary={'baseline':'005ba38a170f226d51ee906ce7d390ef682af9ac','candidate':'Final v5 after headwear alpha-speck removal','costumes':{},'acceptance':{'production_integrated':False,'owner':'PENDING','device':'PENDING','child':'PENDING','game_wide':'UNSATISFIED'},'publication':{'branch':'codex/native-rig-costumes-20261031','dev_integration':False,'reason':'ODR-DEMO-FREEZE-20261031'}}
 for theme in ['ballet','magician']:
  folder=ROOT/f'evidence/render_{theme}_v5';g=read(folder/'geometry_audit.json');m=read(folder/'motion_audit.json');engine=read(folder/'engine_receipt.json')
  summary['costumes'][theme]={'geometry_pass':g.get('machine_geometry_pass') if g else None,'motion_pass':m.get('pass') if m else None,'engine_receipt':engine}
 for key,name in [('swap','swaps_v3/swap_audit.json'),('identity','identity_audit.json'),('same_audit','same_audit_contract.json'),('aseprite','aseprite_roundtrip.json'),('media','media_verification.json'),('reproduction','reproduction.json')]:
  r=read(ROOT/'evidence'/name);summary[key]={'pass':r.get('pass') if r else None,'evidence':'evidence/'+name}
 summary['costume_audits_pass']=all(all(v[k] is True for k in ['geometry_pass','motion_pass']) for v in summary['costumes'].values()) if all(v[k] is not None for v in summary['costumes'].values() for k in ['geometry_pass','motion_pass']) else None
 summary['final_machine_pass']=all(all(v[k] is True for k in ['geometry_pass','motion_pass']) for v in summary['costumes'].values()) and all(summary[k]['pass'] is True for k in ['swap','identity','same_audit','aseprite','media','reproduction'])
 receipts=[read(p) for p in (ROOT/'evidence').glob('render_*/engine_receipt.json')];summary['retained_render_runs']=len(receipts);summary['retained_render_frames']=sum(r['frames_rendered'] for r in receipts);summary['retained_state_seeks']=sum(r['state_seeks'] for r in receipts)
 gates=ROOT/'evidence/project_gates.exit';rerun=ROOT/'evidence/project_probes_rerun.exit';project=read(ROOT/'evidence/project_gate_receipt.json');summary['local_project_probe_lane']={'initial_exit':gates.read_text().strip() if gates.exists() else None,'final_rerun_exit':rerun.read_text().strip() if rerun.exists() else None,'latest_individual_pass':project.get('pass') if project else None,'single_full_rerun_pass':project.get('single_full_rerun_pass') if project else None,'scope':'Initial exact import/2D-regression/82-probe suffix found a reproduced zero-sample Geologist probe gap. A complete rerun follows a probe-only sampling repair, retaining every geometry predicate. The later unchanged Melody intermittent miss and downstream count failure are retained; read-only trace and uninstrumented focused retest pass, without proving historical cause. Latest individual verdicts are distinct from a green uninterrupted full-suite run. Earlier static/audio/full-CI prefix is prior exact baseline evidence, not a new local full-ci claim. Exact published-head full CI tracked separately.','evidence':'evidence/project_gate_receipt.json'}
 (ROOT/'evidence/summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
 p=ROOT/'provenance.json';prov=read(p)
 for attempt in prov['attempts']:
  f=ROOT/'native'/('ballet_fit.png' if attempt['brief'].startswith('ballet') else 'magician_fit.png');attempt['retained_path']=f.relative_to(ROOT).as_posix();attempt['sha256']=sha(f);attempt['source_reference_hashes']={n:sha(REPO/n) for n in [attempt['edit_target']]+attempt['appearance_references']}
 prov['final_preparation']='scripts/build_costumes.py and godot/costumes.json; uniform registration, bounded clothing RGB masks, no generated identity pixels; source headpiece matte cleanup retains the main opaque component and antialias support.'
 prov['rejected_intermediate_evidence']='preparation_reject_v1-v8 plus render v1-v4. Numerical passes were not visual acceptance. v4 exact face check failed on one alpha=1 headwear speck per costume; final v5 derives a clean headpiece matte.'
 prov['time_accounting']='Exact per-call tool wall seconds retained; manual cleanup minutes not separately instrumented. No additional generation after two fitting calls; action caps in job_cards.json. Verification/export/probe time is retained in process logs rather than invented cleanup timings.'
 p.write_text(json.dumps(prov,indent=2)+'\n',encoding='utf-8')
 card=read(ROOT/'job_cards.json');card['attempts']=prov['attempts'];card['current_method']='Uniform garment-only fitting plate RGB over approved undergarment; same skeleton, meshes and action curves; direct original headpiece reuse with matte cleanup.';(ROOT/'job_cards.json').write_text(json.dumps(card,indent=2)+'\n',encoding='utf-8')
 fs=files();lic=REPO/'ASSET_LICENSES.md';s=lic.read_text(encoding='utf-8');marker='<!-- NATIVE_RIG_COSTUMES_20261031 -->';end='<!-- NATIVE_RIG_COSTUMES_20261031_END -->'
 if marker in s:
  a=s.index(marker)
  if end in s[a:]:b=s.index(end,a)+len(end)
  else:
   title=s.index('## Native rig replaceable costume study',a);following=s.find('\n## ',title+4);b=len(s) if following<0 else following
  s=s[:a].rstrip()+s[b:]
 rows=[]
 for n in fs:
  f=REPO/n
  if f.suffix.lower() in {'.png','.jpg','.mp4','.mkv','.aseprite'}:rows.append(f'| `{n}` | Existing Fashion Designer beta source / built-in ImageGen fitted garment derivative / actual native Godot render | Project source / generated candidate; production acceptance pending | [{REL}/provenance.json]({REL}/provenance.json) | Non-destructive registered clothing masks, source-only rig capture or lossless review master; originals preserved. |')
 lic.write_text(s+'\n\n'+marker+'\n\n## Native rig replaceable costume study\n\n| Asset | Source | Licence / scope | Evidence | Modifications |\n|---|---|---|---|---|\n'+'\n'.join(rows)+'\n\n'+end+'\n',encoding='utf-8')
 impact_path=REPO/'design/audit_impacts/native-rig-costumes-20261031.json';impact=read(impact_path);root_files=['ASSET_LICENSES.md','design/05_DOC_LEDGER.md','audit/MASTER_AUDIT_2026-08-09.md','audit/findings/ACTIVE_FINDINGS_2026-08-13.md','scripts/probe_opera_2d.gd'];impact['files']=sorted(set(files()+root_files))
 checks=[('Same original auditor bytes, shared rig/curves and real wardrobe IDs','same_audit_contract.json','pass'),('Original geometry and seam audit on both costumes','summary.json','costume_audits_pass'),('Exhaustive mixed-slot/fresh-instance/live swap/negative controls','swaps_v3/swap_audit.json','pass'),('Exact face/hand preservation and whole-original restoration','identity_audit.json','pass'),('Six Aseprite masters reopened/exported losslessly','aseprite_roundtrip.json','pass')]
 impact['validation']=[]
 for command,name,key in checks:
  value=read(ROOT/'evidence'/name);state='PENDING' if not value or value.get(key) is None else ('PASS' if value.get(key) else 'FAIL');impact['validation'].append({'command':command,'result':state,'evidence':REL+'/evidence/'+name})
 for command,name in [('Approved-engine import/2D inventory and latest individual 82-probe verdicts, including unchanged Melody retest; non-green complete runs retained','project_gate_receipt.json'),('Changed-script, authority/development and whitespace checks','final_gate_receipt.json')]:
  receipt=read(ROOT/'evidence'/name);impact['validation'].append({'command':command,'result':'PENDING' if not receipt or receipt.get('pass') is None else ('PASS' if receipt.get('pass') else 'FAIL'),'evidence':REL+'/evidence/'+name})
 impact['validation'].append({'command':'Exact published-head full GitHub CI','result':'PENDING','evidence':'GitHub Actions exact commit receipt is recorded after publication; local tests do not establish remote CI.'})
 impact['lessons']=[{'lesson':'A geometry pass can coexist with visibly wrong fabric registration. Inspect garment RGB, masks, shared waist and fin boundaries independently.','write_back':'audit/MASTER_AUDIT_2026-08-09.md#0-planning-entry'},{'lesson':'Alpha=1 specks in a head accessory can tint a single face pixel while component/seam metrics pass. Clean the derivative matte and require exact protected-pixel comparison.','write_back':REL+'/README.md'},{'lesson':'Independent costume replacement should retain one skeleton/timeline and immutable base; compare mixed-slot snapshots to fresh actors and inject stale materials.','write_back':REL+'/README.md'}]
 impact['references_used']=[{'path':'design/FASHION_DESIGNER_ROSHAN_2026-10-06.md','purpose':'Persistent independent slot IDs and existing candidate clothing scope.'},{'path':'design/animation/ANIMATION_PRODUCTION_PROTOCOL.md','purpose':'Bounded source derivation, Aseprite and separate acceptance lanes.'},{'path':'assets_src/animation/native_rig_stress_20261031/README.md','purpose':'Exact prior numerical floors, acting curves and scoped native-rig study exception.'}]
 impact_path.write_text(json.dumps(impact,indent=2)+'\n',encoding='utf-8')
 fs=files();payload=[{'path':n[len(REL)+1:],'bytes':(REPO/n).stat().st_size,'sha256':sha(REPO/n)} for n in fs if not n.endswith('/manifest.json')]
 manifest={'id':'native-rig-costumes-20261031','baseline':summary['baseline'],'scope':'Internal source-only two-costume shared-rig study; no external animation handoff','source_acceptance':'Existing wardrobe garments and original character sources retain their candidate/approved scopes; derivatives not preaccepted.','payload':payload,'sorted_payload_sha256':hashlib.sha256('\n'.join(f"{r['path']} {r['sha256']}" for r in payload).encode()).hexdigest(),'publication':summary['publication'],'acceptance':summary['acceptance'],'limits':'RGBA archives retain exact pixels, not original PNG container bytes. Raw PNG captures remain locally preserved in ignored paths. Native source images are retained unchanged.'}
 (ROOT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
 impact['files']=sorted(set(files()+root_files));impact_path.write_text(json.dumps(impact,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({'final_machine_pass':summary['final_machine_pass'],'files':len(fs),'payload_bytes':sum(r['bytes'] for r in payload),'max_file_bytes':max(r['bytes'] for r in payload)},indent=2))
if __name__=='__main__':main()
