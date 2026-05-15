import numpy as np
import time
import pyautogui
import cv2
import mss
from skimage.measure import regionprops, label

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.0001

y1 = 95
y2 =115 
x1 = 300
x2 = 311
def enemy_here(binary, shift):
    area = binary[y1:y2, x1+shift:x2+shift]

    if len(regionprops(label(area))) > 0 :
            pyautogui.keyUp('down')    
            pyautogui.press('space')   
            time.sleep(0.25 ) 
            pyautogui.keyDown('down')


monitor = {
    'left': 400,
    'top': 300,
    'width': 1200,
    'height': 600
}

print("3 секунды...")
time.sleep(3)
pyautogui.press('space')

sct = mss.MSS()
start_time = time.time()

while True:
    screenshot = np.array(sct.grab(monitor))
    frame = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    elapsed = time.time() - start_time
    shift = min(int(elapsed * 0.8), 100)
    _, binary = cv2.threshold(
        frame,
        0,
        255,
        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )

    enemy_here(binary, shift)

    debug = cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)

    cv2.rectangle(
        debug,
        (x1+shift, y1),
        (x2+shift, y2),
        (0, 0, 255),
        2
    ) 
    
 
    cv2.imshow("T-Rex Bot", debug)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cv2.destroyAllWindows()