"""Freeze the owner-rejected cover baseline and derive caption-free references."""
from pathlib import Path
import hashlib,json
import pypdfium2 as pdfium
from pypdf import PdfReader,PdfWriter
V=Path(__file__).resolve().parent;L=V.parents[1];R=L.parents[2]
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert not (V/'BOOK_BASELINE.json').exists(),'Never overwrite the frozen baseline'
(V/'BOOK_BASELINE.json').write_bytes((L/'book.json').read_bytes())
save(V/'REVISION_SCOPE.json',dict(baseline='2719d2fcf66afe4cb73b8445087e09dd52319849',date='2026-10-17',changed_pdf_pages=[0,33],interior_pages_unchanged=list(range(1,33)),owner_request='The cover and back page feature parts of the story that do not actually exist. Repair them.',front='Existing rendered art and identity patches retained; only lower-right pink paint cup/spill and Puff face inpainted.',rear='Exact existing story26 source scene/extensions reused without its caption; tiny canonical Lamma local cameo.',source_scene_rule='No full-scene redraw or newly invented scene. Caption-free PNGs are reference-only PDF renders, not replacement delivery art.',delivery=dict(repository='Ebonyks/mermaid-roshan-reef',branch='codex/mermaid-roshan-picture-book',access='Anonymous HTTPS immutable revision'),review='Root visual/editorial review with exact machine binding; no new independent-agent or clinical approval claim.'))
scratch=R/'tmp/pdfs/book_cover_v33';scratch.mkdir(parents=True,exist_ok=True)
source=L/'revisions/v32_rainbow_story/complete/Mermaid_Roshan_LANDSCAPE_ROUGH.pdf'
reader=PdfReader(source);writer=PdfWriter()
for n in [0,26]:writer.add_page(reader.pages[n])
writer.remove_text()
refpdf=scratch/'caption_free_reference.pdf'
with refpdf.open('wb') as f:writer.write(f)
doc=pdfium.PdfDocument(str(refpdf));refs=[]
for i,name in enumerate(['front_reference','washing_reference']):
 p=scratch/(name+'.png');doc[i].render(scale=1484/504).to_pil().convert('RGB').save(p)
 refs.append(dict(path=p.relative_to(R).as_posix(),sha256=sha(p),native_size=[1484,1060],role='Reference-only rendering of original accepted PDF artwork with text removed; no delivery pixels',source_pdf=str(source.relative_to(R).as_posix()),source_pdf_sha256=sha(source),source_page_index=[0,26][i]))
save(V/'reference_provenance.json',dict(references=refs,note='Actual source layer paths/hashes/transforms remain in baseline page_provenance.json; final delivery reuses those source layers, never the reference raster.'))
print(json.dumps(refs,indent=2))
