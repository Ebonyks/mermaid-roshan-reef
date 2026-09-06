extends SceneTree
## Focused pure-model probe for Opera mastery and Encore-token persistence.

const Mastery := preload("res://scripts/opera_mastery.gd")

var failures := 0


func _initialize() -> void:
	_probe_thresholds()
	_probe_invalid_and_practice()
	_probe_upgrade_ledger()
	_probe_spending_and_legacy()
	if failures == 0:
		print("OPERAMASTERY|result: ALL OK")
		quit(0)
	else:
		print("OPERAMASTERY|result: %d FAIL" % failures)
		quit(1)


func _probe_thresholds() -> void:
	var all_explicit := Mastery.CAREERS.size() == 15 \
		and Mastery.RULES.size() == Mastery.CAREERS.size()
	for career: String in Mastery.CAREERS:
		var rule: Dictionary = Mastery.RULES[career]
		all_explicit = all_explicit \
			and int(rule.get("min_actions", 0)) > 0 \
			and float(rule.get("gold_seconds", 0.0)) > 0.0 \
			and float(rule.get("silver_seconds", 0.0)) \
				> float(rule.get("gold_seconds", 0.0))
		var precise := _stats(rule, 0, 0, float(rule["gold_seconds"]))
		var competent := _stats(rule, int(rule["silver_misses"]),
			int(rule["silver_assists"]), float(rule["silver_seconds"]))
		var completed := _stats(rule, int(rule["silver_misses"]) + 1,
			int(rule["silver_assists"]) + 1, float(rule["silver_seconds"]) + 1.0)
		all_explicit = all_explicit \
			and Mastery.evaluate(career, precise) == Mastery.GOLD \
			and Mastery.evaluate(career, competent) == Mastery.SILVER \
			and Mastery.evaluate(career, completed) == Mastery.BRONZE
	_check("all fifteen careers have explicit bronze, competence, and precision rules",
		all_explicit)

	var racer_rule: Dictionary = Mastery.RULES["racer"]
	var unpaused := _stats(racer_rule, 0, 0, float(racer_rule["gold_seconds"]))
	var paused := unpaused.duplicate(true)
	paused["paused_seconds"] = 3600.0
	_check("pause duration is excluded from mastery time",
		Mastery.evaluate("racer", unpaused) == Mastery.GOLD
		and Mastery.evaluate("racer", paused) == Mastery.GOLD)


func _probe_invalid_and_practice() -> void:
	_check("incomplete, practice, and unknown acts award nothing",
		Mastery.evaluate("chef", {"stage_completed": false}) == Mastery.NONE
		and Mastery.evaluate("chef", {"stage_completed": true, "practice": true}) \
			== Mastery.NONE
		and Mastery.evaluate("unknown", {"stage_completed": true}) == Mastery.NONE)
	var malformed_cases: Array[Variant] = [
		{"stage_completed": true},
		{"stage_completed": true, "actions": true, "misses": 0,
			"assists": 0, "active_seconds": 10.0},
		{"stage_completed": true, "actions": 20, "misses": "0",
			"assists": 0, "active_seconds": 10.0},
		{"stage_completed": true, "actions": 20, "misses": 0,
			"assists": 0, "active_seconds": NAN},
		{"stage_completed": true, "practice": "false", "actions": 20,
			"misses": 0, "assists": 0, "active_seconds": 10.0},
	]
	var safe_bronze := true
	for malformed: Variant in malformed_cases:
		safe_bronze = safe_bronze \
			and Mastery.evaluate("chef", malformed) == Mastery.BRONZE
	_check("confirmed completion falls back strictly and safely to bronze",
		safe_bronze)


