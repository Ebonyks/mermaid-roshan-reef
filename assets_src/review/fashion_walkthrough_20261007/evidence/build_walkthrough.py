from pathlib import Path
import hashlib, html, json, shutil, textwrap
from PIL import Image, ImageDraw, ImageFont

ROOT = Path.cwd()
OUT = ROOT / 'assets_src/review/fashion_walkthrough_20261007'
OUT.mkdir(parents=True, exist_ok=True)
for folder in ['native', 'annotations', 'audio', 'evidence']:
    (OUT / folder).mkdir(exist_ok=True)
bindings = {}

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def bind(source, destination, role):
    src, dst = ROOT / source, OUT / destination
    shutil.copyfile(src, dst)
    bindings[destination] = {'source_path': source, 'source_sha256': sha(src), 'role': role,
                             'modification': 'Byte-identical copy; source preserved'}
    return destination

old = 'assets_src/review/fashion_runtime_20261007/'
pics = {}
for src in sorted((ROOT / old).glob('*.png')):
    pics[src.name[:2]] = bind(old + src.name, 'native/' + src.name, 'SYNTHETIC_RUNTIME_REFERENCE')
assets = {
    'wardrobe': 'assets/flats/castle/dream_house/shell_wardrobe.png',
    'table': 'assets/flats/castle/dream_house/dining_table.png',
    'roshan': 'assets/characters/roshan_25d/roshan_base.png',
    'ribbon': 'assets/fashion/outfits/roshan_base_ribbon.png',
    'garden': 'assets/fashion/outfits/roshan_base_garden.png',
    'disguise': 'assets/fashion/outfits/roshan_base_disguise.png',
    'eagle': 'assets/fashion/outfits/baby_eagle_party.png',
    'daddy': 'assets/fashion/outfits/daddy_party.png',
    'rainbow': 'assets/fashion/outfits/rainbow_friend_party.png',
}
for key, src in assets.items():
    pics[key] = bind(src, 'native/asset-' + key + '.png', 'ASSET_BACKED_REFERENCE')
for i in ['11', '12', '13']:
    f = next((OUT / 'native').glob(i + '-*.png'))
    pics[i] = f.relative_to(OUT).as_posix()
    bindings[pics[i]] = {'source_path': 'Fresh-profile native output of evidence/capture_natural.gd',
                         'source_sha256': sha(f), 'role': 'NATURAL_INPUT_ENTRY_CAPTURE',
                         'modification': 'Native capture; no edits'}
catalog = json.loads((ROOT / 'assets/audio/fashion/VOICE_CATALOG.json').read_text(encoding='utf-8'))
voices = {}
for row in catalog['rows']:
    event = row['cue_id'].removeprefix('roshan_fashion_')
    dst = bind(row['audio_path'], 'audio/' + Path(row['audio_path']).name, 'EXACT_PROVISIONAL_RUNTIME_CUE')
    voices[event] = {'caption': row['caption'], 'path': dst, 'status': row['status']}
for src, dst in [
    (old + 'manifest.json', 'evidence/original_capture_manifest.json'),
    (old + 'machine_verification.json', 'evidence/runtime_machine_verification.json'),
    (old + 'frame_binding_revalidation.json', 'evidence/frame_binding_revalidation.json'),
    ('assets/audio/fashion/VOICE_CATALOG.json', 'evidence/voice_catalog.json'),
    ('assets_src/fashion_designer/party_garment_v1/provenance.json', 'evidence/garment_provenance.json'),
    ('tmp/capture_fashion.gd', 'evidence/original_synthetic_capture.gd'),
    ('tmp/capture_fashion_natural.gd', 'evidence/capture_natural.gd'),
    ('tmp/fashion-natural-capture.log', 'evidence/natural_capture.log'),
]:
    bind(src, dst, 'PROVENANCE_NOT_PLAYER_ROUTE_PROOF')

steps = []
def step(id, group, title, image, status, see, do, action, next_, cue=None, target=None, gap=None, refs=None):
    steps.append(dict(id=id, group=group, title=title, native=pics[image], status=status,
                      see=see, do=do, action=action, next=next_, cue=voices.get(cue),
                      target=target, gap=gap, source_refs=refs or []))

