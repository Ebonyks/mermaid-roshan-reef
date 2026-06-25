# Asset Licensing Audit & Free-Source Replacement Status

_Run 2026-06-25 on branch `claude/replace-assets-free-sources-lnplz7`._

Goal of the queued task: make the asset set **free-to-use and as high-quality as possible** for a
**freeware** release. (Original framing was "CC0-clean"; the project owner has since clarified —
2026-06-25 — that strict CC0 is **not** required: "this project will be freeware, use whatever
assets are of highest quality.")

This document records (1) the audit, (2) the **network blocker** that prevents downloading a
higher-quality replacement pack, and (3) the resulting decision.

---

## 1. TL;DR

- **Freeware decision (2026-06-25):** strict CC0 is no longer required; any free-to-use asset is
  acceptable. This **resolves** the only open licensing item — the Riley *Aquatic Animal Models*
  pack (itch.io, "free use, no redistribution"). It is **free-use, good-quality, and already
  integrated**, so it is **kept**. (The "no redistribution" clause is a known, accepted caveat for
  a personal freeware repo; if the repo is ever made strictly redistributable, swap per §5.)
- **Everything else was already clean** — terrain PBR is ambientCG **CC0**, nature/ship kits are
  Kenney **CC0**, music is original, voices are family/own TTS, book art is project IP.
- **No higher-quality replacement was importable this session.** The egress policy **403-blocks
  every free-asset host**; only `github.com` is reachable, and every *complete, higher-fidelity*
  marine pack found there (ir-engine's perfectly-matched `assets/ocean/`, X3Native, NikLever) is
  **Git-LFS-hosted — and the LFS object host is also 403.** Repos with real committed GLBs hold only
  one-off models, not a coherent reef set. Swapping the working animated pack for mismatched
  one-offs would *lower* quality and risk breaking the swim/idle animation lookup in `main.gd`, so
  the existing pack stands. See §3.
- **Net:** the queue's actual driver (the licensing flag) is **closed**. A genuine *quality upgrade*
  of the 3D packs is gated on network access (§4) — the only network-free path to new marine assets
  is going procedural (§4, Option C).

---

## 2. Full per-group audit

| Group | Files | Source (verified) | License | Verdict |
|---|---|---|---|---|
| `assets/terrain/*.jpg` (Ground054, Rock061, Planks023B, up_* set) | PBR col/nrm/rgh | ambientCG | **CC0** | ✅ keep |
| `assets/terrain/*.png` (caustics, leaf, polyp, scales, star_detail, flower, beachball) | small textures | procedural / project-baked | original | ✅ keep |
| `assets/nature/*.glb` | trees, rocks, flowers, bushes, mushrooms | Kenney Nature Kit | **CC0** | ✅ keep |
| `assets/ship/*.glb` (ship-ghost, ship-wreck, chest, barrel, cliff rocks) | set pieces | Kenney Pirate Kit | **CC0** | ✅ keep |
| `assets/mg/*.png` | 2D minigame sprites (flowers, ornaments, snowman, etc.) | Kenney Foliage + project-drawn | **CC0 / original** | ✅ keep |
| `assets/aquatic/*.glb` | 16 fauna + corals/seaweed/shells/rocks | **Riley *Aquatic Animal Models*, itch.io** | **"free use, no redistribution"** | ✅ keep (free-use; OK for freeware — see §1) |
| `assets/characters/roshan.*`, `lamb.*`, sprites | hero + lamb | book illustration (project IP) | project-owned | ✅ keep (heart of the game) |
| `assets/characters/friends/*.png`, `assets/book/**` | character & scene art | book illustrations (project IP) | project-owned | ✅ keep |
| `assets/audio/music/*.ogg` | 11 loops | synthesized for project | original | ✅ keep |
| `assets/audio/voices/*.ogg` | Roshan + friends + daddy | family recordings + Piper neural TTS | own / permissive | ✅ keep* |
| `assets/audio/{chime,buzz,fart,buy}.ogg` | SFX | synthesized for project | original | ✅ keep |
| `assets/audio/voice_yay.mp3`, `chuck*.ogg` | "Yay!" / dog bark | Pixabay (floraphonic / DRAGON-STUDIO) | Pixabay Content License | ✅ keep |

\* `assets/audio/voices/VOICE_MANIFEST.md` invites CC0 drop-in replacements; the current clips
are already own/TTS so they are not a *licensing* problem, only an optional quality upgrade.

**Net:** the only mandatory replacement is the aquatic pack (the exact item the
`REEF_FLORA.md` ledger already flagged as "pending download unblock").

### Files to replace (`assets/aquatic/`)
Fauna (16): `Octopus Crab Lobster Penguin Shark Hammerhead Whale Turtle StingRay Dolphin Squid
ClownFish Dory Carp Tuna Eel`
Flora/dressing: `Coral Coral1..Coral6 SeaWeed SeaWeed1 SeaWeed2 FanShell SmallFanShell
SpiralShell SandDollar Rock Rock1..Rock11`

These names are loaded by string in `scripts/main.gd` (`_aq()` / `_place_aq()` at lines
~1016–1123). **Replacements must keep the same filenames** (or remap those arrays) so scenes
keep working with no code change.

---

## 3. Network blocker (why the download half is not done)

The proxy README (`/root/.ccr/README.md`) is explicit: *"Do not retry or route around \[a policy
denial] — report the blocked host."* Every free-asset host returns a gateway **403 / connect-
rejected**. Authoritative sweep on 2026-06-25:

| Reachable (HTTP 2xx/3xx) | Blocked (403 / connect-rejected) |
|---|---|
| github.com, raw.githubusercontent.com, codeload.github.com, api.github.com, media.githubusercontent.com | ambientcg.com, kenney.nl, pixabay.com, cdn.pixabay.com, polyhaven.com, dl.polyhaven.org, poly.pizza, api.poly.pizza, opengameart.org, freesound.org, sketchfab.com, archive.org, web.archive.org, upload.wikimedia.org, commons.wikimedia.org, huggingface.co, itch.io, rkuhlf-assets.itch.io, **github-cloud.githubusercontent.com (Git-LFS objects)** |

Consequence: I can only download asset files **committed directly (non-LFS) into a public
GitHub repo under a clear free license.** That rules out the canonical CC0 marine sources.

### Search log (GitHub-only hunt for a clean CC0 marine pack)
- `KhronosGroup/glTF-Sample-Assets` — only `BarramundiFish` (CC0), `Duck`, `Fox`. One fish ≠ a
  16-species reef; swapping the whole pack for one model would degrade the game. Rejected.
- `Quaternius/showcase` (CC0) / `Quaternius/TestGltfAssets` — no marine GLBs (Deer, Slime only).
- `ir-engine/ir-engine-assets-basic` (`assets/ocean/` — perfect species list!) — **Git-LFS
  pointers (132 B)** + repo license `NOASSERTION`. Undownloadable + unclear license. Rejected.
- `1GreenNinja/X3Native` (`assets/rigged_glb/sea_*`) — Git-LFS pointers + `NOASSERTION`. Rejected.
- `ToxSam/open-source-3D-assets` — a *catalog* whose entries link to poly.pizza/Sketchfab
  (blocked). Rejected.
- Code-search hits for `Shark.glb`/`Hammerhead.glb` in random game repos — no clear license
  (likely asset-flips); using them would swap one licensing problem for another. Rejected.

I deliberately did **not** download anything dubiously-licensed to "finish" the task — that
would defeat the entire purpose (a clean repo).

---

## 4. What's needed to finish (unblock options)

**Option A — open the allow-list (preferred, lets us use the exact ledger sources).**
Add these hosts to the session's egress policy, then re-run the manifest in §5:
```
poly.pizza  api.poly.pizza          (Quaternius CC0 marine models — direct GLB)
ambientcg.com  acg-download.struffel.net   (already-used CC0 PBR vendor, for parity)
kenney.nl                            (CC0 kits already used elsewhere)
cdn.pixabay.com  pixabay.com  freesound.org   (CC0 audio, if voices get upgraded)
github-cloud.githubusercontent.com   (so Git-LFS-hosted CC0 packs become fetchable)
```

**Option B — drop the files in directly.** Hand me a CC0 marine pack (zip or a GitHub repo with
real committed GLBs) and I'll rename to the filenames in §2 and wire it in — no code change.

**Option C — go procedural.** The reef already has hand-built procedural coral/anemone/urchin/
seagrass meshes (see `REEF_FLORA.md`). I can extend those to cover the fauna silhouettes and
delete the aquatic pack entirely — 100% original, zero third-party license. Larger code effort;
say the word and I'll scope it.

---

## 5. Ready-to-run replacement manifest (Quaternius CC0, via poly.pizza)

The moment `poly.pizza` (or an equivalent CC0 host) is reachable, each game model maps to a
free CC0 equivalent below. Filenames stay identical so `scripts/main.gd` is untouched.

| Game file | CC0 replacement (Quaternius "Animated Animals"/"Ultimate Fish") | Notes |
|---|---|---|
| Shark.glb / Hammerhead.glb | Shark / Hammerhead Shark | rigged swim anim |
| Whale.glb | Whale | |
| Dolphin.glb | Dolphin | |
| Turtle.glb | Sea Turtle | |
| StingRay.glb | Manta Ray | |
| Octopus.glb / Squid.glb | Octopus / Squid | |
| Crab.glb / Lobster.glb | Crab / Lobster | |
| Penguin.glb / Seal.glb | Penguin / Seal | |
| ClownFish/Dory/Carp/Tuna/Eel.glb | Clownfish / Blue Tang / generic Fish (×3 tints) | |
| Coral.glb, Coral1..6 | Quaternius "Ultimate Nature" coral set | |
| SeaWeed*, FanShell, SpiralShell, SandDollar | seaweed + shell props | |
| Rock..Rock11 | Kenney/Quaternius CC0 rock set (already CC0 in repo nature kit) | can source locally |

All Quaternius assets are **CC0-1.0** (no attribution required) and license-compatible with this
non-commercial project. The ledger (`REEF_FLORA.md`, `ASSET_LICENSES.md`) must be updated to cite
them once imported.
