#!/usr/bin/env python3
"""Authoritative specs for the additive Pearl Castle interaction v3 pack.

V2 remains immutable placement/runtime evidence. This module is the single
source of truth for 38 additive, complete-object state sheets. Positions are
art pixels: Main Hall stores visual centres on its 3344x941 logical canvas;
the seven 1024x576 rooms store top-left placement.
"""

from __future__ import annotations

from collections import Counter
from typing import Any


STATEFUL_8 = list(range(8))
RUNTIME_CELL_SIZE = {
    "main_hall": 192,
    "opera_hall": 224,
    "kitchen": 192,
    "library": 224,
    "playroom": 256,
    "craft_room": 256,
    "mermaid_pool": 256,
    "bubble_bath": 256,
}


def ellipse(
    role: str,
    center: tuple[float, float],
    radius: tuple[float, float],
    **extra: Any,
) -> dict[str, Any]:
    return {
        "role": role,
        "shape": "ellipse",
        "center": list(center),
        "radius": list(radius),
        **extra,
    }


def polygon(
    role: str,
    points: list[tuple[float, float]],
    **extra: Any,
) -> dict[str, Any]:
    return {
        "role": role,
        "shape": "polygon",
        "points": [list(point) for point in points],
        **extra,
    }


def s(
    room: str,
    item: str,
    name: str,
    position: tuple[float, float],
    placement: tuple[float, float],
    action: str,
    sound: str,
    z: float,
    *,
    duration: float = 0.13,
    pitch: float = 1.0,
    anchor: str = "bottom_center",
    physics: str = "none",
    pivot: tuple[float, float] = (0.5, 0.5),
    physics_angle: float = 0.0,
    physics_impulse_scale: float = 1.0,
    water: list[dict[str, Any]] | None = None,
    timeline: list[int] | None = None,
    hotspot: tuple[float, float] | None = None,
    offset: tuple[float, float] | None = None,
    color: tuple[float, float, float] = (0.72, 0.90, 1.0),
) -> dict[str, Any]:
    hotspot = hotspot or placement
    if offset is None:
        offset = (
            (-hotspot[0] * 0.5, -hotspot[1] * 0.5)
            if room == "main_hall"
            else (0.0, 0.0)
        )
    timeline_sequence = list(timeline or STATEFUL_8)
    return {
        "id": f"{room}_{item}",
        "room": room,
        "item": item,
        "name": name,
        "position": list(position),
        "position_mode": "center" if room == "main_hall" else "top_left",
        "placement_size": list(placement),
        "runtime_center_offset": [placement[0] * 0.5, placement[1] * 0.5],
        "hall_center_offset": [0.0, 0.0],
        "hotspot_size": list(hotspot),
        "hotspot_offset": list(offset),
        "z": z,
        "color": list(color),
        "semantic_action": action,
        "sound": sound,
        "sound_frame": 0,
        "pitch": pitch,
        "frame_duration_seconds": duration,
        "authored_frame_count": 8,
        "timeline_sequence": timeline_sequence,
        "timeline_frame_count": len(timeline_sequence),
        "rest_frame": 0,
        "grid": [4, 2],
        "anchor_mode": anchor,
        "runtime_cell_size": RUNTIME_CELL_SIZE[room],
        "physics_mode": physics,
        "physics_pivot": list(pivot),
        "physics_max_angle_radians": physics_angle,
        "physics_impulse_scale": physics_impulse_scale,
        "water_layers": water or [],
        "render_mode": "generated_full_object_states",
        "primary_animation_is_overlay": False,
    }


