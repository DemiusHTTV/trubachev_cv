import numpy as np
from skimage.io import imread
import matplotlib.pyplot as plt
from skimage.color import rgb2hsv
from skimage.measure import label, regionprops
from skimage.morphology import erosion
image=imread("lektciya/bols/balls.png")
hsv=rgb2hsv(image)
hue=hsv[:,:,0]
binary=hue>0
result={}
balls_count=0
colors=[]
for color in np.unique(hue):
    # if color==0:
    #     continue
    binary = hue == color
    labeled = label(binary)
    count=np.max(labeled)
    colors.extend([color]*count)
print(len(colors))
while colors:
    value = colors.pop()
    res = [value]
    detals = []
    for color in colors:
            detals.append(color,abs(color-value))
    for key , value in deltas.items():
            if value<0.1:
                res.append(key)
                colors.remove(key)
            print(value, len(res))

    # # if not result:
    # #     result[color]=count
    # #     continue
    # # for key in list(result):
    # #     delta=abs(color - key)
    # #     if delta<0.1:
    # #         result[key]+=count
    # #         continue
    # #     else:
    # #         result[color]=count
    # #         break
    # if color not in result:
    #     result[color]=0
    # result[color]+=count
    # balls_count+=count
print(result)
print(balls_count)
plt.plot(np.diff(sorted(np.unique(hue))))
plt.show()