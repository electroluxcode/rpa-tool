import json
import time
import pyautogui
from time import sleep
#导入pynput控制鼠标的模块
from pynput import mouse
import sys
from pynput.keyboard import Key,Listener
 
# pyautogui.alert(text='This is an alert box.', title='Test')
# 阿里云 
# http://mirrors.aliyun.com/pypi/simple/
# 豆瓣
# http://pypi.douban.com/simple/
 
 
mx = 0
my = 0
bt = "left"
count = 1
t1 = t2 = time.time()
 
# 鼠标move监听
def on_move(x, y):
    print(f'Current position： ({x}, {y})')
    global count 
    count = 1
 
# 鼠标click监听
def on_click(x, y, button, pressed):
    #print(f'Click position： ({x}, {y})')
    global count 
    global mx 
    global my
    global bt
    global t1
    global t2
    if pressed :
        if mx == x and my == y and bt == button  :
            if count ==1:
                t1 = time.time()
                print(t1)
                print('\n')
            t2 = time.time()
            print(t2)
            if t2 - t1<1:
                count = count + 1
        else:
            bt = str(bt)[7:]
            with open(r'./record.json','a',encoding='utf8') as f:
                s = f"\n({mx}, {my})Click button： {bt}   times:{count} "                 
                s1 = f"\ntime.sleep(0.5)\npyautogui.click(x={mx}, y={my},clicks={count}, interval=0.0, button='{bt}', duration=0.0, tween=pyautogui.linear) "                 
                f.write(s1)
            print("zuobiao:",mx,my)
            count = 1
            mx,my = x,y
            bt = button
 
# 鼠标滚轮scroll监听
def on_scroll(x, y, dx, dy):
    print(f'Scroll position： ({x}, {y})')
    print(f'Scroll direction： ({dx}, {dy})')
    return False
 
def on_press(key):
    global press_key
    with open(r'./record.json','a',encoding='utf8') as f:
        try:
            print(f"正在按压key:{key.char}")
            press_key = key.char 
            s1 = f"\npyautogui.keyDown({key}) "
            print(key)                 
            f.write(s1)
            
        except AttributeError:
            print("正在按压:{}".format(key))
            s1 = f"\npyautogui.keyDown('{str(key)[4:]}') "  
            print(str(key)[4:])  
            print(key)             
            f.write(s1)
 
def on_release(key):
    with open(r'./record.json','a',encoding='utf8') as f:
        try:
            press_key = key.char 
            s1 = f"\npyautogui.keyUp({key}) " 
            print(key)                
            f.write(s1)
            
        except AttributeError:
            print("正在按压:{}".format(key))
            s1 = f"\npyautogui.keyUp('{str(key)[4:]}') " 
            print(key)                
            f.write(s1)        
 
# 开始键盘监听
def start_listen():
    with Listener(on_press=on_press,on_release=on_release) as listener:
        listener.join()
 
def record_script():
    with mouse.Listener(on_click=on_click, on_scroll=on_scroll) as listener :
        listener.join()  
 
if __name__ == '__main__':
    key_listener = Listener(on_press=on_press,on_release=on_release)
    key_listener.start()
    control = mouse.Controller() 
    with open(r'./record.json','a',encoding='utf8') as f:
        f.write("\nimport pyautogui\nimport  time \n")
    record_script()
    # start_listen()
    print("zuobiao:",mx,my)
 
 
 