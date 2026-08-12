class_name OperaCareerWorld2D
extends CanvasLayer
## The runtime 2D/2.5D Pearl Opera career world.
##
## Each career supplies artwork and a phase list, while this class owns the
## common living-world language: full-bleed environment painting, Mermaid
## Roshan and a dressed rival on opposite sides, one-finger job gestures,
## parallel score/progress, audience energy and a graded curtain call.

const GestureSurface := preload("res://scripts/opera_gesture_surface.gd")
const BoxingSurface := preload("res://scripts/opera_boxing_surface.gd")
const BalletSurface := preload("res://scripts/opera_ballet_surface.gd")
const WorldBackdrop := preload("res://scripts/opera_world_backdrop_2d.gd")
const NurseryCatch := preload("res://scripts/opera_nursery_catch.gd")
const StagePaths := preload("res://scripts/opera_stage_paths.gd")
const ImpClips := preload("res://scripts/opera_imp_clips.gd")
const RoshanAnimator := preload("res://scripts/opera_roshan_actor.gd")
const WorldHotspot := preload("res://scripts/opera_world_hotspot_2d.gd")
const HotspotCatalog := preload("res://scripts/opera_hotspot_catalog.gd")

## Detective search geometry. The authored magnifier is a 512px square with
## its glass centred near (181, 181); anchoring the art by that point keeps the
## actual zoom, clue capture and visible glass on the same spot under a finger.
const LENS_RADIUS := 130.0
const LENS_CLUE_CAPTURE_RADIUS := 112.0
const LENS_GRAPHIC_SIZE := Vector2(420.0, 420.0)
const LENS_ART_GLASS_CENTER := Vector2(0.354, 0.354)
const LENS_MAGNIFICATION := 1.75
const LENS_HINT_DELAY := 12.0
const LENS_TRAIL_DURATION := 2.4

## The mystery begins in voices the child already knows: the off-screen imp
## gives away the theft, then Roshan turns that event into a concrete search.
## These are existing protected family recordings; runtime code only queues
## them and never edits or substitutes their source assets.
const DETECTIVE_INTRO_LINES: Array[Dictionary] = [
	{"who": "Mischief Imp", "text": "The sparkly crown! Now everyone will look at ME!", "vo": "op_detective_steal", "hold": 2.8},
	{"who": "Roshan", "text": "Search the whole stage! Sweep your magnifying glass to find every hidden sparkle!", "vo": "op_detective_search", "hold": 3.8},
]

## The detective painting is deliberately dense. These are safe inspection
## targets, not extra objectives: every landmark gives a satisfying response,
## while only lens_clues advance the case. Positions are normalized to the
## frozen 1280x720 stage so they survive phone/tablet letterboxing unchanged.
const DETECTIVE_ROOM_OBJECTS: Array[Dictionary] = [
	{"id": "moon", "at": Vector2(0.35, 0.10), "radius": 68.0, "colour": Color("#fff0a8")},
	{"id": "curtain_door", "at": Vector2(0.055, 0.31), "radius": 76.0, "colour": Color("#ffb7dc")},
	{"id": "left_lantern", "at": Vector2(0.085, 0.43), "radius": 52.0, "colour": Color("#ffd36e")},
	{"id": "lockbox_shelf", "at": Vector2(0.16, 0.34), "radius": 72.0, "colour": Color("#75e6dc")},
	{"id": "round_case_shelf", "at": Vector2(0.29, 0.35), "radius": 72.0, "colour": Color("#ff9fb8")},
	{"id": "evidence_shelf", "at": Vector2(0.40, 0.34), "radius": 72.0, "colour": Color("#8cd8ff")},
	{"id": "hatbox_table", "at": Vector2(0.50, 0.35), "radius": 72.0, "colour": Color("#d6a8ff")},
	{"id": "magnifier_tower", "at": Vector2(0.49, 0.12), "radius": 78.0, "colour": Color("#ffe27a")},
	{"id": "arched_bridge", "at": Vector2(0.64, 0.30), "radius": 74.0, "colour": Color("#80e7ff")},
	{"id": "mirror_gallery", "at": Vector2(0.58, 0.43), "radius": 78.0, "colour": Color("#b8f4ff")},
	{"id": "crown_chest", "at": Vector2(0.88, 0.34), "radius": 84.0, "colour": Color("#ffe27a")},
	{"id": "glowing_footprints", "at": Vector2(0.42, 0.49), "radius": 76.0, "colour": Color("#a8fff3")},
	{"id": "round_hatbox", "at": Vector2(0.25, 0.63), "radius": 64.0, "colour": Color("#ffb0c7")},
	{"id": "coral_case", "at": Vector2(0.39, 0.63), "radius": 64.0, "colour": Color("#ffab8f")},
	{"id": "pearl_case", "at": Vector2(0.51, 0.63), "radius": 64.0, "colour": Color("#e0b4ff")},
	{"id": "fish_display", "at": Vector2(0.63, 0.63), "radius": 68.0, "colour": Color("#70e5ff")},
	{"id": "feather_chest", "at": Vector2(0.76, 0.63), "radius": 70.0, "colour": Color("#ffd482")},
	{"id": "curved_stairs", "at": Vector2(0.84, 0.61), "radius": 82.0, "colour": Color("#a9e8ff")},
]

const SLUGS := {
	"chef": "chef",
	"detective": "detective",
	"ballerina": "ballerina",
	"candymaker": "candymaker",
	"doctor": "doctor",
	"farmer": "farmer",
	"boxer": "boxer",
	"magician": "magician",
	"painter": "painter",
	"astronaut": "astronaut",
	"racer": "racer",
	"popstar": "popstar",
	"nursery": "nursery",
}

## Every career follows the same five-beat arc (OPERA_2D_REBUILD_2026-08-01.md):
## short imp scuffle -> learn the job -> do the job -> the imp captain steals
## the goal prop -> two-phase finale on the proscenium stage against the
## dressed rival. "bop" phases carry a "combat" dict; FINALE_START is always
## the first on-stage phase.
const LEGACY_PHASES := {
	"chef": [
		{"name": "IMPS!", "icon": "!", "mode": "bop", "goal": 5.0, "combat": {"count": 5}, "vo": "op_chef_imps", "voice": "Mischief imps grabbed the spoons! Tap each imp to shoo them off!"},
		{"name": "POUR", "icon": "●", "mode": "pourt", "goal": 5.0, "vo": "op_chef_pour", "voice": "Grab the pitcher and TIP it — pour the sparkling batter into the bowl!"},
		{"name": "STIR", "icon": "↻", "mode": "circle", "goal": 4.0, "vo": "op_chef_stir", "voice": "Draw big circles to stir!"},
		{"name": "BAKE", "icon": "★", "mode": "oven", "goal": 6.0, "vo": "op_chef_bake", "voice": "Watch the cake turn golden — then grab the big mitt and take it out!"},
		{"name": "CAKE CHASE", "icon": "!", "mode": "bop", "goal": 10.0, "combat": {"count": 8, "captain": true}, "vo": "op_chef_cake_chase", "voice": "The imp captain snatched the cake! Bop the crew to the stage door!"},
		{"name": "PIPE", "icon": "〰", "mode": "swipe", "goal": 7.0, "vo": "op_chef_pipe", "voice": "On stage! Swipe to pipe the frosting!"},
		{"name": "TOP", "icon": "●", "mode": "tap", "goal": 8.0, "vo": "op_chef_top", "voice": "Tap the bright toppings and win the cake back!"},
	],
	"detective": [
		{"name": "IMPS!", "icon": "!", "mode": "bop", "goal": 5.0, "combat": {"count": 5}, "vo": "op_detective_imps", "voice": "The mermaid crown is GONE from its cushion — and imps scattered the clue boxes! Tap each imp!"},
		{"name": "ASK KAREEM", "icon": "?", "mode": "talk", "goal": 1.0, "speaker": "Kareem", "vo": "op_detective_ask_kareem", "voice": "Somebody saw something! Walk over and ask Kareem!", "lines": [
			{"who": "Kareem", "text": "A sparkle zoomed behind the big CLOCK!", "vo": "op_detective_hint_clock", "hold": 2.8},
			{"who": "Roshan", "text": "To the clock — detective time!", "vo": "op_detective_to_clock", "hold": 2.2}]},
		{"name": "CLOCK", "icon": "?", "mode": "lens", "goal": 2.0, "vo": "op_detective_lens", "voice": "Sweep the magnifying glass by the clock — glitter footprints!"},
		{"name": "TRAIL TRICK", "icon": "!", "mode": "bop", "goal": 3.0, "combat": {"count": 3}, "vo": "op_detective_trail_trick", "voice": "Sneaky! That imp is re-laying the footprints the WRONG way! Bop the tricksters!"},
		{"name": "ASK ROSALINA", "icon": "?", "mode": "talk", "goal": 1.0, "speaker": "Rosalina", "vo": "op_detective_ask_rosalina", "voice": "He dropped a torn crown ribbon! Show it to Rosalina!", "lines": [
			{"who": "Rosalina", "text": "That ribbon was floating by the FOUNTAIN!", "vo": "op_detective_hint_fountain", "hold": 2.8},
			{"who": "Roshan", "text": "The fountain! Come on!", "vo": "op_detective_to_fountain", "hold": 2.0}]},
		{"name": "FOUNTAIN", "icon": "?", "mode": "lens", "goal": 2.0, "vo": "op_detective_search", "voice": "Look into the fountain water — something glitters down there!"},
		{"name": "ASK CHUCK", "icon": "?", "mode": "talk", "goal": 1.0, "speaker": "Chuck", "vo": "op_detective_ask_chuck", "voice": "A crown jewel! One person left to ask — Chuck!", "lines": [
			{"who": "Chuck", "text": "I heard giggling under the STAGE STAIRS!", "vo": "op_detective_hint_stairs", "hold": 2.8},
			{"who": "Roshan", "text": "Shhh... tip-toe, tip-toe...", "vo": "op_detective_tiptoe", "hold": 2.2}]},
		{"name": "STAIRS", "icon": "?", "mode": "lens", "goal": 1.0, "vo": "op_detective_lens", "voice": "Shine the lens under the stage stairs..."},
		{"name": "CROWN CHASE", "icon": "!", "mode": "bop", "goal": 10.0, "combat": {"count": 8, "captain": true}, "vo": "op_detective_tiara_chase", "voice": "The imp captain is wearing the crown like a HAT! He bolts — bop the crew!"},
		{"name": "TEAM CORNER", "icon": "!", "mode": "bop", "goal": 6.0, "combat": {"count": 4, "captain": true}, "vo": "op_detective_team_corner", "voice": "The rival detective wants the crown found too! Corner the captain together!"},
	],
	"ballerina": [
		{"name": "IMPS!", "icon": "!", "mode": "bop", "goal": 5.0, "combat": {"count": 5}, "vo": "op_ballerina_imps", "voice": "Imps are bouncing on the recital tiles! Tap them gently off!"},
		{"name": "STEPS", "icon": "◆", "mode": "choice", "goal": 7.0, "vo": "op_ballerina_steps", "voice": "Tap the glowing dance step!"},
		{"name": "RIBBON", "icon": "〰", "mode": "swipe", "goal": 6.5, "vo": "op_ballerina_ribbon", "voice": "Trace the ribbon across the floor!"},
		{"name": "RIBBON CHASE", "icon": "!", "mode": "bop", "goal": 10.0, "combat": {"count": 8, "captain": true}, "vo": "op_ballerina_ribbon_chase", "voice": "The imp captain tangled the ribbons! Twirl-bop the crew!"},
		{"name": "TWIRL", "icon": "↻", "mode": "circle", "goal": 3.6, "vo": "op_ballerina_twirl", "voice": "Draw circles for the grand twirl!"},
	],
	"candymaker": [
		{"name": "IMPS!", "icon": "!", "mode": "bop", "goal": 5.0, "combat": {"count": 5}, "vo": "op_candymaker_imps", "voice": "Imps are juggling the gumdrops! Tap each imp!"},
		{"name": "SYRUP", "icon": "●", "mode": "pourt", "goal": 4.5, "vo": "op_candymaker_syrup", "voice": "Grab the syrup bottle and TIP it over the candy mold!"},
		{"name": "SORT", "icon": "◆", "mode": "choice", "goal": 7.0, "vo": "op_candymaker_sort", "voice": "Tap the glowing candy chute!"},
		{"name": "WRAP", "icon": "↻", "mode": "circle", "goal": 3.6, "vo": "op_candymaker_wrap", "voice": "Twist the wrappers in circles!"},
		{"name": "CANDY CHASE", "icon": "!", "mode": "bop", "goal": 10.0, "combat": {"count": 8, "captain": true}, "vo": "op_candymaker_candy_chase", "voice": "The imp captain rolled away the candy cart! Bop the crew!"},
		{"name": "SHARE", "icon": "●", "mode": "tap", "goal": 6.0, "vo": "op_candymaker_share", "voice": "The candy cart rolls by — toss a candy to every waving friend!"},
	],
	"doctor": [
		{"name": "IMPS!", "icon": "!", "mode": "bop", "goal": 5.0, "combat": {"count": 5}, "vo": "op_doctor_imps", "voice": "Imps are hiding the bandages! Tap each imp!"},
		{"name": "WASH", "icon": "●", "mode": "hold", "goal": 4.5, "vo": "op_doctor_wash", "voice": "Hold to wash Doctor Roshan's hands!"},
		{"name": "FIND", "icon": "?", "mode": "choice", "goal": 6.0, "vo": "op_doctor_find", "voice": "Find the plushy with the glowing ouch!"},
		{"name": "X-RAY", "icon": "?", "mode": "lens", "goal": 3.0, "vo": "op_doctor_x_ray", "voice": "Slide the X-ray scanner over the plushy to find the cracked bone!"},
		{"name": "PLUSHY CHASE", "icon": "!", "mode": "bop", "goal": 10.0, "combat": {"count": 8, "captain": true}, "vo": "op_doctor_plushy_chase", "voice": "The imp captain borrowed the plushy patient! Bop the crew to the stage!"},
		{"name": "CAST", "icon": "↻", "mode": "circle", "goal": 3.6, "vo": "op_doctor_cast", "voice": "Draw circles to wrap the soft cast!"},
		{"name": "BANDAGE", "icon": "〰", "mode": "swipe", "goal": 6.5, "vo": "op_doctor_bandage", "voice": "Swipe the stretchy bandage around!"},
	],
	"farmer": [
		{"name": "IMPS!", "icon": "!", "mode": "bop", "goal": 5.0, "combat": {"count": 5}, "vo": "op_farmer_imps", "voice": "Imps are splashing in the mud! Tap each imp!"},
		{"name": "PLANT", "icon": "◆", "mode": "choice", "goal": 6.0, "vo": "op_farmer_plant", "voice": "Tap the glowing garden row and plant the seed!"},
		{"name": "FEED", "icon": "★", "mode": "timing", "goal": 6.0, "vo": "op_farmer_feed", "voice": "Tap when the veggie reaches a piggy!"},
		{"name": "MUD HOP", "icon": "●", "mode": "hold", "goal": 4.0, "vo": "op_farmer_mud_hop", "voice": "Hold to wind up... and make a big mud hop!"},
		{"name": "PIGGY CHASE", "icon": "!", "mode": "bop", "goal": 10.0, "combat": {"count": 8, "captain": true}, "vo": "op_farmer_piggy_chase", "voice": "The imp captain opened the piggy gate! Bop the crew!"},
		{"name": "HERD", "icon": "↔", "mode": "swipe", "goal": 7.0, "vo": "op_farmer_herd", "voice": "Sweep back and forth to guide the herd on stage!"},
		{"name": "PICNIC", "icon": "●", "mode": "tap", "goal": 7.0, "vo": "op_farmer_picnic", "voice": "Tap a snack for every happy piggy!"},
	],
	"boxer": [
		{"name": "SPAR", "icon": "!", "mode": "bop", "goal": 5.0, "combat": {"count": 5}, "vo": "op_boxer_spar", "voice": "Friendly sparring! Bop each padded imp!"},
		{"name": "JAB", "icon": "!", "mode": "bop", "goal": 4.0, "combat": {"count": 4}, "vo": "op_boxer_jab", "voice": "Jab practice! Bop every training pad the partners hold up!"},
		{"name": "DUCK", "icon": "↓", "mode": "swipe", "goal": 4.0, "dir": "down", "vo": "op_boxer_duck", "voice": "Swipe down to duck the friendly counter!"},
		{"name": "BELL CHASE", "icon": "!", "mode": "bop", "goal": 10.0, "combat": {"count": 8, "captain": true}, "vo": "op_boxer_bell_chase", "voice": "The imp captain grabbed the championship belt and rang the big bell! Win it back in the title match!"},
		{"name": "ROUND", "icon": "◆", "mode": "choice", "goal": 8.0, "vo": "op_boxer_round", "voice": "Punch the glowing pad — left, middle, right!"},
		{"name": "BELT", "icon": "★", "mode": "tap", "goal": 1.0, "vo": "op_boxer_belt", "voice": "Tap the championship belt for the winner!"},
	],
	"magician": [
		{"name": "IMPS!", "icon": "!", "mode": "bop", "goal": 5.0, "combat": {"count": 5}, "vo": "op_magician_imps", "voice": "Imps popped out of the magic hats! Tap each imp!"},
		{"name": "VANISH", "icon": "●", "mode": "hold", "goal": 4.2, "vo": "op_magician_vanish", "voice": "Hold the wand to make Lamba vanish!"},
		{"name": "TRACK", "icon": "?", "mode": "choice", "goal": 6.0, "vo": "op_magician_track", "voice": "Follow the glowing hat through the shuffle!"},
		{"name": "ROPE", "icon": "〰", "mode": "swipe", "goal": 6.5, "vo": "op_magician_rope", "voice": "Swipe the magic rope into one long ribbon!"},
		{"name": "LAMBA CHASE", "icon": "!", "mode": "bop", "goal": 10.0, "combat": {"count": 8, "captain": true}, "vo": "op_magician_bunny_chase", "voice": "The imp captain hid Lamba! Bop the crew to the stage!"},
		{"name": "CABINET", "icon": "〰", "mode": "swipe", "dir": "down", "goal": 6.0, "vo": "op_magician_cabinet", "voice": "Grab the doors and swipe down — pull the magic cabinet open!"},
		{"name": "PORTAL", "icon": "↻", "mode": "circle", "goal": 4.0, "vo": "op_magician_portal", "voice": "Draw circles to open the giant star portal!"},
	],
	"painter": [
		{"name": "IMPS!", "icon": "!", "mode": "bop", "goal": 5.0, "combat": {"count": 5}, "vo": "op_painter_imps", "voice": "Imps splashed the paint pots! Tap each imp!"},
		{"name": "SKETCH", "icon": "〰", "mode": "swipe", "goal": 6.5, "vo": "op_painter_sketch", "voice": "Trace the sunrise sketch!"},
		{"name": "FILL", "icon": "●", "mode": "hold", "goal": 4.5, "vo": "op_painter_fill", "voice": "Hold to fill the glowing shape!"},
		{"name": "SPLAT", "icon": "●", "mode": "tap", "goal": 7.0, "vo": "op_painter_splat", "voice": "Tap five happy splatters!"},
		{"name": "SUNRISE CHASE", "icon": "!", "mode": "bop", "goal": 10.0, "combat": {"count": 8, "captain": true}, "vo": "op_painter_sunrise_chase", "voice": "The imp captain took the sunrise painting! Bop the crew!"},
		{"name": "STROKES", "icon": "↻", "mode": "circle", "goal": 3.6, "vo": "op_painter_strokes", "voice": "Paint grand circles for the crowd!"},
		{"name": "REVEAL", "icon": "★", "mode": "choice", "goal": 1.0, "vo": "op_painter_reveal", "voice": "Tap the glowing frame to hang the sunrise!"},
	],
	"astronaut": [
		{"name": "IMPS!", "icon": "!", "mode": "bop", "goal": 5.0, "combat": {"count": 5}, "vo": "op_astronaut_imps", "voice": "Imps are floating around the rocket bay! Tap each imp!"},
		{"name": "PIPES", "icon": "◆", "mode": "pipe", "goal": 3.0, "vo": "op_astronaut_pipes", "voice": "Connect the bubble pipes from the fuel tank all the way to the rocket!"},
		{"name": "PATCH", "icon": "●", "mode": "tap", "goal": 6.0, "vo": "op_astronaut_patch", "voice": "Tap the sparkle leaks to patch them!"},
		{"name": "VALVE", "icon": "↻", "mode": "circle", "goal": 3.6, "vo": "op_astronaut_valve", "voice": "Draw circles to turn the launch valve!"},
		{"name": "ROCKET CHASE", "icon": "!", "mode": "bop", "goal": 10.0, "combat": {"count": 8, "captain": true}, "vo": "op_astronaut_rocket_chase", "voice": "The imp captain scooped up the little rocket and pressed the silly button! Bop the crew!"},
		{"name": "LAUNCH", "icon": "●", "mode": "hold", "goal": 5.0, "vo": "op_astronaut_launch", "voice": "Hold through the countdown... and launch!"},
	],
	"racer": [
		{"name": "IMPS!", "icon": "!", "mode": "bop", "goal": 5.0, "combat": {"count": 5}, "vo": "op_racer_imps", "voice": "Imps rolled tires onto the track! Tap each imp!"},
		{"name": "TUNE UP", "icon": "↻", "mode": "circle", "goal": 3.6, "vo": "op_racer_tune_up", "voice": "Turn the wrench in big circles — tighten every wheel before the race!"},
		{"name": "TO THE LINE", "icon": "↔", "mode": "swipe", "goal": 6.0, "vo": "op_racer_to_the_line", "voice": "Push the kart all the way out to the starting line!"},
		{"name": "TROPHY CHASE", "icon": "!", "mode": "bop", "goal": 10.0, "combat": {"count": 8, "captain": true}, "vo": "op_racer_trophy_chase", "voice": "The imp captain grabbed the shell trophy and jumped into his kart! Clear the track!"},
		{"name": "RACE!", "icon": "★", "mode": "circle", "widget": "", "goal": 1.0, "vo": "op_racer_lap_two", "voice": "Loop the loop! Draw big racing circles!"},
	],
	"nursery": [
		{"name": "IMPS!", "icon": "!", "mode": "bop", "goal": 5.0, "combat": {"count": 5}, "vo": "op_nursery_imps", "voice": "Mischief imps are tickling the babies awake! Tap each imp!"},
		{"name": "WASH HANDS", "icon": "●", "mode": "hold", "goal": 3.6, "vo": "op_nursery_wash", "voice": "Nursery Nurse Roshan! Hold the bubbly basin to wash your hands first!"},
		{"name": "CATCH BABIES", "icon": "↓", "mode": "catch", "goal": 5.0, "speaker": "Faron", "vo": "op_nursery_catch", "voice": "Slide the soft cradle under five falling babies! Pillows keep every miss safe."},
		{"name": "FEED", "icon": "♡", "mode": "hold", "goal": 4.2, "speaker": "Faron", "vo": "op_nursery_feed", "voice": "Hold the warm bottle while Roshan and Faron feed every baby!"},
		{"name": "BABY CHASE", "icon": "!", "mode": "bop", "goal": 10.0, "combat": {"count": 8, "captain": true}, "vo": "op_nursery_baby_chase", "voice": "The imp captain is playing peek-a-boo with the babies! Bop the crew to the stage!"},
		{"name": "BURP", "icon": "○", "mode": "tap", "widget": "", "pace": 0.55, "goal": 4.0, "vo": "op_nursery_burp", "voice": "Pat the baby's back — gentle and slow. Pat... pat... pat!"},
		{"name": "BEDTIME", "icon": "☾", "mode": "swipe", "goal": 6.0, "speaker": "Faron", "vo": "op_nursery_bedtime", "voice": "Swipe the blankets down and tuck every sleepy baby into bed!"},
	],
	"popstar": [
		{"name": "IMPS!", "icon": "!", "mode": "bop", "goal": 5.0, "combat": {"count": 5}, "vo": "op_popstar_imps", "voice": "Imps are drumming on the speakers! Tap each imp!"},
		{"name": "SOUND CHECK", "icon": "●", "mode": "hold", "goal": 4.5, "vo": "op_popstar_sound_check", "voice": "Hold the microphone for sound check!"},
		{"name": "DANCE", "icon": "◆", "mode": "choice", "goal": 8.0, "vo": "op_popstar_dance", "voice": "Tap the glowing dance arrow!"},
		{"name": "MIC CHASE", "icon": "!", "mode": "bop", "goal": 10.0, "combat": {"count": 8, "captain": true}, "vo": "op_popstar_mic_chase", "voice": "The imp captain unplugged the microphone! Bop the mischief band!"},
		{"name": "RHYTHM", "icon": "♪", "mode": "echo", "goal": 3.0, "vo": "op_popstar_rhythm", "voice": "Listen to the stars sing — then tap their song back, as slow as you like!"},
		{"name": "ENCORE", "icon": "↻", "mode": "circle", "goal": 4.2, "vo": "op_popstar_encore", "voice": "Draw a big encore spin for the crowd!"},
	],
}

