# Boss Splash Design Language

Status: domain guidance subordinate to
`design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md` and
`audit/MASTER_AUDIT_2026-08-09.md`. Runtime captures are diagnostic evidence;
only owner review can grant final visual acceptance or a 5/5 rating.

Boss splashes are short, full-screen, true-2D gameplay introductions. They are
not cinematic delivery frames. Their job is to make a new boss feel special
while teaching a non-reader the boss's one important rule before play resumes.

## Review history and rejected directions

The 2026-08-30 owner review rated the first implementation about 3/5. Its large
radial burst, diagonal colour slashes, angular title field and high-saturation
arcade geometry captured the event but not Mermaid Roshan's design language.
A later experiment with an oversized ornate task-card frame and tall banner was
also rejected as gaudy, distracting and poorly sized.

Those treatments are not reusable boss-splash language. Do not reintroduce:

- large opaque banners, title slabs or menu-card containers;
- full-screen neon, radial rays, halftone fields or broad diagonal slashes;
- rough flat polygons standing in for painted scenery or ornament;
- dense peripheral decoration competing with the boss or story reveal.

## Visual grammar

- Preserve the readable earlier composition: the boss owns the left side and
  restrained identity typography owns the right. The character remains the
  primary focal action.
- Use a cool, high-key painted field with broad value bands. A soft radial light
  may organize a focal zone, but it must not read as a solid geometric panel.
- Place type directly in the scene. A small event pill and a small picture-first
  tell pill are allowed; neither may become a large banner.
- Use established Storybook UI cues sparingly: one painted shell, a thin violet
  rule, a few pearls, and small gold highlights. Saturated colour is a peak, not
  the field.
- Use clean deep-indigo contours at 2–4 authored pixels on the 1280×720 canvas.
  Avoid scratchy hatching, noisy speed lines and heavy perimeter ink.
- Reuse the boss's approved gameplay art. Never redraw or reinterpret the
  character when an accepted pose already exists.
- Echo the live gameplay tell exactly: same icon, colour, pulse rate and relative
  placement. The splash is the first safe lesson, not decorative misdirection.
- Reading is supporting information only. The signature action and flashing
  vulnerability must communicate the rule without text.

For a new-day or chapter bridge, the destination artwork is primary. The castle
owns the Day Two composition; the painted dawn, clouds and sun support it. Room
medallions remain small and unboxed in the quiet periphery. Do not place the
castle or unlocks inside a large UI tray.

## Motion grammar

Every splash follows the same three-beat sentence:

1. **Action:** the boss enters with its signature movement.
2. **Identity:** the boss settles into its clearest personality pose.
3. **Tell:** the vulnerable point or required interaction flashes exactly as it
   will during play.

This is the shared anticipation → readable action → payoff → settle rhythm from
the canonical design language. The complete sequence stays near three seconds,
blocks gameplay input, needs no tap to advance and exits automatically. It may
animate approved atlas frames and Godot-native 2D transforms; it must not add 3D
staging or create a new fail state.

## Grand Puff and Day Two implementation

`BossSplash2D` reuses `DustBunnyBossSprite.make_sprite_frames()` so the splash
plays the shipped `jump` and `laugh_vulnerable` frames. Its gold badge uses the
same current fallback star and the same 22-radian-per-second strobe formula as
the live Dust Bunny battle.

`DayTwoTransition2D` is a separate picture-first story bridge: moon down,
painted sun up, the approved Sky Lagoon castle revealed, then approved
Opera/Craft/Kitchen room medallions wake at the edge. It accompanies the saved
Day One policy change that unlocks jobs and the Opera House.

The current refinement reuses existing castle, cloud, sun, shell, room and boss
art. No new raster generation, protected-asset edit or asset-license entry is
required.

## Acceptance audit

Review renders are scored on five one-point lanes: composition and hierarchy,
project-art cohesion, motion and personality, non-reader tell clarity, and
mobile/technical fitness. A candidate needs at least 4.5/5 with no lane below
0.8 before it is presented for owner acceptance.

The latest Mobile-renderer frames are an internal candidate, not an owner-granted
final rating:

| Sequence | Composition | Art cohesion | Motion | Tell clarity | Mobile fitness | Candidate total |
|---|---:|---:|---:|---:|---:|---:|
| Grand Puff splash | 0.90 | 0.90 | 0.95 | 0.95 | 0.90 | **4.60/5** |
| Day Two bridge | 0.90 | 0.95 | 0.90 | 0.90 | 0.90 | **4.55/5** |

The ignored review set is produced by `scripts/probe_dust_boss_shots.gd`.
Its visual-only clock owns deterministic review beats; production presentation
continues to use real frame delta. A runtime capture can expose hierarchy,
cropping, contrast and motion defects, but it cannot override owner style
judgment.
