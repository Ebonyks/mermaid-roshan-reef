# Mermaid Roshan: Reef of Light — font and typography audit, 2026-08-30

- **Audit ID:** `MA-TYPE-2026-08-30`
- **Historical inventory source:** `0ddbe65685b7dde09e4d9179d71580ed406bcc13`
  on `codex/font-audit-20260830` (the V1 baseline; it has no runtime role
  plumbing or candidate layout edits)
- **Current implementation source:** committed partial implementation
  `828e169f` (role/token plumbing, bounded TYPE-C edits, and the initial
  scanner/probe/test harness), reconciled with review candidate `4e4e66b4`.
  These commits are implementation history, not a new typography authority
  head.
- **Scope:** runtime typography, text controls, semantic glyphs, text layout,
  localization readiness, and `Label3D` typography debt
- **Document authority:** `SUPPORTING_CURRENT`. Stable requirements are
  `DL-TYPE-01`–`DL-TYPE-12` in
  `design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md`; canonical lifecycle records
  are `MA-TYPE-001`–`MA-TYPE-007` in
  `audit/findings/ACTIVE_FINDINGS_2026-08-13.md`; the canonical audit ledger
  remains `audit/MASTER_AUDIT_2026-08-09.md`
- **Evidence limit:** V1 static source and repository evidence only. No Godot
  render, screenshot, font rasterization, Android package, Lenovo M11, older
  phone, child, accompanying-adult, localization, or owner review was performed
  in this source/review round.
- **Runtime/asset change:** partial implementation only: shared role/token plumbing,
  completed picture-button styling, selected TYPE-C size/layout edits, and
  focused scanner/probe tests. No font asset, default-font authority, glyph
  coverage, device, child, human, or owner acceptance exists.

## 1. Verdict

The interface already has the right child-facing strategy: large touch
targets, picture-first choices, voice cues, live pointers, progress pips,
neutral exits, and a shared Storybook color/outline grammar. The font layer
under that strategy is not controlled. The repository contains no project font
asset or font resource, no project-wide Theme/default-font assignment, no font
licence row, and no glyph-coverage proof. Text therefore uses the exact Godot
4.7.2 default unless an individual node overrides size/color/outline; semantic
symbols and emoji have no recorded packaged-coverage result.

The committed implementation now adds explicit role/token plumbing and a bounded subset of
child-size/layout checks, while deliberately leaving overflow-prone Craft and
companion surfaces at their audited sizes. This is not evidence that every
current glyph is missing or unreadable. It is
evidence that the project cannot yet prove the font, glyph, size, wrapping, and
device properties on which parts of its non-reader interface rely. The correct
response is a bounded control-and-verification program, not an invented font
choice or a broad UI redesign.

## 2. Reproduced inventory

The constructor census covers all non-probe `scripts/**/*.gd`, including the
developer overlay. Probe files are excluded because they do not ship the
child-facing surface.

| Surface | Exact V1 result | Reading |
|---|---:|---|
| Tracked `.ttf`, `.otf`, `.woff*`, `.font`, `.fontdata`, or font import paths | 0 | No redistributable project font is selected |
| Font resource/default-font declarations (`FontFile`, `FontVariation`, `SystemFont`, `font_data`, `default_font`, font override) | 0 | Runtime controls inherit the engine default face |
| Font-specific `ASSET_LICENSES.md` rows | 0 | No candidate has established redistribution/licensing authority |
| Translation assets/settings (`.po`, `.pot`, `.mo`, `.translation`, `[internationalization]`) | 0 | No localization layer exists |
| `Label.new(` | 96 across 29 files | Broad direct construction surface |
| literal `Button.new(` | 84 across 25 files | The earlier “85 `Button.new`” summary was one high |
| `CheckButton.new(` | 1 in `scripts/dev_mode.gd` | 84 Buttons + 1 CheckButton = 85 button-class controls |
| `Label3D.new(` | 45 across 13 files | Typography is part of measured true-2D migration debt |
| `add_theme_font_size_override(` | baseline 45 at `0ddbe656`; committed implementation 39 | Some direct size overrides were removed, but size is not yet fully role-owned |
| `Label3D.outline_size` assignments | 39 | Most, not all, spatial labels carry local outline treatment |

The reconciled source head `5bf3b1a4` adds one live code point, `U+26A1` (⚡),
at `scripts/games/dust_boss.gd:1044`. It is classified as **redundant**, not
critical: it is an optional incoming-hop attention flash on the dodge button,
while the same state is voiced (`dustboss_dodge`), marked by the visible
pointer at `dust_boss.gd:1050`, and represented by the action affordance and
parent hint at `dust_boss.gd:995`. The dodge is harmless and never gates
progress. The manifest records these exact source routes in `glyph_evidence`;
this is source classification evidence only, not font coverage or device
acceptance. The live inventory is therefore 148 observed code points: 11
decorative, 2 redundant, and 135 critical; all 135 critical points remain
unresolved while font authority is absent.

Representative commands:

