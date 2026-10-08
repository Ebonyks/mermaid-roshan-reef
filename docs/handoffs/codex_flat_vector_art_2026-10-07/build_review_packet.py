from pathlib import Path
import collections, hashlib, json, re, shutil, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageOps
P=Path(__file__).resolve().parent;R=P.parents[2];BASE='92c9fe70319ef46bfaa8f61348a6f51512141ec3'
def load(n):return json.loads((P/n).read_text(encoding='utf-8-sig'))
def save(n,v):(P/n).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n',encoding='utf8', newline='\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
inv=load('source_inventory.json');pieces=load('per_piece.json')['pieces'];scopes=load('source_scopes.json')['scopes'];assets=[a for s in inv['image_shards'] for a in load(s['path'])['images']]
# Literal route census; reachability and actual screen/state counts remain separate.
routes=[]
cat='scripts/living_world_catalog.gd';text=(R/cat).read_text(encoding='utf8');lines=text.splitlines()
for i,l in enumerate(lines,1):
    m=re.match(r'\s*\["([\w.]+)",\s*"([^"]+)",\s*(.*)',l)
    if m:
        source=re.match(r'"([^"]+)"',m[3]);src=source[1] if source else 'scripts/arena/castle_rooms_25d.gd (catalogue source variable)'
        routes.append({'id':m[1],'name':m[2],'source':{'path':cat,'line':i,'caller_expression':src},'route_evidence':'STATIC_REGISTERED_STAGE; not fresh live reachability','state_checks':['ready/idle','active contact','changed state','payoff/reward','settle','leave/re-entry','pause/save/load','dirty/clean where applicable'],'capture_status':'COVERAGE_GAP','current_mobile_captures':[],'device_child_owner':None})
# Exact live career table, preserving sparse slots and current names.
house=(R/'scripts/opera_house.gd').read_text(encoding='utf8');live=[]
for m in re.finditer(r'"save_bit":\s*(\d+),\s*"name":\s*"([^"]+)",\s*"career":\s*"([^"]+)"[\s\S]*?"costume":\s*"([^"]+)"',house):
    live.append({'save_bit':int(m[1]),'name':m[2],'career':m[3],'costume':m[4],'source_line':house[:m.start()].count('\n')+1})
phase_source=(R/'scripts/opera_career_world_2d.gd').read_text(encoding='utf8').split('const PHASES := {',1)[1].split('\n}',1)[0]
phase_map={};career=None
for l in phase_source.splitlines():
    m=re.match(r'\s*"([a-z]+)": \[',l)
    if m:career=m[1];phase_map[career]=[]
    phase=re.search(r'"name":\s*"([^"]+)".*?"mode":\s*"([^"]+)"',l)
    if phase and career:phase_map[career].append({'name':phase[1],'mode':phase[2]})
room_text=(R/'scripts/castle_career_routes.gd').read_text(encoding='utf8').split('const ROOM_ACT_INDICES := {',1)[1].split('\n}',1)[0]
rooms={int(n):room for room,nums in re.findall(r'"([a-z_]+)":\s*\[([\d, ]+)\]',room_text) for n in nums.replace(' ','').split(',') if n}
for career in live:
    career['room']=rooms.get(career['save_bit']);career['phases']=phase_map[career['costume']];career['route']='Castle room '+str(career['room'])+' picture route; temporary Opera painted left elevator -> playtest card also launches same engine without durable rewards'
    for row in routes:
        if row['id']=='opera.act.%02d'%career['save_bit']:row['current_live_name']=career['name'];row['route']=career['route'];row['phases']=career['phases']
ui=[('start','Start/options/reset','scripts/start_menu.gd'),('intro','Intro/book pages','scripts/intro_overlay.gd'),('pause','Pause/options/back','scripts/pause_menu.gd'),('save_hud','HUD/objectives/save/transition','scripts/main.gd'),('touch','Fallback touch controls','scripts/touch_ui.gd'),('craft','Craft studio','scripts/craft_studio.gd'),('wardrobe','Wardrobe','scripts/wardrobe_ui.gd'),('collection','Sticker/collection book','scripts/collection_system.gd'),('logo','Castle logo studio','scripts/castle_logo_studio.gd'),('attack','Attack customizer','scripts/attack_customizer.gd'),('fashion','Fashion Designer and head/body/tail dress-up','scripts/fashion_wardrobe.gd'),('job_playtest','Temporary Opera elevator job menu','scripts/opera_job_playtest_menu.gd')]
for id,name,p in ui:routes.append({'id':'ui.'+id,'name':name,'source':{'path':p,'line':1},'route_evidence':'SOURCE_BOUND_OVERLAY','state_checks':['entry','normal','selected/pressed/focus','changed/saved','back/close','reload/focus-loss'],'capture_status':'COVERAGE_GAP','current_mobile_captures':[]})
games=json.loads((R/'design/reference/games.json').read_text(encoding='utf8'))['games']
for g in games:
    routes.append({'id':'game.'+g['id'],'name':g['name'],'source':{'path':'design/reference/games.json','catalogue_id':g['id'],'sources':g.get('sources',[]),'host':g.get('host',[])},'route':g.get('route'),'declared_state':g.get('state'),'route_evidence':'SOURCE_CATALOGUE; original assessment may be historical','state_checks':['ready','active action/contact','changed object','payoff','settle','repeat','pause/save/load'],'capture_status':'COVERAGE_GAP','current_mobile_captures':[]})
