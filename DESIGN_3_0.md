# Mermaid Roshan Undersea Adventure 3.0 — What Changed and Why

Built from the critical audit in AUDIT_3_0.md. Theme of this revision: **finish the game**
(give it a beginning, a guide, and an ending) and **make it run everywhere** (PC, Android,
iOS, gamepad, touch, mouse, keyboard).

## Platform & performance

- **Forward Mobile renderer** (was Forward+). Single-pass Vulkan renderer that actually
  ships on phones; Metal on iOS, works fine on PC.
- **Stretch: canvas_items + expand**, base 1280×720, landscape sensor lock. The UI scales
  to any phone, tablet, or desktop window; no fixed-pixel HUD at 2400×1080 anymore.
- **etc2/astc VRAM compression** enabled for mobile texture memory.
- **Quality tiers — "Sparkly" and "Speedy"** (pause menu, persisted, auto-Speedy on
  mobile): sun shadow on/off, bloom on/off, every-other pearl light, plankton density,
  3D resolution scale 1.0/0.8, flora distance-fade at 150 m.
- **Animation culling**: all 128 creature AnimationPlayers pause beyond 95 m (Speedy) /
  160 m (Sparkly) of the player and resume on approach. Biggest CPU win on old phones.

## Input — one game, four input styles

- **Touch**: floating virtual stick (appears where the left thumb lands), big round
  JUMP/THROW action button bottom-right, ≥110 px tap targets in every minigame UI.
- **Gamepad**: left stick + A (jump/throw), face buttons in melody/seek, Start = pause.
- **Keyboard**: WASD/arrows + Space, ESC = pause.
- **Mouse**: click to throw, click diamond buttons, drag in dolls game.
- Every minigame is completable with one finger on a phone screen:
  fetch = tap button; seek & melody = tap the on-screen color diamond;
  dolls = drag or stick; race = swim through big forgiving rings (8 m hit radius).

## The game now has an arc

1. **Onboarding**: first session shows three timed hints in simple read-aloud language.
2. **Sparkle the guide fish**: a glowing golden fish swims ahead of Roshan, always
   pointing toward the nearest friend whose game isn't won (then toward pearls). No more
   empty-ocean confusion; no UI map needed at age 4.
3. **Progress is visible**: a gold star hangs over every friend whose game was won.
4. **Pearl pickups celebrate**: sparkle burst + chime + voice.
5. **The finale**: winning the 5th trophy gathers all five friends in a swimming circle
   around Roshan with rainbow firework bursts and a brand-new celebration track
   (synthesized C-major, 96 bpm). The game now *ends* — then keeps playing freely.
6. **Progress persists** (user://reef_save.json): friends met, games won, finale seen,
   plus quality & music settings. Quitting no longer erases a child's afternoon.

## Settings & safety

- Pause anywhere: ⏸ button (touch/mouse), ESC, or Start. Big buttons:
  Keep Swimming! / Graphics / Music.
- Music keeps playing while paused (calmer for kids than sudden silence).

## Validation (headless bot, every build)

- Parse checks on all scripts; full import; scene probe (node census).
- Minigame bot wins all 5 games through the real input paths, asserts cutaway arenas,
  save-file write, finale trigger, and 5/5 persisted wins after reload.
- probe_load.gd boots a second session and asserts trophies/stars restore.

## Still open (next revision candidates)

- FFT ocean surface graft (example/Example.tscn must be confirmed under 4.4).
- Idle/voice variety (more recorded lines), ambient bubble SFX bed.
- Texture downscale presets per export target (2K → 1K mobile).
- Android/iOS export presets + icons.
