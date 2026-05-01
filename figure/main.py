import matplotlib.pyplot as plt
from skimage.measure import label, regionprops
from skimage.morphology import binary_erosion,binary_dilation
from skimage.color import rgb2hsv
from collections import defaultdict
import numpy as np

def count_figure_and_color(regions):
    cnt = 0
    colors = []
    rect = defaultdict(int)
    circle = defaultdict(int)

    for r in regions:
        if r.eccentricity==0:
            y,x=r.centroid
            hsv_color = hsv_image[int(y),int(x),0]
            colors.append(round(hsv_color,1))
            circle[str(round(hsv_color,1))] += 1
            cnt += 1
        else:
            y,x=r.centroid
            hsv_color = hsv_image[int(y),int(x),0]
            colors.append(round(hsv_color,1))
            rect[str(round(hsv_color,1))] += 1
            cnt += 1
        
    #print(colors)
    return cnt,colors,rect,circle

image = plt.imread("balls_and_rects.png")
hsv_image = rgb2hsv(image)
gray = image.mean(axis = 2)


gray[gray>0]=1
gray[gray<1]=0
binary = binary_erosion(gray)
labeled = label(binary)
regions = regionprops(labeled)

cnt,colors,rect_res,circle_res=count_figure_and_color(regions)

print("Quantity of all figure:",cnt)


print("Quantity of rectangle:",sum(rect_res.values()))
for key in rect_res:
    print(f"Shade of rectangle {key}: {rect_res[key]}")
print()
print("Quantity of circle:",sum(circle_res.values()))
for key in circle_res:
    print(f"Shade of circle {key}: {circle_res[key]}")
