<div align="center"><h1>
<br/>
🔨 
<br />
electroluxRPA
<br /><br />
</h1>
<sup>
<br />
<br />
<a href="none"><img src="https://img.shields.io/static/v1?label=version&message=v1.0.0&color=blue" alt="npm package" /></a><a href=https://space.bilibili.com/286773126><img src="https://img.shields.io/static/v1?label=Bili&message=Electrolux&color=pink" alt="temp" /></a>
<a href="none">   <img src="https://img.shields.io/static/v1?label=Author&message=Electrolux&color=yellow" alt="demos" /></a>
<a href="none">   <img src="https://img.shields.io/static/v1?label=Contribute&message=welcome&color=green" alt="demos" /></a>
<br />
</a>
<br />
Translations: <a href="">🇨🇳 汉语</a>
</sup>
</div>




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
如果你想添加你自己的东西
--1.在pcRPA.py 和 phoneRPA.py 中 的 mainWork中 添加事件
--2.为了程序的可读性，可以在pcDataExample.json和 phoneDataExample.json中添加你的示例
--3.只要在 pcData.json 和 phoneData.json 中 添加 你的参数 然后 python 你的文件.py就可以运行
```



## Example



手机识图示例

<img src = "./img/mobile.gif">

pc端示例

<img src = "./img/data.png">















## Badge

[![Size](https://img.shields.io/static/v1?label=plugin&message=electroluxRPA&color=green)](https://gitee.com/Electrolux)

```
[![Size](https://img.shields.io/static/v1?label=plugin&message=electroluxRPA&color=green)](https://gitee.com/Electrolux)
```



## Support

frontEngineerPlugin is developed by me. Please use frontEngineerPlugin, star it on gitee or even become a [sponsor](https://gitee.com/Electrolux) to support us!



## update