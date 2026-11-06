// Keyboard + touch input. Two keyboard players; touch drives player 1.
(function () {
  const down = new Set();
  const pressed = new Set();
  const touch = { left: false, right: false, kick: false, charm: false, kickEdge: false, charmEdge: false };
  let pointer = null; // last tap in canvas pixels, consumed by scenes

  RL.KEYS = {
    1: { left: ['KeyA'], right: ['KeyD'], kick: ['KeyW', 'Space'], charm: ['KeyS'] },
    2: { left: ['ArrowLeft'], right: ['ArrowRight'], kick: ['ArrowUp'], charm: ['ArrowDown'] },
    solo: { left: ['KeyA', 'ArrowLeft'], right: ['KeyD', 'ArrowRight'], kick: ['KeyW', 'Space', 'ArrowUp'], charm: ['KeyS', 'ArrowDown'] },
  };

  addEventListener('keydown', e => {
    if (!down.has(e.code)) pressed.add(e.code);
    down.add(e.code);
    if (['Space', 'ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight'].includes(e.code)) e.preventDefault();
  });
  addEventListener('keyup', e => down.delete(e.code));
  addEventListener('blur', () => down.clear());

  RL.Input = {
    // Returns { dir, kick (edge), charm (held), charmEdge } for a player slot.
    read(slot, useTouch) {
      const k = RL.KEYS[slot];
      const any = codes => codes.some(c => down.has(c));
      const edge = codes => codes.some(c => pressed.has(c));
      let dir = 0;
      if (any(k.left) || (useTouch && touch.left)) dir -= 1;
      if (any(k.right) || (useTouch && touch.right)) dir += 1;
      return {
        dir,
        kick: edge(k.kick) || (useTouch && touch.kickEdge),
        charm: any(k.charm) || (useTouch && touch.charm),
        charmEdge: edge(k.charm) || (useTouch && touch.charmEdge),
      };
    },
    key(code) { return pressed.has(code); },
    anyKey() { return pressed.size > 0; },
    tap() { const p = pointer; return p; },
    endFrame() { pressed.clear(); touch.kickEdge = false; touch.charmEdge = false; pointer = null; },

    bindTouch(canvas, padEl) {
      const toCanvas = e => {
        const r = canvas.getBoundingClientRect();
        return { x: (e.clientX - r.left) * canvas.width / r.width, y: (e.clientY - r.top) * canvas.height / r.height };
      };
      canvas.addEventListener('pointerdown', e => { pointer = toCanvas(e); });
      if (!padEl) return;
      padEl.querySelectorAll('[data-pad]').forEach(btn => {
        const k = btn.dataset.pad;
        const on = e => { e.preventDefault(); if (!touch[k]) { if (k === 'kick') touch.kickEdge = true; if (k === 'charm') touch.charmEdge = true; } touch[k] = true; btn.classList.add('on'); };
        const off = e => { e.preventDefault(); touch[k] = false; btn.classList.remove('on'); };
        btn.addEventListener('pointerdown', on);
        btn.addEventListener('pointerup', off);
        btn.addEventListener('pointercancel', off);
        btn.addEventListener('pointerleave', off);
      });
    },
  };
})();
