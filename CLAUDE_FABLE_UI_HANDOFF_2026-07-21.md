# Claude Fable handoff — storybook menu system

Date: 2026-07-21  
Work branch: `codex/menu-system`  
Base: fresh `origin/dev` at `203af2e4`  
Recovered design source: `75cf9b67` / `gen2/UI_PROTOTYPE_REVISIONS_2026-07-19.md`

## What was found

The UI improvement had already been designed and committed as four audited
image prototypes, but deliberately stopped before runtime implementation. The
selected images are under `gen2/ui_prototypes_2026-07-19/`:

- `hud_navigation_v1_1024x576.png`
- `pause_overlay_v1_1024x576.png`
- `craft_studio_v2_1024x576.png`
- `intro_story_v1_1024x576.png`

Do not ship those rasters as flat overlays. They are layout evidence only.

## Runtime architecture now in place

`scripts/storybook_ui.gd` is the shared design system. It provides the cool
paper/aqua/lavender field, navy-purple ink, mint/coral/gold focus roles,
storybook panels, pressed/focus states, responsive 1280x720 stages, neutral
back buttons, and the 110x110 minimum child touch contract.

No save keys were removed or renamed. No protected book, voice, or friend art
was edited. All menus still call their original reward, unlock, save, teardown,
and controller paths.

The runtime migration covers:

1. Exploration HUD: fixed status tray, top-centre objective card, centre-safe
   voice caption, visible bottom-left stick affordance, and 148px coral action.
2. Pause: 128px corner control; dominant resume; sticker, music, quality, and
   conditional neutral-exit tiles. Start/Escape raises the sheet from layer 12
   to 29 so it works over activity overlays; layer 30 fades still win.
3. Intro: protected art inside a native book frame, four shape pips, replay
   voice, explicit next, and 1.2-second hold-to-skip.
4. Craft: large live preview, 112px creature tabs, three part selectors, one
   active row of eight 112px colors plus rainbow, neutral back, large swim-away
   finish, and voice feedback when an unlock is short of pearls.
5. Wardrobe, Sticker Book, Critter Book, and Stuffie picker: shared panels,
   neutral 112px exits, large primary actions, and one active stuffie color row.
6. Tamagotchi care: a 128px stuffie launcher occupies the upper-right hand
   area at x=982, inset from the far-corner Pause control. It opens a shared
   storybook sheet with the live friend preview, current need, non-reading
   growth stars, five 126px care actions (feed, nap, bath, cuddle, play),
   injury/rest state, and friend switching. Menu care runs the same persisted
   care moments as the in-world thought bubbles; it is not a parallel reward.
7. Activity navigation: picture games, kart, dungeon, Opera House, and dance
   now use the same neutral back language instead of a small/alarming X.

## Fable visual-QA brief

Run CI first. The new `probe_ui_system.gd` checks runtime construction, overlay
layering, four intro pips, deliberate skip, neutral exits, one-row palettes,
and minimum touch geometry. Then capture these Mobile-renderer states at
1280x720 and at the actual phone's landscape resolution:

1. Reef idle, then active joystick and active action button.
2. Long objective plus speech portrait/caption; confirm no corner collision.
3. Pause in free swim and pause opened with Start from inside another overlay.
4. Intro pages 1 and 4, including two-character composition.
5. Craft body, accent, and detail tabs; locked Kitty/Birdie; completion flight.
6. Wardrobe classic/fairy locked/unlocked, Sticker Book, and Critter Book.
7. Stuffie picker with two starter friends and with all three friends unlocked.
8. Tamagotchi launcher beside Pause: content, active want, injured, and resting
   icons; then all five care buttons and the switch-friend path.
9. Picture game, kart armed-exit state, dungeon, Opera House, and dance exit.

Review at physical phone scale. Required acceptance points:

- no required target below 110x110;
- no status/objective/caption enters the bottom-left or bottom-right control
  zones;
- accepted taps show their pressed state within two rendered frames;
- selected, locked, toggle, and complete states remain distinguishable without
  relying on color;
- all child exits are neutral and preserve progress;
- the Speedy tier remains at or above the 30 fps target.

## Likely iteration points

- `craft_part == "third"` changes the saved third color used by rigged crafted
  friends, but the current layered 2D preview has only body/accent/line sheets.
  Do not recolor the protected line art. If the detail choice is not legible on
  device, add a small native color badge or request a separately-authored mask.
- The HUD medal suffix can become dense only on a highly completed save. Test a
  max-progress save and, if needed, move medal counts into a third icon row
  without restoring prose.
- The stuffie friend list currently has three roster entries and fits vertically.
  If the roster grows beyond four, move the left cards into a child-safe scroll
  container rather than shrinking them.
- Developer Mode remains intentionally compact and parent-facing; it is outside
  the child menu contract.

## Validation and promotion

Local static gates:

```text
python -m gdtoolkit.parser <changed .gd files>
python tools/lint_inference.py <changed .gd files>
git diff --check
```

Full gate (Godot machine or CI):

```text
GODOT=<Godot 4.4.1 binary> scripts/ci.sh
```

Do not merge into `dev` until the exact branch HEAD has a green probe run and
the Mobile screenshots above have been reviewed. Reconcile `origin/dev`, rerun
the gates, then merge to `dev`; never merge or push `master` directly.