N = 'NATURAL INPUT • ENTRY ONLY'
S = 'SYNTHETIC RUNTIME REFERENCE'
A = 'ASSET ILLUSTRATION • CAPTURE GAP'
P = 'PROPOSED • NOT YET PLAYABLE'
step('01','Entry and everyday clothes','Start a fresh adventure','11',N,
     'The launch splash has New Game on the right. Continue is disabled in this isolated fresh profile.',
     'Tap New Game at (820,607), inside StartMenuNewGameButton. A real mouse press/release entered through the normal UI.',
     'The menu hands off to the existing Day One opening; this is entry evidence, not Fashion progress.',
     'Watch the opening, then follow Roshan toward the castle.',target=[650,548,340,118],refs=['scripts/start_menu.gd:322'])
step('02','Entry and everyday clothes','The castle introduction','13',N,
     'Roshan is outside the castle. The visible message says “Let’s go to the castle!”',
     'This panel records the reached state after the opening. No additional action was injected.',
     'New Game → opening → castle arrival was observed. No wardrobe selection or party unlock was created.',
     'Play Day One and follow the real castle route. That traversal was not captured in this bounded check.',
     gap='Natural footage from this arrival through Royal Bedroom wardrobe entry is missing. The short run is not a full-route test.')
step('03','Entry and everyday clothes','Find the shell wardrobe','wardrobe',A,
     'Source artwork for the shell wardrobe in Royal Bedroom, item ID shell_wardrobe. This is a prop reference, not a room screenshot.',
     'Tap the actual wardrobe object in Royal Bedroom. Its room-authored target is the prop, not this illustration.',
     'The handler flashes the wardrobe through four short glint states, emits a sparkle burst and opens the old look picker. It does not make Roshan travel to or touch the wardrobe.',
     'In the old picker, tap the pictured Clothes button at (1080,548), size 132×132.',
     gap='Entry, glint midpoint, picker and hand/contact captures are absent. Text cue: “Pretend dress-up time! A crown, a cape, or both!” The exact entry voice/pointer is not bound by this packet.',
     refs=['scripts/arena/castle_rooms_25d.gd:698','scripts/wardrobe_ui.gd'])
step('04','Entry and everyday clothes','Choose who to dress','01',S,
     'Five portraits: Roshan, Rumi, Baby Eagle, Daddy and Rainbow Friend. The large left picture previews the chosen person.',
     'Tap a portrait. Rumi’s target is (171,106), size 116×136. Portraits are the visual choice cue.',
     'The selected portrait turns warm gold; the preview and three clothing cards rebuild for that person. No fitting animation occurs.',
     'Choose one of that person’s clothing cards.',cue='choose',target=[171,106,116,136],refs=['scripts/fashion_wardrobe.gd:89'])
step('05','Entry and everyday clothes','Rumi has her own saved look','02',S,
     'Rumi replaces Roshan in the preview and clothing cards; the selected Rumi portrait is highlighted.',
     'Tap an unlocked pictured outfit on the right. Original and Ribbon are always available; Party and Garden depend on earned milestones.',
     'The look replaces Rumi’s texture and saves independently of Roshan’s choice. The existing capture was staged by direct model/UI calls; it does not prove a natural tap.',
     'Select another friend or return to Roshan.',cue='changed',target=[787,258,196,306],refs=['scripts/fashion_designer.gd','scripts/fashion_outfit_renderer.gd'])
step('06','Entry and everyday clothes','Try a ribbon on Roshan','ribbon',A,
     'The existing ribbon derivative is shown alone so its change is inspectable. This is not a captured equip moment.',
     'In the wardrobe choose Roshan, then the Ribbon card, the middle card on page one.',
     'Original → ribbon detail on existing Roshan. The model equips, saves immediately, refreshes the portrait and emits a bounded sparkle burst. No drag, sewing or physical dressing is implemented.',
     'Keep exploring clothes; leaving does not undo the choice.',cue='changed',
     gap='Actual before / press / sparkle / after sequence was not captured. This illustration cannot establish the transition.',refs=['scripts/fashion_wardrobe.gd:207'])