const LEGACY_FINALE_START := {
	"chef": 5,
	"detective": 9,
	"ballerina": 4,
	"candymaker": 5,
	"doctor": 5,
	"farmer": 5,
	"boxer": 4,
	"magician": 5,
	"painter": 5,
	"astronaut": 5,
	"racer": 4,
	"popstar": 4,
	"nursery": 5,
}

## Shipping career structure (2026-08-09 quality overhaul).
##
## Similarity now comes from the theatre framing, helpers, imps, wordless
## teaching and curtain call. The playable verb belongs to the job. Boxer is
## deliberately the only career that resolves its complication with combat.
## The old five-beat tables remain above for audit comparison only.
const BALLET_PHASE_HOLD_SECONDS := 1.75
const PHASES := {
	"chef": [
		{"name": "MIX", "mode": "pourt", "goal": 5.0, "vo": "op_chef_pour", "voice": "Tip the sparkling batter into the bowl!"},
		{"name": "STIR", "mode": "circle", "goal": 2.0, "vo": "op_chef_stir", "voice": "Draw big circles to stir the batter!"},
		{"name": "BAKE", "mode": "oven", "goal": 6.0, "vo": "op_chef_bake", "voice": "Watch for golden, then take the cake out with the mitt!"},
		{"name": "FROST", "mode": "swipe", "goal": 6.0, "vo": "op_chef_pipe", "voice": "Trace the frosting ribbon across the cake!"},
		{"name": "TOP", "mode": "tap", "goal": 7.0, "vo": "op_chef_top", "voice": "Place the bright toppings on the finished cake!"},
	],
	"detective": [
		{"name": "SEARCH", "mode": "lens", "goal": 3.0, "vo": "op_detective_lens", "voice": "Sweep the magnifying glass across the painted clues!"},
		{"name": "CASE BOARD", "mode": "clue_board", "widget": "", "goal": 3.0, "vo": "op_detective_match", "voice": "Match each glowing clue to the case board!"},
		{"name": "CROWN", "mode": "crown_chest", "widget": "", "goal": 1.0, "vo": "op_detective_name", "voice": "Tap when the spotlight shines on the answer!"},
	],
	"ballerina": [
		{"name": "PEARL MIRROR", "mode": "ballet_pose", "widget": "", "goal": 3.0, "vo": "op_ballerina_watch", "voice": "Watch Roshan hold each ballet pose, then tap the matching pearl mirror!"},
		{"name": "RIBBON TRAIL", "mode": "ballet_ribbon", "widget": "", "goal": 1.0, "vo": "op_ballerina_ribbon", "voice": "Guide the pearl along the glowing ribbon current!"},
		{"name": "GRAND TWIRL", "mode": "ballet_twirl", "widget": "", "goal": 1.0, "vo": "op_ballerina_twirl", "voice": "Turn the pearl around the shell for the grand twirl!"},
	],
	"candymaker": [
		{"name": "SYRUP", "mode": "pourt", "goal": 5.0, "vo": "op_candymaker_syrup", "voice": "Tip the syrup into the candy mold!"},
		{"name": "SORT", "mode": "candy_sort", "goal": 6.0, "vo": "op_candymaker_sort", "voice": "Drag each candy into its matching shape box!"},
		{"name": "WRAP", "mode": "circle", "goal": 1.8, "vo": "op_candymaker_wrap", "voice": "Twist the finished wrappers in circles!"},
		{"name": "SHARE", "mode": "tap", "goal": 6.0, "vo": "op_candymaker_share", "voice": "Give one finished candy to every waving friend!"},
	],
	"doctor": [
		{"name": "WASH", "mode": "hold", "goal": 3.6, "vo": "op_doctor_wash", "voice": "Hold the bubbly basin to wash Doctor Roshan's hands!"},
		{"name": "FIND", "mode": "choice", "goal": 4.0, "vo": "op_doctor_find", "voice": "Choose the plushy with the glowing ouch!"},
		{"name": "X-RAY", "mode": "xray_scan", "goal": 2.0, "vo": "op_doctor_x_ray", "voice": "Slide the scanner over the plushy to find the sore spots!"},
		{"name": "CAST", "mode": "circle", "goal": 1.8, "vo": "op_doctor_cast", "voice": "Draw gentle circles to wrap the soft cast!"},
		{"name": "BANDAGE", "mode": "swipe", "goal": 5.0, "vo": "op_doctor_bandage", "voice": "Swipe the stretchy bandage around the plushy!"},
	],
	"farmer": [
		{"name": "PLANT", "mode": "garden_plant", "widget": "", "goal": 5.0, "vo": "op_farmer_plant", "voice": "Plant each seed in the glowing garden bed!"},
		{"name": "TOSS", "mode": "farm_lob", "goal": 4.0, "vo": "op_farmer_feed", "voice": "Pull back a vegetable and toss it gently to a piggy!"},
		{"name": "HERD", "mode": "swipe", "goal": 6.0, "vo": "op_farmer_herd", "voice": "Sweep the happy piggies through the barn gate!"},
		{"name": "PICNIC", "mode": "tap", "goal": 3.0, "vo": "op_farmer_picnic", "voice": "Set one picnic snack beside every piggy!"},
	],
	"boxer": [
		{"name": "GLOVE GUIDE", "mode": "boxing_guide", "widget": "", "goal": 2.0, "vo": "op_boxer_work", "voice": "Put a finger on a glove and push it toward the glowing mitt!"},
		{"name": "JAB PRACTICE", "mode": "boxing_jab", "widget": "", "goal": 4.0, "vo": "op_boxer_jab", "voice": "Jab practice! Punch each glowing training pad!"},
		{"name": "SOFT GUARD", "mode": "boxing_guard", "widget": "", "goal": 3.0, "vo": "op_boxer_duck", "voice": "Bring a glove into the glowing guard bubble!"},
		{"name": "TITLE IMP", "mode": "boxing_imp", "widget": "", "goal": 6.0, "vo": "op_boxer_bell_chase", "voice": "The boxer imp rang the bell! Punch when the bright star opens!"},
		{"name": "BELT", "mode": "boxing_belt", "widget": "", "goal": 1.0, "vo": "op_boxer_belt", "voice": "Punch the glowing championship belt for the curtain call!"},
	],
	"magician": [
		{"name": "VANISH", "mode": "hold", "widget": "", "visual_context": "magic_vanish", "goal": 3.8, "vo": "op_magician_vanish", "voice": "Hold the wand to hide Lamba under a hat!"},
		{"name": "TRACK", "mode": "choice", "goal": 5.0, "vo": "op_magician_track", "voice": "Follow the glowing hat through the shuffle!"},
		{"name": "ROPE", "mode": "swipe", "goal": 5.0, "vo": "op_magician_rope", "voice": "Swipe the knotted rope into one long ribbon!"},
		{"name": "CABINET", "mode": "magic_cabinet", "widget": "", "goal": 1.0, "vo": "op_magician_cabinet", "voice": "Swipe down to open the magic cabinet!"},
		{"name": "PORTAL", "mode": "circle", "goal": 2.0, "vo": "op_magician_portal", "voice": "Draw circles to open the star portal!"},
	],
	"painter": [
		{"name": "PAINT", "mode": "paint_reveal", "goal": 1.0, "vo": "op_painter_sketch", "voice": "Paint across the cloudy canvas to reveal the sunrise!"},
		{"name": "STAMPS", "mode": "tap", "goal": 5.0, "vo": "op_painter_splat", "voice": "Add any five bright finishing stamps!"},
		{"name": "GALLERY", "mode": "choice", "goal": 1.0, "vo": "op_painter_reveal", "voice": "Choose the glowing frame and hang your sunrise!"},
	],
	"astronaut": [
		{"name": "PIPES", "mode": "pipe", "goal": 3.0, "vo": "op_astronaut_pipes", "voice": "Connect the fuel tank to the rocket through three pipe boards!"},
		{"name": "PATCH", "mode": "tap", "goal": 5.0, "vo": "op_astronaut_patch", "voice": "Patch every sparkling leak on the rocket!"},
		{"name": "VALVE", "mode": "circle", "goal": 1.8, "vo": "op_astronaut_valve", "voice": "Draw circles to turn the launch valve!"},
		{"name": "LAUNCH", "mode": "hold", "goal": 4.5, "vo": "op_astronaut_launch", "voice": "Hold through the countdown and launch!"},
	],
	"racer": [
		{"name": "TUNE", "mode": "circle", "goal": 1.8, "vo": "op_racer_tune_up", "voice": "Turn the wrench to finish the pit stop!"},
		{"name": "TO THE LINE", "mode": "swipe", "goal": 5.0, "vo": "op_racer_to_the_line", "voice": "Push the kart to the pearl starting arch!"},
		{"name": "RACE", "mode": "circle", "widget": "", "goal": 0.9, "vo": "op_racer_lap_two", "voice": "Loop the loop! Draw big racing circles!"},
	],
	"nursery": [
		{"name": "WASH HANDS", "mode": "hold", "widget": "", "visual_context": "nursery_wash", "goal": 3.4, "vo": "op_nursery_wash", "voice": "Hold the bubbly basin to wash your hands first!"},
		{"name": "CATCH BABIES", "mode": "catch", "goal": 5.0, "speaker": "Faron", "vo": "op_nursery_catch", "voice": "Slide the soft cradle under five babies. Pillows keep every miss safe!"},
		{"name": "FEED", "mode": "hold", "widget": "", "visual_context": "nursery_feed", "goal": 4.0, "speaker": "Faron", "vo": "op_nursery_feed", "voice": "Hold the warm bottle while Roshan and Faron feed each baby!"},
		{"name": "BURP", "mode": "tap", "widget": "", "visual_context": "nursery_burp", "pace": 0.55, "goal": 4.0, "vo": "op_nursery_burp", "voice": "Pat the baby's back gently and slowly: pat, pat, pat!"},
		{"name": "BEDTIME", "mode": "swipe", "widget": "", "visual_context": "nursery_bedtime", "dir": "down", "goal": 3.0, "speaker": "Faron", "vo": "op_nursery_bedtime", "voice": "Swipe each blanket down and tuck every baby into bed!"},
	],
	"popstar": [
		{"name": "SOUND CHECK", "mode": "hold", "goal": 3.8, "vo": "op_popstar_sound_check", "voice": "Hold the microphone while the rainbow note grows!"},
		{"name": "DANCE", "mode": "choice", "goal": 6.0, "vo": "op_popstar_dance", "voice": "Tap the glowing dance arrow!"},
		{"name": "RHYTHM", "mode": "echo", "goal": 3.0, "vo": "op_popstar_rhythm", "voice": "Listen to the three stars, then sing their song back!"},
		{"name": "ENCORE", "mode": "circle", "goal": 1.8, "vo": "op_popstar_encore", "voice": "Draw one big encore spin for the crowd!"},
	],
}

const FINALE_START := {
	"chef": 3,
	"detective": 1,
	"ballerina": 2,
	"candymaker": 3,
	"doctor": 3,
	"farmer": 2,
	"boxer": 3,
	"magician": 3,
	"painter": 2,
	"astronaut": 3,
	"racer": 2,
	"nursery": 4,
	"popstar": 2,
}

## Stable landmark IDs keep every task attached to the painted object that
## explains it. Even specialist full-stage beats begin from a physical room
## object; their stage-wide play only starts after Roshan reaches it.
const PHASE_STATIONS := {
	"chef": {"MIX": "mixing_bowl", "STIR": "mixing_bowl", "BAKE": "hearth_oven", "FROST": "grand_cake_stage", "TOP": "grand_cake_stage"},
	"detective": {"SEARCH": "magnifier_tower", "CASE BOARD": "evidence_shelves", "CROWN": "treasure_dais"},
	"ballerina": {"PEARL MIRROR": "trifold_mirror", "RIBBON TRAIL": "wave_tuffets", "GRAND TWIRL": "rose_finale_stage"},
	"candymaker": {"SYRUP": "gumball_vat", "SORT": "taffy_press", "WRAP": "candy_bag_cottage", "SHARE": "candy_cart"},
	"doctor": {"WASH": "stethoscope_clinic", "FIND": "starfish_triage", "X-RAY": "exam_booth", "CAST": "exam_booth", "BANDAGE": "recovery_bed"},
	"farmer": {"PLANT": "seed_beds", "TOSS": "hay_bales", "HERD": "barn_doors", "PICNIC": "blossom_arch"},
	"boxer": {"GLOVE GUIDE": "glove_wall_shelf", "JAB PRACTICE": "purple_sparring_mat", "SOFT GUARD": "teal_heavy_bag", "TITLE IMP": "shell_pavilion_stage", "BELT": "shell_pavilion_stage"},
	"magician": {"VANISH": "violet_shell_stage", "TRACK": "pearl_tide_pool", "ROPE": "teal_shell_stage", "CABINET": "rose_shell_stage", "PORTAL": "rose_shell_stage"},
	"painter": {"PAINT": "gazebo_easel", "STAMPS": "rainbow_brush", "GALLERY": "arch_easel"},
	"astronaut": {"PIPES": "coolant_tank_pad", "PATCH": "pipe_arch_planter", "VALVE": "periscope_elbow", "LAUNCH": "rocket_launch_dais"},
	"racer": {"TUNE": "pearl_dome_pavilion", "TO THE LINE": "pearl_start_arch", "RACE": "ribbon_finish_arch"},
	"nursery": {"WASH HANDS": "wash_basin", "CATCH BABIES": "cuddle_cushions", "FEED": "bottle_nook", "BURP": "cuddle_cushions", "BEDTIME": "moon_bed"},
	"popstar": {"SOUND CHECK": "mic_gazebo", "DANCE": "record_dais", "RHYTHM": "shell_stage", "ENCORE": "shell_stage"},
}

## The specialist rebuild renamed its phases but intentionally reuses the
## already-approved isolated invitation art. Keeping that translation here
## lets the new ballet/boxing surfaces enter through the room's physical
## objects without duplicating or silently dropping the diegetic hotspot.
const HOTSPOT_PHASE_ALIASES := {
	"ballerina": {
		"PEARL MIRROR": "POSE",
		"RIBBON TRAIL": "RIBBON",
		"GRAND TWIRL": "TWIRL",
	},
	"boxer": {
		"GLOVE GUIDE": "COMBO",
		"JAB PRACTICE": "COMBO",
		"SOFT GUARD": "COMBO",
		"TITLE IMP": "TITLE ROUND",
	},
}

## Career goal prop shown at the workbench until the imp captain steals it in
## beat four; celebrate() brings it back for the curtain call. Textures are
## codex flat-package cards matted by tools/prepare_opera_2d_props.py; a
## missing file simply hides the prop.
const GOAL_PROPS := {
	"chef": "goal_chef",
	"detective": "goal_detective",
	"ballerina": "goal_ballerina",
	"candymaker": "goal_candymaker",
	"doctor": "goal_doctor",
	"farmer": "goal_farmer",
	"boxer": "goal_boxer",
	"magician": "goal_magician",
	"painter": "goal_painter",
	"astronaut": "goal_astronaut",
	"racer": "goal_racer",
	"popstar": "goal_popstar",
	"nursery": "goal_nursery",
}
var m: ReefMain
var config: Dictionary = {}
var competition: OperaCompetition
var win_callback: Callable
var career_id := ""
var phases: Array = []
var phase_index := 0
var phase_progress := 0.0
var active := true
var guided := false
var reveal_t := 0.0
var elapsed := 0.0
var timing_phase := 0.0
var choice_target := 1

var phase_gap := 0.0
var phase_complete_t := 0.0
var phase_advance_pending := false
## One owner per animated stage element. Rest snapshots never come from an
## interrupted tween, so rapid input always converges on the same transform.
var actor_rests: Dictionary = {}
var actor_tweens: Dictionary = {}
var bop_time := 0.0
var steal_index := -1
var captain_pending := false
var idle_t := 0.0
## Testable count of spoken ballet re-prompts. Initial phase VO is separate.
var ballet_instruction_repeats := 0
## WANDER (owner 2026-08-04, the curiosity layer): between tasks the world
## is HERS — tap-to-walk along the painted route while the armed station
## breathes and invites. The task opens when she arrives (150px + 0.35s
## dwell), when she taps the lit marker, or on any card gesture (which is
## also the probes' pump path, so every existing drive still works).
var task_open := true
## The racer finale stays inside this Canvas world. The same large circle
## grammar used by TUNE UP becomes a steering turn on the supplied painted
## race stage; every honest turn wins the stolen trophy back, with no timer,
## placement requirement, or fail branch.
## Gentle-pace gate (nursery BURP): taps faster than the phase "pace" pay
## nothing — the baby just bounces. Restraint is the skill being taught.
var pace_cool := 0.0
## "talk" beats (detective crown hunt): the witness speaks via say_sequence
## while she may keep strolling; the beat completes when the lines finish
## (or instantly on any probe/child gesture — the standard pump path).
var talk_t := 0.0
var armed_station := -1
var wander_dwell := 0.0
var wander_dest := Vector2.ZERO
var wander_walking := false
## the walk's own clean feet position: the bob/lean never feed back into it,
## so twenty interrupted walks still end on exactly the painted route
var wander_feet := Vector2.ZERO
var wander_stride := 0.0
var wander_lean := 0.0
var wander_layer: Control
var wander_route := PackedVector2Array()
var wander_route_index := 0
var interaction_station := -1
var interaction_requested := false
var hotspot_opening := false
var score_cool := 0.0
var bounce_cool := 0.0
var bop_puff_texture: Texture2D = null
var nursery_catch: OperaNurseryCatch = null
## Stage geography: the painted world's walkable route and task stations.
var stage_points := PackedVector2Array()
var station_list: Array[Dictionary] = []
var station_nodes: Array[Control] = []
var station_for_phase: Dictionary = {}
## Roaming stage combat (replaces the old panel scuffle).
var combat_layer: Control = null
var combat_fx: Control = null
var combat_imps: Array[Dictionary] = []
var combat_marks: Array[Dictionary] = []
var imp_idle_texture: Texture2D = null
var imp_bopped_texture: Texture2D = null
var imp_bow_texture: Texture2D = null
var captain_idle_texture: Texture2D = null
var captain_bopped_texture: Texture2D = null
var captain_bow_texture: Texture2D = null
var fx_telegraph_ring_texture: Texture2D = null
var fx_telegraph_bang_texture: Texture2D = null
var fx_slash_arc_texture: Texture2D = null
var fx_dust_puff_texture: Texture2D = null
var fx_stolen_sparkle_texture: Texture2D = null
var fx_dizzy_stars_texture: Texture2D = null
## True while the crew wears the career costume: their states are clips over
## that costume, never a swap back to the base purple imp.
var costumed_crew := false
var swipe_stroke := 0
var combat_miss_cool := 0.0
var imp_state_cache: Dictionary = {}
## The shared mischief-imp brain (scripts/imp_ai.gd) drives the crew: who
## closes in, who telegraphs, who hangs back. All state stays here.
var imp_brain: ImpAI = null
var combat_warned := false
## Magnifier lens phases (detective's masked reveal over the whole stage).
var lens_layer: Control = null
var lens_pos := Vector2(640, 400)
var lens_clues := PackedVector2Array()
var lens_found: Array[bool] = []
var lens_dwell := 0.0
var lens_target := -1
var lens_demo := true
var lens_zoom_surface: ColorRect = null
var lens_zoom_material: ShaderMaterial = null
var lens_since_find := 0.0
var lens_hint_target := -1
var lens_room_objects: Array[Dictionary] = []
var lens_object_pulses: Array[Dictionary] = []
var lens_room_reactions := 0
var lens_object_sound_cool := 0.0
var detective_intro_played := false
var lens_find_count := 0
var lens_trail_from := Vector2.ZERO
var lens_trail_to := Vector2.ZERO
var lens_trail_t := 0.0
## Compatibility-only handles for the retired easel/beacon draw helpers below.
## Runtime never loads or connects either asset in the diegetic room flow.
var task_frame_texture: Texture2D = null
var station_marker_texture: Texture2D = null
var magnifier_texture: Texture2D = null

