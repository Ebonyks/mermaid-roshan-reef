"""Package only the assets actually used by a rendered landscape proof."""
from pathlib import Path
import argparse,hashlib,json,zipfile
ROOT=Path(__file__).resolve().parent

def digest(data):return hashlib.sha256(data).hexdigest()

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--proof',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
 provenance=json.loads((args.proof/'page_provenance.json').read_text(encoding='utf8'))
 book=json.loads((ROOT/'book.json').read_text(encoding='utf8'))
 keys=sorted({layer['source_key'] for layer in provenance['layers']})
 expected_pages={'front_cover','back_cover',*range(1,33)}
 assert {layer['page'] for layer in provenance['layers']}==expected_pages
 payload={};portable_sources={}
 for key in keys:
  source=ROOT/book['sources'][key]['file'];data=source.read_bytes();assert all(layer['sha256']==digest(data) for layer in provenance['layers'] if layer['source_key']==key)
  name=f'art/{key}{source.suffix}';payload[name]=data;portable_sources[key]={**book['sources'][key],'file':name,'archive_source_path':book['sources'][key]['file']}
 book['sources']=portable_sources
 font=ROOT/book['font'];payload['fonts/Sniglet-Regular.ttf']=font.read_bytes();payload['fonts/OFL.txt']=(font.parent/'OFL.txt').read_bytes();book['font']='fonts/Sniglet-Regular.ttf'
 payload['book.json']=(json.dumps(book,indent=2,ensure_ascii=False)+'\n').encode('utf8')
 for name in ['render_book.py','PAGE_PLAN.md','REVIEW.md','image_edit_provenance.json','eagle_isolation_provenance.json','waterfall_progress_evidence.json','waterfall_lane_prompt.txt','border_base_prompt.txt','border_revision_evidence.json','layout_evidence.json','stress_review.json','audit_book.py','STRESS_TEST.md']:
  payload[name]=(ROOT/name).read_bytes()
 for name in ['DESIGN_LANGUAGE.md','ORIGINAL_GEMINI_BACKGROUND_PROMPT.txt']:
  payload[name]=(ROOT.parent/name).read_bytes()
 for name in ['page_provenance.json','verification.json']:
  payload['delivered_proof/'+name]=(args.proof/name).read_bytes()
 payload['README.txt']=('MERMAID ROSHAN - EDITABLE LANDSCAPE ROUGH\n\n'
 '32 story pages plus covers, 7 x 5 inches. This is a review rough, not a print master.\n'
 'Edit book.json for manuscript, artwork choice and named page layouts.\n'
 'Edit render_book.py for layout geometry and typography.\n'
 'Install Python dependencies: Pillow, reportlab, pypdfium2.\n'
 'Run from this extracted directory: python render_book.py --output output\n'
 'Open output/READ_BOOK.html or output/Mermaid_Roshan_LANDSCAPE_ROUGH.pdf.\n\n'
 'All required images and the Sniglet font/license are included at relative paths.\n'
 'Historical absolute paths inside provenance are source attribution only; the builder never reads them.\n'
 'Unused generation candidates are excluded. Only ceiling strips from finale extension images are drawn;\n'
 'all original finale scene pixels remain intact. See REVIEW.md for outstanding visual/source gaps.\n'
 'delivered_proof/page_provenance.json records the actual original delivery layers. A new rebuild writes\n'
 'fresh page_provenance.json with the relocated paths. asset_manifest.json hashes every archive payload.\n').encode('utf8')
 payload['asset_manifest.json']=(json.dumps({'format':'portable-book-source-v1','files':[{'file':name,'sha256':digest(data),'bytes':len(data)} for name,data in sorted(payload.items())],'acceptance':'rough only; portable rebuild does not establish final visual acceptance'},indent=2)+'\n').encode('utf8')
 args.output.parent.mkdir(parents=True,exist_ok=True)
 with zipfile.ZipFile(args.output,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for name,data in sorted(payload.items()):z.writestr('Mermaid_Roshan_Editable/'+name,data)
 print(json.dumps({'archive':str(args.output),'files':len(payload),'used_art_sources':len(keys),'sha256':digest(args.output.read_bytes())},indent=2))

if __name__=='__main__':main()
