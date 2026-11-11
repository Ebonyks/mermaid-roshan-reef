"""Verify each required packet file and the deterministic payload digest."""
from hashlib import sha256
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent

def verify(root):
    manifest = json.loads((root / "manifest.json").read_bytes())
    summary = []
    names = set()
    for row in sorted(manifest["files"], key=lambda item: item["path"]):
        name = row["path"]
        path = (root / name).resolve()
        if name in names or not path.is_relative_to(root.resolve()):
            raise ValueError(f"Invalid manifest path {name}")
        names.add(name)
        data = path.read_bytes()
        actual = sha256(data).hexdigest()
        if len(data) != row["bytes"] or actual != row["sha256"]:
            raise ValueError(f"Size or SHA-256 mismatch for {name}")
        summary.append(f"{actual}  {name}\n")
    aggregate = sha256("".join(summary).encode()).hexdigest()
    if aggregate != manifest["payload_sha256"]:
        raise ValueError("Packet digest mismatch")
    print(f"Verified {len(names)} payload files: {aggregate}")
    return manifest

if __name__ == "__main__":
    verify(ROOT)
