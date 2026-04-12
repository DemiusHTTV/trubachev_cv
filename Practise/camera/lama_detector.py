import matplotlib.pyplot as plt 
import numpy as np
from skimage.measure import label, regionprops
from skimage.io import imread
from skimage.filters import sobel
from skimage.morphology import closing

image = imread("lama_on_moon.png")[31:-50,40:-20,:-1]
print(image.shape)
gray = image.mean(2)
contour = sobel(gray)
binary = contour>15
binary = closing(binary, footprint=np.ones((3,3)))
labled = label(binary)


def neighbours4(binary,y,x):
    return (y,x+1),(y,x-1),(y+1,x),(y-1,x)


def fill(binary,y,x):
    if binary[y,x]==0:
        binary[y,x]=1
    for yn,xn in neighbours4(binary,y,x):
        if yn>len(binary[1]) or xn >len(binary[0]):
            break
        if binary[y,x]==0:
            fill(binary,yn,xn)
    

# for region in regionprops(labled):
#     if region.area < 1000:
#         rr,cc = region.coords[:,0], region.coords[:,1]
#         binary[rr,cc] = 0


regions = regionprops(labled)
regions = sorted(regions, key=lambda region: region.perimeter)
region = regions[-1]
fill(region,0,0)
plt.imshow(labled == region.label)
plt.show()
plt.imsave('lama_binary.png', binary)