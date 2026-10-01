"""Render the source-preserving 7 x 5 inch landscape review book."""
from pathlib import Path
import argparse,json,html,hashlib,math
from PIL import Image,ImageDraw
from reportlab.pdfgen import canvas
from reportlab import rl_config
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
import pypdfium2 as pdfium
ROOT=Path(__file__).resolve().parent
B=json.loads((ROOT/'book.json').read_text(encoding='utf8'))
ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,default=Path.cwd()/'output/pdf/landscape');args=ap.parse_args();O=args.output;O.mkdir(parents=True,exist_ok=True)
pdfmetrics.registerFont(TTFont('Sniglet',str(ROOT/B['font'])))
W,H=504,360
rl_config.useA85=0  # Preserve lossless image streams without ASCII85 overhead.
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
def visible_strip(k,box,target):
 # PDF layout resource: omit permanently hidden pixels, keeping source files intact.
 im=Image.open(path(k));x,y,w,h=target
 record(k,box,target,'source_region_visible_pdf_resource')
 c.drawImage(ImageReader(im.crop(box)),x,y,width=w,height=h,mask='auto')
def full(k,anchor=.5):
 iw,ih=Image.open(path(k)).size;s=max(W/iw,H/ih);record(k,(0,0,iw,ih),((W-iw*s)*anchor,(H-ih*s)/2,iw*s,ih*s),'page_trim');c.saveState();cliprect(0,0,W,H);c.drawImage(str(path(k)),(W-iw*s)*anchor,(H-ih*s)/2,width=iw*s,height=ih*s);c.restoreState()
def local_patch(p):
 # The original full-art frame remains the base. Only this irregular lane is exposed.
 q=p['local_patch'];k=q['source'];rw,rh=q['reference_size'];s=max(W/rw,H/rh);ox=(W-rw*s)*q.get('anchor',.5);oy=(H-rh*s)/2
 im=Image.open(path(k));iw,ih=im.size
 c.saveState();cliprect(0,0,W,H);shape=c.beginPath()
 for i,(x,y) in enumerate(q['polygon']):
  (shape.moveTo if i==0 else shape.lineTo)(ox+x*s,oy+(rh-y)*s)
 shape.close();c.clipPath(shape,stroke=0,fill=0)
 # Embed only the PDF-visible source resource. Native derivative remains unchanged.
 xs=[v[0] for v in q['polygon']];ys=[v[1] for v in q['polygon']]
 l=max(0,math.floor(min(xs)*iw/rw));t=max(0,math.floor(min(ys)*ih/rh));r=min(iw,math.ceil(max(xs)*iw/rw));b=min(ih,math.ceil(max(ys)*ih/rh))
 target=(ox+l*rw/iw*s,oy+(rh-b*rh/ih)*s,(r-l)*rw/iw*s,(b-t)*rh/ih*s)
 c.drawImage(ImageReader(im.crop((l,t,r,b))),*target,mask='auto')
 record(k,(l,t,r,b),target,'bounded_inpaint_polygon_visible_pdf_resource')
 LAYERS[-1]['clip_reference_size']=q['reference_size'];LAYERS[-1]['clip_polygon_source_pixels']=q['polygon']
 c.restoreState()

def cut(k,x,y,w,h):
 im=Image.open(path(k));assert im.mode=='RGBA' and im.getextrema()[3][0]==0,k
 box=B['sources'][k].get('alpha_box') or ((512,0,1024,512) if k=='grand_puff_jump_sheet' else im.getchannel('A').getbbox())
 l,t,r,b=box;s=min(w/(r-l),h/(b-t));dw=(r-l)*s;dh=(b-t)*s;region(k,box,(x+(w-dw)/2,y+(h-dh)/2,dw,dh));return (x+(w-dw)/2,y+(h-dh)/2,dw,dh)
def text(s,x,y,width,size=18,center=False,halo=False,color="navy",shadow=False,outline=0):
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
  if halo:
   c.setStrokeColorRGB(*((.06,.12,.25) if color=='white' else (1,1,.98)));c.setLineWidth(.85)
   obj=c.beginText(xx,y);obj.setFont('Sniglet',size);obj.setTextRenderMode(1);obj.textOut(line);obj.setTextRenderMode(0);c.drawText(obj)
   obj=c.beginText(xx,y);obj.setFont('Sniglet',size);obj.setTextRenderMode(0);obj.textOut(line);c.drawText(obj)
  elif outline:
   c.setStrokeColorRGB(.06,.16,.29);c.setLineWidth(outline)
   obj=c.beginText(xx,y);obj.setFont('Sniglet',size);obj.setTextRenderMode(2);obj.textOut(line);c.drawText(obj)
  else:c.drawString(xx,y,line)
  c.restoreState()
  line_width=pdfmetrics.stringWidth(line,'Sniglet',size)
  TEXT_LINES.append({'page':PAGE,'text':line,'box':[xx,y+pdfmetrics.getDescent('Sniglet')*size/1000,line_width,(pdfmetrics.getAscent('Sniglet')-pdfmetrics.getDescent('Sniglet'))*size/1000],'font_size':size,'color':color})
  y-=size*1.3
 return y
