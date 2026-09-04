#!/usr/bin/env python3
"""Build the selective Day One Grok regeneration handoff overlay.

The overlay deliberately does not alter or replace the approved visual archive.
It records rough-cut disposition, weak-frame reconstruction instructions, and
DRAFT Imagine cards whose missing shot-opening bindings remain explicit.
"""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CIN = ROOT / "assets_src" / "cinematics"
SOURCE_COMMIT = "076661afb9e092627eb5dfae7c39fecb27463892"
CLIP_COMMIT = "5ca170e11c77ea55c3224f9f275b94b8fd62ca36"
REPO = "Ebonyks/mermaid-roshan-reef"
RELEASE_TAG = "day1-regen-motion-ref-2026-09-03"
RELEASE_URL = f"https://github.com/{REPO}/releases/tag/{RELEASE_TAG}"
DATE = "2026-09-03"
OVERLAY = CIN / f"day_one_grok_regeneration_handoffs_{DATE}"


PACKETS = {
	"D1-C00": "d1_c00_opening_flight_visual_v1",
	"D1-C01": "d1_c01_lagoon_landing_castle_approach_visual_v1",
	"D1-C02": "d1_c02_first_dirty_castle_discovery_visual_v1",
	"D1-C03": "d1_c03_bathroom_dirty_entry_visual_v1",
	"D1-C04": "d1_c04_bathroom_restored_visual_v1",
	"D1-C05": "d1_c05_pool_dirty_discovery_visual_v1",
	"D1-C06": "d1_c06_pool_purification_rumi_hug_visual_v1",
	"D1-C07": "d1_c07_stuffie_dirty_discovery_visual_v1",
	"D1-C08": "d1_c08_stuffie_restoration_visual_v1",
	"D1-C09": "d1_c09_art_room_dirty_discovery_visual_v1",
	"D1-C10": "d1_c10_art_room_restored_visual_v1",
	"D1-C11": "d1_c11_grand_puff_reveal_visual_v1",
	"D1-C12": "d1_c12_restored_castle_finale_visual_v1",
	"D1-C13": "d1_c13_grand_puff_friendship_completion_visual_v1",
}

TITLES = {
	"D1-C00": "Opening Flight — Roshan and Daddy",
	"D1-C01": "Lagoon Landing and Castle Approach",
	"D1-C02": "First Dirty Castle Discovery",
	"D1-C03": "Bubble Bathroom — Dirty Entry",
	"D1-C04": "Bubble Bathroom — Restored",
	"D1-C05": "Sparkle Pool — Dirty Discovery",
	"D1-C06": "Sparkle Pool — Purification, Rumi and Hug",
	"D1-C07": "Stuffie Room — Dirty Discovery",
	"D1-C08": "Stuffie Room — Basket and Wing-Blast Restoration",
	"D1-C09": "Art Room — Spilled Supplies Discovery",
	"D1-C10": "Art Room — Clean Desk Awakening",
	"D1-C11": "Boss Door and Grand Puff Reveal",
	"D1-C12": "Day One Restored-Castle Celebration",
	"D1-C13": "Grand Puff Friendship Completion",
}

GAME_AUTHORITY = {
	"D1-C01": ("scripts/day_one_director.gd", "arrival media precedes the dirty-castle discovery; the lagoon handoff must preserve Roshan, Daddy, the stationary plane, and the closed castle"),
	"D1-C02": ("scripts/day_one_director.gd", "dirty_castle_discovery is observation only; no cleanup or labeled evidence is created"),
	"D1-C03": ("scripts/games/day_one_bathroom_cleanup.gd", "one dirty tub, one separate swimming bunny, an authorized tool basket, and two later live cleaning gestures"),
	"D1-C05": ("scripts/games/day_one_pool_cleanup.gd", "the dirty pool begins with six surface targets, three waterfall lanes, and an eight-tug seahorse obstruction"),
	"D1-C06": ("scripts/games/day_one_pool_cleanup.gd", "pool_surface → waterfall → seahorse is the fixed order; Rumi rises only after all three complete"),
	"D1-C07": ("scripts/arena/castle_rooms_25d.gd", "one Baby Eagle is visibly held by exactly two rescue pin bunnies; no swing or partial-wing hunt exists"),
	"D1-C08": ("scripts/arena/castle_rooms_25d.gd", "Roshan clears eagle_pin_left and eagle_pin_right; the room cleans, Baby Eagle thanks/rises/departs, then the companion picker opens"),
	"D1-C09": ("scripts/day_one_art_studio.gd", "four loose material groups are collected before exactly three fixed grime cards become the active targets"),
	"D1-C10": ("scripts/day_one_art_studio.gd", "all seven cleanup actions unlock the blank desk; customization UI opens only after the desk touch"),
	"D1-C11": ("scripts/day_one_director.gd and scripts/games/dust_boss.gd", "all four rooms arm the boss door; the empty octagonal arena precedes Grand Puff's soft showing"),
	"D1-C12": ("scripts/games/dust_boss.gd", "the FRIENDS result is harmless and positive; this recap remains motion reference until its inherited endpoint is accepted"),
	"D1-C13": ("scripts/games/dust_boss.gd plus owner-directed C13 extension", "insert the cooperative coda immediately after the third successful round and before the FRIENDS implosion completes; never reconstitute Grand Puff after he has vanished"),
}

KEEP = {
	"D1-C00": ["C00_S01_v1_plane_clouds.mp4", "C00_S02_v1_cabin.mp4", "C00_S03_v1_roshan_wonder.mp4", "C00_S04_v1_handhold.mp4", "C00_S05_v1_lagoon_reveal.mp4", "C00_S06_v1_landing_prep.mp4"],
	"D1-C01": ["C01_S01_v1_dock.mp4", "C01_S04_v1_castle_doors.mp4"],
	"D1-C02": ["C02_S01_v1_door_open.mp4", "C02_S02_v1_dirty_hall.mp4", "C02_S04_v1_bathroom_glow.mp4"],
	"D1-C03": ["C03_S01_v2_empty_dirty_bath.mp4"],
	"D1-C04": ["C04_S01_v2_scrub.mp4", "C04_S02_water_clears.mp4", "C04_S03_bunny_exits.mp4", "C04_S04_v2_clean_endpoint.mp4"],
	"D1-C05": ["C05_S01_v1_pool_entry.mp4", "C05_S02_waterline_trash.mp4", "C05_S03_v1_skimmer.mp4", "C05_S06_problem_map.mp4"],
	"D1-C06": ["C06_S01_v2_pull_plug.mp4", "C06_S02_seahorse_flow.mp4", "C06_S07_v1_rumi_rise.mp4"],
	"D1-C07": ["C07_S01_v2_empty_dirty_stuffie.mp4", "C07_S02_v2_roshan_enters.mp4", "C07_S06_v1_eagle_pinned.mp4"],
	"D1-C08": ["C08_S01_basket_wobble.mp4", "C08_S05_eagle_wing_prep.mp4"],
	"D1-C09": ["C09_S01_v1_loose_supplies_OFFICIAL.mp4", "C09_S02_v1_roshan_scan_OFFICIAL.mp4", "C09_S03_four_supplies.mp4"],
	"D1-C10": ["C10_S01_v1_final_scrub_OFFICIAL.mp4", "C10_S04_v1_desk_wake_OFFICIAL.mp4"],
	"D1-C11": ["C11_S01_route_lights.mp4"],
	"D1-C12": ["C12_S01_clean_bath_bunny.mp4", "C12_S02_rumi_pool_recap.mp4", "C12_S03_stuffie_recap.mp4", "C12_S04_art_desk_glow.mp4", "C12_family_reunion_hug.mp4"],
	"D1-C13": [],
}

REJECT = {
	"D1-C03": ["C03_bunny_discover.mp4"],
	"D1-C07": ["C07_S06_v2_eagle_pinned.mp4"],
	"D1-C09": ["C09_S01_v1_empty_dirty_art_PROVISIONAL.mp4", "C09_S01_v2_empty_dirty_art_PROVISIONAL.mp4", "C09_S02_v1_roshan_enters_art.mp4", "C09_S02_v2_roshan_enters_art.mp4"],
	"D1-C10": ["C10_S04_v1_desk_wake.mp4", "C10_S04_v2_desk_wake.mp4"],
	"D1-C11": ["C11_S01_v1_routes_converge.mp4"],
	"D1-C12": ["C12_S04_v1_art_desk.mp4"],
}


def shot(
	movie: str,
	number: str,
	title: str,
	camera: str,
	timeline: tuple[str, str, str],
	must_move: str,
	must_not_move: str,
	end: str,
	negatives: str,
	sound: str,
	bindings: list[tuple[str, str]],
	evidence: list[tuple[str | None, str]],
	duration: int = 6,
	conditional: bool = False,
	image1_requirement: str | None = None,
) -> dict:
	return {
		"movie": movie,
		"shot_id": f"{movie}-S{number}",
		"title": title,
		"camera": camera,
		"timeline": timeline,
		"must_move": must_move,
		"must_not_move": must_not_move,
		"end": end,
		"negatives": negatives,
		"sound": sound,
		"bindings": bindings,
		"evidence": evidence,
		"duration": duration,
		"conditional": conditional,
		"image1_requirement": image1_requirement or "human-approved, clean, HUD-free shot-opening frame in the exact inherited state",
	}


SHOTS = [
	shot("D1-C01", "02", "Daddy offers his hand on the dock", "locked", (
		"daddy exits the stationary pearl plane, turns, and offers one open hand",
		"roshan places her hand in his while both tails and costumes remain coherent",
		"they settle at child-safe distance with correct hand contact",
	), "Daddy exits and offers; Roshan completes one hand contact", "plane, dock, waterline, castle silhouette, costumes, crowns, glasses, and continuous tails", "Roshan and Daddy hold hands beside the unchanged stationary plane", "no pulling, floating hands, legs, extra cast, costume drift, plane redesign, text, HUD, or camera drift", "soft water and pearl/fabric movement; no voices", [("location", "layout and lighting"), ("roshan", "Roshan identity"), ("daddy", "Daddy identity"), ("plane", "pearl plane identity")], [(None, "shot is absent from the delivered clip set")], image1_requirement="accepted clean endpoint extracted from D1-C01-S01"),
	shot("D1-C01", "03", "Hand-in-hand castle approach", "smooth side-follow", (
		"roshan and daddy begin moving hand-in-hand from the accepted dock endpoint",
		"they travel toward the exact four-tower pearl castle at stable scale",
		"they stop in the forecourt with the same closed doors ahead",
	), "one continuous paired approach", "lagoon geography, hand contact, castle proportions, closed doors, costumes, and tails", "both characters stand together in the forecourt facing the unchanged closed doors", "no teleport, bridge, wildlife, castle enlargement, changed costumes, extra cast, text, HUD, or camera drift", "lagoon water and light magic; no voices", [("location", "lagoon geography"), ("roshan", "Roshan identity"), ("daddy", "Daddy identity"), ("castle", "castle topology")], [(None, "shot is absent from the delivered clip set")], image1_requirement="accepted D1-C01-S02 hand-contact endpoint"),
	shot("D1-C02", "03", "Close dirty-hall evidence inspection", "short lateral", (
		"the camera begins on the accepted Screen-A dirty-hall composition",
		"one integrated grime patch, one friendly dust-bunny trace, and one harmless scrap become readable",
		"roshan points once without touching or cleaning",
	), "evidence becomes readable and Roshan points", "Screen-A floor, molding, portals, walls, fixtures, Daddy, and all existing character positions", "the three evidence types remain visible and untouched", "no UI marker, clip-art trash, insects, danger, cleanup, invented wall, reverse-room geometry, text, or HUD", "tiny dust rustle and muted hall room tone; no voices", [("location", "Main Hall Screen-A layout"), ("roshan", "Roshan identity"), ("daddy", "Daddy identity")], [(None, "shot is absent from the delivered clip set")], image1_requirement="accepted D1-C02-S02 endpoint after Screen-A topology approval"),
	shot("D1-C03", "02", "Roshan crosses the dirty-bathroom threshold", "short follow", (
		"roshan crosses into the single-tub dirty bathroom",
		"she looks from the murky tub to the dirty sink while moving fully inside",
		"she settles with the entrance and room orientation still readable",
	), "Roshan crosses and makes one tub-to-sink look", "single tub, sink, tools, grime cards, entrance, child identity, clothes, and continuous tail", "Roshan is fully inside and the entrance remains spatially clear", "no legs, shoes, room rotation, second tub, cleaning, extra cast, text, or HUD", "soft tail movement and a quiet drip; no voices", [("location", "dirty bathroom layout"), ("roshan", "Roshan identity"), ("tub_grime", "dirty tub material")], [(None, "shot is absent from the delivered clip set")], image1_requirement="accepted D1-C03-S01 dirty-room endpoint"),
	shot("D1-C03", "03", "Swimming bunny in the dirty tub", "locked", (
		"one approved swimming dust bunny paddles weakly but safely in the murky tub",
		"the water stays dirty and the bunny remains a coherent single creature",
		"roshan reacts with concern at frame edge",
	), "one bunny paddles and Roshan reacts", "tub geometry, sink, dirty water state, bunny anatomy, and Roshan edge position", "the single swimmer is clearly visible and needs gentle rescue", "no duplicate bunny, land bunny, clean water, drowning terror, invented anatomy, room redesign, text, or HUD", "small paddles and a gentle worried pulse; no voices", [("location", "dirty bathroom layout"), ("swimming_bunny", "swimming bunny identity"), ("tub_grime", "murky tub material")], [("C03_bunny_discover.mp4", "frames 0–144 use a clean, bright tub state and oversized creature, so the entire shot contradicts the dirty-entry setup")], image1_requirement="accepted D1-C03-S02 endpoint"),
	shot("D1-C03", "04", "Pre-contact tool resolve", "subtle push-in", (
		"roshan follows her gaze from the swimmer toward the dirty sink and approved tools",
		"she reaches toward the nearest approved tool without changing the room state",
		"her hand stops in a clean visible gap before contact",
	), "Roshan makes one gaze-and-reach action", "dirty room, murky tub, swimmer, sink, tools, grime, and character anatomy", "Roshan holds a determined pre-contact hand gap while all dirt remains", "no scrub, tool teleport, UI pointer, extra supplies, room redesign, cleanup, text, or HUD", "resolve chime over quiet drips; no voices", [("location", "dirty bathroom layout"), ("roshan", "Roshan identity"), ("cleanup_basket", "approved tool group")], [("C03_S04_v1_tool_reach.mp4", "frames 48–144 do not preserve a clear pre-contact endpoint"), ("C03_S04_v1_tools_resolve.mp4", "frames 0–47 begin from an unstable dirty-room composition and frames 108–144 leave the tool gap ambiguous"), ("C03_S04_v2_tools_resolve.mp4", "frames 48–144 drift tool/room relationships during the resolve")], image1_requirement="accepted D1-C03-S03 endpoint"),
	shot("D1-C05", "04", "Blocked rainbow-source close-up", "subtle upward tilt", (
		"begin on the exact top source with dull rainbow flow fully blocked",
		"opaque olive-brown sludge with one leaf and one wrapper remains lodged at the source",
		"the tilt stops on the unchanged readable obstruction",
	), "camera reveals one fixed obstruction", "rainbow fixture, arch, source position, debris contact, and dirty grade", "the top source remains blocked, dull, and still", "no clean water, bright rainbow, bottom-up motion, invented basin, relocated fixture, Roshan, seahorse, text, or HUD", "thick drip and blocked gurgle; no voices", [("location", "pool geography"), ("waterfall_clog", "clog material and fixture identity"), ("pool_trash", "debris identity")], [("C05_S04_clogged_waterfall.mp4", "frames 0–144 fail to hold a clean top-source obstruction view"), ("C05_S04_v2_waterfall.mp4", "frames 48–144 weaken source location and obstruction readability")], image1_requirement="approved clean close composition of the blocked top source"),
	shot("D1-C05", "05", "Sick seahorse with mouth plug", "locked", (
		"show the exact long-snouted seahorse at correct right-center scale",
		"a soggy pink wrapper-and-weed plug remains unmistakably lodged in its mouth nozzle",
		"roshan's concerned face enters at frame edge and stops",
	), "Roshan enters the edge while the weak seahorse coughs once", "seahorse topology, right-center position, plug contact, pool geography, and dirty state", "the mouth plug is readable and still lodged", "no different animal, plug beside the mouth, clean flow, frightening injury, extraction, text, or HUD", "weak watery cough and room tone; no voices", [("location", "pool geography"), ("roshan", "Roshan identity"), ("seahorse", "sick seahorse identity"), ("seahorse_plug", "mouth plug material")], [("C05_S05_sick_seahorse.mp4", "frames 0–144 do not consistently lock scale, identity, and mouth-plug contact"), ("C05_S05_v1_seahorse_plug.mp4", "frames 48–144 leave the plug position ambiguous"), ("C05_S05_v2_seahorse.mp4", "frames 0–144 drift seahorse identity/scale")], conditional=True, image1_requirement="approved right-center seahorse close composition; skip regeneration only if Sol confirms the existing mouth plug and topology"),
]


