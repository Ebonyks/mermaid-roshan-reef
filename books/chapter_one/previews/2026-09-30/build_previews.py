"""Build owner-review comparisons; never mutates the V27 manuscript or art."""
from pathlib import Path
import json, hashlib, html, shutil, argparse, math
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab import rl_config
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import pypdfium2 as pdfium

P=Path(__file__).resolve().parent
R=P.parents[3]
L=R/'books/chapter_one/landscape'
B=json.loads((L/'book.json').read_text(encoding='utf8'))
W,H=504,360
rl_config.useA85=0  # Binary lossless image streams; avoids ASCII85 size overhead.
CW,CH=1056,462
FONT=(L/B['font']).resolve()
pdfmetrics.registerFont(TTFont('Sniglet',str(FONT)))
S=[6,8,13,15,18,19,23,26,27,31]
ap=argparse.ArgumentParser()
ap.add_argument('--before-dir',type=Path)
args=ap.parse_args()
for d in ['before','after','comparisons']: (P/d).mkdir(exist_ok=True)
if args.before_dir:
 for n in sorted(set(S+[23,24,25,26,27,28,29,30])):
  shutil.copy2(args.before_dir/f'page_{n:02}.png',P/'before'/f'story_{n:02}.png')
PDF=P/'BEFORE_AFTER.pdf'
c=canvas.Canvas(str(PDF),pagesize=(CW,CH))
c.setTitle('Mermaid Roshan — Before / After proposals')
c.setAuthor('Mermaid Roshan picture-book project')
layers=[];lines=[];page_id=''
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def source(k):return (L/B['sources'][k]['file']).resolve()
def art(k):return P/'art'/f'{k}.png'
def clip(x,y,w,h):
 q=c.beginPath();q.rect(x,y,w,h);c.clipPath(q,stroke=0,fill=0)
def draw(p,x,y,w,h,operation):
 im=Image.open(p)
 c.drawImage(str(p),x,y,width=w,height=h,mask='auto')
 layers.append(dict(page=page_id,path=p.relative_to(R).as_posix(),sha256=sha(p),native_size=list(im.size),target=[x,y,w,h],operation=operation))
def full(p):
 iw,ih=Image.open(p).size;s=max(W/iw,H/ih)
 c.saveState();clip(0,0,W,H);draw(p,(W-iw*s)/2,(H-ih*s)/2,iw*s,ih*s,'uniform full-page placement');c.restoreState()
def cut(p,x,y,w,h):
 im=Image.open(p);assert im.mode=='RGBA' and im.getextrema()[3][0]==0,p
 l,t,r,b=im.getchannel('A').getbbox();s=min(w/(r-l),h/(b-t))
 dx=x+(w-(r-l)*s)/2;dy=y+(h-(b-t)*s)/2
 c.saveState();clip(dx,dy,(r-l)*s,(b-t)*s)
 draw(p,dx-l*s,dy-(im.height-b)*s,im.width*s,im.height*s,'transparent contour, uniform scale')
 layers[-1]['alpha_box']=[l,t,r,b];c.restoreState()
def patch(p,poly):
 # Page layout clips an imagegen edit to its bounded source area.
 # No procedural pixel painting or generated full-scene substitution.
 iw,ih=Image.open(p).size;s=max(W/iw,H/ih);ox=(W-iw*s)/2;oy=(H-ih*s)/2
 c.saveState();q=c.beginPath()
 for i,(x,y) in enumerate(poly):
  (q.moveTo if i==0 else q.lineTo)(ox+x*s,oy+(ih-y)*s)
 q.close();c.clipPath(q,stroke=0,fill=0)
 draw(p,ox,oy,iw*s,ih*s,'bounded generated patch');layers[-1]['polygon_source_pixels']=poly;c.restoreState()
