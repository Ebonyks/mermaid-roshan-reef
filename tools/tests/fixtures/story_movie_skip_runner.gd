extends SceneTree
const CASES := preload("res://tools/tests/fixtures/story_movie_skip_cases.gd")
var failures: int = 0

func _init() -> void:
	call_deferred("_run")

func _check(label: String, passed: bool) -> void:
	if not passed:
		failures += 1
	print("STORY_MOVIE_SKIP|", label, ": ", "OK" if passed else "FAIL")

func _run() -> void:
	await CASES.new().run(self, Callable(self, "_check"))
	print("STORY_MOVIE_SKIP|RESULT: ", "PASS" if failures == 0 else "FAIL")
	quit(1 if failures > 0 else 0)