var root: Control
var stage_bleed: ColorRect
var backdrop_node: OperaWorldBackdrop2D
var action_panel: ColorRect
var prop_rect: TextureRect
var player_actor: TextureRect
var player_animator: OperaRoshanActor
var rival_actor: TextureRect
var player_bar: ProgressBar
var rival_bar: ProgressBar
## Curtain-call cheer as data (spoken by VO, asserted by probes) - the owner
## removed every on-screen text header 2026-08-04: these are full-screen art
## games, and the child cannot read.
var last_cheer := ""
var surface: OperaGestureSurface
var phase_fill: ProgressBar
var confetti: Array[ColorRect] = []


func setup(main: ReefMain, act_config: Dictionary, director: OperaCompetition, on_win: Callable) -> void:
	m = main
	config = act_config
	competition = director
	competition.pause()
	win_callback = on_win
	career_id = String(config.get("costume", "chef"))
	phases = (PHASES.get(career_id, []) as Array).duplicate(true)
	steal_index = -1
	for index in range(phases.size()):
		var phase := phases[index] as Dictionary
		if String(phase.get("mode", "")) == "bop" and bool((phase.get("combat", {}) as Dictionary).get("captain", false)):
			steal_index = index
	layer = 38
	_build_world()
	# The room is part of every activity. Setup arms the first physical object;
	# it never bypasses discovery by opening a minigame synchronously.
	_arm_phase()


func _full_rect(control: Control) -> void:
	control.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)


func _sync_root_scale() -> void:
	if root == null or not is_instance_valid(root):
		return
	var vs: Vector2 = get_viewport().get_visible_rect().size
	if vs.x <= 0.0 or vs.y <= 0.0:
		return
	var uniform_scale := minf(vs.x / StagePaths.SCREEN.x, vs.y / StagePaths.SCREEN.y)
	root.scale = Vector2.ONE * uniform_scale
	root.position = (vs - StagePaths.SCREEN * uniform_scale) * 0.5
	if stage_bleed != null and is_instance_valid(stage_bleed):
		stage_bleed.position = Vector2.ZERO
		stage_bleed.size = vs
	_sync_lens_zoom_surface()


func _label(text: String, font_size: int, colour: Color = Color.WHITE) -> Label:
	var label := Label.new()
	label.text = text
	label.add_theme_font_size_override("font_size", font_size)
	label.add_theme_color_override("font_color", colour)
	label.add_theme_color_override("font_shadow_color", Color(0.03, 0.02, 0.12, 0.92))
	label.add_theme_constant_override("shadow_offset_x", 3)
	label.add_theme_constant_override("shadow_offset_y", 3)
	label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	return label


func _build_world() -> void:
	stage_bleed = ColorRect.new()
	stage_bleed.name = "OperaStageBleed"
	stage_bleed.color = Color("#16214d")
	stage_bleed.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(stage_bleed)
	root = Control.new()
	root.name = "OperaCareerWorld2D"
	root.mouse_filter = Control.MOUSE_FILTER_IGNORE
	# DEVICE GEOMETRY (alpha audit 2026-08-05). Every station, clue spot,
	# path point and depth rule in this world was derived in a fixed
	# 1280x720 painting space — but the backdrop used to stretch to the REAL
	# canvas, which under canvas_items/expand is 1280x800 on the M11 and
	# ~1600x720 on a tall phone. Landmarks drifted up to 80px vertically /
	# 320px horizontally off their painted objects on exactly the two alpha
	# devices (CI probes run at 1280x720, so they never saw it). The root is
	# now FROZEN at 1280x720 and scaled to the live canvas: children keep
	# their derived coordinates, the painting stretches exactly with them,
	# and gui_input events are inverse-transformed through the scale by the
	# engine — so the same numbers are correct at every aspect ratio.
	root.size = StagePaths.SCREEN
	add_child(root)
	_sync_root_scale()
	get_viewport().size_changed.connect(_sync_root_scale)
	magnifier_texture = _load_if_exists("res://assets/opera/worlds/ui/magnifier.png")

	backdrop_node = WorldBackdrop.new() as OperaWorldBackdrop2D
	backdrop_node.name = "CareerWorldBackdrop"
	_full_rect(backdrop_node)
	root.add_child(backdrop_node)
	backdrop_node.setup(career_id)

	var shade := ColorRect.new()
	shade.color = Color(0.0, 0.0, 0.0, 0.0)
	shade.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_full_rect(shade)
	root.add_child(shade)

	# Floor input sits below diegetic object buttons. Empty floor moves Roshan;
	# an object button receives the same touch first and creates activity intent.
	wander_layer = Control.new()
	wander_layer.name = "WalkableRoomInput"
	wander_layer.position = Vector2.ZERO
	wander_layer.size = StagePaths.SCREEN
	wander_layer.mouse_filter = Control.MOUSE_FILTER_IGNORE
	wander_layer.visible = false
	wander_layer.gui_input.connect(_wander_input)
	root.add_child(wander_layer)

	stage_points = StagePaths.path_points(career_id)
	station_list = StagePaths.stations(career_id)
	# Specialist ballet and boxing surfaces still begin at authored room objects.
	# The full-canvas lesson starts only after Roshan follows the painted route
	# and opens that object's invitation, just like every other career.
	_assign_stations()
	_build_station_markers()

	# owner 2026-08-04: NO audience, NO text headers - full-screen art games
	# like the rest of Mermaid Roshan. The only chrome that remains is the
	# finale race, drawn as two slim footlight bars on the bottom edge where
	# they sit on the painted apron instead of covering the district.
	player_bar = ProgressBar.new()
	player_bar.position = Vector2(30, 698)
	player_bar.size = Vector2(500, 12)
	player_bar.show_percentage = false
	player_bar.visible = false
	root.add_child(player_bar)
	rival_bar = ProgressBar.new()
	rival_bar.position = Vector2(750, 698)
	rival_bar.size = Vector2(500, 12)
	rival_bar.show_percentage = false
	rival_bar.visible = false
	root.add_child(rival_bar)

	player_actor = _actor("res://assets/opera/worlds/actors/roshan_%s.png" % career_id)
	# scale contract: Roshan is ~1.3x a crew imp, ~1.2x the captain —
	# a small bit taller, never more than 1.5x (owner 2026-08-03)
	# The ballet silhouette gets a little more room, while staying below the
	# established 1.5x costumed-imp scale ceiling (280 / 190 = 1.47).
	player_actor.size = Vector2(280, 280) if career_id == "ballerina" else Vector2(250, 250)
	# Every career begins on its room route. Ballet moves to its recital mark
	# only after Roshan has walked to and opened the glowing rehearsal object.
	_place_on_stage(player_actor, StagePaths.point_along(stage_points, 0.08))
	root.add_child(player_actor)
	player_animator = RoshanAnimator.new() as OperaRoshanActor
	player_animator.name = "RoshanAtlasAnimator"
	player_actor.add_child(player_animator)
	player_animator.setup(player_actor, career_id, player_actor.texture)
	var partner_path := "res://assets/opera/worlds/actors/rival_%s.png" % career_id
	if career_id == "nursery":
		partner_path = "res://assets/opera/worlds/actors/faron_nursery.png"
	rival_actor = _actor(partner_path)
	rival_actor.size = Vector2(190, 190)   # he is an imp, not her equal in height
	_place_on_stage(rival_actor, StagePaths.point_along(stage_points, 0.92))
	root.add_child(rival_actor)
	_set_finale_visible(false)

	prop_rect = TextureRect.new()
	var prop_path := "res://assets/opera/worlds/props/%s.png" % String(GOAL_PROPS.get(career_id, ""))
	if ResourceLoader.exists(prop_path):
		prop_rect.texture = load(prop_path) as Texture2D
	prop_rect.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	prop_rect.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	prop_rect.mouse_filter = Control.MOUSE_FILTER_IGNORE
	prop_rect.position = Vector2.ZERO
	prop_rect.size = Vector2(280, 230)
	prop_rect.visible = false
	root.add_child(prop_rect)
	_anchor_goal_prop()

	action_panel = ColorRect.new()
	# Transparent host for the borderless activity focus; no clipboard/easel.
	action_panel.color = Color(0, 0, 0, 0)
	action_panel.position = Vector2(430, 160)
	action_panel.size = Vector2(420, 430)
	action_panel.mouse_filter = Control.MOUSE_FILTER_IGNORE
	action_panel.draw.connect(_draw_activity_focus)
	root.add_child(action_panel)
	if career_id == "boxer":
		surface = BoxingSurface.new() as OperaGestureSurface
	elif career_id == "ballerina":
		surface = BalletSurface.new() as OperaGestureSurface
	else:
		surface = GestureSurface.new() as OperaGestureSurface
	if career_id == "boxer":
		surface.name = "BoxingGloveSurface"
	elif career_id == "ballerina":
		surface.name = "BalletPartySurface"
	else:
		surface.name = "CareerGestureSurface"
	surface.position = Vector2(24, 78)
	surface.size = Vector2(372, 266)
	surface.gesture.connect(_on_gesture)
	# The scuffle crews wear the career's special imp costume (the accepted
	# costume-sheet slices). Co-op careers keep the dedicated mischief-imp
	# sprites (the partner is not an imp); placeholders are the last fallback.
	if competition != null and competition.is_cooperative():
		if ResourceLoader.exists("res://assets/opera/worlds/actors/imp_mischief.png"):
			surface.bop_texture = load("res://assets/opera/worlds/actors/imp_mischief.png") as Texture2D
		if ResourceLoader.exists("res://assets/opera/worlds/actors/imp_captain.png"):
			surface.bop_captain_texture = load("res://assets/opera/worlds/actors/imp_captain.png") as Texture2D
	elif rival_actor != null and rival_actor.texture != null:
		surface.bop_texture = rival_actor.texture
		surface.bop_captain_texture = rival_actor.texture
	else:
		if ResourceLoader.exists("res://assets/opera/worlds/actors/imp_mischief.png"):
			surface.bop_texture = load("res://assets/opera/worlds/actors/imp_mischief.png") as Texture2D
		if ResourceLoader.exists("res://assets/opera/worlds/actors/imp_captain.png"):
			surface.bop_captain_texture = load("res://assets/opera/worlds/actors/imp_captain.png") as Texture2D
	if ResourceLoader.exists("res://assets/opera/worlds/props/fx_bop_puff.png"):
		bop_puff_texture = load("res://assets/opera/worlds/props/fx_bop_puff.png") as Texture2D
	action_panel.add_child(surface)
	if career_id == "nursery":
		nursery_catch = NurseryCatch.new() as OperaNurseryCatch
		nursery_catch.name = "NurseryCatchSurface"
		nursery_catch.position = Vector2(24, 78)
		nursery_catch.size = Vector2(372, 266)
		nursery_catch.visible = false
		nursery_catch.baby_caught.connect(_on_nursery_baby_caught)
		nursery_catch.baby_missed.connect(_on_nursery_baby_missed)
		action_panel.add_child(nursery_catch)
	phase_fill = ProgressBar.new()
	phase_fill.position = Vector2(24, 362)
	phase_fill.size = Vector2(372, 40)
	phase_fill.show_percentage = false
	phase_fill.mouse_filter = Control.MOUSE_FILTER_IGNORE
	phase_fill.visible = false
	action_panel.add_child(phase_fill)

	combat_layer = Control.new()
	combat_layer.name = "StageCombatLayer"
	_full_rect(combat_layer)
	combat_layer.mouse_filter = Control.MOUSE_FILTER_IGNORE
	combat_layer.gui_input.connect(_combat_input)
	root.add_child(combat_layer)
	# telegraph rings, slash arcs and stolen-sparkle glints draw above the
	# crew but never take input — the imps themselves stay tappable
	combat_fx = Control.new()
	combat_fx.name = "StageCombatFX"
	_full_rect(combat_fx)
	combat_fx.mouse_filter = Control.MOUSE_FILTER_IGNORE
	combat_fx.draw.connect(_draw_combat_fx)
	root.add_child(combat_fx)
	imp_idle_texture = _load_if_exists("res://assets/opera/worlds/actors/imp_mischief.png")
	imp_bopped_texture = _load_if_exists("res://assets/opera/worlds/actors/imp_mischief_bopped.png")
	imp_bow_texture = _load_if_exists("res://assets/opera/worlds/actors/imp_mischief_bow.png")
	captain_idle_texture = _load_if_exists("res://assets/opera/worlds/actors/imp_captain.png")
	captain_bopped_texture = _load_if_exists("res://assets/opera/worlds/actors/imp_captain_bopped.png")
	captain_bow_texture = _load_if_exists("res://assets/opera/worlds/actors/imp_captain_bow.png")
	fx_telegraph_ring_texture = _load_if_exists("res://assets/opera/worlds/props/fx_telegraph_ring.png")
	fx_telegraph_bang_texture = _load_if_exists("res://assets/opera/worlds/props/fx_telegraph_bang.png")
	fx_slash_arc_texture = _load_if_exists("res://assets/opera/worlds/props/fx_slash_arc.png")
	fx_dust_puff_texture = _load_if_exists("res://assets/opera/worlds/props/fx_dust_puff.png")
	fx_stolen_sparkle_texture = _load_if_exists("res://assets/opera/worlds/props/fx_stolen_sparkle.png")
	fx_dizzy_stars_texture = _load_if_exists("res://assets/opera/worlds/props/fx_dizzy_stars.png")
	costumed_crew = not competition.is_cooperative() \
		and rival_actor != null and rival_actor.texture != null
	if costumed_crew:
		# The crew wears the career's special imp costume. Painted per-costume
		# state art is preferred whenever it exists; otherwise the costume
		# texture is KEPT and the state plays as a transform clip. A costumed
		# imp must never pop back to the base purple imp mid-scuffle — that
		# reads as a different character every time she is bopped.
		imp_idle_texture = rival_actor.texture
		captain_idle_texture = rival_actor.texture
		imp_bopped_texture = _load_if_exists(ImpClips.state_path(career_id, "bopped"))
		# the captain wears the same costume — the gold ring marks him, not
		# a second set of art
		captain_bopped_texture = imp_bopped_texture
	_prewarm_imp_textures()

	_build_lens_zoom_surface()
	lens_layer = Control.new()
	lens_layer.name = "MagnifierLensLayer"
	_full_rect(lens_layer)
	lens_layer.mouse_filter = Control.MOUSE_FILTER_IGNORE
	lens_layer.visible = false
	lens_layer.gui_input.connect(_lens_input)
	lens_layer.draw.connect(_draw_lens_layer)
	root.add_child(lens_layer)

	_capture_actor_rest("player", player_actor)
	_capture_actor_rest("rival", rival_actor)
	_capture_actor_rest("prop", prop_rect)


func _actor(path: String) -> TextureRect:
	var actor := TextureRect.new()
	actor.texture = load(path) as Texture2D
	actor.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	actor.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	actor.mouse_filter = Control.MOUSE_FILTER_IGNORE
	return actor


func _load_if_exists(path: String) -> Texture2D:
	return load(path) as Texture2D if ResourceLoader.exists(path) else null


func _build_lens_zoom_surface() -> void:
	# Mobile has no spatial post-process path, but its Canvas renderer supports a
	# screen-texture sample. One small circular ColorRect therefore gives the
	# glass honest optical zoom without duplicating the 2048px tiled backdrop.
	var shader := Shader.new()
	shader.code = """shader_type canvas_item;
uniform sampler2D screen_texture : hint_screen_texture, filter_linear;
uniform vec2 lens_center_screen = vec2(0.5, 0.5);
uniform float magnification = 1.75;

void fragment() {
	float distance_from_center = distance(UV, vec2(0.5));
	if (distance_from_center > 0.5) {
		discard;
	}
	vec2 sample_uv = lens_center_screen
		+ (SCREEN_UV - lens_center_screen) / magnification;
	sample_uv = clamp(sample_uv, vec2(0.001), vec2(0.999));
	vec4 sampled = texture(screen_texture, sample_uv);
	float feather = 1.0 - smoothstep(0.465, 0.5, distance_from_center);
	COLOR = vec4(sampled.rgb * 1.045, sampled.a * feather);
} """
	lens_zoom_material = ShaderMaterial.new()
	lens_zoom_material.shader = shader
	lens_zoom_material.set_shader_parameter("magnification", LENS_MAGNIFICATION)
	lens_zoom_surface = ColorRect.new()
	lens_zoom_surface.name = "MagnifierOpticalZoom"
	lens_zoom_surface.color = Color.WHITE
	lens_zoom_surface.mouse_filter = Control.MOUSE_FILTER_IGNORE
	lens_zoom_surface.material = lens_zoom_material
	lens_zoom_surface.visible = false
	root.add_child(lens_zoom_surface)
	_sync_lens_zoom_surface()


func _sync_lens_zoom_surface() -> void:
	if lens_zoom_surface == null or not is_instance_valid(lens_zoom_surface):
		return
	lens_zoom_surface.position = lens_pos - Vector2.ONE * LENS_RADIUS
	lens_zoom_surface.size = Vector2.ONE * LENS_RADIUS * 2.0
	if lens_zoom_material == null or root == null or not is_instance_valid(root):
		return
	var viewport_size := get_viewport().get_visible_rect().size
	if viewport_size.x <= 0.0 or viewport_size.y <= 0.0:
		return
	var screen_center := root.position + lens_pos * root.scale
	lens_zoom_material.set_shader_parameter(
		"lens_center_screen", screen_center / viewport_size)


func _place_on_stage(actor: Control, feet: Vector2, depth_factor: float = 1.0) -> void:
	# anchor a stage character by its feet with gentle painted-depth scaling
	var depth := clampf(0.62 + (feet.y / 720.0) * 0.55, 0.62, 1.1) \
		* clampf(depth_factor, 0.68, 1.0)
	actor.scale = Vector2(depth, depth)
	var visual_size := actor.size * depth
	var placed := feet - Vector2(visual_size.x * 0.5, visual_size.y - 12.0)
	placed.x = clampf(placed.x, 16.0, StagePaths.SCREEN.x - visual_size.x - 16.0)
	placed.y = clampf(placed.y, 16.0, StagePaths.SCREEN.y - visual_size.y - 16.0)
	actor.position = placed


func _capture_actor_rest(key: String, actor: Control) -> void:
	if actor == null:
		return
	var rest := {
		"position": actor.position,
		"size": actor.size,
		"scale": actor.scale,
		"rotation": actor.rotation,
		"modulate": actor.modulate,
	}
	if actor is TextureRect:
		var sprite := actor as TextureRect
		rest["flip_h"] = sprite.flip_h
		rest["texture"] = sprite.texture
	actor_rests[key] = rest


func _apply_actor_rest(key: String, actor: Control) -> void:
	if actor == null or not actor_rests.has(key):
		return
	var rest: Dictionary = actor_rests[key]
	actor.position = rest.get("position", actor.position) as Vector2
	actor.size = rest.get("size", actor.size) as Vector2
	actor.scale = rest.get("scale", Vector2.ONE) as Vector2
	actor.rotation = float(rest.get("rotation", 0.0))
	actor.modulate = rest.get("modulate", Color.WHITE) as Color
	if actor is TextureRect:
		var sprite := actor as TextureRect
		sprite.flip_h = bool(rest.get("flip_h", sprite.flip_h))
		sprite.texture = rest.get("texture", sprite.texture) as Texture2D


func _restore_actor(key: String, actor: Control) -> void:
	var old := actor_tweens.get(key) as Tween
	if old != null and old.is_valid():
		old.kill()
	actor_tweens.erase(key)
	_apply_actor_rest(key, actor)


func _restore_stage_actors() -> void:
	_restore_actor("player", player_actor)
	_restore_actor("rival", rival_actor)
	_restore_actor("prop", prop_rect)


func _claim_actor_tween(key: String, actor: Control) -> Tween:
	var old := actor_tweens.get(key) as Tween
	if old != null and old.is_valid():
		old.kill()
	var tween := actor.create_tween()
	actor_tweens[key] = tween
	return tween


func _finish_actor_motion(key: String, actor: Control) -> void:
	actor_tweens.erase(key)
	_apply_actor_rest(key, actor)


func _set_actor_arc(progress_value: float, actor: Control, start: Vector2,
		target: Vector2, height: float) -> void:
	if actor == null or not is_instance_valid(actor):
		return
	actor.position = start.lerp(target, progress_value) \
		- Vector2(0.0, sin(progress_value * PI) * height)


func _set_glide_rotation(progress_value: float, actor: Control,
		start_rotation: float, lean: float) -> void:
	if actor == null or not is_instance_valid(actor):
		return
	actor.rotation = lerpf(start_rotation, 0.0, progress_value) \
		+ sin(progress_value * PI) * lean


