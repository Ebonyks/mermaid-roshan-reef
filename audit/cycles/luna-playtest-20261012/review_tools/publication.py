"""Seal the study payload and verify every byte anonymously from immutable GitHub."""
from pathlib import Path, PurePosixPath
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor
import argparse, hashlib, json, subprocess, time
from urllib.request import Request, urlopen
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[4]
PREFIX = "audit/cycles/luna-playtest-20261012/"
CYCLE = ROOT / PREFIX
REPO = "Ebonyks/mermaid-roshan-reef"
MANIFEST = CYCLE / "MANIFEST.json"
RECEIPT = CYCLE / "verification/remote_publication.json"
GLOBAL = {".gitattributes", "ASSET_LICENSES.md", "audit/MASTER_AUDIT_2026-08-09.md", "audit/MASTER_AUDIT_CHANGELOG_ROLLBACK_2026-08-10.md", "audit/cycles/README.md", "audit/findings/ACTIVE_FINDINGS_2026-08-13.md", "design/05_DOC_LEDGER.md", "design/audit_impacts/luna-playtest-20261012.json"}

def digest(data):
    return hashlib.sha256(data).hexdigest()

def allowed(path):
    parsed = PurePosixPath(path)
    return not parsed.is_absolute() and ".." not in parsed.parts and "\\" not in path and (path.startswith(PREFIX) or path in GLOBAL)

def fetch(revision, path):
    if not allowed(path):
        raise ValueError("Remote path outside authorized study payload")
    url = f"https://raw.githubusercontent.com/{REPO}/{revision}/{quote(path, safe='/')}"
    for attempt in range(3):
        try:
            with urlopen(Request(url, headers={"User-Agent": "Reef-Luna-audit-byte-verifier"}), timeout=45) as response:
                return response.read()
        except Exception:
            if attempt == 2:
                raise
            time.sleep(1 + attempt)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seal", action="store_true")
    parser.add_argument("--check-index", action="store_true")
    parser.add_argument("--revision")
    parser.add_argument("--receipt", type=Path, default=RECEIPT)
    args = parser.parse_args()
    if args.check_index:
        manifest = json.loads(MANIFEST.read_bytes())
        rows = manifest['files'] + [{'path': MANIFEST.relative_to(ROOT).as_posix(), 'bytes': MANIFEST.stat().st_size, 'sha256': digest(MANIFEST.read_bytes())}]
        request = ''.join(':' + row['path'] + '\n' for row in rows).encode('utf-8')
        proc = subprocess.run(['git', 'cat-file', '--batch'], input=request, capture_output=True, cwd=ROOT, check=True)
        offset = 0
        for row in rows:
            end = proc.stdout.index(b'\n', offset)
            header = proc.stdout[offset:end].split()
            if len(header) != 3 or header[1] != b'blob':
                raise ValueError('Missing staged payload: ' + row['path'])
            size = int(header[2]); offset = end + 1
            raw = proc.stdout[offset:offset + size]; offset += size + 1
            if size != row['bytes'] or digest(raw) != row['sha256']:
                raise ValueError('Index would change sealed bytes: ' + row['path'])
        print(json.dumps({'status': 'PASS', 'staged_payload_and_manifest_blobs': len(rows)}))
        return
    if args.seal:
        sessions = json.loads((CYCLE / "verification/sessions.json").read_text(encoding="utf-8"))
        if sessions["status"] != "PASS" or sessions["completed_valid_sessions"] != 57:
            raise ValueError("Cannot seal a planned or incomplete reviewer cohort")
        files = [p for p in CYCLE.rglob("*") if p.is_file() and p not in [MANIFEST, RECEIPT] and "__pycache__" not in p.parts]
        files += [ROOT / p for p in GLOBAL]
        payload = [{"path": p.relative_to(ROOT).as_posix(), "bytes": p.stat().st_size, "sha256": digest(p.read_bytes())} for p in sorted(files)]
        canonical = "".join(f"{r['path']}\t{r['bytes']}\t{r['sha256']}\n" for r in sorted(payload, key=lambda r: r["path"]))
        data = {"schema": "luna_study_publication_manifest/1", "repository": REPO, "branch": "codex/luna-playtest-20261012", "baseline": sessions["baseline"],
                "study_status": "REVIEW_COMPLETE", "actual_luna_reviews": 57, "access_mode": "anonymous HTTPS, no authentication headers",
                "packet_payload_sha256": digest(canonical.encode("utf-8")), "payload_hash_definition": "Sorted UTF-8 path TAB decimal bytes TAB lowercase SHA-256 LF for each payload file.",
                "excluded_attestation_metadata": [MANIFEST.relative_to(ROOT).as_posix(), RECEIPT.relative_to(ROOT).as_posix()],
                "exclusion_reason": "Manifest cannot include its own hash; post-publication attestation is written only after remote bytes are checked. Neither exclusion grants gameplay/child/device acceptance.",
                "byte_preservation": "Study subtree is -text in .gitattributes so native logs/reports retain literal bytes. Affected canonical text documents were serialized as UTF-8 LF before sealing; index blobs must match every sealed local payload before push.",
                "files": payload}
        MANIFEST.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"payload_files": len(payload), "payload_sha256": data["packet_payload_sha256"], "manifest_sha256": digest(MANIFEST.read_bytes())}))
        return
    if not args.revision or len(args.revision) != 40 or any(c not in "0123456789abcdef" for c in args.revision):
        raise ValueError("Exact immutable 40-character Git revision required")
    expected_bytes = MANIFEST.read_bytes()
    remote_bytes = fetch(args.revision, MANIFEST.relative_to(ROOT).as_posix())
    if remote_bytes != expected_bytes:
        raise ValueError("Remote manifest bytes differ from sealed local payload")
    manifest = json.loads(remote_bytes)
    if manifest["repository"] != REPO or manifest["actual_luna_reviews"] != 57:
        raise ValueError("Unexpected manifest repository/count")
    def verify(row):
        raw = fetch(args.revision, row["path"])
        if len(raw) != row["bytes"] or digest(raw) != row["sha256"]:
            raise ValueError("Remote file bytes/hash mismatch: " + row["path"])
        return row
    with ThreadPoolExecutor(max_workers=6) as pool:
        rows = list(pool.map(verify, manifest["files"]))
    result = {"schema": "luna_study_remote_verification/1", "status": "PUBLIC_BYTES_VERIFIED", "repository": REPO, "revision": args.revision,
              "checked_utc": datetime.now(timezone.utc).isoformat(), "access_mode": "anonymous HTTPS, no GitHub token/cookie/authorization header",
              "payload_files_verified": len(rows), "manifest_sha256": digest(remote_bytes), "packet_payload_sha256": manifest["packet_payload_sha256"],
              "entry_url": f"https://github.com/{REPO}/tree/{args.revision}/{PREFIX}",
              "manifest_url": f"https://raw.githubusercontent.com/{REPO}/{args.revision}/{MANIFEST.relative_to(ROOT).as_posix()}",
              "helper_sha256": digest(Path(__file__).read_bytes()), "files": rows,
              "scope": "Immutable public audit payload and all references in its file inventory; no receipt of messages by a person, gameplay release, full-route, device, child or owner acceptance."}
    if args.receipt.exists():
        previous = json.loads(args.receipt.read_text(encoding="utf-8"))
        if previous.get("status") != "PENDING":
            raise ValueError("Preserve prior remote verification; choose a new receipt path")
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k != "files"}))

if __name__ == "__main__":
    main()