scenes=subprocess.check_output(['git','ls-tree','-r','--name-only',BASE,'scenes'],cwd=R).decode().splitlines()
for p in scenes:
    if p.endswith('.tscn'):routes.append({'id':'standalone.'+Path(p).stem,'name':p,'source':{'path':p,'line':1},'route_evidence':'MAIN_ENTRY' if p=='scenes/main.tscn' else 'STANDALONE_SCENE; normal reachability not established','state_checks':['explicit standalone route','ready','action','completion','close/reload'],'capture_status':'COVERAGE_GAP','current_mobile_captures':[]})
save('scene_coverage.json',{'schema':'reef.flat_vector_coverage/1','baseline':BASE,'live_opera_careers':live,'live_opera_count':len(live),'current_phase_count':sum(len(x['phases']) for x in live),'retired_opera_slots':[4,9,14],'stage_registry_rows':sum(not r['id'].startswith(('ui.','game.','standalone.')) for r in routes),'entries':routes,'coverage_note':'Entries overlap deliberately (stage, game, UI, standalone). Route-entry count is not a distinct-screen or state count. Current Mobile/device/child/owner coverage is absent; historical contact sheets never reduce these gaps. Dynamic callbacks, saved variants, proc meshes and shaders remain to enumerate at runtime.'})
# Functional infrastructure is retained explicitly; a visible decorative shape is never exempt by API.
functional=[]
for scope in scopes:
    path,fn=scope['path'],scope['scope'].split('.')[-1]
    if path=='scripts/arena/castle_rooms_25d.gd' and fn in {'_new_letterbox_band','_build_stage'}:
        functional.append({'scope_id':scope['id'],'path':path,'line':scope['start_line'],'disposition':'EXEMPT_FUNCTIONAL_PART_ONLY','role':'Transition input cover and narrow letterbox bands','limit':'Only the transition/band geometry; named art inside the same builder is not exempt. Bounds must be verified; hidden full-screen fill remains overdraw retirement work.'})
    elif fn in {'_build_fade_cover'}:
        functional.append({'scope_id':scope['id'],'path':path,'line':scope['start_line'],'disposition':'EXEMPT_FUNCTIONAL_PART_ONLY','role':'Transition fade/input isolation','limit':'Plain fade covering during transition only; no implied art or full-screen hidden-layer exemption.'})
