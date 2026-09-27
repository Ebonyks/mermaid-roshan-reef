"""Verify the public, immutable bands packet with anonymous recipient access."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
PACKET = "assets_src/cinematics/battle_of_bands_2026-09-20"
REPOSITORY = "Ebonyks/mermaid-roshan-reef"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("commit")
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    if not re.fullmatch(r"[0-9a-f]{40}", args.commit):
        parser.error("commit must be a full 40-character lowercase Git SHA")
    base = f"https://raw.githubusercontent.com/{REPOSITORY}/{args.commit}/{PACKET}/"

    def fetch(path):
        request = urllib.request.Request(base + path, headers={"User-Agent": "Mermaid-Roshan-public-handoff-verifier"})
        with urllib.request.urlopen(request, timeout=60) as response:
            return response.read()

    manifest_bytes = fetch("ARCHIVE_MANIFEST.json")
    local_bytes = (ROOT / PACKET / "ARCHIVE_MANIFEST.json").read_bytes()
    if manifest_bytes != local_bytes:
        raise ValueError("Remote manifest bytes differ from the local content candidate")
    manifest = json.loads(manifest_bytes)

    def verify(entry):
        payload = fetch(entry["path"])
        actual = hashlib.sha256(payload).hexdigest()
        if actual != entry["sha256"]:
            raise ValueError(f"Remote hash mismatch: {entry['path']}")
        return {"path": entry["path"], "sha256": actual, "bytes": len(payload)}

    with ThreadPoolExecutor(max_workers=6) as pool:
        files = sorted(pool.map(verify, manifest["files"]), key=lambda item: item["path"])
    rows = "".join(f"{entry['sha256']}  {entry['path']}\n" for entry in files).encode()
    if hashlib.sha256(rows).hexdigest() != manifest["packet_payload_sha256"]:
        raise ValueError("Remote payload aggregate mismatch")
    receipt = {
        "content_commit": args.commit,
        "repository": REPOSITORY,
        "access_mode": "anonymous HTTPS; no GitHub credentials, cookies or Authorization header",
        "verified_at": datetime.now(timezone.utc).isoformat(),
        "entry": f"https://github.com/{REPOSITORY}/blob/{args.commit}/{PACKET}/README.md",
        "tree": f"https://github.com/{REPOSITORY}/tree/{args.commit}/{PACKET}",
        "manifest": base + "ARCHIVE_MANIFEST.json",
        "manifest_sha256": hashlib.sha256(manifest_bytes).hexdigest(),
        "packet_payload_sha256": manifest["packet_payload_sha256"],
        "verified_files": files,
        "publication": "PASS: exact public content bytes verified",
        "ARCHIVE_COMPLETE": False,
        "GENERATION_READY": False,
        "DELIVERY_ACCEPTED": False,
        "acceptance_gaps": "Recording/timecodes, clean first-frame approvals and shot binding review remain missing. Public access proves retrievability, not that Grok executed the jobs.",
    }
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_bytes((json.dumps(receipt, indent=2) + "\n").encode("utf-8"))
    print(f"PUBLIC HANDOFF PASS: {len(files)} payload files, manifest and aggregate verified at {args.commit}")


if __name__ == "__main__":
    main()
