from pathlib import Path
import datetime, hashlib, html, json, re, shutil, subprocess

b = Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
f = b / 'audit/job_geode_coherent_runtime_v1_20261002'
prefix = f.relative_to(b).as_posix()
live = b / 'audit/job_artwork_refinement_live'
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
now = datetime.datetime.now(datetime.timezone.utc).isoformat()
esc = html.escape
bt = chr(96)
def write(p, data):
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')

# Review material is outside the frozen production source boundary.
snapshot = read(f / 'full_ci_v2/SOURCE_BEFORE.json')['source_files']
checks = [dict(path=x['path'], sha256=x['sha256'], match=sha(b/x['path']) == x['sha256']) for x in snapshot]
assert len(checks) == 368 and all(x['match'] for x in checks)
assert not (f / 'REVIEW_V2.json').exists()
frames, boards = [], []
for width in [1280, 1600]:
    manifest = read(f / ('BOARD_MANIFEST_V2_' + str(width) + '.json'))
    for entry in manifest['frames']:
        x = dict(entry)
        assert sha(b/x['path']) == x['sha256']
        n = x['index']
        x.update(direct_review=True, native_detail_review=n in [31,32,41,42], owner_acceptance=None, priority=True)
        x['review_method'] = 'Every cell of all26 complete ordered12-frame boards directly inspected; row-major without sampling. Frames31/32/41/42 also directly inspected at native resolution at both widths.'
        x['scores'] = dict(static_state=4.5, material=4.6, rooted_crystals=4.6, opening_geometry=4.5, room=2.8, working_contact=2.7 if n<92 else None, clap_transition=4.0 if 92<=n<112 else None, production_return=None)
        x['evaluation'] = 'Fixed center and base keep the geode planted on the painted slab; authored proportions are preserved. Aqua/lavender broad painted bands and plum contours fit the prop family. Crystals remain embedded inside two mineral-lined stone cavities; no detached reward crystal travels out. Static state and continuous opening4.5 provisional, material/rooted semantics4.6. Minor edge fringe and discrete authored reveal, especially bridge-to-half, remain inclusive refinement priorities; no5/5 or owner acceptance.'
        x['evaluation'] += (' Roshan works at the floor away from the raised object; contact2.7, room flat bands2.8 remain separate failures.' if n<92 else ' Working-to-clap jump4.0 remains abrupt; the geode stays open and its crystals stay embedded.' if n<112 else ' Empty completion callback leaves a fixture-only tail; this frame does not prove ordinary production return or a production return defect.')
        frames.append(x)
    for entry in manifest['boards']:
        x = dict(entry)
        assert sha(b/x['path']) == x['sha256']
        x.update(direct_review=True, review_method='Every12 native frames directly inspected in row-major order; no sampled omissions.')
        boards.append(x)
assert len(frames)==312 and len(boards)==26

binding = read(f/'BINDING.json')
names = ['Closed shell', 'First opening', 'Quarter reveal', 'Intermediate cavity reveal', 'Half opening', 'Three-quarter opening', 'Fully open geode']
notes = [
    'Rounded lavender shell reads as one mineral specimen; warm seam and plum contour are clear. Minor fringe remains at the source edge.',
    'Narrow central separation reveals mineral lining while the closed masses retain their identity. The opening originates in the stone.',
    'Crystals are revealed through occlusion inside the widening seam, rather than appearing outside the specimen.',
    'The selected bridge reduces the earlier abrupt width jump. Interior crystal facets are somewhat reinterpreted; conservative state continuity remains4.5.',
    'Two cavities become fully readable and remain rooted in distinct shell halves. Bridge-to-half reveal is still a discrete authored change.',
    'Calm aqua and violet clusters stay within the cream cavity rims. Width increases through opening rather than translation of the whole specimen.',
    'Both stone halves rest on the same slab and show their crystals inside through completion and celebration; no loot-style departure.'
]
states=[]
for x, name, note in zip(binding['selected_states'], names, notes):
    y=dict(x)
    y['source_path']=x['path']
    y['path']=binding['copies'][1 if x['index']==3 else 0]['path']
    assert sha(b/y['path']) == binding['copies'][1 if x['index']==3 else 0]['sha256']
    y.update(id='GEO-COHERENT-RUNTIME-STATE-'+str(x['index']), name=name, sha256=sha(b/y['path']), score=4.5, material_score=4.6, geometry_score=4.5, direct_review=True, owner_acceptance=None, evaluation=note+' Actual mounted opinion from both-width complete sequence; contact/room/transition scored separately.')
    y['representative_frames']=[next(z['path'] for z in frames if z['width']==w and z['authored_state']==x['index']) for w in [1280,1600]]
    states.append(y)

