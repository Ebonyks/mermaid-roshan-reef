# Mermaid Roshan — Critical Audit (pre-3.0)
Audited June 12, 2026 against goal: delightful, complete game for a 4-year-old on PC / Android / iOS.

## GAMEPLAY — biggest gaps

**G1. No persistence (CRITICAL).** Every launch starts at zero pearls / zero trophies. A
4-year-old plays in 10-minute bursts; losing every trophy between sessions breaks the core
reward loop. No save file exists anywhere in the project.

**G2. No ending (CRITICAL).** Winning all 5 trophies and 10 pearls produces… nothing. The
HUD counter fills and the world shrugs. The game has a middle but no climax — the most
important moment for a child (the payoff) is missing.

**G3. No active wayfinding.** Beacon pillars help at distance, but the world is 540 m
across and mostly open water. Between friends there is nothing pulling the player forward.
A child who wanders to the rim has no idea where to go.

**G4. Onboarding is one static text line.** "Find the glowing friends" assumes reading
ability the target player does not have. No control hints, nothing timed, nothing repeated.

**G5. Stale instruction text.** Fetch still says "Press JUMP when the power bar is BIG!"
— the power bar was removed a build ago. Trust-breaking even for adults reading aloud.

**G6. Won-state is invisible in world.** A friend whose game was already won looks
identical to one never played. No star/marker — a child can't see their own progress.

**G7. Pearl pickup is flat.** The pearl just vanishes (light + halo freed). One pitched
voice clip. No burst, no sparkle, no chime — the most frequent reward in the game has the
weakest feedback.

**G8. No pause, no settings.** ESC does nothing. No music toggle, no quality switch, no
resume screen. On mobile an accidental thumb has no escape hatch.

## INPUT / PLATFORM — blocking for the stated 3.0 targets

**I1. Zero touch support (CRITICAL).** No virtual stick, no touch buttons. The game is
strictly unplayable on Android/iOS today.

**I2. No stretch/scaling mode set.** UI is fixed 1280×720 pixels; on a 2400×1080 phone the
HUD renders tiny in a corner, on small windows it clips. Needs canvas_items stretch +
expand aspect.

**I3. Input is hard-coded.** `Input.is_physical_key_pressed(...)` inline in 6 places; no
InputMap actions; gamepad/keyboard/touch each handled ad-hoc per minigame.

**I4. Touch target sizes.** Melody diamond buttons are 72 px — below the ~96 px minimum
for small fingers. Seek accepts only gamepad face buttons or swim-tag; on touch neither is
reliable.

## GRAPHICS / PERFORMANCE — wrong renderer for the target hardware

**P1. Forward+ renderer (CRITICAL for mobile).** Desktop-class clustered renderer; on a
3–4-year-old Android phone it is unsupported-to-unusable. Forward Mobile is the correct
4.4 choice (Vulkan, single-pass, light-limited).

**P2. Unbudgeted dynamic lights.** ~10 pearl omnis + 5 beacons + hero fairy lights + 3
ship lanterns + arena lights, all live simultaneously. Forward Mobile clamps per-mesh
lights and old GPUs crawl. Needs a quality tier that culls non-hero lights.

**P3. Sun shadow always on.** Single biggest mobile GPU cost in the scene; must be
tier-gated.

**P4. No texture compression policy.** 2K PBR sets everywhere with no etc2/astc import
setting — VRAM blowout on older phones.

**P5. Glow/bloom always on; plankton GPUParticles uncapped.** Fine on PC, needs Speedy
tier reduction.

## AUDIO

**A1.** One voice clip total; no pickup chime, no ambient bubbles.
**A2.** No finale/celebration track (no finale exists — see G2).

## CODE STRUCTURE

**C1.** main.gd is a 1,751-line monolith; quality and touch belong in their own scripts.
**C2.** Probes don't cover save/load or the (missing) finale path.

## 3.0 PLAN (what this build implements)

1. Forward Mobile renderer + canvas_items/expand stretch + etc2_astc import + landscape lock (P1, I2, P4)
2. Quality tiers "Sparkly/Speedy": shadows, bloom, pearl lights, plankton, 3D resolution scale; auto-Speedy on mobile (P2, P3, P5)
3. touch_ui.gd: virtual stick (left), big context action button (right), auto-shown on touch devices (I1)
4. Diamond button UI shared by melody AND seek, enlarged to 110 px (I4)
5. save_state in user://reef_save.json: found/won per friend, finale flag, quality, music (G1)
6. Finale celebration: friends gather, rainbow confetti, new finale music, saved (G2, A2)
7. Sparkle the guide fish: glowing companion that swims ahead toward the next un-won friend (G3)
8. Timed onboarding hints in the first ~30 s, icon-simple language (G4)
9. Gold star Label3D over won friends (G6)
10. Pearl pickup: particle burst + chime + existing voice (G7, A1)
11. Pause/settings: ESC / Start / gear button — Resume, Quality, Music (G8)
12. Fetch text fix (G5); probes extended to save + finale (C2)

---

# Post-3.0 passes (same day)

## Beauty audit — every material reviewed

| Element | Was | Now |
|---|---|---|
| Water surface | flat translucent plane, plain color | animated shader: vertex waves + two scrolling caustic layers, sparkle emission, depth-varying alpha |
| Garden rock outcrops | literal BoxMesh boxes | Riley rock models (12 forms) with the 2K stone PBR |
| Scatter anemones/urchins | flat color + tip glow | polyp surface detail modulating albedo + glow |
| Scatter starfish | flat color + tip glow | star_detail surface texture |
| Fetch ball | plain orange sphere | classic 6-wedge beach ball bake, glossy |
| Arena floors (all 5) | single flat color discs | themed PBR: snow (bright sand+normal), nursery & concert (wood planks), meadow (leaf), sunset (warm sand) |
| Whole frame | neutral grade | color grading: saturation 1.18, contrast 1.06 — the "pop" |
| Guide | (golden fish) | Baby Eagle from the book (P02b cutout, with her packed bag) |
| Kept as-is | seagrass/kelp (already leaf-textured), Riley corals/creatures (phase-5 materials), pearls (rainbow shader), beacons, book-art sprites |

## Child-paced playtest (instrumented bot: 1.1-1.6s reactions, 30% wrong buttons, wandering swim)

**Before:** 215s session, travel gaps 27-37s (~45% dead time), fetch ran 30s, pearls collected: 0/10 (!) — they were never on the path a guided child swims.

**Fixes:** friend ring tightened 60-170r → 55-115r; pearls re-seeded along friend-to-friend routes; gentle helping current (+5.5 u/s) when swimming toward the guide; fetch throws shorter + Chuck 40 u/s; game-start countdown 4→2.5s; rematch cooldown 8→5s.

**After:** 154s session; gaps 11-21s, each gap contains ~2 pearl pickups (8/10 collected on the natural route); reward event every ~4s of travel; first game at 13s. Bot still 5/5 + save + finale.
