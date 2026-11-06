"""Require current-dev successful push probes before manual APK build/publication."""
from __future__ import annotations
import json
import os
import re
import urllib.parse
import urllib.request

REPOSITORY = "Ebonyks/mermaid-roshan-reef"


def verify_runs(payload: object, repository: str, sha: str) -> int:
    if not re.fullmatch(r"[0-9a-f]{40}", sha):
        raise ValueError("invalid SHA")
    if not isinstance(payload, dict) or not isinstance(payload.get("workflow_runs"), list):
        raise ValueError("invalid response")
    expected = {"event": "push", "head_branch": "dev", "head_sha": sha,
                "path": ".github/workflows/probes.yml", "name": "Probe suite (graphics fork)"}
    candidates = []
    for run in payload["workflow_runs"]:
        if not isinstance(run, dict) or any(run.get(k) != v for k, v in expected.items()):
            continue
        if any(not isinstance(run.get(k), dict) or run[k].get("full_name") != repository
               for k in ("repository", "head_repository")):
            continue
        if type(run.get("id")) is not int or run["id"] <= 0 or type(run.get("run_number")) is not int or run["run_number"] <= 0:
            raise ValueError("invalid probe identity")
        candidates.append(run)
    if not candidates:
        raise ValueError("no exact-commit dev push probes")
    latest = max(candidates, key=lambda run: run["run_number"])
    if latest.get("status") != "completed" or latest.get("conclusion") != "success":
        raise ValueError("latest exact-commit probes are not green")
    return latest["id"]


def fetch_json(path: str, token: str) -> object:
    req = urllib.request.Request("https://api.github.com" + path, headers={
        "Authorization": "Bearer " + token, "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28", "User-Agent": "Reef-Android-Build"})
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.load(response)


def main() -> int:
    try:
        if os.environ.get("GITHUB_EVENT_NAME") != "workflow_dispatch" or os.environ.get("GITHUB_REF") != "refs/heads/dev":
            raise ValueError("manual packaging is dev-only")
        repo, sha, token = (os.environ.get(k, "") for k in ("GITHUB_REPOSITORY", "ANDROID_SOURCE_SHA", "GH_TOKEN"))
        if repo != REPOSITORY or not re.fullmatch(r"[0-9a-f]{40}", sha) or not token:
            raise ValueError("invalid source binding")
        branch = fetch_json("/repos/" + repo + "/git/ref/heads/dev", token)
        if not isinstance(branch, dict) or branch.get("ref") != "refs/heads/dev" or not isinstance(branch.get("object"), dict) or branch["object"].get("sha") != sha:
            raise ValueError("dev moved")
        query = urllib.parse.urlencode({"branch": "dev", "event": "push", "head_sha": sha, "per_page": 100})
        run_id = verify_runs(fetch_json("/repos/" + repo + "/actions/workflows/probes.yml/runs?" + query, token), repo, sha)
        print(f"ANDROID_SOURCE|PASS|dev|{sha}|probe_run={run_id}")
        return 0
    except (ValueError, OSError, KeyError, TypeError):
        # Never echo credentials, response bodies or untrusted error text.
        print("ANDROID_SOURCE|FAIL|current dev needs successful exact-commit push probes")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
