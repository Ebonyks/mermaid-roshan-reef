"""Prepare a source-bound review packet without granting creative acceptance."""
import hashlib,json,struct,subprocess,time
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];PROJECT=ROOT.parents[2]
REL=ROOT.relative_to(PROJECT).as_posix();BRANCH='codex/sky-lagoon-review-refinement-20261001'
OLD=PROJECT/'assets_src/cinematics/sky_lagoon_moderate_motion_v2_2026-09-30'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d): p.write_text(json.dumps(d,indent=2),encoding='utf-8')
def describe():
 task=json.loads((ROOT/'TASK_START.json').read_text());previous=json.loads((OLD/'TASK_START.json').read_text())
 task['objects']=previous['objects']
 addition=' Review also reproduced berry-cluster teleportation in v2 states 4 and 5; six new leaf poses retain two fixed three-berry junctions.'
 task['generation_gap']=task['generation_gap'].split(addition)[0]+addition
 task['result']={'status':'AGENT_REVIEWED_REFERENCE_CANDIDATE','object_masters':10,'raster_states':72,'scene':[1920,640,48,12],'runtime_integration':False}
 write(ROOT/'TASK_START.json',task)
 prompts=json.loads((ROOT/'PROMPT_SET.json').read_text())
 write(ROOT/'objects/07_swing/GENERATION.json',{'id':'07_swing','mode':'built-in image_gen','near':prompts['swing_near'],'far':prompts['swing_far'],'native_dimensions':[1024,1536],'purpose':'Bounded topology and pitch-continuity correction; no final cinematic generation'})
 write(ROOT/'objects/02_huckleberry/GENERATION.json',{'id':'02_huckleberry','mode':'built-in image_gen',**prompts['huckleberry'],'native_dimensions':[1024,1536],'postprocess':'Aseprite stationary berry-junction mask; new leaf silhouettes retained'})
 for p in [ROOT/'objects/07_swing/generated_native.png',ROOT/'objects/02_huckleberry/REPAIR_PROMPTS.json',ROOT/'production/finish.py']:
  if p.exists(): p.unlink() # Own new derivative copies; previous v2 remains intact.
 builder=ROOT/'production/build.py';s=builder.read_text();s=s.replace("if __name__ == '__main__': main()","if __name__ == '__main__': raise SystemExit('Use production/refine.py; this module supplies read-only source analysis and bounded import helpers.')");builder.write_text(s,encoding='utf-8')
 lua=ROOT/'production/import_pose_sheet.lua';s=lua.read_text();s=s.replace('local natives={[cfg.input]=native}\nlocal natives={[cfg.input]=native}','local natives={[cfg.input]=native}')
 repeated=" local input=p.input or cfg.input\n if not natives[input] then natives[input]=Image{fromFile=dir..'/'..input} end\n local source=natives[input]\n"
 s=s.replace(repeated+repeated,repeated)
 block="""-- Front ropes remain visibly attached; the shell back must not hide them.
  rope(out,193,118,math.floor(lx+.5),math.floor(ly+.5));rope(out,320,118,math.floor(rx+.5),math.floor(ry+.5))"""
 s=s.replace(block,"""-- Front ropes remain visibly attached; the shell back must not hide them.
  if app.params.foreground~='false' then
   rope(out,193,118,math.floor(lx+.5),math.floor(ly+.5));rope(out,320,118,math.floor(rx+.5),math.floor(ry+.5))
  end""")
 if 'local output=' not in s:
  s=s.replace("local dir=root..'/objects/'..id","local dir=root..'/objects/'..id\nlocal output=app.params.output or dir")
  s=s.replace("out:saveAs(dir..string.format('/frames/frame_%02d.png',n-1))","out:saveAs(output..string.format('/frames/frame_%02d.png',n-1))")
  s=s.replace("sprite:saveAs(dir..'/'..id..'.aseprite')","sprite:saveAs(output..'/'..id..'.aseprite')")
 lua.write_text(s,encoding='utf-8')
 samples=json.loads((ROOT/'SAMPLES.json').read_text())
 html=(ROOT/'index.html').read_text(encoding='utf-8')
 for bad,good in [('Â·','·'),('Ã—','×'),('Â½','½'),('â€¦','…')]: html=html.replace(bad,good)
 addition='Painted contact shadows ground the playground. Smoke now starts at the upper cabin roof. '
 while addition+addition in html: html=html.replace(addition+addition,addition)
 html=html.replace('Moderate animation studies','Reviewed animation studies')
 html=html.replace('These are motion studies for choosing the next cleanup pass; the six-key cycles still need more drawings for finished animation.','The swing now has twelve pitch drawings. This revision corrects changing berry locations, rope occlusion, grounding and synchronized motion; these are reviewed environment references.')
 html=html.replace('Motion studies','Reviewed studies').replace('for(const s of samples)show(s,state(s,time))','for(const s of samples)show(s,state(s,time+(s.phase||0)))')
 html=html.replace('Play 4-second video','Play reviewed 4-second video')
 if addition not in html:html=html.replace('Door keys are shown inside the castle aperture; its original portrait receives light only.',addition+'Door keys are shown inside the castle aperture; its original portrait receives light only.')
 html=html.replace('<a href="PROMPT_SET.json">Exact prompt set</a>','<a href="PROMPT_SET.json">Correction prompts</a> · <a href="REVIEW.json">Audit and corrections</a>')
 (ROOT/'index.html').write_text(html,encoding='utf-8')
 lines=['# Sky Lagoon reviewed animation reference — v3','',
 'Owner-directed audit/correction iteration of the ten moderate samples and Sky Lagoon composition. `AGENT_REVIEWED_REFERENCE_CANDIDATE`; owner, runtime, device and child acceptance remain open.','',
 'Open the local PNG gallery at http://127.0.0.1:8191/. Durable exchange record: the GitHub packet and exact anonymous byte-verification receipt.','',
 'The approved 6144×2048 panorama and shared castle/bridge anchor are preserved. The editable scene remains 1920×640, 48 frames / 12 fps / four seconds. It is an environment reference composite, not a game screenshot or accepted cinematic.','',
 '[Play the scene](scene/sky_lagoon_sample.mp4) · [Layered scene in Aseprite](scene/sky_lagoon_sample.aseprite) · [Audit and iteration log](REVIEW.json) · [Machine evidence](MACHINE_VERIFICATION.json)','',
 '![Reviewed Sky Lagoon reference](scene/sky_lagoon_sample.png)','',
 '| Sample | Distinct states | Editable master | Native review board |','|---|---:|---|---|']
 for s in samples:
  ident=s['id'];lines.append(f"| {s['title']} | {s['count']} × 512×512 | [{ident}.aseprite](objects/{ident}/{ident}.aseprite) | [All states](objects/{ident}/spritesheet.png) |")
 lines+=['','Twelve fresh swing-seat drawings keep seven shell panels, four front scrolls, one front shell/pearl and two attached gold eyelets. Its fixed approved frame is reused; foreground ropes meet each freshly drawn seat. Six fresh huckleberry drawings keep exactly two three-berry clusters; a small Aseprite mask locks the berries/junctions while new leaf silhouettes flutter. Other usable v2 keys are reused. The ten masters contain 72 distinct raster states.','',
 'The second correction pass fixes lower ropes hidden by the seat layer. Independent phases and slower garden/seesaw/cloud loops keep the environment quiet. Contact shadows ground the playground. The smoke emitter is moved to a visible cabin roof. The standalone fir remains excluded from the scene to preserve the mountain path.','',
 'All isolation, pixel cleanup, source registration, berry-junction correction, rope painting and composition use Aseprite Lua. Python only reads/analyzes image pixels. Built-in ImageGen supplied three new native sheets; no local 3060 Ti video generation or human hand drawing is claimed. The [exact prompts](PROMPT_SET.json), native sheets and prior version are retained.','',
 'Open each `.aseprite` at 100% or integer zoom for further pixel editing. The gate master contains opening pose keys; its explicit return/hold timeline is in `SAMPLES.json`. The layered scene is the complete four-second playback master.','',
 'Rebuild: `python -s -B production/refine.py`. Recheck without pixel changes: `python -s -B production/verify_v3.py`. Packet metadata: `python -s -B production/package_v3.py --hash-only`. Workstation tools: Aseprite 1.3.18.4, Python 3.13 with Pillow/NumPy/SciPy, FFmpeg 8.1.2. Paths are explicit near script tops.','',
 'The retained rejection under `review/rejected_behind_ropes/` is a deterministic reproduction of the first v3 layering defect from the same native drawings, not a claimed preserved original export. Previous v2 originals are immutable history and remain on the same branch.','',
 'Current file/scene review finds the named corrections suitable for the motion-reference purpose. Leaf/blossom micro-detail still has AI variation; the six-key flora is deliberately stepped. This is not a claim of final smooth runtime animation. Final runtime art needs selection, actual Mobile captures, gameplay contact/lifecycle evidence, device/child review and owner acceptance. No master finding is closed.','',
 '`ARCHIVE_COMPLETE` requires exact remote bytes. `GENERATION_READY` remains false (no video shot card). `DELIVERY_ACCEPTED` remains false (sprite references are not full-frame cinematic delivery).','']
 (ROOT/'README.md').write_text('\n'.join(lines),encoding='utf-8')
 observations={
 '01_fir':'Five bough tiers and fixed trunk/root retained; local silhouettes change. Standalone only: scenic path exclusion preserved.',
 '02_huckleberry':'Six berries, two clusters remain fixed after local junction cleanup; six fresh attached leaf silhouettes. Matte painted finish now closer to source than v2.',
 '03_hydrangea':'One broad bloom cluster and one bud cluster retained; stem/leaf bending visible. Small blossom detail varies; acceptable for this reference purpose, production detail lock remains open.',
 '04_bellflower':'Three open bells and one bud retained; turned petals expose interior, attached stems and fixed root. No cropped tips.',
 '05_cloud':'Billowing silhouette changes at stable center; blue/cyan source identity retained. Broad shapes readable in scene.',
 '06_smoke':'Fresh curl contours rise from one stable emission point; soft alpha intentional. Visible emitter corrected to upper cabin roof.',
 '07_swing':'Fore/aft pitch reveals cushion/underside surfaces. Seven back panels, four front scrolls, one front shell/pearl and two eyelets retained. Fixed frame; foreground ropes visibly attach to each seat.',
 '08_seesaw':'Beam/seats/handles change tilt about registered axle; fixed lower support and contact shadow ground it. Minor painted texture variance remains.',
 '09_gate':'Two leaf faces open and return inside fixed facade/aperture. Existing castle portrait and bridge remain intact. This door crop is a study approximation.',
 '10_glass':'Existing owner portrait geometry preserved with restrained light states; no identity redraw. Scene lights its original castle portrait.'}
 review={'status':'AGENT_REVIEWED_REFERENCE_CANDIDATE','reviewer':'Codex','evidence_level':'Native FILE/SHEET plus reference-context/browser playback; not runtime or owner acceptance','checked_at_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),
  'iterations':[{'revision':'v2 at b9a502e75a37bbc451f81315393d929496ad5c6e','disposition':'REVISE','defects':['07_swing states 2/5: changing chair details and coarse perspective transition','02_huckleberry states 4/5: berry clusters move between branches','Scene: missing contact shadows, synchronized phases, tiny smoke emitter']},
   {'revision':'v3 first composition','disposition':'REVISE','defects':['Seat layer hides the lower ropes before the eyelets','New bush retains two clusters but their junctions need pixel locking'],'retained_evidence':'Native generation sheets retained; rejected rope layering reproduced deterministically under review/rejected_behind_ropes'},
   {'revision':'v3 corrected composition','disposition':'KEEP_FOR_REFERENCE_REVIEW','corrections':['12 fresh swing pitch drawings with fixed decorative topology','Foreground attached ropes','6 fresh bush drawings; exact stationary berry/junction pixels','Ground contact shadows, visible smoke emitter, independent phases and quieter timing']}],
  'objects':[{'id':ident,'disposition':'KEEP_FOR_REFERENCE','observation':obs,'board':'objects/'+ident+'/spritesheet.png','board_sha256':sha(ROOT/'objects'/ident/'spritesheet.png')} for ident,obs in observations.items()],
  'scene':{'still':'scene/sky_lagoon_sample.png','still_sha256':sha(ROOT/'scene/sky_lagoon_sample.png'),'parameters':'scene/SCENE_PARAMETERS.json','panorama':'Unmodified source byte copy; no new full-scene design','review_crops':['review/screen_0.png','review/screen_1.png','review/screen_2.png'],'known_limits':['Reference composition only; no Roshan work/ride acting','AI leaf/blossom micro-detail variance and stepped flora','Door crop not an accepted runtime replacement']},
  'loop_playback_review':'PENDING_BROWSER_REVIEW','owner_acceptance':False,'runtime_integration':False,'device_acceptance':False,'child_acceptance':False,'cinematic_delivery':False,'findings_closed':[]}
 if (ROOT/'REVIEW.json').exists():
  prior=json.loads((ROOT/'REVIEW.json').read_text(encoding='utf-8'))
  if prior.get('loop_playback_review')!='PENDING_BROWSER_REVIEW':review['loop_playback_review']=prior['loop_playback_review']
 write(ROOT/'REVIEW.json',review)
