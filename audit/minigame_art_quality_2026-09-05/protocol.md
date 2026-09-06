# Minigame art-quality baseline protocol

## Current reconciliation status

This packet began as a historical baseline against revision
`775ceee1b9f20118abec25ce933db292bb3c847e`. It is now reconciled on the clean
current-development base `f4a5de339f3a8b7b9e4081924f4d3127d54959d7` with
additional source repairs recorded in this packet. The registry and packet manifest bind
the recorded evidence bytes. Code-source records explicitly declare `hash_normalization: "utf8_lf"` to canonicalize CRLF to LF; all image and capture records use exact-byte hashes. Historical captures
and scores remain historical evidence only; they do not review or accept the
reconciled runtime. Current Mobile-renderer state captures and owner/device
review are still required before any 4.5 claim.

## Historical baseline method

This registry is an intentionally open inventory derived from `tmp/minigame-art-quality/opera_art_findings.json` and `tmp/minigame-art-quality/nonopera_inventory.json`. It enumerates all fifteen supplied Opera career surfaces and the known non-Opera families. It does not claim that every live raster, atlas cell, procedural layer, state, or indirect caller dependency is enumerated. `scope.coverage_complete` therefore remains `false`.

The supplied revision `775ceee1b9f20118abec25ce933db292bb3c847e` was recorded as the historical comparison base. At baseline time, the registry and candidate work were uncommitted. Every baseline `source.sha256` described the named file as it existed in that baseline worktree. The hash proved those bytes only. It did not prove that the bytes belonged to the base revision or that a runtime capture was generated from them. The reconciled registry now refreshes changed-source hashes against the current worktree while preserving that same limitation: exact Git and capture linkage must come from the canonical same-process fresh-runtime evidence contract.

Each entry currently represents a surface implementation and its procedural-art source. It is not yet an exhaustive raster asset ledger. This distinction matters for surfaces that load art indirectly. The next inventory pass must expand each surface into its live backgrounds, actors and atlas cells, props, targets, pointers, cards, foregrounds, shadows, and effects, each with an exact current path and SHA-256.

No preliminary family score was converted into eight dimension scores. A single family number or isolated-image impression cannot truthfully populate identity, finish, edges, readability, animation, ownership, consistency, and technical review. Candidate reviews remain `null`; external or historical screenshots were omitted because they are not imported, repository-relative, hashed, and bound to the declared runtime candidate.

Defects preserve the actionable source findings and named weak renderer functions in concise form. They are open blockers rather than accepted diagnoses of every rendered state. In particular, source-only concern, historical byte-equivalence, or an isolated image inspection does not prove runtime composition, animation, touch alignment, contact, or device readability.

Validation modes:

```text
python tools/audit_minigame_art_quality.py --validate-only
python tools/audit_minigame_art_quality.py --check
```

`--validate-only` should return zero when the JSON, paths, hashes, and declarations are internally sound while printing `UNSATISFIED`. `--check` must return nonzero until coverage is complete, every declared live asset has a complete current state-bound review at or above 4.5 in every applicable dimension, all blocking defects are resolved, and required evidence is present. Neither command auto-scores pixels.

For each repair batch, first add the exact live asset inventory and failing state evidence. Reuse approved art when it fits. Record a replacement only after its output exists and its current hash can populate `replacement_history`; do not predeclare a generated candidate. Re-run validation, focused checks, and state capture after each bounded family, and keep the global result open until a clean second audit finds no omitted live assets.