def add_more_shots() -> None:
	SHOTS.extend([
		shot("D1-C06", "03", "Rainbow waterfall restarts top-down", "gentle downward tilt", ("clean rainbow ignites at the exact blocked top source", "the clean band travels downward and pushes sludge and debris away", "the flow reaches the lower lip and settles"), "one top-down clearing front", "fixture position, arches, flow direction, pool scale, and dirty room outside the cleared band", "clean rainbow reaches the lower lip without changing the rest of the room", "no bottom-up start, instant clean room, separate basin, seahorse, Rumi, text, or HUD", "rising water rush and crystalline sweep; no voices", [("location", "pool geography"), ("waterfall_rest", "restored waterfall identity")], [("C06_S03_rainbow_waterfall.mp4", "frames 0–47 begin too clean or from the wrong source composition"), ("C06_S03_v1_rainbow_restart.mp4", "frames 48–144 reverse or blur the top-down causal read"), ("C06_S03_v2_rainbow.mp4", "frames 0–144 use an inconsistent composition")], image1_requirement="accepted blocked-source endpoint inherited from D1-C05-S04"),
		shot("D1-C06", "04", "Both clean sources feed one giant pool", "smooth pullback", ("begin on the restored rainbow-source endpoint", "pull back once to reveal rainbow stream left-center and seahorse stream right-center", "both streams visibly enter the same giant pool"), "one re-establishing pullback", "arches, source positions, seahorse position, pool boundary, and flow directions", "both sources and the complete giant-pool geometry are visible together", "no small basin, moved arches, moved seahorse, reversed flow, new outlet, text, or HUD", "layered clean-water rush; no voices", [("location", "pool geography"), ("waterfall_rest", "rainbow fixture identity"), ("seahorse_rest", "seahorse fountain identity")], [("C06_S04_purification_meet.mp4", "frames 0–144 do not clearly prove both fixed sources enter the same giant pool")], image1_requirement="accepted D1-C06-S03 endpoint"),
		shot("D1-C06", "05", "Two purification fronts meet", "locked", ("two distinct clear fronts spread from the fixed left and right sources", "each front displaces algae through the same water volume", "the fronts meet once near center in one bright ripple"), "two water fronts spread and meet once", "pool boundary, sources, fixtures, room geometry, and dry surfaces", "one joined bright ripple rests at pool center", "no instant flash, dry floor, third source, overlay-only effect, characters, text, or HUD", "converging shimmer and soft impact chime; no voices", [("location", "pool geography"), ("waterfall_rest", "left source identity"), ("seahorse_rest", "right source identity")], [("C06_S05_v1_rumi_rises.mp4", "frames 0–144 are mislabeled Rumi-rise imagery and omit the required two-front purification"), ("C06_S05_v2_rumi_rises.mp4", "frames 0–144 are mislabeled Rumi-rise imagery and omit the required two-front purification")], image1_requirement="accepted D1-C06-S04 two-source endpoint"),
		shot("D1-C06", "06", "Violet emergence prelude", "slow push-in", ("begin on the joined purification ripple", "clean clarity fills the giant pool and the grade returns to pearl, aqua, and lavender", "a localized violet light rises from below without revealing a person"), "one localized underwater glow rises", "pool geometry, both sources, fixtures, water surface, and empty character field", "clean water and a contained violet glow rest at pool center", "no neon room wash, silhouette substitute, empty basin, early Rumi, text, or HUD", "deep magical resonance and clear-water ambience; no voices", [("location", "pool geography"), ("waterfall_rest", "restored fixture identity"), ("seahorse_rest", "restored seahorse identity")], [(None, "shot is absent from the delivered clip set")], image1_requirement="accepted D1-C06-S05 joined-front endpoint"),
		shot("D1-C06", "08", "Rumi thanks Roshan and opens her arms", "locked", ("rumi places one hand over her heart and gives one warm speaking gesture", "she opens both arms toward Roshan while both bodies stay separate", "she holds the clear invitation"), "Rumi makes one thanks-to-invitation gesture", "Rumi and Roshan identities, scale, faces, hands, continuous tails, pool, and both streams", "Rumi's arms are open and Roshan remains separate before the hug", "no subtitles, synthetic dialogue, hand deformation, extra cast, fused bodies, text, or HUD", "quiet water and warm music; final family dialogue added later", [("location", "clean pool geography"), ("rumi", "Rumi identity"), ("roshan", "Roshan identity")], [("C06_rumi_swim.mp4", "frames 0–144 depict swimming rather than the required thanks and invitation beat")], image1_requirement="accepted D1-C06-S07 Rumi reveal endpoint"),
		shot("D1-C06", "09", "Roshan completes the hug", "subtle pullback", ("roshan moves from the accepted invitation endpoint into Rumi's arms", "their arms make one coherent affectionate contact while faces remain visible", "they settle with distinct torsos and two separate tails"), "Roshan approaches and completes one hug", "faces, torsos, hands, two tails, scale, pool geometry, and both fixed streams", "Roshan and Rumi hold one stable joyful embrace with distinct bodies", "no fused torsos, merged tails, extra arms, substitute Rumi, kiss, tiny pool, text, or HUD", "water sparkle and warm resolution; no voices", [("location", "clean pool geography"), ("rumi", "Rumi identity"), ("roshan", "Roshan identity")], [("C06_rumi_roshan_hug.mp4", "frames 0–47 begin in an ambiguous pre-fused embrace and frames 48–144 never establish a clean approach/contact")], image1_requirement="accepted D1-C06-S08 open-arm endpoint"),
	])


add_more_shots()


