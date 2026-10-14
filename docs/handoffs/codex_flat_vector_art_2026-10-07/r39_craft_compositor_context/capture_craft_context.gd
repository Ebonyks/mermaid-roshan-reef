extends SceneTree
## Current Craft compositor context. Production GUI, synthetic private profiles, no runtime/source edits.
var m: ReefMain
var out_dir := ""
var states: Array[Dictionary] = []
var errors: Array[String] = []
var normal_before: Dictionary = {}
var case_receipts: Array[Dictionary] = []
var active_profile := ""
var active_seed: Dictionary = {}

func _init() -> void:
	call_deferred("_run")

func _normal_hashes() -> Dictionary:
	var result: Dictionary = {}
	var base := ProjectSettings.globalize_path("user://reef_save.json")
	for suffix: String in ["", ".bak", ".tmp", ".tmp0", ".tmp1", ".old", ".bak.tmp", ".bak.old"]:
		var path := base + suffix
		result[suffix] = FileAccess.get_sha256(path) if FileAccess.file_exists(path) else "absent"
	return result

func _wait_frames(count: int) -> void:
	for i: int in range(count):
		await process_frame

func _set_aspect(target: Vector2i) -> bool:
	get_root().mode = Window.MODE_WINDOWED
	for i: int in range(180):
		DisplayServer.window_set_position(Vector2i(-2400, 0))
		get_root().size = target
		DisplayServer.window_set_size(target)
		await process_frame
		var test: Image = get_root().get_texture().get_image()
		if test != null and test.get_size() == target:
			return true
	return false

func _visible_nodes(node: Node, output: Array[Dictionary]) -> void:
	var item := node as CanvasItem
	if item != null and item.is_visible_in_tree():
		var row: Dictionary = {"path": str(node.get_path()), "class": node.get_class(), "modulate": str(item.modulate), "z_index": item.z_index}
		var control := node as Control
		if control != null:
			row["global_rect"] = str(control.get_global_rect())
		var texture := node as TextureRect
		if texture != null and texture.texture != null:
			row["texture"] = texture.texture.resource_path
		var button := node as Button
		if button != null:
			row["disabled"] = button.disabled
		output.append(row)
	for child: Node in node.get_children():
		_visible_nodes(child, output)

func _presentation() -> Dictionary:
	return {"boot_splash_present": m.get_node_or_null("BootSplashHandoff") != null, "start_menu_active": m.start_menu_active, "start_menu_layer_present": m.start_menu_layer != null, "intro_active": m.intro_active, "intro_layer_present": m.intro_layer != null, "fade_alpha": m.fade_rect.modulate.a if m.fade_rect != null else 0.0, "medal_present": m.get_node_or_null("MedalCelebrationLayer") != null}

func _wait_presentation() -> bool:
	for i: int in range(300):
		await process_frame
		var present := _presentation()
		if not bool(present["boot_splash_present"]) and not bool(present["start_menu_active"]) and not bool(present["start_menu_layer_present"]) and not bool(present["intro_active"]) and not bool(present["intro_layer_present"]) and float(present["fade_alpha"]) <= 0.02:
			return true
	return false

func _capture(id: String, input_info: Dictionary = {}) -> void:
	await RenderingServer.frame_post_draw
	var presentation := _presentation()
	if bool(presentation["boot_splash_present"]) or bool(presentation["start_menu_active"]) or bool(presentation["medal_present"]) or float(presentation["fade_alpha"]) > 0.02:
		errors.append("blocking/foreign presentation overlay " + id)
	var frame: Image = get_root().get_texture().get_image()
	var target := get_root().size
	if frame == null or frame.get_size() != target:
		errors.append("image backing mismatch " + id)
		return
	var path := out_dir.path_join(id + ".png")
	if frame.save_png(path) != OK:
		errors.append("save failed " + id)
		return
	var visible: Array[Dictionary] = []
	if m.craft_layer != null:
		_visible_nodes(m.craft_layer, visible)
	var image_file := FileAccess.open(path, FileAccess.READ)
	states.append({"id": id, "image": {"file": id + ".png", "sha256": FileAccess.get_sha256(path), "bytes": image_file.get_length(), "dimensions": [frame.get_width(),frame.get_height()]}, "presentation": presentation, "kind": m.craft_kind, "part": m.craft_part, "body": str(m.craft_body), "accent": str(m.craft_fins), "third": str(m.craft_c3), "body_rainbow": m.craft_body_rb, "accent_rainbow": m.craft_fins_rb, "pearls": m.pearl_count, "input": input_info, "visible_nodes": visible, "synthetic_profile":active_profile, "profile_is_actual_child_data":false, "custom_fish":m.custom_fish.duplicate(true), "custom_friends":m.custom_friends.duplicate(true), "craft_unlocks":m.craft_unlocks.duplicate(true), "closing":bool(m.get_meta("craft_closing",false)), "preview_layers":_layer_metadata(), "ticks_msec":Time.get_ticks_msec(), "main_hud_visible": m.hud_layer.visible if m.hud_layer != null else false, "save_path": m._save_state.save_path})
	image_file.close()
	print("CRAFT39|CAPTURE|" + id)

