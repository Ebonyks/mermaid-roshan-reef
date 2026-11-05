"""Hash the self-contained source review packet and its exact helper inputs."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess

ROOT=Path(__file__).resolve().parents[1]
REPO=ROOT.parents[2]


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--staged',action='store_true',help='Hash exact staged Git blobs, including normal root text EOL normalization')
    args=parser.parse_args()
    prefix=ROOT.relative_to(REPO).as_posix()
    paths=subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard','--',prefix],cwd=REPO,text=True,encoding='utf-8').splitlines()
    paths += ['tools/prepare_costume_skin.py','tools/validate_costume_skin.py','tools/tests/test_costume_skin_binding.py',
              'tools/resolve_godot.py','tools/audit_godot_baseline.py','tools/godot_baseline.json',
              'design/animation/skin_binding/rig_binding.schema.json','design/animation/skin_binding/skin_package.schema.json',
              'design/animation/skin_binding/attachment_mesh.schema.json','design/animation/skin_binding/skin.recipe.template.json',
              'ASSET_LICENSES.md','design/audit_impacts/shared-roshan-skin-swim-20261101.json']
    target=ROOT/'manifest.json'
    paths=sorted(set(p for p in paths if p!=target.relative_to(REPO).as_posix()))
    files=[]
    batch=subprocess.Popen(['git','cat-file','--batch'],cwd=REPO,stdin=subprocess.PIPE,stdout=subprocess.PIPE) if args.staged else None
    for name in paths:
        file=REPO/name
        assert file.is_file(),name
        if batch:
            batch.stdin.write((':'+name+'\n').encode());batch.stdin.flush()
            header=batch.stdout.readline().split()
            assert len(header)==3 and header[1]==b'blob',name
            size=int(header[2]);remaining=size;digest=hashlib.sha256()
            while remaining:
                chunk=batch.stdout.read(min(1024*1024,remaining));assert chunk,name
                digest.update(chunk);remaining-=len(chunk)
            assert batch.stdout.read(1)==b'\n'
            files.append({'path':name,'bytes':size,'sha256':digest.hexdigest()})
        else:
            files.append({'path':name,'bytes':file.stat().st_size,'sha256':hashlib.sha256(file.read_bytes()).hexdigest()})
    if batch:
        batch.stdin.close();assert batch.wait(timeout=20)==0
    payload=''.join(f"{f['path']}\0{f['bytes']}\0{f['sha256']}\n" for f in files).encode()
    manifest={'format':'roshan.shared-native-skin-review/1','task':'shared-roshan-skin-swim-20261101',
              'repository':'https://github.com/Ebonyks/mermaid-roshan-reef',
              'branch':'codex/shared-roshan-skin-swim-20261101','baseline':'27c88288bf6e39582072811443df79919e7bbb89',
              'entry':prefix+'/README.txt','required_files':files,'payload_sha256':hashlib.sha256(payload).hexdigest(),
              'payload_hash_rule':'Sorted repository-relative path NUL decimal byte count NUL lowercase SHA-256 LF; manifest excluded from its own payload hash.',
              'byte_scope':'Exact staged Git blob bytes. Packet .gitattributes preserves raw source/art/evidence; normal root text EOL normalization is included.' if args.staged else 'Working bytes; rebuild with --staged before publication.',
              'claim':'SOURCE_REVIEW_PACKET; one common actor and two data-only skins. See exact evidence/result_summary.json.',
              'generation_ready':'NOT_APPLICABLE: no external generator jobs commissioned by this packet',
              'delivery_accepted':False,'production_accepted':False,
              'master_audit_writeback_authorized':False,'master_audit_changed':False,
              'acceptance_limits':'Machine checks and a source archive do not accept identity/style/natural movement, fin interpolation, actual device, child/owner or production integration. Historical failed stages remain rejected.'}
    target.write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8',newline='\n')
    print('PACKET_HASHED',len(files),sum(x['bytes'] for x in files),'bytes',manifest['payload_sha256'],flush=True)


if __name__=='__main__':main()