step('07','Entry and everyday clothes','Dress Baby Eagle','eagle',A,
     'Existing Baby Eagle Party derivative: accessory changes on the original character.',
     'Tap the third portrait (297,106), then its unlocked outfit card. The party look shown requires the party milestone.',
     'Baby Eagle’s outfit is saved separately and used by the companion texture lookup. No cape fitting or Eagle reaction is authored.',
     'Tap Daddy or Rainbow Friend to dress them.',cue='choose',gap='No native Baby Eagle chooser/equip/world-reload capture is available.')
step('08','Entry and everyday clothes','Dress Daddy','daddy',A,
     'Existing Daddy Party derivative; this is accessory clothing rather than a new tailored coat.',
     'Tap the fourth portrait (423,106), then a pictured unlocked outfit.',
     'Daddy’s saved selection updates participating family/world portraits. The illustration proves only the available source pixels.',
     'Choose Rainbow Friend or finish.',cue='choose',gap='No native Daddy chooser, family appearance or save-reload capture is available.')
step('09','Entry and everyday clothes','Dress Rainbow Friend','rainbow',A,
     'Existing Rainbow Friend Party derivative, reused without a character redraw.',
     'Tap the fifth portrait (549,106), then an unlocked clothing card.',
     'The saved selection is independent of the other four people. This is a texture change; there is no wrap fitting animation.',
     'Browse the next clothing page or close the wardrobe.',cue='choose',gap='No native Rainbow Friend equip, following or save-reload capture is available.')
step('10','Entry and everyday clothes','Locked clothes explain where to earn them','03',S,
     'The next Roshan page shows Garden and Garden Disguise with locks and source pictures. On page one, Party has a cake picture.',
     'Tap Next at (738,577), size 132×110. Tap a locked card to hear its source cue; it never equips locked clothes.',
     'Party earns the party looks; Farmer strawberries / earned Farmer progress earns Garden. Finishing disguise practice earns the disguise. Unlocking makes a choice available; it does not automatically change anyone’s look.',
     'Earn the pictured milestone, then reopen the wardrobe and choose the look.',cue='locked_garden',target=[575,258,196,306],refs=['scripts/fashion_designer.gd:109'])
step('11','Entry and everyday clothes','Leave wearing the selected look','06',S,
     'A diagnostic world capture shows Roshan in the party look in Throne Hall. The older harness used the bedroom alias, which resolved here; this is not a Royal Bedroom capture.',
     'In the wardrobe tap the bottom-right check at (1040,577), size 165×110, or the top-left Back button.',
     'The overlay closes and the equipped look remains in the world. Roshan’s position in this screenshot was staged, so it proves composition only.',
     'Return to normal play. Reopening should display saved choices.',
     gap='Natural leave, cross-room traversal and close/relaunch captures are missing. Save/re-entry model checks are machine evidence, not visible player-route proof.',refs=['scripts/wardrobe_ui.gd','scripts/save_state.gd'])
step('12','The pre-party special dress','Finish preparations and touch the party table','table',A,
     'The existing dining-table source stands for the Main Hall party display. This isolated prop is not the finished in-room party table.',
     'After all eight preparation careers and the rainbow candle are ready, tap the Main Hall party display/rainbow hotspot. ChapterTwoPartyTableTouch occupies room coordinates (285,352), size 710×238.',
     'The real route asks for Roshan’s dress before first lawn ignition. Room text says “Your friends are waiting outside! Tap the rainbow to visit the party!”',
     'The special-dress page opens.',
     gap='Natural eight-job completion and party-hotspot entry capture are absent. MA-PLAY-005 tracks the existing fresh-play Chapter 2 route problem; this packet does not repair or close it. Room text is source-backed; its exact voice/pointer is not captured.',
     refs=['scripts/chapter_two_room_plot.gd:92','scripts/main.gd:6019'])
step('13','The pre-party special dress','Put on the special dress','04',S,
     'The Party dress page offers one outfit card and a downward hand pointer above it.',
     'Tap the dress card at (575,258), size 196×306. Help repeats the same instruction.',
     'The intentional choice equips the party look, writes the outfit and dress milestone, then closes the wardrobe. The child does not drag a garment or personalise its flower/bow in this alpha.',
     'The deferred normal route opens the lawn party before Iko Iko / Ember King.',cue='party_dress',target=[575,258,196,306],refs=['scripts/fashion_wardrobe.gd:207','scripts/main.gd:6019'])
