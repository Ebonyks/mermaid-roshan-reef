"""Fail-closed V44 source/scope/export checks; open audit findings are not a pass."""
from pathlib import Path
import hashlib,json,subprocess,sys
import numpy as np
from PIL import Image
from pypdf import PdfReader
import pypdfium2 as pdfium

V=Path(__file__).resolve().parent;R=V.parents[4];L=V.parents[1];C=V/'complete'
sha=lambda data:hashlib.sha256(data).hexdigest()
baseline='5284b6dc0774ef24059790ab7a3a45da15c28c05'
b=json.loads((V/'BOOK_CURRENT.json').read_text('utf8'));old=json.loads((V/'BOOK_BASELINE.json').read_text('utf8'))
assert b==json.loads((L/'book.json').read_text('utf8'))
assert old==json.loads(subprocess.check_output(['git','show',baseline+':books/chapter_one/landscape/book.json'],cwd=R))
for key in old:
 if key not in ['cover','sources','revision','download_pdf_href']:assert b[key]==old[key],key
assert b['download_pdf_href']=='Mermaid_Roshan_and_the_Dust_Bunnies_V44.pdf'
for key in old['sources']:assert b['sources'][key]==old['sources'][key],key
assert set(b['sources'])-set(old['sources'])=={'v44_door_repair'}
cover_control=json.loads(json.dumps(b['cover']));cover_control['treatment']=old['cover']['treatment']
assert len(cover_control['local_patches'])==len(old['cover']['local_patches'])+2
assert all(x['source']=='v44_door_repair' for x in cover_control['local_patches'][-2:])
cover_control['local_patches']=cover_control['local_patches'][:-2]
for row in cover_control['title_lines']:assert row['x']==113;row['x']=133
assert cover_control==old['cover'],'Uncommissioned cover controls changed'
paths={(L/q['file']).resolve().relative_to(R).as_posix() for q in old['sources'].values()}
paths.add((L/old['font']).resolve().relative_to(R).as_posix());sealed=[]
for path in sorted(paths):
 data=subprocess.check_output(['git','show',baseline+':'+path],cwd=R)
 assert (R/path).read_bytes()==data,path
 sealed.append(dict(path=path,sha256=sha(data)))
record=json.loads((V/'generation_record.json').read_text('utf8'));assert len(record['attempts'])==2
for q in record['attempts']:
 for path,key in [('native','sha256'),('input','input_sha256'),('prompt','prompt_sha256')]:assert sha((V/q[path]).read_bytes())==q[key]
old_pdf=L/'revisions/v43_dust_bunnies_cover/complete/Mermaid_Roshan_and_the_Dust_Bunnies_V43.pdf'
new_pdf=C/'Mermaid_Roshan_and_the_Dust_Bunnies_V44.pdf';cover_pdf=C/'Mermaid_Roshan_Dust_Bunnies_Cover_V44.pdf'
x,y=PdfReader(old_pdf),PdfReader(new_pdf);dx,dy=pdfium.PdfDocument(str(old_pdf)),pdfium.PdfDocument(str(new_pdf))
assert len(x.pages)==len(y.pages)==34 and y.metadata.title==b['title'];checks=[]
for i in range(1,34):
 a,c=x.pages[i],y.pages[i]
 assert a.mediabox==c.mediabox and a.extract_text()==c.extract_text(),i
 assert a.get_contents().get_data()==c.get_contents().get_data(),i
 images=0;masks=0
 for name,val in a['/Resources'].get('/XObject',{}).items():
  u=val.get_object();w=c['/Resources']['/XObject'][name].get_object()
  if u.get('/Subtype')!='/Image':continue
  assert u._data==w._data and u['/Width']==w['/Width'] and u['/Height']==w['/Height'],(i,name)
  images+=1
  if u.get('/SMask'):assert u['/SMask'].get_object()._data==w['/SMask'].get_object()._data;masks+=1
 pa=np.asarray(dx[i].render(scale=1.5).to_pil().convert('RGB'));pb=np.asarray(dy[i].render(scale=1.5).to_pil().convert('RGB'))
 assert np.array_equal(pa,pb),i
 checks.append(dict(pdf_entry=i,render_rgb_sha256=sha(pa.tobytes()),dimensions=list(pa.shape[1::-1]),text_vectors_boxes_and_image_streams_exact=True,images=images,masks=masks))
