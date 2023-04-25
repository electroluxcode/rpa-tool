



用python | adb | opencv | pyautogui实现手机和电脑的自动化。具体的请看各个文件夹的README







# electroluxRPA

[![gitee](https://img.shields.io/static/v1?label=Gitee&message=Electrolux&color=blue)](https://gitee.com/Electrolux)[![bili](https://img.shields.io/static/v1?label=Bili&message=Electrolux&color=yellow)](https://space.bilibili.com/286773126)[![Contribute](https://img.shields.io/static/v1?label=Contribute&message=welcome&color=red)](https://gitee.com/Electrolux)[![Size](https://img.shields.io/static/v1?label=Size&message=4MB&color=green)](https://gitee.com/Electrolux)



<img src="https://cdn.jsdelivr.net/npm/frontengineerplugin/img/main.png"/>



##  Quickstart

begin

```shell
npm install frontengineerplugin -g
# 第一种方法，推荐：
npm run  engineer 
# 第二种方法：不推荐 项目根目录的package.json中输入
frontengineerplugin install prettier husky env eslint npm
# 第三种方法：命令行下面 输入
frontengineerplugin gui
```





## struct

```js
tree /f > list.txt 生成

│  README.md // 总的readme
│  
├─pcRPA  // pc端 的  RPA
│      pcData.json // 你的逻辑写在这里
│      pcDataExample.json  // 所有示例的传参
│      pcRPA.py   // RPA主文件   python pcRPA.py
│      README.md // pc端 的 readme
│      requirements.txt // 依赖文件
│      test.py // 我的测试文件
│      
└─phoneRPA // 手机端的  RPA
    │  button.jpg 
    │  output.png
    │  phoneData.json // 你的逻辑写在这里
    │  phoneDataExample.json // 所有示例的传参
    │  phoneRPA.py // RPA主文件   python phoneRPA.py
    │  phoneRPAFn.py // 本来想模块化的，结果发现虚拟环境(conda)和用exe真实环境的模块有出入，因此删掉了这个文件
    │  README.md // 移动端 的 readme
    │  requirements.txt  // 依赖文件
    │  screen.png // 这就是你 手机上面的 截图 
    │  test.py // 我的测试文件
    │  ui.xml // ui的 xml 文件 也是 通过 adb 得到的 。 用来查找UI的属性 进行点击
    │  
    ├─adb
    │      adb.zip  // 这玩意解压后 添加环境变量就好了
    │      adb说明.md
    │      element.sh
    │      index.sh
    │      index.txt
    │      ls.txt
    │      test.txt
    │      
    
            

```











## Developer

```js
如果你想添加你自己工程化的东西
--1.首先将你的文件放进file 文件夹
--2.修改project.js和util/handleEvent.js里面的文件，将你的方法添加进去
--3.接下来的测试阶段请输入npm link 
然后 npm run engineer 
```



## Example



手机识图示例

<img src = "./img/mobile.gif">

pc端示例

<img src = "./img/data.png">















## Badge

[![Size](https://img.shields.io/static/v1?label=plugin&message=frontEngineerPlugin&color=green)](https://gitee.com/Electrolux)

```
[![Size](https://img.shields.io/static/v1?label=plugin&message=frontEngineerPlugin&color=green)](https://gitee.com/Electrolux)
```



## Support

frontEngineerPlugin is developed by me. Please use frontEngineerPlugin, star it on gitee or even become a [sponsor](https://gitee.com/Electrolux) to support us!



## update