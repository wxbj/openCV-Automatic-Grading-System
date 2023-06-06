import cv2 as cv
import numpy as np
import pandas


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
        if 10000 < area < 100000:
            perimeter = cv.arcLength(contour, True)
            approx = cv.approxPolyDP(contour, 0.02 * perimeter, True)
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


# 主观题和科目栏选项的划分
def splitSubjectiveQuestionsAndSubject(img):
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
    # 第一部分
    rows = np.vsplit(blocks[0][5:70, :], 5)
    for j in range(5):
        cols = np.hsplit(rows[j], 4)
        line = []
        for k in range(4):
            line.append(cols[k])
        boxes.append(line)
    # 第二部分
    rows = np.vsplit(blocks[1][5:75, :], 5)
    for j in range(5):
        cols = np.hsplit(rows[j], 4)
        line = []
        for k in range(4):
            line.append(cols[k])
        boxes.append(line)
    # 第三部分
    rows = np.vsplit(blocks[2][5:75, :], 5)
    for j in range(5):
        cols = np.hsplit(rows[j], 4)
        line = []
        for k in range(4):
            line.append(cols[k])
        boxes.append(line)
    # 第四部分
    rows = np.vsplit(blocks[3][10:75, :], 5)
    for j in range(5):
        cols = np.hsplit(rows[j], 4)
        line = []
        for k in range(4):
            line.append(cols[k])
        boxes.append(line)
    # 第五部分
    rows = np.vsplit(blocks[4][10:80, :], 5)
    for j in range(5):
        cols = np.hsplit(rows[j], 4)
        line = []
        for k in range(4):
            line.append(cols[k])
        boxes.append(line)
    # 第六部分
    rows = np.vsplit(blocks[5][10:80, :], 5)
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
    # 第一部分
    rows = np.vsplit(blocks[0][10:140, :], 5)
    for j in range(5):
        cols = np.hsplit(rows[j], 4)
        line = []
        for k in range(4):
            line.append(cols[k])
        boxes.append(line)
    # 第二部分
    rows = np.vsplit(blocks[1][10:140, :], 5)
    for j in range(5):
        cols = np.hsplit(rows[j], 4)
        line = []
        for k in range(4):
            line.append(cols[k])
        boxes.append(line)
    # 第三部分
    rows = np.vsplit(blocks[2][15:145, :], 5)
    for j in range(5):
        cols = np.hsplit(rows[j], 4)
        line = []
        for k in range(4):
            line.append(cols[k])
        boxes.append(line)

    return boxes


# 姓名栏、准考证栏、主观题栏、考试科目栏填涂检测
def detectNameAdmissionSubject(darryBoxes, number, optionNumber):
    choice = []
    for i in range(number):
        id = -1
        max = -1
        for j in range(optionNumber):
            if cv.countNonZero(darryBoxes[i][j]) >= max:
                max = cv.countNonZero(darryBoxes[i][j])
                id = j
        if max >= 200:
            choice.append(id)
    return choice


# 缺考栏填涂检测
def detectMissExam(darryBoxes, number):
    choice = ["否"]
    if cv.countNonZero(darryBoxes[number]) >= 100:
        choice = ["是"]
    return choice


# 单选填涂检测
def detectSingleChoice(darryBoxes, number, optionNumber, numberToLetter):
    choice = []
    choiceLetter = []
    for i in range(number):
        id = -1
        max = -1
        number = 0  # 用于检测多选
        for j in range(optionNumber):
            if cv.countNonZero(darryBoxes[i][j]) >= max:
                max = cv.countNonZero(darryBoxes[i][j])
                if max >= 200:  # 若有多个选中，要记录下来
                    number += 1
                if number == 2:  # 多选，直接跳出本次循环
                    id = -1
                    break
                else:
                    id = j
        if number == 2:  # 多选
            choice.append(id)
        elif max >= 200:  # 正常选择
            choice.append(id)
        else:  # 空选
            choice.append(-1)
    for i in choice:
        choiceLetter.append(numberToLetter[i])
    return choiceLetter


# 多选填涂检测
def detectMultipleChoice(darryBoxes, number, optionNumber, numberToLetter):
    choices = []
    choiceLetter = []
    for i in range(number):
        listChoice = []
        for j in range(optionNumber):
            if cv.countNonZero(darryBoxes[i][j]) >= 200:
                listChoice.append(j)
        choices.append(listChoice)
    for choice in choices:
        strChoice = ""
        for i in choice:
            strChoice += numberToLetter[i]
        choiceLetter.append(strChoice)
    return choiceLetter


# 解决opencv不支持中文路径问题
def cv_imread(file_path):
    return cv.imdecode(np.fromfile(file_path, dtype=np.uint8), -1)


# 跟踪栏值更改的回调函数
def nothing(x):
    pass


# 初始化界面
def initializeInterface():
    cv.namedWindow("settings", cv.WINDOW_NORMAL)
    cv.resizeWindow("settings", 500, 500)
    cv.createTrackbar("gaussBlur", "settings", 2, 5, nothing)
    cv.createTrackbar("minThresh", "settings", 10, 255, nothing)
    cv.createTrackbar("maxThresh", "settings", 50, 255, nothing)
    cv.createTrackbar("kernel", "settings", 2, 10, nothing)
    cv.createTrackbar("dilate", "settings", 1, 5, nothing)
    cv.createTrackbar("erosion", "settings", 0, 5, nothing)
    cv.createTrackbar("minChoice", "settings", 50, 255, nothing)
    cv.createTrackbar("maxChoice", "settings", 200, 255, nothing)
    cv.createTrackbar("kerChoice", "settings", 2, 10, nothing)
    cv.createTrackbar("dilChoice", "settings", 2, 5, nothing)
    cv.createTrackbar("eroChoice", "settings", 1, 5, nothing)


# 获取滑动条数值
def getValTrackbars():
    GaussianBlur = cv.getTrackbarPos("gaussBlur", "settings")
    minCannyThresh = cv.getTrackbarPos("minThresh", "settings")
    maxCannyThresh = cv.getTrackbarPos("maxThresh", "settings")
    kernel = cv.getTrackbarPos("kernel", "settings")
    dilate = cv.getTrackbarPos("dilate", "settings")
    erosion = cv.getTrackbarPos("erosion", "settings")
    minCannyChoice = cv.getTrackbarPos("minChoice", "settings")
    maxCannyChoice = cv.getTrackbarPos("maxChoice", "settings")
    kernelChoice = cv.getTrackbarPos("kerChoice", "settings")
    dilateChoice = cv.getTrackbarPos("dilChoice", "settings")
    erosionChoice = cv.getTrackbarPos("eroChoice", "settings")
    return [GaussianBlur*2+1, minCannyThresh, maxCannyThresh, kernel, dilate, erosion, minCannyChoice, maxCannyChoice,
            kernelChoice,
            dilateChoice, erosionChoice]
