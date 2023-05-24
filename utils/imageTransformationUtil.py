import cv2 as cv
import numpy as np


# 跟踪栏值更改的回调函数
def nothing(x):
    pass


# 初始化界面
def initializeInterface():
    cv.namedWindow("settings", cv.WINDOW_NORMAL)
    cv.createTrackbar("minThresh", "settings", 106, 255, nothing)
    cv.createTrackbar("maxThresh", "settings", 74, 255, nothing)
    cv.createTrackbar("dilate", "settings", 2, 5, nothing)
    cv.createTrackbar("erode", "settings", 1, 5, nothing)


# 获取滑动条数值
def getValTrackbars():
    Thresh1 = cv.getTrackbarPos("minThresh", "settings")
    Thresh2 = cv.getTrackbarPos("maxThresh", "settings")
    dilate = cv.getTrackbarPos("dilate", "settings")
    erode = cv.getTrackbarPos("erode", "settings")
    return [Thresh1, Thresh2, dilate, erode]


# 查找最大的轮廓
def getBiggestContours(contours):
    biggest = []
    max_area = 0
    for contour in contours:
        area = cv.contourArea(contour)
        peri = cv.arcLength(contour, True)
        approx = cv.approxPolyDP(contour, 0.02 * peri, True)
        if area > max_area and len(approx) == 4:
            biggest = approx
            max_area = area
    return biggest


# 重新排列轮廓的四点
def reorderFourPoints(point):
    point = point.reshape((4, 2))
    pointNew = np.zeros((4, 1, 2), np.int32)
    add = point.sum(1)
    pointNew[0] = point[np.argmin(add)]  # [0,0]
    pointNew[3] = point[np.argmax(add)]  # [w,h]
    diff = np.diff(point, axis=1)
    pointNew[1] = point[np.argmin(diff)]  # [w,0]
    pointNew[2] = point[np.argmax(diff)]  # [0,h]

    return pointNew
