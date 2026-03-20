from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops

dir_path = Path("TrajectoryOfMovement/out")
files = sorted(dir_path.iterdir(), key=lambda p: int(p.stem.split("_")[1]))

centers = []
for f in files:
    img = np.load(f).astype(bool)
    lbl = label(img)
    props = regionprops(lbl)
    if not props:
        continue
    cy, cx = props[0].centroid
    centers.append((cx, cy))

xs, ys = zip(*centers)
plt.plot(xs, ys, "-o", ms=3)
plt.gca().invert_yaxis()
plt.axis("equal")
plt.show()
