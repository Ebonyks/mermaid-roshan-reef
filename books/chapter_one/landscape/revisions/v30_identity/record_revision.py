"""Record actual six generation calls, selected native derivatives and masks."""
from pathlib import Path
import hashlib,json
from PIL import Image
V=Path(__file__).resolve().parent;L=V.parents[1];R=L.parents[2]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text('utf-8-sig'))
def rel(p):return p.resolve().relative_to(R.resolve()).as_posix()
def save(p,q):p.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
B=read(L/'book.json');prov=read(V/'complete/page_provenance.json');prior=read(V.parent/'v29_polish/generation_evidence.json')
rows=[]
for j in read(V/'generation_jobs.json'):
 p=V/'art'/f"{j['id']}.png";im=Image.open(p)
 layers=[q for q in prov['layers'] if q['source_key']=='v30_'+j['id']]
 rows.append({'id':j['id'],'method':'Built-in imagegen; source-conditioned bounded inpaint or isolated object derivative','prompt':j['prompt'],'prompt_sha256':hashlib.sha256(j['prompt'].encode()).hexdigest(),'references':[{'path':rel(Path(q)),'sha256':sha(Path(q)),'role':'Edit target' if n==0 else 'Adult identity / existing-object reference'} for n,q in enumerate(j['refs'])],'native_output':rel(p),'native_sha256':sha(p),'native_size':list(im.size),'native_mode':im.mode,'selection':'SELECTED_DERIVATIVE' if layers else 'REJECTED_UNUSED','selection_reason':'Bounded regions/source-derived whole object only; native proof and independent review required.' if layers else 'Face identity change too slight at book size; superseded by focused facial crop. No delivered page uses it.','delivered_layers':layers})
assert len(rows)==6 and sum(bool(q['delivered_layers']) for q in rows)==5
q={'revision':'V30','baseline':'82a6dc1dba381c0b3ef507a8397512fa09ef624e','previous_generation_evidence':{'path':rel(V.parent/'v29_polish/generation_evidence.json'),'sha256':sha(V.parent/'v29_polish/generation_evidence.json')},'generated_count':6,'selected_candidate_count':5,'rejected_candidate_count':1,'cumulative_polish_generation_candidates':prior['generated_count']+6,'cumulative_selected_derivatives':prior['selected_candidate_count']+5,'generated':rows,'native_originals_preserved':True,'source_crop_reference':{'file':rel(V/'references/rumi_face_crop.png'),'sha256':sha(V/'references/rumi_face_crop.png'),'source':B['sources']['v26_rumi_trapped']['file'],'source_sha256':sha(L/B['sources']['v26_rumi_trapped']['file']),'source_box':[704,558,863,711],'operation':'Lossless crop for targeted facial edit input only'},'scope':'Seven explicitly recorded irregular facial/bodice inpaint regions; one complete existing-source-derived yellow sponge cutout. No full-scene redraw or narrative invention. Accepted full-art base scenes remain unchanged outside the declared regions; page5 rearranges true foreground tool cutouts.','generation_budget':'Owner approved upwards of50 regenerations for quality gaps; no numeric upper cap inferred. No generation for novelty.'}
save(V/'generation_evidence.json',q)
scope=read(V/'REVISION_SCOPE.json');scope['scope']=q['scope'];scope['status']='COMPOSED_DERIVATIVES; frozen review and verification pending';save(V/'REVISION_SCOPE.json',scope)
PY=V.parent/'v29_polish'
for name in ['verify_remote.py']:
 (V/name).write_text((PY/name).read_text('utf-8').replace('v29_polish','v30_identity').replace('V29','V30'),encoding='utf-8',newline='\n')
print('Recorded six native candidates; five selected, one rejected.')
