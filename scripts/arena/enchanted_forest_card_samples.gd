extends RefCounted
## Shared mipmapped samples for the demo world cards.

static var _prop_samples: Dictionary[Texture2D, Texture2D] = {}


static func prop_sample(source: Texture2D) -> Texture2D:
	if _prop_samples.has(source):
		return _prop_samples[source]
	var pixels: Image = source.get_image()
	if pixels == null or (pixels.is_compressed() and pixels.decompress() != OK):
		return source
	var longest: int = maxi(pixels.get_width(), pixels.get_height())
	if longest > 512:
		var size: Vector2i = Vector2i(Vector2(pixels.get_size()) * (512.0 / longest))
		pixels.clear_mipmaps()
		pixels.resize(size.x, size.y, Image.INTERPOLATE_LANCZOS)
	pixels.generate_mipmaps()
	var sampled: ImageTexture = ImageTexture.create_from_image(pixels)
	_prop_samples[source] = sampled
	return sampled