func _probe_upgrade_ledger() -> void:
	var rule: Dictionary = Mastery.RULES["teacher"]
	var bronze_stats := _stats(rule, 5, 2, float(rule["silver_seconds"]) + 1.0)
	var silver_stats := _stats(rule, 1, 1, float(rule["silver_seconds"]))
	var gold_stats := _stats(rule, 0, 0, float(rule["gold_seconds"]))
	var bronze := Mastery.apply_result({}, "teacher", bronze_stats)
	var silver := Mastery.apply_result(bronze["ledger"], "teacher", silver_stats)
	var replay := Mastery.apply_result(silver["ledger"], "teacher", bronze_stats)
	var gold := Mastery.apply_result(replay["ledger"], "teacher", gold_stats)
	var gold_replay := Mastery.apply_result(gold["ledger"], "teacher", gold_stats)
	var wallet: Dictionary = gold_replay["ledger"]["encore_tokens"]
	_check("bronze, silver, and gold upgrades grant cumulative 1, 3, and 6 tokens",
		int(bronze["token_delta"]) == 1 and int(silver["token_delta"]) == 2
		and int(replay["token_delta"]) == 0 and int(gold["token_delta"]) == 3
		and int(gold_replay["token_delta"]) == 0
		and int(wallet["balance"]) == 6 and int(wallet["total_earned"]) == 6
		and int(wallet["total_spent"]) == 0
		and int(gold_replay["best_tier"]) == Mastery.GOLD)

	var chef_rule: Dictionary = Mastery.RULES["chef"]
	var second_career := Mastery.apply_result(gold_replay["ledger"], "chef",
		_stats(chef_rule, 0, 0, float(chef_rule["gold_seconds"])))
	_check("each career contributes its achievement value once",
		int(second_career["token_delta"]) == 6
		and int(second_career["ledger"]["encore_tokens"]["balance"]) == 12)

	var spent_silver: Dictionary = silver["ledger"].duplicate(true)
	spent_silver["encore_tokens"]["balance"] = 1
	spent_silver["encore_tokens"]["total_spent"] = 2
	var upgrade_after_spend := Mastery.apply_result(spent_silver, "teacher", gold_stats)
	var upgraded_wallet: Dictionary = upgrade_after_spend["ledger"]["encore_tokens"]
	_check("a later medal upgrade preserves spending and adds only its delta",
		int(upgrade_after_spend["token_delta"]) == 3
		and int(upgraded_wallet["balance"]) == 4
		and int(upgraded_wallet["total_earned"]) == 6
		and int(upgraded_wallet["total_spent"]) == 2)


func _probe_spending_and_legacy() -> void:
	var spent_gold := Mastery.normalise({
		"best_tiers": {"racer": Mastery.GOLD},
		"encore_tokens": {"balance": 0, "total_earned": 6, "total_spent": 6},
	})
	var racer_rule: Dictionary = Mastery.RULES["racer"]
	var replay := Mastery.apply_result(spent_gold, "racer",
		_stats(racer_rule, 0, 0, float(racer_rule["gold_seconds"])))
	_check("spending leaves lifetime totals intact and replay cannot regrant tokens",
		int(replay["token_delta"]) == 0
		and int(replay["ledger"]["encore_tokens"]["balance"]) == 0
		and int(replay["ledger"]["encore_tokens"]["total_earned"]) == 6
		and int(replay["ledger"]["encore_tokens"]["total_spent"]) == 6)

	var legacy := Mastery.normalise({
		"tiers": {"chef": 3.0, "teacher": true, "racer": 2.5},
		"encore_tokens": 2,
		"encore_tokens_spent": 4,
	})
	var legacy_wallet: Dictionary = legacy["encore_tokens"]
	_check("legacy and malformed ledger data normalises without retroactive cash",
		int(legacy["best_tiers"]["chef"]) == Mastery.GOLD
		and int(legacy["best_tiers"]["teacher"]) == Mastery.NONE
		and int(legacy["best_tiers"]["racer"]) == Mastery.NONE
		and int(legacy_wallet["balance"]) == 2
		and int(legacy_wallet["total_earned"]) == 6
		and int(legacy_wallet["total_spent"]) == 4)

	var medal_only := Mastery.normalise({"best_tiers": {"geologist": 3}})
	var medal_replay := Mastery.apply_result(medal_only, "geologist",
		_stats(Mastery.RULES["geologist"], 0, 0,
			float(Mastery.RULES["geologist"]["gold_seconds"])))
	_check("a legacy best medal is treated as already earned and already spent",
		int(medal_only["encore_tokens"]["balance"]) == 0
		and int(medal_only["encore_tokens"]["total_earned"]) == 6
		and int(medal_only["encore_tokens"]["total_spent"]) == 6
		and int(medal_replay["token_delta"]) == 0)


func _stats(rule: Dictionary, misses: int, assists: int,
		active_seconds: float) -> Dictionary:
	return {
		"stage_completed": true,
		"practice": false,
		"actions": int(rule["min_actions"]),
		"misses": misses,
		"assists": assists,
		"active_seconds": active_seconds,
	}


func _check(label: String, condition: bool) -> void:
	if condition:
		print("OPERAMASTERY|OK|%s" % label)
	else:
		failures += 1
		print("OPERAMASTERY|FAIL|%s" % label)
