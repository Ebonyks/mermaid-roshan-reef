"""Render the source-preserving 7 x 5 inch landscape review book."""
from pathlib import Path
import argparse,json,html,hashlib
from PIL import Image,ImageDraw
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
import pypdfium2 as pdfium
ROOT=Path(__file__).resolve().parent
B=json.loads((ROOT/'book.json').read_text(encoding='utf8'))
ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,default=Path.cwd()/'output/pdf/landscape');args=ap.parse_args();O=args.output;O.mkdir(parents=True,exist_ok=True)
pdfmetrics.registerFont(TTFont('Sniglet',str(ROOT/B['font'])))
W,H=504,360
PDF=O/'Mermaid_Roshan_LANDSCAPE_ROUGH.pdf';c=canvas.Canvas(str(PDF),pagesize=(W,H));c.setTitle(B['title']);c.setAuthor('Mermaid Roshan picture-book project')
def path(k):return ROOT/B['sources'][k]['file']
PAGE='front_cover'
LAYERS=[]
TEXT_LINES=[]
ROLE='story_art'
def record(k,source_box,target,operation):
 im=Image.open(path(k));LAYERS.append({'page':PAGE,'source_key':k,'file':B['sources'][k]['file'],'sha256':hashlib.sha256(path(k).read_bytes()).hexdigest(),'native_size':list(im.size),'source_box_pixels':list(source_box),'target_box_points':list(target),'operation':operation,'role':ROLE,'alpha':im.mode=='RGBA'})

def cliprect(x,y,w,h):
 p=c.beginPath();p.rect(x,y,w,h);c.clipPath(p,stroke=0,fill=0)
def region(k,box,target):
 im=Image.open(path(k));iw,ih=im.size;l,t,r,b=box;x,y,w,h=target
 record(k,box,target,'source_region');c.saveState();cliprect(x,y,w,h);c.drawImage(str(path(k)),x-l*w/(r-l),y-(ih-b)*h/(b-t),width=iw*w/(r-l),height=ih*h/(b-t),mask='auto');c.restoreState()
def full(k,anchor=.5):
 iw,ih=Image.open(path(k)).size;s=max(W/iw,H/ih);record(k,(0,0,iw,ih),((W-iw*s)*anchor,(H-ih*s)/2,iw*s,ih*s),'page_trim');c.saveState();cliprect(0,0,W,H);c.drawImage(str(path(k)),(W-iw*s)*anchor,(H-ih*s)/2,width=iw*s,height=ih*s);c.restoreState()
def local_patch(p):
 # The original full-art frame remains the base. Only this irregular lane is exposed.
 q=p['local_patch'];k=q['source'];rw,rh=q['reference_size'];s=max(W/rw,H/rh);ox=(W-rw*s)/2;oy=(H-rh*s)/2
 im=Image.open(path(k));iw,ih=im.size
 c.saveState();cliprect(0,0,W,H);shape=c.beginPath()
 for i,(x,y) in enumerate(q['polygon']):
  (shape.moveTo if i==0 else shape.lineTo)(ox+x*s,oy+(rh-y)*s)
 shape.close();c.clipPath(shape,stroke=0,fill=0)
 c.drawImage(str(path(k)),ox,oy,width=rw*s,height=rh*s)
 record(k,(0,0,iw,ih),(ox,oy,rw*s,rh*s),'bounded_inpaint_polygon')
 LAYERS[-1]['clip_reference_size']=q['reference_size'];LAYERS[-1]['clip_polygon_source_pixels']=q['polygon']
 c.restoreState()

def cut(k,x,y,w,h):
 im=Image.open(path(k));assert im.mode=='RGBA' and im.getextrema()[3][0]==0,k
 box=B['sources'][k].get('alpha_box') or ((512,0,1024,512) if k=='grand_puff_jump_sheet' else im.getchannel('A').getbbox())
 l,t,r,b=box;s=min(w/(r-l),h/(b-t));dw=(r-l)*s;dh=(b-t)*s;region(k,box,(x+(w-dw)/2,y+(h-dh)/2,dw,dh));return (x+(w-dw)/2,y+(h-dh)/2,dw,dh)
