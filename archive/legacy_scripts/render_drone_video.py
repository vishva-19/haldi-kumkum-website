import cv2
import numpy as np
import math
import os

print("Starting Drone Video Render...")

WIDTH = 1920
HEIGHT = 1080
FPS = 60
TOTAL_FRAMES = 1080 # 18.0 seconds of butter-smooth 60fps drone flight

# Load all images
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

def fit_cover(img, target_w, target_h, center_x=0.5, center_y=0.5, scale=1.0, offset_x=0, offset_y=0):
    ih, iw = img.shape[:2]
    # compute scale to cover
    base_scale = max(target_w / iw, target_h / ih) * scale
    nw = int(iw * base_scale)
    nh = int(ih * base_scale)
    resized = cv2.resize(img, (nw, nh), interpolation=cv2.INTER_LANCZOS4)
    
    # calculate crop / placement
    cx = int(nw * center_x + offset_x)
    cy = int(nh * center_y + offset_y)
    
    x1 = cx - target_w // 2
    y1 = cy - target_h // 2
    x2 = x1 + target_w
    y2 = y1 + target_h
    
    # Pad if necessary
    pad_left = max(0, -x1)
    pad_top = max(0, -y1)
    pad_right = max(0, x2 - nw)
    pad_bottom = max(0, y2 - nh)
    
    if pad_left > 0 or pad_top > 0 or pad_right > 0 or pad_bottom > 0:
        resized = cv2.copyMakeBorder(resized, pad_top, pad_bottom, pad_left, pad_right, cv2.BORDER_REFLECT)
        x1 += pad_left
        y1 += pad_top
        x2 += pad_left
        y2 += pad_top
        
    cropped = resized[y1:y2, x1:x2]
    return cropped[:target_h, :target_w]

def smoothstep(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)

def ease_in_out(t):
    t = max(0.0, min(1.0, t))
    return 2 * t * t if t < 0.5 else -1 + (4 - 2 * t) * t

# Pre-render doors onto main2 with 3D opening angle
def render_main2_with_doors(angle_deg, curt_part, curt_opacity):
    # In main2 (1376x768):
    # Door box: y: 494 to 580 (86px), x: 648 to 728 (80px)
    # Left door: 648 to 688
    # Right door: 688 to 728
    frame_m2 = img_main2.copy()
    
    # Interior glow in doorway
    if angle_deg > 2.0:
        cv2.rectangle(frame_m2, (648, 494), (728, 580), (70, 160, 240), -1)
        # Soft warm inner gradient
        glow_layer = frame_m2[494:580, 648:728].astype(np.float32)
        glow_layer = glow_layer * 0.4 + np.array([50, 180, 255]) * 0.6
        frame_m2[494:580, 648:728] = np.clip(glow_layer, 0, 255).astype(np.uint8)
        
        # Warp left door leaf (opens inward)
        # width narrows as angle increases: cos(angle)
        rad = math.radians(min(80, angle_deg))
        w_factor = max(0.12, math.cos(rad))
        dh, dw = img_door_l.shape[:2]
        new_w = max(4, int(dw * w_factor))
        warped_l = cv2.resize(img_door_l, (new_w, dh))
        frame_m2[494:580, 648:648+new_w] = warped_l
        
        # Warp right door leaf
        warped_r = cv2.resize(img_door_r, (new_w, dh))
        frame_m2[494:580, 728-new_w:728] = warped_r
        
    # Render curtains on right window (x: 770 to 840, y: 480 to 580)
    if curt_opacity > 0.02:
        wx1, wx2 = 770, 840
        wy1, wy2 = 480, 580
        win_w = wx2 - wx1
        win_h = wy2 - wy1
        
        # Resize curtains to window
        c_w = int(win_w * 0.6)
        cl_res = cv2.resize(img_curt_l, (c_w, win_h))
        cr_res = cv2.resize(img_curt_r, (c_w, win_h))
        
        part_px = int(curt_part * win_w * 0.5)
        
        # Left drape
        lx1 = max(wx1, wx1 - part_px)
        lx2 = min(wx2, wx1 - part_px + c_w)
        cw_l = lx2 - lx1
        if cw_l > 0:
            roi = frame_m2[wy1:wy2, lx1:lx2].astype(np.float32)
            c_rgb = cl_res[:, :cw_l, :3].astype(np.float32)
            c_a = (cl_res[:, :cw_l, 3].astype(np.float32) / 255.0) * curt_opacity
            c_a = np.expand_dims(c_a, axis=2)
            blended = roi * (1.0 - c_a) + c_rgb * c_a
            frame_m2[wy1:wy2, lx1:lx2] = np.clip(blended, 0, 255).astype(np.uint8)
            
        # Right drape
        rx1 = max(wx1, wx2 + part_px - c_w)
        rx2 = min(wx2, wx2 + part_px)
        cw_r = rx2 - rx1
        if cw_r > 0:
            roi = frame_m2[wy1:wy2, rx1:rx2].astype(np.float32)
            c_rgb = cr_res[:, -cw_r:, :3].astype(np.float32)
            c_a = (cr_res[:, -cw_r:, 3].astype(np.float32) / 255.0) * curt_opacity
            c_a = np.expand_dims(c_a, axis=2)
            blended = roi * (1.0 - c_a) + c_rgb * c_a
            frame_m2[wy1:wy2, rx1:rx2] = np.clip(blended, 0, 255).astype(np.uint8)

    return frame_m2

