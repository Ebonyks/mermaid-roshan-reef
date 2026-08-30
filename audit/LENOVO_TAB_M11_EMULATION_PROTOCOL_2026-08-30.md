# Lenovo Tab M11 emulation protocol — tablet performance program

- **Protocol ID:** `TEP-2026-08-30`
- **Date:** 2026-08-30
- **Branch:** `tablet-performance` (cut from `dev` head `0ddbe656`)
- **Authority:** SUPPORTING_CURRENT runbook. Canonical performance rules stay
  with `AGENTS.md` (target device, 30 fps, transparent-overdraw hard limits)
  and `design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md`. This protocol quantifies
  and operationalizes them; it redefines nothing.
- **Services finding:** `MA-PERF-001` (P1, `BLOCKED_EXTERNAL`) — no
  exact-release target-device performance matrix exists. Lane D below is the
  matrix that finding calls for.

## 1. Purpose

Every performance claim in this repository ultimately means one thing: the
game holds a locked 30 fps, cool and responsive, in the hands of one
four-year-old on one specific tablet. This protocol defines that tablet
exactly, converts the "Speedy tier" into numeric budgets, and defines four
emulation/measurement lanes (A–D) ordered from cheapest desktop emulation to
device truth, so that any change can be evaluated against the same standard.

## 2. Canonical device profile (confirmed hardware)

The owner has confirmed the exact retail unit (Best Buy SKU `6572176`):
**Lenovo Tab M11 11" Wi-Fi, 64 GB, Storm Grey** — the 4 GB RAM variant.
All budgets in this protocol assume this configuration, not the 8 GB variant.

| Component | Specification | Performance consequence |
|---|---|---|
| SoC | MediaTek Helio G88, 12 nm | Modest IPC; throttles under sustained load |
| CPU | 2× Cortex-A75 @ 2.0 GHz + 6× Cortex-A55 @ 1.8 GHz | GDScript main loop lands on one A75 core; single-thread budget is the scarce resource |
| GPU | Arm Mali-G52 MC2 (Bifrost, 2 cores, ~1 GHz) | Tile-based; blended (transparent) fill and bandwidth are the limiting factors, not vertices |
| RAM | 4 GB LPDDR4X, shared CPU/GPU | OS + services hold ~1.5–2 GB; game working set must stay well under the remainder |
| Storage | 64 GB eMMC 5.1 + microSD | ~250 MB/s sequential reads; large APK hurts install, update, and family storage |
| Display | 10.95" IPS, 1920×1200 (WUXGA, 16:10), up to 90 Hz, ~207 ppi | 2.3 Mpx output; 1.5× scale of the 1280×720 design canvas; expand stretch exposes ≈1280×800 of design space |
| OS | Android 13 (ships), Android 14 upgrade path | Standard adb tooling available; no root |
| Battery | 7040 mAh | Thermal/battery discipline decides whether a 20-minute session stays smooth |

Contrast with current test settings: `project.godot` window override is
1920×1080 (16:9). Desktop emulation for this device MUST run 1920×1200
(16:10) instead — Lane A supplies the command line without changing project
settings.

## 3. Speedy tier, quantified (budget table)

Values marked **E** are engineering estimates derived from the hardware
profile; they become binding numbers only after Lane D traces calibrate them.
Until then they are the working pass bar for Lanes A–C.

