# Engine adoption evaluation — the 4.4 → 4.7.2 line (2026-08-30)

_First evaluation of the **Engine adoption wing** (master audit section 3.4).
Owner question: the baseline was updated on paper — code written against the
historical, superseded Godot 4.4 era now runs on exactly 4.7.2-stable — but
none of the newer engine features are used. What benefits exist, and which
belong in the master-audit framework?_

Method: the 4.5, 4.6, and 4.7 release feature sets and the 4.7.2
maintenance notes were read from godotengine.org (2026-08-30), and every
candidate was tested against a repo evidence inventory (workaround
comments, idiom adoption counts, export surface, renderer usage) at the
current head. Verdicts are triaged the same way audit findings are:
adoption is package-gated, reversible, and never for novelty
(`DL-ENGINE-04`). Feature availability claims below trace to the release
pages; anything this container could not verify in code is marked for
empirical verification rather than asserted.

## 1. The honest baseline picture

- The **pin is governed**: `tools/godot_baseline.json` holds
  4.7.2-stable + hashes, `tools/audit_godot_baseline.py` enforces it
  across 13 files in CI, and the workflows verify SHA512 on download.
  "Updated on paper" is therefore literally true and well-built paper.
- The **features are not**: `Dictionary[K,V]` 0 uses against 1,789
  untyped dictionary declarations; `uid://` 0 against 1,167 `res://`
  strings; `@export`/`@tool` 0 in `scripts/` (code-built world); AgX unset
  (runtime uses ACES); no physics interpolation; no 2D AA settings.
