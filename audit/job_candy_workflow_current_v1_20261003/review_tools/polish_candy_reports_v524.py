from pathlib import Path
import json,re,shutil
b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
c=b/'audit/job_candy_workflow_current_v1_20261003';l=b/'audit/job_artwork_refinement_live'
p=l/'all_items.html';t=p.read_text(encoding='utf-8')
replacements={
 'refresh_current_job_review_v35.py':'refresh_current_job_review_v44.py',
 'Current Nursery washing: every state and complete action':'Earlier Nursery washing: current mounted claims withheld',
 'Current illustrated review and supported geode evidence':'Earlier illustrated review and supported geode evidence',
 'Current Nursery review covers every captured frame;':'The dated Nursery review covers every captured frame; current mounted claims require a refreshed capture after the shared station source changed;',
 'V41 retains45 current Geologist opinions/38 inclusive priorities':'V41 recorded 45 Geologist opinions/38 inclusive priorities, now historical after the shared station source changed',
 'Complete current fossil and panning review: every884 frame,58 selected canvases and22 individual opinions':'Earlier complete fossil and panning review: all 884 frames,58 canvases and22 opinions',
 'All783 production sources unchanged.':'Those captures preceded the shared station repair; their current mounted claims are withheld.',
 'All8 connected sources':'All10 connected sources',
 'missing bridgeA8 source4.1 rejected.':'bridges A8/A9/A10 score 4.1/4.1/4.2 and remain rejected.',
 'Current game and Geologist opinions unchanged.':'The dated current-game opinions are now historical after the shared source changed.'
}
for a,z in replacements.items():t=t.replace(a,z)
p.write_text(t,encoding='utf-8')
for p in [c/'index.html',b/'audit/job_candy_wrap_contact_runtime_v1_20261003/index.html',b/'assets_src/imagegen/candy_wrap_contact_v1_20261003/index.html',b/'assets_src/imagegen/candy_wrap_states_v1_20261003/index.html',l/'index.html',l/'all_items.html']:
 t=p.read_text(encoding='utf-8').replace('All8 source attempts','All10 source attempts')
 def img(m):
  attrs=m.group(1)
  if re.search(r'\balt\s*=',attrs):return m.group(0)
  src=re.search(r'\bsrc="([^"]+)"',attrs)
  if not src:return m.group(0)
  label='Artwork evidence: '+src.group(1).replace('_',' ')
  return '<img alt="'+label+'"'+attrs+'>'
 t=re.sub(r'<img\b([^>]*)>',img,t)
 # Exact prompts, JSON/state pre blocks, script and style remain verbatim.
 chunks=re.split(r'(<(?:script|style|pre|code)\b[^>]*>.*?</(?:script|style|pre|code)>)',t,flags=re.S|re.I)
 for i in range(0,len(chunks),2):
  def words(m):
   z=m.group(1)
   if re.search(r'[a-f0-9]{64}',z):return m.group(0)
   z=re.sub(r'\b(all|All|every|Every|native|whole|source|action|Attempt|attempt|production|below|to|at|with|from|exact|current|Current|static|endpoints|grips|contact|states|phase|frame|canvases|views|boards|details|opinions|registry|has|remains|score|scores)(?=\d)',r'\1 ',z)
   return '>'+z+'<'
  chunks[i]=re.sub(r'>([^<>]*)<',words,chunks[i])
 p.write_text(''.join(chunks),encoding='utf-8')
shutil.copyfile(__file__,c/'review_tools/polish_candy_reports_v524.py')
p=b/'design/audit_impacts/job-candy-workflow-current-20261003.json';d=json.loads(p.read_text(encoding='utf-8'));d['files']=sorted(set(d['files'])|{'audit/job_candy_workflow_current_v1_20261003/review_tools/polish_candy_reports_v524.py'});p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print('Human report labels and image alternatives updated; exact source opinions, prompts, raw captures and scores unchanged.')
