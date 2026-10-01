"""Apply the source-preserving V32 layout and owner rainbow clarification."""
from pathlib import Path
import copy,hashlib,json
from PIL import Image
V=Path(__file__).resolve().parent;L=V.parents[1];R=L.parents[2]
def read(p):return json.loads(p.read_text(encoding='utf8'))
def save(p,q):p.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
def rel(p):return p.resolve().relative_to(R.resolve()).as_posix()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
B=read(V/'BOOK_BASELINE.json');old={p['page']:p for p in B['pages']};jobs=read(V/'generation_jobs.json')['jobs']
native_names={'dusty_chest':'exec-6885ca8d-055e-4e5f-9ce6-5411e3b81c0d.png','shell_cobweb':'exec-cf607e56-defe-41bb-8d74-95e1ea700edb.png','dirty_bank04':'exec-1b291204-ad85-4470-82e3-e8c9d818c6f6.png','clean_room30':'exec-1ab86eba-f8be-4822-8053-9fa6052f2e00.png','dusty_chest_clean':'exec-d7e3c749-24b1-4992-a834-ff1104f6ecc7.png'}
files={'dusty_chest':'dusty_chest_attempt1.png','dusty_chest_clean':'dusty_chest_attempt2.png'}
for j in jobs:
 k=j['id'];p=V/'art'/files.get(k,k+'.png');im=Image.open(p)
 B['sources']['v32_'+k]=dict(file=p.relative_to(L).as_posix(),native_size=list(im.size),sha256=sha(p),provenance=dict(method='Built-in image_gen source-bound local derivative',prompt_sha256=j['prompt_sha256'],references=j['reference_hashes'],source_preserved=True,native_path=rel(p),native_sha256=sha(p)))
# The first extraction retained a diffuse halo. The book uses its original
# object pixels ONLY through a tight irregular PDF contour, never that halo.
alpha=Image.open(V/'art/dusty_chest_attempt1.png').getchannel('A')
# Measure the existing opaque source contour; only PDF path coordinates result.
# Neither native RGB nor native alpha pixels are changed or recompressed.
rows=[]
for y in range(alpha.height):
 xs=[x for x in range(alpha.width) if alpha.getpixel((x,y))>=200]
 if xs:rows.append((y,min(xs),max(xs)))
edge_rows=rows[::2]
if edge_rows[-1]!=rows[-1]:edge_rows.append(rows[-1])
chest_contour=[[left,y] for y,left,right in edge_rows]+[[right,y] for y,left,right in reversed(edge_rows)]
B['sources']['v32_dusty_chest']['alpha_box']=[min(x for x,y in chest_contour),min(y for x,y in chest_contour),max(x for x,y in chest_contour)+1,max(y for x,y in chest_contour)+1]
B['sources']['v32_dusty_chest']['contour_polygon']=chest_contour
B['sources']['v32_dusty_chest']['provenance']['contour_measurement']='Existing alpha>=200 outer row envelope sampled every2rows, projected only as a PDF clip; native raster/alpha unchanged. Native source-alpha edge values exclude the diffuse background backing.'
B['sources']['v32_dusty_chest']['provenance']['delivery']='Only the documented contour is visible in the PDF. The native halo-bearing raster is preserved and is not a standalone accepted alpha asset.'
bank_polys=[[[159,909],[179,893],[259,893],[346,910],[375,940],[388,1007],[367,1040],[218,1041],[170,1014]],[[1062,929],[1113,902],[1236,900],[1261,930],[1268,1002],[1229,1034],[1064,1034]]]
room_poly=[[790,575],[817,558],[862,562],[909,595],[928,599],[926,475],[923,412],[922,344],[937,303],[972,283],[982,257],[1039,256],[1073,277],[1104,307],[1158,333],[1176,354],[1182,400],[1166,453],[1120,479],[1094,500],[1104,530],[1146,546],[1188,568],[1202,616],[1180,641],[1113,642],[1073,671],[1046,694],[1013,715],[969,739],[927,749],[878,745],[837,732],[802,704],[790,670],[804,636],[807,606]]
def patch(k,poly):return dict(source='v32_'+k,reference_size=[1484,1060],polygon=poly)
new4=dict(page=4,mode='C',art=['v32_shell_cobweb','v32_dusty_chest'],layout='placements',text='Cobwebs in the corners.\nDust on the chest!',border_assets=[],border_placements=[],integrated_background='v29_bank30_tiny',background_patches=[patch('dirty_bank04',poly) for poly in bank_polys],background_theme='A close inspection of existing dusty castle belongings. One tiny curious curl-ear bunny peeks beside a dusty book, with lightly dusty open book/lamp opposite. No anonymous dust smear or repeated brushes.',integrated_motifs=['curious_book_bunny','dusty_closed_castle_book','dusty_open_castle_book','dusty_shell_lamp'],integrated_prop_bounds=[[.118,.856,.074,.087],[.167,.891,.087,.079],[.725,.912,.091,.063],[.805,.870,.050,.079]],marginal_bunny_count=1,foreground_zone=[30,53,444,211],placements=[dict(source='v32_shell_cobweb',box=[59,181,261,93]),dict(source='v32_dusty_chest',box=[298,64,158,132])],caption=dict(x=32,y=316,width=440,size=20,align='center',color='navy',shadow=False,halo=False,outline=0),focal_exclusions=[],original_page='castle_inspection',beat='dirty_castle_belongings',bounds_note='Visible native subject annotations; the native low-bank derivative supplies bounded regions only.')
pages=[];mapping=[]
for n in range(1,33):
 baseline=n if n<=3 or 23<=n<=29 or n==32 else n-1 if 5<=n<=22 else 22 if n==30 else 30 if n==31 else None
 p=copy.deepcopy(new4 if n==4 else old[baseline]);p['page']=n
 if n==13:
  p.pop('local_patches',None);p['text']='“Rainbow colors!” said Roshan.\nShe kept clearing the gunk.';p['background_theme']='Exact restored source: rainbow colors emerge while gunk still hides the remaining bands. No ordinary-aqua replacement and no stream count.'
 if n==14:
  p['text']='Whoosh! The waterfall turned rainbow!\n“This swimming pool is magic,” said Daddy.\n“It makes the water rainbow-colored!”';p['caption']['y']=84;p['focal_exclusions']=[[0,115,504,245]]
 if n==22:p['text']='Roshan put the paints in their places.\nThen she scrubbed the table. Scrub, scrub!'
 if n==30:
  p['text']='Pearl Castle was clean again.\nIt was time to rest.';p.setdefault('local_patches',[]).append(patch('clean_room30',room_poly));p['background_theme']='Quiet result of the already completed cleaning: remove only the source Roshan/held brush footprint and fill their local wall/floor/table gap; no new room or action.';p['beat']='clean_castle_closing'
 if n==31:
  rest=old[31]
  for k in ['integrated_background','background_patches','integrated_motifs','integrated_prop_bounds','marginal_bunny_count','bounds_note']:p[k]=copy.deepcopy(rest[k])
  p['text']='“We helped your rainbow shine!” said Roshan.\n“Thank you!” said Grand Puff.\n“Come and rest with us!” said Roshan.'
  p['placements'][0]['box']=[276,56,196,200];p['placements'][1]['box']=[62,86,146,163]
  face=copy.deepcopy(rest['local_patches'][0]);face['placement']=copy.deepcopy(p['placements'][1]);p['local_patches']=[face]
  p['background_theme']='Combined rainbow reflection, grateful Puff and invitation to rest. Existing attentive Roshan contour, grateful Puff face and sleepy toy banks unite the former30/31 beats; no second static exchange page.';p['beat']='rainbow_gratitude_and_belonging'
 pages.append(p);mapping.append(dict(new_page=n,baseline_page=baseline,status='NEW_INSERT' if baseline is None else 'REVISED' if n in [13,14,22,30,31] else 'EXACT_REUSE'))