| Budget | Value | Basis |
|---|---|---|
| Frame budget | 33.3 ms @ 30 fps, locked | `AGENTS.md` hard limit |
| Frame pacing | 30 fps on the 90 Hz panel = clean 3:1 vsync cadence; the project MUST make an explicit pacing decision (see §7 deviation D1) | 90 Hz panel would otherwise run the engine at up to 90 fps |
| Script time (all GDScript, per frame) | ≤ 10 ms on device (**E**); desktop proxy ≤ 2.5 ms | One A75 core does this serially |
| Total fill per frame | ≤ 8 screen-equivalents ≈ 18.4 Mpx (**E**) | Mali-G52 MC2 practical blended fill ~1 Gpx/s at 30 fps |
| Transparent fill per frame | ≤ 4 screen-equivalents above the opaque background (**E**) | Transparent overdraw is the named hard limit |
| Draw calls per frame | ≤ 150 (**E**) | Canvas batching breaks on texture/material switches |
| Process memory (RSS) | ≤ 1.2 GB sustained (**E**) | 4 GB shared, OS resident ~1.5–2 GB |
| Texture memory per zone | ≤ 450 MB (**E**) | Shared-memory GPU; leaves heap headroom |
| APK size | ≤ 350 MB target (current: 596 MB — over) | 64 GB family device; download + install + update burden |
| Cold launch → title | ≤ 12 s (**E**) | eMMC sequential reads |
| Tap → zone playable | ≤ 3 s (**E**) | Short-session player; waiting is a fail state for a 4-year-old |
| Hitches | P99 frame ≤ 50 ms; no single frame > 100 ms during play (**E**) | Hitches read as "broken" to the child |
| Touch → visible response | ≤ 100 ms (3 frames @ 30 fps) (**E**) | Respond on press, not release |
| Thermal | 20-minute continuous session holds 30 fps without throttle collapse | 12 nm SoC in a passive chassis |

## 4. Lane A — desktop geometry emulation (available now)

Purpose: exercise the exact device viewport (16:10 expand) for composition,
reachability, and touch-target size. No project-setting changes needed:

```
godot --path . --windowed --resolution 1920x1200
```

- Local runs under the on-PATH Godot 4.7.1 are **advisory**; the release
  baseline is exactly Godot 4.7.2-stable. CI remains the trusted gate.
- Check per screen: nothing essential composed for 1280×720 is cropped,
  occluded, or orphaned in the extra ≈80 design-space rows the 16:10 panel
  exposes; HUD anchors hold; touch targets measured at device scale
  (1 design px = 1.5 device px; a 9 mm fingertip ≈ 73 device px ≈ 49 design
  px — targets below that are misses for a 4-year-old).
- Screenshots for review are taken at 1920×1200 native.

## 5. Lane B — instrumented budget proxy (desktop, advisory)

Purpose: catch budget regressions early with numbers, accepting that desktop
hardware is 5–20× faster than the M11.

- Instruments: Godot `Performance` monitors — `TIME_PROCESS`,
  `TIME_PHYSICS_PROCESS`, `RENDER_TOTAL_DRAW_CALLS_IN_FRAME`,
  `RENDER_TOTAL_OBJECTS_IN_FRAME`, `RENDER_TEXTURE_MEM_USED`, plus
  `RenderingServer.get_rendering_info()`.
- Interpretation rule: a **desktop miss is a real miss** (if a desktop GPU
  blows the draw-call or texture-memory budget, the M11 certainly does); a
  desktop pass is **not** a device pass — only Lane D proves the frame rate.
- Proposed follow-up work (not yet implemented, not a trusted probe): a
  `scripts/probe_perf_budget.gd` headless/windowed bot that walks the
  existing probe route and emits one line per zone —
  `PERF|<zone>|draw_calls|objects|texture_mem_mb|script_ms_p95` — so CI can
  diff budgets per commit. It must be additive and must not touch trusted
  probes.

## 6. Lane C — Android Virtual Device (AVD) emulation

Purpose: install-size, memory-pressure, DPI/touch, and lifecycle fidelity.
Explicitly NOT valid for GPU frame rate or thermal (the AVD passes GPU work
through the host).

AVD definition ("TabM11-proxy"): tablet profile, 1920×1200 @ ~207 dpi,
RAM 4096 MB, Android 13 (API 33), x86_64 image, "cold boot" snapshots off.

Useful checks and commands:

```
adb install -r roshan-reef.apk
```

```
adb shell dumpsys meminfo <package-id>
```

- Watch PSS during a full zone tour; compare against the 1.2 GB RSS budget.
- Exercise pause/re-entry, screen-off/on, and process-death restore (Android
  "Don't keep activities" toggle) — save integrity under memory pressure is a
  release gate elsewhere; this lane is where it is cheap to drill.

## 7. Lane D — device truth (closes `MA-PERF-001`)

