# Fashion Designer Roshan

Status: `SUPPORTING_CURRENT` feature brief and playable runtime alpha.
The persistent wardrobe and pre-party dress checkpoint now have code, append-only
save fields and separate clothing derivatives. Five recurring characters have
original, ribbon, party and garden looks; Roshan also earns a garden disguise.
Optional three-beat disguise practice opens from the wardrobe after the Chapter 2
story. Its later narrative mission remains unbound. Runtime artwork, synthesized
voice, target-device performance and child/owner acceptance remain provisional.
The earlier full-figure dress candidate is source review only; runtime keeps the
original character art and adds the separate garment.

Baseline: `96274aab9cebd563b10846a4a48de5d017588563` (`origin/dev` at intake).
[Design impact](audit_impacts/fashion-designer-roshan-20261006.json) ·
[Runtime impact](audit_impacts/fashion-designer-runtime-20261006.json) ·
[Feature card](fashion_designer/FEATURE_CARD_V1.json) ·
[Reuse inventory](fashion_designer/REUSE_INVENTORY_20261006.json).

## Owner direction — 2026-10-06

The owner commissions Fashion Designer Roshan as primarily a cosmetic
customization feature, with minigames that explain dressing and mermaid outfits.
The follow-up defines the lasting consequence:

> This game has persistent effects. You can redress characters that appear throughout the game using this feature, we'll have unlockable outfits throughout the game too. The fashion designer job will be involving dress up games for disguise, happens later in the game

This supersedes the initial working assumption that all clothes would be freely
available. Starter looks remain available; additional outfits can be earned.
The wardrobe and disguise activities share the same persistent clothing system.

The owner then specifies the first story dressing moment:

> Roshan should put on a special dress before the party, so prior to the iko iko ember king scene

Place that dressing beat in Chapter 2 after party preparation and before party
start, hence before the Iko Iko/Ember King scene. Add the clothing beat alongside
the existing eight preparation careers, preserving their order and stable
identities. This planning change allocates no Opera bit for Fashion Designer;
derive its global job registration at the implementation head. The dress remains
an unlocked wardrobe choice afterward. Its
exact design and the dressing area's room are still candidates. The specific
story purpose for a disguise is also unbound: a party dress is not itself a
disguise, and the owner has not commissioned an infiltration or deception plot.

## The child's wish and persistent payoff

“I can choose what Roshan and her friends wear, and they keep wearing it.”
The child chooses a familiar character, taps a pictured outfit, sees it on that
same character immediately, and meets them wearing it elsewhere. Dressing never
changes who a character is, their voice, their relationships, or their abilities.
Roshan remains a mermaid with her recognizable face, rainbow forelock and
iridescent tail, with her approved tiara outside a career costume under the
existing owner direction. Mermaid clothes fit a tail; they never require legs
or shoes, cover required fins, or substitute another character's anatomy.

Changing clothes is satisfying free play. It needs no score, fashion ranking,
timer, purchase, separate confirmation, or minigame completion. Starting looks
are always available. Earned clothes become permanent wardrobe choices. There
is no “wrong” everyday outfit and no unlock is consumed by wearing it.

The later job gives that familiar action a purpose: “Let's dress up so we look
like we belong here.” Its puzzles teach disguise through pictures and visible
results. A chosen disguise survives leave, reload and return until the child
changes it or a clearly scoped story costume overrides its presentation.

## Wardrobe interaction and character scope

Use a picture-first character rail, a large live preview, and a small number of
outfit cards per page. Every required target meets the shared 110-pixel touch
floor. Portraits identify the character; an outfit picture identifies clothes.
Text is supplemental. Show a pictured unlock source on a locked card and speak
its exact hint when tapped. Do not put a greyed-out lock symbol in charge of the
meaning. Keep the current look if locked clothes are touched.

Tap a card to wear it immediately and save the change. Back leaves the wardrobe
without reverting the choice. A large pictured exit restores the exact launching
room; it is navigation, not a second confirmation. A short bounded sparkle and
the character's own appropriate show-off pose acknowledge an intentional change.
Repeated taps on the selected outfit do not award rewards or accumulate effects.

Start the renderer coverage inventory with Roshan, Rumi, Baby Eagle, Daddy
Mermaid and the friendly rainbow dust bunny. These are rollout candidates drawn
from existing recurring characters, not a new cast or an exhaustive approved
clothing roster. Each selectable character needs at least one actual alternate
outfit with coverage for every reachable appearance. Do not present an empty
character wardrobe as delivered customization. Keep future characters and
outfits extensible through stable IDs and explicit compatibility.

