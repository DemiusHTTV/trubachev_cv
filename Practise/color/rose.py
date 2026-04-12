import cv2
import matplotlib.pyplot as plt
import numpy as np

image = cv2.imread("data/rose.jpg")
hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)

lower = np.array([0,200,100])
upper = np.array([0,255,255])

mask = cv2.inRange(hsv, lower,upper)
mask = cv2.morphologyEx(mask,cv2.MORPH_CLOSE,np.ones((11,11)))

result = cv2.bitwise_and(image,image,mask=mask)



plt.subplot(121)
plt.imshow(cv2.cvtColor(image,cv2.COLOR_BGR2RGB))
plt.subplot(122)
plt.imshow(cv2.cvtColor(result,cv2.COLOR_BGR2RGB))
plt.show()