/* Interface fixture only. No song chart, drum part, reward or save state. */
(function (root) {
  'use strict';
  class RhythmFixture {
    constructor() { this.reset(); }
    reset() {
      this.time = 0; this.arrival = 3.2; this.target = 0; this.index = 0;
      this.running = false; this.held = null; this.hit = false; this.feedbackUntil = -1;
      this.hits = 0; this.passed = 0; this.window = 0.35;
    }
    start() { this.running = true; }
    pause() { this.running = false; this.held = null; }
    resume() {
      // A returning child always sees a fresh approach, never an immediate deadline.
      this.arrival = Math.max(this.arrival, this.time + 1.6);
      this.running = true;
    }
    advance(seconds) {
      if (!this.running || !Number.isFinite(seconds) || seconds <= 0) return;
      this.time += seconds;
      while (this.time > this.arrival + 0.8) {
        if (!this.hit) this.passed++;
        this.index++; this.target = this.index % 3; this.arrival += 4;
        this.hit = false;
      }
    }
    press(target, pointer) {
      if (!this.running || this.held !== null) return 'ignored';
      this.held = pointer;
      if (this.hit || target !== this.target) return 'neutral';
      if (Math.abs(this.time - this.arrival) > this.window) return 'neutral';
      this.hit = true; this.hits++; this.feedbackUntil = this.time + 0.65;
      return 'contact';
    }
    release(pointer) { if (this.held === pointer) this.held = null; }
    cancel() { this.held = null; }
    cue() {
      const remaining = this.arrival - this.time;
      return { target: this.target, remaining, hit: this.hit,
        visible: !this.hit && remaining <= 3.2 && remaining >= -0.35,
        progress: Math.max(0, Math.min(1.11, 1 - remaining / 3.2)),
        feedback: this.time < this.feedbackUntil };
    }
  }
  if (typeof module !== 'undefined' && module.exports) module.exports = RhythmFixture;
  else root.RhythmFixture = RhythmFixture;
})(typeof window !== 'undefined' ? window : globalThis);
