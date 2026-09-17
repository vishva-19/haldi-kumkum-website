import cv2
import numpy as np
import math
import os

print("--- Starting True 3D Continuous FPV Drone Flight Render ---")

WIDTH = 1920
HEIGHT = 1080
FPS = 30
TOTAL_FRAMES = 600 # 20.0 seconds of smooth flight

# 1. Load Assets
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

# 2. Build Seamless Facade Master (1376x1080)
# Shift between main1 and main2 is exactly 312px
w_facade = img_main2.shape[1] # 1376
pano_facade = np.zeros((1080, w_facade, 3), dtype=np.uint8)
pano_facade[0:768, :] = img_main1

overlap_h = 768 - 312 # 456px
alpha_ramp = np.linspace(0, 1, overlap_h)[:, None, None].astype(np.float32)
blend = (img_main1[312:768, :].astype(np.float32) * (1.0 - alpha_ramp) + img_main2[0:overlap_h, :].astype(np.float32) * alpha_ramp).astype(np.uint8)
pano_facade[312:768, :] = blend
pano_facade[768:1080, :] = img_main2[overlap_h:768, :]

# Door coordinates in pano_facade:
# main2 y: 494 to 580 -> pano y: 494 + 312 = 806 to 892. x: 648 to 728.
door_y1, door_y2 = 806, 892
door_x1, door_x2 = 648, 728

# Window coordinates in pano_facade:
# main2 y: 480 to 580 -> pano y: 480 + 312 = 792 to 892. x: 770 to 840.
win_y1, win_y2 = 792, 892
win_x1, win_x2 = 770, 840

print("Master facade assembled. Dimensions:", pano_facade.shape)

def smoothstep(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)

def ease_in_out(t):
    t = max(0.0, min(1.0, t))
    return 2 * t * t if t < 0.5 else -1 + (4 - 2 * t) * t

def render_facade_doors(pano, door_angle, curtain_part, curtain_opacity):
    res = pano.copy()
    
    # 1. 3D Doors
    if door_angle > 1.0:
        # Interior portal warm glow
        cv2.rectangle(res, (door_x1, door_y1), (door_x2, door_y2), (70, 160, 245), -1)
        roi = res[door_y1:door_y2, door_x1:door_x2].astype(np.float32)
        roi = roi * 0.35 + np.array([45, 185, 255]) * 0.65
        res[door_y1:door_y2, door_x1:door_x2] = np.clip(roi, 0, 255).astype(np.uint8)
        
        # Left door swing
        rad = math.radians(min(82, door_angle))
        wf = max(0.08, math.cos(rad))
        dh, dw = img_door_l.shape[:2]
        nw = max(3, int(dw * wf))
        wl = cv2.resize(img_door_l, (nw, dh))
        res[door_y1:door_y2, door_x1:door_x1+nw] = wl
        
        # Right door swing
        wr = cv2.resize(img_door_r, (nw, dh))
        res[door_y1:door_y2, door_x2-nw:door_x2] = wr

    # 2. Window Curtains
    if curtain_opacity > 0.02:
        ww = win_x2 - win_x1
        wh = win_y2 - win_y1
        cw = int(ww * 0.65)
        cl_res = cv2.resize(img_curt_l, (cw, wh))
        cr_res = cv2.resize(img_curt_r, (cw, wh))
        part_px = int(curtain_part * ww * 0.55)
        
        # Left drape
        lx1 = max(win_x1, win_x1 - part_px)
        lx2 = min(win_x2, win_x1 - part_px + cw)
        if lx2 > lx1:
            w_act = lx2 - lx1
            roi = res[win_y1:win_y2, lx1:lx2].astype(np.float32)
            c_rgb = cl_res[:, :w_act, :3].astype(np.float32)
            c_a = (cl_res[:, :w_act, 3].astype(np.float32) / 255.0) * curtain_opacity
            c_a = np.expand_dims(c_a, axis=2)
            res[win_y1:win_y2, lx1:lx2] = np.clip(roi * (1.0 - c_a) + c_rgb * c_a, 0, 255).astype(np.uint8)
            
        # Right drape
        rx1 = max(win_x1, win_x2 + part_px - cw)
        rx2 = min(win_x2, win_x2 + part_px)
        if rx2 > rx1:
            w_act = rx2 - rx1
            roi = res[win_y1:win_y2, rx1:rx2].astype(np.float32)
            c_rgb = cr_res[:, -w_act:, :3].astype(np.float32)
            c_a = (cr_res[:, -w_act:, 3].astype(np.float32) / 255.0) * curtain_opacity
            c_a = np.expand_dims(c_a, axis=2)
            res[win_y1:win_y2, rx1:rx2] = np.clip(roi * (1.0 - c_a) + c_rgb * c_a, 0, 255).astype(np.uint8)
            
    return res

