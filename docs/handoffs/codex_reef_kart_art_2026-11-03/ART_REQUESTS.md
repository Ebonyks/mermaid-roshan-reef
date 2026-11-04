# Art requests for Codex (all reorganizations of existing art)

Owner rule, 2026-11-03: "It is okay to make new art requests from codex, but
they must all be a reorganization of existing assets rather than genuinely new
content requests."

## 0. Binding rules for every request

1. **Allowed operations only.** Crop, isolate or cut out (with edge cleanup
   only), mirror, tile, scale, rotate or lay flat, re-lay-out several existing
   pieces into one image, inverse-perspective re-projection, and the
   owner-named colour (green stick, red brake) where a request says so.
2. **Nothing hidden is invented.** Do not repaint a part of an object that
   the source hides. If a source is occluded, crop so the occluder is outside
   the card, keep the occluder as part of the card, or record a gap.
3. **Cite every source.** Give the source path and SHA-256 (below) and the
   exact operation in `ASSET_LICENSES.md` and in a provenance JSON beside the
   output, in the same commit.
4. **Size.** At most 1024 px on the longest side, or power-of-two (the floor
   and skyline are POT). RGBA PNG.
5. **No outside IP.** Nothing from any commercial game, film or brand.
6. **Protected art is untouched.** `assets/book/`, `assets/audio/voices/`,
   `assets/characters/friends/` and `attic/` are out of bounds.
7. **Claude built no images.** Every picture here is Codex's to make from
   these words. Viewing the sources is all Claude did.
8. **Status labels.** A delivered file is a candidate. Report
   `ARCHIVE_COMPLETE`, `GENERATION_READY` and `DELIVERY_ACCEPTED` separately;
   only the owner on the device can accept.

The engine already draws every role with an interim shape and switches to the
file the moment it exists (paths in `ENGINE.md` section 5). No code change is
needed to land any request.

## 1. Sources (SHA-256 of the current files)

| Key | Path | Size | SHA-256 |
|---|---|---|---|
| CANAL | `assets_src/imagegen/opera_codex_2026-08-02/native/world_racer_native.png` | 1672x941 | `d7a7cba283c0f06c7159949d63f1ca345ee4938c63374ec43bebc7c78e13deda` |
| CANAL_MASTER | `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_world_master_racer.png` | 2048x2048 | `deb79c0b95bb32410bbfa4fe56fffb15e860736a72b4aaa533005efcb83cc08e` |
| KART_S | `assets/kart/chase/kart_straight.png` | 627x627 | `6a3107b79afd615b96b3777cd002b9d2e5814743dbfef718567d7e535693deee` |
| KART_EMPTY | `assets/kart/chase/empty_kart.png` | 1024x1024 | `35457c5cf602bffa666d6663f9fcbefb9be26bd2d0eca1c96cb5c2a6fbf9ac88` |
| IMP_FLEE | `assets/opera/worlds/actors/rival_racer_flee.png` | 512x512 | `32b062cd2e5ce61974a88eb38f62fd710babb136ebf74c8328049096157f60b8` |
| PEARL | `assets/opera/worlds/teacher/pearl_uncounted.png` | 128x128 | `4f71a7beff48024df5eb89a5cbd760148576ada6bf05fe784bd8d2828dba4037` |
| BUBBLES | `assets/castle/dirty_cleanup_2d/effects/fx_soap_bubbles.png` | 512x512 | `394d0fddb89237bf1e152060a31f585e71e37b54a46246bb1444c52454d15d08` |
| SPARKLE | `assets/opera/worlds/props/fx_stolen_sparkle.png` | 128x128 | `fad456ad3641cf67e194945ba9208108cd1f0cf9f35b8ee10516e18bc88eb772` |
| DIZZY | `assets/opera/worlds/props/fx_dizzy_stars.png` | 256x256 | `81bd48fc49666a365c84792fabc6a0313cfa78d8e431bcec1024a4b14d81c7a2` |
| RIBBON | `assets/kart/boost_ribbon.png` | 1024x256 | `b2617ce45be09837625bf21e145ef37401a87b9104f576c6093c3e44f912feb5` |
| GAUGE | `assets/opera/worlds/widgets/widget_gauge_racer.png` | 1024x608 | `21cb4e5ca4a9b91610b39938b8f76135db0fb978608a00aba4677a759c3dd56a` |

Native pixel boxes for CANAL are listed in `TRACK.md` section 1.

## 2. Requests, in priority order

