class_name TeacherLessonPlan
extends RefCounted
## Deterministic, reading-free lesson selection and per-kind mastery state.
## All public dictionaries contain only JSON-safe scalar values and arrays.

const VERSION := 1
const KINDS: Array[String] = ["pattern", "count", "add", "match"]
const MAX_TIER := 2
const WINS_TO_PROMOTE := 3
const MAX_ROUNDS := 1000000

const CIRCLE := 0
const TRIANGLE := 1
const SQUARE := 2
const STAR := 3
const HEART := 4
const SHAPE_COUNT := 5


static func normalise_progress(raw: Variant) -> Dictionary:
	var source: Dictionary = raw as Dictionary if raw is Dictionary else {}
	var raw_kinds: Variant = source.get("kinds", {})
	var kind_sources: Dictionary = raw_kinds as Dictionary \
		if raw_kinds is Dictionary else source
	var kinds := {}
	for kind: String in KINDS:
		var raw_state: Variant = kind_sources.get(kind, {})
		var state: Dictionary = raw_state as Dictionary \
			if raw_state is Dictionary else {}
		kinds[kind] = {
			"tier": _safe_int(state.get("tier", 0), 0, MAX_TIER, 0),
			"clean_successes": _safe_int(state.get("clean_successes", 0),
				0, WINS_TO_PROMOTE - 1, 0),
			"rounds": _safe_int(state.get("rounds", 0), 0, MAX_ROUNDS, 0),
		}
	return {"version": VERSION, "kinds": kinds}


static func record_result(saved: Dictionary, kind: String,
		assisted: bool) -> Dictionary:
	var progress := normalise_progress(saved)
	if kind not in KINDS:
		return progress
	var kinds: Dictionary = progress["kinds"]
	var state: Dictionary = (kinds[kind] as Dictionary).duplicate()
	state["rounds"] = mini(MAX_ROUNDS, int(state["rounds"]) + 1)
	if not assisted:
		var clean := int(state["clean_successes"]) + 1
		var tier := int(state["tier"])
		if clean >= WINS_TO_PROMOTE and tier < MAX_TIER:
			tier += 1
			clean = 0
		state["tier"] = tier
		state["clean_successes"] = mini(WINS_TO_PROMOTE - 1, clean)
	kinds[kind] = state
	return progress


static func make_lesson(kind: String, saved: Dictionary) -> Dictionary:
	if kind not in KINDS:
		return {}
	var progress := normalise_progress(saved)
	var state: Dictionary = (progress["kinds"] as Dictionary)[kind]
	var tier := int(state["tier"])
	var sequence := int(state["rounds"])
	var lesson: Dictionary
	match kind:
		"pattern":
			lesson = _pattern_lesson(tier, sequence)
		"count":
			lesson = _count_lesson(tier, sequence)
		"add":
			lesson = _add_lesson(tier, sequence)
		"match":
			lesson = _match_lesson(tier, sequence)
	lesson["kind"] = kind
	lesson["tier"] = tier
	lesson["sequence"] = sequence
	lesson["target"] = int((lesson["choices"] as Array)[int(lesson["answer"])])
	return lesson


static func _pattern_lesson(tier: int, sequence: int) -> Dictionary:
	var a := sequence % SHAPE_COUNT
	var b := (a + 1 + sequence / SHAPE_COUNT) % SHAPE_COUNT
	if b == a:
		b = (a + 1) % SHAPE_COUNT
	var c := (b + 1) % SHAPE_COUNT
	if c == a:
		c = (c + 1) % SHAPE_COUNT
	var prompt: Array[int]
	var correct := a
	var distractors: Array[int] = [b]
	var choice_count := 2
	match tier:
		0:
			prompt = [a, b, a, b]
		1:
			prompt = [a, a, b, a, a, b]
			distractors = [b, c]
			choice_count = 3
		_:
			prompt = [a, b, c, a, b, c]
			distractors = [b, c]
			choice_count = 3
	var choice_data := _arrange_choices(correct, distractors,
		sequence, choice_count)
	return {"prompt_tokens": prompt, "choices": choice_data["choices"],
		"answer": choice_data["answer"], "operands": []}


