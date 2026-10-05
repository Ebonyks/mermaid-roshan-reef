from pathlib import Path
import json,hashlib,struct,subprocess,re
from PIL import Image
p=Path(__file__).resolve().parents[1];r=p.parents[2]
def sha(f):
 with Path(f).open('rb') as s:return hashlib.file_digest(s,'sha256').hexdigest()
ff=r'C:\Users\Peter\AppData\Local\Programs\MermaidReefTools\FFmpeg\8.1.2\bin\ffprobe.exe'
payload=[];rows=[];media={'.png','.mp4','.aseprite','.latent'}
for f in sorted(p.rglob('*')):
 if not f.is_file() or f.name in {'manifest.json','remote_verification.json','remote_receipt_publication.json'} or '__pycache__' in f.parts:continue
 rel=f.relative_to(p).as_posix();repo=f.relative_to(r).as_posix();parents=[]
 item={'path':rel,'sha256':sha(f),'bytes':f.stat().st_size,'acceptance':'SOURCE_ONLY; rejected footage, owner/device/child acceptance absent'}
 role='workflow_or_actual_evidence';mod='Source-side research, code or measured receipt; no pixel acceptance.'
 if rel.startswith('inputs/'):
  parents=['assets_src/cinematics/ltx_two_pass_wave_20261004/inputs/'+f.name];role='reused_complete_figure_guide';mod='Exact byte copy of previous Aseprite full-figure guide; owner review pending for the missing-pose key.'
 elif rel.startswith('results/'):
  take=rel.split('/')[1];base=p/'results'/take;record=base/'receipt.json'
  if f.name!='receipt.json' and record.exists():parents=[record.relative_to(r).as_posix()]
  role='actual_native_model_output_or_review'
  mod='Unmodified native complete frames or declared whole-frame encoding/Aseprite export; no limb replacement.'
  if f.suffix=='.png' and f.parent.name in {'refined_frames','stage1_frames','preflight_frames'}:
   rec=json.loads(record.read_text());item.update(timeline_index=int(f.stem),fps=rec['fps'],generation_record=record.relative_to(r).as_posix(),workflow_record=(base/'workflow.api.json').relative_to(r).as_posix())
   if rec['model_job']:parents += [(p/f'inputs/guide_{i:04d}.png').relative_to(r).as_posix() for i in [0,3,7,17,22,27,36,40]]
   else:parents += [(p/'inputs/guide_0022.png').relative_to(r).as_posix()]
  if f.parent.name=='comparison24_frames':
   index=int(f.stem)*2;parents=[(base/f'refined_frames/{index:04d}.png').relative_to(r).as_posix()];item.update(source_index=index,output_index=int(f.stem));mod='Exact complete frame selection on even indices; no interpolation/resizing.'
  if f.name in {'native_review.aseprite','native.mp4','lowering_native_contact.png'}:
   parents += [(base/f'refined_frames/{i:04d}.png').relative_to(r).as_posix() for i in range(json.loads(record.read_text())['frames'])]
 elif rel.startswith('comparison/'):
  role='native_1to1_same_action_comparison';mod='Aseprite whole-frame side-by-side placement; no spatial resampling, interpolation or pixel repair.'
  if f.suffix=='.png':
   i=int(f.stem);parents=[(p/f'results/{t}/refined_frames/{i*2 if t=="temporal_48fps" else i:04d}.png').relative_to(r).as_posix() for t in ['base_two_pass','temporal_retake','anti_blur_nag','temporal_48fps']]
  elif f.suffix in {'.mp4','.aseprite'}:parents=[(p/f'comparison/frames/{i:04d}.png').relative_to(r).as_posix() for i in range(41)]
 if any(not(r/x).is_file() for x in parents):raise ValueError(('Missing declared parent',rel,parents))
 license='Project-owned Roshan/Aseprite derivatives; prior named ImageGen key per previous source manifest; generated2.5 outputs under LTX-2.x community model terms. Weights not redistributed.'
 if rel.startswith('scripts/official_refine_nodes/'):license='Pinned Lightricks ComfyUI-LTXVideo source; accompanying LICENSE; minimal initializer is declared project glue.'
 elif f.name=='ltx_nag_vendor.py':license='Pinned Kijai KJNodes source excerpt, retained attribution/license in KJNODES_LICENSE.'
 item.update(role=role,modification_status=mod,source_paths=parents,source_sha256={x:sha(r/x) for x in parents},license_provenance=license)
 if f.suffix=='.png':
  with Image.open(f) as im:item.update(dimensions=list(im.size),mode=im.mode)
 if f.suffix=='.aseprite':
  with f.open('rb') as s:header=s.read(14)
  item.update(dimensions=list(struct.unpack_from('<HH',header,8)),frames=struct.unpack_from('<H',header,6)[0])
 if f.suffix=='.mp4':
  j=json.loads(subprocess.run([ff,'-v','error','-show_streams','-of','json',str(f)],capture_output=True,text=True,check=True).stdout);v=next(x for x in j['streams'] if x['codec_type']=='video');item.update(dimensions=[v['width'],v['height']],frames=int(v['nb_frames']),fps=v['avg_frame_rate'])
 if f.suffix in media:rows.append('| '+chr(96)+repo+chr(96)+' | '+license+' | https://github.com/Ebonyks/mermaid-roshan-reef/tree/abbffecbf27479e1349326f2c9685962e7964c55/assets/characters/roshan_25d | '+mod+' Reference only. |')
 payload.append(item)
