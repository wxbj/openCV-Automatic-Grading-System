import numpy as np
import cv2 as cv


# 获取矩形区域
def getContoursRect(contours):
    contoursRect = []
    for contour in contours:
        area = cv.contourArea(contour)
        if area > 10000:
            perimeter = cv.arcLength(contour, True)
            approx = cv.approxPolyDP(contour, 0.02 * perimeter, True)
            if len(approx) == 4 or len(approx) == 6:
                contoursRect.append(contour)
    contoursRect = sorted(contoursRect, key=cv.contourArea, reverse=True)
    return contoursRect


# 获取矩形轮廓的四角
def getCornerPoints(cont):
    peri = cv.arcLength(cont, True)
    approx = cv.approxPolyDP(cont, 0.02 * peri, True)
    return approx


# 获取选项的矩形区域
def getContourChoice(contours):
    contoursRect = []
    for contour in contours:
        area = cv.contourArea(contour)
        if area > 10000:
            perimeter = cv.arcLength(contour, True)
            approx = cv.approxPolyDP(contour, 0.06 * perimeter, True)
            if len(approx) == 4:
                contoursRect.append(contour)
    contoursRect = sorted(contoursRect, key=cv.contourArea, reverse=True)
    return contoursRect


# 排序各列选项栏
def reorderContourChoice(contours):
    myReorderContours = []
    contoursNew = np.sum(contours, 1)
    contoursNew = contoursNew[:, :, 0].reshape(4)
    for i in range(4):
        myReorderContours.append(contours[np.argsort(contoursNew)[i]])
    return myReorderContours


# 排序矩形四角的坐标
def reorderContoursPoints(points):
    pointsNew = {}
    for key, point in points.items():
        point = point.reshape((4, 2))
        pointNew = np.zeros((4, 1, 2), np.int32)
        add = point.sum(1)
        pointNew[0] = point[np.argmin(add)]  # [0,0]
        pointNew[3] = point[np.argmax(add)]  # [w,h]
        diff = np.diff(point, axis=1)
        pointNew[1] = point[np.argmin(diff)]  # [w,0]
        pointNew[2] = point[np.argmax(diff)]  # [0,h]
        pointsNew[key] = pointNew
    return pointsNew


# 姓名栏选项的划分
def splitNameBoxes(img):
    cols = np.hsplit(img[:, :324], 12)
    boxes = []
    for i in range(12):
        line = []
        rows = np.vsplit(cols[i], 10)
        for j in range(10):
            line.append(rows[j])
        boxes.append(line)
    return boxes


# 准考证号栏选项的划分
def splitAdmissionBoxes(img):
    cols = np.hsplit(img, 9)
    boxes = []
    for i in range(9):
        line = []
        rows = np.vsplit(cols[i], 10)
        for j in range(10):
            line.append(rows[j])
        boxes.append(line)
    return boxes


# 缺考栏选项的划分
def splitMissExamBoxes(img):
    cols = np.hsplit(img, 5)
    boxes = []
    for i in range(5):
        line = []
        rows = np.vsplit(cols[i], 10)
        for j in range(10):
            line.append(rows[j])
        boxes.append(line)
    return boxes


# 前三个选择栏选项的划分
def splitTheFirstThreeColumnChoiceBoxes(img):
    blocks = np.vsplit(img, 6)
    boxes = []
    for i in range(6):
        rows = np.vsplit(blocks[i][5:70, :], 5)
        for j in range(5):
            cols = np.hsplit(rows[j], 4)
            line = []
            for k in range(4):
                line.append(cols[k])
            boxes.append(line)
    return boxes


# 第四个选择栏选项的划分
def splitTheFourthColumnChoiceBoxes(img):
    blocks = np.vsplit(img, 3)
    boxes = []
    for i in range(3):
        rows = np.vsplit(blocks[i][5:140, :], 5)
        for j in range(5):
            cols = np.hsplit(rows[j], 4)
            line = []
            for k in range(4):
                line.append(cols[k])
            boxes.append(line)
    return boxes


if __name__ == "__main__":
    pass
