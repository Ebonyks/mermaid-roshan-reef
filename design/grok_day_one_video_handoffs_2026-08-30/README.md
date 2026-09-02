# Day One Grok video handoffs — 2026-08-30

This directory separates Day One into **14 Grok direction handoffs** containing
**75 individually pasteable shot jobs**. It translates the local production
slate into an operator-facing format without pretending that missing visual
packets or unreviewed generations are complete.

## How to use

1. Start a Grok project and paste `00_SHARED_STYLE_AND_CHARACTER_REFERENCE.txt`.
2. Open exactly one `D1-Cxx_*.txt` file and paste its `VIDEO SETUP BLOCK`.
3. Upload only the references named for the current shot. Use two to four
   approved images; do not upload a storyboard or gameplay capture as visual
   generation authority.
4. Paste one `SHOT COPY BLOCK` as one image-to-video job. Never ask one Grok
   generation to make multiple shots.
5. Review and accept that shot's complete end frame before starting a
   continuity-dependent next shot. Assemble accepted clips with straight cuts.
6. Treat Grok motion as editorial reference until every changed delivery frame
   independently passes the project's full-frame cinematic audit.

## Files

| ID | Video handoff | Shots |
|---|---|---:|
| D1-C00 | `D1-C00_OPENING_FLIGHT.txt` | 6 |
| D1-C01 | `D1-C01_LAGOON_LANDING_AND_CASTLE_APPROACH.txt` | 4 |
| D1-C02 | `D1-C02_FIRST_DIRTY_CASTLE_DISCOVERY.txt` | 4 |
| D1-C03 | `D1-C03_BATHROOM_DIRTY_ENTRY.txt` | 4 |
| D1-C04 | `D1-C04_BATHROOM_RESTORED.txt` | 4 |
| D1-C05 | `D1-C05_POOL_DIRTY_DISCOVERY.txt` | 6 |
| D1-C06 | `D1-C06_POOL_DUAL_PURIFICATION_RUMI_HUG.txt` | 9 |
| D1-C07 | `D1-C07_STUFFIE_DIRTY_DISCOVERY.txt` | 6 |
| D1-C08 | `D1-C08_STUFFIE_RESTORATION.txt` | 7 |
| D1-C09 | `D1-C09_ART_ROOM_DIRTY_DISCOVERY.txt` | 5 |
| D1-C10 | `D1-C10_ART_ROOM_RESTORED.txt` | 5 |
| D1-C11 | `D1-C11_GRAND_PUFF_REVEAL.txt` | 4 |
| D1-C12 | `D1-C12_RESTORED_CASTLE_FINALE.txt` | 6 |
| D1-C13 | `D1-C13_GRAND_PUFF_FRIENDSHIP_COMPLETION.txt` | 5 |

The source slate remains
`design/day_one_cinematic_slate_2026-08-30.json`. Each handoff repeats its
relevant identity and topology locks so it remains understandable when copied
out of the repository.

## Readiness claims

- `ARCHIVE_COMPLETE`: **false**. Several films still need approved perspective
  boards, exact first frames, provenance, and immutable remote reference links.
- `GENERATION_READY`: **false**. These are separated direction blocks; a shot
  becomes ready only after its named two-to-four-image packet passes the V2
  handoff validator.
- `DELIVERY_ACCEPTED`: **false; 0/14 movies**. Grok clips are not accepted
  delivery frames.
