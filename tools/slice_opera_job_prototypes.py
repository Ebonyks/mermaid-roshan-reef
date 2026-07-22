#!/usr/bin/env python3
"""Normalize and slice the accepted Opera House job prototype sheets."""

from __future__ import annotations

import csv
from pathlib import Path

from PIL import Image, ImageOps


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets_src" / "concepts" / "opera_jobs_flat_2026-07-21"
OUTPUT = SOURCE / "cards"
LEDGER = ROOT / "audit" / "opera_job_flat_prototype_ledger_2026-07-21.csv"
CONTACT_SHEET = ROOT / "audit" / "opera_job_flat_contact_sheet_2026-07-21.png"
CARD_SIZE = (1024, 1024)

OUTFIT_NAMES = (
	"hero_front_three_quarter",
	"turnaround_side",
	"turnaround_back_three_quarter",
	"signature_action_pose",
	"headwear_views",
	"main_garment_front_back",
	"tail_attachment_front_back",
	"primary_tool_or_accessory",
	"secondary_tool_or_accessory",
	"tertiary_tool_or_accessory",
	"job_crest",
	"material_color_swatches",
	"idle_silhouette",
	"action_silhouette",
	"completion_bow_pose",
	"wardrobe_display",
)

JOBS = {
	"pastry_chef": {
		"scores": (4.7, 4.8, 4.8),
		"gameplay": ("vanilla_layer", "coral_layer", "plum_layer", "recipe_board",
			"bowl_empty", "bowl_calm", "bowl_stirring", "whisk", "oven_closed",
			"oven_open", "cherry_topping", "cream_topping", "chocolate_topping",
			"topping_targets", "finished_cake", "piping_ribbon"),
		"stage": ("pastry_proscenium", "work_counter", "ingredient_shelf",
			"presentation_cart", "topping_pedestals", "recipe_board_stand",
			"oven_alcove", "cake_reveal_table", "frosting_pointer", "stir_effect",
			"frosting_ribbon", "placement_glows", "gentle_retry", "oven_success",
			"cake_reveal", "curtain_call"),
	},
	"detective": {
		"scores": (4.8, 4.8, 4.8),
		"gameplay": ("coral_mystery_box", "teal_mystery_box", "plum_hatbox",
			"cream_trunk", "round_ribbon_box", "tall_prop_crate", "paw_clue",
			"feather_clue", "ribbon_clue", "magnifier", "fish_decoy", "sock_decoy",
			"chest_closed", "chest_open", "pearl_tiara", "clue_complete_medallion"),
		"stage": ("prop_library_proscenium", "archive_shelf", "search_table",
			"six_box_display", "searchlight_pool", "magnifier_pointer", "clue_glows",
			"case_board_empty", "case_board_complete", "box_wiggle", "fish_surprise",
			"chest_pedestal", "gentle_retry", "tiara_reveal", "case_complete_tableau",
			"curtain_call"),
	},
	"ballerina": {
		"scores": (4.8, 4.8, 4.8),
		"gameplay": ("coral_shell_tile", "teal_wave_tile", "plum_ribbon_tile",
			"cream_pearl_tile", "coral_demo_glow", "teal_demo_glow", "plum_demo_glow",
			"cream_demo_glow", "pressed_tile_ripple", "four_tile_floor",
			"example_sequence", "practice_barre", "music_box", "mirror_ball",
			"twirl_ribbon", "sequence_complete"),
		"stage": ("recital_proscenium", "dance_floor", "practice_barre_unit",
			"mirror_panels", "mirror_ball_rig", "coral_wing_curtain", "teal_wing_curtain",
			"spotlight_pool", "watch_state", "repeat_state", "correct_step_ripple",
			"gentle_retry", "twirl_effect", "floor_bloom", "recital_reveal",
			"curtain_call_bouquet"),
	},
	"candy_maker": {
		"scores": (4.7, 4.8, 4.8),
		"gameplay": ("press_machine", "press_open", "press_squish", "timing_gauge",
			"slider_approach", "slider_centered", "coral_round_candy", "teal_shell_candy",
			"plum_wrapped_candy", "cream_heart_candy", "coral_flower_candy",
			"teal_spiral_candy", "plum_bow_candy", "mold_plates", "scoop_and_tongs",
			"wrapped_candy_reward"),
		"stage": ("candy_workshop_proscenium", "conveyor", "candy_hopper",
			"press_platform", "wrapping_station", "seven_slot_shelf", "parade_cart",
			"parade_arch", "timing_pointer", "success_squish", "gentle_retry",
			"wrapping_swirl", "shelf_partial", "shelf_complete", "parade_tableau",
			"curtain_call"),
	},
	"doctor": {
		"scores": (4.8, 4.8, 4.8),
		"gameplay": ("starfish_worried", "starfish_calm", "starfish_happy",
			"stethoscope", "listening_pad", "thermometer_cool", "thermometer_warm",
			"kiss_heart_puff", "bandage_roll", "bandage_unrolled", "bandage_wrap",
			"checkup_tray", "heartbeat_ripple", "guidance_shell", "care_complete_medallion",
			"recovered_starfish"),
		"stage": ("clinic_proscenium", "exam_platform", "tool_trolley",
			"privacy_curtain", "pictogram_cabinet", "handwashing_basin", "waiting_bench",
			"four_step_board", "guidance_pointer", "listening_state", "warmth_state",
			"kiss_state", "bandage_state", "before_after", "recovery_tableau",
			"curtain_call"),
	},
	"farmer": {
		"scores": (4.7, 4.8, 4.8),
		"gameplay": ("piggy_trot_a", "piggy_trot_b", "piggy_hop", "piggy_munch",
			"piggy_fed", "carrot", "apple", "corn", "berries", "pumpkin",
			"vegetable_basket", "toss_arc", "mud_splash", "hay_bale",
			"piggy_target_medallion", "happy_piggy_group"),
		"stage": ("meadow_proscenium", "distant_parallax", "orchard_parallax",
			"flower_parallax", "barn_flat", "fence_segment", "picnic_blanket",
			"mud_puddle", "hay_stack", "toss_pointer", "piggy_approach",
			"vegetable_in_flight", "fed_piggy_hop", "piggy_picnic", "piggy_finale",
			"sunset_curtain_call"),
	},
	"boxer": {
		"scores": (4.8, 4.8, 4.8),
		"gameplay": ("padded_gloves", "focus_mitt", "ring_post_ropes", "ring_corner",
			"shell_bell", "round_lamps", "training_bag", "championship_belt",
			"imp_peek", "imp_bopped", "bubble_puff_impact", "recoil_arcs",
			"punch_medallion", "towel_and_flask", "belt_pedestal", "imp_bow_group"),
		"stage": ("boxing_proscenium", "ring_platform", "coral_corner_stool",
			"teal_corner_stool", "bell_stand", "training_bag_rig", "audience_pennants",
			"round_progress_lights", "glove_pointer", "imp_peek_state", "bop_state",
			"round_complete", "gentle_retry", "belt_reward", "victory_podium",
			"curtain_call"),
	},
	"magician": {
		"scores": (4.7, 4.7, 4.8),
		"gameplay": ("coral_band_hat", "teal_band_hat", "cream_band_hat",
			"hat_open", "bunny_fish_swim", "bunny_fish_peek", "bunny_fish_reveal",
			"pearl_wand", "swap_trail", "crossed_swap_trails", "feint_arc",
			"decoy_bubble_puff", "selector_glow", "hat_start_lineup", "hat_shuffle_lineup",
			"successful_reveal"),
		"stage": ("magic_proscenium", "trick_table", "trick_cabinet",
			"hat_pedestal_rail", "rolling_mirror", "wing_curtains", "spotlight_pool",
			"watch_state", "swap_state", "selector_state", "decoy_state",
			"bunny_fish_reveal", "gentle_retry", "round_complete", "final_reveal",
			"curtain_call"),
	},
	"painter": {
		"scores": (4.8, 4.8, 4.8),
		"gameplay": ("coral_paint_pot", "cream_paint_pot", "plum_paint_pot",
			"coral_loaded_brush", "cream_loaded_brush", "plum_loaded_brush",
			"canvas_blank", "canvas_plum", "canvas_plum_coral", "canvas_finished",
			"color_order_board", "palette", "rinse_cup", "swipe_ribbon",
			"splat_stamp_set", "framed_sunrise"),
		"stage": ("painting_proscenium", "easel_platform", "ordered_paint_pedestal",
			"paint_cart", "drop_cloth", "blank_gallery_wall", "rinse_station",
			"ordered_color_board", "plum_pointer", "paint_carry_trail", "ordered_swipe",
			"gentle_retry", "splat_state", "before_after", "gallery_reveal",
			"curtain_call"),
	},
	"astronaut_engineer": {
		"scores": (4.8, 4.8, 4.8),
		"gameplay": ("bubble_tank", "rocket_side", "rocket_front", "straight_pipe",
			"elbow_pipe", "ring_pipe", "straight_ghost_slot", "elbow_ghost_slot",
			"ring_ghost_slot", "wrong_shape_hover", "straight_fitted", "elbow_fitted",
			"ring_fitted", "valve_wheel", "valve_spin_bubbles", "bubble_launch"),
		"stage": ("launch_proscenium", "launch_pad", "mobile_gantry", "workbench",
			"pipe_wall", "bubble_tank_pedestal", "valve_pedestal", "pressure_lamps",
			"match_pointer", "gentle_return", "pipes_complete", "valve_spin",
			"prelaunch_glow", "bubble_launch", "rocket_reveal", "curtain_call"),
	},
	"racecar_driver": {
		"scores": (4.8, 4.8, 4.8),
		"gameplay": ("opera_kart_front", "opera_kart_side", "opera_kart_rear",
			"steering_wheel", "turbo_button", "zoom_strip_idle", "zoom_strip_active",
			"finish_flag", "course_flag", "shell_trophy", "pit_toolkit",
			"safety_barrier", "bubble_turbo_trail", "steering_arrow", "finish_ribbon",
			"kart_victory_pedestal"),
		"stage": ("grand_prix_proscenium", "starting_arch", "straight_track",
			"banked_curve", "padded_barrier", "pit_cart", "grandstand_flat",
			"progress_lamps", "steering_guidance", "zoom_strip_idle", "zoom_strip_active",
			"bubble_turbo", "finish_state", "lap_complete", "trophy_podium",
			"curtain_call"),
	},
	"pop_star": {
		"scores": (4.8, 4.8, 4.8),
		"gameplay": ("microphone_idle", "microphone_active", "microphone_stand",
			"left_arrow", "right_arrow", "up_arrow", "down_arrow", "dance_sequence",
			"pressed_arrow", "rainbow_rhythm_ribbon", "beat_pulse", "speaker",
			"stage_monitor", "shell_tambourine", "dance_complete", "microphone_finale"),
		"stage": ("concert_proscenium", "pearl_light_frame", "speaker_stacks",
			"catwalk", "rainbow_backdrop", "dance_floor", "microphone_pedestal",
			"glow_stick_rail", "microphone_pointer", "arrow_lane", "rhythm_ripple",
			"gentle_retry", "rainbow_rhythm_state", "arrows_complete", "encore_reveal",
			"curtain_call"),
	},
}


