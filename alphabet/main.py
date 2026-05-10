import os
from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np
from skimage.io import imread
from skimage.measure import label, regionprops

os.environ.setdefault("MPLCONFIGDIR", "/tmp/mpl")

BASE_DIR = Path(__file__).resolve().parent

DEBUG_8B = False
VLINES_B8_THRESHOLD = 0.2
ASPECT_DASH_THRESHOLD = 2.5
HOLE_CY_P_THRESHOLD = 0.40
HOLE_AREA_A_THRESHOLD = 0.12
HOLE_AREA_BIG_THRESHOLD = 0.33
ECCENTRICITY_D_THRESHOLD = 0.60
ASPECT_D_THRESHOLD = 0.75


def first_existing_path(*candidates) :
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return candidates[0]


def count_holes(region) :
    shape = region.image.shape
    padded = np.zeros((shape[0] + 2, shape[1] + 2), dtype=bool)
    padded[1:-1, 1:-1] = region.image
    inverted = np.logical_not(padded)
    labeled = label(inverted)
    return int(np.max(labeled) - 1)


def largest_hole_stats(region):
    shape = region.image.shape
    padded = np.zeros((shape[0] + 2, shape[1] + 2), dtype=bool)
    padded[1:-1, 1:-1] = region.image
    inverted = np.logical_not(padded)
    labeled = label(inverted)

    inner = []
    for r in regionprops(labeled):
        minr, minc, maxr, maxc = r.bbox
        if minr == 0 or minc == 0 or maxr == labeled.shape[0] or maxc == labeled.shape[1]:
            continue
        inner.append(r)

    if not inner:
        return 0.0, 0.0

    h = max(inner, key=lambda r: r.area)
    hole_area = float(h.area) / float(region.image.size)
    hole_cy = float(h.centroid[0]) / float(region.image.shape[0])
    return hole_area, hole_cy


def classificator(region):
    holes = count_holes(region)

    if holes == 2:  # B,8
        vlines = (np.sum(region.image, 0) == region.image.shape[0]).sum()
        vlines = vlines / region.image.shape[1]
        decision = "B" if vlines > VLINES_B8_THRESHOLD else "8"
        if DEBUG_8B:
            print(f"label={region.label} holes=2 vlines={vlines:.4f} -> {decision}")
        return decision

    if holes == 1:  # A,0,P,D
        hole_area, hole_cy = largest_hole_stats(region)
        aspect = region.image.shape[1] / region.image.shape[0]

        if hole_cy < HOLE_CY_P_THRESHOLD:
            return "P"
        if hole_area < HOLE_AREA_A_THRESHOLD:
            return "A"
        if hole_area > HOLE_AREA_BIG_THRESHOLD:
            if (region.eccentricity < ECCENTRICITY_D_THRESHOLD) or (aspect > ASPECT_D_THRESHOLD):
                return "D"
        return "0"

    # holes == 0: 1,W,X,*,-,/
    if region.image.sum() / region.image.size == 1.0:
        return "-"

    shape = region.image.shape
    aspect = shape[1] / shape[0]
    if aspect > ASPECT_DASH_THRESHOLD:
        return "-"

    aspect2 = np.min(shape) / np.max(shape)
    if aspect2 > 0.9:
        return "*"

    vlines = (np.sum(region.image, 0) == region.image.shape[0]).sum()
    hlines = (np.sum(region.image, 1) == region.image.shape[1]).sum()
    if vlines > 0 and hlines > 0:
        return "1"

    labeled = label(np.logical_not(region.image))
    bays = 0
    for r in regionprops(labeled):
        if r.area > 3:
            bays += 1
    if bays == 2:
        return "/"
    if bays == 4:
        return "X"
    if bays == 5:
        return "W"
    return "?"


if len(sys.argv) > 1:
    arg_path = Path(sys.argv[1]).expanduser()
    if arg_path.is_absolute():
        input_candidate = arg_path
    else:
        input_candidate = first_existing_path(Path.cwd() / arg_path, BASE_DIR / arg_path)
else:
    input_candidate = BASE_DIR / "symbols.png"

input_path = first_existing_path(
    input_candidate,
    BASE_DIR / "symbols.png",
    Path("symbols.png"),
)

image = imread(str(input_path))[:, :, :3]
abinary = image.mean(2) > 0

alabeled = label(abinary)
aprops = regionprops(alabeled)

results: dict[str, int] = {}

image_path = BASE_DIR / "out"
image_path.mkdir(parents=True, exist_ok=True)

plt.figure(figsize=(5, 7))

for region in aprops:
    symbol = classificator(region)
    results[symbol] = results.get(symbol, 0) + 1

    plt.cla()
    plt.title(f"Class - '{symbol}'")
    plt.imshow(region.image)
    plt.axis("off")
    plt.savefig(image_path / f"image_{region.label}.png", bbox_inches="tight", pad_inches=0.02)

print(results)

plt.imshow(abinary)
plt.show()