"""Fail closed on words, artwork, unchanged entries, margins and composed contrast."""
from collections import Counter
import io, json
import numpy as np
from PIL import Image, ImageFont
from pypdf import PdfReader, PdfWriter
import pypdfium2 as pdfium
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from build_revision import V,L,R,C,OLD,BASE,PDF_NAME,EMAIL_NAME,read,save,sha

def words(s):return ' '.join(s.split())
def lum(a):
    a=np.asarray(a,dtype=float)/255
    a=np.where(a<=.04045,a/12.92,((a+.055)/1.055)**2.4)
    return a@np.array([.2126,.7152,.0722])
def textfree(reader,path):
    w=PdfWriter()
    for p in reader.pages:w.add_page(p)
    w.remove_text()
    with path.open('wb') as f:w.write(f)
def images(page):
    result=[]
    for obj in page['/Resources'].get('/XObject',{}).values():
        q=obj.get_object()
        if q.get('/Subtype')=='/Image':
            mask=q.get('/SMask');mask=mask.get_object()._data if mask else b''
            import hashlib
            result.append((int(q['/Width']),int(q['/Height']),hashlib.sha256(q._data).hexdigest(),hashlib.sha256(mask).hexdigest()))
    return sorted(result)

def contrast(doc,lines):
    fills={'navy':float(lum([15.3,40.8,73.95])),'white':float(lum([255,255,249.9]))}
    out=[];cache={}
    for q in lines:
        n=0 if q['page']=='front_cover' else 33 if q['page']=='back_cover' else q['page']
        if n not in cache:cache[n]=lum(doc[n].render(scale=1.5).to_pil().convert('RGB'))
        x,y,w,h=q['box'];a=cache[n][max(0,int((360-y-h)*3)):min(1080,int((360-y)*3)),max(0,int(x*3)):min(cache[n].shape[1],int((x+w)*3))]
        assert a.size,('Empty caption',q)
        f=fills[q['color']];ratio=lambda v:(max(f,v)+.05)/(min(f,v)+.05)
        typical=ratio(float(np.median(a)));worst=ratio(float(np.quantile(a,.9 if q['color']=='white' else .1)))
        verdict='FAIL' if worst<3 else 'OUTLINE_REQUIRED' if typical<4.5 else 'PASS'
        out.append(dict(q,typical=round(typical,3),worst=round(worst,3),verdict=verdict))
    return out

