class_name OperaTeacherImpPlan
extends RefCounted
## Clock-free round data; picture readiness is a separate owner acceptance gate.
const Lessons := preload("res://scripts/teacher_lesson_plan.gd")
const PICTURE_ROOT := "res://assets/opera/worlds/teacher_silly/"
const SILLY := {
	"smell": ["farts", "garbage", "diaper", "cheese", "rose"],
	"loud": ["burp", "drum", "lion", "firetruck", "mouse"],
	"big": ["whale", "elephant", "dinosaur", "castle", "ant"],
	"sticky": ["honey", "gum", "booger", "slime", "feather"],
	"cold": ["icecream", "snowman", "icecube", "penguin", "sun"],
	"slow": ["snail", "turtle", "sloth", "slug", "rocket"],
	"squishy": ["jelly", "marshmallow", "mud", "whoopee", "rock"],
	"yucky": ["mudpie", "worm", "sock", "soap", "cupcake"],
}
const VOICE_TEXT := {
	"imp_op_lesson_fixed": "Oops! You fixed it! My brain is full of bubbles!",
	"imp_op_lesson_tricked": "Hee hee! Tricked you!",
	"imp_op_teacher_arrive": "Hello, class! I'm the new teacher! I know everything! I think.",
	"imp_op_teacher_challenge": "My turn to be the teacher! Can you catch my silly mistakes?",
	"imp_op_teacher_claim_add": "Two plus one makes... a banana! No wait. This many!",
	"imp_op_teacher_claim_count": "One, two, three... eleventy-twelve! It's this many!",
	"imp_op_teacher_claim_match": "Look! These two are twins! Same, same, same!",
	"imp_op_teacher_claim_pattern": "Easy peasy, lemon squeezy! This one comes next!",
	"imp_op_teacher_defeat": "You're the real teacher! I'll go sit in the silly corner.",
	"imp_op_teacher_silly_big_ask": "Which is the biggest? A whale, an elephant, a dinosaur, or a castle?",
	"imp_op_teacher_silly_big_claim": "I know! This itty bitty ant! Look at its muscles!",
	"imp_op_teacher_silly_big_right": "Whoa! That's so big! I feel teeny!",
	"imp_op_teacher_silly_big_tricked": "Hee hee! Tricked you! Ants are tiny!",
	"imp_op_teacher_silly_cold_ask": "Which is the coldest? Ice cream, a snowman, an ice cube, or a penguin?",
	"imp_op_teacher_silly_cold_claim": "Brrr! The sun! It's freezing!",
	"imp_op_teacher_silly_cold_right": "Brrr! My toes are frozen!",
	"imp_op_teacher_silly_cold_tricked": "Hee hee! Tricked you! The sun is hot!",
	"imp_op_teacher_silly_loud_ask": "Which is the loudest? A burp, a big drum, a roaring lion, or a fire truck?",
	"imp_op_teacher_silly_loud_claim": "Easy! This teeny tiny mouse! Squeak!",
	"imp_op_teacher_silly_loud_right": "Ow, my ears! That's so loud!",
	"imp_op_teacher_silly_loud_tricked": "Hee hee! Tricked you! Mice are super quiet!",
	"imp_op_teacher_silly_slow_ask": "Which is the slowest? A snail, a turtle, a sloth, or a slug?",
	"imp_op_teacher_silly_slow_claim": "Zoom! This rocket is soooo slow!",
	"imp_op_teacher_silly_slow_right": "Sooo... slooow... Yaaawn!",
	"imp_op_teacher_silly_slow_tricked": "Hee hee! Tricked you! Rockets go zoom!",
	"imp_op_teacher_silly_smell_ask": "Which smells the worst? Farts, garbage, old diapers, or rotten cheese?",
	"imp_op_teacher_silly_smell_claim": "I know! This pretty rose! Pee-yew!",
	"imp_op_teacher_silly_smell_right": "Pee-yew! That's so stinky! I'm gonna faint!",
	"imp_op_teacher_silly_smell_tricked": "Hee hee! Tricked you! Roses smell nice!",
	"imp_op_teacher_silly_squishy_ask": "Which is the squishiest? Jelly, a marshmallow, mud, or a whoopee cushion?",
	"imp_op_teacher_silly_squishy_claim": "This hard rock! Squishy squishy!",
	"imp_op_teacher_silly_squishy_right": "Squish! So squishy!",
	"imp_op_teacher_silly_squishy_tricked": "Hee hee! Tricked you! Rocks are hard!",
	"imp_op_teacher_silly_sticky_ask": "Which is the stickiest? Honey, bubble gum, a booger, or slime?",
	"imp_op_teacher_silly_sticky_claim": "This fluffy feather! It sticks to everything!",
	"imp_op_teacher_silly_sticky_right": "Eww! My fingers are stuck together!",
	"imp_op_teacher_silly_sticky_tricked": "Hee hee! Tricked you! Feathers float away!",
	"imp_op_teacher_silly_yucky_ask": "Which is the yuckiest to eat? A mud pie, a wiggly worm, a stinky sock, or soap?",
	"imp_op_teacher_silly_yucky_claim": "Yuck! This cupcake!",
	"imp_op_teacher_silly_yucky_right": "Bleh! Yucky yucky yuck!",
	"imp_op_teacher_silly_yucky_tricked": "Hee hee! Tricked you! Cupcakes are yummy!",
	"roshan_op_teacher_contest": "The imp is teaching it wrong! Tap the right answer to fix it!",
}


