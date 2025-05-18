import pyautogui
import time
import json
import sys
import pyperclip
import getopt
from win32api import SetConsoleCtrlHandler
#定义鼠标事件
#pyautogui库其他用法 https://blog.csdn.net/qingfengxd1/article/details/108270159
import socketio

sio = socketio.Client()

def socketioInit(port=5000):
    # 连接服务端 IP+端口
    sio.connect('http://localhost:'+str(port))
    print("ws连接中")
def socketioSend(ut):
    # 向服务端发送消息
    sio.emit('rpa_tool_message', ut)


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
                time.sleep(0.5)
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

        if cmdType == "Click":   
            pyautogui.click( 
                x=cmdParam.get("x"), 
                y=cmdParam.get("y"), 
                clicks=cmdParam.get("clicks", 1), 
                interval=cmdParam.get("interval", 0), 
                button=cmdParam.get("button", "left")
            )
            print("点击",cmdParam,"次")

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
            mouseClick(
                1,
                cmdParam.get("button","left"),
                cmdParam.get("imgPath"),
                cmdParam.get("reTry", 1)
            )
            print("点击",cmdParam,"次")

        
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
            pyautogui.keyDown(cmdParam)
            print("KeyDown")
        
        # 10
        if cmdType == "KeyUp":
            print("KeyUp")
            pyautogui.keyUp(cmdParam)

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
        if cmdType == "WebRPA":
            message={
                 "message": cmdParam
            }
            socketioSend(ut=message)
            time.sleep(0.2)
            pyautogui.hotkey('ctrl', 'v')
        i += 1


# 解决socket不能退出的问题
def handler(event):
    if event == 0:
        exit()


if __name__ == '__main__':
    SetConsoleCtrlHandler(handler, 1)
    try:
        opts, args = getopt.getopt(sys.argv[1:], "f:s:p:", ["file=", "source=", "port="])
    except getopt.GetoptError as err:
        print(err)  # will print something like "option -a not recognized"
        sys.exit(2)
    for o, a in opts:
        if o in ("-p", "--port"):
            socketioInit(port=int(a))

        elif o in ("-f", "--file"):
            print("file:", a)
            with open(a, 'r', encoding='utf-8') as file: 
                content = file.read() 
                param_dict = json.loads(content)
                mainWork(param_dict)
        elif o in ("-o", "--source"):
            print("source:", a)
            try:
                param_dict = json.loads(a)
                mainWork(param_dict)
            except json.JSONDecodeError as e:
                 print('传入的参数无法解析为合法的JSON格式，错误信息：', e)
   
