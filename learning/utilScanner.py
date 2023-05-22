import cv2 as cv
import numpy as np


def nothing(x):
    pass


def initializeTrackBar():
    cv.namedWindow("TrackBar")
    cv.resizeWindow("TrackBar", 360, 180)
    cv.createTrackbar("Thresh1", "TrackBar", 106, 255, nothing)
    cv.createTrackbar("Thresh2", "TrackBar", 74, 255, nothing)
    cv.createTrackbar("dilate", "TrackBar", 2, 5, nothing)
    cv.createTrackbar("erode", "TrackBar", 1, 5, nothing)


def valTrackbars():
    Thresh1 = cv.getTrackbarPos("Thresh1", "TrackBar")
    Thresh2 = cv.getTrackbarPos("Thresh2", "TrackBar")
    dilate = cv.getTrackbarPos("dilate", "TrackBar")
    erode = cv.getTrackbarPos("erode", "TrackBar")
    return [Thresh1, Thresh2, dilate, erode]


def biggestContours(contours):
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


def reorder(point):
    point = point.reshape((4, 2))
    pointNew = np.zeros((4, 1, 2), np.int32)
    add = point.sum(1)
    pointNew[0] = point[np.argmin(add)]  # [0,0]
    pointNew[3] = point[np.argmax(add)]  # [w,h]
    diff = np.diff(point, axis=1)
    pointNew[1] = point[np.argmin(diff)]  # [w,0]
    pointNew[2] = point[np.argmax(diff)]  # [0,h]

    return pointNew
