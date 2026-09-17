import sys

html_code = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>The Royal Palace Resort</title>
  <style>
    /* RESET & BASE */
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
      background-color: #12100e;
      color: #f6f3ee;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      overflow-x: hidden;
      overscroll-behavior: none;
      user-select: none;
      -webkit-user-select: none;
    }

    /* VIRTUAL SCROLL TRACK */
    .scroll-track {
      width: 100%;
      height: 750vh;
      position: relative;
      pointer-events: none;
    }

    /* FIXED CINEMATIC VIEWPORT (100vh / 100dvh) */
    .cinema-stage {
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      height: 100dvh;
      overflow: hidden;
      background: #110f0d;
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
    .scene {
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      display: flex;
      align-items: center;
      justify-content: center;
      pointer-events: none;
      will-change: transform, opacity;
      transform-origin: center center;
    }

    /* PERFECT ASPECT-LOCKED MEDIA WRAPPER */
    /* Ensures door and window coordinates stay locked down to the sub-pixel on all screens */
    .media-wrapper {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      will-change: transform;
      transform-style: preserve-3d;
    }

    .media-photo {
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      object-fit: fill;
      display: block;
      pointer-events: none;
    }

    /* SCENE SPECIFICS */
    #scene-1 .media-photo {
      object-fit: cover;
      object-position: center 30%;
    }

    #scene-2 {
      opacity: 0;
    }

    /* ENTRANCE DOORS OVERLAY (Positioned precisely on main2.jpg: 1376x768) */
    .door-portal {
      position: absolute;
      top: 64.32%;
      left: 47.09%;
      width: 5.81%;
      height: 11.20%;
      perspective: 800px;
      transform-style: preserve-3d;
      z-index: 5;
      pointer-events: none;
    }

    /* Warm interior hallway glow behind doors */
    .door-interior-glow {
      position: absolute;
      inset: 0;
      background: radial-gradient(ellipse at center, rgba(255, 215, 140, 0.95) 0%, rgba(210, 145, 60, 0.85) 55%, rgba(45, 25, 10, 0.98) 100%);
      box-shadow: 0 0 25px rgba(255, 210, 130, 0.8);
      opacity: 0;
      border-radius: 2px;
      overflow: hidden;
    }

    .door-interior-glow::after {
      content: '';
      position: absolute;
      bottom: 0;
      left: 15%;
      right: 15%;
      height: 70%;
      background: linear-gradient(to top, rgba(255, 248, 220, 0.9), transparent);
    }

    .door-leaf {
      position: absolute;
      top: 0;
      width: 50%;
      height: 100%;
      background-size: cover;
      background-position: center;
      transform-style: preserve-3d;
      will-change: transform;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.4);
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

    /* WINDOW & CURTAINS CONTAINER */
    .window-portal {
      position: absolute;
      top: 62.5%;
      left: 55.96%;
      width: 5.09%;
      height: 13.02%;
      z-index: 6;
      pointer-events: none;
      overflow: visible;
      perspective: 900px;
    }

    .curtain-drape {
      position: absolute;
      top: -5%;
      width: 65%;
      height: 110%;
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

    .window-light-beam {
      position: absolute;
      inset: -30%;
      background: radial-gradient(ellipse at 50% 50%, rgba(255, 238, 205, 0.7) 0%, rgba(255, 225, 175, 0.35) 45%, transparent 75%);
      opacity: 0;
      pointer-events: none;
      mix-blend-mode: screen;
    }

    /* SCENES 3 to 6 */
    #scene-3, #scene-4, #scene-5, #scene-6 {
      opacity: 0;
    }

    /* AMBIENT PARTICLES (Pastel Rose & Champagne Petals) */
    #ambient-canvas {
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      pointer-events: none;
      z-index: 10;
    }

    /* CINEMA OPTICAL VIGNETTE (No blur, soft warm optical vignette) */
    .cinema-vignette {
      position: absolute;
      inset: 0;
      pointer-events: none;
      z-index: 9;
      background: radial-gradient(circle at 50% 50%, transparent 65%, rgba(18, 14, 12, 0.4) 100%);
    }

    /* MINIMAL PROGRESS BAR AT BOTTOM */
    .flight-progress-track {
      position: fixed;
      bottom: 0;
      left: 0;
      width: 100%;
      height: 3px;
      background: rgba(255, 245, 235, 0.08);
      z-index: 50;
      pointer-events: none;
    }

    .flight-progress-fill {
      height: 100%;
      width: 0%;
      background: linear-gradient(90deg, #d8baa1 0%, #f4e8db 50%, #e2c2a9 100%);
      box-shadow: 0 0 8px rgba(230, 200, 175, 0.6);
      will-change: width;
    }

    /* CONTROLS (Discreet bottom pills) */
    .controls-container {
      position: fixed;
      bottom: 24px;
      right: 28px;
      z-index: 60;
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .drone-control-pill {
      display: flex;
      align-items: center;
      gap: 9px;
      padding: 8px 18px;
      border-radius: 40px;
      background: rgba(26, 22, 19, 0.50);
      border: 1px solid rgba(240, 230, 220, 0.20);
      cursor: pointer;
      transition: all 0.3s ease;
      color: rgba(245, 238, 230, 0.88);
      font-size: 11px;
      letter-spacing: 0.14em;
      text-transform: uppercase;
      pointer-events: auto;
    }

    .drone-control-pill:hover {
      background: rgba(45, 38, 33, 0.8);
      border-color: rgba(240, 230, 220, 0.4);
      color: #ffffff;
      transform: translateY(-1px);
    }

    .drone-pill-dot {
      width: 7px;
      height: 7px;
      border-radius: 50%;
      background: #e2c0a5;
      box-shadow: 0 0 6px rgba(226, 192, 165, 0.8);
      transition: background 0.3s ease;
    }

    .drone-control-pill.active .drone-pill-dot {
      background: #a2e8ae;
      box-shadow: 0 0 8px rgba(162, 232, 174, 0.9);
      animation: pulse-dot 1.5s infinite ease-in-out;
    }

    @keyframes pulse-dot {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.5; transform: scale(0.85); }
    }

    /* SCROLL HINT */
    .scroll-hint {
      position: fixed;
      bottom: 28px;
      left: 50%;
      transform: translateX(-50%);
      z-index: 60;
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
      animation: scroll-bob 2s infinite ease-in-out;
    }

    @keyframes scroll-bob {
      0% { transform: scaleY(0); transform-origin: top; }
      50% { transform: scaleY(1); transform-origin: top; }
      50.1% { transform: scaleY(1); transform-origin: bottom; }
      100% { transform: scaleY(0); transform-origin: bottom; }
    }

    /* VIDEO OVERLAY MODAL (When user clicks 'Watch Video') */
    .video-modal {
      position: fixed;
      inset: 0;
      background: #000;
      z-index: 100;
      display: none;
      align-items: center;
      justify-content: center;
    }
    .video-modal.active {
      display: flex;
    }
    .video-modal video {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }
    .video-close-btn {
      position: absolute;
      top: 24px;
      right: 28px;
      z-index: 110;
      background: rgba(20, 18, 16, 0.6);
      border: 1px solid rgba(255, 255, 255, 0.25);
      color: #fff;
      padding: 8px 16px;
      border-radius: 30px;
      font-size: 11px;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      cursor: pointer;
      transition: background 0.3s;
    }
    .video-close-btn:hover {
      background: rgba(50, 45, 40, 0.9);
    }
  </style>
</head>
<body>

  <!-- VIRTUAL SCROLL CONTAINER -->
  <div class="scroll-track" id="scroll-track"></div>

  <!-- FIXED CINEMATIC VIEWPORT -->
  <main class="cinema-stage" id="cinema-stage">

    <div class="camera-rig" id="camera-rig">

      <!-- SCENE 1: FACADE & TWILIGHT SKY (main1.jpg) -->
      <section class="scene" id="scene-1">
        <div class="media-wrapper" id="wrapper-1">
          <img class="media-photo" src="img/main1.jpg" alt="Palace Facade and Twilight Sky" id="photo-1" />
        </div>
      </section>

      <!-- SCENE 2: COURTYARD, ENTRANCE & WINDOW (main2.jpg) -->
      <section class="scene" id="scene-2">
        <div class="media-wrapper" id="wrapper-2">
          <img class="media-photo" src="img/main2.jpg" alt="Courtyard Entrance" id="photo-2" />

          <!-- 3D OPENING DOUBLE DOORS -->
          <div class="door-portal" id="door-portal">
            <div class="door-interior-glow" id="door-glow"></div>
            <div class="door-leaf left" id="door-leaf-left"></div>
            <div class="door-leaf right" id="door-leaf-right"></div>
          </div>

          <!-- BIG WINDOW & TRANSLUCENT PASTEL CURTAINS -->
          <div class="window-portal" id="window-portal">
            <div class="window-light-beam" id="window-beam"></div>
            <div class="curtain-drape left" id="curtain-left"></div>
            <div class="curtain-drape right" id="curtain-right"></div>
          </div>
        </div>
      </section>

      <!-- SCENE 3: FLORAL ARRIVAL HALL (banq1.jpg) -->
      <section class="scene" id="scene-3">
        <div class="media-wrapper" id="wrapper-3">
          <img class="media-photo" src="img/banq1.jpg" alt="Banquet Arrival Pavilion" id="photo-3" />
        </div>
      </section>

      <!-- SCENE 4: GRAND BALLROOM SIDE (banq2.jpg) -->
      <section class="scene" id="scene-4">
        <div class="media-wrapper" id="wrapper-4">
          <img class="media-photo" src="img/banq2.jpg" alt="Grand Ballroom Chandelier Perspective" id="photo-4" />
        </div>
      </section>

      <!-- SCENE 5: CENTER AISLE PUSH (banq3.jpg) -->
      <section class="scene" id="scene-5">
        <div class="media-wrapper" id="wrapper-5">
          <img class="media-photo" src="img/banq3.jpg" alt="Imperial Ballroom Center Aisle" id="photo-5" />
        </div>
      </section>

      <!-- SCENE 6: ROYAL MANDAP FINALE (banq4.jpg) -->
      <section class="scene" id="scene-6">
        <div class="media-wrapper" id="wrapper-6">
          <img class="media-photo" src="img/banq4.jpg" alt="Royal Wedding Mandap" id="photo-6" />
        </div>
      </section>

    </div>

    <!-- AMBIENT LIVING PARTICLES -->
    <canvas id="ambient-canvas"></canvas>

    <!-- CINEMA OPTICAL VIGNETTE -->
    <div class="cinema-vignette"></div>

    <!-- SUBTLE SCROLL HINT -->
    <div class="scroll-hint" id="scroll-hint">
      <div class="scroll-hint-line"></div>
    </div>

    <!-- TIMELINE PROGRESS BAR -->
    <div class="flight-progress-track">
      <div class="flight-progress-fill" id="flight-progress-fill"></div>
    </div>

    <!-- CONTROLS CONTAINER -->
    <div class="controls-container">
      <button class="drone-control-pill" id="video-btn">
        <div class="drone-pill-dot" style="background: #e2a5a5;"></div>
        <span>Watch Video</span>
      </button>

      <button class="drone-control-pill" id="autopilot-btn">
        <div class="drone-pill-dot"></div>
        <span id="autopilot-label">Drone Autopilot</span>
      </button>
    </div>

    <!-- VIDEO MODAL -->
    <div class="video-modal" id="video-modal">
      <button class="video-close-btn" id="video-close-btn">Close Video [Esc]</button>
      <video id="drone-video-player" src="resort_drone_flight.mp4" playsinline controls></video>
    </div>

  </main>

  <script>
    (function () {
      'use strict';

      const scrollTrack = document.getElementById('scroll-track');
      const progressFill = document.getElementById('flight-progress-fill');
      const scrollHint = document.getElementById('scroll-hint');
      const autopilotBtn = document.getElementById('autopilot-btn');
      const autopilotLabel = document.getElementById('autopilot-label');
      const videoBtn = document.getElementById('video-btn');
      const videoModal = document.getElementById('video-modal');
      const videoCloseBtn = document.getElementById('video-close-btn');
      const droneVideoPlayer = document.getElementById('drone-video-player');

      // Elements
      const cameraRig = document.getElementById('camera-rig');
      const scene1 = document.getElementById('scene-1');
      const wrapper1 = document.getElementById('wrapper-1');
      const scene2 = document.getElementById('scene-2');
      const wrapper2 = document.getElementById('wrapper-2');
      const doorGlow = document.getElementById('door-glow');
      const doorLeft = document.getElementById('door-leaf-left');
      const doorRight = document.getElementById('door-leaf-right');
      const windowBeam = document.getElementById('window-beam');
      const curtainLeft = document.getElementById('curtain-left');
      const curtainRight = document.getElementById('curtain-right');
      const scene3 = document.getElementById('scene-3');
      const wrapper3 = document.getElementById('wrapper-3');
      const scene4 = document.getElementById('scene-4');
      const wrapper4 = document.getElementById('wrapper-4');
      const scene5 = document.getElementById('scene-5');
      const wrapper5 = document.getElementById('wrapper-5');
      const scene6 = document.getElementById('scene-6');
      const wrapper6 = document.getElementById('wrapper-6');

      // Scroll State
      let targetScrollY = 0;
      let currentScrollY = 0;
      let maxScroll = 1;
      let scrollProgress = 0;
      let isAutopilot = false;
      let autopilotSpeed = 0.00062;
      let hasScrolledOnce = false;

      // Aspect Ratio Fit Utility
      function layoutMediaWrappers() {
        const sw = window.innerWidth;
        const sh = window.innerHeight;
        maxScroll = Math.max(1, scrollTrack.offsetHeight - sh);

        // Aspect ratios:
        // main1: 1376 / 768
        // main2: 1376 / 768
        // banq1: 1024 / 1024 (1.0)
        // banq2: 1024 / 1024 (1.0)
        // banq3: 896 / 1200 (0.7467)
        // banq4: 896 / 1200 (0.7467)
        const ratios = [
          { el: wrapper1, r: 1376 / 768 },
          { el: wrapper2, r: 1376 / 768 },
          { el: wrapper3, r: 1024 / 1024 },
          { el: wrapper4, r: 1024 / 1024 },
          { el: wrapper5, r: 896 / 1200 },
          { el: wrapper6, r: 896 / 1200 }
        ];

        ratios.forEach(function (item) {
          const r = item.r;
          let w, h;
          if (sw / sh > r) {
            w = sw;
            h = sw / r;
          } else {
            h = sh;
            w = sh * r;
          }
          item.el.style.width = Math.ceil(w) + 'px';
          item.el.style.height = Math.ceil(h) + 'px';
        });
      }

      layoutMediaWrappers();
      window.addEventListener('resize', layoutMediaWrappers, { passive: true });

      // Synchronize native window scroll to target
      window.addEventListener('scroll', function () {
        if (!isAutopilot) {
          targetScrollY = window.scrollY;
          if (!hasScrolledOnce && targetScrollY > 10) {
            hasScrolledOnce = true;
            scrollHint.style.opacity = '0';
          }
        }
      }, { passive: true });

      // Smooth Touch & Wheel Listeners
      window.addEventListener('wheel', function (e) {
        if (isAutopilot) stopAutopilot();
        targetScrollY = Math.max(0, Math.min(maxScroll, targetScrollY + e.deltaY * 1.05));
      }, { passive: true });

      // Touch handling for mobile
      let touchStartY = 0;
      window.addEventListener('touchstart', function (e) {
        if (e.touches.length === 1) {
          touchStartY = e.touches[0].clientY;
        }
      }, { passive: true });

      window.addEventListener('touchmove', function (e) {
        if (e.touches.length === 1) {
          if (isAutopilot) stopAutopilot();
          const touchY = e.touches[0].clientY;
          const deltaY = (touchStartY - touchY) * 1.5;
          touchStartY = touchY;
          targetScrollY = Math.max(0, Math.min(maxScroll, targetScrollY + deltaY));
          if (!hasScrolledOnce && targetScrollY > 10) {
            hasScrolledOnce = true;
            scrollHint.style.opacity = '0';
          }
        }
      }, { passive: true });

      // Autopilot Toggle
      autopilotBtn.addEventListener('click', function () {
        if (isAutopilot) {
          stopAutopilot();
        } else {
          startAutopilot();
        }
      });

      function startAutopilot() {
        isAutopilot = true;
        autopilotBtn.classList.add('active');
        autopilotLabel.textContent = 'Pause Autopilot';
        if (!hasScrolledOnce) {
          hasScrolledOnce = true;
          scrollHint.style.opacity = '0';
        }
        if (scrollProgress >= 0.99) {
          targetScrollY = 0;
          currentScrollY = 0;
          window.scrollTo(0, 0);
        }
      }

      function stopAutopilot() {
        isAutopilot = false;
        autopilotBtn.classList.remove('active');
        autopilotLabel.textContent = 'Drone Autopilot';
      }

      // Video Modal Handlers
      videoBtn.addEventListener('click', function () {
        if (isAutopilot) stopAutopilot();
        videoModal.classList.add('active');
        droneVideoPlayer.currentTime = 0;
        droneVideoPlayer.play();
      });

      function closeVideo() {
        videoModal.classList.remove('active');
        droneVideoPlayer.pause();
      }

      videoCloseBtn.addEventListener('click', closeVideo);
      window.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && videoModal.classList.contains('active')) {
          closeVideo();
        }
      });

      // Keyboard navigation
      window.addEventListener('keydown', function (e) {
        if (videoModal.classList.contains('active')) return;
        if (isAutopilot) stopAutopilot();
        if (e.key === 'ArrowDown' || e.key === 'PageDown' || e.key === ' ') {
          targetScrollY = Math.min(maxScroll, targetScrollY + window.innerHeight * 0.45);
        } else if (e.key === 'ArrowUp' || e.key === 'PageUp') {
          targetScrollY = Math.max(0, targetScrollY - window.innerHeight * 0.45);
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
      // CORE DRONE CINEMA TIMELINE (Frame-by-Frame Scroll Choreography)
      // =========================================================================
      function renderTimeline(p) {
        progressFill.style.width = (p * 100).toFixed(2) + '%';

        // -----------------------------------------------------------------------
        // PHASE 1: [0.00 -> 0.20] START FROM main1.jpg
        // -----------------------------------------------------------------------
        if (p <= 0.25) {
          const t = norm(p, 0.00, 0.20);
          const st = smoothstep(t);
          scene1.style.opacity = (1 - norm(p, 0.12, 0.22)).toFixed(3);
          scene1.style.display = 'flex';

          const scale1 = 1.0 + st * 0.22;
          const translateY1 = -(st * 12);
          wrapper1.style.transform = 'translate(-50%, -50%) translate3d(0, ' + translateY1 + '%, 0) scale(' + scale1 + ')';
        } else {
          scene1.style.opacity = '0';
          scene1.style.display = 'none';
        }

        // -----------------------------------------------------------------------
        // PHASE 2 & 3: [0.10 -> 0.58] TRANSITION TO main2.jpg, ZOOM IN, DOORS OPEN,
        //               AND CAMERA ANGLE MOVES SLIGHTLY TO THE RIGHT SIDE
        // -----------------------------------------------------------------------
        if (p >= 0.10 && p <= 0.60) {
          scene2.style.display = 'flex';

          const inOpacity = norm(p, 0.12, 0.22);
          const outOpacity = 1 - norm(p, 0.50, 0.58);
          scene2.style.opacity = (Math.min(inOpacity, outOpacity)).toFixed(3);

          const zoomProg = norm(p, 0.14, 0.48);
          const zoomSmooth = easeInOutQuad(zoomProg);

          // Camera moves slightly to the right side per user specification
          const rightPanProg = norm(p, 0.28, 0.50);
          const rightPanSmooth = smoothstep(rightPanProg);

          const scale2 = 1.0 + zoomSmooth * 1.85;
          const panX2 = -(rightPanSmooth * 8.5);
          const panY2 = -(zoomSmooth * 18.0);

          wrapper2.style.transform = 'translate(-50%, -50%) translate3d(' + panX2 + '%, ' + panY2 + '%, 0) scale(' + scale2 + ')';
          wrapper2.style.transformOrigin = '50% 65%';

          // DOORS OPENING SEQUENCE:
          const doorProg = norm(p, 0.25, 0.44);
          const doorSmooth = easeInOutQuad(doorProg);

          const leftAngle = -(doorSmooth * 85);
          const rightAngle = doorSmooth * 85;

          doorLeft.style.transform = 'rotateY(' + leftAngle + 'deg)';
          doorRight.style.transform = 'rotateY(' + rightAngle + 'deg)';

          // Interior warm glow behind doors
          doorGlow.style.opacity = (doorSmooth * 0.95).toFixed(3);

          // WINDOW & SHEER CURTAINS INTERACTION:
          const windowZoomProg = norm(p, 0.42, 0.56);
          const windowZoomSmooth = smoothstep(windowZoomProg);

          const curtainPart = windowZoomSmooth * 75;
          curtainLeft.style.transform = 'translate3d(' + (-curtainPart) + '%, 0, 0) scale(' + (1 + windowZoomSmooth * 0.3) + ')';
          curtainRight.style.transform = 'translate3d(' + curtainPart + '%, 0, 0) scale(' + (1 + windowZoomSmooth * 0.3) + ')';

          const curtainFade = 1 - norm(p, 0.49, 0.56);
          curtainLeft.style.opacity = curtainFade.toFixed(3);
          curtainRight.style.opacity = curtainFade.toFixed(3);

          windowBeam.style.opacity = (windowZoomSmooth * (1 - norm(p, 0.52, 0.58))).toFixed(3);
        } else {
          scene2.style.opacity = '0';
          scene2.style.display = 'none';
        }

        // -----------------------------------------------------------------------
        // PHASE 4: [0.46 -> 0.74] CAMERA ZOOMS OUT FROM BIG WINDOW WITH CURTAINS
        //          DIRECTLY INTO banq1.jpg (Floral Walkway)
        // -----------------------------------------------------------------------
        if (p >= 0.46 && p <= 0.76) {
          scene3.style.display = 'flex';

          const inOpacity3 = norm(p, 0.49, 0.57);
          const outOpacity3 = 1 - norm(p, 0.67, 0.74);
          scene3.style.opacity = (Math.min(inOpacity3, outOpacity3)).toFixed(3);

          const pushProg = norm(p, 0.48, 0.73);
          const pushSmooth = easeInOutQuad(pushProg);

          const scale3 = 1.08 + pushSmooth * 0.28;
          // As it reaches end of banq1, camera dollies directly to left:
          const leftDolly = -(norm(p, 0.62, 0.74) * 22);

          wrapper3.style.transform = 'translate(-50%, -50%) translate3d(' + leftDolly + '%, 0, 0) scale(' + scale3 + ')';
        } else {
          scene3.style.opacity = '0';
          scene3.style.display = 'none';
        }

        // -----------------------------------------------------------------------
        // PHASE 5: [0.64 -> 0.87] CAMERA MOVES DIRECTLY TO LEFT & CONNECTS banq2.jpg
        // -----------------------------------------------------------------------
        if (p >= 0.64 && p <= 0.88) {
          scene4.style.display = 'flex';

          const inOpacity4 = norm(p, 0.66, 0.73);
          const outOpacity4 = 1 - norm(p, 0.81, 0.87);
          scene4.style.opacity = (Math.min(inOpacity4, outOpacity4)).toFixed(3);

          const sweepProg = norm(p, 0.65, 0.84);
          const sweepSmooth = easeInOutQuad(sweepProg);

          const enterX = (1 - norm(p, 0.65, 0.74)) * 18;
          const exitX = -(norm(p, 0.78, 0.86) * 12);
          const posX4 = enterX + exitX;
          const scale4 = 1.02 + sweepSmooth * 0.18;

          wrapper4.style.transform = 'translate(-50%, -50%) translate3d(' + posX4 + '%, 0, 0) scale(' + scale4 + ')';
        } else {
          scene4.style.opacity = '0';
          scene4.style.display = 'none';
        }

        // -----------------------------------------------------------------------
        // PHASE 6: [0.78 -> 0.95] FOLLOWED BY banq3.jpg (Center Aisle Push)
        // -----------------------------------------------------------------------
        if (p >= 0.78 && p <= 0.95) {
          scene5.style.display = 'flex';

          const inOpacity5 = norm(p, 0.80, 0.86);
          const outOpacity5 = 1 - norm(p, 0.90, 0.95);
          scene5.style.opacity = (Math.min(inOpacity5, outOpacity5)).toFixed(3);

          const aisleProg = norm(p, 0.80, 0.94);
          const aisleSmooth = easeInOutQuad(aisleProg);

          const scale5 = 1.0 + aisleSmooth * 0.35;
          const panY5 = -(aisleSmooth * 8);

          wrapper5.style.transform = 'translate(-50%, -50%) translate3d(0, ' + panY5 + '%, 0) scale(' + scale5 + ')';
        } else {
          scene5.style.opacity = '0';
          scene5.style.display = 'none';
        }

        // -----------------------------------------------------------------------
        // PHASE 7: [0.89 -> 1.00] FINALE AT banq4.jpg (Grand Floral Mandap)
        // -----------------------------------------------------------------------
        if (p >= 0.89) {
          scene6.style.display = 'flex';

          const inOpacity6 = norm(p, 0.90, 0.96);
          scene6.style.opacity = inOpacity6.toFixed(3);

          const mandapProg = norm(p, 0.90, 1.00);
          const mandapSmooth = easeOutCubic(mandapProg);

          const scale6 = 1.15 - (1 - mandapSmooth) * 0.15;
          const panY6 = (1 - mandapSmooth) * 4;

          wrapper6.style.transform = 'translate(-50%, -50%) translate3d(0, ' + panY6 + '%, 0) scale(' + scale6 + ')';
        } else {
          scene6.style.opacity = '0';
          scene6.style.display = 'none';
        }

        // Gentle sub-degree natural drone banking
        const droneRoll = Math.sin(p * Math.PI * 5) * 0.45;
        const dronePitch = (p - 0.5) * 1.2;
        cameraRig.style.transform = 'rotateZ(' + droneRoll.toFixed(2) + 'deg) rotateX(' + dronePitch.toFixed(2) + 'deg)';
      }

      // ANIMATION LOOP
      function loop() {
        if (isAutopilot) {
          targetScrollY += autopilotSpeed * maxScroll;
          if (targetScrollY >= maxScroll) {
            targetScrollY = maxScroll;
            stopAutopilot();
          }
          window.scrollTo(0, targetScrollY);
        }

        currentScrollY += (targetScrollY - currentScrollY) * 0.082;
        scrollProgress = clamp(currentScrollY / maxScroll, 0, 1);

        renderTimeline(scrollProgress);
        requestAnimationFrame(loop);
      }
      requestAnimationFrame(loop);

      // LIVING ATMOSPHERE CANVAS
      const canvas = document.getElementById('ambient-canvas');
      const ctx = canvas.getContext('2d');

      let w = 0, h = 0;
      function resizeCanvas() {
        w = canvas.width = window.innerWidth;
        h = canvas.height = window.innerHeight;
      }
      resizeCanvas();
      window.addEventListener('resize', resizeCanvas, { passive: true });

      const particles = [];
      const PARTICLE_COUNT = 36;
      const colors = [
        'rgba(248, 238, 224, 0.45)',
        'rgba(255, 230, 220, 0.50)',
        'rgba(250, 245, 235, 0.40)',
        'rgba(235, 210, 185, 0.35)'
      ];

      for (let i = 0; i < PARTICLE_COUNT; i++) {
        particles.push({
          x: Math.random() * window.innerWidth,
          y: Math.random() * window.innerHeight,
          radiusX: 1.5 + Math.random() * 3.5,
          radiusY: 1.0 + Math.random() * 2.5,
          color: colors[Math.floor(Math.random() * colors.length)],
          vx: (Math.random() - 0.5) * 0.45 + 0.15,
          vy: 0.35 + Math.random() * 0.65,
          angle: Math.random() * Math.PI * 2,
          angularSpeed: (Math.random() - 0.5) * 0.025,
          swaySpeed: 0.002 + Math.random() * 0.003,
          swayOffset: Math.random() * Math.PI * 2
        });
      }

      let time = 0;
      function animateAtmosphere() {
        time += 1;
        ctx.clearRect(0, 0, w, h);

        for (let i = 0; i < particles.length; i++) {
          const p = particles[i];
          p.x += p.vx + Math.sin(time * p.swaySpeed + p.swayOffset) * 0.35;
          p.y += p.vy;
          p.angle += p.angularSpeed;

          if (p.y > h + 20) {
            p.y = -20;
            p.x = Math.random() * w;
          }
          if (p.x > w + 20) p.x = -20;
          if (p.x < -20) p.x = w + 20;

          ctx.save();
          ctx.translate(p.x, p.y);
          ctx.rotate(p.angle);
          ctx.beginPath();
          ctx.ellipse(0, 0, p.radiusX, p.radiusY, 0, 0, Math.PI * 2);
          ctx.fillStyle = p.color;
          ctx.fill();
          ctx.restore();
        }

        requestAnimationFrame(animateAtmosphere);
      }
      requestAnimationFrame(animateAtmosphere);

    })();
  </script>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_code)
print("Updated index.html with sub-pixel aspect lock!")