SHOTS.extend([
	shot("D1-C07", "04", "One supported swinging dust bunny", "slow pendulum-follow", ("show exactly one intact lavender playroom dust bunny attached to the established support", "the bunny makes one small gentle swing with visible rope contact", "the swing settles and one harmless dust trace falls"), "one supported bunny swings and settles", "dirty room, basket, support, rope contact, bunny face, ears, body, and curl silhouette", "one bunny remains safely attached and settled", "no second bunny, smoke creature, floating trail, detached rope, clone, scary expression, rescue, cleanup, room rotation, text, or HUD", "soft rope creak, fabric rustle, and a tiny playful squeak; no voices", [("location", "dirty Stuffie Room geography"), ("playroom_bunny", "playroom bunny identity"), ("stuffie_nook", "support and nook topology")], [("C07_S04_v1_swing_bunny.mp4", "frames 48–144 make support contact weak or unclear"), ("C07_S04_v2_swing_bunny.mp4", "frames 48–144 lose the rope and turn the bunny into a floating trail")], image1_requirement="approved clean opening composition of the existing supported bunny in the dirty room"),
	shot("D1-C07", "05", "Partial Baby Eagle wing trail", "slow lateral reveal", ("begin with Roshan's gaze line and only a partly obscured turquoise, yellow, and pink wing beneath grounded clutter", "reveal more of the same wing along the existing floor trail without exposing the full bird", "stop while the wing remains partly hidden"), "one partial wing becomes identifiable", "every pile, fixture, floor contact, Roshan, and the hidden bird position", "one Baby Eagle wing is identifiable but the full bird is not yet revealed", "no full-body reveal, duplicate bird, injury, arrow, moving furniture, cleanup, new prop, camera rotation, text, or HUD", "soft clutter rustle and a restrained concerned chord; no voices", [("location", "dirty Stuffie Room geography"), ("roshan", "Roshan identity"), ("baby_eagle_pinned", "Baby Eagle colors and anatomy")], [("C07_S05_wing_trail.mp4", "frames 48–144 expose the full eagle too early instead of preserving the partial discovery")], image1_requirement="accepted D1-C07-S04 endpoint with the established floor trail"),
	shot("D1-C07", "06", "Exactly one pinned Baby Eagle", "locked", ("show exactly one Baby Eagle partly concealed under soft grounded room mess", "roshan moves into concerned eye contact while the bird remains alert, intact, and visibly pinned", "both settle as Roshan resolves to help"), "Roshan makes eye contact with one pinned bird", "dirty room, clutter contact, bird position, turquoise/yellow/pink identity, beak, two wings, two feet, and Roshan's tail", "exactly one unharmed Baby Eagle is visibly pinned and Roshan is ready to help", "no second bird, brown substitute animal, duplicate body, backpack, crushed anatomy, horror, bunny takeover, cleanup, room change, text, or HUD", "small hopeful chirp and quiet resolve music; no voices", [("location", "dirty Stuffie Room geography"), ("roshan", "Roshan identity"), ("baby_eagle_pinned", "pinned Baby Eagle identity")], [("C07_S06_v1_eagle_discover.mp4", "frames 0–144 do not hold one exact pinned identity and clean reveal state"), ("C07_S06_v1_eagle_pinned.mp4", "usable as motion reference, but frames 108–144 still need full identity/topology confirmation"), ("C07_S06_v2_eagle_pinned.mp4", "frames 0–144 introduce an unrelated brown animal and identity conflict")], image1_requirement="accepted D1-C07-S05 partial-wing endpoint"),
	shot("D1-C08", "02", "Left basket ears-only warning", "locked", ("the established left basket makes one small warning wobble", "exactly one pair of lavender bunny ears rises briefly above the rim and ducks back", "the basket becomes still without a full bunny emerging"), "one left basket wobble and one ear-pair peek", "left basket, dirty room, background, rim, and hidden bunny body", "the left basket is still after one ears-only warning", "no full body, second ear pair, claws, scary eyes, duplicated basket, room change, cleanup, text, or HUD", "soft wicker rattle and a tiny playful squeak; no voices", [("location", "dirty Stuffie Room geography"), ("playroom_bunny", "bunny ear and color identity"), ("play_tent", "left-side landmark")], [("C08_S02_left_basket_ears.mp4", "frames 48–144 drift bunny anatomy beyond the approved ears-only read")], image1_requirement="accepted D1-C08-S01 left-basket endpoint"),
	shot("D1-C08", "03", "Right basket ears-only warning", "locked", ("the established right basket makes one small warning wobble", "exactly one pair of lavender bunny ears rises briefly above the opposite rim and ducks back", "the basket becomes still without a full bunny emerging"), "one right basket wobble and one ear-pair peek", "right basket, opposite-room position, dirty room, background, rim, and hidden bunny body", "the right basket is still after one ears-only warning", "no left-basket geometry reuse, full body, second ear pair, teleport, claws, scary eyes, room change, cleanup, text, or HUD", "soft wicker rattle and a tiny playful squeak; no voices", [("location", "dirty Stuffie Room geography"), ("playroom_bunny", "bunny ear and color identity"), ("stuffie_nook", "right-side landmark")], [("C08_S03_right_basket_ears.mp4", "frames 0–144 do not reliably preserve the opposite-room basket position and ears-only anatomy")], image1_requirement="accepted D1-C08-S02 endpoint with the right basket established"),
	shot("D1-C08", "04", "Exactly four bunnies emerge", "gentle pullback", ("begin with both established basket zones visible and no bunnies outside", "exactly four coherent lavender bunnies emerge, two from each basket", "all four settle separately while Roshan and one Baby Eagle watch"), "four and only four bunnies emerge and settle", "both baskets, room fixtures, Roshan, one Baby Eagle, floor contacts, and each bunny identity", "exactly four bunnies are individually countable and safely settled", "no fifth bunny, merged bodies, clone row, duplicate eagle, smoke, attack, cleanup, room change, text, or HUD", "four soft hops and cheerful fabric rustle; no voices", [("location", "dirty Stuffie Room geography"), ("playroom_bunny", "bunny identity"), ("baby_eagle_standing", "standing Baby Eagle identity"), ("roshan", "Roshan identity")], [("C08_S04_four_bunnies.mp4", "frames 48–144 leave the basket/foreground count ambiguous"), ("C08_S04_v2_four_bunnies.mp4", "frames 48–144 change the readable individual count and spacing")], image1_requirement="accepted D1-C08-S03 endpoint showing both baskets"),
	shot("D1-C08", "06", "Safe Baby Eagle wing blast", "locked", ("one standing Baby Eagle plants both feet and prepares both wings", "it performs one broad soft wing blast and only dust plus lightweight clutter move toward storage", "the last dust clears while all characters remain anchored"), "one safe wing blast clears integrated dust and light clutter", "walls, furniture, Roshan, exactly four bunnies, one eagle, room topology, and floor contacts", "the clean established room is revealed with all cast safe and anchored", "no tornado, character lift, violent impact, magic-only flash, furniture relocation, topology change, duplicate cast, text, or HUD", "broad soft whoosh, fabric flutter, and a clean reveal chime; no voices", [("location", "Stuffie Room geography"), ("baby_eagle_standing", "standing Baby Eagle identity"), ("playroom_bunny", "four-bunny identity"), ("roshan", "Roshan identity")], [("C08_S06_v1_wing_blast.mp4", "frames 48–144 jump to a clean bright room without readable airflow causality"), ("C08_S06_v2_wing_blast.mp4", "frames 48–107 form a tornado-like ring and frames 108–144 alter the clean-room read")], image1_requirement="accepted D1-C08-S05 wing-prep endpoint"),
	shot("D1-C08", "07", "Clean Stuffie Room endpoint with Roshan", "slow pullback", ("show Roshan at child scale with exactly one Baby Eagle and exactly four friendly bunnies", "Baby Eagle folds its wings and the four bunnies make one small grateful bounce", "hold the stable clean room endpoint"), "one wing fold and four small grateful bounces", "Roshan, one eagle, four bunnies, baskets, furniture, fixture count, and clean state", "Roshan, one eagle, and four bunnies are safe in the clean established room", "no human boy, adult cast, extra eagle, fifth bunny, dirty residue, new exit, room redesign, text, or HUD", "cheerful chirp, four small hops, and a warm cadence; no voices", [("location", "Stuffie Room geography"), ("roshan", "Roshan identity"), ("baby_eagle_standing", "standing Baby Eagle identity"), ("playroom_bunny", "bunny identity")], [("C08_S07_v1_clean_endpoint.mp4", "frames 0–144 use a human boy instead of Roshan"), ("C08_S07_v2_clean_endpoint.mp4", "frames 0–144 use a human boy instead of Roshan and do not preserve the required cast count")], image1_requirement="accepted D1-C08-S06 clean reveal endpoint"),
	shot("D1-C09", "04", "Exactly three Art Room grime cards", "locked", ("show the exact post-collection front Art Room with all four loose supply groups absent", "exactly three small lavender grime cards remain at the left counter, rectangular center desk, and right counter", "roshan points once without touching"), "Roshan points and exactly three fixed grime targets remain readable", "two shell windows, two pearl columns, chandelier, shell board, rectangular desk, two curved counters, rear shelves, and front projection", "exactly three grime cards remain visible at left, center, and right", "no fourth target, floor grime, toxic sludge, supply duplicate, cleanup, desk glow, floating objects, side wall, doorway, room rotation, text, or HUD", "faint sticky paint ambience and a concerned chord; no voices", [("location", "runtime-locked Art Room front projection"), ("roshan", "Roshan identity"), ("fixture_sheet", "fixture topology"), ("grime_desk", "grime material")], [("C09_S04_three_grime_zones.mp4", "frames 0–144 introduce the wrong child cast and weaken the fixed three-zone layout"), ("C09_S04_v1_three_grime_OFFICIAL.mp4", "frames 48–144 do not keep all three grime locations simultaneously readable")], image1_requirement="new human-approved HUD-free complete front projection of the exact post-collection runtime state"),
	shot("D1-C09", "05", "Art Room pre-contact cleaning seam", "locked", ("roshan looks across the left, center, and right grime cards", "she raises the approved magic cleaning brush toward them without touching", "she stops with a visible hand-to-tool gap and all grime present"), "Roshan makes one pre-contact raise", "front projection, all fixtures, three grime cards, Roshan anatomy, brush identity, and dirty state", "all three grime cards remain and Roshan is ready for the next cleaning shot", "no brush contact, grime removal, desk activation, reverse angle, extra limb, new fixture, text, or HUD", "small resolve chime over quiet room tone; no voices", [("location", "runtime-locked Art Room front projection"), ("roshan", "Roshan identity"), ("fixture_sheet", "fixture topology"), ("cleaning_brush", "magic cleaning brush identity")], [("C09_S05_resolve_brush.mp4", "frames 48–144 begin to read as active cleaning and fail to preserve a clean pre-contact seam")], image1_requirement="accepted D1-C09-S04 three-grime endpoint; bind the approved brush from the C10 archive as IMAGE_4"),
	shot("D1-C10", "02", "Four supplies already home", "locked", ("show all four target cards absent and each supply represented exactly once at its established station", "one restrained sparkle settles at the existing paint-table and palette stations", "hold with no loose duplicates and no travel path"), "one restrained station sparkle settles", "front projection, fixture order, storage stations, four single supply identities, counters, desk, windows, columns, and chandelier", "four supplies are home once each in the locked front room", "no flying supplies, carrying montage, transport arcs, new cupboard, relocated fixture, duplicates, side wall, room rotation, text, or HUD", "gentle placement ticks and light magic shimmer; no voices", [("location", "runtime-locked Art Room front projection"), ("fixture_sheet", "fixture topology"), ("supply_sheet", "four supply identities")], [("C10_S02_supplies_home.mp4", "frames 0–144 do not provide a reliable runtime-locked storage-station layout")], image1_requirement="accepted D1-C10-S01 clean-contact endpoint in the exact front projection"),
	shot("D1-C10", "03", "Clean Art Room reveal with readable Roshan", "small pullback", ("begin with three grime cards gone, four supplies stored once, and Roshan fully readable at runtime scale", "pull back once to reveal the complete clean front layout", "hold before desk activation"), "one restrained clean-room pullback", "rectangular desk, two counters, shelves, two windows, two columns, chandelier, Roshan identity, and blank desk state", "the complete clean room and fully readable Roshan are stable in one front projection", "no Roshan hidden under furniture, doorway, reverse view, extra supplies, completed painting, dust bunny, desk transformation, text, or HUD", "clean-room sparkle and warm reveal chord; no voices", [("location", "runtime-locked Art Room front projection"), ("roshan", "Roshan identity"), ("fixture_sheet", "fixture topology")], [("C10_S03_clean_reveal.mp4", "frames 48–144 obscure Roshan behind or beneath the center desk"), ("C10_S03_v1_clean_reveal_OFFICIAL.mp4", "frames 48–144 leave Roshan insufficiently readable at child scale")], image1_requirement="accepted D1-C10-S02 supplied-and-clean endpoint"),
	shot("D1-C10", "05", "Blank awakened desk hand-gap seam", "locked", ("show the awakened but blank rectangular center desk with Roshan smiling at frame edge", "Roshan raises one hand toward the desk without touching", "hold a clear UI-free hand gap before gameplay"), "Roshan makes one pre-touch hand raise", "blank desk, front room geometry, Roshan face/body, fixture order, and UI-free frame", "the blank desk is awake and Roshan's hand remains visibly short of contact", "no customizer UI, bubbles, pointer hand, text, completed design, attack effects, extra limb, fade, desk transformation, room drift, or HUD", "expectant sparkle and gentle cadence; no voices", [("location", "runtime-locked clean Art Room"), ("roshan", "Roshan identity"), ("fixture_sheet", "fixture and desk topology")], [("C10_S05_v1_before_play_OFFICIAL.mp4", "frames 0–144 hide too much of Roshan behind the desk and weaken the hand gap"), ("C10_S05_v1_before_play.mp4", "frames 0–144 use a less reliable room/character composition"), ("C10_S05_v2_before_play.mp4", "frames 0–144 do not preserve the exact blank-desk seam")], image1_requirement="accepted D1-C10-S04 awakened-desk endpoint"),
])


SHOTS.extend([
	shot("D1-C11", "02", "Main Hall boss-door approach", "smooth follow", ("roshan glides through the approved clean Main Hall toward the glowing boss door", "her continuous rainbow tail moves naturally while the closed door remains unchanged", "she stops and holds one hand just before the handle seam"), "Roshan makes one continuous approach and stops", "Main Hall architecture, four restored route lights, boss-door geometry, handle seam, and Roshan identity", "Roshan's hand is just before the unchanged closed boss-door seam", "no door redesign, curtain-to-wood morph, legs, adult proportions, extra cast, teleport, text, HUD, or camera drift", "soft tail movement, quiet hall tone, and an anticipatory pearl pulse; no voices", [("location", "Main Hall Screen-B layout"), ("roshan", "Roshan identity"), ("main_hall_a", "connected hall topology")], [("C11_S02_approach_boss_door.mp4", "frames 48–144 do not reliably hold the exact door geometry and pre-contact seam")], image1_requirement="accepted D1-C11-S01 endpoint with all four route lights restored"),
	shot("D1-C11", "03", "Coherent Main Hall-to-arena threshold", "gentle push-in", ("the exact boss door opens once from the accepted hall endpoint", "the approved octagonal arena appears with coherent floor, walls, depth, and entry orientation", "roshan stays at the threshold while the camera stops on the empty landing zone"), "one door opens and one coherent arena volume is revealed", "hall-door proportions, arena ring, walls, lamps, central platform, landing zone, and Roshan threshold position", "the empty arena landing zone is clearly framed beyond the open door", "no Grand Puff yet, unrelated room, giant void, dark horror, geography jump, arena redesign, Roshan entering center, text, or HUD", "soft pearl-door movement, small playful low rumble, and clean hall ambience; no voices", [("main_hall_location", "Main Hall door-side layout"), ("arena_location", "approved arena geography"), ("roshan", "Roshan identity")], [("C11_S03_door_opens_arena.mp4", "frames 48–144 land in a pearl-hall-like alternate space rather than the approved arena"), ("C11_S03_v1_door_open_arena.mp4", "frames 0–144 do not preserve a coherent hall-door-to-arena orientation")], image1_requirement="accepted D1-C11-S02 closed-door endpoint"),
	shot("D1-C11", "04", "Grand Puff lands in the fixed arena", "locked", ("Grand Puff makes one soft landing squash in the approved empty arena", "he settles upright with three tiers, symmetrical spiral ears, pearl paws, and exactly two small teeth", "one lavender four-point forehead sparkle gives a playful vulnerability pulse"), "Grand Puff lands, squashes once, and settles", "arena topology, landing zone, Roshan's safe edge position, Grand Puff tiers, ears, paws, face, and teeth", "Grand Puff is upright, cute, smiling, and centered in the fixed arena", "no pearl hall, smoke body, attack, sharp teeth, injury, defeat, title, text, HUD, or arena morph", "soft puffy landing, comic bounce, and a bright tell chime; no voices", [("arena_location", "approved arena geography"), ("grand_puff", "Grand Puff identity"), ("roshan", "Roshan identity")], [("C11_grand_puff_reveal.mp4", "frames 0–144 use an unstable arena/hall context and do not fully lock Grand Puff topology")], image1_requirement="accepted D1-C11-S03 empty-arena landing-zone endpoint"),
	shot("D1-C12", "05", "Post-friendship arena vignette", "locked", ("Grand Puff sits upright with the newly friendly small rainbow bunny in the accepted post-friendship arena", "Grand Puff gives one soft laugh and squash while the bunny makes one tiny grateful bounce", "both settle as separate friendly bodies"), "one soft Grand Puff laugh/squash and one tiny bunny bounce", "arena topology, Grand Puff identity, rainbow bunny identity, positions, floor contacts, and friendly state", "Grand Puff rests upright smiling with exactly two teeth while the separate rainbow bunny settles beside him", "no Main Hall, defeat, injury, attack, smoke, boss UI, invented cleanup, morphing, text, or HUD", "soft puffy chuckle, tiny hop, and warm room cadence; no voices", [("arena_endpoint", "accepted D1-C13-S05 endpoint"), ("grand_puff", "Grand Puff identity"), ("rainbow_bunny_missing", "approved rainbow bunny identity")], [("C12_S05_v1_grand_puff_friend.mp4", "frames 0–144 use the wrong Main Hall-like location and do not inherit the arena friendship state"), ("C12_S05_v2_grand_puff_friend.mp4", "frames 0–144 fail arena and new-friend continuity")], image1_requirement="accepted final arena state from D1-C13-S05"),
	shot("D1-C13", "01", "Roshan's final cleaning pass", "locked", ("Roshan holds the approved magic cleaning brush and makes one gentle pass across Grand Puff's front and near floor", "one localized dusty shell band becomes clean while Grand Puff compresses playfully without damage", "Roshan and Grand Puff settle as separate bodies"), "one physically held brush pass makes one localized clean patch", "octagonal arena, central platform, walls, lamps, Grand Puff topology, Roshan identity, and unaffected dust bands", "Roshan holds the brush at frame edge and Grand Puff rests centered with one localized clean patch", "no Daddy, Rumi, Baby Eagle, rainbow bunny, morphing, clone, merged body, extra limb, topology change, cropped character, attack, defeat, text, or HUD", "soft brush pass and tiny sparkle; no voices", [("arena_location", "approved arena geography"), ("roshan", "Roshan identity"), ("grand_puff", "Grand Puff identity"), ("cleaning_brush", "magic cleaning brush identity")], [("C13_S01_v1_roshan_cleanup.mp4", "frames 0–144 are 1264×720 and drift arena/action continuity"), ("C13_S01_v2_roshan_cleanup.mp4", "useful action reference, but frames 48–144 still need exact arena, brush contact, and native 1280×720 reconstruction")], duration=4, image1_requirement="human-approved clean HUD-free FRIENDS transition endpoint in the exact arena"),
	shot("D1-C13", "02", "Daddy's distinct broad sweep", "locked", ("Daddy stands at safe contact distance and makes one broad broom-or-cloth sweep around Grand Puff's base", "loose dust gathers into one controlled lower curl band without changing Grand Puff", "Daddy returns to calm neutral and both settle"), "one broad Daddy sweep gathers loose dust", "arena, central platform, Grand Puff topology, Daddy crown/glasses/costume/tail, and unaffected clean patch", "Daddy and Grand Puff rest separately with loose dust gathered at the base", "no Roshan, Rumi, Baby Eagle, rainbow bunny, morphing, cloned bodies, merged tails, extra limbs, arena change, attack, defeat, text, or HUD", "gentle sweep, cape swish, and pearl chime; no voices", [("arena_location", "approved arena geography"), ("daddy", "Daddy identity"), ("grand_puff", "Grand Puff identity")], [("C13_S02_v1_daddy_sweep.mp4", "frames 0–144 are 1264×720 and mix action/identity reads"), ("C13_S02_v2_daddy_sweep.mp4", "useful action reference, but frames 48–144 need stable Daddy identity, arena, and native 1280×720")], duration=4, image1_requirement="accepted D1-C13-S01 endpoint"),
	shot("D1-C13", "03", "Baby Eagle's safe wing lift", "locked", ("exactly one Baby Eagle plants both feet and opens both wings", "one symmetrical soft wing blast lifts only residual dust toward the arena perimeter", "the eagle folds its wings and settles without moving Grand Puff"), "one safe symmetrical wing blast lifts dust", "arena ring, central platform, Grand Puff, one eagle, floor contacts, and the final dusty shell", "one Baby Eagle rests with folded wings and the final dusty shell remains isolated", "no Roshan, Daddy, Rumi, rainbow bunny, duplicate eagle, displaced character, tornado, morphing, clone, extra limb, arena change, attack, defeat, text, or HUD", "controlled wing whoosh and light dust lift; no voices", [("arena_location", "approved arena geography"), ("baby_eagle_standing", "standing Baby Eagle identity"), ("grand_puff", "Grand Puff identity")], [("C13_S03_v1_eagle_lift.mp4", "frames 48–144 collapse Grand Puff into a ring/bowl-like form and are 1264×720"), ("C13_S03_v2_eagle_lift.mp4", "useful motion reference, but frames 0–144 need exact eagle count, boss topology, and native 1280×720")], duration=4, image1_requirement="accepted D1-C13-S02 endpoint"),
	shot("D1-C13", "04", "Rumi's contained rinse", "locked", ("Rumi sends one low contained violet-and-rainbow water ribbon around Grand Puff's base", "the rinse clears the final grime without creating a basin or changing the arena", "Rumi and Grand Puff settle separately around one small prismatic cradle"), "one contained water-ribbon rinse clears the final grime", "arena ring, platform, lamps, Grand Puff topology, Rumi adult identity, braid, clothes, continuous tail, and prismatic cradle", "Grand Puff is fully clean and friendly beside one small prismatic cradle; no rainbow bunny is visible yet", "no Roshan, Daddy, Baby Eagle, Mermaid Pool conversion, basin, morphing, merged tails, extra limbs, arena change, early bunny, attack, defeat, text, or HUD", "gentle water shimmer and violet hum; no voices", [("arena_location", "approved arena geography"), ("rumi", "Rumi identity"), ("grand_puff", "Grand Puff identity")], [("C13_S04_v1_rumi_rinse.mp4", "strongest motion reference, but frames 0–144 are 1264×720 and need fixed arena/identity reconstruction"), ("C13_S04_v2_rumi_rinse.mp4", "frames 48–144 drift Rumi/arena relationships and are 1264×720")], duration=4, image1_requirement="accepted D1-C13-S03 endpoint"),
	shot("D1-C13", "05", "Separate rainbow dust bunny emerges", "locked", ("one small contained lavender-prismatic puff opens from the established cradle", "exactly one separate rainbow dust bunny emerges while Grand Puff remains unchanged", "the bunny settles beside Grand Puff with a cloud body, spiral ears, readable face, and curl-to-curl pastel colors"), "one separate rainbow bunny emerges and settles", "arena, platform, lamps, clean Grand Puff topology, prismatic cradle, exact two-character count, and floor contacts", "a clean unchanged Grand Puff and exactly one calm separate rainbow dust bunny rest together", "no Roshan, Daddy, Rumi, Baby Eagle, Grand Puff morph, unapproved rainbow identity, second bunny, smoke monster, clone, merged body, extra limb, arena change, attack, defeat, text, or HUD", "soft poof, warm rainbow chime, and a friendly two-note cadence; no voices", [("arena_location", "approved arena geography"), ("grand_puff", "Grand Puff identity"), ("rainbow_bunny_missing", "dedicated human-approved rainbow bunny identity")], [("C13_S05_v1_rainbow_friend.mp4", "frames 0–144 are 1264×720 and do not preserve a reliable separate emergence identity"), ("C13_S05_v2_rainbow_friend.mp4", "useful action reference only; frames 48–144 still mix emergence, identity, and Grand Puff state at 1264×720")], duration=4, image1_requirement="accepted D1-C13-S04 clean-Grand-Puff/prismatic-cradle endpoint; generation remains blocked until the rainbow bunny identity is human approved"),
])


