# 自己写的rpa工具教程: RPA-Tool

一个自己写的RPA工具，支持Python和EXE直接运行，适用于Windows PC端和Android移动端。本教程将详细介绍如何安装、配置和使用这款工具。

## 项目概述

RPA-Tool是一个自动化工具集，可以模拟鼠标点击、键盘输入、图像识别、OCR文字识别等操作，帮助您自动化日常重复性工作。

- **项目地址**：[https://github.com/electroluxcode/rpa-tool](https://github.com/electroluxcode/rpa-tool)
- **下载地址**：[https://github.com/electroluxcode/rpa-tool/releases/tag/0.0.6](https://github.com/electroluxcode/rpa-tool/releases/tag/0.0.6)

## 主要功能

- 图像识别和点击
- OCR文本识别和基于文本的操作
- 鼠标移动、点击、拖拽
- 键盘输入和按键操作
- 等待和延时
- 循环执行
- 支持JSON和Excel两种配置方式

## 安装方法

1. 从[项目发布页](https://github.com/electroluxcode/rpa-tool/releases/tag/0.0.6)下载最新的EXE安装包
2. 双击安装包，按照向导指示完成安装
3. 如果需要使用手机端RPA功能，请确保在电脑上安装了ADB工具（Android Debug Bridge）

## 运行方式

启动时默认进入GUI界面，你也可以通过命令行参数进入命令行模式。

## 命令参数详解

以下是PC端RPA支持的命令类型及其参数说明：

### 1. 图像识别与操作

这里将你图片放到和启动的exe同一个文件夹就可以了

| 命令类型(cmdType) | 描述 | 参数示例(cmdParam) |
|---------|------|---------|
| `ImgClick` | 查找并点击图片 | `{"target": ["button.jpg"]}` |
| `SearchImage` | 在屏幕上查找图片 | `{"target": ["button.jpg"], "waitForTarget": true, "detecttime": 0.5, "maxWaitTime": 30}` |
| `ClickAfterImg` | 在找到的图片位置进行点击 | `{"x": 0, "y": 0, "clicks": 1, "button": "left"}` |
| `MoveToAfterImg` | 移动到找到的图片位置 | `{"x": 100, "y": 50}` |
| `DragToAfterImg` | 从找到的图片位置拖拽到指定位置 | `{"x": 200, "y": 100}` |

### 2. 鼠标操作

| 命令类型(cmdType) | 描述 | 参数示例(cmdParam) |
|---------|------|---------|
| `Click` | 点击指定坐标 | `{"x": 100, "y": 100, "clicks": 2}` |
| `MoveTo` | 移动鼠标到指定坐标 | `{"x": 100, "y": 100}` |
| `DragTo` | 拖拽到指定坐标 | `{"x": 100, "y": 100}` |
| `Scroll` | 滚轮操作 | `10` (正数向下滚动，负数向上滚动) |

### 3. 键盘操作

| 命令类型(cmdType) | 描述 | 参数示例(cmdParam) |
|---------|------|---------|
| `Write` | 输入文本 | `{"message": "Hello World"}` |
| `ChineseWrite` | 输入中文文本 | `"你好世界"` |
| `Press` | 按下并释放按键 | `{"keys": "enter", "presses": 1}` |
| `KeyDown` | 按下按键 | `"enter"` |
| `KeyUp` | 释放按键 | `"enter"` |

### 4. OCR文字识别与操作

| 命令类型(cmdType) | 描述 | 参数示例(cmdParam) |
|---------|------|---------|
| `OCR` | 执行OCR文字识别 | `{"target": ["文件"], "waitForTarget": true, "detecttime": 0.5, "maxWaitTime": 30}` |
| `ClickAfterOCR` | 基于OCR结果点击 | `{"x": 100, "y": 100}` |
| `MoveToAfterOCR` | 基于OCR结果移动鼠标 | `{"x": 100, "y": 100}` |
| `DragToAfterOCR` | 基于OCR结果拖拽 | `{"x": 200, "y": 100}` |

### 5. 其他操作

| 命令类型(cmdType) | 描述 | 参数示例(cmdParam) |
|---------|------|---------|
| `Sleep` | 等待指定秒数 | `2` |
| `ShutDown` | 关机 | `{"timeout": 10}` |

## 参数详细解释

以下是常用参数的详细解释：

### 通用参数

| 参数名 | 类型 | 描述 | 示例值 |
|-------|-----|------|-------|
| `x` | 整数 | 屏幕横坐标，以像素为单位，从左到右增大 | `100` |
| `y` | 整数 | 屏幕纵坐标，以像素为单位，从上到下增大 | `200` |
| `clicks` | 整数 | 点击次数，默认为1，用于设置单击、双击等 | `2` |
| `button` | 字符串 | 鼠标按键，可选值为"left"(左键)、"right"(右键)、"middle"(中键)，默认为"left" | `"right"` |

### 查找与等待相关参数

| 参数名 | 类型 | 描述 | 示例值 |
|-------|-----|------|-------|
| `target` | 数组 | 要查找的目标列表，可以是图片文件名或文本内容 | `["button.jpg", "button_alt.jpg"]` |
| `waitForTarget` | 布尔值 | 是否等待目标出现，为true时会持续查找直到找到目标或超时 | `true` |
| `detecttime` | 浮点数 | 检测间隔时间(秒)，指定每次重新查找的时间间隔 | `0.5` |
| `maxWaitTime` | 整数 | 最大等待时间(秒)，指定等待目标出现的最长时间，超时后会继续执行下一步 | `30` |
| `region` | 字符串 | 查找区域，可选值如"center"(屏幕中心区域)，默认为整个屏幕 | `"center"` |

### 键盘操作相关参数

| 参数名 | 类型 | 描述 | 示例值 |
|-------|-----|------|-------|
| `message` | 字符串 | 要输入的文本内容 | `"Hello World"` |
| `keys` | 字符串 | 按键名称，如"enter"、"tab"、"f1"等 | `"enter"` |
| `presses` | 整数 | 按键次数，默认为1 | `2` |
| `interval` | 浮点数 | 连续点击/按键之间的间隔时间(秒) | `0.25` |

### 鼠标操作相关参数

| 参数名 | 类型 | 描述 | 示例值 |
|-------|-----|------|-------|
| `duration` | 浮点数 | 鼠标移动的持续时间(秒)，值越大移动越慢，默认为0.25 | `0.5` |

### 其他参数

| 参数名 | 类型 | 描述 | 示例值 |
|-------|-----|------|-------|
| `timeout` | 整数 | 在ShutDown命令中，指定关机前的等待时间(秒) | `60` |
| `then` | 数组 | 在OCR命令中，指定找到目标后要执行的后续操作列表 | `[{"cmdType": "ClickAfterOCR", "cmdParam": {"x": 50, "y": 0}}]` |

## 使用实例

下面是一个完整的JSON配置文件示例，展示了如何组合使用各种命令实现一个自动化流程：

```json
{
    "name": "示例",
    "data": [
       {
            "cmdType": "SearchImage",
            "cmdParam": {
                "target": ["button.jpg"],
                "waitForTarget": true,
                "detecttime": 0.5,
                "maxWaitTime": 30
            }
        },
        {
            "cmdType": "Sleep",
            "cmdParam": 2
        },
        {
            "cmdType": "Click",
            "cmdParam": {
                "x": 20,
                "y": 1050,
                "clicks": 1
            }
        }
    ]
}
```



## 高级用法

### 1. 条件等待与超时设置

对于图像识别和OCR操作，你可以设置等待条件：

```json
{
    "cmdType": "SearchImage",
    "cmdParam": {
        "target": ["button.jpg"],
        "waitForTarget": true,
        "detecttime": 0.5,
        "maxWaitTime": 30
    }
}
```

这将使RPA-Tool不断尝试寻找目标图像，直到找到或超时。

### 2. 链式操作

对于OCR识别，你可以定义一系列后续操作：

```json
{
    "cmdType": "OCR",
    "cmdParam": {
        "target": ["登录"],
        "waitForTarget": true,
        "then": [
            {
                "cmdType": "ClickAfterOCR",
                "cmdParam": {
                    "x": 50,
                    "y": 0
                }
            }
        ]
    }
}
```

### 3. 使用Excel配置

除了JSON，你还可以使用Excel表格配置自动化流程。选择"创建Excel模板"选项可以生成一个模板文件，然后按照模板格式填写命令和参数。

### 4. 全局热键

在脚本执行过程中，按下F10键可以随时中断脚本执行。

## 注意事项

1. 对于图像识别功能，建议使用清晰、特征明显的截图
2. 坐标点是相对于屏幕左上角的像素位置
3. 使用OCR功能需要确保已正确安装PaddleOCR相关组件
4. 移动端操作需要确保手机已通过ADB连接到电脑


