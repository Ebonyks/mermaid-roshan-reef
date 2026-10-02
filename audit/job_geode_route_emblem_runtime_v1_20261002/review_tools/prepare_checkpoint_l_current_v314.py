from pathlib import Path
import json, shutil
r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
root=Path('C:/Users/Peter/Documents/mermaid-roshan-reef')
g=r/'audit/job_geode_route_emblem_runtime_v1_20261002'
w=r/'audit/job_wash_root_remaining_sequences_v1_20261002'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
for name in ['wash_nursery_native_browser_v313.png','wash_remaining_report_v313.png','wash_remaining_browser_qa_v313.json']:
 shutil.copyfile(root/'tmp'/name,w/name)
shutil.copyfile(root/'tmp/current_review_landing_v313.png',g/'current_review_landing_v313.png')
shutil.copyfile(__file__,g/'review_tools'/Path(__file__).name)

s=(g/'review_tools/seal_geology_checkpoint_l_v296.py').read_text(encoding='utf-8')
s=s.replace('geology_checkpoint_l_seal_v296','geology_checkpoint_l_seal_v315')
s=s.replace("full_ci_v1/RECEIPT.json","full_ci_v2/RECEIPT.json").replace('==372','==373')
s=s.replace("['parserv3','inferencev3','importartv1','contractv2','capture1280v1','capture1600v1','authorityv3','developmentv3','audit2dv1']","['parserv4','inferencev4','importartv2','contractv3','capture1280v2','capture1600v2','authorityv3','developmentv3','audit2dv1']")
s=s.replace("'job-wash-root-doctor-sequence-review-20261002.json']","'job-wash-root-doctor-sequence-review-20261002.json','job-wash-root-remaining-sequences-review-20261002.json']")
start=s.index("'qualification':'Additive reversible current painted-geode")
end=s.index("'}\nrefs=",start)
qualification=('Reversible painted geode opens to two stone halves with cyan/violet crystals rooted inside. Library50px and invitation142px are 4.5 provisional, existing developer80px4.6, celebration artwork4.6 but unsupported placement4.2/composition3.3. Same source atlas pixels; three production script bindings and two AtlasTexture metadata resources share the identical painting/crop. Function bodies, input, mechanics, saves and rewards preserved. All58 current stills/317 consecutive frames/27 motion boards/10 still boards/eight native details/23 current individual opinions directly reviewed against373 frozen source files. First full suite1 failed81/82 because the crest path violated the unchanged probe contract; raw failure preserved. Corrected suite2 passes82/82 with373 source files unchanged and no relaxed probe; raw diagnostics retained. Room2.8/contact2.7/clearing3.9/pan3.8/caption4.0/native-background coverage remain priorities. V31 searchable known register1726 entries/1245 sources/328 pose cells/49 runtime regions/104 source regions retains676 source priorities/385 unassigned source opinions; four geode mounted uses are separately scoped. Earlier V30 bytes and technical labels preserved; current source/binding changes withhold affected claims. Separately all2074 preservedOctober1 WASH frames across all8 training/birthday-catalog cases at1280/1600 directly reviewed: Doctor256 report and seven-case1818 report,117 complete boards/29 native details/110 individual opinions. Nursery has an empty wash oval:workflow1.8/subject-contact1.5, no absent basin source score. Doctor workflow2.7/contact2.3/subject2.2/basin2.9. Dated source boundary470/475 current matches, not a newly rendered current wash capture or repair. Current washing rerender, ordinary story launch, later phases, device, child, owner and comprehensive all-job acceptance remain open. Verify all2077 required unchanged references at this exact immutable remote revision plus every changed payload and manifest. No finding closure, dev/master integration or release.')
s=s[:start]+"'qualification':"+repr(qualification)+s[end+1:]
s=s.replace("refs=json.loads((b/'audit/job_wash_root_doctor_sequence_v1_20261002/REQUIRED_UNCHANGED_REFERENCES.json').read_text())['files']", "refs=json.loads((b/'audit/job_wash_root_doctor_sequence_v1_20261002/REQUIRED_UNCHANGED_REFERENCES.json').read_text())['files']\nrefs.update(json.loads((b/'audit/job_wash_root_remaining_sequences_v1_20261002/REQUIRED_UNCHANGED_REFERENCES.json').read_text())['files'])")
s=s.replace("assert not set(refs)&set(files)","assert len(refs)==2077\nassert not set(refs)&set(files)")
s=s.replace('full-suite and372-source','full-suite and373-source')
(g/'review_tools/seal_geology_checkpoint_l_v315.py').write_text(s,encoding='utf-8',newline='\n')