def release_audit(
	shot_id: str,
	verdict: str,
	clips: list[str],
	weak_frames: str,
	finding: str,
	next_action: str,
	preferred: str | None = None,
	replacement_shot: str | None = None,
) -> dict:
	return {
		"shot_id": shot_id,
		"verdict": verdict,
		"clips": clips,
		"preferred_clip": preferred,
		"weak_frames": weak_frames,
		"finding": finding,
		"next_action": next_action,
		"replacement_shot": replacement_shot,
	}


# The 40 release files cover 36 unique cards. These judgments deliberately use
# a loose rough-cut bar: an accepted clip may remain an editorial/motion
# reference even though it is not a delivery frame. Event and topology errors
# are never accepted merely because the render is attractive.
RELEASE_AUDIT = [
	release_audit("D1-C01-S02", "REGENERATE", ["C01_S02_v1_dock_handoffer_REGEN.mp4"], "000–144", "Daddy is already outside and offering at frame 0; the required plane exit, turn, and Roshan-from-doorway handoff never occur.", "Rebuild Daddy exit → offer → Roshan hand contact → stable two-character endpoint."),
	release_audit("D1-C01-S03", "ACCEPT_MOTION_REFERENCE", ["C01_S03_v1_handinhand_castle_REGEN.mp4"], "none blocking", "The paired travel, identities, tails, castle approach, and closed-door endpoint remain coherent; loss of the dock during frames 000–024 is an acceptable cut.", "Retain this release clip for rough assembly only.", preferred="C01_S03_v1_handinhand_castle_REGEN.mp4"),
	release_audit("D1-C02-S03", "REGENERATE", ["C02_S03_v1_dirty_hall_evidence_REGEN.mp4"], "000–144", "The broad hall tableau replaces the required low evidence close-up, invents multiple bunny bodies and readable EVIDENCE labels, and lets full-body Daddy/Roshan movement compete with the evidence.", "Lock Screen A low; show one integrated grime patch, one dust trace, one harmless scrap, then one pointing hand with no text."),
	release_audit("D1-C03-S02", "REGENERATE", ["C03_S02_v1_dirty_bathroom_threshold_REGEN.mp4", "C03_S02_v1_threshold_cross_REGEN.mp4"], "000–144 both variants", "Neither variant establishes the doorway. One starts mid-room and ends seated by the sink; the other begins inside the bathtub and crosses the tub instead of the threshold.", "Start with the entrance readable; cross fully inside, look tub-to-sink, and preserve the single-tub orientation."),
	release_audit("D1-C03-S03", "REGENERATE", ["C03_S03_v1_swimming_bunny_REGEN.mp4"], "000–144", "The swimmer is coherent, but Roshan is a black silhouette/substitute and the bunny mostly holds instead of paddling visibly.", "Use approved Roshan at frame edge and one weak-but-safe paddling swimmer in murky water."),
	release_audit("D1-C03-S04", "REGENERATE", ["C03_S04_v1_precontact_tools_REGEN.mp4"], "000–144 swimmer absent; 060–144 premature contact", "The required swimmer disappears and Roshan advances into scrub-brush contact rather than stopping at the pre-contact seam.", "Keep swimmer, tub, sink, tools, and grime; stop Roshan's hand visibly before the nearest tool."),
	release_audit("D1-C05-S04", "REGENERATE", ["C05_S04_v1_blocked_rainbow_source_REGEN.mp4"], "000–144", "A clean empty pool becomes a bright rainbow doorway. The exact top waterfall source, dull blockage, olive-brown sludge, leaf, and wrapper are absent.", "Show the fixed top source blocked and unchanged; no glow or flow."),
	release_audit("D1-C05-S05", "REGENERATE", ["C05_S05_v1_sick_seahorse_plug_REGEN.mp4"], "000–144", "The mouth plug is readable, but the pool is already clean and Roshan is full-body from frame 0 instead of entering only at the edge of a dirty-state close-up.", "Restore dirty algae/trash grade, right-center seahorse scale, lodged plug, and edge-only Roshan reaction."),
	release_audit("D1-C06-S03", "REGENERATE", ["C06_S03_v1_rainbow_waterfall_restart_REGEN.mp4"], "000–047 missing blocked start; 048–144 wrong clearing", "The waterfall starts clean; later debris becomes a central raised dark mass and the flow retracts instead of clearing from the top source downward.", "Begin blocked, ignite at the top, drive debris down the channel, and stop at the lower lip."),
	release_audit("D1-C06-S04", "ACCEPT_MOTION_REFERENCE", ["C06_S04_v1_both_sources_pool_REGEN.mp4"], "none blocking", "Both fixed clean sources visibly enter the same giant pool and the pullback resolves the shared geometry.", "Retain this release clip for rough assembly only.", preferred="C06_S04_v1_both_sources_pool_REGEN.mp4"),
	release_audit("D1-C06-S05", "REGENERATE", ["C06_S05_v1_purification_fronts_REGEN.mp4"], "000–144", "The pool begins clean; white V-shaped streaks replace two fronts displacing algae through murky water.", "Start dirty, advance two distinct fronts from the fixed sources, displace algae, and join once at center."),
	release_audit("D1-C06-S06", "ACCEPT_MOTION_REFERENCE", ["C06_S06_v1_violet_prelude_REGEN.mp4"], "none blocking", "The clean giant pool, both fixtures, and localized violet center glow are coherent without revealing Rumi early.", "Retain this release clip for rough assembly only.", preferred="C06_S06_v1_violet_prelude_REGEN.mp4"),
	release_audit("D1-C06-S08", "REGENERATE", ["C06_S08_v1_rumi_invitation_REGEN.mp4"], "104–144", "Rumi's thanks and open-arm invitation work through frame 103, but Roshan then approaches and starts the hug before the dedicated hug shot.", "Regenerate the full shot so Rumi holds open arms and Roshan remains separate through frame 144."),
	release_audit("D1-C06-S09", "ACCEPT_MOTION_REFERENCE", ["C06_S09_v1_hug_complete_REGEN.mp4"], "none blocking", "Approach, arm contact, faces, distinct torsos, two tails, pool fixtures, and the final embrace remain coherent.", "Retain this release clip for rough assembly only.", preferred="C06_S09_v1_hug_complete_REGEN.mp4"),
	release_audit("D1-C07-S04", "OMIT_SUPERSEDED_EVENT", ["C07_S04_v1_swinging_bunny_REGEN.mp4"], "000–144; detachment 108–144", "No swinging-bunny event exists in gameplay, and the rendered bunny loses its support before landing on the floor.", "Remove this shot from the corrected cut; do not regenerate the invented event."),
	release_audit("D1-C07-S05", "OMIT_SUPERSEDED_EVENT", ["C07_S05_v1_partial_wing_trail_REGEN.mp4"], "000–144; full reveal 048–144", "Gameplay presents one visible Baby Eagle held by two pin bunnies; it does not hide the bird behind a partial-wing trail.", "Remove this shot from the corrected cut; do not regenerate the invented event."),
	release_audit("D1-C07-S06", "REGENERATE", ["C07_S06_v1_pinned_baby_eagle_REGEN.mp4"], "000–144", "One Eagle is present, but neither of the two required rescue-pin bunnies is visible and the bird becomes free/upright before player action.", "Reveal exactly one Baby Eagle visibly held by exactly two distinct pin bunnies; no release yet."),
	release_audit("D1-C08-S02", "REPLACE_WITH_GAME_EVENT", ["C08_S02_v1_left_basket_ears_REGEN.mp4"], "000–144", "Basket warnings do not occur in gameplay; the bunny body is already outside the basket.", "Replace with corrected C08-S01: Roshan approaches the exact two-pin rescue state.", replacement_shot="D1-C08-S01"),
	release_audit("D1-C08-S03", "REPLACE_WITH_GAME_EVENT", ["C08_S03_v1_right_basket_ears_REGEN.mp4"], "000–144", "The opposite-basket warning is also invented and exposes a full bunny rather than an ears-only cue.", "Replace with corrected C08-S02: Roshan clears the left rescue pin after physical contact.", replacement_shot="D1-C08-S02"),
	release_audit("D1-C08-S04", "REPLACE_WITH_GAME_EVENT", ["C08_S04_v1_four_bunnies_emerge_REGEN.mp4"], "000–144; count failure 048–144", "The game has two rescue pins, not four emerging basket bunnies; the rendered count also grows ambiguous beyond four.", "Replace with corrected C08-S03: reframe the still-pinned right bunny after the left pin clears.", replacement_shot="D1-C08-S03"),
	release_audit("D1-C08-S06", "REPLACE_WITH_GAME_EVENT", ["C08_S06_v1_wing_blast_clean_REGEN.mp4"], "000–144", "Baby Eagle never performs a wing-blast cleanup. Gameplay completes when Roshan clears the second pin.", "Replace with corrected C08-S04: Roshan clears the right pin and the room resolves from that contact.", replacement_shot="D1-C08-S04"),
	release_audit("D1-C08-S07", "REPLACE_WITH_GAME_EVENT", ["C08_S07_v1_clean_endpoint_REGEN.mp4"], "000–144; side-wall drift 048–144", "The one-Eagle/four-bunny endpoint is not a game state and the room projection drifts into invented side-wall geometry.", "Replace with corrected C08-S05: Baby Eagle thanks Roshan, rises, and departs from the clean room before the picker UI.", replacement_shot="D1-C08-S05"),
	release_audit("D1-C09-S04", "REGENERATE", ["C09_S04_v1_three_grime_cards_REGEN.mp4"], "048–144", "The Art Room front concept is close, but the left/right zones multiply into upright card groups instead of exactly one small lavender grime card at each of three fixed targets.", "Lock the exact front plate and show one card each at left counter, center desk, and right counter; Roshan points once."),
	release_audit("D1-C09-S05", "ACCEPT_MOTION_REFERENCE", ["C09_S05_v1_precontact_brush_REGEN.mp4"], "none blocking", "The three-zone pre-contact beat, brush separation, and straight-on fixture order remain coherent.", "Retain this release clip for rough assembly only.", preferred="C09_S05_v1_precontact_brush_REGEN.mp4"),
	release_audit("D1-C10-S02", "REGENERATE", ["C10_S02_v1_four_supplies_home_REGEN.mp4"], "000–144", "Supplies begin on/near the center desk and materialize at the right during the clip; ribbon and fixture topology also change.", "Place all four supplies home once at frame 0 and allow only localized station sparkle."),
	release_audit("D1-C10-S03", "REGENERATE", ["C10_S03_v1_clean_art_room_REGEN.mp4"], "000–144", "The opening crop omits the complete layout, the pullback is far greater than ten percent, and Roshan becomes too small for a child-readable endpoint.", "Start on the complete exact front projection; limit pullback to ten percent and keep Roshan readable."),
	release_audit("D1-C10-S05", "ACCEPT_MOTION_REFERENCE", ["C10_S05_v1_blank_desk_handgap_REGEN.mp4"], "none blocking", "The blank rectangular desk, front fixture order, raised hand, and visible hand gap remain stable.", "Retain this release clip for rough assembly only.", preferred="C10_S05_v1_blank_desk_handgap_REGEN.mp4"),
	release_audit("D1-C11-S02", "ACCEPT_MOTION_REFERENCE", ["C11_S02_v1_boss_door_approach_REGEN.mp4"], "minor 132–144", "Main Hall geometry, Roshan, closed door, and approach are coherent; only the final hand reaches the handle instead of stopping just before it.", "Retain for rough assembly; require a clean pre-contact endpoint for final delivery.", preferred="C11_S02_v1_boss_door_approach_REGEN.mp4"),
	release_audit("D1-C11-S03", "ACCEPT_MOTION_REFERENCE", ["C11_S03_v1_door_open_arena_REGEN.mp4"], "none blocking", "The door opens into the octagonal arena, Roshan stays at threshold, and the landing zone remains empty; exact predecessor-frame inheritance is unproven.", "Retain for rough assembly; audit the final seam independently.", preferred="C11_S03_v1_door_open_arena_REGEN.mp4"),
	release_audit("D1-C11-S04", "REGENERATE", ["C11_S04_v1_grand_puff_lands_REGEN.mp4"], "006–071 impact/topology; 066–144 expression", "A dark crater, oversized cloud, and pancake-flat squash destabilize Grand Puff; the recovered face remains menacing and the vulnerability sparkle does not read.", "Use a soft vertical landing, at most ten-percent squash, full three-tier recovery by 2.5 seconds, cute two-teeth face, and one four-point sparkle pulse."),
	release_audit("D1-C12-S05", "ACCEPT_MOTION_REFERENCE", ["C12_S05_v1_post_friendship_vignette_REGEN.mp4"], "minor 108–144", "Arena topology and the one-Puff/one-rainbow-bunny count are coherent; the ending closes Grand Puff's mouth and does not prove exact C13 inheritance.", "Retain for rough assembly; final delivery still needs the approved C13 endpoint and two-teeth smile.", preferred="C12_S05_v1_post_friendship_vignette_REGEN.mp4"),
	release_audit("D1-C13-S01", "ACCEPT_MOTION_REFERENCE", ["C13_S01_v1_roshan_cleaning_pass_REGEN.mp4"], "minor causal gap 000–031", "Roshan's brush pass and identities are useful, though the initial residual dust is faint.", "Retain after locking the corrected post-third-hit, pre-implosion boundary.", preferred="C13_S01_v1_roshan_cleaning_pass_REGEN.mp4"),
	release_audit("D1-C13-S02", "ACCEPT_MOTION_REFERENCE", ["C13_S02_v1_daddy_broad_sweep_REGEN.mp4", "C13_S02_v2_daddy_broad_sweep_REGEN.mp4"], "minor causal gap 000–031 both", "Both lack a strongly dirty opening shell; v2 has the cleaner composition and sustained Daddy sweep.", "Retain v2; reject v1 as the less stable duplicate.", preferred="C13_S02_v2_daddy_broad_sweep_REGEN.mp4"),
	release_audit("D1-C13-S03", "REGENERATE", ["C13_S03_v1_baby_eagle_wing_blast_REGEN.mp4", "C13_S03_v2_baby_eagle_wing_blast_REGEN.mp4"], "v1 048–144; v2 000–144", "V1's cloud hides/collapses Grand Puff into a bowl; v2 preserves identity but supplies almost no visible dust lift.", "One controlled wingbeat lifts only a thin dust veil while Grand Puff remains fully visible and three-tiered."),
	release_audit("D1-C13-S04", "ACCEPT_MOTION_REFERENCE", ["C13_S04_v1_rumi_contained_rinse_REGEN.mp4", "C13_S04_v2_rumi_contained_rinse_REGEN.mp4"], "v1 minor 032–144; v2 blocking 108–144", "V1 provides the usable rinse despite a broad ribbon; v2 makes Grand Puff collapse/disappear into pearls.", "Retain v1 and reject v2.", preferred="C13_S04_v1_rumi_contained_rinse_REGEN.mp4"),
	release_audit("D1-C13-S05", "REGENERATE", ["C13_S05_v1_rainbow_bunny_emerges_REGEN.mp4"], "000–047 cradle; 048–071 occlusion; identity 000–144", "The floor cradle becomes a tall canopy/chair, multicolor smoke obscures emergence, and the bunny remains an unapproved identity stand-in.", "Use a floor-level cradle below ten percent of Grand Puff height and reveal one approved bunny without smoke or occlusion."),
]


