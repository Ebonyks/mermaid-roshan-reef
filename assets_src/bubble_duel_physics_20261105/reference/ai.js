// CPU swimmer. Written fresh around the priority idea in docs/STUDY_NOTES.md:
// stay off the bottom, don't let the rival get above you, and drop onto the rival from above.
(function () {
  class Brain {
    constructor(skill, reflex) {
      this.skill = skill; this.reflex = reflex;
      this.hist = [];      // recent rival positions, newest first
      this.plan = { dir: 0, kick: false, charmEdge: false, charm: false };
    }
    roll(p) { return Math.random() * 100 < p; }

    think(me, foe, world) {
      const out = { dir: me.dir, kick: false, charm: false, charmEdge: false };
      if (!foe || foe.lost) return out;
      this.hist.unshift({ x: foe.x, y: foe.y });
      if (this.hist.length > 10) this.hist.pop();
      // React only some frames: lower reflex = slower to notice things
      if (!this.roll(this.reflex * 1.25)) return out;

      const dx = RL.wrapDX(foe.x - me.x);           // + means rival is to my right
      const toward = Math.sign(dx) || 1;
      const old = this.hist[this.hist.length - 1];
      const fvx = old ? RL.wrapDX(foe.x - old.x) / this.hist.length : foe.vx;
      const fvy = old ? (foe.y - old.y) / this.hist.length : foe.vy;
      const aboveRival = me.y < foe.y - 12;
      const myFuture = me.y + me.vy * 18;
      const grum = world.hazard;
      const s = this.skill;

      const kickToward = d => { out.kick = true; out.dir = d; };
      const nearCap = d => d > 0 ? me.vx > me.maxVX * 0.85 : me.vx < -me.maxVX * 0.85;

      // 1. Never sink into the trench
      if (myFuture > 250 || (grum && Math.abs(RL.wrapDX(grum.x - me.x)) < 90 && me.y > 210)) {
        if (this.roll(40 + s / 2)) kickToward(0);
        return out;
      }
      // 2. Rival will soon be above me and close: get up and away
      const t = 12;
      const relYsoon = (foe.y + fvy * t) - (me.y + me.vy * t);
      const relXsoon = RL.wrapDX((foe.x + fvx * t) - (me.x + me.vx * t));
      if (relYsoon < -8 && Math.abs(relXsoon) < 40 && this.roll(s * 0.9)) {
        kickToward(-toward);
        return out;
      }
      // 3. Below the rival: climb, drifting toward them
      if (!aboveRival) {
        if (me.vy > -1.5 && this.roll(30 + s / 2)) kickToward(nearCap(toward) ? 0 : toward);
        return out;
      }
      // 4. Above the rival: line up horizontally and fall onto their bubbles
      if (Math.abs(dx) > 14 && !nearCap(toward) && this.roll(s * 0.6)) {
        // small sideways nudge; skip if it would lift us too far above
        if (foe.y - me.y < 70 || this.roll(30)) kickToward(toward);
      }
      // 5. Use the charm sometimes when it's ready and the rival is close
      if (RL.Charms.ready(me) && me.charm !== 'none' && Math.abs(dx) < 120 && this.roll(s / 8)) out.charmEdge = true;
      if (me.charm === 'pearl') out.charm = me.y > 200;
      return out;
    }
  }
  RL.Brain = Brain;
})();