def role(path):
 rel=path.relative_to(ROOT).as_posix();oldrows={r['path']:r for r in json.loads((OLD/'MANIFEST.json').read_text())['files']}
 if rel in oldrows and sha(path)==oldrows[rel]['sha256']:
  r=oldrows[rel];return r['role'],r['sources'],'Byte reuse from v2; '+r['modification'],r['license_provenance']
 sources=[]
 if rel.startswith('objects/'):
  ident=rel.split('/')[1]
  if ident not in ['02_huckleberry','07_swing'] and rel in oldrows:
   r=oldrows[rel];return r['role'],r['sources'],'Timing/phase metadata updated; original authored pixels and source identity retained. '+r['modification'],r['license_provenance']
  names=['near_native.png','far_native.png','identity_source.png'] if ident=='07_swing' else ['generated_native.png','identity_source.png'] if ident=='02_huckleberry' else []
  sources=[{'path':REL+'/objects/'+ident+'/'+name,'sha256':sha(ROOT/'objects'/ident/name)} for name in names if (ROOT/'objects'/ident/name).is_file() and path.name!=name]
  return 'Native correction drawing / Aseprite reference derivative / source evidence',sources,'Fresh generated pose drawings and recorded Aseprite pixel cleanup; inputs preserved','Project identity references and OpenAI-generated output; https://openai.com/policies/terms-of-use/'
 if rel.startswith('review/rejected_behind_ropes/'):
  names=['near_native.png','far_native.png','identity_source.png']
  sources=[{'path':REL+'/objects/07_swing/'+name,'sha256':sha(ROOT/'objects/07_swing'/name)} for name in names]
  return 'Rejected rope-layering reproduction; not delivery pixels',sources,'Same native seat drawings, foreground ropes disabled to reproduce the occlusion defect','Project reference derivative; generated pose and approved-frame source rights retained'
 if rel.startswith(('scene/','review/')):
  return 'Reference-context or rejected diagnostic; never cinematic delivery', [{'path':REL+'/context/approved_clean_panorama.png','sha256':sha(ROOT/'context/approved_clean_panorama.png')}],'Aseprite 2D reference composition or diagnostic export; source originals retained','Project reference derivative; existing source rights retained'
 return 'Project-authored audit / production tooling / operator metadata',[],'New task-specific source/evidence; no third-party code copied','Project-authored content'