save('functional_dispositions.json',{'schema':'reef.flat_vector_functional/1','baseline':BASE,'dispositions':functional,'excluded_infrastructure':['Invisible collision/hit regions','Selection/mask geometry used without visible art','Ordinary engine font rasterization and text layout'],'explicit_review_required':['Visible UI frames/buttons/ornaments','Progress icons/glyphs and effects','Shader-rendered visible water/dirt/material','Child-authored saved logo/drawing marks; preserve content while reviewing presentation'],'note':'EXEMPT_FUNCTIONAL_PART_ONLY never approves every primitive in its source scope. No removal/reset of child content is commissioned.'})
# Reference previews use already public baseline sources; originals remain untouched.
(P/'review').mkdir(exist_ok=True);(P/'.gdignore').write_text('',encoding='utf8', newline='\n')
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',16);titlefont=ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',23)
groups={
'context_castle':[
('audit/visual_polish_2026-09-26/shots/free_royal_bedroom.png','Royal Bedroom: flat shell / painted furniture'),
('audit/visual_polish_2026-09-26/shots/free_movie_lounge.png','Movie Lounge: ceiling/window/floor'),
('audit/visual_polish_2026-09-26/shots/free_dining_room.png','Dining Room: architecture and rug'),
('audit/visual_polish_2026-09-26/shots/d1_bath_bubble_bath.png','Day One bathroom: grime/cue context'),
('audit/visual_polish_2026-09-26/shots/d1_playroom_playroom.png','Day One playroom: dirt/rescue context'),
('audit/visual_polish_2026-09-26/shots/d1_pool_mermaid_pool.png','Pool: HISTORICAL before later GS repairs')],
'context_geology_teacher':[
('audit/minigame_art_quality_2026-09-05/evidence/current-opera/run02/captures/geologist_river_intro.png','Geology river: HISTORICAL configured state'),
('audit/minigame_art_quality_2026-09-05/evidence/current-opera/run02/captures/geologist_fossil_partial.png','Fossil: dirt cells / fragments'),
('audit/minigame_art_quality_2026-09-05/evidence/current-opera/run02/captures/geologist_pan_intro.png','Pan: material / wash surface'),
('audit/minigame_art_quality_2026-09-05/evidence/current-opera/run02/captures/geologist_geode_partial.png','Geode: opening / seam'),
('audit/minigame_art_quality_2026-09-05/evidence/current-opera/run02/captures/teacher_pattern_intro.png','Teacher: preserve exact pattern shapes'),
('audit/minigame_art_quality_2026-09-05/evidence/current-opera/run02/captures/teacher_count_intro.png','Teacher: preserve counts and choices')],
'context_activities':[
('audit/chef_overdraw_20261003/active_1280/phase_0_work.png','Chef: authored props and added cues'),
('audit/chef_overdraw_20261003/active_1280/phase_3_work.png','Chef: piping contact / overlay context'),
('audit/minigame_art_quality_2026-09-05/evidence/garden-realtime-9df/garden_can_visible_static.png','Garden: watering tool context'),
('audit/minigame_art_quality_2026-09-05/evidence/garden-realtime-9df/garden_sprout_all.png','Garden: common sprout family'),
('audit/minigame_art_quality_2026-09-05/evidence/picture-current/034_trampoline_ready.png','Trampoline: procedural surface'),
('audit/minigame_art_quality_2026-09-05/evidence/carrot-reuse/run07/snowman_chase_active.png','Snowman: keep painted carrot; scene gap')],
'source_reuse_and_gaps':[
('assets/opera/worlds/widgets/widget_track_farmer_mover.png','Painted pig: reuse candidate'),
('assets/opera/worlds/widgets/widget_target_farmer_piece_0.png','Painted carrot: reuse candidate'),
('assets/opera/worlds/widgets/widget_crank_chef_mover.png','Painted whisk: reuse candidate'),
('assets/mg/star.png','Painted star: preserve / context review'),
('assets/mg/k_sprout.png','Sprout: flat-look raster candidate'),
('assets/mg/flower.png','Flower: flat-look raster candidate'),
('assets/mg/k_bush2.png','Bush: cel-look raster candidate'),
('assets/mg/wateringcan.png','Can: material fit review; alpha retained')]
}
def wrapped_caption(draw, text, width):
    lines=[];current=''
    for word in text.split():
        candidate=(current+' '+word).strip()
        if current and draw.textlength(candidate,font=font)>width:
            lines.append(current);current=word
        else:current=candidate
    if current:lines.append(current)
    if len(lines)>3:raise ValueError('caption needs more than its reserved 3 lines: '+text)
    return '\n'.join(lines)

index=[]
for group,items in groups.items():
    sheet=Image.new('RGB',(1024,1024),'#eaf2f1');d=ImageDraw.Draw(sheet)
    d.text((20,15),group.replace('_',' ').title(),fill='#34284f',font=titlefont)
    sourceonly=group.startswith('source_');d.text((20,49),'SOURCE-ONLY COMPOSITE' if sourceonly else 'HISTORICAL-CAPTURE COMPOSITE - NOT CURRENT LIVE EVIDENCE',fill='#893743',font=font)
    cols=4 if sourceonly else 2;cellw=1024//cols;cellh=420 if sourceonly else 300
    for i,(src,label) in enumerate(items):
        f=R/src
        if not f.is_file():raise FileNotFoundError(src)
        with Image.open(f) as im:
            native=list(im.size);thumb=ImageOps.contain(im.convert('RGBA'),(cellw-24,cellh-50),Image.Resampling.LANCZOS)
            x=(i%cols)*cellw+(cellw-thumb.width)//2;y=90+(i//cols)*cellh
            sheet.paste(thumb,(x,y),thumb);d.multiline_text(((i%cols)*cellw+12,y+cellh-44),wrapped_caption(d,label,cellw-24),fill='#34284f',font=font,spacing=2)
        index.append({'source_path':src,'source_sha256':sha(f),'source_dimensions':native,'role':'source_art_preview' if sourceonly else 'historical_capture_preview','modifications':'Contain resize on labelled 1024x1024 contact sheet; no source changes','evidence_level':'SOURCE_ONLY' if sourceonly else 'HISTORICAL_CAPTURE','capture_revision':'See original capture manifest; not substituted with current baseline','packet_path':'review/'+group+'.png','panel':i+1,'license_provenance':'Existing first-party project art/capture; original ASSET_LICENSES.md and bound source record control. No protected book/family voice originals copied.'})
    out=P/'review'/(group+'.png');sheet.save(out)
    for entry in index:
        if entry['packet_path']=='review/'+group+'.png':entry['sha256']=sha(out);entry['dimensions']=[1024,1024]
