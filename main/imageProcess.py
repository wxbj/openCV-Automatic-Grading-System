from utils.imageUtil import *


def getAnswer(fileName):
    ####################################
    path = fileName  # 图片地址
    widthImg = 720  # 图片宽度
    heightImg = 960  # 图片长度
    questionNumber = 30  # 前三栏问题数
    lastQuestionNumber = 15  # 最后一栏选题目数
    nameNumber = 12  # 姓名栏选项数
    admissionNumber = 9  # 准考证号栏选项数
    missExamNumber = 5  # 缺考栏选项数
    questionOptionNumber = 4  # 选择问题选项数
    otherOptionNumber = 10  # 其他选项数
    numberToLetter = {0: "A", 1: "B", 2: "C", 3: "D"}  # 数字对应的字母
    answer = {}  # 正确答案
    ####################################
    # 预处理
    image = cv.imread(path)
    image = cv.resize(image, (widthImg, heightImg))
    imgGray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    imgBlur = cv.GaussianBlur(imgGray, (5, 5), 1)
    imgCanny = cv.Canny(imgBlur, 10, 50)

    # 所有矩形填涂区域轮廓
    contours = cv.findContours(imgCanny, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)[0]
    contoursRect = getContoursRect(contours)

    # 提取矩形轮廓的四角
    contoursNeedHandle = {}

    contourName = getCornerPoints(contoursRect[1])
    contourAdmission = getCornerPoints(contoursRect[2])
    contourMissExam = getCornerPoints(contoursRect[3])

    contoursNeedHandle["contourName"] = contourName
    contoursNeedHandle["contourAdmission"] = contourAdmission
    contoursNeedHandle["contourMissExam"] = contourMissExam

    # 单独处理选项区域
    mask = np.zeros(imgCanny.shape, np.uint8)
    cv.drawContours(mask, [contoursRect[0]], -1, (255, 255, 255), -1)
    imgCannyChoice = cv.bitwise_and(imgCanny, imgCanny, mask=mask)
    kernel = np.ones((3, 3), np.uint8)
    imgMorphChoice = cv.morphologyEx(imgCannyChoice, cv.MORPH_CLOSE, kernel)
    contoursChoice = cv.findContours(imgMorphChoice, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)[0]
    contoursChoiceRect = getContourChoice(contoursChoice)

    contourChoicePoints = []
    for i in contoursChoiceRect:
        contourChoicePoint = getCornerPoints(i)
        contourChoicePoints.append(contourChoicePoint)

    contourChoicePointsReorder = reorderContourChoice(contourChoicePoints)

    contoursNeedHandle["firstColumnChoiceContour"] = contourChoicePointsReorder[0]
    contoursNeedHandle["secondColumnChoiceContour"] = contourChoicePointsReorder[1]
    contoursNeedHandle["thirdColumnChoiceContour"] = contourChoicePointsReorder[2]
    contoursNeedHandle["fourColumnChoiceContour"] = contourChoicePointsReorder[3]

    # 透视变换
    imgWarpColoreds = {}
    contoursNeedHandle = reorderContoursPoints(contoursNeedHandle)
    for key, needHandelContour in contoursNeedHandle.items():
        pt1 = np.float32(needHandelContour)
        pt2 = np.float32([[0, 0], [widthImg // 2, 0], [0, heightImg // 2], [widthImg // 2, heightImg // 2]])
        matrix = cv.getPerspectiveTransform(pt1, pt2)
        imgWarpColoreds[key] = cv.warpPerspective(imgGray, matrix, (widthImg // 2, heightImg // 2))

    # 简单阈值
    imgThreshs = {}
    for key, imgWarpColored in imgWarpColoreds.items():
        imgThreshs[key] = cv.threshold(imgWarpColored, 110, 255, cv.THRESH_BINARY_INV)[1]
    # 划分姓名栏（12，10）
    darryNameBoxes = splitNameBoxes(imgThreshs["contourName"][120:, 30:])
    # 划分准考证号栏（9，10）
    darryAdmissionBoxes = splitAdmissionBoxes(imgThreshs["contourAdmission"][120:, :])
    # 划分缺考栏（5，10）
    darryMissExamBoxes = splitMissExamBoxes(imgThreshs["contourMissExam"][200:, :])
    # 划分选择第一栏（30，4）
    darryFirstColumnChoiceBoxes = splitTheFirstThreeColumnChoiceBoxes(
        imgThreshs["firstColumnChoiceContour"][:, 70:330])
    # 划分选择第二栏（30，4）
    darrySecondColumnChoiceBoxes = splitTheFirstThreeColumnChoiceBoxes(
        imgThreshs["secondColumnChoiceContour"][:, 70:330])
    # 划分选择第三栏（30，4）
    darryThirdColumnChoiceBoxes = splitTheFirstThreeColumnChoiceBoxes(
        imgThreshs["thirdColumnChoiceContour"][:, 70:330])
    # 划分选项第四栏（15，4）
    darryFourColumnChoiceBoxes = splitTheFourthColumnChoiceBoxes(
        imgThreshs["fourColumnChoiceContour"][:, 100:])

    # 姓名栏填涂检测
    choiceName = detectNameAdmissionMiss(darryNameBoxes, nameNumber, otherOptionNumber)
    answer["姓名栏:"] = choiceName
    # 准考证号栏填涂检测
    choiceAdmission = detectNameAdmissionMiss(darryAdmissionBoxes, admissionNumber, otherOptionNumber)
    answer["准考证号栏:"] = choiceAdmission
    # 缺考栏填涂检测
    choiceMissExam = detectNameAdmissionMiss(darryMissExamBoxes, missExamNumber, otherOptionNumber)
    answer["缺考栏:"] = choiceMissExam
    # 选择第一栏填涂检测
    choiceFirstColumnLetter = detectSingleChoice(darryFirstColumnChoiceBoxes, questionNumber,
                                                 questionOptionNumber, numberToLetter)
    answer["选择第一栏:"] = choiceFirstColumnLetter
    # 选择第二栏填涂检测
    choiceSecondColumnLetter = detectSingleChoice(darrySecondColumnChoiceBoxes, questionNumber,
                                                  questionOptionNumber, numberToLetter)
    answer["选择第二栏:"] = choiceSecondColumnLetter
    # 选择第三栏填涂检测
    choiceThirdColumnLetter = detectMultipleChoice(darryThirdColumnChoiceBoxes, questionNumber,
                                                   questionOptionNumber, numberToLetter)
    answer["选择第三栏:"] = choiceThirdColumnLetter
    # 选择第四栏填涂检测
    choiceFourColumnLetter = detectMultipleChoice(darryFourColumnChoiceBoxes, lastQuestionNumber,
                                                  questionOptionNumber, numberToLetter)
    answer["选择第四栏:"] = choiceFourColumnLetter

    return answer