# Expandable cast registry

Each character owns a folder under `characters/`. Status meanings:

- `APPROVED`: may be used as character authority.
- `APPROVED_PRIVATE_CANON`: fully authoritative for this private family animation project.
- `CONCEPT`: may be tested but cannot silently define canon.
- `REFERENCE_PENDING`: name and registry slot exist; appearance must not be invented.

## Mermaid Roshan — APPROVED

- Role: young mermaid protagonist.
- Authorities: `characters/roshan/ROSHAN_FRONT_IDENTITY.png`, `ROSHAN_REAR_POSE_SHEET.png`.
- Locks: child age; exact face, hair, tiara, clothing and palette; mer-tail anatomy; rear sheet represents one character in multiple cells.
- Needed expansion: approved full turnaround, expression sheet and scale chart derived from the canonical identity.

## Daddy Mermaid — APPROVED

- Role: Roshan's safe adult guide and father.
- Authority: `characters/daddy_mermaid/DADDY_FRONT_IDENTITY.png`.
- Locks: crown, glasses, long brown/green hair, pointed ears, ornate navy coat with gold trim, shell clasps, teal cape, full rainbow scaled tail and multicolor fins.
- Behavior: patient, demonstrative, waits for Roshan's choice, leads without abandoning her.
- Needed expansion: approved rear view, three-quarter views, handhold sheet and expression sheet.

## Princess Huluu — APPROVED

- Role: recurring princess and friend.
- Authority: `characters/huluu/HULUU_CANONICAL.png`.
- Locks: blonde high ponytail with rainbow-toned highlights, blue eyes, pale headset/helmet collar, layered coral-pink bodice and fin-like shoulder details, long coral/peach/pink mer-tail with gold/pearl accents. Preserve her authored proportions and distinctive silhouette.
- Behavior notes from existing story: organized, proactive, princessly, eager to help; can be gently comic when rules and lists meet playful situations.
- Needed expansion: turnaround, expression sheet and simplified motion reference that remain source-faithful.

## Baby Eagle — APPROVED_PRIVATE_CANON

- Role: young plush-like rainbow eagle friend rescued in the Day One Stuffie Room.
- Primary identity: `characters/baby_eagle/BABY_EAGLE_STANDING_IDENTITY.png`.
- Pinned-state authority: `characters/baby_eagle/BABY_EAGLE_PINNED_STATE.png`.
- Locks: turquoise/mint scalloped feathers, yellow face patches, pink crest and wings, black wing tips, large blue eyes, pale pink/black beak, silver-glitter feet and complete body.
- Wrong-reference restriction: never use `assets/book/baby_eagle.png`; its backpack-packing action and lower-body crop are explicitly rejected for animation.
- Motion vocabulary: gentle standing idle, sad low wing-spread pose, worried blink, broad safe double-wing flap and feather settle.
- Safety: sad or inconvenienced is allowed; injury, terror and aggressive attack acting are not.

## Playroom Dust Bunny — APPROVED

- Role: small playful Stuffie Room troublemaker, distinct from the Boss Dust Bunny.
- Identity authority: `characters/playroom_dust_bunny/PLAYROOM_DUST_BUNNY_HOP_IDENTITY.png`.
- Motion authorities: `MOTION_LIGHT_SWING.png`, `MOTION_BOUNDER.png` and `MOTION_TWIRLER.png` in the same folder.
- Locks: small rounded lavender curl-cloud body, two long spiral ears, pearl joints/paws, glossy plum eyes, coral blush and tiny delighted mouth.
- Motion vocabulary: small wing bounce, upside-down light swing, basket spring, floor bound, sideways twirl and harmless wind tumble.
- Safety: mischievous fluff, never a realistic rodent, attacker or injured target. Wing gusts move the intact bunny safely out of frame; no death, impact or explosion.

## Boss Dust Bunny — APPROVED

- Role: playful, non-frightening boss creature.
- Identity authority: `characters/boss_dust_bunny/BOSS_DUST_BUNNY_IDENTITY.png`.
- Motion authorities: five atlases in the same folder.
- Locks: wide three-tier smoky grey/lavender storm-cloud body, deep-plum lower values, enormous spiral ears, pearl joints/paws, natural curl crest, lavender four-point forehead sparkle, large glossy plum eyes, coral blush and compact grin with exactly two small pearl teeth.
- Emotional range: smug, laughing, comically angry, startled and harmlessly defeated—never cruel, injured or terrifying.
- Existing motion vocabulary: squash/lift/peak/land jump; vulnerable laugh; harmless flinch; comic angry crouch; inward implosion to three or four wisps.

## Rainbow Dust Bunny — CONCEPT

