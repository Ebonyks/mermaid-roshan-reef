class_name OperaMastery
extends RefCounted
## Pure, deterministic mastery and Encore-token ledger for staged Opera acts.
##
## The caller records only the on-stage act. Intro/practice interactions never
## enter these stats. `active_seconds` is interaction time with pause intervals
## removed; wall-clock time and `paused_seconds` are deliberately ignored.
## `actions` counts four unique progress-quarter milestones per on-stage phase;
## it never counts raw input events. `misses` counts incorrect or off-target
## inputs, and `assists` counts revealed answers or guided actions. Repeated
## held frames, duplicate taps, demo fingers, and helper animation cannot add a
## quarter, so input spam and frame rate cannot improve a tier.
## A confirmed completion always earns bronze even when optional telemetry is
## absent or malformed. Better tiers require every metric to be valid.

const NONE := 0
const BRONZE := 1
const SILVER := 2
const GOLD := 3
const VERSION := 1

const CAREERS: Array[String] = [
	"chef", "detective", "ballerina", "candymaker", "doctor", "farmer",
	"boxer", "magician", "painter", "astronaut", "racer", "popstar",
	"nursery", "geologist", "teacher",
]

# Cumulative lifetime value of the best medal. An upgrade therefore grants
# 1 token for bronze, 2 more for silver, and 3 more for gold.
const TIER_VALUE := {NONE: 0, BRONZE: 1, SILVER: 3, GOLD: 6}

# Explicit per-career calibration for the four observable stage metrics.
# Gold means an independent, precise act. Silver allows limited correction and
# one guided cue. These are data so playtest tuning never changes ledger math.
const RULES := {
	"chef":       {"min_actions": 20, "gold_seconds": 38.0, "silver_seconds": 64.0, "silver_misses": 2, "silver_assists": 1},
	"detective":  {"min_actions": 12, "gold_seconds": 42.0, "silver_seconds": 72.0, "silver_misses": 2, "silver_assists": 1},
	"ballerina":  {"min_actions": 12, "gold_seconds": 54.0, "silver_seconds": 86.0, "silver_misses": 2, "silver_assists": 1},
	"candymaker": {"min_actions": 16, "gold_seconds": 40.0, "silver_seconds": 66.0, "silver_misses": 2, "silver_assists": 1},
	"doctor":     {"min_actions": 20, "gold_seconds": 42.0, "silver_seconds": 70.0, "silver_misses": 2, "silver_assists": 1},
	"farmer":     {"min_actions": 16, "gold_seconds": 40.0, "silver_seconds": 68.0, "silver_misses": 3, "silver_assists": 1},
	"boxer":      {"min_actions": 20, "gold_seconds": 36.0, "silver_seconds": 60.0, "silver_misses": 2, "silver_assists": 1},
	"magician":   {"min_actions": 20, "gold_seconds": 40.0, "silver_seconds": 68.0, "silver_misses": 2, "silver_assists": 1},
	"painter":    {"min_actions": 12, "gold_seconds": 40.0, "silver_seconds": 68.0, "silver_misses": 2, "silver_assists": 1},
	"astronaut":  {"min_actions": 16, "gold_seconds": 42.0, "silver_seconds": 70.0, "silver_misses": 2, "silver_assists": 1},
	"racer":      {"min_actions": 12, "gold_seconds": 46.0, "silver_seconds": 64.0, "silver_misses": 3, "silver_assists": 1},
	"popstar":    {"min_actions": 16, "gold_seconds": 40.0, "silver_seconds": 66.0, "silver_misses": 2, "silver_assists": 1},
	"nursery":    {"min_actions": 20, "gold_seconds": 48.0, "silver_seconds": 78.0, "silver_misses": 3, "silver_assists": 1},
	"geologist":  {"min_actions": 16, "gold_seconds": 58.0, "silver_seconds": 92.0, "silver_misses": 2, "silver_assists": 1},
	"teacher":    {"min_actions": 16, "gold_seconds": 60.0, "silver_seconds": 90.0, "silver_misses": 1, "silver_assists": 1},
}