# Initialize VideoWriter
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('resort_drone_flight.mp4', fourcc, FPS, (WIDTH, HEIGHT))

# Pastel living particle seed
np.random.seed(42)
PART_COUNT = 32
part_x = np.random.uniform(0, WIDTH, PART_COUNT)
part_y = np.random.uniform(0, HEIGHT, PART_COUNT)
part_r = np.random.uniform(2.0, 5.0, PART_COUNT)
part_col = [(225, 240, 250), (220, 230, 255), (200, 220, 245), (230, 245, 255)]

for f in range(TOTAL_FRAMES):
    progress = f / float(TOTAL_FRAMES - 1)
    
    # -------------------------------------------------------------------------
    # SCENE TIMELINE
    # -------------------------------------------------------------------------
    # Stage 1: [0.00 to 0.18] main1.jpg
    # Stage 2: [0.12 to 0.50] main2.jpg with doors opening & right pan
    # Stage 3: [0.44 to 0.68] banq1.jpg (curtain pass through)
    # Stage 4: [0.62 to 0.82] banq2.jpg (left dolly)
    # Stage 5: [0.78 to 0.92] banq3.jpg (aisle push)
    # Stage 6: [0.88 to 1.00] banq4.jpg (mandap finale)
    
    frame = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
    
    # 1. main1
    if progress < 0.22:
        t = progress / 0.18
        st = smoothstep(t)
        sc1 = fit_cover(img_main1, WIDTH, HEIGHT, center_x=0.5, center_y=0.35 + st * 0.15, scale=1.0 + st * 0.18)
        op1 = 1.0 - smoothstep(max(0.0, (progress - 0.12) / 0.08))
        frame = (sc1.astype(np.float32) * op1).astype(np.uint8)
        
    # 2. main2
    if 0.10 <= progress <= 0.54:
        op2_in = smoothstep((progress - 0.10) / 0.08)
        op2_out = 1.0 - smoothstep(max(0.0, (progress - 0.46) / 0.08))
        op2 = min(op2_in, op2_out)
        
        # Door opening: 0.24 to 0.42
        door_t = smoothstep(max(0.0, min(1.0, (progress - 0.24) / 0.18)))
        door_angle = door_t * 78.0
        
        # Window curtain interaction: 0.38 to 0.52
        curt_t = smoothstep(max(0.0, min(1.0, (progress - 0.38) / 0.12)))
        curt_opacity = 1.0 - smoothstep(max(0.0, (progress - 0.44) / 0.08))
        
        m2_render = render_main2_with_doors(door_angle, curt_t, curt_opacity)
        
        # Camera zoom and pan slightly to right side
        zoom_t = ease_in_out(max(0.0, min(1.0, (progress - 0.14) / 0.34)))
        right_pan_t = smoothstep(max(0.0, min(1.0, (progress - 0.26) / 0.24)))
        
        cx = 0.5 + right_pan_t * 0.075 # Move camera to right side
        cy = 0.65 - zoom_t * 0.15
        sc2 = fit_cover(m2_render, WIDTH, HEIGHT, center_x=cx, center_y=cy, scale=1.0 + zoom_t * 1.6)
        
        if op2 > 0:
            frame = np.clip(frame.astype(np.float32) + sc2.astype(np.float32) * op2, 0, 255).astype(np.uint8)

    # 3. banq1 (zoops out from window into arrival hall)
    if 0.44 <= progress <= 0.72:
        op3_in = smoothstep((progress - 0.45) / 0.08)
        op3_out = 1.0 - smoothstep(max(0.0, (progress - 0.64) / 0.08))
        op3 = min(op3_in, op3_out)
        
        push3 = ease_in_out((progress - 0.45) / 0.25)
        # At end of banq1, camera dollies to left:
        left3 = smoothstep(max(0.0, (progress - 0.60) / 0.10)) * 0.18
        
        sc3 = fit_cover(img_banq1, WIDTH, HEIGHT, center_x=0.5 + left3, center_y=0.5, scale=1.05 + push3 * 0.24)
        if op3 > 0:
            frame = np.clip(frame.astype(np.float32) * (1.0 - op3_in) + sc3.astype(np.float32) * op3, 0, 255).astype(np.uint8)

    # 4. banq2 (connects directly from left dolly into wide ballroom)
    if 0.62 <= progress <= 0.84:
        op4_in = smoothstep((progress - 0.63) / 0.08)
        op4_out = 1.0 - smoothstep(max(0.0, (progress - 0.76) / 0.08))
        op4 = min(op4_in, op4_out)
        
        sweep4 = ease_in_out((progress - 0.62) / 0.20)
        # Enters with camera glide to left
        pan4_x = 0.60 - sweep4 * 0.15
        sc4 = fit_cover(img_banq2, WIDTH, HEIGHT, center_x=pan4_x, center_y=0.5, scale=1.02 + sweep4 * 0.15)
        if op4 > 0:
            frame = np.clip(frame.astype(np.float32) * (1.0 - op4_in) + sc4.astype(np.float32) * op4, 0, 255).astype(np.uint8)

    # 5. banq3 (center aisle push)
    if 0.75 <= progress <= 0.94:
        op5_in = smoothstep((progress - 0.76) / 0.08)
        op5_out = 1.0 - smoothstep(max(0.0, (progress - 0.88) / 0.06))
        op5 = min(op5_in, op5_out)
        
        aisle5 = ease_in_out((progress - 0.76) / 0.16)
        sc5 = fit_cover(img_banq3, WIDTH, HEIGHT, center_x=0.5, center_y=0.55 - aisle5 * 0.10, scale=1.0 + aisle5 * 0.35)
        if op5 > 0:
            frame = np.clip(frame.astype(np.float32) * (1.0 - op5_in) + sc5.astype(np.float32) * op5, 0, 255).astype(np.uint8)

    # 6. banq4 (grand mandap finale)
    if progress >= 0.86:
        op6_in = smoothstep((progress - 0.87) / 0.07)
        mandap6 = ease_in_out((progress - 0.87) / 0.13)
        sc6 = fit_cover(img_banq4, WIDTH, HEIGHT, center_x=0.5, center_y=0.52 - (1.0 - mandap6) * 0.04, scale=1.15 - (1.0 - mandap6) * 0.15)
        frame = np.clip(frame.astype(np.float32) * (1.0 - op6_in) + sc6.astype(np.float32) * op6_in, 0, 255).astype(np.uint8)

    # Ambient Living Particles (Pastel Petals & Light Dust)
    for p_idx in range(PART_COUNT):
        part_x[p_idx] += np.sin(f * 0.03 + p_idx) * 0.45 + 0.15
        part_y[p_idx] += 0.55 + (p_idx % 3) * 0.25
        if part_y[p_idx] > HEIGHT:
            part_y[p_idx] = -10
            part_x[p_idx] = np.random.uniform(0, WIDTH)
        px = int(part_x[p_idx])
        py = int(part_y[p_idx])
        pr = int(part_r[p_idx])
        cv2.circle(frame, (px, py), pr, part_col[p_idx % len(part_col)], -1)

    out.write(frame)
    if f % 120 == 0 or f == TOTAL_FRAMES - 1:
        print(f"Rendered {f}/{TOTAL_FRAMES} frames ({(f/TOTAL_FRAMES*100):.1f}%)")

out.release()
print("SUCCESS: Rendered resort_drone_flight.mp4!")