ADDITIONS: list[dict[str, Any]] = [
    # Main Hall: +7.
    s("main_hall", "shell_clock", "Royal shell clock", (920, 190),
      (150, 210), "open_clock_and_chime", "assets/audio/chime.ogg", 0.70,
      duration=0.14, anchor="center", color=(1.0, 0.82, 0.48)),
    s("main_hall", "visitor_bell", "Pearl visitor bell", (1518, 185),
      (110, 190), "pull_bell_cord_and_ring", "assets/audio/chime.ogg", 0.71,
      duration=0.12, pitch=1.18, anchor="top_center",
      hotspot=(112, 190), offset=(-56, -95),
      color=(1.0, 0.76, 0.40)),
    s("main_hall", "left_pearl_vitrine", "Crown pearl vitrine", (1160, 170),
      (150, 190), "open_vitrine_and_raise_crown",
      "assets/audio/castle/light_switch.ogg", 0.69, anchor="center",
      color=(0.66, 0.94, 1.0)),
    s("main_hall", "right_pearl_vitrine", "Compass pearl vitrine",
      (2255, 170), (150, 190), "open_vitrine_and_reveal_compass",
      "assets/audio/castle/light_switch.ogg", 0.69, anchor="center",
      color=(0.68, 0.90, 1.0)),
    s("main_hall", "banner_left", "Royal pearl banner", (1810, 150),
      (190, 210), "unroll_and_rewind_banner",
      "assets/audio/castle/curtain_swish.ogg", 0.68, anchor="top_center",
      color=(1.0, 0.68, 0.86)),
    s("main_hall", "fern_planter", "Pearl fern planter", (920, 530),
      (170, 150), "unfurl_and_fold_fern_fronds",
      "assets/audio/castle/craft_brush.ogg", 1.15, duration=0.115,
      color=(0.48, 0.90, 0.70)),
    s("main_hall", "chest_bench", "Royal chest bench", (2302.5, 530),
      (180, 135), "unlock_open_and_close_bench",
      "assets/audio/castle/oven_door.ogg", 1.18, duration=0.15,
      color=(0.88, 0.72, 1.0)),

    # Opera Hall: +4.
    s("opera_hall", "shell_piano", "Shell piano", (92, 300), (230, 155),
      "open_piano_lid_and_play_keys", "assets/audio/castle/toy_blocks.ogg",
      1.05, duration=0.105, color=(1.0, 0.66, 0.82)),
    s("opera_hall", "coral_harp", "Coral concert harp", (795, 190),
      (150, 230), "pluck_harp_strings_and_rebound", "assets/audio/chime.ogg",
      0.84, duration=0.095, pitch=1.22, color=(1.0, 0.76, 0.42)),
    s("opera_hall", "conductor_podium", "Conductor podium", (310, 350),
      (145, 185), "lift_baton_and_turn_score_page",
      "assets/audio/castle/page_flip.ogg", 0.88, duration=0.105,
      color=(0.82, 0.70, 1.0)),
    s("opera_hall", "costume_trunk", "Shell costume trunk", (820, 430),
      (165, 120), "unlatch_trunk_and_lift_costume",
      "assets/audio/castle/oven_door.ogg", 1.16, duration=0.14,
      color=(1.0, 0.62, 0.80)),

    # Royal Kitchen: +7.
    s("kitchen", "seafoam_kettle", "Seafoam kettle", (500, 225),
      (145, 145), "tilt_kettle_and_pour_into_cup",
      "assets/audio/castle/faucet_water.ogg", 1.10, duration=0.15, water=[
          polygon("stream", [(0.5655, 0.6429), (0.5774, 0.6667),
                             (0.5295, 0.8571), (0.4700, 0.8571)],
                  points_frames=[
                      [(0.4405, 0.7262), (0.4524, 0.7440), (0.3509, 0.8631), (0.2914, 0.8631)],
                      [(0.4286, 0.7262), (0.4405, 0.7381), (0.3665, 0.8631), (0.3070, 0.8631)],
                      [(0.4345, 0.6488), (0.4464, 0.7321), (0.3632, 0.8631), (0.3037, 0.8631)],
                      [(0.3869, 0.7440), (0.3988, 0.7619), (0.3672, 0.8631), (0.3076, 0.8631)],
                      [(0.5655, 0.6429), (0.5774, 0.6667), (0.5295, 0.8571), (0.4700, 0.8571)],
                      [(0.4167, 0.6310), (0.4286, 0.7143), (0.3613, 0.8631), (0.3017, 0.8631)],
                      [(0.4226, 0.7083), (0.4345, 0.7321), (0.3559, 0.8631), (0.2964, 0.8631)],
                      [(0.4226, 0.7143), (0.4345, 0.7262), (0.3572, 0.8631), (0.2976, 0.8631)],
                  ], active_frames=[4], stream=True, z_offset=0.010,
                  render_priority=2, flow_start=0.28),
          ellipse("cup_fill", (0.50, 0.87), (0.09, 0.02),
                  active_frames=[4], z_offset=0.009, render_priority=1,
                  flow_start=0.42),
      ], timeline=[0, 1, 2, 3, 4, 4, 4, 5, 6, 7],
      color=(0.50, 0.92, 0.82)),
    s("kitchen", "soup_pot", "Shell soup pot", (300, 205), (155, 135),
      "lift_pot_lid_and_reveal_soup", "assets/audio/castle/oven_door.ogg",
      1.07, duration=0.14, color=(0.42, 0.88, 0.82)),
    s("kitchen", "cookie_jar", "Pearl cookie jar", (865, 195), (110, 135),
      "twist_jar_lid_and_raise_cookie", "assets/audio/castle/toy_blocks.ogg",
      0.91, duration=0.12, hotspot=(112, 135), offset=(-1, 0),
      color=(1.0, 0.72, 0.72)),
    s("kitchen", "cutlery_drawer", "Pearl cutlery drawer", (74, 356),
      (185, 105), "pull_drawer_and_rock_spoon",
      "assets/audio/castle/pan_clang.ogg", 1.28, duration=0.12,
      hotspot=(185, 112), offset=(0, -3.5),
      color=(0.52, 0.88, 0.82)),
    s("kitchen", "ladle_rack", "Shell ladle rack", (450, 35), (190, 155),
      "swing_ladles_on_hooks", "assets/audio/castle/pan_clang.ogg", 0.86,
      duration=0.105, anchor="top_center",
      color=(1.0, 0.70, 0.34)),
    s("kitchen", "serving_tureen", "Royal serving tureen", (680, 350),
      (145, 120), "lift_tureen_lid_and_reveal_soup",
      "assets/audio/castle/oven_door.ogg", 1.04, duration=0.14,
      color=(1.0, 0.68, 0.82)),
    s("kitchen", "shell_cupboard", "Shell cup cupboard", (840, 326),
      (160, 155), "open_cupboard_and_settle_cups",
      "assets/audio/castle/oven_door.ogg", 1.24, duration=0.14,
      color=(0.48, 0.86, 0.80)),

    # Library: +4.
    s("library", "rolling_ladder", "Rolling library ladder", (820, 90),
      (135, 315), "release_brake_and_roll_ladder",
      "assets/audio/castle/toy_blocks.ogg", 0.86, duration=0.12,
      color=(0.88, 0.68, 0.42)),
    s("library", "secret_panel", "Secret story panel", (610, 92),
      (200, 245), "pull_book_and_open_secret_panel",
      "assets/audio/castle/page_flip.ogg", 0.78, duration=0.14,
      anchor="center", color=(0.78, 0.70, 1.0)),
    s("library", "quill_set", "Pearl quill set", (620, 332), (145, 125),
      "dip_quill_write_and_return", "assets/audio/castle/craft_brush.ogg",
      1.34, duration=0.105, color=(0.62, 0.86, 1.0)),
    s("library", "telescope", "Shell telescope", (790, 390), (150, 180),
      "unclasp_extend_and_focus_telescope",
      "assets/audio/castle/light_switch.ogg", 1.08, duration=0.12,
      color=(1.0, 0.78, 0.42)),

    # Stuffie Playroom: +4.
    s("playroom", "toy_chest", "Stuffie toy chest", (650, 445), (175, 125),
      "unlatch_chest_and_peek_stuffie",
      "assets/audio/castle/toy_blocks.ogg", 1.30, duration=0.13,
      color=(1.0, 0.64, 0.80)),
    s("playroom", "rocking_horse", "Pearl rocking horse", (790, 315),
      (185, 185), "rock_horse_forward_and_back",
      "assets/audio/hop_boing.ogg", 1.18, duration=0.095,
      physics="hinge_z", pivot=(0.5, 0.82), physics_angle=0.035,
      physics_impulse_scale=0.28, color=(0.68, 0.88, 1.0)),
    s("playroom", "xylophone", "Rainbow shell xylophone", (445, 368),
      (190, 100), "press_xylophone_keys_in_sequence",
      "assets/audio/chime.ogg", 1.38, duration=0.085, pitch=1.30,
      hotspot=(190, 112), offset=(0, -6),
      color=(1.0, 0.74, 0.42)),
    s("playroom", "dollhouse", "Pearl dollhouse", (650, 40), (190, 240),
      "unlatch_and_open_dollhouse", "assets/audio/castle/oven_door.ogg", 0.82,
      duration=0.14, color=(1.0, 0.68, 0.86)),

    # Craft Room: +4.
    s("craft_room", "sewing_machine", "Shell sewing machine", (540, 390),
      (200, 155), "turn_wheel_stitch_and_feed_cloth",
      "assets/audio/castle/craft_brush.ogg", 1.20, duration=0.095,
      color=(0.54, 0.90, 0.84)),
    s("craft_room", "scissors", "Pearl craft scissors", (320, 465),
      (155, 100), "open_scissors_and_cut_ribbon",
      "assets/audio/castle/ribbon_roll.ogg", 1.36, duration=0.095,
      hotspot=(155, 112), offset=(0, -6),
      color=(0.82, 0.72, 1.0)),
    s("craft_room", "stamp_press", "Shell stamp press", (750, 292),
      (170, 175), "lower_stamp_and_emboss_card",
      "assets/audio/castle/toy_blocks.ogg", 1.22, duration=0.11,
      color=(1.0, 0.72, 0.42)),
    s("craft_room", "bead_jar", "Pearl bead jar", (875, 170), (110, 145),
      "open_bead_jar_and_lift_strand",
      "assets/audio/castle/ribbon_roll.ogg", 0.94, duration=0.11,
      hotspot=(112, 145), offset=(-1, 0),
      color=(1.0, 0.66, 0.84)),

    # Mermaid Pool: +4.
    s("mermaid_pool", "waterwheel", "Pearl pool waterwheel", (72, 175),
      (195, 230), "open_gate_and_turn_waterwheel",
      "assets/audio/castle/bubble_water.ogg", 0.86, duration=0.15,
      anchor="center", water=[
          polygon("wheel_feed", [(0.46, 0.25), (0.54, 0.25),
                                (0.56, 0.68), (0.46, 0.68)],
                  stream=True, z_offset=0.010, render_priority=2,
                  flow_start=0.16),
          ellipse("paddle_splash", (0.50, 0.78), (0.28, 0.055),
                  z_offset=0.009, render_priority=1, flow_start=0.35),
      ], color=(0.48, 0.90, 1.0)),
    s("mermaid_pool", "sailboat", "Pearl pool sailboat", (700, 225),
      (165, 125), "raise_sail_and_float_boat",
      "assets/audio/castle/bubble_water.ogg", 2.08, duration=0.11,
      anchor="center", physics="buoyant", pivot=(0.5, 0.58), water=[
          ellipse("ripple", (0.50, 0.78), (0.40, 0.070),
                  z_offset=-0.010, render_priority=0, flow_start=0.08),
      ], color=(0.64, 0.88, 1.0)),
    s("mermaid_pool", "buoy_bell", "Pearl buoy bell", (870, 205),
      (105, 145), "bob_buoy_and_ring_bell", "assets/audio/chime.ogg", 2.10,
      duration=0.095, pitch=1.20, anchor="center",
      hotspot=(112, 145), offset=(-3.5, 0), water=[
          ellipse("ripple", (0.50, 0.79), (0.39, 0.065),
                  z_offset=-0.010, render_priority=0, flow_start=0.08),
      ], color=(1.0, 0.74, 0.40)),
    s("mermaid_pool", "dock_chest", "Pool dock chest", (270, 410),
      (170, 120), "unlatch_chest_and_unroll_map",
      "assets/audio/castle/page_flip.ogg", 2.22, duration=0.14,
      color=(0.84, 0.70, 1.0)),

    # Bubble Bath: +4.
    s("bubble_bath", "shell_shower", "Shell bath shower", (810, 285),
      (190, 285), "turn_shower_control_and_run_water",
      "assets/audio/castle/faucet_water.ogg", 0.78, duration=0.15,
      anchor="top_center", water=[
          polygon("shower_stream", [(0.7155, 0.3247), (0.7672, 0.3333),
                                    (0.6379, 0.5115), (0.5948, 0.5058)],
                  points_frames=[
                      [(0.6000, 0.2800), (0.6400, 0.2900), (0.6100, 0.5100), (0.5700, 0.5100)],
                      [(0.6300, 0.2900), (0.6700, 0.3000), (0.6200, 0.5100), (0.5800, 0.5100)],
                      [(0.7000, 0.3100), (0.7500, 0.3200), (0.6400, 0.5100), (0.5900, 0.5100)],
                      [(0.7200, 0.3200), (0.7700, 0.3300), (0.6400, 0.5100), (0.5900, 0.5100)],
                      [(0.7155, 0.3247), (0.7672, 0.3333), (0.6379, 0.5115), (0.5948, 0.5058)],
                      [(0.7200, 0.3200), (0.7700, 0.3300), (0.6400, 0.5100), (0.5900, 0.5100)],
                      [(0.6300, 0.2900), (0.6700, 0.3000), (0.6200, 0.5100), (0.5800, 0.5100)],
                      [(0.6000, 0.2800), (0.6400, 0.2900), (0.6100, 0.5100), (0.5700, 0.5100)],
                  ], active_frames=[4], stream=True, z_offset=0.010,
                  render_priority=2, flow_start=0.18),
          ellipse("tub_entry", (0.60, 0.52), (0.15, 0.018),
                  active_frames=[4], z_offset=0.009, render_priority=1,
                  flow_start=0.34),
      ], timeline=[0, 1, 2, 3, 4, 4, 4, 5, 6, 7],
      color=(0.56, 0.90, 1.0)),
    s("bubble_bath", "vanity_cupboard", "Pearl vanity cupboard", (430, 315),
      (185, 150), "open_vanity_and_reveal_towels",
      "assets/audio/castle/oven_door.ogg", 1.20, duration=0.14,
      color=(1.0, 0.68, 0.84)),
    s("bubble_bath", "soap_pump", "Pearl soap pump", (625, 230),
      (95, 140), "press_soap_pump_and_dispense_bead",
      "assets/audio/castle/duck_squeak.ogg", 1.02, duration=0.10, pitch=1.16,
      hotspot=(112, 140), offset=(-8.5, 0),
      color=(0.66, 0.92, 0.88)),
    s("bubble_bath", "towel_spool", "Shell towel spool", (0, 335),
      (115, 225), "turn_spool_unroll_and_rewind_towel",
      "assets/audio/castle/ribbon_roll.ogg", 0.84, duration=0.12,
      anchor="top_center", color=(0.82, 0.70, 1.0)),
]


