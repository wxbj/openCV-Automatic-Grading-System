import cv2 as cv
import numpy as np
import pandas
from test.imageTest import *


############################图片处理相关##########################

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
    choice = []
    choiceLetter = []
    for i in range(number):
        listChoice = []
        for j in range(optionNumber):
            if cv.countNonZero(darryBoxes[i][j]) >= 100:
                listChoice.append(j)
        choice.append(listChoice)
    for choice in choice:
        strChoice = ""
        for i in choice:
            strChoice += numberToLetter[i]
        choiceLetter.append(strChoice)
    return choiceLetter


################################参数设置相关#######################################

# 窗口回调函数
def nothing(x):
    pass


# 初始化滑动条
def initializeTrackBar():
    cv.namedWindow("TrackBar")
    cv.resizeWindow("TrackBar", 360, 180)
    cv.createTrackbar("Thresh1", "TrackBar", 106, 255, nothing)
    cv.createTrackbar("Thresh2", "TrackBar", 74, 255, nothing)
    cv.createTrackbar("dilate", "TrackBar", 2, 5, nothing)
    cv.createTrackbar("erode", "TrackBar", 1, 5, nothing)


# 获取滑动条数值
def valTrackbars():
    Thresh1 = cv.getTrackbarPos("Thresh1", "TrackBar")
    Thresh2 = cv.getTrackbarPos("Thresh2", "TrackBar")
    dilate = cv.getTrackbarPos("dilate", "TrackBar")
    erode = cv.getTrackbarPos("erode", "TrackBar")
    return [Thresh1, Thresh2, dilate, erode]


# 查找最大的轮廓
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


# 重新排列轮廓的四点
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


###################################窗口相关########################################

# 返回评分列表
def getGradingLists(answer, replyUrls):
    subject = answer['考试科目栏:']
    firstColumnAnswer = answer['选择第一栏:']
    secondColumnAnswer = answer['选择第二栏:']
    thirdColumnAnswer = answer['选择第三栏:']
    fourthColumnAnswer = answer['选择第四栏:']

    replys = []
    for replyUrl in replyUrls:
        try:
            replys.append(getAnswer(replyUrl))
            continue
        except Exception:
            continue

    gradings = []
    for reply in replys:
        student = []
        if (reply['考试科目栏:'] == subject) and (reply['缺考栏:'] == ['否']):
            student.append(''.join('%s' % id for id in reply["准考证号栏:"]))
            student.append(''.join('%s' % id for id in reply["姓名栏:"]))
            firstColumnGrading = getSingleChoiceGrad(firstColumnAnswer, reply["选择第一栏:"])
            secondColumnGrading = getSingleChoiceGrad(secondColumnAnswer, reply["选择第二栏:"])
            singleChoiceGrad = firstColumnGrading + secondColumnGrading
            student.append(singleChoiceGrad)
            thirdColumnGrading = getMultipleChoiceGrad(thirdColumnAnswer, reply["选择第三栏:"])
            fourthColumnGrading = getMultipleChoiceGrad(fourthColumnAnswer, reply["选择第四栏:"])
            multipleChoiceGrad = thirdColumnGrading + fourthColumnGrading
            student.append(multipleChoiceGrad)
            subjectiveGrad = int(''.join('%s' % id for id in reply["主观题栏:"]))
            student.append(subjectiveGrad)
            student.append(singleChoiceGrad + multipleChoiceGrad + subjectiveGrad)
            totalGrad = singleChoiceGrad + multipleChoiceGrad + subjectiveGrad
            if totalGrad >= 90:
                student.append("优秀")
            elif 80 <= totalGrad < 90:
                student.append("良好")
            elif 70 <= totalGrad < 80:
                student.append("中")
            elif 60 <= totalGrad < 70:
                student.append("差")
            else:
                student.append("不及格")
            gradings.append(student)
        elif reply['考试科目栏:'] != subject:
            student.append(''.join('%s' % id for id in reply["准考证号栏:"]))
            student.append(''.join('%s' % id for id in reply["姓名栏:"]))
            student.append(0)
            student.append(0)
            student.append(0)
            student.append(0)
            student.append("科目错误")
            gradings.append(student)
        else:
            student.append(''.join('%s' % id for id in reply["准考证号栏:"]))
            student.append(''.join('%s' % id for id in reply["姓名栏:"]))
            student.append(0)
            student.append(0)
            student.append(0)
            student.append(0)
            student.append("缺考")
            gradings.append(student)
    return gradings


# 单选题判分
def getSingleChoiceGrad(Answer, reply):
    grade = 0
    for i, j in zip(Answer, reply):
        if i == j:
            grade += 0.5
    return grade


# 多选题判分
def getMultipleChoiceGrad(Answer, reply):
    grade = 0
    for i, j in zip(Answer, reply):
        if i == j:
            grade += 1
    return grade


# 打印成绩
def writeGradExcel(gradings):
    titles = ["学号", "姓名代码", "单选成绩", "多选成绩", "主观题成绩", "总成绩", "备注"]
    data = {}
    for title in titles:
        data[title] = []
    for grading in gradings:
        data[titles[0]].append(grading[0])
        data[titles[1]].append(grading[1])
        data[titles[2]].append(grading[2])
        data[titles[3]].append(grading[3])
        data[titles[4]].append(grading[4])
        data[titles[5]].append(grading[5])
        data[titles[6]].append(grading[6])
    a = pandas.DataFrame(data)
    a.to_excel('grad.xlsx', sheet_name='成绩单', index=False)
