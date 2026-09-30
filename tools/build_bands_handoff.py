"""Build a review packet. Displays original scene art; never edits or animates it."""
from pathlib import Path
import hashlib, html, json, math, shutil
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'assets_src/cinematics/battle_of_bands_2026-09-20'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def txt(p,s):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(s.replace('\r\n','\n').encode('utf-8'))
def js(p,v): txt(p,json.dumps(v,indent=2)+'\n')
CONTROLS=[
 ('roshan_drums.png','candle.png','roshan raises her two sticks and looks to her bandmates','everyone is ready; the single candle stays on the supported cake'),
 ('roshan_drums.png',None,'roshan alternates two contacts on the upper tom heads with clear rebounds','both sticks rebound above their drumheads; she keeps a relaxed smile'),
 ('daddy_ukulele.png',None,'daddy gently strums his four-string ukulele and smiles toward roshan offscreen right','the ukulele stays securely held; his gaze rests on roshan'),
 ('eagle_bass.png',None,'baby eagle plucks the four-string bass with one wing while the other supports the neck','the bass stays secure with four strings connected to four posts and four keys'),
 ('king_guitar.png','prince_drums.png','the king leans into a theatrical lead-guitar flourish and open-mouth growl','the king returns upright with his guitar strapped; the candle has not moved'),
 ('roshan_drums.png',None,'roshan answers with two tom contacts and one light cymbal contact','the cymbal settles as she resumes her cheerful groove'),
 ('roshan_drums.png','daddy_ukulele.png','roshan cues daddy and baby eagle with a small nod; they answer on ukulele and bass','all three share the groove without leaving their places'),
 ('prince_drums.png',None,'the prince performs a two-stick fill around his many toms then taps a cymbal','both sticks rebound; the single kick drum and crowned-flame crest remain unchanged'),
 ('roshan_drums.png','eagle_bass.png','roshan keeps a gentle tom pulse while baby eagle answers with a bass pluck','roshan and baby eagle exchange a happy glance, still playing securely'),
 ('roshan_drums.png',None,'roshan lands a satisfying final tom contact then raises both sticks in delight','roshan is pleased with her successful phrase; the candle still belongs to her'),
 ('king_guitar.png','prince_drums.png','the king strums a final flourish as the prince lands a two-stick fill','their instruments settle; the king looks toward the offscreen candle'),
 ('king_guitar.png','candle.png',"the king's royal magic lifts the one lit pillar candle from the intact cake into his free palm","one candle rests in the king's palm; its former place on the cake is empty"),
 ('prince.png','king_guitar.png','the prince appeals with one empty open hand; the king turns away with the candle and the disappointed prince follows','king and prince leave frame together with the single candle; the guitar stays strapped'),
 ('roshan_drums.png','daddy_ukulele.png','daddy leans gently toward roshan; baby eagle moves a small step closer as she looks up','roshan has her friends beside her; instruments and earned cake remain safe')]
