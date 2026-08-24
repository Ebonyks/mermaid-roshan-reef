# Intro nonvoice sound palette

This is a deterministic source-palette proposal for the 42.125 s intro video.
It is intentionally separate from the existing review mix, renderer, final OGG,
and MP4. The supplied source MP4 was inspected read-only at representative
frames; no source audio was copied into these masters.

## Scope and guardrails

- All files in `authored/` are original procedural, nonvoice source masters.
- `author_sound_palette.py` derives each random texture from a SHA-256 label,
  so rerunning it produces byte-stable WAVs.
- Masters are 48,000 Hz, stereo, signed 16-bit PCM, with a bounded peak below
  -1.7 dBFS. They are scene layers, not a finished loudness-normalized mix.
- No family dialogue is synthesized. Cabin dialogue remains an owner-recording
  dependency and must be mixed around the room tone.
- No runtime game SFX or ambience assets are reused or copied. The approved
  `assets/audio/music/home.ogg` remains the only musical-bed candidate; it is
  not embedded in this palette.
- A read-only spectral check of that bed found its strongest low/mid energy
  around D3/F-sharp3 (approximately 145/183 Hz). Reveal anchors use D4/A3 and
  the bridge arrival uses F-sharp3, with gentle filtering and no copied sample;
  this keeps the new layers musically consonant without claiming a final key.
- The masters use soft envelopes and low transient density for a 3–4-year-old
  listener on a phone. There are no UI clicks, alarms, combat hits, or literal
  text-dependent cues.

## Timeline mapping

| Picture time | Visual beat | Palette layer and treatment |
|---|---|---|
| 0.00–2.00 | Plane cruising in open sky | Loop `flight_exterior_loop.wav`; low, slowly spooling engine harmonic plus filtered air. Start below the music bed. |
| 2.00–4.50 | Cabin conversation | Loop `cabin_room_loop.wav`; warm aircraft/interior resonance with restrained air noise. Duck under owner dialogue when available. |
| 4.50 | Island reveal | One `reveal_island.wav`; continuous airy swell, rising partials, and sparse shimmer grains. It is a reveal accent, not a pitched chime. |
| 4.50–7.50 | Plane approaches the island and castle | `flight_exterior_loop.wav`, crossfaded under the reveal and home motif. |
| 7.50 | Castle reveal | One `reveal_castle.wav`; longer, lower wonder swell suited to the large castle/water view. |
| 7.50–12.50 | Castle, forest, lakeside, playground | Loop `forest_lakeside_loop.wav`; broad water/leaf texture with sparse soft droplets. |
| 12.50–14.00 | Parked playground plane before the otter | Keep forest layer; optionally bring in the flight loop at very low level as a toy-plane continuity cue. |
| 14.00–23.00 | Otter arrives and plays around the plane | Loop `otter_plane_action_loop.wav`; rounded glissandi, soft low-mid contacts, and airy motion. It is playful movement support, not a bounce SFX. |
| 23.04–28.00 | Cut back to cabin and conversation | Crossfade to `cabin_room_loop.wav`; preserve dialogue space. |
| 28.04–36.08 | Family, otter, and plane outside | Layer `reunion_walk_loop.wav` with low `flight_exterior_loop.wav`; keep forest texture available at a reduced bed level. |
| 36.08–42.13 | Family walks hand-in-hand toward bridge/castle | Loop or tail `bridge_water_arrival_loop.wav`; water flow, irregular wood resonance, and a sustained arrival bed. Do not use a one-shot chime. |

## Authored masters

| File | Duration | Semantic category |
|---|---:|---|
| `flight_exterior_loop.wav` | 8.000 s | gentle aircraft/air movement |
| `cabin_room_loop.wav` | 6.000 s | warm interior room tone |
| `reveal_island.wav` | 2.200 s | magical island reveal |
| `reveal_castle.wav` | 2.600 s | magical castle reveal |
| `forest_lakeside_loop.wav` | 8.000 s | forest, water, and lakeside bed |
| `otter_plane_action_loop.wav` | 9.000 s | playful otter/plane movement |
| `reunion_walk_loop.wav` | 7.000 s | gentle exterior reunion/walk |
| `bridge_water_arrival_loop.wav` | 6.000 s | bridge wood and water arrival |

The generator is the provenance source for all eight files. Do not hand-edit,
normalize, or replace a master without rerunning the hash/measurement checks;
any downstream mix should perform its own short crossfades and phone-level
loudness pass.
