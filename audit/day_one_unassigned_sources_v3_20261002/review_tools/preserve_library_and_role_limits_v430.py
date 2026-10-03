from pathlib import Path
import datetime,hashlib,html,json,shutil
R=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
P=R/'assets_src/local_motion/nursery_connected_scrub_v4_20261002';S=R/'audit/day_one_unassigned_sources_v3_20261002';L=R/'audit/job_artwork_refinement_live'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
for suffix in ('png','json'):shutil.copyfile('C:/Users/Peter/Documents/mermaid-roshan-reef/tmp/BROWSER_LIBRARY_V429.'+suffix,P/('BROWSER_LIBRARY_V429.'+suffix))
proof=read(P/'BROWSER_LIBRARY_V429.json');assert '713 known source/cell/region priorities' in proof['summary'] and '377 source file reviews required' in proof['summary']
trace=read(S/'STATIC_CONSUMER_REFERENCES.json');roles={}
for file in trace['members']:
 for match in file['matches']:
  role=match['text'].split('"')[1]
  for id in match['source_ids']:roles.setdefault(id,[]).append(dict(script=file['script'],line=match['line'],literal_role=role))
write(S/'DECLARED_SOURCE_ROLE_LIMITS.json',dict(status='STATIC_ROLE_QUALIFICATION_ADDED',checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),roles=roles,qualification='First opinions evaluate complete source appearance named by its file; literal fallback roles can differ. Carrot wedge is referenced as Beak, pine as Triangle/tower, snowman as Ice, sun as Flame/gate_veil, sprout as Question, star as Glow/Spark/beacon, rainbow as home_ring and texture as CrystalPedestal/Diamond/crystal. These semantic substitutes are not verified played job bindings. Do not replace a bird beak with a leafy carrot, or regenerate non-job graphics as a claimed job repair. Confirm actual target semantics and use before any replacement.'))
rows=''.join('<tr><td>'+html.escape(id)+'</td><td>'+html.escape(', '.join(x['literal_role']+' ('+x['script']+':'+str(x['line'])+')' for x in members))+'</td></tr>' for id,members in sorted(roles.items()))
note='<section><h2>Source names and literal consumer roles are separate</h2><p>These first opinions concern the complete source appearance. The explicit fallback table roles below are not verified played job bindings. A source named carrot is used as a Beak, so replacing that role with a leafy carrot would be wrong. Confirm actual semantics and dynamic/shared use before any regeneration or binding.</p><table><thead><tr><th>Source ID</th><th>Literal table roles</th></tr></thead><tbody>'+rows+'</tbody></table><p><a href="DECLARED_SOURCE_ROLE_LIMITS.json">Exact role qualification</a></p></section>'
raw=(S/'index.html').read_text(encoding='utf-8');assert note not in raw;raw=raw.replace('</html>',note+'</html>');(S/'index.html').write_text(raw,encoding='utf-8',newline='\n')
shutil.copyfile(__file__,S/'review_tools'/Path(__file__).name)
for ip,packet in ((R/'design/audit_impacts/job-nursery-scrub-prompt-a4-20261002.json',P),(R/'design/audit_impacts/job-unassigned-source-eight-20261002.json',S)):
 d=read(ip);d['files']=sorted(set(d['files'])|{x.relative_to(R).as_posix() for x in packet.rglob('*') if x.is_file()});d['validation'].append(dict(command='Refreshed actual browser register and literal consumer-role qualification',result='PASS',evidence=(P/'BROWSER_LIBRARY_V429.json').relative_to(R).as_posix()+'; '+(S/'DECLARED_SOURCE_ROLE_LIMITS.json').relative_to(R).as_posix()));write(ip,d)
print('LIBRARY_PROOF_AND_ROLE_LIMITS_PRESERVED|713 priorities/377 source reviews remain|no false job use or semantic substitution')
