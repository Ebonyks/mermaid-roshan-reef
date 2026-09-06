class_name OperaPerformancePlan
extends RefCounted
## Career lessons reused in a separate stage performance. Story adapters opt out.

const VERSION := 1
# First rollout follows the physical Opera Hall venue. Other career maps are
# recommendations ready for a later, explicit wider rollout.
const ENABLED: Array[String] = ["ballerina", "magician", "popstar"]
const PRACTICE_COUNTS := {
	"chef": 3, "detective": 2, "ballerina": 3, "candymaker": 2,
	"doctor": 3, "farmer": 2, "boxer": 3, "magician": 3,
	"painter": 2, "astronaut": 2, "racer": 2, "popstar": 3,
	"nursery": 4, "geologist": 4, "teacher": 4,
}

static func enabled(career: String, config: Dictionary) -> bool:
	return career in ENABLED and not bool(config.get("chapter2_tutorial", false)) \
		and String(config.get("reward_policy", "")) != "chapter2_story" \
		and not config.has("phase_overrides") and not config.has("scene_adapter")

static func build(career: String, source: Array) -> Dictionary:
	var phases: Array[Dictionary] = []
	var practice := mini(int(PRACTICE_COUNTS.get(career, source.size())), source.size())
	for index in range(practice):
		var phase := (source[index] as Dictionary).duplicate(true)
		phase["performance_part"] = "practice"
		phase["source_phase"] = index
		phases.append(phase)
	for index in range(source.size()):
		var phase := (source[index] as Dictionary).duplicate(true)
		phase["performance_part"] = "stage"
		phase["source_phase"] = index
		phases.append(phase)
	return {"version": VERSION, "phases": phases, "stage_start": practice}
