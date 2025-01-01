import pyautogui
import time
import pyperclip
import json
import sys
#定义鼠标事件
#pyautogui库其他用法 https://blog.csdn.net/qingfengxd1/article/details/108270159

def mouseClick(clickTimes,lOrR,img,reTry):
    print("正在寻找图片：")
    print(img)
    if reTry == 1:
        while True:
            try:
                location=pyautogui.locateCenterOnScreen(img,confidence=0.7)
                if location is not None:
                    pyautogui.click(location.x,location.y,clicks=clickTimes,interval=0.2,duration=0.2,button=lOrR)
                    break
                print("未找到匹配图片,0.5秒后重试")
                time.sleep(0.5)
            except:
                print("未找到匹配图片,0.5秒后重试")
                pass
    elif reTry > 1:
        i = 1
        while i < reTry + 1:
            try:
                location=pyautogui.locateCenterOnScreen(img,confidence=0.9)
                if location is not None:
                    pyautogui.click(location.x,location.y,clicks=clickTimes,interval=0.2,duration=0.2,button=lOrR)
                    print("重复")
                    i += 1
                time.sleep(0.1)
            except:
                print("重复")
                pass
    elif reTry == 0:
        if True:
            try:
                location=pyautogui.locateCenterOnScreen(img,confidence=0.7)
                if location :
                    print("遇到指定图片停止30分钟")
                    time.sleep(1*60*30)
            except:
                pass


#主任务
def mainWork(allData):
    i = 0
    while i < len(allData):
        cmdType = allData[i]["cmdType"]
        cmdParam = allData[i]["cmdParam"]
        cmdCound = allData[i]["cmdCound"]

        # 1.点击鼠标
        if cmdType == "ClickPosition":   
            pyautogui.click(x=cmdParam["x"], y=cmdParam["y"], clicks=cmdCound, interval=0.25, button='left')
            print("点击",cmdParam,cmdCound,"次")

        # 2.MouseMove
        if cmdType == "MouseMove":   
            pyautogui.moveTo(x=cmdParam["x"], y=cmdParam["y"], duration=0.25)
            print("MouseMove到",cmdParam)

        # 3.MouseDrag
        if cmdType == "MouseDrag":   
            pyautogui.dragTo(x=cmdParam["x"], y=cmdParam["y"], duration=0.25,button='left')
            print("MouseDrag到",cmdParam)

        # 4.ClickImage
        if cmdType == "ClickImage":   
            mouseClick(1,"left",cmdParam,cmdCound)
            print("点击",cmdParam,cmdCound,"次")

        # 5.RightClick点击
        if cmdType == "RightClick":
            mouseClick(1,"right",cmdParam,cmdCound)
            print("RightClick",cmdParam,cmdCound,"次")
        
        # 6.Input
        if cmdType == "Input":
            pyperclip.copy(cmdParam)
            pyautogui.hotkey('ctrl','v')
            time.sleep(0.5)
            print("Input:",cmdParam)                                        
        
        # 7.Wait
        if cmdType == "Wait":
            time.sleep(cmdParam)
            print("Wait",cmdParam,"秒")
        
        # 8.滚轮
        if cmdType == "Wheel":
            pyautogui.scroll(int(cmdParam))
            print("滚轮滑动",int(cmdParam),"距离")  
        
        # 9.网页刷新
        if cmdType == "SiteFresh":
            time.sleep(2)
            pyautogui.keyDown('f5')
            print("SiteFresh")
            time.sleep(0.5)
        
        # 10.tab栏目切换
        if cmdType == "TabSwitch":
            print("TabSwitch")
            pyautogui.hotkey('ctrl','tab')
            time.sleep(1)           
        i += 1

if __name__ == '__main__':
    
    if len(sys.argv) > 1:
        try:
            # 获取传入的第一个参数（索引为1，因为索引0是脚本自身名称）并尝试解析为字典
            
            print(sys.argv)
            param_dict = json.loads(sys.argv[1])
            print(param_dict)
            """
step1: 定义传参
const data =  '[{ "cmdType": "ClickPosition", "cmdParam":{ "x":146, "y":400 }, "cmdCound":1 }]'

const normalJsonStr = JSON.stringify(data)
const escapedJsonStr = (normalJsonStr).replaceAll("\"", "\\\"").replaceAll("\\\\", "\\")
// 传参的值
console.log(escapedJsonStr);
step2 : python pcRPAToolCli.py [{\"cmdType\":\"ClickPosition\",\"cmdParam\":{\"x\":146,\"y\":400},\"cmdCound\":1}]

            """
            mainWork(param_dict)
        except json.JSONDecodeError as e:
            print('传入的参数无法解析为合法的JSON格式，错误信息：', e)
   
