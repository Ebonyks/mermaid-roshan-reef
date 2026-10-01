"""Recognize only the JP1 SaveState catalogue substitutions; never execute code.

Literal reading elsewhere remains the constrained GDParser contract. These
source checks bind the preload, scalar expressions, registration fragments and
normalization loop to their exact commissioned forms and pinned Git baseline.
"""
from __future__ import annotations

import copy
import re
import subprocess
from functools import lru_cache
from pathlib import Path

try:
    from .content_gd_literals import GDParser, mask_source
except ImportError:
    from content_gd_literals import GDParser, mask_source

SAVE_PATH = "scripts/save_state.gd"
SCALAR_REFERENCES = {
    "OPERA_ACTIVE_STAR_MASK": "ACTIVE_STAR_MASK",
    "OPERA_ACTIVE_ACT_COUNT": "ACTIVE_ACT_COUNT",
}
REGISTRATION_LISTS = ("DICTIONARY_KEYS", "KNOWN_KEYS")
NORMALIZATION_LOOP = (
    'for checkpoint_job_id: String in JobData.SAVE_CHECKPOINT_JOB_ORDER:',
    'var checkpoint_spec: Dictionary = JobData.SAVE_CHECKPOINTS[checkpoint_job_id] as Dictionary',
    'var checkpoint_key: String = String(checkpoint_spec["key"])',
    'data[checkpoint_key] = _normalise_job_checkpoint(raw, checkpoint_job_id)',
)

LEGACY_NORMALIZATION_LINES = (
    '\tdata["teacher_lesson_checkpoint"] = _teacher_lesson_checkpoint_or_default(raw)',
    '\tdata["opera_geology_checkpoint"] = _opera_geology_checkpoint_or_default(raw)',
)


def _constant_parser(text: str, name: str) -> GDParser:
    matches = list(re.finditer(r"(?m)^const\s+" + re.escape(name) + r"\b[^=\n]*=(?:\s*\\)?", mask_source(text)))
    if len(matches) != 1:
        raise ValueError(f"SaveState must declare {name} exactly once")
    return GDParser(text, matches[0].end())


def _finish(text: str, index: int, context: str) -> None:
    end = text.find("\n", index)
    tail = text[index:end if end >= 0 else len(text)].strip()
    if tail and not tail.startswith("#"):
        raise ValueError("trailing expression after " + context)


def _literal_const(text: str, name: str):
    parser = _constant_parser(text, name)
    value = parser.value()
    _finish(text, parser.i, name)
    return value


def _require_preload(text: str) -> None:
    declarations = list(re.finditer(r"(?m)^const\s+JobData\b[^\n]*", mask_source(text)))
    if len(declarations) != 1 or not re.fullmatch(
        r'const\s+JobData\s*:=\s*preload\("res://scripts/generated/job_catalog_data\.gd"\)\s*(?:#.*)?',
        text[declarations[0].start():declarations[0].end()] if declarations else "",
    ):
        raise ValueError("SaveState JobData preload differs from the fixed JP1 target")


def _function_body(text: str, name: str) -> str:
    code = mask_source(text)
    matches = list(re.finditer(r"(?m)^(?:static\s+)?func\s+" + re.escape(name) + r"\([^\n]*\)\s*->\s*[^:\n]+:\s*\n", code))
    if len(matches) != 1:
        raise ValueError("expected exactly one real SaveState function " + name)
    start = matches[0]
    end = re.search(r"(?m)^(?:static\s+)?func\b", code[start.end():])
    return text[start.end():start.end() + end.start() if end else len(text)]


def _literal_checkpoint_keys(text: str) -> list[str]:
    body = _function_body(text, "_normalise_save")
    result = []
    for raw, code in zip(body.splitlines(), mask_source(body).splitlines()):
        if re.search(r"_\w+_checkpoint_or_default\(raw\)", code):
            match = re.fullmatch(r'\s*data\["([^"]+)"\]\s*=\s*_\w+_checkpoint_or_default\(raw\)\s*(?:#.*)?', raw)
            if match:
                result.append(match.group(1))
    return result


