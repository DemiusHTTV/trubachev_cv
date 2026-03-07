import matplotlib.pyplot as plt
import numpy as np
from scipy.datasets import face
from pathlib import Path  
from skimage.io import imread 
from model import ImagingModel

def brightness(image):
    return np.mean(image)

def median_brightness(image):
    return np.median(image)
def contrast(image):
    return np.std(image)
def contrast_michelson(image):
    f_min , f_max =image.min(),image.max()
def varation(image):
    return (f_max-f_min)/(f_max + f_min+10**-6)
def dinamic_range(image):
    f_min , f_max = image.min(),image.max()
    return 20*np.log10(f_max/(f_min + 10**-6)) 

def mean_spatial_frenquency(image):
    grad_x = np.gradient(image,axis=1)
    grad_y =np.gradient(image,axis=0)
    sq = grad_x **2 + grad_y**2
    return np.sqrt(np.mean(sq))
r = face(gray=True)
im = ImagingModel(r,shape)
f = np.clip(r*im.ambiant_light(0.4),0,255)
print(brightness(f))
print(brightness(r))
plt.figure(figsize=(15,7))
plt.subplot(121)
plt.imshow(r,cmap="gray")
plt.clim(0,225)
plt.subplot(122)
plt.imshow(f,cmap="gray")
plt.clim(0,255)
plt.imshow()
path =Path("anna-images")
for i file in path.glob("*.jpg"):
    image = imread(file,as_gray=True)
    print(fole.stem, round(median_brightness(image),3),round(mean_spatial_frenquency(images),3))