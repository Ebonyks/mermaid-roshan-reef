"""Inventory real artifacts only; never create future output placeholders."""
from pathlib import Path
import json,hashlib,subprocess,struct
from PIL import Image
p=Path(__file__).resolve().parents[1];r=p.parents[2]
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
media={'.png','.apng','.mp4','.webm','.gif','.aseprite'}
previous=p.parent/'ltx_registered_wave_20261004';old=json.loads((previous/'manifest.json').read_text());old_by_sha={}
for row in old['payload']:old_by_sha.setdefault(row['sha256'],[]).append((previous/row['path']).relative_to(r).as_posix())

license_path=r/'ASSET_LICENSES.md';text=license_path.read_text(encoding='utf-8');marker='\n## Whole-figure Aseprite retake trial — 2026-10-04\n'
if marker in text:text=text[:text.index(marker)]
rows=[];payload=[]
for f in sorted(p.rglob('*')):
 if not f.is_file() or f.name in ['manifest.json','remote_verification.json','remote_receipt_publication.json']:continue
 rel=f.relative_to(p).as_posix();repo=f.relative_to(r).as_posix()
 item={'path':rel,'sha256':sha(f),'bytes':f.stat().st_size,'acceptance':'SOURCE_ONLY; owner/device/child acceptance absent'}
 if '/native_frames/' in rel:role='unmodified_model_output';mod='Native generated complete frame; PNG bytes preserved.'
 elif '/assembled_frames/' in rel:role='review_splice_complete_frame';mod='Whole-frame contiguous window replacement; original byte-preserved outside 41–63, see verification.'
 elif '/normalized_frames/' in rel:role='whole_canvas_preview_normalization';mod='Aseprite complete-canvas bilinear preview upscaling; native retained, not quality repair.'
 elif rel.startswith('inputs/source_frames/') or rel in ['inputs/original_0040.png','inputs/original_0048.png','inputs/original_0064.png','inputs/approved_figure_key_03.png']:role='source_reference_copy';mod='Byte copy of prior packet; approved identity reference or rejected original motion as declared.'
 elif rel=='inputs/corrected_0048_native.png':role='imagegen_whole_figure_key';mod='One complete-figure ImageGen redraw; owner identity review pending; see exact prompt receipt.'
 elif rel.startswith('inputs/'):role='editable_guide_or_lossless_input_derivative';mod='Aseprite normalization/export/master or source APNG/mask; complete guide pixels, no isolated-limb overlay.'
 elif f.suffix.lower()=='.aseprite':role='editable_native_inspection_master';mod='Native generated frames visible; original and guide layers hidden, whole-canvas scaled if dimensions differ.'
 elif f.suffix.lower() in media:role='reference_review_preview';mod='Whole-figure contact/encoded preview; no interpolation or frame-repair masking.'
 else:role='workflow_or_evidence';mod='Source-side workflow, settings or actual evidence; no delivery pixel authority.'
 item.update(role=role,modification_status=mod)
 parents=old_by_sha.get(item['sha256'],[])[:4]
 if not parents:
  if rel=='inputs/corrected_0048_native.png':parents=[(p/'inputs'/x).relative_to(r).as_posix() for x in ['original_0048.png','approved_figure_key_03.png','original_0040.png','original_0064.png']]
  elif rel.startswith('inputs/corrected_0048') or rel=='inputs/guide_mid.png':parents=[(p/'inputs/corrected_0048_native.png').relative_to(r).as_posix()]
  elif rel.startswith('inputs/tagged_exports/'):parents=[(p/'inputs/repair_keys.aseprite').relative_to(r).as_posix()]
  elif rel.startswith('results/'):
   take=rel.split('/')[1];base=p/'results'/take
   if '/assembled_frames/' in rel:
    idx=int(f.stem);local=idx-40;replacement=41<=idx<=63;folder='normalized_frames' if (base/'normalized_frames').exists() else 'native_frames'
    parents=[((base/folder/f'{local:04d}.png') if replacement else (previous/f'results/figure_wide_slow/native_frames/{idx:04d}.png')).relative_to(r).as_posix()]
   elif '/normalized_frames/' in rel:parents=[(base/'native_frames'/f.name).relative_to(r).as_posix()]
   elif '/native_frames/' in rel:
    parents=[(p/'inputs'/x).relative_to(r).as_posix() for x in ['original_0040.png','corrected_0048.png','original_0064.png']]
    if take.startswith('ltx23'):parents.append((p/'inputs/source_window.apng').relative_to(r).as_posix())
    item['generation_record']=(base/'receipt.json').relative_to(r).as_posix();item['workflow_record']=(base/'workflow.api.json').relative_to(r).as_posix()
   elif f.name=='repair_window.aseprite':parents=[(base/f'native_frames/{i:04d}.png').relative_to(r).as_posix() for i in range(25)]+[(p/'inputs/source_window.apng').relative_to(r).as_posix(),(p/'inputs/repair_keys.aseprite').relative_to(r).as_posix()]
   elif f.name=='normalized_window.aseprite':parents=[(base/'repair_window.aseprite').relative_to(r).as_posix()]
   elif f.name in ['receipt.json','history.json']:parents=[(base/'workflow.api.json').relative_to(r).as_posix()]
   elif f.name=='workflow.api.json':parents=[(p/'briefs/job_card.json').relative_to(r).as_posix()]
   else:parents=[(base/'receipt.json').relative_to(r).as_posix()]
  elif rel=='comparison/completed_takes.mp4':parents=[(previous/'results/figure_wide_slow/preview.mp4').relative_to(r).as_posix()]+[(p/'results'/x/'assembled.mp4').relative_to(r).as_posix() for x in ['ltxv_guide_standard','ltxv_guide_strong','ltx23_retake_lowmem']]
 item['source_paths']=parents
 item['source_sha256']={path:sha(r/path) for path in parents if (r/path).is_file()}
 item['source_authority']='Owner2026-10-04 trial; baseline/actual native receipts. Source references and generated guide acceptance retain their separate recorded scope.'
 item.setdefault('license_provenance','Project-authored source/evidence or retained publisher metadata/license notice; model weights not included.')
 if f.suffix.lower() in ['.png','.apng','.gif']:
  with Image.open(f) as im:item.update(dimensions=list(im.size),mode=im.mode,frames=getattr(im,'n_frames',1))
 if f.suffix.lower() in ['.mp4','.webm']:
  ffprobe=r'C:\Users\Peter\AppData\Local\Programs\MermaidReefTools\FFmpeg\8.1.2\bin\ffprobe.exe'
  data=json.loads(subprocess.run([ffprobe,'-v','error','-show_streams','-of','json',str(f)],capture_output=True,text=True,check=True).stdout)
  v=next(x for x in data['streams'] if x['codec_type']=='video');item.update(dimensions=[v['width'],v['height']],fps=v['avg_frame_rate'],frames=v.get('nb_frames','not exposed'))
 if f.suffix.lower()=='.aseprite':
  header=f.read_bytes()[:14];item.update(dimensions=list(struct.unpack_from('<HH',header,8)),frames=struct.unpack_from('<H',header,6)[0])
 if f.suffix.lower() in media:
  item['license_provenance']='Project-owned Roshan derivative; ImageGen output where declared; LTX Community License and Gemma terms for new-model use. Model weights not redistributed.'
  item['source_record']='environment/imagegen_receipt.json; briefs/job_card.json; results/<take>/workflow.api.json and receipt.json; previous ltx_registered_wave_20261004 manifest'
  rows.append(f'| `{repo}` | Project-owned Roshan; ImageGen/LTX derivative as declared; inherited original provenance, LTX Community License, Gemma terms for LTX-2.3 | https://github.com/Ebonyks/mermaid-roshan-reef/blob/a4674e81d1528639b0a23b7b7d34a5c013f90925/assets_src/cinematics/ltx_registered_wave_20261004/manifest.json | {mod} Source-only, no runtime acceptance. |')
 payload.append(item)