@lru_cache(maxsize=16)
def _baseline_save(root_name: str, baseline: str):
    text = subprocess.check_output(
        ["git", "show", baseline + ":" + SAVE_PATH], cwd=root_name,
        text=True, encoding="utf-8", stderr=subprocess.DEVNULL,
    )
    return text, {name: _literal_const(text, name) for name in REGISTRATION_LISTS}, _literal_checkpoint_keys(text)


def baseline_checkpoint_order(root: Path, baseline: str, data: dict) -> list[str]:
    _, _, keys = _baseline_save(str(Path(root).resolve()), baseline)
    by_key = {spec["key"]: jid for jid, spec in data["SAVE_CHECKPOINTS"].items()}
    if not keys or len(keys) != len(set(keys)) or any(key not in by_key for key in keys):
        raise ValueError("checkpoint identity differs from the pinned normalization baseline")
    return [by_key[key] for key in keys]


def _registration_fragments(root: Path, baseline: str, name: str):
    _, arrays, checkpoints = _baseline_save(str(Path(root).resolve()), baseline)
    original = arrays[name]
    slots = [i for i, key in enumerate(original) if key in checkpoints]
    if not slots or slots != list(range(slots[0], slots[-1] + 1)):
        raise ValueError("pinned checkpoint registration is not one contiguous segment in " + name)
    return original[:slots[0]], original[slots[-1] + 1:], original


def read_save_const(root: Path, name: str, data: dict, baseline: str):
    """Resolve only two scalar aliases and two fixed registration concatenations."""
    if name not in SCALAR_REFERENCES and name not in REGISTRATION_LISTS:
        raise ValueError("unapproved SaveState catalogue constant " + name)
    text = (Path(root) / SAVE_PATH).read_text(encoding="utf-8")
    parser = _constant_parser(text, name)
    parser.ws()
    if name in SCALAR_REFERENCES:
        reference = "JobData." + SCALAR_REFERENCES[name]
        if text.startswith(reference, parser.i):
            _require_preload(text)
            _finish(text, parser.i + len(reference), name)
            value = data[SCALAR_REFERENCES[name]]
            if type(value) is not int:
                raise ValueError("catalogue scalar is not an integer: " + reference)
            return value
        value = parser.value()
        _finish(text, parser.i, name)
        return value
    prefix = parser.value()
    prefix_end = parser.i
    expected_prefix, expected_tail, original = _registration_fragments(root, baseline, name)
    if parser.peek() != "+":
        _finish(text, prefix_end, name)
        if prefix != original:
            raise ValueError("literal " + name + " differs from pinned key order")
        return prefix
    _require_preload(text)
    if prefix != expected_prefix:
        raise ValueError("static checkpoint registration prefix differs in " + name)
    parser.i += 1
    parser.ws()
    reference = re.match(r'JobData\.SAVE_CHECKPOINT_KEY_LISTS\["' + name + r'"\]', text[parser.i:])
    if not reference:
        raise ValueError("unapproved checkpoint registration reference in " + name)
    parser.i += len(reference.group())
    if parser.peek() != "+":
        raise ValueError("checkpoint registration must retain its exact static tail in " + name)
    parser.i += 1
    tail = parser.value()
    _finish(text, parser.i, name)
    if tail != expected_tail:
        raise ValueError("static checkpoint registration tail differs in " + name)
    keys = data["SAVE_CHECKPOINT_KEY_LISTS"][name]
    if not isinstance(keys, list) or any(type(key) is not str for key in keys) or len(keys) != len(set(keys)) or set(keys) & set(prefix + tail):
        raise ValueError("invalid or colliding checkpoint registration keys in " + name)
    return copy.deepcopy(prefix + keys + tail)


def _without_comments(text: str) -> str:
    return mask_source(text, mask_strings=False)


