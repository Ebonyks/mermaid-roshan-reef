#!/usr/bin/env python3
"""Regenerate the Grok animation package SHA-256 inventory."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
INVENTORY = PACKAGE_ROOT / "PACKAGE_INVENTORY_SHA256.csv"


def sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as handle:
		for chunk in iter(lambda: handle.read(1024 * 1024), b""):
			digest.update(chunk)
	return digest.hexdigest()


def main() -> None:
	files = sorted(
		(path for path in PACKAGE_ROOT.rglob("*") if path.is_file() and path != INVENTORY),
		key=lambda path: path.relative_to(PACKAGE_ROOT).as_posix(),
	)
	with INVENTORY.open("w", newline="", encoding="utf-8") as handle:
		writer = csv.writer(handle, quoting=csv.QUOTE_ALL, lineterminator="\n")
		writer.writerow(("relative_path", "bytes", "sha256"))
		for path in files:
			writer.writerow(
				(
					path.relative_to(PACKAGE_ROOT).as_posix(),
					path.stat().st_size,
					sha256(path),
				)
			)
	print(f"WROTE: {INVENTORY} ({len(files)} files)")


if __name__ == "__main__":
	main()