script=b/'scripts/opera_geology_surface.gd'
before=subprocess.run(['git','show',binding['baseline']+':scripts/opera_geology_surface.gd'],cwd=b,capture_output=True,check=True).stdout
after=script.read_bytes()
def methods(data):
    matches=list(re.finditer(rb'^func ([A-Za-z_][A-Za-z0-9_]*)\(',data,re.M))
    return {m.group(1).decode():data[m.start():matches[i+1].start() if i+1<len(matches) else len(data)] for i,m in enumerate(matches)}
old,new=methods(before),methods(after)
changed=sorted(k for k in old if old[k]!=new.get(k))
unchanged=[dict(method=k,sha256=hashlib.sha256(v).hexdigest()) for k,v in old.items() if v==new.get(k)]
assert changed==sorted(['_load_textures','_geode_right_rect','_draw_geode','_geode_pair_rect'])
assert len(unchanged)==59 and sorted(set(new)-set(old))==['_geode_state_index']
write(f/'MECHANIC_UNCHANGED_V2.json',dict(status='PASS59_EXISTING_METHODS_LITERAL_UNCHANGED',checked_utc=now,baseline=binding['baseline'],script_before_sha256=hashlib.sha256(before).hexdigest(),script_after_sha256=sha(script),unchanged_methods=unchanged,changed_existing_methods=changed,new_methods=['_geode_state_index'],qualification='Art loading, geode draw, fixed display geometry and matching right-half hit bounds only. Existing touch/progress/save/demo/reward/river/fossil/pan methods remain literal unchanged; ordinary input and full-suite evidence separately required. Initial60-method proof belongs to the preserved failed mount.'))

report=dict(status='ACTUAL_GEODE_OPENING4.5_PROVISIONAL_ALL312_FRAMES_REVIEWED',reviewed_utc=now,baseline=binding['baseline'],production_script=dict(path=script.relative_to(b).as_posix(),sha256=sha(script)),source_checks=checks,states=states,frames=frames,boards=boards,counts=dict(frames=312,boards=26,native_details=8,individual_mounted_states=7),scores=dict(static_states=4.5,continuous_opening=4.5,material=4.6,rooted_crystals=4.6,room=2.8,working_contact=2.7,clap_transition=4.0,production_return=None),full_ci='full_ci_v2/RECEIPT.json',owner_acceptance=None,qualification='Actual production render through ordinary four-phase intentional viewport input at both widths; no injected surface, forced phases, freeze or explicit restore interruption. Every rendered opening/celebration frame preserved. Readback slows wall-clock pacing. Empty callback tail is a fixture boundary. Reversible topic candidate only; training/story/ordinary return/device/child/owner/global acceptance and current fullCI remain separate. Earlier actual4.2, rejected actual mount4.3 and unbound pilot4.5 remain preserved. No finding closure, integration or release. Inclusive4.5 priorities remain.')
write(f/'REVIEW_V2.json',report)
write(f/'MOUNTED_STATES_V2.json',dict(status=report['status'],states=states,production_script=report['production_script'],review='REVIEW_V2.json'))
def url(path): return '../../'+path
whole=''.join('<figure><a href="'+url(x['path'])+'"><img src="'+url(x['path'])+'" alt="Complete runtime geode atlas"></a><figcaption>Exact complete runtime copy · '+x['sha256']+'<p>'+esc(x['modification'])+'</p></figcaption></figure>' for x in binding['copies'])
state_html=''
for x in states:
    rx,ry,rw,rh=x['region']; sw,sh=2048,1024
    state_html+='<article class="state" id="'+x['id']+'"><h3>'+esc(x['name'])+' ·4.5/5</h3><figure class="region" style="aspect-ratio:'+str(rw)+'/'+str(rh)+'"><img src="'+url(x['path'])+'" alt="'+esc(x['name'])+'" style="position:absolute;max-width:none;width:'+str(sw/rw*100)+'%;height:'+str(sh/rh*100)+'%;left:'+str(-rx/rw*100)+'%;top:'+str(-ry/rh*100)+'%"></figure><p>'+esc(x['evaluation'])+'</p><small>'+x['id']+'; material4.6; geometry4.5; exact region '+esc(json.dumps(x['region']))+'</small></article>'