def _compact(text: str) -> str:
    out, quote, escaped = [], None, False
    for char in text:
        if quote:
            out.append(char)
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = None
        elif char in ('"', "'"):
            quote = char
            out.append(char)
        elif not char.isspace():
            out.append(char)
    return "".join(out)


def _star_clamp(body: str, prefix: str, arguments: str, before: str, after: str) -> str:
    matches = list(re.finditer(r"(?m)^\t" + re.escape(prefix), mask_source(body)))
    if len(matches) != 1:
        raise ValueError("missing or duplicate commissioned star clamp: " + prefix)
    start = body.index("clampi(", matches[0].start())
    depth, index, quote, escaped = 1, start + len("clampi("), None, False
    while depth and index < len(body):
        char = body[index]
        if quote:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = None
        elif char in ('"', "'"):
            quote = char
        else:
            depth += {"(": 1, ")": -1}.get(char, 0)
        index += 1
    if depth:
        raise ValueError("unterminated commissioned star clamp")
    _finish(body, index, prefix)
    previous = [(raw.rstrip(), code) for raw, code in zip(body[:matches[0].start()].splitlines(), mask_source(body[:matches[0].start()]).splitlines()) if code.strip()]
    following = [(raw.rstrip(), code) for raw, code in zip(body[index:].splitlines(), mask_source(body[index:]).splitlines()) if code.strip()]
    if not previous or not following or previous[-1][0] != before or following[0][0] != after:
        raise ValueError("commissioned star clamp moved from original insertion site: " + prefix)
    call = _compact(body[start:index])
    expected = "clampi(" + _compact(arguments)
    if not call.startswith(expected):
        raise ValueError("commissioned star clamp arguments differ: " + prefix)
    upper = call[len(expected):-1]
    if not re.fullmatch(r"\d+|JobData\.STAR_CEILING", upper):
        raise ValueError("unapproved SaveState star ceiling expression")
    return upper


def read_save_bounds(root: Path, data: dict) -> dict[str, int]:
    text = (Path(root) / SAVE_PATH).read_text(encoding="utf-8")
    code = mask_source(text)
    if len(re.findall(r"\bfor\s+bit_index\s+in\s+range\(", code)) != 1:
        raise ValueError("SaveState has extra or missing commissioned star loops")
    clamp_targets = r"(?:m\.opera_stars\s*=|var\s+raw_opera_stars\s*:=|var\s+opera_stars\s*:\s*int\s*=)\s*clampi\("
    if len(re.findall(clamp_targets, code)) != 4:
        raise ValueError("SaveState has extra or missing commissioned star clamps")
    live_body = mask_source(_function_body(text, "_opera_live_star_count"))
    loops = re.findall(r'(?m)^\tfor bit_index in range\(([^\n)]*)\):\s*$', live_body)
    if len(loops) != 1:
        raise ValueError("SaveState commissioned star loop differs or is absent")
    live_lines = [line.rstrip() for line in live_body.splitlines() if line.strip()]
    loop_index = next(i for i, line in enumerate(live_lines) if line.startswith("\tfor bit_index in range("))
    if loop_index == 0 or loop_index + 1 >= len(live_lines) or live_lines[loop_index - 1] != "\tvar total := 0" or live_lines[loop_index + 1] != "\t\tvar bit := 1 << bit_index":
        raise ValueError("commissioned star loop moved from original insertion site")
    bound = loops[0].strip()
    if bound == "JobData.SLOT_COUNT":
        _require_preload(text)
        slots = data["SLOT_COUNT"]
    elif re.fullmatch(r"\d+", bound):
        slots = int(bound)
    else:
        raise ValueError("unapproved SaveState star loop bound")
    sites = (
        ("load_save", "m.opera_stars = clampi(", 'int(m.save_data.get("opera_stars", 0)), 0,', '\tm.ember_done = bool(m.save_data.get("ember_done", false))', '\tm.opera_progress = _opera_live_star_count(m.opera_stars)'),
        ("write_save", "m.opera_stars = clampi(", 'm.opera_stars, 0,', '\tnext_data["ember_done"] = m.ember_done', '\tm.opera_progress = _opera_live_star_count(m.opera_stars)'),
        ("_normalise_save", "var raw_opera_stars := clampi(", '_nonnegative_int_or_default(raw, "opera_stars", 0), 0,', '\tdata["comfy_games"] = comfy_state', '\tvar chapter_two_state := ChapterTwoDirector.normalise_save_patch('),
        ("_normalise_save", "var opera_stars: int = clampi(", '_nonnegative_int_or_default(raw, "opera_stars", (1 << opera_prog) - 1), 0,', '\tvar opera_prog: int = clampi(_nonnegative_int_or_default(raw, "opera_progress", 0), 0, 16)', '\tdata["opera_stars"] = opera_stars'),
    )
    ceilings = []
    for function, prefix, arguments, before, after in sites:
        upper = _star_clamp(_without_comments(_function_body(text, function)), prefix, arguments, before, after)
        if upper == "JobData.STAR_CEILING":
            _require_preload(text)
            ceilings.append(data["STAR_CEILING"])
        else:
            ceilings.append(int(upper))
    if len(set(ceilings)) != 1:
        raise ValueError("the four commissioned SaveState star clamps differ")
    return {"SLOT_COUNT": slots, "STAR_CEILING": ceilings[0]}


