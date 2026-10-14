extends SceneTree
## Executes exact current fixture helper with independent corruption cases, not production save schema changes.
func _init() -> void:
	var text: String=FileAccess.get_file_as_string("res://docs/handoffs/codex_flat_vector_art_2026-10-07/r39_craft_compositor_context/capture_craft_context.gd")
	var start: int=text.find("func _gene_rows_equal(")
	var end: int=text.find("\nfunc _run_case(",start)
	var code: GDScript=GDScript.new()
	code.source_code="extends RefCounted\n"+text.substr(start,end-start)
	if start<0 or end<0 or code.reload()!=OK:
		quit(1)
		return
	var helper: RefCounted=code.new()
	var fish: Array=[0.9,0.3,0.3,1.0,0.8,0.2,1,0]
	var friend: Array=["cat",0.9,0.3,0.3,1.0,0.8,0.2,1,0,0.9,0.8,0.7]
	var cases: Array[Dictionary]=[]
	cases.append({"name":"JSON numeric types fish flags","pass":helper._gene_rows_equal([fish],JSON.parse_string(JSON.stringify([fish])))})
	cases.append({"name":"JSON numeric types friend flags","pass":helper._gene_rows_equal([friend],JSON.parse_string(JSON.stringify([friend])))})
	var changed: Array=fish.duplicate()
	changed[6]=0
	cases.append({"name":"changed fish flag rejected","pass":not helper._gene_rows_equal([fish],[changed])})
	changed=friend.duplicate()
	changed[8]=1
	cases.append({"name":"changed friend flag rejected","pass":not helper._gene_rows_equal([friend],[changed])})
	changed=friend.duplicate()
	changed[0]="bird"
	cases.append({"name":"changed identity rejected","pass":not helper._gene_rows_equal([friend],[changed])})
	changed=fish.duplicate()
	changed[0]=0.92
	cases.append({"name":"changed body color rejected","pass":not helper._gene_rows_equal([fish],[changed])})
	changed=friend.duplicate()
	changed[11]=0.6
	cases.append({"name":"changed detail color rejected","pass":not helper._gene_rows_equal([friend],[changed])})
	changed=fish.duplicate()
	changed.pop_back()
	cases.append({"name":"missing field rejected","pass":not helper._gene_rows_equal([fish],[changed])})
	cases.append({"name":"missing row rejected","pass":not helper._gene_rows_equal([fish],[])})
	for row: Dictionary in cases:
		if not row["pass"]:
			print("R39_NUMERIC_HELPER_FAIL|",row["name"])
			quit(1)
			return
	print("R39_NUMERIC_HELPER_ALL_OK|",JSON.stringify(cases))
	quit(0)
