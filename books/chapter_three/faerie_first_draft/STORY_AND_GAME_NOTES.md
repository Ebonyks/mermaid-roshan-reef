# Mermaid Roshan and the Butterfly Garden - first-draft design notes

Status: `PROPOSED / FIRST_DRAFT`. Owner correction 2026-09-30: bottom-up design, a book first, and game adaptation afterward. Baseline `b65c21fdddd79f272a6854f241faa1441abe6616`. [Impact record](../../../design/audit_impacts/fairy-storybook-bottom-up-20260930.json). The manuscript is in book.json; SOURCE_MANIFEST.json records every source hash and PDF placement. The PDF is output/pdf/Mermaid_Roshan_and_the_Butterfly_Garden_DRAFT_01.pdf at repository root.

## 1. Corrected commission and authority

The previous playable prototype went beyond the story design. It is preserved as an experiment, with its real test history, but its three-apple/three-butterfly/three-flower loop, magical root rubbing, costumes and compressed geography do not control this chapter. Machine passes did not establish a suitable whole-game design. This commission produces a book draft, not more runtime implementation.

Development order: inspect existing resources and their authority; connect them into a story; establish read-aloud pacing; review the illustrated manuscript; derive only the play required by that story. This follows DL-AUTH-05 through DL-AUTH-07 and DL-PLAN-02, DL-PLAN-03, DL-PLAN-05 and DL-PLAN-06. Direct owner steering controls the work order when the generic chapter guide describes an early playable activity.

Current domain sources are the [chapter guide](../../../design/09_CHAPTER_DEVELOPMENT_GUIDE.md), [Chapter Two spine](../../../design/CHAPTER2_EIGHT_CAREER_PRODUCTION_SPINE_2026-08-30.md), [Chapter Three route](../../../design/FAIRY_CONSERVATORY_CHAPTER3_2026-08-30.md), and [revised Tree Book](../../../design/ARBORIST_TREE_BOOK_HANDOFF_2026-09-29.md), classified in the [ledger](../../../design/05_DOC_LEDGER.md). Old three-dimensional reef/Butterfly implementations supply evidence, not accepted final construction.

The Rumi reference is the latest resource-led proposal in the chat **Design Rumi's undersea adventure** (`01a0f35d-f268-7751-aa9b-79fa94ceeacc`): the existing turtle family, Kareem, kelp and wreck/cave lead to *The Turtle's Way Home*. Its superseded Nori/Singing Shell and Lantern Reef inventions are excluded. That chat establishes the desired method, not accepted shared ending canon. The Chapter One v29 book at `82a6dc1dba381c0b3ef507a8397512fa09ef624e` supplies the pacing and 7 x 5 inch Sniglet reference: someone Roshan helps can later help Roshan; a quiet beat separates rescue from the larger payoff. Chapter One's cleaning finale is book-scoped and is not a game combat rewrite.

## 2. Story before activities

Roshan leaves a still-loved Pearl Castle seeking faerie magic after the candle-taking. The existing sky doorway leads her to the existing Butterfly House. Finding its seven lost babies changes her priority: help these little friends first. The rescue becomes a relationship, not a collection count.

At home together, the butterflies need a meal. The sick tree makes that wish concrete. Roshan uses what she knows as an arborist, looking at the tree and its visibly spotted leaf, then choosing the matching pictured spray. The same tree recovers, blossoms and provides the fruit. Her earlier chef experience now has a purpose: prepare a picnic for the friends she brought home.

The picnic is the quiet middle of the story, with a small funny butterfly loop. The butterflies then help Roshan find the Fairy Fountain and stay beside her through the pond journey. The existing Fairy Flower's closed, opening and bloom states supply the larger climax. Roshan returns with a contribution for the castle, leaving the garden bright and its friends safe.

The fruit-bearing consequence, picnic, one baby's local personality, guide relationship and flower-to-castle sharing are **proposed connections**, not established old scene facts. No new principal character, magical machine, kingdom or antagonist is introduced. The existing source art supports identities and states; it does not prove every new story moment is already illustrated.

## 3. Pacing and purpose

