import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label
from skimage.morphology import opening


image = np.load('StarsTask/stars.npy')
plt.imshow(image, cmap="gray")
print(plt.get_backend())
plt.show
input("Press Enter to exit")
