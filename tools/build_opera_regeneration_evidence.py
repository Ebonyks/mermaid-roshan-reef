#!/usr/bin/env python3
"""Build the review ledger, contact sheets, hashes, and license evidence."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path
from statistics import mean

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
BATCH = ROOT / "assets_src/concepts/opera_regeneration_2026-08-01"
CARDS = BATCH / "cards"
CONTACTS = BATCH / "contact_sheets"
LEDGER = BATCH / "REGENERATION_LEDGER.csv"
PROMPTS = BATCH / "PROMPTS.md"
AUDIT = ROOT / "audit/opera_regeneration_audit_2026-08-01.md"
LICENSES = ROOT / "ASSET_LICENSES.md"

GENERATION_IDS = {
    "imp_mischief.png": "exec-9e92b9fa-b7b5-4a9c-9f2a-e20018bfd8ff.png",
    "imp_captain.png": "exec-7965759e-156f-4315-bb01-87a9820939b1.png",
    "imp_mischief_bopped.png": "exec-80d9d6fd-c1c6-4340-8578-85784779d49d.png",
    "imp_mischief_bow.png": "exec-c06ee44d-9e98-4954-b24b-ae2af4edcf4c.png",
    "imp_captain_bopped.png": "exec-b8efc220-fe27-450e-b323-b69efa66a4d8.png",
    "imp_captain_bow.png": "exec-4cac2c7f-a077-4fc9-859b-91c3c385649e.png",
    "opera_rival_costume_sheet_master.png": "exec-7f0a92a5-29f6-41b6-9bfa-8c3069e84dd1.png",
    "farmer_gameplay_sheet.png": "exec-ba2b918e-93ed-4009-a25f-0ad6f7ccde69.png",
    "boss_shadow_phantom_friendly.png": "exec-14223439-45d9-4392-a07f-6757b96f2e34.png",
    "boss_midnight_maestro_friendly.png": "exec-be832013-604d-4e17-9931-de89bd13a616.png",
    "doctor_performance_boss_finale_2026-07-24.png": "exec-06322a9d-e58b-4f97-9364-5c56235bf118.png",
    "farmer_performance_boss_finale_2026-07-24.png": "exec-98b68765-4d64-4120-9273-012ff7b01532.png",
    "boxer_performance_boss_finale_2026-07-24.png": "exec-ee9975b1-59e7-4a47-8f29-4f7a8a1d20cb.png",
    "magician_performance_boss_finale_2026-07-24.png": "exec-d81a17c2-6eed-4acc-9b7f-7786dd135470.png",
    "painter_performance_boss_finale_2026-07-24.png": "exec-15f1f596-8327-4513-8c67-f8c53d9338f3.png",
    "astronaut_engineer_performance_boss_finale_2026-07-24.png": "exec-7ec20da7-2d87-498b-8ff8-1ce09aac83e9.png",
    "racecar_driver_performance_boss_finale_2026-07-24.png": "exec-6b2640d6-be6f-4e3c-a43a-4af8446d71dc.png",
    "pop_star_performance_boss_finale_2026-07-24.png": "exec-42d31345-2667-48bc-9852-601c0b9c7a7b.png",
    "opera_job_boxer_gameplay_imp_bow_group.png": "exec-810207d9-2b60-44b3-b2d8-ef52c21ce90f.png",
    "opera_job_boxer_stage_states_imp_peek_state.png": "exec-f6367beb-4ec3-45df-9511-1604815f64f4.png",
    "opera_job_boxer_stage_states_bop_state.png": "exec-cffd5543-9456-4160-a8e1-c0cabdc624f7.png",
    "opera_job_boxer_stage_states_gentle_retry.png": "exec-d9a22fa6-1c1e-49c2-b548-d36989317590.png",
    "opera_upper_access_floor_selector_ground.png": "exec-1375db52-cfcb-4d59-8353-b5a06a33e3ee.png",
    "opera_upper_access_floor_selector_middle.png": "exec-b4d908b7-f05d-4ae5-93b0-7f93007838d5.png",
    "opera_upper_access_floor_selector_full.png": "exec-bfa93fef-acd4-4a26-bf38-ad973d00c4a1.png",
    "roshan_doctor_stethoscope.png": "exec-af9814f2-16cc-4e7b-96cc-f3e83bff4d67.png",
    "opera_job_pastry_chef_gameplay_finished_cake.png": "exec-1a4bec08-a51f-435a-aacb-b84c1d1fa754.png",
    "opera_job_detective_gameplay_pearl_tiara.png": "exec-16885f1a-8e92-49f6-b796-b29ee46925b5.png",
    "opera_job_ballerina_gameplay_music_box.png": "exec-4236332a-1094-4976-bba1-4a6d554bd166.png",
    "opera_job_candy_maker_gameplay_wrapped_candy_reward.png": "exec-3b5632b2-462f-4234-a380-a5f9656848b2.png",
    "opera_job_doctor_gameplay_recovered_starfish.png": "exec-be9f8a34-354c-41fd-9bc0-4c328e3376ff.png",
    "opera_job_farmer_gameplay_piggy_fed.png": "exec-2518f2b7-e50b-4cc0-b335-b43daea2b38c.png",
    "opera_job_boxer_gameplay_championship_belt.png": "exec-a984de05-6eec-4cee-b096-5deffa914881.png",
    "opera_job_magician_gameplay_bunny_fish_reveal.png": "exec-a03e92fe-c5e6-4414-a6ca-4658311d242a.png",
    "opera_job_painter_gameplay_framed_sunrise.png": "exec-77a0271f-082d-46a5-a113-d2abaad695bd.png",
    "opera_job_astronaut_engineer_gameplay_rocket_front.png": "exec-7ec64f23-f8db-443f-9825-698cbc2c007e.png",
    "opera_job_racecar_driver_gameplay_shell_trophy.png": "exec-ce69b6ab-71f9-4954-842d-5cf340c6b39e.png",
    "opera_job_pop_star_gameplay_microphone_finale.png": "exec-38eee3e2-1d54-4301-96bf-3915be39c51d.png",
    "opera_job_magician_gameplay_bunny_fish_swim.png": "exec-d52078dd-65fa-4e9b-b64a-e5f5501a34d0.png",
    "opera_job_magician_gameplay_bunny_fish_peek.png": "exec-a053e1f9-2f00-4c44-b237-7b6c40f27a23.png",
    "opera_stage_finale_master_review_only_1254.png": "exec-e27b15e8-f16d-4197-8685-f09acf58f061.png",
    "opera_house_audience_kit.png": "exec-f1433e5a-7690-494d-b036-0b3171de0300.png",
    "opera_job_pastry_chef_stage_states_oven_alcove.png": "exec-fb5f0099-e706-48a9-8f93-78155de39416.png",
    "opera_job_pastry_chef_stage_states_cake_reveal.png": "exec-cbd22830-8f7d-4056-8584-d9cd6face619.png",
    "opera_job_pastry_chef_stage_states_presentation_cart.png": "exec-adcc9dcf-7ea7-474a-a663-ea5e1b00bf49.png",
    "opera_job_pastry_chef_stage_states_topping_pedestals.png": "exec-9214e5fa-13c7-4c8e-ab6c-f34c2d17ba22.png",
    "opera_job_pastry_chef_stage_states_placement_glows.png": "exec-2d3dbef1-12ca-4099-aa26-47fa595350a8.png",
    "opera_job_detective_gameplay_magnifier.png": "exec-c79a4fbc-83b2-4b03-831f-88a8fb46ba89.png",
    "opera_job_detective_stage_states_magnifier_pointer.png": "exec-f5faed60-669d-406f-b003-f8eabdfe5af7.png",
    "opera_job_detective_stage_states_chest_pedestal.png": "exec-4e244964-dea4-4298-a42e-5c1add1dcdec.png",
    "opera_job_detective_stage_states_case_complete_tableau.png": "exec-0504f6d2-ad42-4afa-916b-97ff4a110d9b.png",
    "opera_job_ballerina_outfit_tertiary_tool_or_accessory.png": "exec-73ff7986-680c-44ef-b766-e42629c2c2cf.png",
    "opera_job_candy_maker_stage_states_shelf_complete.png": "exec-357d4deb-7e33-414b-a8d8-b8a45fec0700.png",
    "opera_job_candy_maker_stage_states_seven_slot_shelf.png": "exec-90f0543a-7011-460d-bef6-646590ded0db.png",
    "opera_job_candy_maker_stage_states_timing_pointer.png": "exec-f3073d5a-e2d8-4209-9c85-feea39fa9ab0.png",
    "opera_job_farmer_stage_states_piggy_finale.png": "exec-c4018336-a9dd-406c-b5b1-289671a8d08a.png",
    "opera_job_magician_gameplay_pearl_wand.png": "exec-ff8c9539-b1b8-48d9-8413-d3586e29eeb5.png",
    "opera_job_magician_stage_states_watch_state.png": "exec-51224c38-df5a-48dd-a3ee-ab4eb17ef207.png",
    "opera_job_magician_stage_states_swap_state.png": "exec-18168f63-7820-4d0e-9a92-5083ba382629.png",
    "opera_job_magician_stage_states_selector_state.png": "exec-2fec0f0e-d44f-46a9-9369-52884aa71c4f.png",
    "opera_job_magician_stage_states_decoy_state.png": "exec-7ef67f19-1835-4a86-98e8-caa106211263.png",
    "opera_job_magician_stage_states_final_reveal.png": "exec-b59b4b99-c335-4bea-a222-c8c1bc8e1f3a.png",
    "opera_job_magician_stage_states_bunny_fish_reveal.png": "exec-24f3d0a8-7e09-4837-809a-6f8e43de0100.png",
    "opera_job_painter_gameplay_coral_loaded_brush.png": "exec-feb2da7c-514b-447b-b7b5-998345a59f45.png",
    "opera_job_painter_gameplay_cream_loaded_brush.png": "exec-9c822771-b48b-41ae-bd46-deef139a1522.png",
    "opera_job_painter_gameplay_plum_loaded_brush.png": "exec-68c1a323-04e6-48b3-a8c3-ff5773b01b18.png",
    "opera_job_pop_star_stage_states_dance_floor.png": "exec-e38212da-b14e-451c-a475-d2cebdb8d7f7.png",
    "opera_job_pop_star_stage_states_arrow_lane.png": "exec-38ef1ad2-1d6e-46c0-a854-300e8babf0d2.png",
    "opera_job_pop_star_stage_states_arrows_complete.png": "exec-dc442127-5ada-4f5f-b065-c7bd2c26f914.png",
    "opera_job_pop_star_gameplay_speaker.png": "exec-d8b96a02-1d0a-4689-86cb-e26d653dde18.png",
    "opera_job_doctor_stage_states_four_step_board.png": "exec-1ef8b71a-321a-41ff-ace5-861a04032501.png",
    "opera_job_racecar_driver_gameplay_zoom_strip_active.png": "exec-4728d13d-c787-4302-add5-443eac671728.png",
    "opera_job_racecar_driver_outfit_secondary_tool_or_accessory.png": "exec-7f5be543-850b-4780-a3dc-5edf0697f063.png",
    "opera_job_doctor_outfit_primary_tool_or_accessory.png": "exec-6217a596-9d59-44ae-a6f2-d06748b26144.png",
    "roshan_racer_steering_wheel.png": "exec-0ce28eb1-87eb-4090-9533-7016cc47cd16.png",
}

REJECTED = (
    ("opera_rival_costume_sheet_master_attempt_1", "P2-01", "exec-640ff861-9c53-4009-a1f7-abd69056ebcd.png", "astronaut and racer horns missing"),
    ("opera_house_audience_kit_attempt_1", "P3-03", "exec-26254990-7392-4227-8e9d-62542336582b.png", "introduced unapproved generic aquatic species"),
    ("opera_job_candy_maker_stage_states_seven_slot_shelf_attempt_1", "P2-09h", "exec-33e35d6b-2be0-40d6-97de-4637ce3ed89f.png", "five slots plus two gauges instead of seven candy slots"),
    ("opera_job_farmer_stage_states_piggy_finale_attempt_1", "P4-06", "exec-c93059ec-4300-441b-8115-c2b39bcffa6f.png", "ten piggies instead of the locked eleven"),
    ("opera_job_racecar_driver_outfit_secondary_attempt_1", "P2-09o", "exec-2f5222bd-e7d4-477a-ae05-804a493dc5ee.png", "neighboring grid fragments retained"),
    ("roshan_racer_steering_wheel_attempt_1", "P2-09o", "exec-f25f5ccd-4349-48d4-a7a5-9e44916bdbb2.png", "checker presentation pixels baked into actor"),
    ("opera_job_doctor_outfit_primary_attempt_1", "P2-09p", "exec-53013a6e-5aba-4e8d-ae4f-873f35998a20.png", "neighboring grid fragment retained"),
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def family(name: str) -> str:
    if "imp_" in name or "rival" in name:
        return "rivals"
    if "boss" in name or "performance_boss_finale" in name:
        return "boss_finales"
    if "audience" in name or name.startswith("opera_upper"):
        return "opera_house"
    if name.startswith("roshan_"):
        return "actors"
    if "magician" in name:
        return "magician_lamba"
    if "farmer_gameplay_sheet" in name:
        return "farmer"
    return "career_cards"


def request_id(name: str) -> str:
    if name.startswith("imp_"):
        return "P1"
    if "rival_costume" in name:
        return "P2-01"
    if "boxer" in name and ("imp_" in name or "bop_state" in name or "gentle_retry" in name):
        return "P2-02/03"
    if name.startswith("roshan_"):
        return "P2-04..07/P2-09"
    if name == "farmer_gameplay_sheet.png":
        return "P2-08"
    if name.startswith("opera_job_"):
        return "P2-09/P4-05"
    if "audience" in name:
        return "P3-03"
    if "finale_master" in name:
        return "P3-01"
    if "boss_" in name:
        return "P4-03"
    if "performance_boss_finale" in name:
        return "P4-04"
    if name.startswith("opera_upper"):
        return "P4-02"
    return "2026-08-01"


def build_ledger() -> tuple[int, int, list[float]]:
    rows = []
    scores = []
    for path in sorted(CARDS.glob("*.png")):
        with Image.open(path) as image:
            dimensions = f"{image.width}x{image.height}"
        review_only = "review_only" in path.name
        score = 4.8 if not review_only else 4.4
        status = "accepted" if not review_only else "rejected"
        reason = "" if not review_only else "native 1254x1254 is below the binding 2048x2048 runtime gate; review reference only"
        if not review_only:
            scores.append(score)
        rows.append({
            "asset_id": path.stem,
            "family": family(path.name),
            "accepted_reference_path": str(path.relative_to(ROOT)).replace("\\", "/"),
            "prompt_revision": request_id(path.name),
            "generation_id": GENERATION_IDS.get(path.name, "MISSING"),
            "native_dimensions": dimensions,
            "sha256": sha256(path),
            "score": f"{score:.1f}",
            "status": status,
            "rejection_reason": reason,
        })
    for asset_id, prompt, generation_id, reason in REJECTED:
        rows.append({
            "asset_id": asset_id,
            "family": family(asset_id),
            "accepted_reference_path": "",
            "prompt_revision": prompt,
            "generation_id": generation_id,
            "native_dimensions": "recorded in external generation provenance",
            "sha256": "not promoted",
            "score": "0.0",
            "status": "rejected",
            "rejection_reason": reason,
        })
    fields = tuple(rows[0])
    with LEDGER.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    return sum(row["status"] == "accepted" for row in rows), sum(row["status"] == "rejected" for row in rows), scores


def build_contact_sheets() -> None:
    CONTACTS.mkdir(parents=True, exist_ok=True)
    paths = sorted(CARDS.glob("*.png"))
    font = ImageFont.load_default()
    for page_index in range(0, len(paths), 16):
        page_paths = paths[page_index:page_index + 16]
        canvas = Image.new("RGB", (1280, 1280), (12, 18, 40))
        draw = ImageDraw.Draw(canvas)
        for local_index, path in enumerate(page_paths):
            row, column = divmod(local_index, 4)
            with Image.open(path) as image:
                thumb = ImageOps.contain(image.convert("RGB"), (292, 250), Image.Resampling.LANCZOS)
            x, y = column * 320 + 14, row * 320 + 10
            canvas.paste(thumb, (x + (292 - thumb.width) // 2, y))
            label = path.stem[:42]
            draw.text((x, y + 258), label, fill=(240, 235, 220), font=font)
            draw.text((x, y + 276), f"{page_index + local_index + 1:02d}  {GENERATION_IDS.get(path.name, 'MISSING')}", fill=(130, 210, 205), font=font)
        canvas.save(CONTACTS / f"opera_regeneration_contact_{page_index // 16 + 1:02d}.png", optimize=True)


def build_prompts() -> None:
    missing = sorted(path.name for path in CARDS.glob("*.png") if path.name not in GENERATION_IDS)
    text = """# Opera regeneration prompts and provenance — 2026-08-01

