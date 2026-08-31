# Chapter 2 cake visual progression

Status: implemented runtime candidate; owner/device/child acceptance remains open.

The party cake is one persistent physical prop. Each contributing game adds an
irreversible, visible change to that same prop. The final candied-strawberry
cake is the endpoint, not the artwork shown at the beginning of Chef or Candy
Maker.

## Causal stage model

| Saved cake mask | Career result | Persistent visual | Explicit absence |
|---:|---|---|---|
| `0x00` | Farmer delivery only | Five fresh Sky Lagoon strawberries remain visible as five individual ingredients; no cake exists. | No bowl, tier, frosting, candy, or candle. |
| `0x01` | Chef — Mix | Six separate red/orange/yellow/green/blue/violet batter ribbons sit in the shell bowl. | No baked tier. |
| `0x03` | Chef — Stir | The same six colors form one smooth rainbow spiral in the same bowl. | No baked tier. |
| `0x07` | Chef — Bake | Six separate baked sponge rounds rest on three two-round trays; their diameters increase strictly red < orange < yellow < green < blue < violet. | No stack or frosting. |
| `0x0F` | Chef — Stack | The same six bare rounds form one centered red-to-violet stack. | No frosting or fruit. |
| `0x1F` | Chef — Frost | The stacked cake gains shell crest, cream swags, pearls, medallions, and finished frosting. | No strawberries or candle. |
| `0x3F` | Candy Maker — Glaze | The frosted cake remains unchanged; exactly five glossy candied strawberries wait on a separate tray. | No strawberry is mounted yet. |
| `0x7F` | Candy Maker — Place | The grand cake gains exactly those five strawberries, one on each upper tier and none on the violet base. | No extra fruit and no candle is baked into the cake texture. |

Candy Maker's Coat and Sort phases intentionally do not mutate the cake. Their
widgets visibly transform the Farmer ingredients while the persisted cake stays
at `0x1F`. Glaze earns `0x3F`; Place earns `0x7F`.

The completed `0x1F` Chef result and `0x7F` Candy Maker result are committed
before the career closes, then remain on screen for a 2.2-second result hold.
This hold shows the persistent story prop, not merely the minigame's
pre-completion widget.

## Detective and party handoff

Detective comes after all cake work. Completing the Library search adds the
existing unlit rainbow candle as a separate `ChapterTwoRainbowCandle2D` sibling
layer on the completed cake. It does not change the cake mask or cake bitmap.

At the party, Astronaut Roshan's parked rocket changes only the candle from the
unlit asset to the large rainbow-flame asset. When the Ember King takes the
candle for his own birthday party, the sibling candle layer disappears and the
`0x7F` cake remains unchanged.

## Runtime authority

- `chapter2_strawberry_mask` owns the five Farmer ingredients.
- `chapter2_cake_piece_mask` owns the seven ordered cake states above.
- `ChapterTwoGiantCake2D` maps the masks to stage artwork in the Chef room,
  Candy Maker room, and Main Hall party table.
- `ChapterTwoRainbowCandle2D` owns discovery, ignition, and removal independently.
- Later mask bits are invalid without their complete prefix; load healing prunes
  impossible visual jumps.

Every generated stage is a separate, non-destructive runtime derivative. The
earlier ten-strawberry cake remains preserved as a superseded test model; the
active endpoint is the five-strawberry derivative. Candle assets and protected
project art are unchanged.
