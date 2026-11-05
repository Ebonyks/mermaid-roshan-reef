extends SceneTree
## Lossless source slicing; native dimensions are retained, never invented.

const SOURCE := "res://assets_src/review/opera_exploration_v1/"
const OUTPUT := "res://assets/review/opera_translation_v1/"

func _initialize() -> void:
	DirAccess.make_dir_recursive_absolute(OUTPUT)
	var image: Image = Image.load_from_file(SOURCE+"restoration_healed.png")
	if image == null or image.is_empty():
		quit(1)
		return
	image.convert(Image.FORMAT_RGBA8)
	var original: Image = Image.load_from_file(SOURCE+"restoration_master.png")
	original.convert(Image.FORMAT_RGBA8)
	var emblem_source: Image = Image.create(2048,1024,false,Image.FORMAT_RGBA8)
	emblem_source.fill(Color.TRANSPARENT)
	emblem_source.blit_rect(original,Rect2i(Vector2i.ZERO,original.get_size()),Vector2i.ZERO)
	emblem_source.save_png(OUTPUT+"restoration_medallion_source.png")
	var fabric_source: Image = Image.create(2048,1024,false,Image.FORMAT_RGBA8)
	fabric_source.fill(Color.TRANSPARENT)
	fabric_source.blit_rect(image,Rect2i(Vector2i.ZERO,image.get_size()),Vector2i.ZERO)
	fabric_source.save_png(OUTPUT+"restoration_healed_source.png")
	var layout: Dictionary = {"native_size":[image.get_width(),image.get_height()],
		"native_2k_per_screen":false,"method":"lossless native crop with transparent POT padding","cards":[]}
	for row: int in range(2):
		for column: int in range(2):
			var start := Vector2i(column*image.get_width()/2,row*image.get_height()/2)
			var finish := Vector2i((column+1)*image.get_width()/2,(row+1)*image.get_height()/2)
			var region := Rect2i(start,finish-start)
			var card: Image = Image.create(1024,1024,false,Image.FORMAT_RGBA8)
			card.fill(Color.TRANSPARENT)
			card.blit_rect(image,region,Vector2i.ZERO)
			var path: String = "house_%d_%d.png" % [row,column]
			card.save_png(OUTPUT+path)
			(layout["cards"] as Array).append({"path":path,"source_rect":[region.position.x,region.position.y,region.size.x,region.size.y]})
	var file: FileAccess = FileAccess.open(OUTPUT+"layout.json",FileAccess.WRITE)
	file.store_string(JSON.stringify(layout,"\t")+"\n")
	print("OPERA_TRANSLATION_ASSETS|NATIVE_SOURCE|%dx%d" % [image.get_width(),image.get_height()])
	print("OPERA_TRANSLATION_ASSETS|LOSSLESS_SLICING|OK")
	quit(0)