board_html=''.join('<figure class="board"><a href="'+url(x['path'])+'"><img src="'+url(x['path'])+'" alt="'+str(x['width'])+' frames '+str(x['first_frame'])+' through '+str(x['last_frame'])+'"></a><figcaption>'+str(x['width'])+' · frames'+str(x['first_frame'])+'–'+str(x['last_frame'])+' · all12 directly inspected</figcaption></figure>' for x in boards)
detail_html=''.join('<figure class="detail"><a href="'+url(x['path'])+'"><img src="'+url(x['path'])+'" alt="Native threshold '+str(x['width'])+' frame'+str(x['index'])+'"></a><figcaption>'+str(x['width'])+' frame'+str(x['index'])+' · state'+str(x['authored_state'])+' · native directly inspected</figcaption></figure>' for x in frames if x['native_detail_review'])
frame_html=''.join('<article class="frame" id="frame-'+str(x['width'])+'-'+str(x['index'])+'"><h3><a href="'+url(x['path'])+'">'+str(x['width'])+' frame'+str(x['index'])+'</a></h3><p>'+esc(x['evaluation'])+'</p><small>State'+str(x['authored_state'])+'; pull'+str(x['pull'])+'; '+x['sha256']+'</small></article>' for x in frames)
header='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Actual geode opening review2</title><style>body{font:17px/1.5 system-ui;background:#eef4fa;color:#25304a;margin:0}main{max-width:1460px;margin:auto;padding:24px}section{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,600px),1fr));gap:18px}.states,.frames{grid-template-columns:repeat(auto-fit,minmax(280px,1fr))}figure,article{background:white;padding:16px;border-radius:14px;margin:0;min-width:0}img{width:100%;height:auto;display:block}.region{position:relative;overflow:hidden;padding:0;background:repeating-conic-gradient(#dce5ed 0% 25%,#f8fbff 0% 50%) 50%/24px 24px}small{font-size:12px;overflow-wrap:anywhere;display:block}a{color:#385797}</style><main>'
content='<a href="../job_artwork_refinement_live/all_items.html">All known job items</a><h1>The geode opens to reveal its crystals</h1><p>Actual production opening4.5/5 provisional; material and embedded-crystal semantics4.6. Seven individually reviewed authored states preserve a fixed center,350px height and515px base. All312 opening/celebration frames at1280 and1600 are directly reviewed on26 complete boards, plus8 native threshold details.</p><p>Minor edge fringe and discrete authored reveal remain at the inclusive refinement threshold. The surrounding flat room2.8, Roshan’s remote working contact2.7 and abrupt clap transition4.0 remain weak. The empty-callback fixture tail does not prove production return. Training/story/ordinary return/device/child/owner/final all-job acceptance remains open; current full-suite status has its own receipt.</p><p><a href="REVIEW_V2.json">Every written evaluation and exact source boundary</a> · <a href="MECHANIC_UNCHANGED_V2.json">59 unchanged existing methods</a> · <a href="full_ci_v2/RECEIPT.json">Current full machine suite</a> · <a href="attempt_01/index.html">Rejected mounting attempt4.3</a> · <a href="../job_geode_coherent_pilot_v1_20261002/index.html">Earlier unbound pilot</a> · <a href="../../assets_src/imagegen/geologist_geode_coherent_states_v1_20261002/index.html">Every generated source trial</a> · <a href="../job_geology_river_runtime_v1_20261002/timed.html">Earlier actual opening4.2</a></p><h2>Each mounted object state</h2><section class="states">'+state_html+'</section><h2>Exact complete runtime source files</h2><section>'+whole+'</section><h2>Every ordered frame</h2><section>'+board_html+'</section><h2>Native threshold details</h2><section>'+detail_html+'</section><h2>Individual frame evaluations</h2><section class="frames">'+frame_html+'</section></main></html>'
(f/'index.html').write_text(header+content,encoding='utf-8',newline='\n')

