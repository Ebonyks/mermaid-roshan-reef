// One arena bout: two swimmers, the trench fish, charm shots, effects, HUD.
(function () {
  const C = () => RL.CONFIG;

  class Match {
    // opts: { mode: 'pvc'|'pvp'|'practice', stage, p1:{...}, p2:{...}|null, rival, kind }
    constructor(opts) {
      this.mode = opts.mode; this.stage = opts.stage; this.kind = !!opts.kind;
      this.rival = opts.rival || null;
      this.fighters = [];
      this.p1 = new RL.Fighter(Object.assign({ slot: 1, x: 90, y: 300, vy: -20, face: 1 }, opts.p1));
      if (this.p1.cpu) this.p1.brain = new RL.Brain(this.p1.cpu.skill, this.p1.cpu.reflex);
      this.fighters.push(this.p1);
      if (opts.p2) {
        this.p2 = new RL.Fighter(Object.assign({ slot: 2, x: 310, y: 300, vy: -20, face: -1 }, opts.p2));
        if (this.p2.cpu) this.p2.brain = new RL.Brain(this.p2.cpu.skill, this.p2.cpu.reflex);
        this.fighters.push(this.p2);
      }
      this.hazard = opts.mode === 'practice' ? null : new RL.Grumbletooth();
      this.targets = opts.mode === 'practice' ? makeTargets() : [];
      this.shots = []; this.fx = [];
      this.drift = C().START_DRIFT;
      this.frame = 0; this.endT = 0; this.result = null; this.paused = false;
    }
    opponentOf(f) { return this.fighters.find(o => o !== f) || null; }

    step() {
      if (Input.key('KeyP')) this.paused = !this.paused;
      if (this.paused) return;
      this.frame++;
      // Inputs
      const solo = this.mode !== 'pvp';
      for (const f of this.fighters) {
        let inp;
        if (f.brain) inp = f.brain.think(f, this.opponentOf(f), this);
        else inp = RL.Input.read(solo ? 'solo' : f.slot, f.slot === 1);
        f.step(inp, this);
      }
      if (this.drift > 0) this.drift = Math.max(0, this.drift - C().START_DRIFT_DECAY);
      if (this.hazard) this.hazard.step(this);

      // Practice: trench is a safety net, targets to pop
      if (this.mode === 'practice') {
        const f = this.p1;
        if (f.y > 285) { f.y = 285; f.vy = -9; f.bubbles = 2; RL.Sfx.launch(); }
        f.lives = C().START_LIVES;
        for (const t of this.targets) {
          t.t += 1 / 30; t.y = t.baseY + Math.sin(t.t * 1.3 + t.phase) * 6;
          if (!t.popped && RL.overlapWrapped(RL.boxAt(f, C().FIN_BOX), { x: t.x - 10, y: t.y - 10, w: 20, h: 20 }) && f.y < t.y) {
            t.popped = true; t.respawn = 90; this.fx.push({ key: 'fx_pop', x: t.x, y: t.y, t: 0 }); RL.Sfx.pop(); this.score = (this.score || 0) + 1;
          }
          if (t.popped && --t.respawn <= 0) t.popped = false;
        }
      }

      // Swimmer vs swimmer
      if (this.p2) {
        const [a, b] = this.fighters;
        this.checkPop(a, b); this.checkPop(b, a);
        const touching = !a.lost && !b.lost && !a.swallowed && !b.swallowed &&
          RL.overlapWrapped(RL.boxAt(a, C().BODY_BOX), RL.boxAt(b, C().BODY_BOX));
        if (touching && !this.bumped) { this.bump(a, b); if (a.bubbles && b.bubbles) RL.Sfx.bonk(); }
        this.bumped = touching;
      }

      // Charm shots
      for (const s of this.shots) {
        s.x += s.vx; s.life--;
        if (s.x > C().WRAP_MAX) s.x = C().WRAP_MIN; if (s.x < C().WRAP_MIN) s.x = C().WRAP_MAX;
        const foe = this.opponentOf(s.owner);
        if (foe && foe.bubbles > 0 && foe.invincible === 0 &&
            RL.overlapWrapped({ x: s.x - 5, y: s.y - 5, w: 10, h: 10 }, RL.boxAt(foe, C().BUBBLE_BOX))) {
          foe.pop(); s.life = 0; this.fx.push({ key: 'fx_pop', x: s.x, y: s.y, t: 0 });
        }
      }
      this.shots = this.shots.filter(s => s.life > 0);
      this.fx.forEach(e => e.t += 1 / 30);
      this.fx = this.fx.filter(e => !RL.Assets.frameFor(e.key, 'play', e.t).done);

      // End of bout
      if (this.p2 && (this.p1.lost || this.p2.lost)) {
        if (++this.endT > 50 && !this.result) {
          const won = this.p2.lost && !this.p1.lost;
          this.result = { won, livesDiff: this.p1.lives - this.p2.lives, winner: won ? this.p1 : this.p2 };
          won ? RL.Sfx.win() : RL.Sfx.lose();
        }
      }
    }

    checkPop(att, def) {
      if (att.lost || def.lost || att.swallowed || def.swallowed) return;
      if (att.bubbles <= 0 || def.bubbles <= 0 || def.invincible > 0) return;
      if (!(att.y < def.y - C().POP_HEIGHT_MARGIN)) return;
      if (!RL.overlapWrapped(RL.boxAt(att, C().FIN_BOX), RL.boxAt(def, C().BUBBLE_BOX))) return;
      def.pop();
      this.fx.push({ key: 'fx_pop', x: def.x, y: def.y - 26, t: 0 });
      this.bump(att, def);
      att.vy = Math.min(att.vy, -2); // little hop off the bubble
    }

    bump(a, b) {
      const m = C().BUMP_MIN_SEP;
      if (Math.abs(RL.wrapDX(a.x - b.x)) > m) { const t = a.vx; a.vx = b.vx; b.vx = t; }
      if (Math.abs(a.y - b.y) > m) { const t = a.vy; a.vy = b.vy; b.vy = t; }
    }

    draw(ctx) {
      const A = RL.Assets, s = C().RENDER_SCALE;
      A.image(ctx, this.stage.bg, 0, 0);
      for (const t of this.targets) if (!t.popped) A.sprite(ctx, 'bubble', 'wobble', t.t, t.x, t.y + 10, { tint: '#ffd36b' });
      if (this.hazard) this.hazard.draw(ctx);
      A.image(ctx, 'fg_trench', 0, 250 * s);
      for (const f of this.fighters) f.draw(ctx);
      for (const sh of this.shots) A.sprite(ctx, 'fx_sparkle', 'play', this.frame / 30, sh.x, sh.y);
      for (const e of this.fx) A.sprite(ctx, e.key, 'play', e.t, e.x, e.y);
      this.drawHud(ctx);
      if (this.paused) banner(ctx, 'Paused', 'Press P to keep swimming');
    }

    drawHud(ctx) {
      const A = RL.Assets;
      const drawSide = (f, left) => {
        if (!f) return;
        const x0 = left ? 24 : 1200 - 24 - 330, y0 = 900 - 96;
        A.image(ctx, 'hud_glow_frame', x0, y0);
        const pct = Math.max(0, Math.min(1, f.charge / C().CHARGE_MAX));
        A.image(ctx, 'hud_glow_fill', x0 + 12, y0 + 18, { crop: [Math.max(1, Math.round(306 * pct)), 24] });
        const lightX = left ? x0 + 330 + 30 : x0 - 30;
        A.sprite(ctx, 'hud_ready', 'on', 0, lightX / 3, (y0 + 30) / 3, { frame: { row: 0, col: RL.Charms.ready(f) && f.charm !== 'none' ? 1 : 0 } });
        for (let i = 0; i < f.lives; i++) A.image(ctx, 'hud_spare', left ? x0 + i * 36 : x0 + 330 - 30 - i * 36, y0 + 62);
        text(ctx, f.name, left ? x0 : x0 + 330, y0 - 10, 28, left ? 'left' : 'right');
      };
      drawSide(this.p1, true);
      drawSide(this.p2, false);
      if (this.mode === 'practice') text(ctx, `Bubbles popped: ${this.score || 0}   (Esc: back to the reef)`, 600, 50, 30, 'center');
    }
  }

  function makeTargets() {
    return [[80, 120], [200, 80], [320, 140], [140, 200], [270, 210]].map(([x, y], i) =>
      ({ x, y, baseY: y, t: 0, phase: i, popped: false, respawn: 0 }));
  }
  function text(ctx, str, x, y, size, align) {
    ctx.save(); ctx.font = `700 ${size}px ${RL.UI_FONT}`; ctx.textAlign = align || 'left';
    ctx.lineWidth = 6; ctx.strokeStyle = 'rgba(10,40,70,0.85)'; ctx.strokeText(str, x, y);
    ctx.fillStyle = '#fff'; ctx.fillText(str, x, y); ctx.restore();
  }
  function banner(ctx, title, sub) {
    ctx.save(); ctx.fillStyle = 'rgba(5,25,50,0.55)'; ctx.fillRect(0, 330, 1200, 220); ctx.restore();
    text(ctx, title, 600, 430, 72, 'center'); if (sub) text(ctx, sub, 600, 500, 32, 'center');
  }
  const Input = { key: c => RL.Input.key(c) };
  RL.Match = Match; RL.drawText = text; RL.drawBanner = banner;
})();
