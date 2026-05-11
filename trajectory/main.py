from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops

path_of_dir = Path("trajectory/out")
files = sorted(path_of_dir.iterdir(), key=lambda n: int(n.stem.split("_")[1]))


trajectories = [[] for _ in range(3)]

for file in files:
    img = np.load(file).astype(bool)
    lbl = label(img)
    props = regionprops(lbl)
    
 
    props_sorted = sorted(props, key=lambda p: p.centroid[1])  # по x
    
    for i, prop in enumerate(props_sorted):
        if i < 3:  
            cy, cx = prop.centroid
            trajectories[i].append((cx, cy))

plt.figure(figsize=(10, 10))
colors = ['red', 'green', 'blue']
for i, traj in enumerate(trajectories):
    if traj:
        x, y = zip(*traj)
        plt.plot(x, y, "-o", ms=3, color=colors[i], label=f"Траектория {i+1}")

plt.gca().invert_yaxis()
plt.axis("equal")
plt.legend()
plt.title("Траектории движения")
plt.show()

print(f"Найдено траекторий: {len([t for t in trajectories if t])}")