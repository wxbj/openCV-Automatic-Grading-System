from utils.optionDetectionUtil import *


# 从答题卡中提取答案
def getAnswer(imageSegmentation, filePath, paperOption):
    ####################################
    path = filePath  # 图片地址
    widthImg = 720  # 图片宽度
    heightImg = 960  # 图片长度
    singleChoiceNumber = paperOption["单选题终止"] - paperOption["单选题开始"] + 1  # 单选题数目
    multChoiceNumber = paperOption["多选题终止"] - paperOption["多选题开始"] + 1  # 多选题数目
    nameColumnNumber = 12  # 姓名栏选项数
    admissionColumnNumber = 9  # 准考证号栏选项数
    missExamColumnNumber = 1  # 缺考栏选项数
    subjectiveQuestionColumnNumber = 3  # 主观题栏选项数
    subjectColumnNumber = 2  # 考试科目栏选项数
    questionOptionNumber = 4  # 选择问题选项数
    otherOptionNumber = 10  # 其他选项数
    choiceBoxes = [[]]  # 全部问题，为了选项从1开始，所以有初始空列表
    numberToLetter = {-1: "错填", 0: "A", 1: "B", 2: "C", 3: "D"}  # 数字对应的字母
    answerSheet = {}  # 答题卡
    ####################################

    # 预处理
    image = cv_imread(path)
    image = cv.resize(image, (widthImg, heightImg))
    imgGray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    imgBlur = cv.GaussianBlur(imgGray, (imageSegmentation[0], imageSegmentation[0]), 1)
    imgCanny = cv.Canny(imgBlur, imageSegmentation[1], imageSegmentation[2])

    kernel = np.ones((imageSegmentation[3], imageSegmentation[3]), np.uint8)
    dilate = cv.dilate(imgCanny, kernel, iterations=imageSegmentation[4])
    erosion = cv.erode(dilate, kernel, iterations=imageSegmentation[5])

    # 所有矩形填涂区域轮廓
    contours = cv.findContours(erosion, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)[0]
    contoursRect = getContoursRect(contours)

    # 提取矩形轮廓的四角
    contoursNeedHandle = {}

    contourName = getCornerPoints(contoursRect[1])
    contourAdmission = getCornerPoints(contoursRect[2])
    contourMissExamAndSubject = getCornerPoints(contoursRect[3])

    contoursNeedHandle["contourName"] = contourName
    contoursNeedHandle["contourAdmission"] = contourAdmission
    contoursNeedHandle["contourMissExamAndSubject"] = contourMissExamAndSubject

    # 单独处理选项区域
    maskChoice = np.zeros(imgGray.shape, np.uint8)
    cv.drawContours(maskChoice, [contoursRect[0]], -1, (255, 255, 255), -1)
    imgGrayChoice = cv.bitwise_and(imgGray, imgGray, mask=maskChoice)

    imgCannyChoice = cv.Canny(imgGrayChoice, imageSegmentation[6], imageSegmentation[7])

    kernel = np.ones((imageSegmentation[8], imageSegmentation[8]), np.uint8)
    dilate = cv.dilate(imgCannyChoice, kernel, iterations=imageSegmentation[9])
    erosion = cv.erode(dilate, kernel, iterations=imageSegmentation[10])

    contoursChoice = cv.findContours(erosion, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)[0]
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
        imgThreshs[key] = cv.threshold(imgWarpColored, 150, 255, cv.THRESH_BINARY_INV)[1]

    # 划分姓名栏（12，10）
    darryNameBoxes = splitNameBoxes(imgThreshs["contourName"][120:, 30:])
    # 划分准考证号栏（9，10）
    darryAdmissionBoxes = splitAdmissionBoxes(imgThreshs["contourAdmission"][120:, :])
    # 划分缺考栏（1，1）
    darryMissExamBoxes = imgThreshs["contourMissExamAndSubject"][35:43, 305:350]
    # 划分主观题、科目栏（5，10）
    darrySubjectiveQuestionsAndSubjectBoxes = splitSubjectiveQuestionsAndSubject(
        imgThreshs["contourMissExamAndSubject"][200:, :])
    darrySubjectiveQuestionsBoxes = darrySubjectiveQuestionsAndSubjectBoxes[:3]
    darrySubjectBoxes = darrySubjectiveQuestionsAndSubjectBoxes[3:]
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
    # 全部选择题整理
    for i in darryFirstColumnChoiceBoxes:
        choiceBoxes.append(i)
    for i in darrySecondColumnChoiceBoxes:
        choiceBoxes.append(i)
    for i in darryThirdColumnChoiceBoxes:
        choiceBoxes.append(i)
    for i in darryFourColumnChoiceBoxes:
        choiceBoxes.append(i)

    # 姓名栏填涂检测
    choiceName = detectNameAdmissionSubject(darryNameBoxes, nameColumnNumber, otherOptionNumber)
    answerSheet["姓名栏:"] = choiceName
    # 准考证号栏填涂检测
    choiceAdmission = detectNameAdmissionSubject(darryAdmissionBoxes, admissionColumnNumber, otherOptionNumber)
    answerSheet["准考证号栏:"] = choiceAdmission
    # 缺考栏填涂检测
    choiceMissExam = detectMissExam(darryMissExamBoxes, missExamColumnNumber)
    answerSheet["缺考栏:"] = choiceMissExam
    # 主观题栏填涂检测
    choiceSubjectiveQuestions = detectNameAdmissionSubject(darrySubjectiveQuestionsBoxes,
                                                           subjectiveQuestionColumnNumber,
                                                           otherOptionNumber)
    answerSheet["主观题栏:"] = choiceSubjectiveQuestions
    # 考试科目栏填涂检测
    choiceSubject = detectNameAdmissionSubject(darrySubjectBoxes, subjectColumnNumber, otherOptionNumber)
    answerSheet["考试科目栏:"] = choiceSubject
    # 单选填涂检测
    singleChoiceBoxes = choiceBoxes[paperOption["单选题开始"]:paperOption["单选题终止"] + 1]
    answerSheet["单选题:"] = detectSingleChoice(singleChoiceBoxes, singleChoiceNumber,
                                             questionOptionNumber, numberToLetter)
    # 多选填涂检测
    multChoiceBoxes = choiceBoxes[paperOption["多选题开始"]:paperOption["多选题终止"] + 1]
    answerSheet["多选题:"] = detectMultipleChoice(multChoiceBoxes, multChoiceNumber,
                                               questionOptionNumber, numberToLetter)
    return answerSheet


