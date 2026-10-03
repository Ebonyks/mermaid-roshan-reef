#!/usr/bin/env python3
"""Keep advisory results observable without treating them as product acceptance."""
from __future__ import annotations

import argparse
import hashlib
import glob
import json
import re
import subprocess
import time
from pathlib import Path


# A metric header or a single case is not a completed sensor. Legacy probes
# retain their authored completion tokens until their contracts are rebuilt.
TERMINAL_RE = re.compile(r"\|RESULT\|\s*(?:PASS|MEASURED|ALL OK)(?:\||\s*$)|\|result:\s*ALL OK\s*$|\|DONE(?:\||\s*$)", re.I)


def classify(output: str, exit_code: int, expected: str, missing: list[str]) -> tuple[str, str]:
	if exit_code in (124, -9):
		return "CAPPED", "process timeout; no completed measurement"
	if exit_code != 0 or re.search(r"SCRIPT ERROR|Parse Error|Compile Error|\|FAIL(?:ED)?(?:\||\s*$)|(?:RESULT\|FAIL)|result:\s*\d+\s+FAILED\b|SAVE_ERROR|ART_AUDIT\|saved[^\r\n]*\bERR\s+\d+\s*$|verdict=(?:fail|failed)", output, re.I | re.M):
		return "FAILED", f"process exit {exit_code} or explicit failure"
	if re.search(r"verdict=capped|RESULT\|CAPPED", output, re.I):
		return "CAPPED", "at least one simulated run reached its cap"
	if re.search(r"NOT_MEASURED|UNSUPPORTED|HEADLESS SKIP|\|INCOMPLETE(?:\||\s*$)", output, re.I | re.M):
		return "NOT_MEASURED", "at least one required case is unsupported or unmeasured"
	if not output.strip() or (expected and not any(
		expected in line and TERMINAL_RE.search(line) for line in output.splitlines()
	)):
		return "EMPTY", "no expected completed verdict output"
	if missing:
		return "NOT_MEASURED", "missing required outputs: " + ", ".join(missing)
	return "MEASURED", "measurement/output exists; human/device acceptance is separate"


def output_inventory(patterns: list[str]) -> dict[str, dict]:
	rows = {}
	for pattern in patterns:
		for name in glob.glob(pattern):
			path = Path(name)
			if path.is_file():
				stat = path.stat()
				rows[str(path)] = {"size": stat.st_size, "modified_ns": stat.st_mtime_ns,
					"sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
	return rows


def stale_requirements(patterns: list[str], before: dict, after: dict) -> list[str]:
	return [pattern for pattern in patterns if not any(
		name in after and after[name]["size"] > 0 and after[name] != before.get(name)
		for name in glob.glob(pattern))]


def main() -> int:
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("--name", required=True)
	parser.add_argument("--report-dir", type=Path, default=Path("audit/advisory"))
	parser.add_argument("--expected", default="", help="Prefix/marker of the required terminal verdict; metric headers never suffice")
	parser.add_argument("--require", action="append", default=[], help="Required output glob relative to current directory")
	parser.add_argument("--timeout", type=float, default=600)
	parser.add_argument("--not-measured", help="Record an explicitly retired or unavailable sensor")
	parser.add_argument("command", nargs=argparse.REMAINDER)
	args = parser.parse_args()
	if not re.fullmatch(r"[a-z0-9_-]+", args.name):
		parser.error("name must be a safe lowercase ID")
	command = args.command[1:] if args.command[:1] == ["--"] else args.command
	started_ns = time.time_ns()
	before = output_inventory(args.require)
	if args.not_measured:
		output, code = args.not_measured + "\n", 0
		status, reason = "NOT_MEASURED", args.not_measured
	elif not command:
		parser.error("supply a command after -- or --not-measured")
	else:
		try:
			result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=args.timeout, check=False)
			output, code = result.stdout.decode("utf-8", errors="replace"), result.returncode
		except subprocess.TimeoutExpired as exc:
			output, code = (exc.stdout or b"").decode("utf-8", errors="replace"), 124
		except OSError as exc:
			output, code = str(exc), 127
		missing = stale_requirements(args.require, before, output_inventory(args.require))
		status, reason = classify(output, code, args.expected, missing)
		if missing:
			reason += "; existing unchanged outputs do not count as this run's evidence"
	args.report_dir.mkdir(parents=True, exist_ok=True)
	(args.report_dir / (args.name + ".log")).write_text(output, encoding="utf-8")
	data = {"schema": "advisory_sensor/1", "name": args.name, "status": status, "reason": reason, "command": command, "exit_code": code, "output_sha256": hashlib.sha256(output.encode()).hexdigest(), "required_outputs": args.require,
		"started_ns": started_ns, "finished_ns": time.time_ns(), "outputs": output_inventory(args.require)}
	(args.report_dir / (args.name + ".json")).write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
	print(output, end="" if output.endswith("\n") else "\n")
	print(f"ADVISORY|{args.name}|RESULT|{status}|{reason}")
	return 0 if status == "MEASURED" else 1


if __name__ == "__main__":
	raise SystemExit(main())
