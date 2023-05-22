import sys
from utils.imageTransformationUtil import *


def getBasicParameter(filePath):
    ###################################
    pathImg = filePath
    widthImg = 720  # 图片宽度
    heightImg = 960  # 图片长度
    ####################################
    initializeTrackBar()
    img = cv.imread(pathImg)
    img = cv.resize(img, (widthImg, heightImg))
    imgGray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    imgBlur = cv.GaussianBlur(imgGray, (5, 5), 1)
    while True:
        thres = valTrackbars()
        imgCanny = cv.Canny(imgBlur, thres[0], thres[1])

        kernel = np.ones((5, 5))
        imgDial = cv.dilate(imgCanny, kernel, iterations=thres[2])
        imgCanny = cv.erode(imgDial, kernel, iterations=thres[3])

        contours = cv.findContours(imgCanny, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[0]

        image = img.copy()
        cv.drawContours(image, contours, -1, (0, 255, 0), 1)

        cv.imshow("img", image)

        k = cv.waitKey(1) & 0xFF
        if k == 27:
            break
    cv.destroyWindow("TrackBar")
    biggest = biggestContours(contours)

    biggest = reorder(biggest)

    pt1 = np.float32(biggest)
    pt2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
    matrix = cv.getPerspectiveTransform(pt1, pt2)
    imgWarpColoreds = cv.warpPerspective(img, matrix, (widthImg, heightImg))

    cv.imshow("img", imgWarpColoreds)
    cv.waitKey(0)

    cv.destroyAllWindows()
    cv.imwrite('temp.png', imgWarpColoreds)

    return sys.path[0] + r"\temp.png"