def _require_normalization_site(lines: list[str], index: int, count: int) -> None:
    if index < 2 or lines[index - 2:index] != [
        '\tdata["teacher_learning_progress"] = TeacherLessonPlan.normalise_progress(',
        '\t\traw.get("teacher_learning_progress", {}))',
    ] or index + count >= len(lines) or lines[index + count] != '\tdata["stickers"] = _dictionary_or_default(raw, "stickers")':
        raise ValueError("checkpoint normalization moved from its immutable insertion site")


def read_checkpoint_order(root: Path, data: dict) -> list[str]:
    text = (Path(root) / SAVE_PATH).read_text(encoding="utf-8")
    body = _without_comments(_function_body(text, "_normalise_save"))
    literal_keys = _literal_checkpoint_keys(text)
    pairs = [(raw.rstrip(), code) for raw, code in zip(body.splitlines(), mask_source(body).splitlines()) if code.strip()]
    lines = [raw for raw, _ in pairs]
    code_lines = [code for _, code in pairs]
    if "JobData.SAVE_CHECKPOINT_JOB_ORDER" not in mask_source(body):
        by_key = {spec["key"]: jid for jid, spec in data["SAVE_CHECKPOINTS"].items()}
        if not literal_keys or any(key not in by_key for key in literal_keys):
            raise ValueError("missing or unregistered literal checkpoint normalization")
        starts = [i for i, line in enumerate(code_lines) if re.search(r"_\w+_checkpoint_or_default\(raw\)", line)]
        if len(starts) != len(LEGACY_NORMALIZATION_LINES) or tuple(lines[starts[0]:starts[0] + len(LEGACY_NORMALIZATION_LINES)]) != LEGACY_NORMALIZATION_LINES:
            raise ValueError("literal checkpoint normalization differs from fixed legacy sequence or indentation")
        _require_normalization_site(lines, starts[0], len(LEGACY_NORMALIZATION_LINES))
        return [by_key[key] for key in literal_keys]
    _require_preload(text)
    loop = ["\t" + NORMALIZATION_LOOP[0], *["\t\t" + line for line in NORMALIZATION_LOOP[1:]]]
    starts = [i for i, line in enumerate(code_lines) if "for checkpoint_job_id:" in line]
    if len(starts) != 1 or lines[starts[0]:starts[0] + len(loop)] != loop or literal_keys:
        raise ValueError("checkpoint normalization loop differs from fixed JP1 form or indentation")
    _require_normalization_site(lines, starts[0], len(loop))
    if sum("JobData.SAVE_CHECKPOINT_JOB_ORDER" in line for line in code_lines) != 1:
        raise ValueError("duplicate checkpoint normalization loop")
    return copy.deepcopy(data["SAVE_CHECKPOINT_JOB_ORDER"])