text+=marker+'\n| Asset | Source/license | Source URL | Modifications |\n|---|---|---|---|\n'+'\n'.join(rows)+'\n';license_path.write_text(text,encoding='utf-8')
manifest={'schema':'source-study-payload-v1','status':'REFERENCE_ONLY','baseline':'a4674e81d1528639b0a23b7b7d34a5c013f90925','source_packet':'assets_src/cinematics/ltx_registered_wave_20261004','source_window_inclusive':[40,64],'defect_span_inclusive':[44,52],'payload':payload,'payload_sha256':hashlib.sha256('\n'.join(x['path']+' '+x['sha256'] for x in payload).encode()).hexdigest(),'acceptance':'Source-only repair study; production quality and owner/device/child acceptance not established','model_weights_redistributed':False}
(p/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
impact_path=r/'design/audit_impacts/ltx-retake-repair-20261004.json';impact=json.loads(impact_path.read_text())
impact['files']=[f.relative_to(r).as_posix() for f in sorted(p.rglob('*')) if f.is_file()]+['ASSET_LICENSES.md','audit/animation/README.md','audit/MASTER_AUDIT_2026-08-09.md','design/05_DOC_LEDGER.md','design/animation/ANIMATION_PRODUCTION_PROTOCOL.md','design/reference/OWNER_DECISIONS.md']
impact_path.write_text(json.dumps(impact,indent=2)+'\n');print('REAL_ARTIFACT_REFRESH',len(payload),'payload files',len(rows),'asset rows',flush=True)
