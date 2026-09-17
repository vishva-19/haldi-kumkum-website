/**
 * HeroMorphController: Handles the luxury morph transition connecting
 * Page 1 (Centered Sky Hero Branding) to Page 2 (Floating Luxury Navigation Bar).
 */
(function (global) {
  'use strict';

  function cubicEaseInOut(t) {
    return t < 0.5 ? 4.0 * t * t * t : 1.0 - Math.pow(-2.0 * t + 2.0, 3.0) / 2.0;
  }

  class HeroMorphController {
    constructor(options = {}) {
      this.logoEl = typeof options.logo === 'string' ? document.querySelector(options.logo) : options.logo;
      this.taglineEl = typeof options.tagline === 'string' ? document.querySelector(options.tagline) : options.tagline;
      this.navbarEl = typeof options.navbar === 'string' ? document.querySelector(options.navbar) : options.navbar;
      this.navSlotEl = typeof options.navSlot === 'string' ? document.querySelector(options.navSlot) : options.navSlot;
      this.transitionEnd = options.transitionEnd || 0.14;

      this.aspectRatio = 1024.0 / 681.0; // Logo aspect ratio
      this._lastProgress = -1;
      this._resizeHandler = this.updateLayout.bind(this);

      this.init();
    }

    init() {
      if (!this.logoEl || !this.taglineEl || !this.navbarEl || !this.navSlotEl) {
        console.warn('HeroMorphController: Required elements missing');
        return;
      }

      window.addEventListener('resize', this._resizeHandler, { passive: true });
      this.updateLayout();
      this.update(0.0);
    }

    updateLayout() {
      // Re-evaluate on next update
      this._lastProgress = -1;
      if (this._currentProgress !== undefined) {
        this.update(this._currentProgress);
      }
    }

    update(progress) {
      this._currentProgress = progress;
      const rawT = Math.min(1.0, Math.max(0.0, progress / this.transitionEnd));

      if (Math.abs(progress - this._lastProgress) < 0.0001 && rawT !== 0 && rawT !== 1) {
        return;
      }
      this._lastProgress = progress;

      const t = cubicEaseInOut(rawT);
      const vw = window.innerWidth;
      const vh = window.innerHeight;

      // 1. Initial State (Center of Sky in Page 1)
      const isMobile = vw < 768;
      const startW = Math.min(isMobile ? 290 : 380, vw * 0.72);
      const startH = startW / this.aspectRatio;
      const startX = (vw - startW) * 0.5;
      const startY = Math.max(40, vh * 0.28 - startH * 0.5);

      // 2. Target Docked State (Inside Navbar Slot in Page 2)
      const slotRect = this.navSlotEl.getBoundingClientRect();
      // Visible, beautifully proportioned logo size for navbar: height 48px on desktop / 36px on mobile
      const targetH = isMobile ? 36 : 48;
      const targetW = targetH * this.aspectRatio;
      const targetX = slotRect.left > 0 ? slotRect.left : (isMobile ? 16 : 36);
      const targetY = slotRect.top + (slotRect.height - targetH) * 0.5;

      // 3. Interpolate Position & Size
      const curX = startX + (targetX - startX) * t;
      const curY = startY + (targetY - startY) * t;
      const curW = startW + (targetW - startW) * t;
      const curH = curW / this.aspectRatio;

      this.logoEl.style.width = curW.toFixed(1) + 'px';
      this.logoEl.style.height = curH.toFixed(1) + 'px';
      this.logoEl.style.transform = `translate3d(${curX.toFixed(1)}px, ${curY.toFixed(1)}px, 0)`;

      // 4. Tagline Fade & Drift
      const taglineOpacity = Math.max(0.0, 1.0 - rawT * 1.8);
      const taglineDrift = rawT * 26.0;
      this.taglineEl.style.opacity = taglineOpacity.toFixed(3);
      this.taglineEl.style.transform = `translate3d(-50%, ${taglineDrift.toFixed(1)}px, 0)`;
      this.taglineEl.style.pointerEvents = taglineOpacity > 0.05 ? 'auto' : 'none';

      // 5. Navbar Background & Links Fade-In
      const navOpacity = Math.min(1.0, Math.max(0.0, (rawT - 0.20) / 0.80));
      this.navbarEl.style.opacity = navOpacity.toFixed(3);
      this.navbarEl.style.pointerEvents = rawT >= 0.85 ? 'auto' : 'none';
    }

    destroy() {
      window.removeEventListener('resize', this._resizeHandler);
    }

    static mount(options) {
      return new HeroMorphController(options);
    }
  }

  global.HeroMorphController = HeroMorphController;
})(window);
