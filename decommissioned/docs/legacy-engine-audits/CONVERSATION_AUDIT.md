# Mermaid Roshan — Conversation Audit (every discussed detail vs shipped state)
Audited June 13, 2026 against the live reef2 build.

## CORE GAME — all shipped
- Open-world undersea game built from the book's characters — YES (reef2, Godot 4.4)
- Swimming on X-Y plane, floaty physics, jump/up button — YES (player.gd)
- 26-bone procedural swim: tail + arms + head + neck + hair — YES
- Roshan from the actual book art (inflated mesh, 2K texture, lit) — YES
- Canonical character names (Evie/Lamb-a', Harper & Fiona, Faron, Gabby, Wacky & Chuck, Huluu) — YES
- Music: world theme + per-minigame tracks + finale + cavern + shop + banjo — YES

## MINIGAMES — all 5 + 2 hub activities shipped
- Wacky & Chuck FETCH: Roshan holds ball, winter Lake Michigan, lake-splash buzz = miss, losable — YES
- Evie & Lamb-a' SEEK: real lamb model, button/tap diamond, living meadow decor — YES
- Faron DOLLS: 2D catch game, book-art plush dolls, nursery backdrop — YES
- Gabby RAINBOW: catch 7 ROYGBIV orbs, Gabby + concert stage backdrop (replaced memory game) — YES
- Harper & Fiona PLAY-PLACE: 3-story climb, ballpit, trampoline, physics finger-curtains, big slide; tuned easy for 4yo — YES
- Cutaways to new location/music/style; talk-to-start; 10-15s microgame pacing — YES
- Controller-diamond layout on shells/seek; gamepad + touch + mouse + keyboard — YES

## SHIPS & ECONOMY — shipped
- Floating ghost ship = walk-in PEARL SHOP (plank cabin, octopus keeper, see-through walls, spawn inside) — YES
- Cosmetics: Glowing Tiara (on head bone), Extra Pretty Tail, Can of Beans — YES
- Can of Beans: 2x speed 10-20s + banjo + toots; buy sound = your THANKYOU clip — YES
- Sunken wreck = TREASURE cavern dive (+3 pearls, repeatable) — YES
- Pearls = currency, respawn on stage-complete / ship-exit; pickup plays DIATONIC scale — YES

## LEVEL 2 — shipped (original design, not a Mario clone)
- 100% gate raises a rainbow conch portal; the sea drains into a river at the top — YES
- Sky Lagoon: real grass, warm sun + shadows, 400-flower field, groves, pond, rainbow, butterflies — YES
- Original Pearl Castle: moat, drawbridge, towers, 3 Dream Stars open the door (visible slide-open) — YES
- Interior Grand Hall: marble + carpet, columns, sconces, tapestries, chandeliers, her book art framed — YES
- Princess Huluu on the throne; Kaitlyn Rose mermaid stained-glass window (re-keyed clean) — YES

## VISUALS / PLATFORM — shipped
- Forward Mobile renderer, UI stretch, quality tiers (Sparkly/Speedy), anim culling — YES
- Dream-world art pass (killed neon look): lit translucent flora, soft caustics, calmer grade — YES
- Beauty pass: 2K PBR ground/rocks/wood, beach-ball, themed arena floors — YES
- Save system, finale celebration, pause menu — YES

## AUDIO / VOICE — shipped this pass
- Roshan: 10 lines, consistent 4-6yo girl voice (Piper neural TTS, pitch+formant shaped, sped up) — YES
- Roshan SPECIAL lines: whale, floating ship, sunken wreck — YES
- 3 alternating pearl phrases + 3 idle voice lines (idle voice command) — YES (added in audit pass)
- Each friend has a distinct voice (Huluu/Evie/Harper/Faron/Gabby/Wacky/Shop/Sparkle/Everyone) — YES (added in audit pass)
- Text replaced with audio + portrait speech-bubble; intro rewritten short + voiced — YES

## DEFERRED / OPEN (not yet in, by design or pending)
- FFT ocean surface (godot4-oceanfft) graft — DEFERRED: still a custom water shader; awaiting your OK to graft the heavier surface (mobile-cost tradeoff).
- Higher-end voice (ElevenLabs) or real recordings of your daughter — OPTIONAL upgrade; files drop straight into voices/.
- Friend voices are "close enough" Piper lines (you said only Roshan needs cohesion) — can deepen to 2-3 lines each on request.
- Flamingo plush (early upload) — never saved as a file; not integrated. Re-share it and I'll add it to the creature roster.
- Wind Waker hard cel-shade — SUPERSEDED by your later "Avatar Way-of-Water / dream world" direction.
- Minigames built FROM the wall portraits — your stated "later, organically" idea; not started yet.
