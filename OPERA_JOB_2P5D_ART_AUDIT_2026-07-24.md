# Opera job 2.5D environment art audit

Date: 2026-07-24

Audit ceiling: 4.9/5

Acceptance threshold: 4.5/5

## Outcome

PASS. All 24 delivered images score at least 4.7/5. The set supplies one
continuous-world key and one large-module/background-texture kit for each of
the twelve non-boss jobs.

The pass corrects the earlier spatial disagreement:

- regular jobs are 2.5D side-scrolling story worlds;
- the lobby is the navigation hub;
- small curtain portals frame entry and exit only;
- literal stages are reserved for later boss fights;
- boss-specific art remains deferred.

## Scoring

| Dimension | Weight |
| --- | ---: |
| Style, palette, and group consistency | 25% |
| 2.5D route/background usefulness | 20% |
| Child-readable silhouette and hierarchy | 20% |
| Job/mechanic continuity | 20% |
| Mobile-safe modelability | 10% |
| Completeness and uniqueness | 5% |

Binding count, order, species, state, a nonuniform kit grid, a literal
job-stage composition, or a score below 4.5 caused automatic rejection.

## Accepted results

| Job | Scene | Kit | Continuity result |
| --- | ---: | ---: | --- |
| Pastry Chef | 4.8 | 4.8 | Continuous pastry district and readable process landmarks |
| Detective | 4.8 | 4.8 | Archive route remains distinct from background detail |
| Ballerina | 4.7 | 4.8 | Preserves all four color/icon identities |
| Candy Maker | 4.8 | 4.8 | Large hopper/press/conveyor sequence |
| Doctor | 4.8 | 4.8 | One visible coral five-armed patient; later bays empty |
| Farmer | 4.8 | 4.8 | Nine empty pads, no baked piggies, zero food baskets |
| Boxer | 4.8 | 4.8 | Friendly training district and exactly three practice pads |
| Magician | 4.8 | 4.8 | Three hats and empty runtime reveal destination |
| Painter | 4.9 | 4.8 | Plum/coral/cream order and uniform kit grid |
| Astronaut Engineer | 4.8 | 4.8 | Distinct pipe shapes; no flame or smoke |
| Racecar Driver | 4.8 | 4.8 | Safe brand-free continuous track-city |
| Pop Star | 4.8 | 4.8 | Four mapped arrows; catwalk reads as city route |

Minimum: 4.7

Maximum: 4.9

Mean: 4.80

## Rejected iterations

| Candidate | Score | Automatic rejection |
| --- | ---: | --- |
| Doctor scene v1 | 4.0 | Repeated the single patient |
| Farmer scene v1 | 3.9 | Produced too many piggies/placements |
| Farmer kit v1 | 4.2 | Baked an incorrect food-basket count into scenery |
| Boxer kit v1 | 4.4 | Omitted the three interaction pads |
| Painter kit v1 | 4.4 | Broke the equal-cell 4 x 4 format |

Rejected images remain in generation provenance only and are not in the
repository package.

## Group consistency

- Coral, teal, cream, and plum foundations connect every job.
- Navy-purple separation and aqua/lavender depth remain consistent.
- Shell, pearl, rope, velvet, brass, and coral connect the worlds to the Opera
  without enclosing them in stages.
- Background contrast is lower than the playable routes.
- Landmarks use rounded, modelable forms and broad material regions.
- No accepted environment contains boss content, an audience, text-heavy
  signage, or copied franchise symbols.

## 3D retention risks

- Do not replace the continuous route with a single arena during blockout.
- Do not turn the reference swatches into realistic high-frequency materials.
- Keep parallax cards sparse to protect transparent-overdraw budget.
- Preserve exact runtime counts and orders as separate objects rather than
  baking them into scenic meshes.
- Review every world at the actual Mobile-renderer camera and phone scale.

The authoritative implementation guide is
`CLAUDE_OPERA_JOB_2P5D_CONTINUATION_2026-07-24.md`.
