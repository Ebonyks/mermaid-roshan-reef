// Charms: one equipped per swimmer, powered by the glow meter.
(function () {
  const def = id => RL.CHARMS.find(c => c.id === id) || RL.CHARMS[0];
  const ready = f => f.charge >= Math.max(def(f.charm).use, 1);

  RL.Charms = {
    def, ready,
    apply(f, input, world) {
      const d = def(f.charm);
      const foe = world.opponentOf(f);
      switch (f.charm) {
        case 'finmotor': // gentle automatic kick when sinking
          if (f.autoTimer > 0) f.autoTimer--;
          if (f.vy > 1.8 && f.autoTimer === 0 && f.bubbles > 0) { f.kick(f.dir); f.autoTimer = 12; }
          break;
        case 'pearl':    // hold to hover
          if (input.charm && f.charge >= d.use && f.bubbles > 0) {
            f.floating = true; f.vy *= 0.85; f.charge -= d.use;
          }
          break;
        case 'conch':
          if (input.charmEdge && ready(f)) { f.vx += f.face * 8; f.charge -= d.use; fx(world, 'fx_splash', f); RL.Sfx.charm(); }
          break;
        case 'wand':
          if (input.charmEdge && ready(f)) {
            world.shots.push({ x: f.x + f.face * 10, y: f.y - 20, vx: f.face * 6, life: 45, owner: f });
            f.charge -= d.use; RL.Sfx.charm();
          }
          break;
        case 'lasso':
          if (input.charmEdge && ready(f) && foe && !foe.lost) {
            const dx = RL.wrapDX(f.x - foe.x), dy = f.y - foe.y;
            const m = Math.max(1, Math.hypot(dx, dy));
            foe.vx += dx / m * 5; foe.vy += dy / m * 3;
            f.charge -= d.use; RL.Sfx.charm();
          }
          break;
        case 'hush':
          if (input.charmEdge && ready(f) && foe) {
            f.charge -= d.use; foe.charge = Math.max(0, foe.charge - 100); RL.Sfx.charm();
          }
          break;
        case 'ink':
          if (input.charmEdge && ready(f) && foe && !foe.lost && foe.invincible === 0) {
            foe.held = 40; foe.vx *= 0.2; foe.vy *= 0.2; f.charge -= d.use; RL.Sfx.charm();
          }
          break;
      }
    },
  };
  function fx(world, key, f) { world.fx.push({ key, x: f.x, y: f.y, t: 0 }); }
})();