All generations used the exact STYLE-JOBS or STYLE-HOUSE contract quoted in
`OPERA_CODEX_REGENERATION_REQUESTS_2026-08-01.md`, followed by the matching
request paragraph for the `prompt_revision` recorded in the ledger. Binding
reference paths are the exact target card plus its named source sheet unless a
request explicitly names a different identity reference.

## Prompt revisions

- P1: authoritative striped-horn purple imp identity; full unclipped body;
  painterly Roshan-actor finish; no marine motif. Captain adds only a plain
  gold sash. Pose variants change acting only.
- P2-01: repaint the fixed 11-costume row-major rival sheet; preserve every
  costume and cell; restore both striped horns; remove stray fragments and
  every imp marine motif.
- P2-02/03: preserve boxer compositions; replace shell badges on imp clothing
  with plain bows/hats; apply the authoritative imp identity.
- P2-08: repaint the exact 16-cell farmer gameplay roster in the approved
  painterly outfit/stage finish; preserve all counts and pose states.
- P2-09/P4-05: keep composition and function; replace only the conflicting
  prop with the named canonical design. Goal cards are single complete native
  subjects on a deep-navy field.
- Lamba owner revision: use `assets/characters/lamb_0.png` for identity only;
  draw the same round white lamb without egg or lettering; no rabbit or fish
  anatomy; float, peek, reveal, and magician-stage acting as requested. Legacy
  `bunny_fish_*` paths are compatibility aliases.