static func evaluate(career: String, stats: Variant) -> int:
	if career not in CAREERS or not (stats is Dictionary):
		return NONE
	var values := stats as Dictionary
	var completed: Variant = values.get("stage_completed")
	if not (completed is bool) or not bool(completed):
		return NONE
	var practice: Variant = values.get("practice", false)
	if practice is bool:
		if bool(practice):
			return NONE
	else:
		return BRONZE

	var actions := _read_nonnegative_int(values.get("actions"))
	var misses := _read_nonnegative_int(values.get("misses"))
	var assists := _read_nonnegative_int(values.get("assists"))
	var active_seconds := _read_positive_float(values.get("active_seconds"))
	if actions < 0 or misses < 0 or assists < 0 or active_seconds < 0.0:
		return BRONZE

	var rule: Dictionary = RULES[career]
	if actions < int(rule["min_actions"]):
		return BRONZE
	if misses == 0 and assists == 0 \
			and active_seconds <= float(rule["gold_seconds"]):
		return GOLD
	if misses <= int(rule["silver_misses"]) \
			and assists <= int(rule["silver_assists"]) \
			and active_seconds <= float(rule["silver_seconds"]):
		return SILVER
	return BRONZE


static func normalise(raw: Variant) -> Dictionary:
	var source: Dictionary = raw as Dictionary if raw is Dictionary else {}
	var raw_tiers: Variant = source.get("best_tiers", source.get("tiers", {}))
	var tiers_source: Dictionary = raw_tiers as Dictionary \
		if raw_tiers is Dictionary else {}
	var best_tiers: Dictionary = {}
	var implied_earned := 0
	for career: String in CAREERS:
		var tier := _read_bounded_int(tiers_source.get(career), NONE, GOLD, NONE)
		best_tiers[career] = tier
		implied_earned += int(TIER_VALUE[tier])

	var wallet_raw: Variant = source.get("encore_tokens", {})
	var wallet_source: Dictionary = wallet_raw as Dictionary \
		if wallet_raw is Dictionary else {}
	var legacy_balance: Variant = wallet_raw if wallet_raw is int or wallet_raw is float \
		else source.get("encore_token_balance")
	var balance := _read_nonnegative_int(wallet_source.get("balance", legacy_balance))
	var earned := _read_nonnegative_int(wallet_source.get(
		"total_earned", source.get("encore_tokens_earned")))
	var spent := _read_nonnegative_int(wallet_source.get(
		"total_spent", source.get("encore_tokens_spent")))
	balance = maxi(0, balance)
	earned = maxi(0, earned)
	spent = maxi(0, spent)
	# Preserve a valid current balance and reconcile missing lifetime fields
	# conservatively as already spent. Best medals never create retroactive cash.
	earned = maxi(maxi(earned, balance + spent), implied_earned)
	spent = maxi(spent, earned - balance)
	earned = balance + spent

	return {
		"version": VERSION,
		"best_tiers": best_tiers,
		"encore_tokens": {
			"balance": balance,
			"total_earned": earned,
			"total_spent": spent,
		},
	}


static func apply_result(saved: Variant, career: String, stats: Variant) -> Dictionary:
	var ledger := normalise(saved)
	var tier := evaluate(career, stats)
	var previous_tier := int((ledger["best_tiers"] as Dictionary).get(career, NONE)) \
		if career in CAREERS else NONE
	var best_tier := maxi(previous_tier, tier)
	var token_delta := 0
	if career in CAREERS and best_tier > previous_tier:
		token_delta = int(TIER_VALUE[best_tier]) - int(TIER_VALUE[previous_tier])
		(ledger["best_tiers"] as Dictionary)[career] = best_tier
		var wallet := ledger["encore_tokens"] as Dictionary
		wallet["balance"] = int(wallet["balance"]) + token_delta
		wallet["total_earned"] = int(wallet["total_earned"]) + token_delta
	return {
		"ledger": ledger,
		"tier": tier,
		"previous_tier": previous_tier,
		"best_tier": best_tier,
		"token_delta": token_delta,
		"upgraded": best_tier > previous_tier,
	}


static func _read_nonnegative_int(raw: Variant) -> int:
	return _read_bounded_int(raw, 0, 2147483647, -1)


static func _read_bounded_int(raw: Variant, minimum: int,
		maximum: int, fallback: int) -> int:
	if raw is bool:
		return fallback
	if raw is int:
		var integer := int(raw)
		return integer if integer >= minimum and integer <= maximum else fallback
	if raw is float:
		var number := float(raw)
		if is_finite(number) and number == floor(number) \
				and number >= float(minimum) and number <= float(maximum):
			return int(number)
	return fallback


static func _read_positive_float(raw: Variant) -> float:
	if raw is bool or not (raw is int or raw is float):
		return -1.0
	var number := float(raw)
	return number if is_finite(number) and number > 0.0 else -1.0