func _swatch(index: int) -> Button:
	var want: Color = CraftStudio.PALETTE[index]
	for node: Node in get_nodes_in_group("craft_palette_button"):
		var button := node as Button
		if button == null or button.is_queued_for_deletion() or not m.craft_layer.is_ancestor_of(button):
			continue
		var style := button.get_theme_stylebox("normal") as StyleBoxFlat
		if style != null and style.bg_color.is_equal_approx(want):
			return button
	return null

func _find(name: String) -> Button:
	return m.craft_layer.find_child(name,true,false) as Button

func _raw_button(button: Button, pressed: bool) -> void:
	var where := button.get_global_rect().get_center()
	var event := InputEventMouseButton.new()
	event.button_index = MOUSE_BUTTON_LEFT
	event.pressed = pressed
	event.position = where
	event.global_position = where
	get_root().push_input(event,true)
	await process_frame

func _tap(button: Button) -> void:
	if button == null:
		errors.append("current button missing")
		return
	await _raw_button(button,true)
	await _raw_button(button,false)
	await _wait_frames(3)

func _current_color() -> Color:
	return m.craft_body if m.craft_part == "body" else (m.craft_fins if m.craft_part == "accent" else m.craft_c3)

func _rainbow() -> Button:
	for node: Node in get_nodes_in_group("craft_palette_button"):
		var button := node as Button
		if button != null and not button.is_queued_for_deletion() and m.craft_layer.is_ancestor_of(button) and button.text == "🌈":
			return button
	return null

func _layer_metadata() -> Array[Dictionary]:
	var rows: Array[Dictionary] = []
	if m.craft_fishbox == null:
		return rows
	for node: Node in m.craft_fishbox.get_children():
		var tr := node as TextureRect
		if tr == null or tr.is_queued_for_deletion() or tr.texture == null:
			continue
		var ts: Vector2 = tr.texture.get_size()
		var fit: float = minf(tr.size.x / maxf(ts.x,1.0), tr.size.y / maxf(ts.y,1.0))
		rows.append({"role":String(tr.get_meta("role","")),"texture":tr.texture.resource_path,"texture_dimensions":[int(ts.x),int(ts.y)],"control_rect":str(tr.get_global_rect()),"fit":fit,"drawn_texture_size":str(ts*fit),"drawn_texture_local_origin":str((tr.size-ts*fit)*0.5),"modulate":str(tr.modulate),"mouse_filter":tr.mouse_filter,"material":tr.material.resource_path if tr.material != null else "none","fx_tween_present":tr.has_meta("fxtw")})
	return rows

func _delay(seconds: float) -> void:
	await create_timer(seconds).timeout
	await _wait_frames(2)

func _seed(legacy: bool) -> Dictionary:
	if not legacy:
		return {}
	return {"schema_version":1,"won":{},"found":{},"plays":0,"pearls":23,"pearls_ever":23,"music":false,"mic":false,"quality":"speedy","crafts":{},"stickers":{},"custom_fish":[[0.9,0.3,0.3,1.0,0.8,0.2],[0.2,0.7,0.8,0.9,0.3,0.4,1,0]],"custom_friends":[["cat",0.95,0.7,0.85,0.6,0.4,0.9],["bird",1.0,0.85,0.3,0.3,0.8,0.9,0,1],["cat",0.95,0.7,0.85,0.6,0.4,0.9,1,0,0.97,0.96,0.93]]}

