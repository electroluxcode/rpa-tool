
import time
import json
import cv2
import os
import numpy as np
import xml.etree.ElementTree as ET
import re
# 定义鼠标事件
# pyautogui库其他用法 https://blog.csdn.net/qingfengxd1/article/details/108270159


def elementFind(attr,attrValue):
 
    while True:
        # 1.读手机界面的dom tree
        os.system("adb shell uiautomator dump --compressed /sdcard/ui.xml")
        os.system("adb pull sdcard/ui.xml")
        # 2.查找元素并且点击
        tree = ET.parse('ui.xml')
        root = tree.getroot()
        Nodes = root.findall(".//*[@%s='%s']" %(str(attr),str(attrValue)))
        position = []
        print("没找到元素,0.2秒后面接着试一下")
        time.sleep(0.2)
        if len(Nodes):
            position = Nodes[0].attrib["bounds"]
            position = re.findall(r"\d+",position)
            x = (float(position[0])+float(position[2])) / 2
            y = (float(position[1])+float(position[3])) / 2
            cmd = "adb shell input tap %s %s" % ( x, y)
            os.system(cmd)
            break
        
def imgClick(img, retry): 
    while ( retry!=0 & True):
        # 图片保存在里面
        os.system("adb shell screencap -p /sdcard/screen.png ")
        os.system("adb pull /sdcard/screen.png ")

        # 1.加载大图
        bigImg = cv2.imread('screen.png')
        # smallImg = cv2.imread('pos.jpg',0) 1259 969
        smallImg = cv2.imread(img, 0)
        # 2.存储大小图的宽高 | 大图转化灰度图像
        # bigWidth, bigHeight = bigImg.shape[0:2]
        smallWidth, smallHeight = smallImg.shape[0:2]
        img_gray = cv2.cvtColor(bigImg, cv2.COLOR_BGR2GRAY)

        # 2.5查看灰度图像
        # cv2.namedWindow("img_rgb",0)
        # cv2.resizeWindow('img_rgb',300,600)
        # cv2.resize(bigImg,None,fx=0.5,fy=0.5)
        # cv2.imshow('img_rgb', img_gray)
        # cv2.waitKey(0)

        # 3.开始查找
        res = cv2.matchTemplate(img_gray, smallImg, cv2.TM_CCOEFF_NORMED)
        threshold = 0.7
        loc = np.where(res >= threshold)
        x = loc[1]
        y = loc[0]

        # 4.输出坐标

        if len(x) and len(y):
            print("最终坐标：", x[0]+smallWidth/2, y[0]+smallHeight/2)
            cmd = "adb shell input tap %s %s" % (
                str(x[0]+smallWidth/2), str(y[0]+smallHeight/2))

            os.system(cmd)
            cv2.rectangle(
                bigImg, (x[0], y[0]), (x[0] + smallWidth, y[0] + smallHeight), (0, 255, 255), 5)
            cv2.imwrite("output.png", bigImg)
            retry = retry - 1
            

        else:
            time.sleep(0.2)
            print('找不到图像呢,等0.2秒后重试')

def mainWork(allData):
    i = 0
    while i < len(allData):
        cmdType = allData[i]["cmdType"]
        cmdParam = allData[i]["cmdParam"]
        cmdCound = allData[i]["cmdCound"]

        # 1.点击鼠标
        if cmdType == "ClickPosition":
            cmd = "adb shell input tap %s %s" % ( str(cmdParam["x"]), str(cmdParam["y"]))
            os.system(cmd)
            print("点击", cmdParam, cmdCound, "次")

        # 2.滑动
        if cmdType == "滑动":
            cmd = "adb shell input swipe %s %s %s %s" % (str(cmdParam["originX"]), str(
                cmdParam["originY"]), str(cmdParam["targetX"]), str(cmdParam["targetY"]))
            os.system(cmd)
            print("滑动", cmdParam)

        # 3.Wait
        if cmdType == "Wait":
            time.sleep(cmdParam)
            print("Wait", cmdParam, "秒")

        # 4.ClickImage
        if cmdType == "ClickImage":
            imgClick(cmdParam, cmdCound)
            print("点击了", cmdParam,cmdCound,"次")

        if cmdType == "返回":
            os.system("adb shell input keyevent BACK")
            print("返回")
            
        if cmdType == "点击元素":
            elementFind(cmdParam["key"], cmdParam["value"])
            print("点击了", cmdParam)
        i += 1


# from phoneRPAFn import mainWork

if __name__ == '__main__':
    # print(mainWork)
    print('Electrolux_Phone_RPA欢迎使用')
    # 数据检查
    # checkCmd = dataCheck(allData)
    f = open('phoneData.json', encoding='UTF-8')
    allData = json.load(f)
    key = input('选择功能: 1.做一次 2.循环到死 \n')
    if key == '1':
        # 循环拿出每一行指令
        mainWork(allData["data"])
    elif key == '2':
        while True:
            mainWork(allData["data"])
            time.sleep(0.1)
            print("Wait0.1秒")
