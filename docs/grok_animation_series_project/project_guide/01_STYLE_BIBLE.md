# Series style bible

## Authority hierarchy

Style is not inferred from a single character cutout. Use this order:

1. Owner-approved base video and selected frames — motion cadence, finished rendering, facial acting, camera behavior and lighting.
2. Accepted adjacent series footage — local sequence continuity.
3. This written style bible — vocabulary and guardrails.
4. Canonical character cutouts — identity and authored colors, not necessarily full scene rendering.
5. Location/environment masters — geography, palette families and object placement.

Character identity and location geography remain authoritative in their own domains even when the base video renders them differently.

## Existing written style notes

The target is a polished **1990s Japanese shōjo magical-girl television-animation language**, interpreted through Mermaid Roshan's existing designs. It should evoke the era's romantic cel craft and emotionally clear staging without copying a particular franchise's characters, costumes, symbols or exact shots.

- Finished 2D painted-cel appearance, not a digital illustration sliding through space.
- Graceful shōjo proportions and facial acting while preserving each canonical character's actual age, face and silhouette.
- Clean navy, violet or warm umber contour lines; avoid uniform hard-black ink.
- Two principal paint values plus a selective third accent/shadow value on characters. Shadows form deliberate graphic shapes rather than soft 3D volume.
- Pearl-white cel glints, tiny star highlights and restrained rim accents only where they support the emotional beat.
- Pastel watercolor/gouache-feeling backgrounds with visible broad paint organization, atmospheric depth and quieter detail behind faces.
- Aqua, lavender, rose and moonlit blue shadow families; warm peach light for affection and safety.
- Graphic water, bubbles, flower-petal shapes, luminous ribbons, prismatic sparkles and soft-focus emotional overlays used sparingly.
- Elegant limited-animation timing: strong key poses, readable holds, blinks, hair/tail settling, mouth shapes and one or two meaningful gestures. Motion should feel intentionally drawn, not continuously liquid.
- Character acting begins with eyes, brows, head angle and hands; tails, braids, sleeves and ribbons follow as controlled secondary motion.
- Camera language favors composed wides, medium two-shots, profile/reaction cuts, slow pans, gentle pushes and occasional dramatic still tableaux. Avoid constant orbiting or handheld movement.
- Action uses clean anticipation, a decisive silhouette, a short follow-through and a readable end pose. Avoid rubbery morphing and frantic filler motion.
- Child-facing warmth remains essential: danger is theatrical and recoverable; affection, wonder and humor dominate.

## Era-specific visual target

The image should look as though painted cels were photographed over hand-painted backgrounds and then carefully restored: crisp character shapes, slight organic line variation, restrained highlight bloom and soft atmospheric compositing. It must not look like a modern glossy mobile-game splash illustration, a plastic 3D render, a hyper-detailed AI fantasy painting, a webtoon panel, or a vector puppet cartoon.

Do not redesign Mermaid Roshan, Daddy Mermaid, Rumi, Huluu or the Dust Bunnies to resemble pre-existing magical-girl characters. The 1990s shōjo language controls rendering, staging and timing—not identity.

## Base-video extraction set

When the base video is available, create a `STYLE_SET_v01` containing twelve stills and one short clip:

1. clean daylight wide environment;
2. interior wide;
3. medium two-shot;
4. face close-up;
5. rear-view character shot;
6. hand/object interaction;
7. fast movement pose;
8. still emotional hold;
9. magic/effects frame;
10. brightest lighting frame;
11. darkest acceptable lighting frame;
12. final polished hero composition;
13. one 6–15 second clip showing preferred motion cadence and camera restraint.

Name them `STYLE_v01_01_day-wide` through `STYLE_v01_13_motion-clip`. Do not include a visibly failed, off-model or transitional frame merely for variety.

## Style prompt block

```text
STYLE_AUTHORITY: Render as polished 1990s Japanese shōjo magical-girl television animation interpreted through Mermaid Roshan's established private-project art. Match the attached approved base-video frames for line weight, facial rendering, motion cadence, camera restraint and atmosphere. Use photographed-painted-cel clarity, navy/violet organic contours, deliberate two- or three-tone cel shading, pastel watercolor/gouache backgrounds, aqua/lavender/rose shadow families, expressive held key poses and restrained prismatic sparkles. Preserve graceful limited-animation timing with controlled hair, braid, sleeve and tail follow-through. Do not copy character identity, costume, symbols or exact compositions from any outside franchise; canonical Mermaid Roshan references control identity.
```

## Style drift rejection

Reject outputs with photoreal skin, 3D volumetric rendering, plastic CGI highlights, hyper-detailed AI fantasy texture, modern mobile-game splash-art gloss, webtoon/vector treatment, hard uniform black ink, chibi proportion changes, excessive camera motion, continuous liquid morphing, over-animated filler, or effects that obscure acting.
