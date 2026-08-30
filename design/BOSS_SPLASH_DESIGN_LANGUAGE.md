# Boss Splash Design Language

Boss splashes are short, full-screen, true-2D gameplay introductions. They
are not cinematic delivery frames. Their job is to make a new boss feel
special while teaching a non-reader the boss's one important rule before play
resumes.

## Visual grammar

- Use the fixed 1280×720 storybook canvas and `StorybookUI` colours, violet
  contours, pearl surfaces and gold accents.
- Give the boss one side of the frame and integrate large, stacked display
  type into the other. A radial character burst, angled title field and two
  broad diagonal colour slashes create energy without adding a high-overdraw
  full-screen texture or falling back to ordinary menu-card UI.
- Reuse the boss's approved gameplay art. The splash must never redraw or
  reinterpret the character when an accepted pose already exists.
- Use a large name, a short boss-kind line and picture marks. Reading is never
  required to understand the action.
- Echo the live gameplay tell exactly: same icon, colour, pulse rate and
  relative placement. The splash is the first safe lesson, not decorative
  misdirection.

## Motion grammar

Every splash follows the same three-beat sentence:

1. **Action:** the boss enters with its signature movement.
2. **Identity:** the boss holds its clearest personality pose.
3. **Tell:** the vulnerable point or required interaction flashes exactly as
   it will during play.

The complete sequence stays near three seconds, blocks gameplay input, needs
no tap to advance and exits automatically. It may animate approved atlas
frames and Godot-native UI transforms; it must not add 3D staging or create a
new fail state.

## Grand Puff implementation

`BossSplash2D` reuses `DustBunnyBossSprite.make_sprite_frames()` so the splash
plays the shipped `jump` and `laugh_vulnerable` frames. Its gold badge uses the
same fallback star and the same 22-radian-per-second strobe formula as the
live Dust Bunny battle. No new raster asset or generation was needed.

The post-victory `DayTwoTransition2D` is a separate picture-first story bridge:
moon down, sun up, the approved Sky Lagoon castle revealed, and the approved
Opera/Craft/Kitchen room medallions lit. It accompanies the saved Day One
policy change that unlocks jobs and the Opera House.

## Acceptance audit

Review renders are scored on five one-point lanes: composition and hierarchy,
project-art cohesion, motion and personality, non-reader tell clarity, and
mobile/technical fitness. A splash or story bridge needs at least 4.5/5 with
no lane below 0.8.

The accepted 2026-08-30 mobile-renderer review scored:

| Sequence | Composition | Art cohesion | Motion | Tell clarity | Mobile fitness | Total |
|---|---:|---:|---:|---:|---:|---:|
| Grand Puff splash | 0.95 | 0.90 | 0.95 | 0.95 | 0.90 | **4.65/5** |
| Day Two bridge | 0.95 | 1.00 | 0.90 | 0.95 | 0.90 | **4.70/5** |

Grand Puff has a clear character/title split, expressive jump-to-grin acting,
and an unmistakable battle-authentic star strobe. The Day Two sunrise and
castle communicate the new day at a glance; separated room medallions and the
matching voice event communicate the unlocks.

The ignored review set is produced by `scripts/probe_dust_boss_shots.gd`.
Its visual-only clock owns deterministic review beats; production presentation
continues to use real frame delta.
