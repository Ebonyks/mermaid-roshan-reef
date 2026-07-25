# Claude START HERE - Opera job asset access and regeneration handoff

Date: 2026-07-24

## Task

Make the complete accepted Opera House non-boss job-art package available in
your Claude worktree, then use it to regenerate or promote production-quality
asset references and build the continuous 2.5D job worlds described in the
2026-07-24 companion handoff.

Do not rely on a Codex worktree path, a chat attachment, or an external
generated-image cache. All usable source material is tracked in this Git
repository. Use repository-relative paths only.

This handoff covers twelve jobs and excludes all boss fights:

- Floor 1: Pastry Chef, Detective, Ballerina, Candy Maker.
- Floor 2: Doctor, Farmer, Boxer, Magician.
- Floor 3: Painter, Astronaut Engineer, Racecar Driver, Pop Star.
- Deferred: Curtain Dragon, Shadow Phantom, Midnight Maestro.

## Binding spatial correction

The twelve regular jobs are short 2.5D side-scrolling story worlds, not
mechanics placed on twelve literal theatre stages. Use
`CLAUDE_OPERA_JOB_2P5D_CONTINUATION_2026-07-24.md` as the authoritative
environment and level-layout guide.

The package at `assets_src/concepts/opera_jobs_2p5d_2026-07-24/` supplies one
wide world key and one large-module/background-texture kit per job. The older
36-sheet and 576-card package remains authoritative for outfits, implements,
mechanic states, and close-up modeling detail.

Literal stages are reserved for the future boss phase. This handoff does not
authorize Curtain Dragon, Shadow Phantom, or Midnight Maestro production.

## Why the art may have appeared unavailable

The accepted package first entered Git in commit
`203af2e4c16be64fb2722d7b663e9b64bbae8756`. It is present in current
`origin/dev` and was reverified there on 2026-07-24.

The package contains ordinary tracked PNG files. It does not use Git LFS.
`assets_src/.gdignore` prevents Godot from importing source concepts into the
game build; it does not hide the files from Git, Claude, PowerShell, or image
inspection tools.

At handoff time the tracked package contains:

- 36 accepted 4 x 4 source sheets;
- 576 accepted individual reference cards;
- 1 prompt/provenance record;
- 613 tracked files under the package root in total.

If these files are absent, the Claude worktree is stale, was created from the
wrong branch, or uses a sparse checkout that omitted `assets_src`. Do not
substitute memory, thumbnails, or similarly named assets.

## Required access recovery

Start a fresh task branch from current `origin/dev`, following `AGENTS.md`.
Never commit directly to local `dev` or `master`.

```powershell
git fetch origin
git switch -c claude/opera-job-assets-regeneration origin/dev
git rev-parse HEAD
```

If the current worktree must be retained, merge current `origin/dev` into that
feature branch after preserving its work. Do not rebase shared work and do not
force-push.

Check for sparse checkout:

```powershell
git sparse-checkout list
```

If sparse checkout is active and omits the source package, either disable it in
the isolated feature worktree or explicitly include these repository paths:

```text
assets_src/concepts/opera_jobs_flat_2026-07-21
audit
tools
```

Then verify the package directly:

```powershell
$root = "assets_src/concepts/opera_jobs_flat_2026-07-21"
Test-Path "$root/PROMPTS.md"
Test-Path "$root/pastry_chef_outfit_sheet_2026-07-21.png"
Test-Path "$root/cards/opera_job_pastry_chef_outfit_hero_front_three_quarter.png"
(Get-ChildItem "$root" -Filter "*_sheet_2026-07-21.png" -File).Count
(Get-ChildItem "$root/cards" -Filter "*.png" -File).Count
```

The last two commands must report `36` and `576`. If they do not, stop asset
work and correct the branch or checkout. Do not generate against an incomplete
family.

## Repository-visible source map

Use these paths exactly:

