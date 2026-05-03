import cv2
import time
import numpy as np

tv = cv2.imread('news.jpg', cv2.IMREAD_COLOR)

cam = cv2.VideoCapture(0)
pts2 = np.array([[18, 25], [432, 53], [435, 270], [30, 294]], dtype="f4")
prev_time = time.perf_counter()
print(tv)
while cam.isOpened():
    ret, frame = cam.read()
    rows, cols, _ = frame.shape
    pts1 = np.array([[0, 0], [cols, 0], [cols, rows], [0, rows]], dtype="f4")
    m = cv2.getPerspectiveTransform(pts1, pts2)
    transform = cv2.warpPerspective(frame, m, (tv.shape[1], tv.shape[0]))
    gray = cv2.cvtColor(transform, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
    print(tv)
    background = cv2.bitwise_and(tv, tv, mask=cv2.bitwise_not(mask))
    foreground = cv2.bitwise_and(transform, transform, mask=mask)
    result = cv2.add(background, foreground)
    cv2.imshow ("result",result)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    curr_time = time.perf_counter()
    print(f"FPS = {1 / (curr_time - prev_time):.1f}")
    prev_time = curr_time

cam.release()
cv2.destroyAllWindows()