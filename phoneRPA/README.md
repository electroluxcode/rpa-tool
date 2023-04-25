# phoneRPA



## 1.ADB

```JS
无线连接必须先有线连接
--1. 手机上开发者选项和USB调试 模拟点击打开
--2. 这个文件夹下面的adb/adb.zip 解压后，添加这个环境到环境变量
--3. 有线连上后
--3.1 adb devices // 输出现在连接的设备，有限连接后 才有设备。这个时候 会输出 xxxxxx（反正不是空值）
--3.2 手机上设置中状态信息 找到手机ipv4的地址
--3.3 adb tcpip 6666 //电脑端开启新的端口，这个时候可以拔掉有线连接
--3.4 adb connect 172.18.89.56:6666 //（手机网段 在步骤3.2 找到的）
--3.5 这时候就可以开始了
```

## 2.Python

```js
--1.去到这个网站然后下载，注意只为我安装就可以添加到环境变量
https://repo.anaconda.com/archive/
--2.安装完后可以
conda create -n autoPhone python=3.7
conda activate autoPhone 

pip install -r requirements.txt


opencv的区域往色彩多的地方画


python phoneRPA.py

--3.然后我们看到pcData.json中

可以根据pcDataExample.json里面的示例来定义自己想要的东西

--4.关于开发者的小tips
pip install pipreqs
pipreqs ./ --encoding=utf8


--5.遇到一个大坑，关于模块无法导入的问题
原因是虚拟环境 conda 需要 需要

--5.1打开命令面板 ( Ctrl++ )，然后选择ShiftPython : Select Interpreter。从列表中，选择项目文件夹中以 开头的虚拟环境。P.env

--5.2运行终端：创建新的集成终端（Ctrl++或从命令面板），这将创建一个终端并通过运行其激活脚本自动Shift激活虚拟环境。

--5.3 Python: Clear Cache and Reload Window

鉴于不同环境可能无法导入的问题，所以我干脆模块都写进一个文件去。第五点不用看了

```






