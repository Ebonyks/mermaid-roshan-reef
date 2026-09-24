class_name RainbowFriendFollower
extends RefCounted
## The rainbow dust bunny follows Roshan through the castle rooms once the Day
## One transformation has freed him from Grand Puff's dusty shell (owner canon
## 2026-09-23, DL-CIN-16). Like Baby Eagle's companion card, it is one reusable
## true-2D card in the castle's Canvas item layer, placed beside Roshan's feet on
## the side opposite Baby Eagle. Satellite mold: all state stays on ReefMain
## except the single card reference, and nothing allocates per frame.

const TEXTURE_PATH: String = "res://assets/sprites/dust_bunnies/rainbow_friend.png"
const CARD_SIZE: Vector2 = Vector2(132.0, 132.0)
## Stage-space offset from Roshan's foot (Baby Eagle's card sits at +108, -100).
const STAGE_OFFSET: Vector2 = Vector2(-104.0, -78.0)

var m: ReefMain
var card: TextureRect = null


func _init(main: ReefMain) -> void:
	m = main


func befriended() -> bool:
	return m._day_one_ref().giant_dust_bunny_boss_defeated


func tick() -> void:
	var rooms: CastleRooms25D = m._castle_rooms_ref()
	var layer: Node2D = m.castle_room_item_visual_layer
	var player: Sprite2D = m.castle_room_player_sprite
	if not befriended() or not rooms.is_open() \
			or layer == null or not is_instance_valid(layer) \
			or player == null or not is_instance_valid(player):
		if card != null and is_instance_valid(card):
			card.visible = false
		return
	if card == null or not is_instance_valid(card) or card.get_parent() != layer:
		var texture: Texture2D = load(TEXTURE_PATH) as Texture2D
		if texture == null:
			return
		card = TextureRect.new()
		card.name = "CastleRainbowFriendCard"
		card.size = CARD_SIZE
		card.texture = texture
		card.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		card.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		card.mouse_filter = Control.MOUSE_FILTER_IGNORE
		card.set_meta("source_asset_path", TEXTURE_PATH)
		card.set_meta("castle_canvas_only", true)
		layer.add_child(card)
	var foot: Vector2 = player.get_meta("current_stage_foot",
		player.get_meta("stage_foot", Vector2.ZERO)) as Vector2
	var depth_z: float = float(player.get_meta("depth_z", CastleRooms25D.PLAYER_FRONT_Z))
	var wide_hall: bool = rooms._is_wide_hall()
	var canvas_scale: float = CastleRooms25D.HALL_STAGE_SCALE if wide_hall \
		else CastleRooms25D.ART_TO_STAGE
	var center: Vector2 = rooms._hall_art_to_world(foot + STAGE_OFFSET, depth_z) \
		if wide_hall else rooms._stage_to_world(foot + STAGE_OFFSET, depth_z)
	card.scale = Vector2.ONE * canvas_scale
	card.position = center - CARD_SIZE * canvas_scale * 0.5
	card.z_index = player.z_index + 1
	card.visible = true
