import os

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
      background-color: #0d0b0a;
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
      height: 800vh;
      position: relative;
      pointer-events: none;
    }

    /* FIXED CINEMATIC VIEWPORT (100vh / 100dvh) */
    .cinema-viewport {
      position: fixed;
      inset: 0;
      width: 100vw;
      height: 100vh;
      height: 100dvh;
      overflow: hidden;
      background: #0d0b0a;
    }

    /* 60-120 FPS DRONE FLIGHT CANVAS */
    #drone-canvas {
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      display: block;
      pointer-events: none;
      will-change: transform;
    }

    /* AMBIENT LIVING PARTICLES (Subtle drifting pastel rose & champagne petals) */
    #particle-canvas {
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      pointer-events: none;
      z-index: 10;
    }

    /* CINEMA OPTICAL VIGNETTE (Soft warm gradient, no blur) */
    .cinema-vignette {
      position: absolute;
      inset: 0;
      pointer-events: none;
      z-index: 15;
      background: radial-gradient(circle at 50% 50%, transparent 68%, rgba(13, 11, 10, 0.45) 100%);
    }

    /* PRELOADER SCREEN (Pastel elegant luxury loader) */
    .preloader {
      position: fixed;
      inset: 0;
      background: #0d0b0a;
      z-index: 200;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      gap: 16px;
      transition: opacity 0.8s cubic-bezier(0.16, 1, 0.3, 1), visibility 0.8s;
    }

    .preloader.loaded {
      opacity: 0;
      visibility: hidden;
      pointer-events: none;
    }

    .loader-ring {
      width: 44px;
      height: 44px;
      border: 1.5px solid rgba(240, 230, 220, 0.12);
      border-top-color: #d8baa1;
      border-radius: 50%;
      animation: spin 1.2s cubic-bezier(0.5, 0.1, 0.5, 0.9) infinite;
    }

    @keyframes spin {
      to { transform: rotate(360deg); }
    }

    .loader-text {
      font-size: 11px;
      letter-spacing: 0.22em;
      text-transform: uppercase;
      color: rgba(240, 230, 220, 0.75);
    }

    /* MINIMAL PROGRESS LINE AT BOTTOM */
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
      background: rgba(24, 20, 18, 0.55);
      border: 1px solid rgba(240, 230, 220, 0.22);
      cursor: pointer;
      transition: all 0.3s ease;
      color: rgba(245, 238, 230, 0.88);
      font-size: 11px;
      letter-spacing: 0.14em;
      text-transform: uppercase;
      pointer-events: auto;
    }

    .drone-control-pill:hover {
      background: rgba(45, 38, 33, 0.85);
      border-color: rgba(240, 230, 220, 0.45);
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

    /* VIDEO OVERLAY MODAL */
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

  <!-- PRELOADER -->
  <div class="preloader" id="preloader">
    <div class="loader-ring"></div>
    <div class="loader-text" id="loader-progress">Preparing Drone Flight 0%</div>
  </div>

  <!-- VIRTUAL SCROLL TRACK -->
  <div class="scroll-track" id="scroll-track"></div>

  <!-- FIXED CINEMATIC VIEWPORT -->
  <main class="cinema-viewport" id="cinema-viewport">

    <!-- CANVAS FOR CONTINUOUS FPV DRONE FLIGHT SCRUBBING -->
    <canvas id="drone-canvas"></canvas>

    <!-- LIVING ATMOSPHERE CANVAS -->
    <canvas id="particle-canvas"></canvas>

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

      const TOTAL_FRAMES = 120;
      const frames = [];
      let loadedCount = 0;

      const preloader = document.getElementById('preloader');
      const loaderProgress = document.getElementById('loader-progress');
      const droneCanvas = document.getElementById('drone-canvas');
      const droneCtx = droneCanvas.getContext('2d', { alpha: false });
      const scrollTrack = document.getElementById('scroll-track');
      const progressFill = document.getElementById('flight-progress-fill');
      const scrollHint = document.getElementById('scroll-hint');
      const autopilotBtn = document.getElementById('autopilot-btn');
      const autopilotLabel = document.getElementById('autopilot-label');
      const videoBtn = document.getElementById('video-btn');
      const videoModal = document.getElementById('video-modal');
      const videoCloseBtn = document.getElementById('video-close-btn');
      const droneVideoPlayer = document.getElementById('drone-video-player');

      // Setup Canvas Dimensions (DPI aware)
      let viewWidth = 0;
      let viewHeight = 0;
      let dpr = 1;

      function resizeCanvas() {
        dpr = Math.min(window.devicePixelRatio || 1, 2);
        viewWidth = window.innerWidth;
        viewHeight = window.innerHeight;

        droneCanvas.width = viewWidth * dpr;
        droneCanvas.height = viewHeight * dpr;
        droneCanvas.style.width = viewWidth + 'px';
        droneCanvas.style.height = viewHeight + 'px';
        droneCtx.scale(dpr, dpr);

        maxScroll = Math.max(1, scrollTrack.offsetHeight - viewHeight);

        // Re-draw current frame
        drawDroneFrame(currentFrameIndex);
      }

      let maxScroll = 1;
      let targetScrollY = 0;
      let currentScrollY = 0;
      let scrollProgress = 0;
      let currentFrameIndex = 0;
      let isAutopilot = false;
      let autopilotSpeed = 0.00055;
      let hasScrolledOnce = false;

      // Draw image to canvas using object-fit: cover math
      function drawDroneFrame(frameIndex) {
        const img = frames[frameIndex];
        if (!img || !img.complete || img.naturalWidth === 0) return;

        const iw = img.naturalWidth;
        const ih = img.naturalHeight;

        const imgRatio = iw / ih;
        const screenRatio = viewWidth / viewHeight;

        let renderW, renderH, offsetX, offsetY;

        if (screenRatio > imgRatio) {
          renderW = viewWidth;
          renderH = viewWidth / imgRatio;
          offsetX = 0;
          offsetY = (viewHeight - renderH) / 2;
        } else {
          renderH = viewHeight;
          renderW = viewHeight * imgRatio;
          offsetX = (viewWidth - renderW) / 2;
          offsetY = 0;
        }

        droneCtx.drawImage(img, offsetX, offsetY, renderW, renderH);
      }

      // Preload all 120 WebP frames into browser cache
      function padZero(num, size) {
        let s = num + '';
        while (s.length < size) s = '0' + s;
        return s;
      }

      for (let i = 0; i < TOTAL_FRAMES; i++) {
        const img = new Image();
        img.src = 'frames/frame_' + padZero(i, 3) + '.webp';
        img.onload = function () {
          loadedCount++;
          const percent = Math.round((loadedCount / TOTAL_FRAMES) * 100);
          loaderProgress.textContent = 'Preparing Drone Flight ' + percent + '%';

          if (loadedCount === 1) {
            // Immediately draw first frame
            drawDroneFrame(0);
          }

          if (loadedCount === TOTAL_FRAMES) {
            setTimeout(function () {
              preloader.classList.add('loaded');
            }, 250);
          }
        };
        frames.push(img);
      }

      resizeCanvas();
      window.addEventListener('resize', resizeCanvas, { passive: true });

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

      // Smooth Inertia Wheel Listener
      window.addEventListener('wheel', function (e) {
        if (isAutopilot) stopAutopilot();
        targetScrollY = Math.max(0, Math.min(maxScroll, targetScrollY + e.deltaY * 1.15));
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
          const deltaY = (touchStartY - touchY) * 1.6;
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

      // Main Animation Loop
      function animationLoop() {
        if (isAutopilot) {
          targetScrollY += autopilotSpeed * maxScroll;
          if (targetScrollY >= maxScroll) {
            targetScrollY = maxScroll;
            stopAutopilot();
          }
          window.scrollTo(0, targetScrollY);
        }

        // Buttery Lenis-style Lerp inertia
        currentScrollY += (targetScrollY - currentScrollY) * 0.085;
        scrollProgress = Math.max(0, Math.min(1, currentScrollY / maxScroll));

        // Update progress line
        progressFill.style.width = (scrollProgress * 100).toFixed(2) + '%';

        // Calculate continuous frame index (0 to 119)
        const targetFrame = Math.min(TOTAL_FRAMES - 1, Math.floor(scrollProgress * (TOTAL_FRAMES - 1)));
        if (targetFrame !== currentFrameIndex) {
          currentFrameIndex = targetFrame;
          drawDroneFrame(currentFrameIndex);
        }

        requestAnimationFrame(animationLoop);
      }
      requestAnimationFrame(animationLoop);

      // LIVING ATMOSPHERE CANVAS (Pastel Ivory, Soft Rose & Champagne Motes)
      const partCanvas = document.getElementById('particle-canvas');
      const partCtx = partCanvas.getContext('2d');

      let pw = 0, ph = 0;
      function resizeParticles() {
        pw = partCanvas.width = window.innerWidth;
        ph = partCanvas.height = window.innerHeight;
      }
      resizeParticles();
      window.addEventListener('resize', resizeParticles, { passive: true });

      const particles = [];
      const PARTICLE_COUNT = 32;
      const colors = [
        'rgba(248, 238, 224, 0.40)',
        'rgba(255, 230, 220, 0.45)',
        'rgba(250, 245, 235, 0.35)',
        'rgba(235, 210, 185, 0.30)'
      ];

      for (let i = 0; i < PARTICLE_COUNT; i++) {
        particles.push({
          x: Math.random() * window.innerWidth,
          y: Math.random() * window.innerHeight,
          radiusX: 1.5 + Math.random() * 3.0,
          radiusY: 1.0 + Math.random() * 2.0,
          color: colors[Math.floor(Math.random() * colors.length)],
          vx: (Math.random() - 0.5) * 0.35 + 0.12,
          vy: 0.30 + Math.random() * 0.55,
          angle: Math.random() * Math.PI * 2,
          angularSpeed: (Math.random() - 0.5) * 0.02,
          swaySpeed: 0.002 + Math.random() * 0.003,
          swayOffset: Math.random() * Math.PI * 2
        });
      }

      let time = 0;
      function animateParticles() {
        time += 1;
        partCtx.clearRect(0, 0, pw, ph);

        for (let i = 0; i < particles.length; i++) {
          const p = particles[i];
          p.x += p.vx + Math.sin(time * p.swaySpeed + p.swayOffset) * 0.35;
          p.y += p.vy;
          p.angle += p.angularSpeed;

          if (p.y > ph + 20) {
            p.y = -20;
            p.x = Math.random() * pw;
          }
          if (p.x > pw + 20) p.x = -20;
          if (p.x < -20) p.x = pw + 20;

          partCtx.save();
          partCtx.translate(p.x, p.y);
          partCtx.rotate(p.angle);
          partCtx.beginPath();
          partCtx.ellipse(0, 0, p.radiusX, p.radiusY, 0, 0, Math.PI * 2);
          partCtx.fillStyle = p.color;
          partCtx.fill();
          partCtx.restore();
        }

        requestAnimationFrame(animateParticles);
      }
      requestAnimationFrame(animateParticles);

    })();
  </script>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_code)
print("SUCCESS: index.html upgraded to true Canvas Drone Scrollytelling Engine!")