Begin with complete outfits. Mix-and-match accessories can expand the system
once their per-character/per-pose anchors are established. Do not recolor skin,
hair or the entire body to simulate a garment, swap another character's portrait
onto Roshan, or cover an already painted garment with an unrelated sticker.
Existing legacy whole-character skins remain readable as legacy save choices;
they do not define the new clothing/identity contract.

## Outfits unlocked throughout the game

Unlock sources can include a chapter reward, an intentionally completed job,
a discovery, or a gift from an existing friend. The specific outfit and source
are candidate content until bound to an approved event and matching artwork.
Award a new outfit once, show the familiar character trying it on, and record
ownership immediately. Let the child keep their current outfit if they prefer;
an unlock never silently replaces a saved clothing choice.

Reuse existing earned milestones when introducing the wardrobe to an older
save. Backfill only the named outfits whose precise prerequisites are already
true. Do not infer a win from an old generic progress counter, reset existing
stars, shift Opera bits, or grant every outfit to every legacy save.
Unlocks do not require the later disguise job to have been reached. That job can
teach the system and award additional disguise pieces without monopolizing it.

## Confirmed story introduction — the special party dress

By dressing herself, Roshan gets ready for her birthday, and her special dress
becomes a lasting part of the wardrobe. This beat belongs before the party
starts, not as a costume change after the Ember King's entrance.

Use the existing ready-party boundary as the first integration candidate:
`ChapterTwoDirector.party_is_ready()` becomes true after the eight required
contributions, while `party_started` is still false. Offer the dressing beat
before `start_main_hall_party()` commits party start. The child taps the pictured
dress to put it on; a short show-off pose leads back to the ready party.
Proposed exact cue `fashion_party_dress`: “Let's get dressed for our party!
Tap your special dress!” The moving pointer targets the actual dress.

Equip and persist `roshan_party_dress_v1`, record its permanent unlock and the
additive `chapter2_party_dress_done` milestone, then continue to the existing
party/Iko Iko/Ember sequence. Save the result immediately; a timer, preview,
pointer or opening the wardrobe cannot mark the dressing beat done. Keep the
chosen dress visible through live party appearances and return to normal
wardrobe access afterward; do not silently take it away.

Older saves already beyond party start keep their current chapter progress.
Backfill access to the dress without replaying the party or inventing an outfit
choice the child never made. A pre-party older save sees the dressing beat.
The new clothing milestone stays outside `chapter2_party_piece_mask`, the
eight-entry job phase array and the existing career/star namespace. The exact
wardrobe entrance and garment pixels still need production binding.

### Party dress review candidate

The [standing dress candidate](../assets_src/fashion_designer/party_dress_v1/roshan_party_dress_candidate.png)
fits the existing Ballerina coral petal-gown design to Roshan's base standing
pose. The [source manifest](../assets_src/fashion_designer/party_dress_v1/provenance.json)
records unchanged input hashes, the exact prompt and native output. The candidate
is kept outside runtime under a `.gdignore`; no game appearance uses it.

The overall hair, mermaid silhouette and violet-blue tail remain recognizable.
The generator redraws the face and turns the tiara's jewel into a heart shape,
so exact identity and tiara correction remain necessary before acceptance.
This is one standing concept, not a complete outfit atlas. Owner garment review,
all required poses/anchors, runtime-sized exports and live wardrobe integration
remain pending. No protected original or runtime image was changed.

## Disguise activities — candidate activity sequence

These three activities use the same equipment and save service as ordinary
dressing. Each has a different decision and a truthful visible payoff. Examples
are local play situations, not approved story events or new chapter canon.

| Activity | Child action | Visible result and purpose | Exact proposed objective / cue |
|---|---|---|---|
| Dress for the part | Inspect a pictured role, then tap the outfit that fits it; select from a small set of clearly different silhouettes | The real character wears the selected clothes and can try the pictured role; a tiny enacted example explains the choice | `fashion_role_pick`: “Tap the clothes that match the picture!” A moving pointer visits the role picture, then the candidate clothes. |
| Blend into the setting | Compare the character with a pictured environment; choose a fitting costume and try it in that same setting | The character appears among the matching forms while their identity stays recognizable to the child; no disappearance trick or arbitrary color-only quiz | `fashion_blend_pick`: “Let's blend in! Tap a disguise for this place!” A pointer connects the pictured setting to the clothes. |
| Finish the disguise | Look at a dressed character and a pictured complete example; tap the missing compatible piece, with optional generous drag-and-snap | The missing clothing piece visibly fits that character; the child uses the completed disguise for the small local pretend-play payoff | `fashion_finish_piece`: “Something is missing! Tap the piece to finish our disguise!” A pointer marks the actual missing slot and its matching piece. |

