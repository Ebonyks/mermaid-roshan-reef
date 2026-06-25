# Mermaid Roshan's Ocean World — Comprehensive Audit (build v3_49)

*Audited from the live reef2 source. This is a design + code audit with an emulated 1-hour playthrough, not a live visual playtest (the build here runs headless with no display). Where something can only be confirmed on-device, it's flagged "verify on device."*

Audience the whole design serves: **one ~4-year-old girl**, on a 3–4-year-old Android phone, in landscape, by touch. Every recommendation below is weighed against that.

---

## 1. Emulated 1-Hour Playthrough

**00:00 — Boot & intro.** Title → short voiced intro (Roshan sees Huluu in the sky, the storm, "I'll help you!"). Onboarding shows the touch joystick + action button. *Good:* short, voiced, skippable. *Risk:* the intro text assumes reading; for a non-reader the voice carries it, so make sure the intro voice always plays.

**00:02 — The reef (Level 1).** Open-world swim in a PBR-textured reef: coral groves, rocks, animated Riley-pack creatures, rainbow pearls to collect, beacon pillars for wayfinding, a custom animated water plane overhead. Roshan is a 26-bone rigged 3D model here. *Strength:* this is the most visually "finished" space — real textures, lit, dynamic. *Weakness:* with no guide character (removed earlier) a 4-yo may swim aimlessly; beacons help but aren't self-explanatory to a non-reader.

**00:06 — First friend game (whichever is nearest).** Swim to a friend → cut to a themed arena. Five friend games:
- **Chuck / fetch** — winter Lake Michigan (now with dock, boulders, shore path), throw the ball, real dog bark, splash = miss.
- **Faron / dolls** — 2D falling-baby catch over a nursery backdrop (now the 3 real baby images).
- **Evie & Lamb-a' / seek** — find the lamb behind a wiggly bush by swimming to it; grass meadow.
- **Gabby / melody** — catch 7 rainbow orbs by swimming into them; concert backdrop.
- **Harper & Fiona / race** — 3-story play-place climb to a slide.
*Strength:* genuine variety of verbs (throw, catch, find, collect, climb). *Weakness:* the games mix **2D UI minigames** (dolls is a flat CanvasLayer) with **3D arena games** — a jarring tonal jump mid-flow. See §5.

**00:15 — Pearl economy.** Pearls respawn; the ghost-ship Pearl Shop (walk-in cabin) sells a tiara, prettier tail, Can of Beans (speed boost). *Strength:* a real reason to collect. *Weakness:* a 4-yo may not grasp "currency"; the shop is a bonus, which is fine.

**00:25 — Treasure cavern.** Repeatable dive for +3 pearls. Good pacing breather.

**00:35 — All 5 trophies → finale → Level 2 unlocks.** A rainbow conch portal rises; swim up into it.

**00:38 — Sky Lagoon (Level 2).** Grassy floating island: lamp-lit path with book-art banners, **rivers now carved into the ground (CSG) with real aquatic fish**, a pond, rainbow arc, clouds, CC0 trees/bushes. Find **3 Dream Stars** (iridescent, magnet-assisted) → castle door opens with a cutscene.

**00:48 — Grand Hall (Level 3).** Marble + red carpet, columns, chandeliers, **stone keep interior**, throne with **Princess Huluu** and the **Crown Star**. Wall-picture minigames (snowman, garden, trampoline, rainbow slide→3D, xmas). A **secret room** holds **Daddy mermaid** with his real recorded voice. Reaching the Crown Star awards the tiara and returns to the ocean.

**00:58 — Wind-down.** Replay favorite minigames, dress Roshan in the tiara, listen to Daddy. *Observation:* after the Crown Star there isn't a strong "what now" loop for a 4-yo; see expansion ideas §6.

**Net:** ~45–55 min of fresh content, then replay. That's a strong amount for the audience. The main felt problem across the hour is **tonal/visual inconsistency** between spaces and **reading-dependent guidance**.

---

## 2. Strengths

