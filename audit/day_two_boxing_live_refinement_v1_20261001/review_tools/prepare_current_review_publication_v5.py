from pathlib import Path
import re

r = Path(__file__).resolve().parents[1]
families = [('day-one-pool-live-refinement-v2-20261001','audit/day_one_pool_live_refinement_v2_20261001'),('day-one-playroom-sign-v2-20261001','assets_src/imagegen/day1_playroom_sign_v2_20261001'),('day-two-boxing-puff-reuse-v1-20261001','audit/day_two_boxing_puff_reuse_v1_20261001'),('day-two-boxing-single-gloves-v1-20261001','assets_src/imagegen/day2_boxing_single_gloves_v1_20261001'),('day-two-boxing-live-refinement-v1-20261001','audit/day_two_boxing_live_refinement_v1_20261001')]
s = (r/'tmp/seal_current_job_art_review.py').read_text()
a = s.index('families='); b = s.index('\nmanifest_paths=',a)
s = s[:a]+'families='+repr(families)+s[b:]
s = s.replace("=='04a362c732840b091cafe7731399789eb735789f'", "=='5b8bfb989ca8012924115d45901252808edb9b62'")
s = s.replace("assert subprocess.check_output(['git','rev-parse','MERGE_HEAD'],cwd=root,text=True).strip()=='c5e98477efe4fe3c36d6bffe68818d84c2d08325'", "assert subprocess.run(['git','rev-parse','--verify','MERGE_HEAD'],cwd=root,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode != 0")
s = s.replace('audit/job_art_current_source_reconciliation_20261001/SOURCE_BEFORE_CI.json','audit/day_one_pool_live_refinement_v2_20261001/full_ci_current_retry_v3/SOURCE_BEFORE.json')
s = s.replace('audit/job_art_current_source_reconciliation_20261001/full_ci_retry/RECEIPT.json','audit/day_one_pool_live_refinement_v2_20261001/full_ci_current_retry_v3/RECEIPT.json')
s = s.replace("=='PASS_UNMODIFIED_FULL_RETRY'", "=='PASS_UNMODIFIED_CURRENT_FULL_SUITE'")
s = s.replace("assert len(retry['probe_results'])==82", "assert retry['source_unchanged'] and len(retry['source_checks'])==325\nassert len(retry['probe_results'])==82")
s = s.replace("'baseline':'04a362c732840b091cafe7731399789eb735789f'", "'baseline':'5b8bfb989ca8012924115d45901252808edb9b62'")
s = s.replace('root=Path(__file__).resolve().parents[1]', "root=next(p for p in Path(__file__).resolve().parents if (p/'project.godot').is_file())")
scope = 'Joint reversible review: live pool six refined props with complete ordered native action evidence and named body/grip priorities; unbound matte teddy sign; historical clean-puff and separate-glove source/static comparisons; live painted left/right boxing gloves and exact clean puff, all1402 action frames and16 current edge views reviewed. Failed generations, earlier native limits and red full-suite attempts remain inspectable. This does not establish exhaustive all-job acceptance.'
acceptance = 'OWNER_REVIEW_DRAFT. Selected individual art has scoped4.6 drafting opinions. Pool full actions4.2; guard/imp sequences4.2; belt sequence4.0. Counter4.0, connected imp acting3.8, belt contact/return3.8 and shared marked puff2.5 remain priorities. All-jobs discovery/refinement, ordinary played traversal, phone/child/owner approval and comprehensive final report remain unfinished. No finding closure, integration or release.'
s = re.sub(r"'scope':'Joint reversible source review:.*?',\s*'acceptance':'.*?',\s*'files':payload", "'scope':"+repr(scope)+",'acceptance':"+repr(acceptance)+",'files':payload", s, count=1)
a = s.index("'machine_evidence':{"); b = s.index(",'delivery_instructions':",a)
s = s[:a]+"'machine_evidence':{'full_retry':'audit/day_one_pool_live_refinement_v2_20261001/full_ci_current_retry_v3/RECEIPT.json','unchanged_production_sources':325,'trusted_probe_processes':82,'fresh_document_contract':'audit/day_two_boxing_live_refinement_v1_20261001/current_document_gates_v5/RECEIPT.json','http_receipt':'audit/day_one_pool_live_refinement_v2_20261001/delivery_http_v4/RECEIPT.json'}"+s[b:]
s = s.replace('|299 tested sources unchanged','|325 tested sources unchanged')
s = s.replace("'delivery_instructions':'Read individual written opinions beside native artwork and inspect retained failed attempts. Source, static fit, observed contact/transfer and complete played action are separate claims. Buffered actual timestamps retain GPU capture limits. Fresh skimmer used zero image uploads after rejection of an unexecuted reference-upload proposal. Never treat source scores or green probes as device/owner/cinematic acceptance.'", "'delivery_instructions':'Read each individual opinion beside its artwork, inspect ordered frames and failed attempts, and keep source, mounted appearance, contact, complete sequence and full played route distinct. Scores are drafting evaluations. Preserve protected originals. Approved-source reuse and complete-source new generations retain provenance. Green tests do not establish device, child, owner or cinematic acceptance.'")
s = s.replace("ours=set()", "gates=json.loads((root/'audit/day_two_boxing_live_refinement_v1_20261001/current_document_gates_v5/RECEIPT.json').read_text())\nassert gates['status']=='PASS'\nhttp=json.loads((root/'audit/day_one_pool_live_refinement_v2_20261001/delivery_http_v4/RECEIPT.json').read_text())\nassert http['status']=='PASS' and not http['failures'] and len(http['video_byte_ranges'])==18\nours=set()",1)
s = s.replace("for _,prefix in families:\n    for p in (root/prefix).rglob('*.json'):visit(json.loads(p.read_text(encoding='utf-8-sig')))", "for _,prefix in families:\n    for p in (root/prefix).rglob('*.json'):visit(json.loads(p.read_text(encoding='utf-8-sig')))\nvisit(json.loads((root/'audit/job_artwork_refinement_live/ALL_ITEMS.json').read_text(encoding='utf-8')))")
assert "'scope':"+repr(scope) in s and 'MERGE_HEAD' in s and '325 tested' in s
compile(s,'seal_current_job_art_review_v5.py','exec')
(r/'tmp/seal_current_job_art_review_v5.py').write_text(s,encoding='utf-8')
remote=(r/'tmp/verify_current_job_art_remote.py').read_text()
remote=remote.replace('root=Path(__file__).resolve().parents[1]', "root=next(p for p in Path(__file__).resolve().parents if (p/'project.godot').is_file())")
a=remote.index('families=');b=remote.index('\nparser=',a)
remote=remote[:a]+'families='+repr([p for _,p in families])+remote[b:]
compile(remote,'verify_current_job_art_remote_v5.py','exec')
(r/'tmp/verify_current_job_art_remote_v5.py').write_text(remote,encoding='utf-8')
print('Prepared guarded publication helpers for five NEW review families; nothing sealed, staged, committed or pushed.')
