# GitHub delivery layout

Game repo: protocol, shot plans, prompts, reference metadata, requests and QC.
Private `Ebonyks/mermaid-roshan-grok-videos`: actual images, boards and media;
visual packet under `assets_src/cinematics/grok_v2_repaired_2026-09-19/`.
No private media is republished into the public game repository.

Repair branch: `codex/grok-v2-repairs-20260919`. The former
`codex/grok-handoff-v2` entry receives a forward pointer without rewriting history.
PUBLICATION.json records immutable links and verification. Local staging never
counts as delivery.

The packet contains supplied references and historical boards; newly approved
dirty masters, ensemble identity, turnarounds and complete openings remain explicit
gaps, not invented files. Exchange remains
`exchange/attempts/<SHOT_ID>/A00N/{REQUEST,RETURN,REVIEW}.json`.
Never overwrite attempts, reset caps silently, or infer recipient access from
Codex authentication. Coverage returns have their own COV-* job IDs.