```text
git ls-files | Select-String '\.(ttf|otf|woff2?|fontdata|font|translation|po|pot|mo)(\.import)?$'
rg -n 'FontFile|FontVariation|SystemFont|font_data|default_font|theme/default_font|font_override' .
rg -o '\bLabel\.new\(' scripts -g '*.gd' -g '!probe*.gd' -g '!probe_*.gd'
rg -o '\bButton\.new\(' scripts -g '*.gd' -g '!probe*.gd' -g '!probe_*.gd'
rg -o '\bCheckButton\.new\(' scripts -g '*.gd' -g '!probe*.gd' -g '!probe_*.gd'
rg -o '\bLabel3D\.new\(' scripts -g '*.gd' -g '!probe*.gd' -g '!probe_*.gd'
```

## 3. What already works

- `StorybookUI.style_button()` and `style_label()` centralize size, color,
  outline, pressed/focus treatment, and the shared Storybook palette.
- Required targets are generally large and picture-first. The shared
  `MIN_TOUCH` is 110×110, and Back/exit controls have a neutral icon route.
- Voice hooks, objective pointers, pips, and picture cues keep text
  supplemental in many important flows. Opera also retains a caption fallback
  when an exact recording is absent; that is useful diagnosis/adult support,
  not a substitute for the exact spoken cue.
- The Castle room selector already uses authored room-button images under
  `assets/ui/castle_room_buttons_v2/`. This is the correct precedent for
  replacing critical platform-glyph semantics with controlled art.
- Colors and outlines are usually intentional, and the current code already
  distinguishes parent captions, HUD labels, status labels, and direct
  controls in practice. The missing step is to make those roles explicit and
  exhaustive.
- Candidate-only implementation evidence: `storybook_ui.gd` now exposes eight
  named roles and complete picture-button state styling; the candidate scanner,
  focused probe, and deterministic TYPE-C layout tests are present. These are
  implementation controls, not font/glyph/device acceptance.

## 4. Confirmed gaps

### 4.1 Font source and fallback are implicit

No repository asset or Theme owns the default face. A third-party font MUST
NOT be added merely to fill this gap: the selection first needs an embedding/
redistribution licence, a root licence-ledger row, exact hash/source evidence,
measured size and performance, child/device legibility, and coverage for the
approved live code-point inventory. An explicit, audited decision to retain an
engine-bundled face would still need a reproducible version/coverage record and
a deterministic fallback policy.

### 4.2 Shared styling is partial

At historical `0ddbe656`, `StorybookUI.style_button()` owned font size and
outline, `style_label()` owned font size/color/outline, and
`style_picture_button()` omitted complete typography state; Wardrobe repaired
that omission with a local size override. Commits `828e169f` and `4e4e66b4` add named role
tokens and complete picture-button state styling, but its engine/default font
and fallback remain unresolved, and Opera/Kart/dance/direct HUD clusters still
need exhaustive role migration and capture evidence.

### 4.3 Small text is not consistently bounded by role

Confirmed child-facing or adjacent examples include:

| Surface | Current size | Context |
|---|---:|---|
| Intro parent caption | 22 | Wrapped and voice-backed; adult-support role is plausible but unverified on device |
| New-game preservation note | baseline 22; candidate 28 | Child/safety warning; candidate expands the box to 580×132 and allows three wrapped lines; it is not an adult-caption exception |
| Craft status | baseline/current 21 | Child-facing state/instruction in a 175×150 wrapped box; enlargement is explicitly deferred because the exact status strings are not proven to fit |
| Sticker names/hints | baseline/current 20 / 15 | Child-adjacent collection labels; the fixed 72px cell is deliberately deferred rather than enlarged into clipped two-line text |
| Critter habitat | 22 | Supplemental word plus emoji |
| Several choice labels | baseline/current 24–27 | Used on child-facing craft/companion controls; fixed-box enlargement is explicitly deferred where line capacity is not proven |

Static size alone does not prove unreadability, and the 22px voice-backed intro
caption must not be conflated with a 15px required hint. The actionable defect
is the absence of role minima and the presence of child-relevant semantics
below the proposed floor without device/child evidence.

### 4.4 Picture-button and semantic-glyph coverage are incomplete

The UI uses stars, shells, crowns, arrows, locks, check marks, emoji, and other
symbols as progress, navigation, category, habitat, care, career, and objective
cues. Some are redundant decoration; others carry meaning. With no packaged
glyph manifest or runtime proof, critical coverage is unconfirmed. Emoji shape,
color, advance, baseline, and availability must not be assumed. Critical
meaning uses controlled authored assets or a proved bundled monochrome glyph;
Unicode may remain redundant decoration. The new Dust Bunny `⚡` cue is kept in
that redundant class because the optional dodge is simultaneously voiced,
pointed at, and pulsed; it never carries the only action or progress meaning.

### 4.5 Fixed English layout has expansion risk

There is no translation layer or pseudo-locale gate. Several strings use fixed
rectangles; wrapping is present on some captions/status blocks and absent on
other direct labels/buttons. Concatenated strings, repeated emoji, and line
breaks are authored around current English widths. No current evidence proves
longest-English, 130% expansion, two-line button labels, RTL, truncation, or
font-ascent behavior. This audit does not require a second language; it requires
layout-safe strings and forbids calling the build localization-ready before the
layer and tests exist.

