"""Find quiet legal caption spaces in actual caption-free composed art; proposes only."""
from pathlib import Path
import json
import numpy as np
from PIL import Image
from pypdf import PdfReader,PdfWriter
import pypdfium2 as pdfium
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
V=Path(__file__).resolve().parent;L=V.parents[1];R=L.parents[2];C=V/'complete'
b=json.loads((L/'book.json').read_text('utf8'));pdfmetrics.registerFont(TTFont('Sniglet',str(L/b['font'])))
nums=[1,6,10,12,13,15,19];scratch=R/'tmp/pdfs/v34';wr=PdfWriter();rd=PdfReader(C/'Mermaid_Roshan_LANDSCAPE_ROUGH.pdf')
for n in nums:wr.add_page(rd.pages[n])
wr.remove_text()
with (scratch/'caption_spaces.pdf').open('wb') as f:wr.write(f)
doc=pdfium.PdfDocument(str(scratch/'caption_spaces.pdf'))
def lum(rgb):
 a=np.asarray(rgb,dtype=float)/255;a=np.where(a<=.04045,a/12.92,((a+.055)/1.055)**2.4);return a@np.array([.2126,.7152,.0722])
navy=float(lum(np.array([15.3,40.8,73.95])));white=float(lum(np.array([255,255,249.9])))
texts={12:'Rainbow colors\npeeked through the gunk.',13:'The pool’s magic made\nrainbow water. Whoosh!',19:'Roshan brushed them gently away.\nBaby Eagle was free!'}
ranges={1:([270,280,290],[280,288,296,304,312],[180,190,200]),6:(range(24,225,20),[58,60],[260,280,300,320,340,360,380,400,420,440]),10:(range(160,191,5),[57,58,59,60],[280,290,300,310]),12:(range(200,271,10),[58,60],[210,220,230,240,250,260,270]),13:(range(210,271,10),[58,60],[210,220,230,240,250,260]),15:(range(24,65,10),[82,84,86,88,90],[400,420,440]),19:(range(24,165,10),[58,60,62,64,66],[300,320,340,360,380,400,420,440])}
out={}
for i,n in enumerate(nums):
 image=doc[i].render(scale=.5).to_pil().convert('RGB');a=lum(image);text=texts.get(n,b['pages'][n-1]['text']);candidates=[]
 for x in ranges[n][0]:
  for y in ranges[n][1]:
   for w in ranges[n][2]:
    if x+w>480:continue
    lines=[]
    for para in text.split('\n'):
     line=''
     for word in para.split():
      trial=(line+' '+word).strip()
      if pdfmetrics.stringWidth(trial,'Sniglet',20)>w and line:lines.append(line);line=word
      else:line=trial
     lines.append(line)
    if y-26*(len(lines)-1)-5.78<24:continue
    for color,f in [('navy',navy),('white',white)]:
     scores=[]
     for j,line in enumerate(lines):
      sw=pdfmetrics.stringWidth(line,'Sniglet',20);xx=x+(w-sw)/2;yy=y-26*j
      crop=a[max(0,int(360-yy-19.12)):min(360,int(360-yy+5.78)),max(0,int(xx)):min(504,int(xx+sw))]
      median=float(np.median(crop));worst=float(np.quantile(crop,.9 if color=='white' else .1));ratio=lambda v:(max(f,v)+.05)/(min(f,v)+.05)
      scores.append(dict(text=line,typical=ratio(median),worst=ratio(worst)))
     low=min(q['worst'] for q in scores);med=min(q['typical'] for q in scores)
     candidates.append(dict(x=x,y=y,width=w,color=color,minimum_worst=low,minimum_typical=med,lines=scores,text=text))
 candidates.sort(key=lambda q:(q['minimum_worst']>=3,q['minimum_typical']>=4.5,q['minimum_worst']),reverse=True)
 out[n]=candidates[:3]
 print(n,json.dumps(out[n][0],ensure_ascii=False))
(V/'caption_space_candidates.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
