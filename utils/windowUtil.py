import pandas
from main.imageProcess import *


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
