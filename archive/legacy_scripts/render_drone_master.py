import cv2
import numpy as np
import math
import os

print("=== Rendering 100% Artifact-Free FPV Drone Flight ===")

WIDTH = 1920
HEIGHT = 1080
FPS = 30
TOTAL_FRAMES = 600 # 20 seconds

# 1. Load Original Assets
img_main1 = cv2.imread('img/main1.jpg')
img_main2 = cv2.imread('img/main2.jpg')
img_door_l = cv2.imread('img/door_left.png')
img_door_r = cv2.imread('img/door_right.png')
img_curt_l = cv2.imread('img/curtain_left.png', cv2.IMREAD_UNCHANGED)
img_curt_r = cv2.imread('img/curtain_right.png', cv2.IMREAD_UNCHANGED)
img_banq1 = cv2.imread('img/banq1.jpg')
img_banq2 = cv2.imread('img/banq2.jpg')
img_banq3 = cv2.imread('img/banq3.jpg')
img_banq4 = cv2.imread('img/banq4.jpg')

# 2. Build Seamless Master Facade
# main1 (768x1376) and main2 (768x1376) overlap by 456px vertically
w_raw = 1376
pano_raw = np.zeros((1080, w_raw, 3), dtype=np.uint8)
pano_raw[0:768, :] = img_main1
overlap_h = 456
alpha = np.linspace(0, 1, overlap_h)[:, None, None].astype(np.float32)
pano_raw[312:768, :] = (img_main1[312:768, :].astype(np.float32) * (1 - alpha) + img_main2[0:overlap_h, :].astype(np.float32) * alpha).astype(np.uint8)
pano_raw[768:1080, :] = img_main2[overlap_h:768, :]

# Scale pano to 1920 width (1920x1506)
pano = cv2.resize(pano_raw, (1920, int(1080 * 1920 / 1376)), interpolation=cv2.INTER_LANCZOS4)
P_H, P_W = pano.shape[:2] # 1506, 1920
print(f"Master Facade scaled to: {P_W}x{P_H}")

# Calculate door coordinates in 1920x1506 pano:
# Raw: x: 648 to 728, y: 806 to 892
door_x1 = int(648 * 1920 / 1376)
door_x2 = int(728 * 1920 / 1376)
door_y1 = int(806 * 1920 / 1376)
door_y2 = int(892 * 1920 / 1376)

# Calculate right window coordinates in 1920x1506 pano:
# Raw: x: 770 to 840, y: 792 to 892
win_x1 = int(770 * 1920 / 1376)
win_x2 = int(840 * 1920 / 1376)
win_y1 = int(792 * 1920 / 1376)
win_y2 = int(892 * 1920 / 1376)

# Scale other images to cover 1920x1080 with margin
def make_cover_asset(raw_img):
    rh, rw = raw_img.shape[:2]
    scale = max(1920.0 / rw, 1080.0 / rh)
    return cv2.resize(raw_img, (int(rw * scale), int(rh * scale)), interpolation=cv2.INTER_LANCZOS4)

asset_banq1 = make_cover_asset(img_banq1) # 1920x1920
asset_banq2 = make_cover_asset(img_banq2) # 1920x1920
asset_banq3 = make_cover_asset(img_banq3) # 1920x2571
asset_banq4 = make_cover_asset(img_banq4) # 1920x2571

print("All assets pre-scaled to high-res cover dimensions.")

def smoothstep(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)

def ease_in_out(t):
    t = max(0.0, min(1.0, t))
    return 2 * t * t if t < 0.5 else -1 + (4 - 2 * t) * t

