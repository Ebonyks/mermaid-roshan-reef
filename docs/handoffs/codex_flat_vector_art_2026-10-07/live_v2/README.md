# Current Castle and Opera visual evidence — R2

This is a **partial current visual inventory**, not the completed full-game weakness audit. The zero-flat-vector-art goal remains active. No replacement pixels, runtime integration or artistic acceptance are delivered here.

[Source audit and register](../README.md) · [Current observations](observations.json) · [All route coverage](coverage.json) · [Drawing-scope review](scope_review.json) · [Machine evidence](MACHINE.json) · [Capture launch and derivation](CAPTURE_LAUNCH.json).

Current production source is frozen at `44a36776ab3db0d9078aacf09eca144fde342330`; it is unchanged from runtime baseline `92c9fe70319ef46bfaa8f61348a6f51512141ec3`. Fresh `origin/dev` at `4c9235a6862834d7dbeb09615404e0cb4b47b82a` adds only a non-runtime Halloween concept.

## What was actually captured

The approved Godot 4.7.2-stable official.ed1daf0bf Windows build rendered the actual project with Vulkan **Mobile**, **Speedy** quality, and the real same-process viewport at both **1280×720** and **1600×720**. The desktop GPU was an RTX 3060 Ti. Each aspect has 96 images: eight Castle room routes, three staged positions in the painted Opera venue, all 15 free-play career entries, and 70 actual open phases.

The static source table has 61 phases; production `OperaPerformancePlan` expands Ballet to six, Magician to eight and Pop Star to seven, adding nine live phases. Neither 61 nor 70 is the game-wide state denominator.

The harness invokes the guarded shipping route callback for career entry, then directly selects each phase and calls production arm/open methods. Unlocks and phase selection are **declared fixtures**, not natural child actions, intentional wins or save-resume tests. It freezes the process for individual captures. Castle route views suppress the ordinary main HUD, while the route/message surfaces remain; they do not establish full HUD review.

The window is positioned offscreen; the renderer is Windows Mobile, **not headless**. Each run/aspect uses a fresh isolated `SaveState` path before Main enters the tree. Normal child-save and backup hashes match before/after. Audio uses Dummy; these images supply no voice/sound verification.

## Review boards

Each board is a layout derivative of exact 1280×720 capture PNGs, scaled by Lanczos to 640×360 panels with audit captions. No source character, room or prop artwork is edited. Native captures at both aspects remain separately available under their aspect directories, with per-state dimensions, byte lengths and SHA-256 in each `opera_capture_manifest.json`.

### Castle And Venue

![Current castle_and_venue review](contacts/castle_and_venue.png)

### Chef

![Current chef review](contacts/chef.png)

### Detective

![Current detective review](contacts/detective.png)

### Ballerina

![Current ballerina review](contacts/ballerina.png)

### Candymaker

![Current candymaker review](contacts/candymaker.png)

### Doctor

![Current doctor review](contacts/doctor.png)

### Farmer

![Current farmer review](contacts/farmer.png)

### Boxer

![Current boxer review](contacts/boxer.png)

### Magician

![Current magician review](contacts/magician.png)

### Painter

![Current painter review](contacts/painter.png)

### Astronaut

![Current astronaut review](contacts/astronaut.png)

### Racer

![Current racer review](contacts/racer.png)

### Popstar

![Current popstar review](contacts/popstar.png)

### Nursery

![Current nursery review](contacts/nursery.png)

### Geologist

![Current geologist review](contacts/geologist.png)

### Teacher

![Current teacher review](contacts/teacher.png)

## What remains open

All 176 overlapping declared route entries remain incomplete. Twenty-four stage rows now have a partial static slice; zero has complete ready/action/change/payoff/settle/re-entry/pause/save/fallback coverage. Chapter 2 story adapters, Day One, other rooms/worlds, full UI, dynamic art, random answers, repeated instances and raster lookalikes need further review. Eighteen drawing scopes have current partial context evidence; **all 369 remain unresolved** for complete object/helper/loop/variant disposition. The source register remains a 224 named-family lower bound. Individual-art totals, instances and regressions remain unknown.

Current observations confirm flat cave/workbench and learning-board materials, free-play Chef oven/batter/cake, first-person boxing gloves, pipe pieces, cradle/catch forms, choice/rhythm/control surfaces, performance UI, room raster fields and shared card/panel materials. Suitable painted identity/room/prop sources are preserved and routed for reuse. No format rename or acceptable weakness score exempts reachable flat ART. Transparent hit geometry and normal text rendering must be distinguished with exact evidence.

Earlier failed trials are retained as diagnostic logs only. Their local staging image paths are **not delivered evidence**. The first trial retained obsolete venue/floor assertions and missed two career entries. The second captured every phase but expected only 87 states rather than96 and reused isolated profiles from the first trial. The final capture run corrects these fixture defects, uses a fresh profile per aspect, and passes all96 rows. No production probe or runtime expectation was changed.

## Verification and acceptance

`python -B live_v2/validate.py` checks every image's dimensions/bytes/SHA, exact route/phase matrix, renderer/engine/quality/save protection, every source-closure hash, review-board derivation and explicit coverage limits. `--stress` rejects five falsified records. GDScript parser, inference lint and approved-engine analyzer pass for the non-runtime harness. The earlier full82 local suite is inherited only because production inputs are unchanged; it is not a newly executed full suite for R2. Published-head CI remains separate.

Implementation: current audit evidence only; zero replacements or fallback retirements. Machine verification:192 current captures and source/save protection pass. Human review: agent static/context inspection only, with remaining variants listed in `observations.json`. Actual device, child and exact owner artistic acceptance: **pending**. Game-wide master audit remains **UNSATISFIED**.

Complete and publish/verify the full current visual weakness inventory before producing new replacement pixels. Reuse investigation and reversible current captures may continue immediately. This sequence creates no new approval checkpoint.
