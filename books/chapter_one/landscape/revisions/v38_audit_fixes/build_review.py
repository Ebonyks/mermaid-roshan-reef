"""Build review-only diagnostics, comparisons and unchanged print pagination."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,html
import pypdfium2 as pdfium
V=Path(__file__).resolve().parent;L=V.parents[1];R=L.parents[2];C=V/'complete';D=V/'details';D.mkdir(exist_ok=True)
def read(p):return json.loads(p.read_text('utf8'))
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
old=V.parent/'v37_consistency_20261022/complete'
detail_rows=[]
for page,name,box in [(5,'door_dust',(965,580,1205,655)),(9,'pail_join',(1135,952,1335,1055)),(16,'caption_splash_clearance',(470,638,1045,782)),(33,'lamma',(525,508,630,617)),(33,'cobweb',(1390,0,1512,135)),(33,'carpet',(620,720,1512,1080))]:
 p=C/f'page_{page:02}.png';out=D/(name+'.png');im=Image.open(p).crop(box);im=im.resize((im.width*2,im.height*2),Image.Resampling.LANCZOS);im.save(out)
 detail_rows.append(dict(path=out.relative_to(R).as_posix(),source=p.relative_to(R).as_posix(),source_sha256=sha(p),crop=list(box),diagnostic_scale=2,operation='Read-only PDF proof crop/enlargement; never delivery art',sha256=sha(out)))
pdf=pdfium.PdfDocument(str(C/'Mermaid_Roshan_Book_V38_Email.pdf'));board=Image.new('RGB',(1512,1130),'#d8e3ed');draw=ImageDraw.Draw(board)
for i,n in enumerate([0,9,16,33]):
 im=pdf[n].render(scale=.75).to_pil().convert('RGB');x=i%2*756;y=i//2*565;board.paste(im,(x,y));draw.text((x+8,y+542),f'Email PDF: page {n}',fill='black')
board.save(D/'email_export_review.png')
detail_rows.append(dict(path=(D/'email_export_review.png').relative_to(R).as_posix(),source=(C/'Mermaid_Roshan_Book_V38_Email.pdf').relative_to(R).as_posix(),source_sha256=sha(C/'Mermaid_Roshan_Book_V38_Email.pdf'),pages=[0,9,16,33],operation='Read-only exact email PDF renders at0.75scale, assembled as comparison board',sha256=sha(D/'email_export_review.png')))
pagination=read(V.parent/'v36_next_draft/print_pagination.json')
pagination.update(baseline='V37 preserves exact V36 binding sequence',revision='V38',format='14x10 review only; final trim remains open; no print edition started')
save(C/'print_pagination.json',pagination)
# Preserve spread reveals, rather than faking consecutive reader spreads.
out=Image.new('RGB',(1008,3072),'#d8e3ed');d=ImageDraw.Draw(out)
for i,(a,b) in enumerate([(8,9),(10,11),(12,13),(14,15),(22,23),(24,25),(26,27),(28,29)]):
 for j,n in enumerate([a,b]):
  im=Image.open(C/f'page_{n:02}.png');im.thumbnail((504,360));x=j*504;y=i*384;out.paste(im,(x,y));d.text((x+8,y+365),f'Facing spread: story {n}',fill='black')
out.save(C/'reveals.jpg',quality=94)
turns=Image.new('RGB',(1008,1152),'#d8e3ed');d=ImageDraw.Draw(turns)
for i,(a,b) in enumerate([(13,14),(23,24),(27,28)]):
 for j,n in enumerate([a,b]):
  im=Image.open(C/f'page_{n:02}.png');im.thumbnail((504,360));x=j*504;y=i*384;turns.paste(im,(x,y));d.text((x+8,y+365),f'{"Before" if j==0 else "After"} page turn: story {n}',fill='black')
turns.save(C/'turns_before_after.jpg',quality=94)
for name,pages in [('reveals.jpg',[8,9,10,11,12,13,14,15,22,23,24,25,26,27,28,29]),('turns_before_after.jpg',[13,14,23,24,27,28])]:
 detail_rows.append(dict(path=(C/name).relative_to(R).as_posix(),operation='Read-only labeled review-board layout from final proof PNGs; not book art',sources=[dict(path=(C/f'page_{n:02}.png').relative_to(R).as_posix(),sha256=sha(C/f'page_{n:02}.png')) for n in pages],sha256=sha(C/name)))
save(V/'diagnostic_provenance.json',detail_rows)
notes={0:'A4 two13pt subtitle lines, right edges428.2, baselines262/246. Original cover art and seven repairs exact.',5:'A8 four faint irregular dust wisps at the closed threshold. No Roshan, curl, face or halo. Original true-alpha door retained.',9:'A5 shell pail replaces the bank plug/chain. A9 HELD: two undersized/contour-drifting native takes; approved Roshan/tub stays exact.',16:'A2 all navy with existing halo/outline, baselines110/84/58. Actual ink+stroke clears the unchanged focal box by2.12pt.',18:'A3 three manual lines keep needs help together; same white type and outline, exact artwork.',22:'A1 three manual lines avoid the orphan; same20pt, box, navy, exact artwork.',33:'A6 small Lamma head at far left curtain; A7 thin corner web and four added dust drifts. Original hall, copy, hair repair and all other pixels preserved.'}
sections=[]
for n,note in notes.items():
 sections.append(f'<section><h2>{"Front cover" if n==0 else "Rear cover" if n==33 else "Story "+str(n)}</h2><p>{html.escape(note)}</p><div class="pair"><figure><figcaption>V37</figcaption><img src="../v37_consistency_20261022/complete/page_{n:02}.png"></figure><figure><figcaption>V38</figcaption><img src="complete/page_{n:02}.png"></figure></div></section>')
(V/'REVISION_REVIEW.html').write_text('<!doctype html><meta charset="utf-8"><title>V38 compared with V37</title><style>body{margin:24px;font:18px/1.5 system-ui;background:#e7f1f6;color:#163047}h1,h2{line-height:1.2}.pair{display:grid;grid-template-columns:1fr 1fr;gap:20px}figure{margin:0}img{width:100%}section{margin:45px 0}@media(max-width:800px){.pair{grid-template-columns:1fr}}</style><h1>V38 compared with V37</h1><p>Seven named pages changed;27proofs remain byte-identical. A9native-resolution target is explicitly held. Five implementer passes and a separate second-AI critique are recorded independently; owner, child, SLP, trim and physical print remain open.</p><p><a href="complete/READ_BOOK.html">Read book</a> · <a href="complete/Mermaid_Roshan_Book_V38_Email.pdf">Email PDF</a> · <a href="visual_audits.json">Five visual passes</a> · <a href="peer_review/README.md">Second-AI handback</a> · <a href="complete/verification.json">Machine evidence</a></p>'+''.join(sections),encoding='utf8',newline='\n')
save(V/'changed_page_review.json',dict(baseline='eb405fe45edbcc37b59bebebba475de445cffb58',pdf_sha256=sha(C/'Mermaid_Roshan_LANDSCAPE_ROUGH.pdf'),pages=[dict(page=n,note=note,before_sha256=sha(old/f'page_{n:02}.png'),after_sha256=sha(C/f'page_{n:02}.png')) for n,note in notes.items()]))
# Record every actual source crop, including the narrowly focused second carpet input.
crops=read(V/'input_crops.json');p=V/'inputs/rear_carpet.png';origin=V.parent/'v36_rear_composition_20261021/rear_scene_attempt1.png'
crops=[q for q in crops if not q['path'].endswith('rear_carpet.png')]
crops.append(dict(path=p.relative_to(R).as_posix(),sha256=sha(p),source=origin.relative_to(R).as_posix(),source_sha256=sha(origin),crop=[600,700,1484,1060],operation='Exact source crop for second A7 dust take'))
save(V/'input_crops.json',crops)
print('V38 review artifacts generated')
