"""Verify published packet bytes, atlas states, and editable Aseprite exports."""
import argparse,hashlib,json,shutil,subprocess,tempfile
from pathlib import Path
from PIL import Image
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--packet',type=Path,default=Path(__file__).resolve().parents[1]);p.add_argument('--aseprite',default='C:/Program Files/Aseprite/Aseprite.exe');p.add_argument('--output',type=Path);args=p.parse_args()
 root=args.packet.resolve();manifest=json.loads((root/'manifest.json').read_text());rows=manifest['files']
 for row in rows:
  path=(root/row['path']).resolve();assert path.is_relative_to(root)
  assert path.stat().st_size==row['bytes'] and sha(path)==row['sha256'],row['path']
 payload=hashlib.sha256(''.join(r['path']+'\t'+r['sha256']+'\n' for r in sorted(rows,key=lambda r:r['path'])).encode()).hexdigest()
 assert payload==manifest['packet_payload_sha256']
 ase=args.aseprite if Path(args.aseprite).exists() else shutil.which('aseprite');assert ase,'Aseprite executable required for editable-master verification'
 checked=[]
 with tempfile.TemporaryDirectory(prefix='sky_packet_verify_') as scratch:
  scratch=Path(scratch).resolve()
  for item in manifest['objects']:
   outputs=item['reference_outputs'];sheet=Image.open(root/outputs['atlas']).convert('RGBA');data=json.loads((root/outputs['timing']).read_text())
   assert sheet.size==(2048,1024) and len(data['frames'])==32
   for n,state in enumerate(data['frames']):
    f=state['frame'];pose=sheet.crop((f['x'],f['y'],f['x']+f['w'],f['y']+f['h'])).resize((256,256))
    assert hashlib.sha256(pose.tobytes()).hexdigest()==item['state_rgba_sha256'][n],(item['id'],n,'atlas state')
   target=scratch/item['id'];target.mkdir()
   subprocess.run([ase,'--batch',str(root/outputs['master']),'--save-as',str(target/'pose{frame}.png')],capture_output=True,check=True)
   paths=sorted(target.glob('pose*.png'),key=lambda p:int(p.stem.replace('pose','')));assert len(paths)==32
   for n,path in enumerate(paths):assert hashlib.sha256(Image.open(path).convert('RGBA').tobytes()).hexdigest()==item['state_rgba_sha256'][n],(item['id'],n,'editable state')
   checked.append(item['id']);print(item['id']+' payload, atlas and editable states PASS',flush=True)
  # TemporaryDirectory removes only its own verified, explicitly named scratch tree.
  assert scratch.name.startswith('sky_packet_verify_')
 result={'status':'PASS','payload_files':len(rows),'objects':checked,'editable_states':320,'payload_sha256':payload,'claim':'Byte integrity and exact editable raster states; reference-only, no creative/runtime/cinematic acceptance.'}
 if args.output:args.output.write_text(json.dumps(result,indent=2),encoding='utf-8')
 print('PACKET BYTES AND 320 EDITABLE RASTER STATES: ALL OK')
if __name__=='__main__':main()
