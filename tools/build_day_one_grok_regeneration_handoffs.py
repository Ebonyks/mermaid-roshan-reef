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
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CIN = ROOT / "assets_src" / "cinematics"
SOURCE_COMMIT = "076661afb9e092627eb5dfae7c39fecb27463892"
CLIP_COMMIT = "5ca170e11c77ea55c3224f9f275b94b8fd62ca36"
REPO = "Ebonyks/mermaid-roshan-reef"
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


ALIASES = {
	"location": (None, "approved_location_geography_authority"),
	"roshan": (None, "approved_roshan_identity_authority"),
	"daddy": (None, "approved_daddy_identity_authority"),
	"rumi": (None, "approved_rumi_identity_authority"),
	"swimming_bunny": (None, "approved_swimming_bunny_identity_authority"),
	"baby_eagle_pinned": (None, "approved_baby_eagle_pinned_identity_authority"),
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
		windows.append({
			"source_clip": filename,
			"source_clip_url": _clip_url(filename),
			"frame_rate": 24,
			"reviewed_frame_domain": [0, 144],
			"observation": observation,
		})
	return windows


def _card(item: dict, prompt_sha: str) -> dict:
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
		frame_rows = [("000–031", item["timeline"][0]), ("032–071", item["timeline"][1]), ("072–095", item["timeline"][2])]
	else:
		frame_rows = [("000–047", item["timeline"][0]), ("048–107", item["timeline"][1]), ("108–144", item["timeline"][2])]
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
			lines.append(f"- [{filename}]({_clip_url(filename)}): {observation}.")
		else:
			lines.append(f"- {observation.capitalize()}.")
	lines.extend([
		"",
		"Frame ranges above are direct 24 fps review indices for the 145-frame source clips. They identify the repair window, not permission to interpolate or patch pixels.",
		"",
		"## Full-frame reconstruction map",
		"",
		"| Output frames | Required full-frame content |",
		"|---|---|",
	])
	for frame_range, content in frame_rows:
		lines.append(f"| {frame_range} | {content.capitalize()}. Every changed frame is a new complete flattened image. |")
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
	lines = [
		f"# {movie} selective regeneration — {TITLES[movie]}",
		"",
		"> `ARCHIVE_COMPLETE`: true (source archive)  ",
		"> `REGENERATION_GUIDE_COMPLETE`: true  ",
		"> `GENERATION_READY`: false  ",
		"> `DELIVERY_ACCEPTED`: false",
		"",
		f"[Open the immutable source visual archive]({_source_readme_url(movie)}). This repair guide changes no approved source art. Existing clips below are editorial/motion references only.",
		"",
		"## Retain for the loose rough cut",
		"",
	]
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
	lines.extend(["", "## Regenerate", ""])
	if items:
		lines.extend(["| Shot | Replacement | Card | Reconstruction |", "|---|---|---|---|"])
		for item in items:
			label = item["title"] + (" (conditional)" if item["conditional"] else "")
			shot_id = item["shot_id"]
			lines.append(f"| {shot_id} | {label} | [{shot_id} card](shots/{shot_id}/SHOT_PACKET.json) | [weak frames and rebuild](shots/{shot_id}/RECONSTRUCTION.md) |")
	else:
		lines.append("- No immediate regeneration under the loose rough-cut criteria. Escalate only an exact frame that later fails identity, topology, or endpoint review.")
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
		"The loose audit accepts coherent clips for assembly without pretending they are final delivery. `GENERATION_READY` stays false until every card's IMAGE_1 and identity bindings are actually approved and remotely opened.",
	])
	return "\n".join(lines) + "\n"


