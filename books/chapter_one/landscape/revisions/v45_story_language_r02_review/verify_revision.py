"""Exact V45 words, unchanged pages/art and original composed-caption thresholds."""
from pathlib import Path
from collections import Counter
import json,hashlib,subprocess
from pypdf import PdfReader,PdfWriter
from pypdf.generic import ContentStream
import pypdfium2 as pdfium
from PIL import Image
import numpy as np
V=Path(__file__).resolve().parent;L=V.parents[1];R=V.parents[4];C=V/'complete';T=R/'tmp/pdfs/v45';T.mkdir(parents=True,exist_ok=True)
read=lambda p:json.loads(p.read_text('utf8'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
save=lambda p,d:p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
words=lambda s:' '.join(s.split())
b=read(V/'BOOK_CURRENT.json');old=read(V/'BOOK_BASELINE.json');m=read(R/'books/chapter_one/handoffs/2026-10-31_v45_story_language/MANUSCRIPT.json');scope=read(V/'revision_scope.json');changed=scope['changed_pages'];issues=[]
assert b==read(L/'book.json')
assert set(changed)=={q['page'] for q in m['pages'] if q['changed']}-set(scope['held_words_pages'])
assert scope['held_words_pages']==[11,15]
for k in old:
 if k not in ['pages','revision','download_pdf_href']:assert b[k]==old[k],k
for q in read(V/'source_seals.json')['files']:assert sha(R/q['path'])==q['sha256'],q['path']
assert b['sources']==old['sources'] and b['cover']==old['cover'] and b['back_cover']==old['back_cover'] and b['font']==old['font']
for n,(p,q,s) in enumerate(zip(b['pages'],old['pages'],m['pages']),1):
 assert p['page']==q['page']==s['page']==n
 if n in scope['held_words_pages']:assert p==q,n
 else:assert words(p['text'])==words(s['v45_text']),n
 if not s['changed']:assert p==q,n
 assert {k:v for k,v in p.items() if k not in ['text','caption','speech_bubbles']}=={k:v for k,v in q.items() if k not in ['text','caption','speech_bubbles']},n
 assert p['caption']['size']==q['caption']['size']==20
 if n==21:
  assert [words(x['text']) for x in p['speech_bubbles']]==[words(x) for x in s['v45_bubbles']]
  assert [{k:v for k,v in x.items() if k!='text'} for x in p['speech_bubbles']]==[{k:v for k,v in x.items() if k!='text'} for x in q['speech_bubbles']]
 else:assert p.get('speech_bubbles')==q.get('speech_bubbles'),n
baseline=L/'revisions/v44_door_and_consistency/complete/Mermaid_Roshan_and_the_Dust_Bunnies_V44.pdf';current=C/'Mermaid_Roshan_Book_V45.pdf';email=C/'Mermaid_Roshan_Book_V45_Email.pdf'
assert current.read_bytes()==email.read_bytes() and email.stat().st_size<=25000000
a,z=PdfReader(baseline),PdfReader(current);assert len(a.pages)==len(z.pages)==34
assert [p.mediabox for p in a.pages]==[p.mediabox for p in z.pages]
oldlines=read(L/'revisions/v42_doublewide_arrival/complete/page_provenance.json')['text_lines']
oldlines=[q for q in oldlines if q['page']!='front_cover']+read(L/'revisions/v44_door_and_consistency/complete/cover_provenance.json')['text_lines']
newlines=[q for q in oldlines if q['page'] not in changed]+read(C/'caption_provenance.json')['text_lines']
for n in changed:
 expected=words(b['pages'][n-1]['text']);actual=[q['text'] for q in read(C/'caption_provenance.json')['text_lines'] if q['page']==n and q['font_size']==20]
 assert words(' '.join(actual))==expected,(n,actual,expected)
 # Extracted text has the exact expected punctuation/words (line wraps ignored).
 # Existing halo method paints the same glyphs once for stroke and once for
 # fill. Extraction repeats those draw strings; do not mistake them for two
 # visually separate captions or silently weaken the manuscript comparison.
 drawlines=[q for q in read(C/'caption_provenance.json')['text_lines'] if q['page']==n]
 expected_full=' '.join(q['text']*(2 if q.get('halo') else 1) for q in drawlines)
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
print('34/34 art-only and outside-caption pixels exact;'+str(len(scope['unchanged_pdf_pages']))+' unchanged entries exact',flush=True)
def lum(a):
 a=np.asarray(a,dtype=float)/255;a=np.where(a<=.04045,a/12.92,((a+.055)/1.055)**2.4);return a@np.array([.2126,.7152,.0722])
fills={'navy':float(lum([15.3,40.8,73.95])),'white':float(lum([255,255,249.9]))}
def contrast(lines,doc):
 imgs={};out=[]
 for q in lines:
  n=0 if q['page']=='front_cover' else 33 if q['page']=='back_cover' else q['page']
  if n not in imgs:imgs[n]=lum(doc[n].render(scale=1.5).to_pil().convert('RGB'))
  x,y,w,h=q['box'];sample=imgs[n][max(0,int((360-y-h)*3)):min(1080,int((360-y)*3)),max(0,int(x*3)):min(imgs[n].shape[1],int((x+w)*3))]
  if not sample.size:issues.append('Empty caption '+str(q));continue
  f=fills[q['color']];ratio=lambda v:(max(f,v)+.05)/(min(f,v)+.05)
  typical=ratio(float(np.median(sample)));worst=ratio(float(np.quantile(sample,.9 if q['color']=='white' else .1)))
  verdict='FAIL' if worst<3 else 'OUTLINE_REQUIRED' if typical<4.5 else 'PASS'
  out.append(dict(**q,typical=round(typical,3),worst=round(worst,3),verdict=verdict))
 return dict(lines=out,counts={k:sum(q['verdict']==k for q in out) for k in ['PASS','OUTLINE_REQUIRED','FAIL']})
basecheck=contrast(oldlines,aa);check=contrast(newlines,bb)
for q in check['lines']:
 if q['verdict']=='FAIL':issues.append('Contrast FAIL '+str(q['page'])+' '+q['text'])
 if q['verdict']=='OUTLINE_REQUIRED' and not(q.get('outline',0)>=1 or q.get('halo')):issues.append('Missing heavier outline '+str(q['page'])+' '+q['text'])
 x,y,w,h=q['box'];margin=18 if isinstance(q['page'],str) else 24
 if x<margin or y<margin or x+w>(1008 if q['page']==2 else 504)-margin or y+h>360-margin:issues.append('Caption inset '+str(q['page'])+' '+q['text'])
review=read(V/'visual_audits.json');assert review['reading_sha256']==sha(current) and review['email_sha256']==sha(email)
assert len(review['passes'])==5 and review['held']==[11,15]
for q in review['passes']:
 assert q['result']=='PASS_IMPLEMENTED_SCOPE_WITH_HELD11_AND15' and not q['remaining_implemented_scope_defects']
 for path in q['inspected']:assert sha(V/path)==q['inspected_sha256'][path],path
save(V/'composed_caption_contrast.json',dict(method='Unchanged V37/V42 fill/median/worst-decile thresholds on actual caption-free delivery PDF. Stroke excluded. PASS typical>=4.5;OUTLINE_REQUIRED typical<4.5 with worst>=3;FAIL worst<3.',v44=basecheck,v45=check))
save(C/'verification.json',dict(status='FAIL' if issues else 'PASS_IMPLEMENTED_SCOPE_WITH_DECLARED_HELD_PAGE',reading_sha256=sha(current),email_sha256=sha(email),bytes=email.stat().st_size,exact_changed_captions=len(changed),held_words_pages=scope['held_words_pages'],unchanged_pdf_entries=scope['unchanged_pdf_pages'],all34=rows,contrast_v44=basecheck['counts'],contrast_v45=check['counts'],issues=issues,held=['Stories11and15 longer captions await shorter supplied words','Owner new story facts/illustrations','Child spoken read-aloud/qualified SLP','V44 geography/fountain','Physical print,arrival imposition/gutter and V41printPart2']))
print('V44 contrast',basecheck['counts'],'V45',check['counts']);print('\n'.join(issues) or 'Words/art/contrast/insets ALL OK')
if issues:raise SystemExit(1)
