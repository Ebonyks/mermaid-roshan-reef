"""Archive actual generation inputs, native candidates and delivered uses."""
from pathlib import Path
import hashlib, json
from PIL import Image

V=Path(__file__).resolve().parent; L=V.parents[1]; R=L.parents[2]
BASE='5da33b22c9b95358d98defe8e340a901d5470991'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p): return p.resolve().relative_to(R.resolve()).as_posix()
def read(p): return json.loads(p.read_text(encoding='utf8'))
def save(p,v): p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')

B=read(L/'book.json'); layout=read(V/'complete/page_provenance.json')
jobs={}
for f in sorted(V.glob('generation_jobs*.json')):
 for j in read(f):
  if j['id'] in jobs: assert jobs[j['id']]['prompt']==j['prompt'],j['id']
  jobs[j['id']]=j
outputs={}
for f in [V/'generation_outputs_all.json',*sorted(V.glob('generation_outputs_round*.json'))]:
 for j in read(f):
  if j['id'] in outputs: assert outputs[j['id']]['native']==j['native']
  outputs[j['id']]=j
assert len(jobs)==len(outputs)==50,(len(jobs),len(outputs))
used={}
for layer in layout['layers']:
 key=layer['source_key']
 if key.startswith('v29_'):used.setdefault(key[4:],[]).append(layer)
reject={
 'caption06':'The first composed mask made a visible floor boundary; floor06_final follows grout and the tub base instead.',
 'neck19':'The first tiny costume edit retained the pendant; neck19_final replaces it.',
 'ceiling27':'Full-page assembly showed a duplicated partial chandelier and horizontal join; reuse approved_scrub_ceiling instead.',
 'ceiling28':'Full-page assembly showed a discontinuous architectural join; reuse approved_scrub_ceiling instead.',
 'ceiling29':'Full-page assembly showed a duplicated partial chandelier and horizontal join; preserve canonical landing with approved_scrub_ceiling instead.',
 'bank31_tiny':'One ear remained above the strict bottom15% limit; final candidate was generated and measured.'}
records=[]
for id,j in sorted(jobs.items()):
 p=V/'art'/f'{id}.png'; native=Path(outputs[id]['native'])
 assert sha(p)==sha(native),'Workspace copy differs from native generator output: '+id
 refs=[]
 for f in j['refs']:
  q=Path(f) if Path(f).is_absolute() else R/f
  refs.append(dict(path=rel(q),sha256=sha(q),dimensions=list(Image.open(q).size),role='Source/edit target or identity/prop continuity input, as specified by prompt.'))
 selected=id in used
 reason=reject.get(id,'Earlier bank study failed strict lower15%/12% geometry or weaker event-specific clarity; selected measured native revision supersedes it.')
 records.append(dict(
  id=id,page=j['page'],attempt=j.get('attempt',1),specific_gap=j['gap'],
  generation_method='Built-in image_gen, source-conditioned static-book edit; native PNG retained unchanged.',
  prompt=j['prompt'],prompt_sha256=hashlib.sha256(j['prompt'].encode()).hexdigest(),references=refs,
  transparent_background_requested=j.get('transparent',False),
  output=dict(path=rel(p),sha256=sha(p),native_dimensions=list(Image.open(p).size),native_generator_basename=native.name,native_copy_byte_identical=True),
  selection='SELECTED_DERIVATIVE' if selected else 'REJECTED_UNUSED',
  selection_reason='Inspected at native and composed-page size; actual scope below.' if selected else reason,
  actual_delivery_layers=used.get(id,[]),
  local_masks=[dict(page=q['page'],configuration={k:q.get(k) for k in ['local_patch','local_patches','background_patches'] if q.get(k)}) for q in B['pages'] if any(x['page']==q['page'] for x in used.get(id,[]))],
  review_evidence=['character_final.json','style_final.json','language_final.json'],
  external_acceptance='Owner/child/print review pending. Agent review is not human approval.'))
save(V/'generation_evidence.json',dict(schema_version=1,baseline=BASE,scope='Static picture book; no runtime/game/cinematic change; source identity and staging retained. Owner-authorized decorative bunny performances and local character repairs only.',generated_count=50,selected_candidate_count=len(used),rejected_candidate_count=50-len(used),generation_budget_authority='Owner explicitly approved substantial iteration, including upwards of50 generations; no numeric upper cap is inferred.',generated=records,unchanged_sources=[q for q in layout['layers'] if not q['source_key'].startswith('v29_')],local_edit_policy='Masks/layout coordinates in book.json and actual page_provenance layers are authoritative. Entire regenerated stationery backgrounds11/21 were selected to avoid rectangular wash seams; their ground props preserve design visually, not byte-exact extraction. Narrative source-preserving restorations3/14/18/19 retain action/staging rather than invent scenes.',pixel_edit_limitations='Generated image pixels do not prove exact hidden10% ground occlusion or numeric shadow opacity. No claim of pixel-exact integration is made. Native masters are not silently upscaled into higher-density art.',bubble_policy='Audit distinguishes painted watercolor/lather grain from observed broken rings and block/halo patterns; final sources use lossless PNG and PDF image streams use Flate encoding, never new JPEG recompression.',hidden_visitors=dict(adult_only=True,story_pages=[9,31],count=2,prompted_in_book=False),external_acceptance=['owner','child read-aloud','physical print dummy','professional SLP review']))
print(json.dumps(dict(generations=len(records),selected=len(used),rejected=len(records)-len(used))))