def build() -> None:
	OVERLAY.mkdir(parents=True, exist_ok=True)
	by_scene = {movie: [] for movie in PACKETS}
	for item in SHOTS:
		by_scene[item["movie"]].append(item)

	rows: list[dict] = []
	for movie, packet in PACKETS.items():
		items = sorted(by_scene[movie], key=lambda value: value["shot_id"])
		repair_root = OVERLAY / "scenes" / movie
		repair_root.mkdir(parents=True, exist_ok=True)
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
		scenes.append({
			"movie_id": movie,
			"title": TITLES[movie],
			"source_packet": f"assets_src/cinematics/{packet}",
			"regeneration_guide": f"assets_src/cinematics/day_one_grok_regeneration_handoffs_{DATE}/scenes/{movie}/README.md",
			"retain_rough": KEEP.get(movie, []),
			"reject_as_authority": REJECT.get(movie, []),
			"regenerate_shots": [item["shot_id"] for item in items],
		})
	index = {
		"schema": "day-one-grok-selective-regeneration-index-v1",
		"date": DATE,
		"source_visual_archive_commit": SOURCE_COMMIT,
		"audited_clip_commit": CLIP_COMMIT,
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

	readme = [
		"# Day One Grok selective regeneration handoffs — 2026-09-03",
		"",
		"> `ARCHIVE_COMPLETE`: true (2026-09-02 source archive)  ",
		"> `REGENERATION_GUIDE_COMPLETE`: true  ",
		"> `GENERATION_READY`: false  ",
		"> `DELIVERY_ACCEPTED`: false",
		"",
		"This is the looser, production-practical audit: coherent clips stay in the rough cut; only missing or materially weak geometry, identity, cast-count, causality, or endpoint shots are targeted. Every replacement remains a separate full-frame 1280×720 Grok job and a motion/editorial reference until the independent delivery audit passes.",
		"",
		"| Scene | Decision | Single-link updated handoff |",
		"|---|---|---|",
	]
	for movie, packet in PACKETS.items():
		count = len(by_scene[movie])
		decision = f"{count} replacement card{'s' if count != 1 else ''}" if count else "retain rough; no immediate replacement"
		readme.append(f"| {movie} | {decision} | [Open updated {movie} handoff](scenes/{movie}/README.md) |")
	readme.extend([
		"",
		"## How to use",
		"",
		"Open one scene link, choose a replacement shot, review its exact weak-frame diagnosis, bind the planned two to four images, and paste its prompt. The DRAFT card states the precise missing IMAGE_1. Do not generate downstream continuous shots until the preceding endpoint is accepted.",
		"",
		"- [Sol master audit and priority order](SOL_MASTER_AUDIT.md)",
		"- [Machine-readable index](INDEX.json)",
		"- [Flat shot regeneration index](SHOT_REGENERATION_INDEX.csv)",
		"- [Deterministic overlay manifest](REGENERATION_PACKET.json)",
		"- [Immutable remote verification](REMOTE_VERIFICATION.json)",
		"",
		"Generated boards and audited MP4s are narrative or motion evidence only. They are never bound generation pixels, accepted keyframes, or delivery frames.",
	])
	(OVERLAY / "README.md").write_text("\n".join(readme) + "\n", encoding="utf-8", newline="\n")

	audit = """# Sol master audit — selective Day One regeneration

The earlier all-reject result was too strict for rough-cut editorial use. This overlay applies a looser but still coherent production threshold: retain a clip when its core action, identity, and room read are usable; regenerate when a defect changes geography, character identity, cast count, action causality, or the stable endpoint needed by the next shot.

## Priority order

1. **P0 continuity chain:** C11-S02/S03/S04 → C13-S01–S05 → C12-S05. This is one inherited Main Hall-to-arena-to-friendship chain. Do not generate downstream cards until the previous endpoint is accepted.
2. **P0 identity/count:** C07-S04–S06 and C08-S02/S03/S04/S06/S07. These repair missing rope contact, premature eagle reveal, wrong animal/child identity, and changing bunny/eagle counts.
3. **P0 room topology:** C09-S04/S05 and C10-S02/S03/S05. Use only the exact straight-on runtime Art Room: two shell windows, two pearl columns, one chandelier, shell idea board, rectangular center desk, rear shelves, and two curved counters; zero interior doors.
4. **P1 causal action:** C03-S02–S04 and C06-S03–S06/S08/S09. These create missing discovery/purification/relationship bridges with stable contact and endpoints.
5. **P2 coverage/detail:** C01-S02/S03, C02-S03, and C05-S04/S05. C05-S05 is conditional: skip it only if Sol confirms exact seahorse topology and a plug physically lodged in the mouth.

## Retention policy

- C00 and C04 need no immediate regeneration under the loose rough-cut threshold.
- Retained clips remain editorial/motion references only; this does not set `DELIVERY_ACCEPTED`.
- C02's 1264×720 clips may receive a uniform whole-frame pad to 1280×720 in the edit. Padding cannot repair content or subject motion.
- C13 action variants may inform motion, but all five are rebuilt at native 1280×720 because the arena/identity chain is a new story-critical bridge and every source is 1264×720.

## Blocking truth

All replacement cards are `DRAFT`. The source location and identity authorities are available at immutable GitHub URLs, but the exact clean shot-opening frame is not yet human approved. C13-S05 and inherited C12-S05 also require a dedicated approved rainbow dust bunny identity. Therefore `GENERATION_READY` remains false even though every prompt is paste-ready.
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
		"assets": payload_records,
		"remote_verification": "separate REMOTE_VERIFICATION.json is written only after the content commit is pushed and resolved from GitHub",
	}
	(OVERLAY / "REGENERATION_PACKET.json").write_text(json.dumps(packet, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def validate() -> None:
	if len(SHOTS) != 36:
		raise AssertionError(f"expected 36 cards, found {len(SHOTS)}")
	for card_path in OVERLAY.glob("scenes/*/shots/*/SHOT_PACKET.json"):
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


if __name__ == "__main__":
	build()
	validate()
	print(f"REGEN_HANDOFF|RESULT|ALL OK|cards={len(SHOTS)}|overlay={OVERLAY}")
