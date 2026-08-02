# Fable handoff — Lamba takes over the magician-game reveal

Owner decision, 2026-08-01: **replace the rabbit-fish / bunny-fish in the
magician game with Lamba.** The decision is final for the rebuilt 2D career
act. Lamba is the round white lamb established by
`assets/characters/lamb_0.png`; protected source art remains untouched.

## Completed by Codex

- Generated and human-reviewed native Lamba float, peek, and reveal cards,
  plus magician stage watch/swap/selector/decoy/final-reveal states.
- Removed the egg, lettering, rabbit anatomy, and fish anatomy from the new
  magician-game art while retaining Lamba's approved face, wool, ears, and
  gentle proportions.
- Replaced the runtime goal-prop source art. Old `bunny_fish_*` filenames are
  compatibility aliases only; their pixels now depict Lamba.
- Updated the rebuilt 2D act's visible instruction copy to say “Lamba” and
  “LAMBA CHASE.”

## Fable takeover tasks

Fable owns the remaining cross-system migration because it requires family
recording coordination and the legacy 3D act, neither of which can be safely
invented or destructively replaced in this art pass.

1. Coordinate new family recordings for the existing protected voice event
   slots `op_magician_vanish` and `op_magician_bunny_chase`. Do not modify or
   overwrite `assets/audio/voices/` until the owner supplies/approves the new
   recordings. The temporary on-screen copy already says Lamba; the current
   audio still says bunny-fish.
2. Replace the legacy 3D `opera_magician_bunnyfish.glb` actor and associated
   `scripts/opera_act.gd`, `scripts/opera_house.gd`, and probe terminology with
   an owner-approved Lamba 3D model or approved fallback. Preserve save keys
   and behavioral timing.
3. Once voice and legacy 3D coverage land together, rename the compatibility
   asset IDs and voice IDs to `lamba` aliases while retaining old IDs as save
   and resource compatibility shims.
4. Update the art-manifest probe only after the new 3D resource exists; never
   weaken the probe to accept a missing actor.

The original `assets/characters/lamb_0.png`, all family voice recordings, and
all existing friend-character source assets remain protected and unmodified.