# Camera sampling that is 100% strictly clamped inside image pixels
def sample_virtual_cam(src, center_x, center_y, zoom=1.0, roll_deg=0.0):
    sh, sw = src.shape[:2]
    
    # Visible viewport size in source coordinates
    vw = WIDTH / zoom
    vh = HEIGHT / zoom
    
    # Clamp center so camera never samples outside source image
    half_vw = vw / 2.0
    half_vh = vh / 2.0
    
    cx = max(half_vw, min(sw - half_vw, center_x))
    cy = max(half_vh, min(sh - half_vh, center_y))
    
    M = cv2.getRotationMatrix2D((cx, cy), roll_deg, zoom)
    M[0, 2] += (WIDTH / 2.0) - cx * zoom
    M[1, 2] += (HEIGHT / 2.0) - cy * zoom
    
    return cv2.warpAffine(src, M, (WIDTH, HEIGHT), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REPLICATE)

# Render doors and curtains onto pano
def render_doors_and_curtains(pano_base, door_angle, curtain_part, curtain_alpha):
    f = pano_base.copy()
    
    # 3D Double Doors
    if door_angle > 1.0:
        # Portal interior warm light
        cv2.rectangle(f, (door_x1, door_y1), (door_x2, door_y2), (65, 160, 245), -1)
        roi = f[door_y1:door_y2, door_x1:door_x2].astype(np.float32)
        f[door_y1:door_y2, door_x1:door_x2] = np.clip(roi * 0.3 + np.array([40, 185, 255]) * 0.7, 0, 255).astype(np.uint8)
        
        # 3D door leaf rotation
        rad = math.radians(min(80, door_angle))
        wf = max(0.08, math.cos(rad))
        dh, dw = door_y2 - door_y1, (door_x2 - door_x1) // 2
        dl = cv2.resize(img_door_l, (max(3, int(dw * wf)), dh))
        dr = cv2.resize(img_door_r, (max(3, int(dw * wf)), dh))
        
        f[door_y1:door_y2, door_x1:door_x1+dl.shape[1]] = dl
        f[door_y1:door_y2, door_x2-dr.shape[1]:door_x2] = dr
        
    # Sheer Curtains on Right Window
    if curtain_alpha > 0.02:
        ww = win_x2 - win_x1
        wh = win_y2 - win_y1
        cw = int(ww * 0.65)
        cl_res = cv2.resize(img_curt_l, (cw, wh))
        cr_res = cv2.resize(img_curt_r, (cw, wh))
        part_px = int(curtain_part * ww * 0.60)
        
        # Left curtain
        lx1 = max(win_x1, win_x1 - part_px)
        lx2 = min(win_x2, win_x1 - part_px + cw)
        if lx2 > lx1:
            w_act = lx2 - lx1
            roi = f[win_y1:win_y2, lx1:lx2].astype(np.float32)
            c_rgb = cl_res[:, :w_act, :3].astype(np.float32)
            c_a = (cl_res[:, :w_act, 3].astype(np.float32) / 255.0) * curtain_alpha
            f[win_y1:win_y2, lx1:lx2] = np.clip(roi * (1.0 - c_a[:, :, None]) + c_rgb * c_a[:, :, None], 0, 255).astype(np.uint8)
            
        # Right curtain
        rx1 = max(win_x1, win_x2 + part_px - cw)
        rx2 = min(win_x2, win_x2 + part_px)
        if rx2 > rx1:
            w_act = rx2 - rx1
            roi = f[win_y1:win_y2, rx1:rx2].astype(np.float32)
            c_rgb = cr_res[:, -w_act:, :3].astype(np.float32)
            c_a = (cr_res[:, -w_act:, 3].astype(np.float32) / 255.0) * curtain_alpha
            f[win_y1:win_y2, rx1:rx2] = np.clip(roi * (1.0 - c_a[:, :, None]) + c_rgb * c_a[:, :, None], 0, 255).astype(np.uint8)
            
    return f

# Pre-render video
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('resort_drone_flight.mp4', fourcc, FPS, (WIDTH, HEIGHT))

