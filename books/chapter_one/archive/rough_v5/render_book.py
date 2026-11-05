from pathlib import Path
import json,html,hashlib,zipfile
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader, simpleSplit
import pypdfium2 as pdfium
from pypdf import PdfReader
O=Path(__file__).resolve().parent;B=json.loads((O/'book.json').read_text(encoding='utf-8'));W,H=B['page_size_points'];pdfmetrics.registerFont(TTFont('Sniglet',str(O/'fonts'/B['font'])))
PDF=O/'Mermaid_Roshan_REFERENCE_STYLE_ROUGH.pdf';c=canvas.Canvas(str(PDF),pagesize=(W,H));c.setTitle(B['title']);web=[];checks=[];used=set()
def path(k):used.add(k);return O/B['sources'][k]['file']
for page in B['pages']:
 n=page['story_page'];parts=[];text_rects=[];art_rects=[]
 if not page['layout'].startswith('full-art'):
  p=path(B['background']);c.drawImage(str(p),0,0,W,H);parts.append(f'<img class="bg" src="{p.relative_to(O).as_posix()}">')
 for bl in page['blocks']:
  if bl['type'] in ('image','spread'):
   p=path(bl['art']);im=Image.open(p);iw,ih=im.size
   if bl.get('source_crop'):
    left,top,right,bottom=bl['source_crop'];cw,ch=right-left,bottom-top;rx,ry,rw,rh=bl['rect'];scale=min(rw/cw,rh/ch);tx=rx+(rw-cw*scale)/2;ty=ry+(rh-ch*scale)/2;rect=[tx,ty,cw*scale,ch*scale];x=tx-left*scale;y=ty-(ih-bottom)*scale;w,h=iw*scale,ih*scale;op=bl['opacity'];cover=True
   elif bl['type']=='spread':
    scale=max(720/iw,504/ih);w,h=iw*scale,ih*scale;x=(720-w)/2-360*bl['side'];y=(504-h)/2;rect=[0,0,360,504];op=1;cover=True
   else:
    x,y,w,h=bl['rect'];rect=[x,y,w,h];op=bl['opacity'];cover=bl['fit']=='cover';scale=(max if cover else min)(w/iw,h/ih);dw,dh=iw*scale,ih*scale;x+=(w-dw)*bl['anchor'];y+=(h-dh)/2;w,h=dw,dh
   c.saveState();c.setFillAlpha(op)
   if cover:
    cp=c.beginPath();cp.rect(*rect);c.clipPath(cp,stroke=0,fill=0)
   c.drawImage(ImageReader(im),x,y,w,h,mask='auto');c.restoreState()
   src=p.relative_to(O).as_posix();parts.append(f'<div style="position:absolute;left:{rect[0]}pt;top:{H-rect[1]-rect[3]}pt;width:{rect[2]}pt;height:{rect[3]}pt;overflow:hidden"><img src="{src}" style="position:absolute;left:{x-rect[0]}pt;top:{rect[3]-(y-rect[1])-h}pt;width:{w}pt;height:{h}pt;opacity:{op}"></div>')
   checks.append({'story_page':n,'art':bl['art'],'image_rect':[x,y,w,h],'clip_rect':rect if cover else None,'source_crop':bl.get('source_crop'),'effective_ppi':round(iw/w*72,1),'role':'lower footing detail' if op<1 else 'main art'});art_rects.append([x,y,w,h])
  elif bl['type']=='text':
   t=bl['text'];top=bl['top'];size=bl['size'];x=bl['x'];w=bl['width'];leading=size*1.42;lines=[part for line in t.splitlines() for part in simpleSplit(line,'Sniglet',size,w)];t='\n'.join(lines);bottom=top-(len(lines)-1)*leading-size*.3
   assert bottom>20,(n,t,bottom)
   for line in lines:assert pdfmetrics.stringWidth(line,'Sniglet',size)<=w+.1,(n,line,w)
   if bl['wash']:
    c.saveState();c.setFillAlpha(.90);c.setFillColor(HexColor('#effaf9'));c.rect(0,bottom-15,360,top-bottom+size+25,stroke=0,fill=1);c.restoreState();parts.append(f'<div style="position:absolute;left:0;top:{H-top-size-10}pt;width:360pt;height:{top-bottom+size+25}pt;background:rgba(239,250,249,.9)"></div>')
   c.setFillColor(HexColor('#242776'));c.setFont('Sniglet',size)
   for j,line in enumerate(lines):
    if bl['align']=='center':c.drawCentredString(x+w/2,top-j*leading,line)
    else:c.drawString(x,top-j*leading,line)
   parts.append(f'<p contenteditable style="left:{x}pt;top:{H-top-size*.94}pt;width:{w}pt;font-size:{size}pt;line-height:1.42;text-align:{bl["align"]}">{html.escape(t)}</p>');text_rects.append([x,bottom,w,top-bottom+size])
 if 1<=n<=40:
  c.setFillColor(HexColor('#596b78'));c.setFont('Sniglet',6);c.drawCentredString(180,12,str(n));parts.append(f'<span class="num">{n}</span>')
 web.append('<section class="page">'+''.join(parts)+'</section>');c.showPage()