def text(s,x,y,width,size=18,center=False,halo=False):
 assert size>=18
 for para in s.split('\n'):
  ll=[];line=''
  for word in para.split():
   trial=(line+' '+word).strip()
   if line and pdfmetrics.stringWidth(trial,'Sniglet',size)>width:ll.append(line);line=word
   else:line=trial
  ll.append(line)
  for line in ll:
   sw=pdfmetrics.stringWidth(line,'Sniglet',size);xx=x+(width-sw)/2 if center else x
   assert sw<=width+.1,(page_id,line,sw,width)
   c.saveState();c.setFillColorRGB(.06,.16,.29)
   if halo:
    c.setStrokeColorRGB(1,1,.98);c.setLineWidth(.85)
    t=c.beginText(xx,y);t.setFont('Sniglet',size);t.setTextRenderMode(1);t.textOut(line);t.setTextRenderMode(0);c.drawText(t)
   t=c.beginText(xx,y);t.setFont('Sniglet',size);t.setTextRenderMode(0);t.textOut(line);c.drawText(t);c.restoreState()
   asc=pdfmetrics.getAscent('Sniglet')*size/1000;desc=pdfmetrics.getDescent('Sniglet')*size/1000
   assert xx>=18 and xx+sw<=486 and y+desc>=18 and y+asc<=342,(page_id,line,xx,y)
   lines.append(dict(page=page_id,text=line,font='Sniglet',size=size,box=[xx,y+desc,sw,asc-desc]))
   y-=size*1.3
 return y
def bubble(s,x,y,w,h,tx,ty):
 # Soft rounded capsule and integrated short, curved tail.
 r=h/2;mid=max(x+r+10,min(tx+5,x+w-r-10))
 p=c.beginPath();p.moveTo(x+r,y);p.lineTo(mid-7,y)
 p.curveTo(mid-6,y-7,tx-4,ty+4,tx,ty)
 p.curveTo(tx+1,ty+7,mid+5,y-5,mid+7,y)
 p.lineTo(x+w-r,y);p.curveTo(x+w-r*.448,y,x+w,y+r*.448,x+w,y+r)
 p.curveTo(x+w,y+h-r*.448,x+w-r*.448,y+h,x+w-r,y+h)
 p.lineTo(x+r,y+h);p.curveTo(x+r*.448,y+h,x,y+h-r*.448,x,y+h-r)
 p.curveTo(x,y+r*.448,x+r*.448,y,x+r,y);p.close()
 c.saveState();c.setFillColorRGB(1,1,.985);c.setStrokeColorRGB(.19,.29,.47);c.setLineWidth(1.15);c.drawPath(p,fill=1,stroke=1);c.restoreState()
 num=len(s.split('\n'));asc=pdfmetrics.getAscent('Sniglet')*18/1000;desc=pdfmetrics.getDescent('Sniglet')*18/1000
 baseline=y+h/2+((num-1)*23.4-asc-desc)/2
 text(s,x+12,baseline,w-24,18,True)
def after(n):
 p=B['pages'][n-1]
 if n==6:
  full(source(p['integrated_background']));cut(art('sink_action'),32,60,440,218)
  text('Round and round went the sponge.\nRoshan wiped the sink clean.',32,318,440,18,True)
 elif n==8:
  full(source(p['art'][0]))
  patch(art('lamba_bath'),[(83,782),(100,757),(128,758),(143,746),(178,747),(198,763),(208,787),(211,809),(186,824),(150,831),(107,826)])
  text('Clean water filled the bath.\nThe dust bunny splashed again!',30,55,444,18,True,True)
 elif n==13:
  full(art('fountain_clear_v2'))
  text('Roshan pulled the cup free!',207,320,270,18,False,True)
 elif n==15:
  full(art('hug_stationery_v2') if art('hug_stationery_v2').exists() else art('hug_stationery'))
  cut(art('hug_cutout_v2'),184,64,296,244)
  text('“You helped me!”\nsaid Rumi.\nShe gave Roshan\na great big hug.',40,263,148,18)
 elif n==18:
  full(art('rescue_release'))
  text('“I’ll help!” said Roshan.\nShe brushed one bunny away, then the other.',33,58,438,18,True,True)
 elif n==19:
  full(art('apology_canvas'));cut(source('eagle_original_isolated'),205,70,98,174)
  text('Baby Eagle was free!',32,318,440,22,True)
  text('Now they could play gently.',32,283,440,18,True)
  bubble('Sorry!',40,162,135,52,122,145)
  bubble('We were just\nplaying!',327,166,146,63,373,148)
 elif n==23:
  full(source(p['art'][0]))
  patch(art('art_caption_space'),[(708,0),(1264,0),(1264,174),(1090,228),(708,220)])
  text('“Purple sparkles!”\nsaid Roshan.',260,320,164,18,False,False)
 elif n==26:
  full(source(p['integrated_background']));cut(source(p['art'][0]),*p['foreground_zone'])
  text('Sparkles flew from Roshan’s shell.\nGrand Puff wobbled. “Easy, Grand Puff!”',30,317,444,18,True)
 elif n==27:
  full(art('scrub_ceiling'))
  iw,ih=Image.open(source(p['art'][0])).size
  draw(source(p['art'][0]),0,0,W,W*ih/iw,'unchanged complete original below extension')
  text(p['text'],32,318,440,18,True,True)
 elif n==31:
  full(source(p['integrated_background']))
  cut(source('roshan_reflect_large'),276,62,196,230)
  cut(art('rainbow_puff_cutout'),62,86,146,174)
  text('“Your rainbow was there all along,\nGrand Puff. We helped it shine!”',32,316,440,18,True)

