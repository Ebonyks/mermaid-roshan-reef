"""Apply only recorded local identity derivatives to the frozen V29 book."""
from pathlib import Path
import hashlib,json
V=Path(__file__).resolve().parent; L=V.parents[1]
def read(p):return json.loads(p.read_text('utf-8-sig'))
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
baseline=V/'BOOK_BASELINE.json'
if not baseline.exists():
 current=read(L/'book.json')
 assert current['revision'].startswith('V29')
 write(baseline,current)
B=read(baseline)
for name in ['front_identity','rear_identity','castle_attention','rumi_face_crop','yellow_sponge']:
 p=V/'art'/f'{name}.png'
 assert p.is_file()
 B['sources']['v30_'+name]={'file':p.relative_to(L).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'provenance':'Built-in imagegen bounded inpaint. Native candidate preserved; only the explicit local polygon is delivered over the unchanged V29 scene.'}
B['sources']['v30_yellow_sponge']['alpha_box']=[236,108,1156,1037]
B['sources']['v30_yellow_sponge']['provenance']='Existing yellow sponge isolated with local hand-occlusion fill, true generated RGBA preserved. Whole authored sponge contour retained; padded crop excludes isolated alpha<=8 generator specks away from the object, without modifying native pixels.'
def patch(name,polygon,window=None):
 q={'source':'v30_'+name,'reference_size':[1484,1060],'polygon':polygon}
 if window:q['source_canvas_box']=window
 return q
B['cover']['local_patches']=[
 patch('front_identity',[[398,310],[412,296],[446,291],[477,300],[492,324],[492,350],[479,374],[455,386],[433,378],[412,362],[391,348]]),
 patch('front_identity',[[734,550],[758,545],[783,551],[789,575],[779,597],[757,603],[737,593],[731,570]])]
B['back_cover']['local_patches']=[
 patch('rear_identity',[[971,313],[990,294],[1030,290],[1072,303],[1110,326],[1137,352],[1138,380],[1111,405],[1063,438],[1027,444],[998,421],[974,388],[945,369]]),
 patch('rear_identity',[[622,479],[645,475],[670,484],[672,508],[659,530],[637,533],[620,519],[615,497]])]
P={p['page']:p for p in B['pages']}
P[4]['local_patches']=[
 patch('castle_attention',[[139,508],[163,504],[189,511],[199,531],[192,553],[178,574],[155,575],[138,561],[127,539]]),
 patch('castle_attention',[[279,385],[302,379],[327,385],[340,405],[333,429],[314,449],[292,454],[274,437],[265,408]])]
P[10]['local_patches']=[patch('rumi_face_crop',[[744,598],[766,588],[792,590],[815,602],[829,624],[831,645],[814,665],[792,678],[767,677],[749,660],[735,637],[733,616]],[704,558,863,711])]
P[5]['text']='Daddy gave her a brush and some sponges.\n“One little job at a time.”'
P[5]['placements']=[{'source':P[5]['art'][0],'box':[49,65,205,190]},{'source':P[5]['art'][1],'box':[346,82,107,126]},{'source':'v30_yellow_sponge','box':[247,98,86,114]}]
P[5]['art'].append('v30_yellow_sponge')
B['revision']='V30 - local identity and continuity polish'
B['review_href']='../AUDIT_REVIEW.html'
B['revision_notes'].append('V30: local adult-Rumi face repairs0/10/33; Roshan brooch removals on covers; dirty-hall face attention4; supplies plural5 with an existing-source-derived yellow sponge cutout. Page5 brush stays exact; pink sponge is reduced/right-shifted beside the added yellow sponge. No new narrative scene. V29 native art/scene compositions/canon/borders remain the base.')
write(L/'book.json',B)
write(V/'BOOK_CURRENT.json',B)
write(V/'visual_review.json',{'revision_verdict':'COMPOSED_LOCAL_STUDIES; INDEPENDENT_VISUAL_REVIEW_PENDING','open_findings':[]})
print('Applied seven bounded regions, a supplies-caption revision and a source-derived whole-sponge cutout.')
