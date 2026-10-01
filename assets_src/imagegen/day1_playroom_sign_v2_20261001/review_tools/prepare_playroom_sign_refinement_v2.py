from pathlib import Path
import hashlib, json
from PIL import Image

root=Path(__file__).resolve().parents[1];family=root/'assets_src/imagegen/day1_playroom_sign_v2_20261001'
assert not family.exists(),'Preserve prior sign generation studies.';family.mkdir(parents=True)
(family/'.gdignore').write_text('',encoding='utf-8')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
paths=['assets/flats/castle/main_hall_redraw_2026-08-03/signs/sign_playroom.png',
 'assets/flats/castle/main_hall_redraw_2026-08-03/signs/sign_mermaid_pool.png',
 'assets/flats/castle/main_hall_redraw_2026-08-03/signs/sign_kitchen.png']
rows=[]
for name in paths:
 p=root/name
 with Image.open(p) as image:dimensions=list(image.size)
 rows.append({'path':name,'sha256':sha(p),'dimensions':dimensions,'role':'Identity/layout source' if 'playroom' in name else 'Existing sibling medal style source','source_modified':False})
prompt='''Use case: illustration-story. Asset type: a single transparent 2D game navigation medallion for the existing toy playroom, replacing only a named uneven top-border defect. Generate a fresh illustration from this text; no uploaded reference images.
Subject: a friendly honey-brown teddy bear HEAD emblem, round and softly padded, two equal complete round ears with cream inner ears, simple large dark-brown eyes with tiny restrained highlights, a warm cream oval muzzle, small brown nose and a calm little smile. Front view, welcoming and suitable for a four-year-old. Keep the established generic teddy emblem identity; no body, costume, new character, scene or story.
Frame: one complete circular cream scalloped medal with a coherent honey-gold inner edge, dark navy/plum outer contour, restrained lavender outer shadow. Every top scallop joins cleanly into the continuous ring; no flat dark fragment, tag, ribbon or extra attachment at twelve o'clock. Broad matte painted value bands, rounded toy forms and very restrained soft shading, polished 2D storybook illustration. No metallic realism, fine noise, wet glints, photorealistic fur or 3D render.
Composition: perfectly centered square transparent canvas. The entire bear-and-medal silhouette is complete and occupies about forty percent of the canvas width and height, matching a generously padded existing256px icon card. True alpha around it, including the large empty margins. All art remains within the canvas. Plain transparent background, no checkerboard pixels, text, letters, symbols, watermark or extra objects. The face must stay readable when the medal itself is rendered about50px wide.'''
profile={'schema':'reef.playroom-sign-refinement.v1','status':'GENERATION_PENDING_SOURCE_AND_NATIVE_REVIEW',
 'baseline':'5b8bfb989ca8012924115d45901252808edb9b62','source_catalog':'audit/day_one_job_art_census_v2_20261001/NATIVE_RESOURCE_CATALOG.json#D1N-0072',
 'gap':'Published whole-source4.5 drafting opinion remains an inclusive priority: the upper medal ring contains a short dark/tan/cream flat fragment breaking the otherwise scalloped border. This is a local coherence issue, not canvas-edge clipping of the bear.',
 'reuse_inventory':rows,'scoped_search':'Relevant room-sign directory and repository filenames were searched for alternate bear/playroom badge/medal sources. Only this bear sign was found in the scoped existing family; water and kitchen medals carry different objective symbols. No suitable clean same-bear source was established. This is one named live navigation-art gap, not an open redesign.',
 'constraints':'Preserve original and runtime binding. Candidate is non-runtime. Keep generic teddy head identity, warm rounded proportions, cream/gold scalloped frame and navy/plum/lavender contour family; no new scene, canon or protected artwork. New source/style and actual normalized navigation fit must be individually audited before selection.',
 'prompt':prompt,'prompt_sha256':hashlib.sha256(prompt.encode()).hexdigest(),'generation_method':'Built-in imagegen, fresh text-only, true transparent background; no reference uploads',
 'acceptance':'No generation/source/native/owner pass yet; original score remains4.5. Source and in-context phone-size readability are separate. Working target4.6 clears the inclusive queue.'}
(family/'PROFILE_AND_PROMPT.json').write_text(json.dumps(profile,indent=2)+'\n',encoding='utf-8')
impact={'id':'day-one-playroom-sign-v2-20261001','baseline':profile['baseline'],'scope':profile['gap']+' '+profile['constraints'],
 'rules':['DL-AUTH-05','DL-AUTH-06','DL-AUTH-07','DL-ASSET-01','DL-ASSET-03','DL-ASSET-04','DL-ASSET-05','DL-VIS-01','DL-VIS-02','DL-VIS-03','DL-VIS-05','DL-READ-01','DL-READ-02','DL-READ-03','DL-PERF-01','DL-QA-03','DL-QA-06','DL-QA-07'],
 'findings':['MA-VIS-006'],'files':[p.relative_to(root).as_posix() for p in family.rglob('*') if p.is_file()],
 'validation':[{'command':'Exact original and sibling source/reuse inventory with direct individual inspection','result':'PASS','evidence':'assets_src/imagegen/day1_playroom_sign_v2_20261001/PROFILE_AND_PROMPT.json; catalogD1N-0072/source4.5 retains scope. Original and two siblings directly inspected; no alternate clean same-bear source established.'},
 {'command':'Generated source identity/style and normalized native navigation fit','result':'PENDING','evidence':'No candidate generated or selected yet.'}],
 'acceptance_gaps':'Generation/source/native/action/owner/device/child acceptance remain separate. Original remains bound. No global quality pass, finding closure or release.'}
(root/'design/audit_impacts/day-one-playroom-sign-v2-20261001.json').write_text(json.dumps(impact,indent=2)+'\n',encoding='utf-8')
print('One named4.5 playroom sign border gap inventoried; exact prompt/source hashes saved; original and binding unchanged.')