The role and setting use more than hue: silhouette, motif and context keep the
choice accessible without color discrimination or reading. More than one outfit
may be correct if it has the required traits. Do not grade the child's taste or
pretend arbitrary stylistic preferences are objective errors.

Wrong choices receive a kind try-on and a short demonstration of why the pictured
disguise is still incomplete. They keep the child in control. Help first points,
then repeats the specific spoken cue, then reduces distractors or shows a ghost
placement. A demonstration never equips, completes, unlocks or pays on its own.
No-input waiting never wins. The final result always needs the child's touch.

Use short separate rounds with natural stopping points. Save a finished piece
or round immediately. Leave, pause and focus loss cancel an unfinished gesture
without erasing finished clothes or rounds. Replaying never duplicates rewards.
Free dressing remains available outside the job.

This cosmetic feature has no fashion contest or imp race in the present brief.
Do not force the competitive Opera finale formula onto free dressing. If an
owner-selected late story route later makes it a competitive career, apply the
actual live extension contract and `DL-INT-14` to that scoped activity then.

## Persistent state and appearance ownership

The implementation should use a shared wardrobe satellite receiving `ReefMain`
by reference. Durable state stays on the main state owner and is serialized by
`SaveState`; overlay controls own only temporary presentation. These are planned
new additive keys, not a claim that the runtime already recognizes them:

| Save key | Default | Meaning |
|---|---|---|
| `character_outfits` | `{}` | Stable character ID → chosen complete outfit ID; absence resolves to that character's original outfit |
| `outfits_unlocked` | `{}` | Stable outfit ID → ownership; grants only grow |
| `fashion_disguise_progress` | `{}` | Stable challenge ID → completed rounds/pieces and explicitly chosen current disguise; no transient pointer/timer data |
| `fashion_rewards_claimed` | `{}` | Stable source/reward ID → already granted; makes reward re-entry idempotent |
| `chapter2_party_dress_done` | `false` | Intentional pre-party dress choice; legacy post-party progress remains grandfathered without replay |

Preserve unknown fields and future IDs in the stored data. Validate types and
compatibility before rendering; an unavailable, corrupt or incompatible choice
renders that character's default without erasing the stored choice or unlock.
Reject path-like IDs and arbitrary save-provided asset paths. The trusted outfit
catalog owns asset paths, character compatibility, unlock prerequisite, source,
frame layout and coverage. Unlock flags alone cannot prove that art is ready.

Write through the existing transactional save and backup path when equipping
or granting an outfit, and flush at lifecycle boundaries. Future-schema saves
retain their read-only behavior. A failed write must not claim persistence;
keep the recoverable in-memory choice and follow the existing save-error path.
Never repurpose `skin`, `fairyskin`, `owned`, `companion_colors`, Opera stars or
chapter masks. Migrate legacy aliases deliberately without removing old keys.

Appearance precedence: a scoped story/job presentation costume, then the chosen
everyday outfit, then the character's original appearance. A temporary override
never overwrites the everyday selection and restores it on every exit path.
Outfit choice does not alter hitboxes, touch reach, voice, navigation or rewards.

Every render owner must use this shared resolver: the castle's Roshan actor,
standalone Canvas Roshan loops, minigame character cards, recurring NPCs,
companions, family-play appearances and later chapter actors. Inspect each
consumer; an existing `skin_sprite_path()` call is not proof of full coverage.
The selected look must survive a scene rebuild as well as update the visible
instance when changed. Keep gameplay-appropriate authored motion and contact.

The selected Day One clips are flattened fixed footage. They cannot display
arbitrary runtime outfits. Dynamic dressing inside those clips is an explicit
coverage limitation, not permission to alter owner-selected footage or invent
a cinematic exception. Resolve any desired clip continuity with the owner
before dependent production; implement independent live-game appearances first.

## Existing sources, reusable mechanics and named gaps

The hashed inventory records the inspected Roshan base, directional atlas,
Rumi atlas, Baby Eagle isolate, Detective and Ballerina costume atlases and an
existing Pop Star costume reference. Base-world Roshan
and existing Rumi/Eagle art anchor identity. The Detective sheet supplies a
role/disguise and layout reference; it is not a new base-world outfit already
accepted for wearing everywhere. Existing career outfits include props and
career-specific poses and therefore need per-consumer review before reuse.

