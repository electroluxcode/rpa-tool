const innosetup = require('innosetup-compiler');
const path = require('path');
const fs = require('fs-extra');

console.log('开始编译PaddleOCR-json安装程序...');

// 确保输出目录存在
fs.ensureDirSync(path.join(__dirname, 'output'));

// 编译Inno Setup脚本
innosetup(path.join(__dirname, 'installer.iss'), {
  gui: false,
  verbose: true
}, function(error) {
  if (error) {
    console.error('编译错误:', error);
    return;
  }
  
  console.log('安装程序已成功创建!');
  console.log('输出位置:', path.join(__dirname, 'output', 'PaddleOCR-json_setup.exe'));
}); 