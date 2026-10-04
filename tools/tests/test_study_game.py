from __future__ import annotations

import contextlib
import datetime as dt
import hashlib
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tools import build_study_roadmap as roadmap
from tools import measure_loop_health as health
from tools import study_game as study


class StudyGameTests(unittest.TestCase):
    def write(self, root: Path, path: str, data: object) -> Path:
        target = root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(data if isinstance(data, str) else json.dumps(data), encoding="utf-8")
        return target

    def git(self, root: Path, *args: str, day: str = "2026-10-03") -> str:
        environment = {**os.environ, "GIT_AUTHOR_DATE": day + "T12:00:00+00:00",
                       "GIT_COMMITTER_DATE": day + "T12:00:00+00:00"}
        return subprocess.run(["git", *args], cwd=root, capture_output=True, text=True,
                              check=True, env=environment).stdout.strip()

    def fixture(self, root: Path) -> str:
        self.git(root, "init", "-q")
        self.git(root, "config", "user.name", "Study Fixture")
        self.git(root, "config", "user.email", "study@example.invalid")
        self.write(root, str(health.FINDINGS), """# Findings

## MA-CI-001

| Field | Value |
|---|---|
| lifecycle | `CONFIRMED_OPEN` |
| severity | P2 |
| evidence | `scripts/changed.gd` |
| history | 2026-08-01: recorded open. |

## MA-VIS-001

| Field | Value |
|---|---|
| lifecycle | `FIXED_PENDING_VERIFICATION` |
| severity | P1 |
| evidence | `scripts/changed.gd` |
| history | 2026-09-03: implementation only. |
""")
        self.write(root, str(health.MASTER), "## 0. Planning entry\n\n## 14. Change history\n\n| 2026-09-03 | Implemented |\n")
        self.write(root, "scripts/changed.gd", "extends Node\n")
        self.write(root, "scripts/opera_house.gd", "const LIVE_ACT_INDICES: Array[int] = [0, 2]\n")
        self.write(root, "scripts/opera_career_world_2d.gd", 'const PHASES := {\n "chef": [{"mode": "tap"}, {"mode": "hold"}],\n}\n')
        self.write(root, "tools/godot_baseline.json", {"version": "4.7.2", "release": "4.7.2-stable"})
        self.write(root, ".github/workflows/probes.yml", """name: Probe Suite
jobs:
  probes:
    steps:
      - name: Capture Sky Lagoon visual review
        continue-on-error: true
        run: some capture
      - name: Opera balance playtest (advisory)
        continue-on-error: true
        run: some sensor
      - name: Upload pearl-castle visual review
        continue-on-error: true
        run: some upload
""")
        for index in range(3):
            self.write(root, f"design/audit_impacts/example-{index}.json", {
                "id": f"example-{index}", "scope": "An object-motion study", "rules": ["DL-MOT-13"],
                "files": ["scripts/changed.gd", "assets_src/cinematics/object_motion_2026/swing.png"], "findings": ["MA-CI-001"],
                "lessons": [{"lesson": "Keep sensor gaps visible", "write_back": "tools/study_game.py",
                             "recurrence_key": "silent-sensor"}],
                "validation": [{"command": "Owner visual review", "result": "FAIL", "evidence": "Wrong axis"},
                               {"command": "Probe Suite CI", "result": "PENDING", "evidence": "Wait"}],
                "acceptance_gaps": "Owner review not passed"})
        self.write(root, "docs/handoffs/untracked/README.md", "Untracked handoff")
        self.git(root, "add", ".")
        self.git(root, "commit", "-qm", "baseline", day="2026-09-03")
        baseline = self.git(root, "rev-parse", "HEAD")
        self.git(root, "update-ref", "refs/remotes/origin/dev", baseline)
        self.write(root, "scripts/changed.gd", "extends Node\n# change\n")
        self.git(root, "add", ".")
        self.git(root, "commit", "-qm", "source changed")
        return baseline

    def test_read_only_health_uses_root_and_reports_exact_30_day_age(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixture(root)
            result = health.measure(root, dt.date(2026, 10, 3))
            self.assertEqual(2, result["findings"]["open"])
            self.assertEqual(2, result["findings"]["open_without_history_entry_for"]["30_days"])
            self.assertEqual(3, result["impact_records"]["with_structured_lessons"])
            self.assertEqual("UNTRACKED", result["handoffs"][0]["status"])
            self.assertEqual("", self.git(root, "status", "--porcelain"))

    def test_game_2d_summary_preserves_digit_bearing_debt_counts(self):
        result = {"truncated": False, "output": "GAME2D| production_3d_files=54| probe_3d_files=19| scene_3d_files=2| configuration_3d_files=1| model_files=0\nGAME2D| STATUS| UNSATISFIED"}
        summary = study.sensor_summary("game_2d", result)
        self.assertEqual({"production_3d_files": 54, "probe_3d_files": 19, "scene_3d_files": 2, "configuration_3d_files": 1, "model_files": 0}, summary["counts"])
        self.assertEqual("UNSATISFIED", summary["status"])

    def test_advisory_failure_capped_empty_and_new_wrapper_tokens(self):
        for output, expected in (("LAGOONSHOT|RESULT|FAIL", "FAIL"),
                                 ("BALANCE|canvas|summary verdict=capped", "CAPPED"),
                                 ("", "NOT_MEASURED"),
                                 ("CASTLESHOT|RESULT|PASS", "MEASURED"),
                                 ("ADVISORY|Opera|RESULT|MEASURED|finite", "MEASURED"),
                                 ("ADVISORY|Opera|RESULT|FAILED|exit 1", "FAIL"),
                                 ("ADVISORY|Castle|RESULT|EMPTY|no files", "NOT_MEASURED"),
                                 ("CASTLESHOT|RESULT|NOT_MEASURED|written=0", "NOT_MEASURED"),
                                 ("Warning: No files were found", "FAIL")):
            with self.subTest(output=output):
                self.assertEqual(expected, study.advisory_status(output, "success")[0])
        self.assertEqual("FAIL", study.advisory_status("CASTLESHOT|RESULT|PASS", "failure")[0])
        self.assertEqual("CAPPED", study.advisory_status("ADVISORY|Opera|RESULT|CAPPED|timeout", "failure")[0])
        self.assertEqual("NOT_MEASURED", study.advisory_status("ADVISORY|Castle|RESULT|NOT_MEASURED|retired", "failure")[0])

    def test_green_ci_does_not_hide_failed_or_missing_advisories(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixture(root)
            head = self.git(root, "rev-parse", "HEAD")
            data = {"run": {"head_sha": head, "conclusion": "success"}, "log":
                    "probes\tCapture Sky Lagoon visual review\tLAGOONSHOT|RESULT|FAIL\n"
                    "probes\tOpera balance playtest (advisory)\tBALANCE|RESULT|CAPPED\n"}
            result = study.analyze_ci(root, head, data)
            self.assertEqual(["FAIL", "CAPPED", "NOT_MEASURED"], [s["status"] for s in result["advisory_steps"]])
            data["run"]["head_sha"] = "b" * 40
            self.assertEqual("HEAD_MISMATCH", study.analyze_ci(root, head, data)["status"])

    def test_unknown_step_real_github_format_uses_unique_job_windows(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixture(root)
            head = self.git(root, "rev-parse", "HEAD")
            rows = [{"name": "Run trusted probes", "conclusion": "success", "started_at": "2026-10-03T17:20:00Z", "completed_at": "2026-10-03T17:25:00Z"},
                    {"name": "Opera balance playtest (advisory)", "conclusion": "success", "started_at": "2026-10-03T17:30:33Z", "completed_at": "2026-10-03T17:30:38Z"},
                    {"name": "Capture Sky Lagoon visual review", "conclusion": "success", "started_at": "2026-10-03T17:31:46Z", "completed_at": "2026-10-03T17:31:50Z"}]
            data = {"run": {"head_sha": head, "conclusion": "success"}, "jobs": [{"name": "probes", "steps": rows}],
                    "log": "probes\tUNKNOWN STEP\t2026-10-03T17:24:59.4735153Z DUSTBAL|result: ALL OK\n"
                           "probes\tUNKNOWN STEP\t2026-10-03T17:30:37.0682736Z BALANCE|canvas|chef|summary verdict=capped\n"
                           "probes\tUNKNOWN STEP\t2026-10-03T17:31:48.0682736Z LAGOONSHOT|RESULT|FAIL\n"}
            result = study.analyze_ci(root, head, data)
            self.assertEqual(["FAIL", "CAPPED", "NOT_MEASURED"], [row["status"] for row in result["advisory_steps"]])
            self.assertEqual({"job_time_window": 1}, result["advisory_steps"][1]["log_attribution"])
            self.assertEqual(1, len(result["unattributed_result_lines"]))
            self.assertIn("DUSTBAL|result: ALL OK", result["unattributed_result_lines"][0])

    def test_unknown_step_missing_ambiguous_or_coarse_boundary_windows_stay_unmeasured(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixture(root)
            head = self.git(root, "rev-parse", "HEAD")
            opera = {"name": "Opera balance playtest (advisory)", "conclusion": "success",
                     "started_at": "2026-10-03T17:30:33Z", "completed_at": "2026-10-03T17:30:38Z"}
            following = {"name": "Publish opera art manifest (advisory)", "conclusion": "success",
                         "started_at": "2026-10-03T17:30:38Z", "completed_at": "2026-10-03T17:30:40Z"}
            line = "probes\tUNKNOWN STEP\t2026-10-03T17:30:38.0682736Z BALANCE|canvas|chef|summary verdict=capped"
            cases = [[], [{"name": "other-job", "steps": [opera]}],
                     [{"name": "probes", "steps": [{**opera, "completed_at": None}]}],
                     [{"name": "probes", "steps": [opera, following]}],
                     [{"name": "probes", "steps": [opera]}, {"name": "probes", "steps": [opera]}]]
            for jobs in cases:
                with self.subTest(jobs=jobs):
                    result = study.analyze_ci(root, head, {"run": {"head_sha": head}, "jobs": jobs, "log": line})
                    self.assertEqual("NOT_MEASURED", result["advisory_steps"][1]["status"])
                    self.assertEqual([line], result["unattributed_result_lines"])
            invalid = line.replace("2026-10-03T17:30:38.0682736Z", "invalid-timestamp")
            result = study.analyze_ci(root, head, {"run": {"head_sha": head}, "jobs": [{"name": "probes", "steps": [opera]}], "log": invalid})
            self.assertEqual("NOT_MEASURED", result["advisory_steps"][1]["status"])
            self.assertEqual([invalid], result["unattributed_result_lines"])

    def test_unknown_step_registered_legacy_protocol_can_resolve_boundary_owner(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixture(root)
            head = self.git(root, "rev-parse", "HEAD")
            path = root / ".github/workflows/probes.yml"
            original = path.read_text()
            path.write_text(original.replace("run: some sensor", "run: godot -s scripts/probe_opera_balance.gd -- --touch"))
            self.git(root, "commit", "-qam", "workflow")
            head = self.git(root, "rev-parse", "HEAD")
            jobs = [{"name": "probes", "steps": [
                {"name": "Opera balance playtest (advisory)", "conclusion": "success", "started_at": "2026-10-03T17:30:33Z", "completed_at": "2026-10-03T17:30:38Z"},
                {"name": "Publish opera art manifest (advisory)", "conclusion": "success", "started_at": "2026-10-03T17:30:38Z", "completed_at": "2026-10-03T17:30:40Z"}]}]
            line = "probes\tUNKNOWN STEP\t2026-10-03T17:30:38.0682736Z BALANCE|canvas|chef|summary verdict=capped"
            result = study.analyze_ci(root, head, {"run": {"head_sha": head}, "jobs": jobs, "log": line})
            self.assertEqual("CAPPED", result["advisory_steps"][1]["status"])
            self.assertEqual({"registered_protocol": 1}, result["advisory_steps"][1]["log_attribution"])
            path.write_text(path.read_text().replace("run: some capture", "run: godot -s scripts/probe_opera_balance.gd"))
            self.assertEqual("CAPPED", study.analyze_ci(root, head, {"run": {"head_sha": head}, "jobs": jobs, "log": line})["advisory_steps"][1]["status"])
            self.git(root, "commit", "-qam", "workflow 2")
            head = self.git(root, "rev-parse", "HEAD")
            result = study.analyze_ci(root, head, {"run": {"head_sha": head}, "jobs": jobs, "log": line})
            self.assertEqual("NOT_MEASURED", result["advisory_steps"][1]["status"])
            self.assertEqual([line], result["unattributed_result_lines"])

    def test_unknown_step_unique_wrapper_id_is_explicit_result_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixture(root)
            head = self.git(root, "rev-parse", "HEAD")
            path = root / ".github/workflows/probes.yml"
            original = path.read_text()
            command = "run: python tools/run_advisory_sensor.py --name opera-balance --timeout 30 -- command"
            path.write_text(original.replace("run: some sensor", command))
            self.git(root, "commit", "-qam", "workflow")
            head = self.git(root, "rev-parse", "HEAD")
            line = "probes\tUNKNOWN STEP\t2026-10-03T17:30:38.0682736Z ADVISORY|opera-balance|RESULT|CAPPED|timeout"
            result = study.analyze_ci(root, head, {"run": {"head_sha": head}, "log": line})
            self.assertEqual("CAPPED", result["advisory_steps"][1]["status"])
            self.assertEqual({"wrapper_id": 1}, result["advisory_steps"][1]["log_attribution"])
            path.write_text(path.read_text().replace("run: some capture", command))
            self.git(root, "commit", "-qam", "workflow 2")
            head = self.git(root, "rev-parse", "HEAD")
            result = study.analyze_ci(root, head, {"run": {"head_sha": head}, "log": line})
            self.assertEqual("NOT_MEASURED", result["advisory_steps"][1]["status"])
            self.assertEqual([line], result["unattributed_result_lines"])

    def test_roadmap_health_observes_absent_stale_current_and_source_invalid_states(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixture(root)
            data = study.collect(root, "2026-10-03", "2026-10-03", offline=True, skip_sensors=True)
            self.assertEqual("NOT_MEASURED", data["roadmap_observation"]["status"])
            source = self.write(root, "docs/strength-source.md", "Candidate source")
            self.write(root, "design/reference/strengths.json", {"strengths": [{
                "id": "S-01", "strength": "A scoped candidate", "tier": "candidate",
                "acceptance_scope": "No human acceptance", "reuse": "Study only",
                "evidence": [{"path": "docs/strength-source.md", "kind": "source", "sha256": hashlib.sha256(source.read_bytes()).hexdigest()}]}]})
            recipes = []
            for identifier in ("REC-REPAIR", "REC-ADD-JOB", "REC-ROOM-ACTIVITY", "REC-STUDY"):
                recipe = f"design/recipes/{identifier}.md"
                self.write(root, recipe, "Fixture recipe")
                recipes.append({"recipe": {"id": identifier, "path": recipe}})
            self.write(root, "design/reference/prompt_intents.json", {"intents": recipes})
            self.write(root, "design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md", "DL-AUTH-05")
            path = self.write(root, "audit/ROADMAP.md", "Old roadmap")
            before = path.read_bytes()
            stale = study.roadmap_observation(root, data)
            self.assertEqual("MEASURED", stale["status"])
            self.assertFalse(stale["current"])
            self.assertEqual(before, path.read_bytes())
            data["roadmap_observation"] = stale
            self.assertEqual("NEEDS_ATTENTION", next(row for row in study.health_targets(data) if row["id"] == "roadmap_current_cycle")["status"])
            self.write(root, "audit/ROADMAP.md", roadmap.build_outputs(root, data)["ROADMAP.md"])
            data = study.collect(root, "2026-10-03", "2026-10-03", offline=True, skip_sensors=True, allow_dirty=True)
            self.assertTrue(data["roadmap_observation"]["current"])
            target = next(row for row in data["health_targets"] if row["id"] == "roadmap_current_cycle")
            self.assertEqual("ON_TARGET", target["status"])
            self.assertEqual("MEASURED", target["measurement_status"])
            self.assertFalse(study.roadmap_observation(root, {**data, "cycle_date": "2026-10-04"})["current"])
            self.assertFalse(study.roadmap_observation(root, {**data, "head": "f" * 40, "studied_head": "f" * 40})["current"])
            source.write_text("Changed candidate source")
            changed = study.roadmap_observation(root, data)
            self.assertEqual("MEASURED", changed["status"])
            self.assertFalse(changed["current"])
            self.assertIn("STRENGTH-S-01", roadmap.build_outputs(root, data)["ROADMAP.md"])
            (root / "design/reference/strengths.json").unlink()
            self.assertEqual("NOT_MEASURED", study.roadmap_observation(root, data)["status"])

    def test_runner_collects_findings_lessons_motion_and_reproducible_report(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            baseline = self.fixture(root)
            previous = self.write(root, "build/previous.json", {"cycle": "baseline", "head": baseline})
            result = study.collect(root, "2026-10-03", "2026-10-03", previous, offline=True, skip_sensors=True, allow_dirty=True)
            self.assertEqual("NOT_MEASURED", result["ci"]["status"])
            self.assertEqual(2, len(result["findings_changed_since_history"]))
            self.assertEqual(3, len(result["impacts"]["lessons"]))
            self.assertEqual(3, len(result["impacts"]["pending"]))
            self.assertEqual(3, len(result["impacts"]["failed"]))
            self.assertEqual("object", result["motion_studies"][0]["kind"])
            self.assertFalse(result["cycle_evidence"]["complete"])
            self.assertEqual(study.render_report(result), study.render_report(json.loads(json.dumps(result, sort_keys=True))))
            self.assertEqual(2, result["live_status"]["opera_active_careers"])
            self.assertEqual(2, result["live_status"]["opera_declared_phases"])

    def test_sensor_timeout_empty_nonzero_and_truncation_preserve_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.assertEqual("EMPTY", study.execute(root, [sys.executable, "-c", "pass"])["status"])
            self.assertEqual("FAIL", study.execute(root, [sys.executable, "-c", "raise SystemExit(2)"])["status"])
            self.assertEqual("TIMEOUT", study.execute(root, [sys.executable, "-c", "import time; time.sleep(2)"], .01)["status"])
            result = study.execute(root, [sys.executable, "-c", "print('x'*4096); print('LAGOONSHOT|RESULT|FAIL')"], max_output=1024)
            self.assertEqual("TRUNCATED", result["status"])
            self.assertIn("LAGOONSHOT|RESULT|FAIL", result["result_lines"])
            self.assertEqual(64, len(result["output_sha256"]))

    def test_library_hash_delta_without_rebuilding_art(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write(root, "assets/art.png", "old image bytes")
            self.write(root, "audit/day2_art_library_2026-09-30/inventory.json", {
                "source_revision": "a" * 40, "watched_sources": {"scripts/source.gd": "0" * 64},
                "items": [{"path": "assets/art.png", "sha256": "0" * 64}]})
            self.write(root, "scripts/source.gd", "extends Node")
            self.write(root, "audit/day2_art_library_2026-09-30/refresh_delta.json", {"changed": []})
            result = study.library_delta(root)
            self.assertEqual(["scripts/source.gd"], result["changed_watched_sources"])
            self.assertEqual("hash changed", result["stale_items"][0]["reason"])
            self.assertEqual("old image bytes", (root / "assets/art.png").read_text())

    def test_safety_guard_excludes_escape_symlink_and_secrets(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in ("../outside", ".secrets/secret", ".git/config", "assets/key.keystore", "C:/outside", None, 123):
                self.assertIsNone(study.safe_relative(root, name))
            self.assertEqual(root / "scripts/test.gd", study.safe_relative(root, "res://scripts/test.gd"))

    def test_recurrence_is_cycle_scoped_and_only_proposes(self):
        rows = [{"record": f"record-{index}", "value": {"lesson": "Same correction", "write_back": "sensor"}}
                for index in range(3)]
        self.assertEqual([], study.recurrence_proposals({"lessons": rows}, ["record-0"]))
        result = study.recurrence_proposals({"lessons": rows}, [r["record"] for r in rows])
        self.assertEqual(3, result[0]["count"])
        self.assertIn("authority remains unchanged", result[0]["proposal"])

    def test_operating_defaults_never_complete_cycle(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write(root, "design/reference/owner_decisions.json", {"decisions": [
                {"id": "default", "authority": "operating_default"},
                {"id": "actual", "authority": "recorded_owner"}]})
            result = study.decision_inventory(root)
            self.assertEqual(1, len(result["recorded_owner"]))
            self.assertEqual(1, len(result["operating_default"]))
            self.write(root, "docs/evidence.md", "Actual evidence")
            self.write(root, "audit/cycles/one/CYCLE_EVIDENCE.json", {
                "owner_answers": [{"question": "Q1", "answer": "yes", "authority": "operating_default", "evidence": "docs/evidence.md"}],
                "build": [{"evidence": "docs/evidence.md"}], "check": [{"evidence": "docs/evidence.md"}],
                "learn": [{"evidence": "docs/evidence.md"}]})
            result = study.cycle_evidence(root, "one")
            self.assertIn("actual_owner_answers", result["missing"])
            self.assertFalse(result["complete"])

    def test_unavailable_visual_sensor_is_explicit(self):
        with tempfile.TemporaryDirectory() as directory:
            result = study.run_sensors(Path(directory), 1, False, 1024)
            self.assertEqual("UNAVAILABLE", result["visual_profile"]["status"])

    def test_visual_sensor_list_shape_and_baseline_delta(self):
        result = {"output": json.dumps([{"severity": "COVERAGE_GAP"}, {"severity": "FAIL"}]), "truncated": False}
        summary = study.sensor_summary("visual_profile", result)
        self.assertEqual(2, summary["findings"])
        self.assertEqual(1, summary["severity_counts"]["COVERAGE_GAP"])
        current = {"findings": {"open_without_history_entry_for": {"30_days": 2}, "fixed_pending_verification": []},
                   "impact_records": {"records": 4, "with_structured_lessons": 2}, "handoffs": []}
        baseline = {"measure": "loop_health", "findings": {"open_without_history_entry_for": {"30_days": 3},
                    "fixed_pending_verification": [{"id": "old"}]}, "impact_records": {"records": 3}, "handoffs": []}
        delta = study.loop_delta(current, baseline)
        self.assertEqual("baseline_measurement", delta["baseline_kind"])
        self.assertEqual(-1, delta["metrics"]["stale_open"]["delta"])
        self.assertEqual("NOT_COMPARABLE", delta["metrics"]["structured_lessons_fraction"]["status"])

    def test_library_comparison_and_changed_sha_reference(self):
        self.assertEqual("NOT_COMPARABLE", study.library_comparison({"status": "MEASURED"}, {})["status"])
        prior = {"status": "MEASURED", "stale_items": [{"path": "old", "reason": "missing"}], "changed_watched_sources": ["controller"]}
        current = {"status": "MEASURED", "stale_items": [{"path": "new", "reason": "hash changed"}], "changed_watched_sources": []}
        comparison = study.library_comparison(current, prior)
        self.assertEqual(["new"], comparison["new_stale_items"])
        self.assertEqual(["old"], comparison["no_longer_stale_items"])
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            baseline = self.fixture(root)
            self.write(root, "docs/shas.md", f"Existing {baseline}; invented {'f' * 40}")
            result = study.document_sha_references(root, ["docs/shas.md"], 30)
            self.assertEqual(2, result["checked"])
            self.assertEqual("f" * 40, result["unresolved"][0]["sha"])

    def test_stress_proves_failed_sensor_is_not_a_green_measurement(self):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(0, study.stress())
        self.assertIn("ALL OK", output.getvalue())

    def test_cli_round_trip_does_not_run_measurements(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixture(root)
            data = study.collect(root, "one", "2026-10-03", offline=True, skip_sensors=True)
            saved = self.write(root, "build/study.json", data)
            with mock.patch.object(study, "collect", side_effect=AssertionError("must render JSON only")), \
                 mock.patch.object(study, "roadmap_observation", side_effect=AssertionError("ordinary render must retain saved observation")), \
                 mock.patch.object(study, "health_targets", side_effect=AssertionError("ordinary render must retain saved targets")):
                with contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(0, study.main(["--root", str(root), "--render", str(saved), "--output", "build/rendered"]))
            self.assertEqual(study.render_report(data), (root / "build/rendered/STUDY_REPORT.md").read_text(encoding="utf-8"))

    def test_cli_refresh_roadmap_requires_saved_study(self):
        with mock.patch.object(study, "collect", side_effect=AssertionError("guard must reject before collection")):
            with contextlib.redirect_stderr(io.StringIO()) as output:
                with self.assertRaises(SystemExit) as error:
                    study.main(["--refresh-roadmap"])
        self.assertEqual(2, error.exception.code)
        self.assertIn("--refresh-roadmap requires --render", output.getvalue())

    def test_cli_refresh_changes_only_roadmap_observation_and_health_targets(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixture(root)
            data = study.collect(root, "2026-10-03", "2026-10-03", offline=True, skip_sensors=True)
            saved = self.write(root, "build/study.json", data)
            receipt = self.write(root, "build/sensor-receipt.txt", "RAW|RESULT|FAIL|Preserved original")
            before = (saved.read_bytes(), receipt.read_bytes())
            current = {"status": "MEASURED", "current": True, "source": "audit/ROADMAP.md",
                       "cycle": "2026-10-03", "studied_head": data["head"], "reason": "Same-cycle render fixture"}
            with mock.patch.object(study, "collect", side_effect=AssertionError("refresh must use the saved study")), \
                 mock.patch.object(study, "run_sensors", side_effect=AssertionError("refresh must not run sensors")), \
                 mock.patch.object(study, "roadmap_observation", return_value=current) as observe:
                with contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(0, study.main(["--root", str(root), "--render", str(saved),
                                                  "--refresh-roadmap", "--output", "build/refreshed"]))
            observe.assert_called_once()
            self.assertEqual(root, observe.call_args.args[0])
            refreshed = json.loads((root / "build/refreshed/study.json").read_text(encoding="utf-8"))
            self.assertEqual(current, refreshed["roadmap_observation"])
            self.assertEqual("ON_TARGET", next(row for row in refreshed["health_targets"] if row["id"] == "roadmap_current_cycle")["status"])
            for key in set(data) - {"roadmap_observation", "health_targets"}:
                self.assertEqual(data[key], refreshed[key], key)
            self.assertEqual(before, (saved.read_bytes(), receipt.read_bytes()))
            self.assertEqual(study.render_report(refreshed), (root / "build/refreshed/STUDY_REPORT.md").read_text(encoding="utf-8"))

    def test_malformed_previous_render_and_owner_answers_fail_explicitly(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixture(root)
            previous = self.write(root, "build/previous.json", [])
            with self.assertRaisesRegex(ValueError, "Study a committed head"):
                study.collect(root, "one", "2026-10-03", previous, offline=True, skip_sensors=True)
            with self.assertRaisesRegex(ValueError, "Previous observation"):
                study.collect(root, "one", "2026-10-03", previous, offline=True, skip_sensors=True, allow_dirty=True)
            saved = self.write(root, "build/saved.json", {"cycle": "one"})
            with contextlib.redirect_stderr(io.StringIO()) as output:
                self.assertEqual(1, study.main(["--root", str(root), "--render", str(saved), "--output", "build/rendered"]))
            self.assertIn("STUDY|RESULT|FAIL", output.getvalue())
            self.assertFalse((root / "build/rendered/study.json").exists())
            self.write(root, "audit/cycles/one/CYCLE_EVIDENCE.json", {"owner_answers": None})
            result = study.cycle_evidence(root, "one")
            self.assertEqual("INCOMPLETE", result["status"])
            self.assertIn("actual_owner_answers", result["missing"])

    def test_cycle_intake_answers_are_consumed_deduplicated_and_read_only(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write(root, "docs/session.md", "Actual owner answers from this session")
            answer = {"id": "ODR-CYCLE-Q1", "authority": "recorded_owner", "cycle": "one",
                      "question": "Q1", "decision": "Yes", "source": "docs/session.md"}
            saved = self.write(root, "audit/cycles/one/owner_answers.json", [answer])
            receipt = self.write(root, "audit/cycles/one/CYCLE_EVIDENCE.json", {
                "owner_answers": [answer], "build": [{"evidence": "docs/session.md"}],
                "check": [{"evidence": "docs/session.md"}], "learn": [{"evidence": "docs/session.md"}]})
            before = (saved.read_bytes(), receipt.read_bytes())
            result = study.cycle_evidence(root, "one")
            self.assertEqual(1, len(result["actual_owner_answers"]))
            self.assertTrue(result["recorded_lanes_complete"])
            self.assertFalse(result["complete"])
            self.assertEqual(before, (saved.read_bytes(), receipt.read_bytes()))
            self.write(root, "audit/cycles/one/owner_answers.json", {"owner_answers": [answer]})
            malformed = saved.read_bytes()
            result = study.cycle_evidence(root, "one")
            self.assertEqual("FAIL", result["status"])
            self.assertEqual(malformed, saved.read_bytes())
            self.write(root, "audit/cycles/one/owner_answers.json", [{**answer, "cycle": "other"}])
            self.assertEqual("FAIL", study.cycle_evidence(root, "one")["status"])


class StudyRepairTests(unittest.TestCase):
    """Repairs from the 2026-10-03 review of the loop implementation."""

    LOG = ("probes\tDust boss balance playtest (advisory)\t2026-10-04T00:05:00.1Z \x1b[36;1mpython3 tools/run_advisory_sensor.py --name dust --timeout 610 -- timeout 10m godot\x1b[0m\n"
           "probes\tDust boss balance playtest (advisory)\t2026-10-04T00:05:01.1Z WARNING: All audio drivers failed, falling back to the dummy driver.\n"
           "probes\tDust boss balance playtest (advisory)\t2026-10-04T00:07:56.2Z ADVISORY|dust|RESULT|MEASURED|measurement/output exists\n")

    def test_echoed_script_and_benign_warnings_are_not_failures(self):
        self.assertEqual("MEASURED", study.advisory_status(self.LOG, "success")[0])
        self.assertTrue(study.is_noise("probes\tStep\t2026-10-04T00:05:00.1Z \x1b[36;1mtimeout 10m godot\x1b[0m"))
        self.assertTrue(study.is_noise("probes\tStep\t2026-10-04T00:05:00.1Z WARNING: All audio drivers failed"))
        self.assertFalse(study.is_noise("probes\tStep\t2026-10-04T00:05:00.1Z LAGOONSHOT|RESULT|FAIL"))

    def test_worst_wrapper_verdict_wins_and_retirement_is_declared(self):
        text = ("x\ty\t2026-10-04T00:00:00.1Z ADVISORY|one|RESULT|FAILED|exit 1\n"
                "x\ty\t2026-10-04T00:00:01.1Z ADVISORY|two|RESULT|NOT_MEASURED|unsupported\n")
        self.assertEqual("FAIL", study.advisory_status(text)[0])
        retired = "x\ty\t2026-10-04T00:00:00.1Z ADVISORY|reef|RESULT|NOT_MEASURED|Retired Reef capture removed from live review"
        self.assertEqual([("NOT_MEASURED", "reef", "Retired Reef capture removed from live review")], study.wrapper_results(retired))

    def test_pending_entries_reconcile_by_exact_head(self):
        pending = [{"record": "a.json", "command": "GitHub Probe Suite at the branch head", "last_changed_head": "a" * 40},
                   {"record": "b.json", "command": "Probe Suite CI", "last_changed_head": "b" * 40},
                   {"record": "c.json", "command": "Probe Suite CI", "last_changed_head": None},
                   {"record": "d.json", "command": "Owner review", "last_changed_head": "d" * 40}]
        runs = {"a" * 40: [{"id": 2, "status": "completed", "conclusion": "success"}, {"id": 1, "status": "completed", "conclusion": "cancelled"}],
                "b" * 40: [{"id": 3, "status": "completed", "conclusion": "cancelled"}]}
        study.reconcile_pending(pending, runs, [])
        self.assertEqual(["RUN_FOUND", "CANCELLED_ONLY", "UNKNOWN_HEAD", "NOT_CI"], [row["ci_reconciliation"]["state"] for row in pending])
        offline = [{"record": "e.json", "command": "Probe Suite CI", "last_changed_head": "e" * 40}]
        study.reconcile_pending(offline, {}, [], looked_up=set())
        self.assertEqual("NOT_LOOKED_UP", offline[0]["ci_reconciliation"]["state"])
        self.assertEqual(2, pending[0]["ci_reconciliation"]["run"]["id"])

    def test_health_targets_fail_closed_without_findings(self):
        data = {"loop_health": {"findings": {}}, "impacts": {"records": [], "owner_corrections": []}}
        targets = {row["id"]: row for row in study.health_targets(data)}
        self.assertEqual("NOT_MEASURED", targets["stale_open_fraction"]["status"])
        self.assertEqual("NOT_MEASURED", targets["old_unverified_fixes"]["status"])
        self.assertEqual("NOT_MEASURED", targets["repeated_owner_corrections"]["status"])

    def test_text_sources_hash_the_same_on_every_platform(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            lf = root / "lf.gd"
            crlf = root / "crlf.gd"
            lf.write_bytes(b"extends Node\n")
            crlf.write_bytes(b"extends Node\r\n")
            self.assertEqual(study.content_sha256(lf), study.content_sha256(crlf))
            image = root / "image.png"
            image.write_bytes(b"\x89PNG\r\n")
            self.assertEqual(hashlib.sha256(b"\x89PNG\r\n").hexdigest(), study.content_sha256(image))


class StudyReportTests(unittest.TestCase):
    # Reuse the repository fixture helpers without re-running the base tests.
    write = StudyGameTests.write
    git = StudyGameTests.git
    fixture = StudyGameTests.fixture

    def collected(self, root: Path) -> dict:
        self.fixture(root)
        return study.collect(root, "2026-10-03", "2026-10-03", offline=True, skip_sensors=True)

    def test_dirty_tree_is_refused_but_cycle_outputs_are_allowed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixture(root)
            self.write(root, "audit/cycles/2026-10-03/owner_answers.json", [])
            data = study.collect(root, "2026-10-03", "2026-10-03", offline=True, skip_sensors=True,
                                 output=root / "audit/cycles/2026-10-03")
            self.assertEqual(["audit/cycles/2026-10-03/owner_answers.json"], data["working_tree"]["paths"])
            self.write(root, "scripts/changed.gd", "extends Node\n# uncommitted\n")
            with self.assertRaisesRegex(ValueError, "Study a committed head"):
                study.collect(root, "2026-10-03", "2026-10-03", offline=True, skip_sensors=True, output=root / "audit/cycles/2026-10-03")
            scratch = study.collect(root, "2026-10-03", "2026-10-03", offline=True, skip_sensors=True, allow_dirty=True)
            self.assertIn("NOT REPRODUCIBLE", study.render_report(scratch))

    def test_report_is_short_plain_and_free_of_raw_machine_text(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            data = self.collected(root)
            data["ci"] = {"status": "MEASURED", "run": {"id": 1, "html_url": "https://example.invalid/1", "status": "completed", "conclusion": "success"},
                          "advisory_steps": [{"name": "Capture Sky Lagoon visual review", "status": "FAIL", "reason": "sky: process exit 1", "retired": False},
                                             {"name": "Capture first-world visual review", "status": "NOT_MEASURED", "reason": "reef: Retired Reef capture", "retired": True}],
                          "unattributed_result_lines": ["\x1b[36;1mraw\x1b[0m"] * 40, "trusted_probes": {"ran": ["probe_a"], "failed": [], "hung_after_verdict": []}}
            report = study.render_report(data)
            self.assertLessEqual(len(report.splitlines()), 90)
            self.assertLessEqual(len(report.split()), 1200)
            self.assertNotIn("\x1b", report)
            self.assertNotIn('{"lesson"', report)
            self.assertNotRegex(report, r"0\.\d{6,}")
            self.assertIn("1 retired", report)
            self.assertIn("## 7. Questions for the owner", report)
            self.assertIn("(generated candidate)", report)

    def test_judgement_drives_prompts_and_questions(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            data = self.collected(root)
            catalogue = json.loads((Path(__file__).resolve().parents[2] / "design/reference/prompt_intents.json").read_text(encoding="utf-8"))
            self.write(root, "design/reference/prompt_intents.json", catalogue)
            judgement = {"schema": "cycle_judgement/1", "cycle": "2026-10-03", "author": "Claude", "summary": "Short summary.",
                         "strengths": [{"id": "S-02", "note": "Scrubbing changes the room where the child touches."}],
                         "weaknesses": [{"item": "Captures fail on CI", "action": "Report the renderer fallback"}],
                         "prompts": [{"say": "Study the game", "intent": "INT-STUDY", "why": "next cycle", "size": "small"}],
                         "questions": [{"question": "May we keep the defaults?", "default": "yes"}]}
            path = self.write(root, "audit/cycles/2026-10-03/judgement.json", judgement)
            loaded = study.load_judgement(root, path, data)
            report = study.render_report(data, loaded)
            self.assertIn("written by Claude", report)
            self.assertIn("**S-02**", report)
            self.assertIn('"Study the game"', report)
            self.assertNotIn("(generated candidate)", report)
            for bad in ({"prompts": [{"say": "Study the game", "intent": "INT-REPAIR", "why": "x", "size": "small"}]},
                        {"questions": [{"question": "No question mark", "default": "yes"}]},
                        {"prompts": [{"say": "Study the game", "intent": "INT-STUDY", "why": "x", "size": "small"}] * 6},
                        {"cycle": "other"}):
                with self.subTest(bad=bad):
                    self.write(root, "audit/cycles/2026-10-03/judgement.json", {**judgement, **bad})
                    with self.assertRaises(ValueError):
                        study.load_judgement(root, path, data)

    def test_compact_study_drops_duplicates_and_raw_output(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            data = self.collected(root)
            self.assertNotIn("impact_records", data)
            self.assertTrue(all("files" not in row and "validation" not in row for row in data["impacts"]["records"]))
            self.assertTrue(all(len(row.get("summary", "")) <= 300 for row in data["impacts"]["records"]))
            self.assertIn("unmerged_count", data["branches"])


if __name__ == "__main__":
    unittest.main()
