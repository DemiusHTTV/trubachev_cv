import numpy as np
from skimage.measure import label
from skimage.morphology import opening
import matplotlib.pyplot as plt

image = np.load("StarsTask/stars.npy")

plusses_structure = np.array (([0, 0, 1, 0, 0],
                         [0, 0, 1, 0, 0],
                         [1, 1, 1, 1, 1],
                         [0, 0, 1, 0, 0],
                         [0, 0, 1, 0, 0]))


cross_structure = np.array (([1, 0, 0, 0, 1],
                          [0, 1, 0, 1, 0],
                          [0, 0, 1, 0, 0],
                          [0, 1, 0, 1, 0],
                          [1, 0, 0, 0, 1]))

pluses = opening(image, plusses_structure)
crosses = opening(image, plusses_structure)
process = pluses + crosses

labeled_pluses = label(pluses)
labeled_crosses = label(crosses)
pluses_count = np.max(labeled_pluses)
crosses_count = np.max(labeled_crosses)

print(f"Количество плюсов: {pluses_count}")
print(f"Количество крестов: {crosses_count}")
print(f"Всего звезд: {pluses_count + crosses_count}")

plt.subplot(121)
plt.imshow(image)
plt.subplot(122)
plt.imshow(process)
plt.show()