from test.windowUtilTest import *
from test.imageTest import *

answer = getAnswer(r'D:\BaiduSyncdisk\code\openCV-Automatic-Grading-System\img\imgAnswer.jpg')
replys1 = getAnswer(r'D:\BaiduSyncdisk\code\openCV-Automatic-Grading-System\img\reply\img3.jpg')
replys2 = getAnswer(r'D:\BaiduSyncdisk\code\openCV-Automatic-Grading-System\img\reply\img2.jpg')
replys = []
replys.append(replys1)
replys.append(replys2)

getGradingLists(answer, replys)