for f in range(TOTAL_FRAMES):
    # -------------------------------------------------------------------------
    # 1. PHASE 1: [0 to 140] SKY TO FACADE DIVE
    # -------------------------------------------------------------------------
    if f <= 140:
        t = f / 140.0
        st = smoothstep(t)
        
        # Starts at sky/cupola (cy=540) and dives down to courtyard (cy=960)
        cy = 540 + st * 420
        cx = P_W / 2.0
        zoom = 1.0 + st * 0.25
        roll = math.sin(t * math.pi * 2) * 0.4
        
        frame_src = render_doors_and_curtains(pano, 0.0, 0.0, 1.0)
        frame = sample_virtual_cam(frame_src, cx, cy, zoom, roll)
        
    # -------------------------------------------------------------------------
    # 2. PHASE 2: [140 to 240] COURTYARD GLIDE, DOORS OPEN, WINDOW APPROACH
    # -------------------------------------------------------------------------
    elif f <= 240:
        t = (f - 140) / 100.0
        st = smoothstep(t)
        
        door_t = smoothstep(min(1.0, (f - 140) / 55.0))
        door_angle = door_t * 80.0
        
        curtain_part = st * 0.85
        curtain_alpha = 1.0 - smoothstep(max(0.0, (f - 200) / 40.0))
        
        # Camera glides towards right window: win_cx ~ 1120, win_cy ~ 1170
        win_cx = (win_x1 + win_x2) / 2.0
        win_cy = (win_y1 + win_y2) / 2.0
        
        cx = (P_W / 2.0) * (1 - st) + win_cx * st
        cy = 960 * (1 - st) + win_cy * st
        zoom = 1.25 + st * 2.2 # Push in towards the window
        roll = math.sin(t * math.pi) * 0.6
        
        frame_src = render_doors_and_curtains(pano, door_angle, curtain_part, curtain_alpha)
        frame = sample_virtual_cam(frame_src, cx, cy, zoom, roll)
        
    # -------------------------------------------------------------------------
    # 3. PHASE 3: [240 to 330] PENETRATING WINDOW & ENTERING FLORAL CORRIDOR (banq1)
    # -------------------------------------------------------------------------
    elif f <= 330:
        t = (f - 240) / 90.0
        st = smoothstep(t)
        
        # Cross window threshold: 0 to 30 frames
        trans_t = smoothstep(min(1.0, (f - 240) / 30.0))
        
        # banq1 camera motion: fly down the aisle, then drift slightly left
        b1_w, b1_h = asset_banq1.shape[1], asset_banq1.shape[0]
        push1 = ease_in_out(t)
        cx1 = (b1_w / 2.0) + smoothstep(max(0.0, (f - 280) / 50.0)) * 120
        cy1 = (b1_h / 2.0)
        zoom1 = 1.02 + push1 * 0.45
        roll1 = math.sin(t * math.pi * 1.5) * 0.5
        
        cam1 = sample_virtual_cam(asset_banq1, cx1, cy1, zoom1, roll1)
        
        if trans_t < 1.0:
            # Last moments of window exterior
            frame_src = render_doors_and_curtains(pano, 80.0, 1.0, 0.0)
            cam_ext = sample_virtual_cam(frame_src, (win_x1 + win_x2) / 2.0, (win_y1 + win_y2) / 2.0, 3.45 + trans_t * 4.0, roll1)
            frame = (cam_ext.astype(np.float32) * (1.0 - trans_t) + cam1.astype(np.float32) * trans_t).astype(np.uint8)
        else:
            frame = cam1
            
    # -------------------------------------------------------------------------
    # 4. PHASE 4: [330 to 430] FPV BANKING TURN LEFT INTO BALLROOM (banq2)
    # -------------------------------------------------------------------------
    elif f <= 430:
        t = (f - 330) / 100.0
        st = smoothstep(t)
        
        # Banking turn: Quadcopter banks left (-5.0 deg roll)
        bank_roll = -math.sin(st * math.pi) * 5.0
        
        b2_w, b2_h = asset_banq2.shape[1], asset_banq2.shape[0]
        turn_t = ease_in_out(t)
        # Pan across ballroom from right to left
        cx2 = (b2_w * 0.58) - turn_t * (b2_w * 0.16)
        cy2 = (b2_h * 0.50)
        zoom2 = 1.02 + turn_t * 0.25
        
        cam2 = sample_virtual_cam(asset_banq2, cx2, cy2, zoom2, bank_roll)
        
        if t < 0.22:
            exit_t = t / 0.22
            b1_w, b1_h = asset_banq1.shape[1], asset_banq1.shape[0]
            cam1_exit = sample_virtual_cam(asset_banq1, (b1_w / 2.0) + 120 + exit_t * 180, b1_h / 2.0, 1.47, bank_roll)
            frame = (cam1_exit.astype(np.float32) * (1.0 - exit_t) + cam2.astype(np.float32) * exit_t).astype(np.uint8)
        else:
            frame = cam2
            
    # -------------------------------------------------------------------------
    # 5. PHASE 5: [430 to 520] HIGH-SPEED PUSH DOWN CENTER AISLE (banq3)
    # -------------------------------------------------------------------------
    elif f <= 520:
        t = (f - 430) / 90.0
        st = ease_in_out(t)
        
        drone_roll = math.sin(t * math.pi) * 0.4
        
        b3_w, b3_h = asset_banq3.shape[1], asset_banq3.shape[0]
        # Fast push down the aisle towards royal stage
        cx3 = b3_w / 2.0
        cy3 = (b3_h * 0.58) - st * (b3_h * 0.12)
        zoom3 = 1.0 + st * 0.65
        
        cam3 = sample_virtual_cam(asset_banq3, cx3, cy3, zoom3, drone_roll)
        
        if t < 0.16:
            trans_t = t / 0.16
            b2_w, b2_h = asset_banq2.shape[1], asset_banq2.shape[0]
            cam2_exit = sample_virtual_cam(asset_banq2, b2_w * 0.42, b2_h * 0.50, 1.27 + trans_t * 0.25, drone_roll)
            frame = (cam2_exit.astype(np.float32) * (1.0 - trans_t) + cam3.astype(np.float32) * trans_t).astype(np.uint8)
        else:
            frame = cam3
            
    # -------------------------------------------------------------------------
    # 6. PHASE 6: [520 to 600] ROYAL WEDDING MANDAP ARRIVAL & HOVER (banq4)
    # -------------------------------------------------------------------------
    else:
        t = (f - 520) / 80.0
        t_ease = 1.0 - math.pow(1.0 - t, 3.0) # Smooth deceleration to hover
        
        drone_roll = math.sin(t * math.pi * 0.5) * 0.25
        
        b4_w, b4_h = asset_banq4.shape[1], asset_banq4.shape[0]
        cx4 = b4_w / 2.0
        cy4 = (b4_h * 0.52) - t_ease * (b4_h * 0.04)
        zoom4 = 1.02 + t_ease * 0.22
        
        cam4 = sample_virtual_cam(asset_banq4, cx4, cy4, zoom4, drone_roll)
        
        if t < 0.20:
            trans_t = t / 0.20
            b3_w, b3_h = asset_banq3.shape[1], asset_banq3.shape[0]
            cam3_exit = sample_virtual_cam(asset_banq3, b3_w / 2.0, b3_h * 0.46, 1.65 + trans_t * 0.2, drone_roll)
            frame = (cam3_exit.astype(np.float32) * (1.0 - trans_t) + cam4.astype(np.float32) * trans_t).astype(np.uint8)
        else:
            frame = cam4

    out.write(frame)
    if f % 100 == 0 or f == TOTAL_FRAMES - 1:
        print(f"Rendered frame {f}/{TOTAL_FRAMES} ({(f/TOTAL_FRAMES*100):.1f}%)")

out.release()
print("=== Render Complete! resort_drone_flight.mp4 updated ===")
