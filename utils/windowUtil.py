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
    imgNames = []
    for i in range(len(os.listdir(imageFolderPath))):
        img = Image.open(imageFolderPath + "\\" + os.listdir(imageFolderPath)[i]).convert('RGB')
        imgs.append(np.array(ImageOps.exif_transpose(img))[:, :, ::-1])
        imgNames.append(imageFolderPath + "\\" + os.listdir(imageFolderPath)[i])
    shutil.rmtree(imageFolderPath)
    os.mkdir(imageFolderPath)
    for img, imgName in zip(imgs, imgNames):
        cv.imencode('.jpg', img)[1].tofile(imgName)


# 返回评分列表
def getGradingLists(answer, replyUrls, paperOption, imageSegmentation):
    subject = answer['考试科目栏:']
    singleChoiceAnswer = answer['单选题:']
    multChoiceAnswer = answer['多选题:']

    replys = []
    for replyUrl in replyUrls:
        try:
            replys.append(getAnswer(imageSegmentation, replyUrl, paperOption))
            continue
        except Exception:
            continue

    accuracy = {}
    for i in range(paperOption["单选题终止"] - paperOption["单选题开始"] + 1):
        accuracy[f"单选题第{i + 1}题"] = 0
    for i in range(paperOption["多选题终止"] - paperOption["多选题开始"] + 1):
        accuracy[f"多选题第{i + 1}题"] = 0
    accuracy["总学生数"] = 0

    gradings = []
    for reply in replys:
        student = []
        if (reply['考试科目栏:'] == subject) and (reply['缺考栏:'] == ['否']):
            accuracy["总学生数"] += 1
            student.append(''.join('%s' % id for id in reply["准考证号栏:"]))
            student.append(''.join('%s' % id for id in reply["姓名栏:"]))
            accuracy, singleChoiceGrad = getSingleChoiceGrad(accuracy, singleChoiceAnswer, reply["单选题:"],
                                                             paperOption['单选题分值'])
            student.append(singleChoiceGrad)
            accuracy, multipleChoiceGrad = getMultipleChoiceGrad(accuracy, multChoiceAnswer, reply["多选题:"],
                                                                 paperOption['多选题分值'])
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

    return accuracy, gradings


# 单选题判分
def getSingleChoiceGrad(accuracy, Answer, reply, score):
    grade = 0
    for i, j, k in zip(Answer, reply, range(len(Answer))):
        if i == j:
            accuracy[f"单选题第{k + 1}题"] += 1
            grade += score
    return accuracy, grade


# 多选题判分
def getMultipleChoiceGrad(accuracy, Answer, reply, score):
    grade = 0
    for i, j, k in zip(Answer, reply, range(len(Answer))):
        if i == j:
            accuracy[f"多选题第{k + 1}题"] += 1
            grade += score
    return accuracy, grade


# 打印成绩
def writeGradExcel(gradings, fileUrl):
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
    a.to_excel(fileUrl, sheet_name='成绩单', index=False)


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
    for imgName, image in zip(imgNames, images):
        cv.imencode('.jpg', image)[1].tofile(folder + f"\\{imgName}.jpg")


if __name__ == "__main__":
    answer = {'姓名栏:': [9], '准考证号栏:': [9, 9, 9, 9, 9, 9], '缺考栏:': ['否'], '主观题栏:': [9], '考试科目栏:': [0, 1],
              '单选题:': ['A', 'B', 'C', 'C', 'D', 'B', 'C', 'C', 'D', 'A', 'B', 'C', 'D', 'B', 'C', 'A', 'B', 'B', 'A',
                       'D', 'D', 'B', 'B', 'C', 'D', 'B', 'C', 'C', 'B', 'D', 'A', 'C', 'B', 'D', 'A', 'A', 'B', 'B',
                       'D', 'D', 'A', 'A', 'B', 'D', 'D', 'B', 'B', 'C', 'A', 'A', 'D', 'C', 'A', 'C', 'B', 'A', 'B',
                       'A', 'B', 'D'],
              '多选题:': ['AB', 'BC', 'BC', 'CD', 'ABC', 'BC', 'BD', 'BD', 'AC', 'AD', 'AC', 'BC', 'CD', 'BD', 'ABD', 'BC',
                       'BD', 'AC', 'BC', 'ACD', 'AC', 'BC', 'ACD', 'ABCD', 'BCD', 'BC', 'CD', 'AC', 'AB', 'BD', 'AB',
                       'BC', 'CD', 'AD', 'ABC', 'AB', 'BC', 'BD', 'AC', 'BC', 'AD', 'BD', 'BC', 'AC', 'BCD']}
    replyUrls = ['D:/BaiduSyncdisk/code/openCV-Automatic-Grading-System/img/第二次月考/img2.jpg',
                 'D:/BaiduSyncdisk/code/openCV-Automatic-Grading-System/img/第二次月考/img1.jpg']
    paperOption = {'单选题开始': 1, '单选题终止': 60, '单选题分值': 1, '多选题开始': 61, '多选题终止': 105, '多选题分值': 2}
    imageSegmentation = [5, 10, 50, 2, 1, 0, 50, 200, 2, 2, 1]
    getGradingLists(answer, replyUrls, paperOption, imageSegmentation)