func _new_main(profile: String) -> bool:
	var scene := load("res://scenes/main.tscn") as PackedScene
	m = scene.instantiate() as ReefMain
	m._save_state = SaveState.new(m,profile)
	get_root().add_child(m)
	await _wait_frames(3)
	m._apply_quality("speedy")
	m.day_one_active = false
	if m.start_menu_active:
		m._start_menu_ref()._dismiss_menu()
	if m.intro_active:
		m._skip_intro()
	if not await _wait_presentation():
		errors.append("startup presentation did not settle "+active_profile)
		return false
	return true

func _retire_main() -> void:
	m.set_process(false)
	m.queue_free()
	await _wait_frames(10)
	m = null

func _assert_seed_preserved() -> void:
	for key: String in ["custom_fish","custom_friends"]:
		var expected: Array = active_seed.get(key,[])
		var actual: Array = m.custom_fish if key=="custom_fish" else m.custom_friends
		if actual.size()<expected.size():
			errors.append("legacy array lost "+active_profile+key)
			continue
		for i: int in range(expected.size()):
			if not _gene_rows_equal([actual[i]],[expected[i]]):
				errors.append("legacy row changed "+active_profile+key+str(i))

func _gene_rows_equal(a: Array, b: Array) -> bool:
	if a.size()!=b.size():
		return false
	for i: int in range(a.size()):
		var left: Array=a[i]
		var right: Array=b[i]
		if left.size()!=right.size():
			return false
		var flags: Array=[7,8] if not left.is_empty() and typeof(left[0])==TYPE_STRING else [6,7]
		for j: int in range(left.size()):
			if typeof(left[j]) in [TYPE_FLOAT,TYPE_INT] and typeof(right[j]) in [TYPE_FLOAT,TYPE_INT]:
				if j in flags:
					if float(left[j])!=float(right[j]):
						return false
				elif absf(float(left[j])-float(right[j]))>0.000001:
					return false
			elif left[j]!=right[j]:
				return false
	return true

