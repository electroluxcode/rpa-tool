# pcRPA

## 说明

参数说明和参数使用方法参考可以参照 `pcDataExample.json` ，都是语义化的东西

核心是两个文件

- pcRPA.py 用来执行json中的代码，默认读取 pcData.json 中的代码 
- pcRPAToolCli.py 用来执行命令行的代码，以供其他语言直接调用，以下是调用实例
- pcRPAToolCli.exe 在released中，功能和pcRPAToolCli.py 相同，打包是为了方便使用


## 打包
pip install pyinstaller  -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com
pyinstaller -F -w -i ./ico/rpa.png  pcRPAToolCli.py

## 开发
```js
--1.去到这个网站然后下载，注意只为我安装就可以添加到环境变量
https://repo.anaconda.com/archive/
--2.安装完后运行命令
conda create -n autoPC python=3.7
conda activate autoPC    

pip install pyperclip xlrd pillow -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com

pip install opencv-python==4.5.3.56 pyautogui==0.9.50 -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com

python pcRPA.py   


--3.然后我们看到pcData.json中

可以根据pcDataExample.json里面的示例来定义自己想要的东西

--4.关于开发者的小tips
pip install pipreqs
pipreqs ./ --encoding=utf8

```