| Pages | Emotional purpose | Visible cause and lasting consequence | Natural stopping point |
|---|---|---|---|
| 1-4 | Familiar home, shared wish, then wonder | Candle-taking precedes the existing Moonflower/Skyway route; completed birthday and cleaning remain intact | Butterfly House arrival |
| 5-8 | Concern and reassuring rescue | Seven existing lost babies return home; Roshan chooses kindness before her own search | Every baby remains home |
| 9-17 | Notice a need, observe, choose, care, harvest | The actual spotted leaf matches the actual spray; the same tree becomes healthy and bears fruit | Diagnosis, treatment and harvest |
| 18-22 | Familiar skill, sharing, rest and humour | Fruit from that tree becomes the picnic; the rescued friends recover and become partners | Picnic together |
| 23-25 | Reciprocity and fresh wonder | Friends guide Roshan through the existing Fairy Fountain into fairy flight | Pond arrival |
| 26-30 | Sustained shared effort and a large release | One Fairy Flower changes from shut bud through opening to bloom | Visible bloom |
| 31-32 | Safe homecoming and room for the next book | Faerie contribution reaches home without taking the garden's magic | Exact castle return |

The book uses spacious object/character pages and a few wider source-art reveals, not one activity panel per page. Each picture is either existing full art at the page edges or a real alpha silhouette; no HUD captures, rounded screenshot cards or invented replacement scenes. Text remains editable navy Sniglet in quiet space, without opaque caption bands. There is no generated raster art. Application/contact, cut fruit and full rescue staging remain gaps, rather than fabricated finished frames.

## 4. Existing resources that shaped the draft

| Resource family | Existing use and why it matters | Decision and limits |
|---|---|---|
| Moonflower, Rainbow Skyway, Butterfly House | Current Chapter Three physical route; the house supplies a recognizable destination and return | Reuse actual doorway/causeway/house sources; preserve geographic order |
| Seven baby butterflies | scripts/galaxy.gd SHARDS/_build_shards, per-baby sticker keys and rescued-following train | Keep seven rescues and saved meanings. The one reused GEN2 card is a layout study, not seven newly approved identities |
| Revised Tree Book | Current orange-spotted/healthy patient, matched leaf/spray sheet, book-reading pose | Use the same patient and actual orange badge. Do not revive the superseded prune/wrap or fixed thirst/broken-branch sequence |
| Story apples and chef atlas | Existing fruit-prop family and established birthday cooking skill | They make the ingredient-to-meal connection affordable. True fruit growth, wash, cutting, plates and feeding art remain open |
| Fairy V5 pond and Fairy Flower states | scripts/games/fairy.gd background, leaf wreath, closed bud, opening and bloom | One coherent flower climax, not the prototype's invented three-flower finale. Existing 3D runtime debt grants no 3D rebuild authority |
| Roshan base, book pose, chef cell and fairy cutout | Existing authored identities, actual alpha and complete usable selected cells | Preserve contours, native pixels and authored light; existing poses do not prove new contact verbs |

SOURCE_MANIFEST.json records selected source paths, hashes, native dimensions, license/provenance, every page crop/placement and unchanged-source claims. Originals are not modified or recompressed. Cropping here is a PDF clipping window; no derivative raster is created. Any later raster repair uses Aseprite under the owner's current workflow, and must remain within DL-ASSET-08.

## 5. Source gaps exposed by the book

| ID | Missing book moment | What the draft actually shows |
|---|---|---|
| G01 | Candle absence and partial castle restoration in the real hall | Existing Moonflower/Roshan cards; no false newly restored castle plate |
| G02 | Distinct seven-baby lost, approach, rescue and home compositions | Existing complete butterfly card and Roshan; multiple cards are a layout study |
| G03 | Rest, meal sharing and the funny loop/reaction | Existing butterfly and Roshan identities; no accepted new acting |
| G04 | Roshan's hand/bottle contact and spray landing on the correct leaf | Actual pictured leaf/remedy pair; reading is not claimed as treatment animation |
| G05 | Blossoms-to-fruit and local harvest/carrying | Same healthy tree plus existing apples in a proposed book composition |
| G06 | Fruit washing, full cutting pose, cut faces, plates and snack portions | Existing whole fruit/chef cell or picnic friends; no invented sliced-fruit pixels |
| G07 | A current reusable 2D Fairy Fountain and transformation staging | Guiding butterflies and existing fairy identity; no borrowed castle fountain substitute |
| G08 | Butterfly-guided flight, Roshan's sparkles/contact and cooperative reactions | Existing pond, fairy identity and single flower state family |
| G09 | What exactly carries the magic and how each half changes Pearl Castle | Existing flower/doorway cards; contribution mechanism remains a shared-story proposal |

