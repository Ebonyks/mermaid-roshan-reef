"""Archive exact V38 inputs and owner-selected demo-frame pixels without editing originals."""
from pathlib import Path
import datetime,hashlib,json,subprocess
from PIL import Image
from pypdf import PdfReader,PdfWriter
import pypdfium2 as pdfium
V=Path(__file__).resolve().parent;L=V.parents[1];R=L.parents[2];OLD=V.parent/'v38_audit_fixes'
for name in ['art','inputs','complete','details','peer_review']:(V/name).mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
baseline=json.loads((OLD/'BOOK_CURRENT.json').read_text('utf8'));save(V/'BOOK_BASELINE.json',baseline)
scratch=R/'tmp/pdfs/v39';scratch.mkdir(parents=True,exist_ok=True)
reader=PdfReader(OLD/'complete/Mermaid_Roshan_LANDSCAPE_ROUGH.pdf');writer=PdfWriter()
for n in [0,1]:writer.add_page(reader.pages[n])
writer.remove_text()
with (scratch/'inputs_no_text.pdf').open('wb') as f:writer.write(f)
doc=pdfium.PdfDocument(str(scratch/'inputs_no_text.pdf'));rows=[]
for i,n in enumerate([0,1]):
 p=V/'inputs'/('cover_composed.png' if n==0 else 'window_composed.png');doc[i].render(scale=1.5).to_pil().convert('RGB').save(p)
 rows.append(dict(path=p.relative_to(R).as_posix(),sha256=sha(p),source=(OLD/'complete/Mermaid_Roshan_LANDSCAPE_ROUGH.pdf').relative_to(R).as_posix(),source_sha256=sha(OLD/'complete/Mermaid_Roshan_LANDSCAPE_ROUGH.pdf'),page=n,operation='Exact V38 composed-art input at1512x1080; vector text omitted using pypdf remove_text, actual source art/masks unchanged. Input only, not new accepted scene pixels.'))
for name,source,box in [('cover_tails',V/'inputs/cover_composed.png',[0,425,545,760]),('puffs24',L/baseline['sources']['v34_care_bank24']['file'],[1040,890,1370,1040]),('puffs25',OLD/'complete/page_25.png',[1060,910,1280,1040]),('window_panel',V/'inputs/window_composed.png',[1040,500,1145,620]),('rumi_caudal_target',V/'inputs/cover_composed.png',[80,630,395,745]),('rumi_caudal_reference',R/'assets_src/characters/rumi_2026-08-22/rumi_full_body_identity.png',[75,720,380,1024]),('daddy_caudal_target',V/'inputs/cover_composed.png',[0,445,325,730]),('daddy_caudal_reference',R/'assets_src/cinematics/d1_c02_first_dirty_castle_discovery_visual_v1/handoff_art/characters/daddy_daddy_master.png',[900,1000,1677,2320])]:
 p=V/'inputs'/(name+'.png');Image.open(source).crop(box).save(p);rows.append(dict(path=p.relative_to(R).as_posix(),sha256=sha(p),source=source.relative_to(R).as_posix(),source_sha256=sha(source),crop=box,operation='Exact unmodified source-pixel crop; originals preserved.'))
demo=R.parents[1]/'export/day_one_review_demo_2026-09-09/parts/00_OPENING_C00_C01.mp4'
assert demo.is_file(),demo
for frame in [384,396,408]:
 p=V/'inputs'/f'demo_landing_frame_{frame}.png'
 subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-i',str(demo),'-vf',f'select=eq(n\\,{frame})','-frames:v','1',str(p)],check=True)
 rows.append(dict(path=p.relative_to(R).as_posix(),sha256=sha(p),source='export/day_one_review_demo_2026-09-09/parts/00_OPENING_C00_C01.mp4',source_sha256=sha(demo),source_location=str(demo),source_role='Owner-selected otter opening, intact V05 edit; current owner explicitly directs this demo landing as book reference',frame_index_zero_based=frame,rate='24/1',time_seconds=frame/24,operation='One exact decoded native1280x720 RGB frame; no retiming, new pixels or recompression. Candidate page source; final selected frame remains separately recorded.'))
if (V/'occlusion_input_provenance.json').exists():rows.extend(json.loads((V/'occlusion_input_provenance.json').read_text('utf8')))
save(V/'input_provenance.json',rows)
save(V/'revision_scope.json',dict(baseline='cb3e2995df8fdf82e308352eb850b3e285f2c6c4',owner_date='2026-10-25',changed_pdf_pages=[0,1,2,24,25],unchanged_pdf_pages=[n for n in range(34) if n not in [0,1,2,24,25]],page_number_mapping='Owner PDF2/3 correspond to story1/2; cover is PDF1. Grand Puff tissue-box vignettes on stories24/25.',corrections=dict(cover='Daddy/Rumi tails repaired locally to identity references; existing Lamma added visibly to cover',window='Restore exact existing Roshan stained-glass image inside existing castle arch',landing='Replace source with exact demo ground landing by slide/swings; no invented water/dock replacement',puffs='Replace handkerchief cues with tissue box and gently unwell little-puff expressions; preserve sofa/water and two+two pearl anatomy'),authority='Current owner correction supersedes old water landing and cloth-only care props in these named places. Full-scene redraw remains prohibited. Cover Lamma is an additional owner-requested silent appearance, retaining existing10/rear cameos.',scope='Static book only; V38 remains sealed; no runtime/release/print edition.'))
print('Archived exact baseline inputs and demo frames; no originals changed')