func _set_actor_recoil(progress_value: float, actor: Control, start: Vector2,
		target: Vector2, offset: Vector2) -> void:
	if actor == null or not is_instance_valid(actor):
		return
	actor.position = start.lerp(target, progress_value) \
		+ offset * sin(progress_value * PI)


func _actor_key(actor: Control) -> String:
	if actor == player_actor:
		return "player"
	if actor == rival_actor:
		return "rival"
	if actor == prop_rect:
		return "prop"
	return ""


func _anchor_goal_prop(curtain_call := false) -> void:
	if prop_rect == null or phases.is_empty():
		return
	prop_rect.size = Vector2(220.0, 220.0)
	if curtain_call:
		# The completed work gets the centre spotlight only after every room
		# activity is over. This is a stage composition, not a room hotspot.
		var curtain_anchor := Vector2(StagePaths.SCREEN.x * 0.5,
			StagePaths.SCREEN.y * 0.56)
		prop_rect.position = curtain_anchor - prop_rect.size * 0.5
		prop_rect.set_meta("anchor_station", "curtain_call_spotlight")
		return
	var final_station := int(station_for_phase.get(phases.size() - 1, -1))
	if final_station < 0 or final_station >= station_list.size():
		prop_rect.visible = false
		return
	var station: Dictionary = station_list[final_station]
	var anchor: Vector2 = station.get(
		"object_pos", station.get("pos", StagePaths.SCREEN * 0.5)) as Vector2
	prop_rect.position = Vector2(
		clampf(anchor.x - prop_rect.size.x * 0.5, 12.0,
			StagePaths.SCREEN.x - prop_rect.size.x - 12.0),
		clampf(anchor.y - prop_rect.size.y * 0.5, 12.0,
			StagePaths.SCREEN.y - prop_rect.size.y - 12.0))
	prop_rect.set_meta("anchor_station", String(station.get("id", "")))


func _stage_room_finale_partner() -> void:
	# Room finales keep Roshan beside the object she deliberately reached. Pick
	# a route rest that clears both Roshan and the already-laid-out activity;
	# the old simple "opposite side" rule put the rival directly under that UI.
	if player_actor == null or rival_actor == null or stage_points.is_empty():
		return
	_restore_actor("rival", rival_actor)
	var player_centre := player_actor.position \
		+ player_actor.size * player_actor.scale * 0.5
	var player_rect := Rect2(player_actor.position,
		player_actor.size * player_actor.scale).grow(8.0)
	var panel_rect := Rect2(action_panel.position, action_panel.size).grow(8.0) \
		if action_panel != null and action_panel.visible else Rect2()
	var best_feet := StagePaths.point_along(stage_points, 0.88)
	var best_depth_factor := 1.0
	var best_score := -INF
	# The route is continuous but its landmark spacing differs by career. Sample
	# it densely rather than assuming five universal rests; this guarantees the
	# narrow actor/panel gap is considered in every painted room.
	var found_clear := false
	# A few rooms have no full-size route slot between Roshan and the 416px
	# activity focus. In those rooms the background partner takes one authored
	# depth step smaller; she remains >130px tall on the shipping surface and is
	# never hidden behind the interaction she is meant to demonstrate.
	for depth_factor: float in [1.0, 0.86, 0.70]:
		for sample_index in range(101):
			var candidate_t := float(sample_index) / 100.0
			var candidate_feet := StagePaths.point_along(stage_points, candidate_t)
			_place_on_stage(rival_actor, candidate_feet, depth_factor)
			var candidate_rect := Rect2(rival_actor.position,
				rival_actor.size * rival_actor.scale).grow(8.0)
			var player_overlap := candidate_rect.intersection(player_rect).get_area()
			var panel_overlap := candidate_rect.intersection(panel_rect).get_area() \
				if action_panel != null and action_panel.visible else 0.0
			var clear := is_zero_approx(player_overlap) and is_zero_approx(panel_overlap)
			var score := candidate_rect.get_center().distance_to(player_centre) * 0.05 \
				- player_overlap * 20.0 - panel_overlap * 20.0
			if clear:
				score += 100000.0
			if score > best_score:
				best_score = score
				best_feet = candidate_feet
				best_depth_factor = depth_factor
			found_clear = found_clear or clear
		if found_clear:
			break
	_place_on_stage(rival_actor, best_feet, best_depth_factor)
	rival_actor.flip_h = best_feet.x > player_centre.x
	rival_actor.rotation = 0.0
	rival_actor.modulate = Color.WHITE
	_capture_actor_rest("rival", rival_actor)


func _position_curtain_call_cast() -> void:
	# The proscenium has its own composition. It must not inherit any room
	# approach/rest transform captured while opening the final activity.
	if player_actor != null:
		_place_on_stage(player_actor, Vector2(360.0, 570.0))
		player_actor.flip_h = false
		player_actor.rotation = 0.0
		player_actor.modulate = Color.WHITE
	if rival_actor != null:
		_place_on_stage(rival_actor, Vector2(920.0, 570.0))
		rival_actor.flip_h = true
		rival_actor.rotation = 0.0
		rival_actor.modulate = Color.WHITE
	if prop_rect != null:
		_anchor_goal_prop(true)
		prop_rect.scale = Vector2.ONE
		prop_rect.rotation = 0.0
		prop_rect.modulate = Color.WHITE


func _assign_stations() -> void:
	# Resolve every task by its authored landmark ID. A sequential fallback can
	# silently put an activity on an unrelated object, so unmapped phases remain
	# visibly unarmed and fail the focused probe instead.
	station_for_phase = {}
	if station_list.is_empty():
		return
	var preferred: Dictionary = PHASE_STATIONS.get(career_id, {}) as Dictionary
	for index in range(phases.size()):
		var phase := phases[index] as Dictionary
		var station_id := String(preferred.get(String(phase.get("name", "")), ""))
		if not station_id.is_empty():
			var resolved := _station_index_for_id(station_id)
			if resolved >= 0:
				station_for_phase[index] = resolved
				continue
		push_warning("Opera phase has no authored room object: %s/%s" % [
			career_id, String(phase.get("name", "phase_%d" % index))])


func _station_index_for_id(station_id: String) -> int:
	for index in range(station_list.size()):
		if String(station_list[index].get("id", "")) == station_id:
			return index
	return -1


func _build_station_markers() -> void:
	for index in range(station_list.size()):
		var station: Dictionary = station_list[index]
		var hotspot := WorldHotspot.new() as OperaWorldHotspot2D
		hotspot.name = "ActivityHotspot_%s" % String(station.get("id", index))
		var object_pos: Vector2 = station.get(
			"object_pos", (station.get("pos", Vector2(640, 480)) as Vector2)
				- Vector2(0.0, 96.0)) as Vector2
		var hit_size: Vector2 = station.get("hotspot_size", Vector2(136, 136)) as Vector2
		hotspot.setup(index, String(station.get("id", "station_%d" % index)),
			object_pos, "", "breathe", Vector2(124, 124), hit_size)
		hotspot.pressed.connect(_on_hotspot_pressed)
		hotspot.opening_finished.connect(_on_hotspot_opening_finished)
		root.add_child(hotspot)
		station_nodes.append(hotspot)


func _active_hotspot() -> OperaWorldHotspot2D:
	if armed_station < 0 or armed_station >= station_nodes.size():
		return null
	return station_nodes[armed_station] as OperaWorldHotspot2D


func _refresh_hotspots() -> void:
	var phase_name := ""
	if phase_index >= 0 and phase_index < phases.size():
		phase_name = String((phases[phase_index] as Dictionary).get("name", ""))
	var invitation_name := phase_name
	var aliases: Dictionary = HOTSPOT_PHASE_ALIASES.get(career_id, {}) as Dictionary
	if aliases.has(phase_name):
		invitation_name = String(aliases[phase_name])
	var spec: Dictionary = HotspotCatalog.spec(career_id, invitation_name)
	for index in range(station_nodes.size()):
		var hotspot := station_nodes[index] as OperaWorldHotspot2D
		var is_current := index == armed_station and not task_open \
			and active and not phase_name.is_empty()
		if is_current:
			var texture_path := String(spec.get("path", ""))
			var motion_name := String(spec.get("motion", "breathe"))
			var presentation_name := String(spec.get("presentation", "overlay"))
			var visual_size: Vector2 = spec.get("size", Vector2(124, 124)) as Vector2
			var visual_offset: Vector2 = spec.get("offset", Vector2.ZERO) as Vector2
			hotspot.configure_object(texture_path, motion_name, visual_size,
				presentation_name, visual_offset)
			hotspot.set_meta("phase_name", phase_name)
			hotspot.set_meta("approach_pos",
				station_list[index].get("approach_pos", station_list[index]["pos"]))
		hotspot.set_armed(is_current)


func _clear_hotspot_intent() -> void:
	interaction_requested = false
	interaction_station = -1
	hotspot_opening = false
	var hotspot := _active_hotspot()
	if hotspot != null:
		hotspot.set_focused(false)


func _begin_wander_route(route: PackedVector2Array) -> void:
	wander_route = route
	wander_route_index = 0
	wander_walking = not wander_route.is_empty()
	if wander_walking:
		wander_dest = wander_route[wander_route.size() - 1]
		_play_roshan_animation("travel")


func _on_hotspot_pressed(station_index: int) -> void:
	if task_open or not active or reveal_t > 0.0 \
			or station_index != armed_station \
			or station_index < 0 or station_index >= station_list.size():
		return
	if phase_gap > 0.0:
		phase_gap = 0.0
	idle_t = 0.0
	interaction_requested = true
	interaction_station = station_index
	hotspot_opening = false
	for index in range(station_nodes.size()):
		var hotspot := station_nodes[index] as OperaWorldHotspot2D
		hotspot.set_focused(index == station_index)
	var station_id := String(station_list[station_index].get("id", ""))
	var route := StagePaths.player_route_to_station(
		career_id, wander_feet, station_id)
	if route.is_empty():
		push_warning("No approved Opera route to %s/%s" % [career_id, station_id])
		_clear_hotspot_intent()
		return
	_begin_wander_route(route)


func _on_hotspot_opening_finished(station_index: int) -> void:
	if task_open or not active or not hotspot_opening \
			or not interaction_requested or station_index != interaction_station \
			or station_index != armed_station:
		return
	hotspot_opening = false
	_open_task()


func _draw_activity_focus() -> void:
	# No clipboard, easel, title ribbon, or reading chrome. The existing themed
	# minigame art floats in a soft theatre-light bloom, with a tiny pearl trail
	# carrying the only generic progress information.
	var centre := action_panel.size * Vector2(0.5, 0.48)
	var radius := maxf(action_panel.size.x, action_panel.size.y) * 0.52
	action_panel.draw_set_transform(centre, 0.0, Vector2(1.0, 0.62))
	action_panel.draw_circle(Vector2.ZERO, radius,
		Color(0.04, 0.08, 0.24, 0.32))
	action_panel.draw_circle(Vector2.ZERO, radius * 0.88,
		Color(0.18, 0.46, 0.92, 0.12))
	action_panel.draw_arc(Vector2.ZERO, radius * 0.94, -PI * 0.84,
		-PI * 0.16, 42, Color(0.44, 0.78, 1.0, 0.48), 5.0)
	action_panel.draw_set_transform(Vector2.ZERO, 0.0, Vector2.ONE)
	if phase_fill == null:
		return
	var progress := clampf(float(phase_fill.value) / 100.0, 0.0, 1.0)
	var pearl_count := 7
	var span := minf(action_panel.size.x - 52.0, 350.0)
	var start_x := (action_panel.size.x - span) * 0.5
	var y := action_panel.size.y - 24.0
	for index in range(pearl_count):
		var at := Vector2(start_x + span * float(index) / float(pearl_count - 1), y)
		var filled := progress + 0.001 >= float(index + 1) / float(pearl_count)
		var colour := Color("#fff1b2") if filled else Color(0.34, 0.55, 0.86, 0.42)
		action_panel.draw_circle(at, 8.5 if filled else 6.5, colour)
		if filled:
			action_panel.draw_circle(at - Vector2(2.0, 2.0), 2.2, Color.WHITE)


func _draw_task_card() -> void:
	if career_id in ["boxer", "ballerina"]:
		# Specialist surfaces draw directly over their stage paintings. An opaque
		# generic card would cover the glove lanes or shrink the recital canvas.
		return
	# the exact StorybookUI menu language (see the UI extraction report):
	# paper fill, violet drop shadow, PURPLE->PURPLE_DEEP contour, gold
	# title ribbon and corner pearls — a task card that matches the menus
	var card_size := action_panel.size
	var rect := Rect2(Vector2.ZERO, card_size)
	if task_frame_texture != null:
		action_panel.draw_rect(rect.grow(-20.0), Color("#e6f5ff"), true)
		action_panel.draw_texture_rect(task_frame_texture, rect, false)
		return
	var frame := StyleBoxFlat.new()
	frame.bg_color = Color("#e6f5ff")
	frame.set_border_width_all(5)
	frame.border_color = Color("#4b33a0")
	frame.set_corner_radius_all(44)
	frame.shadow_color = Color(0.19, 0.10, 0.48, 0.34)
	frame.shadow_size = 14
	frame.shadow_offset = Vector2(0, 8)
	frame.draw(action_panel.get_canvas_item(), rect)
	var ribbon := StyleBoxFlat.new()
	ribbon.bg_color = Color("#fff7db")
	ribbon.set_border_width_all(4)
	ribbon.border_color = Color("#ffc74d").lerp(Color("#382485"), 0.62)
	ribbon.set_corner_radius_all(32)
	ribbon.draw(action_panel.get_canvas_item(), Rect2(20.0, 14.0, card_size.x - 40.0, 56.0))
	for corner: Vector2 in [
		Vector2(26, 26), Vector2(card_size.x - 26.0, 26),
		Vector2(26, card_size.y - 26.0), Vector2(card_size.x - 26.0, card_size.y - 26.0),
	]:
		action_panel.draw_circle(corner, 9.0, Color("#382485"))
		action_panel.draw_circle(corner, 6.5, Color("#b3f7ff"))
		action_panel.draw_circle(corner + Vector2(-2, -2), 2.0, Color.WHITE)


func _draw_station_marker(marker: Control) -> void:
	var index := station_nodes.find(marker)
	var current := int(station_for_phase.get(phase_index, -1)) == index
	var pulse := (sin(elapsed * 4.2) + 1.0) * 0.5 if current else 0.0
	var base := Color(1.0, 0.86, 0.42, 0.55 + pulse * 0.35) if current else Color(1.0, 1.0, 1.0, 0.22)
	if station_marker_texture != null:
		var marker_size := Vector2(96.0, 192.0) * (1.0 + pulse * 0.06)
		var marker_rect := Rect2(Vector2(-marker_size.x * 0.5, -marker_size.y + 14.0), marker_size)
		marker.draw_texture_rect(station_marker_texture, marker_rect, false, base)
		return
	marker.draw_circle(Vector2.ZERO, 26.0 + pulse * 7.0, Color(base, base.a * 0.35))
	marker.draw_arc(Vector2.ZERO, 26.0 + pulse * 7.0, 0.0, TAU, 32, base, 5.0)
	if current:
		marker.draw_circle(Vector2.ZERO, 8.0, Color(1.0, 0.97, 0.85))


func _glide_roshan_to(feet: Vector2, duration: float = 1.3) -> void:
	var depth := clampf(0.62 + (feet.y / 720.0) * 0.55, 0.62, 1.1)
	var visual_size := player_actor.size * depth
	var target := feet - Vector2(visual_size.x * 0.5, visual_size.y - 12.0)
	target.x = clampf(target.x, 16.0, StagePaths.SCREEN.x - visual_size.x - 16.0)
	target.y = clampf(target.y, 16.0, StagePaths.SCREEN.y - visual_size.y - 16.0)
	var start := player_actor.position
	var moving_left := target.x < start.x
	var rest: Dictionary = actor_rests.get("player", {})
	rest["position"] = target
	rest["scale"] = Vector2(depth, depth)
	rest["rotation"] = 0.0
	rest["flip_h"] = moving_left
	actor_rests["player"] = rest
	player_actor.flip_h = moving_left
	_play_roshan_animation("travel")
	var tween := _claim_actor_tween("player", player_actor)
	tween.set_parallel(true)
	tween.tween_method(_set_actor_arc.bind(player_actor, start, target, 12.0),
		0.0, 1.0, duration).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	tween.tween_property(player_actor, "scale", Vector2(depth, depth), duration) \
		.set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	var lean := -0.055 if moving_left else 0.055
	tween.tween_method(_set_glide_rotation.bind(player_actor, player_actor.rotation, lean),
		0.0, 1.0, duration) \
		.set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	tween.chain().tween_callback(_finish_player_glide)


func _finish_player_glide() -> void:
	_finish_actor_motion("player", player_actor)
	_play_roshan_animation("idle")


func _play_roshan_animation(animation: String) -> void:
	if player_animator == null or not is_instance_valid(player_animator):
		return
	if player_animator.current_animation != animation:
		player_animator.play(animation)


func _widget_template(phase: Dictionary) -> String:
	var mode := String(phase.get("mode", ""))
	var name := String(phase.get("name", ""))
	# A rebuilt beat can name its own family, or opt out of the generic card-art
	# family entirely. Direct specialist surfaces and contextual nursery/magic
	# scenes use "widget": "" so retired reskins cannot leak back in.
	if phase.has("widget"):
		return String(phase["widget"])
	match mode:
		"ballet_pose", "ballet_ribbon", "ballet_twirl":
			return ""
		"talk":
			return ""
		"boxing_guide", "boxing_jab", "boxing_guard", "boxing_imp", "boxing_belt":
			return ""
		"echo":
			# draws its own three singing stars; star-pad art is ledgered P2
			return ""
		"pourt":
			# the tilt-pour uses the pour art family (pitcher, bowl, fill)
			return "pour"
		"pipe":
			# draws its own rocket-bay scene; tile art is ledgered P1
			return ""
		"oven":
			# chef BAKE reuses the gauge_chef art family (ledger redirect:
			# oven face, no needle) — remove-before-toasty, never ping-pong
			return "gauge"
		"timing":
			return "gauge" if career_id in ["chef", "astronaut", "racer"] else "track"
		"hold":
			if name in ["WASH", "WASH HANDS"]:
				return "basin"
			if name in ["POUR", "SYRUP", "FILL", "FEED"]:
				return "pour"
			return "charge"
		"circle":
			return "crank"
		"swipe":
			return "push" if name in ["HERD", "DUCK", "STEER", "BEDTIME", "TO THE LINE"] else "trace"
		"tap":
			return "target"
		"choice":
			return "lanes"
		"catch":
			return "catch"
		"dance_sequence", "boxer_rhythm":
			return "lanes"
		"candy_sort":
			return "lanes"
		"paint_reveal":
			return "trace"
		"farm_lob":
			return "target"
		"xray_scan":
			return "target"
	return ""


func _show_phase() -> void:
	# Trusted probe compatibility only. Shipping setup and retries call
	# _arm_phase(), preserving room discovery and physical-object handoff.
	_arm_phase()
	_open_task()


func _arm_phase() -> void:
	_restore_stage_actors()
	competition.pause()
	phase_complete_t = 0.0
	phase_advance_pending = false
	task_open = false
	for hotspot_node in station_nodes:
		(hotspot_node as OperaWorldHotspot2D).set_armed(false)
	armed_station = -1
	wander_dwell = 0.0
	wander_walking = false
	wander_route.clear()
	wander_route_index = 0
	interaction_station = -1
	interaction_requested = false
	hotspot_opening = false
	wander_lean = 0.0
	wander_stride = 0.0
	wander_feet = _hero_feet() if player_actor != null else Vector2.ZERO
	if phase_index >= phases.size():
		active = false
		if win_callback.is_valid():
			win_callback.call()
		return
	if phase_index == _finale_start():
		# A longer sting marks the contest, but the rival clock and bars stay
		# paused until Roshan reaches the physical activity object.
		phase_gap = 0.0 if career_id == "boxer" else 2.6
	elif phase_index < _finale_start():
		if phase_index > 0:
			phase_gap = 0.0 if career_id == "boxer" else 1.0
	else:
		phase_gap = 0.0 if career_id == "boxer" else 1.0
	if career_id == "ballerina":
		# The recital stays responsive between its three specialist lessons.
		phase_gap = 0.0
	# Discovery/navigation time is never counted as competition time.
	_set_finale_visible(false)
	# Boxing switches to first-person gloves only after the invitation opens;
	# Roshan must remain visible while she walks to the physical training prop.
	if career_id == "boxer" and player_actor != null:
		player_actor.visible = true
	if backdrop_node != null:
		# The navigable room owns every interaction. Stage masters use different
		# landmark geometry and cannot share room hotspots without floating art.
		backdrop_node.set_stage(false)
	phase_progress = 0.0
	idle_t = 0.0
	var phase := phases[phase_index] as Dictionary
	var mode_name := String(phase.get("mode", "tap"))
	_play_roshan_animation("idle")
	if mode_name != "bop":
		_clear_stage_combat()
	armed_station = int(station_for_phase.get(phase_index, -1))
	if action_panel != null:
		action_panel.visible = false
	if lens_layer != null and mode_name != "lens":
		lens_layer.visible = false
		lens_layer.mouse_filter = Control.MOUSE_FILTER_IGNORE
	if lens_zoom_surface != null and mode_name != "lens":
		lens_zoom_surface.visible = false
	if prop_rect != null:
		# A separate unlit goal overlay competes with the one active blue object
		# and looked like a floating sticker. It returns only for celebration.
		prop_rect.visible = false
	var defer_detective_intro := career_id == "detective" and phase_index == 0 \
		and mode_name == "lens" and not detective_intro_played
	if m != null and not defer_detective_intro:
		m.show_msg(String(phase.get("speaker", "Roshan")), String(phase.get("voice", "Follow the golden sparkle!")), String(phase.get("vo", "hint")))
	# Bind static game art while clocks are held. The activity itself stays
	# closed until the corresponding room object has been selected and reached.
	if mode_name != "bop" and mode_name != "lens":
		_bind_widget(phase, mode_name,
			Color(competition.spec.get("accent", Color(1.0, 0.62, 0.8))), true)
	_refresh_hotspots()
	if armed_station >= 0 and armed_station < station_list.size():
		wander_layer.visible = true
		wander_layer.mouse_filter = Control.MOUSE_FILTER_STOP
	else:
		wander_layer.visible = false
		wander_layer.mouse_filter = Control.MOUSE_FILTER_IGNORE


