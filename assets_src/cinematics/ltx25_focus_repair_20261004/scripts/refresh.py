"""Bind exact source-only payload, per-asset attribution and changed-file impact."""
import hashlib,json,struct
from pathlib import Path
from PIL import Image
P=Path(__file__).resolve().parents[1];ROOT=P.parents[2]
OLD='assets_src/cinematics/ltx25_8gb_wave_20261004'
V2='assets_src/cinematics/ltx25_scale_filter_v2_20261004'
prefix=P.relative_to(ROOT).as_posix()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
native=[prefix+f'/decoder_2_frames/{i:04d}.png' for i in range(41)]
baseline=[OLD+f'/results/scale_registered/refined_frames/{i:04d}.png' for i in range(41)]
payload=[];licenses=[]
for f in sorted(P.rglob('*')):
    if not f.is_file() or '__pycache__' in f.parts or f.name in {'manifest.json','remote_verification.json','receipt_publication.json'}:continue
    rel=f.relative_to(P).as_posix();parents=[];role='recipe_or_measured_evidence'
    mod='Source-only analysis, recipe or measured evidence; no runtime acceptance.'
    if f.parent.name=='decoder_2_frames':
        parents=[OLD+'/results/scale_registered/refined_video.latent',prefix+'/workflow.api.json',prefix+'/decoder_2_proof.json']
        role='experimental_native_complete_frame';mod='Same saved video latent decoded with experimental2-step matched diffusion VAE; no transformer resampling; rejected added grain and persistent defects.'
    elif f.name in {'decoder_2_review.aseprite','decoder_2_review.mp4'}:
        parents=native;role='editable_review_master' if f.suffix=='.aseprite' else 'encoded_review'
        mod='Complete41-frame native2-step decode at24fps; Aseprite lossless master or H264 CRF15 yuv420p viewing copy. Rejected/reference only.'
    elif f.name=='decoder_1_vs_2.mp4':
        parents=baseline+native;role='same_latent_same_timeline_comparison'
        mod='Aseprite1:1 native default-left/experimental2-step-right columns; identical timeline; H264 CRF15 yuv420p preview; no temporal repair.'
    elif f.name=='focus_metrics.json':
        parents=baseline+native+[V2+f'/frames/{i:04d}.png' for i in range(41)]+[OLD+f'/scale_continuity/registered_guides/guide_{i:04d}.png' for i in [0,3,7,17,22,27,36,40]]
        role='read_only_numeric_diagnostics'
    elif f.name=='verification.json':parents=baseline+native+[prefix+'/decoder_2_review.aseprite',prefix+'/receipt.json']
    elif f.name in {'receipt.json','decoder_1_proof.json','decoder_2_proof.json'}:parents=[OLD+'/results/scale_registered/refined_video.latent',prefix+'/workflow.api.json']
    row={'path':rel,'bytes':f.stat().st_size,'sha256':sha(f),'role':role,'modification_status':mod,
         'source_paths':parents,'source_sha256':{x:sha(ROOT/x) for x in parents},
         'license_provenance':'Project-owned Roshan source-study derivatives; inherited source attribution and LTX-2.x community model terms for generated footage; no model weights redistributed.'}
    if f.suffix=='.png':
        with Image.open(f) as im:row.update(dimensions=list(im.size),mode=im.mode)
    elif f.suffix=='.aseprite':
        header=f.read_bytes()[:14];row.update(dimensions=list(struct.unpack_from('<HH',header,8)),frames=struct.unpack_from('<H',header,6)[0])
    elif f.suffix=='.mp4':row.update(dimensions=[1152 if f.name=='decoder_1_vs_2.mp4' else 576,832],frames=41,fps='24/1')
    if f.suffix in {'.png','.mp4','.aseprite'}:
        licenses.append('| `'+prefix+'/'+rel+'` | '+row['license_provenance']+' | https://github.com/Ebonyks/mermaid-roshan-reef/tree/c51075fff13cfd8f4795b5ef7da232fc7462e7f4/'+OLD+' | '+mod+' |')
    payload.append(row)
manifest={'schema':'source-study-payload-v1','status':'REJECTED_REFERENCE_ONLY','baseline':'19d6de9fca64faf22086ca6c55315cd9eea96bd4',
          'payload':payload,'payload_sha256':hashlib.sha256('\n'.join(x['path']+' '+x['sha256'] for x in payload).encode()).hexdigest(),
          'new_transformer_jobs':0,'new_imagegen_calls':0,'new_decoder_ablation_jobs':1,
          'model_weights_redistributed':False,'accepted':False,'previous_source_manifest':OLD+'/manifest.json',
          'prior_registration_manifest':V2+'/manifest.json','future_adapter_execution':'UNTESTED_ON_8GB',
          'archive_complete_requires':'Actual anonymous remote receipt at exact published revision; not inferred from this manifest'}
(P/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
marker='\n## LTX-2.5 size and focus corrective study — 2026-10-04\n'
path=ROOT/'ASSET_LICENSES.md';text=path.read_text(encoding='utf-8')
if marker in text:
    start=text.index(marker);end=text.find('\n## ',start+len(marker));text=text[:start]+(text[end:] if end>=0 else '')
text+=marker+'\n| Asset | Source/license | Source URL | Modifications |\n|---|---|---|---|\n'+'\n'.join(licenses)+'\n'
path.write_text(text,encoding='utf-8',newline='')
path=ROOT/'design/audit_impacts/ltx25-focus-repair-20261004.json';impact=json.loads(path.read_text())
docs=['ASSET_LICENSES.md','audit/MASTER_AUDIT_2026-08-09.md','audit/animation/README.md','design/05_DOC_LEDGER.md',
      'design/animation/ANIMATION_PRODUCTION_PROTOCOL.md','design/reference/owner_decisions.json','design/reference/OWNER_DECISIONS.md']
impact['files']=sorted(set(docs+[f.relative_to(ROOT).as_posix() for f in P.rglob('*') if f.is_file() and '__pycache__' not in f.parts]))
path.write_text(json.dumps(impact,indent=2)+'\n',encoding='utf-8')
assert all(x['bytes']<104857600 for x in payload),'GitHub per-file limit'
print('PAYLOAD',len(payload),'LICENSE_ROWS',len(licenses),'BYTES',sum(x['bytes'] for x in payload),'MAX_FILE',max(x['bytes'] for x in payload))