def normalize_sheet(sheet_path: Path) -> None:
	with Image.open(sheet_path) as source:
		if max(source.size) <= 1024:
			return
		scale = 1024.0 / max(source.size)
		size = (round(source.width * scale), round(source.height * scale))
		normalized = source.resize(size, Image.Resampling.LANCZOS)
		normalized.save(sheet_path, optimize=True)


def slice_sheet(sheet_path: Path, prefix: str, names: tuple[str, ...]) -> None:
	if len(names) != 16:
		raise ValueError(f"{sheet_path.name} needs 16 names")
	with Image.open(sheet_path) as source:
		for index, name in enumerate(names):
			row, column = divmod(index, 4)
			box = (
				round(column * source.width / 4),
				round(row * source.height / 4),
				round((column + 1) * source.width / 4),
				round((row + 1) * source.height / 4),
			)
			# Each accepted master is a 4 x 4 design sheet, so its native cell is
			# 256 px.  Export a deterministic 1024 px modeling reference from that
			# exact cell instead of asking a generator to reinterpret the design.
			# This preserves composition, color, silhouette, and state continuity.
			card = source.crop(box).resize(CARD_SIZE, Image.Resampling.LANCZOS)
			card.save(OUTPUT / f"opera_job_{prefix}_{name}.png", optimize=True,
				compress_level=9)