def build():
 sequence=json.loads((P/'SCENE_SEQUENCE.json').read_text(encoding='utf-8'));scenes=sequence['scenes']
 art=json.loads((P/'SCENE_ART_PROVENANCE.json').read_text(encoding='utf-8'))['frames']
 assert len(scenes)==len(art)==len(CONTROLS)==14
 assert all(abs(a['end']-b['start'])<1e-7 for a,b in zip(scenes,scenes[1:]))
 copies={'ART_PROVENANCE.json':'assets_src/imagegen/bands_20260920/PROVENANCE.json','SOURCE_ASSET_LICENSES.txt':'ASSET_LICENSES.md','runtime/prototype.png':'build/bands/prototype.png'}
 for n in ['roshan_drums','king_guitar','prince_drums','daddy_ukulele','eagle_bass','stage_platform']: copies['references/'+n+'.png']='assets/prototypes/bands/'+n+'.png'
 for dest,src in copies.items():
  (P/dest).parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/src,P/dest)
 cards=[];jobs=[];sections=[]
 readme=['# Battle of the Bands — Sky Lagoon review packet\n','**14 developed scene candidates · 19 short clip jobs · Iko Iko v89 (91 seconds) + 18-second story coda.**\n','[Start here](START_HERE.txt) · [Interactive board](SHOT_BOARD.html) · [Codex work order](CODEX_REFINEMENT.txt) · [Audio cues](AUDIO_CUE_SHEET.json) · [Manifest](ARCHIVE_MANIFEST.json) · [Publication receipt](REMOTE_VERIFICATION.json)\n','Roshan drums; Daddy Mermaid plays ukulele; Baby Eagle plays four-string/four-peg bass. Ember King leads on guitar; Ember Prince plays his elaborate **single-kick** kit with the trial crowned-flame emblem. The shared stage replaces playground equipment in the **middle Sky Lagoon meadow**, using the literal v5 panorama.\n','These are full-frame **scene-design candidates**, awaiting first-frame and continuity approval. Grok clips are motion/editorial reference only. Download the directory and open SHOT_BOARD.html to inspect timing with local song playback. GitHub renders the scene images below; it displays HTML as source.\n']
 for i,(s,f,c) in enumerate(zip(scenes,art,CONTROLS),1):
  assert sha(P/f['path'])==f['sha256']
  subject,prop,action,end=c;n=math.ceil((s['end']-s['start'])/8);duration=(s['end']-s['start'])/n;scene_jobs=[]
  for part in range(n):
   shot=s['id']+(chr(65+part) if n>1 else '');start=s['start']+part*duration;stop=s['end'] if part==n-1 else start+duration
   prompt=f'locked camera on the shared wood stage in sky lagoon from IMAGE_1.\n\n0.0-0.5s: continue naturally from the opening pose.\n0.5-{duration-.7:.3f}s: {action}.\n{duration-.7:.3f}-{duration:.3f}s: {end}.\n\nkeep the stage, mountains, shrubs and unaffected props fixed. preserve identity and instrument anatomy from IMAGE_2'+(' and the supporting reference IMAGE_3' if prop else '')+'. maintain visible floor contact. no cuts, hud, text, extra limbs, extra sticks, duplicate candle, new stage or costume drift. the prince has one kick drum; the bass has four strings and four tuning keys.\n'+f'end: {end}.\nSound: quiet contact foley only; original song added unchanged in edit, no generated singing or family voices.\n'
   folder=P/'shots'/shot;txt(folder/'PROMPT.txt',prompt)
   gap='Owner first-frame/continuity approval pending' if part==0 else 'Bind accepted preceding clip endpoint after it exists; never substitute a board'
   refs=[{'id':'IMAGE_1','role':'approved_clean_first_frame','path':f['path'] if part==0 else None,'sha256':f['sha256'] if part==0 else None,'candidate_scene_path':f['path'],'hud_present':False,'human_decision':'pending','blocking_gap':gap}]
   for number,name in enumerate([subject]+([prop] if prop else []),2):
    path='references/'+name;refs.append({'id':f'IMAGE_{number}','role':'subject_identity' if number==2 else 'object_or_material_identity','path':path,'sha256':sha(P/path),'hud_present':False,'human_decision':'pending shot binding review'})
   card={'schema':'imagine-shot-packet-v1','movie_id':'battle_of_bands','shot_id':shot,'scene_id':s['id'],'title':s['title'],'status':'DRAFT','template':'design/templates/IMAGINE_SHOT_CARD_V1.md','duration_seconds':duration,'aspect_ratio':'16:9','delivery_size':[1280,720],'mode':'image_to_video','output_disposition':'motion_reference_only','bound_references':refs,'camera':{'verb':'locked','move_count':0},'must_move':[action],'must_not_move':['stage geometry','literal lagoon geography','unaffected props'],'end_state':end,'negative_constraints':['no cuts','no HUD','no extra limbs','no instrument topology drift','no duplicate candle'],'prompt_path':f'shots/{shot}/PROMPT.txt','prompt_sha256':sha(folder/'PROMPT.txt'),'editorial_start_seconds':start,'editorial_end_seconds':stop,'recording_start_seconds':start if start<91 else None,'recording_end_seconds':min(stop,91) if start<91 else None,'continuation_of':scene_jobs[-1] if part else None,'timing_note':'One continuous clip per job. Trim excess handles only. Never retime song or repeat a frame to fill action. Later parts need an accepted previous endpoint. 91.000 rounds the 90.9998866-second master.','non_pixel_references':[{'path':'SHOT_BOARD.html','used_as_pixel_reference':False},{'path':'runtime/prototype.png','used_as_pixel_reference':False}],'ARCHIVE_COMPLETE':False,'GENERATION_READY':False,'DELIVERY_ACCEPTED':False,'blocking_findings':[gap,'Human identity/contact/topology review pending']}
   path=f'shots/{shot}/SHOT_PACKET.json';js(P/path,card);cards.append(path);jobs.append(card);scene_jobs.append(shot)
  links=' · '.join(f'<a href="shots/{j}/SHOT_PACKET.json">{j}</a> / <a href="shots/{j}/PROMPT.txt">prompt</a>' for j in scene_jobs)
  sections.append(f'<section data-start="{s["start"]}" data-end="{s["end"]}"><h2>{s["id"]} · {html.escape(s["title"])}</h2><p>{s["start"]:.3f}–{s["end"]:.3f}s</p><a href="{f["path"]}"><img loading="lazy" src="{f["path"]}" alt="{html.escape(s["title"])} candidate"></a><p>{html.escape(action)}.</p><p><b>End:</b> {html.escape(end)}.</p><button data-seek="{s["start"]}">Inspect this beat</button><p>{links}</p><small>Candidate · owner approval pending</small></section>')
  readme += [f'## {s["id"]} — {s["title"]}\n',f'**{s["start"]:.3f}–{s["end"]:.3f}s.** {action.capitalize()}. End: {end}.\n',f'![{s["id"]} scene candidate]({f["path"]})\n',' · '.join(f'[{j} card](shots/{j}/SHOT_PACKET.json) / [prompt](shots/{j}/PROMPT.txt)' for j in scene_jobs)+'\n']
 assert len(jobs)==19 and abs(sum(j['duration_seconds'] for j in jobs)-109)<1e-7
 readme+=['## Playable prototype\n','![Godot Mobile capture — never generator input](runtime/prototype.png)\n','Run scenes/battle_of_bands_prototype.tscn in Godot 4.7.2. Twelve forgiving intentional hits plus completion of the recording unlock the story. Exact objective voice, contact animation, target-device/child review and production chapter integration remain open.\n','**Archive:** consult REMOTE_VERIFICATION.json for exact published bytes. **Generation readiness: blocked** by first-frame/continuity/topology approval and continuation endpoint bindings. **Delivery acceptance: false.** Full-frame cinematic/human/device gates still apply.\n']
 txt(P/'README.md','\n'.join(readme))
 template=(ROOT/'tools/bands_board_template.html').read_text(encoding='utf-8');txt(P/'SHOT_BOARD.html',template.replace('<!-- SCENES -->',''.join(sections)))
 js(P/'IMAGINE_HANDOFF.json',{'schema':'imagine-handoff-v1','movie_id':'battle_of_bands','archive_status':'incomplete','archive_note':'Content candidate; completion evidence is in the subsequent immutable remote receipt.','generation_status':'blocked','delivery_status':'not_accepted','shot_packets':[],'draft_shot_packets':cards,'shot_board':'SHOT_BOARD.html','scene_count':14,'job_count':19,'blocking_findings':['Owner first-frame approval and continuity/topology review pending','Five continuation jobs need accepted predecessor endpoints','Remote receipt required for archive completion']})
 js(P/'EDIT_DECISION_LIST.json',{'recording':'audio/iko_iko_v89.ogg','duration_seconds':109,'music_seconds':[0,91],'coda_seconds':[91,109],'no_retiming':True,'jobs':[{k:j[k] for k in ['shot_id','scene_id','editorial_start_seconds','editorial_end_seconds','duration_seconds','continuation_of']} for j in jobs]})
 for j in jobs:
  assert 2<=j['duration_seconds']<=8 and 2<=len(j['bound_references'])<=4 and not j['GENERATION_READY']
  for ref in j['bound_references']:
   if ref['path']: assert sha(P/ref['path'])==ref['sha256']
 for path in P.rglob('*'):
  if path.is_file() and path.suffix in {'.json','.txt','.md','.html'}: path.write_bytes(path.read_bytes().replace(b'\r\n',b'\n'))
 old='assets_src/cinematics/chapter2_lawn_scale_v2_2026-09-06'
 sources={**copies, 'references/roshan_popstar.png':'assets/opera/worlds/actors/roshan_popstar.png','references/roshan_costume_poses.png':'assets/opera/worlds/actors/animation/roshan_popstar_sheet_a.png','references/king.png':old+'/characters/ember_king_v4.png','references/prince.png':old+'/characters/ember_prince_identity.png','references/cake.png':old+'/references/cake.png','references/candle.png':old+'/references/candle_lit.png','references/daddy.webp':'assets/characters/friends/daddy.webp','references/baby_eagle.png':'assets/book/baby_eagle.png','references/sky_lagoon_middle_literal.png':'assets_src/sky_lagoon/masters/sky_lagoon_panorama_master_v5_hd_3x1.png','audio/iko_iko_v89.ogg':'assets/prototypes/bands/iko_iko_v89.ogg'}
 sources['audio/iko_iko_v89.mp3']='https://github.com/Ebonyks/mermaid-roshan-reef/releases/download/music-iko-iko-v89-20260920/iko-iko-v89.mp3'
 files=[]
 for path in sorted(P.rglob('*'),key=lambda q:q.relative_to(P).as_posix()):
  if not path.is_file() or path.name in {'ARCHIVE_MANIFEST.json','REMOTE_VERIFICATION.json'}: continue
  rel=path.relative_to(P).as_posix();role='planning_and_audit'
  for prefix,label in [('frames/','unapproved_scene_candidate_or_prompt'),('references/','identity_prop_or_literal_location'),('runtime/','runtime_seam_never_generation_pixels'),('generation_inputs/','generation_history_only_not_approved_binding'),('audio/','published_song_derivative_for_local_edit'),('shots/','draft_single_clip_job')]:
   if rel.startswith(prefix): role=label
  entry={'path':rel,'sha256':sha(path),'source_path':sources.get(rel,path.relative_to(ROOT).as_posix()),'role':role,'license_provenance':'See SOURCE_ASSET_LICENSES.txt, ART_PROVENANCE.json, SCENE_ART_PROVENANCE.json and AUDIO_CUE_SHEET.json; copied sources retain original terms. No new music-composition rights asserted.','modification_status':'literal crop and uniform 0.5 scale; see BACKGROUND_PROVENANCE.json' if rel=='references/sky_lagoon_middle_literal.png' else ('byte-identical source copy' if rel in sources and path.suffix not in {'.json','.txt'} else 'See individual provenance; text normalized to UTF-8 LF'),'dimensions':None}
  if path.suffix.lower() in {'.png','.jpg','.webp'}:
   with Image.open(path) as im: entry['dimensions']=list(im.size)
  files.append(entry)
 payload=''.join(f"{e['sha256']}  {e['path']}\n" for e in files).encode()
 js(P/'ARCHIVE_MANIFEST.json',{'schema':'bands-review-archive-v1','request_id':'bands-middle-meadow-r2-20260930','repository':'Ebonyks/mermaid-roshan-reef','branch':'codex/battle-of-bands-20260920','recipient_access':'anonymous public HTTPS; verify exact revision in remote receipt','payload_algorithm':'sha256 of case-sensitive path-sorted sha256 + two spaces + path + LF; excludes manifest and receipt','packet_payload_sha256':hashlib.sha256(payload).hexdigest(),'ARCHIVE_COMPLETE':False,'GENERATION_READY':False,'DELIVERY_ACCEPTED':False,'files':files})
 print(f'BANDS PACKET PASS: {len(files)} files, 14 candidates, 19 draft jobs, contiguous 0..109s coverage')
if __name__=='__main__': build()