def main():
    b=read(V/'BOOK_CURRENT.json');old=read(V/'BOOK_BASELINE.json');m=read(V/'APPLIED_MANUSCRIPT.json');source=read(V/'MANUSCRIPT.json');scope=read(V/'revision_scope.json')
    edits=read(V/'EDITORIAL_ADAPTATIONS.json')['pages'];assert len(edits)==1 and edits[0]['page']==11
    for a,z in zip(m['pages'],source['pages']):
        if a['page']==11:
            assert z['v45_text']==edits[0]['source_text'] and a['v45_text']==edits[0]['applied_text']
            assert {k:v for k,v in a.items() if k!='v45_text'}=={k:v for k,v in z.items() if k!='v45_text'}
        else:assert a==z
    assert b==read(L/'book.json') and old==read(OLD/'BOOK_CURRENT.json')
    assert {k:v for k,v in b.items() if k not in ['pages','revision','download_pdf_href']}=={k:v for k,v in old.items() if k not in ['pages','revision','download_pdf_href']}
    changed=scope['changed_story_pages'];assert len(changed)==25
    for p,q,previous in zip(b['pages'],m['pages'],old['pages']):
        n=p['page'];assert words(p['text'])==words(q['v45_text']),n
        assert {k:v for k,v in p.items() if k not in ['text','caption','speech_bubbles']}=={k:v for k,v in previous.items() if k not in ['text','caption','speech_bubbles']},n
        assert p['caption']['size']==previous['caption']['size']==20
        if n not in changed:assert p==previous,n
        if n==21:
            for now,before,text in zip(p['speech_bubbles'],previous['speech_bubbles'],q['v45_bubbles']):
                assert words(now['text'])==words(text)
                assert {k:v for k,v in now.items() if k!='text'}=={k:v for k,v in before.items() if k!='text'}
        else:assert p.get('speech_bubbles')==previous.get('speech_bubbles')
    assert b['back_cover']['caption']['text']==m['rear_text']
    old_path=OLD/'complete/Mermaid_Roshan_and_the_Dust_Bunnies_V44.pdf'
    new_path=C/PDF_NAME;previous=PdfReader(old_path);current=PdfReader(new_path)
    assert len(previous.pages)==len(current.pages)==34
    scratch=R/'tmp/pdfs/v45/verification';scratch.mkdir(parents=True,exist_ok=True)
    textfree(previous,scratch/'baseline_art.pdf');textfree(current,scratch/'current_art.pdf')
    a=pdfium.PdfDocument(str(old_path));z=pdfium.PdfDocument(str(new_path))
    af=pdfium.PdfDocument(str(scratch/'baseline_art.pdf'));zf=pdfium.PdfDocument(str(scratch/'current_art.pdf'))
    old_body_lines=read(V.parent/'v42_doublewide_arrival/complete/page_provenance.json')['text_lines']
    new_body_lines=read(C/'caption_provenance.json')['text_lines']
    page_checks=[];issues=[]
    for n,(u,v) in enumerate(zip(previous.pages,current.pages)):
        assert u.mediabox==v.mediabox and images(u)==images(v),('Image/alpha/box changed',n)
        assert np.array_equal(np.asarray(af[n].render(scale=1.5).to_pil()),np.asarray(zf[n].render(scale=1.5).to_pil())),('Art/vector pixels changed',n)
        before=np.asarray(a[n].render(scale=1.5).to_pil().convert('RGB'));after=np.asarray(z[n].render(scale=1.5).to_pil().convert('RGB'))
        assert np.array_equal(after,np.asarray(Image.open(C/f'page_{n:02}.png').convert('RGB'))),('Stale proof',n)
        if n not in changed:
            assert u.get_contents().get_data()==v.get_contents().get_data() and u.extract_text()==v.extract_text() and np.array_equal(before,after),('Unchanged entry',n)
        else:
            p=b['pages'][n-1]
            # Existing renderer draws halo text twice (stroke then fill).
            expected=words('\n'.join(t*2 if p['caption'].get('halo') else t for t in p['text'].split('\n')))
            if n==21:expected+=' '+' '.join(words(q['text']) for q in b['pages'][20]['speech_bubbles'])
            assert words(v.extract_text())==expected,('PDF words',n,v.extract_text(),expected)
        changed_mask=np.any(before!=after,axis=2)
        permitted=np.zeros(changed_mask.shape,bool)
        for q in old_body_lines+new_body_lines:
            if q['page']!=n:continue
            x,y,w,h=q['box'];pad=2
            permitted[max(0,int((360-y-h-pad)*3)):min(1080,int((360-y+pad)*3)+1),max(0,int((x-pad)*3)):min(permitted.shape[1],int((x+w+pad)*3)+1)]=True
        outside=int((changed_mask & ~permitted).sum())
        assert outside==0,('Pixels changed outside old/new caption ink windows',n,outside)
        page_checks.append(dict(pdf_entry=n,page_box=list(v.mediabox),art_and_vector_pixels_exact=True,encoded_image_and_alpha_streams_exact=True,whole_entry_exact=n not in changed,changed_pixels=int(changed_mask.sum()),outside_caption_window_changed_pixels=outside))
        print('PDF entry',n,'art exact;','all content exact' if n not in changed else 'words exact',flush=True)
    # The V37 method carried by V42: identical fill, median and worst-decile
    # thresholds on caption-free COMPOSED PDF pixels; stroke is excluded.
    baseline_prov=read(V.parent/'v42_doublewide_arrival/complete/page_provenance.json')
    baseline_lines=[q for q in baseline_prov['text_lines'] if q['page']!='front_cover']
    baseline_lines+=read(OLD/'complete/cover_provenance.json')['text_lines']
    new_lines=read(C/'caption_provenance.json')['text_lines']
    new_lines += [q for q in baseline_lines if isinstance(q['page'],str)]
    base_contrast=contrast(af,baseline_lines);new_contrast=contrast(zf,new_lines)
    count=lambda rows:{k:sum(q['verdict']==k for q in rows) for k in ['PASS','OUTLINE_REQUIRED','FAIL']}
    for q in new_contrast:
        if q['verdict']=='FAIL':issues.append('Contrast: '+str(q))
        if q['verdict']=='OUTLINE_REQUIRED' and not(q.get('outline',0)>=1 or q.get('halo')):issues.append('Unresolved outline: '+str(q))
    save(V/'composed_caption_contrast.json',dict(method='Unchanged V37/V42 composed-art fill/median/worst10percent method; no stroke in sampling.',baseline_revision='V44 actual reading PDF',baseline_counts=count(base_contrast),counts=count(new_contrast),baseline_lines=base_contrast,lines=new_contrast))
    pdfmetrics.registerFont(TTFont('V45Gate',str(L/b['font'])))
    font=ImageFont.truetype(str(L/b['font']),2000);geometry=[]
    for q in new_lines:
        if not isinstance(q['page'],int):continue
        x,y,w,h=q['box'];size=q['font_size'];stroke=max(q.get('outline',0),.85 if q.get('halo') else 0)/2
        il,it,ir,ib=font.getbbox(q['text'],anchor='ls');factor=size/2000
        baseline=y-pdfmetrics.getDescent('V45Gate')*size/1000
        box=[x+il*factor-stroke,baseline-ib*factor-stroke,x+ir*factor+stroke,baseline-it*factor+stroke]
        margin=min(box[0],box[1],504*b['pages'][q['page']-1].get('width_multiplier',1)-box[2],360-box[3])
        row=dict(page=q['page'],text=q['text'],ink_and_stroke_box=box,minimum_inset=margin);geometry.append(row)
        if margin<24:issues.append('Text inset: '+str(row))
    save(C/'text_geometry.json',dict(method='Actual glyph ink plus half stroke, unchanged Sniglet at20logicalpt; bubbles18.',required_inset=24,lines=geometry))
    assert (C/EMAIL_NAME).read_bytes()==new_path.read_bytes() and new_path.stat().st_size<=25000000
    result=dict(status='FAIL' if issues else 'PASS_TEXT_ART_EXPORT_AND_CONTRAST',baseline=BASE,book_sha256=sha(V/'BOOK_CURRENT.json'),reading_sha256=sha(new_path),email_sha256=sha(C/EMAIL_NAME),reading_bytes=new_path.stat().st_size,story_captions_changed=25,source_manuscript_exact_changed_captions=24,declared_editorial_adaptations=[11],unchanged_pdf_entries=scope['unchanged_pdf_entries'],all34_art_layers_pixels_and_encoded_images_exact=True,page_checks=page_checks,contrast_baseline=count(base_contrast),contrast_v45=count(new_contrast),issues=issues,acceptance='Machine verification of applied draft. Page11 is a deliberate concise adaptation, not an exact source-manuscript implementation. Layout inspection, owner/new-story-facts/adaptation, actual child oral reading, qualifiedSLP and print remain separate. BK44-O01/O02 stay open.')
    save(C/'verification.json',result)
    print(json.dumps({k:v for k,v in result.items() if k not in ['page_checks','issues']},indent=2))
    if issues:
        print('\n'.join(issues));raise SystemExit(1)
if __name__=='__main__':main()