step('14','The pre-party special dress','Inspect the equipped dress','05',S,
     'Roshan’s preview has the floral party clothing; the card carries a check.',
     'This image was made by direct model equip followed by reopening the dress page. In normal play, selecting the dress closes this page immediately.',
     'Before: original clothing in step 13. After: party clothing shown here. The midpoint, Roshan’s physical dressing and the natural lawn handoff are not recorded.',
     'Normal gameplay proceeds onto the lawn. This reopened diagnostic page is not an additional child step.',
     gap='No actual dress fitting/contact or admiration acting exists. No natural party arrival / Iko Iko / Ember King capture is included.')
step('15','Later disguise practice','Open the mask button after the story','10',S,
     'The wide-screen clothes page includes the mask button at lower left after Chapter 2 story completion. It is not an Opera career card.',
     'Open clothes, then tap FashionDisguisePlay at design coordinates (55,577), size 180×110. At wide aspects, the stage scales these coordinates.',
     'The wardrobe switches to a pictured three-phase practice. No Fashion Opera star is added and the eight birthday preparation bits are unchanged.',
     'Start or resume the first incomplete practice phase.',
     gap='Practice entry was staged by setting the story-complete flag and calling the UI method. Natural unlock and mask-button press are not captured.',refs=['scripts/fashion_designer.gd','scripts/fashion_wardrobe.gd:201'])
step('16','Later disguise practice','Phase 1: pick Garden','07',S,
     'A small Garden Roshan picture is above three full-character outfit cards: Ribbon, Party and Garden.',
     'Tap the Garden card on the right at (999,258), size 196×306. Static hand pointers sit above all cards.',
     'Correct pick: equips Garden and saves practice prefix 1; next prompt opens. Roshan’s torso changes to green. There is no garden station, prop selection or gardening act.',
     'Phase 2 replaces the goal picture with Garden Rumi.',cue='role_pick',target=[999,258,196,306],refs=['scripts/fashion_designer.gd:166'])
step('17','Later disguise practice','Phase 2: choose Garden again','08',S,
     'Garden Rumi is now the goal picture. Roshan is already wearing Garden, which is checked on the right.',
     'Tap the same Garden card again. A Ribbon or Party choice repeats the gentle help cue without advancing.',
     'Practice prefix becomes 3. Usually no visible clothing change occurs because phase 1 already equipped Garden. No plant camouflage, movement or Rumi hide-and-seek is implemented.',
     'Phase 3 offers a single Bow card.',cue='blend_pick',target=[999,258,196,306],refs=['scripts/fashion_designer.gd:166'])
step('18','Later disguise practice','Phase 3: choose the finished bow look','09',S,
     'One card labelled Bow pictures the full finished disguise, not an isolated bow piece or attachment socket.',
     'Tap that card at (575,258), size 196×306.',
     'The model saves prefix 7, grants the Garden Disguise once, records the reward and equips it. The UI then returns to the normal clothes page and says the done cue.',
     'Keep wearing the reward in normal play.',cue='finish_piece',target=[575,258,196,306],
     gap='The old diagnostic harness stopped before this choice. There is no input midpoint, completed page or reward-transition screenshot.',refs=['scripts/fashion_wardrobe.gd:116','scripts/fashion_designer.gd:166'])
step('19','Later disguise practice','The persistent reward','disguise',A,
     'The existing Garden Disguise derivative illustrates the earned look. It is not a captured completion screen.',
     'No further confirmation is needed. Leave clothes with Check / Back.',
     'Garden → finished disguise with its accessory. The done cue plays on the ordinary wardrobe. Reward is once-only; no score, loss, timer or party star.',
     'Return later with the reward available as an everyday choice.',cue='done',
     gap='Native before / bow contact / completion / return / reload evidence is missing. The alpha has no authored bow-placement contact or pretend-show finish.')
