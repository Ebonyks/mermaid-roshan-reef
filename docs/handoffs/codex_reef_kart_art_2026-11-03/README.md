# Reef Grand Prix: new Racer engine and Codex art handoff (2026-11-03)

| | |
|---|---|
| Status | Engine `IMPLEMENTED_ON_BRANCH`; art `REQUESTED`; nothing `DELIVERY_ACCEPTED` |
| Branch | `claude/reef-kart-engine-20261103` (base `27c88288`); not merged to `dev` during the demo freeze (demo 2026-11-07) |
| Prepared by | Claude: engine code at the owner's explicit request, plus this written handoff. Claude built no images. |
| Recipient | Codex: all relevant artwork, from the written requests in `ART_REQUESTS.md` |
| Owner decisions | `ODR-RACER-ENGINE-20261103`, `ODR-RACER-TOUCH-20261103`, `ODR-TRACK-FIDELITY-20261103` (supersede `ODR-RACER-VIEW-20261018`) |
| Finding | `MA-OPERA-014` (Racer rebuild) |

## 1. What the owner asked (2026-11-03, verbatim in `audit/cycles/reef-kart-engine-20261103/owner_request.json`)

1. A far better Racer engine, after studying a commercial kart racer running
   in an emulator. Do not copy its art or assets; strip all of its IP and use
   Mermaid Roshan's instead. Keep track design, pickups that make you faster
   and a basic item system. Codex produces all relevant artwork.
2. A touchscreen interface: "Left is control stick, Right is break (green and
   red respectively) as well as a bubble for the items/boost."
3. A project rule: "the tracks themselves must resemble the in game settings
   with high accuracy. It is okay to make new art requests from codex, but
   they must all be a reorganization of existing assets rather than genuinely
   new content requests."

## 2. What is built (see `ENGINE.md`)

- A true-2D perspective kart race. A canvas shader projects the ground, and
  sprites and the HUD are drawn in depth order. The node tree is fixed.
- The **Pearl Canal Circuit**: the Racer career's own in-game world painting
  laid out flat (`TRACK.md`). It has the pearl starting arch, three gem
  buoys, the checkered-ribbon arch, an S-bend to the east pearl arch, the
  bowed back straight behind the pearl-dome pavilion, and the west pearl arch
  and S-bend back to the line.
- **Pearls** raise top speed (+2.5 % each, 10 max, never lost).
- **Items** come from the gem buoys and from the bubbles under the pearl
  arches: zoom, sparkle bubble, kelp patch and pearl bundle.
- **The imp races for real.** If he wins, only the race restarts. He slows
  after each win, and ties go to Roshan.
- **The owner's touch layout:** a green floating stick on the left, and the
  item bubble and red brake on the right. One finger owns each control.
- **A child-first assist.** The stick picks a lane and the kart holds it, so
  it never fights her. It eases off before bends it cannot hold, and it turns
  itself round if she faces the wrong way.
- **Voice reactions** use existing recorded clips only (`VOICE.md`).
- **Probes.**
  - `probe_racer_integration.gd`: 42 checks.
  - `probe_opera_2d.gd`: ALL OK with the new Racer legs, including a
    purposeful driver beating a held stick by 4.1 s.

## 3. Calls Claude made, and why

| Call | Why |
|---|---|
| Nothing from the studied game was copied | The owner asked to strip its IP, and copying its tracks, characters, items or names would infringe. The engine follows only the genre's general principles. |
| The setting is the canal painting the game shows, not `world_racer.png` | Two Racer paintings exist. The game draws the canal tiles; `world_racer.png` is an unshown fallback (`TRACK.md` section 0). The earlier 2026-10-17 Racer handoff described the wrong one. |
| No boost pads, ramps or painted start line | The painting has none (owner rule 3). Pearls and the zoom item do the speeding up. |
| Gem buoys deal items | They are the painting's own treasure objects on the lane. |
| The recorded instruction "Swipe to steer through the coral gates!" stays | It is the exact recorded line (probe-pinned); the arches are the gates. No new recording was requested. |
| Controls stay code-drawn | No runtime-quality stick or brake art exists. Recolouring an existing button is owner question Q2. |

## 4. Codex work order

Do the requests in `ART_REQUESTS.md` section 2 in order, A1 (floor) first.
Every request is a reorganization of existing art with its source path and
SHA-256. Each lands by adding a file at the listed path; the engine picks it
up without code changes. Run the probes after each batch and report
`ARCHIVE_COMPLETE`, `GENERATION_READY` and `DELIVERY_ACCEPTED` separately.

## 5. Owner questions (defaults apply until answered)

| # | Question | Default |
|---|---|---|
| Q1 | Give the imp's kart its own recoloured art, or keep the runtime lavender tint on the existing kart? | Keep the runtime tint (no recolour) |
| Q2 | Replace the code-drawn green stick and red brake with the existing pearl-dome turbo button (`widget_gauge_racer.png`) recoloured green and red? | Keep the code-drawn controls |
| Q3 | Add more tracks from other in-game settings (castle rooms of the earlier kart game, Sky Lagoon)? | No; one track first |
| Q4 | Record new voice lines for the brake, the bubble, the imp's win and "this way"? | No new recordings now |

## 6. Acceptance still open

- **Visual.** No capture exists (Claude makes none). Codex or the owner must
  look at the race on screen.
- **Device.** Frame time and touch feel on the Lenovo Tab M11.
- **Child.** Can she steer with the stick, find the bubble and enjoy racing
  the imp?
- **Owner.** The race, the track's fidelity to the painting, and every
  delivered art file.

## 7. Files

| File | Role |
|---|---|
| `README.md` | This entry point |
| `ENGINE.md` | Engine behaviour, touch geometry, art binding contract, measurements |
| `TRACK.md` | Which painting, its reading, course layout, floor and skyline recipes |
| `ART_REQUESTS.md` | Every art request with sources, hashes and operations; gaps |
| `VOICE.md` | Existing clips wired to race moments; voice gaps |
| `MANIFEST.json` | Hashes of every packet file |