func _run_case(target: Vector2i, base_out: String, profile_id: String, chosen_kind: String, legacy: bool) -> void:
	active_profile = profile_id
	active_seed = _seed(legacy)
	out_dir=base_out.path_join("%dx%d" % [target.x,target.y]).path_join(profile_id)
	DirAccess.make_dir_recursive_absolute(out_dir)
	states.clear()
	if not await _set_aspect(target):
		errors.append("aspect readiness failed "+profile_id)
		return
	var profile := out_dir.path_join("profile/reef_save.json")
	DirAccess.make_dir_recursive_absolute(profile.get_base_dir())
	if legacy:
		var seed_file := FileAccess.open(profile,FileAccess.WRITE)
		seed_file.store_string(JSON.stringify(active_seed,"\t",true)+"\n")
		seed_file.close()
	if not await _new_main(profile):
		await _retire_main()
		return
	_assert_seed_preserved()
	var expected_pearls: int = 23 if legacy else 0
	if m.pearl_count!=expected_pearls:
		errors.append("profile pearls mismatch "+profile_id)
	m._open_craft_studio()
	await _wait_frames(4)
	await _capture("opened_default_fish",{"entry":"direct guarded production API, synthetic profile"})
	if not legacy:
		for kind: String in ["cat","bird"]:
			await _tap(_find("CraftKind_"+kind))
			if m.craft_kind!="fish" or m.pearl_count!=0:
				errors.append("unearned locked selection changed "+kind)
			await _capture("locked_"+kind+"_feedback",{"method":"raw pointer press/release","synthetic_earned_pearls":0})
	elif chosen_kind!="fish":
		var price: int = 5 if chosen_kind=="cat" else 8
		await _tap(_find("CraftKind_"+chosen_kind))
		expected_pearls-=price
		if m.craft_kind!=chosen_kind or m.pearl_count!=expected_pearls or not bool(m.craft_unlocks.get(chosen_kind,false)):
			errors.append("actual purchase transition failed "+profile_id)
		await _capture("purchased_"+chosen_kind+"_ready",{"method":"raw pointer press/release","price":price,"private_seed_pearls":23})
		await _tap(_find("CraftKind_"+chosen_kind))
		if m.pearl_count!=expected_pearls:
			errors.append("repeat unlocked choice charged again "+profile_id)
		await _capture("unlocked_repeat_"+chosen_kind)
	else:
		await _capture("saved_fish_default_ready")
	for part: String in ["body","accent","third"]:
		await _tap(_find("CraftPart_"+part))
		if m.craft_part!=part:
			errors.append("part pointer transition failed "+profile_id+part)
		await _capture(part+"_palette_ready")
		for index: int in [0,2,6]:
			await _tap(_swatch(index))
			if not _current_color().is_equal_approx(CraftStudio.PALETTE[index]):
				errors.append("palette pointer transition failed "+profile_id+part+str(index))
			await _capture(part+"_color"+str(index)+"_selected",{"method":"raw pointer press/release","part":part,"palette_index":index})
		if part!="third":
			await _tap(_rainbow())
			if not (m.craft_body_rb if part=="body" else m.craft_fins_rb):
				errors.append("rainbow transition failed "+profile_id+part)
			for beat: int in range(7):
				if beat>0:
					await _delay(0.4)
				await _capture(part+"_rainbow_beat"+str(beat),{"method":"timed same-process viewport","nominal_cycle_beat":beat,"continuous_motion_review":false})
			await _tap(_swatch(0))
			await _capture(part+"_solid_restored")
	# The third selector is recorded exactly; source code doesnot consume c3 inpreview.
	await _capture("before_finish_current_state")
	var before_fish: int = m.custom_fish.size()
	var before_friends: int = m.custom_friends.size()
	var expected_new: Array
	if chosen_kind=="fish":
		expected_new=[m.craft_body.r,m.craft_body.g,m.craft_body.b,m.craft_fins.r,m.craft_fins.g,m.craft_fins.b,1 if m.craft_body_rb else 0,1 if m.craft_fins_rb else 0]
	else:
		expected_new=[chosen_kind,m.craft_body.r,m.craft_body.g,m.craft_body.b,m.craft_fins.r,m.craft_fins.g,m.craft_fins.b,1 if m.craft_body_rb else 0,1 if m.craft_fins_rb else 0,m.craft_c3.r,m.craft_c3.g,m.craft_c3.b]
	await _tap(_find("CraftFinishButton"))
	await _capture("finish_release",{"method":"raw pointer press/release","expected_new_gene":expected_new})
	if chosen_kind=="fish":
		if m.custom_fish.size()!=before_fish+1 or m.custom_fish[-1]!=expected_new:
			errors.append("fish append mismatch "+profile_id)
	else:
		if m.custom_friends.size()!=before_friends+1 or m.custom_friends[-1]!=expected_new:
			errors.append("friend append mismatch "+profile_id)
	await _tap(_find("CraftFinishButton"))
	if m.custom_fish.size()!=(before_fish+1 if chosen_kind=="fish" else before_fish) or m.custom_friends.size()!=(before_friends+1 if chosen_kind!="fish" else before_friends):
		errors.append("duplicate finish append "+profile_id)
	await _capture("duplicate_finish_guarded")
	for step: int in range(5):
		await _delay(0.4)
		await _capture("finish_motion_step"+str(step),{"method":"timed actual productiontween","continuous_motion_review":false})
	await _delay(0.8)
	if m.craft_layer!=null or bool(m.get_meta("craft_closing",false)):
		errors.append("natural craft completionteardown failed "+profile_id)
	_assert_seed_preserved()
	var saved_fish: Array=m.custom_fish.duplicate(true)
	var saved_friends: Array=m.custom_friends.duplicate(true)
	var saved_unlocks: Dictionary=m.craft_unlocks.duplicate(true)
	await _capture("completion_teardown",{"art_context_credit":false,"reason":"Craftclosed;actual lifetime/save evidence only"})
	await _retire_main()
	if not await _new_main(profile):
		await _retire_main()
		return
	if not _gene_rows_equal(m.custom_fish,saved_fish) or not _gene_rows_equal(m.custom_friends,saved_friends) or m.craft_unlocks!=saved_unlocks or m.pearl_count!=expected_pearls:
		errors.append("actualprivate save/reload mismatch "+profile_id)
	_assert_seed_preserved()
	m._open_craft_studio()
	await _wait_frames(4)
	await _capture("reloaded_reentry_default_fish",{"entry":"freshMain/SaveState fromactualprivate emitted save;synthetic seeds notchild data"})
	if chosen_kind!="fish":
		await _tap(_find("CraftKind_"+chosen_kind))
		if m.craft_kind!=chosen_kind or m.pearl_count!=expected_pearls:
			errors.append("saved unlock reentry failed "+profile_id)
		await _capture("reloaded_unlocked_"+chosen_kind)
	m._craft_ref()._close_craft()
	await _wait_frames(4)
	if m.craft_layer!=null:
		errors.append("cancel teardown failed "+profile_id)
	await _capture("reentry_cancel_teardown",{"art_context_credit":false,"reason":"Lifetime/source evidence only"})
	await _retire_main()
	var manifest: Dictionary={"schema":"reef.craft_compositor_context/1","source_revision":OS.get_environment("ROOTPIC_REV"),"engine":Engine.get_version_info(),"renderer":RenderingServer.get_current_rendering_method(),"quality":"speedy","aspect":[target.x,target.y],"profile_id":profile_id,"synthetic_seed":active_seed,"actual_child_data":false,"chosen_kind":chosen_kind,"states":states,"saved_fish":saved_fish,"saved_friends":saved_friends,"saved_unlocks":saved_unlocks,"private_save_path":profile,"normal_save_before":normal_before,"normal_save_after":_normal_hashes(),"errors":errors,"numeric_save_tolerance":0.000001,"scope_limits":"Direct guarded productionGUI entry,raw syntheticpointeractual handlers,8isolated profile/aspect instances. Synthetic seed andemittedprivate save roundtrip;notactualchild data/naturalcastle route/phone touch/device/owner/QA11 orcomplete continuous motion. Frame/layer/file counts notartpiece counts."}
	var file:=FileAccess.open(out_dir.path_join("capture_manifest.json"),FileAccess.WRITE)
	file.store_string(JSON.stringify(manifest,"\t",true)+"\n")
	file.close()
	case_receipts.append({"profile":profile_id,"aspect":[target.x,target.y],"capture_count":states.size(),"manifest":out_dir.path_join("capture_manifest.json"),"errors":errors.duplicate()})

