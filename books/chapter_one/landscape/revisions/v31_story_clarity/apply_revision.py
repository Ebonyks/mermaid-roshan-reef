"""Apply bounded V31 local art, truthful progress, and Puff's belonging beat."""
from pathlib import Path
import hashlib,json
from PIL import Image
V=Path(__file__).resolve().parent; L=V.parents[1]; R=L.parents[2]
def read(p):return json.loads(p.read_text(encoding='utf8'))
def save(p,q):p.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p):return p.resolve().relative_to(R.resolve()).as_posix()
B=read(V/'BOOK_BASELINE.json');jobs=read(V/'generation_jobs.json')['jobs']
regions={
 'waterfall_progress': [[[398,290],[415,259],[449,251],[492,250],[548,259],[570,287],[568,610],[570,825],[590,854],[680,864],[1484,867],[1484,1060],[0,1060],[0,867],[380,866],[399,828],[408,613],[408,434]]],
 'door_mystery': [[[1180,632],[1189,451],[1203,403],[1240,367],[1296,346],[1346,365],[1382,402],[1407,451],[1408,638]],[[905,558],[926,544],[949,545],[966,559],[968,589],[955,610],[931,611],[912,597]]],
 'rear_lamma': [[[39,277],[59,274],[66,288],[96,288],[110,307],[108,334],[69,337],[47,326],[39,304]]],
 'rest_bank31': [[[202,909],[257,900],[321,900],[381,911],[402,940],[402,997],[379,1011],[257,1012],[210,995]],[[1097,929],[1118,904],[1176,901],[1238,913],[1261,946],[1252,995],[1224,1013],[1110,1012],[1090,983]]],
}
outputs={
 'door_mystery':'exec-0e2ac13d-b595-4bae-b1c2-cbf89c33cba1.png',
 'waterfall_progress':'exec-6dd06f92-74f1-4068-8cf1-2bb492f04159.png',
 'rear_lamma':'exec-41610ac7-fe94-4155-9331-1303fdbe7b4c.png',
 'rest_bank31':'exec-273a6d19-dccc-420f-9037-daa5491495ad.png',
 'puff_gratitude':'exec-c8c480b8-8c7f-4e68-b3dc-0f0f02080a62.png',
}
base_keys={'waterfall_progress':'v22_scene_11','door_mystery':'v27_door','rear_lamma':'v23_cover_h','rest_bank31':'v29_bank31_final','puff_gratitude':'approved_rainbow_puff_cutout'}
for job in jobs:
 k=job['id'];p=V/'art'/f'{k}.png';im=Image.open(p)
 refs=[dict(path=rel(Path(f)),sha256=sha(Path(f)),dimensions=list(Image.open(f).size),role='edit_target' if i==0 else 'identity_reference') for i,f in enumerate(job['refs'])]
 B['sources']['v31_'+k]=dict(file=p.relative_to(L).as_posix(),provenance=dict(method='Built-in image_gen local inpaint',native_path=rel(p),native_sha256=sha(p),dimensions=list(im.size),mode=im.mode,prompt_sha256=hashlib.sha256(job['prompt'].encode()).hexdigest(),references=refs,source_base_key=base_keys[k],source_preserved=True,delivery='Only explicit native candidate polygons are exposed over the existing source in the PDF renderer. Whole candidate is retained for provenance, not used as a scene replacement.'))
