"""Source-preserving illustrated manuscript, not runtime or completed scene art."""
from __future__ import annotations
import hashlib
import json
import math
from pathlib import Path
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[3]
PACK = Path(__file__).resolve().parent
OUT = ROOT / 'output/pdf/Mermaid_Roshan_and_the_Butterfly_Garden_DRAFT_01.pdf'
W, H = 504, 360
NAVY = HexColor('#333666')
CREAM = HexColor('#fff5df')
BLUE = HexColor('#e8f6fa')
placements: list[dict] = []

def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def picture(c, sources, key, box, page, crop=None, cover=False):
    path = ROOT / sources[key]['path']
    with Image.open(path) as im:
        iw, ih = im.size
    region = crop or [0, 0, iw, ih]
    x0, y0, x1, y1 = region
    x, y, bw, bh = box
    scale = max(bw / (x1-x0), bh / (y1-y0)) if cover else min(bw / (x1-x0), bh / (y1-y0))
    rw, rh = (x1-x0)*scale, (y1-y0)*scale
    px, py = x+(bw-rw)/2, y+(bh-rh)/2
    c.saveState()
    clip = c.beginPath()
    clip.rect(x, y, bw, bh)
    c.clipPath(clip, stroke=0)
    c.drawImage(str(path), px-x0*scale, py-(ih-y1)*scale, iw*scale, ih*scale, mask='auto')
    c.restoreState()
    placements.append({'pdf_page':page,'source':key,'source_sha256':digest(path),'crop_xyxy':region,'layout_box_points':box,'treatment':'whole source image, PDF clipping/translation/uniform scaling only; no raster edits'})

def caption(c, text, size=21, top=328, color=NAVY, width=454):
    words = text.split()
    lines, line = [], ''
    for word in words:
        trial = (line+' '+word).strip()
        if line and pdfmetrics.stringWidth(trial, 'Sniglet', size)>width:
            lines.append(line); line=word
        else:
            line=trial
    if line: lines.append(line)
    assert len(lines)<=4, text
    c.setFont('Sniglet', size)
    c.setFillColor(color)
    for n, line in enumerate(lines):
        c.drawCentredString(W/2, top-n*(size+4), line)
    return top-len(lines)*(size+4)

