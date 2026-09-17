import sys

html_code = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>The Royal Palace Resort - Virtual Tour</title>
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
      background-color: #0b0908;
      color: #f7f4ee;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      overflow-x: hidden;
      overscroll-behavior: none;
      user-select: none;
      -webkit-user-select: none;
    }

    /* SCROLL CONTAINER (1000vh FOR CINEMATIC MULTI-STAGE VIRTUAL TOUR) */
    .scroll-container {
      width: 100%;
      height: 1000vh;
      position: relative;
      pointer-events: none;
    }

    /* FIXED 100VH CINEMATIC VIEWPORT */
    .viewport-stage {
      position: fixed;
      inset: 0;
      width: 100vw;
      height: 100vh;
      height: 100dvh;
      overflow: hidden;
      background: #0b0908;
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
    }

    /* ASPECT-RATIO CONTROLLED MEDIA FRAMES */
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
       SCENE 1: STARTING HERO PALACE FACADE (main1.jpg: 1376x768)
       ========================================================================= */
    #scene-1 {
      opacity: 1;
      z-index: 2;
    }

    /* =========================================================================
       SCENE 2: PALACE COURTYARD & 3D ENTRANCE (main2.jpg: 1376x768)
       ========================================================================= */
    #scene-2 {
      opacity: 0;
      z-index: 3;
    }

    /* PIXEL-PERFECT 3D DOOR ASSEMBLY (1376x768 coordinates)
       Door: left 47.093%, top 64.323%, width 5.814%, height 11.198%
    */
    .door-assembly {
      position: absolute;
      left: 47.093%;
      top: 64.323%;
      width: 5.814%;
      height: 11.198%;
      perspective: 700px;
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
      box-shadow: 0 1px 6px rgba(0, 0, 0, 0.45);
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

    /* WINDOW ASSEMBLY (Right Arch Window: 1376x768 coordinates)
       Window: left 55.959%, top 62.500%, width 5.087%, height 13.021%
    */
    .window-assembly {
      position: absolute;
      left: 55.959%;
      top: 62.500%;
      width: 5.087%;
      height: 13.021%;
      z-index: 12;
      perspective: 900px;
      transform-style: preserve-3d;
      pointer-events: none;
      overflow: visible;
    }

    .window-curtain {
      position: absolute;
      top: -4%;
      width: 65%;
      height: 108%;
      background-size: 100% 100%;
      background-repeat: no-repeat;
      will-change: transform, opacity;
      pointer-events: none;
    }

    .window-curtain.left {
      left: 0;
      background-image: url('img/curtain_left.png');
      transform-origin: left top;
    }

    .window-curtain.right {
      right: 0;
      background-image: url('img/curtain_right.png');
      transform-origin: right top;
    }

    .window-light-halo {
      position: absolute;
      inset: -35%;
      background: radial-gradient(ellipse at 50% 50%, rgba(255, 238, 205, 0.8) 0%, rgba(255, 220, 160, 0.35) 50%, transparent 75%);
      opacity: 0;
      pointer-events: none;
      mix-blend-mode: screen;
    }

    /* =========================================================================
       SCENE 3: BANQUET ENTRANCE AT NIGHT (ban1.webp: 800x394)
       ========================================================================= */
    #scene-3 {
      opacity: 0;
      z-index: 4;
    }

    /* =========================================================================
       SCENE 4: FLORAL ARRIVAL WALKWAY (banq1.jpg: 1024x1024)
       ========================================================================= */
    #scene-4 {
      opacity: 0;
      z-index: 5;
    }

    /* =========================================================================
       SCENE 5: GRAND CRYSTAL BALLROOM (banq2.jpg: 1024x1024)
       ========================================================================= */
    #scene-5 {
      opacity: 0;
      z-index: 6;
    }

    /* =========================================================================
       SCENE 6: BALLROOM OVERVIEW TOWARDS MANDAP (ban6.webp: 1000x1000)
       ========================================================================= */
    #scene-6 {
      opacity: 0;
      z-index: 7;
    }

    /* =========================================================================
       SCENE 7: CENTER AISLE CHANDELIER PUSH (banq3.jpg: 896x1200)
       ========================================================================= */
    #scene-7 {
      opacity: 0;
      z-index: 8;
    }

    /* =========================================================================
       SCENE 8: ROYAL WEDDING MANDAP FINALE (banq4.jpg: 896x1200)
       ========================================================================= */
    #scene-8 {
      opacity: 0;
      z-index: 9;
    }

    /* AMBIENT LIVING PARTICLES (Pastel Rose & Champagne Petals) */
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
      background: radial-gradient(circle at 50% 50%, transparent 68%, rgba(11, 9, 8, 0.45) 100%);
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
      box-shadow: 0 0 8px rgba(230, 200, 175, 0.6);
      will-change: width;
    }

    /* SUBTLE SCROLL HINT */
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

      <!-- SCENE 1: STARTING PALACE FACADE (main1.jpg) -->
      <section class="tour-scene" id="scene-1">
        <div class="media-box" id="box-1">
          <img class="bg-img" src="img/main1.jpg" alt="The Royal Palace Facade" id="img-1" />
        </div>
      </section>

      <!-- SCENE 2: PALACE COURTYARD & 3D DOORWAY (main2_open.jpg + 3D doors) -->
      <section class="tour-scene" id="scene-2">
        <div class="media-box" id="box-2">
          <!-- Image with the open reception lobby inside the door opening -->
          <img class="bg-img" src="img/main2_open.jpg" alt="Courtyard Entrance" id="img-2" />

          <!-- Pixel-perfect 3D double doors covering the open door cavity -->
          <div class="door-assembly" id="door-assembly">
            <div class="door-leaf left" id="door-l"></div>
            <div class="door-leaf right" id="door-r"></div>
          </div>

          <!-- Big Window with translucent sheer curtains -->
          <div class="window-assembly" id="window-assembly">
            <div class="window-light-halo" id="window-halo"></div>
            <div class="window-curtain left" id="curtain-l"></div>
            <div class="window-curtain right" id="curtain-r"></div>
          </div>
        </div>
      </section>

      <!-- SCENE 3: GRAND BANQUET ENTRANCE AT NIGHT (ban1.webp) -->
      <section class="tour-scene" id="scene-3">
        <div class="media-box" id="box-3">
          <img class="bg-img" src="img/ban1.webp" alt="Banquet Grand Entrance" id="img-3" />
        </div>
      </section>

      <!-- SCENE 4: FLORAL ARRIVAL WALKWAY (banq1.jpg) -->
      <section class="tour-scene" id="scene-4">
        <div class="media-box" id="box-4">
          <img class="bg-img" src="img/banq1.jpg" alt="Royal Elephant Floral Walkway" id="img-4" />
        </div>
      </section>

      <!-- SCENE 5: GRAND CRYSTAL BALLROOM (banq2.jpg) -->
      <section class="tour-scene" id="scene-5">
        <div class="media-box" id="box-5">
          <img class="bg-img" src="img/banq2.jpg" alt="Grand Ballroom Chandeliers" id="img-5" />
        </div>
      </section>

      <!-- SCENE 6: BALLROOM OVERVIEW TOWARDS MANDAP (ban6.webp) -->
      <section class="tour-scene" id="scene-6">
        <div class="media-box" id="box-6">
          <img class="bg-img" src="img/ban6.webp" alt="Grand Ballroom Mandap View" id="img-6" />
        </div>
      </section>

      <!-- SCENE 7: CENTER AISLE CHANDELIER PUSH (banq3.jpg) -->
      <section class="tour-scene" id="scene-7">
        <div class="media-box" id="box-7">
          <img class="bg-img" src="img/banq3.jpg" alt="Ballroom Center Aisle" id="img-7" />
        </div>
      </section>

      <!-- SCENE 8: ROYAL WEDDING MANDAP FINALE (banq4.jpg) -->
      <section class="tour-scene" id="scene-8">
        <div class="media-box" id="box-8">
          <img class="bg-img" src="img/banq4.jpg" alt="Royal Wedding Mandap" id="img-8" />
        </div>
      </section>

    </div>

    <!-- LIVING ATMOSPHERE CANVAS -->
    <canvas id="particles-canvas"></canvas>

    <!-- CINEMATIC VIGNETTE -->
    <div class="cinema-vignette"></div>

    <!-- SUBTLE SCROLL HINT -->
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

      const scene1 = document.getElementById('scene-1');
      const box1 = document.getElementById('box-1');
      const scene2 = document.getElementById('scene-2');
      const box2 = document.getElementById('box-2');
      const doorL = document.getElementById('door-l');
      const doorR = document.getElementById('door-r');
      const windowHalo = document.getElementById('window-halo');
      const curtainL = document.getElementById('curtain-l');
      const curtainR = document.getElementById('curtain-r');

      const scene3 = document.getElementById('scene-3');
      const box3 = document.getElementById('box-3');
      const scene4 = document.getElementById('scene-4');
      const box4 = document.getElementById('box-4');
      const scene5 = document.getElementById('scene-5');
      const box5 = document.getElementById('box-5');
      const scene6 = document.getElementById('scene-6');
      const box6 = document.getElementById('box-6');
      const scene7 = document.getElementById('scene-7');
      const box7 = document.getElementById('box-7');
      const scene8 = document.getElementById('scene-8');
      const box8 = document.getElementById('box-8');

      // Scroll State
      let maxScroll = 1;
      let targetScrollY = 0;
      let currentScrollY = 0;
      let scrollProgress = 0;
      let hasScrolled = false;

      // Responsive aspect-ratio cover sizing
      function resizeMediaBoxes() {
        const vw = window.innerWidth;
        const vh = window.innerHeight;
        maxScroll = Math.max(1, scrollContainer.offsetHeight - vh);

        const targets = [
          { el: box1, ratio: 1376 / 768 },
          { el: box2, ratio: 1376 / 768 },
          { el: box3, ratio: 800 / 394 },
          { el: box4, ratio: 1024 / 1024 },
          { el: box5, ratio: 1024 / 1024 },
          { el: box6, ratio: 1000 / 1000 },
          { el: box7, ratio: 896 / 1200 },
          { el: box8, ratio: 896 / 1200 }
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

      resizeMediaBoxes();
      window.addEventListener('resize', resizeMediaBoxes, { passive: true });

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
          targetScrollY = Math.min(maxScroll, targetScrollY + window.innerHeight * 0.40);
        } else if (e.key === 'ArrowUp' || e.key === 'PageUp') {
          targetScrollY = Math.max(0, targetScrollY - window.innerHeight * 0.40);
        } else if (e.key === 'Home') {
          targetScrollY = 0;
        } else if (e.key === 'End') {
          targetScrollY = maxScroll;
        }
      });

      // Easing Utilities
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
      // VIRTUAL TOUR CHOREOGRAPHY ENGINE (ALL 10 ASSETS IN CONTINUOUS SEQUENCE)
      // =========================================================================
      function renderTour(p) {
        progressFill.style.width = (p * 100).toFixed(2) + '%';

        // -----------------------------------------------------------------------
        // STAGE 1: [0.00 -> 0.16] START AT main1.jpg (Twilight sky, cupola, birds)
        //          TILTS DOWN AND CONNECTS INTO main2.jpg
        // -----------------------------------------------------------------------
        if (p <= 0.18) {
          scene1.style.display = 'flex';
          const t1 = norm(p, 0.00, 0.14);
          const st1 = easeInOutQuad(t1);

          // Camera descends down facade: starts at top chhatri, moves down
          const scale1 = 1.0 + st1 * 0.18;
          const panY1 = -(st1 * 14.0); // Tilts down
          box1.style.transform = 'translate(-50%, -50%) translate3d(0, ' + panY1 + '%, 0) scale(' + scale1 + ')';

          const outAlpha1 = 1.0 - norm(p, 0.08, 0.16);
          scene1.style.opacity = outAlpha1.toFixed(3);
        } else {
          scene1.style.opacity = '0';
          scene1.style.display = 'none';
        }

        // -----------------------------------------------------------------------
        // STAGE 2: [0.08 -> 0.36] main2.jpg COURTYARD, ZOOM TO ENTRANCE,
        //          3D DOORS OPEN & RECEPTION LOBBY REVEALED
        //          THEN CAMERA PANS TO RIGHT ARCH WINDOW WITH TRANSLUCENT CURTAINS
        // -----------------------------------------------------------------------
        if (p >= 0.07 && p <= 0.38) {
          scene2.style.display = 'flex';

          const inAlpha2 = norm(p, 0.08, 0.15);
          const outAlpha2 = 1.0 - norm(p, 0.32, 0.37);
          scene2.style.opacity = Math.min(inAlpha2, outAlpha2).toFixed(3);

          // Camera motion:
          // Part A: Push towards entrance doors (dead center X: 50%, Y: 70%)
          // Part B: Pan to right window (X: 58.5%, Y: 69%)
          const pushDoor = norm(p, 0.10, 0.24);
          const pushDoorSmooth = easeInOutQuad(pushDoor);

          // Door opening progression: 0.18 to 0.27
          const doorProg = norm(p, 0.18, 0.27);
          const doorSmooth = easeInOutQuad(doorProg);

          // Door leaves swing open in 3D:
          const leftAngle = -(doorSmooth * 82.0);
          const rightAngle = doorSmooth * 82.0;
          doorL.style.transform = 'rotateY(' + leftAngle + 'deg)';
          doorR.style.transform = 'rotateY(' + rightAngle + 'deg)';

          // Part B: Pan right to arched window with curtains (0.24 to 0.36)
          const panWindow = norm(p, 0.24, 0.36);
          const panWindowSmooth = easeInOutQuad(panWindow);

          // Transform center & scale
          // While pushing toward doors, center is 50% 70%
          // As we pan to window, camera shifts right by -18% and zooms deeper
          const totalScale = 1.0 + pushDoorSmooth * 1.8 + panWindowSmooth * 3.5;
          const panX = -(panWindowSmooth * 20.0);
          const panY = -(pushDoorSmooth * 8.0) - (panWindowSmooth * 2.0);

          box2.style.transform = 'translate(-50%, -50%) translate3d(' + panX + '%, ' + panY + '%, 0) scale(' + totalScale + ')';
          box2.style.transformOrigin = '50% 69.9%'; // Centered on the entrance door!

          // Window curtains billow & part in 3D (0.27 to 0.36)
          const curtainProg = norm(p, 0.27, 0.36);
          const curtainSmooth = smoothstep(curtainProg);
          const partPx = curtainSmooth * 85.0;

          curtainL.style.transform = 'translate3d(' + (-partPx) + '%, 0, 0) scale(' + (1 + curtainSmooth * 0.25) + ')';
          curtainR.style.transform = 'translate3d(' + partPx + '%, 0, 0) scale(' + (1 + curtainSmooth * 0.25) + ')';

          const curtainAlpha = 1.0 - norm(p, 0.31, 0.36);
          curtainL.style.opacity = curtainAlpha.toFixed(3);
          curtainR.style.opacity = curtainAlpha.toFixed(3);
          windowHalo.style.opacity = (curtainSmooth * (1.0 - norm(p, 0.33, 0.37))).toFixed(3);
        } else {
          scene2.style.opacity = '0';
          scene2.style.display = 'none';
        }

        // -----------------------------------------------------------------------
        // STAGE 3: [0.33 -> 0.46] CAMERA PASSES THROUGH WINDOW INTO ban1.webp
        //          (Grand palace entrance at night with chandelier & candelabras)
        // -----------------------------------------------------------------------
        if (p >= 0.32 && p <= 0.48) {
          scene3.style.display = 'flex';

          const inAlpha3 = norm(p, 0.34, 0.39);
          const outAlpha3 = 1.0 - norm(p, 0.43, 0.48);
          scene3.style.opacity = Math.min(inAlpha3, outAlpha3).toFixed(3);

          const push3 = norm(p, 0.33, 0.46);
          const push3Smooth = easeInOutQuad(push3);

          // Camera glides up the steps towards the illuminated glass doors
          const scale3 = 1.02 + push3Smooth * 0.35;
          const panY3 = -(push3Smooth * 8.0);
          box3.style.transform = 'translate(-50%, -50%) translate3d(0, ' + panY3 + '%, 0) scale(' + scale3 + ')';
        } else {
          scene3.style.opacity = '0';
          scene3.style.display = 'none';
        }

        // -----------------------------------------------------------------------
        // STAGE 4: [0.44 -> 0.60] PASSING DOORS INTO banq1.jpg (Floral Arrival Walkway)
        //          THEN CAMERA DOLLIES TO THE LEFT
        // -----------------------------------------------------------------------
        if (p >= 0.43 && p <= 0.62) {
          scene4.style.display = 'flex';

          const inAlpha4 = norm(p, 0.45, 0.50);
          const outAlpha4 = 1.0 - norm(p, 0.56, 0.61);
          scene4.style.opacity = Math.min(inAlpha4, outAlpha4).toFixed(3);

          const push4 = norm(p, 0.44, 0.58);
          const push4Smooth = easeInOutQuad(push4);
          const scale4 = 1.0 + push4Smooth * 0.30;

          // As it reaches end of walkway, camera dollies to the left:
          // "then camera moves directly to left and connect banq2.jpg"
          const leftDolly = -(norm(p, 0.52, 0.61) * 26.0);

          box4.style.transform = 'translate(-50%, -50%) translate3d(' + leftDolly + '%, 0, 0) scale(' + scale4 + ')';
        } else {
          scene4.style.opacity = '0';
          scene4.style.display = 'none';
        }

        // -----------------------------------------------------------------------
        // STAGE 5: [0.57 -> 0.72] GRAND CRYSTAL BALLROOM SIDE ANGLE (banq2.jpg)
        // -----------------------------------------------------------------------
        if (p >= 0.56 && p <= 0.74) {
          scene5.style.display = 'flex';

          const inAlpha5 = norm(p, 0.58, 0.63);
          const outAlpha5 = 1.0 - norm(p, 0.68, 0.73);
          scene5.style.opacity = Math.min(inAlpha5, outAlpha5).toFixed(3);

          // Sweeps in from right as camera yaws left
          const sweep5 = norm(p, 0.57, 0.71);
          const sweep5Smooth = easeInOutQuad(sweep5);

          const enterX = (1.0 - norm(p, 0.57, 0.64)) * 20.0;
          const exitX = -(norm(p, 0.65, 0.73) * 12.0);
          const posX5 = enterX + exitX;
          const scale5 = 1.02 + sweep5Smooth * 0.20;

          box5.style.transform = 'translate(-50%, -50%) translate3d(' + posX5 + '%, 0, 0) scale(' + scale5 + ')';
        } else {
          scene5.style.opacity = '0';
          scene5.style.display = 'none';
        }

        // -----------------------------------------------------------------------
        // STAGE 6: [0.69 -> 0.83] BALLROOM OVERVIEW SHOWING MANDAP AHEAD (ban6.webp)
        // -----------------------------------------------------------------------
        if (p >= 0.68 && p <= 0.84) {
          scene6.style.display = 'flex';

          const inAlpha6 = norm(p, 0.70, 0.75);
          const outAlpha6 = 1.0 - norm(p, 0.80, 0.84);
          scene6.style.opacity = Math.min(inAlpha6, outAlpha6).toFixed(3);

          const push6 = norm(p, 0.69, 0.82);
          const push6Smooth = easeInOutQuad(push6);

          const scale6 = 1.02 + push6Smooth * 0.25;
          box6.style.transform = 'translate(-50%, -50%) scale(' + scale6 + ')';
        } else {
          scene6.style.opacity = '0';
          scene6.style.display = 'none';
        }

        // -----------------------------------------------------------------------
        // STAGE 7: [0.79 -> 0.93] CENTER AISLE DIVE UNDER CHANDELIERS (banq3.jpg)
        // -----------------------------------------------------------------------
        if (p >= 0.78 && p <= 0.94) {
          scene7.style.display = 'flex';

          const inAlpha7 = norm(p, 0.80, 0.85);
          const outAlpha7 = 1.0 - norm(p, 0.90, 0.94);
          scene7.style.opacity = Math.min(inAlpha7, outAlpha7).toFixed(3);

          const aisleProg = norm(p, 0.80, 0.93);
          const aisleSmooth = easeInOutQuad(aisleProg);

          // Fast push down aisle towards royal stage
          const scale7 = 1.0 + aisleSmooth * 0.45;
          const panY7 = -(aisleSmooth * 9.0);

          box7.style.transform = 'translate(-50%, -50%) translate3d(0, ' + panY7 + '%, 0) scale(' + scale7 + ')';
        } else {
          scene7.style.opacity = '0';
          scene7.style.display = 'none';
        }

        // -----------------------------------------------------------------------
        // STAGE 8: [0.89 -> 1.00] ROYAL WEDDING MANDAP FINALE ARRIVAL (banq4.jpg)
        // -----------------------------------------------------------------------
        if (p >= 0.88) {
          scene8.style.display = 'flex';

          const inAlpha8 = norm(p, 0.89, 0.95);
          scene8.style.opacity = inAlpha8.toFixed(3);

          const mandapProg = norm(p, 0.89, 1.00);
          const mandapSmooth = easeOutCubic(mandapProg);

          // Decelerates smoothly into royal throne hover
          const scale8 = 1.18 - (1.0 - mandapSmooth) * 0.18;
          const panY8 = (1.0 - mandapSmooth) * 4.0;

          box8.style.transform = 'translate(-50%, -50%) translate3d(0, ' + panY8 + '%, 0) scale(' + scale8 + ')';
        } else {
          scene8.style.opacity = '0';
          scene8.style.display = 'none';
        }

        // Subtle 3D virtual tour camera banking for organic human movement
        const camRoll = Math.sin(p * Math.PI * 4.5) * 0.40;
        const camPitch = (p - 0.5) * 0.8;
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
    f.write(html_code.strip())

print("SUCCESS: index.html regenerated with ALL 10 assets & pixel-perfect door alignment!")