RELEASE_EVIDENCE = {
	row["replacement_shot"] or row["shot_id"]: [
		(filename, f"release frames {row['weak_frames']}: {row['finding']}")
		for filename in row["clips"]
	]
	for row in RELEASE_AUDIT
	if row["verdict"] in {"REGENERATE", "REPLACE_WITH_GAME_EVENT"}
}


# Remove the two discovery beats and the basket/four-bunny/wing-blast chain
# because they are not events in the current game. C08 is rebuilt as the exact
# two-pin rescue and Baby Eagle departure that the runtime performs.
ACTIVE_SHOT_IDS = {
	"D1-C01-S02", "D1-C02-S03",
	"D1-C03-S02", "D1-C03-S03", "D1-C03-S04",
	"D1-C05-S04", "D1-C05-S05",
	"D1-C06-S03", "D1-C06-S05", "D1-C06-S08",
	"D1-C07-S06",
	"D1-C09-S04",
	"D1-C10-S02", "D1-C10-S03",
	"D1-C11-S04",
	"D1-C13-S03", "D1-C13-S05",
}
SHOTS = [item for item in SHOTS if item["shot_id"] in ACTIVE_SHOT_IDS]

for item in SHOTS:
	item["evidence"] = RELEASE_EVIDENCE[item["shot_id"]]
	if item["shot_id"] == "D1-C05-S05":
		item["conditional"] = False

for item in SHOTS:
	if item["shot_id"] == "D1-C07-S06":
		item.update({
			"title": "One Baby Eagle held by exactly two rescue pins",
			"camera": "locked",
			"timeline": (
				"show the exact dirty Stuffie Room floor position with one Baby Eagle fully readable beneath soft clutter",
				"show exactly two separate lavender rescue-pin bunnies visibly holding the left and right sides while Roshan enters the edge",
				"Roshan makes concerned eye contact and stops before either pin is touched",
			),
			"must_move": "Roshan makes one edge entrance and concerned look; the pinned trio only breathes",
			"must_not_move": "Baby Eagle position, two pin contacts, dirty room, clutter, floor landmarks, bodies, and cast count",
			"end": "one unharmed Baby Eagle remains visibly held by exactly two pin bunnies while Roshan is ready to help",
			"negatives": "no missing pin, third bunny, basket, swing, partial-wing trail, release, cleanup, bird rise, duplicate body, injury, text, HUD, or camera drift",
			"bindings": [("location", "dirty Stuffie Room geography"), ("roshan", "Roshan identity"), ("baby_eagle_pinned", "pinned Baby Eagle identity"), ("playroom_bunny", "two rescue-pin identities")],
			"image1_requirement": "accepted D1-C07-S02 dirty-room entry endpoint, with the stale swinging/partial-wing S04–S05 beats omitted",
		})
	elif item["shot_id"] == "D1-C10-S03":
		item.update({
			"camera": "front-axis pullback no greater than ten percent",
			"timeline": (
				"begin on the complete exact straight-on Art Room projection with Roshan readable at runtime child scale",
				"pull back no more than ten percent while every required landmark stays inside frame",
				"hold the clean room, four supplies stored once, all grime absent, and blank rectangular desk before activation",
			),
			"negatives": item["negatives"] + ", no tight opening crop, pullback beyond ten percent, lost landmark, tiny Roshan, or side perspective",
		})
	elif item["shot_id"] == "D1-C11-S04":
		item.update({
			"timeline": (
				"Grand Puff drops softly into the exact empty central ring with no crater, smoke cloud, or dark impact hole",
				"his full three-tier body compresses vertically by no more than ten percent, then recovers fully upright by 2.5 seconds",
				"he holds a cute neutral face with plum eyes, coral blush, exactly two teeth, and one lavender four-point sparkle pulse",
			),
			"must_move": "one soft vertical landing, one limited squash-and-recovery, and one vulnerability sparkle pulse",
			"end": "Grand Puff is fully upright, three-tiered, cute, smiling with two teeth, and centered in the unchanged arena",
			"negatives": "no crater, dark hole, opaque cloud, pancake flattening, top crop, scale growth, missing tier, menacing brow, angry face, attack, arena morph, text, or HUD",
		})
	elif item["shot_id"] == "D1-C13-S03":
		item.update({
			"timeline": (
				"exactly one Baby Eagle plants both feet and opens both wings while Grand Puff remains fully visible",
				"one symmetrical controlled wingbeat lifts only a thin twenty-to-thirty-percent dust veil toward the arena perimeter",
				"the eagle folds both wings; Grand Puff stays upright, unobscured, and three-tiered with the final dirty shell readable",
			),
			"must_move": "one safe symmetrical wingbeat lifts a thin dust veil without moving Grand Puff",
			"negatives": "no Roshan, Daddy, Rumi, rainbow bunny, duplicate eagle, wingbeat-free hold, opaque dust cloud, tornado, bowl or ring collapse, displaced Grand Puff, morph, extra limb, arena change, attack, defeat, text, or HUD",
		})
	elif item["shot_id"] == "D1-C13-S05":
		item.update({
			"timeline": (
				"one tiny floor-level prismatic cradle below ten percent of Grand Puff's height opens without growing into furniture",
				"exactly one approved rainbow dust bunny rises visibly from the cradle with no smoke, occlusion, morph, or teleport",
				"the bunny settles beside the unchanged clean three-tier Grand Puff and both hold as separate friendly bodies",
			),
			"must_move": "one approved rainbow bunny emerges visibly from one tiny floor cradle and settles",
			"negatives": "no Roshan, Daddy, Rumi, Baby Eagle, tall canopy, chair, cart, arch, smoke cloud, occluded reveal, Grand Puff morph, second bunny, unapproved identity, merged body, arena change, attack, text, or HUD",
		})