def text(s,x,y,width,size=18,center=False,halo=False,color="navy",shadow=False):
 lines=[]
 for para in s.split('\n'):
  line=''
  for word in para.split():
   trial=(line+' '+word).strip()
   if pdfmetrics.stringWidth(trial,'Sniglet',size)>width and line:lines.append(line);line=word
   else:line=trial
  lines.append(line)
 for line in lines:
  xx=x+(width-pdfmetrics.stringWidth(line,'Sniglet',size))/2 if center else x
  c.saveState();c.setFont('Sniglet',size)
  if shadow:
   c.setFillColorRGB(.04,.09,.18);c.drawString(xx+.6,y-.6,line)
  c.setFillColorRGB(*((1,1,.98) if color=='white' else (.06,.16,.29)))
  c.drawString(xx,y,line);c.restoreState()
  line_width=pdfmetrics.stringWidth(line,'Sniglet',size)
  TEXT_LINES.append({'page':PAGE,'text':line,'box':[xx,y+pdfmetrics.getDescent('Sniglet')*size/1000,line_width,(pdfmetrics.getAscent('Sniglet')-pdfmetrics.getDescent('Sniglet'))*size/1000],'font_size':size,'color':color})
  y-=size*1.3
 return y
base='landscape_base'
def background(p):
 global ROLE
 if p.get('integrated_background'):
  ROLE='integrated_stationery';full(p['integrated_background']);ROLE='story_art';return
 ROLE='stationery_base';full(base)
 assert not p.get('border_placements'), 'Use an inspected integrated background; flat ground masks are retired.'
 ROLE='story_art'
def extension(k):
 global ROLE
 ext=k+'_wide';iw,ih=Image.open(path(k)).size;middle=ih/iw*W;top=H-middle;ew,eh=Image.open(path(ext)).size
 ROLE='empty_ceiling_extension';region(ext,(0,0,ew,B['sources'][ext].get('ceiling_end',100)),(0,middle,W,top))
 ROLE='original_complete_scene';region(k,(0,0,iw,ih),(0,0,W,middle));ROLE='story_art'
# Covers remain part of the rough, outside the 32 numbered story pages.
background({})
text('Mermaid Roshan',24,306,456,34,True)
text('and the Hidden Rainbow',24,270,456,25,True)
cut('boss_cut',286,58,182,192)
cut('roshan_cover',43,58,187,195)
cut('eagle_original_isolated',220,58,77,127)
cut('brush',226,189,45,51);cut('sponge',262,198,32,30)
text('A Pearl Castle friendship story',24,28,456,13,True)
c.showPage()
for p in B['pages']:
 PAGE=p['page'];a=p['art'];layout=p['layout']
 if p['mode']=='F':
  if 'art_crop' in p:region(a[0],p['art_crop'],(0,0,W,H))
  elif layout=='extension':extension(a[0])
  else:full(a[0],0 if layout=='full_left' else .5)
 else:
  background(p)
  if layout=='sink_and_sponge':
   cut(a[0],42,73,215,188);cut(a[1],183,188,43,42)
  elif layout=='dodge_pair':
   cut(a[0],266,64,189,203);cut(a[1],48,75,189,179)
  elif layout=='pair':
   cut(a[0],65,51,175,219);cut(a[1],255,55,176,206)
  elif layout=='friends_pair':
   cut(a[0],70,55,198,216);cut(a[1],310,74,124,172)
  elif layout=='tools':
   cut(a[0],49,65,205,190);cut(a[1],302,62,143,139)
  elif layout=='supplies':
   cut(a[0],40,76,190,148);cut(a[1],232,146,207,116);cut(a[2],339,57,91,117)
  else:cut(a[0],*p.get('foreground_zone',[30,53,444,211]))
 if 'local_patch' in p:local_patch(p)
 q=p['caption'];text(p['text'],q['x'],q['y'],q['width'],q['size'],q['align']=='center',color=q['color'],shadow=q['shadow'])
 c.showPage()