register=read(live/'ALL_ITEMS.json'); assert register['counts']['registered_items']==1712
shutil.copyfile(live/'ALL_ITEMS.json',live/'ALL_ITEMS_V27.json')
(live/'all_items_V27.html').write_text((live/'all_items.html').read_text(encoding='utf-8').replace('ALL_ITEMS.json','ALL_ITEMS_V27.json'),encoding='utf-8',newline='\n')
entries=[dict(id='GEO-COHERENT-RUNTIME-ATLAS-'+str(i),path=x['path'],region=None,score=4.5,evaluation='Exact whole-canvas runtime copy of individually reviewed source; selected actual states/opening4.5 provisional, material4.6. Unselected first bridge remains excluded; no owner/whole-job acceptance.',kind='runtime source',dimensions=x['dimensions']) for i,x in enumerate(binding['copies'])]
entries += [dict(id=x['id'],path=x['path'],region=x['region'],score=x['score'],evaluation=x['evaluation'],kind='runtime object region',dimensions=[2048,1024]) for x in states]
for x in entries:
    register['items'].append(dict(id=x['id'],aliases=[x['id']],kind=x['kind'],path=x['path'],region=x['region'],earlier_sha256=sha(b/x['path']),historical_source_score=x['score'],evaluation=x['evaluation'],refinement='Inclusive4.5 priority: refine minor contour/reveal while preserving rooted crystal semantics, fixed support and approved painting. Room/contact/clap remain separate.',families=['Geologist','Actual coherent geode opening'],original_reports=[prefix+'/REVIEW_V2.json',prefix+'/index.html'],source_qualification='Current production art; every312 actual frames reviewed at both widths. Owner/training/return/device/child/global acceptance remains open.',preview_path=x['path'],native_reference_observations=[],current_checkout_sha256=sha(b/x['path']),current_byte_status='EXACT_REVIEWED_SOURCE_BYTES',current_source_score=x['score'],source_dimensions=x['dimensions'],priority=True,protected_original=False,current_mounted_score=4.5,current_complete_action_score=4.5,image_path=x['path'],image_scope='Exact native runtime region shown by CSS; original pixels preserved' if x['region'] else 'Native whole runtime source',current_binding='scripts/opera_geology_surface.gd',owner_acceptance=None))
register['created_utc']=now
register['scope']='V28 union of known job discovery sources,328 pose cells,45 runtime object regions and104 source-object regions; current coherent geode adds two runtime files/seven individually mounted states. Not exhaustive actual-use/all-job/owner acceptance.'
register['counts'].update(registered_items=len(register['items']),unique_source_files=len({x['path'] for x in register['items']}),individual_runtime_prop_regions=45,inclusive_current_source_priorities=sum(x['priority'] for x in register['items']),unreviewed_current_source=sum(x['current_source_score'] is None for x in register['items']))
# Preserve the register's existing field spelling for runtime regions.
for key in list(register['counts']):
    if 'region' in key and 'source' not in key and key!='individual_runtime_prop_regions': register['counts'][key]=45
register['counts']['exact_earlier_bytes']+=9
assert register['counts']['registered_items']==1721 and register['counts']['unique_source_files']==1244
write(live/'ALL_ITEMS.json',register)
(live/'all_items.html').write_text((live/'all_items.html').read_text(encoding='utf-8').replace('38 runtime','45 runtime'),encoding='utf-8',newline='\n')

