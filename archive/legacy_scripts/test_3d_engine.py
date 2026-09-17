import cv2
import numpy as np
import math

# Test 3D perspective camera projection on main2.jpg
img = cv2.imread('img/main2.jpg')
h, w = img.shape[:2]

# Create depth map for main2:
# Ground plane (brick courtyard) is in lower half (y > 450)
# Building facade is in middle (y: 150 to 580)
# Sky is in upper half (y < 200)
y_coords, x_coords = np.mgrid[0:h, 0:w]

# Approximate depth Z:
# Foreground ground: Z ~ 1.0 at bottom (y=h) to Z ~ 5.0 at base of building (y=580)
# Building facade: Z ~ 5.0 to 6.0
# Sky / distance: Z ~ 20.0
Z = np.ones((h, w), dtype=np.float32) * 5.5

# Ground plane depth gradient
ground_mask = y_coords > 480
Z[ground_mask] = 1.0 + (h - y_coords[ground_mask]) / float(h - 480) * 4.5

print("Depth map generated, min Z:", np.min(Z), "max Z:", np.max(Z))

# Let's test a forward camera push (dZ = 0.5) with perspective remap
f = float(w) * 0.9 # focal length
cx = w / 2.0
cy = h / 2.0

# Virtual camera movement: push forward by delta_z = 1.2
delta_z = 1.2
# Projected 3D points
X_3d = (x_coords - cx) * Z / f
Y_3d = (y_coords - cy) * Z / f
Z_3d = Z - delta_z

# Re-project to source image
new_x = (X_3d * f / Z_3d) + cx
new_y = (Y_3d * f / Z_3d) + cy

warped = cv2.remap(img, new_x.astype(np.float32), new_y.astype(np.float32), cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REFLECT)
cv2.imwrite('/tmp/test_3d_push.jpg', warped)
print("Successfully generated 3D camera push frame!")