notes={
6:('Show the cleaning action','The sponge now touches the sink in Roshan’s hand. The source shell sink and contextual border remain.'),
8:('A quiet hidden visitor','One small Lamb-a peeks from the towels. No clue or search prompt appears on the child’s page.'),
13:('Make the fountain action readable','The cup is visibly clear of the mouth; water flows into the pool. Caption names the concrete action.'),
15:('Give the hug a quieter page','A connected character cutout replaces the scenic rectangle; the tiny fountain recalls the rescue.'),
18:('Clarify how Eagle is freed','The brush contacts the bunny away from Eagle’s face. The sentence supplies the missing action verb.'),
19:('Make the apology a conversation','Larger speaking bunnies, central Eagle, compact rounded balloons and short curved tails.'),
23:('Give the words a clear home','A quiet wall recess replaces only the distant shelf behind the caption; the painting action stays intact.'),
26:('Signal Roshan’s care','Copy-only proposal: Roshan responds to Puff’s wobble. Existing art and spectator border stay unchanged.'),
27:('Replace the stretched ceiling strip','An upward extension replaces the compressed strip; all original characters and lower scene are retained.'),
31:('Let Roshan speak to Grand Puff','The rainbow Puff from the accepted landing replaces Daddy as the conversation’s visible recipient.')
}
def ui(s,x,y,size=12,color=(.1,.2,.3)):
 c.setFillColorRGB(*color);c.setFont('Helvetica',size);c.drawString(x,y,s)
def plate_header(title):
 c.setFillColorRGB(.92,.96,.98);c.rect(0,0,CW,CH,fill=1,stroke=0)
 ui(title,18,438,17);ui('BEFORE — V27',18,409,12);ui('AFTER — PROPOSED',534,409,12)
for n in S:
 page_id=f'S{n:02}'
 title,note=notes[n]
 plate_header(f'Story page {n}  |  {title}')
 c.drawImage(str(P/'before'/f'story_{n:02}.png'),18,40,504,360)
 c.saveState();c.translate(534,40);after(n);c.restoreState()
 ui(note,18,19,10)
 c.showPage()
def thumb(n,x,y,w,label):
 h=w*5/7;c.drawImage(str(P/'before'/f'story_{n:02}.png'),x,y,w,h)
 ui(label,x,y-13,9)
def turn_plate(title,current,prev,following,labels):
 global page_id
 page_id=title
 c.setFillColorRGB(.92,.96,.98);c.rect(0,0,CW,CH,fill=1,stroke=0)
 ui(title,18,438,17)
 ui('BEFORE | Setup and reveal visible together',18,408,12)
 thumb(current[0],18,165,252,f'Current S{current[0]} (left)')
 thumb(current[1],270,165,252,f'Current S{current[1]} (right)')
 ui('AFTER | Proposed order holds the reveal behind a page turn',552,408,12)
 thumb(prev[0],552,241,210,labels[0]);thumb(prev[1],762,241,210,labels[1])
 ui('TURN THE PAGE',729,211,12)
 thumb(following[0],552,39,210,labels[2]);thumb(following[1],762,39,210,labels[3])
 ui('Pagination study only. Assumes S1 begins on a right-hand page.',18,105,11)
 ui('Combine the current Eagle aftermath (S19–20) to shift later beats.',18,85,11)
 ui('Reserve the freed page after the reveals; an earlier insert cancels this gain.',18,65,10)
 ui('Current 34-page book remains unchanged.',18,45,11)
 c.showPage()
