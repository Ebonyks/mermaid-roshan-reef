from pathlib import Path
R=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
p=R/'audit/job_geology_painted_invitation_fit_v1_20261003/review_tools/prepare_geology_lower_boards_v446.py'
s=p.read_text(encoding='utf-8')
for a,b in [('attempt02','attempt03'),('runtime_gate_lower_a2','runtime_gate_small_a3'),('QA_BOARD_MANIFEST_A2.json','QA_BOARD_MANIFEST_A3.json'),('lower-foreground A2','three-small-support A3'),('A1 exact failed layout preserved separately.','A1 exact failed layout and A2 reviewed oversized-support trial preserved separately.')]:
 assert a in s;s=s.replace(a,b)
exec(compile(s,str(Path(__file__)),'exec'),{'__file__':str(Path(__file__)),'__name__':'__main__'})
