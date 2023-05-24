import sys
from utils.imageTransformationUtil import *


def getPreprocessedImage(filePath, basicSettings):
    ###################################
    widthImg = 720  # 图片宽度
    heightImg = 960  # 图片长度
    ####################################

    img = cv.imread(filePath)
    img = cv.resize(img, (widthImg, heightImg))
    imgGray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    imgBlur = cv.GaussianBlur(imgGray, (5, 5), 1)

    imgCanny = cv.Canny(imgBlur, basicSettings[0], basicSettings[1])

    kernel = np.ones((5, 5))
    imgDial = cv.dilate(imgCanny, kernel, iterations=basicSettings[2])
    imgCanny = cv.erode(imgDial, kernel, iterations=basicSettings[3])

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
    getPreprocessedImage(r'D:\BaiduSyncdisk\code\openCV-Automatic-Grading-System\img\camera\img1.jpg')
