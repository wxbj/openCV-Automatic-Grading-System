import sys
from utils.imageTransformationUtil import *


# 返回列表[透视变换后的图片地址, 透视变换的参数]
def getParameter(filePath):
    ###################################
    pathImg = filePath
    widthImg = 720  # 图片宽度
    heightImg = 960  # 图片长度
    ####################################

    # 初始化
    initializeInterface()
    img = cv.imread(pathImg)
    img = cv.resize(img, (widthImg, heightImg))
    imgGray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    imgBlur = cv.GaussianBlur(imgGray, (5, 5), 1)

    # 接受用户的调整数值，最终的数据放在thres和contours中
    while True:
        parameter = getValTrackbars()
        imgCanny = cv.Canny(imgBlur, parameter[0], parameter[1])

        kernel = np.ones((5, 5))
        imgDial = cv.dilate(imgCanny, kernel, iterations=parameter[2])
        imgCanny = cv.erode(imgDial, kernel, iterations=parameter[3])

        contours = cv.findContours(imgCanny, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[0]

        image = img.copy()
        cv.drawContours(image, contours, -1, (0, 255, 0), 5)
        cv.imshow("settings", image)

        k = cv.waitKey(1) & 0xFF
        if k == 27:
            break

    # 透视变换
    cv.destroyWindow("settings")

    biggest = getBiggestContours(contours)
    biggest = reorderFourPoints(biggest)

    pt1 = np.float32(biggest)
    pt2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
    matrix = cv.getPerspectiveTransform(pt1, pt2)
    imgWarpColoreds = cv.warpPerspective(img, matrix, (widthImg, heightImg))
    cv.destroyAllWindows()

    cv.imwrite(sys.path[0] + r"\temp.png", imgWarpColoreds)

    return [sys.path[0] + r"\temp.png", parameter]


# 批量化预处理试卷
def getPreprocessedImage(filePath, perspectiveTransformation):
    ###################################
    widthImg = 720  # 图片宽度
    heightImg = 960  # 图片长度
    ####################################

    img = cv.imread(filePath)
    img = cv.resize(img, (widthImg, heightImg))
    imgGray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    imgBlur = cv.GaussianBlur(imgGray, (5, 5), 1)

    imgCanny = cv.Canny(imgBlur, perspectiveTransformation[0], perspectiveTransformation[1])

    kernel = np.ones((5, 5))
    imgDial = cv.dilate(imgCanny, kernel, iterations=perspectiveTransformation[2])
    imgCanny = cv.erode(imgDial, kernel, iterations=perspectiveTransformation[3])

    contours = cv.findContours(imgCanny, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[0]

    # 透视变换
    biggest = getBiggestContours(contours)
    biggest = reorderFourPoints(biggest)

    pt1 = np.float32(biggest)
    pt2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
    matrix = cv.getPerspectiveTransform(pt1, pt2)
    imgWarpColoreds = cv.warpPerspective(img, matrix, (widthImg, heightImg))

    return imgWarpColoreds


if __name__ == "__main__":
    getParameter(r'D:\BaiduSyncdisk\code\openCV-Automatic-Grading-System\img\normal\img1.jpg')
    getPreprocessedImage(r'D:\BaiduSyncdisk\code\openCV-Automatic-Grading-System\img\normal\img1.jpg')
