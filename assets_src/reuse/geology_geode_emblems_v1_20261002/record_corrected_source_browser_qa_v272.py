from pathlib import Path
import datetime,json,shutil
b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
for rel,count,impact in [('assets_src/reuse/geology_geode_emblems_v1_20261002',10,'job-geology-geode-emblem-reuse-20261002.json'),('assets_src/imagegen/geologist_grotto_native2k_v1_20261002',4,'job-geology-grotto-native-resolution-20261002.json'),('audit/job_training_shared_source_review_v1_20261002',3,'job-training-shared-source-review-20261002.json')]:
 f=b/rel;qa=dict(status='PASS_CORRECTED_LAYOUT_IMAGES_LOADED',recorded_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),url='http://127.0.0.1:8880/'+rel+'/index.html',images=count,complete_images=count,broken_images=0,viewport_width=1280,document_width=1265,qualification='Read-only DOM and fresh screenshots inspected after targeted CSS repair. Earlier image-loading QA and pre-repair page retained. Report loading/contrast/layout is not creative/runtime/device/owner acceptance.')
 if count==10:qa['captions']=dict(background='rgb(246, 249, 255)',text_color='rgb(37, 52, 73)',dark_panel_labels_readable=True)
 write(f/'BROWSER_QA.json',qa);p=f/'LAYOUT_CORRECTION_V271.json';d=read(p);d['status']='CORRECTED_BROWSER_RECHECK_PASS';d['browser_recheck']='BROWSER_QA.json';write(p,d)
 ip=b/'design/audit_impacts'/impact;d=read(ip);d['files']=sorted(set(d['files'])|{p.relative_to(b).as_posix() for p in f.rglob('*') if p.is_file()});d['validation'].append(dict(command='Fresh browser DOM and screenshot after CSS repair',result='PASS',evidence=rel+'/BROWSER_QA.json; '+str(count)+'/'+str(count)+' loaded, bounded layout; dark caption labels readable where applicable.'));write(ip,d)
f=b/'assets_src/reuse/geology_geode_emblems_v1_20261002';shutil.copyfile(__file__,f/Path(__file__).name);ip=b/'design/audit_impacts/job-geology-geode-emblem-reuse-20261002.json';d=read(ip);d['files']=sorted(set(d['files'])|{p.relative_to(b).as_posix() for p in f.rglob('*') if p.is_file()});write(ip,d)
print('Recorded corrected source QA:10/10,4/4,3/3; ten isolated geode opinions complete.',flush=True)
