"""Download the verified review packet from an immutable GitHub manifest URL."""
from argparse import ArgumentParser
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
from pathlib import Path
from urllib.parse import quote, urlsplit
from urllib.request import urlopen
import json
import re
import time

def read(url):
    for attempt in range(3):
        try:
            with urlopen(url, timeout=35) as response:
                return response.read()
        except OSError:
            if attempt == 2:
                raise
            time.sleep(1 + attempt)

def download(manifest_url, dest):
    url = urlsplit(manifest_url)
    if (url.scheme != "https" or url.netloc != "raw.githubusercontent.com" or
            not re.fullmatch(r"/[^/]+/[^/]+/[0-9a-f]{40}/.+/manifest\.json", url.path)):
        raise ValueError("Use the raw GitHub manifest URL pinned to a full commit.")
    raw_manifest = read(manifest_url)
    manifest = json.loads(raw_manifest)
    base = manifest_url.rsplit("/", 1)[0]
    dest = dest.resolve()
    dest.mkdir(parents=True, exist_ok=True)
    rows = sorted(manifest["files"], key=lambda row: row["path"])
    seen = set()
    for row in rows:
        name = row["path"]
        if name in seen or "\\" in name or not (dest / name).resolve().is_relative_to(dest):
            raise ValueError(f"Unsafe or duplicate packet path: {name}")
        seen.add(name)
    aggregate = sha256("".join(f'{row["sha256"]}  {row["path"]}\n' for row in rows).encode()).hexdigest()
    if aggregate != manifest["payload_sha256"]:
        raise ValueError("Manifest payload digest mismatch.")
    def fetch(row):
        name = row["path"]
        data = read(base + "/" + quote(name, safe="/"))
        if len(data) != row["bytes"] or sha256(data).hexdigest() != row["sha256"]:
            raise ValueError(f"Remote byte check failed for {name}")
        target = dest / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    with ThreadPoolExecutor(max_workers=8) as pool:
        list(pool.map(fetch, rows))
    (dest / "manifest.json").write_bytes(raw_manifest)
    print(f"Verified anonymous GitHub access for {len(rows)} files. Payload SHA-256 {aggregate}")

if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("manifest_url")
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    download(args.manifest_url, args.destination)