func _bind_widget(phase: Dictionary, mode_name: String, accent: Color, armed := false) -> void:
	var template := _widget_template(phase)
	var context := "%s_%s" % [template, career_id] if not template.is_empty() else ""
	if phase.has("visual_context"):
		context = String(phase.get("visual_context", context))
	surface.configure(mode_name, accent, choice_target, context)
	# while she is still wandering, the bound widget shows but its clocks
	# (oven heat, pipe fuel, echo song) hold still until she arrives
	surface.armed_only = armed


func _open_task() -> void:
	if task_open or not active or phase_index >= phases.size():
		return
	task_open = true
	wander_walking = false
	wander_route.clear()
	wander_route_index = 0
	interaction_requested = false
	interaction_station = -1
	hotspot_opening = false
	for hotspot_node in station_nodes:
		(hotspot_node as OperaWorldHotspot2D).set_armed(false)
	if wander_layer != null:
		wander_layer.visible = false
		wander_layer.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var phase := phases[phase_index] as Dictionary
	var mode_name := String(phase.get("mode", "tap"))
	if phase_index >= _finale_start():
		competition.begin()
		_set_finale_visible(true)
	_play_roshan_animation("idle" if mode_name == "talk" else "work")
	var is_bop := mode_name == "bop"
	var is_lens := mode_name == "lens"
	var accent := Color(competition.spec.get("accent", Color(1.0, 0.62, 0.8)))
	choice_target = (phase_index + int(competition.rival_step)) % 3
	_apply_panel_layout(phase)
	if career_id == "boxer" and player_actor != null:
		# The walk-in is third person; the opened lesson is the specialist's
		# first-person two-glove view.
		player_actor.visible = false
	if phase_index >= _finale_start() or competition.is_cooperative():
		_stage_room_finale_partner()
	if action_panel.visible:
		# The activity grows out of the room object Roshan just opened instead
		# of appearing as an unrelated card at screen centre.
		action_panel.pivot_offset = _activity_reveal_pivot()
		action_panel.scale = Vector2(0.78, 0.78)
		action_panel.modulate.a = 0.0
		var reveal := action_panel.create_tween()
		reveal.set_parallel(true)
		reveal.tween_property(action_panel, "scale", Vector2.ONE, 0.28) \
			.set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
		reveal.tween_property(action_panel, "modulate:a", 1.0, 0.20)
	if is_bop:
		_start_stage_combat(phase.get("combat", {}) as Dictionary)
	if is_lens:
		_start_lens_phase(phase)
	var is_nursery_catch := career_id == "nursery" and mode_name == "catch"
	surface.visible = not is_nursery_catch
	if nursery_catch != null:
		nursery_catch.visible = is_nursery_catch
		if is_nursery_catch:
			nursery_catch.start(int(ceilf(float(phase.get("goal", 5.0)))))
		else:
			nursery_catch.stop()
	_bind_widget(phase, mode_name, accent)
	if career_id == "magician" and mode_name == "choice":
		# the shuffle the fiction always promised: glow glides into its lane
		surface.start_shuffle((choice_target + 1 + (phase_index % 2)) % 3)
	if mode_name == "talk":
		var lines: Array = phase.get("lines", [])
		talk_t = 0.6
		for line: Dictionary in lines:
			talk_t += maxf(0.8, float(line.get("hold", 3.2)))
		if m != null and not lines.is_empty():
			m.say_sequence(lines)
		# the stage stays hers while the witness talks
		if wander_layer != null:
			wander_layer.visible = true
			wander_layer.mouse_filter = Control.MOUSE_FILTER_STOP
	surface.set_fill(0.0)
	match String(phase.get("dir", "")):
		"down":
			surface.swipe_dir = Vector2.DOWN
			surface.swipe_require_dir = true
		"up":
			surface.swipe_dir = Vector2.UP
			surface.swipe_require_dir = true
	phase_fill.value = 0.0
	action_panel.queue_redraw()


func _activity_reveal_pivot() -> Vector2:
	var stage_anchor := action_panel.position + action_panel.size * 0.5
	var station_index := int(station_for_phase.get(phase_index, -1))
	if station_index >= 0 and station_index < station_list.size():
		stage_anchor = station_list[station_index].get(
			"object_pos", station_list[station_index].get("pos", stage_anchor)) as Vector2
	var local_anchor := stage_anchor - action_panel.position
	return Vector2(
		clampf(local_anchor.x, 18.0, action_panel.size.x - 18.0),
		clampf(local_anchor.y, 18.0, action_panel.size.y - 18.0))


func _repeat_phase_prompt() -> void:
	if m == null or phase_index < 0 or phase_index >= phases.size():
		return
	var phase := phases[phase_index] as Dictionary
	m.show_msg(
		String(phase.get("speaker", "Roshan")),
		String(phase.get("voice", "Follow the golden sparkle!")),
		String(phase.get("vo", "hint"))
	)


func _apply_panel_layout(phase: Dictionary) -> void:
	if action_panel == null:
		return
	var mode := String(phase.get("mode", "tap"))
	if career_id == "boxer":
		# Both glove fingers share the frozen 1280x720 Opera coordinate space.
		# The transparent host preserves the approved 2K training/stage painting.
		action_panel.visible = true
		action_panel.position = Vector2.ZERO
		action_panel.size = StagePaths.SCREEN
		surface.position = Vector2.ZERO
		surface.size = StagePaths.SCREEN
	elif career_id == "ballerina":
		# Roshan owns the left third of the proscenium; the entire remaining
		# two-thirds are a touch canvas. This is roughly six times the area of
		# the retired 392x232 card and keeps every target clear of her silhouette.
		action_panel.visible = true
		action_panel.position = Vector2(382, 20)
		action_panel.size = Vector2(874, 680)
		surface.position = Vector2(10, 10)
		surface.size = Vector2(854, 660)
	if career_id in ["boxer", "ballerina"]:
		phase_fill.visible = false
		if career_id == "ballerina":
			_stage_player_clear_of_activity()
		action_panel.queue_redraw()
		return
	if mode == "bop" or mode == "lens" or mode == "talk":
		# stage-wide beats play on the painting itself — no card at all
		action_panel.visible = false
		return
	action_panel.visible = true
	if mode == "pipe":
		# The pipe board remains large, but the ornate outer card is gone.
		action_panel.size = Vector2(736, 608)
		var left_pipe := Rect2(Vector2(24, 36), action_panel.size)
		var right_pipe := Rect2(Vector2(520, 36), action_panel.size)
		action_panel.position = _safer_panel_rect(left_pipe, right_pipe).position
		# The board occupies most of the phone canvas. Once Roshan has physically
		# reached the coolant fixture, give her a nearby route-side watching mark
		# opposite the board so neither her tail nor hands sit underneath it.
		_stage_player_clear_of_activity()
		surface.position = Vector2(12, 12)
		surface.size = Vector2(712, 560)
		action_panel.queue_redraw()
		return
	action_panel.position = _card_position_near_station()
	action_panel.size = Vector2(416, 292)
	surface.position = Vector2(12, 12)
	surface.size = Vector2(392, 232)
	if mode == "catch" and nursery_catch != null:
		# The catch surface owns the same borderless viewport as every other verb.
		nursery_catch.position = surface.position
		nursery_catch.size = surface.size
	action_panel.queue_redraw()


func _card_position_near_station() -> Vector2:
	# Dock left or right according to Roshan's actual visual rectangle. The
	# card must never cover the actor, regardless of station order or depth.
	var station_index := int(station_for_phase.get(phase_index, -1))
	var anchor := Vector2(640, 430)
	if station_index >= 0 and station_index < station_list.size():
		anchor = station_list[station_index].get(
			"approach_pos", station_list[station_index].get("pos", anchor)) as Vector2
	var y := clampf(anchor.y - 238.0, 24.0, 404.0)
	var left := Rect2(Vector2(24, y), Vector2(416, 292))
	var right := Rect2(Vector2(840, y), Vector2(416, 292))
	return _safer_panel_rect(left, right).position


func _safer_panel_rect(first: Rect2, second: Rect2) -> Rect2:
	if player_actor == null:
		return first
	var actor_rect := Rect2(player_actor.position, player_actor.size * player_actor.scale).grow(28.0)
	var candidates: Array[Rect2] = [first, second]
	# Phone-sized activity focuses can move vertically as well as switching
	# sides. This closes the last tight-room cases where both same-height docks
	# intersect Roshan even though a clear upper/lower berth exists.
	if first.size.y <= 320.0 and second.size.y <= 320.0:
		for candidate_y: float in [24.0, 214.0, 404.0]:
			candidates.append(Rect2(Vector2(first.position.x, candidate_y), first.size))
			candidates.append(Rect2(Vector2(second.position.x, candidate_y), second.size))
	var best := candidates[0]
	var best_overlap := INF
	var best_travel := INF
	for candidate: Rect2 in candidates:
		var overlap := candidate.intersection(actor_rect).get_area()
		var travel := candidate.position.distance_squared_to(first.position)
		if overlap < best_overlap - 0.01 \
				or (is_equal_approx(overlap, best_overlap) and travel < best_travel):
			best = candidate
			best_overlap = overlap
			best_travel = travel
	return best


func _stage_player_clear_of_activity() -> void:
	if player_actor == null or not player_actor.visible or action_panel == null \
			or not action_panel.visible or stage_points.is_empty() or career_id == "boxer":
		return
	var panel_rect := Rect2(action_panel.position, action_panel.size).grow(24.0)
	var current_rect := Rect2(player_actor.position,
		player_actor.size * player_actor.scale).grow(24.0)
	if current_rect.intersection(panel_rect).get_area() <= 0.01:
		return
	var current_feet := _hero_feet()
	var best_feet := current_feet
	var best_overlap := INF
	var best_travel := INF
	for sample_index in range(101):
		var candidate_feet := StagePaths.point_along(stage_points,
			float(sample_index) / 100.0)
		var depth := clampf(0.62 + (candidate_feet.y / 720.0) * 0.55, 0.62, 1.1)
		var visual_size := player_actor.size * depth
		var candidate_position := candidate_feet \
			- Vector2(visual_size.x * 0.5, visual_size.y - 12.0)
		candidate_position.x = clampf(candidate_position.x, 16.0,
			StagePaths.SCREEN.x - visual_size.x - 16.0)
		candidate_position.y = clampf(candidate_position.y, 16.0,
			StagePaths.SCREEN.y - visual_size.y - 16.0)
		var candidate_rect := Rect2(candidate_position, visual_size).grow(24.0)
		var overlap := candidate_rect.intersection(panel_rect).get_area()
		var travel := candidate_feet.distance_squared_to(current_feet)
		if overlap < best_overlap - 0.01 \
				or (is_equal_approx(overlap, best_overlap) and travel < best_travel):
			best_feet = candidate_feet
			best_overlap = overlap
			best_travel = travel
			if is_zero_approx(overlap) and travel <= 1.0:
				break
	_place_on_stage(player_actor, best_feet)
	player_actor.rotation = 0.0
	wander_feet = best_feet
	_capture_actor_rest("player", player_actor)


## Screen-space tuning for the shared imp brain. The brain thinks in the
## caller's own units, so these are PIXELS on the 1280x720 stage: a crew
## that closes from ~a third of the stage away, telegraphs for most of a
## second, and lunges about two imp-widths.
const IMP_BRAIN_TUNE := {
	"strike_range": 300.0,
	"stand_off": 186.0,
	"contact": 104.0,
	"speed": 132.0,
	"charge_speed": 520.0,
	"flee_speed": 250.0,
	"windup": 0.95,
	"charge_time": 0.4,
	"slash_time": 0.28,
	"recover": 1.15,
	"stagger": 0.5,
	"guard_time": 0.8,
	"taunt_time": 0.85,
	"flee_time": 1.1,
	"cool_min": 2.4,
	"cool_max": 5.0,
	"max_attackers": 2,
	"captain_scale": 1.2,
}


func _start_stage_combat(combat: Dictionary) -> void:
	_clear_stage_combat()
	bop_time = 0.0
	swipe_stroke = 0
	combat_warned = false
	combat_layer.mouse_filter = Control.MOUSE_FILTER_STOP
	var count := maxi(1, int(combat.get("count", 3)))
	var captain_coming := bool(combat.get("captain", false))
	# one brain per scuffle; the seed is the career + beat so the crew makes
	# the SAME decisions on every run (probe-checkable, never luck)
	imp_brain = ImpAI.new(IMP_BRAIN_TUNE, career_id.hash() + phase_index * 7919)
	imp_brain.begin_crew(count + (1 if captain_coming else 0))
	for index in range(count):
		# deterministic spread along the painted route — no RNG
		var roam := StagePaths.roam_range(career_id)
		var spread := roam.y - roam.x
		var t := roam.x + fmod(float(index) * spread / float(count)
			+ float(career_id.length()) * 0.031, spread)
		_spawn_stage_imp(t, false, index)
	captain_pending = captain_coming
	# Roshan takes her mark so the crew has room to come at her from both
	# sides: mid-route for the first scuffle, the stage door for the chase
	_glide_roshan_to(StagePaths.point_along(stage_points, 0.78 if captain_coming else 0.42), 0.9)


func _spawn_stage_imp(path_t: float, captain: bool, seed_index: int) -> void:
	var node := TextureRect.new()
	node.texture = captain_idle_texture if captain else imp_idle_texture
	node.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	node.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	node.mouse_filter = Control.MOUSE_FILTER_IGNORE
	# scale contract (owner 2026-08-03): Roshan is a small bit taller than the
	# imps and never more than 1.5x — 1.39x the crew, 1.25x the captain.
	node.size = Vector2(200, 200) if captain else Vector2(180, 180)
	# Pivot at the imp's feet: squash, stretch, and the hop lean all keep him
	# planted on the painted route without touching the placement maths.
	node.pivot_offset = node.size * Vector2(0.5, 1.0)
	combat_layer.add_child(node)
	var feet := StagePaths.point_along(stage_points, path_t)
	var imp := {
		"node": node, "t": path_t, "dir": 1.0 if seed_index % 2 == 0 else -1.0,
		"speed": (46.0 if captain else 60.0) + float(seed_index % 3) * 14.0,
		"hp": 2 if captain else 1, "captain": captain,
		"popped": false, "seed": seed_index, "stroke": -1,
		"feet": feet, "carrying": false, "pose": "prowl",
	}
	if imp_brain != null:
		var mind: Dictionary = imp_brain.spawn_mind(seed_index, captain)
		mind["pos"] = feet
		imp["ai"] = mind
	# place it once up front: a tap that arrives before the first tick must
	# still find the imp where it looks like it is
	_apply_imp_pose(imp, node, feet, "prowl", 1.0)
	combat_imps.append(imp)


func _clear_stage_combat() -> void:
	for imp: Dictionary in combat_imps:
		var node_ref: Variant = imp.get("node")
		if is_instance_valid(node_ref):
			var node := node_ref as TextureRect
			node.queue_free()
	combat_imps = []
	combat_marks = []
	imp_brain = null
	captain_pending = false
	if combat_layer != null:
		combat_layer.mouse_filter = Control.MOUSE_FILTER_IGNORE
	if combat_fx != null:
		combat_fx.queue_redraw()


func _combat_remaining() -> int:
	var left := 0
	for imp: Dictionary in combat_imps:
		if not bool(imp.get("popped", false)):
			left += 1
	return left


func _spawn_stage_captain() -> void:
	captain_pending = false
	_spawn_stage_imp(0.5, true, combat_imps.size())
	if m != null:
		m.show_msg("Imp Captain", "Hee hee! You'll have to bop ME twice!", "op_captain")


func _combat_input(event: InputEvent) -> void:
	if not active or combat_imps.is_empty():
		return
	if event is InputEventMouseButton and (event as InputEventMouseButton).device == InputEvent.DEVICE_ID_EMULATION:
		return
	if event is InputEventMouseMotion and (event as InputEventMouseMotion).device == InputEvent.DEVICE_ID_EMULATION:
		return
	if event is InputEventScreenTouch and (event as InputEventScreenTouch).pressed:
		_combat_strike((event as InputEventScreenTouch).position, (event as InputEventScreenTouch).position)
		swipe_stroke += 1
	elif event is InputEventMouseButton and (event as InputEventMouseButton).button_index == MOUSE_BUTTON_LEFT and (event as InputEventMouseButton).pressed:
		_combat_strike((event as InputEventMouseButton).position, (event as InputEventMouseButton).position)
		swipe_stroke += 1
	elif event is InputEventScreenDrag:
		var drag := event as InputEventScreenDrag
		_combat_strike(drag.position - drag.relative, drag.position)
	elif event is InputEventMouseMotion and Input.is_mouse_button_pressed(MOUSE_BUTTON_LEFT):
		var motion := event as InputEventMouseMotion
		_combat_strike(motion.position - motion.relative, motion.position)


func _combat_strike(from: Vector2, to: Vector2) -> void:
	# taps and swipe sweeps both bop: an imp is hit when the stroke segment
	# passes within its friendly reach
	var hit_any := false
	for imp: Dictionary in combat_imps:
		if bool(imp.get("popped", false)) or int(imp.get("stroke", -1)) == swipe_stroke:
			continue
		var node := imp.get("node") as TextureRect
		if node == null or not is_instance_valid(node):
			continue
		# aim at where the imp is actually drawn: the pose tick publishes the
		# drawn centre and a depth-scaled reach, and _imp_centre backstops it
		# from the node's own pivot/scale if a stroke ever lands first
		var center: Vector2 = imp.get("center", _imp_centre(node))
		var reach: float = float(imp.get("reach", node.size.x * 0.62))
		# the counter window: an imp caught in its recovery is a bigger,
		# friendlier target than one still on its feet
		if String(imp.get("pose", "")) == "recover":
			reach *= 1.45
		if _segment_distance(from, to, center) <= reach:
			imp["stroke"] = swipe_stroke
			hit_any = true
			_hit_stage_imp(imp, center)
	if imp_brain != null:
		imp_brain.on_player_swing(hit_any)
	if not hit_any and from.distance_to(to) < 6.0:
		# a stray tap fizzles kindly; repeats inside the cooldown pay nothing
		_bop_burst_at(to, true)
		var pay := 0.0
		if combat_miss_cool <= 0.0:
			combat_miss_cool = 0.45
			pay = 0.05
		_register_bop(pay, 0.2)


func _segment_distance(a: Vector2, b: Vector2, point: Vector2) -> float:
	var ab := b - a
	var len_sq := ab.length_squared()
	if len_sq <= 0.0001:
		return a.distance_to(point)
	var t := clampf((point - a).dot(ab) / len_sq, 0.0, 1.0)
	return (a + ab * t).distance_to(point)


func _hit_stage_imp(imp: Dictionary, at: Vector2) -> void:
	var mind: Dictionary = imp.get("ai", {})
	var node := imp.get("node") as TextureRect
	if String(imp.get("pose", "")) == "guard" and not mind.is_empty() and imp_brain != null:
		# the captain's guard: a bop bounces off, breaks the block early and
		# leaves him open. It costs no health, but nothing is ever wasted —
		# the guard drops NOW instead of running its own clock out.
		mind["state"] = "recover"
		mind["pose"] = "recover"
		mind["t"] = 0.0
		combat_marks.append({"kind": "bump", "pos": at, "t": 0.0, "life": 0.4})
		_bop_burst_at(at, true)
		_register_bop(0.2, 1.0)
		return
	imp["hp"] = int(imp.get("hp", 1)) - 1
	var popped := int(imp["hp"]) <= 0
	if imp_brain != null and not mind.is_empty():
		imp_brain.on_hit(mind, popped)
	if popped:
		imp["popped"] = true
		if node != null and is_instance_valid(node):
			# Painted per-costume state art when it exists; when it does not the
			# imp KEEPS her own texture and the pop clip carries the state. A
			# costumed imp must never pop back to the base purple imp — that
			# reads as a different character every time she is bopped.
			var bopped := _imp_texture(imp, "bopped")
			combat_marks.append({"kind": "dizzy", "pos": at, "node": node,
				"t": 0.0, "life": 0.62})
			if bopped != null:
				node.texture = bopped
			_pop_imp_node(node)
	# (a survivor needs no squash tween: the brain puts it straight into the
	# stagger pose, which the pose renderer plays every frame)
	_bop_burst_at(at, false)
	var bonus := 0.0
	if popped and bool(imp.get("carrying", false)):
		# it swiped a sparkle off her earlier — bopping it wins the sparkle
		# back, so being bumped only ever ADDS something to chase
		imp["carrying"] = false
		bonus = 0.5
		combat_marks.append({"kind": "taunt", "pos": at, "t": 0.0, "life": 0.6})
		_bop_burst_at(at, false)
	# one gesture, bonus folded in: a pop that finishes the beat must not
	# spill its sparkle bonus into the next phase
	_register_bop(1.0 + bonus, 1.0)


func _imp_centre(node: Control) -> Vector2:
	# Where the sprite is drawn: a Control scales about its pivot, so the feet
	# pivot the roaming imps use puts their centre above their position.
	var half := node.size * 0.5
	return node.position + node.pivot_offset + node.scale * (half - node.pivot_offset)