| ID | Output path | Source | Operation | Acceptance |
|---|---|---|---|---|
| A1 | `assets/racer/tracks/pearl_canal/floor.png` (2048x2048) | CANAL | Re-project the painting's lane, curb, wall, sand and infield onto the course bands (recipe in `TRACK.md` section 5) | Band edges within 4 units of the engine's field; nothing the painting lacks |
| A2 | `assets/racer/tracks/pearl_canal/billboards/pearl_start_arch.png` | CANAL 45,280-285,600 | Isolate the pearl starting arch. The painting shows it turned; make it face the camera by mirroring its better-preserved half about the arch's centre line. Opening transparent | Aspect 330:250; kart reads through the opening; no new pearls or ornaments |
| A3 | `.../billboards/ribbon_arch.png` | CANAL 1386,252-1640,640 | Isolate the ornate arch, post and pink checkered ribbon with its bow; frontal by mirroring the arch half; ribbon kept low across the opening | Aspect 330:250; ribbon pattern unchanged |
| A4 | `.../billboards/pearl_arch.png` | CANAL 367,187-532,317 (or 1151,162-1291,317, whichever is cleaner) | Isolate one lilac pearl arch, frontal by mirroring; opening transparent. One card serves both arch positions | Aspect 330:260 |
| A5 | `.../billboards/pavilion.png` | CANAL 727,192-1000,455 | Isolate the pearl-dome pavilion with its steps and base; keep any coral that overlaps the base, or crop above it | Aspect 340:320; bottom edge is the ground line |
| A6 | `assets/racer/tracks/pearl_canal/skyline.png` (4096x256) | CANAL top band | Lay crops of the top band side by side and mirror them into a seamless loop (recipe in `TRACK.md` section 6) | Left and right edges join; band in rows 28-256 |
| A7 | `assets/racer/pickups/gem_buoy_teal.png`, `_lavender.png`, `_pink.png` | CANAL x 432-572, 762-905, 1066-1206 (y 450-640) | Isolate each gem buoy (orb and pearl-ringed float) as its own card | Square-ish 56:60; orb colour unchanged |
| A8 | `.../billboards/pennant.png` | CANAL 212,57-312,197 (or any of the four) | Isolate one pennant on its pole | Aspect 110:190 |
| A9 | `.../billboards/coral_cluster.png` | CANAL 0,600-245,935 or 1496,771-1646,931 | Isolate one coral cluster | Aspect 200:150 |
| A10 | `.../billboards/pearl_clam.png` | CANAL 202,771-377,901 | Isolate the open clam with its pearl | Aspect 170:110 |
| B1 | `assets/racer/pickups/pearl.png` | PEARL | Copy at 128x128 (already a clean isolated pearl) | Reads as the same pearl as the HUD |
| B2 | `assets/racer/pickups/item_bubble.png` | BUBBLES | Crop the largest single bubble to a square | One bubble, no neighbours |
| B3 | `assets/racer/karts/imp_kart_straight.png` (627x627) | KART_EMPTY + IMP_FLEE | Composite: seat the imp from IMP_FLEE (seen from behind, glancing back) in the empty kart, framed like KART_S (contact point near 335,546). The engine tints it lavender at runtime; do not recolour | Same scale and ground line as Roshan's kart |
| B4 | `assets/racer/karts/imp_kart_left.png`, `_right.png` (optional) | B3 | Rotate the B3 composite about 6 degrees each way; no repaint | Ground line kept |
| B5 | `assets/racer/pickups/kelp_patch.png` | CANAL kelp fronds near 60,60-170,210 | Isolate one frond cluster and lay it flat (rotate 90 degrees, squash to 52:22) | Same greens as the painting |
| B6 | `assets/racer/pickups/sparkle.png` | SPARKLE | Copy | |
| B7 | `assets/racer/pickups/dizzy_stars.png` | DIZZY | Crop to 2:1 around the ring | |
| C1 | `assets/racer/icons/zoom.png` | RIBBON | Crop one wave of the ribbon into a square; clean the green fringe near 88,130 | Reads as speed at 77 px |
| C2 | `assets/racer/icons/sparkle.png` | SPARKLE | Copy | |
| C3 | `assets/racer/icons/kelp.png` | B5 isolate, upright | Square crop | |
| C4 | `assets/racer/icons/pearls.png` | PEARL x3 | Arrange three copies in a triangle | |

## 3. Not requested (the engine's drawing stays)

- **Touch controls.** The green stick, red brake and item-bubble button are
  code-drawn in the owner's colours. An existing button (GAUGE, the
  pearl-dome turbo button near 55,145-300,330) could be recoloured instead;
  that waits for owner question Q2 in `README.md`.
- **HUD.** Lap flags, the pearl meter, leader faces (crops of the existing
  Roshan and imp art), the minimap, the countdown lights, the wrong-way arrow
  and the confetti. No runtime-quality source exists for the countdown
  lights or confetti; the review-only 07-21 cards are not runtime art.
- **Roshan's kart.** It keeps the approved chase sprites
  `assets/kart/chase/kart_{straight,left,right,boost}.png`.

## 4. Gaps (owner decision; nothing requested)

1. No source shows the imp in a kart; B3 composites one from existing parts.
2. The painting shows the arches turned, not face-on; A2-A4 use mirroring.
   If mirroring looks wrong on the device, the owner decides whether a
   targeted cleanup is acceptable.
3. Runtime-quality control, countdown and confetti art.
4. New voice lines (see `VOICE.md`).
