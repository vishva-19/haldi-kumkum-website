import cv2
import numpy as np

pano = cv2.imread('/tmp/stitched_facade.jpg') # 1080x1376
h, w = pano.shape[:2]
target_w, target_h = 1920, 1080

# To cover 1920x1080, base scale must be max(1920/1376, 1080/1080) = 1.39535
base_scale = max(target_w / float(w), target_h / float(h))
# Pre-scale pano with high quality lanczos so it is at least 1920 wide
base_w = int(w * base_scale * 1.5) # extra margin for camera movement
base_h = int(h * base_scale * 1.5)
pano_large = cv2.resize(pano, (base_w, base_h), interpolation=cv2.INTER_LANCZOS4)
print(f"Pano pre-scaled to: {base_w}x{base_h}")

def safe_camera(img, cx_norm, cy_norm, zoom=1.0, roll=0.0):
    ih, iw = img.shape[:2]
    # Center pixel
    cx = iw * cx_norm
    cy = ih * cy_norm
    
    # We want a 1920x1080 window
    eff_zoom = zoom
    M = cv2.getRotationMatrix2D((cx, cy), roll, eff_zoom)
    M[0, 2] += (target_w / 2.0) - cx * eff_zoom
    M[1, 2] += (target_h / 2.0) - cy * eff_zoom
    
    # Use BORDER_REPLICATE or BORDER_CONSTANT, but with our large margin it will never be out of bounds!
    warped = cv2.warpAffine(img, M, (target_w, target_h), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REPLICATE)
    return warped

# Test at top (sky)
f_top = safe_camera(pano_large, 0.5, 0.25, zoom=0.6)
cv2.imwrite('/tmp/test_safe_top.jpg', f_top)

# Test at bottom courtyard
f_courtyard = safe_camera(pano_large, 0.5, 0.75, zoom=0.75)
cv2.imwrite('/tmp/test_safe_courtyard.jpg', f_courtyard)

print("Safe camera frames generated!")