static func _count_lesson(tier: int, sequence: int) -> Dictionary:
	var maximum: int = [3, 5, 10][tier]
	var quantity := 1 + sequence % maximum
	var shape := (sequence / maximum + tier) % SHAPE_COUNT
	var prompt := _repeat_token(shape, quantity)
	var distractors := _nearby_values(quantity, 1, maximum)
	var choice_count := 2 if tier == 0 else 3
	var choice_data := _arrange_choices(quantity, distractors,
		sequence + tier, choice_count)
	return {"prompt_tokens": prompt, "choices": choice_data["choices"],
		"answer": choice_data["answer"], "operands": []}


static func _add_lesson(tier: int, sequence: int) -> Dictionary:
	var pairs: Array[Array] = []
	match tier:
		0:
			pairs = [[1, 1], [1, 2]]
		1:
			pairs = [[1, 2], [1, 3], [2, 2], [2, 3]]
		_:
			pairs = [[2, 3], [3, 3], [3, 4], [4, 4], [4, 5], [5, 5]]
	var pair: Array = pairs[sequence % pairs.size()]
	var left := int(pair[0])
	var right := int(pair[1])
	var total := left + right
	var maximum: int = [3, 5, 10][tier]
	var shape := (sequence / pairs.size() + tier + 2) % SHAPE_COUNT
	var distractors := _nearby_values(total, 2, maximum)
	var choice_count := 2 if tier == 0 else 3
	var choice_data := _arrange_choices(total, distractors,
		sequence + tier, choice_count)
	return {"prompt_tokens": _repeat_token(shape, total),
		"choices": choice_data["choices"], "answer": choice_data["answer"],
		"operands": [left, right]}


static func _match_lesson(tier: int, sequence: int) -> Dictionary:
	var target := (sequence + tier) % SHAPE_COUNT
	var distractors: Array[int] = []
	for offset in range(1, SHAPE_COUNT):
		distractors.append((target + offset) % SHAPE_COUNT)
	var choice_count: int = [2, 3, 4][tier]
	var choice_data := _arrange_choices(target, distractors,
		sequence + tier, choice_count)
	return {"prompt_tokens": [target], "choices": choice_data["choices"],
		"answer": choice_data["answer"], "operands": []}


static func _arrange_choices(correct: int, distractors: Array[int],
		sequence: int, choice_count: int) -> Dictionary:
	var values: Array[int] = [correct]
	for distractor: int in distractors:
		if distractor != correct and distractor not in values:
			values.append(distractor)
		if values.size() >= choice_count:
			break
	var shift := sequence % values.size()
	var choices: Array[int] = []
	for index in range(values.size()):
		choices.append(values[(index + shift) % values.size()])
	return {"choices": choices, "answer": choices.find(correct)}


static func _nearby_values(correct: int, minimum: int,
		maximum: int) -> Array[int]:
	var values: Array[int] = []
	for distance in range(1, maximum - minimum + 1):
		for candidate: int in [correct - distance, correct + distance]:
			if candidate >= minimum and candidate <= maximum \
					and candidate != correct and candidate not in values:
				values.append(candidate)
	return values


static func _repeat_token(token: int, count: int) -> Array[int]:
	var tokens: Array[int] = []
	for _index in range(count):
		tokens.append(token)
	return tokens


static func _safe_int(raw: Variant, minimum: int, maximum: int,
		fallback: int) -> int:
	if typeof(raw) not in [TYPE_INT, TYPE_FLOAT]:
		return fallback
	var number := float(raw)
	if not is_finite(number) or number != floorf(number):
		return fallback
	return clampi(int(number), minimum, maximum)