Only this lane produces the target-device matrix. Run on the actual Tab M11
with the exact release-candidate APK (verify SHA-256 before testing).

Scenario matrix (from the `MA-PERF-001` reproduction row, expanded):

| # | Scenario | What to capture |
|---|---|---|
| S1 | Cold boot → title → loaded save | Wall-clock times |
| S2 | Reef traversal (continuous swim, 3 min) | Frame times, hitches |
| S3 | Castle hall + 3 rooms, touch interactions | Frame times, memory |
| S4 | Opera (heaviest full-screen alpha staging) | Frame times, hitches |
| S5 | Sky Lagoon full route | Frame times, memory |
| S6 | Courtyard train ride | Frame times |
| S7 | Stuffie battle incl. DODGE QTE | Frame times, touch latency |
| S8 | Two picture games | Frame times |
| S9 | Craft studio + wardrobe | Frame times, memory |
| S10 | 20-minute continuous mixed session | Thermal, battery, sustained fps |
| S11 | Pause / home / re-entry ×5, then save check | Restore correctness, re-entry time |
| S12 | Touch-latency spot check (slow-mo video of tap → response, 10 taps) | ms per tap |

Capture tooling (no root required):

```
adb shell dumpsys meminfo <package-id>
```

```
adb shell dumpsys thermalservice
```

```
adb shell dumpsys battery
```

- Frame times: the debug APK should log per-zone frame-time percentiles from
  inside the engine (a small opt-in perf logger writing
  `user://perf_trace.json`, enabled by a hidden debug flag file — proposed
  follow-up work, additive only). Until that exists, Arm Performance Studio
  (Streamline) over USB provides Mali counters and frame times on Mali GPUs.
- Report format per scenario: P50 / P95 / P99 frame ms, hitch count
  (> 50 ms), peak PSS, thermal status transitions, and pass/fail against §3.
- Acceptance: every scenario inside budget on the confirmed 4 GB / 64 GB
  unit → the matrix attaches to `MA-PERF-001` as closure evidence. Any miss
  files a bounded hotspot (zone + counter) rather than a vague "slow" note.

## 8. Known baseline deviations at protocol creation (2026-08-30)

Logged here so Lane runs do not rediscover them; the companion evaluation
report on this branch owns the full weakness list.

- **D1 — No frame-rate pacing decision.** `application/run/max_fps` is unset
  and no script sets `Engine.max_fps`; on the 90 Hz panel the engine will
  attempt up to 90 fps — triple the intended frame work for motion a
  four-year-old cannot perceive, spent directly as heat and battery. Needs an
  owner-ratified pacing decision (cap 30 vs cap 45/90-divisor) — one line,
  but it is a behavior change and must go through normal probe gating.
- **D2 — Desktop test override is the wrong aspect.** `project.godot` window
  override is 1920×1080 (16:9); the device is 1920×1200 (16:10). Lane A works
  around it; screenshots taken via the override under-test the tall aspect.
- **D3 — APK is 596 MB** against a 64 GB family tablet; §3 sets a 350 MB
  target. `export_presets.cfg` excludes docs/tools/staging but not every
  non-runtime tree (e.g. `attic/`, `disabled_addons/`).
- **D4 — 3D remnant cost is nonzero.** `tools/audit_game_2d.py` at this head:
  0 model files, 56 production 3D files, 1 3D scene file, Jolt 3D physics
  still enabled in `project.godot`. Exact shrinking debt per `CLAUDE.md`.
- **D5 — Headless import deadlock hazard** (NPOT + `compress/mode=2`) still
  applies to any Lane B/C import step; watch the last `Importing file:` line
  if import stalls beyond 3 minutes.

## 9. Cadence and ownership

- Lanes A–B: every performance-relevant change on this branch; advisory
  locally, trusted on CI once the budget probe exists.
- Lane C: before each `dev` → `master` promotion candidate.
- Lane D: owner-run on the physical Tab M11 for each release candidate APK
  (exact SHA), and once immediately to baseline the current dev build —
  that first run calibrates every **E** value in §3 and unblocks
  `MA-PERF-001`.