func _pop_imp_node(node: TextureRect) -> void:
	# Re-anchor to the sprite's centre so the shoo-off spins and squashes about
	# the imp instead of about her feet, keeping her where she was standing.
	var half := node.size * 0.5
	var centre := _imp_centre(node)
	node.pivot_offset = half
	node.position = centre - half
	node.rotation = 0.0
	var depth := maxf(0.2, (node.scale.x + node.scale.y) * 0.5)
	node.scale = Vector2(depth, depth) * ImpClips.bopped_squash()
	node.modulate = ImpClips.bopped_tint()
	var stretch := Vector2(depth, depth) * ImpClips.bopped_stretch()
	var pop := node.create_tween()
	pop.tween_property(node, "scale", stretch, 0.18).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	pop.parallel().tween_property(node, "rotation", ImpClips.bopped_spin(), 0.3).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	pop.parallel().tween_property(node, "modulate:a", 0.0, ImpClips.duration("bopped"))
	pop.tween_callback(node.queue_free)



func _register_bop(amount: float, quality: float) -> void:
	# feeds the shared phase pipeline exactly like a gesture-surface event
	_on_gesture("bop", amount, quality)


func _finale_start() -> int:
	return clampi(int(FINALE_START.get(career_id, phases.size() - 1)), 0, maxi(0, phases.size() - 1))


func in_competition_finale() -> bool:
	return phase_index >= _finale_start()


func competition_progress() -> float:
	if phases.is_empty() or phase_index < _finale_start():
		return 0.0
	if phase_index >= phases.size():
		return 1.0
	var phase := phases[phase_index] as Dictionary
	var local := clampf(phase_progress / maxf(0.1, float(phase.get("goal", 1.0))), 0.0, 1.0)
	var finale_size := maxi(1, phases.size() - _finale_start())
	return (float(phase_index - _finale_start()) + local) / float(finale_size)


func _set_finale_visible(show_finale: bool) -> void:
	if career_id in ["boxer", "ballerina"]:
		# Specialist surfaces own their feedback. The boxer draws exactly one
		# padded imp; ballet uses held poses and pearls instead of race meters.
		if player_bar != null:
			player_bar.visible = false
		if rival_bar != null:
			rival_bar.visible = false
		if player_actor != null:
			player_actor.visible = career_id == "ballerina"
		if rival_actor != null:
			rival_actor.visible = false
		return
	var cooperative := competition != null and competition.is_cooperative()
	if player_bar != null:
		player_bar.visible = show_finale
	if rival_bar != null:
		rival_bar.visible = show_finale
	if rival_actor != null:
		rival_actor.visible = show_finale or cooperative

func _on_boxing_gesture(kind: String, amount: float, quality: float) -> void:
	# Cosmetic contact is deliberately outside scoring. It cannot become a
	# miss, change a high-water mark, or consume the next accepted punch.
	if kind == "boxing_contact":
		idle_t = 0.0
		return
	if kind not in [
		"boxing_guide", "boxing_jab", "boxing_guard", "boxing_imp", "boxing_belt",
	]:
		return
	if phase_advance_pending:
		return
	if not task_open:
		_open_task()
	if amount <= 0.0:
		# A short, sideways, guarded, or out-of-bounds try is a fresh wordless
		# cue. Crucially, competition.note_miss() is never called here.
		idle_t = 0.0
		surface.note_result(false)
		surface.restart_demo()
		return
	idle_t = 0.0
	surface.note_input()
	surface.note_result(quality >= 0.5)
	var phase := phases[phase_index] as Dictionary
	var goal := maxf(0.1, float(phase.get("goal", 1.0)))
	phase_progress = minf(goal, phase_progress + amount)
	var progress := clampf(phase_progress / goal, 0.0, 1.0)
	phase_fill.value = progress * 100.0
	surface.set_fill(progress)
	if competition != null and competition.active and score_cool <= 0.0:
		competition.note_success(10)
		score_cool = 0.5
	if phase_progress < goal:
		return
	surface.accept_completion()
	phase_complete_t = 2.2 if kind == "boxing_belt" else 1.1
	phase_advance_pending = true


func _repeat_ballet_instruction() -> void:
	if m == null or phase_index >= phases.size():
		return
	ballet_instruction_repeats += 1
	var phase := phases[phase_index] as Dictionary
	if String(phase.get("mode", "")) == "ballet_pose":
		# The first line asks her to watch; once a portrait is tappable, the
		# existing family recording clearly hands the turn to the child.
		m.show_msg("Roshan", "Tap the glowing dance pose!", "op_ballerina_steps")
		return
	_repeat_phase_prompt()


func _on_ballet_gesture(kind: String, amount: float, quality: float) -> void:
	if phase_advance_pending:
		# Trusted probes may skip the celebratory hold just as the shared gesture
		# path does. Real touch remains locked until the held pose has been seen.
		if kind == "probe":
			_advance_completed_phase()
			if phase_index >= phases.size():
				return
		else:
			return
	if kind == "ballet_pose_cue":
		if player_animator != null:
			player_animator.show_pose("work", clampi(int(round(amount)), 0, 3))
		return
	if kind == "ballet_ready":
		idle_t = 0.0
		# Only Pearl Mirror emits this event: its 2.15-second watch demo has
		# finished, so the shorter "your turn" recording can now play alone.
		_repeat_ballet_instruction()
		return
	if kind not in ["ballet_pose", "ballet_ribbon", "ballet_twirl", "probe"]:
		return
	if not task_open:
		_open_task()
	if amount <= 0.0:
		# A near miss is a cue, never a penalty. The specialist surface keeps the
		# accepted portrait/checkpoints and replays only the unresolved part.
		if surface != null:
			surface.note_result(false)
			surface.restart_demo()
		return
	idle_t = 0.0
	if surface != null:
		surface.note_input()
		surface.note_result(true)
	var phase := phases[phase_index] as Dictionary
	var goal := maxf(0.1, float(phase.get("goal", 1.0)))
	phase_progress = minf(goal, phase_progress + amount)
	var progress := clampf(phase_progress / goal, 0.0, 1.0)
	phase_fill.value = progress * 100.0
	surface.set_fill(progress)
	if competition != null and competition.active and score_cool <= 0.0:
		competition.note_success(10)
		score_cool = 0.5
	# A real accepted unit may change her pose; finger samples and mistakes may
	# not. Three broad arm-shape holds read as port de bras instead of flailing.
	if player_animator != null:
		var mode := String(phase.get("mode", ""))
		if mode == "ballet_ribbon":
			var ribbon_band := mini(BalletSurface.POSE_FRAMES.size() - 1,
				int(floor(progress * 3.0)))
			player_animator.show_pose("work", int(BalletSurface.POSE_FRAMES[ribbon_band]))
	if phase_progress < goal:
		return
	surface.accept_completion()
	if phase_index == phases.size() - 1:
		_play_roshan_animation("cheer")
		phase_complete_t = 2.2
	else:
		# Let the current instruction/pose settle before the next phase speaks.
		phase_complete_t = BALLET_PHASE_HOLD_SECONDS
	phase_advance_pending = true


func _on_gesture(_kind: String, amount: float, quality: float) -> void:
	if not active or reveal_t > 0.0 or phase_index >= phases.size():
		return
	if career_id == "boxer":
		_on_boxing_gesture(_kind, amount, quality)
		return
	if career_id == "ballerina":
		_on_ballet_gesture(_kind, amount, quality)
		return
	if _kind == "echo_note":
		if m != null and m.chime != null:
			var steps: Array = [1.0, 1.1892, 1.4983]
			m.chime.pitch_scale = float(steps[clampi(surface.echo_last_note, 0, 2)]) * (1.0 if quality >= 0.9 else 0.94)
			m.chime.play()
		return
	if _kind == "pour_ding":
		if m != null and m.chime != null:
			m.chime.pitch_scale = 1.45
			m.chime.play()
		return
	if _kind == "hold_release":
		# the wind-up's payoff: MUD HOP's actual hop, the sound-check flourish
		if player_actor != null:
			_bounce_actor(player_actor, 36.0, 0.5)
		return
	if phase_advance_pending:
		_advance_completed_phase()
		return
	if phase_gap > 0.0:
		# any touch skips the between-phase sparkle sting
		phase_gap = 0.0
		if phase_index == steal_index and prop_rect != null:
			_restore_actor("prop", prop_rect)
			prop_rect.visible = false
		return
	if not task_open:
		# WANDER: real gestures never bypass the physical room object. The
		# trusted probe event preserves deterministic headless drivers only.
		if _kind != "probe":
			return
		_open_task()
		if not task_open:
			return
	var phase := phases[phase_index] as Dictionary
	var mode := String(phase.get("mode", ""))
	_play_roshan_animation("work")
	if mode == "catch" and amount < 5.0:
		return
	idle_t = 0.0
	surface.note_input()
	var pace := float(phase.get("pace", 0.0))
	if pace > 0.0 and _kind == "tap":
		if pace_cool > 0.0:
			# too quick — the baby bounces happily, the pat pays nothing
			amount = 0.0
			quality = 0.6
		else:
			pace_cool = pace
	var continuous := mode == "hold" or mode == "swipe" or mode == "circle" or mode == "pourt"
	if quality < 0.5:
		competition.note_miss()
	elif not continuous or score_cool <= 0.0:
		# continuous verbs award applause at most twice a second — a held
		# finger must not out-score the whole finale
		competition.note_success(10)
		if continuous:
			score_cool = 0.5
	var gain := amount if continuous else (maxf(0.04, amount) if amount > 0.0 else 0.0)
	phase_progress += gain
	var goal := maxf(0.1, float(phase.get("goal", 1.0)))
	var progress := clampf(phase_progress / goal, 0.0, 1.0)
	phase_fill.value = progress * 100.0
	action_panel.queue_redraw()
	# the widget's own art fills with the work: the bowl actually pours,
	# the basin actually fills. Without this the delivered _fill/_bubbles/
	# _full overlays never move and the child gets no feedback at all.
	surface.set_fill(progress)
	surface.note_result(quality >= 0.5)
	# one bounce per 0.22s: mashing used to restart the tween every frame and
	# leave her drifting off her rest transform
	if bounce_cool <= 0.0:
		bounce_cool = 0.22
		_bounce_actor(player_actor, 14.0 if quality >= 0.5 else 7.0)
	if mode == "choice":
		if quality >= 0.5:
			var previous_choice := choice_target
			# never rotate by a multiple of three — that froze the target
			choice_target = (choice_target + 1 + (phase_index % 2)) % 3
			surface.target_choice = choice_target
			# Every success immediately teaches the next answer. TRACK spends
			# that same cue time on a fresh, visible hat shuffle.
			if career_id == "magician":
				surface.start_shuffle(previous_choice)
			else:
				surface.reflash_choice()
		else:
			# A wrong pick keeps the same answer and gently repeats its cue.
			surface.reflash_choice()
	elif mode == "bop":
		if quality >= 0.5 and captain_pending and _combat_remaining() <= 2 and phase_progress < goal:
			_spawn_stage_captain()
		# the captain can never be mashed past: his two bops are reserved.
		# (probe pumps arrive with amount 100 and skip the reserve)
		if amount < 5.0 and (captain_pending or _live_captain_hp() > 0):
			var reserve := 2.0 if captain_pending else float(_live_captain_hp())
			phase_progress = minf(phase_progress, goal - reserve)
	if phase_progress >= goal:
		# hold the finished picture and celebrate it — the completion state
		# used to exist for ~0.18s before the next phase wiped it, so the
		# child never saw the thing she had just made
		surface.accept_completion()
		_play_roshan_animation("cheer")
		# The authored syrup-at-the-brim picture is already the reward. The
		# shared boxer impact puff covered its mold with an unrelated abstract
		# blob, so this one picture holds cleanly while Roshan still cheers.
		if action_panel != null and surface != null \
				and not _uses_authored_completion_picture(mode):
			_bop_burst_at(action_panel.position + surface.position + surface.size * 0.5, false)
		phase_complete_t = 2.2
		phase_advance_pending = true


func _uses_authored_completion_picture(mode: String) -> bool:
	return career_id == "candymaker" and mode == "pourt" \
		and surface != null and surface.visual_context == "pour_candymaker"


func _advance_completed_phase() -> void:
	if not phase_advance_pending:
		return
	phase_advance_pending = false
	phase_complete_t = 0.0
	phase_index += 1
	# no forced gap here: the wander window IS the breath between tasks —
	# the world stays hers until she walks up to the next lit station
	_arm_phase()


func _live_captain_hp() -> int:
	for imp: Dictionary in combat_imps:
		if bool(imp.get("captain", false)) and not bool(imp.get("popped", false)):
			return maxi(0, int(imp.get("hp", 0)))
	return 0


func _bop_burst_at(origin: Vector2, fizzle: bool) -> void:
	if bop_puff_texture != null and not fizzle:
		# the accepted boxer bubble-puff impact card is the shared hit effect
		var puff := TextureRect.new()
		puff.texture = bop_puff_texture
		puff.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		puff.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		puff.mouse_filter = Control.MOUSE_FILTER_IGNORE
		puff.position = origin - Vector2(34, 34)
		puff.size = Vector2(68, 68)
		puff.pivot_offset = Vector2(34, 34)
		root.add_child(puff)
		var pop := puff.create_tween()
		pop.tween_property(puff, "scale", Vector2(2.2, 2.2), 0.3).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
		pop.parallel().tween_property(puff, "modulate:a", 0.0, 0.34)
		pop.tween_callback(puff.queue_free)
	var bits := 4 if fizzle else 6
	for index in range(bits):
		var bit := ColorRect.new()
		bit.color = Color.from_hsv(0.72 + float(index) * 0.04, 0.4, 1.0)
		bit.position = origin
		bit.size = Vector2(7, 7) if fizzle else Vector2(9, 9)
		bit.mouse_filter = Control.MOUSE_FILTER_IGNORE
		root.add_child(bit)
		var jump := Vector2(cos(float(index) * TAU / float(bits)), sin(float(index) * TAU / float(bits))) * (40.0 if fizzle else 64.0)
		var tween := bit.create_tween()
		tween.tween_property(bit, "position", origin + jump, 0.34).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
		tween.parallel().tween_property(bit, "modulate:a", 0.0, 0.34)
		tween.tween_callback(bit.queue_free)


func _on_nursery_baby_caught(quality: float) -> void:
	if not active or phase_index >= phases.size():
		return
	var phase := phases[phase_index] as Dictionary
	if career_id != "nursery" or String(phase.get("mode", "")) != "catch":
		return
	idle_t = 0.0
	competition.note_success(18 if quality >= 0.5 else 8)
	phase_progress += 1.0
	var goal := maxf(1.0, float(phase.get("goal", 5.0)))
	var progress := clampf(phase_progress / goal, 0.0, 1.0)
	phase_fill.value = progress * 100.0
	action_panel.queue_redraw()
	# the widget's own art fills with the work: the bowl actually pours,
	# the basin actually fills. Without this the delivered _fill/_bubbles/
	# _full overlays never move and the child gets no feedback at all.
	surface.set_fill(progress)
	surface.note_result(true)
	_bounce_actor(player_actor, 14.0)
	_bounce_actor(rival_actor, 9.0)
	if phase_progress >= goal:
		# join the shared advance rhythm: hold the cozy scene, then arm
		phase_complete_t = 0.8
		phase_advance_pending = true
		_play_roshan_animation("cheer")


func _on_nursery_baby_missed() -> void:
	if not active or phase_index >= phases.size():
		return
	var phase := phases[phase_index] as Dictionary
	if career_id != "nursery" or String(phase.get("mode", "")) != "catch":
		return
	_bounce_actor(rival_actor, 14.0)
	competition.note_miss()
	if m != null:
		m._say("faron", "miss", 3.0)


func _bounce_actor(actor: Control, height: float, duration: float = 0.30) -> void:
	if actor == null:
		return
	var key := _actor_key(actor)
	if key.is_empty() or not actor_rests.has(key):
		return
	var rest: Dictionary = actor_rests[key]
	var target: Vector2 = rest.get("position", actor.position)
	var start := actor.position
	var tween := _claim_actor_tween(key, actor)
	tween.set_parallel(true)
	tween.tween_method(_set_actor_arc.bind(actor, start, target, height),
		0.0, 1.0, duration).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_OUT)
	tween.tween_property(actor, "scale", rest.get("scale", Vector2.ONE), duration)
	tween.tween_property(actor, "rotation", rest.get("rotation", 0.0), duration)
	tween.tween_property(actor, "modulate", rest.get("modulate", Color.WHITE), duration)
	tween.chain().tween_callback(_finish_actor_motion.bind(key, actor))


func _set_rival_pose(state: String) -> bool:
	if rival_actor == null or competition == null or competition.is_cooperative():
		return false
	var texture := _state_texture("rival_%s_%s" % [career_id, state])
	if texture == null:
		return false
	rival_actor.texture = texture
	return true


func progress() -> float:
	if phases.is_empty():
		return 0.0
	if phase_index >= phases.size():
		return 1.0
	var phase := phases[phase_index] as Dictionary
	var local := clampf(phase_progress / maxf(0.1, float(phase.get("goal", 1.0))), 0.0, 1.0)
	return (float(phase_index) + local) / float(phases.size())


func rival_step() -> void:
	if rival_actor == null:
		return
	_set_rival_pose("taunt")
	_bounce_actor(rival_actor, 10.0 + float(competition.rival_step) * 1.8)


func begin_guided_retry() -> void:
	# the rival's clock may only claim the STAGE contest: the investigation
	# (talk and lens hops) has no rival, so the retry can never teleport her
	# past ASK ROSALINA, the FOUNTAIN, the STAIRS and the CROWN CHASE
	if career_id != "detective" or reveal_t > 0.0 or phase_index < _finale_start():
		return
	active = false
	reveal_t = 3.6
	# the finale is the ally-corner: the rival detective DEMONSTRATES the
	# corner (taunt + VO) — there is no choice widget in this career
	_set_rival_pose("taunt")
	_bounce_actor(rival_actor, 16.0, 0.5)
	surface.restart_demo()
	if m != null:
		m.show_msg("Rival Imp", "The rival detective corners him first — watch, then trap him together!", "op_retry")


func update_competition() -> void:
	if competition == null:
		return
	player_bar.value = competition.player_progress * 100.0
	rival_bar.value = competition.rival_progress * 100.0


func celebrate(result: Dictionary) -> void:
	active = false
	competition.pause()
	_restore_stage_actors()
	if backdrop_node != null:
		# Room objects own every playable beat; the proscenium returns only for
		# this non-interactive curtain call, after hotspot geometry is irrelevant.
		backdrop_node.set_stage(true)
	# The last activity must leave with the room. Otherwise its surface survives
	# over the proscenium and obscures the cast we just staged there.
	task_open = false
	if action_panel != null:
		action_panel.visible = false
	if surface != null:
		surface.visible = false
	if lens_layer != null:
		lens_layer.visible = false
		lens_layer.mouse_filter = Control.MOUSE_FILTER_IGNORE
	if lens_zoom_surface != null:
		lens_zoom_surface.visible = false
	_clear_stage_combat()
	if nursery_catch != null:
		nursery_catch.stop()
		nursery_catch.visible = false
	# Specialist surfaces deliberately hide some cast members during play.
	# Restore both actors before applying the shared curtain-call composition.
	if player_actor != null:
		player_actor.visible = true
	if rival_actor != null:
		# The pearl ballet is a recital, not a rival contest. Keep its accepted
		# solo curtain composition while every competitive/co-op career restores
		# its partner for the bow.
		rival_actor.visible = career_id != "ballerina"
	_position_curtain_call_cast()
	_play_roshan_animation("cheer")
	_capture_actor_rest("player", player_actor)
	if wander_layer != null:
		wander_layer.visible = false
		wander_layer.mouse_filter = Control.MOUSE_FILTER_IGNORE
	for hotspot_node in station_nodes:
		(hotspot_node as OperaWorldHotspot2D).set_armed(false)
	if player_bar != null:
		player_bar.visible = false
	if rival_bar != null:
		rival_bar.visible = false
	if rival_actor != null:
		rival_actor.visible = career_id != "ballerina"
	var tier := int(result.get("tier", 1))
	if career_id == "ballerina":
		last_cheer = "A BEAUTIFUL PEARL BALLET!"
	else:
		last_cheer = (
			"THE BABIES ARE COZY!" if competition.is_cooperative()
			else "%s — ROSHAN WINS!" % String(result.get("cheer", "BIG CHEERS"))
		)
	if prop_rect != null and prop_rect.texture != null:
		# The finished object shares the centre spotlight instead of floating at
		# the old universal right-edge overlay position.
		prop_rect.visible = true
		_capture_actor_rest("prop", prop_rect)
		_bounce_actor(prop_rect, 26.0, 0.48)
	_bounce_actor(player_actor, 34.0 + float(tier) * 4.0, 0.52)
	if rival_actor != null and rival_actor.visible:
		if not _set_rival_pose("bow"):
			# Faron keeps her one accepted cutout and answers with a gentle nod.
			rival_actor.rotation = -0.045
		_capture_actor_rest("rival", rival_actor)
		_bounce_actor(rival_actor, 10.0, 0.58)
	for index in range(24):
		var bit := ColorRect.new()
		bit.color = Color.from_hsv(float(index) / 24.0, 0.58, 1.0)
		bit.position = Vector2(30.0 + float((index * 97) % 1220), -30.0 - float((index * 31) % 160))
		bit.size = Vector2(10, 22)
		bit.mouse_filter = Control.MOUSE_FILTER_IGNORE
		root.add_child(bit)
		confetti.append(bit)
		var fall := bit.create_tween()
		fall.tween_property(bit, "position:y", 760.0, 1.8 + float(index % 5) * 0.17)


