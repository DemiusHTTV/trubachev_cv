import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label
from skimage.morphology import binary_opening

image=np.load("PClook/14.03/wires6.npy")
struct=np.ones((3,1))
process=binary_opening(image,struct)

labeled_image=label(image)
labeled_process=label(process)

print(f"Original: {np.max(labeled_image)}")
print(f"Processed: {np.max(labeled_process)}\n")


for wire_num in range(1, np.max(labeled_image) + 1):
    wire_mask = (labeled_image == wire_num)
    wire_parts = labeled_process[wire_mask]
    unique_parts = np.unique(wire_parts[wire_parts > 0])
    num_parts = len(unique_parts)
    if num_parts == 0:
        result = "нет"
    elif num_parts == 1:
        result = "целый"
    else:
        result = str(num_parts)
    print(f"провод {wire_num}, {result} ")

plt.subplot(121)
plt.imshow(image) 

plt.subplot(122)
plt.imshow(process)

plt.show()