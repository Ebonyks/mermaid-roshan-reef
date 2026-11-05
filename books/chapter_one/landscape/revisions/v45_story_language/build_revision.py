"""Replace vector text in existing PDF pages without re-encoding any artwork."""
from pathlib import Path
import copy, hashlib, html, io, json, subprocess, sys
from PIL import Image, ImageDraw
from pypdf import PdfReader, PdfWriter
from reportlab.pdfbase import pdfmetrics
import pypdfium2 as pdfium

V=Path(__file__).resolve().parent; L=V.parents[1]; R=V.parents[4]; C=V/'complete'
H=R/'books/chapter_one/handoffs/2026-10-31_v45_story_language'
OLD=V.parent/'v44_door_and_consistency'; BASE='550a0b86216dee020d5070428ab4ddcfe0da4dc1'
PDF_NAME='Mermaid_Roshan_and_the_Dust_Bunnies_V45.pdf'
EMAIL_NAME='Mermaid_Roshan_and_the_Dust_Bunnies_V45_Email.pdf'
def read(p): return json.loads(p.read_text('utf8'))
def save(p,d):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def wrap(s,width,size=20):
    lines=[]; line=''
    for word in s.split():
        trial=(line+' '+word).strip()
        if line and pdfmetrics.stringWidth(trial,'Sniglet',size)>width: lines.append(line); line=word
        else: line=trial
    if line: lines.append(line)
    return '\n'.join(lines)
def text_environment(book,folder):
    # Reuse the exact production text functions, stopping BEFORE any art draw.
    source=(L/'render_book.py').read_text('utf8'); prefix=source[:source.index("base='landscape_base'")]
    argv=sys.argv; sys.argv=['render_book.py','--book',str(book),'--output',str(folder)]
    env={'__file__':str(L/'render_book.py'),'__name__':'v45_text_overlay'}
    try: exec(compile(prefix,str(L/'render_book.py'),'exec'),env)
    finally: sys.argv=argv
    return env
def caption(env,p):
    q=p['caption']
    env['text'](p['text'],q['x'],q['y'],q['width'],q['size'],q['align']=='center',color=q['color'],shadow=q['shadow'],halo=q.get('halo',False),outline=q.get('outline',0),line_colors=q.get('line_colors'),leading=q.get('leading'),line_baselines=q.get('line_baselines'))
    # Original balloon vectors stay in V44's page; overlay only their words.
    for q in p.get('speech_bubbles',[]):
        x,y,w,h=q['box'];size=18;count=len(q['text'].split('\n'))
        baseline=y+h/2+((count-1)*size*1.3-(pdfmetrics.getAscent('Sniglet')+pdfmetrics.getDescent('Sniglet'))*size/1000)/2
        env['text'](q['text'],x+12,baseline,w-24,size,True)
def overlay(b,folder):
    env=text_environment(V/'BOOK_CURRENT.json',folder);c=env['c']
    for p in b['pages']:
        c.setPageSize((1008*p.get('width_multiplier',1),720))
        if p['page']!=1: c.scale(2,2)
        env['PAGE']=p['page'];caption(env,p);c.showPage()
    c.save()
    return folder/'Mermaid_Roshan_LANDSCAPE_ROUGH.pdf',env['TEXT_LINES']
def verify_inputs():
    manifest=json.loads(subprocess.check_output(['git','show',BASE+':'+(H/'MANIFEST.json').relative_to(R).as_posix()],cwd=R))
    request=''.join(BASE+':'+q['path']+'\n' for q in manifest['files']).encode()
    stream=io.BytesIO(subprocess.check_output(['git','cat-file','--batch'],cwd=R,input=request));rows=[]
    for q in manifest['files']:
        head=stream.readline().split();assert head[1]==b'blob',q['path']
        data=stream.read(int(head[2]));assert stream.read(1)==b'\n'
        digest=hashlib.sha256(data).hexdigest();assert digest==q['sha256'] and len(data)==q['bytes'],q['path']
        rows.append(dict(path=q['path'],bytes=len(data),sha256=digest))
    save(V/'input_verification.json',dict(status='PASS',revision=BASE,files=rows,method='All48 required immutable Git blobs, including dependencies subsequently updated by V45.'))
