"""Freeze the exact review payload after local evidence is complete."""
from pathlib import Path
import hashlib,json
from PIL import Image
P=Path(__file__).resolve().parent
ROOT=P.parents[2]
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def build():
 source='assets_src/sky_lagoon/masters/sky_lagoon_panorama_master_v5_hd_3x1.png'
 deriv=json.loads((P/'derivation.json').read_text(encoding='utf-8'))
 entries=[]
 for f in sorted(P.rglob('*')):
  if not f.is_file() or f.name=='manifest.json' or f.suffix=='.uid':continue
  rel=f.relative_to(P)
  if any(part in {'.godot','frames','roundtrip','capture_frames','__pycache__'} for part in rel.parts):continue
  name=rel.as_posix();role='workflow_or_documentation';mod='Workflow, settings or evidence; no appearance input'
  if name.startswith('sources/') or (name.startswith('demo_project/patches/') and not name.endswith('_field.png')):
   role='exact_original_appearance_crop';mod='Lossless512-square crop at job-card native coordinates; no repaint'
  elif name.startswith('fields/') or name.endswith('_field.png'):
   role='data_motion_field';mod='Hand-bounded original flower selections and authored stems, rooted grayscale field; data only, not appearance pixels'
  elif name.startswith('demo_project/background/') and f.suffix=='.png':
   role='static_original_tile_derivative';mod='Native1024-square v5 tile; clears replacement-window interiors, with1px boundary sampling underlap'
  elif f.suffix=='.aseprite':
   role='editable_complete_frame_master';mod='60whole-context source-derived RGBA frames,33/33/34ms timing; no separately moving sprite pieces'
  elif f.suffix=='.gif':
   role='review_animation';mod='Original source-pixel deformation; fixed palette256 colours,60timed frames/2000ms, no dithering'
  elif name.startswith('evidence/mobile') and f.suffix=='.png':
   role='actual_desktop_mobile_capture';mod='Exact native-engine screenshot; not generation reference or device-performance evidence'
  elif f.suffix=='.png':
   role='source_or_motion_review_image';mod='Source downsample, target annotation, mask overlay, frame-step sheet or rejected numerical difference; not generation pixels'
  entry={'path':name,'bytes':f.stat().st_size,'sha256':sha(f),'role':role,'source_path':source,'rights':'Project-original derivative, inherits existing v5 provenance and ASSET_LICENSES.md attribution','modifications':mod,'used_as_generation_pixels':False}
  if f.suffix in {'.png','.gif'}:
   with Image.open(f) as im:entry['dimensions']=list(im.size)
  elif f.suffix=='.aseprite':entry['dimensions']=[512,512];entry['frames']=60
  entries.append(entry)
 payload=''.join(f"{e['path']}\0{e['sha256']}\0{e['bytes']}\n" for e in entries).encode('utf-8')
 manifest={'schema':'sky_lagoon_original_art_motion/1','date':'2026-11-05','scope':'SOURCE_ONLY_REVIEW','appearance_inputs':[deriv['source']],'position_guides':[],'files':entries,'packet_payload_sha256':hashlib.sha256(payload).hexdigest(),'payload_hash_method':'Sorted relative-path NUL SHA256 NUL byte-count LF, UTF8. Excludes manifest itself and ignored reproducible frames/caches.','claims':deriv['claims']}
 (P/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
 print(f"Frozen {len(entries)} files, {sum(e['bytes'] for e in entries)} bytes, payload {manifest['packet_payload_sha256']}")
if __name__=='__main__':build()
