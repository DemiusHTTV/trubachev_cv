import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.ndimage import label, center_of_mass

path = Path("trajectory/out/")
files = sorted(path.iterdir(), key=lambda p: int(p.stem.split("_")[1]))

tracks, prev = [], []

for file in files:
    mask = np.load(file)
    labeled, num = label(mask)
    centers = [(cx, cy) for i in range(1, num+1)
               if (area := np.sum(labeled==i)) > 30
               for cy, cx in [center_of_mass(mask, labeled, i)]]
    centers.sort(key=lambda p: p[0])

    if not tracks:
        tracks = [[c] for c in centers]
    else:
        new_tracks, used = [], [False]*len(centers)
        for i, pc in enumerate(prev):
            best = min(((j, np.hypot(pc[0]-cc[0], pc[1]-cc[1]))
                        for j, cc in enumerate(centers) if not used[j]),
                       default=(-1, float('inf')), key=lambda x: x[1])
            if best[0]!=-1 and best[1]<100:
                new_tracks.append(tracks[i]+[centers[best[0]]])
                used[best[0]]=True
            else:
                new_tracks.append(tracks[i])
        new_tracks += [[c] for j,c in enumerate(centers) if not used[j]]
        tracks = new_tracks

    prev = [t[-1] for t in tracks if t]

# визуализация
plt.figure(figsize=(10,8))
for traj in tracks:
    if len(traj)>5:
        xs, ys = zip(*traj)
        plt.plot(xs, ys, 'o-', linewidth=2)
plt.gca().invert_yaxis()
plt.title('Траектории движения')
plt.show()