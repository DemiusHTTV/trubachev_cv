import matplotlib.pyplot as plt
import numpy as np
from skimage.measure import label, regionprops
from skimage.io import imread
from pathlib import Path

save_path = Path("lektciya/alphabet/alphabet.png").parent

DEBUG_8B = False

MIRROR_8B_THRESHOLD = None


def mirror_diff(image: np.ndarray) -> float:

    image = image.astype(bool)
    on = int(image.sum())
    if on == 0:
        return 1.0

    w = image.shape[1]
    half = w // 2
    left = image[:, :half]
    right = image[:, w - half :]
    right = np.fliplr(right)

    mismatch = np.logical_xor(left, right).sum()
    return float(mismatch) / float(on)


def count_holes(region):
    shape = region.image.shape
    new_image = np.zeros((shape[0]+2, shape[1]+2), dtype=bool)
    new_image[1:-1, 1:-1] = region.image
    new_image=np.logical_not(new_image)
    labeled = label(new_image)
    return np.max(labeled)-1
def extractor(region):
    cy,cx = region.centroid_local
    cy/= region.image.shape[0]
    cx/= region.image.shape[1]
    perimeter = region.perimeter/region.image.size
    holes=count_holes(region)
    vlines =(np.sum(region.image, axis=0) / region.image.shape[0]).sum()
    hlines = (np.sum(region.image, axis=1) / region.image.shape[1]).sum()
    eccentricity = region.eccentricity
    aspect= region.image.shape[1]/region.image.shape[0]
    return np.array([region.area/region.image.size,cy,cx,perimeter,holes,vlines,hlines,eccentricity,aspect])

def classificator(region, templates):

    if count_holes(region) == 2:
        diff = mirror_diff(region.image)
        thr = MIRROR_8B_THRESHOLD if MIRROR_8B_THRESHOLD is not None else 0.25
        decision = "8" if diff <= thr else "B"
        if DEBUG_8B:
            print(
                f"label={region.label} holes=2 mirror_diff={diff:.4f} "
                f"thr={thr:.4f} -> {decision}"
            )
        return decision

    features = extractor(region)
    result = ""
    min_d = 10**16
    for symbol, t in templates.items():
        d = (((t - features)**2).sum()) **0.5
        if d < min_d:
            result = symbol
            min_d = d
    return result

template = imread("lektciya/alphabet/alphabet-small.png")[:,:,:-1]
#print(template.shape)
template = template.sum(2)
binary = template != 765.

labeled = label(binary)
props = regionprops(labeled)
#print(type(props))

templates = {}
mirror_templates = {}

for region, symbol in zip (props,["8", "O",
                                  "A", "B", "1", "W",
                                  "X","*", "/","-" ]):
    templates[symbol] = extractor(region)
    mirror_templates[symbol] = mirror_diff(region.image)

# Calibrate threshold for 8 vs B using the same template font.
if ("8" in mirror_templates) and ("B" in mirror_templates):
    MIRROR_8B_THRESHOLD = (mirror_templates["8"] + mirror_templates["B"]) / 2.0
    if DEBUG_8B:
        print(
            f"calibration: mirror8={mirror_templates['8']:.4f} "
            f"mirrorB={mirror_templates['B']:.4f} thr={MIRROR_8B_THRESHOLD:.4f}"
        )

image = imread("lektciya/alphabet/alphabet.png")[:,:,:-1]
abinary = image.mean(2)>0
alabeled = label(abinary)
print(np.max(alabeled))
aprops = regionprops(alabeled)
results = {}
image_path = save_path / "out"
image_path.mkdir(exist_ok=True)
#plt.ion()
plt.figure(figsize=(5,7))
for region in aprops:
    symbol = classificator(region, templates)
    if symbol not in results:
        results[symbol] = 0
    results[symbol] += 1
    plt.cla()
    plt.title(f"Class - '{symbol}'")
    plt.imshow(region.image)
    plt.savefig(image_path / f"image_{region.label}.png")
print(results)
print((props[1]))
#print(templates)
#print(classificator(props[0],templates))
plt.imshow(abinary)
plt.show()
