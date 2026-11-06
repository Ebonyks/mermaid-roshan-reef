// Execute only the supplied fresh JS movement model, with inert audio/art adapters.
// Numeric reference data only; no Flash code, pixels, sound or UI enters delivery.
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");
const crypto = require("node:crypto");
const root = path.resolve(__dirname, "../assets_src/bubble_duel_physics_20261105/reference");
const ctx = { console, Math };
ctx.window = ctx;
vm.createContext(ctx);
for (const name of ["config.js", "fighter.js", "charms.js"]) {
  vm.runInContext(fs.readFileSync(path.join(root, name), "utf8"), ctx, { filename: name });
}
ctx.RL.Sfx = Object.fromEntries(["kick", "pop", "launch", "charm", "bonk"].map(k => [k, () => {}]));
ctx.RL.Assets = { frameFor: () => ({ done: true }) };
const cases = [
  { id: "neutral", frames: 100 },
  { id: "one-neutral-flap", frames: 100, kicks: [0] },
  { id: "right-flap", frames: 90, kicks: [0], dir: 1 },
  { id: "held-direction-no-flap", frames: 90, dir: 1 },
  { id: "counter-steer", frames: 100, kicks: [0, 8, 30, 38], dirs: { 0: 1, 8: 1, 30: -1, 38: -1 } },
  { id: "repeat-flaps", frames: 120, period: 8, dir: 1 },
  { id: "one-bubble", frames: 100, bubbles: 1, period: 12, dir: -1 },
  { id: "no-bubbles", frames: 100, bubbles: 0, period: 10, dir: 1 },
  { id: "wrap", frames: 70, x: 410, vx: 6 },
  { id: "ceiling-bounce", frames: 50, y: 22, vx: 2, vy: -4, drift: 0 },
  { id: "respawn-launch", frames: 100, y: 390, vy: 7, spares: 2 },
  { id: "soft-cap", frames: 70, vx: 12, vy: -12 },
  { id: "growing", frames: 150, stage: 1, period: 10, dir: 1 },
  { id: "shrinking", frames: 150, stage: 2, period: 10, dir: -1 },
  { id: "depth", frames: 150, stage: 3, period: 12, dir: 1 },
  { id: "kind-gravity", frames: 100, kind: true, kicks: [0] },
  { id: "control-muted", frames: 70, held: 8, period: 4, dir: -1 },
];
for (const spec of cases) {
  const f = new ctx.RL.Fighter({ slot: 1, name: "reference", sheet: "unused", x: spec.x ?? 200, y: spec.y ?? 160, vy: spec.vy ?? 0, lives: spec.spares ?? 4 });
  f.vx = spec.vx ?? 0;
  f.bubbles = spec.bubbles ?? 2;
  f.held = spec.held ?? 0;
  const world = { drift: spec.drift ?? 0.5, kind: spec.kind ?? false,
    stage: { inflation: ["normal", "grow", "shrink", "depth"][spec.stage ?? 0] },
    fx: [], shots: [], opponentOf: () => null };
  spec.trace = [];
  for (let tick = 0; tick < spec.frames; tick++) {
    const kick = (spec.kicks ?? []).includes(tick) || (spec.period && tick % spec.period === 0);
    f.step({ dir: spec.dirs?.[tick] ?? spec.dir ?? 0, kick: !!kick, charm: false, charmEdge: false }, world);
    world.drift = Math.max(0, world.drift - ctx.RL.CONFIG.START_DRIFT_DECAY);
    spec.trace.push([f.x, f.y, f.vx, f.vy, f.bubbles, f.lives, f.inflation, f.charge, f.invincible, f.held, f.lost]);
  }
}
const hashes = Object.fromEntries(["config.js", "fighter.js", "charms.js"].map(n =>
  [n, crypto.createHash("sha256").update(fs.readFileSync(path.join(root, n))).digest("hex")]));
const result = { source: "Unmodified owner-supplied fresh JavaScript", fps: 30, hashes, cases,
  wrap_samples: [-645, -215, 0, 215, 645].map(dx => [dx, ctx.RL.wrapDX(dx)]),
  scope: "Movement/impulse/cap/wrap/inflation/rescue traces; inert audio and animation completion adapters. Not rendered play or a human-fun rating." };
const out = process.argv[2] || path.resolve(root, "../reference-traces.json");
fs.mkdirSync(path.dirname(out), { recursive: true });
fs.writeFileSync(out, JSON.stringify(result, null, 2) + "\n");
console.log(JSON.stringify({ out, cases: cases.length, steps: cases.reduce((n, s) => n + s.frames, 0) }));