func _run() -> void:
	var engine:=Engine.get_version_info()
	if int(engine.get("major",0))!=4 or int(engine.get("minor",0))!=7 or int(engine.get("patch",0))!=2 or String(engine.get("status",""))!="stable" or String(engine.get("build",""))!="official" or RenderingServer.get_current_rendering_method()!="mobile" or DisplayServer.get_name()=="headless":
		print("CRAFT39|FAIL|engine/renderer/display")
		quit(1)
		return
	normal_before=_normal_hashes()
	var base_out:=OS.get_environment("ROOTPIC_OUT")
	if base_out.is_empty() or DirAccess.dir_exists_absolute(base_out):
		print("CRAFT39|FAIL|new output required")
		quit(1)
		return
	DirAccess.make_dir_recursive_absolute(base_out)
	var requested: String=OS.get_environment("R39_PROFILE")
	var requested_width: int=int(OS.get_environment("R39_WIDTH"))
	if requested in ["fresh_locked","saved_fish","saved_cat","saved_bird"] and requested_width in [1280,1600]:
		var kind: String="cat" if requested=="saved_cat" else ("bird" if requested=="saved_bird" else "fish")
		await _run_case(Vector2i(requested_width,720),base_out,requested,kind,requested!="fresh_locked")
	else:
		errors.append("exact declared native case/profile required")
	if normal_before!=_normal_hashes():
		errors.append("normal save changed")
	var report:Dictionary={"schema":"reef.craft_context_batch/1","engine":engine,"renderer":RenderingServer.get_current_rendering_method(),"quality":"speedy","cases":case_receipts,"normal_before":normal_before,"normal_after":_normal_hashes(),"errors":errors,"source_revision":OS.get_environment("ROOTPIC_REV"),"runtime_or_asset_edits":false,"accepted_removed":0,"mission_complete":false}
	var file:=FileAccess.open(base_out.path_join("BATCH.json"),FileAccess.WRITE)
	file.store_string(JSON.stringify(report,"\t",true)+"\n")
	file.close()
	print("CRAFT39|RESULT|"+("PASS" if errors.is_empty() else "FAIL")+"|"+str(errors))
	quit(0 if errors.is_empty() else 1)
