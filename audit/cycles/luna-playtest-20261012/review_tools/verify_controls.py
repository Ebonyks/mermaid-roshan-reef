"""Falsify session-count/evidence claims in disposable fixtures, never real reports."""
from pathlib import Path
from datetime import datetime, timezone
import contextlib
import copy
import hashlib
import importlib.util
import io
import json
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[4]
CYCLE = ROOT / "audit/cycles/luna-playtest-20261012"


def main():
    source = CYCLE / "review_tools/verify_sessions.py"
    spec = importlib.util.spec_from_file_location("luna_verifier_controls", source)
    verifier = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(verifier)
    report = json.loads((CYCLE / "reports/L01.json").read_text(encoding="utf-8"))
    receipt = json.loads((ROOT / report["runtime_receipt"]).read_text())
    log_bytes = (ROOT / receipt["log"]).read_bytes()
    matrix = json.loads((CYCLE / "matrix.json").read_text())
    coordinator = json.loads((CYCLE / "coordinator.json").read_text())
    first = next(x for x in coordinator["agents"] if x["session_id"] == "L01")
    cases = [
        ("Valid scoped single session passes partial review", "valid", True, 0),
        ("Planned assignments cannot establish actual completed agents", "valid", False, 1),
        ("Mutated raw log fails exact hash", "log", True, 1),
        ("PASS report cannot mask failed runtime", "failure", True, 1),
        ("Numeric child/product fun score is rejected", "score", True, 1),
        ("Uninvoked agent identity is rejected", "identity", True, 1),
        ("Wrong frozen source baseline is rejected", "baseline", True, 1),
        ("Prose cannot masquerade as structured finding IDs", "finding_type", True, 1),
    ]
    results = []
    fixture_root = Path(tempfile.mkdtemp(prefix="reef-luna-verifier-controls-"))
    for number, (label, mutation, partial, expected) in enumerate(cases, 1):
        test_root = fixture_root / str(number)
        test_cycle = test_root / "audit/cycles/luna-playtest-20261012"
        (test_cycle / "reports").mkdir(parents=True)
        (test_cycle / "runtime/L01/attempt_1").mkdir(parents=True)
        test_report, test_receipt = copy.deepcopy(report), copy.deepcopy(receipt)
        test_report["runtime_receipt"] = "audit/cycles/luna-playtest-20261012/runtime/L01/attempt_1/receipt.json"
        if mutation == "failure":
            test_receipt["status"], test_report["verdict"] = "FAIL", "PASS"
        elif mutation == "score":
            test_report["play_appeal"]["fun_score"] = 9
        elif mutation == "identity":
            test_report["reviewer"]["agent_id"] = "/uninvoked/luna_l01"
        elif mutation == "finding_type":
            test_report["observations"][0]["existing_findings"] = "MA-PLAY-005 is context, not an ID array"
        elif mutation == "baseline":
            test_report["baseline"] = "0" * 40
        (test_cycle / "matrix.json").write_text(json.dumps(matrix))
        (test_cycle / "coordinator.json").write_text(json.dumps({"agents": [first], "completed_count": 1}))
        (test_cycle / "reports/L01.json").write_text(json.dumps(test_report))
        (test_cycle / "runtime/L01/attempt_1/receipt.json").write_text(json.dumps(test_receipt))
        (test_root / receipt["log"]).write_bytes(log_bytes + (b"mutation" if mutation == "log" else b""))
        verifier.ROOT, verifier.CYCLE = test_root, test_cycle
        old_argv = sys.argv
        try:
            sys.argv = [str(source)] + (["--partial"] if partial else [])
            with contextlib.redirect_stdout(io.StringIO()):
                actual = verifier.main()
        finally:
            sys.argv = old_argv
        outcome = json.loads((test_cycle / "verification/sessions.json").read_text())
        results.append({"case": label, "expected_exit": expected, "actual_exit": actual,
                        "errors": outcome["errors"], "pass": expected == actual})
    result = {"schema": "luna_verifier_controls/1", "checked_utc": datetime.now(timezone.utc).isoformat(),
              "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
              "helper_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "planned_assignments": len(matrix["sessions"]),
              "status": "PASS" if all(x["pass"] for x in results) else "FAIL", "cases": results,
              "fixture_root": str(fixture_root),
              "scope": "Disposable copied fixtures outside the repository; no real reports altered or counted. Evidence/count validator only, no gameplay/child acceptance."}
    destination = CYCLE / "verification/verifier_controls_current.json"
    destination.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"Verifier controls: {result['status']} ({len(results)} cases)")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