step('20','Persistence and variants','Return, resume and replay limits','10',S,
     'The ordinary wardrobe remains available in free play and preserves five independent character choices.',
     'Reopen the wardrobe and choose any owned look. If practice was unfinished, the mask button resumes its first incomplete phase.',
     'Saved prefixes and outfits survive reload in machine probes. Completed practice redirects to normal clothes with the done cue; there is currently no reset button for a fresh round.',
     'Use the wardrobe for repeated dressing; completed disguise practice is not a replayable minigame yet.',
     gap='No natural close/relaunch capture is available. Existing model/UI save probes prove data behavior, not the complete child route.',refs=['scripts/fashion_designer_test_case.gd'])
step('21','Persistence and variants','World and Opera presentation','06',S,
     'The diagnostic Throne Hall capture is one world appearance example. Other participating scenes use the shared texture lookup.',
     'Continue normal play to see chosen clothes on recurring characters where their shared renderer is used.',
     'Career uniforms retain their activity-specific presentation; fixed owner-selected Day One clips retain their flattened original pixels. There is no separate Fashion Opera career or authored costume reaction here.',
     'Review actual wardrobe-to-world, Opera return and family appearances on a device.',
     gap='Castle companion, Rumi, family/lawn, kart, Galaxy, combat/dungeon, Conservatory and Opera return natural captures are absent. Source integration is not visual acceptance.',refs=['scripts/fashion_outfit_renderer.gd','assets_src/review/fashion_runtime_20261007/machine_verification.json'])
step('P1','Proposed redesign — not yet playable','Make clothes for a friend','02',P,
     'Current Rumi chooser is used only as a reference for the proposed dressing doll.',
     'Proposed: choose a friend, then a distinct garment, pattern and accessory from pictured hangers. Every everyday combination is welcome.',
     'Proposed: garments fit visibly onto the friend; use a dress for Rumi, coat for Daddy, cape for Baby Eagle and wrap for Rainbow Friend. These tailored garments and contact animations are missing sources, not existing gameplay.',
     'Admire the outfit together and save it immediately.',gap='Proposal only. Current alpha uses small outfit variants and card taps. No new garment/acting art was generated for this walkthrough.')
step('P2','Proposed redesign — not yet playable','A birthday dressing ritual','04',P,
     'The existing special-dress page anchors the owner-required placement before the party / Iko Iko / Ember King.',
     'Proposed: open the special dress, choose a flower or bow, and place it on Roshan with one generous gesture.',
     'Proposed: Roshan looks down at the fitted dress, admires it and enters the party in her personalised look. Keep save immediate and Back safe.',
     'The birthday begins after the dressing beat.',gap='Personalisation, placement contact and admiration are not implemented. This screenshot is a reference, not a new storyboard scene.')
step('P3','Proposed redesign — not yet playable','Dress for a role, then act it','07',P,
     'The existing Garden choice is a limited costume reference for a later pretend-play rehearsal.',
     'Proposed: pick role clothes and a pictured prop, then help the friend act that role through one simple touch activity.',
     'Proposed: Roshan travels to the station, visibly uses the prop and completes the act before advancing. Role-specific clothes, location, actions and exact voice/pointer need authoring.',
     'Try blending into a friendly setting.',gap='Role rehearsal and a specific narrative disguise mission are not playable or bound. Preserve later story placement; do not treat this proposal as canon approval.')
step('P4','Proposed redesign — not yet playable','Blend, finish a friend and play together','08',P,
     'The current Garden Rumi picture is a reference for a friend-based disguise activity.',
     'Proposed: choose a flower or leaf silhouette, swim among plants for gentle hide-and-seek, then fit a missing piece onto a friend.',
     'Proposed: placement has generous contact, the friend reacts, and both join a pretend show. Roshan remains recognisable. A mismatch invites another playful try without losing progress.',
     'The earned clothes remain wearable across the game and the rehearsal can be replayed.',gap='Camouflage shapes, hiding location, fitting/contact, friend reaction, show and repeat-round flow are missing. No invented gameplay screenshot or new art is supplied.')

font_path = 'C:/Windows/Fonts/segoeui.ttf'
bold_path = 'C:/Windows/Fonts/segoeuib.ttf'
def font(size, bold=False):
    return ImageFont.truetype(bold_path if bold else font_path, size)

