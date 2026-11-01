from pathlib import Path
import json,hashlib,subprocess,datetime
from PIL import Image
R=Path(__file__).resolve().parents[1];REPO=R.parents[2]
EXCLUDED={'manifest.json','evidence/remote_verification.json','evidence/publication_receipt.json','evidence/remote_ci.json','evidence/manifest_check.log','evidence/handoff_status.json'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    asset_map={x['path']:x for x in json.loads((R/'asset_manifest.json').read_text())['assets']}
    names=set()
    for args in [['git','ls-files','--',str(R.relative_to(REPO))],['git','ls-files','--others','--exclude-standard','--',str(R.relative_to(REPO))]]:
        names.update(subprocess.run(args,cwd=REPO,capture_output=True,text=True,check=True).stdout.splitlines())
    rows=[]
    for name in sorted(names):
        p=REPO/name;relative=p.relative_to(R).as_posix()
        if relative in EXCLUDED:continue
        item={'path':name,'package_path':relative,'sha256':sha(p),'bytes':p.stat().st_size,'role':'source program, reference or audit evidence','source_path':'Project-authored review packet; derivation links in provenance.json and source_inventory.json','license_provenance':'Existing project artwork/code or built-in ImageGen prototype source; ASSET_LICENSES.md and asset_manifest.json','modification_status':'New source-only review path; protected originals untouched','dimensions_px':None}
        if name in asset_map:
            a=asset_map[name];item.update(role=a['role'],source_path=a['provenance'],license_provenance=a['license'],modification_status=a['modification_status'])
        if p.suffix.lower() in ['.png','.jpg','.jpeg']:item['dimensions_px']=list(Image.open(p).size)
        elif p.suffix.lower()=='.aseprite':item['dimensions_px']=[1024,1024]
        elif p.suffix.lower()=='.mp4':item['dimensions_px']=[1280,720]
        elif p.suffix.lower()=='.zip':item['dimensions_px']=[1024,1024];item['role']='Literal actual Godot native-frame archive; per-frame hashes inside'
        rows.append(item)
    payload=''.join(x['path']+'\0'+x['sha256']+'\n' for x in rows).encode()
    manifest={'schema_version':1,'id':'roshan-job-rig-investigation-20261101','scope':'SOURCE_ONLY_REVIEW_DRAFT; preferredv6, not an accepted wardrobe/animation or production integration','repository':'Ebonyks/mermaid-roshan-reef','branch':'codex/roshan-rig-investigation-20261101','baseline':'f59a1d1d5bdd58604f4706d16fb4e76d8f7db8b9','corrected_seed_revision':'b700b846d1d2f4b1843279f268e2bb12e4b1f4ec','shared_contract':{'version':'1.0.0','sha256':sha(R/'contract/rig_v1.json'),'scope':'Copied provisional frozen upstream snapshot; sole shared owner has not published its official packet. No compatibility signoff.'},'files':rows,'sorted_packet_payload_sha256':hashlib.sha256(payload).hexdigest(),'payload_hash_recipe':'UTF8 sorted repo-relative path + NUL + literal file SHA256 + LF; exclude manifest/self-referential publication receipts','metadata_files_outside_payload_hash':sorted(EXCLUDED),'ARCHIVE_COMPLETE':'See remote_verification.json; local paths are staging until immutable remote byte verification','GENERATION_READY':False,'DELIVERY_ACCEPTED':False,'COMPATIBILITY_ACCEPTED':False,'quality_blockers':['Strict continuity floors still fail in preferred complete-set arm/tail captures.',str(json.loads((R/'evidence/mixed_outline.json').read_text())['fit_failing_snapshots'])+'of250 mixed rest/arm snapshots fail despite zero fresh/live mismatch.','Full-speed player review was blocked by computer-use app approval timeout; exact human/device/child/owner acceptance pending.'],'frame_authority':'exports/*.zip are literal native PNG bytes; review MP4s are uniformly scaled silent diagnostics. APNG alpha-changing export was rejected.','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    (R/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print('MANIFEST',len(rows),sum(x['bytes'] for x in rows),manifest['sorted_packet_payload_sha256'])
if __name__=='__main__':main()
