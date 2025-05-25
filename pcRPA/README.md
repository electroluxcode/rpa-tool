# 1. pcRPA

## 1.1 说明

参数说明和参数使用方法参考可以参照 `pcDataExample.json` ，都是语义化的东西

核心是两个文件

- pcRPA.py  用来执行json中的代码，默认读取 pcRPAResouece.json 中的代码 

## 1.2 打包

pip install pyinstaller  -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com
pyinstaller -F  -i ./ico/rpa.png  pcRPA.py

-F：生成单个可执行文件
-w：不显示控制台窗口（Windows 系统下）
-i ./ico/rpa.png：设置应用程序图标

## 1.3 开发

### 1.3.1 依赖库

https://repo.anaconda.com/archive/

### 1.3.2 安装

```shell
conda config --set show_channel_urls yes

conda create -n autoPC311-new python=3.11
conda activate autoPC311-new  

python -m pip install pyperclip xlrd pillow -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com

python -m pip install opencv-python==4.11.0.86 pyautogui==0.9.54 -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com

python -m pip install PyQt5 numpy pynput  -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com 


pip install python-socketio eventlet -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com

pip install pypiwin32   socketio eventlet  -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com

python pcRPA.py  
```



### 1.3.3 ocr模块可选

ref: `packages\paddleocr-installer\README.md`



```js
关于开发者的小tips
pip install pipreqs
pipreqs ./ --encoding=utf8

```