Reuse the Storybook UI stage, wardrobe navigation/control suspension, bounded
try-on feedback, and SaveState's transactional lifecycle. Reuse intentional
picture choice and generous piece placement as mechanics, with clothing-specific
targets and results. The proposed Job Platform is not an implemented service.

Named production gaps: compatible alternate clothing/pose coverage for each
enabled character; identity-preserving mermaid costumes; per-pose garment or
accessory anchors; wardrobe thumbnails; approved pictured disguise contexts;
exact spoken objective and locked-source cues; renderer coverage; the later job's
story home and prerequisite. Existing general props or a missing search hit do
not justify speculative mass generation. Generate only bound gaps, preserve
originals, record provenance and licenses, and visually review the full pose set.
New art stays true 2D and within texture/Speedy budgets. No new 3D clothing path.

## Build and verification sequence

1. Bind the first character/outfit family and every live appearance, keeping
   the original identity and the existing save baseline. Implement the shared
   catalog, resolver and append-only save behavior before UI-specific copies.
2. Build the wardrobe's intentional equip/locked/default/exit paths. Verify
   that two recurring characters independently retain their choices across
   two appearances, room rebuild, reload, focus loss and Back. Then expand
   coverage to the rest of the enabled recurring cast.
3. Bind the special dress to the confirmed pre-party moment, then bind other
   outfit rewards to exact approved existing events and test idempotent
   grant, older-save backfill, no passive award, retained unknown IDs and a
   malformed or incompatible selection.
4. Build the three disguise interactions on the same wardrobe model. Keep
   the actual disguise story purpose unbound until selected; the confirmed
   pre-party dress introduction does not invent a disguise plot.
   If that entry uses Opera, re-run the prompt planner at that implementation
   head and derive every bit, clamp, count, route and probe update. No bit is
   reserved or added by this planning change.
5. Extend the existing trusted wardrobe/save and relevant character/activity
   probes. Run the exact engine/full suite, authority/development gates and
   applicable art, audio, typography and 2D checks. Use Mobile captures at
   1280×720 and a wide phone; separately seek device, child and owner evidence.

Must-have behavior checks: different outfits on two characters; same character
in multiple scenes; immediate visible equip; locked tap keeps the current look;
earned unlock kept after interruption; new unlock does not auto-equip; repeat
grant pays once; correct/wrong/passive disguise play; saved partial disguise;
temporary costume restore; pre-party dress before party/Ember launch;
post-party older-save backfill without replay; legacy and future-ID preservation; invalid asset
path rejection; transactional write failure; pause/Back/focus-loss cleanup.

Speedy budget: load only the displayed character and current outfit page;
release unused previews; cache approved frame resources; bound feedback to one
burst and stop preview animation when hidden. Do not scan scenes or create
clothing nodes every frame. Measure residency and touch response in the actual target
build before claiming performance acceptance.

This is new feature planning, not closure of an existing defect. `MA-DOC-006`
is extension-path context; `MA-SAVE-001` concerns a different existing castle
progress defect. Neither finding is closed or rewritten by this brief.
Applicable rules include `DL-AUTH-05`–`07`, `DL-AGE-01`–`07`, `DL-UI-01`–`07`,
`DL-INT-01`/`02`/`04`–`07`/`12`, `DL-MOT-01`/`02`/`04`/`05`,
`DL-MED-01`/`02`/`04`/`05`, `DL-SAVE-01`–`04`, `DL-ASSET-01`–`06`,
`DL-PERF-01`–`04`/`07`, `DL-QA-01`–`07`,
`DL-SND-01`/`05`/`13`, `DL-CODE-01`/`03`/`05`/`08`/`10`, and `DL-PLAN-01`–`06`.
Visual, device, child, owner and runtime evidence remain outstanding.


## Runtime alpha — 2026-10-07

The bedroom wardrobe retains its legacy three skin choices and adds a pictured
clothes button. The clothes page selects Roshan, Rumi, Baby Eagle, Daddy or the
rainbow friend. Each intentional clothing tap applies and writes immediately;
Back and Finish retain it. Unknown future IDs/fields survive normalization and
fall back visually. Starter ribbons are available; Farmer's earned strawberry
milestone unlocks garden looks, and completed party preparation unlocks party
looks. Rewards never automatically equip. Existing post-party saves gain access
without replaying the dressing beat. Full-character legacy skins remain compatible.

