# Pearl Opera rival artwork provenance

Date: 2026-07-29

## Authoritative identity reference

`authoritative_boxer_imp_reference.png` is an untouched repository copy of
the owner-supplied `Generated image 8 (1).png`. It is the identity source for
the Pearl Opera competition imp:

- purple humanoid face and body;
- large amber eyes;
- short muzzle/nose and friendly fanged smile;
- two curled, striped purple horns;
- pointed side ears and small purple hair tuft;
- curled tail, childlike proportions, and purple/coral boots.

It supersedes the unrelated cream heart-mask concept cards and the generic
bean-shaped 3D dungeon imp for 2D career-rival identity.

## Match-ready boxer

`opera_rival_boxer_match_master.png` is the accepted identity-preserving edit
of the authoritative reference. The edit kept the face, horns, ears, body,
tail, and boots; replaced the focus mitt with a second boxing glove; removed
the chest target and pearl belt; and used a plain teal waistband. It contains
exactly two coral gloves. It contains no shell, pearl, ocean badge, medallion,
crest, logo, jewelry, or target motif.

`prepare_boxer_match_asset.py` converts only the green presentation field to
alpha and aspect-fits the result into the non-destructive 1024×1024 runtime
asset at `assets/opera/rivals/opera_rival_boxer_match.png`.

## Eleven-costume sheet

`opera_rival_costume_sheet_master.png` is one art-budget-conscious generated
sheet derived from the same authoritative identity. Its fixed row-major cells
are:

1. pastry chef;
2. detective;
3. ballerina;
4. candy maker;
5. doctor;
6. farmer;
7. magician;
8. painter;
9. astronaut engineer;
10. racecar driver; and
11. pop star.

The twelfth cell is intentionally empty. Every character uses profession
clothing and a simple job tool. The generation explicitly prohibited shells,
pearls, scallop shapes, ocean emblems, marine badges, targets, medallions,
crests, logos, jewelry, boxing gloves, shields, and weapons.

`tools/prepare_opera_2d_worlds.py` deterministically slices the sheet, removes
only its neutral checker presentation field, and emits 512×512 transparent
runtime actors at `assets/opera/worlds/actors/rival_<career>.png`. The boxer
slot is not sourced from the sheet; it receives the dedicated two-glove
match asset above.

## Rejected iterations

The `rejected/` directory preserves failed generated versions for provenance
only. They are not loaded by Godot. Recorded failures include:

- changed face/identity;
- shell-like badges and pearl ornament;
- incorrect imp anatomy; and
- boxer equipment that was not two proper gloves.

No protected project original was changed or recompressed.