def manifest():
 rows=[]
 for p in sorted(ROOT.rglob('*'),key=lambda p:p.relative_to(ROOT).as_posix()):
  if not p.is_file() or p.name in ['MANIFEST.json','REMOTE_VERIFICATION.json']: continue
  dim=list(Image.open(p).size) if p.suffix in ['.png','.jpg'] else list(struct.unpack_from('<HH',p.read_bytes(),8)) if p.suffix=='.aseprite' else [1920,640] if p.suffix=='.mp4' else None
  r,s,m,l=role(p);rows.append({'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size,'dimensions':dim,'role':r,'sources':s,'modification':m,'license_provenance':l,'runtime_asset':False,'accepted_keyframe':False})
 digest=hashlib.sha256(''.join(r['path']+'\t'+r['sha256']+'\n' for r in rows).encode()).hexdigest()
 write(ROOT/'MANIFEST.json',{'id':ROOT.name,'baseline':'1e62991ee8db27afe045ed1791d938976762e38d','branch':BRANCH,'repository':'https://github.com/Ebonyks/mermaid-roshan-reef','packet_path':REL,'status':'AGENT_REVIEWED_REFERENCE_CANDIDATE','objects':10,'raster_states':72,'ARCHIVE_COMPLETE':'PENDING_REMOTE_BYTE_VERIFICATION','GENERATION_READY':False,'DELIVERY_ACCEPTED':False,'packet_payload_sha256':digest,'payload_hash_method':'SHA256 UTF-8 case-sensitive sorted relative path + TAB + file SHA256 + LF','excluded_from_payload':['MANIFEST.json','REMOTE_VERIFICATION.json'],'files':rows})
 print('Manifest',len(rows),'files',round(sum(r['bytes'] for r in rows)/1024**2,1),'MiB',digest,flush=True)
def docs():
 licenses=PROJECT/'ASSET_LICENSES.md';s=licenses.read_text(encoding='utf-8');start='<!-- SKY_REVIEW_V3_START -->';end='<!-- SKY_REVIEW_V3_END -->'
 if start in s:s=s[:s.index(start)]+s[s.index(end)+len(end):]
 rows=[start,'','## Sky Lagoon reviewed references v3 — 2026-10-01','','| Asset | Source / provenance | License / URL | Modifications |','|---|---|---|---|']
 for p in sorted(ROOT.rglob('*')):
  if p.is_file() and p.suffix in ['.png','.jpg','.aseprite','.mp4']:
   r,src,m,l=role(p);rows.append('| `'+p.relative_to(PROJECT).as_posix()+'` | '+r+'; '+'; '.join('`'+v['path']+'`' for v in src)+' | '+l+' | '+m+' |')
 licenses.write_text(s.rstrip()+'\n\n'+'\n'.join(rows)+'\n'+end+'\n',encoding='utf-8')
 ledger=PROJECT/'design/05_DOC_LEDGER.md';s=ledger.read_text(encoding='utf-8')
 if REL+'/README.md' not in s:ledger.write_text(s.rstrip()+'\n| `'+REL+'/README.md` | 🟣 | `AGENT_REVIEWED_REFERENCE_CANDIDATE`; two correction/review passes on ten object studies and a layered Sky Lagoon sample. Preserved sources, 72 states, attached ropes and stationary berries. No runtime, owner, device, child, cinematic or finding acceptance. |\n',encoding='utf-8')
 master=PROJECT/'audit/MASTER_AUDIT_2026-08-09.md';s=master.read_text(encoding='utf-8')
 entry='Sky Lagoon review iteration (2026-10-01): [corrected ten-object reference and scene](../'+REL+'/README.md), [audit impact](../design/audit_impacts/sky-lagoon-review-v3-20261001.json). Two review/correction passes address swing topology/rope occlusion, berry drift, grounding and ambient rhythm. This is agent-reviewed reference evidence; no runtime, owner, device, child, cinematic or finding closure.\n\n'
 if REL+'/README.md' not in s:master.write_text(s.replace('## 0. Planning entry\n\n','## 0. Planning entry\n\n'+entry,1),encoding='utf-8')
 attrs=PROJECT/'.gitattributes';s=attrs.read_text(encoding='utf-8');line=REL+'/** -text whitespace=cr-at-eol'
 if line not in s:attrs.write_text(s.rstrip()+'\n'+line+'\n',encoding='utf-8')
def impact():
 p=PROJECT/'design/audit_impacts/sky-lagoon-review-v3-20261001.json';d=json.loads(p.read_text());d['files']=sorted({'.gitattributes','ASSET_LICENSES.md','audit/MASTER_AUDIT_2026-08-09.md','design/05_DOC_LEDGER.md'}|{p.relative_to(PROJECT).as_posix() for p in ROOT.rglob('*') if p.is_file()}|{REL+'/REMOTE_VERIFICATION.json'})
 prior=d.get('validation',[])
 d['validation']=[{'command':'Native board/context and loop review; two correction passes','result':'PASS','evidence':REL+'/REVIEW.json; agent reference inspection only'}, {'command':'python -s -B production/verify_v3.py','result':'PASS','evidence':REL+'/MACHINE_VERIFICATION.json; 72 exact states, fixed frame, 24 attachment endpoints and berry lock'}, {'command':'Project authority/impact/import gates','result':'PENDING','evidence':'verification/ logs and PROJECT_VERIFICATION.json'}, {'command':'Anonymous exact GitHub revision byte verification','result':'PENDING','evidence':REL+'/REMOTE_VERIFICATION.json'}]
 for n in [2,3]:
  if len(prior)>n and prior[n]['result']=='PASS':d['validation'][n]=prior[n]
 d['acceptance_gaps']='References only. Agent inspection does not grant final runtime, Mobile, device, child, owner or cinematic acceptance; no finding closed.';write(p,d)
if __name__=='__main__':
 import argparse
 parser=argparse.ArgumentParser();parser.add_argument('--hash-only',action='store_true');args=parser.parse_args()
 if not args.hash_only:describe();docs()
 manifest();impact()
