from pathlib import Path

r = Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
source = r / 'audit/job_geode_embedded_mount_v2_20261001/executed_run_geode_embedded_mount_v98.py'
body = source.read_text(encoding='utf-8')
body = body.replace("out=r/'audit/job_geode_embedded_mount_v2_20261001'", "out=r/'audit/job_geode_embedded_mount_v2_20261001/attempt_02'")
body = body.replace('tmp/geode_embedded_mount_v98/native_views', 'tmp/geode_embedded_mount_v99/native_views')
body = body.replace('var half_height := 350.0', 'var half_height := 320.0')
body = body.replace("out/'executed_run_geode_embedded_mount_v98.py'", "out/'executed_run_geode_embedded_mount_v99.py'")
body = body.replace("preserved_half_aspect=True,", "preserved_half_aspect=True,half_height=320,previous_capture_attempt='audit/job_geode_embedded_mount_v2_20261001',placement_gap='Previous full-open right half overhung work slab; this fixture reduces both halves uniformly without changing source pixels.',")
exec(compile(body, str(source), 'exec'))
