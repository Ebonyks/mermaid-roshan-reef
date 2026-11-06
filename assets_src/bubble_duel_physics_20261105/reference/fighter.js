// A swimmer held up by two bubbles. Physics follow docs/STUDY_NOTES.md.
(function () {
  const C = () => RL.CONFIG;

  RL.wrapDX = function (dx) {
    const w = C().WRAP_MAX - C().WRAP_MIN; // 430
    while (dx > w / 2) dx -= w;
    while (dx < -w / 2) dx += w;
    return dx;
  };

  RL.boxAt = function (f, box) { return { x: f.x + box.x, y: f.y + box.y, w: box.w, h: box.h }; };
  RL.overlapWrapped = function (a, b) {
    const dx = RL.wrapDX((b.x + b.w / 2) - (a.x + a.w / 2));
    const dy = (b.y + b.h / 2) - (a.y + a.h / 2);
    return Math.abs(dx) < (a.w + b.w) / 2 && Math.abs(dy) < (a.h + b.h) / 2;
  };

  class Fighter {
    constructor(o) {
      this.slot = o.slot;             // 1 or 2
      this.name = o.name;
      this.sheet = o.sheet;           // manifest key
      this.tint = o.tint || '#7fe6ff';
      this.charm = o.charm || 'none';
      this.cpu = o.cpu || null;       // { skill, reflex } or null
      this.lives = o.lives != null ? o.lives : C().START_LIVES;
      this.maxVX = o.maxVX || C().MAX_VX;
      this.maxVY = o.maxVY || C().MAX_VY;
      this.strength = C().STRENGTH;
      this.x = o.x; this.y = o.y;
      this.vx = 0; this.vy = o.vy || 0;
      this.dir = 0; this.face = o.face || 1;
      this.bubbles = 2; this.inflation = 100;
      this.invincible = 0; this.charge = 0;
      this.held = 0;                  // frames frozen by Ink Puff
      this.lost = false; this.swallowed = false;
      this.anim = 'idle'; this.animT = 0;
      this.sway = 0;                  // bubble lean, degrees
      this.autoTimer = 0;
      this.bumped = false;
      this.popping = [];              // bubble pop effects { side, t }
    }

    get drag() { return C().DRAG_BY_BUBBLES[this.bubbles]; }

    setAnim(a) { if (this.anim !== a) { this.anim = a; this.animT = 0; } }

    kick(dir) {
      if (this.held > 0 || this.lost || this.swallowed) return;
      const s = this.strength * (this.inflation + 50) / 150;
      const n = this.bubbles;
      if (n > 0) this.vy -= s * (n + 6) / 8;
      this.vx += s * dir * 0.75 * (n + 2) / 4;
      if (dir) this.face = dir;
      this.setAnim('kick');
      RL.Sfx.kick();
    }

    pop() {
      if (this.bubbles <= 0) return false;
      this.bubbles -= 1;
      this.popping.push({ side: this.bubbles === 1 ? 1 : -1, t: 0 });
      this.setAnim('hurt');
      RL.Sfx.pop();
      return true;
    }

    respawn() {
      this.y = C().RESPAWN_Y; this.vy = C().RESPAWN_VY; this.vx = 0;
      this.bubbles = 2; this.inflation = 100;
      this.invincible = C().INVINCIBLE_FRAMES;
      this.swallowed = false; this.held = 0;
      this.setAnim('kick');
      RL.Sfx.launch();
    }

    loseLife(world) {
      if (this.lives > 0) {
        this.lives -= 1;
        world.fx.push({ key: 'fx_respawn', x: this.x, y: C().RESPAWN_Y - 10, t: 0 });
        this.respawn();
      } else {
        this.lost = true; this.charge = 0;
        this.y = C().LOST_Y + 50;
      }
    }

    // input: { dir, kick, charm, charmEdge }
    step(input, world) {
      const c = C();
      if (this.lost) return;
      this.animT += 1 / c.FPS;
      if (this.swallowed) return;

      // Controls
      if (this.held > 0) { this.held--; input = { dir: 0, kick: false, charm: false, charmEdge: false }; }
      this.dir = input.dir;
      if (input.dir) this.face = input.dir;
      if (input.kick) this.kick(input.dir);
      RL.Charms.apply(this, input, world);

      // Integrate (start-of-round drift pushes everyone down a little)
      this.y += this.vy + world.drift;
      this.x += this.vx;
      let g = c.GRAVITY * (this.bubbles > 0 ? 1 : c.GRAVITY_NO_BUBBLES);
      if (world.kind && this.cpu == null) g *= 0.9;
      if (this.floating) g = 0;
      this.vy += g;
      if (Math.abs(this.vy) > this.maxVY * this.drag) this.vy *= c.SOFTCAP_DAMP;
      if (Math.abs(this.vx) > this.maxVX * this.drag) this.vx *= c.SOFTCAP_DAMP;
      this.floating = false;

      // Edges
      if (this.x > c.WRAP_MAX) this.x = c.WRAP_MIN;
      if (this.x < c.WRAP_MIN) this.x = c.WRAP_MAX;
      if (this.y < c.SURFACE_Y) {
        this.y = c.SURFACE_Y;
        if (this.vy < 0) {
          this.vy *= c.SURFACE_BOUNCE; this.vx *= 0.8;
          world.fx.push({ key: 'fx_splash', x: this.x, y: c.SURFACE_Y - 6, t: 0 });
          RL.Sfx.bonk();
        }
      }

      // Glow (energy) refills while you still have bubbles
      if (this.bubbles > 0 && this.charge < c.CHARGE_MAX) this.charge += 1;
      if (this.invincible > 0) this.invincible--;

      // Bubble lean follows horizontal speed (eased)
      this.sway = (this.sway * 3 + (-6 * this.vx + 0)) / 4;

      // Inflation by stage
      const mode = world.stage.inflation;
      if (mode === 'grow' && this.inflation < 125) this.inflation += 0.1;
      if (mode === 'shrink' && this.inflation > 50) this.inflation -= 0.1;
      if (mode === 'depth') this.inflation = Math.max(50, Math.min(140, this.inflation + Math.pow(this.y / 400, 3) - 0.15));

      // Animation choice
      const kickDone = this.anim === 'kick' && RL.Assets.frameFor(this.sheet, 'kick', this.animT).done;
      const hurtDone = this.anim === 'hurt' && RL.Assets.frameFor(this.sheet, 'hurt', this.animT).done;
      if (this.bubbles === 0) this.setAnim('tumble');
      else if (kickDone || hurtDone || this.anim === 'tumble') this.setAnim('idle');

      this.popping.forEach(p => p.t += 1 / c.FPS);
      this.popping = this.popping.filter(p => p.t < 0.4);

      if (this.y > c.LOST_Y) this.loseLife(world);
    }

    draw(ctx) {
      if (this.lost || this.swallowed) return;
      if (this.invincible > 0 && (this.invincible % 4) < 2) return; // blink
      const A = RL.Assets, s = C().RENDER_SCALE;
      const flip = this.face < 0;
      // Bubbles and tethers
      const scale = Math.sqrt(this.inflation / 100);
      const lean = this.sway * Math.PI / 180;
      const sides = this.bubbles === 2 ? [-1, 1] : this.bubbles === 1 ? [1] : [];
      sides.forEach(side => {
        const bx = this.x + side * 8 + Math.sin(lean) * 22, by = this.y - 24 * Math.cos(lean) - 2;
        ctx.save();
        ctx.strokeStyle = 'rgba(70,120,90,0.9)'; ctx.lineWidth = 3;
        if (A.has('tether')) {
          const len = Math.hypot(bx - this.x, by - (this.y - 3)) * s;
          const ang = Math.atan2(bx - this.x, -(by - (this.y - 3)));
          A.sprite(ctx, 'tether', 'still', 0, this.x, this.y - 3, { rot: ang, sy: len / 60 });
        } else {
          ctx.beginPath(); ctx.moveTo(this.x * s, (this.y - 3) * s); ctx.lineTo(bx * s, by * s); ctx.stroke();
        }
        ctx.restore();
        A.sprite(ctx, 'bubble', 'wobble', this.animT + side * 0.3, bx, by, { tint: this.tint, sx: scale, sy: scale, rot: lean * 0.5 });
      });
      this.popping.forEach(p => {
        const bx = this.x + p.side * 8, by = this.y - 26;
        A.sprite(ctx, 'bubble', 'pop', p.t, bx, by, { tint: this.tint });
      });
      A.sprite(ctx, this.sheet, this.anim, this.animT, this.x, this.y, { flip });
      if (this.held > 0) A.sprite(ctx, 'fx_ink', 'play', this.animT, this.x, this.y, { alpha: 0.85 });
    }
  }
  RL.Fighter = Fighter;
})();