pages={p['page']:p for p in B['pages']}
def patch(k,poly,size=(1484,1060),**extra):return dict(source='v31_'+k,reference_size=list(size),polygon=poly,**extra)
p=pages[12];p['text']='Roshan kept clearing the gunk,\nlittle by little.';p['local_patches']=[patch('waterfall_progress',q) for q in regions['waterfall_progress']];p['background_theme']='Partial progress: one small aqua patch of falling water emerges from the gunk; completion is reserved for13. No stream count is claimed.'
p=pages[13];p['text']='Whoosh! Clean water flowed.\nThe waterfall turned rainbow!'
p=pages[23];p['text']='One last door was still shut.\nA low rumble came from behind it...';p['local_patches']=[patch('door_mystery',q) for q in regions['door_mystery']];p['background_theme']='The same final shell door is shadowed violet with a narrow uncertain seam glow. Correct completed room doors and converging route paths remain, but there is no rainbow welcome; Roshan looks cautiously curious.'
p=pages[31];p['art']=['roshan_wave_large','approved_rainbow_puff_cutout'];p['layout']='placements';p['placements']=[dict(source='roshan_wave_large',box=[73,57,191,215]),dict(source='approved_rainbow_puff_cutout',box=[303,89,139,156])]
p['text']='“Thank you,” said Grand Puff.\n“Come and rest with us!” said Roshan.'
p['background_patches']=[patch('rest_bank31',q) for q in regions['rest_bank31']]
puff_size=Image.open(L/B['sources']['approved_rainbow_puff_cutout']['file']).size
fw,fh=puff_size
# This face mask stays well inside the unchanged source cloud silhouette/paws.
face=[[int(fw*.25),int(fh*.57)],[int(fw*.34),int(fh*.53)],[int(fw*.47),int(fh*.57)],[int(fw*.60),int(fh*.57)],[int(fw*.69),int(fh*.60)],[int(fw*.72),int(fh*.70)],[int(fw*.63),int(fh*.74)],[int(fw*.46),int(fh*.72)],[int(fw*.29),int(fh*.69)]]
regions['puff_gratitude']=[face]
p['local_patches']=[patch('puff_gratitude',face,puff_size,placement=p['placements'][1])]
p['integrated_motifs']=['yawning_bunny','closed_toy_chest','resting_bunny','settled_sailboat','toy_rings','new_toy_coral']
p['integrated_prop_bounds']=[[.139,.85,.073,.096],[.195,.879,.070,.070],[.780,.855,.072,.096],[.749,.866,.048,.088],[.751,.913,.046,.038],[.273,.908,.030,.043]]
p['background_theme']='Puff is welcomed to rest after cleaning; two tiny bunnies wind down beside their game toys. Old Lamma chest peek is removed, leaving two appearances total (bath9 and rear).'
p['beat']='puff_thanks_and_belonging';p['marginal_bunny_count']=2
B['back_cover'].setdefault('local_patches',[]).extend(patch('rear_lamma',q) for q in regions['rear_lamma'])
B['status']='V31 story-clarity review proof; external acceptance pending'
B['revision']='V31 story clarity and belonging'
B['review_href']='../AUDIT_REVIEW.html'
save(L/'book.json',B);save(V/'BOOK_CURRENT.json',B)
e=[]
for j in jobs:
 k=j['id'];p=V/'art'/f'{k}.png';q=B['sources']['v31_'+k]['provenance']
 e.append(dict(id=k,attempt=1,generation_method='built-in image_gen',selection='SELECTED_LOCAL_DERIVATIVE',prompt=j['prompt'],prompt_sha256=q['prompt_sha256'],references=q['references'],native_output=dict(path=rel(p),sha256=sha(p),dimensions=q['dimensions'],mode=q['mode']),original_tool_filename=outputs[k],base_source_key=base_keys[k],delivery_polygons=regions[k],reference_size=list(puff_size) if k=='puff_gratitude' else [1484,1060],delivery_pages=[12] if k=='waterfall_progress' else [23] if k=='door_mystery' else ['back_cover'] if k=='rear_lamma' else [31],review='PENDING native composed-page review; all outside-mask pixels remain source base',source_preservation='Original untouched; no full-scene replacement'))
save(V/'generation_evidence.json',dict(baseline='19ee6ce8ec4c20c05714f101d0d222a33477e400',generated_count=len(e),selected_candidate_count=len(e),generated=e,meaning='Selected native candidates supply only declared local polygons; editorial acceptance is reviewed separately.'))
print(json.dumps(dict(changed_story_pages=[12,13,23,31],rear_cover=True,story_pages=len(B['pages']),selected_local_candidates=len(e),puff_reference_size=puff_size)))