def build_contact_sheet(sheet_paths: list[Path]) -> None:
	canvas = Image.new("RGB", (1024, 1024), (4, 22, 45))
	cell = 1024 // 6
	for index, sheet_path in enumerate(sheet_paths):
		with Image.open(sheet_path) as source:
			thumb = ImageOps.contain(source.convert("RGB"), (cell - 8, cell - 8),
				Image.Resampling.LANCZOS)
			x = (index % 6) * cell + (cell - thumb.width) // 2
			y = (index // 6) * cell + (cell - thumb.height) // 2
			canvas.paste(thumb, (x, y))
	canvas.save(CONTACT_SHEET, optimize=True)


def write_ledger() -> None:
	LEDGER.parent.mkdir(parents=True, exist_ok=True)
	with LEDGER.open("w", newline="", encoding="utf-8") as ledger_file:
		writer = csv.writer(ledger_file)
		writer.writerow(("asset_id", "job", "sheet_type", "display_name",
			"score_out_of_5", "status", "pixel_dimensions", "prototype_card",
			"source_sheet"))
		for job, spec in JOBS.items():
			for sheet_type, names, score in (
				("outfit", OUTFIT_NAMES, spec["scores"][0]),
				("gameplay", spec["gameplay"], spec["scores"][1]),
				("stage_states", spec["stage"], spec["scores"][2]),
			):
				sheet_name = f"{job}_{sheet_type}_sheet_2026-07-21.png"
				for name in names:
					asset_id = f"opera_job_{job}_{sheet_type}_{name}"
					writer.writerow((asset_id, job, sheet_type,
						name.replace("_", " ").title(), f"{score:.1f}", "accepted",
						f"{CARD_SIZE[0]}x{CARD_SIZE[1]}",
						f"assets_src/concepts/opera_jobs_flat_2026-07-21/cards/{asset_id}.png",
						f"assets_src/concepts/opera_jobs_flat_2026-07-21/{sheet_name}"))


def main() -> None:
	OUTPUT.mkdir(parents=True, exist_ok=True)
	accepted_sheets: list[Path] = []
	card_count = 0
	for job, spec in JOBS.items():
		for sheet_type, names in (
			("outfit", OUTFIT_NAMES),
			("gameplay", spec["gameplay"]),
			("stage_states", spec["stage"]),
		):
			sheet_path = SOURCE / f"{job}_{sheet_type}_sheet_2026-07-21.png"
			if not sheet_path.is_file():
				raise FileNotFoundError(sheet_path)
			normalize_sheet(sheet_path)
			slice_sheet(sheet_path, f"{job}_{sheet_type}", names)
			accepted_sheets.append(sheet_path)
			card_count += len(names)
	write_ledger()
	build_contact_sheet(accepted_sheets)
	print(f"OPERA_JOB_FLAT|sheets={len(accepted_sheets)}|cards={card_count}"
		f"|card_px={CARD_SIZE[0]}x{CARD_SIZE[1]}")


if __name__ == "__main__":
	main()