### 4.6 `Label3D` is typography and medium debt

Forty-five `Label3D` constructors remain across 13 production files, with 39
local outline assignments. They include pointers, labels, counters, care
bubbles, shop tags, and other child-visible semantics. They are already within
`MA-2D-002`; a typography migration must preserve semantic role, visible size,
position, occlusion, and touch/voice relationships while converting each family
to `Label`/Canvas ownership. No new `Label3D` may be introduced.

## 5. Canonical findings opened

| Finding | Severity / lifecycle | Bounded problem |
|---|---|---|
| `MA-TYPE-001` | P1 / `CONFIRMED_OPEN` | No explicit licensed font/default-font/fallback/coverage authority |
| `MA-TYPE-002` | P2 / `CONFIRMED_OPEN` | No complete shared role/token plumbing; picture-button and direct clusters bypass it |
| `MA-TYPE-003` | P1 / `CONFIRMED_OPEN` | Child-facing size/read-dependency contract is not enforced |
| `MA-TYPE-004` | P1 / `CONFIRMED_OPEN` | Critical Unicode/emoji semantics lack controlled coverage or authored replacement |
| `MA-TYPE-005` | P2 / `CONFIRMED_OPEN` | Fixed English boxes and strings lack expansion/localization safety |
| `MA-TYPE-006` | P1 / `IN_PROGRESS` | 45 `Label3D` instances remain inside game-wide 2D migration debt |
| `MA-TYPE-007` | P1 / `BLOCKED_EXTERNAL` | No current M11/older-phone/human/child typography acceptance record |

All are V1 unless a future history entry cites higher evidence.

## 6. Safe implementation batches

These batches are intentionally separable for Luna agents. A later batch may
start only from a reviewed inventory and must not smuggle in a font, copy
rewrite, layout redesign, 3D growth, or acceptance claim.

1. **TYPE-A — font-resource and default-font control.** Inventory live code
   points. Evaluate candidates without committing binaries. Select only after
   licence, redistribution/embedding, provenance, hash, glyph coverage, APK/
   memory, and child/device legibility are established. Then add the selected
   resource, root licence row, deterministic fallback chain, and project Theme
   in one asset-gated change. “Use a cute font” is not a selection criterion.
2. **TYPE-B — shared role/token plumbing.** Add explicit display/title,
   control, body, caption, status, numeric/progress, and decorative-glyph roles
   to the Theme/Storybook layer. Make `style_picture_button()` complete. Migrate
   one bounded constructor family at a time, including Opera, Kart, dance, and
   direct HUD clusters, with no string or layout behavior change.
3. **TYPE-C — child minimum and picture-button coverage.** Enforce 28px
   minimum for child-action/state text and 22px for genuinely supplemental
   adult captions at the 1280×720 base canvas. Review every sub-28 child-facing
   use; do not mechanically enlarge decoration. Preserve 110×110 targets and
   picture/voice routes so required understanding never depends on reading.
4. **TYPE-D — Unicode/emoji critical semantics.** Classify each live non-ASCII
   code point as decorative, redundant, or critical. Convert critical emoji/
   symbols to approved authored texture icons or prove exact bundled glyph
   coverage. Reuse the Castle room-button precedent and existing approved art
   before generating anything.
5. **TYPE-E — wrapping and localization readiness.** Externalize player-facing
   strings behind stable keys without changing English wording, replace unsafe
   concatenation with placeholders, and add longest-English plus 130%
   pseudo-locale capture tests. Define wrap/clip/ellipsis per role; do not claim
   a language supported until translations and human review exist.
6. **TYPE-F — `Label3D` true-2D migration.** Work one gameplay family at a
   time under `MA-2D-002`: capture current intent, replace with Canvas `Label`/
   icon ownership, preserve voice/pointer/touch semantics, run focused and full
   probes, then decrement the exact GAME2D/Label3D census. Never add a spatial
   fallback.
7. **TYPE-G — device and human verification.** At the exact integrated APK,
   record 1280×720 Mobile captures plus Lenovo M11 and required older-phone
   screenshots for default, longest, wrapped, locked, selected, and missing-
   glyph stress states. Check truncation, tofu, baseline, outline, contrast,
   touch occlusion, adult caption utility, and a private observed child path.
   Machine glyph coverage is necessary and not sufficient.

## 7. Closure boundary

The committed partial implementation (`828e169f`, reconciled at `4e4e66b4`) changes shared role plumbing and a bounded subset of
runtime layout values, but changes no font asset or authority and closes none
of the findings. The save warning is now a 28px child/safety status surface;
the Wardrobe locked hint uses a bounded 28px right-aligned picture-button
layout; overflow-prone Craft locked choices/status, companion picker labels,
and the 34px sparkle row remain at their audited sizes and remain open. The
candidate scanner and deterministic fit tests are diagnostic controls only.
The typography program is complete only when the canonical record for each
batch contains its own exact implementation, machine, capture, device, human,
child, and owner evidence as applicable. A chosen font, a clean desktop
screenshot, or a green glyph scanner cannot stand in for the remaining lanes.
