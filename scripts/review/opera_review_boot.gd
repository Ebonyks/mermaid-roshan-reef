extends Node
## Explicit review entry point. Never attaches itself to a normal child profile.

func _ready() -> void:
	print("OPERA_TRANSLATION|BOOT_ENTRY")
	call_deferred("_open_review")

func _open_review() -> void:
	if DisplayServer.get_name()=="headless":
		return
	var profile: String = str(ProjectSettings.get_setting("application/config/custom_user_dir_name", ""))
	if profile != "MermaidReef-OperaRemovalReview-20261017":
		push_error("Opera v1 requires its isolated review profile")
		return
	for index: int in range(120):
		if get_tree().current_scene is ReefMain:
			break
		await get_tree().process_frame
	var main: ReefMain = get_tree().current_scene as ReefMain
	if main==null:
		push_error("Opera review requires the existing main state owner")
		return
	for index: int in range(3):
		await get_tree().process_frame
	main.day_one_active = false
	main.chapter2_active = false
	main.start_menu_active = false
	if main.start_menu_layer != null:
		main.start_menu_layer.hide()
	main._skip_intro()
	main.game = "level2"
	main.g["t"] = 0.0
	main._enter_castle_interior_now(false)
	print("OPERA_TRANSLATION|CASTLE_ENTERED")
	for index: int in range(30):
		await get_tree().process_frame
	main._castle_rooms_ref().show_room("opera_hall", false)
	for index: int in range(12):
		await get_tree().process_frame
	if main.fade_rect != null:
		main.fade_rect.modulate.a = 0.0
	var venue: OperaHouseVenue2D = main._castle_career_routes_ref().opera_venue
	if venue.find_child("OperaExplorationV1",false,false)!=null:
		return
	var scene: PackedScene = load("res://scenes/review/opera_exploration_v1.tscn") as PackedScene
	var review: Control = scene.instantiate() as Control
	venue.add_child(review)
	review.setup(main, venue)
	print("OPERA_TRANSLATION|READY")