print('33/33 carried pages exact: renders, text, vectors, boxes, image streams and alpha',flush=True)
cover=pdfium.PdfDocument(str(cover_pdf));actual=np.asarray(cover[0].render(scale=1.5).to_pil().convert('RGB'))
assert np.array_equal(actual,np.asarray(Image.open(C/'page_00.png').convert('RGB')))
proof=np.asarray(Image.open(L/'revisions/v43_dust_bunnies_cover/complete/page_00.png').convert('RGB'))
mask=np.zeros(actual.shape[:2],bool);mask[:355,400:1340]=True;mask[140:680,1225:1512]=True
assert not np.any(np.any(actual!=proof,axis=2)&~mask),'Pixels changed outside door/title windows'
assert np.array_equal(actual[390:550,1328:1402],proof[390:550,1328:1402]),'Central original Puff face changed'
assert np.array_equal(actual[350:1080,:1220],proof[350:1080,:1220]),'Family, Eagle, Lamma or bucket changed'
assert np.array_equal(actual[720:1080,1220:],proof[720:1080,1220:]),'Foreground bunny group changed'
scratch=R/'tmp/pdfs/v44/default_regression';scratch.mkdir(parents=True,exist_ok=True)
program=(L/'render_book.py').read_text('utf8');program=program[:program.index("for p in B['pages']:")]+"c.save()\n"
sys.argv=['render_book.py','--book',str(V/'BOOK_BASELINE.json'),'--output',str(scratch)]
exec(compile(program,str(L/'render_book.py'),'exec'),{'__file__':str(L/'render_book.py'),'__name__':'__main__'})
reg=pdfium.PdfDocument(str(scratch/'Mermaid_Roshan_LANDSCAPE_ROUGH.pdf'))
assert np.array_equal(np.asarray(reg[0].render(scale=1.5).to_pil().convert('RGB')),proof)
provenance=json.loads((C/'cover_provenance.json').read_text('utf8'))
for q in provenance['layers']:assert sha((L/q['file']).read_bytes())==q['sha256']
text=cover[0].get_textpage();boxes=[dict(char=text.get_text_range(i,1),box=list(text.get_charbox(i))) for i in range(text.count_chars()) if text.get_text_range(i,1).strip()]
inset=(720-max(q['box'][3] for q in boxes))/2
assert inset>=18 and text.get_text_range().replace('\r\n',' ')==b['title']
geometry=dict(cover_pdf_sha256=sha(cover_pdf.read_bytes()),controls_sha256=sha((V/'BOOK_CURRENT.json').read_bytes()),minimum_top_ink_inset_logical_points=inset,required_inset=18,character_boxes_pdf_points=boxes,actual_title=text.get_text_range(),title_shift_logical_points=-20,door_tip_clearance='Visually inspected native detail; no collision. Font/size/baselines unchanged.')
(V/'title_geometry.json').write_text(json.dumps(geometry,indent=2)+'\n',encoding='utf8',newline='\n')
review=json.loads((V/'visual_audits.json').read_text('utf8'));assert len(review['passes'])==5
assert review['cover_sha256']==sha(cover_pdf.read_bytes()) and review['reading_sha256']==sha(new_pdf.read_bytes())
for q in review['passes']:
 assert q['result']=='PASS_SCOPED_DOOR_REVIEW' and not q['remaining_in_scope_defects']
 for p in q['inspected']:assert sha((V/p).read_bytes())==q['inspected_sha256'][p],p
for p,d in review['artifact_bindings'].items():assert sha((V/p).read_bytes())==d,p
audit=json.loads((V/'audit/primary_book_audit.json').read_text('utf8'));peer=json.loads((V/'peer_review/whole_book_audit.json').read_text('utf8'))
assert len(audit['pages'])==len(peer['page_reviews'])==34
assert {q['pdf_entry'] for q in audit['pages']}==set(range(34))
assert len([q for q in audit['findings'] if q['status']=='OPEN'])==2
assert audit['verdict']=='AUDIT_COMPLETE_WITH_OPEN_CONTINUITY_FINDINGS'
assert audit['final_reading_pdf_sha256']==sha(new_pdf.read_bytes())
for q in checks:assert audit['pages'][q['pdf_entry']]['decoded_rgb_sha256']==q['render_rgb_sha256']
assert audit['pages'][0]['decoded_rgb_sha256']==sha(actual.tobytes())
for q in audit['identity_sources']:assert sha((R/q['path']).read_bytes())==q['sha256']
for q in json.loads((V/'asset_derivations.json').read_text('utf8'))['files']:
 assert sha((V/q['path']).read_bytes())==q['sha256'],q['path']
 assert sha((R/q['source']['path']).read_bytes())==q['source']['sha256'],q['source']['path']
e=json.loads((C/'export_record.json').read_text());assert e['reading_sha256']==sha(new_pdf.read_bytes()) and e['cover_master_sha256']==sha(cover_pdf.read_bytes())
assert new_pdf.stat().st_size<25000000 and e['cover_compression_attempts'][-1]['psnr_db']>=40
result=dict(status='PASS_SCOPED_SOURCE_EXPORT_CHECKS',baseline=baseline,source_files_sealed=len(sealed),source_seals=sealed,body_entries_exact=checks,cover_master_sha256=sha(cover_pdf.read_bytes()),reading_sha256=sha(new_pdf.read_bytes()),cover_proof_sha256=sha((C/'page_00.png').read_bytes()),default_cover_regression='Exact V43 RGB with V43 controls and unchanged renderer',cover_change_windows_only=True,original_central_puff_and_family_eagle_lamma_bunnies_exact=True,cover_email_psnr_db=e['cover_compression_attempts'][-1]['psnr_db'],whole_book_visual_verdict=audit['verdict'],open_continuity_findings=['BK44-O01','BK44-O02'],held=audit['acceptance_holds'],issues=[])
(C/'verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf8',newline='\n')
print('V44 source/scope/export checks: ALL OK; whole-book audit retains two open continuity findings')