1. **Book fidelity / personal meaning.** Real cut book art, canonical character names, and—most powerfully—**real family voices** (Daddy, the "thankyou", Roshan's consistent voice). For this specific child this is the game's superpower; nothing else matters as much.
2. **Verb variety.** Throw, catch, find, collect, climb, stack, grow, bounce, decorate — unusually broad for a toddler game.
3. **Forgiving by design.** Magnets pull the player to stars/goals, proximity-based wins, one-tap actions, no fail states that punish. Correct for age.
4. **Cohesive "dream" intent** and a clear 3-act structure (ocean → sky lagoon → castle).
5. **Original, IP-respectful** core (the licensed-character cameos are personal-use only; assets are CC0/own/royalty-free with a ledger).

---

## 3. Weaknesses, Risks & Bugs

**Visual/tonal consistency (biggest issue).** The game mixes at least four art languages:
- 2D anime **cut-out billboards** (Roshan, friends) that always face camera and read flat from the side;
- **PBR-textured** reef (high fidelity);
- **flat-colored boxes** for the castle/play-place (low fidelity);
- **low-poly Kenney** nature (mid fidelity);
- **flat 2D UI** minigames (snowman/garden/etc.) that break the 3D frame entirely.
These don't share a lighting model, outline treatment, or color grade. A 4-yo won't articulate it, but it reads as "several different games stitched together."

**Reading dependency.** HUD strings ("Swim up the stairs to Princess Huluu and the Crown Star!") are invisible to a non-reader. Guidance leans on text + beacons. The voice lines help but aren't tied to every objective.

**Wayfinding.** With the guide character removed, the reef can feel directionless. Beacons exist but a 4-yo won't decode them.

**Performance risk (verify on device).** CSG ground rebuild, many OmniLights (the rainbow slide adds 8 animated ones), multiple particle systems, billboard sprites — all on a 3–4-yo phone. Watch frame rate in the Sky Lagoon and rainbow slide especially.

**Billboard side-view.** Cut-out characters look paper-thin when the camera swings beside them (visible in your screenshots). Inherent to the sprite approach.

**Minigame "juice" inconsistency.** Some games now pause on the result with confetti (good); confirm all five 2D games and the 3D ones feel equally celebratory.

**Recently-fixed, keep an eye on:** the rainbow-slide crash (synthetic friend had no `node`) — fixed v3_47; Daddy voice leaking into the seek game — fixed v3_42; door-open reliability — self-healing v3_39. Regression-test these after any change near them.

---

## 4. Graphics & Visual-Effects Audit (consistency between stages)

| Dimension | Reef (L1) | Sky Lagoon (L2) | Castle (L3) | 2D minigames |
|---|---|---|---|---|
| Surfacing | 2K PBR | grass/dirt textured + flat boxes | mostly flat-color + some stone/wood | flat UI panels |
| Lighting | lit, glow | sun + shadows | warm omnis | unlit UI |
| Characters | rigged 3D Roshan | billboard sprites | billboard sprites | sprite textures |
| Grade | cool/teal | bright/warm | warm interior | per-theme gradients |

**Findings:**
- **Roshan's representation is inconsistent** — a rigged 3D model in the reef but a flat billboard elsewhere. Pick one (the rigged model everywhere, or the sprite everywhere) for identity consistency. The rigged model is the higher-quality choice.
- **Castle interior is under-textured** relative to the reef — lots of flat-color boxes (floor tiles, columns, throne) next to a few stone/wood pieces. Bring the keep's stone/wood treatment to the columns, dais, and battlements so L3 matches L1's fidelity.
- **Glow/bloom differs per stage** (strong in reef, softer in lagoon). Pick one bloom level so transitions don't "pop."
- **The water is flat** (FFT ocean is disabled for performance) — acceptable, but the custom plane could get a stronger normal/sparkle to feel less like a sheet.
- **Effects that work well:** iridescent Dream Stars, the door-open cutscene, sparkle bursts, the new flashing rainbow-slide lights, falling snow in the fetch scene.
- **Effects to standardize:** confetti/win celebration should be identical across all minigames; sparkle color palettes vary — unify to the rainbow palette for brand identity.

**Does everything make sense?** Spatially yes (the 3-act flow is logical, and removing the duplicate ocean ring helped). The biggest "sense" gaps are *non-reader guidance* and *art-style whiplash*, not layout.

---

## 5. Prioritized Improvement Log

**P0 — highest value for the child / lowest risk**
1. **Voice every objective.** Whenever the HUD changes objective, play a matching voice line ("Find three sparkly stars!", "Go see Daddy!"). Non-readers then never need the text. (Reuse the existing `_say`/voice pipeline.)
2. **Add a friendly wayfinding pointer for non-readers** — not the old arrow, but a gentle trail of sparkles or Roshan's own "helping current" that always drifts toward the next objective. Toddlers follow motion.
3. **Unify the win celebration** across all minigames (same confetti + chime + 1.6s hold already added to some).

**P1 — consistency & polish**
4. **One Roshan representation** everywhere (prefer the rigged 3D model; if perf forbids it in 2D games, at least use the same cut-out art consistently).
5. **Texture the castle interior** (columns/dais/battlements) to match the keep's stone/wood.
6. **Standardize bloom/grade** across stages; unify sparkle palette to rainbow.
7. **Performance pass on device** — cap the rainbow-slide lights, check CSG cost, consider the "Speedy" quality tier auto-enabling on low-end.

**P2 — depth**
8. Replace remaining flat-color boxes with simple textured materials.
9. Give the flat 2D minigames a subtle 3D frame (a shelf/diorama) so they don't break the world as hard.

---

## 6. Expansion Ideas (to make it richer for a 4-yo girl)

Ranked by joy-per-effort for this child:

1. **Dress-up Roshan** — a small wardrobe (tail colors, bows, the tiara, the Bluey backpack toggle). Customization is the #1 engagement driver for this age/audience and you already have the cosmetics system.
2. **More family/friend voice lines** — the real recorded voices are the magic. Add Daddy lines around the world, a Mommy character, named friends greeting Roshan by name. Cheap to add, huge emotional payoff.
3. **A photo / hug moment** — let Roshan "hug" a friend or take a sparkly photo when a game is won; toddlers love affection beats.
4. **Daily-ish surprise** — a new pearl color or a balloon that appears each session in a random spot, to reward "opening the game again."
5. **Simple pet** — a baby fish or Chuck that follows Roshan around the reef (re-add a follower, this time as a companion not a guide).
6. **Music room / instrument** — tap lily pads or shells to make pentatonic notes (you already have pickup tones); pure sandbox play.
7. **Bigger castle interior** — rooms to explore (a bedroom with her book art, a kitchen tied to the Daddy-cooking pages) for free-roam after the Crown Star.
8. **Gentle seasonal swap** — the xmas tree game hints at this; a snow toggle for the lagoon would feel magical.

---

## 7. One-Paragraph Verdict

This is already an unusually heartfelt, content-rich toddler game with real personal meaning that no commercial title can match. The two things holding it back from feeling like *one* polished game rather than a collection are (a) **guidance that a non-reader can follow without text** and (b) **a consistent art language** (one Roshan, one bloom level, textured interiors, unified celebrations). Fix those two, then lean hard into **dress-up + more real family voices** for expansion — that's where a 4-year-old's delight compounds.
