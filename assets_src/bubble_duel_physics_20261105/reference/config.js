// Reef of Light: Bubble Duel — tuning and content tables.
// World space is 400 x 300 logical units; the canvas renders it at RENDER_SCALE.
window.RL = window.RL || {};

RL.CONFIG = {
  WORLD_W: 400,
  WORLD_H: 300,
  RENDER_SCALE: 3,          // art is authored at 3x logical size
  FPS: 30,

  // Movement (see docs/STUDY_NOTES.md for where these come from)
  GRAVITY: 0.25,
  GRAVITY_NO_BUBBLES: 1.25, // multiplier
  MAX_VX: 6,
  MAX_VY: 5,
  STRENGTH: 3,
  DRAG_BY_BUBBLES: [2.0, 1.2, 1.0],
  SOFTCAP_DAMP: 0.9,
  WRAP_MIN: -15,
  WRAP_MAX: 415,
  SURFACE_Y: 20,            // the water surface acts as the ceiling
  SURFACE_BOUNCE: -0.8,
  TRENCH_Y: 300,            // top of the dark trench (visual)
  LOST_Y: 400,              // fall past this = lose a life
  RESPAWN_Y: 300,
  RESPAWN_VY: -25,
  INVINCIBLE_FRAMES: 50,
  START_DRIFT: 0.5,
  START_DRIFT_DECAY: 0.002,
  POP_HEIGHT_MARGIN: 10,
  BUMP_MIN_SEP: 6,
  CHARGE_MAX: 100,
  START_LIVES: 4,           // spares shown in the HUD

  // Hitboxes relative to fighter origin (body center), logical units
  BODY_BOX:   { x: -7, y: -9,  w: 14, h: 20 },
  FIN_BOX:    { x: -8, y: 9,   w: 16, h: 7 },
  BUBBLE_BOX: { x: -18, y: -46, w: 36, h: 22 }, // matches the two drawn bubbles (bottom at y-24)

  // Trench hazard (original anglerfish, "Grumbletooth")
  // y values are the anchor (top of the lure/head). It hides behind the trench lip.
  HAZARD: { patrolCenter: 200, patrolRadius: 250, period: 40, lowY: 240, restY: 300,
            riseY: 262, lungeY: 232, provokeMax: 30, reach: 70, windup: 14, lungeFrames: 14 },

  KIND_MODE_DEFAULT: true,  // gentler CPU, slower fall, for young players
};

// Rivals are original Reef of Light characters. Skill ~ 20..120.
RL.RIVALS = [
  { id: 'tidbit',  name: 'Tidbit the Seahorse', skill: 25, reflex: 30, rank: 1,  sheet: 'rival_tidbit',  bubbleTint: '#ffd36b' },
  { id: 'marlo',   name: 'Marlo the Otter',     skill: 45, reflex: 50, rank: 10, sheet: 'rival_marlo',   bubbleTint: '#8fe3c1' },
  { id: 'inkwell', name: 'Inkwell the Octopus', skill: 70, reflex: 70, rank: 40, sheet: 'rival_inkwell', bubbleTint: '#c9a2ff' },
  { id: 'coralie', name: 'Coralie the Mermaid', skill: 95, reflex: 90, rank: 100, sheet: 'rival_coralie', bubbleTint: '#ff9fb6' },
];

// Stages: same arena, different bubble behavior.
RL.STAGES = [
  { id: 'sunlit',  name: 'Sunlit Shallows', bg: 'bg_sunlit',  inflation: 'normal' },
  { id: 'vents',   name: 'Warm Vents',      bg: 'bg_vents',   inflation: 'grow'   },
  { id: 'kelp',    name: 'Chilly Kelp',     bg: 'bg_kelp',    inflation: 'shrink' },
  { id: 'deep',    name: 'Glowing Deep',    bg: 'bg_deep',    inflation: 'depth'  },
];

// Charms (one equipped). Costs are in pearls. "use" is the charge cost.
RL.CHARMS = [
  { id: 'none',    name: 'No Charm',       price: 0,   use: 0,  desc: 'Just you and your bubbles.' },
  { id: 'finmotor',name: 'Wind-Up Fin',    price: 60,  use: 0,  desc: 'Kicks your tail for you every so often.' },
  { id: 'pearl',   name: 'Float Pearl',    price: 120, use: 2,  desc: 'Hold to hover in place while your glow lasts.' },
  { id: 'conch',   name: 'Current Conch',  price: 150, use: 40, desc: 'A burst of current zooms you sideways.' },
  { id: 'wand',    name: 'Sparkle Wand',   price: 220, use: 50, desc: 'Shoots a sparkle that can pop a bubble.' },
  { id: 'lasso',   name: 'Kelp Lasso',     price: 260, use: 60, desc: 'Tugs your rival toward you.' },
  { id: 'hush',    name: 'Hush Shell',     price: 300, use: 70, desc: 'Dims everyone\'s glow, your rival\'s most.' },
  { id: 'ink',     name: 'Ink Puff',       price: 340, use: 80, desc: 'A cloud of ink holds your rival still for a moment.' },
];

// Cosmetic bubble colors (shop).
RL.BUBBLE_COLORS = [
  { id: 'aqua', name: 'Aqua', tint: '#7fe6ff', price: 0 },
  { id: 'rose', name: 'Rose', tint: '#ff9fc8', price: 20 },
  { id: 'gold', name: 'Gold', tint: '#ffd36b', price: 20 },
  { id: 'mint', name: 'Mint', tint: '#9ff2c4', price: 20 },
  { id: 'lilac',name: 'Lilac',tint: '#c9a2ff', price: 30 },
];

RL.ECONOMY = { startPearls: 100, payBase: 9.5, payPerRank: 0.5, startRank: 1 };
