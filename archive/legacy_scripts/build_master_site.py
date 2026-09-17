import os

html_code = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>The Royal Palace Resort - Virtual Drone Tour</title>
  <style>
    /* =========================================================================
       BASE ARCHITECTURAL CANVAS & RESET
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
      background-color: #080605;
      color: #f7f4ee;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      overflow-x: hidden;
      overscroll-behavior: none;
      user-select: none;
      -webkit-user-select: none;
    }

    /* VIRTUAL SCROLL TRACK */
    .scroll-container {
      width: 100%;
      height: 1400vh;
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
      background: #080605;
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
      box-shadow: 0 1px 8px rgba(0, 0, 0, 0.55);
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

    /* =========================================================================
       SCENE 4: ARCHED WINDOW WITH TRANSLUCENT SHEER CURTAINS
       ========================================================================= */
    .window-curtain-layer {
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      pointer-events: none;
      z-index: 5;
      transform-style: preserve-3d;
      overflow: hidden;
    }

    .curtain-drape {
      position: absolute;
      top: 0;
      width: 55%;
      height: 100%;
      background-size: cover;
      background-repeat: no-repeat;
      will-change: transform, opacity;
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

    .window-portal-glow {
      position: absolute;
      inset: 0;
      background: radial-gradient(ellipse at 50% 50%, rgba(255, 235, 195, 0.75) 0%, rgba(255, 210, 140, 0.25) 45%, transparent 75%);
      opacity: 0;
      pointer-events: none;
      mix-blend-mode: screen;
      z-index: 6;
      will-change: opacity;
    }

    /* LIVING ATMOSPHERE CANVAS */
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
      background: radial-gradient(circle at 50% 50%, transparent 68%, rgba(8, 6, 5, 0.40) 100%);
    }

    /* SUBTLE TOUR PROGRESS LINE */
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

    /* SUBTLE SCROLL HINT (Disappears immediately upon scrolling) */
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

  <!-- VIRTUAL SCROLL CONTAINER (DRIVES TIMELINE) -->
  <div class="scroll-container" id="scroll-container"></div>

  <!-- FIXED CINEMATIC VIEWPORT -->
  <main class="viewport-stage" id="viewport-stage">

    <div class="camera-rig" id="camera-rig">

      <!-- SCENE 1: PALACE FACADE ROOF & TWILIGHT SKY (main1.jpg) -->
      <section class="tour-scene" id="scene-1" style="opacity: 1; z-index: 1;">
        <div class="media-box" id="box-1">
          <img class="bg-img" src="img/main1.jpg" alt="Palace Facade Roof" id="img-1" />
        </div>
      </section>

      <!-- SCENE 2: PALACE COURTYARD & 3D ENTRANCE DOORS (main2_open.jpg + 3D doors) -->
      <section class="tour-scene" id="scene-2" style="z-index: 2;">
        <div class="media-box" id="box-2">
          <img class="bg-img" src="img/main2_open.jpg" alt="Palace Courtyard & Entrance" id="img-2" />
          <div class="door-assembly" id="door-assembly">
            <div class="door-leaf left" id="door-l"></div>
            <div class="door-leaf right" id="door-r"></div>
          </div>
        </div>
      </section>

      <!-- SCENE 3: GRAND RECEPTION LOBBY INTERIOR (reception_lobby.jpg) -->
      <section class="tour-scene" id="scene-3" style="z-index: 3;">
        <div class="media-box" id="box-3">
          <img class="bg-img" src="img/reception_lobby.jpg" alt="Grand Reception Lobby" id="img-3" />
        </div>
      </section>

      <!-- SCENE 4: ARCHED WINDOW WITH SHEER TRANSLUCENT CURTAINS (window_sheer.jpg) -->
      <section class="tour-scene" id="scene-4" style="z-index: 4;">
        <div class="media-box" id="box-4">
          <img class="bg-img" src="img/window_sheer.jpg" alt="Palace Window" id="img-4" />
          <div class="window-portal-glow" id="window-glow"></div>
          <div class="window-curtain-layer" id="window-curtain-layer">
            <div class="curtain-drape left" id="curtain-l"></div>
            <div class="curtain-drape right" id="curtain-r"></div>
          </div>
        </div>
      </section>

      <!-- SCENE 5: BANQUET NIGHT EXTERIOR ENTRANCE (ban1.webp) -->
      <section class="tour-scene" id="scene-5" style="z-index: 5;">
        <div class="media-box" id="box-5">
          <img class="bg-img" src="img/ban1.webp" alt="Banquet Night Entrance" id="img-5" />
        </div>
      </section>

      <!-- SCENE 6: BANQUET ARRIVAL HALLWAY (ban2.webp) -->
      <section class="tour-scene" id="scene-6" style="z-index: 6;">
        <div class="media-box" id="box-6">
          <img class="bg-img" src="img/ban2.webp" alt="Banquet Arrival Hallway" id="img-6" />
        </div>
      </section>

      <!-- SCENE 7: ROYAL ELEPHANT FLORAL WALKWAY (banq1.jpg) -->
      <section class="tour-scene" id="scene-7" style="z-index: 7;">
        <div class="media-box" id="box-7">
          <img class="bg-img" src="img/banq1.jpg" alt="Floral Walkway" id="img-7" />
        </div>
      </section>

      <!-- SCENE 8: GRAND CRYSTAL BALLROOM SIDE PERSPECTIVE (ban3.webp) -->
      <section class="tour-scene" id="scene-8" style="z-index: 8;">
        <div class="media-box" id="box-8">
          <img class="bg-img" src="img/ban3.webp" alt="Ballroom Side Perspective" id="img-8" />
        </div>
      </section>

      <!-- SCENE 9: GRAND BALLROOM CHANDELIERS & SEATING (banq2.jpg) -->
      <section class="tour-scene" id="scene-9" style="z-index: 9;">
        <div class="media-box" id="box-9">
          <img class="bg-img" src="img/banq2.jpg" alt="Grand Ballroom Chandeliers" id="img-9" />
        </div>
      </section>

      <!-- SCENE 10: BALLROOM CENTER AISLE PERSPECTIVE (ban4.webp) -->
      <section class="tour-scene" id="scene-10" style="z-index: 10;">
        <div class="media-box" id="box-10">
          <img class="bg-img" src="img/ban4.webp" alt="Center Aisle Perspective" id="img-10" />
        </div>
      </section>

      <!-- SCENE 11: CENTER AISLE CHANDELIER DIVE (banq3.jpg) -->
      <section class="tour-scene" id="scene-11" style="z-index: 11;">
        <div class="media-box" id="box-11">
          <img class="bg-img" src="img/banq3.jpg" alt="Center Aisle Dive" id="img-11" />
        </div>
      </section>

      <!-- SCENE 12: BALLROOM MANDAP OVERVIEW (ban6.webp) -->
      <section class="tour-scene" id="scene-12" style="z-index: 12;">
        <div class="media-box" id="box-12">
          <img class="bg-img" src="img/ban6.webp" alt="Mandap Overview" id="img-12" />
        </div>
      </section>

      <!-- SCENE 13: ROYAL MANDAP FLORAL PILLARS (ban5.webp) -->
      <section class="tour-scene" id="scene-13" style="z-index: 13;">
        <div class="media-box" id="box-13">
          <img class="bg-img" src="img/ban5.webp" alt="Mandap Floral Pillars" id="img-13" />
        </div>
      </section>

      <!-- SCENE 14: ROYAL WEDDING MANDAP FINALE (banq4.jpg) -->
      <section class="tour-scene" id="scene-14" style="z-index: 14;">
        <div class="media-box" id="box-14">
          <img class="bg-img" src="img/banq4.jpg" alt="Royal Wedding Mandap Finale" id="img-14" />
        </div>
      </section>

    </div>

    <!-- LIVING ATMOSPHERE (Canvas Petals & Sparkles) -->
    <canvas id="particles-canvas"></canvas>

    <!-- OPTICAL VIGNETTE -->
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

      // DOM Elements
      const scrollContainer = document.getElementById('scroll-container');
      const progressFill = document.getElementById('tour-progress-fill');
      const scrollHint = document.getElementById('scroll-hint');
      const cameraRig = document.getElementById('camera-rig');

      // 14 Scenes & Boxes
      const scenes = [];
      const boxes = [];
      for (let i = 1; i <= 14; i++) {
        scenes[i] = document.getElementById('scene-' + i);
        boxes[i] = document.getElementById('box-' + i);
      }

      const doorL = document.getElementById('door-l');
      const doorR = document.getElementById('door-r');
      const curtainL = document.getElementById('curtain-l');
      const curtainR = document.getElementById('curtain-r');
      const windowGlow = document.getElementById('window-glow');

      // Scroll State
      let maxScroll = 1;
      let targetScrollY = 0;
      let currentScrollY = 0;
      let scrollProgress = 0;
      let hasScrolled = false;

      // Aspect ratios for all 14 images:
      const imageRatios = {
        1: 1376 / 768,   // main1.jpg
        2: 1376 / 768,   // main2_open.jpg
        3: 1792 / 1008,  // reception_lobby.jpg
        4: 1024 / 1024,  // window_sheer.jpg
        5: 800 / 394,    // ban1.webp
        6: 800 / 800,    // ban2.webp
        7: 1024 / 1024,  // banq1.jpg
        8: 1000 / 1000,  // ban3.webp
        9: 1024 / 1024,  // banq2.jpg
        10: 750 / 1000,  // ban4.webp
        11: 896 / 1200,  // banq3.jpg
        12: 1000 / 1000, // ban6.webp
        13: 750 / 1000,  // ban5.webp
        14: 896 / 1200   // banq4.jpg
      };

      // Responsive aspect-ratio cover sizing
      function resizeMediaBoxes() {
        const vw = window.innerWidth;
        const vh = window.innerHeight;
        maxScroll = Math.max(1, scrollContainer.offsetHeight - vh);

        for (let i = 1; i <= 14; i++) {
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

      // Window Scroll Synchronization
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

      // Keyboard arrow keys
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

      // Math Helpers & Easing
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

      function easeInQuad(t) {
        return t * t;
      }

      // =========================================================================
      // VIRTUAL TOUR CHOREOGRAPHY ENGINE (14 CONTINUOUS STAGES)
      // =========================================================================
      function renderTour(p) {
        progressFill.style.width = (p * 100).toFixed(2) + '%';

        // -----------------------------------------------------------------------
        // STAGE 1: [0.00 -> 0.08] START AT main1.jpg (Roof pavilion, twilight sky, birds)
        //          Camera descends vertically down the palace facade into courtyard
        // -----------------------------------------------------------------------
        if (p <= 0.09) {
          scenes[1].style.display = 'flex';
          const t = norm(p, 0.00, 0.07);
          const st = easeInOutQuad(t);

          const scale = 1.0 + st * 0.14;
          const panY = -(st * 12.0); // Tilts / pans down facade
          boxes[1].style.transform = 'translate(-50%, -50%) translate3d(0, ' + panY + '%, 0) scale(' + scale + ')';

          const alpha = 1.0 - norm(p, 0.045, 0.08);
          scenes[1].style.opacity = alpha.toFixed(3);
        } else {
          scenes[1].style.opacity = '0';
          scenes[1].style.display = 'none';
        }

        // -----------------------------------------------------------------------
        // STAGE 2: [0.045 -> 0.17] main2.jpg PALACE COURTYARD & 3D DOOR OPENING
        //          Camera approaches grand entrance; double doors swing inward in 3D
        // -----------------------------------------------------------------------
        if (p >= 0.04 && p <= 0.18) {
          scenes[2].style.display = 'flex';

          const inAlpha = norm(p, 0.045, 0.08);
          const outAlpha = 1.0 - norm(p, 0.145, 0.175);
          scenes[2].style.opacity = Math.min(inAlpha, outAlpha).toFixed(3);

          // Push towards the entrance door:
          // Door center in main2.jpg: X=50.0%, Y=68.815%
          const pushProg = norm(p, 0.05, 0.16);
          const pushSmooth = easeInOutQuad(pushProg);
          const scale = 1.0 + pushSmooth * 3.6; // Deep push right to the threshold

          boxes[2].style.transformOrigin = '50.0% 68.815%';
          boxes[2].style.transform = 'translate(-50%, -50%) scale(' + scale + ')';

          // 3D Door Swing: from 0.085 to 0.14
          const doorProg = norm(p, 0.085, 0.14);
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
        // STAGE 3: [0.14 -> 0.24] RECEPTION LOBBY INTERIOR (reception_lobby.jpg)
        //          Gliding through doorway into grand chandelier palace lobby,
        //          then turning towards the grand arch window on the right
        // -----------------------------------------------------------------------
        if (p >= 0.135 && p <= 0.25) {
          scenes[3].style.display = 'flex';

          const inAlpha = norm(p, 0.14, 0.17);
          const outAlpha = 1.0 - norm(p, 0.21, 0.245);
          scenes[3].style.opacity = Math.min(inAlpha, outAlpha).toFixed(3);

          const pushProg = norm(p, 0.14, 0.24);
          const pushSmooth = easeInOutQuad(pushProg);

          // Fly into lobby and pan camera towards the right archway window
          const scale = 1.02 + pushSmooth * 0.40;
          const panX = -(pushSmooth * 14.0); // pans to the right window
          const panY = -(pushSmooth * 4.0);

          boxes[3].style.transform = 'translate(-50%, -50%) translate3d(' + panX + '%, ' + panY + '%, 0) scale(' + scale + ')';
        } else {
          scenes[3].style.opacity = '0';
          scenes[3].style.display = 'none';
        }

        // -----------------------------------------------------------------------
        // STAGE 4: [0.21 -> 0.30] ARCHED WINDOW & SHEER TRANSLUCENT CURTAINS
        //          Curtains billow and part in the breeze; camera punches out into night
        // -----------------------------------------------------------------------
        if (p >= 0.205 && p <= 0.31) {
          scenes[4].style.display = 'flex';

          const inAlpha = norm(p, 0.21, 0.245);
          const outAlpha = 1.0 - norm(p, 0.275, 0.305);
          scenes[4].style.opacity = Math.min(inAlpha, outAlpha).toFixed(3);

          const winProg = norm(p, 0.21, 0.30);
          const winSmooth = easeInOutQuad(winProg);

          // Zooms deep into window opening
          const scale = 1.02 + winSmooth * 1.6;
          boxes[4].style.transform = 'translate(-50%, -50%) scale(' + scale + ')';

          // Curtains billow and part sideways
          const curtainProg = norm(p, 0.22, 0.29);
          const curtainSmooth = easeInOutQuad(curtainProg);
          const partX = curtainSmooth * 75.0;

          curtainL.style.transform = 'translate3d(' + (-partX) + '%, 0, 0) scale(' + (1.0 + curtainSmooth * 0.15) + ')';
          curtainR.style.transform = 'translate3d(' + partX + '%, 0, 0) scale(' + (1.0 + curtainSmooth * 0.15) + ')';

          const glowAlpha = Math.sin(curtainProg * Math.PI) * 0.75;
          windowGlow.style.opacity = glowAlpha.toFixed(3);
        } else {
          scenes[4].style.opacity = '0';
          scenes[4].style.display = 'none';
        }

        // -----------------------------------------------------------------------
        // STAGE 5: [0.27 -> 0.38] BANQUET NIGHT EXTERIOR ENTRANCE (ban1.webp)
        //          Camera glides up illuminated steps towards glowing glass doors
        // -----------------------------------------------------------------------
        if (p >= 0.265 && p <= 0.39) {
          scenes[5].style.display = 'flex';

          const inAlpha = norm(p, 0.27, 0.305);
          const outAlpha = 1.0 - norm(p, 0.35, 0.385);
          scenes[5].style.opacity = Math.min(inAlpha, outAlpha).toFixed(3);

          const pushProg = norm(p, 0.27, 0.38);
          const pushSmooth = easeInOutQuad(pushProg);

          const scale = 1.01 + pushSmooth * 0.35;
          const panY = -(pushSmooth * 6.0);
          boxes[5].style.transform = 'translate(-50%, -50%) translate3d(0, ' + panY + '%, 0) scale(' + scale + ')';
        } else {
          scenes[5].style.opacity = '0';
          scenes[5].style.display = 'none';
        }

        // -----------------------------------------------------------------------
        // STAGE 6: [0.35 -> 0.46] ARRIVAL HALLWAY WITH PEACOCK & ELEPHANTS (ban2.webp)
        //          Entering the palace arrival corridor beneath glowing chandeliers
        // -----------------------------------------------------------------------
        if (p >= 0.345 && p <= 0.47) {
          scenes[6].style.display = 'flex';

          const inAlpha = norm(p, 0.35, 0.385);
          const outAlpha = 1.0 - norm(p, 0.43, 0.465);
          scenes[6].style.opacity = Math.min(inAlpha, outAlpha).toFixed(3);

          const pushProg = norm(p, 0.35, 0.46);
          const pushSmooth = easeInOutQuad(pushProg);

          const scale = 1.01 + pushSmooth * 0.30;
          boxes[6].style.transform = 'translate(-50%, -50%) scale(' + scale + ')';
        } else {
          scenes[6].style.opacity = '0';
          scenes[6].style.display = 'none';
        }

        // -----------------------------------------------------------------------
        // STAGE 7: [0.43 -> 0.54] ROYAL ELEPHANT FLORAL WALKWAY (banq1.jpg)
        //          Camera glides down geometric aisle, then dollies to the left
        // -----------------------------------------------------------------------
        if (p >= 0.425 && p <= 0.55) {
          scenes[7].style.display = 'flex';

          const inAlpha = norm(p, 0.43, 0.465);
          const outAlpha = 1.0 - norm(p, 0.505, 0.54);
          scenes[7].style.opacity = Math.min(inAlpha, outAlpha).toFixed(3);

          const pushProg = norm(p, 0.43, 0.53);
          const pushSmooth = easeInOutQuad(pushProg);
          const scale = 1.01 + pushSmooth * 0.28;

          // Camera sweeps left to connect to ballroom:
          const leftDolly = -(norm(p, 0.47, 0.54) * 22.0);
          boxes[7].style.transform = 'translate(-50%, -50%) translate3d(' + leftDolly + '%, 0, 0) scale(' + scale + ')';
        } else {
          scenes[7].style.opacity = '0';
          scenes[7].style.display = 'none';
        }

        // -----------------------------------------------------------------------
        // STAGE 8: [0.50 -> 0.61] GRAND CRYSTAL BALLROOM SIDE VIEW (ban3.webp)
        //          Entering the vast crystal ballroom from the side angle
        // -----------------------------------------------------------------------
        if (p >= 0.495 && p <= 0.62) {
          scenes[8].style.display = 'flex';

          const inAlpha = norm(p, 0.50, 0.535);
          const outAlpha = 1.0 - norm(p, 0.575, 0.61);
          scenes[8].style.opacity = Math.min(inAlpha, outAlpha).toFixed(3);

          const pushProg = norm(p, 0.50, 0.60);
          const pushSmooth = easeInOutQuad(pushProg);

          const enterX = (1.0 - norm(p, 0.50, 0.55)) * 18.0;
          const exitX = -(norm(p, 0.56, 0.61) * 10.0);
          const scale = 1.02 + pushSmooth * 0.22;

          boxes[8].style.transform = 'translate(-50%, -50%) translate3d(' + (enterX + exitX) + '%, 0, 0) scale(' + scale + ')';
        } else {
          scenes[8].style.opacity = '0';
          scenes[8].style.display = 'none';
        }

        // -----------------------------------------------------------------------
        // STAGE 9: [0.57 -> 0.68] GRAND BALLROOM CHANDELIERS & SEATING (banq2.jpg)
        //          Sweeping over the red seating towards the center
        // -----------------------------------------------------------------------
        if (p >= 0.565 && p <= 0.69) {
          scenes[9].style.display = 'flex';

          const inAlpha = norm(p, 0.57, 0.605);
          const outAlpha = 1.0 - norm(p, 0.645, 0.68);
          scenes[9].style.opacity = Math.min(inAlpha, outAlpha).toFixed(3);

          const pushProg = norm(p, 0.57, 0.67);
          const pushSmooth = easeInOutQuad(pushProg);

          const scale = 1.01 + pushSmooth * 0.25;
          const panX = -(norm(p, 0.57, 0.67) * 12.0);

          boxes[9].style.transform = 'translate(-50%, -50%) translate3d(' + panX + '%, 0, 0) scale(' + scale + ')';
        } else {
          scenes[9].style.opacity = '0';
          scenes[9].style.display = 'none';
        }

        // -----------------------------------------------------------------------
        // STAGE 10: [0.64 -> 0.75] BALLROOM CENTER AISLE PERSPECTIVE (ban4.webp)
        //           Camera rotates smoothly to align dead center down the grand aisle
        // -----------------------------------------------------------------------
        if (p >= 0.635 && p <= 0.76) {
          scenes[10].style.display = 'flex';

          const inAlpha = norm(p, 0.64, 0.675);
          const outAlpha = 1.0 - norm(p, 0.715, 0.75);
          scenes[10].style.opacity = Math.min(inAlpha, outAlpha).toFixed(3);

          const pushProg = norm(p, 0.64, 0.74);
          const pushSmooth = easeInOutQuad(pushProg);

          const scale = 1.02 + pushSmooth * 0.30;
          boxes[10].style.transform = 'translate(-50%, -50%) scale(' + scale + ')';
        } else {
          scenes[10].style.opacity = '0';
          scenes[10].style.display = 'none';
        }

        // -----------------------------------------------------------------------
        // STAGE 11: [0.71 -> 0.82] CENTER AISLE CHANDELIER DIVE (banq3.jpg)
        //           Fast, exhilarating push down the center aisle under chandeliers
        // -----------------------------------------------------------------------
        if (p >= 0.705 && p <= 0.83) {
          scenes[11].style.display = 'flex';

          const inAlpha = norm(p, 0.71, 0.745);
          const outAlpha = 1.0 - norm(p, 0.785, 0.82);
          scenes[11].style.opacity = Math.min(inAlpha, outAlpha).toFixed(3);

          const pushProg = norm(p, 0.71, 0.81);
          const pushSmooth = easeInOutQuad(pushProg);

          const scale = 1.0 + pushSmooth * 0.40;
          const panY = -(pushSmooth * 8.0);
          boxes[11].style.transform = 'translate(-50%, -50%) translate3d(0, ' + panY + '%, 0) scale(' + scale + ')';
        } else {
          scenes[11].style.opacity = '0';
          scenes[11].style.display = 'none';
        }

        // -----------------------------------------------------------------------
        // STAGE 12: [0.78 -> 0.89] BALLROOM MANDAP OVERVIEW (ban6.webp)
        //           Wide overview showing whole ballroom and the Mandap in the distance
        // -----------------------------------------------------------------------
        if (p >= 0.775 && p <= 0.90) {
          scenes[12].style.display = 'flex';

          const inAlpha = norm(p, 0.78, 0.815);
          const outAlpha = 1.0 - norm(p, 0.855, 0.89);
          scenes[12].style.opacity = Math.min(inAlpha, outAlpha).toFixed(3);

          const pushProg = norm(p, 0.78, 0.88);
          const pushSmooth = easeInOutQuad(pushProg);

          const scale = 1.02 + pushSmooth * 0.28;
          boxes[12].style.transform = 'translate(-50%, -50%) scale(' + scale + ')';
        } else {
          scenes[12].style.opacity = '0';
          scenes[12].style.display = 'none';
        }

        // -----------------------------------------------------------------------
        // STAGE 13: [0.85 -> 0.94] ROYAL MANDAP FLORAL PILLARS CLOSE-UP (ban5.webp)
        //           Approaching the red and white rose pillars of the royal stage
        // -----------------------------------------------------------------------
        if (p >= 0.845 && p <= 0.95) {
          scenes[13].style.display = 'flex';

          const inAlpha = norm(p, 0.85, 0.885);
          const outAlpha = 1.0 - norm(p, 0.915, 0.945);
          scenes[13].style.opacity = Math.min(inAlpha, outAlpha).toFixed(3);

          const pushProg = norm(p, 0.85, 0.94);
          const pushSmooth = easeInOutQuad(pushProg);

          const scale = 1.02 + pushSmooth * 0.25;
          boxes[13].style.transform = 'translate(-50%, -50%) scale(' + scale + ')';
        } else {
          scenes[13].style.opacity = '0';
          scenes[13].style.display = 'none';
        }

        // -----------------------------------------------------------------------
        // STAGE 14: [0.91 -> 1.00] ROYAL WEDDING MANDAP FINALE (banq4.jpg)
        //           Imperial finale: throne chairs, golden chandelier, and floral canopy
        // -----------------------------------------------------------------------
        if (p >= 0.905) {
          scenes[14].style.display = 'flex';

          const inAlpha = norm(p, 0.91, 0.945);
          scenes[14].style.opacity = inAlpha.toFixed(3);

          const mandapProg = norm(p, 0.91, 1.00);
          const mandapSmooth = easeOutCubic(mandapProg);

          const scale = 1.15 - (1.0 - mandapSmooth) * 0.15;
          const panY = (1.0 - mandapSmooth) * 3.5;

          boxes[14].style.transform = 'translate(-50%, -50%) translate3d(0, ' + panY + '%, 0) scale(' + scale + ')';
        } else {
          scenes[14].style.opacity = '0';
          scenes[14].style.display = 'none';
        }

        // Organic Drone Camera Banking & Elevation:
        const camRoll = Math.sin(p * Math.PI * 6.0) * 0.35;
        const camPitch = (p - 0.5) * 0.65;
        cameraRig.style.transform = 'rotateZ(' + camRoll.toFixed(2) + 'deg) rotateX(' + camPitch.toFixed(2) + 'deg)';
      }

      // =========================================================================
      // SMOOTH LERP INERTIA ANIMATION LOOP
      // =========================================================================
      function loop() {
        currentScrollY += (targetScrollY - currentScrollY) * 0.080;
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
      const PETAL_COUNT = 38;
      const petalPalette = [
        'rgba(248, 238, 224, 0.45)', // Champagne gold
        'rgba(255, 225, 215, 0.50)', // Soft rose
        'rgba(250, 244, 236, 0.40)', // Jasmine white
        'rgba(235, 208, 180, 0.35)'  // Amber glow
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

print(f"Successfully generated index.html ({len(html_code)} bytes)")
