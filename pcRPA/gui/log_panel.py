from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QLabel, QFrame, 
                             QPushButton, QTextEdit, QFileDialog, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from datetime import datetime

class LogPanel(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameStyle(QFrame.StyledPanel)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # 日志标题和控制按钮
        header_layout = QHBoxLayout()
        
        log_title = QLabel("📋 执行日志")
        log_title.setFont(QFont("Microsoft YaHei", 18, QFont.Bold))
        log_title.setStyleSheet("color: #00D4AA; padding: 15px;")
        
        clear_btn = QPushButton("🗑️ 清空")
        clear_btn.clicked.connect(self.clear_log)
        clear_btn.setMaximumWidth(100)
        clear_btn.setMinimumHeight(40)
        clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #E67E22;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                font-size: 14px;
                padding: 10px 15px;
            }
            QPushButton:hover {
                background-color: #D35400;
            }
        """)
        
        save_btn = QPushButton("💾 保存")
        save_btn.clicked.connect(self.save_log)
        save_btn.setMaximumWidth(100)
        save_btn.setMinimumHeight(40)
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #8E44AD;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                font-size: 14px;
                padding: 10px 15px;
            }
            QPushButton:hover {
                background-color: #7D3C98;
            }
        """)
        
        header_layout.addWidget(log_title)
        header_layout.addStretch()
        header_layout.addWidget(clear_btn)
        header_layout.addWidget(save_btn)
        layout.addLayout(header_layout)
        
        # 日志显示区域
        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        self.log_display.setStyleSheet("""
            QTextEdit {
                background-color: #1A1A1A;
                color: #E0E0E0;
                border: 2px solid #444;
                border-radius: 8px;
                padding: 15px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 15px;
                line-height: 1.8;
            }
        """)
        layout.addWidget(self.log_display)
        
        # 添加欢迎消息
        self.add_log("🎉 欢迎使用 Electrolux PC RPA")
        self.add_log("💡 请选择数据源并配置执行参数")
    
    def add_log(self, message):
        """添加日志"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}"
        self.log_display.append(formatted_message)
        
        # 自动滚动到底部
        scrollbar = self.log_display.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def clear_log(self):
        """清空日志"""
        self.log_display.clear()
        self.add_log("🗑️ 日志已清空")
    
    def save_log(self):
        """保存日志"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "保存日志", "rpa_log.txt", "Text Files (*.txt);;All Files (*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.log_display.toPlainText())
                self.add_log(f"💾 日志已保存到: {file_path}")
                QMessageBox.information(self, "保存成功", f"日志已保存到:\n{file_path}")
            except Exception as e:
                QMessageBox.critical(self, "保存失败", f"保存日志时出错:\n{str(e)}")
                self.add_log(f"❌ 保存日志错误: {str(e)}") 