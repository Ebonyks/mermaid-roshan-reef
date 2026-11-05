from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
from urllib.parse import quote
from urllib.request import urlopen

rev = sys.argv[1]
impact = "design/audit_impacts/reef-kart-visual-context-20261105.json"
repo = "Ebonyks/mermaid-roshan-reef"
ref = "refs/heads/codex/reef-kart-art-20261104"

def git_blob(path):
    return subprocess.check_output(["git", "show", f"{rev}:{path}"])

def verify(path):
    expected = git_blob(path)
    with urlopen(f"https://raw.githubusercontent.com/{repo}/{rev}/{quote(path)}", timeout=30) as response:
        got = response.read()
    assert got == expected, path
    return {"path": path, "bytes": len(got), "sha256": sha256(got).hexdigest()}

assert subprocess.check_output(["git", "ls-remote", "--exit-code", "origin", ref]).decode().split()[0] == rev
manifest = json.loads(git_blob(impact))
jobs = json.loads(git_blob("assets_src/imagegen/reef_kart_context_20261105/generation_jobs.json"))
choices = json.loads(git_blob("assets_src/imagegen/reef_kart_context_20261105/visual_decisions.json"))
references = [r["path"] for j in jobs["jobs"] for r in j["packet"]["source_motif_references"]]
references += [r["source"] for r in choices["extra_reuse"]]
references += [r["path"] for r in choices["decisions"]]
paths = sorted(set([impact] + manifest["files"] + references))
with ThreadPoolExecutor(max_workers=5) as pool:
    results = list(pool.map(verify, paths))
record = {"revision": rev, "ref": ref, "access": "anonymous public GitHub raw download",
          "checked_at": datetime.now().astimezone().isoformat(timespec="seconds"), "files": results}
record["payload_sha256"] = sha256("\n".join(r["path"]+"\0"+r["sha256"] for r in results).encode()).hexdigest()
record["impact_sha256"] = sha256(git_blob(impact)).hexdigest()
record["generation_manifest_sha256"] = sha256(git_blob("assets_src/imagegen/reef_kart_context_20261105/generation_jobs.json")).hexdigest()
out = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(__file__).with_name("remote-verification.json")
out.write_text(json.dumps(record, indent=2)+"\n", encoding="utf8")
print(rev, "anonymous byte matches:", len(results), record["checked_at"])
