from learning.utilScanner import *
import cv2 as cv
import numpy as np

###################################
pathImg = "D:\BaiduSyncdisk\code\openCV-Automatic-Grading-System\learning\imgBig.jpg"
heightImg = 640
widthImg = 480
####################################
initializeTrackBar()
while True:
    img = cv.imread(pathImg)
    img = cv.resize(img, (heightImg, widthImg))
    imgGray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    imgBlur = cv.GaussianBlur(imgGray, (5, 5), 1)
    thres = valTrackbars()
    imgCanny = cv.Canny(imgBlur, thres[0], thres[1])

    kernel = np.ones((5, 5))
    imgDial = cv.dilate(imgCanny, kernel, iterations=2)
    imgCanny = cv.erode(imgDial, kernel, iterations=1)

    contours = cv.findContours(imgCanny, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[0]
    biggest = biggestContours(contours)

    biggest = reorder(biggest)

    pt1 = np.float32(biggest)
    pt2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
    matrix = cv.getPerspectiveTransform(pt1, pt2)
    imgWarpColoreds = cv.warpPerspective(img, matrix, (widthImg, heightImg))

    imgWarpColoreds = imgWarpColoreds[10:, 10:]

    imgWarpGray = cv.cvtColor(imgWarpColoreds, cv.COLOR_BGR2GRAY)
    imgAdaptThre = cv.adaptiveThreshold(imgWarpGray, 255, 1, 1, 7, 2)
    imgAdaptThre = cv.bitwise_not(imgAdaptThre)
    imgAdaptThre = cv.medianBlur(imgAdaptThre, 3)

    cv.imshow("img", imgAdaptThre)

    cv.waitKey(1)


def nothing(x):
    pass

# 创建一个黑色的图像，一个窗口
img = np.zeros((300,512,3), np.uint8)
cv.namedWindow('image')
# 创建颜色变化的轨迹栏
cv.createTrackbar('R','image',0,255,nothing)
cv.createTrackbar('G','image',0,255,nothing)
cv.createTrackbar('B','image',0,255,nothing)
# 为 ON/OFF 功能创建开关
switch = '0 : OFF \n1 : ON'
cv.createTrackbar(switch, 'image',0,1,nothing)
while(1):
    cv.imshow('image',img)
    k = cv.waitKey(1) & 0xFF
    if k == 27:
        break
    # 得到四条轨迹的当前位置
    r = cv.getTrackbarPos('R','image')
    g = cv.getTrackbarPos('G','image')
    b = cv.getTrackbarPos('B','image')
    s = cv.getTrackbarPos(switch,'image')
    if s == 0:
        img[:] = 0
    else:
        img[:] = [b,g,r]
cv.destroyAllWindows()