def annotate(s):
    native = Image.open(OUT / s['native']).convert('RGBA')
    w, h = 1280, 880
    board = Image.new('RGBA',(w,h),'#f4f0fa')
    d = ImageDraw.Draw(board)
    color = '#245948' if s['status']==N else '#5e426f' if s['status']==S else '#875319' if s['status']==A else '#8a3559'
    d.rectangle((0,0,w,94),fill=color)
    d.text((26,10),s['status'],font=font(19,True),fill='white')
    d.text((26,38),s['id']+'  '+s['title'],font=font(30,True),fill='white')
    trim = None
    if s['status']==A:
        trim = native.getbbox()
        native = native.crop(trim)
        native.thumbnail((900,530),Image.Resampling.LANCZOS)
        x,y=(w-native.width)//2,110+(600-native.height)//2
    else:
        native.thumbnail((1280,720),Image.Resampling.LANCZOS)
        x,y=(w-native.width)//2,94+(720-native.height)//2
    board.alpha_composite(native,(x,y))
    comparison = None
    if s['id'] in ['06','19']:
        comparison = pics['roshan' if s['id']=='06' else 'garden']
        board.paste('#f4f0fa',(0,94,w,814))
        before = Image.open(OUT/comparison).convert('RGBA')
        before = before.crop(before.getbbox())
        before.thumbnail((470,560),Image.Resampling.LANCZOS)
        board.alpha_composite(before,((w//2-before.width)//2,185+(560-before.height)//2))
        board.alpha_composite(native,(640+(640-native.width)//2,185+(560-native.height)//2))
        d=ImageDraw.Draw(board)
        d.text((175,120),'BEFORE · source asset',font=font(24,True),fill='#40294f')
        d.text((825,120),'AFTER · source asset',font=font(24,True),fill='#40294f')
        d.text((590,390),'→',font=font(65,True),fill='#875319')
    if s['target'] and s['status']!=A:
        tx,ty,tw,th=s['target']; scale=native.width/Image.open(OUT/s['native']).width
        box=(x+tx*scale,y+ty*scale,x+(tx+tw)*scale,y+(ty+th)*scale)
        d=ImageDraw.Draw(board)
        d.rounded_rectangle(box,radius=14,outline='#f22f5c',width=6)
        d.ellipse((box[0]-20,box[1]-20,box[0]+20,box[1]+20),fill='#f22f5c')
        d.text((box[0]-6,box[1]-17),'1',font=font(24,True),fill='white')
    d=ImageDraw.Draw(board)
    d.rectangle((0,814,w,h),fill='#eee6f7')
    label='Review annotation only • native source preserved • '+('capture/acting gap remains' if s['gap'] else 'read the action and evidence caption below')
    d.text((24,830),label,font=font(20),fill='#40294f')
    dst='annotations/'+s['id']+'.png'
    board.convert('RGB').save(OUT/dst)
    s['annotation']=dst
    bindings[dst]={'source_path':s['native'],'source_sha256':sha(OUT/s['native']),
                   'role':'REVIEW_ANNOTATION_NOT_RUNTIME_PIXELS','modification':'Lossless separate board: fitted source image, status/title/footer; outlined source UI target where applicable. No character or scene painting.'}
    if trim:
        bindings[dst]['annotation_only_alpha_trim']=list(trim)
    if comparison:
        bindings[dst]['comparison_source']=comparison
        bindings[dst]['comparison_sha256']=sha(OUT/comparison)
for s in steps:
    annotate(s)

def esc(x): return html.escape(x or '')
header = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Fashion Designer — illustrated walkthrough</title><style>
:root{color-scheme:light}*{box-sizing:border-box}body{margin:0;background:#f7f3fb;color:#2b2237;font:17px/1.55 system-ui,sans-serif}header,main,footer{max-width:1100px;margin:auto;padding:24px}header{padding-top:40px}h1{font-size:clamp(30px,5vw,48px);line-height:1.1;margin:0 0 18px}h2{margin:44px 0 16px;font-size:30px}h3{margin:0;font-size:25px}.intro,.gap{background:#fff4da;border-left:5px solid #ab731b;padding:14px 18px}.badge{display:inline-block;font-size:12px;font-weight:750;letter-spacing:.05em;background:#eee0f1;border-radius:20px;padding:6px 12px;margin-bottom:12px}nav{display:flex;flex-wrap:wrap;gap:10px;margin-top:22px}nav a,.source{border:1px solid #d8c9e6;border-radius:10px;padding:8px 12px;background:white}a{color:#593080}article{background:white;border:1px solid #ddcfe9;border-radius:18px;margin:18px 0;overflow:hidden;box-shadow:0 5px 20px #3b155b08}article.proposed{border:2px dashed #a34875}.caption{padding:22px}.panel{display:block;width:100%;height:auto}.fields{display:grid;grid-template-columns:130px 1fr;gap:8px 18px;margin:16px 0}.fields dt{font-weight:700}.fields dd{margin:0}audio{width:100%;max-width:460px;height:36px}.proof{font-size:14px;color:#665775}.gap{margin-top:18px}.source{display:inline-block;margin-right:8px}footer{font-size:14px} @media(max-width:600px){header,main{padding:15px}.fields{grid-template-columns:1fr;gap:3px}.fields dd{margin-bottom:10px}.caption{padding:15px}h2{font-size:25px}} </style><header><p class="badge">OWNER REVIEW · SOURCE 62389344 · 7 OCTOBER 2026</p><h1>Fashion Designer<br>What the child does, step by step</h1><p>Current playable alpha first. The redesign proposal appears in a separate final section.</p><div class="intro"><strong>This is an illustrated process reference, not a complete natural-play recording.</strong> The fresh launch uses real UI input. The ten wardrobe screenshots were staged with model/UI calls. Other panels show preserved source assets. Missing action/contact, completion, birthday-route and reload captures stay visible. No device, child or owner acceptance is claimed.</div><nav><a href="#everyday">Everyday clothes</a><a href="#party">Party dress</a><a href="#practice">Disguise practice</a><a href="#saved">Persistence / variants</a><a href="#proposal">Proposed redesign</a><a href="README.md">GitHub-readable version</a><a href="manifest.json">Manifest</a></nav></header><main>'''
ids={'Entry and everyday clothes':'everyday','The pre-party special dress':'party','Later disguise practice':'practice','Persistence and variants':'saved','Proposed redesign — not yet playable':'proposal'}
body=[]; md=['# Fashion Designer — illustrated process walkthrough','','Source runtime: `6238934447cf28834874396dfbaff65effafda46` (Godot 4.7.2-stable / Mobile). Owner review: 2026-10-07.','','[Open the browsable local HTML](index.html) after downloading this folder. This README also renders the complete illustrated walkthrough on GitHub. Click each panel or its **Native full-size source** link to inspect the image. Exact provisional voice files are included.','','**Evidence limits:** fresh launch uses real UI input; the ten wardrobe captures are synthetic model/UI-call references. Source-asset illustrations and missing captures are marked in every affected step. No natural wardrobe-to-party/disguise/reload route, fitting/contact or target-device/child/owner acceptance is claimed. The richer design is a proposal only.','','[Manifest and SHA-256 inventory](manifest.json) · [Step data](steps.json) · [Natural input observation](native/natural_input_observation.json) · [Original synthetic harness](evidence/original_synthetic_capture.gd)','','The child’s current disguise activity is Garden → Garden again → finished Bow look. It has no dress placement, gardening, camouflage, hide-and-seek or pretend-show performance. Persistent clothing is implemented; those proposed play improvements are not.','']
last=None
for s in steps:
    if s['group']!=last:
        body.append('<h2 id="'+ids[s['group']]+'">'+esc(s['group'])+'</h2>')
        md.extend(['## '+s['group'],''])
        last=s['group']
    body.append('<article id="step-'+s['id']+'" class="'+('proposed' if s['status']==P else '')+'"><a href="'+s['annotation']+'"><img class="panel" src="'+s['annotation']+'" alt="'+esc(s['id']+' '+s['title']+' — '+s['status'])+'" loading="lazy"></a><div class="caption"><span class="badge">'+esc(s['status'])+'</span><h3>'+esc(s['id']+' · '+s['title'])+'</h3><dl class="fields">')
    md.extend(['### '+s['id']+' · '+s['title'],'','**'+s['status']+'**','','[![Review panel '+s['id']+']('+s['annotation']+')]('+s['annotation']+')',''])
    for label,key in [('See','see'),('Input / target','do'),('Roshan / change','action'),('Next','next')]:
        body.append('<dt>'+label+'</dt><dd>'+esc(s[key])+'</dd>')
        md.extend(['**'+label+':** '+s[key],''])
    body.append('</dl>')
    if s['cue']:
        c=s['cue']; body.append('<p><strong>Voice:</strong> “'+esc(c['caption'])+'”</p><audio controls preload="none" src="'+c['path']+'"></audio><p class="proof">Exact current provisional cue; human voice acceptance remains pending.</p>')
        md.extend(['**Voice:** “'+c['caption']+'” [Listen]('+c['path']+') — provisional; human acceptance pending.',''])
    if s['gap']:
        body.append('<p class="gap"><strong>Coverage gap:</strong> '+esc(s['gap'])+'</p>')
        md.extend(['**Coverage gap:** '+s['gap'],''])
    body.append('<p><a class="source" href="'+s['native']+'">Native full-size source</a><a class="source" href="#step-'+s['id']+'">Step link</a></p></div></article>')
    md.extend(['[Native full-size source]('+s['native']+')',''])
footer='''</main><footer><p>Annotations are separate copies. No protected originals were changed. No new images were generated and no gameplay was redesigned for this packet.</p><p>Existing full runtime verification: frozen local 82 probes and exact-head remote Probe Suite 37603992197 / 37604042115 succeeded for 62389344. Those checks do not supply missing visual, device, child or owner evidence. MA-VIS-006, MA-PLAY-004 and MA-PLAY-005 retain their existing lifecycle states.</p><p>Scope: no Fashion Opera star; eight birthday careers unchanged; later narrative disguise mission unbound. Proposal garments/actions are named gaps.</p></footer></html>'''
(OUT/'index.html').write_text(header+''.join(body)+footer,encoding='utf-8')
md.extend(['## Verification and remaining acceptance','','The runtime baseline passed the frozen local suite (82 probes; log SHA-256 `8e0650a0d814c88d053cfe3709879f7b9ccfc9b35c8182e4515547922e967826`) and exact-head remote [topic Probe Suite 37603992197](https://github.com/Ebonyks/mermaid-roshan-reef/actions/runs/37603992197) and [PR Probe Suite 37604042115](https://github.com/Ebonyks/mermaid-roshan-reef/actions/runs/37604042115). This packet changes only non-runtime review material and documentation. These machine results do not prove natural-route capture, device, child or owner acceptance.','','MA-VIS-006 / MA-PLAY-004 / MA-PLAY-005 remain in their existing lifecycles. No defect is closed. No 4.6/5 quality score is asserted.','','Native capture limit: one actual UI target; the opening then reaches the castle introduction. No phase/completion callback or save edit was used. The ten old captures explicitly use synthetic state and direct UI/model calls; the original harness is retained for inspection. The before/after dress comparison includes a reopened diagnostic page, not a natural extra child step.','','Packet asset rows in ASSET_LICENSES.md retain their source attribution; copying a provisional asset here does not accept its pixels or voice. The original capture manifest retains its historical baseline; runtime source binding is separately checked at this packet’s source commit.','','[Audit impact](../../../..//design/audit_impacts/fashion-walkthrough-20261007.json) · [Current feature brief](../../../design/FASHION_DESIGNER_ROSHAN_2026-10-06.md) · [Packet check](evidence/verification.json)',''])
(OUT/'README.md').write_text('\n'.join(md).replace('../../../..//','../../../../'),encoding='utf-8')
(OUT/'steps.json').write_text(json.dumps({'schema':'reef.fashion_walkthrough_steps/1','steps':steps},indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
(OUT/'source_bindings.json').write_text(json.dumps(bindings,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print('BUILT',len(steps),'steps;',len(bindings),'source bindings')
