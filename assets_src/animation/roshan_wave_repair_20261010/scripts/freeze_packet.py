"""Freeze literal packet bytes; this never edits raster pixels or accepts artwork."""
import argparse,datetime,hashlib,json,struct,subprocess
from pathlib import Path
from PIL import Image

parser=argparse.ArgumentParser()
parser.add_argument('--final',required=True,help='Final matte folder relative to packet')
parser.add_argument('--paint',required=True,help='Paint source folder relative to packet')
a=parser.parse_args()
packet=Path(__file__).resolve().parent.parent
repo=next(p for p in packet.parents if (p/'project.godot').is_file())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
final=(packet/a.final).resolve();paint=(packet/a.paint).resolve()
for p in [final,paint]:p.relative_to(packet)
assert (final/'frames/0040.png').is_file() and (paint/'0040.png').is_file()
k0=repo/'assets_src/animation/whole_sprite_pipeline_20261007/references/approved_K0.png'
entries=[]
excluded={'packet_manifest.json','remote_verification.json','remote_verification_receipt.json'}
for p in sorted(packet.rglob('*')):
 if not p.is_file() or (p.parent==packet and p.name in excluded) or '__pycache__' in p.parts or any(part.endswith('.tmp') for part in p.relative_to(packet).parts):continue
 rel=p.relative_to(packet).as_posix();media=p.suffix.lower() in {'.png','.gif','.webp','.mp4','.aseprite'}
 row={'path':p.relative_to(repo).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p),'role':'source_or_review_evidence' if media else 'workflow_or_provenance','acceptance_scope':'SOURCE_ONLY','dimensions':None,'license_provenance':'ASSET_LICENSES.md scoped roshan_wave_repair_20261010 rows; project-owned approved identity and declared local/builtin derivatives' if media else 'Project workflow/evidence; no artwork acceptance','modification_status':'Declared by bound derivation/recipe/receipt; preserved rejects remain rejected','source_identity_authority':{'path':k0.relative_to(repo).as_posix(),'sha256':sha(k0),'scope':'Identity authority, not a claim of direct pixel ancestry'}}
 if p.suffix.lower() in {'.png','.gif','.webp'}:
  with Image.open(p) as im:row['dimensions']=list(im.size)
 elif p.suffix.lower()=='.aseprite':
  with p.open('rb') as stream:header=stream.read(16)
  row['dimensions']=list(struct.unpack_from('<HH',header,8))
 elif p.suffix.lower()=='.mp4':
  probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=width,height','-of','json',str(p)],text=True,timeout=30))
  stream=probe['streams'][0];row['dimensions']=[stream['width'],stream['height']]
 if final in p.parents:
  row['candidate_record']=str((final/'verification.json').relative_to(repo)).replace('\\','/')
  if p.parent==final/'frames' and p.suffix=='.png' and p.stem.isdigit():
   n=int(p.stem);source=k0 if n in [0,40] else final/'native_rgba'/p.name
   row.update({'role':'complete_rgba_sprite_cel','index':n,'source_path':source.relative_to(repo).as_posix(),'source_sha256':sha(source),'modification_status':'Exact approved K0 PNG copy' if n in [0,40] else 'One uniform complete-frame resize0.3125 plus translation15,-10; no per-part transform'})
  elif p.parent==final/'native_rgba' and p.suffix=='.png' and p.stem.isdigit():
   n=int(p.stem);source=k0 if n in [0,40] else paint/p.name
   row.update({'role':'complete_native_rgba_cel','index':n,'source_path':source.relative_to(repo).as_posix(),'source_sha256':sha(source),'modification_status':'Declared whole-K0819x819 mapping[-48,32]' if n in [0,40] else 'Same-cel neutral-field/matte and boundary-only color recovery; source interior preservation checked'})
  elif p.parent in [final/'native_roundtrip/frames',final/'sprite_roundtrip/frames'] and p.suffix=='.png' and p.stem.isdigit():
   native=p.parent==final/'native_roundtrip/frames';source=final/('native_rgba' if native else 'frames')/p.name
   row.update({'role':'complete_rgba_master_roundtrip_cel','index':int(p.stem),'source_path':source.relative_to(repo).as_posix(),'source_sha256':sha(source),'modification_status':'Aseprite master reopen/export; exact RGBA pixel equality, no pixel transform; PNG encoding may differ'})
 if any(x in rel for x in ['contact','review/','on_black/','on_dark/','on_light/']):row['role']='review_only';row['pixel_input_allowed']=False
 if p.suffix.lower()=='.png' and '/guide_half/' in rel:
  row.update({'role':'historical_motion_control_with_appearance_contours','used_as_delivery_pixels':False,'appearance_authority':False,'position_guide_exception_eligible':False,'modification_status':'Exact historical rejected LTX structural-control contours contain face/hair/clothing design. Not POSITION_GUIDE_ONLY, not a current generation input or accepted delivery pixels; original workflow and receipt preserved.'})
 entries.append(row)
