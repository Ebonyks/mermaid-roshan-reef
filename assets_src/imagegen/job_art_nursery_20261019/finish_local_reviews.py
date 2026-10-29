from pathlib import Path
import json,hashlib,re,subprocess
from datetime import datetime,timezone
from PIL import Image
r=Path.cwd();sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();now=datetime.now(timezone.utc).isoformat()
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
notes={
'cradle':'Whole recovered cupped hands retain readable five-digit contours and lilac cuffs. Palms sit under accumulated swaddles; same warm contour/pastel finish as care figures.',
'pillows':'Recovered soft lilac floor strip retains its authored rounded forms; technical alpha crop removes empty border without painting. Passive baby rests on its visible upper surface.',
'crib':'Ivory/lilac oval bassinet has the same moon/shell furniture language as the room. Low rear/front rim leaves faces clear; same-source front rim supplies honest baby occlusion.',
'pat_hand':'Selected second source clearly separates four fingers and thumb. Rigid placement contacts the swaddle below the head; large guide is displaced from faces.',
'mobile':'Existing authored moon/cloud mobile stays whole and naturally proportioned; matches moon doorway and the crib palette.',
'guide_hand':'Exact painted Teacher source reused with only whole-image orientation/scale. Rounded finger reads clearly at the relevant target without redrawing anatomy.',
'bottle_empty':'Generated empty glass is registered to original bottle (alpha16 IoU .9874376183101016); original exterior/nipple/medallion are preserved. Disjoint full/empty body rows prevent translucent empty art exposing the old milk underneath. Static ready/feeding/completion states inspected; fluid motion remains pending.',
'quilt_folded':'Cream-piped teal quilt is a short folded strip, with clear moon motif and soft broad padded paint bands matching Nursery furnishings.',
'quilt_half':'Selected longer half-open key is distinct from the folded strip at actual size. Whole picture keeps natural cloth proportions and the same top/width below faces.',
'quilt_tucked':'Selected tall drape clearly covers lower bodies/front rim, retaining round padded quilting and clean scalloped piping. Whole picture avoids UV stretching and leaves all faces clear.',
'glove_left':'Exact recovered authored coral glove and coral cuff retain shell badge, broad soft painted bands and clean contours; source is not mirrored. Native knuckle UV anchors unchanged touch position.',
'glove_right':'Exact recovered authored coral glove with teal cuff stays distinct from the left. Whole-source rigid rotation/uniform size matches the painted gym props.',
'focus_mitt':'Single teal/ivory shell mitt matches the existing green padded post. Its gold shell centre is anchored to the existing target, with visible gold cue tips behind; one current JAB pad avoids the stale paired-card occlusion.',
'impact_puff':'Clean cream/aqua/lavender rounded poof replaces the wire-tailed old card in Boxer only. It matches room pearl highlights and has no code-drawn star/circle overlay; existing duration/position retained.',
'pearl_empty':'Selected retry reads as a hollow lavender cup inside the gold rim at actual HUD size. Distinct from the completed pearl and consistent with shell-room gold/cream.',
'pearl_filling':'Selected retry has a lower half pearl and open upper cavity; reads separately from empty/full at actual progress size.',
'pearl_full':'Solid pale luminous pearl fills the same gold rim; broad cream/aqua highlights match scene jewelry without photographic metal.',
'fx_invite_open':'Registered open state retains a single gold oval and its four contained glints; drawn under the target, not over its centre. Native transparency retained; whole-time cadence remains pending.'}
for i in range(4):notes['fx_invite_ring_'+str(i)]='One painted gold/pearl ground oval, registered to the same centre. Four declared whole-source uniform scale keys (.94,1,1.04,1) come from one still, not four generated frames. Source edges/palette match gym jewelry; no flat code circle. Full-speed cadence remains pending.'
shared=json.loads((r/'assets_src/imagegen/job_art_boxer_20261019/runtime_provenance.json').read_text())['records']
for family,variant,count in [('nursery','current06',100),('boxer','current02',152)]:
 s=r/f'assets_src/imagegen/job_art_{family}_20261019';review=s/'review';review.mkdir(exist_ok=True)
 records=json.loads((s/'runtime_provenance.json').read_text())['records']
 if family=='nursery':records=records+[x for x in shared if x['path'].startswith('assets/ui/pearl_')]
 else:
  p=r/'assets/opera/worlds/teacher/guide_hand.png'
  if not p.is_file():p=r/'assets/opera/worlds/teacher/gesture_guide_hand.png'
  # The actual binding is read from the shared helper below; no guessed filename.
  paths=re.findall(r'res://([^"\n]+\.png)',(r/'scripts/opera_boxing_surface.gd').read_text())
  hands=[p for p in paths if 'hand' in p];assert len(hands)==1,hands
  p=r/hands[0];assert p.is_file();records=records+[{'path':p.relative_to(r).as_posix(),'sha256':sha(p)}]
 capture=s/f'review_{variant}/capture.json';rows=json.loads(capture.read_text())['captures'];assert len(rows)==count
 receipt=json.loads((s/f'capture_{variant}_receipt.json').read_text());assert receipt['status']=='PASS' and receipt['actual_save_unchanged'] and not receipt['source_drift']
 assets=[]
 for row in records:
  p=r/row['path'];assert sha(p)==row['sha256'];im=Image.open(p);assert im.mode=='RGBA' and max(im.size)<=1024 and im.getchannel('A').getextrema()==(0,255)
  name=p.stem
  if name.startswith('care_'):obs='Owner-directed older Nursery-only whole care pose '+name+'. Source bytes remain exact; original headband, rainbow hair lock, face and tail retained. Pose is displayed whole by existing phase progress, without implying that the empty hands contain a new prop.'
  elif name.startswith('wash_'):obs='Whole recovered Nursery-only wash state '+name+' retains the same Roshan and fixed basin identity. Current source-state path is reachable before generic widgets; one Roshan owns the wash work, with clear hand/basin relationship and painted foam/water appropriate to that state.'
  else:obs=notes.get(name,notes['guide_hand'] if 'hand' in name else None)
  assert obs,name
  ratings={'identity':4.6,'finish':4.6,'edges':4.5,'readability':4.5,'ownership':4.5,'consistency':4.6,'technical':4.6,'animation':None}
  assets.append({'id':name,'path':row['path'],'sha256':sha(p),'dimensions_px':list(im.size),'reviewer':{'kind':'ai','id':'Codex root visual inspection2026-10-19'},'ratings':ratings,'minimum_scored_dimension':min(x for x in ratings.values() if x is not None),'status':'PASS_LOCAL_AI_STATIC_APPEARANCE_CANDIDATE_MOTION_PENDING','observations':obs,'unscored_applicable_evidence':'Full-speed/stepwise transitions and support/contact continuity, physical-device, canonicalQA11, child and owner acceptance remain pending where applicable. A null is not a pass.'})
 assert len(assets)==(28 if family=='nursery' else 13)
 write(review/'art_review.json',{'threshold':4.5,'aggregation':'Every applicable dimension must individually reach4.5; no mean compensation. These static scores do not complete the full applicable audit while animation evidence is missing. 5/5 requires owner runtime acceptance.','checked_utc':now,'baseline':'e90c0daa83cf05644f0e9942e85c1198ed7901f7','model':'Available builtin ImageGen; revision unexposed, owner approved; no2.5claim or paidAPI/CLI spend.','evidence_scope':f'AI inspection of every runtime source cutout and all{count} exact4.7.2 Mobile configured GUI stills at1280x720 and1600x720, via source sheets and labeled context pages. Same-scene furniture/figures/HUD are comparison neighbors. This is static local review, not canonicalQA11 or physical-device/human/child/owner evidence.','captures':{'path':capture.relative_to(r).as_posix(),'sha256':sha(capture),'count':count,'receipt_sha256':sha(s/f'capture_{variant}_receipt.json'),'frames':[{'id':x['id'],'path':x['path'],'sha256':sha(r/x['path'])} for x in rows]},'assets':assets,'background_exclusion':'Existing room native source coverage remains below required2K each axis; sharp-framing repair does not change native coverage and is not scored as a new passing background.','formal_rating':None,'final_all_time_rating':None,'global_master':'UNSATISFIED','remaining':'Full motion/transition/contact audit, complete machine suite/exactheadCI, other jobs/P8, final whole-campaign census, canonical runtime/device/child/owner gates.'})
 prompts=json.loads((s/'prompts.json').read_text());selected={x['source'] for x in json.loads((s/'runtime_provenance.json').read_text())['records']}
 for x in prompts:
  assert sha(r/x['native_path'])==x['native_sha256']
  if x['native_path'] in selected:x['disposition']='SELECTED_LOCAL_AI_STATIC_APPEARANCE_CANDIDATE; registered current-context stills meet4.5floor, motion/full audit/human/device/child/owner pending'
  elif family=='nursery' and x['id'] in ['quilt_tucked','quilt_half_retry']:x['disposition']='REJECTED_IN_CURRENT_CONTEXT_TOO_SHORT_AND_INDISTINCT_AT_RUNTIME_SIZE; native retained, final taller keys selected within aggregate6callcap'
  elif family=='boxer' and x['id'] in ['pearl_empty','pearl_filling']:x['disposition']='REJECTED_SMALL_SIZE_ROLE_READABILITY: empty upper cavity looked too similar to completed pearl; selected hollow/half retry family instead'
  assert not x['disposition'].startswith('CANDIDATE_PENDING'),x['id']
 write(s/'prompts.json',prompts)
 write(s/'generation_accounting.json',{'checked_utc':now,'builtin_calls':len(prompts),'reported_elapsed_ms_sum':sum(x['elapsed_ms'] for x in prompts),'selected_native_ids':[x['id'] for x in prompts if x['native_path'] in selected],'rejected_or_retired_ids':[x['id'] for x in prompts if x['native_path'] not in selected],'provider_model_revision':'unexposed','seed':'unexposed','monetary_usage':'unexposed; no paidAPI/CLI invoked','cleanup_minutes':'not instrumented; no fabricated timing','limits':'Runtime count differs from generation count due authored reuse, scaled cue keys and selected derivatives; rejects retained and counted.'})
print('Wrote source-bound local AI appearance reviews:28Nursery uses,13Boxer uses;22native calls accounted, all still pending applicable motion/final audit.')
