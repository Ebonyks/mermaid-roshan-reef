"""Build read-only V39 diagnostics from exact final proof pixels."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,html
import pypdfium2 as pdfium
V=Path(__file__).resolve().parent;L=V.parents[1];R=L.parents[2];C=V/'complete';D=V/'details';D.mkdir(exist_ok=True);OLD=V.parent/'v38_audit_fixes/complete'
def read(p):return json.loads(p.read_text('utf8'))
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
rows=[]
for page,name,box in [(0,'cover_tails',(0,430,545,765)),(0,'cover_lamma',(1220,775,1450,1000)),(1,'window_portrait',(1035,495,1155,630)),(2,'ground_landing',(0,405,1512,1020)),(24,'unwell_puffs_24',(1060,915,1340,1040)),(25,'unwell_puffs_25',(1060,910,1280,1040))]:
 p=C/f'page_{page:02}.png';out=D/(name+'.png');im=Image.open(p).crop(box);im.resize((im.width*2,im.height*2),Image.Resampling.LANCZOS).save(out)
 rows.append(dict(path=out.relative_to(R).as_posix(),source=p.relative_to(R).as_posix(),source_sha256=sha(p),crop=list(box),diagnostic_scale=2,operation='Read-only exact final proof crop/enlargement; not book art',sha256=sha(out)))
notes={0:'Daddy rainbow tail and Rumi pink caudal fin repaired within declared polygons; existing painted Lamma first atlas frame added on floor with existing restrained contact shadow. Old surrounding art and original title/subtitle retained.',1:'Exact Roshan stained-glass portrait reused from approved castle artwork within the existing gold arch; window and scene retained.',2:'Exact owner-directed demo frame408 at17s: plane on wheels beside playground slide/swings, not a water landing. Native1280x720 source with declared7:5 crop; final print resolution remains open.',24:'Same two little puffs/ears/bank/flask: gently unwell expressions and aqua pop-up tissue box. No cloth-only care cue.',25:'Same two little puffs/sofa: unwell faces and tissue box; old handkerchief and cheer marks removed.'}
for n in notes:
 a=Image.open(OLD/f'page_{n:02}.png');b=Image.open(C/f'page_{n:02}.png');a.thumbnail((756,540));b.thumbnail((756,540));out=Image.new('RGB',(1512,575),'#d8e3ed');out.paste(a,(0,30));out.paste(b,(756,30));d=ImageDraw.Draw(out);d.text((8,8),f'V38 / proof {n}',fill='black');d.text((764,8),f'V39 / proof {n}',fill='black');p=D/f'comparison_{n:02}.png';out.save(p)
 rows.append(dict(path=p.relative_to(R).as_posix(),operation='Read-only labeled baseline/current final proof comparison',sources=[dict(path=x.relative_to(R).as_posix(),sha256=sha(x)) for x in [OLD/f'page_{n:02}.png',C/f'page_{n:02}.png']],sha256=sha(p)))
pdf=pdfium.PdfDocument(str(C/'Mermaid_Roshan_Book_V39_Email.pdf'));board=Image.new('RGB',(1512,1695),'#d8e3ed');draw=ImageDraw.Draw(board)
for i,n in enumerate([0,1,2,24,25,33]):
 im=pdf[n].render(scale=.75).to_pil().convert('RGB');x=i%2*756;y=i//2*565;board.paste(im,(x,y));draw.text((x+8,y+542),f'Exact email PDF: proof {n}',fill='black')
board.save(D/'email_export_review.png')
rows.append(dict(path=(D/'email_export_review.png').relative_to(R).as_posix(),source=(C/'Mermaid_Roshan_Book_V39_Email.pdf').relative_to(R).as_posix(),source_sha256=sha(C/'Mermaid_Roshan_Book_V39_Email.pdf'),pages=[0,1,2,24,25,33],operation='Read-only exact email renders at0.75scale assembled as board',sha256=sha(D/'email_export_review.png')))
pagination=read(V.parent/'v38_audit_fixes/complete/print_pagination.json');pagination.update(baseline='V39 preserves exact V38/V36 binding sequence',revision='V39',format='14x10 review only; final trim remains open; no print edition started');save(C/'print_pagination.json',pagination)
for name,pairs in [('reveals.jpg',[(8,9),(10,11),(12,13),(14,15),(22,23),(24,25),(26,27),(28,29)]),('turns_before_after.jpg',[(13,14),(23,24),(27,28)])]:
 out=Image.new('RGB',(1008,384*len(pairs)),'#d8e3ed');d=ImageDraw.Draw(out)
 for i,(a,b) in enumerate(pairs):
  for j,n in enumerate([a,b]):
   im=Image.open(C/f'page_{n:02}.png');im.thumbnail((504,360));x=j*504;y=i*384;out.paste(im,(x,y));d.text((x+8,y+365),f'{"Facing spread" if name=="reveals.jpg" else "Before/after turn"}: story {n}',fill='black')
 out.save(C/name,quality=94)
 rows.append(dict(path=(C/name).relative_to(R).as_posix(),operation='Read-only labeled review board; preserve binding/page-turn distinction',sources=[dict(path=(C/f'page_{n:02}.png').relative_to(R).as_posix(),sha256=sha(C/f'page_{n:02}.png')) for pair in pairs for n in pair],sha256=sha(C/name)))
save(V/'diagnostic_provenance.json',rows)
sections=[]
for n,note in notes.items():
 sections.append(f'<section><h2>{"Front cover" if n==0 else "Story "+str(n)}</h2><p>{html.escape(note)}</p><img src="details/comparison_{n:02}.png"></section>')
(V/'REVISION_REVIEW.html').write_text('<!doctype html><meta charset="utf-8"><title>V39 compared with V38</title><style>body{margin:24px;font:18px/1.5 system-ui;background:#e7f1f6;color:#163047}img{width:100%}section{margin:45px 0}</style><h1>V39 owner corrections</h1><p>Five named proofs changed;29proofs remain byte-identical. Owner PDF pages2/3 are story1/2. Eight native generation calls, five selected local repairs. Existing sources supply Lamma, stained glass and demo landing. A9 and native demo print-resolution holds remain explicit.</p><p><a href="complete/READ_BOOK.html">Read book</a> · <a href="complete/Mermaid_Roshan_Book_V39_Email.pdf">Email PDF</a> · <a href="visual_audits.json">Five visual passes</a> · <a href="peer_review/README.md">Independent critique</a> · <a href="complete/verification.json">Machine evidence</a></p>'+''.join(sections),encoding='utf8',newline='\n')
save(V/'changed_page_review.json',dict(baseline='cb3e2995df8fdf82e308352eb850b3e285f2c6c4',pdf_sha256=sha(C/'Mermaid_Roshan_LANDSCAPE_ROUGH.pdf'),pages=[dict(page=n,note=note,before_sha256=sha(OLD/f'page_{n:02}.png'),after_sha256=sha(C/f'page_{n:02}.png')) for n,note in notes.items()]))
print('V39 exact proof/email comparisons and binding boards generated')