| Purpose | Repository-relative path |
| --- | --- |
| Accepted package root | `assets_src/concepts/opera_jobs_flat_2026-07-21/` |
| Accepted 2.5D environment package | `assets_src/concepts/opera_jobs_2p5d_2026-07-24/` |
| Individual 1024 references | `assets_src/concepts/opera_jobs_flat_2026-07-21/cards/` |
| Exact prompt contracts and cell lists | `assets_src/concepts/opera_jobs_flat_2026-07-21/PROMPTS.md` |
| Exact 576-item manifest | `audit/opera_job_flat_prototype_ledger_2026-07-21.csv` |
| 36-sheet contact sheet | `audit/opera_job_flat_contact_sheet_2026-07-21.png` |
| Accepted scores and corrections | `OPERA_JOB_FLAT_ART_AUDIT_2026-07-21.md` |
| Scope and sheet inventory | `OPERA_JOB_FLAT_PROTOTYPE_PLAN_2026-07-21.md` |
| Authoritative 2.5D world guide | `CLAUDE_OPERA_JOB_2P5D_CONTINUATION_2026-07-24.md` |
| Older outfit and implement guide | `CLAUDE_OPERA_JOB_3D_CONTINUATION_2026-07-21.md` |
| 2.5D environment ledger | `audit/opera_job_2p5d_environment_ledger_2026-07-24.csv` |
| 2.5D environment contact sheet | `audit/opera_job_2p5d_contact_sheet_2026-07-24.png` |
| 2.5D art audit | `OPERA_JOB_2P5D_ART_AUDIT_2026-07-24.md` |
| Existing deterministic card packer | `tools/slice_opera_job_prototypes.py` |

The external `exec-*.png` names in `PROMPTS.md` are provenance records only.
Those raw cache files are not required and may not be accessible to Claude.
The accepted sheets and cards in the repository are the visual source of
truth.

## Resolution truth and regeneration decision

Every accepted individual card currently has a 1024 x 1024 PNG canvas and
preserves the approved design. The current cards were deterministically
rendered from accepted sheet cells so that the owner-approved composition,
silhouette, palette, and object state did not drift.

There are two valid paths:

### Path A - use the accepted cards directly

Use this when Claude can read the repository PNGs and they contain enough
information for modeling. This is the preferred path for objects whose shape,
materials, front/side relationship, and mechanic states are already clear.

Do not regenerate merely to make the art more realistic. The accepted style is
flat, rounded, storybook-cel concept art designed for translation into a
mobile-safe toy-diorama world.

### Path B - regenerate native-detail 1024 references

Use this only when an object needs genuinely new native detail, an additional
modeling angle, or a cleaner isolated presentation. Regeneration must use the
accepted card and its full accepted sheet as image references. It must not
reinterpret the design from text alone.

Each regenerated individual asset must be generated natively at 1024 x 1024 or
higher and delivered as a 1024 x 1024 PNG. Do not generate at 256 and upscale.
Do not crop a 1024-wide 4 x 4 sheet and claim that its 256-wide native cell is
a native 1024 asset.

Important: `tools/slice_opera_job_prototypes.py` is a preservation packer for
the accepted sheets. It intentionally normalizes a whole sheet to 1024 before
slicing and then renders each cell to 1024. Do not use it as the native-detail
regeneration pipeline without first changing that behavior and documenting the
change. For native-detail work, generate individual cards directly, or create
a 4096 x 4096 sheet whose sixteen cells are each truly 1024 and use a new
non-normalizing slicer.

## Regeneration style contract

Use the exact shared and job-specific prompts recorded in
`assets_src/concepts/opera_jobs_flat_2026-07-21/PROMPTS.md`, with these binding
requirements:

- Flat 2D concept illustration, not a Blender render and not photorealism.
- Rounded, modelable toy-diorama forms.
- Confident navy-purple outlines.
- Aqua and lavender shadow shapes.
- Coral, teal, cream, and plum base palette.
- Restrained brushed gold, pearl, and shell accents.
- Clear silhouette and function at phone size.
- No words, letters, numbers, logos, or watermarks.
- No copied franchise symbols, characters, scenery, or UI.
- No generic star mascot repeated as filler.
- No boss content in this phase.
- No punitive fail imagery, injury, or frightening response.
- No clipped objects, repeated filler, malformed anatomy, or micro-detail.
- Roshan remains a mermaid with her continuous rainbow-scaled tail and split
  fin. Never add human legs, shoes, or boots.
- Preserve Roshan's face, long brown hair, vivid rainbow streak, and warm brown
  eyes. Omit the backpack and its printed imagery.

When regenerating one card, supply both of these references:

1. the existing individual card from `cards/`; and
2. its `source_sheet` from the CSV ledger.

The individual card locks content and silhouette. The whole sheet locks family
palette, line weight, relative scale, and finish.

## Hard continuity locks

Reject a result immediately if any of these rules drift:

- Doctor: the patient is always the same coral five-armed starfish plush.
  Never substitute a bear, rabbit, axolotl, ordinary fish, or four-limbed
  creature.
