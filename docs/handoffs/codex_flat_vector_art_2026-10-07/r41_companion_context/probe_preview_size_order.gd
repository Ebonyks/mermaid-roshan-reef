extends SceneTree
## R41 source diagnosis only: real TextureRect intrinsicminimum versus requestedbox.
var failures:=0
var cases: Array[Dictionary]=[]
func _init() -> void:
	call_deferred("_run")
func _run() -> void:
	var engine:=Engine.get_version_info()
	if engine.major!=4 or engine.minor!=7 or engine.patch!=2 or engine.status!="stable" or engine.build!="official":
		quit(1)
		return
	for path: String in ["res://assets/characters/companions/baby_eagle.png","res://assets/sprites/stuffie_studio/lamma.png"]:
		var texture: Texture2D=load(path)
		for requested: Vector2 in [Vector2(150,200),Vector2(150,560.0/3.0-50.0),Vector2(302,302),Vector2(318,328)]:
			var old:=TextureRect.new()
			old.texture=texture
			old.position=Vector2.ZERO
			old.size=requested
			old.expand_mode=TextureRect.EXPAND_IGNORE_SIZE
			old.stretch_mode=TextureRect.STRETCH_KEEP_ASPECT_CENTERED
			get_root().add_child(old)
			await process_frame
			var old_size: Vector2=old.size
			var corrected:=TextureRect.new()
			corrected.expand_mode=TextureRect.EXPAND_IGNORE_SIZE
			corrected.stretch_mode=TextureRect.STRETCH_KEEP_ASPECT_CENTERED
			corrected.texture=texture
			corrected.position=Vector2.ZERO
			corrected.size=requested
			get_root().add_child(corrected)
			await process_frame
			var corrected_size: Vector2=corrected.size
			var current_reproduces: bool=not old_size.is_equal_approx(requested) and old_size.y>requested.y
			var fixed_order_fits: bool=corrected_size.is_equal_approx(requested)
			if not current_reproduces or not fixed_order_fits:
				failures+=1
			cases.append({"texture":path,"texture_size":str(texture.get_size()),"requested_size":str(requested),"current_order_size":str(old_size),"corrected_order_size":str(corrected_size),"current_order_reproduces_intrinsic_clamp":current_reproduces,"corrected_order_respects_requested_box":fixed_order_fits,"original_pixels_modified":false})
			old.queue_free()
			corrected.queue_free()
			await process_frame
	var report: Dictionary={"schema":"reef.companion_preview_size_order/1","source_revision":OS.get_environment("R41_REV"),"engine":engine,"cases":cases,"failures":failures,"production_repair":false,"native_context_repair":false,"accepted_removed":0,"scope":"Real headless Control minimumsize ablation withoriginaltextures/currentassignmentorder versusboundedcorrectedorder. Diagnoses eight currentfailures andeightpositive fits atstudio/swap roster,largepreview,andcare sourceboxes;doesnot repairgameoraccept art/visual/device/child/owner/QA11."}
	var output:=OS.get_environment("R41_SIZE_PROOF")
	var file:=FileAccess.open(output,FileAccess.WRITE)
	file.store_string(JSON.stringify(report,"\t",true)+"\n")
	file.close()
	print("PREVIEWSIZE41|RESULT|"+("PASS_DIAGNOSIS" if failures==0 else "FAIL")+"|"+str(cases.size()))
	quit(0 if failures==0 else 1)
