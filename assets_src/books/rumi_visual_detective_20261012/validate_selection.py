"""Validate explicit native-page selection and original generation provenance.

Read-only by default. --output writes a machine receipt, never a selection.
Hash uniqueness does not establish semantic uniqueness or lettering acceptance.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PREVIOUS = ROOT / "assets_src/books/rumi_voice_book_20261011"
SCRIPT = HERE / "story_script.json"
SELECTION = HERE / "selected_art.json"
FROZEN_SCRIPT = "ab77f7740592a82b9185c10eb22a7b85ff785726b2f9eb8f01158861d54db6cd"
EARLIER_SCRIPT = "b3623441d31710e1afeda9298c0c74e7c3cc3b6b4c8627b7bf9b1b8bafcbf876"
SOURCE_REVISION = "e168c6cfd4b4992c375ff66b0efaab5749cd4d234301fab4ad71b75f06249042"
METHOD_CHANGE_DIAGNOSIS = "391e74c4b79e9866a46059679521f8e45b04e424a0931d8d269a49e0a5001703"
THIRD_TAKE_PAGES = {8, 10}
THIRD_TAKE_METHOD_RECORDS = {
    8: "c7ab8127c3f3e56f64767d8d5363e2e2fe3af0fa0c470103719648e3b834d02a",
    10: "1fd95d87917e49481f4a482625c67f9b5d08dc3534f17529fef36c39b3862bf1",
}
PREVIOUS_SCRIPT = "febb9d5c7f6d82c29dcf8fa3556715577842b2284749fd2f1fea055a046d5967"
PREVIOUS_SELECTION = "0e875f78ffe6299c7c8a1ebd41f95b90ca04fe237a3105d06114c4f301329dee"
PREVIOUS_MANIFEST = "ca2eb5d03251b942ebf114fc7096919cfd53448869fd3eac2177d14f51240a10"
NATIVE_SIZE = (1024, 1536)
CHANGED_STORY_PAGES = {2, 3, 4, 32}
NATIVE_DIRS = (HERE / "native", PREVIOUS / "native")


def sha_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha_file(path):
    return sha_bytes(Path(path).read_bytes())


def project_path(raw):
    value = Path(raw.replace("\\", "/"))
    if value.is_absolute() or ".." in value.parts:
        raise ValueError(f"Literal project-relative path required: {raw}")
    path = (ROOT / value).resolve(strict=True)
    if not path.is_relative_to(ROOT.resolve()):
        raise ValueError(f"Reference escaped project: {raw}")
    return path


def resolve_art(raw):
    path = project_path(raw)
    if path.parent not in [p.resolve() for p in NATIVE_DIRS] or path.suffix.lower() != ".png":
        raise ValueError(f"Selected art must be a whole native PNG in one of the two bound editions: {raw}")
    return path


def rgb_record(path):
    from PIL import Image
    with Image.open(path) as image:
        if image.mode != "RGB" or image.size != NATIVE_SIZE:
            raise ValueError(f"Unconverted RGB 1024x1536 required: {path}: {image.mode}/{image.size}")
        if image.info.get("icc_profile"):
            raise ValueError(f"ICC source needs separately profiled PDF embedding: {path}")
        return {"dimensions": list(image.size), "mode": image.mode,
                "rgb_pixel_sha256": sha_bytes(image.tobytes())}


def page_sha(page):
    return sha_bytes(json.dumps(page, ensure_ascii=False, sort_keys=True).encode("utf-8"))


def validate_method_change(path, page, prompt_path=None, references_path=None, binder=None):
    """Root's one named fresh-layout attempt; never an automatic cap reset."""
    def checked(file, expected=None):
        file = Path(file).resolve(strict=True)
        digest = sha_file(file)
        if expected is not None and digest != expected:
            raise ValueError(f"Method-change bound bytes differ: {file}")
        if binder:
            binder(file, expected)
        return digest

    if page not in THIRD_TAKE_PAGES:
        raise ValueError("Third take is authorized ONLY on pages8 and10.")
    path = Path(path).resolve(strict=True)
    if path.parent != (HERE / "verification").resolve() or path.name != f"page_{page:02}_take3_method_change.json":
        raise ValueError("The named edition-local take3 method-change record is required.")
    record_hash = checked(path, THIRD_TAKE_METHOD_RECORDS[page])
    record = json.loads(path.read_bytes())
    if record.get("page") != page or record.get("take") != 3 or record.get("cycle_call_cap") != 3:
        raise ValueError("Method-change identity and total cycle cap must be page8/10, take3, cap3.")
    if record.get("previous_local_calls") != 2 or record.get("additional_call_cap") != 1 or record.get("no_automatic_retakes") is not True:
        raise ValueError("Method change permits one additional call only and preserves both failed calls.")
    if record.get("method") != "fresh_full_page_staging_after_two_failed_local_repairs" or record.get("script_sha256") != FROZEN_SCRIPT:
        raise ValueError("Method change must bind the final script and fresh whole-page staging lane.")
    if not record.get("authorization"):
        raise ValueError("The record must retain root's explicit named authorization.")
    source = json.loads(SCRIPT.read_bytes())
    if sha_file(SCRIPT) != FROZEN_SCRIPT or record.get("source_page_sha256") != page_sha(source["pages"][page - 1]):
        raise ValueError("Method change must bind the exact final source-page object.")
    diagnosis_path = HERE / "verification/local_repair_diagnosis_pages_08_10.json"
    diagnosis_binding = {"path": diagnosis_path.relative_to(ROOT).as_posix(), "sha256": METHOD_CHANGE_DIAGNOSIS}
    if record.get("diagnosis") != diagnosis_binding:
        raise ValueError("Method change must bind the exact root-authorized failure diagnosis.")
    checked(diagnosis_path, METHOD_CHANGE_DIAGNOSIS)
    diagnosis = json.loads(diagnosis_path.read_bytes())
    if diagnosis["script_sha256"] != FROZEN_SCRIPT or diagnosis["status"] != "ROOT_AUTHORIZED_CHANGED_METHOD_PENDING":
        raise ValueError("Unexpected diagnosis source or authorization state.")
    item = next(p for p in diagnosis["pages"] if p["page"] == page)
    if item["local_calls"] != 2 or not item["all_local_attempts_rejected"] or item["additional_call_cap"] != 1 or item["max_total_cycle_calls"] != 3:
        raise ValueError("Diagnosis must preserve two failed local calls plus one additional call, without resetting.")
    preceding = record.get("preceding_attempts", [])
    if [r.get("take") for r in preceding] != [1, 2]:
        raise ValueError("Both prior attempts must be present, ordered and hash-bound.")
    for previous, diagnosed in zip(preceding, item["attempts"]):
        receipt_path = HERE / f"generation/page_{page:02}_take{previous['take']}.json"
        if previous.get("receipt_path") != receipt_path.relative_to(ROOT).as_posix() or previous.get("receipt_sha256") != diagnosed["capture_receipt_sha256"]:
            raise ValueError("Method-change prior receipt binding differs from the diagnosis.")
        checked(receipt_path, previous["receipt_sha256"])
        receipt = json.loads(receipt_path.read_bytes())
        if receipt["page"] != page or receipt["take"] != previous["take"] or receipt["sha256"] != diagnosed["sha256"]:
            raise ValueError("Prior take identity differs from diagnosed failed attempt.")
        checked(resolve_art(receipt["path"]), diagnosed["sha256"])
    brief = project_path(record["prompt_file"])
    refs = project_path(record["references_file"])
    if not brief.is_relative_to(HERE) or not refs.is_relative_to(HERE):
        raise ValueError("Fresh-layout brief and reference list must be edition-local.")
    checked(brief, record["prompt_sha256"])
    checked(refs, record["references_sha256"])
    if prompt_path is not None and Path(prompt_path).resolve(strict=True) != brief:
        raise ValueError("Actual third-call prompt is not the bound fresh-layout brief.")
    if references_path is not None and Path(references_path).resolve(strict=True) != refs:
        raise ValueError("Actual third-call references are not the bound fresh-layout reference list.")
    if any(r.get("role") == "local_edit_target" for r in json.loads(refs.read_bytes())):
        raise ValueError("The named third attempt is fresh staging, not another local repair.")
    return {"path": path.relative_to(ROOT).as_posix(), "sha256": record_hash,
            "method": record["method"], "total_cycle_call_cap": 3,
            "diagnosis_sha256": METHOD_CHANGE_DIAGNOSIS}