- Painter: every order cue is plum first, coral second, cream third.
- Magician: the reveal creature is a finned bunny-fish with rabbit ears, not a
  land rabbit.
- Astronaut Engineer: pipe shapes are straight, elbow, and ring, each with its
  matching socket. Propulsion and exhaust are bubbles, never flame.
- Racecar Driver: the kart has an open mermaid-tail-safe channel and bubble
  exhaust.
- Farmer: keep the tested 2D piggy mechanic and its five foods; regenerated art
  does not authorize replacing the timing system.
- Ballerina: tile identity pairs color and icon: coral shell, teal wave, plum
  ribbon, cream pearl.
- Pop Star: directions pair with the accepted color mapping; do not replace the
  live DanceEngine.
- Boxer: targets are friendly training imps with soft bubble impacts, not
  injured enemies.
- All jobs: retry is gentle, reversible, and non-punitive.

## Complete 36-sheet manifest

Every job requires exactly three sheet families. These existing files are the
accepted family references and the required scope for any regeneration pass.
Files named `stage_states` remain valid mechanic-state and timing references;
they are not the spatial layout for the 2.5D worlds.

| Job prefix | Outfit reference | Gameplay reference | Stage/state reference |
| --- | --- | --- | --- |
| `pastry_chef` | `pastry_chef_outfit_sheet_2026-07-21.png` | `pastry_chef_gameplay_sheet_2026-07-21.png` | `pastry_chef_stage_states_sheet_2026-07-21.png` |
| `detective` | `detective_outfit_sheet_2026-07-21.png` | `detective_gameplay_sheet_2026-07-21.png` | `detective_stage_states_sheet_2026-07-21.png` |
| `ballerina` | `ballerina_outfit_sheet_2026-07-21.png` | `ballerina_gameplay_sheet_2026-07-21.png` | `ballerina_stage_states_sheet_2026-07-21.png` |
| `candy_maker` | `candy_maker_outfit_sheet_2026-07-21.png` | `candy_maker_gameplay_sheet_2026-07-21.png` | `candy_maker_stage_states_sheet_2026-07-21.png` |
| `doctor` | `doctor_outfit_sheet_2026-07-21.png` | `doctor_gameplay_sheet_2026-07-21.png` | `doctor_stage_states_sheet_2026-07-21.png` |
| `farmer` | `farmer_outfit_sheet_2026-07-21.png` | `farmer_gameplay_sheet_2026-07-21.png` | `farmer_stage_states_sheet_2026-07-21.png` |
| `boxer` | `boxer_outfit_sheet_2026-07-21.png` | `boxer_gameplay_sheet_2026-07-21.png` | `boxer_stage_states_sheet_2026-07-21.png` |
| `magician` | `magician_outfit_sheet_2026-07-21.png` | `magician_gameplay_sheet_2026-07-21.png` | `magician_stage_states_sheet_2026-07-21.png` |
| `painter` | `painter_outfit_sheet_2026-07-21.png` | `painter_gameplay_sheet_2026-07-21.png` | `painter_stage_states_sheet_2026-07-21.png` |
| `astronaut_engineer` | `astronaut_engineer_outfit_sheet_2026-07-21.png` | `astronaut_engineer_gameplay_sheet_2026-07-21.png` | `astronaut_engineer_stage_states_sheet_2026-07-21.png` |
| `racecar_driver` | `racecar_driver_outfit_sheet_2026-07-21.png` | `racecar_driver_gameplay_sheet_2026-07-21.png` | `racecar_driver_stage_states_sheet_2026-07-21.png` |
| `pop_star` | `pop_star_outfit_sheet_2026-07-21.png` | `pop_star_gameplay_sheet_2026-07-21.png` | `pop_star_stage_states_sheet_2026-07-21.png` |

All paths in this table are relative to
`assets_src/concepts/opera_jobs_flat_2026-07-21/`.

The CSV ledger is the authoritative manifest for the sixteen assets within
each sheet. Do not infer cell names or order from appearance.

## Safe output and promotion workflow

Do not overwrite the accepted package while experimenting.

Stage regeneration candidates under:

```text
assets_src/concepts/opera_jobs_flat_regeneration_2026-07-24/
  cards/
  contact_sheets/
  PROMPTS.md
  REGENERATION_LEDGER.csv
```

Use the same `asset_id` filenames as the accepted ledger inside the candidate
`cards/` folder. Record for every candidate:

- `asset_id`;
- job and sheet family;
- accepted reference path;
- prompt revision;
- generation identifier;
- native generation dimensions;
- audit score;
- status: `candidate`, `rejected`, or `accepted`;
- rejection reason when applicable.

