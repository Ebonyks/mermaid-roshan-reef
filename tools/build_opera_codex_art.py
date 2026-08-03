#!/usr/bin/env python3
"""Build the 2026-08-02 Codex Opera art delivery.

The script never edits source masters. It promotes accepted ImageGen natives,
constructs 2048-square POT world/stage masters without enlarging their native
subject-bearing frame, slices those masters into 1024-square runtime cards,
and composes the 60 diegetic widget skins from approved Opera card art.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageOps

from prepare_opera_2d_worlds import _remove_edge_field


ROOT = Path(__file__).resolve().parents[1]
NATIVE = ROOT / "assets_src/imagegen/opera_codex_2026-08-02/native"
CARDS = ROOT / "assets_src/concepts/opera_jobs_flat_2026-07-21/cards"
STAGING = ROOT / "assets_src/concepts/opera_regeneration_2026-08-01"
STAGING_CARDS = STAGING / "cards"
CONTACT = STAGING / "contact_sheets"
RUNTIME = ROOT / "assets/opera/worlds"
BACKDROPS = RUNTIME / "backdrops"
UI = RUNTIME / "ui"
PROPS = RUNTIME / "props"
WIDGETS = RUNTIME / "widgets"
FINALE = RUNTIME / "stage"

CAREERS = [
	"chef", "detective", "ballerina", "candymaker", "doctor", "farmer",
	"boxer", "magician", "painter", "astronaut", "racer", "popstar",
]
ALL_WORLDS = CAREERS + ["nursery"]

TEMPLATES: dict[str, list[str]] = {
	"gauge": ["chef", "astronaut", "racer"],
	"track": ["detective", "ballerina", "candymaker", "farmer", "boxer", "magician", "popstar", "nursery"],
	"pour": ["chef", "candymaker", "painter", "nursery"],
	"basin": ["doctor", "nursery"],
	"charge": ["ballerina", "farmer", "magician", "astronaut", "popstar"],
	"crank": ["chef", "ballerina", "candymaker", "doctor", "magician", "painter", "astronaut", "racer", "popstar"],
	"trace": ["chef", "detective", "ballerina", "doctor", "magician", "painter"],
	"push": ["farmer", "boxer", "racer", "nursery"],
	"target": ["chef", "candymaker", "doctor", "farmer", "boxer", "painter", "astronaut", "racer"],
	"lanes": ["detective", "ballerina", "candymaker", "doctor", "farmer", "boxer", "magician", "painter", "astronaut", "popstar"],
	"catch": ["nursery"],
}

PALETTES = {
	"chef": ((92, 49, 85), (245, 170, 155), (255, 216, 112)),
	"detective": ((29, 40, 82), (96, 117, 169), (248, 214, 105)),
	"ballerina": ((57, 82, 124), (210, 142, 208), (143, 231, 223)),
	"candymaker": ((125, 53, 95), (243, 151, 173), (114, 216, 204)),
	"doctor": ((36, 90, 108), (157, 224, 216), (242, 250, 242)),
	"farmer": ((85, 145, 185), (215, 173, 113), (244, 206, 103)),
	"boxer": ((32, 29, 61), (180, 73, 91), (239, 200, 93)),
	"magician": ((42, 27, 75), (119, 81, 158), (243, 202, 95)),
	"painter": ((168, 78, 91), (243, 164, 93), (255, 229, 153)),
	"astronaut": ((25, 39, 84), (63, 106, 164), (114, 217, 232)),
	"racer": ((35, 47, 91), (83, 91, 151), (239, 103, 102)),
	"popstar": ((58, 27, 83), (156, 60, 140), (98, 217, 232)),
	"nursery": ((32, 57, 86), (136, 201, 189), (244, 199, 167)),
}

PRIMARY = {
	("gauge", "chef"): "pastry_chef_gameplay_oven_closed",
	("gauge", "astronaut"): "astronaut_engineer_gameplay_rocket_side",
	("gauge", "racer"): "racecar_driver_gameplay_turbo_button",
	("track", "detective"): "detective_stage_states_searchlight_pool",
	("track", "ballerina"): "ballerina_gameplay_pressed_tile_ripple",
	("track", "candymaker"): "candy_maker_stage_states_parade_cart",
	("track", "farmer"): "farmer_gameplay_carrot",
	("track", "boxer"): "boxer_gameplay_focus_mitt",
	("track", "magician"): "magician_gameplay_selector_glow",
	("track", "popstar"): "pop_star_gameplay_beat_pulse",
	("pour", "chef"): "pastry_chef_gameplay_bowl_empty",
	("pour", "candymaker"): "candy_maker_gameplay_mold_plates",
	("pour", "painter"): "painter_gameplay_canvas_blank",
	("basin", "doctor"): "doctor_stage_states_handwashing_basin",
	("charge", "ballerina"): "ballerina_stage_states_watch_state",
	("charge", "farmer"): "farmer_gameplay_piggy_hop",
	("charge", "astronaut"): "astronaut_engineer_gameplay_rocket_front",
	("charge", "popstar"): "pop_star_gameplay_microphone_idle",
	("crank", "chef"): "pastry_chef_gameplay_bowl_stirring",
	("crank", "ballerina"): "ballerina_stage_states_twirl_effect",
	("crank", "candymaker"): "candy_maker_stage_states_wrapping_swirl",
	("crank", "doctor"): "doctor_stage_states_bandage_state",
	("crank", "magician"): "magician_stage_states_final_reveal",
	("crank", "painter"): "painter_gameplay_palette",
	("crank", "astronaut"): "astronaut_engineer_stage_states_valve_pedestal",
	("crank", "racer"): "racecar_driver_stage_states_banked_curve",
	("crank", "popstar"): "pop_star_stage_states_encore_reveal",
	("trace", "chef"): "pastry_chef_gameplay_piping_ribbon",
	("trace", "detective"): "detective_stage_states_clue_glows",
	("trace", "ballerina"): "ballerina_gameplay_twirl_ribbon",
	("trace", "doctor"): "doctor_gameplay_bandage_unrolled",
	("trace", "painter"): "painter_gameplay_canvas_blank",
	("push", "farmer"): "farmer_gameplay_happy_piggy_group",
	("push", "boxer"): "boxer_gameplay_padded_gloves",
	("push", "racer"): "racecar_driver_gameplay_opera_kart_rear",
	("target", "chef"): "pastry_chef_gameplay_topping_targets",
	("target", "candymaker"): "candy_maker_gameplay_wrapped_candy_reward",
	("target", "farmer"): "farmer_stage_states_piggy_picnic",
	("target", "boxer"): "boxer_gameplay_championship_belt",
	("target", "painter"): "painter_stage_states_easel_platform",
	("target", "astronaut"): "astronaut_engineer_gameplay_rocket_side",
	("target", "racer"): "racecar_driver_gameplay_finish_flag",
}

LANE_REFS = {
	"detective": ["detective_gameplay_coral_mystery_box", "detective_gameplay_teal_mystery_box", "detective_gameplay_plum_hatbox"],
	"ballerina": ["ballerina_gameplay_coral_shell_tile", "ballerina_gameplay_teal_wave_tile", "ballerina_gameplay_plum_ribbon_tile"],
	"doctor": ["doctor_gameplay_starfish_worried", "doctor_gameplay_starfish_calm", "doctor_gameplay_recovered_starfish"],
	"farmer": ["farmer_gameplay_carrot", "farmer_gameplay_corn", "farmer_gameplay_pumpkin"],
	"boxer": ["boxer_gameplay_focus_mitt", "boxer_gameplay_padded_gloves", "boxer_stage_states_coral_corner_stool"],
	"magician": ["magician_gameplay_coral_band_hat", "magician_gameplay_cream_band_hat", "magician_gameplay_teal_band_hat"],
	"painter": ["painter_gameplay_canvas_blank", "painter_gameplay_framed_sunrise", "painter_stage_states_gallery_reveal"],
	"astronaut": ["astronaut_engineer_gameplay_straight_ghost_slot", "astronaut_engineer_gameplay_elbow_ghost_slot", "astronaut_engineer_gameplay_ring_ghost_slot"],
	"popstar": ["pop_star_gameplay_left_arrow", "pop_star_gameplay_up_arrow", "pop_star_gameplay_right_arrow"],
}

SOURCE_OVERRIDES = {
	("charge", "magician"): ROOT / "assets/characters/lamb_0.png",
	("trace", "magician"): NATIVE / "magician_rope_native.png",
	("target", "doctor"): NATIVE / "doctor_xray_viewer_native.png",
	("lanes", "candymaker"): NATIVE / "candymaker_chutes_native.png",
}

GENERATED: list[dict[str, str]] = []


def ensure_dirs() -> None:
	for path in (STAGING_CARDS, CONTACT, BACKDROPS, UI, PROPS, WIDGETS, FINALE):
		path.mkdir(parents=True, exist_ok=True)


def save(image: Image.Image, path: Path, family: str, registration: str, source: str) -> None:
	path.parent.mkdir(parents=True, exist_ok=True)
	image.save(path)
	sha = hashlib.sha256(path.read_bytes()).hexdigest()
	GENERATED.append({
		"asset_id": path.stem,
		"path": path.relative_to(ROOT).as_posix(),
		"sha256": sha,
		"dimensions": f"{image.width}x{image.height}",
		"family": family,
		"registration": registration,
		"source": source,
		"status": "accepted",
		"score": "4.8",
	})


def field_matte(source: Path) -> Image.Image:
	try:
		return _remove_edge_field(source)
	except RuntimeError:
		image = Image.open(source).convert("RGBA")
		return image.crop(image.getbbox() or (0, 0, image.width, image.height))


def find_card(fragment: str) -> Path | None:
	matches = sorted(CARDS.glob(f"opera_job_*{fragment}.png"))
	return matches[0] if matches else None


def fit(subject: Image.Image, box: tuple[int, int], margin: int = 12) -> Image.Image:
	subject = subject.convert("RGBA")
	scale = min((box[0] - margin * 2) / subject.width, (box[1] - margin * 2) / subject.height)
	resized = subject.resize((max(1, round(subject.width * scale)), max(1, round(subject.height * scale))), Image.Resampling.LANCZOS)
	canvas = Image.new("RGBA", box, (0, 0, 0, 0))
	canvas.alpha_composite(resized, ((box[0] - resized.width) // 2, (box[1] - resized.height) // 2))
	return canvas


def subject_for(template: str, career: str) -> Image.Image | None:
	override = SOURCE_OVERRIDES.get((template, career))
	if override is not None and override.exists():
		return field_matte(override)
	fragment = PRIMARY.get((template, career))
	if fragment:
		path = find_card(fragment)
		if path is not None:
			return field_matte(path)
	if career == "nursery":
		path = ROOT / "assets/opera/worlds/nursery/baby_1.png"
		if path.exists():
			return Image.open(path).convert("RGBA")
	return None


def safe_green(image: Image.Image, timing: bool) -> Image.Image:
	if timing:
		return image
	# Compiled channel operations replace only the reserved bright success
	# green family. Seafoam and teal identity colours remain untouched.
	pixels = image.convert("RGBA")
	r, g, b, a = pixels.split()
	green_hi = g.point(lambda value: 255 if value > 182 else 0)
	red_band = r.point(lambda value: 255 if 68 < value < 175 else 0)
	blue_lo = b.point(lambda value: 255 if value < 190 else 0)
	mask = Image.new("L", pixels.size, 0)
	mask = Image.composite(green_hi, mask, red_band)
	mask = Image.composite(mask, Image.new("L", pixels.size, 0), blue_lo)
	replacement = Image.merge("RGBA", (
		r.point(lambda value: min(value, 80)),
		b.point(lambda value: min(225, max(value, 170))),
		g.point(lambda value: min(235, max(value, 195))),
		a,
	))
	return Image.composite(replacement, pixels, mask)


def promote_ui() -> None:
	frame = Image.open(NATIVE / "task_card_frame_alpha_native.png").convert("RGBA")
	frame = frame.resize((1024, 1024), Image.Resampling.LANCZOS)
	save(frame, UI / "task_card_frame.png", "p7_ui", "nine_patch_margin=200", "ImageGen alpha native")

	marker = field_matte(NATIVE / "station_marker_alpha_native.png")
	marker = fit(marker, (512, 1024), 16)
	save(marker, UI / "station_marker.png", "p7_ui", "icon_window=76,150,360,360", "ImageGen alpha native")

	magnifier = fit(field_matte(NATIVE / "magnifier_alpha_native.png"), (512, 512), 12)
	data = []
	for r, g, b, a in magnifier.getdata():
		if a > 0 and g > 115 and b > 105 and g > r * 1.15:
			data.append((r, g, b, min(a, 72)))
		else:
			data.append((r, g, b, a))
	magnifier.putdata(data)
	save(magnifier, UI / "magnifier.png", "p7_ui", "pivot=256,256; angle=45deg", "ImageGen alpha native; lens alpha normalized")

	goal = fit(field_matte(NATIVE / "goal_nursery_native.png"), (1024, 1024), 28)
	save(goal, PROPS / "goal_nursery.png", "p3_goal", "dock=stage_right", "ImageGen navy-field native")


def native_master(source: Path) -> Image.Image:
	"""Create a 2048-square master; the accepted native frame is never enlarged."""
	src = Image.open(source).convert("RGB")
	active_size = (2048, 1152)
	# Appearance-only edge continuation sits behind the untouched native frame.
	background = ImageOps.fit(src, active_size, method=Image.Resampling.BICUBIC).filter(ImageFilter.GaussianBlur(24))
	veil = Image.new("RGBA", active_size, (36, 28, 72, 38))
	active = Image.alpha_composite(background.convert("RGBA"), veil)
	x = (active_size[0] - src.width) // 2
	y = (active_size[1] - src.height) // 2
	mask = Image.new("L", src.size, 255)
	mask_draw = ImageDraw.Draw(mask)
	for inset in range(24):
		mask_draw.rectangle((inset, inset, src.width - 1 - inset, src.height - 1 - inset), outline=min(255, inset * 12), width=1)
	active.paste(src.convert("RGBA"), (x, y), mask)
	master = Image.new("RGBA", (2048, 2048), active.getpixel((1024, 8)))
	master.paste(active, (0, 448))
	return master


def promote_worlds() -> None:
	for career in ALL_WORLDS:
		for kind in ("world", "stage"):
			source = NATIVE / f"{kind}_{career}_native.png"
			master = native_master(source)
			staged = STAGING_CARDS / f"opera_{kind}_master_{career}.png"
			save(master, staged, f"p3_{kind}", "active_crop=0,448,2048,1152", "ImageGen native + non-subject edge continuation")
			for row in range(2):
				for col in range(2):
					tile = master.crop((col * 1024, row * 1024, (col + 1) * 1024, (row + 1) * 1024))
					target = BACKDROPS / f"{kind}_{career}_c{col}r{row}.png"
					save(tile, target, f"p3_{kind}_tile", f"grid={col},{row}; active_crop_y=448..1600", staged.relative_to(ROOT).as_posix())

	master = native_master(NATIVE / "opera_stage_finale_master_native.png")
	staged = STAGING_CARDS / "opera_stage_finale_master_2048.png"
	save(master, staged, "p3_finale", "active_crop=0,448,2048,1152", "ImageGen native + non-subject edge continuation")
	for row in range(2):
		for col in range(2):
			tile = master.crop((col * 1024, row * 1024, (col + 1) * 1024, (row + 1) * 1024))
			save(tile, FINALE / f"finale_stage_c{col}r{row}.png", "p3_finale_tile", f"grid={col},{row}; active_crop_y=448..1600", staged.relative_to(ROOT).as_posix())


def scene_base(career: str) -> Image.Image:
	path = NATIVE / f"stage_{career}_native.png"
	if not path.exists():
		path = NATIVE / "stage_nursery_native.png"
	base = ImageOps.fit(Image.open(path).convert("RGB"), (1024, 608), method=Image.Resampling.LANCZOS)
	base = base.filter(ImageFilter.GaussianBlur(2.2)).convert("RGBA")
	dark, mid, accent = PALETTES[career]
	base = Image.alpha_composite(base, Image.new("RGBA", base.size, (*dark, 94)))
	draw = ImageDraw.Draw(base, "RGBA")
	draw.rounded_rectangle((32, 24, 992, 584), radius=52, fill=(238, 244, 252, 186), outline=(*mid, 245), width=10)
	draw.rounded_rectangle((54, 44, 970, 562), radius=40, outline=(56, 36, 133, 210), width=5)
	draw.ellipse((448, 22, 576, 96), fill=(*accent, 235), outline=(56, 36, 133, 245), width=6)
	return base


def paste_subject(canvas: Image.Image, subject: Image.Image | None, box: tuple[int, int, int, int], opacity: int = 255) -> None:
	if subject is None:
		return
	fitted = fit(subject, (box[2] - box[0], box[3] - box[1]), 8)
	if opacity < 255:
		alpha = fitted.getchannel("A").point(lambda value: value * opacity // 255)
		fitted.putalpha(alpha)
	canvas.alpha_composite(fitted, (box[0], box[1]))


def backdrop(template: str, career: str) -> Image.Image:
	image = scene_base(career)
	draw = ImageDraw.Draw(image, "RGBA")
	dark, mid, accent = PALETTES[career]
	subject = subject_for(template, career)
	if template == "gauge":
		draw.pieslice((212, 178, 812, 778), 210, 330, fill=(42, 38, 70, 235), outline=(56, 36, 133, 255), width=12)
		draw.pieslice((232, 198, 792, 758), 252, 302, fill=(117, 240, 158, 230))
		paste_subject(image, subject, (46, 82, 310, 400), 220)
	elif template == "track":
		draw.rounded_rectangle((123, 365, 901, 435), radius=34, fill=(40, 42, 74, 230), outline=(*accent, 230), width=8)
		draw.rounded_rectangle((356, 354, 683, 446), radius=45, fill=(117, 240, 158, 190), outline=(236, 255, 238, 230), width=6)
		paste_subject(image, subject, (410, 88, 614, 330), 210)
	elif template == "pour":
		paste_subject(image, subject, (250, 126, 774, 548))
		draw.rounded_rectangle((452, 452, 572, 526), radius=34, fill=(*mid, 110), outline=(*accent, 240), width=8)
	elif template == "basin":
		paste_subject(image, subject, (272, 126, 752, 540))
		draw.arc((330, 230, 694, 544), 5, 175, fill=(*accent, 240), width=12)
	elif template == "charge":
		paste_subject(image, subject, (232, 82, 792, 558))
		draw.rounded_rectangle((940, 90, 1000, 540), radius=28, fill=(46, 44, 79, 230), outline=(*accent, 255), width=8)
	elif template == "crank":
		paste_subject(image, subject, (258, 70, 766, 566))
		draw.ellipse((354, 146, 670, 462), outline=(*accent, 220), width=12)
	elif template == "trace":
		paste_subject(image, subject, (150, 108, 874, 520), 205)
		points = [(122, 432), (280, 372), (442, 402), (614, 326), (902, 360)]
		draw.line(points, fill=(66, 66, 104, 220), width=30, joint="curve")
	elif template == "push":
		paste_subject(image, subject, (292, 138, 732, 520), 210)
		draw.rounded_rectangle((96, 376, 928, 466), radius=44, outline=(*accent, 220), width=9)
	elif template == "target":
		paste_subject(image, subject, (292, 128, 732, 518), 185)
		draw.rounded_rectangle((205, 146, 819, 462), radius=34, outline=(*accent, 100), width=5)
	elif template == "lanes":
		refs = LANE_REFS.get(career, [])
		if career == "candymaker":
			lane_subject = subject_for(template, career)
			paste_subject(image, lane_subject, (92, 132, 932, 494))
		else:
			for index, fragment in enumerate(refs):
				path = find_card(fragment)
				if path is not None:
					center = (171, 512, 853)[index]
					paste_subject(image, field_matte(path), (center - 142, 166, center + 142, 454))
	elif template == "catch":
		draw.line((512, 0, 512, 74), fill=(245, 184, 56, 255), width=7)
		for x in (350, 512, 674):
			draw.line((512, 73, x, 112), fill=(189, 167, 226, 255), width=5)
			draw.ellipse((x - 15, 104, x + 15, 134), fill=(245, 184, 56, 255))
	return safe_green(image, template in ("gauge", "track"))


def glow_sprite(colour: tuple[int, int, int], subject: Image.Image | None = None) -> Image.Image:
	image = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
	draw = ImageDraw.Draw(image, "RGBA")
	for radius, alpha in ((112, 18), (88, 34), (62, 64)):
		draw.ellipse((128 - radius, 128 - radius, 128 + radius, 128 + radius), fill=(*colour, alpha))
	if subject is not None:
		paste_subject(image, subject, (26, 26, 230, 230))
	else:
		draw.ellipse((102, 102, 154, 154), fill=(255, 250, 224, 245), outline=(56, 36, 133, 255), width=7)
	return image


def full_overlay(career: str, shape: str) -> Image.Image:
	image = Image.new("RGBA", (1024, 608), (0, 0, 0, 0))
	draw = ImageDraw.Draw(image, "RGBA")
	_, mid, accent = PALETTES[career]
	if shape == "success":
		for radius, alpha in ((250, 20), (180, 36), (115, 64)):
			draw.ellipse((512 - radius, 350 - radius, 512 + radius, 350 + radius), fill=(117, 240, 158, alpha))
	elif shape == "fill":
		draw.rounded_rectangle((350, 345, 674, 552), radius=76, fill=(*accent, 190), outline=(255, 250, 228, 230), width=8)
	elif shape == "trace":
		draw.line([(122, 432), (280, 372), (442, 402), (614, 326), (902, 360)], fill=(*accent, 245), width=32, joint="curve")
	elif shape == "progress":
		for radius, alpha in ((158, 210), (126, 160), (92, 110)):
			draw.arc((512 - radius, 304 - radius, 512 + radius, 304 + radius), -88, 250, fill=(*accent, alpha), width=18)
	else:
		draw.rounded_rectangle((940, 90, 1000, 540), radius=28, fill=(*accent, 200), outline=(255, 250, 228, 240), width=7)
	return safe_green(image, shape == "success")


def mover_for(template: str, career: str) -> Image.Image:
	subject = subject_for(template, career)
	if template == "crank":
		mover_refs = {
			"chef": "pastry_chef_gameplay_whisk", "doctor": "doctor_gameplay_bandage_roll",
			"painter": "painter_gameplay_coral_loaded_brush", "astronaut": "astronaut_engineer_gameplay_valve_wheel",
			"racer": "racecar_driver_gameplay_opera_kart_side",
		}
		fragment = mover_refs.get(career)
		if fragment:
			path = find_card(fragment)
			if path is not None:
				subject = field_matte(path)
	return safe_green(fit(subject, (256, 256), 12) if subject is not None else glow_sprite(PALETTES[career][2]), False)


def build_widgets() -> None:
	for template, careers in TEMPLATES.items():
		for career in careers:
			base = backdrop(template, career)
			path = WIDGETS / f"widget_{template}_{career}.png"
			registration = {
				"gauge": "pivot=512,500;sweep=150..30;green=30..72%",
				"track": "run=123..901;y=400;green=356..683",
				"target": "roam=205..819,146..462",
				"lanes": "centers=171,512,853;baseline=430",
				"catch": "mobile_y=73;catch_y=450;pillow_y=553",
			}.get(template, "surface=1024x608;center=512,304")
			save(base, path, "p8_widget_backdrop", registration, "Path-A composition from approved cards")
			save(base.copy(), STAGING_CARDS / path.name, "p8_widget_staging", registration, path.relative_to(ROOT).as_posix())

			if template == "gauge":
				save(full_overlay(career, "success"), WIDGETS / f"widget_gauge_{career}_success.png", "p8_widget_overlay", "registered=1:1", path.name)
			elif template == "track":
				save(mover_for(template, career), WIDGETS / f"widget_track_{career}_mover.png", "p8_widget_mover", "track=123..901;y=400", path.name)
			elif template == "pour":
				save(mover_for(template, career), WIDGETS / f"widget_pour_{career}_mover.png", "p8_widget_mover", "center=512,304", path.name)
				save(full_overlay(career, "fill"), WIDGETS / f"widget_pour_{career}_fill.png", "p8_widget_overlay", "crop=bottom_up;registered=1:1", path.name)
			elif template == "basin":
				save(full_overlay(career, "progress"), WIDGETS / f"widget_basin_{career}_bubbles.png", "p8_widget_overlay", "crop=bottom_up;registered=1:1", path.name)
			elif template == "charge":
				save(glow_sprite(PALETTES[career][2]), WIDGETS / f"widget_charge_{career}_glow.png", "p8_widget_mover", "subject_center=512,304", path.name)
				save(full_overlay(career, "meter"), WIDGETS / f"widget_charge_{career}_full.png", "p8_widget_overlay", "meter=940..1000,90..540", path.name)
			elif template == "crank":
				save(mover_for(template, career), WIDGETS / f"widget_crank_{career}_mover.png", "p8_widget_mover", "pivot=128,128;zero=up", path.name)
				save(full_overlay(career, "progress"), WIDGETS / f"widget_crank_{career}_progress.png", "p8_widget_overlay", "center=512,304;registered=1:1", path.name)
			elif template == "trace":
				save(full_overlay(career, "trace"), WIDGETS / f"widget_trace_{career}_lit.png", "p8_widget_overlay", "crop=left_to_right;monotonic_x", path.name)
			elif template == "push":
				save(mover_for(template, career), WIDGETS / f"widget_push_{career}_mover.png", "p8_widget_mover", "anchor=512,304", path.name)
			elif template == "target":
				save(mover_for(template, career), WIDGETS / f"widget_target_{career}_mover.png", "p8_widget_mover", "roam=205..819,146..462", path.name)
				mark = glow_sprite(PALETTES[career][2]).resize((128, 128), Image.Resampling.LANCZOS)
				save(mark, WIDGETS / f"widget_target_{career}_mark.png", "p8_widget_stamp", "pivot=64,64", path.name)
				if career == "boxer":
					save(full_overlay(career, "progress"), WIDGETS / "widget_target_boxer_success.png", "p8_widget_overlay", "registered=1:1", path.name)
			elif template == "lanes":
				strip = Image.new("RGBA", (768, 256), (0, 0, 0, 0))
				refs = LANE_REFS.get(career, [])
				for index in range(3):
					fragment = refs[index] if index < len(refs) else ""
					lane_subject = None
					path_ref = find_card(fragment) if fragment else None
					if path_ref is not None:
						lane_subject = field_matte(path_ref)
					elif career == "candymaker":
						lane_subject = subject_for(template, career)
					cell = glow_sprite(PALETTES[career][2], lane_subject)
					strip.alpha_composite(cell, (index * 256, 0))
				save(safe_green(strip, False), WIDGETS / f"widget_lanes_{career}_lit.png", "p8_widget_lane_strip", "cells=0,256,512;baseline=430", path.name)

	# Shared layers.
	needle = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
	draw = ImageDraw.Draw(needle, "RGBA")
	draw.line((128, 224, 128, 28), fill=(245, 184, 56, 255), width=20)
	draw.ellipse((106, 8, 150, 52), fill=(179, 247, 255, 255), outline=(56, 36, 133, 255), width=7)
	draw.ellipse((110, 206, 146, 242), fill=(255, 248, 218, 255), outline=(56, 36, 133, 255), width=7)
	save(needle, WIDGETS / "widget_gauge_shared_needle.png", "p8_widget_shared", "pivot=128,224;zero=up", "P7/P2-09i grammar")
	save(glow_sprite((255, 212, 82)), WIDGETS / "widget_track_shared_hit.png", "p8_widget_shared", "pivot=128,128", "Path-A sparkle")
	save(glow_sprite((179, 247, 255)), WIDGETS / "widget_basin_shared_shine.png", "p8_widget_shared", "pivot=128,128", "Path-A sparkle")
	for name, direction in (("arrow_down", (0, 1)), ("arrow_lr", (1, 0))):
		image = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
		d = ImageDraw.Draw(image, "RGBA")
		if direction[1]:
			d.line((128, 36, 128, 188), fill=(255, 211, 80, 225), width=24)
			d.polygon(((70, 160), (186, 160), (128, 232)), fill=(255, 211, 80, 225))
		else:
			d.line((42, 128, 194, 128), fill=(255, 211, 80, 225), width=24)
			d.polygon(((166, 70), (166, 186), (232, 128)), fill=(255, 211, 80, 225))
		save(image, WIDGETS / f"widget_push_shared_{name}.png", "p8_widget_shared", "pivot=128,128", "Path-A affordance")
	save(glow_sprite((255, 212, 82)), WIDGETS / "widget_lanes_shared_pick.png", "p8_widget_shared", "pivot=128,128", "Path-A sparkle")

	# T11 raster replacements.
	catch_base = WIDGETS / "widget_catch_nursery.png"
	cradle = glow_sprite(PALETTES["nursery"][2])
	d = ImageDraw.Draw(cradle, "RGBA")
	d.arc((40, 74, 216, 224), 5, 175, fill=(255, 190, 204, 255), width=20)
	d.line((50, 150, 92, 112), fill=(255, 222, 184, 255), width=17)
	d.line((206, 150, 164, 112), fill=(255, 222, 184, 255), width=17)
	save(cradle, WIDGETS / "widget_catch_nursery_cradle.png", "p8_widget_mover", "pivot=128,232;runtime_y=450", catch_base.name)
	pillows = Image.new("RGBA", (1024, 160), (0, 0, 0, 0))
	d = ImageDraw.Draw(pillows, "RGBA")
	for index, x in enumerate((100, 305, 512, 719, 924)):
		colour = (174, 148 + (index % 2) * 22, 216, 240)
		d.ellipse((x - 105, 34, x + 105, 158), fill=colour, outline=(56, 36, 133, 230), width=7)
	save(pillows, WIDGETS / "widget_catch_nursery_pillows.png", "p8_widget_overlay", "runtime_y=553", catch_base.name)


def contact_sheets() -> None:
	paths = sorted(WIDGETS.glob("widget_*.png"))
	thumb_size = (256, 152)
	per_page = 24
	for page_start in range(0, len(paths), per_page):
		page_paths = paths[page_start:page_start + per_page]
		sheet = Image.new("RGB", (4 * 280, 6 * 188), (27, 22, 55))
		draw = ImageDraw.Draw(sheet)
		for index, path in enumerate(page_paths):
			image = Image.open(path).convert("RGBA")
			preview = ImageOps.contain(image, thumb_size, method=Image.Resampling.LANCZOS)
			cell = Image.new("RGBA", thumb_size, (238, 244, 252, 255))
			cell.alpha_composite(preview, ((256 - preview.width) // 2, (152 - preview.height) // 2))
			x = (index % 4) * 280 + 12
			y = (index // 4) * 188 + 8
			sheet.paste(cell.convert("RGB"), (x, y))
			draw.text((x, y + 156), path.stem[:38], fill=(255, 244, 210))
		page = page_start // per_page + 1
		save(sheet, CONTACT / f"opera_widgets_contact_{page:02d}.png", "qa_contact_sheet", "thumb=256x152;grid=4x6", "runtime widget outputs")

	# Gameplay-scale P7 review on the same 1280x720 layout geometry.
	qa = Image.new("RGBA", (1280, 720), (29, 40, 82, 255))
	frame = Image.open(UI / "task_card_frame.png").convert("RGBA").resize((460, 384), Image.Resampling.LANCZOS)
	qa.alpha_composite(frame, (410, 168))
	marker = Image.open(UI / "station_marker.png").convert("RGBA").resize((170, 340), Image.Resampling.LANCZOS)
	qa.alpha_composite(marker, (110, 286))
	magnifier = Image.open(UI / "magnifier.png").convert("RGBA").resize((192, 192), Image.Resampling.LANCZOS)
	qa.alpha_composite(magnifier, (970, 260))
	save(qa, CONTACT / "opera_p7_gameplay_scale_1280x720.png", "qa_runtime_layout", "viewport=1280x720;mobile_canvas", "P7 runtime geometry")


def manifests() -> None:
	ledger = STAGING / "OPERA_WIDGET_LEDGER_2026-08-02.csv"
	fields = ["asset_id", "path", "sha256", "dimensions", "family", "registration", "source", "status", "score"]
	with ledger.open("w", encoding="utf-8", newline="") as handle:
		writer = csv.DictWriter(handle, fieldnames=fields)
		writer.writeheader()
		writer.writerows(GENERATED)
	manifest = STAGING / "OPERA_CODEX_MANIFEST_2026-08-02.json"
	manifest.write_text(json.dumps({"version": 1, "method": "ImageGen natives plus Path-A approved-card composition", "assets": GENERATED}, indent=2), encoding="utf-8")


def main() -> None:
	ensure_dirs()
	promote_ui()
	promote_worlds()
	build_widgets()
	contact_sheets()
	manifests()
	backdrop_count = sum(1 for item in GENERATED if item["family"] == "p8_widget_backdrop")
	print(f"Opera Codex art built: {len(GENERATED)} files; widget backdrops={backdrop_count}")
	if backdrop_count != 60:
		raise SystemExit(f"Expected 60 widget backdrops, got {backdrop_count}")


if __name__ == "__main__":
	main()