- **Two 4.4-era engine-bug protocols run unrevalidated** on 4.7.2: the
  exit-124 amnesty in `scripts/ci.sh:179-186` and
  `.github/workflows/probes.yml:196-205` (comment still blames "Godot 4.4
  … deadlocks at EXIT", dated 2026-07-18) — which today converts a genuine
  4.7.2 exit hang into a pass whenever the transcript tail matches
  `ALL OK|RESULT` — and the NPOT+`compress/mode=2` importer-deadlock
  protocol in `CLAUDE.md`/`AGENTS.md` with its probe-side assertions
  (`scripts/probe_melody.gd:519-523`, `tools/audit_visual_design.py`).
- **One live stale-pin defect**: `tools/audit_opera_capture.py:518-530`
  hard-requires `"4.7.1-stable (official)"` and errors on anything else,
  with `tools/tests/test_audit_opera_capture.py:148,473` locking it in —
  any fresh capture manifest produced by the actual 4.7.2 baseline binary
  is rejected. It is outside `audit_godot_baseline.py`'s required-pins
  coverage; 151 further `4.7.1` mentions exist repo-wide (most are
  legitimately historical evidence; 7 are live rollback-narrative
  instructions in `tools/plan_audit_rollback.py`).

## 2. Banked benefits — inherited by the bump, verify-don't-implement

These arrived with the binary; the work is verification, and the tablet
performance wing (Fable) owns the device half:

| Benefit | Line | Why it matters here | Verification owner |
|---|---|---|---|
| Vulkan Mobile crash fixes for Mali and Adreno | 4.6 | The Lenovo Tab M11 is Mali-G52 — the exact class the fixes target | Tablet wing (device soak) |
| 16 KB page-size compatibility (Android 15+) | 4.5 | New-generation tablets require it; the repo has zero mentions and `target_sdk` is template-default | Tablet wing (install + run on an Android 15+ device); WP-E2 records the result |
| Half-precision F16 Mobile-renderer path | 4.5 | Speed/power on Mali where the driver allows | Tablet wing (frame captures) |
| SDL3 gamepad driver | 4.5 | Pad is the fallback input; better default mappings for free | Existing `probe_touch_*`/pad probes already green — no action |
| Jolt as engine default | 4.6 | Project opted in early (`project.godot` Jolt) — now mainline-supported | None; alignment noted |

## 3. Adoption candidates — triaged

### Tier 1 — this round (code-refinement aligned; Stage E packages)

1. **Revalidate-or-retire the 4.4 exit-deadlock amnesty** (→ WP-E1,
   `MA-ENGINE-002`). Empirical, never changelog archaeology: run the full
   suite N consecutive times under 4.7.2 with the amnesty in report-only;
   zero exit hangs → remove both copies; hangs persist → re-attribute the
   comment to 4.7.2 with a dated observation and keep the guard honest.
   Either outcome removes a gate that currently tells a falsehood about
   which engine bug it forgives.
2. **Same protocol for the NPOT importer deadlock** (→ WP-E1). One
   throwaway branch imports a deliberately NPOT + `compress/mode=2`
   texture under the 20-minute guard. Clean import → the hard "known
   deadlock" warning becomes a POT-preferred performance guideline
   (`CLAUDE.md`/`AGENTS.md` edits are explicit-task-only: the result is
   REPORTED to the owner with proposed wording, not self-applied); hang
   reproduced → the warning gains "reconfirmed on 4.7.2, <date>".
3. **Unify exact-version assertions onto the baseline record** (→ WP-E2,
   `MA-ENGINE-001`). `audit_opera_capture.py` (and any future
   version-asserting tool) reads `tools/godot_baseline.json` instead of a
   literal; its test fixtures follow; `audit_godot_baseline.py` gains the
   file in `required_pins` so the class of bug is structurally closed; the
   7 live rollback-narrative pins get a one-line "at that checkpoint's
   then-current baseline" qualifier from the integration lane.
4. **Typed dictionaries for state** (folds into WP-C5/G10 — no new
   package). `Dictionary[String, Variant]` (and tighter) becomes the rule
   for NEW declarations and for state migrated in M5; 0/1,789 today is the
   baseline the ratchet's g-key work already tracks. No bulk retrofit —
   migrate-as-touched, exactly like the g-key freeze.
5. **`@abstract` on the platform contract** (4.5) (→ design 08 §11 owner
   review point 6). Marking `GameMode.mode_id()` abstract turns a
   mis-declared mode into a load-time error instead of a silent
   empty-string registry miss. The lifecycle methods stay concrete no-ops
   by design (thin modes override only what they use).

### Tier 2 — tablet performance wing's lane (handed over, not taken)

6. **Perfetto default Android tracing (4.7) + Tracy/Perfetto profiler
   hooks (4.6)** — the capture-protocol backbone `MA-PERF-001` has wanted
   since the U0 plan; the wing owns tool choice and thresholds.
7. **Mobile-renderer material debanding (4.6)** — pastel sky/water
   gradients on a budget Mali panel are banding-prone; a runtime flag the
   wing can A/B on device (visual gain vs. cost) before anyone flips it.
8. **Edge-to-edge display opt-in (4.5)** — modern-tablet presentation;
   wing decides with the device in hand.
9. **Shader baker / load-time precompilation (4.5-line)** — the release
   notes headline Metal/D3D12; applicability to this project's
   Android/Vulkan path is UNVERIFIED and must be tested by the wing before
   any claim; the prize is the first-tap shader hitch the audits have
   flagged since U0.
10. **`msaa_2d` and 2D AA settings** — currently unset everywhere; likely
    unnecessary for pixel-fit canvas art at native resolution, but the
    wing should rule once, on device, rather than leave it unconsidered.

### Tier 3 — real value, later era (chapter tooling / owner-gated)

11. **DrawableTexture2D (4.7)** — a direct replacement for the opera
    painter's per-pixel `Image.set_pixel` loops and the natural base for
    future craft/paint modes; a rendering-path swap on shipped acts, so it
    waits for the platform migration to pass it (M4+) and lands as its own
    probe-gated package when a paint surface is next touched.
12. **`tween_await()` (4.7)** — cleaner cutscene/dialogue sequencing for
    Chapter 2's story beats; adopt-as-touched, no retrofit.
13. **Release-build script backtraces + custom loggers (4.5)** — the
    local, private, no-network session health report the July upgrade
    plan wanted: exact error origins from the child's own device via a
    rotating local log the owner can pull with the existing APK tooling.
    Small, additive, owner-notified before it ships (it observes her
    device, even though it never leaves it).
14. **VirtualJoystick node (4.7)** — evaluated and DEFERRED: the custom
    stick carries bespoke, probe-guarded semantics (touch-ownership
    contract, reserved zones, hybrid routing) that the stock node does not
    model; swapping the fallback stick risks the exact regression class
    the touch audits just closed. Revisit only if stick maintenance costs
    recur.

### Rejected / not applicable, with reasons

| Feature | Line | Why not here |
|---|---|---|
| HDR output | 4.7 | Platform list excludes Android; desktop mirrors phone by rule |
| Scene Paint Mode, MeshLibrary, editor workflow gains | 4.6–4.7 | The world is code-built with zero `@tool`/`@export` surface; no editor authoring exists to accelerate — revisit only if the platform era introduces scene-authored modes |
| IK framework, SSR overhaul, AreaLight3D, stencil, SMAA, AgX params | 4.5–4.7 | 3D-side improvements landing on the shrinking `MA-2D-002` surface; adopting them would invest in code the project is deleting |
| XR/Android XR/Steam Frame | 4.5–4.7 | Out of scope for this game |
| Localization CSV tooling | 4.6 | One player, voice-first by design |
| Delta-encoded patch PCKs | 4.6 | Real interest for the 596 MB APK, but distribution is a direct-URL full APK by owner design; a patch channel is a distribution redesign, not a feature flip — parked for a future release-ops decision |
| LibGodot, D3D12, camera feed, PiP, Java interfaces | 4.5–4.7 | No current consumer |

The 4.7.2 patch itself is a routine maintenance release (crash/log/input
fixes, explicitly no compatibility changes); the unharvested value is the
4.5→4.7 feature line above, not the .2 bump.

## 4. What enters the framework

- **This wing**, registered in master audit section 3.4: every future
  baseline bump ships with an evaluation like this one, so "updated on
  paper" can never again persist silently.
- **Rules `DL-ENGINE-01`–`DL-ENGINE-04`** (design 06 section 19): pin
  governance covers every exact-version assertion; a bump is complete
  only with its adoption evaluation; engine-bug workarounds carry their
  observed version and a re-test trigger, and retire only on demonstrated
  evidence; adoption is package-gated and never for novelty.
- **Findings `MA-ENGINE-001`** (stale exact-version assertions outside
  baseline governance) **and `MA-ENGINE-002`** (4.4-attributed engine-bug
  protocols running unrevalidated on 4.7.2), with Stage E packages WP-E1
  and WP-E2 in the round handoff.
- **Tier 2 handed to the tablet performance wing's scope list**; Tier 3
  parked with owners and triggers so the next chapter finds them filed,
  not forgotten.
