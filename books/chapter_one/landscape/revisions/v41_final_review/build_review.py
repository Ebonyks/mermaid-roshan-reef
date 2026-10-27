"""Exact V41 final-proof comparisons and contextual detail boards."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,shutil
import pypdfium2 as pdfium
V=Path(__file__).resolve().parent;C=V/'complete';O=V.parent/'v40_wide_arrival';D=V/'details';D.mkdir(exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,d):p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf8',newline='\n')
for n in [2,5]:
 board=Image.new('RGB',(1512,575),'#d8e3ed');d=ImageDraw.Draw(board)
 for j,(v,label) in enumerate([(O,'V40 / arrival OWNER_REJECTED' if n==2 else 'V40 / previous faint dust'),(V,'V41 Part1 / review candidate')]):
  im=Image.open(v/f'complete/page_{n:02}.png');im.thumbnail((756,540));board.paste(im,(j*756,30));d.text((j*756+8,8),label,fill='black')
 board.save(D/f'comparison_{n:02}.png')
for n,name,box in [(2,'landed_wheels',(140,645,390,755)),(2,'castle_route',(950,500,1480,800)),(2,'whole_playground',(500,540,1090,780)),(2,'upper_join',(0,320,1512,410)),(2,'lower_join',(0,780,1512,905)),(5,'dust',(955,545,1220,665))]:
 im=Image.open(C/f'page_{n:02}.png').crop(box);im.resize((im.width*2,im.height*2),Image.Resampling.LANCZOS).save(D/(name+'.png'))
sequence=Image.new('RGB',(1512,390),'#d8e3ed');d=ImageDraw.Draw(sequence)
for j,n in enumerate([1,2,3]):
 im=Image.open(C/f'page_{n:02}.png');im.thumbnail((504,360));sequence.paste(im,(j*504,0));d.text((j*504+8,365),f'Story{n}; PDF{n+1}',fill='black')
sequence.save(D/'arrival_sequence.png')
doc=pdfium.PdfDocument(str(C/'Mermaid_Roshan_Book_V41_Email.pdf'))
for n in [2,5]:doc[n].render(scale=1.5).to_pil().convert('RGB').save(D/f'email_page_{n:02}.png')
doc.close()
for name in ['reveals.jpg','turns_before_after.jpg']:shutil.copyfile(O/'complete'/name,C/name)
p=json.loads((O/'complete/print_pagination.json').read_text('utf8'));p.update(revision='V41 Part1',baseline='Exact V40/V36 binding sequence retained; review mapping only; Part2 print boxes not implemented');save(C/'print_pagination.json',p)
(V/'REVISION_REVIEW.html').write_text('<!doctype html><meta charset="utf-8"><title>V41 Part1 review</title><style>body{margin:24px;font:18px/1.5 system-ui;background:#e7f1f6;color:#163047}img{max-width:100%;display:block;margin:24px 0}</style><h1>V41: full Sky Lagoon and visible dust</h1><p>Owner rejected V40 arrival. Both original waters, rope-post approach, playground, landing path, mountain route and current four-tower castle now fit in one complete setting. Only sky/foreground extensions and bounded edge joins use generated repair. B2/A9 closed as not needed at11in; print Part2 held for owner illustration acceptance.</p><p><a href="complete/READ_BOOK.html">Read</a> · <a href="complete/Mermaid_Roshan_Book_V41_Email.pdf">Reading PDF</a> · <a href="world_composition_provenance.json">Source and edge recipe</a> · <a href="generation_evidence.json">All prompts/takes/references</a> · <a href="peer_review/README.md">Independent critique</a> · <a href="visual_audits.json">Five focused reviews</a></p><h2>Arrival: rejected/current</h2><img src="details/comparison_02.png"><h2>Flight, arrival, castle</h2><img src="details/arrival_sequence.png"><h2>Landing contact</h2><img src="details/landed_wheels.png"><h2>Castle and route</h2><img src="details/castle_route.png"><h2>Dust: previous/current</h2><img src="details/comparison_05.png"><img src="details/dust.png">',encoding='utf8',newline='\n')
save(V/'changed_page_review.json',dict(baseline='0d1c49d11651e292a13885413a043f8044032836',changed_pages=[2,5],pdf_sha256=sha(C/'Mermaid_Roshan_LANDSCAPE_ROUGH.pdf'),pages=[dict(page=n,before_sha256=sha(O/f'complete/page_{n:02}.png'),after_sha256=sha(C/f'page_{n:02}.png')) for n in [2,5]],notes='Complete source geography retained; first plane draft moved60nativepx up to stone. T01 extension raw join rejected; T02 selected with bounded top180/bottom300nativeworldrow feather. B1 dust stronger.32 unnamedproofs exact. P1-P8 held.'))
print('Exact V41 review boards ready')