marker='\n## LTX-2.5 8 GB wave and blur comparison — 2026-10-04\n'
licensefile=r/'ASSET_LICENSES.md';s=licensefile.read_text(encoding='utf-8')
if marker in s:
 begin=s.index(marker);end=s.find('\n## ',begin+len(marker));s=s[:begin]+(s[end:] if end>=0 else '')
s+=marker+'\n| Asset | Source/license | Source URL | Modifications |\n|---|---|---|---|\n'+'\n'.join(rows)+'\n';licensefile.write_text(s,encoding='utf-8')
manifest={'schema':'source-study-payload-v1','status':'REJECTED_REFERENCE_ONLY','baseline':'abbffecbf27479e1349326f2c9685962e7964c55','payload':payload,'payload_sha256':hashlib.sha256('\n'.join(x['path']+' '+x['sha256'] for x in payload).encode()).hexdigest(),'model_weights_redistributed':False,'accepted':False,'actual_model_jobs':4,'previous_source_manifest':'assets_src/cinematics/ltx_two_pass_wave_20261004/manifest.json','next_adapter_access':'Pending separate explicit gate approval; no output claimed'}
(p/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
impactpath=r/'design/audit_impacts/ltx25-8gb-wave-20261004.json'
impact=json.loads(impactpath.read_text()) if impactpath.exists() else {
'id':'ltx25-8gb-wave-20261004','scope':'Owner-directed isolated2.5 8GB setup and same-action two-pass/whole-figure retake/NAG/48fps tests, native Aseprite publication, blur-method research and binding workflow refinements; separate official adapter gate pending. No game runtime changes.','baseline':'abbffecbf27479e1349326f2c9685962e7964c55','initial_origin_dev':'8a2f30cb0df44ece3b1172ed2dbcb9a55fc5d622','rules':['DL-AUTH-05','DL-AUTH-06','DL-AUTH-07','DL-ASSET-01','DL-ASSET-02','DL-ASSET-03','DL-ASSET-04','DL-ASSET-05','DL-MOT-14','DL-MOT-15','DL-MOT-16','DL-CIN-03','DL-CIN-04','DL-CIN-05','DL-CIN-11'],'findings':[],'no_findings_reason':'Source-only feasibility/quality repair experiments do not change runtime atlas/sampling or accepted art. RelatedMA-ROSHAN-003/005 lifecycles unchanged.','validation':[{'command':'Four bounded actual2.5 GPU jobs and decoder preflight','result':'PASS','evidence':'Packet results/*/receipt.json and actual GPU NAG proof; frame/guide recipe and effective runtime in environment/trial_verification.json.'},{'command':'Native whole-figure quality inspection','result':'FAIL','evidence':'Packet environment/review.json; NAG/retake do not repair torn fingers;48fps improves one key but neighboring smear remains.'},{'command':'Native Aseprite master/export pixel roundtrip','result':'PASS','evidence':'environment/trial_verification.json; original complete frames retained.'},{'command':'python -B tools/audit_document_authority.py; python -B tools/audit_development.py --base auto','result':'PENDING','evidence':'Run before commit; packet environment/project_gates.json.'},{'command':'Exact new-head project CI before integration','result':'PENDING','evidence':'Source-only runtime tree unchanged from green dependencyabbff; new-head CI remains required.'},{'command':'Anonymous immutable GitHub manifest/payload verification','result':'PENDING','evidence':'Separate remote_verification.json written after actual publication.'}],'acceptance_gaps':'All footage rejected/reference-only. Official detail-adapter access and one conditional test pending. No production/runtime/device/child/owner acceptance or finding closure. Cleanup wall not fully metered.','lessons':[{'lesson':'Actual negative-guidance hooks can execute without fixing the named blur/topology defect.','write_back':'design/animation/ANIMATION_PRODUCTION_PROTOCOL.md#verify-the-model-recipe-before-judging-a-take'},{'lesson':'Frozen source video latents do not establish identical decoded pixels; check both.','write_back':'design/animation/ANIMATION_PRODUCTION_PROTOCOL.md#iterative-repair-with-aseprite-and-temporal-retakes'},{'lesson':'Higher fps improves one key but does not accept its neighboring figure motion.','write_back':'assets_src/cinematics/ltx25_8gb_wave_20261004/environment/review.json'}]}
impact['files']=[f.relative_to(r).as_posix() for f in sorted(p.rglob('*')) if f.is_file() and '__pycache__' not in f.parts]+['ASSET_LICENSES.md','audit/MASTER_AUDIT_2026-08-09.md','audit/animation/README.md','design/05_DOC_LEDGER.md','design/animation/ANIMATION_PRODUCTION_PROTOCOL.md','design/animation/WORKFLOW_OPTIONS_2026-10-03.md']
impactpath.write_text(json.dumps(impact,indent=2)+'\n')
print('HASHED_PAYLOAD',len(payload),'ASSET_ROWS',len(rows),'BYTES',sum(x['bytes'] for x in payload),flush=True)
