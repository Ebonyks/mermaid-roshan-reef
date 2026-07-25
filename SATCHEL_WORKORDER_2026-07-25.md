# The Satchel — workorder for R1–R3 (2026-07-25)

Owner direction (2026-07-25): adopt R1 (reactive props), R2 (universal carry)
and R3 (Roshan's room) from TOCA_BOCA_DESIGN_ANALYSIS_2026-07-25.md, with
**casual animation** and a **Minecraft-like inventory** as the way to give the
world a sense of depth.

This is the implementation design. It unifies all three into one system so they
ship as one grammar the child learns once, not three features.

---

## 1. The thesis

R1, R2 and R3 are the same feature seen from three angles:

- R1 says **every object answers a touch**.
- R2 says **you can pick things up**.
- R3 says **you can put them somewhere that stays**.

An inventory is what joins them. Without it, R2 is a toy you carry until you
drop it and R3 is a separate menu. With it, there is one rule —
**the world is made of things you can take and put back** — and every prop in
the reef stops being scenery and becomes a question.

That rule is the actual source of Minecraft's depth. Not the UI. This matters
for what we take and what we leave.

### 1.1 What to take from Minecraft, and what to refuse

| Minecraft feature | Verdict |
|---|---|
| **Hotbar** — one always-visible row, pictures not words, one tap to select, selected item is in your hands in the world | **Take it, verbatim in spirit.** This is the child-friendly half of Minecraft's inventory and it needs no reading, no drag, no memory. |
| **Take-and-place universality** — almost anything can be picked up and put back | **Take it**, bounded by a denylist (§5.4). |
| **Inventory screen** — 4×9 grid, drag-and-drop, shift-click, stack splitting | **Refuse.** Every one of those is a literacy, dexterity or working-memory tax. One finger, age 4, phone screen. |
| **Stack counts** ("64") | **Refuse.** Numbers on the HUD are a reading dependency. If a count is ever needed, it is pips, not digits. |
| **Crafting recipes / grid** | **Refuse.** Recipe knowledge is memorised text. The Craft Studio already covers "make your own thing" without it. |
| **Inventory full = cannot pick up** | **Refuse.** That is a soft fail state. See §3.3. |

So: **take the hotbar, leave the inventory screen.** The result is closer to
Toca's satchel than to Minecraft's `E` key, which is the right target for this
player.

---

## 2. Naming

The **Satchel**. Six slots, one row, bottom-centre of the HUD. The bedroom's
existing **toy chest** (`castle_hall.gd:build_bedroom`, currently pure set
dressing) becomes its diegetic home and the overflow store.

---

## 3. System design

### 3.1 The three animation layers ("casual animation")

Ambient motion is what makes a prop read as a *thing* rather than a decal.
Three layers, in ascending cost:

1. **Idle** — always on, ambient. Gentle sway/bob/breathe.
   - Flora and corals: **vertex sway in shader, zero CPU.** The precedent
     already exists — `assets/shaders/coral_flow.gdshader` is wired in
     `_gen2_prop` for `coral*` props and sways green growth while rocky bodies
     stay rigid.
   - Non-flora props: one shared sine evaluated in a single `_process` over a
     **near-player list only**, culled at the existing creature-animation
     distances (95 m Speedy / 160 m Sparkly, DESIGN_3_0.md) — reuse those
     constants, do not invent new ones.
2. **Reaction** — on touch. Squash-and-stretch plus a chime and a sparkle.
   The curve already exists and already feels right: the singing shell in
   `carry_system.gd` (`scale = 1 + sin(t*18)*0.08*pulse`, decaying over 0.8 s).
   **Lift that exact curve into a shared helper** so every reaction in the game
   is recognisably the same gesture.
3. **Transition** — pickup and placement. Item arcs to the satchel slot, or
   pops out and settles into a snap slot. ~0.35 s, tween-based.

**Budget rule:** cap concurrent reaction tweens (start at 8). Past the cap,
react *instantly* without a tween — never drop the response. A tap that does
nothing breaks the one promise the whole pass is making.

### 3.2 The satchel model

- **6 slots**, single row, bottom-centre. 6 × 110 px + gaps fits inside the
  1280 px base canvas, clear of the left virtual stick and the right action
  button.
- **Slot art is a picture, never a word or a number.**
- **Selected slot = what she is holding.** The held item renders at the
  existing carry point (`CarrySystem.CARRY_FWD` / `CARRY_UP`) with the existing
  bob. One concept, not two: hands and hotbar are the same thing.
- Tap a slot → select / deselect. ACTION near a pickable → pick up.
  ACTION while holding → put down or place.

### 3.3 Never a wall

A full satchel does **not** block pickup. The oldest item **swims home**: it
returns to its world seat with a sparkle and a voice line. Nothing is ever
destroyed, and there is no state where the child is told "no".

This is the non-destructive rule, and it is not negotiable — it is what
separates this from Minecraft's inventory-management chore.

### 3.4 Slot icons — the one real technical risk

Slots need a picture of the prop. Options considered:

| Approach | Cost | Verdict |
|---|---|---|
| Pre-rendered PNG per pickable | New asset + ASSET_LICENSES.md line each | Fallback |
| **Runtime render, cached once** | One shared 128×128 SubViewport; render one frame at first pickup, grab to `ImageTexture`, cache by prop id | **Primary** — 128 is POT, ≤1024, no new assets, no licence lines |
| Silhouette + dominant colour | Cheapest | Too abstract to recognise |

**Prototype the runtime render first.** If SubViewport-to-texture misbehaves
under the Mobile renderer on the M11, fall back to pre-rendered PNGs and accept
the asset lines. Do not build the rest of the satchel on an unproven icon path.

### 3.5 Placement (R3)

**Snap slots only** — no free 3D placement (one finger, age 4; free placement
buries props inside geometry, which is a non-destructive-design violation).

- Bedroom snap slots: chest top, bedside table, windowsills, shelf tops, rug
  spots. Target ~10. Each is a marker position plus an accepted scale.
- Place → item pops into the nearest empty slot and settles.
- ACTION at a filled slot → take it back.
- **Reef placement is session-only**: set down at her feet, returns to its home
  seat on reload. The authored world never degrades.

### 3.6 The pearl sink

Once placement exists, the Pearl Shop sells **room props**. This is what the
existing code comment has been asking for — "real things to save up for instead
of a number that only ever grows" (`main.gd:400`). Prefer already-licensed
`KIT_GEN2` / gen2 props so the shop stock costs no new art.

---

## 4. Save compatibility — corrected

New keys: `"satchel"` (array of prop ids), `"room"` (dictionary slot → prop id).

**Correction to MEDALS.md.** That doc says new keys must stay *out* of
`KNOWN_KEYS` "so pre-medal saves stay schema-complete". That is stale — the
code no longer works that way, and `"critters"` is in `KNOWN_KEYS` today.
`save_state.gd:_has_complete_schema` judges completeness against the frozen
`CORE_KEYS` quartet (`won`, `found`, `pearls`, `plays`) only, and says so
explicitly: requiring every `KNOWN_KEYS` entry "demoted ALL existing saves to
the salvage path the first launch after a build added any new key — new keys
must instead pick up their defaults in `_normalise_save`."

So the correct procedure for both new keys is:

1. Add a default in `_normalise_save` (`_array_or_default` / `_dictionary_or_default`).
2. Add to `KNOWN_KEYS` and to the matching `ARRAY_KEYS` / `DICTIONARY_KEYS`
   type list — `KNOWN_KEYS` is type validation only and never demotes a save
   for merely lacking a key.
3. Remove nothing.

MEDALS.md should get a one-line fix in the same commit so the next person
doesn't follow the stale advice.

---

## 5. Constraints this must respect

### 5.1 Code placement
Everything lands in **new satellites** (RefCounted, receive `main`, state on
main), per the Phase 7 pattern and the refactor rules. main.gd is at 7,345
lines against a <2,500 target and must not grow:

- `scripts/reactive_props.gd` — tagging, idle + reaction animation
- `scripts/satchel.gd` — inventory model, HUD row, pickup/place verbs
- `scripts/room_slots.gd` — bedroom snap slots and persistence

main.gd changes are limited to: one tag call inside `_gen2_prop`, three tick
calls, and the satellite refs.

### 5.2 Renderer and perf
Mobile renderer on every platform. No new OmniLights. Flora sway is shader-side;
prop idle motion is culled at the existing 95/160 m distances. No new textures
except the 128×128 POT runtime icons.

### 5.3 Input gating
All satchel verbs are ACTION-gated and blocked while an overlay or minigame is
up — copy the existing gate at the top of `CarrySystem.tick()` verbatim; it
already handles wardrobe / stickers / craft / collection / intro / `mg_kind`.

### 5.4 The pickable denylist — hard requirement
Never pickable: anything in `game_nodes` (the minigame reclaim list), pearls,
friend nodes, the kart/brawl/slide portals, structural flora, and any prop a
minigame or the guide fish targets. **Nothing that gates progress may ever
enter the satchel.** Pickability is opt-in by tag, not opt-out.

### 5.5 Probes
- `probe_satchel.gd` (new): pick up → held → place in a bedroom slot → save →
  reload → still placed. Plus: satchel-full evicts the oldest **and the evicted
  prop is back at its world seat** — assert nothing was destroyed.
- `probe_passive.gd` must stay silent — zero-input play picks up nothing,
  places nothing, awards nothing.
- `probe_load.gd` must still pass with the two new keys present and absent.
- Add `probe_satchel.gd` to `scripts/ci.sh`.
- No Godot binary in the remote container: CI (`.github/workflows/probes.yml`)
  is the gate. A red probes run is a revert signal, not a probe to patch.

---

## 6. Staging

One commit per stage, probes green before the next. Each stage is independently
shippable and playable — if we stop after any of them, the game is still whole.

| Stage | Content | Gate |
|---|---|---|
| **S0** | Icon-render spike: SubViewport → `ImageTexture` under the Mobile renderer | Throwaway; decides §3.4 |
| **S1** | `reactive_props.gd` — tags, idle sway, touch reaction. No inventory. | probe_passive silent; perf sane |
| **S2** | `satchel.gd` — HUD row, pick up / put down in the reef. Session-only. | probe_satchel part 1 |
| **S3** | `room_slots.gd` — bedroom snap slots, `"room"` + `"satchel"` persistence | probe_satchel full + probe_load |
| **S4** | Pearl Shop sells room props (the sink) | probe_audit |

**S1 alone is worth shipping.** It touches no state, needs no new assets, and
is the biggest world-feel gain per line in the whole plan.

---

## 7. Open questions for the owner

1. **Satchel size** — 6 slots is the recommendation (fits the canvas, fits a
   4-year-old's working memory). 4 would be calmer, 8 would fit the canvas but
   crowds the action button.
2. **Does the satchel survive between areas?** Recommendation: yes, it is hers.
   Placement does not — reef placements go home, bedroom placements persist.
3. **Does the toy chest overflow?** Recommendation: yes — evicted items go to
   the chest rather than home, so the chest becomes "everything I ever found".
   Slightly more code, considerably more charm, and it makes the chest real.
