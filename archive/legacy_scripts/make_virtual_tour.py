import os

html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>The Royal Palace Resort</title>
  <style>
    /* =========================================================================
       BASE & RESET - LUXURY ARCHITECTURAL EXPERIENCE
       ========================================================================= */
    *, *::before, *::after {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
    }

    html, body {
      width: 100%;
      height: 100%;
      background-color: #0c0a09;
      color: #f7f4ee;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      overflow-x: hidden;
      overscroll-behavior: none;
      user-select: none;
      -webkit-user-select: none;
    }

    /* VIRTUAL SCROLL CONTAINER (850vh FOR SMOOTH VIRTUAL TOUR PACING) */
    .scroll-container {
      width: 100%;
      height: 850vh;
      position: relative;
      pointer-events: none;
    }

    /* FIXED 100VH CINEMATIC VIEWPORT */
    .tour-viewport {
      position: fixed;
      inset: 0;
      width: 100vw;
      height: 100vh;
      height: 100dvh;
      overflow: hidden;
      background: #0c0a09;
      perspective: 1200px;
      perspective-origin: 50% 50%;
    }

    /* 3D CAMERA RIG */
    .camera-rig {
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      transform-style: preserve-3d;
      will-change: transform;
    }

    /* SCENE LAYERS */
    .tour-scene {
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      display: flex;
      align-items: center;
      justify-content: center;
      pointer-events: none;
      will-change: transform, opacity;
      transform-style: preserve-3d;
    }

    /* ASPECT-LOCKED MEDIA FRAME */
    /* Keeps high-res photography razor-sharp and locked on all screen sizes */
    .media-frame {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      will-change: transform, opacity;
      transform-style: preserve-3d;
    }

    .media-frame img.tour-img {
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
      pointer-events: none;
    }

    /* =========================================================================
       SCENE 1 & 2: MASTER PALACE FACADE (main1 + main2 continuous master)
       Dimensions: 1376 x 1080
       ========================================================================= */
    #scene-facade {
      opacity: 1;
      z-index: 2;
    }

    /* 3D ENTRANCE DOORWAY PORTAL */
    /* In facade_master (1376x1080):
       Doors at x: 648 to 728 (47.09% to 52.90% of width, w = 5.81%)
       Doors at y: 806 to 892 (74.63% to 82.59% of height, h = 7.96%)
    */
    .doorway-portal {
      position: absolute;
      top: 74.63%;
      left: 47.09%;
      width: 5.81%;
      height: 7.96%;
      perspective: 900px;
      transform-style: preserve-3d;
      z-index: 5;
      pointer-events: none;
    }

    /* Warm illuminated reception hall interior behind open doors */
    .reception-interior {
      position: absolute;
      inset: 0;
      background: radial-gradient(ellipse at 50% 40%, rgba(255, 220, 150, 0.98) 0%, rgba(220, 160, 70, 0.90) 50%, rgba(55, 30, 15, 0.98) 100%);
      box-shadow: 0 0 25px rgba(255, 215, 140, 0.85);
      border-radius: 2px;
      overflow: hidden;
      opacity: 0;
      will-change: opacity, transform;
    }

    .reception-interior img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      opacity: 0.85;
    }

    .reception-interior::after {
      content: '';
      position: absolute;
      inset: 0;
      background: linear-gradient(to top, rgba(30, 20, 12, 0.85) 0%, transparent 65%);
    }

    /* 3D DOOR LEAVES */
    .door-leaf {
      position: absolute;
      top: 0;
      width: 50%;
      height: 100%;
      background-size: cover;
      background-position: center;
      transform-style: preserve-3d;
      will-change: transform;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.45);
    }

    .door-leaf.left {
      left: 0;
      transform-origin: left center;
      background-image: url('img/door_left.png');
    }

    .door-leaf.right {
      right: 0;
      transform-origin: right center;
      background-image: url('img/door_right.png');
    }

    /* RIGHT ARCHWAY WINDOW PORTAL */
    /* In facade_master:
       Window at x: 770 to 840 (55.96% to 61.05%, w = 5.09%)
       Window at y: 792 to 892 (73.33% to 82.59%, h = 9.26%)
    */
    .window-portal {
      position: absolute;
      top: 73.33%;
      left: 55.96%;
      width: 5.09%;
      height: 9.26%;
      z-index: 6;
      perspective: 1000px;
      transform-style: preserve-3d;
      pointer-events: none;
      overflow: visible;
    }

    /* SEMI-TRANSPARENT PASTEL SHEER CURTAINS */
    .curtain-drape {
      position: absolute;
      top: -4%;
      width: 65%;
      height: 108%;
      background-size: 100% 100%;
      background-repeat: no-repeat;
      will-change: transform, opacity;
      pointer-events: none;
    }

    .curtain-drape.left {
      left: 0;
      background-image: url('img/curtain_left.png');
      transform-origin: left top;
    }

    .curtain-drape.right {
      right: 0;
      background-image: url('img/curtain_right.png');
      transform-origin: right top;
    }

    .window-glow {
      position: absolute;
      inset: -35%;
      background: radial-gradient(ellipse at 50% 50%, rgba(255, 238, 205, 0.75) 0%, rgba(255, 220, 160, 0.35) 50%, transparent 75%);
      opacity: 0;
      pointer-events: none;
      mix-blend-mode: screen;
    }

    /* =========================================================================
       SUBSEQUENT SCENES: BANQUET HALLS & WEDDING MANDAP
       ========================================================================= */
    #scene-banq1 {
      opacity: 0;
      z-index: 3;
    }

    #scene-banq2 {
      opacity: 0;
      z-index: 4;
    }

    #scene-banq3 {
      opacity: 0;
      z-index: 5;
    }

    #scene-banq4 {
      opacity: 0;
      z-index: 6;
    }

    /* AMBIENT LIVING PARTICLES (Pastel Rose & Champagne Petals) */
    #particles-canvas {
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      pointer-events: none;
      z-index: 15;
    }

    /* CINEMATIC OPTICAL VIGNETTE (Warm, soft, no blur) */
    .cinema-vignette {
      position: absolute;
      inset: 0;
      pointer-events: none;
      z-index: 12;
      background: radial-gradient(circle at 50% 50%, transparent 68%, rgba(12, 10, 9, 0.42) 100%);
    }

    /* MINIMAL TOUR PROGRESS LINE */
    .tour-progress-track {
      position: fixed;
      bottom: 0;
      left: 0;
      width: 100%;
      height: 3px;
      background: rgba(255, 245, 235, 0.08);
      z-index: 50;
      pointer-events: none;
    }

    .tour-progress-fill {
      height: 100%;
      width: 0%;
      background: linear-gradient(90deg, #d8baa1 0%, #f4e8db 50%, #e2c2a9 100%);
      box-shadow: 0 0 8px rgba(230, 200, 175, 0.6);
      will-change: width;
    }

    /* SCROLL HINT (Subtle line at bottom, fades on first scroll) */
    .scroll-hint {
      position: fixed;
      bottom: 28px;
      left: 50%;
      transform: translateX(-50%);
      z-index: 40;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 8px;
      pointer-events: none;
      transition: opacity 0.6s ease;
    }

    .scroll-hint-line {
      width: 1px;
      height: 28px;
      background: linear-gradient(to bottom, rgba(245, 235, 220, 0.85), transparent);
      animation: scroll-bob 2.2s infinite ease-in-out;
    }

    @keyframes scroll-bob {
      0% { transform: scaleY(0); transform-origin: top; }
      50% { transform: scaleY(1); transform-origin: top; }
      50.1% { transform: scaleY(1); transform-origin: bottom; }
      100% { transform: scaleY(0); transform-origin: bottom; }
    }
  </style>
</head>
<body>

  <!-- VIRTUAL SCROLL CONTAINER -->
  <div class="scroll-container" id="scroll-container"></div>

  <!-- FIXED CINEMATIC VIEWPORT -->
  <main class="tour-viewport" id="tour-viewport">

    <div class="camera-rig" id="camera-rig">

      <!-- ================= SCENE 1 & 2: PALACE MASTER FACADE ================= -->
      <!-- Starts high on cupola/sky (main1), descends into courtyard (main2),
           doors swing open to show reception, then camera pans to right window -->
      <section class="tour-scene" id="scene-facade">
        <div class="media-frame" id="frame-facade">
          <img class="tour-img" src="img/facade_master.jpg" alt="The Royal Palace Facade" id="img-facade" />

          <!-- 3D ENTRANCE DOORWAY -->
          <div class="doorway-portal" id="doorway-portal">
            <div class="reception-interior" id="reception-interior">
              <img src="img/reception_lobby.jpg" alt="Palace Reception Interior" />
            </div>
            <div class="door-leaf left" id="door-left"></div>
            <div class="door-leaf right" id="door-right"></div>
          </div>

          <!-- BIG WINDOW & TRANSLUCENT PASTEL CURTAINS -->
          <div class="window-portal" id="window-portal">
            <div class="window-glow" id="window-glow"></div>
            <div class="curtain-drape left" id="curtain-left"></div>
            <div class="curtain-drape right" id="curtain-right"></div>
          </div>
        </div>
      </section>

      <!-- ================= SCENE 3: BANQUET ARRIVAL WALKWAY (banq1.jpg) ================= -->
      <section class="tour-scene" id="scene-banq1">
        <div class="media-frame" id="frame-banq1">
          <img class="tour-img" src="img/banq1.jpg" alt="Floral Arrival Walkway with Royal Elephants" id="img-banq1" />
        </div>
      </section>

      <!-- ================= SCENE 4: GRAND CRYSTAL BALLROOM (banq2.jpg) ================= -->
      <section class="tour-scene" id="scene-banq2">
        <div class="media-frame" id="frame-banq2">
          <img class="tour-img" src="img/banq2.jpg" alt="Grand Ballroom Chandelier View" id="img-banq2" />
        </div>
      </section>

      <!-- ================= SCENE 5: IMPERIAL CENTER AISLE (banq3.jpg) ================= -->
      <section class="tour-scene" id="scene-banq3">
        <div class="media-frame" id="frame-banq3">
          <img class="tour-img" src="img/banq3.jpg" alt="Ballroom Center Aisle Push" id="img-banq3" />
        </div>
      </section>

      <!-- ================= SCENE 6: ROYAL WEDDING MANDAP (banq4.jpg) ================= -->
      <section class="tour-scene" id="scene-banq4">
        <div class="media-frame" id="frame-banq4">
          <img class="tour-img" src="img/banq4.jpg" alt="Royal Wedding Mandap and Floral Pillars" id="img-banq4" />
        </div>
      </section>

    </div><!-- /.camera-rig -->

    <!-- AMBIENT LIVING PARTICLES -->
    <canvas id="particles-canvas"></canvas>

    <!-- CINEMA OPTICAL VIGNETTE -->
    <div class="cinema-vignette"></div>

    <!-- SUBTLE SCROLL HINT -->
    <div class="scroll-hint" id="scroll-hint">
      <div class="scroll-hint-line"></div>
    </div>

    <!-- TOUR TIMELINE PROGRESS BAR -->
    <div class="tour-progress-track">
      <div class="tour-progress-fill" id="tour-progress-fill"></div>
    </div>

  </main>

  <script>
    (function () {
      'use strict';

      // Elements
      const scrollContainer = document.getElementById('scroll-container');
      const progressFill = document.getElementById('tour-progress-fill');
      const scrollHint = document.getElementById('scroll-hint');
      const cameraRig = document.getElementById('camera-rig');

      const sceneFacade = document.getElementById('scene-facade');
      const frameFacade = document.getElementById('frame-facade');
      const doorwayPortal = document.getElementById('doorway-portal');
      const receptionInterior = document.getElementById('reception-interior');
      const doorLeft = document.getElementById('door-left');
      const doorRight = document.getElementById('door-right');
      const windowPortal = document.getElementById('window-portal');
      const windowGlow = document.getElementById('window-glow');
      const curtainLeft = document.getElementById('curtain-left');
      const curtainRight = document.getElementById('curtain-right');

      const sceneBanq1 = document.getElementById('scene-banq1');
      const frameBanq1 = document.getElementById('frame-banq1');
      const sceneBanq2 = document.getElementById('scene-banq2');
      const frameBanq2 = document.getElementById('frame-banq2');
      const sceneBanq3 = document.getElementById('scene-banq3');
      const frameBanq3 = document.getElementById('frame-banq3');
      const sceneBanq4 = document.getElementById('scene-banq4');
      const frameBanq4 = document.getElementById('frame-banq4');

      // Scroll State
      let maxScroll = 1;
      let targetScrollY = 0;
      let currentScrollY = 0;
      let scrollProgress = 0;
      let hasScrolled = false;

      // Aspect Ratio Sizing (Ensures images fill the screen without blank bars)
      function resizeMediaFrames() {
        const vw = window.innerWidth;
        const vh = window.innerHeight;
        maxScroll = Math.max(1, scrollContainer.offsetHeight - vh);

        // Aspect ratios:
        // facade_master: 1376 / 1080 (1.274)
        // banq1: 1024 / 1024 (1.000)
        // banq2: 1024 / 1024 (1.000)
        // banq3: 896 / 1200 (0.7467)
        // banq4: 896 / 1200 (0.7467)
        const targets = [
          { el: frameFacade, ratio: 1376 / 1080 },
          { el: frameBanq1, ratio: 1024 / 1024 },
          { el: frameBanq2, ratio: 1024 / 1024 },
          { el: frameBanq3, ratio: 896 / 1200 },
          { el: frameBanq4, ratio: 896 / 1200 }
        ];

        targets.forEach(function (item) {
          const r = item.ratio;
          let w, h;
          if (vw / vh > r) {
            w = vw;
            h = vw / r;
          } else {
            h = vh;
            w = vh * r;
          }
          item.el.style.width = Math.ceil(w) + 'px';
          item.el.style.height = Math.ceil(h) + 'px';
        });
      }

      resizeMediaFrames();
      window.addEventListener('resize', resizeMediaFrames, { passive: true });

      // Native Window Scroll Synchronization
      window.addEventListener('scroll', function () {
        targetScrollY = window.scrollY;
        if (!hasScrolled && targetScrollY > 15) {
          hasScrolled = true;
          scrollHint.style.opacity = '0';
        }
      }, { passive: true });

      // Smooth Inertia Wheel Listener
      window.addEventListener('wheel', function (e) {
        targetScrollY = Math.max(0, Math.min(maxScroll, targetScrollY + e.deltaY * 1.15));
      }, { passive: true });

      // Mobile Touch Handling
      let touchY = 0;
      window.addEventListener('touchstart', function (e) {
        if (e.touches.length === 1) touchY = e.touches[0].clientY;
      }, { passive: true });

      window.addEventListener('touchmove', function (e) {
        if (e.touches.length === 1) {
          const currentY = e.touches[0].clientY;
          const delta = (touchY - currentY) * 1.6;
          touchY = currentY;
          targetScrollY = Math.max(0, Math.min(maxScroll, targetScrollY + delta));
          if (!hasScrolled && targetScrollY > 15) {
            hasScrolled = true;
            scrollHint.style.opacity = '0';
          }
        }
      }, { passive: true });

      // Keyboard arrow keys
      window.addEventListener('keydown', function (e) {
        if (e.key === 'ArrowDown' || e.key === 'PageDown' || e.key === ' ') {
          targetScrollY = Math.min(maxScroll, targetScrollY + window.innerHeight * 0.42);
        } else if (e.key === 'ArrowUp' || e.key === 'PageUp') {
          targetScrollY = Math.max(0, targetScrollY - window.innerHeight * 0.42);
        } else if (e.key === 'Home') {
          targetScrollY = 0;
        } else if (e.key === 'End') {
          targetScrollY = maxScroll;
        }
      });

      // Easing Functions
      function clamp(val, min, max) {
        return Math.max(min, Math.min(max, val));
      }

      function norm(val, start, end) {
        return clamp((val - start) / (end - start), 0, 1);
      }

      function smoothstep(t) {
        return t * t * (3 - 2 * t);
      }

      function easeInOutQuad(t) {
        return t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;
      }

      function easeOutCubic(t) {
        const t1 = t - 1;
        return t1 * t1 * t1 + 1;
      }

      // =========================================================================
      // VIRTUAL TOUR CHOREOGRAPHY ENGINE (2.5D CAMERA PUSH)
      // =========================================================================
      function renderTour(p) {
        progressFill.style.width = (p * 100).toFixed(2) + '%';

        // -----------------------------------------------------------------------
        // STAGE 1: [0.00 -> 0.22] START AT SKYLINE & CUPOLA, TILT & DESCEND DOWN FACADE
        // -----------------------------------------------------------------------
        // In facade_master (1376x1080):
        // Top 0% is the upper chhatri, birds in sunset sky (main1)
        // As p goes 0 to 0.22, camera tilts down: translateY moves from 16% down to -10%
        if (p <= 0.55) {
          sceneFacade.style.display = 'flex';

          // Camera vertical glide down facade
          const descentProg = norm(p, 0.00, 0.20);
          const descentSmooth = easeInOutQuad(descentProg);

          // Initial descent down from sky to courtyard
          const startY = 16.0 - descentSmooth * 24.0; // 16% -> -8%

          // ---------------------------------------------------------------------
          // STAGE 2: [0.18 -> 0.38] PUSH IN TOWARDS ENTRANCE, DOORS OPEN, RECEPTION SHOWN
          // ---------------------------------------------------------------------
          const pushProg = norm(p, 0.18, 0.36);
          const pushSmooth = easeInOutQuad(pushProg);

          // Zoom into entrance doors
          const scaleEntrance = 1.0 + pushSmooth * 1.65; // 1.0 -> 2.65
          const focusDoorY = startY - pushSmooth * 18.0;

          // 3D Door Swing (rotateY -82deg / +82deg)
          const doorProg = norm(p, 0.22, 0.36);
          const doorSmooth = easeInOutQuad(doorProg);

          const leftAngle = -(doorSmooth * 82);
          const rightAngle = doorSmooth * 82;

          doorLeft.style.transform = 'rotateY(' + leftAngle + 'deg)';
          doorRight.style.transform = 'rotateY(' + rightAngle + 'deg)';

          // Reveal reception interior through open doorway
          receptionInterior.style.opacity = (doorSmooth * 0.96).toFixed(3);
          receptionInterior.style.transform = 'scale(' + (0.95 + doorSmooth * 0.12) + ')';

          // ---------------------------------------------------------------------
          // STAGE 3: [0.35 -> 0.54] CAMERA ANGLE PANS TO RIGHT WINDOW, ZOOMS IN,
          //          CURTAINS PART, CAMERA PUNCHES THROUGH INTO BANQ1
          // ---------------------------------------------------------------------
          const windowPanProg = norm(p, 0.34, 0.50);
          const windowPanSmooth = easeInOutQuad(windowPanProg);

          // Pan camera right to frame the arched window (win_x: 58%)
          const panX = -(windowPanSmooth * 22.0);
          const panY = focusDoorY - windowPanSmooth * 4.0;
          const scaleWindow = scaleEntrance + windowPanSmooth * 3.5; // Massive push into window

          frameFacade.style.transform = 'translate(-50%, -50%) translate3d(' + panX + '%, ' + panY + '%, 0) scale(' + scaleWindow + ')';
          frameFacade.style.transformOrigin = '55% 78%';

          // Sheer curtains billow & part in 3D
          const curtainPartProg = norm(p, 0.38, 0.52);
          const curtainPartSmooth = smoothstep(curtainPartProg);

          const partOffset = curtainPartSmooth * 85; // Curtains slide outward
          curtainLeft.style.transform = 'translate3d(' + (-partOffset) + '%, 0, 0) scale(' + (1 + curtainPartSmooth * 0.25) + ')';
          curtainRight.style.transform = 'translate3d(' + partOffset + '%, 0, 0) scale(' + (1 + curtainPartSmooth * 0.25) + ')';

          // Curtains opacity fades as camera crosses window threshold
          const curtainAlpha = 1.0 - norm(p, 0.46, 0.52);
          curtainLeft.style.opacity = curtainAlpha.toFixed(3);
          curtainRight.style.opacity = curtainAlpha.toFixed(3);

          windowGlow.style.opacity = (curtainPartSmooth * (1 - norm(p, 0.49, 0.54))).toFixed(3);

          // Facade scene opacity dissolves as camera penetrates through window into banq1
          const facadeAlpha = 1.0 - norm(p, 0.48, 0.54);
          sceneFacade.style.opacity = facadeAlpha.toFixed(3);
        } else {
          sceneFacade.style.opacity = '0';
          sceneFacade.style.display = 'none';
        }

        // -----------------------------------------------------------------------
        // STAGE 4: [0.47 -> 0.72] CAMERA EMERGES THROUGH WINDOW INTO FLORAL CORRIDOR (banq1)
        //          THEN CAMERA MOVES DIRECTLY TO LEFT TOWARD BALLROOM
        // -----------------------------------------------------------------------
        if (p >= 0.46 && p <= 0.74) {
          sceneBanq1.style.display = 'flex';

          // Emerges from center of window: start slightly smaller (0.92) expanding to 1.15
          const inAlpha1 = norm(p, 0.48, 0.54);
          const outAlpha1 = 1.0 - norm(p, 0.65, 0.72);
          sceneBanq1.style.opacity = Math.min(inAlpha1, outAlpha1).toFixed(3);

          const pushCorridor = norm(p, 0.48, 0.70);
          const pushCorridorSmooth = easeInOutQuad(pushCorridor);
          const scale1 = 0.94 + pushCorridorSmooth * 0.35; // 0.94 -> 1.29

          // As it nears the end of banq1, camera dollies to the left:
          // "then camera moves directly to left and connect banq2.jpg"
          const leftDolly = -(norm(p, 0.60, 0.72) * 28.0);

          frameBanq1.style.transform = 'translate(-50%, -50%) translate3d(' + leftDolly + '%, 0, 0) scale(' + scale1 + ')';
        } else {
          sceneBanq1.style.opacity = '0';
          sceneBanq1.style.display = 'none';
        }

        // -----------------------------------------------------------------------
        // STAGE 5: [0.63 -> 0.86] SWEEPING LEFT TURN & CONNECTING GRAND BALLROOM (banq2)
        // -----------------------------------------------------------------------
        if (p >= 0.62 && p <= 0.87) {
          sceneBanq2.style.display = 'flex';

          const inAlpha2 = norm(p, 0.64, 0.71);
          const outAlpha2 = 1.0 - norm(p, 0.80, 0.86);
          sceneBanq2.style.opacity = Math.min(inAlpha2, outAlpha2).toFixed(3);

          // Sweeps in from the right as camera yaws left
          const sweepProg = norm(p, 0.63, 0.84);
          const sweepSmooth = easeInOutQuad(sweepProg);

          const enterX = (1.0 - norm(p, 0.63, 0.72)) * 22.0; // slides in from +22%
          const exitX = -(norm(p, 0.76, 0.85) * 14.0);      // drifts left toward center aisle
          const posX2 = enterX + exitX;
          const scale2 = 1.02 + sweepSmooth * 0.22;

          frameBanq2.style.transform = 'translate(-50%, -50%) translate3d(' + posX2 + '%, 0, 0) scale(' + scale2 + ')';
        } else {
          sceneBanq2.style.opacity = '0';
          sceneBanq2.style.display = 'none';
        }

        // -----------------------------------------------------------------------
        // STAGE 6: [0.78 -> 0.95] IMPERIAL CENTER AISLE PUSH (banq3)
        // -----------------------------------------------------------------------
        if (p >= 0.77 && p <= 0.95) {
          sceneBanq3.style.display = 'flex';

          const inAlpha3 = norm(p, 0.79, 0.85);
          const outAlpha3 = 1.0 - norm(p, 0.90, 0.95);
          sceneBanq3.style.opacity = Math.min(inAlpha3, outAlpha3).toFixed(3);

          // Accelerates down the aisle between the chairs toward the royal stage
          const aisleProg = norm(p, 0.79, 0.94);
          const aisleSmooth = easeInOutQuad(aisleProg);

          const scale3 = 1.0 + aisleSmooth * 0.42;
          const panY3 = -(aisleSmooth * 9.0); // Tilt toward the stage

          frameBanq3.style.transform = 'translate(-50%, -50%) translate3d(0, ' + panY3 + '%, 0) scale(' + scale3 + ')';
        } else {
          sceneBanq3.style.opacity = '0';
          sceneBanq3.style.display = 'none';
        }

        // -----------------------------------------------------------------------
        // STAGE 7: [0.89 -> 1.00] ROYAL WEDDING MANDAP FINALE ARRIVAL (banq4)
        // -----------------------------------------------------------------------
        if (p >= 0.88) {
          sceneBanq4.style.display = 'flex';

          const inAlpha4 = norm(p, 0.89, 0.96);
          sceneBanq4.style.opacity = inAlpha4.toFixed(3);

          const mandapProg = norm(p, 0.89, 1.00);
          const mandapSmooth = easeOutCubic(mandapProg);

          // Glides up close, gently locking in on the royal throne chairs & floral pillars
          const scale4 = 1.18 - (1.0 - mandapSmooth) * 0.18;
          const panY4 = (1.0 - mandapSmooth) * 4.0;

          frameBanq4.style.transform = 'translate(-50%, -50%) translate3d(0, ' + panY4 + '%, 0) scale(' + scale4 + ')';
        } else {
          sceneBanq4.style.opacity = '0';
          sceneBanq4.style.display = 'none';
        }

        // Subtle 3D virtual tour camera banking for organic human movement
        const camRoll = Math.sin(p * Math.PI * 4) * 0.45;
        const camPitch = (p - 0.5) * 0.9;
        cameraRig.style.transform = 'rotateZ(' + camRoll.toFixed(2) + 'deg) rotateX(' + camPitch.toFixed(2) + 'deg)';
      }

      // =========================================================================
      // ANIMATION LOOP (Butter-Smooth Lerp Inertia)
      // =========================================================================
      function loop() {
        // Luxury weighted inertia damping
        currentScrollY += (targetScrollY - currentScrollY) * 0.075;
        scrollProgress = clamp(currentScrollY / maxScroll, 0, 1);

        renderTour(scrollProgress);
        requestAnimationFrame(loop);
      }
      requestAnimationFrame(loop);

      // =========================================================================
      // LIVING ATMOSPHERE (Drifting Pastel Rose & Champagne Petals)
      // =========================================================================
      const canvas = document.getElementById('particles-canvas');
      const ctx = canvas.getContext('2d');

      let cw = 0, ch = 0;
      function resizeCanvas() {
        cw = canvas.width = window.innerWidth;
        ch = canvas.height = window.innerHeight;
      }
      resizeCanvas();
      window.addEventListener('resize', resizeCanvas, { passive: true });

      const petals = [];
      const PETAL_COUNT = 34;
      const palette = [
        'rgba(248, 238, 224, 0.42)', // Champagne gold
        'rgba(255, 228, 218, 0.48)', // Soft pastel rose
        'rgba(250, 244, 236, 0.38)', // Jasmine white
        'rgba(235, 210, 185, 0.32)'  // Warm sand
      ];

      for (let i = 0; i < PETAL_COUNT; i++) {
        petals.push({
          x: Math.random() * window.innerWidth,
          y: Math.random() * window.innerHeight,
          rx: 1.5 + Math.random() * 3.2,
          ry: 1.0 + Math.random() * 2.2,
          color: palette[Math.floor(Math.random() * palette.length)],
          vx: (Math.random() - 0.5) * 0.38 + 0.12,
          vy: 0.32 + Math.random() * 0.58,
          angle: Math.random() * Math.PI * 2,
          vAngle: (Math.random() - 0.5) * 0.022,
          swayFreq: 0.002 + Math.random() * 0.003,
          swayPhase: Math.random() * Math.PI * 2
        });
      }

      let tick = 0;
      function animatePetals() {
        tick++;
        ctx.clearRect(0, 0, cw, ch);

        for (let i = 0; i < petals.length; i++) {
          const pt = petals[i];
          pt.x += pt.vx + Math.sin(tick * pt.swayFreq + pt.swayPhase) * 0.35;
          pt.y += pt.vy;
          pt.angle += pt.vAngle;

          if (pt.y > ch + 20) {
            pt.y = -20;
            pt.x = Math.random() * cw;
          }
          if (pt.x > cw + 20) pt.x = -20;
          if (pt.x < -20) pt.x = cw + 20;

          ctx.save();
          ctx.translate(pt.x, pt.y);
          ctx.rotate(pt.angle);
          ctx.beginPath();
          ctx.ellipse(0, 0, pt.rx, pt.ry, 0, 0, Math.PI * 2);
          ctx.fillStyle = pt.color;
          ctx.fill();
          ctx.restore();
        }

        requestAnimationFrame(animatePetals);
      }
      requestAnimationFrame(animatePetals);

    })();
  </script>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html.strip())

print("SUCCESS: index.html generated with 2.5D Architectural Virtual Tour Camera Push!")