static func total_rounds(saved: Dictionary) -> int:
	var progress := Lessons.normalise_progress(saved)
	var total := 0
	for kind: String in Lessons.KINDS:
		total += int((progress["kinds"] as Dictionary)[kind]["rounds"])
	return total


static func make_round(index: int, saved: Dictionary, rematches: int = 0,
		first_silly: bool = false) -> Dictionary:
	if index % 2 == 0:
		var ids: Array = SILLY.keys()
		var id := "smell" if first_silly or index == 0 else String(ids[posmod(total_rounds(saved) + index / 2, ids.size())])
		return silly_round(id, total_rounds(saved) + index / 2)
	var kind: String = Lessons.KINDS[posmod(index / 2, Lessons.KINDS.size())]
	var eased := Lessons.normalise_progress(saved)
	var state: Dictionary = (eased["kinds"] as Dictionary)[kind]
	state["tier"] = maxi(0, int(state["tier"]) - maxi(0, rematches))
	var lesson := Lessons.make_lesson(kind, eased)
	lesson["imp_answer"] = Lessons.imp_answer(lesson, rematches > 0)
	lesson["claim_vo"] = "op_teacher_claim_" + kind
	return lesson


static func silly_round(id: String, sequence: int) -> Dictionary:
	if not SILLY.has(id):
		return {}
	var pictures: Array = SILLY[id]
	var arranged: Array[String] = []
	var choices: Array[int] = []
	var correct: Array[int] = []
	var imp := -1
	for index in range(5):
		var source := posmod(index + sequence, 5)
		arranged.append(String(pictures[source]))
		choices.append(source)
		if source == 4:
			imp = index
		else:
			correct.append(index)
	return {"kind": "silly", "silly_id": id, "sequence": sequence,
		"tier": 0, "choices": choices, "pictures": arranged,
		"correct_indices": correct, "answer": correct[0], "imp_answer": imp,
		"ask_vo": "op_teacher_silly_%s_ask" % id,
		"claim_vo": "op_teacher_silly_%s_claim" % id,
		"right_vo": "op_teacher_silly_%s_right" % id,
		"tricked_vo": "op_teacher_silly_%s_tricked" % id}


static func picture_path(lesson: Dictionary, index: int) -> String:
	var pictures: Array = lesson.get("pictures", []) as Array
	if index < 0 or index >= pictures.size():
		return ""
	return PICTURE_ROOT + "%s_%s.png" % [String(lesson.get("silly_id", "")), String(pictures[index])]


static func pictures_available() -> bool:
	for id: String in SILLY:
		for picture: String in SILLY[id]:
			if not ResourceLoader.exists(PICTURE_ROOT + "%s_%s.png" % [id, picture]):
				return false
	return true
