import time
import json
import cv2
import os
import sys
import getopt
import numpy as np
import xml.etree.ElementTree as ET
import re
# 定义鼠标事件


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
        
def imgClick(img): 
    while ( True):
        # 图片保存在里面
        os.system("adb shell screencap -p /sdcard/screen.png ")
        os.system("adb pull /sdcard/screen.png")
        # 1.加载大图
        screenImg = cv2.imread('screen.png')
        
        # 2.加载目标图像
        # smallImg = cv2.imread('pos.jpg',0) 1259 969
        smallImg = cv2.imread(img, 0)
        # 2.存储大小图的宽高 | 大图转化灰度图像
        # bigWidth, bigHeight = screenImg.shape[0:2]
        smallWidth, smallHeight = smallImg.shape[0:2]
        img_gray = cv2.cvtColor(screenImg, cv2.COLOR_BGR2GRAY)

        # 2.5查看灰度图像
        cv2.namedWindow("img_rgb",0)
        cv2.resizeWindow('img_rgb',300,600)
        cv2.resize(screenImg,None,fx=0.5,fy=0.5)
        cv2.imshow('img_rgb', img_gray)
        cv2.waitKey(1)

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
                screenImg, (x[0], y[0]), (x[0] + smallWidth, y[0] + smallHeight), (0, 255, 255), 5)
            cv2.destroyAllWindows()
            break
        else:
            time.sleep(1)
            print('找不到图像呢,等0.2秒后重试')

def mainWork(allData):
    i = 0
    while i < len(allData):
        cmdType = allData[i]["cmdType"]
        cmdParam = allData[i]["cmdParam"]

        # 1.点击坐标
        if cmdType == "Click":
            cmd = "adb shell input tap %s %s" % ( str(cmdParam["x"]), str(cmdParam["y"]))
            os.system(cmd)
            print("Click", cmdParam)

        # 2.Swipe
        if cmdType == "Swipe":
            cmd = "adb shell input swipe %s %s %s %s" % (str(cmdParam["originX"]), str(
                cmdParam["originY"]), str(cmdParam["targetX"]), str(cmdParam["targetY"]))
            os.system(cmd)
            print("Swipe", cmdParam)

        # 3.Sleep
        if cmdType == "Sleep":
            time.sleep(cmdParam)
            print("Sleep", cmdParam, "秒")

        # 4.ImgClick
        if cmdType == "ImgClick":
            imgClick(cmdParam)
            print("ElementClick", cmdParam)


        if cmdType == "KeyEventInput":
            os.system("adb shell input keyevent " + str(cmdParam))
            print("KeyEventInput")

        if cmdType == "TextInput":
            os.system("adb shell input text " + str(cmdParam))
            print("TextInput")
            
        if cmdType == "ElementClick":
            elementFind(cmdParam["key"], cmdParam["value"])
            print("ElementClick", cmdParam)
        if cmdType == "ImgCature":
            os.system("adb shell screencap -p /sdcard/"+ str(cmdParam))
            os.system("adb pull /sdcard/"+ str(cmdParam))
            print("ImgCature", cmdParam)
        if cmdType == "AppStart":
            os.system("adb shell am start -n " + str(cmdParam))
            print("AppStart", cmdParam)
        i += 1


# from phoneRPAFn import mainWork

if __name__ == '__main__':
    
    if len(sys.argv) > 1:
        try:
            # 获取传入的第一个参数（索引为1，因为索引0是脚本自身名称）并尝试解析为字典
            
            print(sys.argv)
            param_dict = json.loads(sys.argv[1])
            print(param_dict)
            """

            """
            mainWork(param_dict)
        except json.JSONDecodeError as e:
            print('传入的参数无法解析为合法的JSON格式，错误信息：', e)
   