A missing illustration does not authorize a scene redraw. Record a bounded source-preserving crop/isolation/edit plan only after selecting an actual source. No image generation is performed in this first draft.

## 6. Place in the game as a whole

| Arc | Already established | What this draft proposes | What remains unresolved |
|---|---|---|---|
| Day One | Help castle friends and restore familiar spaces | Repeat the care-to-friendship logic without redoing those rooms | No earlier saved work may be lost |
| Birthday / Chapter Two | Ordered skills, completed party/cake, Ember King's own-birthday candle motive | Let learned arborist/chef care have a new social purpose | Do not change career order, cake state or candle motive |
| Faerie half | Moonflower, Skyway, house, seven babies, fountain, fairy skin and flower | Connect rescue, Tree Book care, fruit and picnic into reciprocal friendship before the flower journey | Book/canon review and source gaps |
| Rumi / undersea half | Existing Rumi and resource-led turtle/Kareem/reef rescue proposal | Both books can share the wish to help home and let helped friends help back | That separate proposal and its turtle-family relationships are not accepted canon here |
| Shared castle ending | Owner requests two halves of magic restoration | Each place keeps its own magic while giving a contribution | Exact vessel, visible castle changes, sequence and combined ending need a concrete shared-story proposal before game code |

There is no claim that three prepared apples equal a chapter key, that a new currency replaces pearls, or that the book allocates new save fields. Existing bwdone, fairyskin, flower, per-baby stickers, rewards and legacy routes retain their meanings.

## 7. Later playable adaptation, conditional on the story

| Story need | Candidate play, derived from that need | Persistent result and non-reader support |
|---|---|---|
| Bring the babies home | Search/approach/gentle guiding variant of the existing rescue | Each actual baby stays home; exact cue and target pointer; wrong/passive input cannot rescue |
| Understand the sick tree | Actual Tree Book tree, leaf and medicine picture decisions, then visible local treatment | Same diagnosed tree recovers; preserve three decisions/four choices in the current job domain; no instant remote heal |
| Make the picnic | Pick that tree's fruit, wash and prepare pictured portions, then serve friends | Ingredients become an actual meal; one-finger forgiving tools, recoverable mistakes and hand/object contact |
| Reach and bloom the flower | Existing gentle fairy-shooter grammar adapted to the book's single flower and helping companions | Same flower opens; helpers give readable assistance, not free completion |
| Bring a contribution home | Intentional return through the existing route | Exact Main Hall context and durable partial contribution, after its story mechanism is designed |

No runtime implementation is commissioned by these candidate verbs. Navigation must remain Main Hall -> Moonflower -> Rainbow Skyway -> Butterfly House -> Butterfly World -> Fairy Fountain -> Fairy Pond and symmetric return. Later state belongs to the current production state owner and adds defaults without removing unknown/legacy data. Key names, reward rules, objective recordings and final contact clips are not allocated in this story draft.

## 8. Review and learning

First review: can a listener explain why Roshan interrupts her magic search, why the tree matters to the picnic, why the butterflies help her, and what remains to do at home? Check for seven distinct rescued friends, a quiet middle, a single larger payoff, kind suspense, meaningful Roshan decisions and useful rather than decorative jobs. Read-aloud length and enjoyment are unobserved design targets, not measured child evidence.

Then refine the story and shared two-book ending before a representative game activity. Complete art-source coverage and contact studies before final illustration/game claims. Later machine checks cover intentional/wrong/passive/repeat input, checkpoint reconstruction, focus/Back, exact voices, true-2D construction and Mobile performance. Device, child, SLP/read-aloud, owner, final-print and release acceptance stay separate.

The owner correction is recorded explicitly: a technically green standalone prototype did not demonstrate that the story and whole-game design were sound. This draft changes the method and authority labels; it does not erase the prototype's historical evidence or rewrite unchanged findings.
