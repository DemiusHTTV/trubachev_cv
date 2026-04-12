import cv2

mush = cv2.imread("data/mushroom.jpg",
                  cv2.IMREAD_UNCHANGED)

logo = cv2.imread("data/cvlogo.png",
                  cv2.IMREAD_ANYCOLOR)[:,:-1]

roi = mush[:logo.shape[0],:logo.shape[1]]
logo = cv2.resize(logo,logo.shape[1]//2 , logo.shape[0]//2)
logo_gray = cv2.cvtColor(logo,cv2.COLOR_BGR2GRAY)
ret, mask = cv2.threshold(logo_gray,10,255,cv2.THRESH_BINARY)

print(ret)


cv2.namedWindow("Result", cv2.WINDOW_GUI_NORMAL)
cv2.imshow('ResultT',mush)
cv2.waitKey(0)
cv2.destroyAllWindows()
print(mush.shape)