- Role: expandable friendly/magical Dust Bunny variant.
- Authority: `characters/rainbow_dust_bunny/RAINBOW_DUST_BUNNY_CONCEPT.png`.
- Locks: compact curl-ear Dust Bunny silhouette, symmetrical spiral ears, two pearl paws, large glossy eyes, tiny cat-like mouth, coral cheeks and one small prismatic forehead sparkle. Color is a soft curl-to-curl pastel rainbow, not hard flag stripes.
- Restriction: concept status until turnaround, expressions and motion tests receive human approval.

## Rumi — APPROVED_PRIVATE_CANON

- Local working name/codename: Violet Tide. Use the series name **Rumi** in scripts and prompts.
- Role seed from the existing local design record: confident, reassuring, playful older-sister/family-friend energy. The owner-supplied sample establishes a warm, trusted bond with Roshan.
- Primary identity authority: `characters/rumi/RUMI_FULL_BODY_IDENTITY.png`.
- Motion authority: `characters/rumi/RUMI_EIGHT_POSE_ATLAS.png`; use the runtime atlas only for inspection or implementation, not as a higher-detail identity reference.
- Relationship authority: `characters/rumi/RUMI_AND_ROSHAN_RELATIONSHIP_SAMPLE.png`. Use this for relative scale, affection and interaction only; preserve each character's own identity card for face, costume and anatomy.
- Locks: young-adult mermaid; large sculptural violet-purple braided high ponytail; pointed ears; strong brows and almond eyes; star-shell earrings; lavender/navy cropped sea-jacket with gold trim, shell/coral/wave motifs and pearly high-neck shell top; turquoise/deep-aqua tail transitioning through lavender to a broad coral-pink split fin; exactly two arms, two hands and one continuous mer-tail.
- Motion vocabulary: gentle hover, friendly wave, broad slow swim with braid/sleeves lagging behind the body.
- Scope: approved canon for this private family animation project. Preserve `SOURCE_PROVENANCE.md` with the character folder so the local source history is not lost.

## Ember King — APPROVED_PRIVATE_CANON identity / REVIEW motion V2

- Role: child-appropriate antagonist and father of the Ember Prince. His simple
  motive is exclusive: he is fascinated by Roshan's fancy birthday candle and
  travels to take it.
- Identity authority: `characters/ember_king/EMBER_KING_IDENTITY.png`.
- Motion authority: `EMBER_KING_MOTION_AUTHORITY.png`; concrete atlas,
  individual frames, review loops and SpriteFrames are in the same folder.
- Locks: lighter stocky-athletic red/coral turtle-dragon body; cream muzzle and
  belly; asymmetrical black emo fringe; obsidian horn crown and natural shell;
  charcoal vest/cuffs/chain; huge aubergine split cape; no tie.
- Personality: adult ruler with melodramatic teenage-emo acting—possessive,
  slouched, defensive, easily embarrassed and transparently delighted by the
  candle while pretending to be bored.
- Motion vocabulary: sparse slouched idle, sixteen-frame heavy blundering walk
  with two complete weight transfers and delayed shell/cape follow-through,
  and theatrical harmless cape fan.
- Relative scale: family anchor at 100%; the Prince is exactly 80% of his
  standing height.
- Restriction: the candle is scene-specific and not baked into reusable motion.

## Ember Prince — APPROVED_PRIVATE_CANON identity / REVIEW motion V2

- Role: the King's observant son. He comes because this is a family journey;
  he has no separate candle fascination, secret mission or elemental destiny.
- Identity authority: `characters/ember_prince/EMBER_PRINCE_IDENTITY.png`.
- Motion authority: `EMBER_PRINCE_MOTION_AUTHORITY.png`; concrete atlas,
  individual frames, review loops and SpriteFrames are in the same folder.
- Locks: lanky red/coral turtle-dragon; cream muzzle; short obsidian horns;
  asymmetrical black emo hair; charcoal/aubergine open-back jacket; ember-heart
  clasp; slim trousers/boots; long split coat tails.
- Relative scale: exactly four-fifths (80%) of the Ember King's standing
  height in every shared shot.
- Shell topology: natural shell grows from exposed red back skin; a continuous
  skin halo surrounds it; the jacket center-back panel is absent; no fabric may
  exist beneath, behind, across or over the shell.
- Motion vocabulary: quiet guarded idle, sixteen-frame sleek level walk with
  distinct contact/passing/high-point phases, diagonal Cinderstep and
  restrained staggered lag in hair, coat tails and tail.
- Relationship behavior: in family shots his eyeline tracks the King and other
  people, never the candle; he quietly clears hazards and protects his father's
  dignity without sharing the goal.

## Adding future characters

Never append a loose image to the root Project. Create a named folder, stable character ID, canonical authority, status, immutable traits, allowed variation, relative scale, expression/motion vocabulary and relationship notes. Use the onboarding template.
