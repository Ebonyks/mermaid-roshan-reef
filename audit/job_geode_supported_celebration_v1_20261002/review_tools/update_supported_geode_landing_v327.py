from pathlib import Path
import json, shutil
b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
f=b/'audit/job_geode_supported_celebration_v1_20261002'
p=b/'audit/job_review_v2_20261001/index.html'
s=p.read_text()
s=s.replace('every58 native stills/316 actual frames','all 58 native stills / 316 actual frames').replace('mounting4.5/rooted material4.6','mounting 4.5 / rooted material 4.6').replace('stage4.1/room2.8/contact2.7','stage 4.1 / room 2.8 / contact 2.7').replace('fresh375-source','fresh 375-source')
s=s.replace('317 consecutive frames','316 consecutive frames').replace('job_geode_route_emblem_runtime_v1_20261002/index.html\">Read every current','job_geode_supported_celebration_v1_20261002/index.html\">Read every current').replace('job_geode_route_emblem_runtime_v1_20261002/REVIEW.json','job_geode_supported_celebration_v1_20261002/REVIEW.json')
s=s.replace('../job_geode_route_emblem_runtime_v1_20261002/attempt_02/native_frames/geode_1280_0109.webp','../job_geode_supported_celebration_v1_20261002/attempt_02/native_frames/geode_1280_0125.webp')
s=s.replace('Complete current captured gameplay canvas. The rooted specimen is improved; flat room graphics and remote actor contact remain visible priorities.','Complete current earned-celebration canvas. Both halves rest on the painted support; crystals remain rooted inside. Flat stage graphics and remote working-hand contact remain separate priorities.')
s=s.replace('<td>4.2: unsupported placement</td>','<td>4.5: stable on the painted stone</td>').replace('</td></tr><tr><td>Existing developer menu','</td></tr><tr><td>Painted celebration support</td><td>4.6</td><td>4.5</td></tr><tr><td>Existing developer menu')
s=s.replace('celebration composition 3.3','whole celebration 4.1').replace('373 frozen literal source files','375 frozen literal source files')
start=s.index('<p>The first suite passed 81 of 82 probes')
end=s.index('</p>',start)+4
s=s[:start]+'<p>The fresh supported-geode suite runs the existing unmodified <code>scripts/ci.sh</code> against 375 frozen literal source files. <a href="../job_geode_supported_celebration_v1_20261002/full_ci_v2/RECEIPT.json">Current suite receipt</a>. Earlier route-emblem evidence remains dated history: <a href="../job_geode_route_emblem_runtime_v1_20261002/full_ci_v1/RECEIPT.json">first 81/82 crest-location failure</a> and <a href="../job_geode_route_emblem_runtime_v1_20261002/full_ci_v2/RECEIPT.json">corrected 82/82 on 373 sources</a>. No probe was relaxed; earlier green evidence does not transfer to the current source.</p>'+s[end:]
s=s.replace('1,726 entries','1,727 entries').replace('49 runtime prop regions','50 runtime prop regions').replace('Three additional current geode mounted','Four additional current geode mounted').replace('refresh_current_job_review_v31.py','refresh_current_job_review_v32.py')
s=s.replace('<ul><li><a href="../job_geology_room_route','<ul><li><a href="../job_geode_route_emblem_runtime_v1_20261002/index.html">Previous four-use geode route and unsupported celebration</a></li><li><a href="INDEX_BEFORE_SUPPORTED_GEODE_V326.original.html">Preserved prior landing at this review transition</a></li><li><a href="../job_geology_room_route')
s=s.replace("fetch('../job_geode_route_emblem_runtime_v1_20261002/full_ci_v2/RECEIPT.json')","fetch('../job_geode_supported_celebration_v1_20261002/full_ci_v2/RECEIPT.json')")
p.write_text(s,encoding='utf-8',newline='\n')
for name in ['report','register']:
 shutil.copyfile(Path('C:/Users/Peter/Documents/mermaid-roshan-reef/tmp')/('supported_geode_'+name+'_v326.png'),f/('browser_'+name+'_v326.png'))
proof={'status':'BROWSER_DIRECT_REVIEW_RECORDED','report':{'images':40,'broken_loaded_images':0,'individual_rows':25,'native_current_links':374,'screenshot':'browser_report_v326.png'},'register':{'entries':1727,'current_geode_use_rows':5,'inclusive_current_geode_mounted_priorities':4,'broken_loaded_images':0,'screenshot':'browser_register_v326.png'},'qualification':'Browser UI/load/navigation evidence only; direct native-canvas artwork opinions are in REVIEW.json. No owner approval.'}
(f/'BROWSER_REVIEW_V326.json').write_text(json.dumps(proof,indent=2)+'\n',encoding='utf-8',newline='\n')
shutil.copyfile(Path(__file__),f/'review_tools'/Path(__file__).name)
ip=b/'design/audit_impacts/job-geode-supported-celebration-20261002.json';d=json.loads(ip.read_text());d['files']=sorted(set(d['files'])|{x.relative_to(b).as_posix() for x in f.rglob('*') if x.is_file()})
d['validation'].append({'command':'Direct browser review: supported-geode report and V32 five-use register','result':'PASS','evidence':f.relative_to(b).as_posix()+'/BROWSER_REVIEW_V326.json; saved surrounding-context screenshots, 25 opinion rows / 374 current native links / no broken loaded images.'})
ip.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
allow=b/'tmp/v2_preview_allowed.json';a=json.loads(allow.read_text());assert isinstance(a,list);a=sorted(set(a)|set(d['files']));allow.write_text(json.dumps(a,indent=2)+'\n',encoding='utf-8',newline='\n')
print('Current supported-geode landing and UI proofs written; prior evidence preserved.')