entries.sort(key=lambda e:e['path'].encode('utf-8'))
payload=''.join(f"{e['path']}\t{e['sha256']}\t{e['bytes']}\n" for e in entries).encode('utf-8')
external=[]
for rel in [
 'assets_src/animation/whole_sprite_pipeline_20261007/references/approved_K0.png',
 'assets_src/animation/whole_sprite_pipeline_20261007/references/approved_K2.png',
 'assets/characters/roshan_25d/roshan_gesture_a.png',
 'assets_src/cinematics/ltx25_union_trial_20261004/native_review.json',
 'assets_src/animation/whole_sprite_pipeline_20261007/catalog.json',
 'docs/handoffs/codex_roshan_wave_whole_sprites_2026-10-07/README.md',
 'docs/handoffs/codex_roshan_wave_whole_sprites_2026-10-07/tools/measure_wave.py',
 'tools/sprite_pipeline.py','tools/sprite_pipeline_bridge.lua','tools/ltx_wave_experiment.py',
 'design/animation/ANIMATION_PRODUCTION_PROTOCOL.md',
 'design/templates/ANIMATION_JOB_CARD_V1.md','ASSET_LICENSES.md']:
 p=repo/rel;data=p.read_bytes();published=subprocess.check_output(['git','show',':'+rel],cwd=repo)
 if published not in [data,data.replace(b'\r\n',b'\n')]:raise ValueError('Stage current external dependency before freeze: '+rel)
 external.append({'path':rel,'sha256':hashlib.sha256(published).hexdigest(),'bytes':len(published),
                  'local_literal_sha256':sha(p),'encoding':'Git index literal bytes; local literal hash recorded separately' if published==data else 'Git canonical text LF; local CRLF hash recorded separately',
                  'role':'required identity, specification or executable dependency; existing acceptance scope unchanged'})
record={'schema':'reef.whole-wave-packet.v1','frozen_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'repository':'https://github.com/Ebonyks/mermaid-roshan-reef','branch':'codex/roshan-wave-repair-20261010','recipient_access_mode':'anonymous public GitHub read','baseline':'245e9c543be771d297b60dafb91b8a3baf73e211','payload_hash_definition':'UTF8 sorted repository-relative path TAB literal SHA256 TAB byte-count LF; root manifest and root remote receipt excluded to avoid recursive self-hashes; nested frozen manifests included','payload_sha256':hashlib.sha256(payload).hexdigest(),'excluded_sidecars':sorted(excluded),'excluded_scratch_components':'Any path component ending .tmp; reproducibility scratch is Git-ignored and its exact duplicate canonical payload is bound by the public receipt','final_candidate':final.relative_to(repo).as_posix(),'paint_source':paint.relative_to(repo).as_posix(),'file_count':len(entries),'files':entries,'claims':{'ARCHIVE_COMPLETE':False,'archive_status':'HISTORICAL_PREPARATION_HELPER_GAP_PRESERVED','anonymous_transport':'PENDING_IMMUTABLE_REMOTE_BYTE_VERIFICATION','GENERATION_READY':'NOT_A_NEW_GENERATOR_JOB','DELIVERY_ACCEPTED':False,'runtime':'NOT_INTEGRATED','human_owner_device_child':'PENDING'}}
record['required_external_files']=external
record['known_archive_limits']=['Historical full06 preparation-helper bytes were not archived; its recorded hash and exact rendered Lua/profile/masks/source cels are preserved. Current archived reusable helper reproduces all41 native cels and reopened master exports byte/pixel exact; provenance/engine_profile_all41_reproduction.json binds that verification. See provenance/inspection_matte03/inspection_config.json.']
record['claims']['derivation_archive_complete']=False
(packet/'packet_manifest.json').write_text(json.dumps(record,indent=2,allow_nan=False)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({'files':len(entries),'bytes':sum(e['bytes'] for e in entries),'payload_sha256':record['payload_sha256']}))