summary='Actual coherent geode correction (2026-10-02): [every312 corrected actual production frames on26 ordered boards plus8 native details]('+prefix.removeprefix('audit/')+'/index.html) directly reviewed at1280/1600. Seven individual mounted states/continuous opening4.5 provisional; material/rooted crystals4.6. Fixed center/base removes the observed50px whole-object drift; rejected actual attempt4.3 and interrupted fullCI1 are preserved.59 existing methods literal unchanged; only art/drawing/display/right-half geometry change. Room2.8/contact2.7/clap transition4.0 remain priorities; fixture tail cannot establish actual return. Fresh unmodified officialGodot4.7.2 fullCI2 is pending against368 frozen literal sources, with receipt separate; no inherited pass. RegisterV28 has1721 entries/1244 source files/328 pose cells/45 runtime regions/104 source regions;675 inclusive priorities/388 unassigned remain. Training/story/return/device/child/owner/final all-job acceptance and finding lifecycles remain open; no integration/release.'
p=b/'audit/MASTER_AUDIT_2026-08-09.md';s=p.read_text(encoding='utf-8');s=s.replace('\n\n','\n\n'+summary+'\n\n',1);p.write_text(s,encoding='utf-8',newline='\n')
p=b/'audit/findings/ACTIVE_FINDINGS_2026-08-13.md';s=p.read_text(encoding='utf-8');point=s.index('\n## MA-COMBAT-001');s=s[:point]+'\n'+summary.replace('('+prefix.removeprefix('audit/')+'/', '(../'+prefix.removeprefix('audit/')+'/')+' MA-PLAY-004 remains IN_PROGRESS; MA-VIS-006 is not closed.\n'+s[point:];p.write_text(s,encoding='utf-8',newline='\n')
p=b/'design/05_DOC_LEDGER.md';s=p.read_text(encoding='utf-8');s+='\n| '+bt+prefix+'/index.html'+bt+' | 🟣 | '+bt+'CANDIDATE'+bt+'; actual coherent geode opening2: every312 frames/26 complete boards/8 native details; seven mounted states/opening4.5 provisional, embedded material4.6; rejected mounting1/partialCI retained, fresh368-source fullCI2 receipt separate. Room/contact/transition/training/return/device/child/owner/all-job open. |\n';s='\n'.join('| '+bt+'audit/job_artwork_refinement_live/all_items.html'+bt+' | 🟣 | '+bt+'CANDIDATE'+bt+'; V28 known register1721 items/1244 source files/328 pose cells/45 runtime regions/104 source regions.675 inclusive priorities/388 unassigned; source/actual state/action/owner acceptance remain separate. |' if row.startswith('|') and 'audit/job_artwork_refinement_live/all_items.html' in row else row for row in s.split('\n'));p.write_text(s,encoding='utf-8',newline='\n')
p=b/'ASSET_LICENSES.md';s=p.read_text(encoding='utf-8')+'\n### Corrected actual coherent geode opening2 review evidence (2026-10-02)\n\n'
for x in frames+boards:
    if x['path'] not in s: s+='| '+bt+x['path']+bt+' | Godot4.7.2 Mobile capture of licensed project art | Project review evidence | '+bt+prefix+'/REVIEW_V2.json'+bt+' | '+('Uniform whole-scene12-frame review board; no production pixels' if 'first_frame' in x else 'Exact native losslessWebP capture')+'; all frames directly reviewed; SHA256 '+x['sha256']+' |\n'
p.write_text(s,encoding='utf-8',newline='\n')
shutil.copyfile(__file__,f/'review_tools'/Path(__file__).name)
shutil.copyfile(__file__,live/'review_tools/build_current_job_item_register_v28.py')
ip=b/'design/audit_impacts/job-geode-coherent-runtime-20261002.json';impact=read(ip)
impact['scope']+=' Actual correction2 reviewed every312 frames/26 boards/8 details and each7 state4.5 provisional; preserve all prior opinions. Extend known item registerV28 by two complete runtime sources/seven regions.'
impact['validation'].append(dict(command='Direct complete corrected actual production frame/state review and literal method comparison',result='PASS',evidence=prefix+'/REVIEW_V2.json and MECHANIC_UNCHANGED_V2.json; source368 unchanged. Provisional object4.5, contact/room/clap fail separately; fresh fullCI2 remains pending.'))
impact['acceptance_gaps']='Full current official suite receipt remains pending. Room2.8/contact2.7/clap4.0, inclusive4.5 fringe/reveal; training/story/actual return/device/child/owner and final comprehensive all-job report. No lifecycle closure/integration/release.'
impact['files']=sorted(set(impact['files'])|{x.relative_to(b).as_posix() for folder in [f,live] for x in folder.rglob('*') if x.is_file()}|{'audit/MASTER_AUDIT_2026-08-09.md','audit/findings/ACTIVE_FINDINGS_2026-08-13.md','design/05_DOC_LEDGER.md','ASSET_LICENSES.md'})
write(ip,impact)
allow=b/'tmp/v2_preview_allowed.json';write(allow,sorted(set(read(allow))|{x.relative_to(b).as_posix() for folder in [f,live] for x in folder.rglob('*') if x.is_file()}|{x['path'] for x in binding['copies']}))
print(json.dumps(dict(review=report['status'],states=len(states),counts=register['counts'],unchanged_methods=len(unchanged)),ensure_ascii=False))
