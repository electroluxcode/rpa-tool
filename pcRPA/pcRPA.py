import pyautogui
import time
import json
import sys
import pyperclip
import cv2
import numpy as np
import os
# 确保 PyScreeze 正确导入
try:
    import pyscreeze
except ImportError:
    print("正在尝试安装 pyscreeze...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyscreeze"])
    import pyscreeze

#定义鼠标事件
#pyautogui库其他用法 https://blog.csdn.net/qingfengxd1/article/details/108270159


def mouseClick(clickTimes, lOrR, img, reTry, region=None):
    print("正在寻找图片：")
    print(img)
    
    # 设置查找区域
    if region:
        # 获取屏幕尺寸
        screen_width, screen_height = pyautogui.size()
        
        # 预定义区域
        if region == 'left':
            search_region = (0, 0, screen_width//2, screen_height)
        elif region == 'right':
            search_region = (screen_width//2, 0, screen_width//2, screen_height)
        elif region == 'top':
            search_region = (0, 0, screen_width, screen_height//2)
        elif region == 'bottom':
            search_region = (0, screen_height//2, screen_width, screen_height//2)
        # 添加四个角落区域
        elif region == 'left_top' or region == 'top_left':
            search_region = (0, 0, screen_width//2, screen_height//2)
        elif region == 'right_top' or region == 'top_right':
            search_region = (screen_width//2, 0, screen_width//2, screen_height//2)
        elif region == 'left_bottom' or region == 'bottom_left':
            search_region = (0, screen_height//2, screen_width//2, screen_height//2)
        elif region == 'right_bottom' or region == 'bottom_right':
            search_region = (screen_width//2, screen_height//2, screen_width//2, screen_height//2)
        # 添加中间区域
        elif region == 'center':
            quarter_width = screen_width//4
            quarter_height = screen_height//4
            search_region = (quarter_width, quarter_height, quarter_width*2, quarter_height*2)
        # 自定义区域
        elif isinstance(region, list) and len(region) == 4:
            search_region = tuple(region)  # 自定义区域 [x, y, width, height]
        else:
            search_region = None
            print(f"无效的区域参数: {region}，将在全屏查找")
    else:
        search_region = None
    
    if reTry == 1:
        while True:
            try:
                location=pyautogui.locateCenterOnScreen(img, confidence=0.7, region=search_region)
                if location is not None:
                    pyautogui.click(location.x,location.y,clicks=clickTimes,interval=0.2,duration=0.2,button=lOrR)
                    print(f"找到匹配图片，点击位置: ({location.x}, {location.y})")
                    return True
                print("未找到匹配图片,0.5秒后重试")
                time.sleep(0.5)
            except:
                print("未找到匹配图片,0.5秒后重试")
                time.sleep(0.5)
                pass
    elif reTry > 1:
        i = 1
        found = False
        while i < reTry + 1:
            try:
                location=pyautogui.locateCenterOnScreen(img, confidence=0.7, region=search_region)
                if location is not None:
                    pyautogui.click(location.x,location.y,clicks=clickTimes,interval=0.2,duration=0.2,button=lOrR)
                    i += 1
                    print("恭喜找到图片")
                    found = True
                time.sleep(0.1)
            except Exception as e:
                print(f"查找图片失败: {str(e)}")
                i += 1
                pass
        return found
    elif reTry == 0:
        try:
            location=pyautogui.locateCenterOnScreen(img, confidencse=0.7, region=search_region)
            if location is not None:
                print("遇到指定图片停止30分钟")
                time.sleep(1*60*30)
                return True
            return False
        except:
            return False
    
    # 如果执行到这里，说明没有找到图片
    return False

#主任务
def mainWork(allData):
    i = 0
    while i < len(allData):
        cmdType = allData[i]["cmdType"]
        cmdParam = allData[i]["cmdParam"]
        if cmdType == "ShutDown":
            timeout = cmdParam.get("timeout", 10)
            print("电脑将在" + str(timeout) + "秒后关机")
            os.system("shutdown -s -t " + str(timeout))
            time.sleep(timeout+3)
            break
        if cmdType == "Click":   
            try:
                x = int(cmdParam.get("x"))
                y = int(cmdParam.get("y"))
                pyautogui.click( 
                    x=x, 
                    y=y, 
                    clicks=cmdParam.get("clicks", 1), 
                    interval=cmdParam.get("interval", 0), 
                    button=cmdParam.get("button", "left")
                )
                print("点击", cmdParam, "次")
            except ValueError:
                print(f"错误: 无效的坐标值 x={cmdParam.get('x')}, y={cmdParam.get('y')}")
            except Exception as e:
                print(f"点击操作出错: {str(e)}")

        if cmdType == "MoveTo":   
            pyautogui.moveTo(
                x=cmdParam.get("x"), 
                y=cmdParam.get("y"), 
                duration=cmdParam.get("duration", 0.25)
            )
            print("MouseMove到",cmdParam)

        # 3.DragTo
        if cmdType == "DragTo":  
            pyautogui.dragTo(
                x=cmdParam.get("x"), 
                y=cmdParam.get("y"), 
                duration=cmdParam.get("duration", 0.25), 
                button=cmdParam.get("button", "left")
            )
            print("MouseDrag到",cmdParam)

        # 4.ImgClick
        if cmdType == "ImgClick":   
            # 执行图片查找和点击
            found = mouseClick(
                1,
                cmdParam.get("button","left"),
                cmdParam.get("imgPath"),
                cmdParam.get("reTry", 1),
                cmdParam.get("region")
            )
            print("点击",cmdParam,"次")
            
            # 如果找到图片并且有后续操作
            if found and "thenActions" in cmdParam:
                print("找到图片，执行后续操作")
                # 递归执行后续操作（阻塞式）
                mainWork(cmdParam["thenActions"])
                print("后续操作执行完毕，继续主流程")
            elif not found and "elseActions" in cmdParam:
                print("未找到图片，执行替代操作")
                # 如果没找到图片，执行替代操作
                mainWork(cmdParam["elseActions"])
                print("替代操作执行完毕，继续主流程")

        
        # 6.Write
        if cmdType == "Write":
            pyautogui.write(
                message=cmdParam.get("message"), 
                interval=cmdParam.get("interval", 0.25)
            )
            print("Write:",cmdParam)                                        
        
        # 7.Sleep
        if cmdType == "Sleep":
            time.sleep(cmdParam)
            print("Sleep",cmdParam,"秒")
        
        # 8.滚轮
        if cmdType == "Scroll":
            pyautogui.scroll(
                cmdParam
            )
            print("Scroll")  
        
        # 9.
        if cmdType == "KeyDown":
            if isinstance(cmdParam, dict):
                key = cmdParam.get("key")
                duration = cmdParam.get("duration", 0)
                pyautogui.keyDown(key)
                print(f"KeyDown {key} 持续 {duration} 秒")
                if duration > 0:
                    time.sleep(duration)
                    pyautogui.keyUp(key)
                    print(f"自动释放按键 {key}")
            else:
                pyautogui.keyDown(cmdParam)
                print(f"KeyDown {cmdParam}")
        
        # 10
        if cmdType == "KeyUp":
            if isinstance(cmdParam, dict):
                key = cmdParam.get("key")
                pyautogui.keyUp(key)
                print(f"KeyUp {key}")
            else:
                pyautogui.keyUp(cmdParam)
                print(f"KeyUp {cmdParam}")

        if cmdType == "Press":
            print("press")
            pyautogui.press(
                keys=cmdParam.get("keys"),
                presses=cmdParam.get("presses", 1),
                interval=cmdParam.get("interval", 0),
            )
        
        if cmdType == "ChineseWrite":
            pyperclip.copy(cmdParam)
            time.sleep(0.2)
            pyautogui.hotkey('ctrl', 'v')
        i += 1

if __name__ == '__main__':
    
    print('Electrolux_PC_RPA欢迎使用')
    #数据检查
    # checkCmd = dataCheck(allData)
    A = open('webRPAResouece.json', encoding='UTF-8') 
    allDataA = json.load(A)
    # D = open('webRPAGameImageD.json', encoding='UTF-8') 
    key=input('选择功能: 1.做一次 2.循环到死 \n')
    if key=='1':
        #循环拿出每一行指令
        mainWork(allDataA["data"])
    elif key=='2':
        while True:
            mainWork(allDataA["data"])
            time.sleep(0.1)
            print("Wait0.1秒")    