def main():
    C.mkdir(parents=True,exist_ok=True);scratch=R/'tmp/pdfs/v45';scratch.mkdir(parents=True,exist_ok=True)
    verify_inputs();m=read(H/'MANUSCRIPT.json')
    (V/'MANUSCRIPT.json').write_bytes(subprocess.check_output(['git','show',BASE+':'+(H/'MANUSCRIPT.json').relative_to(R).as_posix()],cwd=R))
    old=read(OLD/'BOOK_CURRENT.json');save(V/'BOOK_BASELINE.json',old);b=copy.deepcopy(old)
    applied=copy.deepcopy(m)
    for edit in read(V/'EDITORIAL_ADAPTATIONS.json')['pages']:
        assert applied['pages'][edit['page']-1]['v45_text']==edit['source_text']
        applied['pages'][edit['page']-1]['v45_text']=edit['applied_text']
    save(V/'APPLIED_MANUSCRIPT.json',applied)
    b['revision']='V45 story and language: page11 concise editorial adaptation; artwork unchanged';b['download_pdf_href']=PDF_NAME
    env=text_environment(V/'BOOK_BASELINE.json',scratch/'font_init');env['c'].save()
    changed=[q['page'] for q in m['pages'] if q['changed']]
    placements={4:dict(y=110),5:dict(y=300),7:dict(x=24,y=82,width=456),9:dict(x=24,width=456,y=320,leading=22,align='left'),10:dict(x=24,y=82,width=456),11:dict(y=83),14:dict(x=24,width=456),15:dict(y=84),17:dict(width=205,y=290),18:dict(x=145,width=334,y=102,leading=23),24:dict(y=280),32:dict(x=24,width=456,y=320,leading=22)}
    if (V/'layout_adjustments.json').exists():
        for n,q in read(V/'layout_adjustments.json').items():placements.setdefault(int(n),{}).update(q)
    changes=[]
    for p,q in zip(b['pages'],applied['pages']):
        n=p['page'];assert n==q['page'] and p['text']==q['v44_text'],n
        if not q['changed']:continue
        p['caption'].update(placements.get(n,{}))
        # Preserve authored sentence/pause breaks wherever the page has room.
        preserve={4,5,6,7,8,10,11,14,15,16,17,19,21,24,25,26,27,29,30}
        if n in preserve:
            p['text']='\n'.join(wrap(part,p['caption']['width']) for part in q['v45_text'].split('\n'))
        elif n==30:
            p['text']=wrap(q['v45_text'],p['caption']['width'])
        elif n==31:
            parts=q['v45_text'].split('\n');p['text']=wrap(parts[0],p['caption']['width'])+'\n'+wrap(' '.join(parts[1:]),p['caption']['width'])
        else:p['text']=wrap(q['v45_text'],p['caption']['width'])
        if 'line_baselines' in p['caption'] and 'line_baselines' not in placements.get(n,{}):
            p['caption']['line_baselines']=[p['caption']['y']-i*p['caption'].get('leading',26) for i in range(len(p['text'].split('\n')))]
        if n==21:
            for balloon,words in zip(p['speech_bubbles'],q['v45_bubbles']):balloon['text']=wrap(words,balloon['box'][2]-24,18)
        changes.append(dict(page=n,status='DONE',before_caption=old['pages'][n-1]['caption'],after_caption=p['caption'],text=p['text'],box_moved=p['caption']!=old['pages'][n-1]['caption'],whitespace_reflow_only=n!=11,editorial_adaptation=n==11))
    save(V/'BOOK_CURRENT.json',b);save(L/'book.json',b)
    save(V/'revision_scope.json',dict(baseline=BASE,v44_source=m['baseline'],changed_story_pages=changed,unchanged_pdf_entries=[i for i in range(34) if i not in changed],changes=changes,art_changes=0,generation_calls=0,editorial_adaptations=[11],exact_source_caption_changes=24,page21_reading_order='Allowed existing single-top-caption fallback. Exact dialogue preserved; lower bubbles follow caption visually. No new renderer work.',page21_bubbles=b['pages'][20]['speech_bubbles'],held_pages=[]))
    overlay_path,lines=overlay(b,scratch/'overlay')
    save(C/'caption_provenance.json',dict(text_lines=lines,method='Exact existing renderer text() and balloon-text geometry; original V44 balloon vectors retained.',renderer_sha256=sha(L/'render_book.py'),logical_to_physical_scale=2))
    baseline_pdf=OLD/'complete/Mermaid_Roshan_and_the_Dust_Bunnies_V44.pdf'
    old_pdf=PdfReader(baseline_pdf);over=PdfReader(overlay_path);writer=PdfWriter()
    for n,page in enumerate(old_pdf.pages):
        if n not in changed:writer.add_page(page);continue
        temp=PdfWriter();temp.add_page(page);temp.remove_text();buf=io.BytesIO();temp.write(buf);buf.seek(0)
        clean=PdfReader(buf).pages[0];clean.merge_page(over.pages[n-1]);writer.add_page(clean).compress_content_streams()
    writer.add_metadata({'/Title':b['title'],'/Author':'Mermaid Roshan picture-book project','/Subject':'V45 text-only reading review; print and owner acceptance open'})
    # Coalesce repeated font/resources, preserving every encoded image byte.
    writer.compress_identical_objects(remove_duplicates=True,remove_unreferenced=True)
    with (C/PDF_NAME).open('wb') as f:writer.write(f)
    assert (C/PDF_NAME).stat().st_size<=25000000,'Preserved-art PDF exceeds email cap'
    (C/EMAIL_NAME).write_bytes((C/PDF_NAME).read_bytes())
    save(C/'export_record.json',dict(baseline_pdf=baseline_pdf.relative_to(R).as_posix(),baseline_sha256=sha(baseline_pdf),reading_sha256=sha(C/PDF_NAME),reading_bytes=(C/PDF_NAME).stat().st_size,email_sha256=sha(C/EMAIL_NAME),email_bytes=(C/EMAIL_NAME).stat().st_size,method='Original V44 image/alpha/vector layers copied; text removed only on25changed entries and replaced with vector text from unchanged renderer functions. No raster recompression. Email and reading files intentionally identical.',art_generation_calls=0,physical_print_status='HELD; mixed-width review, not a print edition'))
    doc=pdfium.PdfDocument(str(C/PDF_NAME));thumbs=[]
    for n in range(34):
        im=doc[n].render(scale=1.5).to_pil().convert('RGB');im.save(C/f'page_{n:02}.png');im.thumbnail((504,360));thumbs.append(im.copy())
    doc.close()
    for start in range(0,34,6):
        sheet=Image.new('RGB',(1512,772),'#d8e3ed');draw=ImageDraw.Draw(sheet)
        for j,im in enumerate(thumbs[start:start+6]):
            x,y=j%3*504,j//3*386;sheet.paste(im,(x+(504-im.width)//2,y));n=start+j
            draw.text((x+12,y+364),'Cover' if n==0 else 'Rear' if n==33 else f'Story {n}',fill='black')
        sheet.save(C/f'contact_{start//6+1}.jpg',quality=94)
    figures=[]
    for n in range(34):
        label='Cover' if n==0 else 'Rear cover' if n==33 else f'Page {n}'
        alt=label if n in [0,33] else b['pages'][n-1]['text']
        if n==21:alt+=' Bubbles: Sorry! We’ll be gentle!'
        figures.append(f'<figure class="{"wide" if n==2 else "single"}"><figcaption>{label}</figcaption><img loading="lazy" src="page_{n:02}.png" alt="{html.escape(alt)}"></figure>')
    (C/'READ_BOOK.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+html.escape(b['title'])+'</title><style>body{margin:0;background:#193449;color:#e3f5ff;font:18px/1.5 system-ui}header{max-width:1100px;margin:20px auto;padding:20px}main{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:24px;padding:24px}figure{margin:0}.wide{grid-column:1/-1}img{width:100%;display:block}figcaption{padding:8px}a{color:#9cddff}@media(max-width:800px){main{grid-template-columns:1fr}}</style><header><h1>'+html.escape(b['title'])+'</h1><p>V45 story and language review.32 story entries plus covers; arrival remains doublewide.</p><p><a href="'+PDF_NAME+'">Reading PDF</a> · <a href="'+EMAIL_NAME+'">Email PDF</a> · <a href="../README.md">Critique and checks</a></p><p>Owner, child, speech-language and physical-print acceptance remain open.</p></header><main>'+''.join(figures)+'</main></html>',encoding='utf8',newline='\n')
    print('V45 built:',len(changed),'changed captions; art untouched;',(C/PDF_NAME).stat().st_size,'bytes')
if __name__=='__main__':main()
