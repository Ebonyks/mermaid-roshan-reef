"""Keep this study's exact file coverage, derivative licenses and packet hashes current."""
from pathlib import Path
import datetime,hashlib,json,subprocess,sys

ROOT=Path(__file__).resolve().parents[1]
REPO=ROOT.parents[2]
PREFIX=ROOT.relative_to(REPO).as_posix()


def payload():
    names=subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard','--',PREFIX],cwd=REPO,text=True).splitlines()
    return sorted({REPO/n for n in names if (REPO/n).is_file()})


def main():
    files=payload()
    media=[p for p in files if p.suffix.lower() in {'.png','.jpg','.mp4','.mkv','.aseprite'}]
    license_path=REPO/'ASSET_LICENSES.md'
    text=license_path.read_text(encoding='utf-8')
    start='<!-- LAURA_SWIM_TEST_20261101 -->';end='<!-- LAURA_SWIM_TEST_20261101_END -->'
    block=start+'\n\n### Laura-led swimming costume test (source candidates)\n\n| Asset | Source, rights and modifications |\n|---|---|\n'
    for p in media:
        name=p.relative_to(REPO).as_posix()
        source='Project-owned native outfit study derivative; original dependency path/hash and resource-only edits are in sources.json. Existing provisional/rejected status retained; no identity/art acceptance.' if '/sources/' in name else 'Project-owned actual Godot4.7.2 Mobile capture derivative of the frozen sources and common authored motion. QA composition, lossless RGB/alpha archive, editable RGBA Aseprite loop or review encoding. No new generated appearance, no source video pixels, no production/human/device/child/owner acceptance.'
        block+='| `'+name+'` | '+source+' |\n'
    block+=end
    if start in text:
        a=text.index(start);b=text.index(end,a)+len(end);text=text[:a]+block+text[b:]
    else:
        text+='\n\n'+block+'\n'
    license_path.write_text(text,encoding='utf-8',newline='\n')
    impact_path=REPO/'design/audit_impacts/laura-swim-test-20261101.json'
    impact=json.loads(impact_path.read_text(encoding='utf-8'))
    changed=subprocess.check_output(['git','diff','--name-only',impact['baseline']],cwd=REPO,text=True).splitlines()
    new=subprocess.check_output(['git','ls-files','--others','--exclude-standard'],cwd=REPO,text=True).splitlines()
    planned=['evidence/project_ci.log','evidence/project_ci.err','evidence/project_ci_receipt.json','evidence/swim_audit.json','evidence/swim_audit_surface.json','evidence/native_archives.json','evidence/aseprite_roundtrip.json','evidence/review_mapping.json','evidence/final_summary.json','manifest.json']
    groups=json.loads((ROOT/'sources.json').read_text())['groups']
    for group in groups:
        for theme in group['themes']:
            planned+=['masters/'+theme+'.aseprite']
            for directory in ['costumes','costumes_surface']:
                planned+=['evidence/'+directory+'/'+theme+'.json','evidence/'+directory+'/'+theme+'_frame_hashes.json']
            for clip in ['loop','travel']:
                planned+=['archives/'+theme+'/'+clip+suffix for suffix in ['_rgb.mkv','_alpha.mkv','_receipt.json']]
    planned=[PREFIX+'/'+n for n in planned]
    impact['files']=sorted(set(changed+new+planned)-{impact_path.relative_to(REPO).as_posix()})
    if (ROOT/'evidence/swim_audit_surface.json').exists():
        result=json.loads((ROOT/'evidence/swim_audit_surface.json').read_text())
        impact['validation'][0]={'command':'Actual isolated-material native geometry plus original contour/motion floors across4352 frames','result':'PASS' if result['all_machine_checks_pass'] else 'FAIL','evidence':PREFIX+'/evidence/swim_audit_surface.json'}
    if (ROOT/'evidence/final_gate_receipt.json').exists():
        result=json.loads((ROOT/'evidence/final_gate_receipt.json').read_text())
        impact['validation'][1]['result']='PASS' if result['required_gate_coverage_pass'] else 'FAIL'
    elif (ROOT/'evidence/project_ci_receipt.json').exists():
        result=json.loads((ROOT/'evidence/project_ci_receipt.json').read_text())
        impact['validation'][1]['result']='PASS' if result['exit']==0 else 'FAIL'
    impact_path.write_text(json.dumps(impact,indent=2)+'\n',encoding='utf-8',newline='\n')
    if '--coverage-only' not in sys.argv:
        files=[p for p in payload() if p!=ROOT/'manifest.json']
        rows=[{'path':p.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size} for p in files]
        assert all(r['bytes']<100*1048576 for r in rows)
        support_names=['ASSET_LICENSES.md','audit/MASTER_AUDIT_2026-08-09.md','design/05_DOC_LEDGER.md','design/reference/owner_decisions.json','design/reference/OWNER_DECISIONS.md','design/audit_impacts/laura-swim-test-20261101.json','design/animation/COSTUME_SKIN_CONVERSION_GUIDE.md','tools/prepare_costume_skin.py','tools/validate_costume_skin.py','tools/tests/test_costume_skin_binding.py']
        support_names += [p.relative_to(REPO).as_posix() for p in (REPO/'design/animation/skin_binding').glob('*.json')]
        support=[{'path':name,'sha256':hashlib.sha256((REPO/name).read_bytes()).hexdigest(),'bytes':(REPO/name).stat().st_size} for name in sorted(support_names)]
        manifest={'schema':1,'status':'OWNER_REJECTED_MULTI_BUILDER_DIAGNOSTIC_WITH_PROPOSED_CONVERSION_GUIDE','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':rows,'repository_support_files':support,'payload_sorted_sha256':hashlib.sha256(json.dumps(rows,sort_keys=True,separators=(',',':')).encode()).hexdigest(),'support_sorted_sha256':hashlib.sha256(json.dumps(support,sort_keys=True,separators=(',',':')).encode()).hexdigest(),'GENERATION_READY':False,'DELIVERY_ACCEPTED':False,'ARCHIVE_COMPLETE':'PENDING_PUBLICATION_AND_REMOTE_VERIFICATION','production_integration':False}
        (ROOT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8',newline='\n')
    print('REFRESHED_STUDY_COVERAGE',len(impact['files']),'media',len(media),flush=True)


if __name__=='__main__':main()
