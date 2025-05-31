# 1. pcRPA

## description

参数说明和参数使用方法参考可以参照 `pcDataExample.json` ，都是语义化的东西

核心是两个文件

- pcRPA.py  用来执行json中的代码，默认读取 pcRPAResouece.json 中的代码 

## build

pip install pyinstaller  -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com
pyinstaller -F  -i ./ico/rpa.png  pcRPA.py

-F：生成单个可执行文件
-w：不显示控制台窗口（Windows 系统下）
-i ./ico/rpa.png：设置应用程序图标

## dev

### dev env

https://repo.anaconda.com/archive/

### install

```shell
conda config --set show_channel_urls yes

conda create -n autoPC311-new python=3.11
conda activate autoPC311-new  

python -m pip install pyperclip xlrd pillow -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com

python -m pip install opencv-python==4.11.0.86 pyautogui==0.9.54 -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com

python -m pip install PyQt5 numpy pynput  -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com 


pip install python-socketio eventlet -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com

pip install pypiwin32   socketio eventlet  -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com


pip install pandas -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com
python pcRPA.py  
```



### extra feat

ref: `packages\paddleocr-installer\README.md`



```js
关于开发者的小tips
pip install pipreqs
pipreqs ./ --encoding=utf8

```

### todo

- [] 支持浏览器插件引入
- [] 支持命令行调用


