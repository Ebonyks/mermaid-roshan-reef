extends SceneTree
func _initialize() -> void:
	var image_0 := Image.new()
	assert(image_0.load_svg_from_string(FileAccess.get_file_as_string("res://assets_src/vector/job_geology_teacher_refinement_v1_20261001/geologist_fossil_v2.svg")) == OK)
	assert(image_0.save_png("res://assets_src/vector/job_geology_teacher_refinement_v1_20261001/geologist_fossil_v2_native.png") == OK)
	var image_1 := Image.new()
	assert(image_1.load_svg_from_string(FileAccess.get_file_as_string("res://assets_src/vector/job_geology_teacher_refinement_v1_20261001/geologist_layered_rock_v2.svg")) == OK)
	assert(image_1.save_png("res://assets_src/vector/job_geology_teacher_refinement_v1_20261001/geologist_layered_rock_v2_native.png") == OK)
	var image_2 := Image.new()
	assert(image_2.load_svg_from_string(FileAccess.get_file_as_string("res://assets_src/vector/job_geology_teacher_refinement_v1_20261001/teacher_lesson_board_v2.svg")) == OK)
	assert(image_2.save_png("res://assets_src/vector/job_geology_teacher_refinement_v1_20261001/teacher_lesson_board_v2_native.png") == OK)
	print("JOB_VECTOR_ATTEMPT02|3_NATIVE_PREVIEWS|REVIEW_PENDING")
	quit(0)