# 弹窗，让用户提供参数
def getInputAnswerParameter(filePath):
    ####################################
    path = filePath  # 图片地址
    widthImg = 720  # 图片宽度
    heightImg = 960  # 图片长度
    ####################################

    # 初始化
    initializeInterface()
    image = cv_imread(path)
    image = cv.resize(image, (widthImg, heightImg))
    imgGray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    # 接受用户的调整数值，最终的数据放在parameter和contours中
    while True:
        parameter = getValTrackbars()
        imgBlur = cv.GaussianBlur(imgGray, (parameter[0], parameter[0]), 2)
        imgCanny = cv.Canny(imgBlur, parameter[1], parameter[2])

        kernel = np.ones((parameter[3], parameter[3]), np.uint8)
        dilate = cv.dilate(imgCanny, kernel, iterations=parameter[4])
        erosion = cv.erode(dilate, kernel, iterations=parameter[5])

        # 所有矩形填涂区域轮廓
        contours = cv.findContours(erosion, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)[0]
        contoursPrint = []
        for i in contours:
            if cv.contourArea(i) >= 10000:
                contoursPrint.append(i)

        contoursRect = getContoursRect(contours)

        img1 = image.copy()
        cv.drawContours(img1, contoursPrint, -1, (0, 255, 0), 1)
        # 单独处理选项区域
        maskChoice = np.zeros(imgGray.shape, np.uint8)
        cv.drawContours(maskChoice, [contoursRect[0]], -1, (255, 255, 255), -1)
        imgGrayChoice = cv.bitwise_and(imgGray, imgGray, mask=maskChoice)

        imgCannyChoice = cv.Canny(imgGrayChoice, parameter[6], parameter[7])

        kernel = np.ones((parameter[8], parameter[8]), np.uint8)
        dilate = cv.dilate(imgCannyChoice, kernel, iterations=parameter[9])
        erosion = cv.erode(dilate, kernel, iterations=parameter[10])

        contoursChoice = cv.findContours(erosion, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)[0]
        contoursChoiceRect = []
        for i in contoursChoice:
            if cv.contourArea(i) >= 10000:
                contoursChoiceRect.append(i)

        img = img1.copy()
        cv.drawContours(img, contoursChoiceRect, -1, (0, 255, 0), 1)
        cv.imshow("image", img)

        k = cv.waitKey(1) & 0xFF
        if k == 27:
            cv.destroyAllWindows()
            break
    return parameter


if __name__ == "__main__":
    paperOptions = {'单选题开始': 1, '单选题终止': 60, '单选题分值': 1, '多选题开始': 61, '多选题终止': 105, '多选题分值': 2}
    parament = [5, 10, 50, 2, 1, 0, 50, 200, 2, 2, 1]
    answer = getAnswer(parament, r"D:/BaiduSyncdisk/code/openCV-Automatic-Grading-System/img/第二次月考/answer.jpg",
                       paperOptions)
    print(answer)
    # print(getInputAnswerParameter(r"D:/BaiduSyncdisk/code/openCV-Automatic-Grading-System/img/第二次月考/img1.jpg"))
