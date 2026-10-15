extends SceneTree
func _initialize() -> void:
	var original := {"keep": [3, 7], "token": "R53_PRIVATE_ONLY"}
	var parsed: Variant = JSON.parse_string(JSON.stringify(original))
	var normalized: Variant = JSON.parse_string(JSON.stringify(original))
	var mutated: Variant = JSON.parse_string(JSON.stringify(original))
	mutated["keep"][0] = 4.0
	var result := {"raw_strict_equal": original == parsed, "json_domain_equal": normalized == parsed, "changed_value_equal": normalized == mutated, "seed_number_type": typeof(original["keep"][0]), "parsed_number_type": typeof(parsed["keep"][0])}
	print("UNKNOWN_COMPARISON|", JSON.stringify(result))
	quit(0 if not result["raw_strict_equal"] and result["json_domain_equal"] and not result["changed_value_equal"] else 1)