After the complete candidate set passes audit, promote only accepted files into
the existing `cards/` paths in one controlled commit. Preserve rejected
candidates only in a clearly marked nonshipping audit area if they are useful;
otherwise leave them outside Git. Do not keep multiple ambiguous production
versions with names such as `final2` or `better`.

If whole accepted sheets are regenerated, promote them only after all sixteen
cells pass together. Rebuild the contact sheet and ledger in the same commit.
Do not silently mix a new whole sheet with old card exports.

## Audit and automatic rejection

The computer audit maximum is 4.9/5. Every regenerated sheet or individual
card must score at least 4.5. Target 4.7 or higher to match the existing pack.

Score each candidate on:

| Dimension | Weight | Passing condition |
| --- | ---: | --- |
| Style and palette consistency | 25% | Belongs beside the accepted Opera House family |
| Child-readable silhouette | 20% | Function is clear at phone scale |
| Job and mechanic continuity | 20% | Matches the shipped activity and exact state |
| Roshan identity or prop cohesion | 15% | Identity is preserved and parts share one language |
| Modelability and mobile practicality | 10% | Rounded construction without fragile detail |
| Completeness and uniqueness | 10% | Correct asset, uncropped, no duplicate filler |

Automatically reject:

- score below 4.5;
- wrong job or mechanic;
- boss content;
- realistic rendering;
- changed Roshan identity or anatomy;
- human legs on Roshan;
- wrong species or object state;
- text-heavy signage;
- copied third-party imagery;
- clipped asset or missing part;
- repeated filler;
- dominant off-palette treatment;
- detail too intricate to reproduce efficiently in Mobile-renderer 3D.

Review candidates at native resolution, at thumbnail size, beside the accepted
card, beside the full family sheet, and in a combined contact sheet. A card can
be attractive and still fail if it weakens family consistency or modelability.

## Adding accepted art to Git

Every accepted addition or replacement must include:

1. the 1024 x 1024 PNG;
2. its prompt/provenance update;
3. its ledger row and score;
4. the regenerated contact sheet;
5. an `ASSET_LICENSES.md` entry stating OpenAI-generated project concept art,
   the generation date, and modifications;
6. a short audit note describing replacements and rejections.

Before committing, confirm:

```powershell
git status --short
git diff --check
```

Because the concept package is under `.gdignore`, Godot should not import the
source PNGs. Still run the repository gates required by `AGENTS.md` before
integration. Push the Claude feature branch, wait for the exact branch SHA to
pass CI, reconcile current `origin/dev`, then fast-forward the completed work
into `dev`. Never push `master`.

## Transition to 3D

After accepted references are available locally, continue with
`CLAUDE_OPERA_JOB_2P5D_CONTINUATION_2026-07-24.md`.

That guide is binding for:

- lobby as the primary navigation stage;
- visible, pictorial upper-floor locks;
- four career doors per floor;
- continuous left-to-right job districts;
- foreground, playable midground, scenic midground, and far parallax layers;
- large route modules, landmarks, background bands, and material textures;
- literal stages reserved for future boss fights;
- scale relative to the live Roshan avatar;
- pivots, node names, materials, touch targets, and collisions;
- Speedy-tier transparency and particle budgets;
- the exact mechanic sequence for every job.

Do not begin mass modeling from prompt text alone. Complete one vertical slice
per job in this order:

1. accepted outfit silhouette or wardrobe display;
2. primary touch target;
3. required state swaps;
4. nonverbal guidance and gentle retry;
5. completion/reward state;
6. scenic dressing;
7. actual Mobile-renderer gameplay-camera review.

## Required Claude delivery report

When the regeneration and 3D handoff phase is complete, report:

- branch and exact commit SHA;
- whether access recovery was required and how it was resolved;
- number of accepted references reused without regeneration;
- number regenerated, rejected, and accepted;
- confirmation that every delivered raster is at most 1024px on its longest
  side, with environment keys at 1024 x 576 and square cards/kits at
  1024 x 1024;
- per-job asset counts;
- minimum, maximum, and mean audit score;
- list of promoted repository paths;
- list of intentionally deferred assets;
- Blender collection and GLB paths, if 3D work was also completed;
- Godot scene and integration paths;
- license and provenance updates;
- exact CI run URL and result.

Do not report the task complete if any job family is missing, any accepted
candidate scores below 4.5, or the exact delivery SHA has not passed the
repository gates.