B['pages']=pages;B['revision']='V32 rainbow magic and story space';B['status']='V32 complete review proof; external acceptance pending';B['review_href']='../AUDIT_REVIEW.html'
save(L/'book.json',B);save(V/'BOOK_CURRENT.json',B)
save(V/'pagination.json',dict(total_pages=34,story_pages=32,rows=mapping,merged_baseline_pages=[30,31],removed_standalone_baseline_page=31,compensation='Former clean art-room outcome22 becomes quiet clean-castle closing30, keeping the23→24 and27→28 reveal turns.',changed_new_pages=[4,13,14,22,30,31],unchanged_mapped_pages=[r['new_page'] for r in mapping if r['status']=='EXACT_REUSE'],reveal_turns=[[23,24],[27,28]],lamma_pages=[10,'back_cover']))
e=[]
for j in jobs:
 k=j['id'];p=V/'art'/files.get(k,k+'.png');im=Image.open(p)
 e.append(dict(id=k,generation_method='built-in image_gen',attempt=2 if k=='dusty_chest_clean' else 1,prompt=j['prompt'],prompt_sha256=j['prompt_sha256'],references=j['reference_hashes'],native_output=dict(path=rel(p),sha256=sha(p),dimensions=list(im.size),mode=im.mode),original_tool_filename=native_names[k],selection='REJECTED_ALPHA_ASSET' if k in ['dusty_chest','dusty_chest_clean'] else 'SELECTED_LOCAL_DERIVATIVE',delivery='First chest candidate is used only for a document-level exact contour extraction; both candidates fail standalone alpha due to residual diffuse backing.' if 'chest' in k else 'Only declared low-bank polygons' if k=='dirty_bank04' else 'Only declared removed-character/brush gap polygon' if k=='clean_room30' else 'Complete authored object group with true alpha',delivery_polygons=bank_polys if k=='dirty_bank04' else [room_poly] if k=='clean_room30' else [chest_contour] if k=='dusty_chest' else [],delivery_pages=[30] if k=='clean_room30' else [4],review='PENDING final native composed-page review'))
save(V/'generation_evidence.json',dict(baseline=read(V/'REVISION_SCOPE.json')['baseline'],generated_count=5,selected_delivery_components=4,rejected_standalone_alpha_candidates=2,generated=e,meaning='No full-scene redraw. Existing original scenes and source rasters preserved; local PDF patches/contour isolation determine delivery pixels.'))
print(json.dumps(dict(changed_pages=[4,13,14,22,30,31],total_pages=34)))