func _tick_stage_combat(delta: float) -> void:
	# The crew thinks as a crew (scripts/imp_ai.gd) — who closes in, who
	# telegraphs, who hangs back — and each imp is then drawn back onto the
	# painted walkway in whatever pose it decided on.
	var hero := _hero_feet()
	if imp_brain != null:
		var minds: Array = []
		for imp: Dictionary in combat_imps:
			if bool(imp.get("popped", false)):
				continue
			var mind: Dictionary = imp.get("ai", {})
			if mind.is_empty():
				continue
			# the mind keeps its own ring coordinate; the renderer only ever
			# corrects its x (below), so the ring cannot collapse frame by
			# frame into the flattened screen depth
			mind["alive"] = true
			minds.append(mind)
		imp_brain.tick(delta, minds, hero)
		_handle_brain_events()
	for imp: Dictionary in combat_imps:
		if bool(imp.get("popped", false)):
			continue
		var node := imp.get("node") as TextureRect
		if node == null or not is_instance_valid(node):
			continue
		var mind: Dictionary = imp.get("ai", {})
		var feet: Vector2 = imp.get("feet", hero)
		var pose := "prowl"
		var face := 1.0
		if mind.is_empty():
			# no mind (never in normal play): idle in place rather than
			# freeze the fight — an imp must always stay tappable
			feet = _stage_feet_at_x(feet.x)
		else:
			# the brain circles her on a ring; the stage is a promenade, so
			# the ring's "sideways" becomes walkway travel and its "toward
			# camera" becomes standing a little in front of or behind her
			var want: Vector2 = mind.get("pos", feet)
			var base := _stage_feet_at_x(want.x)
			var depth_off := clampf(want.y - hero.y, -190.0, 190.0) * 0.42
			feet = Vector2(base.x, base.y + depth_off)
			mind["pos"] = Vector2(base.x, want.y)   # the walkway owns x
			pose = String(mind.get("pose", "prowl"))
			face = float(mind.get("face", 1.0))
			imp["state_t"] = float(mind.get("t", 0.0))
		imp["feet"] = feet
		imp["pose"] = pose
		_apply_imp_pose(imp, node, feet, pose, face)
	_tick_combat_marks(delta)


func _hero_feet() -> Vector2:
	if player_actor == null:
		return StagePaths.point_along(stage_points, 0.5)
	var s: Vector2 = player_actor.scale
	return player_actor.position + Vector2(
		player_actor.size.x * 0.5 * s.x, player_actor.size.y * s.y - 12.0)


func _stage_feet_at_x(x: float) -> Vector2:
	# snap a brain-space position back onto the painted route: imps walk the
	# walkway the world was painted with, they never float over the scenery
	if stage_points.size() < 2:
		return Vector2(clampf(x, 80.0, 1200.0), 470.0)
	var first: Vector2 = stage_points[0]
	var last: Vector2 = stage_points[stage_points.size() - 1]
	var lo: float = minf(first.x, last.x) + 40.0
	var hi: float = maxf(first.x, last.x) - 40.0
	var cx: float = clampf(x, minf(lo, hi), maxf(lo, hi))
	for index in range(stage_points.size() - 1):
		var a: Vector2 = stage_points[index]
		var b: Vector2 = stage_points[index + 1]
		if absf(b.x - a.x) < 0.001:
			continue
		if cx >= minf(a.x, b.x) and cx <= maxf(a.x, b.x):
			var f: float = clampf((cx - a.x) / (b.x - a.x), 0.0, 1.0)
			return Vector2(cx, lerpf(a.y, b.y, f))
	return Vector2(cx, first.y if cx <= first.x else last.y)


## Pose -> what the imp actually looks like this frame. State art is used
## when it exists (see CODEX_IMP_ANIMATION_HANDOFF_2026-08-02.md); until it
## lands every pose is still readable through squash, tilt, lift and tint.
func _apply_imp_pose(imp: Dictionary, node: TextureRect, feet: Vector2,
		pose: String, face: float) -> void:
	var depth := clampf(0.62 + (feet.y / 720.0) * 0.55, 0.62, 1.1)
	var seed := float(imp.get("seed", 0))
	var t := float(imp.get("state_t", 0.0))
	var resolved := _imp_texture_resolution(imp, pose)
	var resolution_kind := String(resolved.get("resolution", "idle"))
	# Authored silhouettes do the acting. Cousin/idle fallbacks retain more of
	# the old procedural envelope so a missing pose is still readable.
	var envelope := 0.24 if resolution_kind == "exact" else (0.62 if resolution_kind == "cousin" else 1.0)
	var lift := 0.0
	var squash := Vector2.ONE
	var tilt := 0.0
	var tint := Color.WHITE
	match pose:
		"windup":
			# the crouch: held, obvious, and never shorter than MIN_WINDUP
			var hold: float = imp_brain.windup_time() if imp_brain != null else 0.9
			var k := clampf(t / maxf(0.2, hold), 0.0, 1.0)
			squash = Vector2(1.0 + 0.18 * k, 1.0 - 0.2 * k)
			tilt = -0.14 * k * face
			var warning := Color(1.0, 0.9, 0.78).lerp(Color(1.0, 0.6, 0.52), k)
			tint = Color.WHITE.lerp(warning, 0.18 if resolution_kind == "exact" else 0.72)
		"charge":
			squash = Vector2(1.14, 0.92)
			tilt = 0.24 * face
			lift = 12.0
		"slash":
			squash = Vector2(1.08, 1.02)
			tilt = lerpf(-0.55, 0.55, clampf(t / 0.28, 0.0, 1.0)) * face
			lift = 8.0
		"recover":
			# wide open: the counter window reads as an exhausted slump
			squash = Vector2(1.08, 0.88)
			tilt = -0.18 * face
			tint = Color.WHITE if resolution_kind == "exact" else Color(0.84, 0.9, 1.0)
		"guard":
			squash = Vector2(0.9, 1.08)
			tint = Color.WHITE if resolution_kind == "exact" else Color(0.78, 0.93, 1.0)
		"taunt", "rally":
			lift = absf(sin(t * 9.0)) * 18.0
			tilt = sin(t * 12.0) * 0.13
		"stagger":
			tilt = sin(t * 26.0) * 0.3
			lift = 5.0
		"flee":
			lift = absf(sin(bop_time * 9.5 + seed)) * 15.0
			tilt = -0.2 * face
		_:
			lift = sin(bop_time * 5.2 + seed * 1.7) * 9.0
	squash = Vector2.ONE.lerp(squash, envelope)
	tilt *= envelope
	lift *= maxf(0.38, envelope)
	if pose == "stagger" and t <= 0.18:
		tint = Color.WHITE.lerp(Color(1.0, 0.94, 0.78), 0.32)
	var texture := resolved.get("texture") as Texture2D
	if texture != null:
		node.texture = texture
	node.pivot_offset = node.size * Vector2(0.5, 1.0)
	node.scale = Vector2(depth * squash.x, depth * squash.y)
	node.rotation = tilt
	node.flip_h = face < 0.0
	node.modulate = tint
	node.position = feet - Vector2(node.size.x * 0.5, node.size.y) - Vector2(0.0, lift - 8.0)
	imp["texture_resolution"] = resolution_kind
	imp["texture_state"] = String(resolved.get("state", "idle"))
	imp["texture_family"] = String(resolved.get("family", ""))
	imp["sole"] = node.position + node.pivot_offset
	imp["center"] = feet - Vector2(0.0, node.size.y * node.scale.y * 0.5 + lift - 8.0)
	imp["reach"] = node.size.x * 0.62 * maxf(depth, 0.7)


## Pose -> state sprite, ALWAYS inside the same character's own sheet: an
## imp in a chef's hat must never borrow the bare imp's body for one frame.
## The chain is "the pose's own art, then its nearest cousin, then idle" —
## every missing file just falls through (see the codex handoff).
const POSE_STATES := {
	"idle": ["idle"],
	"prowl": [],
	"windup": ["windup", "hop_a"],
	"charge": ["charge", "hop_b"],
	"slash": ["slash", "hop_b"],
	"recover": ["recover"],
	"guard": ["guard"],
	"taunt": ["taunt", "bow"],
	"rally": ["taunt", "bow"],
	"flee": ["flee", "hop_b"],
	"stagger": ["stagger"],
	"bopped": ["bopped"],
	"hop_a": ["hop_a"],
	"hop_b": ["hop_b"],
	"bow": ["bow"],
}
const IMP_PREWARM_STATES: Array[String] = [
	"idle", "windup", "charge", "slash", "recover", "guard", "stagger",
	"flee", "taunt", "hop_a", "hop_b", "bopped", "bow",
]


func _imp_family(captain: bool) -> String:
	# the crew wears the career costume in competitive acts, and the base
	# mischief-imp sheets in the cooperative ones
	if competition != null and not competition.is_cooperative() \
			and rival_actor != null and rival_actor.texture != null:
		return "rival_%s" % career_id
	return "imp_captain" if captain else "imp_mischief"


func _prewarm_imp_textures() -> void:
	var families: Array[String] = [_imp_family(false), _imp_family(true),
		"imp_mischief", "imp_captain"]
	var seen: Dictionary = {}
	for family: String in families:
		if seen.has(family):
			continue
		seen[family] = true
		for state: String in IMP_PREWARM_STATES:
			var slug := family if state == "idle" else "%s_%s" % [family, state]
			_state_texture(slug)


func _imp_texture_resolution(imp: Dictionary, pose: String) -> Dictionary:
	var captain := bool(imp.get("captain", false))
	var family := _imp_family(captain)
	var states: Array = POSE_STATES.get(pose, [])
	for state: String in states:
		var slug := family if state == "idle" else "%s_%s" % [family, state]
		var art := _state_texture(slug)
		if art != null:
			return {
				"texture": art,
				"resolution": "exact" if state == pose else "cousin",
				"family": family,
				"state": state,
			}
	var idle := _state_texture(family)
	return {
		"texture": idle,
		"resolution": "idle",
		"family": family,
		"state": "idle",
	}


func _imp_texture(imp: Dictionary, pose: String) -> Texture2D:
	var resolution := _imp_texture_resolution(imp, pose)
	return resolution.get("texture") as Texture2D


func _state_texture(slug: String) -> Texture2D:
	if imp_state_cache.has(slug):
		return imp_state_cache[slug] as Texture2D
	var texture := _load_if_exists("res://assets/opera/worlds/actors/%s.png" % slug)
	imp_state_cache[slug] = texture
	return texture


func _handle_brain_events() -> void:
	for ev: Dictionary in imp_brain.drain_events():
		var kind := String(ev.get("kind", ""))
		var at: Vector2 = ev.get("pos", Vector2(640, 460))
		var event_index := int(ev.get("index", -1))
		var event_face := 1.0
		for imp: Dictionary in combat_imps:
			if int(imp.get("seed", -2)) == event_index:
				var mind: Dictionary = imp.get("ai", {})
				event_face = float(mind.get("face", imp.get("dir", 1.0)))
				break
		match kind:
			"telegraph":
				combat_marks.append({"kind": "ring", "pos": at, "t": 0.0,
					"life": maxf(0.3, imp_brain.windup_time())})
				if not combat_warned and m != null:
					# the first wind-up of the act gets its own voice line —
					# a new thing to react to is never text-only
					combat_warned = true
					m.show_msg("Roshan", "Watch out! That imp is winding up — bop it before it swipes!", "hint")
			"charge":
				combat_marks.append({"kind": "dust", "pos": at, "t": 0.0, "life": 0.4})
			"contact":
				_imp_contact(int(ev.get("index", -1)), at)
			"whiff":
				combat_marks.append({"kind": "arc", "pos": at, "face": event_face,
					"t": 0.0, "life": 0.3})
			"taunt":
				combat_marks.append({"kind": "taunt", "pos": at, "t": 0.0, "life": 0.7})
			"rally":
				if m != null:
					m.show_msg("Imp Captain", "Crew! Back to me! Hee hee!", "op_captain")
			"flee":
				combat_marks.append({"kind": "dust", "pos": at, "t": 0.0, "life": 0.35})


## A slash landed. NO fail state and NO lost progress (CLAUDE.md): the imp
## bounces off Roshan's bubble shield and runs off with one of her sparkles
## — which turns that imp into a bonus target instead of a punishment.
func _imp_contact(index: int, at: Vector2) -> void:
	for imp: Dictionary in combat_imps:
		if int(imp.get("seed", -1)) != index or bool(imp.get("popped", false)):
			continue
		imp["carrying"] = true
		break
	combat_marks.append({"kind": "bump", "pos": at, "t": 0.0, "life": 0.5})
	_bop_burst_at(at, true)
	if player_actor != null:
		var rest: Dictionary = actor_rests.get("player", {})
		var target: Vector2 = rest.get("position", player_actor.position)
		var away := signf(target.x + player_actor.size.x * 0.5 - at.x)
		var shove := _claim_actor_tween("player", player_actor)
		shove.tween_method(_set_actor_recoil.bind(player_actor, player_actor.position,
			target, Vector2(away * 26.0, -8.0)), 0.0, 1.0, 0.33) \
			.set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_OUT)
		shove.tween_callback(_finish_actor_motion.bind("player", player_actor))


func _tick_combat_marks(delta: float) -> void:
	for index in range(combat_marks.size() - 1, -1, -1):
		var mark: Dictionary = combat_marks[index]
		mark["t"] = float(mark.get("t", 0.0)) + delta
		if float(mark["t"]) >= float(mark.get("life", 0.3)):
			combat_marks.remove_at(index)
	if combat_fx != null:
		combat_fx.queue_redraw()


func _draw_combat_fx() -> void:
	# the crew's intentions, drawn where a four-year-old is already looking:
	# a gold ring + "!" while an imp winds up, a swipe arc when it misses,
	# a stolen sparkle orbiting whoever bumped her
	for mark: Dictionary in combat_marks:
		var at: Vector2 = mark.get("pos", Vector2.ZERO)
		if String(mark.get("kind", "")) == "dizzy":
			var follow_ref: Variant = mark.get("node")
			if is_instance_valid(follow_ref):
				var follow := follow_ref as Control
				at = _imp_centre(follow)
		var life: float = maxf(0.05, float(mark.get("life", 0.3)))
		var k: float = clampf(float(mark.get("t", 0.0)) / life, 0.0, 1.0)
		match String(mark.get("kind", "")):
			"ring":
				var pulse := 1.0 - k
				var head := at - Vector2(0.0, 132.0)
				if fx_telegraph_ring_texture != null and fx_telegraph_bang_texture != null:
					var ring_size := Vector2.ONE * (92.0 + k * 68.0)
					combat_fx.draw_texture_rect(fx_telegraph_ring_texture,
						Rect2(at - ring_size * 0.5, ring_size), false,
						Color(1.0, 1.0, 1.0, 0.25 + pulse * 0.6))
					var bang_size := Vector2(32.0, 64.0)
					combat_fx.draw_texture_rect(fx_telegraph_bang_texture,
						Rect2(head - bang_size * 0.5, bang_size), false,
						Color(1.0, 1.0, 1.0, 0.55 + pulse * 0.45))
				else:
					combat_fx.draw_arc(at, 46.0 + k * 34.0, 0.0, TAU, 28,
						Color(1.0, 0.78, 0.28, 0.25 + pulse * 0.6), 6.0)
					combat_fx.draw_rect(Rect2(head - Vector2(6.0, 30.0), Vector2(12.0, 34.0)),
						Color(1.0, 0.85, 0.3, 0.55 + pulse * 0.45))
					combat_fx.draw_circle(head + Vector2(0.0, 14.0), 7.0,
						Color(1.0, 0.85, 0.3, 0.55 + pulse * 0.45))
			"arc":
				var face := float(mark.get("face", 1.0))
				var arc_center := at - Vector2(0.0, 60.0)
				if fx_slash_arc_texture != null:
					var arc_size := Vector2(210.0, 105.0)
					combat_fx.draw_set_transform(arc_center, 0.0, Vector2(face, 1.0))
					combat_fx.draw_texture_rect(fx_slash_arc_texture,
						Rect2(-arc_size * 0.5, arc_size),
						false, Color(1.0, 1.0, 1.0, 0.55 * (1.0 - k)))
					combat_fx.draw_set_transform(Vector2.ZERO, 0.0, Vector2.ONE)
				else:
					var start_angle := -0.9 if face >= 0.0 else PI - 0.9
					var end_angle := 0.9 if face >= 0.0 else PI + 0.9
					combat_fx.draw_arc(arc_center, 92.0, start_angle, end_angle, 20,
						Color(1.0, 1.0, 1.0, 0.55 * (1.0 - k)), 9.0)
			"dust":
				if fx_dust_puff_texture != null:
					var dust_size := Vector2.ONE * (96.0 + k * 44.0)
					combat_fx.draw_texture_rect(fx_dust_puff_texture,
						Rect2(at - dust_size * 0.5, dust_size), false,
						Color(1.0, 1.0, 1.0, 0.5 * (1.0 - k)))
				else:
					combat_fx.draw_circle(at, 18.0 + k * 26.0,
						Color(0.92, 0.88, 1.0, 0.32 * (1.0 - k)))
			"bump":
				combat_fx.draw_arc(at, 40.0 + k * 60.0, 0.0, TAU, 26,
					Color(0.62, 0.93, 1.0, 0.7 * (1.0 - k)), 7.0)
			"taunt":
				combat_fx.draw_circle(at - Vector2(0.0, 150.0 + k * 20.0), 9.0,
					Color(1.0, 0.72, 0.86, 0.75 * (1.0 - k)))
			"dizzy":
				if fx_dizzy_stars_texture != null:
					combat_fx.draw_set_transform(at - Vector2(0.0, 90.0), k * TAU * 1.5,
						Vector2.ONE * 0.46)
					combat_fx.draw_texture(fx_dizzy_stars_texture, Vector2(-128.0, -128.0),
						Color(1.0, 1.0, 1.0, 1.0 - k))
					combat_fx.draw_set_transform(Vector2.ZERO, 0.0, Vector2.ONE)
	for imp: Dictionary in combat_imps:
		if bool(imp.get("popped", false)) or not bool(imp.get("carrying", false)):
			continue
		var centre: Vector2 = imp.get("center", Vector2.ZERO)
		var spin: float = elapsed * 3.4 + float(imp.get("seed", 0))
		var star: Vector2 = centre + Vector2(cos(spin), sin(spin) * 0.5) * 54.0
		if fx_stolen_sparkle_texture != null:
			var sparkle_size := Vector2.ONE * 32.0
			combat_fx.draw_texture_rect(fx_stolen_sparkle_texture,
				Rect2(star - sparkle_size * 0.5, sparkle_size), false)
		else:
			combat_fx.draw_circle(star, 11.0, Color(1.0, 0.94, 0.55, 0.95))
			combat_fx.draw_circle(star, 5.0, Color.WHITE)


func _start_lens_phase(phase: Dictionary) -> void:
	lens_layer.visible = true
	lens_layer.mouse_filter = Control.MOUSE_FILTER_STOP
	lens_zoom_surface.visible = true
	_set_lens_position(Vector2(640, 400))
	lens_demo = true
	lens_dwell = 0.0
	lens_target = -1
	lens_since_find = 0.0
	lens_hint_target = -1
	lens_room_reactions = 0
	lens_object_sound_cool = 0.0
	lens_find_count = 0
	lens_trail_t = 0.0
	lens_object_pulses.clear()
	lens_room_objects.clear()
	for source: Dictionary in DETECTIVE_ROOM_OBJECTS:
		var entry := source.duplicate(true)
		var normalized: Vector2 = entry.get("at", Vector2.ZERO)
		entry["pos"] = Vector2(
			normalized.x * StagePaths.SCREEN.x,
			normalized.y * StagePaths.SCREEN.y)
		entry["ready_at"] = -1.0
		lens_room_objects.append(entry)
	var spots := StagePaths.clue_spots(career_id)
	var goal := mini(int(ceilf(float(phase.get("goal", 5.0)))), spots.size())
	# rotate which painted details hide sparkles so the two lens phases differ
	var offset := phase_index * 3
	lens_clues = PackedVector2Array()
	lens_found = []
	for index in range(goal):
		lens_clues.append(spots[(index + offset) % spots.size()])
		lens_found.append(false)
	if career_id == "detective" and phase_index == 0 and not detective_intro_played:
		detective_intro_played = true
		# A moving chain of light carries the stolen crown's energy to the first
		# clue while the two-line setup plays. It is guidance, never progress.
		lens_trail_from = Vector2(0.88, 0.34) * StagePaths.SCREEN
		lens_trail_to = lens_clues[0] if not lens_clues.is_empty() \
			else Vector2(0.20, 0.56) * StagePaths.SCREEN
		lens_trail_t = LENS_TRAIL_DURATION
		if m != null:
			m.say_sequence(DETECTIVE_INTRO_LINES)


func _lens_input(event: InputEvent) -> void:
	if event is InputEventMouseButton and (event as InputEventMouseButton).device == InputEvent.DEVICE_ID_EMULATION:
		return
	if event is InputEventMouseMotion and (event as InputEventMouseMotion).device == InputEvent.DEVICE_ID_EMULATION:
		return
	if event is InputEventScreenTouch and (event as InputEventScreenTouch).pressed:
		_move_lens_to((event as InputEventScreenTouch).position, true)
	elif event is InputEventScreenDrag:
		_move_lens_to((event as InputEventScreenDrag).position, true)
	elif event is InputEventMouseButton and (event as InputEventMouseButton).button_index == MOUSE_BUTTON_LEFT and (event as InputEventMouseButton).pressed:
		_move_lens_to((event as InputEventMouseButton).position, true)
	elif event is InputEventMouseMotion and Input.is_mouse_button_pressed(MOUSE_BUTTON_LEFT):
		_move_lens_to((event as InputEventMouseMotion).position, true)
	lens_layer.queue_redraw()


