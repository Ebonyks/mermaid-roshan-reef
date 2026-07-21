#!/usr/bin/env python3
"""Normalize and slice accepted Pearl Opera House flat-art prototypes."""

from __future__ import annotations

import csv
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets_src" / "concepts" / "opera_house_flat"
OUTPUT = SOURCE / "cards"
LEDGER = ROOT / "audit" / "opera_house_flat_prototype_ledger_2026-07-21.csv"

SCORES = {
	"architecture": 4.8,
	"front_of_house": 4.9,
	"lobby_furniture": 4.9,
	"lobby_services": 4.8,
	"lobby_decor": 4.9,
	"upper_access": 4.9,
	"stage": 4.9,
	"floor1": 4.9,
	"floor2": 4.8,
	"floor3": 4.9,
	"crest": 4.9,
}

SHEETS = (
	"opera_house_master_scene_key_2026-07-21.png",
	"opera_house_stage_scene_key_2026-07-21.png",
	"opera_house_architecture_kit_2026-07-21.png",
	"opera_house_front_of_house_kit_2026-07-21.png",
	"opera_house_lobby_furniture_kit_2026-07-21.png",
	"opera_house_lobby_services_kit_2026-07-21.png",
	"opera_house_lobby_architectural_decor_kit_2026-07-21.png",
	"opera_house_upper_floor_access_kit_2026-07-21.png",
	"opera_house_stage_backstage_kit_2026-07-21.png",
	"opera_house_floor1_act_props_2026-07-21.png",
	"opera_house_floor2_act_props_2026-07-21.png",
	"opera_house_floor3_act_props_2026-07-21.png",
	"opera_house_crest_wayfinding_kit_2026-07-21.png",
)

SHEET_SPECS = (
	(
		"architecture",
		"opera_house_architecture_kit_2026-07-21.png",
		4,
		3,
		(
			"grand_arch",
			"curved_balcony_fascia",
			"split_stair",
			"shell_balustrade",
			"column_and_pilaster",
			"cove_cornice",
			"terrazzo_floor_tile",
			"carpet_runner_pair",
			"portal_closed",
			"portal_open",
			"medallion_states",
			"bubble_lift",
		),
	),
	(
		"front_of_house",
		"opera_house_front_of_house_kit_2026-07-21.png",
		4,
		4,
		(
			"ticket_booth",
			"usher_podium",
			"poster_case",
			"coat_check",
			"lobby_settee",
			"compact_lobby_chair",
			"chandelier",
			"wall_sconce",
			"potted_palm",
			"velvet_stanchions",
			"program_rack",
			"sweets_lemonade_cart",
			"lobby_clock",
			"umbrella_stand",
			"waste_bin",
			"egress_double_door",
		),
	),
	(
		"lobby_furniture",
		"opera_house_lobby_furniture_kit_2026-07-21.png",
		4,
		4,
		(
			"curved_settee",
			"shell_back_chair_pair",
			"round_ottoman",
			"waiting_bench",
			"round_side_table",
			"console_table",
			"writing_desk",
			"cheval_mirror",
			"coat_hat_tree",
			"parcel_bench",
			"nesting_table_pair",
			"window_seat",
			"conversation_banquette",
			"balcony_alcove_bench",
			"drinks_table",
			"parcel_trolley",
		),
	),
	(
		"lobby_services",
		"opera_house_lobby_services_kit_2026-07-21.png",
		4,
		4,
		(
			"ticket_kiosk",
			"ticket_token_pedestal",
			"coat_check_counter",
			"umbrella_parcel_check",
			"flower_kiosk",
			"sweets_counter",
			"lemonade_water_cart",
			"program_fan_rack",
			"usher_station",
			"lost_found_chest",
			"drinking_fountain",
			"handwashing_bubble_markers",
			"first_aid_cabinet",
			"child_cloak_shelf",
			"florist_cart",
			"cleaning_trolley",
		),
	),
	(
		"lobby_decor",
		"opera_house_lobby_architectural_decor_kit_2026-07-21.png",
		4,
		4,
		(
			"electric_ember_fireplace",
			"costume_vitrine",
			"prop_vitrine",
			"shell_muse_sculpture",
			"fan_shell_mirror",
			"window_drapes",
			"wall_panel",
			"cove_inside_corner",
			"ceiling_medallion",
			"floor_urn_fronds",
			"numeral_free_lobby_clock",
			"terrazzo_pearl_rosette",
			"carpet_junction_set",
			"balcony_alcove_bench",
			"arched_landing_connector",
			"accessibility_ramp",
		),
	),
	(
		"upper_access",
		"opera_house_upper_floor_access_kit_2026-07-21.png",
		4,
		4,
		(
			"stair_gate_locked",
			"stair_gate_open",
			"balcony_gate_locked",
			"balcony_gate_open",
			"bubble_lift_locked",
			"bubble_lift_ready",
			"pearl_totem_empty",
			"pearl_totem_full",
			"floor_selector_ground",
			"floor_selector_middle",
			"floor_selector_full",
			"act_portal_locked",
			"act_portal_open",
			"shell_clasp_closed",
			"shell_clasp_open",
			"unlock_effect",
		),
	),
	(
		"stage",
		"opera_house_stage_backstage_kit_2026-07-21.png",
		4,
		4,
		(
			"elliptical_proscenium",
			"house_curtain_states",
			"stage_apron_footlights",
			"orchestra_pit",
			"orchestra_bench",
			"side_box",
			"scenic_backdrop",
			"rolling_wing_flats",
			"follow_spotlight",
			"fly_rail_wall",
			"counterweight_cart",
			"backstage_crates",
			"costume_rack",
			"backstage_worktable",
			"callboard_clock_sconce",
			"podium_music_stand",
		),
	),
	(
		"floor1",
		"opera_house_floor1_act_props_2026-07-21.png",
		4,
		4,
		(
			"cake_trio",
			"mixing_bowl_whisk",
			"recipe_pictogram_chef_hat",
			"shell_oven",
			"topping_set",
			"detective_clue_trio",
			"treasure_tiara",
			"magnifier_searchlight",
			"dance_floor_tiles",
			"tutu_mirror_ball",
			"candy_press",
			"candy_gauge",
			"candy_shelf",
			"curtain_dragon",
			"curtain_slot_set",
			"sparkle_bubble_confetti",
		),
	),
	(
		"floor2",
		"opera_house_floor2_act_props_2026-07-21.png",
		4,
		4,
		(
			"starfish_emotion_pair",
			"stethoscope",
			"thermometer_heart_effects",
			"bandage_set",
			"meadow_parallax",
			"piggy_pose_set",
			"snack_basket",
			"barn_mud_set",
			"boxing_corner",
			"gloves_belt",
			"bell_progress_drum",
			"hat_trio",
			"bunny_fish_pose_set",
			"wand_ribbon_effects",
			"phantom_puppet",
			"lantern_beam_bow_set",
		),
	),
	(
		"floor3",
		"opera_house_floor3_act_props_2026-07-21.png",
		4,
		4,
		(
			"paint_pot_set",
			"brush_action_set",
			"sunrise_reveal_set",
			"artist_costume_set",
			"bubble_tank",
			"pearl_rocket",
			"pipe_trio",
			"ghost_engine_set",
			"opera_kart",
			"finish_flag_gantry",
			"grandstand_banner",
			"microphone",
			"dance_pose_frame",
			"shell_glasses_cape",
			"maestro_puppet",
			"finale_podium_effects",
		),
	),
	(
		"crest",
		"opera_house_crest_wayfinding_kit_2026-07-21.png",
		4,
		4,
		(
			"chef",
			"detective",
			"ballerina",
			"candy",
			"dragon",
			"doctor",
			"farmer",
			"boxer",
			"magician",
			"phantom",
			"painter",
			"engineer",
			"racer",
			"singer",
			"maestro",
			"house",
		),
	),
)


