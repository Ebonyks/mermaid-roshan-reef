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

## Grand Puff interactive lesson — 2026-09-12

Owner-authorized playable revision: the Grand Puff splash introduces personality
without a fake gold tap. Other bosses retain the default splash sequence.
The first movement accepts any direction; the first danger shape holds its
anticipation while Roshan remains inside. Leaving any edge starts the actual
jump. A later harmless bump restores the movement demonstration until the next
clean dodge. A real dodge opens the real gold counter with an eight-second first
window. Learned movement, dodge, counter and dash use additive save keys.
The first earned exchange offers an optional double-tap demonstration. Ordinary
movement remains sufficient throughout. Recovery is 1.8 seconds (4.6 seconds
for the first optional dash lesson, allowing the landed-response voice to finish), and the ending has no total-time floor.
One optional contact-scattered dust tuft appears after the first counter; it
cannot damage the boss or grant progression. Existing art supplies landing dust
and the counter uses Roshan's existing point pose with a Canvas sparkle connection.

Implementation/evidence: [audit impact](audit_impacts/grand-puff-intuitive-20260912.json)
and [clip contract](animation/grand_puff_encounter_clips_v1.json).
Phone, child and owner play acceptance remain open. This change does not close
whole-game touch, visual, play or 2D migration findings.
The previous source is preserved on `rollback/grand-puff-before-intuitive-20260912`
at `d33f2ddef98aa39af7cc2b2d066794945a024550`. Roll back by reverting only the
redesign commits on a fresh topic branch, then validate and integrate normally;
keep accumulated saves and Android version codes advancing.

### Storybook cue revision — 2026-09-12

The owner's subsequent presentation direction replaces Grand Puff's boxed caption,
finger demonstrations, geometric countdown and detached progress row with animated
approved effect art. Dust gathers along the same locked landing boundary, with a
quiet ink seam preserving its exact edge. Bubble currents invite movement; two
bubble beats precede a faster wake for the optional dash. The genuine counter
opening unfolds a gold star, and Roshan's point sends a curved sparkle response.
Landing and earned exchanges shed bounded dust plumes. Captions remain plain text.
These effects grant no input, damage, save or reward authority. Existing assisted
lesson timing and freely chosen destinations remain unchanged.

The [v2 choreography contract](animation/grand_puff_storybook_cues_v2.json) supersedes
v1 effect presentation only; v1 gameplay timing and character-pose reuse still apply.
See the [presentation impact](audit_impacts/grand-puff-storybook-cues-20260912.json)
for validation and open acceptance. The preceding playable revision is preserved on
`codex/grand-puff-intuitive-20260912` at
`002320548b88c3fae420c130ebaba57365ed4af0`; this presentation can be reverted
independently through the normal tested integration workflow.

### Shared boss attack convention — owner direction 2026-09-13

Enemy attack warnings follow **aim → locked flashes → launch**. The aiming
animation originates from the enemy and visibly travels or grows toward its
chosen footprint. Arrival is followed by three deliberate local flashes at a
fixed location, confirming commitment; then the enemy attacks that location.
The warning never follows Roshan after commitment, never disappears completely
during a dim interval, and stays steady through the active attack. Purple is
Grand Puff's aiming/early-lock identity; the third flash shifts to coral-peach
to announce imminent launch and stays warm through the strike. Gold remains
the separate earned counter cue.

Grand Puff's jump sends a round two-arm purple swirl out from beneath him,
rotating and unfolding to its final footprint. His charge grows two thick
purple bands from his floor position, unfolding two painted dust crests
and gathering a broad dust front between their ends. The rejected
charge-end vortex is removed. Both settle before the same three lock flashes. The first learning
hold occurs on arrival, before the timed flashing sequence continues, rather
than freezing the marker midway through travel. Warning durations are 2.2–2.7
seconds, with 35% for aiming and the rest for the three flashes. Free movement,
dash, no-loss assistance, geometry and saved progress retain their owners.

This supersedes the v2 dust-outline warning presentation. The other v2 response
and lesson effects remain. [v3 clip contract](animation/grand_puff_attack_windup_v3.json)
and [impact/evidence](audit_impacts/grand-puff-attack-windup-20260913.json) record
the scoped implementation. `EncounterWarningCue2D` supplies the reusable phase
contract for other bosses; their individual presentations are not claimed
converted by this document. New or revised boss attacks must follow this trope.
Owner visual/play, child and device acceptance remain open.

The owner's subsequent 4.75/5 restyle commission keeps that choreography and
raises the presentation target: broad painted purple curls, thin plum contours,
matte lavender value bands, tapered streams and a gathering painted dust front at the
charge destination. The jump retains its painted vortex; the owner rejected
the endpoint vortex on the charge and asked for the distinct third-flash cue. Details cluster at origin and destination; the actual hazard
boundary remains precise and visible. The target is not an awarded score.
[Refinement evidence](audit_impacts/grand-puff-painted-warning-20260913.json)
tracks source reuse, any new art gap, runtime review and open acceptance.
