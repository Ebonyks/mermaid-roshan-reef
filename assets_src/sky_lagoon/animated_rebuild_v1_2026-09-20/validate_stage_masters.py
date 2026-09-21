from pathlib import Path
from PIL import Image
import xml.etree.ElementTree as ET
import zipfile,io,json,hashlib,sys,numpy as np
W=Path(__file__).resolve().parents[3];P=Path(__file__).resolve().parent/'stage_masters';manifest=json.loads((P/'STAGE_MASTERS.json').read_text());results=[]
for layer in manifest['source_layers']:
 source=W/layer['source'];assert source.is_file(),source
 assert hashlib.sha256(source.read_bytes()).hexdigest()==layer['source_sha256'],f'source changed: {source}'
for component in manifest.get('component_sources',{}).values():
 assert hashlib.sha256((W/component['source']).read_bytes()).hexdigest()==component['sha256']
for stage in manifest['stage_masters']:
 path=P/stage['path'];assert hashlib.sha256(path.read_bytes()).hexdigest()==stage['sha256']
 with zipfile.ZipFile(path) as z:
  assert z.read('mimetype')==b'image/openraster'
  tree=ET.fromstring(z.read('stack.xml'));assert tree.attrib['w']=='2048' and tree.attrib['h']=='2048'
  layers=list(tree.find('stack'));assert len(layers)==stage['layer_count'];reconstructed=Image.new('RGBA',(2048,2048))
  for row in reversed(layers):
   image=Image.open(io.BytesIO(z.read(row.attrib['src']))).convert('RGBA');reconstructed.alpha_composite(image,(int(row.attrib['x']),int(row.attrib['y'])))
  merged=Image.open(io.BytesIO(z.read('mergedimage.png'))).convert('RGBA');assert np.array_equal(np.array(reconstructed),np.array(merged));assert reconstructed.getextrema()[3]==(255,255)
  assert hashlib.sha256(merged.tobytes()).hexdigest()==stage['merged_rgba_sha256']
 if len(sys.argv)>1:
  export=Path(sys.argv[1]);oracle=Image.new('RGBA',(2048,2048));left=stage['master_rect'][0]
  for row in sorted(manifest['source_layers'],key=lambda r:(r['z'],r['order'])):
   if not row['visible']:continue
   cell=Image.open(export/row['cell']).convert('RGBA');a,b,c,d,e,f=row['transform'];c-=left;det=a*e-b*d
   if abs(det)<1e-9:continue
   pixels=np.clip(np.array(cell,dtype=float)*np.array(row['tint']),0,255).astype('uint8');cell=Image.fromarray(pixels)
   inverse=(e/det,-b/det,(b*f-e*c)/det,-d/det,a/det,(d*c-a*f)/det)
   oracle=Image.alpha_composite(oracle,cell.transform((2048,2048),Image.Transform.AFFINE,inverse,Image.Resampling.BICUBIC))
  assert np.array_equal(np.array(oracle),np.array(merged)), 'component layering changed flattened source scene: '+stage['stage']
 results.append({'stage':stage['stage'],'size':[2048,2048],'layers':len(layers),'embedded_layer_reconstruction_exact':True,'opaque_background_coverage':True,'source_hashes_match':True,'flat_source_export_comparison_exact':len(sys.argv)>1})
(P/'VALIDATION.json').write_text(json.dumps({'results':results,'limits':'structural/coverage validation and source hashes; not a 4.9 quality score or full background decomposition claim'},indent=2)+'\n');print('SKYMASTER|three self-contained ORAs;',len(manifest['source_layers']),'source hashes; exact reconstruction|PASS')
