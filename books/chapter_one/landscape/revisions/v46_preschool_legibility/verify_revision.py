"""Revised words, preserved artwork, actual opaque ink painting and unchanged contrast floors."""
from pathlib import Path
from collections import Counter
import json,hashlib,subprocess,sys
from pypdf import PdfReader,PdfWriter
from pypdf.generic import ContentStream
import pypdfium2 as pdfium
from PIL import Image
import numpy as np
V=Path(__file__).resolve().parent;L=V.parents[1];R=V.parents[4];C=V/'complete';T=R/'tmp/pdfs/v46';T.mkdir(parents=True,exist_ok=True)
read=lambda p:json.loads(p.read_text('utf8'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
save=lambda p,d:p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
words=lambda s:' '.join(s.split())
b=read(V/'BOOK_CURRENT.json');old=read(V/'BOOK_BASELINE.json');m=read(V/'manuscript.json');scope=read(V/'revision_scope.json');changed=scope['changed_pages'];issues=[]
assert b==read(L/'book.json') and changed==list(range(34)) and scope['held_words_pages']==[]
for k in old:
 if k not in ['pages','revision','download_pdf_href','lettering_profile']:assert b[k]==old[k],k
for q in read(V/'source_seals.json')['files']:assert sha(R/q['path'])==q['sha256'],q['path']
assert b['sources']==old['sources'] and b['cover']==old['cover'] and b['back_cover']==old['back_cover'] and b['font']==old['font']
for n,(p,q,t) in enumerate(zip(b['pages'],old['pages'],m['pages']),1):
 assert p['page']==q['page']==t['page']==n
 assert words(p['text'])==words(t['after']) and words(q['text'])==words(t['before']),n
 assert {k:v for k,v in p.items() if k not in ['text','caption']}=={k:v for k,v in q.items() if k not in ['text','caption']},n
 assert p['caption']['size']==q['caption']['size']==20
 assert p.get('speech_bubbles')==q.get('speech_bubbles'),n
baseline=L/'revisions/v44_door_and_consistency/complete/Mermaid_Roshan_and_the_Dust_Bunnies_V44.pdf';current=C/'Mermaid_Roshan_Book_V46.pdf';email=C/'Mermaid_Roshan_Book_V46_Email.pdf'
assert current.read_bytes()==email.read_bytes() and email.stat().st_size<=25000000
a,z=PdfReader(baseline),PdfReader(current);assert len(a.pages)==len(z.pages)==34
assert [p.mediabox for p in a.pages]==[p.mediabox for p in z.pages]
oldlines=read(L/'revisions/v42_doublewide_arrival/complete/page_provenance.json')['text_lines']
oldlines=[q for q in oldlines if q['page']!='front_cover']+read(L/'revisions/v44_door_and_consistency/complete/cover_provenance.json')['text_lines']
newlines=read(C/'caption_provenance.json')['text_lines']
for n in range(1,33):
 expected=words(b['pages'][n-1]['text']);actual=[q['text'] for q in read(C/'caption_provenance.json')['text_lines'] if q['page']==n and q['font_size']==20]
 assert words(' '.join(actual))==expected,(n,actual,expected)
 # Extracted text has the exact expected punctuation/words (line wraps ignored).
 # Existing halo method paints the same glyphs once for stroke and once for
 # fill. Extraction repeats those draw strings; do not mistake them for two
 # visually separate captions or silently weaken the manuscript comparison.
 drawlines=[q for q in read(C/'caption_provenance.json')['text_lines'] if q['page']==n]
 expected_full=' '.join(q['text']*(2 if q.get('halo') or q['color']=='white' else 1) for q in drawlines)
 assert words(z.pages[n].extract_text())==words(expected_full),(n,z.pages[n].extract_text(),expected_full)
def art_only(reader,path):
 w=PdfWriter()
 for p in reader.pages:
  q=w.add_page(p);cs=ContentStream(q.get_contents(),w);ops=[];inside=False
  for args,op in cs.operations:
   if op==b'BT':inside=True
   elif op==b'ET':inside=False
   elif not inside:ops.append((args,op))
  cs.operations=ops;q.replace_contents(cs)
 with path.open('wb') as f:w.write(f)
art_only(a,T/'baseline_art.pdf');art_only(z,T/'current_art.pdf')
aa,bb=pdfium.PdfDocument(str(T/'baseline_art.pdf')),pdfium.PdfDocument(str(T/'current_art.pdf'));da,dz=pdfium.PdfDocument(str(baseline)),pdfium.PdfDocument(str(current));rows=[]
for i in range(34):
 images=0
 for name,val in a.pages[i]['/Resources'].get('/XObject',{}).items():
  u=val.get_object()
  if u.get('/Subtype')!='/Image':continue
  v=z.pages[i]['/Resources']['/XObject'][name].get_object()
  assert u._data==v._data and u['/Width']==v['/Width'] and u['/Height']==v['/Height'] and u.get('/Filter')==v.get('/Filter'),(i,name)
  if u.get('/SMask'):assert u['/SMask'].get_object()._data==v['/SMask'].get_object()._data,(i,name,'alpha')
  images+=1
 x=np.asarray(aa[i].render(scale=1.5).to_pil().convert('RGB'));y=np.asarray(bb[i].render(scale=1.5).to_pil().convert('RGB'));assert np.array_equal(x,y),('Art pixels',i)
 oldim=np.asarray(da[i].render(scale=1.5).to_pil().convert('RGB'));newim=np.asarray(dz[i].render(scale=1.5).to_pil().convert('RGB'));mask=np.zeros(newim.shape[:2],bool)
 for q in oldlines+newlines:
  n=0 if q['page']=='front_cover' else 33 if q['page']=='back_cover' else q['page']
  if n!=i:continue
  x0,y0,w,h=q['box'];pad=6
  mask[max(0,int((360-y0-h)*3)-pad):min(1080,int((360-y0)*3)+pad),max(0,int(x0*3)-pad):min(mask.shape[1],int((x0+w)*3)+pad)]=True
 assert not np.any(np.any(oldim!=newim,axis=2)&~mask),('Outside caption',i)
 if i not in changed:
  assert np.array_equal(oldim,newim),('Unchanged',i)
  assert a.pages[i].get_contents().get_data()==z.pages[i].get_contents().get_data(),i
  assert a.pages[i].extract_text()==z.pages[i].extract_text(),i
 rows.append(dict(pdf_entry=i,caption_free_pixels_exact=True,outside_caption_pixels_exact=True,native_image_streams_and_alpha_exact=True,image_count=images,unchanged_entry_exact=i not in changed))
print('34/34 art-only and outside-caption pixels exact;'+'0 unchanged text entries; art preserved on all entries',flush=True)
def lum(a):
 a=np.asarray(a,dtype=float)/255;a=np.where(a<=.04045,a/12.92,((a+.055)/1.055)**2.4);return a@np.array([.2126,.7152,.0722])
fills={'navy':float(lum([15.3,40.8,73.95])),'white':float(lum([255,255,249.9]))}
def contrast(lines,doc,fill_map):
 imgs={};out=[]
 for q in lines:
  n=0 if q['page']=='front_cover' else 33 if q['page']=='back_cover' else q['page']
  if n not in imgs:imgs[n]=lum(doc[n].render(scale=1.5).to_pil().convert('RGB'))
  x,y,w,h=q['box'];sample=imgs[n][max(0,int((360-y-h)*3)):min(1080,int((360-y)*3)),max(0,int(x*3)):min(imgs[n].shape[1],int((x+w)*3))]
  if not sample.size:issues.append('Empty caption '+str(q));continue
  f=fill_map[q['color']];ratio=lambda v:(max(f,v)+.05)/(min(f,v)+.05)
  typical=ratio(float(np.median(sample)));worst=ratio(float(np.quantile(sample,.9 if q['color']=='white' else .1)))
  verdict='FAIL' if worst<3 else 'OUTLINE_REQUIRED' if typical<4.5 else 'PASS'
  out.append(dict(**q,typical=round(typical,3),worst=round(worst,3),verdict=verdict))
 return dict(lines=out,counts={k:sum(q['verdict']==k for q in out) for k in ['PASS','OUTLINE_REQUIRED','FAIL']})
newfills={k:float(lum(np.array(b['lettering_profile'][k+'_rgb'])*255)) for k in ['navy','white']}
basecheck=contrast(oldlines,aa,fills);check=contrast(newlines,bb,newfills)
for q in check['lines']:
 if q['verdict']=='FAIL':issues.append('Contrast FAIL '+str(q['page'])+' '+q['text'])
 if q['verdict']=='OUTLINE_REQUIRED' and not(q.get('outline',0)>=1 or q.get('halo')):issues.append('Missing heavier outline '+str(q['page'])+' '+q['text'])
 x,y,w,h=q['box'];margin=18 if isinstance(q['page'],str) else 24
 if x<margin or y<margin or x+w>(1008 if q['page']==2 else 504)-margin or y+h>360-margin:issues.append('Caption inset '+str(q['page'])+' '+q['text'])
# Inspect actual PDF painting, not only the author's requested opacity.
from reportlab.pdfbase.ttfonts import TTFont
font=TTFont('GlyphAudit',str(L/b['font']));cmap=font.face.charToGlyph;chars=set(''.join(q['text'] for q in newlines));missing=[ord(q) for q in chars if not q.isspace() and ord(q) not in cmap];assert not missing,missing
save(V/'font_glyph_audit.json',dict(status='PASS',font_sha256=sha(L/b['font']),used_codepoints=sorted(ord(q) for q in chars if not q.isspace()),missing_codepoints=missing))
paint=[]
for n,page in enumerate(z.pages):
 state=dict(fill_alpha=1.,stroke_alpha=1.,fill_rgb=(0.,0.,0.),stroke_rgb=(0.,0.,0.),line_width=1.,mode=0,font_size=0.);stack=[];events=[]
 for args,op in ContentStream(page.get_contents(),z).operations:
  if op==b'q':stack.append(state.copy())
  elif op==b'Q':state=stack.pop()
  elif op==b'rg':state['fill_rgb']=tuple(map(float,args))
  elif op==b'RG':state['stroke_rgb']=tuple(map(float,args))
  elif op==b'w':state['line_width']=float(args[0])
  elif op==b'Tr':state['mode']=int(args[0])
  elif op==b'Tf':state['font_size']=float(args[1])
  elif op==b'gs':
   g=page['/Resources']['/ExtGState'][args[0]].get_object()
   if '/ca' in g:state['fill_alpha']=float(g['/ca'])
   if '/CA' in g:state['stroke_alpha']=float(g['/CA'])
  elif op in [b'Tj',b'TJ']:events.append(state.copy())
 lines=[q for q in newlines if (0 if q['page']=='front_cover' else 33 if q['page']=='back_cover' else q['page'])==n];j=0
 for q in lines:
  profile=b['lettering_profile'];ink=profile[q['color']+'_rgb'];backed=q['color']=='white' or q.get('halo')
  if backed:
   e=events[j];j+=1;assert e['mode']==1 and e['stroke_alpha']==1,(n,'backing',e)
   assert np.allclose(e['stroke_rgb'],profile['navy_rgb' if q['color']=='white' else 'white_rgb']),n
  e=events[j];j+=1
  assert e['mode']==2 and e['fill_alpha']==e['stroke_alpha']==1,(n,'opaque fill above backing',e)
  assert np.allclose(e['fill_rgb'],ink) and np.allclose(e['stroke_rgb'],ink),(n,e)
  assert abs(e['line_width']-profile['ink_stroke'])<1e-6 and e['font_size']==q['font_size'],n
 assert j==len(events),(n,j,len(events))
 paint.append(dict(pdf_entry=n,lines=len(lines),actual_paint_events=len(events),opaque_fill_and_stroke=True,separate_backing_precedes_ink=True))
save(V/'lettering_paint_audit.json',dict(status='PASS',profile=b['lettering_profile'],method='Actual page content operators and ExtGState stack; defaults1, gs ca/CA, q/Q, Tr, Tf, stroke/fill RGB and width. Every backing stroke is followed by opaque same-colour filled ink.',pages=paint))
review_path=V/'visual_audits.json'
if '--draft' not in sys.argv:assert review_path.exists(), 'Final five-pass visual record required'
if review_path.exists():
 review=read(review_path);assert review['reading_sha256']==sha(current) and review['email_sha256']==sha(email)
 assert len(review['passes'])==5
 for q in review['passes']:
  assert q['result']=='PASS' and not q['remaining_new_defects']
  for path in q['inspected']:assert sha(V/path)==q['inspected_sha256'][path],path
save(V/'composed_caption_contrast.json',dict(method='Unchanged V37/V42 median/worst-decile method on actual caption-free PDF; actual V46 ink RGB used; backing excluded. PASS median>=4.5, OUTLINE_REQUIRED median<4.5 with worst>=3, FAIL worst<3.',v44=basecheck,v46=check))
save(C/'verification.json',dict(status='FAIL' if issues else 'PASS_MACHINE_SCOPE',reading_sha256=sha(current),email_sha256=sha(email),bytes=email.stat().st_size,revised_caption_count=len(scope['text_changed_pages']),all34=rows,contrast_v44=basecheck['counts'],contrast_v46=check['counts'],issues=issues,held=['Actual owner/child spoken read-aloud and qualified SLP','V44 geography/fountain art continuity','Physical print, arrival imposition/gutter and V41printPart2']))
print('V44 contrast',basecheck['counts'],'V46',check['counts']);print('Actual paint order/opaque ink PASS');print('\n'.join(issues) or 'Words/art/contrast/insets ALL OK')
if issues:raise SystemExit(1)