SHOTS.extend([
	shot("D1-C08", "01", "Roshan approaches the two-pin rescue", "subtle push-in", (
		"inherit the exact C07-S06 state with one Baby Eagle held by two distinct pin bunnies",
		"Roshan moves toward the left pin while the right pin and Baby Eagle remain fixed",
		"her hand stops in a visible gap before the left pin",
	), "Roshan makes one careful approach toward the left pin", "one Baby Eagle, both pin bunnies, pin contacts, clutter, room topology, and dirty state", "Roshan is poised before the left pin; both pins still hold the Eagle", "no basket, swing, four-bunny group, touch, pop, release, cleanup, wing blast, text, HUD, or extra cast", "soft tail movement, tiny bunny rustle, and a hopeful chirp; no voices", [("location", "dirty Stuffie Room geography"), ("roshan", "Roshan identity"), ("baby_eagle_pinned", "pinned Baby Eagle identity"), ("playroom_bunny", "two rescue-pin identities")], RELEASE_EVIDENCE["D1-C08-S01"], image1_requirement="accepted D1-C07-S06 exact two-pin endpoint"),
	shot("D1-C08", "02", "Roshan clears the left rescue pin", "locked", (
		"Roshan's hand completes one physical contact with the left pin bunny",
		"only the left bunny expands slightly and pops into a small lavender sparkle burst",
		"the right pin remains attached and Baby Eagle remains safely held on that side",
	), "one left rescue pin pops after Roshan's contact", "right pin, Baby Eagle, room, clutter, Roshan anatomy, and dirty state", "the left pin is gone; the right pin still visibly holds one Baby Eagle", "no right-pin pop, simultaneous pair, basket, four bunnies, eagle release, room cleanup, wing blast, text, HUD, or pearl reward", "one soft boing, small sparkle pop, and hopeful chirp; no voices", [("location", "dirty Stuffie Room geography"), ("roshan", "Roshan identity"), ("baby_eagle_pinned", "pinned Baby Eagle identity"), ("playroom_bunny", "rescue-pin identity")], RELEASE_EVIDENCE["D1-C08-S02"], image1_requirement="accepted D1-C08-S01 pre-contact endpoint"),
	shot("D1-C08", "03", "Roshan reframes the remaining right pin", "short lateral", (
		"begin with the left pin absent and the right pin still attached to Baby Eagle",
		"Roshan shifts once across the fixed floor toward the right pin",
		"she stops with her hand visibly short of the remaining bunny",
	), "Roshan makes one short move toward the right pin", "right-pin contact, Baby Eagle, absent left pin, room, clutter, and dirty state", "one right pin remains; Roshan is poised before contact and Baby Eagle is still safe", "no reappearing left pin, basket, extra bunny, pop, release, cleanup, wing blast, text, HUD, or camera rotation", "soft tail movement and one guiding sparkle; no voices", [("location", "dirty Stuffie Room geography"), ("roshan", "Roshan identity"), ("baby_eagle_pinned", "pinned Baby Eagle identity"), ("playroom_bunny", "remaining right-pin identity")], RELEASE_EVIDENCE["D1-C08-S03"], image1_requirement="accepted D1-C08-S02 one-pin endpoint"),
	shot("D1-C08", "04", "Roshan clears the right pin and completes the room", "locked", (
		"Roshan's hand completes one physical contact with the remaining right pin bunny",
		"only that bunny pops into a small sparkle burst and Baby Eagle becomes free",
		"the exact room resolves from dirty to clean while Baby Eagle stays in the same floor position",
	), "one right-pin contact causes one pop, the rescue release, and the game-authored clean resolve", "Roshan, Baby Eagle identity, fixture positions, floor geography, absent left pin, and camera", "both pins are gone, the room is clean, and Baby Eagle is free but has not departed", "no basket, four-bunny emergence, wing blast, tornado, magic before contact, duplicate eagle, relocation, text, HUD, or picker UI", "one soft boing, clean-room chime, and relieved chirp; no voices", [("location", "Stuffie Room dirty-to-clean geography"), ("roshan", "Roshan identity"), ("baby_eagle_pinned", "Baby Eagle identity"), ("playroom_bunny", "right rescue-pin identity")], RELEASE_EVIDENCE["D1-C08-S04"], image1_requirement="accepted D1-C08-S03 right-pin pre-contact endpoint"),
	shot("D1-C08", "05", "Baby Eagle thanks Roshan and departs", "subtle upward follow", (
		"begin in the exact clean post-rescue room with one free Baby Eagle beside Roshan",
		"Baby Eagle gives one happy chirp, rises slightly, and begins a gentle upward departure",
		"the bird fades only after clearing Roshan while the clean room holds for the companion-picker seam",
	), "one Baby Eagle rises and departs after the rescue", "clean room, Roshan, fixture positions, bird identity, empty pin locations, and UI-free frame", "Roshan remains in the clean room after Baby Eagle exits; the next event may open the picker UI", "no four bunnies, wing-blast cleanup, new companion choice, visible picker UI, duplicate bird, room drift, basket action, text, or HUD", "happy chirp, light feather lift, and warm resolution; no voices", [("location", "clean Stuffie Room geography"), ("roshan", "Roshan identity"), ("baby_eagle_standing", "freed Baby Eagle identity")], RELEASE_EVIDENCE["D1-C08-S05"], image1_requirement="accepted D1-C08-S04 clean post-rescue endpoint"),
])

TITLES["D1-C07"] = "Stuffie Room — Dirty Discovery and Two-Pin Reveal"
TITLES["D1-C08"] = "Stuffie Room — Two-Pin Rescue and Baby Eagle Departure"
KEEP["D1-C07"] = ["C07_S01_v2_empty_dirty_stuffie.mp4", "C07_S02_v2_roshan_enters.mp4"]
KEEP["D1-C08"] = []


ALIASES = {
	"location": (None, "approved_location_geography_authority"),
	"roshan": (None, "approved_roshan_identity_authority"),
	"daddy": (None, "approved_daddy_identity_authority"),
	"rumi": (None, "approved_rumi_identity_authority"),
	"swimming_bunny": (None, "approved_swimming_bunny_identity_authority"),
	"baby_eagle_pinned": ("D1-C07", "approved_baby_eagle_pinned_identity_authority"),
	"baby_eagle_standing": (None, "approved_baby_eagle_standing_identity_authority"),
	"playroom_bunny": (None, "approved_playroom_bunny_identity_authority"),
	"grand_puff": (None, "approved_grand_puff_identity_authority"),
	"plane": (None, "06_AIRPLANE_EXACT.png"),
	"castle": (None, "pearl_castle_exterior_turnaround_v2.png"),
	"main_hall_a": (None, "main_hall_screen_a_room_led_master.png"),
	"main_hall_location": ("D1-C11", "approved_location_geography_authority"),
	"arena_location": ("D1-C13", "approved_location_geography_authority"),
	"tub_grime": (None, "target_tub_grime_v1.png"),
	"cleanup_basket": (None, "cleanup_basket.png"),
	"pool_trash": (None, "pool_algae_trash.png"),
	"waterfall_clog": (None, "waterfall_clogged_turgid.png"),
	"seahorse": (None, "seahorse_sick.png"),
	"seahorse_plug": (None, "seahorse_mouth_trash.png"),
	"waterfall_rest": (None, "mermaid_pool_waterfall_rest.png"),
	"seahorse_rest": (None, "mermaid_pool_seahorse_fountain_rest.png"),
	"play_tent": (None, "room_playroom_item_play_tent.png"),
	"stuffie_nook": (None, "room_playroom_item_stuffie_nook.png"),
	"fixture_sheet": (None, "ART_ROOM_FIXTURE_IDENTITY_SHEET.png"),
	"supply_sheet": ("D1-C09", "FOUR_LOOSE_SUPPLY_IDENTITY_SHEET.png"),
	"grime_desk": (None, "grime_desk.png"),
	"cleaning_brush": ("D1-C10", "magic_cleaning_brush.png"),
}


def _sha256_text(value: str) -> str:
	return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _clip_url(filename: str) -> str:
	return f"https://github.com/{REPO}/blob/{CLIP_COMMIT}/clips/{filename}"


def _release_clip_url(filename: str) -> str:
	return f"https://github.com/{REPO}/releases/download/{RELEASE_TAG}/{filename}"


def _audit_rows(movie: str) -> list[dict]:
	return [row for row in RELEASE_AUDIT if row["shot_id"].startswith(movie + "-S")]


def _source_readme_url(movie: str) -> str:
	packet = PACKETS[movie]
	return f"https://github.com/{REPO}/tree/{SOURCE_COMMIT}/assets_src/cinematics/{packet}"


def _assets(movie: str) -> list[dict]:
	path = CIN / PACKETS[movie] / "HANDOFF_PACKET.json"
	return json.loads(path.read_text(encoding="utf-8"))["assets"]


def _find_asset(movie: str, selector: str) -> dict:
	for asset in _assets(movie):
		if not asset.get("bound_reference_eligible") or not str(asset.get("media_type", "")).startswith("image/"):
			continue
		if asset.get("role") == selector or Path(asset["path"]).name == selector:
			return asset
	raise KeyError(f"No eligible authority for {movie}: {selector}")


def _binding_plan(item: dict) -> list[dict]:
	plan: list[dict] = []
	for index, (alias, job) in enumerate(item["bindings"], start=1):
		entry = {"id": f"IMAGE_{index}", "job": job}
		if alias == "rainbow_bunny_missing":
			entry.update({
				"status": "missing_human_approved_authority",
				"required": "dedicated approved rainbow dust bunny identity; the generated concept and MP4 are not pixel authorities",
			})
		elif alias == "arena_endpoint":
			entry.update({
				"status": "missing_accepted_predecessor_endpoint",
				"required": item["image1_requirement"],
			})
		else:
			source_override, selector = ALIASES[alias]
			source_movie = source_override or item["movie"]
			asset = _find_asset(source_movie, selector)
			packet = PACKETS[source_movie]
			remote_url = f"https://raw.githubusercontent.com/{REPO}/{SOURCE_COMMIT}/assets_src/cinematics/{packet}/{asset['path']}"
			entry.update({
				"status": "approved_source_authority_available",
				"source_movie_id": source_movie,
				"source_packet": packet,
				"path": asset["path"],
				"sha256": asset["sha256"],
				"remote_url": remote_url,
				"hud_present": False,
				"used_as_delivery_pixels": False,
			})
		if index == 1:
			entry["shot_opening_gate"] = item["image1_requirement"]
			entry["status"] = "missing_approved_shot_opening_frame"
			entry["source_authority_is_not_automatic_first_frame_approval"] = True
		plan.append(entry)
	if not 2 <= len(plan) <= 4:
		raise ValueError(f"{item['shot_id']} plans {len(plan)} bindings")
	return plan


def _prompt(item: dict) -> str:
	duration = item["duration"]
	if duration == 4:
		spans = ("0.0–1.3s", "1.3–3.0s", "3.0–4.0s")
	else:
		spans = ("0.0–2.0s", "2.0–4.5s", "4.5–6.0s")
	image_refs = "/".join(f"IMAGE_{i}" for i in range(2, len(item["bindings"]) + 1))
	return (
		f"{item['camera']} on the approved shot-opening frame from IMAGE_1.\n\n"
		f"{spans[0]}: {item['timeline'][0]}.\n"
		f"{spans[1]}: {item['timeline'][1]}.\n"
		f"{spans[2]}: {item['timeline'][2]}.\n\n"
		f"keep {item['must_not_move']} locked. preserve the identity, topology, and material authorities from {image_refs}. "
		f"{item['negatives']}.\n\n"
		f"end: {item['end']}.\n"
		f"Sound: {item['sound']}.\n"
	)


def _weak_windows(item: dict) -> list[dict]:
	windows: list[dict] = []
	for filename, observation in item["evidence"]:
		if filename is None:
			windows.append({"source_clip": None, "source_clip_url": None, "weak_frames": None, "observation": observation})
			continue
		clip_url = _release_clip_url(filename) if filename.endswith("_REGEN.mp4") else _clip_url(filename)
		windows.append({
			"source_clip": filename,
			"source_clip_url": clip_url,
			"frame_rate": 24,
			"reviewed_frame_domain": [0, 144],
			"observation": observation,
		})
	return windows


def _card(item: dict, prompt_sha: str) -> dict:
	authority_path, authority_rule = GAME_AUTHORITY[item["movie"]]
	blockers = [
		f"IMAGE_1 is not yet bound to the required {item['image1_requirement']}",
		"Sol/human approval of the clean full-frame opening and predecessor continuity is still required",
	]
	if any(alias == "rainbow_bunny_missing" for alias, _ in item["bindings"]):
		blockers.append("dedicated rainbow dust bunny identity authority is missing and must be approved before generation")
	return {
		"schema": "imagine-shot-card-draft-v1",
		"movie_id": item["movie"],
		"shot_id": item["shot_id"],
		"title": item["title"],
		"status": "DRAFT",
		"conditional_regeneration": item["conditional"],
		"duration_seconds": item["duration"],
		"aspect_ratio": "16:9",
		"delivery_size": [1280, 720],
		"mode": "image_to_video",
		"output_disposition": "motion_reference_only",
		"binding_plan": _binding_plan(item),
		"start_frame": "IMAGE_1 after the blocking shot-opening approval",
		"camera": {"verb": item["camera"], "move_count": 0 if item["camera"] == "locked" else 1},
		"must_move": item["must_move"],
		"must_not_move": item["must_not_move"],
		"end_state": item["end"],
		"negative_constraints": item["negatives"],
		"sound_intent": item["sound"],
		"prompt_path": "PROMPT.txt",
		"prompt_sha256": prompt_sha,
		"source_clip_audit": _weak_windows(item),
		"audited_release": {"tag": RELEASE_TAG, "url": RELEASE_URL},
		"implemented_event_contract": {
			"authority_path": authority_path,
			"rule": authority_rule,
		},
		"blocking_findings": blockers,
		"audit_claims": {"archive_complete": True, "generation_ready": False, "delivery_accepted": False},
		"review": {
			"luna_parallel_audit": True,
			"sol_master_review": True,
			"reviewed_at": DATE,
			"criteria": "loose rough-cut retention with strict geometry, identity, count, causality, and endpoint repair",
		},
	}


