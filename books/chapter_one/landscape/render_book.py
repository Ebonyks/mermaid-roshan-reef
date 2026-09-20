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
ROLE='story_art'
def record(k,source_box,target,operation):
 im=Image.open(path(k));LAYERS.append({'page':PAGE,'source_key':k,'file':B['sources'][k]['file'],'sha256':hashlib.sha256(path(k).read_bytes()).hexdigest(),'native_size':list(im.size),'source_box_pixels':list(source_box),'target_box_points':list(target),'operation':operation,'role':ROLE,'alpha':im.mode=='RGBA'})

def cliprect(x,y,w,h):
 p=c.beginPath();p.rect(x,y,w,h);c.clipPath(p,stroke=0,fill=0)
def region(k,box,target):
 im=Image.open(path(k));iw,ih=im.size;l,t,r,b=box;x,y,w,h=target
 record(k,box,target,'source_region');c.saveState();cliprect(x,y,w,h);c.drawImage(str(path(k)),x-l*w/(r-l),y-(ih-b)*h/(b-t),width=iw*w/(r-l),height=ih*h/(b-t),mask='auto');c.restoreState()
def full(k):
 iw,ih=Image.open(path(k)).size;s=max(W/iw,H/ih);record(k,(0,0,iw,ih),((W-iw*s)/2,(H-ih*s)/2,iw*s,ih*s),'page_trim');c.saveState();cliprect(0,0,W,H);c.drawImage(str(path(k)),(W-iw*s)/2,(H-ih*s)/2,width=iw*s,height=ih*s);c.restoreState()
def cut(k,x,y,w,h):
 im=Image.open(path(k));assert im.mode=='RGBA' and im.getextrema()[3][0]==0,k
 box=(512,0,1024,512) if k=='grand_puff_jump_sheet' else im.getchannel('A').getbbox()
 l,t,r,b=box;s=min(w/(r-l),h/(b-t));dw=(r-l)*s;dh=(b-t)*s;region(k,box,(x+(w-dw)/2,y+(h-dh)/2,dw,dh));return (x+(w-dw)/2,y+(h-dh)/2,dw,dh)
def text(s,x,y,width,size=16,center=False,halo=False):
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
  if halo:
   c.setFillColorRGB(.98,.99,1)
   for dx,dy in [(-.7,0),(.7,0),(0,-.7),(0,.7)]:c.drawString(xx+dx,y+dy,line)
  c.setFillColorRGB(.08,.18,.31);c.drawString(xx,y,line)
  c.restoreState();y-=size*1.3
 return y
base='landscape_base'
def background(p):
 global ROLE
 ROLE='stationery_base';full(base)
 for i,k in enumerate(p.get('border_assets',[])):
  ROLE='mound_decoration'
  x=53 if i%2==0 else 400;y=10;w=48;h=38
  assert w<=W*.12 and h<=H*.12 and y+h<=H*.15
  c.saveState();c.setFillColorRGB(.25,.4,.6);c.setFillAlpha(.12);c.ellipse(x+4,y-1,x+w-4,y+5,fill=1,stroke=0);c.restoreState();ax,ay,aw,ah=cut(k,x,y,w,h)
  ROLE='mound_occlusion';c.saveState();cliprect(ax,ay,aw,ah*.1);full(base);LAYERS[-1]['clip_points']=[ax,ay,aw,ah*.1];c.restoreState()
 ROLE='story_art'
def extension(k):
 global ROLE
 ext=k+'_wide';iw,ih=Image.open(path(k)).size;middle=ih/iw*W;top=H-middle;ew,eh=Image.open(path(ext)).size
 ROLE='empty_ceiling_extension';region(ext,(0,0,ew,100),(0,middle,W,top))
 ROLE='original_complete_scene';region(k,(0,0,iw,ih),(0,0,W,middle));ROLE='story_art'
