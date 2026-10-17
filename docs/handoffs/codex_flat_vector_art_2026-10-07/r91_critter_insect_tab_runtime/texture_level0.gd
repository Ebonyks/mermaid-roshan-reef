extends SceneTree

func _initialize() -> void:
	DisplayServer.window_set_position(Vector2i(-2400, 0))
	var picture: Texture2D = load("res://assets/mg/butterfly.png")
	await process_frame
	var image: Image = picture.get_image()
	if image == null:
		push_error("Existing texture readback missing")
		quit(1)
		return
	var has_mips: bool = image.has_mipmaps()
	image.clear_mipmaps()
	image.convert(Image.FORMAT_RGBA8)
	var context := HashingContext.new()
	context.start(HashingContext.HASH_SHA256)
	context.update(image.get_data())
	var record: Dictionary = {"source":"res://assets/mg/butterfly.png","source_sha256":FileAccess.get_sha256("res://assets/mg/butterfly.png"),"size":[image.get_width(),image.get_height()],"has_mipmaps":has_mips,"level0_RGBA8_sha256":context.finish().hex_encode(),"viewport_default_filter":root.canvas_item_default_texture_filter,"rendering_method":RenderingServer.get_current_rendering_method(),"scope":"Isolated texture decode/readback, no Main scene or visual acceptance."}
	var file := FileAccess.open(OS.get_environment("R91_TEX_REPORT"),FileAccess.WRITE)
	file.store_string(JSON.stringify(record,"\t",true)+"\n")
	file.close()
	print("R91_LEVEL0|"+JSON.stringify(record))
	quit(0)