def sample_camera(img, cx, cy, scale, roll_deg=0.0):
    ih, iw = img.shape[:2]
    # Center in source image coordinates
    src_cx = iw * cx
    src_cy = ih * cy
    
    # Target size in source pixels
    view_w = WIDTH / scale
    view_h = HEIGHT / scale
    
    # 2D affine rotation & scaling matrix
    M = cv2.getRotationMatrix2D((src_cx, src_cy), roll_deg, scale)
    M[0, 2] += (WIDTH / 2.0) - src_cx * scale
    M[1, 2] += (HEIGHT / 2.0) - src_cy * scale
    
    warped = cv2.warpAffine(img, M, (WIDTH, HEIGHT), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REFLECT)
    return warped

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('resort_drone_flight.mp4', fourcc, FPS, (WIDTH, HEIGHT))

# Ambient pastel particles
np.random.seed(101)
NUM_PART = 36
pxs = np.random.uniform(0, WIDTH, NUM_PART)
pys = np.random.uniform(0, HEIGHT, NUM_PART)
prs = np.random.uniform(2.0, 5.0, NUM_PART)
pcols = [(225, 240, 252), (215, 230, 255), (200, 222, 248), (232, 246, 255)]

for f in range(TOTAL_FRAMES):
    frame = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
    
    # -------------------------------------------------------------------------
    # PHASE 1: [f: 0 to 140] SKYLINE TO PALACE COURTYARD DIVE
    # -------------------------------------------------------------------------
    if f <= 140:
        t = f / 140.0
        st = smoothstep(t)
        
        # Starts at sky/cupola (cy=0.28) and dives down to courtyard (cy=0.76)
        cy = 0.28 + st * 0.48
        cx = 0.50
        scale = 1.35 + st * 0.30
        drone_roll = math.sin(t * math.pi * 2) * 0.4
        
        facade_curr = render_facade_doors(pano_facade, 0.0, 0.0, 1.0)
        frame = sample_camera(facade_curr, cx, cy, scale, drone_roll)
        
    # -------------------------------------------------------------------------
    # PHASE 2: [f: 140 to 240] COURTYARD GLIDE, DOORS OPEN & RIGHT WINDOW APPROACH
    # -------------------------------------------------------------------------
    elif f <= 240:
        t = (f - 140) / 100.0
        st = smoothstep(t)
        
        # Doors swing open: f=140 to 195
        door_t = smoothstep(min(1.0, (f - 140) / 55.0))
        door_angle = door_t * 82.0
        
        # Camera glides toward right window (win_x: 770/1376 = 0.585, win_y: 842/1080 = 0.78)
        cx = 0.50 + st * 0.088
        cy = 0.76 + st * 0.035
        scale = 1.65 + st * 1.85 # Strong camera push into the window
        
        curtain_part = st * 0.75
        curtain_op = 1.0 - smoothstep(max(0.0, (f - 200) / 40.0))
        
        facade_curr = render_facade_doors(pano_facade, door_angle, curtain_part, curtain_op)
        drone_roll = math.sin(t * math.pi) * 0.65
        frame = sample_camera(facade_curr, cx, cy, scale, drone_roll)
        
    # -------------------------------------------------------------------------
    # PHASE 3: [f: 240 to 330] WINDOW PENETRATION & FLORAL ARRIVAL HALL (banq1)
    # -------------------------------------------------------------------------
    elif f <= 330:
        t = (f - 240) / 90.0
        st = smoothstep(t)
        
        # Window penetration: window frame expands offscreen while banq1 rushes in
        pen_t = smoothstep(min(1.0, (f - 240) / 35.0))
        
        # banq1 forward glide
        push1 = ease_in_out(t)
        scale1 = 1.10 + push1 * 0.45
        
        # Camera flies down aisle, slightly panning toward left at the end
        cx1 = 0.50 + smoothstep(max(0.0, (f - 285) / 45.0)) * 0.12
        cy1 = 0.52
        
        drone_roll = math.sin(t * math.pi * 1.5) * 0.6
        cam_banq1 = sample_camera(img_banq1, cx1, cy1, scale1, drone_roll)
        
        if pen_t < 1.0:
            # Last moments of window exterior pushing past camera
            facade_curr = render_facade_doors(pano_facade, 82.0, 1.0, 0.0)
            cam_win = sample_camera(facade_curr, 0.588, 0.795, 3.50 + pen_t * 6.0, drone_roll)
            frame = (cam_win.astype(np.float32) * (1.0 - pen_t) + cam_banq1.astype(np.float32) * pen_t).astype(np.uint8)
        else:
            frame = cam_banq1
            
    # -------------------------------------------------------------------------
    # PHASE 4: [f: 330 to 430] FPV BANKING TURN LEFT INTO GRAND BALLROOM (banq2)
    # -------------------------------------------------------------------------
    elif f <= 430:
        t = (f - 330) / 100.0
        st = smoothstep(t)
        
        # FPV banking turn: quadcopter rolls into the turn (-4.5 deg roll)
        bank_roll = -math.sin(st * math.pi) * 5.0
        
        # banq2 sweeps in as camera yaws left
        turn_t = ease_in_out(t)
        cx2 = 0.62 - turn_t * 0.14
        cy2 = 0.52
        scale2 = 1.08 + turn_t * 0.22
        
        cam_banq2 = sample_camera(img_banq2, cx2, cy2, scale2, bank_roll)
        
        if t < 0.25:
            # Sweeping connection from banq1
            exit_t = t / 0.25
            cam_banq1_exit = sample_camera(img_banq1, 0.62 + exit_t * 0.15, 0.52, 1.55, bank_roll)
            frame = (cam_banq1_exit.astype(np.float32) * (1.0 - exit_t) + cam_banq2.astype(np.float32) * exit_t).astype(np.uint8)
        else:
            frame = cam_banq2
            
    # -------------------------------------------------------------------------
    # PHASE 5: [f: 430 to 520] ACCELERATION DOWN CENTER AISLE (banq3)
    # -------------------------------------------------------------------------
    elif f <= 520:
        t = (f - 430) / 90.0
        st = ease_in_out(t)
        
        # Level off roll, high-speed push down the carpeted aisle
        drone_roll = math.sin(t * math.pi) * 0.4
        
        cx3 = 0.50
        cy3 = 0.56 - st * 0.12 # Tilt toward royal stage
        scale3 = 1.02 + st * 0.55 # Fast push-in
        
        cam_banq3 = sample_camera(img_banq3, cx3, cy3, scale3, drone_roll)
        
        if t < 0.18:
            trans_t = t / 0.18
            cam_banq2_exit = sample_camera(img_banq2, 0.48, 0.52, 1.30 + trans_t * 0.25, drone_roll)
            frame = (cam_banq2_exit.astype(np.float32) * (1.0 - trans_t) + cam_banq3.astype(np.float32) * trans_t).astype(np.uint8)
        else:
            frame = cam_banq3
            
    # -------------------------------------------------------------------------
    # PHASE 6: [f: 520 to 600] ROYAL MANDAP FINALE ARRIVAL (banq4)
    # -------------------------------------------------------------------------
    else:
        t = (f - 520) / 80.0
        # Exponential deceleration / ease-out to gentle hover
        t_ease = 1.0 - math.pow(1.0 - t, 3.0)
        
        drone_roll = math.sin(t * math.pi * 0.5) * 0.25
        
        cx4 = 0.50
        cy4 = 0.54 - t_ease * 0.04
        scale4 = 1.02 + t_ease * 0.18
        
        cam_banq4 = sample_camera(img_banq4, cx4, cy4, scale4, drone_roll)
        
        if t < 0.22:
            trans_t = t / 0.22
            cam_banq3_exit = sample_camera(img_banq3, 0.50, 0.44, 1.57 + trans_t * 0.2, drone_roll)
            frame = (cam_banq3_exit.astype(np.float32) * (1.0 - trans_t) + cam_banq4.astype(np.float32) * trans_t).astype(np.uint8)
        else:
            frame = cam_banq4

    # Subtle ambient pastel petals
    for p_idx in range(NUM_PART):
        pxs[p_idx] += math.sin(f * 0.04 + p_idx) * 0.5 + 0.12
        pys[p_idx] += 0.65 + (p_idx % 3) * 0.22
        if pys[p_idx] > HEIGHT:
            pys[p_idx] = -12
            pxs[p_idx] = np.random.uniform(0, WIDTH)
        x_pt = int(pxs[p_idx])
        y_pt = int(pys[p_idx])
        r_pt = int(prs[p_idx])
        cv2.circle(frame, (x_pt, y_pt), r_pt, pcols[p_idx % len(pcols)], -1)

    out.write(frame)
    if f % 100 == 0 or f == TOTAL_FRAMES - 1:
        print(f"Rendered {f}/{TOTAL_FRAMES} frames ({(f/TOTAL_FRAMES*100):.1f}%)")

out.release()
print("--- SUCCESS: resort_drone_flight.mp4 successfully created! ---")