The Main Hall party route opens a one-choice dress page before lawn entry.
The director independently rejects ignition before the special dress milestone.
A dress tap records that milestone, saves, and resumes the lawn route. The eight
career bits, mask and ordering are unchanged. The lawn's reach and swim poses
continue to use their original frame regions and contact timing while dressed.

The later practice presents a garden outfit picture, then Rumi wearing the same
garden motif, then a missing bow. Matching intentional choices save each prefix;
wrong or passive input cannot advance. A completed practice grants its persistent
disguise once. This is a forgiving pictured introduction with no score, deadline
or failure state; it does not establish a new disguise plot or global Opera bit.

The renderer uses 55 separately assembled 2D PNG variants for all ten Roshan
source families and five recurring-character source families. Original files are
hashed and remain unchanged. Generated clothing comes from one transparent
cutout; ribbons are project-authored 2D shapes. Small ribbon/party/garden variants
on friends are accessory outfits on their existing clothing. Their source,
placement, hashes and provisional status are in the [garment provenance](../assets_src/fashion_designer/party_garment_v1/provenance.json).
The shared lookup covers the player, independent atlas loops, castle companions,
persistent Rumi, family-play cards, lawn guests/poses, kart, speech portraits,
Opera venue, intro replay pictures and the Conservatory handoff.
Career-specific costumes and flattened owner-selected clips keep their scoped
presentation. No new 3D resource or world logic was introduced.

The 55 gameplay derivatives add 32,737,402 PNG bytes before export compression.
They replace textures on existing character nodes and add no clothing draw layers.
The wardrobe loads only its five character thumbnails, current preview and current
three-card page; its existing 14-element feedback pool is bounded and torn down
on exit. Actual APK growth, texture residency, 30 fps and touch/voice latency still
require the target device. The [short desktop Speedy sample](../assets_src/review/fashion_runtime_20261007/desktop_budget.json)
reports a 21.7 MiB peak texture increase over its game baseline, releases 13.7 MiB
on close and retains 8 MiB with the selected looks. Its whole-viewport maximum
is 105 draw calls. First entry costs 56.7 ms and the dress callback 40.7 ms in
that sample; these are wall-clock operations, not Android touchscreen/FPS
acceptance. The clothes page now shares only the overlay shell, avoiding a
legacy picker build that would immediately be discarded. The unchanged castle
prop frame review was rebound
only after [all 96 frame and occlusion records matched](../assets_src/review/fashion_runtime_20261007/frame_binding_revalidation.json).

Verification is recorded in the runtime impact rather than inferred from this
brief. [Mobile review captures](../assets_src/review/fashion_runtime_20261007/manifest.json)
cover 1280×720 and 1920×900. Desktop Mobile captures do not prove Lenovo/older-phone
performance, human voice grades, child readability or owner art acceptance.

The frozen runtime passed the complete local `scripts/ci.sh` suite on exact
Godot `4.7.2.stable.official.ed1daf0bf`: all 82 trusted probes and static/asset
gates pass. The [machine receipt](../assets_src/review/fashion_runtime_20261007/machine_verification.json)
records all 98 unchanged runtime source hashes and exact log hashes. The exact runtime commit `62389344` is integrated on dev after successful topic, PR and dev Probe Suite runs (37603992197, 37604042115 and 37609978581). This machine pass does not establish the outstanding visual/device/child/owner acceptance.

## Illustrated process review — 2026-10-07

The [step-by-step illustrated walkthrough](../assets_src/review/fashion_walkthrough_20261007/README.md) shows current wardrobe, five-character clothing, unlocks, pre-party dress, three-phase practice and saved replay limits. The existing ten captures are synthetic/model-call visual references; a bounded real-input fresh-profile check reaches the castle introduction only. Natural wardrobe entry, fitting/contact, disguise completion, birthday transition and reload images remain gaps.

The separately marked **PROPOSED / NOT YET PLAYABLE** section records the response to the owner’s quality challenge: friend-focused garment/pattern/accessory choices, a personalised birthday dressing ritual, role acting, gentle camouflage play, fitting a missing piece onto a friend and a shared pretend-show finish. These are design proposals with missing sources/actions, not implemented gameplay or a bound later disguise mission. No 4.6/5 acceptance score is asserted. Scope and evidence are in the [walkthrough impact](audit_impacts/fashion-walkthrough-20261007.json).