def speech(q):
 x,y,w,h=q['box'];tx,ty=q['tail'];c.saveState()
 c.setFillColorRGB(1,1,.98);c.setStrokeColorRGB(.16,.26,.45);c.setLineWidth(1.2)
 # Rounded capsule with an integrated, short curved tail aimed at its speaker.
 r=h/2;cy=y+h/2;mid=max(x+r+10,min(tx+5,x+w-r-10))
 p=c.beginPath();p.moveTo(x+r,y);p.lineTo(mid-7,y)
 p.curveTo(mid-6,y-7,tx-4,ty+4,tx,ty)
 p.curveTo(tx+1,ty+7,mid+5,y-5,mid+7,y)
 p.lineTo(x+w-r,y);p.curveTo(x+w-r*.448,y,x+w,y+r*.448,x+w,y+r)
 p.curveTo(x+w,y+h-r*.448,x+w-r*.448,y+h,x+w-r,y+h)
 p.lineTo(x+r,y+h);p.curveTo(x+r*.448,y+h,x,y+h-r*.448,x,y+h-r)
 p.curveTo(x,y+r*.448,x+r*.448,y,x+r,y)
 p.close();c.drawPath(p,fill=1,stroke=1);c.restoreState()
 lines=q['text'].split('\n');size=18;leading=size*1.3
 ascent=pdfmetrics.getAscent('Sniglet')*size/1000;descent=pdfmetrics.getDescent('Sniglet')*size/1000
 baseline=cy+((len(lines)-1)*leading-ascent-descent)/2
 text(q['text'],x+12,baseline,w-24,size,True)

base='landscape_base'
def background(p):
 global ROLE
 if p.get('integrated_background'):
  ROLE='integrated_stationery';full(p['integrated_background'])
  ROLE='bounded_stationery_edit'
  for patch in p.get('background_patches',[]):local_patch({'local_patch':patch})
  ROLE='story_art';return
 ROLE='stationery_base';full(base)
 assert not p.get('border_placements'), 'Use an inspected integrated background; flat ground masks are retired.'
 ROLE='story_art'
def extension(k):
 global ROLE
 ext=k+'_wide';iw,ih=Image.open(path(k)).size;middle=ih/iw*W;top=H-middle;ew,eh=Image.open(path(ext)).size
 ROLE='empty_ceiling_extension';visible_strip(ext,(0,0,ew,B['sources'][ext].get('ceiling_end',100)),(0,middle,W,top))
 ROLE='original_complete_scene';region(k,(0,0,iw,ih),(0,0,W,middle));ROLE='story_art'
def page_extension(p):
 global ROLE
 k=p['art'][0];iw,ih=Image.open(path(k)).size;middle=W*ih/iw
 ext=p['page_extension'];ew,eh=Image.open(path(ext)).size;edge=math.ceil((H-middle)*ew/W)
 ROLE='empty_ceiling_extension';visible_strip(ext,(0,0,ew,edge),(0,H-edge*W/ew,W,edge*W/ew))
 ROLE='original_complete_scene';region(k,(0,0,iw,ih),(0,0,W,middle));ROLE='story_art'
# Covers remain part of the rough, outside the 32 numbered story pages.
full('cover_rendered')
text('Mermaid Roshan',142,312,338,30,True)
text('and the Hidden Rainbow',142,282,338,22,True)
text('A Pearl Castle friendship story',24,28,456,13,True)
c.showPage()
for p in B['pages']:
 PAGE=p['page'];a=p['art'];layout=p['layout']
 if p['mode']=='F':
  if p.get('page_extension'):page_extension(p)
  elif 'art_crop' in p:region(a[0],p['art_crop'],(0,0,W,H))
  elif layout=='extension':extension(a[0])
  else:full(a[0],0 if layout=='full_left' else .5)
 else:
  background(p)
  if p.get('placements'):
   for placement in p['placements']:cut(placement['source'],*placement['box'])
  elif layout=='sink_and_sponge':
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
 for patch in p.get('local_patches',[]):local_patch({'local_patch':patch})
 q=p['caption'];text(p['text'],q['x'],q['y'],q['width'],q['size'],q['align']=='center',color=q['color'],shadow=q['shadow'],halo=q.get('halo',False),outline=q.get('outline',0))
 for balloon in p.get('speech_bubbles',[]):speech(balloon)
 c.showPage()