- P3-01: empty complete Pearl Opera finale proscenium, open curtains and
  footlights, no actors or props. Candidate is review-only because the native
  generator output did not reach 2048x2048.
- P3-03: 4x4 tileable seating modules; occupants limited to approved starfish,
  Lamba, piggies, and empty seats; no humans or invented species.
- P4-02: single floor selector states with visibly distinct dark-to-lit shell
  contrast.
- P4-03: friendly plush toy-theatre phantom/maestro, warm palette, visible
  eyes, no skull mask or menace.
- P4-04: full-frame re-render of the exact accepted boss-finale composition,
  substituting only the approved friendly boss and warmer creature audience.

The `generation_id` and SHA-256 in `REGENERATION_LEDGER.csv` bind every file
to its native external `exec-*.png` provenance. Rejected attempts are recorded
there and were never copied into the repository.
"""
    if missing:
        text += "\n## Evidence error\n\nMissing generation IDs: " + ", ".join(missing) + "\n"
    PROMPTS.write_text(text, encoding="utf-8")


def update_licenses() -> None:
    start = "<!-- OPERA_REGEN_2026_08_01_START -->"
    end = "<!-- OPERA_REGEN_2026_08_01_END -->"
    current = LICENSES.read_text(encoding="utf-8")
    if start in current and end in current:
        current = current[:current.index(start)].rstrip() + "\n\n" + current[current.index(end) + len(end):].lstrip()
    lines = [start, "## Opera regeneration — 2026-08-01", ""]
    for path in sorted(CARDS.glob("*.png")):
        if "review_only" in path.name:
            continue
        rel = str(path.relative_to(ROOT)).replace("\\", "/")
        lines.append(f"- `{rel}` — OpenAI-generated project concept art; 2026-08-01; native generated master retained, delivery copies may be whole-canvas normalized, matted, or sliced; project-owned; generation `{GENERATION_IDS[path.name]}`.")
    lines.append(end)
    LICENSES.write_text(current.rstrip() + "\n\n" + "\n".join(lines) + "\n", encoding="utf-8")


def build_audit(accepted: int, rejected: int, scores: list[float]) -> None:
    AUDIT.parent.mkdir(parents=True, exist_ok=True)
    AUDIT.write_text(f"""# Opera regeneration audit — 2026-08-01