def validate(selection_path=SELECTION, expected_selection_sha256=None):
    if not expected_selection_sha256 or not re.fullmatch(r"[0-9a-f]{64}", expected_selection_sha256):
        raise ValueError("A root-frozen --selection-sha256 is required; this tool never selects takes.")
    selection_path = Path(selection_path).resolve(strict=True)
    if selection_path.parent != HERE or selection_path.name != "selected_art.json":
        raise ValueError("Only this edition's root-owned selected_art.json may be used.")
    snapshots = {}

    def bind(path, expected=None):
        path = Path(path).resolve(strict=True)
        digest = sha_file(path)
        if expected is not None and digest != expected:
            raise ValueError(f"Frozen bytes differ: {path}: {digest} != {expected}")
        snapshots[str(path)] = digest
        return digest

    bind(SCRIPT, FROZEN_SCRIPT)
    bind(HERE / "verification/story_snapshot_before_hair_word_fix.json", EARLIER_SCRIPT)
    bind(HERE / "verification/source_revision.json", SOURCE_REVISION)
    bind(selection_path, expected_selection_sha256)
    bind(PREVIOUS / "story_script.json", PREVIOUS_SCRIPT)
    bind(PREVIOUS / "selected_art.json", PREVIOUS_SELECTION)
    bind(PREVIOUS / "generation_manifest.json", PREVIOUS_MANIFEST)
    bind(Path(__file__))
    source = json.loads(SCRIPT.read_bytes())
    earlier = json.loads((HERE / "verification/story_snapshot_before_hair_word_fix.json").read_bytes())
    revision = json.loads((HERE / "verification/source_revision.json").read_bytes())
    if revision["previous_script_sha256"] != EARLIER_SCRIPT or revision["current_script_sha256"] != FROZEN_SCRIPT:
        raise ValueError("Source revision must truthfully bind the prior and corrected freezes.")
    previous = json.loads((PREVIOUS / "story_script.json").read_bytes())
    selection = json.loads(selection_path.read_bytes())
    old_selection = json.loads((PREVIOUS / "selected_art.json").read_bytes())
    old_manifest = json.loads((PREVIOUS / "generation_manifest.json").read_bytes())
    numbers = list(range(1, 33))
    if [p["number"] for p in source["pages"]] != numbers or [p["number"] for p in selection["pages"]] != numbers:
        raise ValueError("Exactly 32 consecutive source and selected pages required.")
    if selection["script_sha256"] != FROZEN_SCRIPT:
        raise ValueError("Selection must bind the full frozen detective-edition script.")
    if source["pages"][0]["kind"] != "cover" or any(p["kind"] != "story" for p in source["pages"][1:]):
        raise ValueError("Architecture is cover1 and narrative2-32.")
    if source["pages"][0] != previous["pages"][0] or source["pages"][4:31] != previous["pages"][4:31]:
        raise ValueError("Preceding page1 and pages5-31 must remain structurally exact.")
    if old_manifest["script_sha256"] != PREVIOUS_SCRIPT or old_selection["script_sha256"] != PREVIOUS_SCRIPT:
        raise ValueError("Preceding authorities must bind the preserved script.")
    if old_manifest["selection"] != {"path": (PREVIOUS / "selected_art.json").relative_to(ROOT).as_posix(), "sha256": PREVIOUS_SELECTION}:
        raise ValueError("Preceding manifest/selection binding changed.")
    transcript = HERE / "MANUSCRIPT.txt"
    bind(transcript)
    entries = [e for p in source["pages"] for panel in p["panels"] for e in panel["entries"]]
    prefixes = tuple(f"{e['speaker']}: " for e in entries)
    actual = [line for line in transcript.read_text(encoding="utf-8").splitlines() if line.startswith(prefixes)]
    if actual != [f"{e['speaker']}: {e['text']}" for e in entries]:
        raise ValueError("Literal manuscript entry sequence differs from source.")
    story_words = sum(len(re.findall(r"\S+", e["text"])) for p in source["pages"] if p["kind"] == "story" for panel in p["panels"] for e in panel["entries"])
    if story_words != 1050 or sum(len(p["panels"]) for p in source["pages"]) != 102:
        raise ValueError("Frozen source count mismatch: 1050 story words and 102 total panels required.")
    for ref in old_manifest.get("source_catalog", []) + old_manifest.get("review_bindings", []):
        bind(project_path(ref["path"]), ref["sha256"])
    old_rows = {r["number"]: r for r in old_selection["pages"]}
    old_records = {(r["page"], r["take"]): r for r in old_manifest["records"]}

    def check_record(record, edition, expected_page, expected_take, raw_path):
        bind(raw_path)
        if record["page"] != expected_page or record["take"] != expected_take or record["method"] != "built-in image_gen.imagegen" or record["call_count"] != 1:
            raise ValueError(f"Generation record identity/method/call count mismatch: {raw_path}")
        expected_scripts = {FROZEN_SCRIPT, EARLIER_SCRIPT} if edition == HERE else {PREVIOUS_SCRIPT}
        if record["script_sha256"] not in expected_scripts:
            raise ValueError(f"Generation record source script mismatch: {raw_path}")
        if edition == HERE and record["script_sha256"] == EARLIER_SCRIPT and earlier["pages"][expected_page - 1] != source["pages"][expected_page - 1]:
            raise ValueError(f"Earlier full-script hash allowed only for an unchanged source page: {raw_path}")
        native = resolve_art(record["path"])
        if native.parent != (edition / "native").resolve() or native.name != f"page_{expected_page:02}_take{expected_take}.png":
            raise ValueError(f"Generation record page/take path mismatch: {raw_path}")
        digest = bind(native, record["sha256"])
        rgb = rgb_record(native)
        if record["rgb_pixel_sha256"] != rgb["rgb_pixel_sha256"] or record["dimensions"] != list(NATIVE_SIZE) or record["native_mode"] != "RGB":
            raise ValueError(f"Generation record RGB/dimension mismatch: {raw_path}")
        provider = Path(record["provider_path"]).resolve(strict=True)
        if provider.suffix.lower() != ".png" or "generated_images" not in provider.parts:
            raise ValueError(f"Built-in native provider path required: {raw_path}")
        bind(provider, digest)
        if record["provider_sha256"] != digest:
            raise ValueError(f"Provider/native recorded hashes differ: {raw_path}")
        if sha_bytes(record["prompt"].encode("utf-8")) != record["prompt_sha256"]:
            raise ValueError(f"Recorded literal prompt hash differs: {raw_path}")
        for ref in record["references"]:
            bind(project_path(ref["path"]), ref["sha256"])
            if not ref.get("role"):
                raise ValueError(f"Every bound reference needs its role: {raw_path}")
        if edition == HERE:
            if record.get("source_page_sha256") != page_sha(source["pages"][expected_page - 1]):
                raise ValueError(f"New record does not bind exact source page: {raw_path}")
            prompt_file = project_path(record["prompt_file"])
            refs_file = project_path(record["references_file"])
            if not prompt_file.is_relative_to(HERE) or not refs_file.is_relative_to(HERE):
                raise ValueError("New prompt/reference sidecars must be edition-local.")
            bind(prompt_file, record["prompt_sha256"])
            if prompt_file.read_bytes() != record["prompt"].encode("utf-8"):
                raise ValueError(f"Actual prompt bytes differ from recorded literal: {raw_path}")
            bind(refs_file)
            planned_refs = json.loads(refs_file.read_bytes())
            if len(planned_refs) != len(record["references"]):
                raise ValueError(f"Actual reference sidecar length differs: {raw_path}")
            for planned, captured in zip(planned_refs, record["references"]):
                if any(planned[k] != captured.get(k) for k in planned):
                    raise ValueError(f"Actual reference sidecar content differs: {raw_path}")
            if expected_take == 3:
                binding = record.get("method_change")
                if not binding:
                    raise ValueError("Third take requires its explicit method-change provenance.")
                method = validate_method_change(project_path(binding["path"]), expected_page,
                                                prompt_file, refs_file, bind)
                if binding != method:
                    raise ValueError("Third-take captured method-change binding differs.")
        return {"page": expected_page, "take": expected_take, "receipt_path": raw_path.relative_to(ROOT).as_posix(),
                "receipt_sha256": sha_file(raw_path), "native_sha256": digest,
                "provider_native_byte_match": True, "prompt_hash_match": True,
                "reference_hashes_match": True, "rgb_pixel_match": True}

    new_records = {}
    new_checks = []
    for path in sorted((HERE / "generation").glob("page_*_take*.json")):
        match = re.fullmatch(r"page_(\d{2})_take(\d+)\.json", path.name)
        if not match:
            continue
        n, take = map(int, match.groups())
        if not 1 <= n <= 32 or not 1 <= take <= (3 if n in THIRD_TAKE_PAGES else 2):
            raise ValueError("Two-take cycle cap; third take ONLY for named pages8/10 with bound method change.")
        record = json.loads(path.read_bytes())
        new_records[n, take] = record
        new_checks.append(check_record(record, HERE, n, take, path))
    for n, take in new_records:
        if take == 2 and (n, 1) not in new_records:
            raise ValueError(f"Take2 requires preserved initial record on page {n}.")
        if take == 3 and any((n, earlier_take) not in new_records for earlier_take in [1, 2]):
            raise ValueError(f"Named take3 requires preserved take1+take2 on page {n}.")
    recorded_paths = {r["path"] for r in new_records.values()}
    native_paths = {p.relative_to(ROOT).as_posix() for p in (HERE / "native").glob("page_*_take*.png")}
    if recorded_paths != native_paths:
        raise ValueError("Every new native take must have a matching capture receipt, including rejects.")
    rows, reused_checks = [], []
    for page, selected in zip(source["pages"], selection["pages"]):
        n, take = page["number"], selected["take"]
        native = resolve_art(selected["path"])
        rgb = rgb_record(native)
        digest = bind(native, selected["sha256"])
        if selected["rgb_pixel_sha256"] != rgb["rgb_pixel_sha256"] or selected["dimensions"] != list(NATIVE_SIZE):
            raise ValueError(f"Selected RGB/dimensions differ on page {n}.")
        if native.parent == (PREVIOUS / "native").resolve():
            if n in CHANGED_STORY_PAGES or page != previous["pages"][n - 1]:
                raise ValueError(f"Changed story page {n} cannot reuse a preceding picture.")
            old = old_rows[n]
            if any(selected[k] != old[k] for k in ["number", "take", "path", "sha256", "rgb_pixel_sha256", "dimensions"]):
                raise ValueError(f"Reused page {n} must equal the frozen preceding selection.")
            record = old_records[n, take]
            if not record["delivery_selected"]:
                raise ValueError(f"Preceding rejected take cannot be reused: page {n}.")
            raw_path = project_path(record["raw_receipt"]["path"])
            bind(raw_path, record["raw_receipt"]["sha256"])
            raw = json.loads(raw_path.read_bytes())
            if raw != {k: v for k, v in record.items() if k not in ["delivery_selected", "raw_receipt"]}:
                raise ValueError(f"Preceding manifest/receipt content differs on page {n}.")
            reused_checks.append(check_record(raw, PREVIOUS, n, take, raw_path))
            origin = "PREVIOUS_COMPLETE_NATIVE_PAGE_UNCHANGED_STORY"
        else:
            if (n, take) not in new_records:
                raise ValueError(f"Selected new page {n}/take{take} has no capture receipt.")
            record = new_records[n, take]
            if any(selected[k] != record[k] for k in ["take", "path", "sha256", "rgb_pixel_sha256", "dimensions"]):
                raise ValueError(f"Selected new page {n} differs from capture receipt.")
            origin = "NEW_COMPLETE_NATIVE_PAGE_CURRENT_SCRIPT"
        rows.append({"number": n, "kind": page["kind"], "path": native.relative_to(ROOT).as_posix(),
                     "take": take, "sha256": digest, **rgb, "origin": origin,
                     "source_page_sha256": page_sha(page)})
    if len({r["sha256"] for r in rows}) != 32 or len({r["rgb_pixel_sha256"] for r in rows}) != 32:
        raise ValueError("32 distinct native file and decoded-RGB hashes required.")
    for ref in selection.get("review_bindings", []):
        bind(project_path(ref["path"]), ref["sha256"])
    for raw, digest in snapshots.items():
        if sha_file(Path(raw)) != digest:
            raise ValueError(f"Bound input changed during validation: {raw}")
    result = {"schema": "rumi_detective_selection_provenance_check_v1",
              "status": "MACHINE_PROVENANCE_PASS_VISUAL_OWNER_CHILD_ACCEPTANCE_SEPARATE",
              "script_sha256": FROZEN_SCRIPT, "selection_sha256": expected_selection_sha256,
              "source_revision": {"earlier_script_sha256": EARLIER_SCRIPT, "receipt_sha256": SOURCE_REVISION,
                                  "scope": "One staging hair word corrected; earlier calls accepted only for structurally unchanged source pages"},
              "checker": {"path": Path(__file__).relative_to(ROOT).as_posix(), "sha256": sha_file(Path(__file__))},
              "preceding_script_sha256": PREVIOUS_SCRIPT, "preceding_selection_sha256": PREVIOUS_SELECTION,
              "preceding_manifest_sha256": PREVIOUS_MANIFEST, "pages": 32, "total_panels": 102,
              "story_words": story_words, "word_count_method": "Whitespace-separated nonempty entry tokens; cover, labels and staging excluded",
              "manuscript_entry_order_exact": True, "unchanged_source_pages": [1] + list(range(5, 32)),
              "new_cycle_calls": len(new_checks), "new_records": new_checks,
              "reused_selected_records": reused_checks, "selected_pages": rows,
              "unique_native_sha256_count": 32, "unique_rgb_pixel_sha256_count": 32,
              "source_input_snapshots": [{"path": raw, "sha256": digest} for raw, digest in sorted(snapshots.items())],
              "limits": ["Hashes do not establish exact generated lettering, speaker attribution or semantic/action uniqueness.",
                         "Every exact selected page needs human native and final-PDF visual review.",
                         "Owner, child, print, runtime and global master-audit acceptance are not claimed."]}
    return result, rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--selection", type=Path, default=SELECTION)
    parser.add_argument("--selection-sha256", required=True)
    parser.add_argument("--output", type=Path, help="Optional edition-local machine receipt; no PDF or selection authored")
    args = parser.parse_args()
    result, _ = validate(args.selection, args.selection_sha256)
    if args.output:
        output = args.output.resolve()
        if output.parent != (HERE / "verification").resolve() or output.suffix != ".json":
            raise ValueError("Machine receipt must be a JSON in this edition's verification directory.")
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({k: result[k] for k in ["status", "script_sha256", "selection_sha256", "pages", "story_words", "new_cycle_calls"]}, indent=2))


if __name__ == "__main__":
    main()
