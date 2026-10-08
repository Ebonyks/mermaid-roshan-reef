from pathlib import Path
import collections, hashlib, json, re
P=Path(__file__).resolve().parent
R=P.parents[2]
BASE='92c9fe70319ef46bfaa8f61348a6f51512141ec3'
def save(name,data): (P/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf8', newline='\n')
def digest(p):
    data=p.read_bytes()
    if p.suffix in {'.gd','.py','.md','.tscn'}: data=data.replace(b'\r\n',b'\n')
    return hashlib.sha256(data).hexdigest()
def fid(key): return 'FV-'+hashlib.sha256(key.encode()).hexdigest()[:12].upper()
def function_span(path,fn):
    lines=(R/path).read_text(encoding='utf-8-sig').splitlines()
    if fn=='FILE_SCOPE': return 1,len(lines),lines
    matches=[i for i,l in enumerate(lines) if re.match(r'\s*(?:static )?func '+re.escape(fn)+r'\(',l)]
    if not matches: raise ValueError(path+': missing '+fn)
    start=matches[0]; end=next((i for i in range(start+1,len(lines)) if re.match(r'\s*(?:static )?func \w+\(',lines[i])),len(lines))
    return start+1,end,lines[start:end]

# One entry is one named visual design/state family, not one draw call or instance.
# Independent visual roles are split; repeated instances remain recorded below.
SEEDS=[]
def add(family,path,fn,names,priority='P2',status='NEEDS_CONTEXT_REVIEW',note=''):
    for name in names.split('|'):
        SEEDS.append({'family':family,'path':path,'function':fn,'name':name,'priority':priority,'status':status,'note':note})
add('day_one','scripts/arena/day_one_castle_grime.gd','_draw_exterior_grime','Exterior edge dirt bands|Exterior hanging grime drips','P1','IDENTIFIED','Dirty-state visibility guard must be captured. Pool repair is separately scoped; do not reintroduce its retired grime.')
add('day_one','scripts/arena/day_one_castle_grime.gd','_draw_room_dressing','Dirty room tint wash|Dirty room edge grime|Dirty room floor cracks','P1','IDENTIFIED','MA-VIS-008; preserve room-specific authored dirt and Roshan identity. Record dirty/active-cleaning/clean states separately.')
add('shared_ambience','scripts/living_world_canvas.gd','_draw_motif','Bubble motif|Sea-frond motif|Leaf motif|Flower motif|Fish motif|Butterfly motif|Cloud motif|Ripple/wave motif|Snow motif|Lantern motif|Flame motif|Music-note motif|Heart motif|Shell motif|Crown motif|Moon motif|Crystal motif','P1','IDENTIFIED','Scene catalogue owns stage, palette, quiet and idle-only routing. Needed accents use purpose-fitting authored art; remove competing decoration rather than adding a sticker quota.')
add('shared_ambience','scripts/living_world_canvas.gd','_draw_sparkle','Four-arm sparkle motif','P2','IDENTIFIED')
add('opera_shared','scripts/opera_world_backdrop_2d.gd','_draw_stage_frame','Proscenium side columns|Curtain header and scallops|Stage triangular framing|Stage footlight pair','P1','NEEDS_CONTEXT_REVIEW','Can be guarded behind accepted tiles. Trace current route before replacing.')
add('opera_shared','scripts/opera_world_backdrop_2d.gd','_draw_spotlights','Left stage spotlight cone|Right stage spotlight cone','P1','IDENTIFIED','Source adds geometric spotlights to some accepted painted backdrops; own fallback and overlay dispositions separately.')
for fn,name in [('chef','Kitchen cabinet and counter fallback'),('detective','Library shelving and clue fallback'),('ballerina','Dance-floor and ribbon fallback'),('candy','Candy-factory table and sweets fallback'),('doctor','Doctor care-station fallback'),('farmer','Farm beds and herd fallback'),('boxer','Ring and belt fallback'),('magician','Magic stage-prop fallback'),('painter','Easel and paints fallback'),('astronaut','Rocket repair-room fallback'),('racer','Race-track fallback'),('nursery','Cradle-room fallback'),('popstar','Pop-stage fallback'),('geologist','Geology cave fallback')]:
    add('opera_'+fn,'scripts/opera_world_backdrop_2d.gd','_draw_'+fn,name,'P1' if fn=='geologist' else 'P2',note='Fallback role family; child-visible parts and their counts are unresolved. Retirement needs accepted replacement availability, not a repaint of accepted background.')
add('opera_farmer','scripts/opera_world_backdrop_2d.gd','_draw_sky_lagoon_farmer','Farmer soil mound and rim','P1','IDENTIFIED')
add('opera_shared','scripts/opera_world_hotspot_2d.gd','_draw_halo','Hotspot outer glow|Hotspot orbit ring|Hotspot inner moving arc|Hotspot opening ring','P1','IDENTIFIED')
add('opera_shared','scripts/opera_world_hotspot_2d.gd','_draw_sparkles','Hotspot cross sparkle','P1','IDENTIFIED')
add('opera_shared','scripts/opera_world_hotspot_2d.gd','_draw_object','Hotspot ground shadow|Missing-object sphere/highlight fallback','P2',note='Shadow may be functional support; visible material must receive explicit disposition. Painted texture drawing is retained.')
G='scripts/opera_gesture_surface.gd'
for fn,names,fam in [
('draw_clean_widget_playfield','Widget playfield fill bands|Widget frame','opera_shared'),
('draw_long_push','Push track and target','opera_shared'),
('draw_authored_trace_corridor','Trace corridor and target markers','opera_shared'),
('draw_trace_chef_subject','Chef tracing subject','opera_chef'),
('draw_trace_ballerina_subject','Ballet tracing subject','opera_ballerina'),
('draw_trace_doctor_subject','Doctor tracing subject','opera_doctor'),
('draw_trace_magician_subject','Magic tracing subject','opera_magician'),
('draw_magician_portal','Portal charge rings|Portal star aperture','opera_magician'),
('draw_racer_wheel','Steering-wheel rim and spokes','opera_racer'),
('draw_racer_kart_body','Tuning kart body and wheels','opera_racer'),
('draw_racer_tune','Tuning component markers','opera_racer'),
('draw_chef_crank','Whisk/stir vessel fallback','opera_chef'),
('draw_ballerina_crank','Ribbon crank subject','opera_ballerina'),
('draw_candymaker_crank','Candy wrapping subject','opera_candymaker'),
('draw_doctor_crank','Cast/bandage wrapping subject','opera_doctor'),
('draw_astronaut_crank','Valve casing/flow subject','opera_astronaut'),
('draw_popstar_crank','Microphone/sound control subject','opera_popstar'),
('draw_ballerina_blossom','Ballet blossom charge subject','opera_ballerina'),
('draw_astronaut_launch','Launch charge rocket/exhaust','opera_astronaut'),
('draw_popstar_soundcheck','Sound-check meter subject','opera_popstar'),
('draw_widget_family_ground','Widget ground/support surface','opera_shared'),
('draw_doctor_basin_subject','Hand-wash basin fallback','opera_doctor'),
('draw_candymaker_recipients','Candy recipient framing','opera_candymaker'),
('draw_anchored_targets','Anchored target rims','opera_shared'),
('draw_causal_backdrop','Task backdrop top/bottom bands','opera_shared'),
('draw_nursery_feed_scene','Baby feeding contact/fill accents','opera_nursery'),
('draw_nursery_bedtime_scene','Nursery bedtime sleep accents','opera_nursery'),
('draw_nursery_burp_scene','Nursery burp feedback','opera_nursery'),
('draw_magic_vanish_scene','Magic disappearance accents','opera_magician'),
('draw_clue_token','Clue token illustrated fallback','opera_detective'),
('draw_clue_board','Case board frame and target sockets','opera_detective'),
('draw_crown_chest','Crown chest lock/feedback accents','opera_detective'),
('draw_garden_plant','Farm plant growth fallback','opera_farmer'),
('draw_magic_cabinet','Magic cabinet hinge/reveal accents','opera_magician'),
('draw_nursery_context','Nursery context framing','opera_nursery'),
('draw_demo_finger','Gesture demo finger','opera_shared'),
('draw_xray_scan','X-ray scanner frame and scan accents','opera_doctor'),
('draw_dance_capsule','Dance note-pad capsule','opera_popstar'),
('draw_dance_sequence','Dance lane/progress accents','opera_popstar'),
('draw_candy_shape','Candy token shapes','opera_candymaker'),
('draw_candy_sort','Candy chute/sort pads','opera_candymaker'),
('draw_paint_reveal','Painter progressive reveal accents','opera_painter'),
('draw_farm_arc_guide','Vegetable toss arc guide','opera_farmer'),
('draw_farm_munch_reaction','Pig munch response','opera_farmer'),
('draw_farm_lob','Vegetable toss launcher framing','opera_farmer'),
('draw_boxer_mitt','Boxer practice mitt fallback','opera_boxer'),
('draw_boxer_rhythm','Boxer rhythm pads/beat accents','opera_boxer'),
('draw_imp','Generic imp fallback','opera_shared'),
('draw_shuffle_glide','Magic shuffle motion guide','opera_magician'),
('draw_pipe_tile','Straight/curved/cross pipe tile family','opera_astronaut'),
('draw_pipe','Pipe board, socket and flow accents','opera_astronaut'),
('draw_echo_star','Echo-game star token','opera_ballerina'),
('draw_echo','Echo portrait/selection framing','opera_ballerina'),
('draw_candymaker_pour_stream','Syrup stream','opera_candymaker'),
('draw_pour_scene','Candy mold fill/contact fallback','opera_candymaker')]:
    add(fam,G,'_'+fn,names,'P1',note='Draw-path family: accepted painted inputs and visible generated primitives coexist; inspect guards, exact phase and contact before choosing reuse/removal. Do not redraw every texture drawn by this function.')
for fn,names in [('river','Riverbed excavation cells|River source/sink pools|Connected flowing channel'),('fossil','Fossil dirt-cover cells|Fossil reveal slab and fragments'),('pan','Washing pan rim/body|Pan water/wash accents|Pan sand covering'),('geode','Geode closed shell|Geode matching opening halves|Geode seam targets'),('mineral','Mineral specimen token'),('crystal_gallery','Crystal gallery arrangement'),('work_surface','Geology workbench surface')]:
    add('opera_geologist','scripts/opera_geology_surface.gd','_draw_'+fn,names,'P1','IDENTIFIED','PAN_PATH and GEODE_PATH are empty at baseline; compatible states preserve arbitrary excavation, drag/snap, nine pan reversals, five seam targets and 120px pull.')
for fn,names in [('hint_button','Teacher hint button surface'),('pattern','Teacher pattern row sockets'),('counting','Teacher count/add/match answer surface'),('group','Teacher counted dot/token family'),('shape','Teacher circle/triangle/square lesson tokens'),('demo','Teacher demo pointer')]:
    add('opera_teacher','scripts/opera_teacher_surface.gd','_draw_'+fn,names,'P1','IDENTIFIED','Preserve exact shapes, counts, colors and answers. Painted material on the same semantic silhouettes; no decorative substitution.')
for fn,names in [('progress_lights','Boxing progress lights'),('punch_lanes','Boxing punch lanes'),('target','Boxing target cue'),('counter','Boxing counter guide'),('belt','Belt target cue (painted belt retained)'),('glove','Glove fallback'),('impact','Boxing impact starburst'),('friendly_hit','Friendly-hit feedback'),('demo','Boxing demo hand')]:
    add('opera_boxer','scripts/opera_boxing_surface.gd','_draw_'+fn,names,'P1',note='Keep painted actor/gloves where guards bind them; inspect tell, contact, recoil and settle as a complete action.')
for fn,names in [('shell_frame','Ballet portrait shell frame'),('round_pearls','Ballet round pearls'),('ribbon_game','Ballet ribbon guide/trace'),('twirl_game','Ballet twirl rim/guide'),('feedback','Ballet response accents'),('ghost_finger','Ballet ghost finger'),('completion_halo','Ballet completion halo')]:
    add('opera_ballerina','scripts/opera_ballet_surface.gd','_draw_'+fn,names,'P1',note='Keep reviewed held semantic poses and authored ribbon/twirl path; no atlas retiming or figure redraw.')
add('opera_racer','scripts/opera_racer_surface.gd','_draw_car','Kart ground shadow|Missing-kart body fallback','P1')
add('opera_racer','scripts/opera_racer_surface.gd','_draw_race_controls','Steering-control frame|Turbo control frame','P1')
add('dolls','scripts/games/dolls.gd','_draw','Nursery safety mat|Nursery quilt seams and tufts|Nursery cradle sling|Cradle focus halo|Caught-baby progress pips|Safe-landing ring','P1','IDENTIFIED','Painted babies/background stay intact; preserve broad catcher/mercy, no-fail landing and selected-skin mounting. Mat is one whole authored design.')
add('melody','scripts/games/melody.gd','FILE_SCOPE','Left theatre curtain|Right theatre curtain|Theatre crown header|Theatre stage apron|Theatre bulbs|Rainbow note rail|Melody note token|Melody start button|Melody guide arrow/rings|Melody progress pip|Melody reward star','P1','IDENTIFIED','Nested class construction exact lines in source_scopes. Seven pitch/color identities, 84px visual/120px touch footprints, timing and Daddy/Roshan source art are preserved.')
add('chapter2_party','scripts/chapter_two_party_table_2d.gd','_build_ember_visitor_stage','Ember scout silhouette|Ember King silhouette|Ember Prince silhouette|Candle-taking line arm','P1','BLOCKED','Explicit identity_art_approved=false. Inventory authoritative existing whole-unit identity/pose art; missing exact accepted identity/contact state blocks its dependent replacement, not this audit publication.')
add('chapter2_party','scripts/chapter_two_rainbow_candle_2d.gd','_draw','Missing-import vector candle fallback','P2','REUSE_READY','Normal path returns when both painted unlit/lit sprites exist. Accepted painted states remain; prove availability then retire fallback without regeneration.')
add('shared_ui','scripts/storybook_ui.gd','panel_style','Paper/shell panel fill and border','P1','IDENTIFIED','Visible UI art; retained functional Controls get authored texture/NinePatch material and pressed/focus states, preserving touch ownership and content margins.')
add('shared_ui','scripts/storybook_ui.gd','style_button','Button normal/hover/pressed/focus/disabled material','P1','IDENTIFIED')
add('shared_ui','scripts/storybook_ui.gd','style_picture_button','Picture-choice card normal/pressed/focus material','P1','IDENTIFIED')
add('shared_ui','scripts/shell_ornament.gd','_draw','UI shell ornament','P1','IDENTIFIED')
add('shared_ui','scripts/touch_ui.gd','FILE_SCOPE','Movement-pad/button material','P2',note='Optional fallback movement remains functional; visible frame and art receive disposition, invisible hit regions do not count as art.')
add('shared_ui','scripts/start_menu.gd','FILE_SCOPE','Start-menu inset/sheen|Start-menu decorative sparkle|Start-menu hold/reset fill','P1',note='Ordinary text and font rendering stay functional. Pictogram art must have phone-size semantic equivalents.')
add('child_authored','scripts/castle_logo_studio.gd','FILE_SCOPE','Saved logo symbol and color marks|Logo studio choice material','P2',note='Preserve saved child-authored identity and registered banner ownership. Paint presentation around it; child marks are authored content, not disposable placeholder art.')

# Raster lookalikes and literal runtime SVGs get explicit design records.
for filename,label in [('k_sprout.png','Garden common sprout'),('k_flower1.png','Garden mature result 1'),('flower.png','Garden mature result 2'),('flower2.png','Garden mature result 3'),('k_flower2.png','Garden mature result 4'),('flower3.png','Garden mature result 5'),('k_bush2.png','Flat leaf-mass bush'),('wateringcan.png','Garden watering can')]:
    path='assets/mg/'+filename
    if (R/path).is_file(): add('picture_games',path,'FILE_SCOPE',label,'P1',note='Raster extension supplies no visual exemption. Dated September audit is evidence; current slot-to-source/render pairing and source inspection decide replacement. Can material/edge suitability is separate from flatness; valid alpha retained and visible contamination unproved.')
for room in ['royal_bedroom','sleepover_bedroom','movie_lounge','dining_room','family_gallery']:
    path='assets_src/castle/dream_house_rooms_2k/room_'+room+'_background_master.png'
    for name in ['Ceiling and architectural shell','Window/door inset','Floor/rug design']:
        if (R/path).is_file(): add('castle_rooms',path,'FILE_SCOPE',room.replace('_',' ').title()+': '+name,'P1',note='Source composite/historical scene evidence shows flat shell language. Verify current native tile ownership/fixture-rig route before changing any master; preserve strong painted furniture, geometry and perspective. Pixel bounds remain to be measured.')
for path in sorted(R.glob('assets/**/*.svg')):
    add('literal_svg',path.relative_to(R).as_posix(),'FILE_SCOPE',path.stem.replace('_',' '),'P1','IDENTIFIED','Literal SVG source is flat candidate; painted hotspot presentation can suppress its actual pixels. Teacher and geology specialist consumers and crest route need individual visibility proof. Do not rasterize the same weakness.')


add('shared_ambience','scripts/living_world_canvas.gd','_draw_motif','Curtain/ribbon/flag motif|Steam motif|Candy motif|Rocket motif|Book motif|Mushroom motif|Paw motif|Gear motif|Paint motif','P1','IDENTIFIED','Named motif branches retain stage-specific usage and palette; runtime context decides removal or suitable authored reuse.')
add('picture_snowman','scripts/games/picture_games.gd','_mg_build_snowman','Snowman ground snow field','P1','IDENTIFIED','Broad procedural snow field lacks scene-ground material; painted carrot and Roshan retained.')
add('picture_snowman','scripts/games/picture_games.gd','_mg_snow_new_ball','Snowball rolling/stacked family','P1','IDENTIFIED','StyleBoxFlat ball and separate highlight panels; authored material preserves rolling growth, three ball radii, stacking, chase motion and carrot nose angle.')
add('picture_snowman','scripts/games/picture_games.gd','_mg_snow_face_phase','Snowman coal eye token','P1','NEEDS_CONTEXT_REVIEW','Painted farmer carrot already active; coal circle token needs its own context disposition.')
add('picture_trampoline','scripts/games/picture_games.gd','_mg_build_trampoline','Trampoline pad/frame','P1','IDENTIFIED','Procedural blue round panel squashed into a bar. Match painted trampoline surface, supporting rim/legs and contact state; preserve 400x140 target and 0.25/0.3s bounce route. Painted star retained.')
add('picture_slide','scripts/games/picture_games.gd','_mg_build_slide','Six-band diagonal rainbow slide','P1','IDENTIFIED','Six rotated ColorRects imply a broad slide without authored material/support. Preserve rainbow order, 1040x450 target and current travel path; show one supported slide, not a new route.')
add('picture_games','scripts/games/picture_games.gd','_mg2d_open','Picture-game gradient backdrop','P2','NEEDS_CONTEXT_REVIEW','Generated GradientTexture is a visible scene backing; retain only with explicit functional or painted-material disposition after scene review.')
add('picture_games','scripts/games/picture_games.gd','_mg2d_feedback_burst','Picture-game star/sparkle burst','P2','IDENTIFIED','Polygon2D celebration must remain coherent with earned action and unobscured payoff; reuse painted local feedback or remove unnecessary burst.')

def build():
    inv=json.loads((P/'source_inventory.json').read_text(encoding='utf8'))
    scopes=json.loads((P/'source_scopes.json').read_text(encoding='utf8'))['scopes']
    rows=[];errors=[]
    bypath={x['path']:x for shard in inv['image_shards'] for x in json.loads((P/shard['path']).read_text(encoding='utf8'))['images']}
    for seed in SEEDS:
        path=seed['path']; family=('opera_candymaker' if seed['family']=='opera_candy' else seed['family']); fn=seed['function']
        if Path(path).suffix=='.gd':
            try: start,end,lines=function_span(path,fn)
            except ValueError as exc: errors.append(str(exc));continue
        else: start=end=None;lines=[]
        row={'id':fid(path+'|'+fn+'|'+seed['name']),'name':seed['name'],'family':family,'count_unit':'named_art_role_state_family','repeated_instance_count':None,'source':{'path':path,'function':fn,'start_line':start,'end_line':end,'sha256':digest(R/path),'hash_mode':'LF-canonical text' if Path(path).suffix=='.gd' else 'binary byte exact'},'source_scope_ids':[s['id'] for s in scopes if s['path']==path and (fn=='FILE_SCOPE' or s['scope'].split('.')[-1]==fn)],'runtime_consumers':bypath.get(path,{}).get('consumers',[]),'screen_coverage':{'measured_current_bounds':None,'coverage_state':'COVERAGE_GAP','geometry_expressions':[l.strip() for l in lines if any(t in l for t in ['Rect2(','Vector2(','radius','size ='])][:15],'note':'Expressions are scope evidence, not measured per-piece screen bounds.'},'evidence_level':'SOURCE_INSPECTION','observed_weakness':seed['note'] or 'Procedural or flat material candidate identified by named visible role; actual guard, current frame and phone-size finish require review.','priority':seed['priority'],'child_impact':'Readable material, identity, contact and actionable-object hierarchy must remain clear with the HUD at phone size.','context_brief_id':'BRIEF-'+family.upper(),'reuse_candidates':[],'reuse_inspection':'Inventory completed; per-piece exact-purpose source match and current-context fit remain open unless named in context observations.','named_gap':None,'status':seed['status'],'integration_sha':None,'acceptance_evidence':{'current_mobile_runtime':None,'wide_phone_runtime':None,'device':None,'child':None,'owner':None,'machine':None,'old_fallback_retired':None},'dependencies':['Current route/phase capture and source-pixel ownership','Inspected suitable reuse or recorded exact missing gap','Applicable source/provenance/license/import/geometry/passive/save/teardown gates'],'unchanged_contracts':['Visible object/input/socket transforms and generous one-finger targets','Additive saves and unknown keys; no lost progress','Current action, answer/count, narrative and authored identity','Protected originals and owner-selected Day One clips'],'replacement_output':{'lane':'Canvas Sprite2D/TextureRect or authored texture material on functional Control','layer_owner':'Existing scene/controller; exact z_index retained unless reviewed framing change is needed','runtime_budget':'<=1024 longest side or POT; POT-only VRAM; Mobile/Speedy 30fps and measured overdraw','master_budget':'Background >=2048x2048 native PER playable screen before non-overlapping runtime tiles','provenance':'Preserved source hash/acceptance scope/license; separate derivatives, edits/state mapping and final hashes; new asset license rows'},'review_log':[]}
        if row['status']=='BLOCKED':row['named_gap']='Accepted whole-unit exact scene pose/identity authority and candle grasp state unbound; investigate existing accepted sources before generation.'
        if family=='opera_geologist':row['reuse_candidates']=['assets_src/geologist_rebuild_2026-09-05/geology_props_candidate.png','assets_src/geologist_rebuild_2026-09-05/geology_props_alpha_retry.png'];row['reuse_inspection']='Candidates retained, not approved for runtime; prior checkerboard rejection and current angle/whole-unit state gaps require native inspection.'
        if family=='picture_games':row['reuse_candidates']=['assets/props/story/flower_coral.png','assets/props/story/flower_lavender.png'];row['reuse_inspection']='Dated audit identifies references only; five distinct complete mature plants and matching sprout/root slots are not proven from these two flowers.'
        if row['status']=='REUSE_READY': row['reuse_candidates']=['assets/chapter2/birthday/rainbow_candle_unlit.png','assets/chapter2/birthday/rainbow_candle_large_flame.png'];row['reuse_inspection']='Exact normal-path assets bound at baseline; no new drawing required for fallback retirement. REUSE_READY does not grant runtime/owner acceptance.'
        rows.append(row)
    if errors: print('SEED_ERRORS',*errors,sep='\n');raise SystemExit(1)
    families=sorted({r['family'] for r in rows})
    specifics={
      'opera_geologist':('Cool lavender-aqua grotto and quiet warm specimens','Stone relief, sandy riverbed and satin pan','Overhead pan; workbench river/fossil/geode in existing specialist coordinate frame','Dug/flowing river, scrub/reassembled fossil, washing/clean pan, closed/seam/open geode','Arbitrary four-neighbour excavation, nine reversals, three snapping fossil pieces, five seam taps and 120px pull'),
      'opera_teacher':('Existing cool library/lesson palette with preserved answer colors','Painted pearl/wood board, tangible lesson tokens','Existing uncluttered planar board, aligned exact answer sockets','Hint/demo, pattern/count/add/match, selected/correct/settled states','Circle/triangle/square shapes, identical quantities, lesson answers and no reading-dependent substitute'),
      'melody':('Seven existing note colors; violet theatre frame and restrained gold','Fabric folds and painted shell/wood rail','Current Daddy-and-Roshan theatre framing; drape rooted at stage supports','Rest/current/hit note and pip states, guide/start/settle','Seven pitch identities, 84px visual/120px touch note footprint, actual timing and no zero-input reward'),
      'dolls':('Nursery mint/lavender and low-saturation floor','Padded textile mat and soft cradle, broad warm stitched value bands','Floor-plane mat with rim/sling at current catcher height','Idle, focus, catch, safety landing, caught pips and settle','Broad catcher/moving hit region, mercy/no-fail babies, selected skins, exactly earned progress'),
      'chapter2_party':('Current Main Hall party palette and authoritative Ember identities','Authored full-character contour/material; accepted candle pixels','Existing arrival/approach/grasp/carry/exit staging','Whole-unit Scout/King/Prince poses; coherent hand contact and candle ownership','Existing story, exact save beats, cue timing and one candle'),
      'castle_rooms':('Current room-specific ceiling/window/floor colors grounded in painted furniture','Broad painted stone/wood/cloth values; calm architectural fields','Lock source perspective, floor contacts and doorway/fixture geometry','Every currently reachable dirty/clean/free/reward room state','Preserve native plate/card ownership, all room hotspots and per-screen background coverage'),
      'shared_ui':('Shared violet/navy hierarchy, quiet aqua paper and warm action accents','Painted paper/shell NinePatch or bounded authored texture edges','Screen-plane UI and existing content margins; no new foreshortened hit regions','Normal, pressed, focus, disabled, selected and back states','>=110px generous targets, same input ownership and focus/pause/close cancellation'),
      'child_authored':('Preserve exact saved chosen colors and symbol','Painted backing/frame around authored child content','Existing registered banners and craft badge sockets','Current saved mark, change/preview/reload','Never erase/replace child marks or retain a second old generic mark beside them'),
      'picture_games':('Existing activity palette matched to painted Roshan, sun and butterflies','Whole plants with broad leaf/petal volumes and authentic root contact','Current five 228px planting slots and garden tool angle','Seed -> common sprout -> five distinct mature results; contact/settle','Slot mapping, water-can angle/hand/spout, tap states, conserved puzzle pieces and reward timing'),
      'day_one':('Room-authored dirt with Roshan colors preserved','Object-owned authored dirt; broad grime allowed only where current owner scope permits','Current plate/card ownership and actual cleaning sockets','Dirty arrival, cleaning contact, reduced dirt, clean/reward/return','Pool GS-17..21 repair retained; story clips straight-cut unchanged; room-specific wash scope unresolved'),
      'shared_ambience':('Stage-local palette from LivingWorldCatalog','Painted local biological/object silhouette and quiet translucent accent','Existing named corner/layer/pivot, never over active actor or target','Quiet idle and passive surprise only; seam/settle','No activity credit/passive reward, no extra ambience quota; <=one dominant landmark and three quiet support loops')
    }
    briefs=[]
    for family in families:
        palette,material,perspective,states,contracts=specifics.get(family,('Use the actual career/stage palette and source-authorized identity light state','Match the painted real object in that career, with grouped broad material bands','Bind to that job object and current stage perspective; measure support/contact and occlusion','Entry/anticipation/action/contact/payoff/settle plus phase-specific state','Existing phase geometry, object sockets, answer/save/gesture/lifecycle contracts'))
        briefs.append({'id':'BRIEF-'+family.upper(),'family':family,'piece_ids':[r['id'] for r in rows if r['family']==family],'scope':'Replacement planning only, overall replacement mission commissioned; no art generated in Phase 1','palette':palette,'material':material,'lighting':'Retain authored high-key scene light and cool shadows, never relight approved identity or apply blanket tint','perspective_scale':perspective,'support_contact_occlusion':'Measure actual object/hand/floor anchors and per-card depth from current Mobile captures, preserve whole-unit character contours; one owner for background/foreground pixels','interaction_purpose':contracts,'states_animation':states,'source_reuse_order':['Exact currently accepted authored source/states','Inspected equivalent existing repository art or non-destructive derivative','Named missing gap only, after reuse fails materially'],'output':'Separate lossless native/editable master, stable pivots/state map and compliant RGBA runtime cards/texture materials','review_required':['Source/isolated native alpha and contours','Current Mobile full action and frame-step transitions/seam','1280x720 and wide-phone HUD squint review','Actual device frame time/overdraw','Child and owner acceptance with source/build hashes'],'no_generation_reason':'Overall replacement mission is commissioned. Phase 1 audit delivers before subsequent context-reviewed production; no new approval checkpoint is created.'})
    save('piece_seeds.json',{'schema':'reef.flat_vector_seeds/1','seeds':SEEDS})
    save('per_piece.json',{'schema':'reef.flat_vector_pieces/1','baseline':BASE,'count_unit':'named_art_role_state_family; independent designs split, repeated instances and unresolved helper parts excluded from this design count','pieces':rows,'context_brief_ids':[b['id'] for b in briefs],'exhaustiveness_limit':'This is the named design register extracted during the complete source census. Additional designs/variants inside source_scopes and runtime-loaded/dynamic raster families remain unresolved; this count is a lower bound, never the final game-wide piece total.'})
    save('contextual_briefs.json',{'schema':'reef.flat_vector_briefs/1','baseline':BASE,'briefs':briefs})
    print('NAMED_PIECES',len(rows),'FAMILIES',len(families))

if __name__=='__main__': build()