def _reconstruction(item: dict, plan: list[dict]) -> str:
	duration = item["duration"]
	if duration == 4:
		frame_rows = [
			("000–011", "Hold the exact approved IMAGE_1 state long enough to verify geography, cast count, contacts, and inherited dirt/clean state"),
			("012–031", item["timeline"][0]),
			("032–059", item["timeline"][1]),
			("060–071", "Complete the same dominant action without adding a second event or changing topology"),
			("072–083", item["timeline"][2]),
			("084–095", f"Hold the exact endpoint: {item['end']}"),
		]
	else:
		frame_rows = [
			("000–023", "Hold the exact approved IMAGE_1 state long enough to verify geography, cast count, contacts, and inherited dirt/clean state"),
			("024–047", item["timeline"][0]),
			("048–083", item["timeline"][1]),
			("084–107", "Complete the same dominant action without adding a second event or changing topology"),
			("108–131", item["timeline"][2]),
			("132–144", f"Hold the exact endpoint: {item['end']}"),
		]
	authority_path, authority_rule = GAME_AUTHORITY[item["movie"]]
	lines = [
		f"# {item['shot_id']} — {item['title']}",
		"",
		"> `STATUS`: DRAFT  ",
		"> `GENERATION_READY`: false  ",
		"> `DELIVERY_ACCEPTED`: false",
		"",
		"## Why this shot is being rebuilt",
		"",
	]
	for filename, observation in item["evidence"]:
		if filename:
			clip_url = _release_clip_url(filename) if filename.endswith("_REGEN.mp4") else _clip_url(filename)
			punctuation = "" if observation.endswith((".", "!", "?")) else "."
			lines.append(f"- [{filename}]({clip_url}): {observation}{punctuation}")
		else:
			lines.append(f"- {observation.capitalize()}.")
	lines.extend([
		"",
		"Frame ranges above are direct 24 fps review indices for the 145-frame source clips. They identify the repair window, not permission to interpolate or patch pixels.",
		"",
		"## Implemented-event contract",
		"",
		f"- Runtime authority: `{authority_path}`.",
		f"- Event rule: {authority_rule}.",
		f"- Entry state: {item['image1_requirement']}.",
		f"- Single causal action: {item['must_move']}.",
		f"- Required outgoing seam: {item['end']}.",
		"",
		"## Full-frame reconstruction map",
		"",
		"| Output frames | Required full-frame content |",
		"|---|---|",
	])
	for frame_range, content in frame_rows:
		lines.append(f"| {frame_range} | {content}. Every changed frame is a new complete flattened image. |")
	lines.extend([
		"",
		"## Binding plan",
		"",
		"| Slot | Job | Status / source |",
		"|---|---|---|",
	])
	for binding in plan:
		source = binding.get("remote_url") or binding.get("required", "missing")
		lines.append(f"| {binding['id']} | {binding['job']} | {binding['status']}: {source} |")
	lines.extend([
		"",
		"IMAGE_1 must be replaced or explicitly approved as the exact clean shot-opening frame before generation. Storyboards, contact sheets, runtime captures, and MP4 frames are never bound pixels.",
		"",
		"## Locked result",
		"",
		f"- Camera: {item['camera']}.",
		f"- Must move: {item['must_move']}.",
		f"- Must not move: {item['must_not_move']}.",
		f"- End state: {item['end']}.",
		f"- Reject: {item['negatives']}.",
		"- Generate the shot as complete full-frame images; no morphing, optical flow, compositing, cutout motion, or duplicated-frame concealment.",
		"",
		"## Files",
		"",
		"- [Paste-ready Grok prompt](PROMPT.txt)",
		"- [Machine-readable DRAFT shot card](SHOT_PACKET.json)",
	])
	return "\n".join(lines) + "\n"


def _scene_readme(movie: str, items: list[dict]) -> str:
	keep = KEEP.get(movie, [])
	reject = REJECT.get(movie, [])
	audit_rows = _audit_rows(movie)
	accepted = [row for row in audit_rows if row["verdict"] == "ACCEPT_MOTION_REFERENCE"]
	omitted = [row for row in audit_rows if row["verdict"] == "OMIT_SUPERSEDED_EVENT"]
	replaced = [row for row in audit_rows if row["verdict"] == "REPLACE_WITH_GAME_EVENT"]
	authority_path, authority_rule = GAME_AUTHORITY.get(movie, (
		"source visual archive", "retain the approved source beat order"))
	lines = [
		f"# {movie} selective regeneration — {TITLES[movie]}",
		"",
		"> `ARCHIVE_COMPLETE`: true (source archive)  ",
		"> `REGENERATION_GUIDE_COMPLETE`: true  ",
		"> `GENERATION_READY`: false  ",
		"> `DELIVERY_ACCEPTED`: false",
		"",
		f"[Open the immutable source visual archive]({_source_readme_url(movie)}). This repair guide changes no approved source art. It does supersede a source beat when that beat conflicts with the current implemented event.",
		"",
		"## Implemented-event authority",
		"",
		f"- `{authority_path}`",
		f"- {authority_rule}.",
		"- Release MP4s, old MP4s, boards, and runtime captures are evidence only; none is an IMAGE binding or delivery frame.",
		"",
		"## New release decision",
		"",
	]
	if audit_rows:
		lines.extend(["| Released shot | Verdict | Exact finding | Action |", "|---|---|---|---|"])
		for row in audit_rows:
			links = ", ".join(f"[{name}]({_release_clip_url(name)})" for name in row["clips"])
			lines.append(f"| {row['shot_id']} ({links}) | `{row['verdict']}` | Frames {row['weak_frames']}: {row['finding']} | {row['next_action']} |")
	else:
		lines.append("- This release contains no clip for the scene.")
	lines.extend(["", "## Accepted from the new release for rough motion", ""])
	if accepted:
		for row in accepted:
			preferred = row["preferred_clip"] or row["clips"][0]
			lines.append(f"- [{preferred}]({_release_clip_url(preferred)}) — retained as motion/editorial reference only; `DELIVERY_ACCEPTED` remains false.")
	else:
		lines.append("- None.")
	if omitted:
		lines.extend(["", "## Removed from the corrected game-congruent cut", ""])
		for row in omitted:
			lines.append(f"- {row['shot_id']} — {row['finding']}")
	if replaced:
		lines.extend(["", "## Replaced with implemented events", ""])
		for row in replaced:
			lines.append(f"- {row['shot_id']} → {row['replacement_shot']}: {row['next_action']}")
	lines.extend(["", "## Earlier rough references still retained", ""])
	if keep:
		for filename in keep:
			note = "retain as rough reference"
			if movie == "D1-C02" and filename in {"C02_S01_v1_door_open.mp4", "C02_S04_v1_bathroom_glow.mp4"}:
				note += "; whole-frame padding to 1280×720 is allowed in edit"
			if movie in {"D1-C06", "D1-C07", "D1-C08"} and ("S07" in filename or "S06" in filename or "S05" in filename):
				note += "; conditional/temporary pending endpoint and identity check"
			lines.append(f"- [{filename}]({_clip_url(filename)}) — {note}.")
	else:
		lines.append("- None. Existing candidates may inform motion only; none are retained as the preferred rough shot.")
	lines.extend(["", "## Regenerate — complete active queue", ""])
	if items:
		lines.extend(["| Shot | Replacement | Card | Reconstruction |", "|---|---|---|---|"])
		for item in items:
			label = item["title"] + (" (conditional)" if item["conditional"] else "")
			shot_id = item["shot_id"]
			lines.append(f"| {shot_id} | {label} | [{shot_id} card](shots/{shot_id}/SHOT_PACKET.json) | [weak frames and rebuild](shots/{shot_id}/RECONSTRUCTION.md) |")
	else:
		lines.append("- None. Every released shot for this scene either passed the loose motion-reference audit or was removed because its event does not belong in the corrected cut.")
	if reject:
		lines.extend(["", "## Reject as continuity authority", ""])
		for filename in reject:
			lines.append(f"- [{filename}]({_clip_url(filename)})")
	lines.extend([
		"",
		"## Operator gate",
		"",
		"1. Open the linked source archive and the reconstruction page for the selected shot.",
		"2. Supply the missing human-approved, clean, HUD-free IMAGE_1 named in the DRAFT card.",
		"3. Bind only the two to four planned images; never bind storyboards, contact sheets, gameplay captures, or MP4 frames.",
		"4. Paste `PROMPT.txt` unchanged unless the accepted endpoint requires a purely positional clarification.",
		"5. Generate one shot only. Submit its full-frame endpoint for Sol/human approval before the next continuous shot.",
		"",
		"The loose audit accepts coherent clips for assembly without pretending they are final delivery. This page lists every remaining regeneration card for the scene and no accepted card. `GENERATION_READY` stays false until every card's IMAGE_1 and identity bindings are actually approved and remotely opened.",
	])
	return "\n".join(lines) + "\n"