s=(g/'review_tools/publish_geology_checkpoint_l_v297.py').read_text(encoding='utf-8')
s=s.replace('geology_checkpoint_l_publish_v297','geology_checkpoint_l_publish_v316').replace('geology_checkpoint_l_remote_v297','geology_checkpoint_l_remote_v316').replace('publish_geology_checkpoint_l_v297.py','publish_geology_checkpoint_l_v316.py')
s=s.replace('full_ci_v1/','full_ci_v2/').replace('==372','==373').replace("'source_count':372","'source_count':373")
start=s.index("msg.write_text(");end=s.index("\nrun('commit'",start)
message=('Reuse painted opening geode across its actual job route\n\nThe end specimen opens into two stone halves with crystals rooted inside. Reuse unchanged source artwork for Library crest, closed invitation, normal earned celebration and shared developer menu; preserve input, progress, save and rewards. Three script bindings and two metadata resources share one identical crop.\n\nEvery58 current stills/317 consecutive frames/37 complete boards/eight native details and23 qualified opinions reviewed. Library/invitation4.5 provisional; developer4.6; celebration painting4.6 but placement4.2/composition3.3. Room2.8/contact2.7/clearing3.9/pan3.8/caption4.0 and native background coverage remain. V31 known register1726 entries,676 source priorities/385 unassigned; current source/binding freshness withholds stale claims.\n\nAll2074 preservedOctober1 WASH frames across all8 training/birthday cases now reviewed on117 complete boards,29 native details,110 individual opinions. Nursery empty oval:workflow1.8/subject-contact1.5; absent source basin unscored. Doctor workflow2.7/contact2.3/subject2.2/basin2.9. Dated capture source470/475 matches; no new current wash capture or repair.\n\nFirst unchanged full suite retained RED81/82 crest-path failure. Corrected officialGodot4.7.2 suite2 passes82/82 on373 unchanged literal source files; probe untouched, raw diagnostics preserved. Manifest requires anonymous verification of every changed payload plus2077 unchanged review reference files at the immutable revision. Topic review candidate only; no finding closure, all-job/owner acceptance, dev/master integration or release.\n')
s=s[:start]+"msg.write_text("+repr(message)+",encoding='utf-8')"+s[end:]
s=s.replace("'entry_url':'https://github.com/Ebonyks/mermaid-roshan-reef/blob/'+revision+'/audit/job_geode_route_emblem_runtime_v1_20261002/index.html'", "'entry_url':'https://github.com/Ebonyks/mermaid-roshan-reef/blob/'+revision+'/audit/job_review_v2_20261001/index.html'")
(g/'review_tools/publish_geology_checkpoint_l_v316.py').write_text(s,encoding='utf-8',newline='\n')
for name,family in [('job-geode-route-emblem-runtime-20261002.json',g),('job-wash-root-remaining-sequences-review-20261002.json',w)]:
 p=r/'design/audit_impacts'/name;d=read(p);d['files']=sorted(set(d['files'])|{x.relative_to(r).as_posix() for x in family.rglob('*') if x.is_file()});write(p,d)
allow=r/'tmp/v2_preview_allowed.json';write(allow,sorted(set(read(allow))|{x.relative_to(r).as_posix() for family in [g,w] for x in family.rglob('*') if x.is_file()}))
print('Current checkpoint tools prepared: suite2/373-source/317 geode frames/all2074 dated wash frames/2077 unchanged references; not yet sealed or published.')