PAGE='back_cover'
background({});text('One little thing.\nOne helping hand.\nOne very big adventure.',45,268,414,23,True);cut('brush',92,64,135,114);cut('sponge',299,70,99,91);text('Landscape review edition • Chapter One',25,25,454,10,True);c.showPage();c.save()
font_path=ROOT/B['font']
(O/'page_provenance.json').write_text(json.dumps({'page_size_points':[W,H],'coordinate_system':'source pixels: top-left x,y; PDF target points: bottom-left x,y,width,height; page-trim layers clipped to page','font':{'file':B['font'],'sha256':hashlib.sha256(font_path.read_bytes()).hexdigest()},'layers':LAYERS,'text_lines':TEXT_LINES,'note':'Actual draw operations, including covers and background occlusion redraws. This proves source use, not visual acceptance.'},indent=2),encoding='utf8')
doc=pdfium.PdfDocument(str(PDF));thumbs=[]
for i,page in enumerate(doc):
 im=page.render(scale=1.65).to_pil().convert('RGB');im.save(O/f'page_{i:02}.jpg',quality=91);im.thumbnail((336,240));thumbs.append(im.copy())
for start in range(0,len(thumbs),8):
 sheet=Image.new('RGB',(1344,524),'#d8e3ed');d=ImageDraw.Draw(sheet)
 for j,im in enumerate(thumbs[start:start+8]):
  x=j%4*336;y=j//4*262;sheet.paste(im,(x,y));idx=start+j;d.text((x+5,y+243),'Cover' if idx==0 else 'Back cover' if idx==33 else f'Page {idx}',fill='black')
 sheet.save(O/f'contact_{start//8+1}.jpg',quality=94)
body=''.join(f'<figure><figcaption>{"Cover" if i==0 else "Back cover" if i==33 else "Page "+str(i)}</figcaption><img loading="lazy" src="page_{i:02}.jpg" alt="{html.escape("Cover" if i==0 else "Back cover" if i==33 else B["pages"][i-1]["text"])}"></figure>' for i in range(34))
(O/'READ_BOOK.html').write_text('<!doctype html><meta charset="utf-8"><title>Mermaid Roshan · Landscape rough</title><style>body{margin:0;background:#193449;color:#e3f5ff;font:18px system-ui}header{max-width:1100px;margin:30px auto;padding:20px}main{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:24px;padding:24px}figure{margin:0}img{width:100%;display:block}figcaption{padding:8px}a{color:#9cddff}@media(max-width:800px){main{grid-template-columns:1fr}}</style><header><h1>Mermaid Roshan and the Hidden Rainbow</h1><p>7 × 5 inches · 32 story pages + covers · Stress-revised rough · owner acceptance pending</p><p><a href="Mermaid_Roshan_LANDSCAPE_ROUGH.pdf">Download PDF</a> · <a href="STRESS_TEST.html">Page-by-page stress review</a></p><p>Revised dirty-castle opening, contextual blue backgrounds and individual caption placement. Character and source limits remain explicit in the stress report.</p></header><main>'+body+'</main>',encoding='utf8')
# A portable rebuild provides the written review even without the earlier v7 images.
if not (O/'STRESS_TEST.html').exists() and (ROOT/'stress_review.json').exists():
 review=json.loads((ROOT/'stress_review.json').read_text(encoding='utf8'))
 entries=''.join('<h2>Page '+str(row['page'])+'</h2><p><b>Baseline:</b> '+html.escape(row['baseline_issue'])+'</p><p><b>Revision:</b> '+html.escape(row['revision'])+'</p><p>'+html.escape(row['identity_review'])+'</p>' for row in review['pages'])
 (O/'STRESS_TEST.html').write_text('<!doctype html><meta charset="utf-8"><title>Book stress review</title><style>body{max-width:850px;margin:40px auto;padding:20px;font:18px/1.5 system-ui;color:#153047;background:#e5f2f8}</style><h1>Book stress review</h1><p>Revised rough; final owner acceptance remains open. This portable report contains the written review. The full before/after report additionally requires the v7 baseline proof.</p><a href="READ_BOOK.html">Read book</a>'+entries,encoding='utf8')
(O/'verification.json').write_text(json.dumps({'pages':len(doc),'story_pages':len(B['pages']),'full_art':sum(p['mode']=='F' for p in B['pages']),'cutout':sum(p['mode']=='C' for p in B['pages']),'points':[W,H],'pdf_sha256':hashlib.sha256(PDF.read_bytes()).hexdigest(),'status':'rough; visual acceptance pending'},indent=2),encoding='utf8')
print(PDF)