def build() -> None:
	OVERLAY.mkdir(parents=True, exist_ok=True)
	remote_verification = OVERLAY / "REMOTE_VERIFICATION.json"
	if remote_verification.is_file():
		remote_verification.unlink()
	by_scene = {movie: [] for movie in PACKETS}
	for item in SHOTS:
		by_scene[item["movie"]].append(item)

	rows: list[dict] = []
	for movie, packet in PACKETS.items():
		items = sorted(by_scene[movie], key=lambda value: value["shot_id"])
		repair_root = OVERLAY / "scenes" / movie
		repair_root.mkdir(parents=True, exist_ok=True)
		shots_root = repair_root / "shots"
		if shots_root.is_dir():
			if shots_root.resolve().parent != repair_root.resolve():
				raise AssertionError(f"refusing unsafe generated-shot cleanup: {shots_root}")
			shutil.rmtree(shots_root)
		(repair_root / "README.md").write_text(_scene_readme(movie, items), encoding="utf-8", newline="\n")
		for item in items:
			shot_root = repair_root / "shots" / item["shot_id"]
			shot_root.mkdir(parents=True, exist_ok=True)
			prompt = _prompt(item)
			prompt_sha = _sha256_text(prompt)
			plan = _binding_plan(item)
			(shot_root / "PROMPT.txt").write_text(prompt, encoding="utf-8", newline="\n")
			(shot_root / "SHOT_PACKET.json").write_text(json.dumps(_card(item, prompt_sha), indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
			(shot_root / "RECONSTRUCTION.md").write_text(_reconstruction(item, plan), encoding="utf-8", newline="\n")
			rows.append({
				"movie_id": movie,
				"shot_id": item["shot_id"],
				"disposition": "conditional_regenerate" if item["conditional"] else "regenerate",
				"title": item["title"],
				"status": "DRAFT",
				"generation_ready": "false",
				"delivery_accepted": "false",
				"scene_guide": f"assets_src/cinematics/day_one_grok_regeneration_handoffs_{DATE}/scenes/{movie}/README.md",
			})

	with (OVERLAY / "SHOT_REGENERATION_INDEX.csv").open("w", encoding="utf-8", newline="") as handle:
		writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
		writer.writeheader()
		writer.writerows(rows)

	scenes = []
	for movie, packet in PACKETS.items():
		items = by_scene[movie]
		scene_audit = _audit_rows(movie)
		scenes.append({
			"movie_id": movie,
			"title": TITLES[movie],
			"source_packet": f"assets_src/cinematics/{packet}",
			"regeneration_guide": f"assets_src/cinematics/day_one_grok_regeneration_handoffs_{DATE}/scenes/{movie}/README.md",
			"retain_rough": KEEP.get(movie, []),
			"reject_as_authority": REJECT.get(movie, []),
			"release_motion_references_accepted": [
				row["preferred_clip"] for row in scene_audit
				if row["verdict"] == "ACCEPT_MOTION_REFERENCE"
			],
			"release_events_omitted": [
				row["shot_id"] for row in scene_audit
				if row["verdict"] == "OMIT_SUPERSEDED_EVENT"
			],
			"release_events_replaced": [
				{"released_shot": row["shot_id"], "replacement_shot": row["replacement_shot"]}
				for row in scene_audit if row["verdict"] == "REPLACE_WITH_GAME_EVENT"
			],
			"regenerate_shots": [item["shot_id"] for item in items],
		})
	index = {
		"schema": "day-one-grok-selective-regeneration-index-v1",
		"date": DATE,
		"source_visual_archive_commit": SOURCE_COMMIT,
		"audited_clip_commit": CLIP_COMMIT,
		"audited_release_tag": RELEASE_TAG,
		"audited_release_url": RELEASE_URL,
		"claims": {
			"archive_complete": True,
			"regeneration_guide_complete": True,
			"generation_ready": False,
			"delivery_accepted": False,
		},
		"review_protocol": "parallel Luna clip/scene audits followed by Sol master consistency review",
		"shot_card_count": len(SHOTS),
		"scenes": scenes,
	}
	(OVERLAY / "INDEX.json").write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")

	audit_counts = {
		verdict: sum(1 for row in RELEASE_AUDIT if row["verdict"] == verdict)
		for verdict in [
			"ACCEPT_MOTION_REFERENCE", "REGENERATE",
			"REPLACE_WITH_GAME_EVENT", "OMIT_SUPERSEDED_EVENT",
		]
	}
	clip_records = []
	for row in RELEASE_AUDIT:
		for filename in row["clips"]:
			if row["verdict"] == "ACCEPT_MOTION_REFERENCE":
				variant_disposition = "selected_motion_reference" \
					if filename == row["preferred_clip"] else "rejected_duplicate_variant"
			elif row["verdict"] == "REPLACE_WITH_GAME_EVENT":
				variant_disposition = "rejected_wrong_event_replace_with_game_event"
			elif row["verdict"] == "OMIT_SUPERSEDED_EVENT":
				variant_disposition = "rejected_wrong_event_omit_from_cut"
			else:
				variant_disposition = "rejected_requires_regeneration"
			clip_records.append({
				"movie_id": row["shot_id"].rsplit("-S", 1)[0],
				"shot_id": row["shot_id"],
				"filename": filename,
				"url": _release_clip_url(filename),
				"dimensions": [1280, 720],
				"frame_rate": 24,
				"frame_count": 145,
				"duration_seconds": 6.041667,
				"shot_verdict": row["verdict"],
				"variant_disposition": variant_disposition,
				"weak_frames": row["weak_frames"],
				"finding": row["finding"],
				"replacement_shot": row["replacement_shot"],
			})
	release_audit_index = {
		"schema": "day-one-regen-release-motion-audit-v1",
		"release_tag": RELEASE_TAG,
		"release_url": RELEASE_URL,
		"review_basis": "all 40 files inspected at 24 fps against current runtime event logic, source visual packets, and the prior regeneration cards",
		"claims": {
			"motion_reference_review_complete": True,
			"generation_ready": False,
			"delivery_accepted": False,
		},
		"unique_shots": len(RELEASE_AUDIT),
		"clip_files": len(clip_records),
		"verdict_counts": audit_counts,
		"remaining_regeneration_cards": len(SHOTS),
		"clips": clip_records,
	}
	(OVERLAY / "AUDITED_RELEASE_ASSETS.json").write_text(
		json.dumps(release_audit_index, indent=2, ensure_ascii=False) + "\n",
		encoding="utf-8", newline="\n")

	audit_md = [
		"# New draft release audit — Day One selective regeneration",
		"",
		f"Release audited: [{RELEASE_TAG}]({RELEASE_URL})",
		"",
		"> `MOTION_REFERENCE_REVIEW_COMPLETE`: true  ",
		"> `GENERATION_READY`: false  ",
		"> `DELIVERY_ACCEPTED`: false",
		"",
		f"All {len(clip_records)} MP4 files ({len(RELEASE_AUDIT)} unique shots) were inspected at 1280×720, 24 fps, 145 frames, and 6.041667 seconds. The loose audit retains {audit_counts['ACCEPT_MOTION_REFERENCE']} shots for rough motion, sends {audit_counts['REGENERATE']} shots back for direct repair, replaces {audit_counts['REPLACE_WITH_GAME_EVENT']} stale Stuffie beats with implemented events, and removes {audit_counts['OMIT_SUPERSEDED_EVENT']} invented discovery beats from the cut.",
		"",
		"`ACCEPT_MOTION_REFERENCE` is not final acceptance. It only means the action is useful in a rough edit. Full-frame provenance, identity, endpoint, and human review remain blocking.",
		"",
		"## Shot-by-shot findings",
		"",
		"| Shot | Release files | Verdict | Weak frames | Detailed finding | Corrective disposition |",
		"|---|---|---|---|---|---|",
	]
	for row in RELEASE_AUDIT:
		links = ", ".join(f"[{name}]({_release_clip_url(name)})" for name in row["clips"])
		audit_md.append(f"| {row['shot_id']} | {links} | `{row['verdict']}` | {row['weak_frames']} | {row['finding']} | {row['next_action']} |")
	audit_md.extend([
		"",
		"## Corrected game-event chain",
		"",
		"The prior Stuffie handoff encoded events that are absent from the game. The corrected cut is: dirty-room entry → one Baby Eagle visibly held by exactly two rescue pin bunnies → Roshan approaches left pin → left pin pops after contact → Roshan approaches right pin → right pin pops after contact and the room resolves clean → Baby Eagle thanks, rises, and departs → companion picker may open after the UI-free endpoint.",
		"",
		"The cooperative C13 coda is an owner-directed extension. Its seam is now explicit: insert it immediately after the third successful boss round, while Grand Puff has entered the non-hostile FRIENDS boundary but before the runtime implosion completes. This avoids the continuity error of making an intact giant reappear after he has already vanished.",
		"",
		"## Machine record",
		"",
		"- [Per-file release audit](AUDITED_RELEASE_ASSETS.json)",
		"- [Only the remaining regeneration shots](SHOT_REGENERATION_INDEX.csv)",
	])
	(OVERLAY / "NEW_DRAFT_AUDIT.md").write_text(
		"\n".join(audit_md) + "\n", encoding="utf-8", newline="\n")

	readme = [
		"# Day One Grok selective regeneration handoffs — 2026-09-03",
		"",
		"> `ARCHIVE_COMPLETE`: true (2026-09-02 source archive)  ",
		"> `REGENERATION_GUIDE_COMPLETE`: true  ",
		"> `GENERATION_READY`: false  ",
		"> `DELIVERY_ACCEPTED`: false",
		"",
		f"[Open the detailed audit of all 40 release files](NEW_DRAFT_AUDIT.md) from [{RELEASE_TAG}]({RELEASE_URL}).",
		"",
		f"This is the looser, production-practical result: {audit_counts['ACCEPT_MOTION_REFERENCE']} of 36 unique release shots remain useful for rough motion, {audit_counts['REGENERATE']} need direct reconstruction, {audit_counts['REPLACE_WITH_GAME_EVENT']} stale Stuffie beats are replaced by current game events, and {audit_counts['OMIT_SUPERSEDED_EVENT']} invented discovery beats are removed. The queue below contains only the {len(SHOTS)} shots that now need generation.",
		"",
		"Every replacement remains one separate full-frame 1280×720 Grok job and a motion/editorial reference until the independent delivery audit passes.",
		"",
		"| Scene | Decision | Single-link updated handoff |",
		"|---|---|---|",
	]
	for movie, packet in PACKETS.items():
		count = len(by_scene[movie])
		scene_audit = _audit_rows(movie)
		accepted_count = sum(1 for row in scene_audit if row["verdict"] == "ACCEPT_MOTION_REFERENCE")
		omitted_count = sum(1 for row in scene_audit if row["verdict"] == "OMIT_SUPERSEDED_EVENT")
		decision = f"{count} regeneration card{'s' if count != 1 else ''}"
		if accepted_count:
			decision += f"; {accepted_count} release shot{'s' if accepted_count != 1 else ''} retained for motion"
		if omitted_count:
			decision += f"; {omitted_count} stale beat{'s' if omitted_count != 1 else ''} removed"
		if not count and not accepted_count and not omitted_count:
			decision = "no release change; retain earlier rough plan"
		readme.append(f"| {movie} | {decision} | [Open updated {movie} handoff](scenes/{movie}/README.md) |")
	readme.extend([
		"",
		"## How to use",
		"",
		"Open one scene link, choose a replacement shot, review its exact weak-frame diagnosis, bind the planned two to four images, and paste its prompt. The DRAFT card states the precise missing IMAGE_1. Do not generate downstream continuous shots until the preceding endpoint is accepted.",
		"",
		"- [Detailed new-release critique](NEW_DRAFT_AUDIT.md)",
		"- [Per-file machine audit](AUDITED_RELEASE_ASSETS.json)",
		"- [Sol master audit and priority order](SOL_MASTER_AUDIT.md)",
		"- [Machine-readable index](INDEX.json)",
		"- [Flat shot regeneration index](SHOT_REGENERATION_INDEX.csv)",
		"- [Deterministic overlay manifest](REGENERATION_PACKET.json)",
		"- [Immutable remote verification](REMOTE_VERIFICATION.json)",
		"",
		"Generated boards and audited MP4s are narrative or motion evidence only. They are never bound generation pixels, accepted keyframes, or delivery frames.",
	])
	(OVERLAY / "README.md").write_text("\n".join(readme) + "\n", encoding="utf-8", newline="\n")

	audit = f"""# Sol master audit — selective Day One regeneration

Three Luna audits reviewed all 40 release files at frame level; Sol reconciled them against the runtime state machine, source archives, and the owner's cooperative C13 extension. The threshold is deliberately loose for rough-cut motion and strict for event truth: polish cannot rescue the wrong game event.

## Outcome

- `{audit_counts['ACCEPT_MOTION_REFERENCE']}` unique shots are retained as motion/editorial references.
- `{audit_counts['REGENERATE']}` released shots require direct reconstruction.
- `{audit_counts['REPLACE_WITH_GAME_EVENT']}` released Stuffie beats are replaced by the actual two-pin rescue.
- `{audit_counts['OMIT_SUPERSEDED_EVENT']}` discovery beats are removed because the events do not happen.
- `{len(SHOTS)}` DRAFT cards remain. Accepted and omitted shots have no card in this queue.

## Priority order

1. **P0 event correction:** C07-S06 → corrected C08-S01–S05. One Baby Eagle, two rescue pins, two Roshan contacts, clean-room resolve, Baby Eagle thanks/rises/departs. Never generate baskets, four emerging bunnies, or a wing-blast cleanup.
2. **P0 topology and state:** C02-S03, C03-S02–S04, C05-S04/S05, C09-S04, C10-S02/S03. Start from the exact room projection and exact dirty/clean state; never use labeled evidence, substituted silhouettes, flying supplies, or incomplete Art Room framing.
3. **P0 boss continuity:** C11-S04, C13-S03, C13-S05. C13 begins after the third successful round but before FRIENDS implosion completes, preventing an intact giant from reappearing after vanishing.
4. **P1 causal action:** C01-S02 and C06-S03/S05/S08. Each shot must show its physical cause and stop on the intended seam; the dedicated hug remains C06-S09.

## Exact topology locks

- Art Room: straight-on front only; two shell windows, two pearl columns, one chandelier, one shell idea board, one rectangular center desk, rear shelves, two curved counters, zero interior doors.
- Stuffie rescue: exactly one Baby Eagle and exactly two rescue pin bunnies. Ordinary room bunnies are not substitute pins and Daddy's splash cannot clear rescue pins.
- Boss arena: fixed octagonal floor and wall ring; no crater, dark hole, alternate pearl hall, platform morph, or menacing Grand Puff redesign.

## Retention policy

Accepted clips remain motion/editorial references only and do not set `DELIVERY_ACCEPTED`. The per-file ledger records which C13 variant won: Daddy S02 v2 and Rumi S04 v1. Rejected duplicates are not continuity authorities.

## Blocking truth

All remaining cards are `DRAFT`. Exact clean shot-opening frames still require human approval, and C13-S05 still requires a dedicated approved rainbow dust bunny identity. `GENERATION_READY` and `DELIVERY_ACCEPTED` therefore remain false even though the prompts are paste-ready.
"""
	(OVERLAY / "SOL_MASTER_AUDIT.md").write_text(audit, encoding="utf-8", newline="\n")

	payload_records = []
	for path in sorted(OVERLAY.rglob("*"), key=lambda value: value.relative_to(OVERLAY).as_posix()):
		if not path.is_file() or path.name in {"REGENERATION_PACKET.json", "REMOTE_VERIFICATION.json"}:
			continue
		relative = path.relative_to(OVERLAY).as_posix()
		sha = hashlib.sha256(path.read_bytes()).hexdigest()
		if path.name == "SHOT_PACKET.json":
			role = "draft_imagine_shot_card"
		elif path.name == "PROMPT.txt":
			role = "paste_ready_imagine_prompt"
		elif path.name == "RECONSTRUCTION.md":
			role = "weak_frame_reconstruction_guide"
		elif path.name == "README.md":
			role = "operator_index_or_scene_handoff"
		elif path.name == "SOL_MASTER_AUDIT.md":
			role = "sol_master_review"
		elif path.name == "NEW_DRAFT_AUDIT.md":
			role = "frame_level_release_audit"
		elif path.name == "AUDITED_RELEASE_ASSETS.json":
			role = "machine_readable_release_audit"
		else:
			role = "machine_readable_index"
		payload_records.append({"path": relative, "role": role, "sha256": sha})
	payload_lines = "".join(f"{record['path']}|{record['sha256']}\n" for record in payload_records)
	packet = {
		"schema": "day-one-grok-selective-regeneration-packet-v1",
		"packet_id": f"day_one_grok_regeneration_handoffs_{DATE}",
		"date": DATE,
		"runtime_asset": False,
		"used_as_delivery_pixels": False,
		"payload_sha256": _sha256_text(payload_lines),
		"payload_hash_formula": "SHA256 of UTF-8 sorted <relative_path>|<lowercase_sha256>\\n records; excludes this manifest and the separate remote verification record",
		"claims": {
			"source_archive_complete": True,
			"regeneration_guide_complete": True,
			"generation_ready": False,
			"delivery_accepted": False,
		},
		"source_visual_archive": {
			"commit": SOURCE_COMMIT,
			"index": f"https://github.com/{REPO}/tree/{SOURCE_COMMIT}/assets_src/cinematics/day_one_grok_visual_handoffs_2026-09-02",
		},
		"audited_clip_source": {
			"commit": CLIP_COMMIT,
			"tree": f"https://github.com/{REPO}/tree/{CLIP_COMMIT}/clips",
		},
		"audited_release_source": {
			"tag": RELEASE_TAG,
			"release": RELEASE_URL,
			"clip_count": sum(len(row["clips"]) for row in RELEASE_AUDIT),
			"unique_shot_count": len(RELEASE_AUDIT),
		},
		"assets": payload_records,
		"remote_verification": "separate REMOTE_VERIFICATION.json is written only after the content commit is pushed and resolved from GitHub",
	}
	(OVERLAY / "REGENERATION_PACKET.json").write_text(json.dumps(packet, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def validate() -> None:
	if len(RELEASE_AUDIT) != 36:
		raise AssertionError(f"expected 36 audited shots, found {len(RELEASE_AUDIT)}")
	if sum(len(row["clips"]) for row in RELEASE_AUDIT) != 40:
		raise AssertionError("expected 40 audited release files")
	if len(SHOTS) != 22:
		raise AssertionError(f"expected 22 remaining cards, found {len(SHOTS)}")
	generated_card_paths = list(OVERLAY.glob("scenes/*/shots/*/SHOT_PACKET.json"))
	if len(generated_card_paths) != len(SHOTS):
		raise AssertionError(
			f"stale or missing generated cards: expected {len(SHOTS)}, "
			f"found {len(generated_card_paths)}")
	for card_path in generated_card_paths:
		card = json.loads(card_path.read_text(encoding="utf-8"))
		prompt = card_path.with_name("PROMPT.txt").read_text(encoding="utf-8")
		if card["status"] != "DRAFT" or card["audit_claims"]["generation_ready"]:
			raise AssertionError(f"false readiness claim: {card_path}")
		if not 2 <= len(card["binding_plan"]) <= 4:
			raise AssertionError(f"binding count: {card_path}")
		if not prompt.rstrip().splitlines()[-1].startswith("Sound:"):
			raise AssertionError(f"missing final Sound line: {card_path}")
		if _sha256_text(prompt) != card["prompt_sha256"]:
			raise AssertionError(f"prompt hash mismatch: {card_path}")
		for binding in card["binding_plan"]:
			if "remote_url" in binding:
				asset_path = CIN / binding["source_packet"] / binding["path"]
				if not asset_path.is_file():
					raise AssertionError(f"missing source authority: {asset_path}")
	for json_path in OVERLAY.glob("scenes/**/*.json"):
		json.loads(json_path.read_text(encoding="utf-8"))
	json.loads((OVERLAY / "INDEX.json").read_text(encoding="utf-8"))
	packet = json.loads((OVERLAY / "REGENERATION_PACKET.json").read_text(encoding="utf-8"))
	payload_lines = "".join(f"{record['path']}|{record['sha256']}\n" for record in packet["assets"])
	if _sha256_text(payload_lines) != packet["payload_sha256"]:
		raise AssertionError("overlay payload hash mismatch")
	for record in packet["assets"]:
		path = OVERLAY / record["path"]
		if hashlib.sha256(path.read_bytes()).hexdigest() != record["sha256"]:
			raise AssertionError(f"overlay file hash mismatch: {path}")
	remote_verification = OVERLAY / "REMOTE_VERIFICATION.json"
	if remote_verification.is_file():
		remote = json.loads(remote_verification.read_text(encoding="utf-8"))
		if remote.get("missing_manifest_assets") != 0 or remote.get("manifest_assets_resolved") != len(packet["assets"]):
			raise AssertionError("remote verification does not cover the complete overlay manifest")


if __name__ == "__main__":
	build()
	validate()
	print(f"REGEN_HANDOFF|RESULT|ALL OK|cards={len(SHOTS)}|overlay={OVERLAY}")
