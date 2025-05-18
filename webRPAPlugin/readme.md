reactConvertPlugin:

https://c.runoob.com/front-end/854/

我做这个插件的目的主要是我做页面的时候喜欢先用原生css实现一遍，然后接着导入到项目中。react的css又不像vue一样好用，因此写了这个插件，能够将原生css转化成react并且能够加上hash值。效果如下：

<img src="./img/index.png"/>

浏览器导入即可

```js
--1.使用：
--1.1 先把你的公共类名搞进去，点击提取类名，将下面栏目生成的类名替换commonClassName变量。如果有伪类也可以放进PseudoClasses这个变量里面
--1.2 将你的html文件放进上面的栏目先点击转化全部，然后手动把下面栏目生成的结果放到上面去，接下来就可以进行style标签和body标签的选择
--1.3 注意一下 需要在vscode中格式化才能够用（主要是伪类中间不能够空格），不然伪类那里会有问题
```



更新日志：

2023/1/4 增加自定义hash值，增加html和css公共类名逻辑，进一步解耦。伪类也进行解耦

2022/12/31 优化执行逻辑，css和body代码做到逻辑上分离。代码进行了解耦。转化css的代码添加了伪类的处理逻辑.增加公共类名过滤功能

2022/12/30 优化class的正则判断，解决了class 多个类名的识别bug。优化并列style的判断。添加转化css样式，转化html模板两个功能

2022/12/29 优化style的正则





```js
-- 一些测试的时候的东西
--1.vscode中快速替换
class="(.*)"
className="$1"

--2.

let text = ` <div class="test"></div>`
text.replace(/class="(.*)"/,"className=\"$1\"")

--3.测试用例
<div class="container">
    <div class="test2"></div>
</div> 
<style>
.test2{
    background:red
}
<style>
    

    
```