func _clamped_lens_position(point: Vector2) -> Vector2:
	# The functional glass always stays visible. The diagonal decorative handle
	# may cross an edge; forcing all 420px of it on-screen would leave the
	# required far-right clue outside the glass's capture radius.
	return Vector2(
		clampf(point.x, LENS_RADIUS + 4.0,
			StagePaths.SCREEN.x - LENS_RADIUS - 4.0),
		clampf(point.y, LENS_RADIUS + 4.0,
			StagePaths.SCREEN.y - LENS_RADIUS - 4.0))


func _lens_graphic_rect() -> Rect2:
	return Rect2(lens_pos - LENS_GRAPHIC_SIZE * LENS_ART_GLASS_CENTER,
		LENS_GRAPHIC_SIZE)


func _set_lens_position(point: Vector2) -> void:
	lens_pos = _clamped_lens_position(point)
	_sync_lens_zoom_surface()


func _move_lens_to(point: Vector2, inspect_room: bool) -> void:
	_set_lens_position(point)
	lens_demo = false
	idle_t = 0.0
	if inspect_room:
		_try_lens_room_object(lens_pos)


func _try_lens_room_object(point: Vector2) -> bool:
	var nearest := -1
	var nearest_distance := INF
	for index in range(lens_room_objects.size()):
		var room_object: Dictionary = lens_room_objects[index]
		var object_pos: Vector2 = room_object.get("pos", Vector2.ZERO)
		var distance := point.distance_to(object_pos)
		if distance <= float(room_object.get("radius", 64.0)) and distance < nearest_distance:
			nearest = index
			nearest_distance = distance
	if nearest < 0:
		return false
	var target: Dictionary = lens_room_objects[nearest]
	if elapsed < float(target.get("ready_at", -1.0)):
		return true
	target["ready_at"] = elapsed + 0.55
	lens_room_objects[nearest] = target
	lens_room_reactions += 1
	var object_pos: Vector2 = target.get("pos", point)
	lens_object_pulses.append({
		"pos": object_pos,
		"colour": target.get("colour", Color("#fff0a8")),
		"t": 0.0,
	})
	_bop_burst_at(object_pos, true)
	if m != null and m.chime != null and lens_object_sound_cool <= 0.0:
		m.chime.pitch_scale = 0.88 + float(nearest % 5) * 0.08
		m.chime.play()
		lens_object_sound_cool = 0.22
	return true


func _next_unfound_lens_clue() -> int:
	for index in range(lens_found.size()):
		if not lens_found[index]:
			return index
	return -1


func _next_lens_story_target() -> Vector2:
	var next_clue := _next_unfound_lens_clue()
	if next_clue >= 0:
		return lens_clues[next_clue]
	# The last clue points into the next verb instead of leaving the child at
	# a dead end: the evidence-shelf station owns the case-board task.
	var next_phase := phase_index + 1
	var station_index := int(station_for_phase.get(next_phase, -1))
	if station_index >= 0 and station_index < station_list.size():
		return station_list[station_index].get(
			"pos", Vector2(0.20, 0.56) * StagePaths.SCREEN) as Vector2
	return Vector2(0.20, 0.56) * StagePaths.SCREEN


func _tick_lens(delta: float) -> void:
	if lens_layer == null or not lens_layer.visible:
		return
	lens_since_find += delta
	lens_object_sound_cool = maxf(0.0, lens_object_sound_cool - delta)
	lens_trail_t = maxf(0.0, lens_trail_t - delta)
	for pulse_index in range(lens_object_pulses.size() - 1, -1, -1):
		var pulse: Dictionary = lens_object_pulses[pulse_index]
		pulse["t"] = float(pulse.get("t", 0.0)) + delta
		if float(pulse["t"]) >= 0.8:
			lens_object_pulses.remove_at(pulse_index)
	if lens_since_find >= LENS_HINT_DELAY and lens_hint_target < 0:
		lens_hint_target = _next_unfound_lens_clue()
		if lens_hint_target >= 0:
			# One soft burst announces where to look; the continuing glisten is
			# drawn below and never completes the clue on the child's behalf.
			_bop_burst_at(lens_clues[lens_hint_target], true)
			if m != null:
				m.show_msg("Roshan", "Hold the magnifier over the glowing clue!",
					"op_detective_peek")
	if lens_demo:
		# The wordless ghost goes to the actual next clue, not an unrelated
		# decorative sweep. Demo motion never accrues dwell or progress.
		var demo_clue := _next_unfound_lens_clue()
		if demo_clue >= 0:
			var demo_target := _clamped_lens_position(lens_clues[demo_clue])
			_set_lens_position(lens_pos.move_toward(demo_target, delta * 320.0))
	var found_index := -1
	for index in range(lens_clues.size()):
		if not lens_found[index] and lens_pos.distance_to(lens_clues[index]) <= LENS_CLUE_CAPTURE_RADIUS:
			found_index = index
			break
	if found_index != lens_target:
		lens_target = found_index
		lens_dwell = 0.0
	elif found_index >= 0 and not lens_demo:
		lens_dwell += delta
		if lens_dwell >= 0.45:
			var found_spot := lens_clues[found_index]
			lens_found[found_index] = true
			lens_find_count += 1
			lens_target = -1
			lens_dwell = 0.0
			lens_since_find = 0.0
			lens_hint_target = -1
			lens_trail_from = found_spot
			lens_trail_to = _next_lens_story_target()
			lens_trail_t = LENS_TRAIL_DURATION
			_bop_burst_at(found_spot, false)
			if m != null and not m.dialogue_active:
				m.show_msg("Roshan", "A clue! Right there, hiding where nobody looked!",
					"op_detective_work")
			_on_gesture("lens", 1.0, 1.0)
	_sync_lens_zoom_surface()
	lens_layer.queue_redraw()


func _draw_lens_layer() -> void:
	# Every accepted clue launches a short directional evidence trail. A faint
	# chain shows the route; a brighter travelling star makes its direction
	# readable without arrows or text.
	if lens_trail_t > 0.0:
		var trail_age := 1.0 - lens_trail_t / LENS_TRAIL_DURATION
		var trail_fade := clampf(lens_trail_t / 0.55, 0.0, 1.0)
		var trail_vector := lens_trail_to - lens_trail_from
		var trail_normal := trail_vector.normalized().orthogonal()
		for trail_index in range(11):
			var trail_amount := float(trail_index) / 10.0
			var trail_pos := lens_trail_from.lerp(lens_trail_to, trail_amount)
			trail_pos += trail_normal * sin(trail_amount * PI * 3.0) * 7.0
			var head_glow := clampf(1.0 - absf(trail_amount - trail_age) * 5.5,
				0.0, 1.0)
			var dot_alpha := trail_fade * (0.28 + head_glow * 0.72)
			lens_layer.draw_circle(trail_pos, 5.0 + head_glow * 7.0,
				Color(1.0, 0.90, 0.32, dot_alpha))
			if head_glow > 0.45:
				lens_layer.draw_line(trail_pos - Vector2(15.0, 0.0) * head_glow,
					trail_pos + Vector2(15.0, 0.0) * head_glow,
					Color(1.0, 0.97, 0.72, trail_fade * head_glow), 3.5)
				lens_layer.draw_line(trail_pos - Vector2(0.0, 15.0) * head_glow,
					trail_pos + Vector2(0.0, 15.0) * head_glow,
					Color(1.0, 0.97, 0.72, trail_fade * head_glow), 3.5)
	# Every authored landmark responds under the glass, even when it is not a
	# clue. That makes the dense room feel inspectable instead of decorative.
	for room_object: Dictionary in lens_room_objects:
		var object_pos: Vector2 = room_object.get("pos", Vector2.ZERO)
		var distance := lens_pos.distance_to(object_pos)
		if distance > LENS_RADIUS:
			continue
		var closeness := clampf(1.0 - distance / LENS_RADIUS, 0.0, 1.0)
		var object_colour: Color = room_object.get("colour", Color("#fff0a8"))
		var shimmer := 0.45 + (sin(elapsed * 7.0 + object_pos.x * 0.02) + 1.0) * 0.22
		lens_layer.draw_circle(object_pos, 5.0 + closeness * 5.0,
			Color(object_colour, closeness * shimmer))
		lens_layer.draw_line(object_pos - Vector2(13.0, 0.0) * closeness,
			object_pos + Vector2(13.0, 0.0) * closeness,
			Color(object_colour, closeness * 0.72), 2.5)
		lens_layer.draw_line(object_pos - Vector2(0.0, 13.0) * closeness,
			object_pos + Vector2(0.0, 13.0) * closeness,
			Color(object_colour, closeness * 0.72), 2.5)
	for pulse: Dictionary in lens_object_pulses:
		var pulse_t := clampf(float(pulse.get("t", 0.0)) / 0.8, 0.0, 1.0)
		var pulse_pos: Vector2 = pulse.get("pos", Vector2.ZERO)
		var pulse_colour: Color = pulse.get("colour", Color("#fff0a8"))
		lens_layer.draw_arc(pulse_pos, 20.0 + pulse_t * 52.0, 0.0, TAU, 32,
			Color(pulse_colour, (1.0 - pulse_t) * 0.9), 5.0)
		for ray_index in range(4):
			var direction := Vector2.from_angle(float(ray_index) * PI * 0.5 + pulse_t)
			lens_layer.draw_line(pulse_pos + direction * (16.0 + pulse_t * 18.0),
				pulse_pos + direction * (32.0 + pulse_t * 34.0),
				Color(pulse_colour, 1.0 - pulse_t), 4.0)
	# After twelve seconds without a find, one remaining clue glistens in the
	# room itself. It is a directional kindness, not automatic progress.
	if lens_hint_target >= 0 and lens_hint_target < lens_clues.size():
		var hint_pos := lens_clues[lens_hint_target]
		var hint_age := maxf(0.0, lens_since_find - LENS_HINT_DELAY)
		var hint_pulse := (sin(hint_age * 4.8) + 1.0) * 0.5
		lens_layer.draw_circle(hint_pos, 18.0 + hint_pulse * 10.0,
			Color(1.0, 0.91, 0.35, 0.16 + hint_pulse * 0.20))
		lens_layer.draw_arc(hint_pos, 32.0 + hint_pulse * 12.0, 0.0, TAU, 28,
			Color(1.0, 0.86, 0.24, 0.55 + hint_pulse * 0.40), 4.5)
		for hint_ray in range(4):
			var hint_direction := Vector2.from_angle(float(hint_ray) * PI * 0.5)
			lens_layer.draw_line(hint_pos + hint_direction * 16.0,
				hint_pos + hint_direction * (34.0 + hint_pulse * 14.0),
				Color(1.0, 0.96, 0.66, 0.65 + hint_pulse * 0.35), 4.0)
	# sparkles hide in the painting and only glow under the magic lens
	for index in range(lens_clues.size()):
		var spot := lens_clues[index]
		if lens_found[index]:
			lens_layer.draw_circle(spot, 10.0, Color(1.0, 0.9, 0.5, 0.9))
			continue
		var d := lens_pos.distance_to(spot)
		if d <= LENS_RADIUS:
			var reveal := clampf(1.0 - d / LENS_RADIUS, 0.0, 1.0)
			var twinkle := 0.6 + (sin(elapsed * 6.0 + float(index)) + 1.0) * 0.2
			lens_layer.draw_circle(spot, 13.0 * reveal, Color(1.0, 0.95, 0.55, reveal * twinkle))
			lens_layer.draw_arc(spot, 19.0 * reveal, 0.0, TAU, 20, Color(1.0, 0.85, 0.3, reveal * 0.8), 3.0)
	# The raster prop is authored at 45 degrees with translucent aqua glass.
	if magnifier_texture != null:
		lens_layer.draw_texture_rect(
			magnifier_texture,
			_lens_graphic_rect(),
			false
		)
	else:
		lens_layer.draw_circle(lens_pos, LENS_RADIUS, Color(0.75, 0.92, 1.0, 0.14))
		lens_layer.draw_arc(lens_pos, LENS_RADIUS, 0.0, TAU, 48, Color("#c88b3c"), 11.0)
		lens_layer.draw_arc(lens_pos, LENS_RADIUS - 12.0, 0.0, TAU, 48, Color(1.0, 1.0, 1.0, 0.35), 3.0)
		var handle_dir := Vector2(0.72, 0.72)
		lens_layer.draw_line(lens_pos + handle_dir * LENS_RADIUS, lens_pos + handle_dir * (LENS_RADIUS + 88.0), Color("#8a5f3c"), 19.0)
	if lens_target >= 0:
		lens_layer.draw_arc(lens_pos, LENS_RADIUS - 8.0, -PI * 0.5, -PI * 0.5 + TAU * clampf(lens_dwell / 0.45, 0.0, 1.0), 40, Color(1.0, 0.9, 0.4), 7.0)


func _process(delta: float) -> void:
	elapsed += delta
	if phase_advance_pending:
		phase_complete_t = maxf(0.0, phase_complete_t - delta)
		if phase_complete_t <= 0.0:
			_advance_completed_phase()
	if score_cool > 0.0:
		score_cool = maxf(0.0, score_cool - delta)
	if pace_cool > 0.0:
		pace_cool = maxf(0.0, pace_cool - delta)
	if bounce_cool > 0.0:
		bounce_cool = maxf(0.0, bounce_cool - delta)
	if combat_miss_cool > 0.0:
		combat_miss_cool = maxf(0.0, combat_miss_cool - delta)
	if phase_gap > 0.0:
		phase_gap = maxf(0.0, phase_gap - delta)
	if active and not task_open and reveal_t <= 0.0 and phase_index < phases.size():
		_wander_step(delta)
	if active and task_open and not phase_advance_pending and reveal_t <= 0.0 \
			and phase_index < phases.size() and talk_t > 0.0:
		var talk_phase := phases[phase_index] as Dictionary
		if String(talk_phase.get("mode", "")) == "talk":
			talk_t -= delta
			if talk_t <= 0.0:
				phase_progress = maxf(phase_progress, float(talk_phase.get("goal", 1.0)))
				surface.accept_completion()
				phase_complete_t = 0.6
				phase_advance_pending = true
		else:
			talk_t = 0.0
	if active and not phase_advance_pending and reveal_t <= 0.0 and phase_index < phases.size():
		# quiet children get the prompt again plus a fresh finger demo
		idle_t += delta
		var task_hint_delay := 7.0 if career_id == "ballerina" else 9.0
		if not task_open:
			if idle_t >= 20.0:
				# the kind assist: she walks herself to the waiting station.
				# The WALK, not the glide — the walk owns wander_feet, which
				# is what the arrival dwell reads, so she really arrives.
				idle_t = 8.0
				if armed_station >= 0 and armed_station < station_list.size():
					_on_hotspot_pressed(armed_station)
			elif idle_t >= 9.0 and idle_t - delta < 9.0 and m != null:
				# re-prompt with the phase's OWN recorded line — the hardcoded
				# "hint" event has no recording, so a quiet child used to get
				# a content-free pitched yay instead of her instruction again
				_repeat_phase_prompt()
		elif idle_t >= task_hint_delay:
			idle_t = 0.0
			var idle_mode := String((phases[phase_index] as Dictionary).get("mode", ""))
			if idle_mode == "lens":
				lens_demo = true
			else:
				surface.restart_demo()
			if career_id == "ballerina":
				# Mirror speaks only after its watch demo emits ballet_ready.
				# Ribbon and Twirl have no ready echo, so their quiet-time replay
				# uses the phase line here at the seven-second rehint.
				if idle_mode != "ballet_pose":
					_repeat_ballet_instruction()
			else:
				_repeat_phase_prompt()
	timing_phase = fmod(timing_phase + delta * minf(0.70, 0.55 + 0.02 * float(phase_index)), 2.0)
	var marker := timing_phase if timing_phase <= 1.0 else 2.0 - timing_phase
	surface.set_timing_position(marker)
	if active and not phase_advance_pending and phase_index < phases.size():
		var phase := phases[phase_index] as Dictionary
		var mode := String(phase.get("mode", ""))
		if mode == "hold" and surface.held:
			# a finger that is already down generates no new gesture events, so
			# it could never skip its own phase gap — it just went dead for 1s
			if phase_gap > 0.0:
				phase_gap = 0.0
			_on_gesture("hold", delta, 1.0)
		elif mode == "bop":
			bop_time += delta
			_tick_stage_combat(delta)
		elif mode == "lens":
			_tick_lens(delta)
	if reveal_t > 0.0:
		reveal_t -= delta
		# the reveal shows the ACTUAL answer, steady — recognition, not a light show
		surface.target_choice = choice_target
		surface.choice_flash = 0.6
		surface.queue_redraw()
		if reveal_t <= 0.0:
			guided = true
			phase_index = _finale_start()
			phase_progress = 0.0
			active = true
			competition.guided_retry()
			# A guided retry keeps the no-fail clue memory, but still returns to
			# the room's glowing object. It must not resurrect the old auto-open
			# card flow after the reveal.
			_arm_phase()
			if String((phases[phase_index] as Dictionary).get("mode", "")) == "choice":
				# remembered clues earn a head start on a MEMORY rematch;
				# a bop finale credits no hits she never landed
				phase_progress = 2.0
				phase_fill.value = clampf(2.0 / maxf(0.1, float((phases[phase_index] as Dictionary).get("goal", 1.0))), 0.0, 1.0) * 100.0


func close() -> void:
	active = false
	wander_walking = false
	wander_route.clear()
	interaction_requested = false
	hotspot_opening = false
	for hotspot_node in station_nodes:
		(hotspot_node as OperaWorldHotspot2D).set_armed(false)
	if career_id == "boxer" and surface is OperaBoxingSurface:
		(surface as OperaBoxingSurface).cancel_all_touches()
	if m != null:
		# story lines queued by talk beats must not drain into the lagoon
		m.clear_dialogue()
	if wander_layer != null:
		wander_layer.visible = false
		wander_layer.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_restore_stage_actors()
	_clear_stage_combat()
	if nursery_catch != null:
		nursery_catch.stop()
	queue_free()


func _wander_input(event: InputEvent) -> void:
	# A second toddler tap during the object's short opening flourish must not
	# fall through its disabled Button, cancel intent, and strand the invitation.
	if task_open or not active or hotspot_opening:
		return
	var point := Vector2(-1.0, -1.0)
	if event is InputEventScreenTouch:
		var touch := event as InputEventScreenTouch
		if touch.pressed:
			point = touch.position
	elif event is InputEventMouseButton:
		var click := event as InputEventMouseButton
		if click.pressed and click.button_index == MOUSE_BUTTON_LEFT:
			point = click.position
	elif event is InputEventScreenDrag:
		# a held finger leads her — the destination follows it
		point = (event as InputEventScreenDrag).position
	if point.x < 0.0:
		return
	idle_t = 0.0
	_clear_hotspot_intent()
	if phase_gap > 0.0:
		phase_gap = 0.0
	var old := actor_tweens.get("player") as Tween
	if old != null and old.is_valid():
		old.kill()
	actor_tweens.erase("player")
	if not wander_walking:
		# start from where she actually stands, never from a bobbed frame
		wander_feet = _hero_feet()
	# Empty-room input only changes travel. Hotspot buttons sit above this
	# layer and are the sole source of activity intent.
	var route := StagePaths.player_route_to_point(career_id, wander_feet, point)
	_begin_wander_route(route)


func _wander_step(delta: float) -> void:
	if player_actor == null:
		return
	if wander_walking:
		_play_roshan_animation("travel")
		while wander_route_index < wander_route.size() \
				and wander_feet.distance_to(wander_route[wander_route_index]) <= 2.0:
			wander_feet = wander_route[wander_route_index]
			wander_route_index += 1
		if wander_route_index >= wander_route.size():
			_finish_wander_route()
			return
		var previous := wander_feet
		var target := wander_route[wander_route_index]
		wander_feet = wander_feet.move_toward(target, 250.0 * delta)
		var movement := wander_feet - previous
		if absf(movement.x) > 0.5:
			player_actor.flip_h = movement.x < 0.0
		# A shallow step-bob and lean are visual children of the approved route;
		# neither feeds back into the clean feet coordinate.
		wander_stride += movement.length()
		var travel_sign := signf(movement.x) if absf(movement.x) > 0.1 else 0.0
		wander_lean = move_toward(wander_lean, travel_sign * 0.05, delta * 0.9)
		_place_on_stage(player_actor, wander_feet)
		player_actor.position.y -= absf(sin(wander_stride * 0.035)) * 7.0
		player_actor.rotation = wander_lean
		if wander_feet.distance_to(target) <= 2.0:
			wander_feet = target
			wander_route_index += 1
			if wander_route_index >= wander_route.size():
				_finish_wander_route()
	elif absf(wander_lean) > 0.001 or absf(player_actor.rotation) > 0.001:
		# settle: she straightens up and comes down off the last step
		wander_lean = move_toward(wander_lean, 0.0, delta * 2.4)
		_place_on_stage(player_actor, wander_feet)
		player_actor.rotation = wander_lean
		if absf(wander_lean) <= 0.001:
			player_actor.rotation = 0.0
			wander_stride = 0.0
			_capture_actor_rest("player", player_actor)
			_play_roshan_animation("idle")
	else:
		_play_roshan_animation("idle")


func _finish_wander_route() -> void:
	wander_walking = false
	wander_route.clear()
	wander_route_index = 0
	wander_lean = 0.0
	wander_stride = 0.0
	_place_on_stage(player_actor, wander_feet)
	player_actor.rotation = 0.0
	_capture_actor_rest("player", player_actor)
	_play_roshan_animation("idle")
	if not interaction_requested or interaction_station != armed_station:
		return
	if armed_station < 0 or armed_station >= station_list.size():
		_clear_hotspot_intent()
		return
	var approach: Vector2 = station_list[armed_station].get(
		"approach_pos", station_list[armed_station].get("pos", wander_feet)) as Vector2
	if wander_feet.distance_to(approach) > 4.0:
		_clear_hotspot_intent()
		return
	var hotspot := _active_hotspot()
	if hotspot == null:
		_clear_hotspot_intent()
		return
	hotspot_opening = true
	hotspot.play_opening()