PAGE='back_cover'
full(B['back_cover']['art']);c.showPage();c.save()
font_path=ROOT/B['font']
(O/'page_provenance.json').write_text(json.dumps({'page_size_points':[W,H],'coordinate_system':'source pixels: top-left x,y; PDF target points: bottom-left x,y,width,height; page-trim layers clipped to page','font':{'file':B['font'],'sha256':hashlib.sha256(font_path.read_bytes()).hexdigest()},'layers':LAYERS,'text_lines':TEXT_LINES,'note':'Actual draw operations, including covers and background occlusion redraws. This proves source use, not visual acceptance.'},indent=2),encoding='utf8',newline='\n')
doc=pdfium.PdfDocument(str(PDF));thumbs=[]
for i,page in enumerate(doc):
 im=page.render(scale=3).to_pil().convert('RGB');im.save(O/f'page_{i:02}.png')
 if not B.get('revision'):im.save(O/f'page_{i:02}.jpg',quality=98,subsampling=0)
 im.thumbnail((336,240));thumbs.append(im.copy())
for start in range(0,len(thumbs),8):
 sheet=Image.new('RGB',(1344,524),'#d8e3ed');d=ImageDraw.Draw(sheet)
 for j,im in enumerate(thumbs[start:start+8]):
  x=j%4*336;y=j//4*262;sheet.paste(im,(x,y));idx=start+j;d.text((x+5,y+243),'Cover' if idx==0 else 'Back cover' if idx==33 else f'Page {idx}',fill='black')
 sheet.save(O/f'contact_{start//8+1}.jpg',quality=94)
body=''.join(f'<figure><figcaption>{"Cover" if i==0 else "Back cover" if i==33 else "Page "+str(i)}</figcaption><img loading="lazy" src="page_{i:02}.png" alt="{html.escape("Cover" if i==0 else "Back cover" if i==33 else B["pages"][i-1]["text"])}"></figure>' for i in range(34))
(O/'READ_BOOK.html').write_text('<!doctype html><meta charset="utf-8"><title>Mermaid Roshan · Landscape book</title><style>body{margin:0;background:#193449;color:#e3f5ff;font:18px system-ui}header{max-width:1100px;margin:30px auto;padding:20px}main{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:24px;padding:24px}figure{margin:0}img{width:100%;display:block}figcaption{padding:8px}a{color:#9cddff}@media(max-width:800px){main{grid-template-columns:1fr}}</style><header><h1>Mermaid Roshan and the Hidden Rainbow</h1><p>7 × 5 inches · 32 story pages + covers · '+html.escape(B.get('revision','Review proof'))+'</p><p><a href="Mermaid_Roshan_LANDSCAPE_ROUGH.pdf">Download PDF</a> · <a href="'+html.escape(B.get('review_href','../REVISION_REVIEW.html'))+'">Revision audit and before/after views</a></p><p>34 pages including covers. Owner, child and final print acceptance remain open.</p></header><main>'+body+'</main>',encoding='utf8',newline='\n')
# A portable rebuild provides the written review even without the earlier v7 images.
if not B.get('revision') and not (O/'STRESS_TEST.html').exists() and (ROOT/'stress_review.json').exists():
 review=json.loads((ROOT/'stress_review.json').read_text(encoding='utf8'))
 entries=''.join('<h2>Page '+str(row['page'])+'</h2><p><b>Baseline:</b> '+html.escape(row['baseline_issue'])+'</p><p><b>Revision:</b> '+html.escape(row['revision'])+'</p><p>'+html.escape(row['identity_review'])+'</p>' for row in review['pages'])
 (O/'STRESS_TEST.html').write_text('<!doctype html><meta charset="utf-8"><title>Book stress review</title><style>body{max-width:850px;margin:40px auto;padding:20px;font:18px/1.5 system-ui;color:#153047;background:#e5f2f8}</style><h1>Book stress review</h1><p>Revised rough; final owner acceptance remains open. This portable report contains the written review. The full before/after report additionally requires the v7 baseline proof.</p><a href="READ_BOOK.html">Read book</a>'+entries,encoding='utf8',newline='\n')
(O/'verification.json').write_text(json.dumps({'pages':len(doc),'story_pages':len(B['pages']),'full_art':sum(p['mode']=='F' for p in B['pages']),'cutout':sum(p['mode']=='C' for p in B['pages']),'points':[W,H],'pdf_sha256':hashlib.sha256(PDF.read_bytes()).hexdigest(),'status':'rough; visual acceptance pending'},indent=2),encoding='utf8',newline='\n')
print(PDF)