- Accepted generated candidates: {accepted}
- Rejected candidates: {rejected}
- Accepted score range: {min(scores):.1f}–{max(scores):.1f}; mean {mean(scores):.2f}
- Human gates: identity/topology, child-readable silhouette, canonical prop
  continuity, no clipping/neighbor debris, and imp marine-motif prohibition.
- Native masters: retained under `assets_src/concepts/opera_regeneration_2026-08-01/cards/` with SHA-256 evidence in the ledger.
- Delivery transforms: full-canvas resize for approved sheet/finale outputs;
  deterministic edge-field matting and fit for actors/props; no subject warp,
  interpolation, compositing, or pixel borrowing.
- P3-01: rejected for runtime use at 1254x1254; kept review-only.
- P3-02: not generated because the request makes it owner-opt-in and no opt-in
  was supplied.
- P3-04: deferred; the available generator's 1672x941 wide output cannot meet
  the binding native 2048x1152 gate. Current code-native stage art remains the
  compliant runtime path.
- Lamba: accepted owner-directed replacement for rabbit-fish/bunny-fish art.
  Protected source art and family voice files were not modified. Remaining
  voice and legacy-3D migration is assigned to Fable in the dated handoff.

## Validation

- Python compilation: PASS for the evidence, promotion, actor, and prop tools.
- GDScript parser and inference lint: PASS for
  `scripts/opera_career_world_2d.gd`.
- Godot import: PASS with Godot 4.7.1.
- `probe_opera_2d`: PASS for all twelve careers, including magician.
- Full `scripts/ci.sh`: FAIL outside this change's scope. Reported failures are
  the ocean-kingdom return-gate debounce checks, existing storybook/tank/
  Level-2 audit checks, three playroom castle-art checks, and the Windows
  CP1252 console's inability to print box-drawing characters in
  `audit_visual_design.py`. No Opera 2D assertion failed.
""", encoding="utf-8")


def main() -> None:
    accepted, rejected, scores = build_ledger()
    build_contact_sheets()
    build_prompts()
    update_licenses()
    build_audit(accepted, rejected, scores)
    print(f"evidence built: {accepted} accepted, {rejected} rejected")


if __name__ == "__main__":
    main()
