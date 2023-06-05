import os
import sys
import cv2 as cv
import pandas
import shutil
from main.optionDetection import getAnswer
from main.imageTransformation import getPreprocessedImage
from PIL import Image, ImageOps
import numpy as np


# 解决图像自动翻转的问题
def solveAutomaticRotationOfImage(imageFolderPath):
    imgs = []
    imgName = []
    for i in range(len(os.listdir(imageFolderPath))):
        img = Image.open(imageFolderPath + "\\" + os.listdir(imageFolderPath)[i]).convert('RGB')
        imgs.append(np.array(ImageOps.exif_transpose(img))[:, :, ::-1])
        imgName.append(imageFolderPath + "\\" + os.listdir(imageFolderPath)[i])
    shutil.rmtree(imageFolderPath)
    os.mkdir(imageFolderPath)
    for img, imgName in zip(imgs, imgName):
        cv.imwrite(imgName, img)


# 返回评分列表
def getGradingLists(answer, replyUrls, paperOption):
    subject = answer['考试科目栏:']
    singleChoiceAnswer = answer['单选题:']
    multChoiceAnswer = answer['多选题:']

    replys = []
    for replyUrl in replyUrls:
        try:
            replys.append(getAnswer(replyUrl, paperOption))
            continue
        except Exception:
            continue

    gradings = []
    for reply in replys:
        student = []
        if (reply['考试科目栏:'] == subject) and (reply['缺考栏:'] == ['否']):
            student.append(''.join('%s' % id for id in reply["准考证号栏:"]))
            student.append(''.join('%s' % id for id in reply["姓名栏:"]))
            singleChoiceGrad = getSingleChoiceGrad(singleChoiceAnswer, reply["单选题:"], paperOption['单选题分值'])
            student.append(singleChoiceGrad)
            multipleChoiceGrad = getMultipleChoiceGrad(multChoiceAnswer, reply["多选题:"], paperOption['多选题分值'])
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
def getSingleChoiceGrad(Answer, reply, score):
    grade = 0
    for i, j in zip(Answer, reply):
        if i == j:
            grade += score
    return grade


# 多选题判分
def getMultipleChoiceGrad(Answer, reply, score):
    grade = 0
    for i, j in zip(Answer, reply):
        if i == j:
            grade += score
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


# 预处理试卷
def preprocessingPapers(fileUrls, perspectiveTransformation):
    images = []
    for i in fileUrls:
        images.append(getPreprocessedImage(i, perspectiveTransformation))
    return images


# 保存预处理后的试卷
def saveResultFolder(preFolderUrl, folderName, images):
    folder = sys.path[0][:-5] + "\img\\" + folderName
    imgNames = []
    for i in os.listdir(preFolderUrl):
        imgNames.append(i[0:-4])
    os.mkdir(folder)
    for ingName, image in zip(imgNames, images):
        cv.imencode('.jpg', image)[1].tofile(folder + f"\\{ingName}.jpg")


if __name__ == "__main__":
    # urls = ['D:/BaiduSyncdisk/code/openCV-Automatic-Grading-System/img/camera/img1.jpg',
    #         'D:/BaiduSyncdisk/code/openCV-Automatic-Grading-System/img/camera/img10.jpg',
    #         'D:/BaiduSyncdisk/code/openCV-Automatic-Grading-System/img/camera/img11.jpg',
    #         'D:/BaiduSyncdisk/code/openCV-Automatic-Grading-System/img/camera/img12.jpg',
    #         'D:/BaiduSyncdisk/code/openCV-Automatic-Grading-System/img/camera/answer.jpg',
    #         'D:/BaiduSyncdisk/code/openCV-Automatic-Grading-System/img/camera/answer.jpg',
    #         'D:/BaiduSyncdisk/code/openCV-Automatic-Grading-System/img/camera/img15.jpg',
    #         'D:/BaiduSyncdisk/code/openCV-Automatic-Grading-System/img/camera/img6.jpg',
    #         'D:/BaiduSyncdisk/code/openCV-Automatic-Grading-System/img/camera/img2.jpg',
    #         'D:/BaiduSyncdisk/code/openCV-Automatic-Grading-System/img/camera/img3.jpg',
    #         'D:/BaiduSyncdisk/code/openCV-Automatic-Grading-System/img/camera/img4.jpg',
    #         'D:/BaiduSyncdisk/code/openCV-Automatic-Grading-System/img/camera/img5.jpg',
    #         'D:/BaiduSyncdisk/code/openCV-Automatic-Grading-System/img/camera/img6.jpg',
    #         'D:/BaiduSyncdisk/code/openCV-Automatic-Grading-System/img/camera/img7.jpg',
    #         'D:/BaiduSyncdisk/code/openCV-Automatic-Grading-System/img/camera/img8.jpg',
    #         'D:/BaiduSyncdisk/code/openCV-Automatic-Grading-System/img/camera/img9.jpg']
    # # preprocessingPapers(urls, [106, 74, 2, 1])
    # saveResultFolder("x", '')
    solveAutomaticRotationOfImage(r"D:\BaiduSyncdisk\code\openCV-Automatic-Grading-System\img\testNormal")
