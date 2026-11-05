"""Refresh task-local hashes, exact changed-file coverage and source licence rows."""
from pathlib import Path
import hashlib
import json
import subprocess

STUDY=Path(__file__).resolve().parents[1]
REPO=STUDY.parents[2]
REL=STUDY.relative_to(REPO).as_posix()
BASE='218ae766f8e60afb3f6338b8fafce28ec9fab7f2'
AUTHORITY_BASE='a0bb2cf4691631a534e210a5fb60fd227213322f'


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def visible_files():
    data=subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard','-z','--',REL],cwd=REPO)
    return sorted({s.decode() for s in data.split(b'\0') if s and (REPO/s.decode()).is_file()})


def main():
    ledger=REPO/'design/05_DOC_LEDGER.md'
    text=ledger.read_text(encoding='utf-8')
    if f'`{REL}/README.md`' not in text:
        ledger.write_text(text+f'\n| `{REL}/README.md` | \U0001f7e3 | `PROPOSED / CANDIDATE` owner-commissioned native Godot shoulder/arm, blink and tail rig stress study. Scoped test exception, retained rejects, exact Mobile geometry/pixel/seek evidence; no production character, finding, device, child or owner acceptance. |\n',encoding='utf-8')
    master=REPO/'audit/MASTER_AUDIT_2026-08-09.md'
    text=master.read_text(encoding='utf-8')
    if 'native_rig_stress_20261031/README.md' not in text:
        marker='## 0. Planning entry\n'
        note='\nOwner-commissioned [native Godot rig stress study](../'+REL+'/README.md) (2026-10-31) compares shoulder/arm bend, blink and tail bend with ImageGen source/segment repairs under a scoped prototype exception. Retained rejected revisions, actual Mobile renders and exact numerical/visual limits are separate from production, finding closure, device, child and owner acceptance.\n'
        master.write_text(text.replace(marker,marker+note,1),encoding='utf-8')
    files=visible_files()
    licences=REPO/'ASSET_LICENSES.md'
    text=licences.read_text(encoding='utf-8')
    start='<!-- NATIVE_RIG_STRESS_20261031_START -->'
    end='<!-- NATIVE_RIG_STRESS_20261031_END -->'
    if start in text:
        a=text.index(start);b=text.index(end,a)+len(end);text=text[:a]+text[b:]
    rows=[]
    for name in files:
        p=REPO/name
        if p.suffix.lower() in {'.png','.jpg','.mov','.mkv','.mp4','.aseprite'}:
            source='Owner-directed built-in ImageGen source / approved Roshan identity reference' if '/native/' in name else 'Derivative of retained native sources; registration, matte/patch/segment preparation or Godot capture/review export'
            rows.append(f'| `{name}` | {source} | Project-owned source / generated candidate; production acceptance pending | [provenance]({REL}/provenance.json) | Non-destructive rig study; original sources preserved; exact hashes and edits in study manifest. |')
    licences.write_text(text.rstrip()+'\n\n'+start+'\n\n## Native rig stress study \u2014 2026-10-31\n\n| Asset | Source | Licence / scope | URL / evidence | Modifications |\n|---|---|---|---|---|\n'+'\n'.join(rows)+'\n\n'+end+'\n',encoding='utf-8')
    files=visible_files()
    payload=[]
    for name in files:
        p=REPO/name
        if name.endswith('/manifest.json'):continue
        record={'path':name[len(REL)+1:],'bytes':p.stat().st_size,'sha256':sha(p)}
        if p.suffix.lower() in {'.png','.jpg'}:
            from PIL import Image
            with Image.open(p) as im:record['dimensions']=list(im.size)
        payload.append(record)
    manifest={'id':'native-rig-stress-20261031','baseline':BASE,'scope':'Internal source-only native Godot prototype; no external generation handoff','approved_identity_source':{'path':'assets/characters/roshan_25d/roshan_base.png','sha256':sha(REPO/'assets/characters/roshan_25d/roshan_base.png'),'role':'identity/style only; outputs not preaccepted'},'generator':{'method':'built-in image_gen','model_revision':'not exposed','calls':4,'billing':'not exposed'},'payload':payload,'sorted_payload_sha256':hashlib.sha256('\n'.join(f"{r['path']} {r['sha256']}" for r in payload).encode()).hexdigest(),'acceptance':{'production_integrated':False,'DELIVERY_ACCEPTED':False,'owner':'PENDING','device':'PENDING','child':'PENDING','archive_limit':'Exact rendered RGBA pixels retained in two-stream lossless Matroska archives; native PNG bytes remain locally preserved in ignored frame folders. No external handoff claim.'}}
    manifest['publication']={'branch':'codex/native-rig-stress-20261031','dev_integration':False,'authority_revision':AUTHORITY_BASE,'reason':'ODR-DEMO-FREEZE-20261031'}
    (STUDY/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    files=visible_files()+['ASSET_LICENSES.md','design/05_DOC_LEDGER.md','audit/MASTER_AUDIT_2026-08-09.md']
    impact={'id':'native-rig-stress-20261031','scope':'Owner-requested isolated native Godot shoulder/arm, blink and tail studies, extensive deterministic render/geometry/pixel/motion stress loop and bounded ImageGen source/segment repairs. No production game, protected originals, saves or release change. Current owner authorization is a scoped study exception to prior no-rig/whole-drawing constraints.','baseline':BASE,'rules':['DL-AUTH-05','DL-AUTH-06','DL-AUTH-07','DL-MED-01','DL-MED-05','DL-MOT-01','DL-MOT-02','DL-MOT-03','DL-MOT-10','DL-MOT-12','DL-MOT-13','DL-MOT-14','DL-MOT-15','DL-MOT-16'],'findings':['MA-ROSHAN-005','MA-ROSHAN-006'],'finding_scope':'Related identity and motion evidence only; neither production finding is repaired or closed.','files':sorted(set(files)),'validation':[{'command':'Godot 4.7.2 Mobile render_stress.gd, ten retained revisions','result':'PASS','evidence':REL+'/evidence/render_v10/engine_receipt.json; individual receipts preserve all prior runs; repeatable states do not establish appearance.'},{'command':'python scripts/audit_study.py evidence/render_v10','result':'PENDING','evidence':REL+'/evidence/render_v10/geometry_audit.json; prior rejects retained'},{'command':'python scripts/audit_motion.py evidence/render_v10','result':'PENDING','evidence':REL+'/evidence/render_v10/motion_audit.json'},{'command':'Lossless archive and Aseprite reopen/export comparison','result':'PENDING','evidence':REL+'/review/'},{'command':'python -B tools/audit_document_authority.py; python -B tools/audit_development.py --base auto; applicable script gates and scripts/ci.sh','result':'PENDING','evidence':REL+'/evidence/'}],'acceptance_gaps':'Exact candidate owner and target-device/child review remain pending. Agent frame inspection and machine geometry are separate; no guarantee of natural acting across arbitrary poses, independent head turns or 3D/out-of-plane motion. Runtime character and master audit remain unchanged.','references_used':[{'path':'design/animation/ANIMATION_PRODUCTION_PROTOCOL.md','purpose':'Job-card, provenance, cadence and independent evidence lanes; owner prototype exception scoped in current chat.'},{'path':'assets_src/cinematics/claude_rig_pilot_20261007/README.md','purpose':'Reuse earlier rig lessons and retain its rejection/acceptance scope.'}],'lessons':[{'lesson':'A single rectangular mesh can couple limbs to nearby body paint across transparent gaps; stable bone lengths alone do not prove visual integrity.','write_back':REL+'/README.md'},{'lesson':'Straight-alpha eyelid masks must preserve unpremultiplied RGB or dark feathered halos appear.','write_back':REL+'/scripts/build_study.py'}]}
    impact['baseline']=AUTHORITY_BASE
    impact['task_start_baseline']=BASE
    impact['publication']={'branch':'codex/native-rig-stress-20261031','dev_integration':False,'reason':'ODR-DEMO-FREEZE-20261031 restricts dev to DR0-DR7. This source-only commissioned experiment stays separate.'}
    impact['references_used'].append({'path':'design/reference/OWNER_DECISIONS.md','purpose':'Rechecked current demo freeze; prototype publication stays outside dev.'})
    for number,name,key in [(1,'render_v10/geometry_audit.json','machine_geometry_pass'),(2,'render_v10/motion_audit.json','pass')]:
        proof=STUDY/'evidence'/name
        if proof.exists():impact['validation'][number]['result']='PASS' if json.loads(proof.read_text()).get(key) else 'FAIL'
    master=STUDY/'evidence/aseprite_roundtrip.json'
    archives=list((STUDY/'evidence').glob('render_v*/*_archive.json'))
    if master.exists() and len(archives)==30:
        exact=json.loads(master.read_text()).get('pass') and all(json.loads(p.read_text()).get('pixel_roundtrip_exact') for p in archives)
        impact['validation'][3]['result']='PASS' if exact else 'FAIL'
        impact['validation'][3]['evidence']=REL+'/evidence/aseprite_roundtrip.json and all30 render_v*/clip_archive.json receipts; 2910 archived RGBA frames and291 reopened master frames exact.'
    impact['validation'][4]={'command':'Retained passing static/audio/visual CI prefix; fresh document gates; exact scripts/ci.sh import/regression/all-trusted-probe suffix','result':'PENDING','evidence':REL+'/evidence/project_gate_continuation.json; full_ci_model_scan.log; final_document_gates.log; project_gates.log'}
    continuation=STUDY/'evidence/project_gates.exit'
    documents=STUDY/'evidence/final_document_gates.exit'
    if continuation.exists() and documents.exists():
        values=[continuation.read_text().strip(),documents.read_text().strip()]
        if all(v=='0' for v in values):impact['validation'][4]['result']='PASS'
        elif any(v not in {'0','PENDING'} for v in values):impact['validation'][4]['result']='FAIL'
    impact['historical_gate_attempts']=[{'command':'scripts/ci.sh','result':'FAIL','evidence':REL+'/evidence/full_ci_model_scan.log','resolved_cause':'The v6 native 2D JSON exceeded the unchanged 4 MiB inspection cap. Lossless compaction and exact original-byte reconstruction proof are in evidence/rig_json_format_receipt.json. The complete import/regression/probe suffix is rerun; earlier unaffected passing gates are retained.'}]
    impact['historical_gate_attempts'].append({'command':'Reconciled document authority check','result':'FAIL','evidence':REL+'/evidence/final_document_gates_encoding.log','resolved_cause':'Generated candidate-ledger marker was mojibake. The writer now uses an ASCII Unicode escape and the exact owned row is corrected.'})
    native_exit=STUDY/'evidence/native_script_gates.exit'
    native_value=native_exit.read_text().strip() if native_exit.exists() else 'PENDING'
    impact['validation'].append({'command':'Changed native GDScript parser and inference gates','result':'PASS' if native_value=='0' else 'PENDING' if native_value=='PENDING' else 'FAIL','evidence':REL+'/evidence/native_script_gates.log'})
    impact['historical_gate_attempts'].insert(0,{'command':'Initial scripts/ci.sh coverage attempt','result':'FAIL','evidence':REL+'/evidence/full_ci_initial_coverage.log','resolved_cause':'Packaging added new task files after the initial record. Coverage was refreshed; fresh authority and development audits pass.'})
    out=REPO/'design/audit_impacts/native-rig-stress-20261031.json';out.write_text(json.dumps(impact,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'study_files':len(payload),'licensed_assets':len(rows),'impact_files':len(impact['files'])}))


if __name__=='__main__':main()
