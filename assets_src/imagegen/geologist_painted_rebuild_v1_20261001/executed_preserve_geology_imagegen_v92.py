from pathlib import Path
import shutil,json,hashlib
p=Path(__file__).with_name('preserve_geology_imagegen_v91.py')
source=p.read_text(encoding='utf-8')
source=source.replace("geology_imagegen_v91_inputs.json","geology_imagegen_v92_inputs.json")
source=source.replace("records=[]","records=json.loads((out/'GENERATED_NATIVE_REGISTER_V1.json').read_text(encoding='utf-8'))['records']")
source=source.replace("reference_images=[]","reference_images=[dict(x,sha256=hashlib.sha256((r/x['path']).read_bytes()).hexdigest()) for x in job.get('references',[])]")
source=source.replace("executed_preserve_geology_imagegen_v91.py","executed_preserve_geology_imagegen_v92.py").replace("executed_geology_imagegen_v91_inputs.json","executed_geology_imagegen_v92_inputs.json")
source=source.replace("SIX_NATIVE_GENERATIONS_PRESERVED_INDIVIDUAL_REVIEW_PENDING","ELEVEN_NATIVE_GENERATIONS_PRESERVED_INDIVIDUAL_REVIEW_PENDING")
exec(compile(source,str(Path(__file__)),'exec'))