for src in sorted(R.glob('assets/**/*.svg')):
    out=P/'review'/src.name;shutil.copyfile(src,out)
    index.append({'source_path':src.relative_to(R).as_posix(),'source_sha256':sha(src),'source_dimensions':[256,256],'role':'literal_svg_source_review','modifications':'Unmodified byte-identical audit copy','evidence_level':'SOURCE_ONLY','packet_path':'review/'+src.name,'sha256':sha(out),'dimensions':[256,256],'license_provenance':'Existing project-authored SVG, original ASSET_LICENSES.md governs; duplicate outside runtime for review only'})
save('contact_index.json',{'schema':'reef.flat_vector_contact_index/1','baseline':BASE,'images':index,'claim':'These are resized source/capture composites and unchanged source SVG previews, never current live captures or accepted generation pixels.'})
lanes=['NEEDS_CONTEXT_REVIEW','IDENTIFIED','REUSE_READY','DRAWING_REQUIRED','SAMPLE_READY','VISUAL_REVIEW_PENDING','APPROVED_FOR_INTEGRATION','INTEGRATED','RUNTIME_VERIFIED','DEVICE_CHILD_OWNER_PENDING','ACCEPTED_REMOVED','BLOCKED','VERIFIED_NOT_FLAT_VECTOR_ART','EXEMPT_FUNCTIONAL','INACTIVE_ARCHIVE']
save('tally.json',{'schema':'reef.flat_vector_tally/1','baseline':BASE,'revision':'FV-AUDIT-20261007-R1','status_lanes':lanes,'mission_status':'ACTIVE; zero-vector removal NOT achieved','phase':'PHASE_1_SOURCE_CONTEXT_AUDIT; delivery and exact-head CI states are recorded in separate receipts','named_piece_records':len(pieces),'named_family_count':len({p['family'] for p in pieces}),'named_status_counts':dict(collections.Counter(p['status'] for p in pieces)),'all_game_individual_piece_total':None,'total_unknown_reason':'369 source scopes, repeated/phase variants, dynamic resources, raster lookalikes and shader/mesh state visibility need current context enumeration. Named records are a lower bound, not an exhaustive accepted visual-piece total.','source_script_count':len(inv['scripts']),'source_function_scopes':len(scopes),'primitive_candidate_call_sites':len(load('primitive_sites.json')['sites']),'commissioning_scan_call_sites':load('vector_source_scan.json')['candidate_primitive_call_sites'],'scan_count_difference':'Broader collector includes generated textures, primitive meshes, flat styles, scene-only scripts and draw_style_box; narrow root scan uses its documented primitive set. Neither count is an art total.','source_image_count':len(assets),'runtime_svg_assets':sum(x['path'].startswith('assets/') and x['path'].endswith('.svg') for x in assets),'glyph_candidate_rows':len(load('glyph_inventory.json')['sites']),'route_entries':len(routes),'unreviewed_current_route_entries':len(routes),'current_distinct_screen_total':None,'source_or_historical_review_only':True,'replaced':0,'integrated':0,'runtime_verified':0,'accepted_removed':0,'named_resolved_without_replacement':0,'remaining_named_design_records':len(pieces),'remaining_named_definition':'Unresolved/removal-needed candidates; proven non-flat artwork, non-art functional geometry and inactive archive dispositions resolve separately without replacement claims. A quality score never exempts flat-vector ART.','remaining_source_scopes_to_disposition':len(scopes),'regression_count':None,'regression_evidence':'Initial audit baseline; no replacement or runtime change. A zero regression claim awaits repeat census at unchanged/updated candidate.','zero_acceptance_criteria':['No reachable flat-vector art in gameplay or UI across every current route/state/save variant','All runtime-loaded SVG/vector resources and raster vector-lookalikes individually dispositioned','Every procedural draw callback, scene primitive, generated texture, mesh stand-in, shader artwork and decorative glyph has accepted disposition','Old fallback branches, manifests/export references and obsolete builders cannot recreate flat-vector art','Every named item accepted in current Mobile 1280x720 plus phone ratio with HUD, action/contact/settle/seam and source hashes','Device performance/readability, child comprehension and explicit owner style acceptance recorded','Functional collision/masks/text rendering and protected originals preserved; child content not erased','All source scopes resolved; unknown actual totals/coverage gaps reduced to zero before completion']})
print('COVERAGE',len(routes),'entries',len(live),'careers',sum(len(x['phases']) for x in live),'phases; CONTACT',len(index),'source panels')