# Covers remain part of the rough, outside the 32 numbered story pages.
full('arrival');text('Mermaid Roshan',20,324,464,30,True,True);text('and the Hidden Rainbow',20,286,464,23,True,True);text('A Pearl Castle friendship story',20,28,464,13,True,True);c.showPage()
for p in B['pages']:
 PAGE=p['page']
 a=p['art'];layout=p['layout'];s=p['text']
 if p['mode']=='F':
  extension(a[0]) if layout=='extension' else full(a[0])
  if layout=='right_top':text(s,278,332,207,15,False,True)
  else:text(s,22,337,460,15,True,True)
 else:
  background(p)
  if layout=='wide_cut':cut(a[0],24,46,456,235);text(s,27,321,450,16,True)
  elif layout=='pair':
   cut(a[0],32,52,170,224);cut(a[1],211,47,170,231);text(s,27,321,450,16,True)
  elif layout=='tools':
   cut(a[0],40,65,217,190);cut(a[1],294,57,156,145);text(s,27,321,450,16,True)
  elif layout=='supplies':
   cut(a[0],25,73,209,150);cut(a[1],227,128,216,136);cut(a[2],355,46,85,109);text(s,27,321,450,16,True)
  elif layout=='left_art':cut(a[0],25,49,265,258);text(s,303,246,174,17)
  else:cut(a[0],232,45,248,265);text(s,32,254,195,17)
 c.showPage()
PAGE='back_cover'
background({});text('One little thing.\nOne helping hand.\nOne very big adventure.',45,268,414,23,True);cut('brush',92,64,135,114);cut('sponge',299,70,99,91);text('Landscape review edition • Chapter One',25,25,454,10,True);c.showPage();c.save()
font_path=ROOT/B['font']
(O/'page_provenance.json').write_text(json.dumps({'page_size_points':[W,H],'coordinate_system':'source pixels: top-left x,y; PDF target points: bottom-left x,y,width,height; page-trim layers clipped to page','font':{'file':B['font'],'sha256':hashlib.sha256(font_path.read_bytes()).hexdigest()},'layers':LAYERS,'note':'Actual draw operations, including covers and background occlusion redraws. This proves source use, not visual acceptance.'},indent=2),encoding='utf8')
doc=pdfium.PdfDocument(str(PDF));thumbs=[]
for i,page in enumerate(doc):
 im=page.render(scale=1.65).to_pil().convert('RGB');im.save(O/f'page_{i:02}.jpg',quality=91);im.thumbnail((336,240));thumbs.append(im.copy())
for start in range(0,len(thumbs),8):
 sheet=Image.new('RGB',(1344,524),'#d8e3ed');d=ImageDraw.Draw(sheet)
 for j,im in enumerate(thumbs[start:start+8]):
  x=j%4*336;y=j//4*262;sheet.paste(im,(x,y));idx=start+j;d.text((x+5,y+243),'Cover' if idx==0 else 'Back cover' if idx==33 else f'Page {idx}',fill='black')
 sheet.save(O/f'contact_{start//8+1}.jpg',quality=94)
body=''.join(f'<figure><figcaption>{"Cover" if i==0 else "Back cover" if i==33 else "Page "+str(i)}</figcaption><img loading="lazy" src="page_{i:02}.jpg" alt="{html.escape("Cover" if i==0 else "Back cover" if i==33 else B["pages"][i-1]["text"])}"></figure>' for i in range(34))
(O/'READ_BOOK.html').write_text('<!doctype html><meta charset="utf-8"><title>Mermaid Roshan · Landscape rough</title><style>body{margin:0;background:#193449;color:#e3f5ff;font:18px system-ui}header{max-width:1100px;margin:30px auto;padding:20px}main{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:24px;padding:24px}figure{margin:0}img{width:100%;display:block}figcaption{padding:8px}a{color:#9cddff}@media(max-width:800px){main{grid-template-columns:1fr}}</style><header><h1>Mermaid Roshan and the Hidden Rainbow</h1><p>7 × 5 inches · 32 story pages + covers · Landscape rough for review</p><p><a href="Mermaid_Roshan_LANDSCAPE_ROUGH.pdf">Download PDF</a></p><p>Existing game artwork with full-art pages and silhouette compositions. Final resolution, extraction edges, and the waterfall action still await refinement.</p></header><main>'+body+'</main>',encoding='utf8')
(O/'verification.json').write_text(json.dumps({'pages':len(doc),'story_pages':len(B['pages']),'full_art':sum(p['mode']=='F' for p in B['pages']),'cutout':sum(p['mode']=='C' for p in B['pages']),'points':[W,H],'pdf_sha256':hashlib.sha256(PDF.read_bytes()).hexdigest(),'status':'rough; visual acceptance pending'},indent=2),encoding='utf8')
print(PDF)
