import matplotlib.pyplot as plt
import numpy as np
from scipy.datasets import face
from pathlib import Path  
from skimage.io import imread 
from model import ImagingModel

r = face(gray=True)
im = ImagingModel(r,shape)
f = np.clip(r*im.ambiant_light(0.4),0,255)
plt.figure(figsize=(15,7))
plt.subplot(121)
plt.imshow(r,cmap="gray")
plt.clim(0,225)
plt.subplot(122)
plt.imshow(r,cmap="gray")
plt.clim(0,255)
plt.imshow()