def validate_specs() -> None:
    expected = {
        "main_hall": 7,
        "opera_hall": 4,
        "kitchen": 7,
        "library": 4,
        "playroom": 4,
        "craft_room": 4,
        "mermaid_pool": 4,
        "bubble_bath": 4,
    }
    if len(ADDITIONS) != 38:
        raise ValueError(f"expected 38 additive assets, got {len(ADDITIONS)}")
    ids = [entry["id"] for entry in ADDITIONS]
    if len(ids) != len(set(ids)):
        raise ValueError("additive asset ids are not unique")
    counts = Counter(entry["room"] for entry in ADDITIONS)
    if dict(counts) != expected:
        raise ValueError(f"room counts {dict(counts)} != {expected}")
    if sum(entry["physics_mode"] != "none" for entry in ADDITIONS) != 2:
        raise ValueError("v3 must add exactly two mechanically valid Jolt fixtures")
    if sum(bool(entry["water_layers"]) for entry in ADDITIONS) != 5:
        raise ValueError("v3 must add exactly five object-local water fixtures")
    for entry in ADDITIONS:
        timeline = entry["timeline_sequence"]
        if not 4 <= len(timeline) <= 12:
            raise ValueError(f"{entry['id']}: timeline is outside 4-12 frames")
        if any(frame not in STATEFUL_8 for frame in timeline):
            raise ValueError(f"{entry['id']}: timeline references a missing state")
        if set(timeline) != set(STATEFUL_8):
            raise ValueError(f"{entry['id']}: timeline skips an authored state")
        if entry["runtime_cell_size"] * 4 > 1024:
            raise ValueError(f"{entry['id']}: runtime sheet exceeds 1024")
        if any(dimension < 112 for dimension in entry["hotspot_size"]):
            raise ValueError(
                f"{entry['id']}: hotspot must be at least 112x112"
            )


validate_specs()


if __name__ == "__main__":
    print(f"castle interaction v3 specs: {len(ADDITIONS)} additions")
    for room, count in Counter(entry["room"] for entry in ADDITIONS).items():
        print(f"  {room}: +{count}")