turn_plate('Page-turn proposal 1 | The glowing door and Grand Puff',[24,25],[23,24],[25,26],
 ['Proposed S22 (current S23)','Proposed S23 (current S24)','Proposed S24 (current S25)','Proposed S25 (current S26)'])
turn_plate('Page-turn proposal 2 | Bubbles, then POP!',[28,29],[27,28],[29,30],
 ['Proposed S26 (current S27)','Proposed S27 (current S28)','Proposed S28 (current S29)','Proposed S29 (current S30)'])
c.save()
doc=pdfium.PdfDocument(str(PDF))
for i,p in enumerate(doc):
 im=p.render(scale=2).to_pil().convert('RGB')
 key=f'story_{S[i]:02}' if i<len(S) else f'page_turn_{i-9:02}'
 im.save(P/'comparisons'/f'{key}.png')
 if i<len(S):
  # Document screenshot crop, not art editing. Coordinates are the after page viewport.
  im.crop((1068,124,2076,844)).save(P/'after'/f'story_{S[i]:02}.png')
doc.close()
evidence=dict(page_points=[W,H],comparison_points=[CW,CH],font=dict(path=FONT.relative_to(R).as_posix(),sha256=sha(FONT)),layers=layers,text_lines=lines,book_json_sha256=sha(L/'book.json'),render_script_sha256=sha(L/'render_book.py'),status='PROPOSALS_ONLY')
(P/'layout_evidence.json').write_text(json.dumps(evidence,indent=2,ensure_ascii=False),encoding='utf8')
cards=[]
for n in S:
 title,note=notes[n]
 cards.append(f'<section id="s{n}"><h2>Story {n} · {html.escape(title)}</h2><p>{html.escape(note)}</p><a href="comparisons/story_{n:02}.png"><img loading="lazy" src="comparisons/story_{n:02}.png" alt="Story {n}: V27 before and proposed after"></a><p><a href="before/story_{n:02}.png">Before, full size</a> · <a href="after/story_{n:02}.png">After, full size</a></p></section>')
for n in [1,2]:
 cards.append(f'<section><h2>Page-turn study {n}</h2><a href="comparisons/page_turn_{n:02}.png"><img loading="lazy" src="comparisons/page_turn_{n:02}.png" alt="Proposed page-turn comparison"></a></section>')
page='''<!doctype html><html lang="en"><meta charset="utf-8"><title>Mermaid Roshan · Before and after proposals</title><meta name="viewport" content="width=device-width,initial-scale=1"><style>
*{box-sizing:border-box}body{margin:0;background:#122c40;color:#edf8ff;font:17px/1.55 system-ui}header,main{max-width:1500px;margin:auto;padding:24px}header{max-width:1100px;padding-top:40px}h1{font-size:34px;line-height:1.2}h2{font-size:23px}section{background:#e8f3f9;color:#183348;border-radius:16px;margin-bottom:32px;padding:20px}img{display:block;width:100%;height:auto;border-radius:5px}a{color:#0966aa}header a{color:#a8e1ff}nav{display:flex;gap:12px;flex-wrap:wrap}small{color:#accedf}.notice{padding:16px;border:1px solid #4d788f;border-radius:10px}footer{padding:20px}
</style><header><h1>Before / after visual proposals</h1><p>Ten revised page previews and two page-turn studies. Before screenshots are the unchanged V27 book. After pages are separate, editable proposals at the same 7 × 5 inch proportions.</p><p><a href="BEFORE_AFTER.pdf">Open the complete comparison PDF</a> · <a href="README.md">Scope and remaining work</a> · <a href="manifest.json">Source and output manifest</a></p><nav>'''+''.join(f'<a href="#s{n}">Story {n}</a>' for n in S)+'''</nav><p class="notice">Adult review copy. The child-facing Lamb-a appearance has no clue, arrow or label. This set shows one hiding place; the eventual book would contain only two or three. The full manuscript has not been reordered or replaced.</p><p>Still open: the dirty-castle source check, waterfall-clearing action, rescue-room continuity, the remaining finale ceilings, further hidden appearances and a complete read-through after revision. These samples do not claim whole-book or print acceptance.</p></header><main>'''+''.join(cards)+'''</main></html>'''
(P/'PREVIEWS.html').write_text(page,encoding='utf8')
print(json.dumps(dict(pdf=str(PDF),comparisons=12,after_pages=10,text_lines=len(lines))))
