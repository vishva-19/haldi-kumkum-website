/**
 * ScrollyPlayer: Deep scrollytelling player module.
 *
 * Encapsulates:
 * - FrameBuffer: Keyframe-priority preloading, background progressive streaming,
 *   and zero-blank-frame nearest-neighbor recovery.
 * - ViewportRasterizer: DPR-aware Retina rasterization and aspect-ratio cover projection.
 * - InertiaEngine: Unified wheel/touch/scroll/keyboard input physics with 60fps lerp damping.
 */
(function (global) {
  'use strict';

  class FrameBuffer {
    constructor(totalFrames, frameUrlFn) {
      this.totalFrames = totalFrames;
      this.frameUrlFn = frameUrlFn;
      this.cache = new Array(totalFrames);
      this.loadedIndices = new Set();
      this.loadCursor = 1;
      this._streamingTimer = null;
    }

    loadFrame(idx, onLoaded) {
      if (idx < 0 || idx >= this.totalFrames || this.cache[idx]) return;

      const img = new Image();
      img.src = this.frameUrlFn(idx);
      img.onload = () => {
        this.cache[idx] = img;
        this.loadedIndices.add(idx);
        if (onLoaded) onLoaded(img, idx);
      };
    }

    startProgressiveStream(keyframeStep = 8, chunkSize = 12, chunkIntervalMs = 30) {
      // 1. Keyframe priority landmarks across the timeline
      for (let i = 0; i < this.totalFrames; i += keyframeStep) {
        this.loadFrame(i);
      }

      // 2. Progressive background chunk streamer
      const streamChunks = () => {
        let scheduled = 0;
        while (this.loadCursor < this.totalFrames && scheduled < chunkSize) {
          if (!this.cache[this.loadCursor]) {
            this.loadFrame(this.loadCursor);
            scheduled++;
          }
          this.loadCursor++;
        }
        if (this.loadCursor < this.totalFrames) {
          this._streamingTimer = setTimeout(streamChunks, chunkIntervalMs);
        }
      };

      setTimeout(streamChunks, 60);
    }

    getNearestFrame(targetIdx) {
      if (this.loadedIndices.has(targetIdx)) return this.cache[targetIdx];
      if (this.loadedIndices.size === 0) return null;

      for (let offset = 1; offset < this.totalFrames; offset++) {
        const down = targetIdx - offset;
        if (down >= 0 && this.loadedIndices.has(down)) return this.cache[down];
        const up = targetIdx + offset;
        if (up < this.totalFrames && this.loadedIndices.has(up)) return this.cache[up];
      }
      return null;
    }

    destroy() {
      if (this._streamingTimer) clearTimeout(this._streamingTimer);
      this.cache = [];
      this.loadedIndices.clear();
    }
  }

  class ViewportRasterizer {
    constructor(canvas) {
      this.canvas = canvas;
      this.ctx = canvas.getContext('2d', { alpha: false });
      this.dpr = Math.min(window.devicePixelRatio || 1, 2.0);
    }

    resize(width, height) {
      this.dpr = Math.min(window.devicePixelRatio || 1, 2.0);
      this.canvas.width = Math.round(width * this.dpr);
      this.canvas.height = Math.round(height * this.dpr);
      this.canvas.style.width = width + 'px';
      this.canvas.style.height = height + 'px';
    }

    renderCover(img) {
      if (!img || !img.complete || img.naturalWidth === 0) return;

      const cw = this.canvas.width;
      const ch = this.canvas.height;
      const iw = img.naturalWidth;
      const ih = img.naturalHeight;

      const scale = Math.max(cw / iw, ch / ih);
      const sw = iw * scale;
      const sh = ih * scale;
      const sx = (cw - sw) * 0.5;
      const sy = (ch - sh) * 0.5;

      this.ctx.drawImage(img, sx, sy, sw, sh);
    }
  }

  class InertiaEngine {
    constructor(options) {
      this.scrollContainer = options.scrollContainer;
      this.progressTrack = options.progressTrack;
      this.scrollHint = options.scrollHint;
      this.lerpDamping = options.lerpDamping || 0.088;
      this.autoFlightSpeed = options.autoFlightSpeed || 0.0016;

      this.maxScroll = 1;
      this.targetScrollY = 0;
      this.currentScrollY = 0;
      this.scrollProgress = 0;
      this.hasScrolled = false;
      this.isAutoFlying = false;

      this._touchY = 0;
      this._boundListeners = [];
    }

    init(onUserScrolled) {
      this.onUserScrolled = onUserScrolled;
      this.updateBounds();

      const addEvt = (target, type, fn, opts = { passive: true }) => {
        target.addEventListener(type, fn, opts);
        this._boundListeners.push({ target, type, fn });
      };

      // Native Window Scroll
      addEvt(window, 'scroll', () => {
        if (!this.isAutoFlying) {
          this.targetScrollY = window.scrollY;
          this._checkDismissHint();
        }
      });

      // Trackpad / Mouse Wheel
      addEvt(window, 'wheel', (e) => {
        if (this.isAutoFlying) this.stopAutoFlight();
        this.targetScrollY = Math.max(0, Math.min(this.maxScroll, this.targetScrollY + e.deltaY * 1.12));
        this._checkDismissHint();
      });

      // Mobile Touch
      addEvt(window, 'touchstart', (e) => {
        if (this.isAutoFlying) this.stopAutoFlight();
        if (e.touches.length === 1) this._touchY = e.touches[0].clientY;
      });

      addEvt(window, 'touchmove', (e) => {
        if (e.touches.length === 1) {
          const delta = (this._touchY - e.touches[0].clientY) * 1.5;
          this._touchY = e.touches[0].clientY;
          this.targetScrollY = Math.max(0, Math.min(this.maxScroll, this.targetScrollY + delta));
          this._checkDismissHint();
        }
      });

      // Keyboard Controls
      addEvt(window, 'keydown', (e) => {
        if (e.key === ' ') {
          e.preventDefault();
          this.toggleAutoFlight();
        } else if (e.key === 'ArrowDown' || e.key === 'PageDown') {
          if (this.isAutoFlying) this.stopAutoFlight();
          this.targetScrollY = Math.min(this.maxScroll, this.targetScrollY + window.innerHeight * 0.35);
          this._checkDismissHint();
        } else if (e.key === 'ArrowUp' || e.key === 'PageUp') {
          if (this.isAutoFlying) this.stopAutoFlight();
          this.targetScrollY = Math.max(0, this.targetScrollY - window.innerHeight * 0.35);
          this._checkDismissHint();
        } else if (e.key === 'Home') {
          if (this.isAutoFlying) this.stopAutoFlight();
          this.targetScrollY = 0;
          this._checkDismissHint();
        } else if (e.key === 'End') {
          if (this.isAutoFlying) this.stopAutoFlight();
          this.targetScrollY = this.maxScroll;
          this._checkDismissHint();
        }
      }, { passive: false });
    }

    _checkDismissHint() {
      if (!this.hasScrolled && this.targetScrollY > 15) {
        this.hasScrolled = true;
        if (this.scrollHint) this.scrollHint.style.opacity = '0';
      }
    }

    updateBounds() {
      const containerH = this.scrollContainer ? this.scrollContainer.offsetHeight : window.innerHeight * 10;
      this.maxScroll = Math.max(1, containerH - window.innerHeight);
    }

    tick() {
      if (this.isAutoFlying) {
        this.targetScrollY += this.autoFlightSpeed * this.maxScroll;
        if (this.targetScrollY >= this.maxScroll) {
          this.targetScrollY = this.maxScroll;
          this.stopAutoFlight();
        }
      }

      // Smooth lerp physics
      this.currentScrollY += (this.targetScrollY - this.currentScrollY) * this.lerpDamping;
      this.scrollProgress = Math.max(0, Math.min(1, this.currentScrollY / this.maxScroll));

      // Sync native scroll offset
      if (Math.abs(window.scrollY - this.currentScrollY) > 2) {
        window.scrollTo(0, this.currentScrollY);
      }

      // Update progress bar
      if (this.progressTrack) {
        this.progressTrack.style.width = (this.scrollProgress * 100).toFixed(2) + '%';
      }

      return this.scrollProgress;
    }

    startAutoFlight() {
      this.isAutoFlying = true;
      if (this.scrollHint) this.scrollHint.style.opacity = '0';
      if (this.scrollProgress >= 0.99) {
        this.targetScrollY = this.currentScrollY = 0;
      }
    }

    stopAutoFlight() {
      this.isAutoFlying = false;
    }

    toggleAutoFlight() {
      if (this.isAutoFlying) this.stopAutoFlight();
      else this.startAutoFlight();
    }

    destroy() {
      this._boundListeners.forEach(({ target, type, fn }) => target.removeEventListener(type, fn));
      this._boundListeners = [];
    }
  }

  class ScrollyPlayer {
    constructor(canvasElem, options = {}) {
      this.canvas = typeof canvasElem === 'string' ? document.querySelector(canvasElem) : canvasElem;
      if (!this.canvas) throw new Error('ScrollyPlayer: target canvas not found');

      const totalFrames = options.totalFrames || 600;
      const frameUrlFn = options.frameUrl || ((idx) => `frames_webp/frame_${String(idx).padStart(4, '0')}.webp?v=6`);

      this.totalFrames = totalFrames;
      this.buffer = new FrameBuffer(totalFrames, frameUrlFn);
      this.rasterizer = new ViewportRasterizer(this.canvas);
      this.inertia = new InertiaEngine({
        scrollContainer: typeof options.scrollContainer === 'string' ? document.querySelector(options.scrollContainer) : options.scrollContainer,
        progressTrack: typeof options.progressTrack === 'string' ? document.querySelector(options.progressTrack) : options.progressTrack,
        scrollHint: typeof options.scrollHint === 'string' ? document.querySelector(options.scrollHint) : options.scrollHint,
        lerpDamping: options.lerpDamping || 0.088,
        autoFlightSpeed: options.autoFlightSpeed || 0.0016
      });

      this.onProgress = options.onProgress || null;
      this._lastRenderedIdx = -1;
      this._animFrameId = null;
      this._resizeHandler = this._onResize.bind(this);

      this._init();
    }

    _init() {
      // 1. Initial sizing
      this._onResize();
      window.addEventListener('resize', this._resizeHandler, { passive: true });

      // 2. Initialize inputs
      this.inertia.init();

      // 3. Render frame 0 immediately as soon as it arrives
      this.buffer.loadFrame(0, (img) => {
        if (this._lastRenderedIdx === -1) {
          this.rasterizer.renderCover(img);
          this._lastRenderedIdx = 0;
        }
      });

      // 4. Start progressive background frame preloading
      this.buffer.startProgressiveStream();

      // 5. Start main 60fps render loop
      this._loop = this._loop.bind(this);
      this._animFrameId = requestAnimationFrame(this._loop);
    }

    _onResize() {
      const w = window.innerWidth;
      const h = window.innerHeight;
      this.rasterizer.resize(w, h);
      this.inertia.updateBounds();

      // Re-draw current frame after resize
      if (this._lastRenderedIdx >= 0) {
        const frameImg = this.buffer.getNearestFrame(this._lastRenderedIdx);
        if (frameImg) this.rasterizer.renderCover(frameImg);
      }
    }

    _loop() {
      const progress = this.inertia.tick();
      if (this.onProgress) {
        this.onProgress(progress);
      }
      const targetIdx = Math.min(this.totalFrames - 1, Math.floor(progress * this.totalFrames));

      if (targetIdx !== this._lastRenderedIdx) {
        const frameImg = this.buffer.getNearestFrame(targetIdx);
        if (frameImg) {
          this.rasterizer.renderCover(frameImg);
          this._lastRenderedIdx = targetIdx;
        }
      }

      this._animFrameId = requestAnimationFrame(this._loop);
    }

    startAutoFlight() {
      this.inertia.startAutoFlight();
    }

    stopAutoFlight() {
      this.inertia.stopAutoFlight();
    }

    toggleAutoFlight() {
      this.inertia.toggleAutoFlight();
    }

    destroy() {
      if (this._animFrameId) cancelAnimationFrame(this._animFrameId);
      window.removeEventListener('resize', this._resizeHandler);
      this.buffer.destroy();
      this.inertia.destroy();
    }

    static mount(selector, options) {
      return new ScrollyPlayer(selector, options);
    }
  }

  global.ScrollyPlayer = ScrollyPlayer;
})(window);
