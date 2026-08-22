# Grok Project architecture for an hour-plus series

## Permanent Project library

Keep these always searchable inside the Project:

- Project Constitution;
- Style Bible and base-video style set;
- Cast Registry;
- one folder per character;
- one folder per recurring location;
- one folder per recurring vehicle/prop family;
- approved output index;
- rejected-output index with failure reasons;
- templates.

This material defines the series but is not automatically attached to every generation.

## Production hierarchy

```text
SERIES
  episode_or_special
    sequence
      scene
        shot
          attempts
```

Suggested IDs:

- Episode: `E001`, `E002` …
- Special/cinematic: `SP001`
- Sequence: `SQ010`, `SQ020` …
- Scene: `SC010`
- Shot: `SH010`

Filename example:

`E003_SQ020_SC010_SH040_video_a03_APPROVED.mp4`

## Agent/work-area model

Use parallel agents only for independent tasks:

- character turnaround candidate;
- location anchor still;
- prop sheet;
- style comparison;
- continuity review of already-generated material.

Do not parallelize adjacent shots in the same acting chain. After anchor selection, one sequential workstream owns that scene's dependent shots.

## Reference pack per shot

Each generation should have a tiny declared pack:

1. `START_FRAME` when continuing action;
2. primary character authority;
3. secondary character authority if present;
4. location authority;
5. one or two base-video style stills.

Stay below seven references and normally use three to five. The prompt must state the authority domain of each image.

## Long-form assembly

Grok's 15-second limit is a shot-generation limit, not a story-length limit. Build episodes externally from short accepted shots. Create a module-level timeline and ledger for every sequence. For scenes longer than 15 seconds, preserve continuity through accepted ending frames, match cuts, repeated authority packs and external editorial assembly.

## Versioning

- Canonical character revisions increment major versions: `ROSHAN_IDENTITY_v02`.
- Pose/expression additions increment minor versions without replacing identity: `ROSHAN_EXPRESSIONS_v01`.
- A new approved version never silently deletes the previous version.
- Every sequence records which authority version it used.
