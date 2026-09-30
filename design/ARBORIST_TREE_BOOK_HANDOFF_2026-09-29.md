# Roshan's Tree Book — revised art and interaction handoff

Status: **REVIEW_CANDIDATE / ART_RECOVERED**. Owner corrections recorded 2026-09-29.
This revision supersedes the conflicting defaults in the [September 30-labelled source handoff](https://github.com/Ebonyks/mermaid-roshan-reef/blob/4febc33b563ab48a9ba0cd9875d51c57364a5fad/design/ARBORIST_TREE_DOCTOR_HANDOFF_2026-09-30.md). Its later filename date does not override the owner's response in this task.

## Owner decisions

- Candy Maker is reserved for a later section of the game. **Do not place it in the Kitchen.** It is excluded from this Tree Book/Day Two handoff; no replacement free-play route is assigned here.
- Every patient has a visibly diseased leaf. The previous fixed Thirsty → Broken branch two-problem event is superseded.
- Three rounds mean three consecutive decisions for one patient: identify tree, identify diseased leaf, choose appropriate medicine.
- The screen has left/right halves. The book occupies the left. Four choices are available per decision. Keep the patient tree visible in the upper-right corner.
- Tree and leaf decisions use four selectable pictures in the book. On the medicine page, the book explains the leaf-to-medicine match pictorially; the four actual medicines are selected on the right.
- After medicine selection, Roshan visibly gives the medicine to the tree. The same tree becomes healthy. A tree sticker is the payoff.
- The lower-level Opera House activity and Sky Lagoon Day Two event remain the proposed two contexts. Opera Hall launch was not separately reaffirmed in the owner's response; retain as a documented routing default, not new acceptance.
- The four cue families below and the one-case preview are agent implementation choices within this direction. Owner did not specify scientific diagnoses or final species.

## Delivered Step 0: accessible art

[Packet entry](../assets_src/handoffs/arborist_tree_book_20260929/README.md) · [recovery manifest](../assets_src/handoffs/arborist_tree_book_20260929/RECOVERY_MANIFEST.json) · [new art provenance](../assets_src/handoffs/arborist_tree_book_20260929/NEW_ART_PROVENANCE.json).

63 historical art/provenance/tool files were copied byte-for-byte from the dirty
Arborist worktree at base ecad384e. The source worktree was not reset, staged,
committed, or modified. The obsolete game prototype, save-mask edits, policy
edits and deleted imports were excluded. Recovered source and old candidate
runtime PNGs are archived under a non-runtime .gdignore directory, with original
paths retained inside recovered/. Historical acceptance assertions remain
historical; publication grants no current runtime or owner acceptance.

Use current dev for implementation. The old background's nominal 2048 master
contains scaled/padded imagery from a 1672×941 native source. It does **not** meet
the current native 2048-per-screen rule. Do not promote it by quoting the
upscaled dimensions. Some recovered atlas figures have visibly clipped hat tops;
the old atlas is a reference candidate, not approved animation delivery.

## Concrete layout (1280×720 reference canvas)

| Area | Tree page | Leaf page | Medicine page |
|---|---|---|---|
| Left half x0–640 | Open book with four tree pictures, 2×2 | Same book with four leaf-condition pictures, 2×2 | Big diseased leaf → correct remedy, matching badge repeated; spoken explanation |
| Right half x640–1280 | Patient in upper-right; specimen cue beside it; Roshan below | Patient in same corner; magnified diseased leaf from that tree | Patient remains upper-right; Roshan beside it; four selectable medicine props in a 2×2 tray below |
| Persistent memory | Current tree cue | Chosen tree sticker | Tree and leaf stickers |
| Response | Correct tree stays in book | Correct condition stays in book | Selected medicine stays visible through local application |

Keep every choice at least 160×160 base pixels; tree/leaf book choices target
200×200. All four options remain available, including training. Difficulty changes
cue contrast and assistance, not choice count. Separate the two columns around
the book spine. No target may overlap another or the patient preview. On narrow
aspect ratios scale the whole reference canvas uniformly; do not squeeze one half.

## Four proposed leaf / medicine pairs

| Leaf picture | Redundant badge and colour | Book explanation | Right-side medicine | Local action |
|---|---|---|---|---|
| Drooping leaf | Blue drop | Drooping leaf → water | Round blue watering can | Pour at roots |
| Orange-spotted leaf | Three orange circles | Orange spots → leaf spray | Orange spray bottle | Spray leaves |
| Nibbled leaf and tiny bug | Green bug | Bug leaf → ladybug helpers | Green helper jar | Tap to release at canopy |
| Pale yellow leaf | Yellow sprout | Pale leaf → plant food | Yellow food pouch | Sprinkle at roots |

These are fictional child-friendly condition names and visual matching pairs,
not botanical treatment guidance. Broken-branch wrapping is outside the current
leaf-based loop. Old wrap/pruner assets remain archived; do not insert them to
fill the four medicine slots. Reuse one badge design for clue, diagnosis card,
book explanation and medicine label. Wrong options must differ in badge shape
and colour. Tree choices must differ in silhouette AND trunk/leaf cue; the current
concept references still need a four-species distinctness pass.

## Art role / gap table

All paths below are relative to assets_src/handoffs/arborist_tree_book_20260929/.

| Role | Actual files | Current use / gap |
|---|---|---|
| Roshan idle/travel/work/cheer and costume | recovered/assets/opera/worlds/actors/animation/roshan_arborist_sheet_a.png; actors/roshan_arborist.png | Recovered reference. Hats clip in some atlas cells; not final movement acceptance. |
| Career crest / portrait | recovered/assets/opera/worlds/ui/crests/opera_crest_arborist.png; recovered/assets/opera/worlds/actors/roshan_arborist.png | Reusable review candidates; identity review pending. |
| Roshan reading book | new_art/book_pose.png | New complete-tail reading pose. Reviewed visually as still art; opening/page-turn motion absent. |
| Book open surface | new_art/book_open.png | New empty illustrated spread; four choices are UI children, not baked into art. Closed/opening/page-turn sequences still missing. |
| Primary sick/healthy patient | new_art/patient_spaced.png | Two separated complete cells: orange-spotted and healthy blossom state; exact same tree. Selected review candidate. patient_pair.png is rejected for touching canopies. |
| Historic six-state tree | recovered/assets/opera/worlds/arborist/tree_needs_care.png, tree_checked.png, tree_pruned.png, tree_watered.png, tree_treated.png, tree_bloom.png | Preserved originals. Prune/wrap sequence belongs to old prototype, not this matching loop. |
| Tree-choice references | references/lagoon_tree_bigleaf_maple.png, lagoon_tree_pacific_dogwood.png, sky_lagoon_tree_sticker_tall_v1.png plus primary patient | Existing repo references. Need coherent isolated cards, exact species leaf samples and matching sick/healthy variants; dark-background concepts not final world sprites. |
| Four diseased leaves / medicine labels | new_art/leaf_medicine.png top row, columns 0–3 | New clear leaf symptoms and badges. Selected review sheet; full-alpha cell boundaries need final extraction review. |
| Four selectable medicines | new_art/leaf_medicine.png bottom row, columns 0–3 | New badge-matched can, spray, helper jar, pouch. Same sheet binds icon identity. |
| Additional three patient cases | No complete case art yet | Need tree states whose actual leaf symptoms match the selected cue; do not attach orange spots to an unrelated diagnosis. |
| Nursery/world/stage | recovered/assets/opera/worlds/backdrops/world_arborist*.png and stage_arborist*.png | Historic archive only: blurred padding and insufficient native coverage. Current Sky Lagoon remains context source; no new background commissioned here. |
| Local medicine use | No complete hand-contact action sequence yet | Book pose cannot substitute for carrying/pouring/spraying. Bind tool to Roshan's hand, then animate actual contact before heal; MA-PLAY-004 remains open. |
| Helper imp | recovered/assets/opera/worlds/arborist/imp_arborist_{ready,catch,water,cheer}.png | Optional archived helper; not required by revised loop. |
| Sticker | Healthy patient cell from new_art/patient_spaced.png | Reuse same tree identity. No separate new character or reward tree. |

## Exact cue script

1. Arrival/book: “Let's check my Tree Book!”
2. Tree decision: “Which tree is this? Find the same tree!”
3. Correct tree: “It's the pearl-heart tree!” (other species lines after species selection).
4. Leaf decision: “What is wrong with this leaf? Find the same picture!”
5. Orange case explanation: “Orange spots need leaf spray. Find the same sticker!”
6. Other explanations: “Droopy leaves need water!” / “Bugs are tickling it. Find the ladybug helpers!” / “Pale leaves need plant food!”
7. Local help: “Spray the leaves!” / “Pour it on the roots!” / “Let the ladybugs out!” / “Sprinkle the plant food!”
8. Wrong tree: “Look at the tree's shape and heart!”
9. Wrong leaf/medicine: “Look for the orange spots!” (swap in the actual pictured badge).
10. Finish: “The tree feels better! A tree sticker for my book!”

The preview's optional browser speech is temporary and not a shipped voice
asset. Production uses the authorized synthetic voice pipeline and separate
listening acceptance. Do not modify or clone protected family recordings.

## Assistance, agency, and save requirements

At 0s speak the question and pulse the source. At 5s make the correct choice glow
and connect it to the clue. At 10s demonstrate a tap with a moving hand. Neither
demonstration nor elapsed time can select a choice. Wrong taps wiggle, repeat
the cue, advance assistance to at least level1, and preserve every correct choice.
Only a fresh intentional correct tap commits the choice. Holding, double taps,
stale touches across page changes, focus loss and returning from pause must not
auto-answer the next page. Save after each correct choice and after local
treatment. Replay/re-entry retains learned stickers without granting a passive win.

## Part A / Part B and integration boundary

The Opera training can keep three patients across a session, but **each patient
has exactly these three book decisions**, with four choices each. Do not confuse
“three rounds” with the superseded three-card difficulty tier. The Sky Lagoon
party tree uses the same leaf-based sequence; no separate broken-branch page.
A healed tree remains visible at the lawn finale and after the King takes the candle.

Keep Chef strawberry completion in the implementation plan. Migrate legacy
Candy Maker Day Two completion without sending a completed child backward:
credit the replacement tree job and healthy party tree when the legacy completed
piece is present. Preserve partial progress in a compatibility record; map the
replacement to a resumable phase with a welcoming cue rather than silently
deleting the old phase. Never remove save keys.

Do not copy act indices, masks or old save edits from the recovered August
prototype. Recalculate against exact current dev when runtime implementation
starts. The earlier handoff's bit18 remains a proposal requiring code validation.

## Review evidence and acceptance

The packet includes an interactive one-patient layout study (PREVIEW.html), its
pure matching model and logic tests. It demonstrates the three-stage decision
ordering and four options, then a deliberate help tap. It is **not the Godot
implementation**, and its delayed state switch is not accepted medicine-use
animation. Browser security blocked local-page UI inspection in this session;
source/model validation does not claim browser visual acceptance.

Required next production evidence: final four-species leaf/card mapping; authored
book-opening and local medicine gestures; Godot integration and voice assets;
exact 4.7.2 import/trusted probes; two-aspect Mobile captures; mid-step save,
wrong/passive/focus/teardown checks; target-device30fps; child comprehension and
owner art/voice acceptance. No current finding is closed by this handoff.

[Audit impact](audit_impacts/arborist-art-recovery-20260929.json).
