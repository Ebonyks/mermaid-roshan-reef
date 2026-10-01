from pathlib import Path
import hashlib,json,shutil,subprocess
r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
old=r/'audit/job_review_v2_20261001/review_tools/build_current_job_item_register_v4.py';new=old.with_name('build_current_job_item_register_v5.py');assert not new.exists();code=old.read_text()
assert '-q.region[0]*s+(220-q.region[2]*s)/2' in code
code=code.replace('-q.region[0]*s+(220-q.region[2]*s)/2','-q.region[0]*s').replace('-q.region[1]*s+(220-q.region[3]*s)/2','-q.region[1]*s')
code=code.replace('style="height:220px;width:220px;position:relative;overflow:hidden;margin:auto"', 'style="height:heightpx;width:widthpx;position:relative;overflow:hidden;margin:auto"')
code=code.replace('\\\'style="height:heightpx;width:widthpx;position:relative;overflow:hidden;margin:auto"\\\'', '\\\'style="height:\\\'+(220*q.region[3]/Math.max(q.region[2],q.region[3]))+\\\'px;width:\\\'+(220*q.region[2]/Math.max(q.region[2],q.region[3]))+\\\'px;position:relative;overflow:hidden;margin:auto"\\\'')
assert 'heightpx' not in code and 'widthpx' not in code
code=code.replace('build_current_job_item_register_v4.py','build_current_job_item_register_v5.py');new.write_text(code,encoding='utf-8')
browser=r/'audit/job_review_v2_20261001/browser_review_v4';assert not browser.exists();browser.mkdir()
stage=Path('C:/Users/Peter/Documents/mermaid-roshan-reef/tmp/day2_graphics_audit_20260930/tmp')
for name in ['craft_region_register_v10.png','craft_region_register_scrolled_v12.png','doctor_source_mobile_initial_v12.png','doctor_source_mobile_actual_v12.png','wash_viewer_mobile_initial_v12.png']:shutil.copyfile(stage/name,browser/name)
(browser/'REGIONAL_PREVIEW_FAILURE.json').write_text(json.dumps({'status':'FAIL_NEIGHBOR_PIXELS_IN_REGION_GUTTER','evidence':'craft_region_register_scrolled_v12.png','diagnosis':'Image scaling preserves atlas geometry, but a220-square clip is wider than a uniformly scaled256x454 cell. Extra neighbouring cells remain visible in the side gutter. It is a review-gallery crop error, not a source-art or runtime change.','correction':'Use the selected cell actual scaled width/height as the clipping viewport; remove centering offsets from the full-atlas image. New browser proof pending.','responsive_qualification':'The requested390px override affected the register (375px content) but not the doctor/wash tab (1265px content and screenshot). Those wrongly named mobile screenshots are desktop evidence; no doctor/wash phone-width pass is claimed.','source_png_changes':0},indent=2)+'\n',encoding='utf-8')
subprocess.run(['C:/Users/Peter/AppData/Local/Python/bin/python.exe','-X','utf8','-B',str(new)],cwd=r,check=True)
p=r/'audit/job_source_review_hall_craft_v1_20261001/index.html';s=p.read_text()
data=json.loads((r/'audit/job_source_review_hall_craft_v1_20261001/REVIEW.json').read_text())
for x in data['prop_cells']:
 scale=220/max(x['region'][2:]);w,h=x['source_dimensions'];rx,ry,rw,rh=x['region'];previous='width:%gpx;height:%gpx;left:%gpx;top:%gpx'%(w*scale,h*scale,-rx*scale+(220-rw*scale)/2,-ry*scale+(220-rh*scale)/2);current='width:%gpx;height:%gpx;left:%gpx;top:%gpx'%(w*scale,h*scale,-rx*scale,-ry*scale)
 oldtag='<div class="cell"><img style="'+previous+'"';newtag='<div class="cell" style="width:%gpx;height:%gpx"><img style="'% (rw*scale,rh*scale)+current+'"';assert oldtag in s;s=s.replace(oldtag,newtag,1)
p.write_text(s,encoding='utf-8');shutil.copyfile(Path(__file__),browser/'executed_fix_exact_region_clip_v13.py')
license=r/'ASSET_LICENSES.md';s=license.read_text()
for p in browser.glob('*.png'):s+='\n| `'+p.relative_to(r).as_posix()+'` | Native in-app browser screenshot of owned local review library | Existing project-art rights unchanged | SHA-256 `'+hashlib.sha256(p.read_bytes()).hexdigest()+'` | Exact preserved browser evidence: region crop failure or desktop-only view despite mobile filename; no source/action/mobile acceptance |'
license.write_text(s+'\n',encoding='utf-8')
p=r/'design/audit_impacts/job-review-separate-v2-20261001.json';d=json.loads(p.read_text());d['files']=sorted(set(d['files']+[x.relative_to(r).as_posix() for x in browser.rglob('*') if x.is_file()]+[new.relative_to(r).as_posix()]));d['validation'].append({'command':'Craft atlas exact-region gallery preview V4','result':'FAIL','evidence':'audit/job_review_v2_20261001/browser_review_v4/REGIONAL_PREVIEW_FAILURE.json; neighbouring cells leaked into220-square gutter. Exact cell-sized clip correction implemented, new browser proof pending; source PNGs unchanged.'});p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
print('V5 exact selected-cell clipping implemented; all source PNGs unchanged; browser verification pending.')
