import re

html_code = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>The Royal Palace Resort - Virtual Drone Tour</title>
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
      background-color: #060504;
      color: #f7f4ee;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      overflow-x: hidden;
      overscroll-behavior: none;
      user-select: none;
      -webkit-user-select: none;
    }

    /* SCROLL CONTAINER (1000vh FOR FLUID, RELAXED SCROLLING) */
    .scroll-container {
      width: 100%;
      height: 1000vh;
      position: relative;
      pointer-events: none;
    }

    /* FIXED CINEMATIC VIEWPORT */
    .viewport-stage {
      position: fixed;
      inset: 0;
      width: 100vw;
      height: 100vh;
      height: 100dvh;
      overflow: hidden;
      background: #060504;
      perspective: 1200px;
      perspective-origin: 50% 50%;
    }

    /* 3D DRONE CAMERA RIG */
    .camera-rig {
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      transform-style: preserve-3d;
      will-change: transform;
    }

    /* TOUR SCENES */
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
      opacity: 0;
    }

    /* MEDIA BOX (RESPONSIVE COVER) */
    .media-box {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      will-change: transform, opacity;
      transform-style: preserve-3d;
    }

    .media-box img.bg-img {
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
      pointer-events: none;
    }

    /* =========================================================================
       SCENE 2: PIXEL-PERFECT 3D DOOR ASSEMBLY
       Coordinates on 1376x768 main2.jpg:
       Left: 648px (47.093023%)
       Top: 485px (63.151042%)
       Width: 80px (5.813953%)
       Height: 87px (11.328125%)
       Center: 688px (50.000000%), Center Y: 528.5px (68.815104%)
       ========================================================================= */
    .door-assembly {
      position: absolute;
      left: 47.093023%;
      top: 63.151042%;
      width: 5.813953%;
      height: 11.328125%;
      perspective: 800px;
      transform-style: preserve-3d;
      z-index: 10;
      pointer-events: none;
    }

    .door-leaf {
      position: absolute;
      top: 0;
      width: 50%;
      height: 100%;
      background-size: 100% 100%;
      background-position: center;
      background-repeat: no-repeat;
      transform-style: preserve-3d;
      will-change: transform;
      box-shadow: 0 1px 8px rgba(0, 0, 0, 0.6);
    }

    .door-leaf.left {
      left: 0;
      transform-origin: left center;
      background-image: url('img/door_left.png?v=4');
    }

    .door-leaf.right {
      right: 0;
      transform-origin: right center;
      background-image: url('img/door_right.png?v=4');
    }

    /* WARM WINDOW LIGHT GLOW (SCENE 3) */
    .window-glow-overlay {
      position: absolute;
      inset: 0;
      background: radial-gradient(circle at 72% 48%, rgba(255, 235, 195, 0.85) 0%, rgba(255, 210, 140, 0.35) 40%, transparent 75%);
      opacity: 0;
      pointer-events: none;
      mix-blend-mode: screen;
      z-index: 8;
      will-change: opacity;
    }

    /* LIVING ATMOSPHERE (Canvas Petals & Sparkles) */
    #particles-canvas {
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      pointer-events: none;
      z-index: 20;
    }

    /* CINEMATIC OPTICAL VIGNETTE */
    .cinema-vignette {
      position: absolute;
      inset: 0;
      pointer-events: none;
      z-index: 18;
      background: radial-gradient(circle at 50% 50%, transparent 68%, rgba(6, 5, 4, 0.40) 100%);
    }

    /* TOUR PROGRESS LINE */
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
      box-shadow: 0 0 10px rgba(230, 200, 175, 0.7);
      will-change: width;
    }

    /* SUBTLE SCROLL HINT (Disappears on first scroll) */
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
  <main class="viewport-stage" id="viewport-stage">

    <div class="camera-rig" id="camera-rig">

      <!-- SCENE 1: STARTING PAGE (main1.jpg: 1376x768) -->
      <section class="tour-scene" id="scene-1" style="opacity: 1; z-index: 1;">
        <div class="media-box" id="box-1">
          <img class="bg-img" src="img/main1.jpg?v=4" alt="Resort Facade Roof & Sky" id="img-1" />
        </div>
      </section>

      <!-- SCENE 2: COURTYARD & 3D ENTRANCE DOORS (main2_open.jpg: 1376x768) -->
      <section class="tour-scene" id="scene-2" style="z-index: 2;">
        <div class="media-box" id="box-2">
          <img class="bg-img" src="img/main2_open.jpg?v=4" alt="Palace Courtyard" id="img-2" />
          <div class="door-assembly" id="door-assembly">
            <div class="door-leaf left" id="door-l"></div>
            <div class="door-leaf right" id="door-r"></div>
          </div>
        </div>
      </section>

      <!-- SCENE 3: RECEPTION LOBBY & BIG CURTAINED WINDOW (reception.jpg: 1264x848) -->
      <section class="tour-scene" id="scene-3" style="z-index: 3;">
        <div class="media-box" id="box-3">
          <img class="bg-img" src="img/reception.jpg?v=4" alt="Reception Lobby & Grand Window" id="img-3" />
          <div class="window-glow-overlay" id="window-glow"></div>
        </div>
      </section>

      <!-- SCENE 4: BANQUET NIGHT EXTERIOR ENTRANCE (banqent.jpg: 1376x768) -->
      <section class="tour-scene" id="scene-4" style="z-index: 4;">
        <div class="media-box" id="box-4">
          <img class="bg-img" src="img/banqent.jpg?v=4" alt="Banquet Night Entrance" id="img-4" />
        </div>
      </section>

      <!-- SCENE 5: ROYAL ELEPHANT ARRIVAL WALKWAY (banq1.jpg: 1024x1024) -->
      <section class="tour-scene" id="scene-5" style="z-index: 5;">
        <div class="media-box" id="box-5">
          <img class="bg-img" src="img/banq1.jpg?v=4" alt="Arrival Floral Walkway" id="img-5" />
        </div>
      </section>

      <!-- SCENE 6: GRAND CRYSTAL BALLROOM (banq2.jpg: 1024x1024) -->
      <section class="tour-scene" id="scene-6" style="z-index: 6;">
        <div class="media-box" id="box-6">
          <img class="bg-img" src="img/banq2.jpg?v=4" alt="Grand Ballroom Chandeliers" id="img-6" />
        </div>
      </section>

      <!-- SCENE 7: CENTER AISLE CHANDELIER DIVE (banq3.jpg: 896x1200) -->
      <section class="tour-scene" id="scene-7" style="z-index: 7;">
        <div class="media-box" id="box-7">
          <img class="bg-img" src="img/banq3.jpg?v=4" alt="Center Aisle Perspective" id="img-7" />
        </div>
      </section>

      <!-- SCENE 8: ROYAL WEDDING MANDAP FINALE (banq4.jpg: 896x1200) -->
      <section class="tour-scene" id="scene-8" style="z-index: 8;">
        <div class="media-box" id="box-8">
          <img class="bg-img" src="img/banq4.jpg?v=4" alt="Royal Wedding Mandap Finale" id="img-8" />
        </div>
      </section>

    </div>

    <!-- LIVING ATMOSPHERE CANVAS -->
    <canvas id="particles-canvas"></canvas>

    <!-- CINEMATIC VIGNETTE -->
    <div class="cinema-vignette"></div>

    <!-- SCROLL HINT -->
    <div class="scroll-hint" id="scroll-hint">
      <div class="scroll-hint-line"></div>
    </div>

    <!-- TOUR PROGRESS BAR -->
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

      // 8 Scenes & Boxes
      const scenes = [];
      const boxes = [];
      for (let i = 1; i <= 8; i++) {
        scenes[i] = document.getElementById('scene-' + i);
        boxes[i] = document.getElementById('box-' + i);
      }

      const doorL = document.getElementById('door-l');
      const doorR = document.getElementById('door-r');
      const windowGlow = document.getElementById('window-glow');

      // Scroll State
      let maxScroll = 1;
      let targetScrollY = 0;
      let currentScrollY = 0;
      let scrollProgress = 0;
      let hasScrolled = false;

      // Exact aspect ratios of the 8 user assets:
      const imageRatios = {
        1: 1376 / 768,  // main1.jpg
        2: 1376 / 768,  // main2_open.jpg
        3: 1264 / 848,  // reception.jpg
        4: 1376 / 768,  // banqent.jpg
        5: 1024 / 1024, // banq1.jpg
        6: 1024 / 1024, // banq2.jpg
        7: 896 / 1200,  // banq3.jpg
        8: 896 / 1200   // banq4.jpg
      };

      // Responsive aspect-ratio cover sizing
      function resizeMediaBoxes() {
        const vw = window.innerWidth;
        const vh = window.innerHeight;
        maxScroll = Math.max(1, scrollContainer.offsetHeight - vh);

        for (let i = 1; i <= 8; i++) {
          const r = imageRatios[i] || 1.777;
          let w, h;
          if (vw / vh > r) {
            w = vw;
            h = vw / r;
          } else {
            h = vh;
            w = vh * r;
          }
          boxes[i].style.width = Math.ceil(w) + 'px';
          boxes[i].style.height = Math.ceil(h) + 'px';
        }
      }

      resizeMediaBoxes();
      window.addEventListener('resize', resizeMediaBoxes, { passive: true });

      // Window Scroll Sync
      window.addEventListener('scroll', function () {
        targetScrollY = window.scrollY;
        if (!hasScrolled && targetScrollY > 15) {
          hasScrolled = true;
          scrollHint.style.opacity = '0';
        }
      }, { passive: true });

      // Inertial Wheel Listener
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

      // Keyboard Controls
      window.addEventListener('keydown', function (e) {
        if (e.key === 'ArrowDown' || e.key === 'PageDown' || e.key === ' ') {
          targetScrollY = Math.min(maxScroll, targetScrollY + window.innerHeight * 0.40);
        } else if (e.key === 'ArrowUp' || e.key === 'PageUp') {
          targetScrollY = Math.max(0, targetScrollY - window.innerHeight * 0.40);
        } else if (e.key === 'Home') {
          targetScrollY = 0;
        } else if (e.key === 'End') {
          targetScrollY = maxScroll;
        }
      });

      // Math & Easing Utilities
      function clamp(val, min, max) {
        return Math.max(min, Math.min(max, val));
      }

      function norm(val, start, end) {
        return clamp((val - start) / (end - start), 0, 1);
      }

      function easeInOutQuad(t) {
        return t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;
      }

      function easeOutCubic(t) {
        const t1 = t - 1;
        return t1 * t1 * t1 + 1;
      }

      // =========================================================================
      // VIRTUAL TOUR CHOREOGRAPHY ENGINE (ALL 8 ASSETS IN SEQUENCE)
      // =========================================================================
      function renderTour(p) {
        progressFill.style.width = (p * 100).toFixed(2) + '%';

        // -----------------------------------------------------------------------
        // STAGE 1: [0.00 -> 0.14] START AT main1.jpg (Roof pavilion & sky with birds)
        //          Camera tilts and tracks down the facade towards the courtyard
        // -----------------------------------------------------------------------
        if (p <= 0.15) {
          scenes[1].style.display = 'flex';
          const t = norm(p, 0.00, 0.12);
          const st = easeInOutQuad(t);

          const scale = 1.0 + st * 0.15;
          const panY = -(st * 12.0);
          boxes[1].style.transform = 'translate(-50%, -50%) translate3d(0, ' + panY + '%, 0) scale(' + scale + ')';

          const alpha = 1.0 - norm(p, 0.07, 0.13);
          scenes[1].style.opacity = alpha.toFixed(3);
        } else {
          scenes[1].style.opacity = '0';
          scenes[1].style.display = 'none';
        }

        // -----------------------------------------------------------------------
        // STAGE 2: [0.07 -> 0.28] main2.jpg COURTYARD & 3D DOOR OPENING
        //          Camera approaches grand entrance; double doors swing inward in 3D
        // -----------------------------------------------------------------------
        if (p >= 0.065 && p <= 0.29) {
          scenes[2].style.display = 'flex';

          const inAlpha = norm(p, 0.07, 0.12);
          const outAlpha = 1.0 - norm(p, 0.23, 0.28);
          scenes[2].style.opacity = Math.min(inAlpha, outAlpha).toFixed(3);

          // Push into the entrance door:
          // Center of door in main2.jpg: X=50.0%, Y=68.815%
          const pushProg = norm(p, 0.08, 0.26);
          const pushSmooth = easeInOutQuad(pushProg);
          const scale = 1.0 + pushSmooth * 3.7;

          boxes[2].style.transformOrigin = '50.0% 68.815%';
          boxes[2].style.transform = 'translate(-50%, -50%) scale(' + scale + ')';

          // 3D Door Swing: from 0.12 to 0.21
          const doorProg = norm(p, 0.12, 0.21);
          const doorSmooth = easeInOutQuad(doorProg);
          const leftAngle = -(doorSmooth * 85.0);
          const rightAngle = doorSmooth * 85.0;

          doorL.style.transform = 'rotateY(' + leftAngle + 'deg)';
          doorR.style.transform = 'rotateY(' + rightAngle + 'deg)';
        } else {
          scenes[2].style.opacity = '0';
          scenes[2].style.display = 'none';
        }

        // -----------------------------------------------------------------------
        // STAGE 3: [0.22 -> 0.42] reception.jpg (RECEPTION LOBBY & BIG CURTAINED WINDOW)
        //          Glides into reception, then camera pans towards the big arched
        //          window with semi-transparent curtains on the right, zooms deep in,
        //          and camera zoops out through the window!
        // -----------------------------------------------------------------------
        if (p >= 0.215 && p <= 0.43) {
          scenes[3].style.display = 'flex';

          const inAlpha = norm(p, 0.22, 0.27);
          const outAlpha = 1.0 - norm(p, 0.37, 0.42);
          scenes[3].style.opacity = Math.min(inAlpha, outAlpha).toFixed(3);

          // Phase A (0.22 -> 0.29): glide into reception hall
          // Phase B (0.29 -> 0.41): turn and push deep into the big curtained window
          // Window center in reception.jpg is at approx X: 68%, Y: 50%
          const winProg = norm(p, 0.28, 0.41);
          const winSmooth = easeInOutQuad(winProg);

          const scale = 1.02 + norm(p, 0.22, 0.29) * 0.25 + winSmooth * 2.8;
          const panX = -(winSmooth * 20.0);
          const panY = -(winSmooth * 4.0);

          boxes[3].style.transformOrigin = '68.0% 50.0%';
          boxes[3].style.transform = 'translate(-50%, -50%) translate3d(' + panX + '%, ' + panY + '%, 0) scale(' + scale + ')';

          // Sunlight/sunset bloom through the sheer curtains as camera reaches window
          const glowAlpha = Math.sin(norm(p, 0.32, 0.41) * Math.PI) * 0.70;
          windowGlow.style.opacity = glowAlpha.toFixed(3);
        } else {
          scenes[3].style.opacity = '0';
          scenes[3].style.display = 'none';
        }

        // -----------------------------------------------------------------------
        // STAGE 4: [0.37 -> 0.55] banqent.jpg (BANQUET NIGHT EXTERIOR ENTRANCE)
        //          Camera zoops out of the window into the night courtyard,
        //          gliding up the steps towards the glowing banquet entrance
        // -----------------------------------------------------------------------
        if (p >= 0.365 && p <= 0.56) {
          scenes[4].style.display = 'flex';

          const inAlpha = norm(p, 0.37, 0.42);
          const outAlpha = 1.0 - norm(p, 0.50, 0.55);
          scenes[4].style.opacity = Math.min(inAlpha, outAlpha).toFixed(3);

          const pushProg = norm(p, 0.37, 0.53);
          const pushSmooth = easeInOutQuad(pushProg);

          const scale = 1.01 + pushSmooth * 0.38;
          const panY = -(pushSmooth * 6.0);
          boxes[4].style.transform = 'translate(-50%, -50%) translate3d(0, ' + panY + '%, 0) scale(' + scale + ')';
        } else {
          scenes[4].style.opacity = '0';
          scenes[4].style.display = 'none';
        }

        // -----------------------------------------------------------------------
        // STAGE 5: [0.49 -> 0.67] banq1.jpg (ROYAL ELEPHANT FLORAL WALKWAY)
        //          Camera pushes forward down the aisle, then moves directly to left
        //          to connect with banq2.jpg!
        // -----------------------------------------------------------------------
        if (p >= 0.485 && p <= 0.68) {
          scenes[5].style.display = 'flex';

          const inAlpha = norm(p, 0.49, 0.54);
          const outAlpha = 1.0 - norm(p, 0.62, 0.67);
          scenes[5].style.opacity = Math.min(inAlpha, outAlpha).toFixed(3);

          const pushProg = norm(p, 0.49, 0.64);
          const pushSmooth = easeInOutQuad(pushProg);
          const scale = 1.01 + pushSmooth * 0.30;

          // Camera dollies and pans directly to the left:
          // "then camera moves directly to left and connect banq2.jpg"
          const leftDolly = -(norm(p, 0.57, 0.66) * 26.0);

          boxes[5].style.transform = 'translate(-50%, -50%) translate3d(' + leftDolly + '%, 0, 0) scale(' + scale + ')';
        } else {
          scenes[5].style.opacity = '0';
          scenes[5].style.display = 'none';
        }

        // -----------------------------------------------------------------------
        // STAGE 6: [0.61 -> 0.79] banq2.jpg (GRAND CRYSTAL BALLROOM SIDE VIEW)
        //          Connected seamlessly from the left!
        //          Sweeps across the crystal chandeliers and imperial seating
        // -----------------------------------------------------------------------
        if (p >= 0.605 && p <= 0.80) {
          scenes[6].style.display = 'flex';

          const inAlpha = norm(p, 0.61, 0.66);
          const outAlpha = 1.0 - norm(p, 0.74, 0.79);
          scenes[6].style.opacity = Math.min(inAlpha, outAlpha).toFixed(3);

          const pushProg = norm(p, 0.61, 0.77);
          const pushSmooth = easeInOutQuad(pushProg);

          // Sweeps in from right as camera yaws left
          const enterX = (1.0 - norm(p, 0.61, 0.68)) * 20.0;
          const exitX = -(norm(p, 0.69, 0.78) * 12.0);
          const scale = 1.02 + pushSmooth * 0.24;

          boxes[6].style.transform = 'translate(-50%, -50%) translate3d(' + (enterX + exitX) + '%, 0, 0) scale(' + scale + ')';
        } else {
          scenes[6].style.opacity = '0';
          scenes[6].style.display = 'none';
        }

        // -----------------------------------------------------------------------
        // STAGE 7: [0.73 -> 0.90] banq3.jpg (CENTER AISLE CHANDELIER DIVE)
        //          Fast, exhilarating push straight down the center aisle towards
        //          the grand stage directly under the crystal chandeliers
        // -----------------------------------------------------------------------
        if (p >= 0.725 && p <= 0.91) {
          scenes[7].style.display = 'flex';

          const inAlpha = norm(p, 0.73, 0.78);
          const outAlpha = 1.0 - norm(p, 0.86, 0.90);
          scenes[7].style.opacity = Math.min(inAlpha, outAlpha).toFixed(3);

          const aisleProg = norm(p, 0.73, 0.89);
          const aisleSmooth = easeInOutQuad(aisleProg);

          const scale = 1.00 + aisleSmooth * 0.42;
          const panY = -(aisleSmooth * 8.0);
          boxes[7].style.transform = 'translate(-50%, -50%) translate3d(0, ' + panY + '%, 0) scale(' + scale + ')';
        } else {
          scenes[7].style.opacity = '0';
          scenes[7].style.display = 'none';
        }

        // -----------------------------------------------------------------------
        // STAGE 8: [0.85 -> 1.00] banq4.jpg (ROYAL WEDDING MANDAP FINALE)
        //          Grand finale: camera settles gracefully right in front of the
        //          Royal Wedding Mandap, golden chandelier, and royal thrones!
        // -----------------------------------------------------------------------
        if (p >= 0.845) {
          scenes[8].style.display = 'flex';

          const inAlpha = norm(p, 0.85, 0.90);
          scenes[8].style.opacity = inAlpha.toFixed(3);

          const mandapProg = norm(p, 0.85, 1.00);
          const mandapSmooth = easeOutCubic(mandapProg);

          const scale = 1.15 - (1.0 - mandapSmooth) * 0.15;
          const panY = (1.0 - mandapSmooth) * 3.5;
          boxes[8].style.transform = 'translate(-50%, -50%) translate3d(0, ' + panY + '%, 0) scale(' + scale + ')';
        } else {
          scenes[8].style.opacity = '0';
          scenes[8].style.display = 'none';
        }

        // Drone Camera Banking & Elevation (subtle organic 3D camera wobble):
        const camRoll = Math.sin(p * Math.PI * 5.0) * 0.35;
        const camPitch = (p - 0.5) * 0.60;
        cameraRig.style.transform = 'rotateZ(' + camRoll.toFixed(2) + 'deg) rotateX(' + camPitch.toFixed(2) + 'deg)';
      }

      // =========================================================================
      // SMOOTH LERP INERTIA ANIMATION LOOP
      // =========================================================================
      function loop() {
        currentScrollY += (targetScrollY - currentScrollY) * 0.082;
        scrollProgress = clamp(currentScrollY / maxScroll, 0, 1);

        renderTour(scrollProgress);
        requestAnimationFrame(loop);
      }
      requestAnimationFrame(loop);

      // =========================================================================
      // LIVING ATMOSPHERE (Canvas Floating Rose Petals & Champagne Sparkles)
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
      const PETAL_COUNT = 36;
      const petalPalette = [
        'rgba(248, 238, 224, 0.45)', // Champagne gold
        'rgba(255, 225, 215, 0.50)', // Soft rose
        'rgba(250, 244, 236, 0.40)', // Jasmine white
        'rgba(235, 208, 180, 0.35)'  // Warm sand
      ];

      for (let i = 0; i < PETAL_COUNT; i++) {
        petals.push({
          x: Math.random() * window.innerWidth,
          y: Math.random() * window.innerHeight,
          rx: 1.5 + Math.random() * 3.5,
          ry: 1.0 + Math.random() * 2.2,
          color: petalPalette[Math.floor(Math.random() * petalPalette.length)],
          vx: (Math.random() - 0.5) * 0.35 + 0.15,
          vy: 0.35 + Math.random() * 0.60,
          angle: Math.random() * Math.PI * 2,
          vAngle: (Math.random() - 0.5) * 0.025,
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

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_code)

print("index.html written successfully!")
