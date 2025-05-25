import sys
import json
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QWidget, QPushButton, QTextEdit, QLabel, QFileDialog, 
                             QRadioButton, QButtonGroup, QSplitter, QFrame, QMessageBox,
                             QProgressBar, QGroupBox, QGridLayout, QScrollArea)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QPalette, QColor, QIcon
from rpa_command import RPACommand

class RPAWorkerThread(QThread):
    log_signal = pyqtSignal(str)
    finished_signal = pyqtSignal()
    
    def __init__(self, rpa_command, data, is_loop=False):
        super().__init__()
        self.rpa_command = rpa_command
        self.data = data
        self.is_loop = is_loop
        self._is_running = False
        
    def run(self):
        self._is_running = True
        try:
            if self.is_loop:
                self.rpa_command.execute_loop(self.data)
            else:
                self.rpa_command.execute_once(self.data)
        except Exception as e:
            print(f"执行过程中出错: {e}")
        finally:
            self._is_running = False
            self.finished_signal.emit()
    
    def stop(self):
        """停止线程"""
        if self.rpa_command:
            self.rpa_command.stop_execution()
        self._is_running = False

class RPAMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.rpa_command = None
        self.worker_thread = None
        self.current_data = None
        self.init_ui()
        self.apply_dark_theme()
        
    def init_ui(self):
        self.setWindowTitle("Electrolux PC RPA - 可视化界面")
        self.setGeometry(100, 100, 1200, 800)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QHBoxLayout(central_widget)
        
        # 创建分割器
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # 左侧控制面板
        left_panel = self.create_control_panel()
        splitter.addWidget(left_panel)
        
        # 右侧日志面板
        right_panel = self.create_log_panel()
        splitter.addWidget(right_panel)
        
        # 设置分割器比例
        splitter.setSizes([400, 800])
        
    def create_control_panel(self):
        """创建左侧控制面板"""
        panel = QFrame()
        panel.setFrameStyle(QFrame.StyledPanel)
        panel.setMaximumWidth(450)
        
        layout = QVBoxLayout(panel)
        
        # 标题
        title = QLabel("🤖 RPA 控制中心")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Microsoft YaHei", 16, QFont.Bold))
        title.setStyleSheet("color: #00D4AA; margin: 10px; padding: 10px;")
        layout.addWidget(title)
        
        # 数据源配置组
        data_group = QGroupBox("📁 数据源配置")
        data_group.setFont(QFont("Microsoft YaHei", 10, QFont.Bold))
        data_layout = QVBoxLayout(data_group)
        
        # 文件上传按钮
        self.upload_btn = QPushButton("📤 上传 JSON 文件")
        self.upload_btn.clicked.connect(self.upload_json_file)
        self.upload_btn.setMinimumHeight(40)
        data_layout.addWidget(self.upload_btn)
        
        # 当前文件标签
        self.file_label = QLabel("📄 当前文件: 未选择")
        self.file_label.setWordWrap(True)
        self.file_label.setStyleSheet("color: #888; padding: 5px;")
        data_layout.addWidget(self.file_label)
        
        # JSON编辑器
        json_label = QLabel("✏️ 或直接编辑 JSON:")
        json_label.setFont(QFont("Microsoft YaHei", 9, QFont.Bold))
        data_layout.addWidget(json_label)
        
        self.json_editor = QTextEdit()
        self.json_editor.setMinimumHeight(200)
        self.json_editor.setPlaceholderText('{\n  "data": [\n    {\n      "cmdType": "Click",\n      "cmdParam": {\n        "x": 100,\n        "y": 100\n      }\n    }\n  ]\n}')
        data_layout.addWidget(self.json_editor)
        
        # 验证JSON按钮
        self.validate_btn = QPushButton("✅ 验证 JSON 格式")
        self.validate_btn.clicked.connect(self.validate_json)
        self.validate_btn.setMinimumHeight(35)
        data_layout.addWidget(self.validate_btn)
        
        layout.addWidget(data_group)
        
        # 执行配置组
        exec_group = QGroupBox("⚙️ 执行配置")
        exec_group.setFont(QFont("Microsoft YaHei", 10, QFont.Bold))
        exec_layout = QVBoxLayout(exec_group)
        
        # 执行模式选择
        mode_label = QLabel("🔄 执行模式:")
        mode_label.setFont(QFont("Microsoft YaHei", 9, QFont.Bold))
        exec_layout.addWidget(mode_label)
        
        self.mode_group = QButtonGroup()
        self.once_radio = QRadioButton("🎯 执行一次")
        self.loop_radio = QRadioButton("🔁 无限循环")
        self.once_radio.setChecked(True)
        
        self.mode_group.addButton(self.once_radio, 0)
        self.mode_group.addButton(self.loop_radio, 1)
        
        exec_layout.addWidget(self.once_radio)
        exec_layout.addWidget(self.loop_radio)
        
        layout.addWidget(exec_group)
        
        # 控制按钮组
        control_group = QGroupBox("🎮 执行控制")
        control_group.setFont(QFont("Microsoft YaHei", 10, QFont.Bold))
        control_layout = QGridLayout(control_group)
        
        # 开始按钮
        self.start_btn = QPushButton("▶️ 开始执行")
        self.start_btn.clicked.connect(self.start_execution)
        self.start_btn.setMinimumHeight(50)
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #00D4AA;
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #00B894;
            }
            QPushButton:disabled {
                background-color: #555;
                color: #888;
            }
        """)
        
        # 停止按钮
        self.stop_btn = QPushButton("⏹️ 停止执行")
        self.stop_btn.clicked.connect(self.stop_execution)
        self.stop_btn.setEnabled(False)
        self.stop_btn.setMinimumHeight(50)
        self.stop_btn.setStyleSheet("""
            QPushButton {
                background-color: #E74C3C;
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #C0392B;
            }
            QPushButton:disabled {
                background-color: #555;
                color: #888;
            }
        """)
        
        control_layout.addWidget(self.start_btn, 0, 0)
        control_layout.addWidget(self.stop_btn, 0, 1)
        
        layout.addWidget(control_group)
        
        # 状态显示
        status_group = QGroupBox("📊 运行状态")
        status_group.setFont(QFont("Microsoft YaHei", 10, QFont.Bold))
        status_layout = QVBoxLayout(status_group)
        
        self.status_label = QLabel("💤 就绪")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: #00D4AA; font-size: 14px; padding: 10px;")
        status_layout.addWidget(self.status_label)
        
        layout.addWidget(status_group)
        
        # 添加弹性空间
        layout.addStretch()
        
        return panel
    
    def create_log_panel(self):
        """创建右侧日志面板"""
        panel = QFrame()
        panel.setFrameStyle(QFrame.StyledPanel)
        
        layout = QVBoxLayout(panel)
        
        # 日志标题
        log_title = QLabel("📋 执行日志")
        log_title.setAlignment(Qt.AlignCenter)
        log_title.setFont(QFont("Microsoft YaHei", 14, QFont.Bold))
        log_title.setStyleSheet("color: #00D4AA; margin: 10px; padding: 10px;")
        layout.addWidget(log_title)
        
        # 日志显示区域
        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        self.log_display.setFont(QFont("Consolas", 10))
        layout.addWidget(self.log_display)
        
        # 日志控制按钮
        log_control_layout = QHBoxLayout()
        
        self.clear_log_btn = QPushButton("🗑️ 清空日志")
        self.clear_log_btn.clicked.connect(self.clear_log)
        self.clear_log_btn.setMinimumHeight(35)
        
        self.save_log_btn = QPushButton("💾 保存日志")
        self.save_log_btn.clicked.connect(self.save_log)
        self.save_log_btn.setMinimumHeight(35)
        
        log_control_layout.addWidget(self.clear_log_btn)
        log_control_layout.addWidget(self.save_log_btn)
        log_control_layout.addStretch()
        
        layout.addLayout(log_control_layout)
        
        return panel
    
    def apply_dark_theme(self):
        """应用暗黑主题"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            QWidget {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            QFrame {
                background-color: #2d2d2d;
                border: 1px solid #404040;
                border-radius: 8px;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #404040;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #00D4AA;
            }
            QPushButton {
                background-color: #404040;
                color: white;
                border: 1px solid #555;
                border-radius: 6px;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #505050;
                border: 1px solid #00D4AA;
            }
            QPushButton:pressed {
                background-color: #353535;
            }
            QTextEdit {
                background-color: #252525;
                color: #ffffff;
                border: 1px solid #404040;
                border-radius: 6px;
                padding: 8px;
                font-family: 'Consolas', monospace;
            }
            QLabel {
                color: #ffffff;
            }
            QRadioButton {
                color: #ffffff;
                spacing: 8px;
            }
            QRadioButton::indicator {
                width: 16px;
                height: 16px;
            }
            QRadioButton::indicator:unchecked {
                border: 2px solid #555;
                border-radius: 8px;
                background-color: #2d2d2d;
            }
            QRadioButton::indicator:checked {
                border: 2px solid #00D4AA;
                border-radius: 8px;
                background-color: #00D4AA;
            }
            QSplitter::handle {
                background-color: #404040;
                width: 3px;
            }
            QSplitter::handle:hover {
                background-color: #00D4AA;
            }
        """)
    
    def upload_json_file(self):
        """上传JSON文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择 JSON 文件", "", "JSON Files (*.json);;All Files (*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    json.loads(content)  # 验证JSON格式
                    
                self.json_editor.setPlainText(content)
                self.file_label.setText(f"📄 当前文件: {os.path.basename(file_path)}")
                self.file_label.setStyleSheet("color: #00D4AA; padding: 5px;")
                self.add_log(f"✅ 成功加载文件: {file_path}")
                
            except json.JSONDecodeError as e:
                QMessageBox.warning(self, "JSON 格式错误", f"文件格式不正确:\n{str(e)}")
                self.add_log(f"❌ JSON格式错误: {str(e)}")
            except Exception as e:
                QMessageBox.critical(self, "文件读取错误", f"无法读取文件:\n{str(e)}")
                self.add_log(f"❌ 文件读取错误: {str(e)}")
    
    def validate_json(self):
        """验证JSON格式"""
        try:
            content = self.json_editor.toPlainText().strip()
            if not content:
                QMessageBox.warning(self, "验证失败", "JSON内容为空")
                return False
                
            data = json.loads(content)
            
            # 检查是否有data字段
            if "data" not in data:
                QMessageBox.warning(self, "验证失败", "JSON必须包含'data'字段")
                return False
            
            if not isinstance(data["data"], list):
                QMessageBox.warning(self, "验证失败", "'data'字段必须是数组")
                return False
            
            QMessageBox.information(self, "验证成功", "✅ JSON格式正确!")
            self.add_log("✅ JSON格式验证通过")
            return True
            
        except json.JSONDecodeError as e:
            QMessageBox.warning(self, "JSON 格式错误", f"格式不正确:\n{str(e)}")
            self.add_log(f"❌ JSON格式错误: {str(e)}")
            return False
    
    def start_execution(self):
        """开始执行"""
        if not self.validate_json():
            return
        
        try:
            content = self.json_editor.toPlainText().strip()
            data = json.loads(content)
            self.current_data = data["data"]
            
            # 创建RPA命令对象
            self.rpa_command = RPACommand(callback=self.add_log)
            
            # 确定执行模式
            is_loop = self.loop_radio.isChecked()
            mode_text = "循环执行" if is_loop else "单次执行"
            
            # 创建工作线程
            self.worker_thread = RPAWorkerThread(self.rpa_command, self.current_data, is_loop)
            self.worker_thread.finished_signal.connect(self.on_execution_finished)
            
            # 更新UI状态
            self.start_btn.setEnabled(False)
            self.stop_btn.setEnabled(True)
            self.status_label.setText(f"🚀 {mode_text}中...")
            self.status_label.setStyleSheet("color: #E67E22; font-size: 14px; padding: 10px;")
            
            # 开始执行
            self.worker_thread.start()
            self.add_log(f"🚀 开始{mode_text}")
            
        except Exception as e:
            QMessageBox.critical(self, "执行错误", f"启动执行时出错:\n{str(e)}")
            self.add_log(f"❌ 启动执行错误: {str(e)}")
    
    def stop_execution(self):
        """停止执行"""
        self.add_log("⏹️ 正在停止执行...")
        self.status_label.setText("⏹️ 正在停止...")
        self.status_label.setStyleSheet("color: #E67E22; font-size: 14px; padding: 10px;")
        
        # 停止RPA命令
        if self.rpa_command:
            self.rpa_command.stop_execution()
            
        # 停止工作线程
        if self.worker_thread and self.worker_thread.isRunning():
            self.worker_thread.stop()
            
            # 创建定时器来检查线程是否停止
            self.stop_timer = QTimer()
            self.stop_timer.timeout.connect(self.check_thread_stopped)
            self.stop_timer.start(100)  # 每100ms检查一次
    
    def check_thread_stopped(self):
        """检查线程是否已停止"""
        if not self.worker_thread or not self.worker_thread.isRunning():
            self.stop_timer.stop()
            self.on_execution_finished()
    
    def on_execution_finished(self):
        """执行完成回调"""
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.status_label.setText("💤 就绪")
        self.status_label.setStyleSheet("color: #00D4AA; font-size: 14px; padding: 10px;")
        
        # 清理资源
        if hasattr(self, 'stop_timer'):
            self.stop_timer.stop()
        
        if self.worker_thread:
            self.worker_thread.quit()
            self.worker_thread.wait(1000)  # 等待1秒
            self.worker_thread = None
            
        self.add_log("✅ 执行已完成/停止")
    
    def add_log(self, message):
        """添加日志"""
        from datetime import datetime
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
    
    def closeEvent(self, event):
        """关闭事件"""
        if self.worker_thread and self.worker_thread.isRunning():
            reply = QMessageBox.question(
                self, "确认退出", 
                "RPA正在执行中，确定要退出吗？",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                self.stop_execution()
                # 等待线程停止
                if self.worker_thread:
                    self.worker_thread.quit()
                    self.worker_thread.wait(3000)
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

def main():
    app = QApplication(sys.argv)
    
    # 设置应用程序图标和信息
    app.setApplicationName("Electrolux PC RPA")
    app.setApplicationVersion("2.0")
    app.setOrganizationName("Electrolux")
    
    window = RPAMainWindow()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main() 