c.save()
css='@font-face{font-family:Sniglet;src:url(fonts/Sniglet-Regular.ttf)}@page{size:5in 7in;margin:0}body{margin:0;background:#bed4d4;color:#242776;font-family:Sniglet}.page{position:relative;width:360pt;height:504pt;margin:20pt auto;overflow:hidden;break-after:page}.bg{position:absolute;inset:0;width:100%;height:100%}.page p{position:absolute;white-space:pre-line;margin:0}.num{position:absolute;bottom:8pt;text-align:center;width:100%;font-size:6pt;color:#596b78}.bar{padding:16px;text-align:center;background:#242776;color:white}@media print{.bar{display:none}.page{margin:0}}'
js="function saveText(){let a=document.createElement('a');a.href=URL.createObjectURL(new Blob([JSON.stringify([...document.querySelectorAll('.page')].map((p,i)=>({pdf_page:i+1,text:[...p.querySelectorAll('p')].map(x=>x.innerText)})),null,2)],{type:'application/json'}));a.download='edited_text.json';a.click()}"
(O/'EDITABLE_BOOK.html').write_text('<!doctype html><meta charset="utf-8"><title>'+B['title']+'</title><style>'+css+'</style><div class="bar">Click text to edit. <button onclick="saveText()">Save text</button> <button onclick="print()">Print</button></div>'+''.join(web)+'<script>'+js+'</script>',encoding='utf-8')
(O/'page_art_provenance.json').write_text(json.dumps({'sources':{k:B['sources'][k] for k in sorted(used)},'placements':checks},indent=2),encoding='utf-8')
(O/'rendered').mkdir(exist_ok=True);doc=pdfium.PdfDocument(str(PDF))
for i,p in enumerate(doc):p.render(scale=1.5).to_pil().convert('RGB').save(O/'rendered'/f'page_{i:02}.jpg',quality=94)
for start in range(0,len(doc),12):
 sheet=Image.new('RGB',(1080,((min(12,len(doc)-start)+3)//4)*378),'#bfd4d5')
 for i in range(start,min(start+12,len(doc))):
  im=Image.open(O/'rendered'/f'page_{i:02}.jpg');im.thumbnail((270,378));sheet.paste(im,(((i-start)%4)*270,((i-start)//4)*378))
 sheet.save(O/f'proof_{start:02}.jpg',quality=92)
reader=PdfReader(PDF);assert len(reader.pages)==42
v={'pdf_pages':42,'story_pages':40,'frame':'Targeted foreground removal from original book PDF page 4','full_scene_redraws_used':False,'visual_review':'PENDING','source_hashes_match':all(hashlib.sha256((O/B['sources'][k]['file']).read_bytes()).hexdigest()==B['sources'][k]['output_sha256'] for k in used),'pending':B['pending'],'handoff_search':B['handoff_search']}
(O/'verification.json').write_text(json.dumps(v,indent=2));print('Rendered 42 pages with',len(used),'source assets.')
