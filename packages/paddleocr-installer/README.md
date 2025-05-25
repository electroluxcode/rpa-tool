# PaddleOCR-json 安装程序生成工具

这个工具用于将PaddleOCR-json打包成Windows安装程序，并在安装时将程序路径添加到环境变量。
打包的时候将asset放在对应的文件夹中就可以了
ref: https://github.com/hiroi-sora/PaddleOCR-json


## 功能

- 生成可执行的安装程序(.exe)
- 支持自定义安装路径
- 安装时自动将程序路径添加到系统环境变量
- 卸载时自动从系统环境变量中移除程序路径

## 使用方法

1. 确保已安装Node.js和Inno Setup
2. 克隆或下载本仓库
3. 在命令行中运行以下命令：

```bash
# 安装依赖
npm install

# 构建安装程序
npm run build
```

4. 构建完成后，安装程序将位于`output`目录中

## 安装Inno Setup


## 目录结构

```
paddleocr-installer/
├── index.js          # 主脚本文件
├── installer.iss     # Inno Setup脚本
├── package.json      # 项目配置
└── output/           # 输出目录
    └── PaddleOCR-json_setup.exe  # 生成的安装程序
```

## 注意事项

- 此工具假设PaddleOCR-json文件夹位于上一级目录中
- 确保您有足够的磁盘空间来生成安装程序
- 构建过程可能需要几分钟时间，取决于您的计算机性能 