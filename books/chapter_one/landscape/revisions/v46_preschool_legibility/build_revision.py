"""Replace only text over the exact V44 PDF artwork; no image re-encoding."""
from pathlib import Path
import json,sys,hashlib,shutil
from io import BytesIO
from pypdf import PdfReader,PdfWriter
from pypdf.generic import ContentStream
import pypdfium2 as pdfium
V=Path(__file__).resolve().parent;L=V.parents[1];R=V.parents[4];C=V/'complete'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
old=L/'revisions/v44_door_and_consistency/complete/Mermaid_Roshan_and_the_Dust_Bunnies_V44.pdf'
b=json.loads((V/'BOOK_CURRENT.json').read_text('utf8'));baseline=json.loads((V/'BOOK_BASELINE.json').read_text('utf8'))
changed=json.loads((V/'revision_scope.json').read_text('utf8'))['changed_pages']
scratch=R/'tmp/pdfs/v46';scratch.mkdir(parents=True,exist_ok=True)
source=L/'render_book.py';program=source.read_text('utf8');program=program[:program.index('# Covers remain part')]
sys.argv=['render_book.py','--book',str(V/'BOOK_CURRENT.json'),'--output',str(scratch)]
env={'__file__':str(source),'__name__':'__main__'};exec(compile(program,str(source),'exec'),env)
c=env['c'];S=env['S'];text=env['text'];metrics=env['pdfmetrics']
for i in range(34):
 w=1008 if i==2 else 504;c.setPageSize((w*S,360*S))
 if i>0:c.scale(S,S)
 env['PAGE']=i
 env['PAGE']='front_cover' if i==0 else 'back_cover' if i==33 else i
 if i==0:
  for q in b['cover']['title_lines']:
   text(q['text'],q['x'],q['y'],q['width'],q['size'],True)
  q=b['cover'].get('subtitle')
  if q and q['text']:text(q['text'],q['x'],q['y'],q['width'],q['size'],q.get('align','center')=='center',color=q.get('color','navy'),right=q.get('align')=='right')
 elif i==33:
  q=b['back_cover'].get('caption')
  if q:text(q['text'],q['x'],q['y'],q['width'],q['size'],True,halo=q.get('halo',False),color=q['color'],outline=q.get('outline',0))
 else:
  p=b['pages'][i-1];q=p['caption'];text(p['text'],q['x'],q['y'],q['width'],q['size'],q['align']=='center',color=q['color'],shadow=q['shadow'],halo=q.get('halo',False),outline=q.get('outline',0),leading=q.get('leading'))
  for q in p.get('speech_bubbles',[]):
   x,y,w,h=q['box'];size=18;leading=size*1.3;count=len(q['text'].split('\n'));asc=metrics.getAscent('Sniglet')*size/1000;desc=metrics.getDescent('Sniglet')*size/1000
   yy=y+h/2+((count-1)*leading-asc-desc)/2
   text(q['text'],x+12,yy,w-24,size,True)
 c.showPage()
c.save();overlay=PdfReader(scratch/'Mermaid_Roshan_LANDSCAPE_ROUGH.pdf');reader=PdfReader(old);writer=PdfWriter()
for i,p in enumerate(reader.pages):
 page=writer.add_page(p)
 if i not in changed:continue
 stream=ContentStream(page.get_contents(),writer);ops=[];inside=False
 for operands,operator in stream.operations:
  if operator==b'BT':inside=True
  elif operator==b'ET':inside=False
  elif not inside:ops.append((operands,operator))
 stream.operations=ops;page.replace_contents(stream);page.merge_page(overlay.pages[i])
writer.add_metadata({'/Title':b['title'],'/Author':'Mermaid Roshan picture-book project','/Subject':'V46 preschool copy and solid lettering review; V44 artwork preserved; solid opaque lettering on all entries; print held'})
out=C/'Mermaid_Roshan_Book_V46.pdf'
with out.open('wb') as f:writer.write(f)
email=C/'Mermaid_Roshan_Book_V46_Email.pdf';shutil.copyfile(out,email)
assert out.stat().st_size<=25000000, out.stat().st_size
doc=pdfium.PdfDocument(str(out))
for i in range(34):doc[i].render(scale=1.5).to_pil().convert('RGB').save(C/f'page_{i:02}.png')
lines=env['TEXT_LINES'];(C/'caption_provenance.json').write_text(json.dumps(dict(method='Opt-in opaque solid-fill renderer profile; text-only overlay over V44 nontext operators/images/alpha; unchanged pages copied',baseline_pdf=str(old.relative_to(R)).replace('\\','/'),baseline_sha256=sha(old),text_lines=lines),indent=2)+'\n',encoding='utf8',newline='\n')
(C/'export_record.json').write_text(json.dumps(dict(reading_sha256=sha(out),email_sha256=sha(email),bytes=out.stat().st_size,email_is_exact_reading_copy=True,image_reencoding=False,changed_pdf_entries=changed,source='V44 reading PDF; all image payloads and nontext vectors preserved',generation_calls=0),indent=2)+'\n',encoding='utf8',newline='\n')
import html
cards=[]
for i in range(34):
 label='Cover' if i==0 else 'Back cover' if i==33 else f'Story {i}';cards.append(f'<figure class="{"wide" if i==2 else "single"}"><figcaption>{label}</figcaption><img loading="lazy" src="page_{i:02}.png" alt="{label}"></figure>')
(C/'READ_BOOK.html').write_text('<!doctype html><meta charset="utf-8"><title>Mermaid Roshan V46</title><style>body{background:#193449;color:#e3f5ff;font:18px/1.5 system-ui;margin:24px}main{display:grid;grid-template-columns:1fr 1fr;gap:24px}.wide{grid-column:1/-1}figure{margin:0}img{width:100%}a{color:#9cddff}@media(max-width:800px){main{grid-template-columns:1fr}}</style><h1>'+html.escape(b['title'])+'</h1><p>V46 story/language draft:Short preschool read-aloud copy and solid lettering; no held-word pages.34 mixed-width entries; physical print, owner story facts and child/SLP review remain open.</p><p><a href="Mermaid_Roshan_Book_V46_Email.pdf">Email PDF</a> · <a href="../README.md">Scope and verification</a></p><main>'+''.join(cards)+'</main>',encoding='utf8',newline='\n')
print('V46 reading/email',out.stat().st_size,sha(out),';'+str(len(changed))+' text entries;34 actual proof PNGs')
