"""Read-only V40 comparison/sequence/contact diagnostics from exact PDF proofs."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,shutil
import pypdfium2 as pdfium
V=Path(__file__).resolve().parent;C=V/'complete';O=V.parent/'v39_owner_corrections';D=V/'details';D.mkdir(exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,d):p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf8',newline='\n')
board=Image.new('RGB',(1512,575),'#d8e3ed');d=ImageDraw.Draw(board)
for j,(v,label) in enumerate([(O,'V39 / previous'),(V,'V40 / wider source-only composition')]):
 im=Image.open(v/'complete/page_02.png');im.thumbnail((756,540));board.paste(im,(j*756,30));d.text((j*756+8,8),label,fill='black')
board.save(D/'comparison_02.png')
im=Image.open(C/'page_02.png')
details={'landed_wheels':(360,790,650,902),'castle_path':(965,680,1270,890),'playground':(400,510,940,740),'plane_matte':(210,585,720,870)}
for name,box in details.items():
 x=im.crop(box);x.resize((x.width*2,x.height*2),Image.Resampling.LANCZOS).save(D/(name+'.png'))
sequence=Image.new('RGB',(1512,390),'#d8e3ed');d=ImageDraw.Draw(sequence)
for j,n in enumerate([1,2,3]):
 x=Image.open(C/f'page_{n:02}.png');x.thumbnail((504,360));sequence.paste(x,(j*504,0));d.text((j*504+8,365),f'Story{n}; PDF{n+1}',fill='black')
sequence.save(D/'arrival_sequence.png')
edoc=pdfium.PdfDocument(str(C/'Mermaid_Roshan_Book_V40_Email.pdf'));edoc[2].render(scale=1.5).to_pil().convert('RGB').save(D/'email_page_02.png');edoc.close()
for name in ['reveals.jpg','turns_before_after.jpg']:shutil.copyfile(O/'complete'/name,C/name)
pagination=json.loads((O/'complete/print_pagination.json').read_text('utf8'));pagination.update(revision='V40',baseline='Exact V39/V36 binding sequence preserved');save(C/'print_pagination.json',pagination)
(V/'REVISION_REVIEW.html').write_text('<!doctype html><meta charset="utf-8"><title>V40 wider arrival</title><style>body{margin:24px;font:18px/1.5 system-ui;background:#e7f1f6;color:#163047}img{max-width:100%;display:block;margin:24px 0}</style><h1>V40: arrival in one connected place</h1><p>PDF3 / story2 only. Existing landscape, castle and playground cutouts plus exact demo plane pixels. No otter, full-scene redraw or stretched panorama. Condensed book layout, not an exact runtime camera or map.</p><p><a href="complete/READ_BOOK.html">Read</a> · <a href="complete/Mermaid_Roshan_Book_V40_Email.pdf">Email PDF</a> · <a href="composition_provenance.json">Layer recipe</a> · <a href="peer_review/README.md">Independent critique</a> · <a href="visual_audits.json">Five focused reviews</a></p><h2>Previous / current</h2><img src="details/comparison_02.png"><h2>Flight, arrival, castle</h2><img src="details/arrival_sequence.png"><h2>Wheel contact</h2><img src="details/landed_wheels.png"><h2>Castle route</h2><img src="details/castle_path.png">',encoding='utf8',newline='\n')
save(V/'changed_page_review.json',dict(baseline='f55c094cfde2c1722eb210c74f85b868a4158ce9',page=2,pdf_sha256=sha(C/'Mermaid_Roshan_LANDSCAPE_ROUGH.pdf'),before_sha256=sha(O/'complete/page_02.png'),after_sha256=sha(C/'page_02.png'),notes='Owner requested no otter and wider playground plus castle composition. R01 gear/leaf overlap corrected by complete plane placement and native wheel-contact shadows.33 other proofs exact. Native source resolution/print and A9 holds remain.'))
print('Exact V40 diagnostics ready')
