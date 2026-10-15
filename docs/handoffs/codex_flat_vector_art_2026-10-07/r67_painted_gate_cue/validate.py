from pathlib import Path
import json,hashlib,subprocess,sys
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[3];O=P.parent/'r66_display_entry_context';B='858436a8697b06ba1dc8cfa012d5879a218afc20';D='5120b6d59885dd057937aaf284e73681d8eac9f5'
def rd(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(['git',*a],cwd=R)
summary=rd(P/'SUMMARY.json');assert summary['native_cases']==4 and summary['passing_checks']==54 and summary['native_frames']==20 and summary['accepted_removed']==0 and summary['all_game_artwork_total']is None and summary['known_legacy_policy_status']=='FAIL_LEGACY_SOURCE_CONTRACT_UNFIXED'
index=rd(P/'CAPTURE_INDEX.json');assert len(index['frames'])==20 and len({x['path']for x in index['frames']})==20
for x in index['frames']:
 b=(R/x['path']).read_bytes();im=Image.open(R/x['path']).convert('RGBA');assert sha(b)==x['sha256']and list(im.size)==x['size']and sha(im.tobytes())==x['decoded_rgba_sha256']
for case in summary['cases']:
 Q=P/'native'/case['case'];m=rd(Q/'capture_manifest.json');result=rd(Q/'RESULT.json');launch=rd(Q/'LAUNCH.json');assert not m['errors']and all(x['pass']for x in m['checks']);assert result['exit_code']==0 and not result['script_or_shader_errors']and result['sidecars_exact']and not result['source_byte_changes']and result['normal_before']==result['normal_after']and result['fixture_dependencies_unchanged'];assert len(m['normal_before'])==11
 for name,digest in launch['fixture_dependencies'].items():assert sha((P/name).read_bytes())==digest and sha((Q/name).read_bytes())==digest
 assert m['seed']['flat_vector_private_unknown']['token']=='R67_PRIVATE_ONLY'and m['seed']['day_one_active']is True
 ids=[x['snapshot']['gate'].get('glow_id')for x in m['states'][:4]];anchors=[x['snapshot']['gate'].get('anchor_id')for x in m['states'][:4]];assert len(set(ids))==1 and len(set(anchors))==1 and m['states'][4]['snapshot']['gate']=={}
 for x in m['states']:assert x['snapshot']['quality']=='speedy'and x['snapshot']['time_scale']==1.0
for n in ['per_piece.json','scene_coverage.json','tally.json','source_scopes.json','glyph_inventory.json']:
 path=(P.parent/n).relative_to(R).as_posix();assert (R/path).read_bytes()==git('show',B+':'+path)
for n in ['CURRENT_KNOWN_ROLE_UNION.json','CURRENT_PARTIAL_CONTEXT_UNION.json','CURRENT_CATALOGUE_CONTEXT_UNION.json']:assert (P/n).read_bytes()==(O/n).read_bytes()
for n in ['per_piece.json','scene_coverage.json','tally.json','CONGRUENCY_BACKLOG.json']:
 old=rd(O/n);new=rd(P/n)
 for k,v in old.items():
  if k not in ['revision','phase','publication']:assert new[k]==v,(n,k)
 assert new['painted_gate_reuse']['accepted_removed']==0 and new['painted_gate_reuse']['known_roles']==241
review=rd(P/'REVIEW.json');assert review['view_count']==9 and len(review['axes'])==10 and review['status']=='PARTIAL_REUSE_FIT_NEW_USE_ACCEPTANCE_OPEN'
for x in review['viewed_native_frames']:assert sha((P/x['path']).read_bytes())==x['sha256']
for x in rd(P/'DELIVERY_SOURCE_REFERENCES.json')['files']:
 b=git('show',x['revision']+':'+x['path']);assert sha(b)==x['sha256']and len(b)==x['bytes']
assert rd(P/'FIXTURE_SYNTAX_GATES.json')['status']=='PASS_BEFORE_NATIVE';assert rd(P/'FIXTURE_SYNTAX_ATTEMPT1.json')['status']=='FAIL'
# Exact unchanged tick body apart from the documented castle RGB assignment.
lineage=rd(P/'SOURCE_LINEAGE.json');body=next(x['body']for x in lineage['original_methods']if x['method']=='_tick_target_affordances');candidate=(P/'painted_gate.gd').read_text(encoding='utf-8');tick=candidate[candidate.index('func _tick_target_affordances('):];patch='\t\tif str(target.get("id", "")) == "castle_gate":\n\t\t\t# Preserve source alpha/pulse, retain authored gold/violet RGB.\n\t\t\ttint.r = 1.0\n\t\t\ttint.g = 1.0\n\t\t\ttint.b = 1.0\n';assert tick.replace(patch,'')==body
assert 'No flat fallback' in candidate and 'CUE_MASTER_HEIGHT: float = 196.0'in candidate
cur=rd(P.parent/'CURRENT.json');assert cur['current_tally']=='r67_painted_gate_cue/tally.json'and cur['mission_complete']is False
print('R67 evidence consistency PASS;4 cases/54 assertions/20 raw frames,9 views; frozen5/history/unions preserved. Candidate acceptance and missing-art/caller gaps remain open.')
