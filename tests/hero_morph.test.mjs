import { test, describe } from 'node:test';
import assert from 'node:assert/strict';

// Seam under test: computeHeroMorphState
export function computeHeroMorphState(progress, transitionEnd = 0.12) {
  const rawT = Math.min(1.0, Math.max(0.0, progress / transitionEnd));
  // cubic easeInOut
  const t = rawT < 0.5 ? 4.0 * rawT * rawT * rawT : 1.0 - Math.pow(-2.0 * rawT + 2.0, 3.0) / 2.0;

  return {
    rawT,
    t,
    taglineOpacity: Math.max(0.0, 1.0 - rawT * 1.6),
    taglineTranslateY: rawT * 24, // px downward drift
    navbarOpacity: Math.min(1.0, Math.max(0.0, (rawT - 0.25) / 0.75)),
    isDocked: rawT >= 1.0
  };
}

describe('Hero Morph State Machine', () => {
  test('at scroll 0: hero tagline is 100% visible, navbar is invisible, not docked', () => {
    const state = computeHeroMorphState(0.0);
    assert.equal(state.rawT, 0.0);
    assert.equal(state.t, 0.0);
    assert.equal(state.taglineOpacity, 1.0);
    assert.equal(state.navbarOpacity, 0.0);
    assert.equal(state.isDocked, false);
  });

  test('at midpoint (progress 0.06): tagline fading, navbar fading in, smoothly interpolated', () => {
    const state = computeHeroMorphState(0.06);
    assert.ok(state.rawT > 0.49 && state.rawT < 0.51);
    assert.ok(state.taglineOpacity < 0.5);
    assert.ok(state.navbarOpacity > 0.2 && state.navbarOpacity < 0.5);
    assert.equal(state.isDocked, false);
  });

  test('at scroll >= 0.12: hero is docked, navbar is 100% visible, tagline is completely hidden', () => {
    const state = computeHeroMorphState(0.12);
    assert.equal(state.rawT, 1.0);
    assert.equal(state.t, 1.0);
    assert.equal(state.taglineOpacity, 0.0);
    assert.equal(state.navbarOpacity, 1.0);
    assert.equal(state.isDocked, true);
  });

  test('beyond scroll 0.12 (e.g. 0.50 inside banquet hall): state remains pinned at docked', () => {
    const state = computeHeroMorphState(0.50);
    assert.equal(state.rawT, 1.0);
    assert.equal(state.t, 1.0);
    assert.equal(state.navbarOpacity, 1.0);
    assert.equal(state.isDocked, true);
  });
});