def butterflies(c, sources, page, count=7, bottom=110):
    for n in range(count):
        if count==1:
            box=[198,bottom,108,82]
        else:
            box=[40+(n%4)*112,bottom+(n//4)*77,88,65]
        picture(c,sources,'butterfly',box,page)

def compose(c, sources, p, page):
    style=p['art']
    c.setFillColor(BLUE if p['beat'] not in ['tree','chef'] else CREAM)
    c.rect(0,0,W,H,fill=1,stroke=0)
    full=style in ['skyway','pond','bloom_full']
    if full:
        key='sky' if style=='skyway' else 'pond'
        picture(c,sources,key,[0,0,W,H],page,cover=True,crop=p.get('background_crop'))
    color=CREAM if style=='bloom_full' else NAVY
    caption(c,p['text'],color=color)
    if style=='door':
        picture(c,sources,'door_open',[46,29,236,251],page)
        picture(c,sources,'roshan',[290,35,147,202],page)
    elif style=='closed':
        picture(c,sources,'door_closed',[174,34,170,242],page)
        picture(c,sources,'roshan',[38,43,129,182],page)
    elif style=='skyway':
        picture(c,sources,'walkway',[90,0,320,230],page)
        picture(c,sources,'house',[211,139,81,91],page)
        picture(c,sources,'roshan',[106,38,64,95],page)
    elif style=='house':
        picture(c,sources,'house',[99,20,306,265],page)
    elif style=='seven':
        for box in [[35,160,48,38],[136,215,45,36],[257,161,48,38],[381,218,45,36],
                    [62,50,48,38],[217,73,45,36],[412,55,48,38]]:
            picture(c,sources,'butterfly',box,page)
        picture(c,sources,'roshan',[271,7,114,155],page)
    elif style=='home':
        picture(c,sources,'house',[176,48,162,199],page)
        for box in [[37,218,51,40],[100,167,51,40],[41,91,51,40],[111,42,51,40],
                    [360,205,51,40],[417,136,51,40],[365,63,51,40]]:
            picture(c,sources,'butterfly',box,page)
    elif style=='picnic':
        picture(c,sources,'chef',[160,20,171,207],page,crop=[0,0,256,256])
        for box in [[39,201,51,40],[106,234,51,40],[44,107,51,40],[103,38,51,40],
                    [360,220,51,40],[419,139,51,40],[365,57,51,40]]:
            picture(c,sources,'butterfly',box,page)
    elif style=='one':
        picture(c,sources,'leaf',[46,35,168,137],page)
        picture(c,sources,'butterfly',[180,150,60,46],page)
        picture(c,sources,'roshan',[267,26,171,234],page)
    elif style=='play':
        picture(c,sources,'roshan',[268,20,178,244],page)
        picture(c,sources,'butterfly',[72,175,64,50],page)
        picture(c,sources,'butterfly',[166,94,64,50],page)
    elif style=='rest':
        picture(c,sources,'roshan',[130,22,173,238],page)
        picture(c,sources,'butterfly',[278,130,131,99],page)
    elif style in ['sick','healthy','fruit_tree']:
        with Image.open(ROOT/sources['patient']['path']) as im: iw,ih=im.size
        crop=[0,0,iw/2,ih] if style=='sick' else [iw/2,0,iw,ih]
        picture(c,sources,'patient',[111,14,288,260],page,crop=crop)
        if style=='fruit_tree':
            for box in [[177,165,39,46],[279,150,39,46],[229,210,39,46]]:
                picture(c,sources,'apple',box,page)
    elif style=='book':
        picture(c,sources,'book_pose',[69,7,280,263],page)
        picture(c,sources,'patient',[350,106,113,145],page,crop=[0,0,887,887])
    elif style in ['leaf_match','spray']:
        with Image.open(ROOT/sources['medicines']['path']) as im: iw,ih=im.size
        # Uneven source-sheet spacing: exact PDF clips omit neighbouring props.
        a=[500,0,885,431]
        b=[500,433,885,887]
        picture(c,sources,'medicines',[48,31,178,205],page,crop=a)
        picture(c,sources,'medicines',[280,31,178,205],page,crop=b)
    elif style=='apples':
        for box in [[61,67,110,126],[195,109,110,126],[329,67,110,126]]:
            picture(c,sources,'apple',box,page)
    elif style in ['chef','cut']:
        picture(c,sources,'chef',[46,20,220,234],page,crop=[0,0,256,256])
        picture(c,sources,'apple',[318,74,107,125],page)
    elif style=='guide':
        picture(c,sources,'roshan',[80,35,135,198],page)
        for box in [[258,60,93,74],[322,143,93,74],[244,199,82,65]]:
            picture(c,sources,'butterfly',box,page)
    elif style=='fairy':
        picture(c,sources,'fairy',[137,9,229,278],page)
    elif style=='pond':
        picture(c,sources,'fairy',[96,27,130,181],page)
        picture(c,sources,'butterfly',[278,135,77,65],page)
    elif style in ['bud','leaves','opening','bloom_full','carry']:
        key={'bud':'bud','leaves':'bud','opening':'opening','bloom_full':'bloom','carry':'bloom'}[style]
        picture(c,sources,key,[158,27,250,246],page)
        if style=='leaves':
            for n in range(6):
                a=n*math.tau/6
                picture(c,sources,'leaf',[228+105*math.cos(a)-35,146+85*math.sin(a)-31,70,62],page)
        picture(c,sources,'fairy' if style!='carry' else 'roshan',[33,12,120,173],page)
        if style=='opening': picture(c,sources,'butterfly',[375,185,76,59],page)
    else:
        raise ValueError(style)
    c.setFont('Sniglet',7)
    c.setFillColor(color)
    c.drawRightString(482,11,str(p['number']))

def main():
    data=json.loads((PACK/'book.json').read_text(encoding='utf-8'))
    sources=data['sources']
    pdfmetrics.registerFont(TTFont('Sniglet',str(PACK/'fonts/Sniglet-Regular.ttf')))
    OUT.parent.mkdir(parents=True,exist_ok=True)
    c=canvas.Canvas(str(OUT),pagesize=(W,H),pageCompression=1,invariant=1)
    c.setTitle(data['title']+' - First Draft')
    c.setAuthor('Mermaid Roshan story development')
    c.setSubject('Source-art illustrated manuscript; story and game design unaccepted')
    c.setFillColor(BLUE);c.rect(0,0,W,H,fill=1,stroke=0)
    caption(c,'Mermaid Roshan',size=30,top=316)
    caption(c,'and the Butterfly Garden',size=24,top=277)
    picture(c,sources,'house',[265,24,189,214],1)
    picture(c,sources,'roshan',[44,32,150,195],1)
    picture(c,sources,'butterfly',[177,131,109,82],1)
    c.setFillColor(NAVY);c.setFont('Sniglet',10);c.drawCentredString(252,13,'An illustrated first draft - story and art studies')
    c.showPage()
    for p in data['pages']:
        compose(c,sources,p,p['number']+1);c.showPage()
    c.setFillColor(BLUE);c.rect(0,0,W,H,fill=1,stroke=0)
    caption(c,'A little help can grow into something wonderful.',size=24,top=307)
    picture(c,sources,'bloom',[153,45,203,210],34)
    picture(c,sources,'butterfly',[305,183,91,68],34)
    caption(c,'First draft. Existing art reused. Missing story art is recorded separately.',size=10,top=25)
    c.showPage();c.save()
    rows=[]
    for key,v in sources.items():
        path=ROOT/v['path']
        with Image.open(path) as im: dims=list(im.size)
        rows.append({'key':key,**v,'sha256':digest(path),'dimensions':dims,'source_modified':False})
    manifest={'baseline':data['baseline'],'book_status':data['status'],'pdf':{'path':str(OUT.relative_to(ROOT)).replace('\\','/'),'sha256':digest(OUT),'pages':len(PdfReader(OUT).pages),'page_points':[W,H]},'sources':rows,'placements':placements,'new_raster_art':0,'raster_derivatives':0,'source_gap_ids':sorted(set(g for p in data['pages'] for g in p.get('gaps',[]))),'limits':'All pages are source-art layout studies. PDF clipping is non-destructive page layout, not raster editing or completed action art. No runtime/cinematic/owner/child/print acceptance.'}
    assert manifest['pdf']['pages']==34
    (PACK/'SOURCE_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    print(f'BOOK|34 pages|32 story pages|{len(rows)} exact existing sources|new raster art 0|{OUT}')

if __name__=='__main__': main()