def normalize_sheet(sheet_path: Path) -> None:
	"""Keep every concept image inside the repository's 1024px ceiling."""
	with Image.open(sheet_path) as source:
		if max(source.size) <= 1024:
			return
		scale = 1024.0 / max(source.size)
		size = (round(source.width * scale), round(source.height * scale))
		normalized = source.resize(size, Image.Resampling.LANCZOS)
		normalized.save(sheet_path, optimize=True)


def slice_sheet(sheet_path: Path, prefix: str, columns: int, rows: int,
		names: tuple[str, ...]) -> None:
	if len(names) != columns * rows:
		raise ValueError(f"{sheet_path.name} needs {columns * rows} names")
	with Image.open(sheet_path) as source:
		column_edges = tuple(round(column * source.width / columns)
			for column in range(columns + 1))
		row_edges = tuple(round(row * source.height / rows)
			for row in range(rows + 1))
		for index, name in enumerate(names):
			row, column = divmod(index, columns)
			box = (
				column_edges[column],
				row_edges[row],
				column_edges[column + 1],
				row_edges[row + 1],
			)
			card = source.crop(box)
			card.save(OUTPUT / f"opera_{prefix}_{name}.png", optimize=True)


def write_ledger() -> None:
	LEDGER.parent.mkdir(parents=True, exist_ok=True)
	with LEDGER.open("w", newline="", encoding="utf-8") as ledger_file:
		writer = csv.writer(ledger_file)
		writer.writerow((
			"asset_id",
			"family",
			"display_name",
			"score_out_of_5",
			"status",
			"prototype_card",
			"source_sheet",
		))
		for prefix, sheet_name, _columns, _rows, names in SHEET_SPECS:
			for name in names:
				writer.writerow((
					f"opera_{prefix}_{name}",
					prefix,
					name.replace("_", " ").title(),
					f"{SCORES[prefix]:.1f}",
					"accepted",
					f"assets_src/concepts/opera_house_flat/cards/opera_{prefix}_{name}.png",
					f"assets_src/concepts/opera_house_flat/{sheet_name}",
				))


def main() -> None:
	OUTPUT.mkdir(parents=True, exist_ok=True)
	for sheet_name in SHEETS:
		normalize_sheet(SOURCE / sheet_name)
	card_count = 0
	for prefix, sheet_name, columns, rows, names in SHEET_SPECS:
		slice_sheet(SOURCE / sheet_name, prefix, columns, rows, names)
		card_count += len(names)
	write_ledger()
	print(f"OPERA_HOUSE_FLAT|sheets={len(SHEETS)}|cards={card_count}")


if __name__ == "__main__":
	main()
