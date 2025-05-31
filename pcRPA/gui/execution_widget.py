import json
from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QLabel, QGroupBox, 
                             QPushButton, QRadioButton, QButtonGroup, QMessageBox)
from PyQt5.QtCore import QThread, pyqtSignal, QTimer, Qt
from PyQt5.QtGui import QFont

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

class ExecutionWidget(QGroupBox):
    log_signal = pyqtSignal(str)
    
    def __init__(self):
        super().__init__("⚙️ 执行控制")
        self.setFont(QFont("Microsoft YaHei", 12, QFont.Bold))
        self.current_data = None
        self.rpa_command = None
        self.worker_thread = None
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # 执行模式选择
        mode_label = QLabel("🎯 执行模式:")
        mode_label.setFont(QFont("Microsoft YaHei", 11, QFont.Bold))
        layout.addWidget(mode_label)
        
        mode_layout = QHBoxLayout()
        self.mode_group = QButtonGroup()
        
        self.once_radio = QRadioButton("单次执行")
        self.once_radio.setChecked(True)
        self.once_radio.setStyleSheet("color: #D4D4D4; font-size: 13px;")
        
        self.loop_radio = QRadioButton("循环执行")
        self.loop_radio.setStyleSheet("color: #D4D4D4; font-size: 13px;")
        
        self.mode_group.addButton(self.once_radio)
        self.mode_group.addButton(self.loop_radio)
        
        mode_layout.addWidget(self.once_radio)
        mode_layout.addWidget(self.loop_radio)
        layout.addLayout(mode_layout)
        
        # 执行控制按钮
        control_layout = QHBoxLayout()
        
        self.start_btn = QPushButton("🚀 开始执行")
        self.start_btn.clicked.connect(self.start_execution)
        self.start_btn.setMinimumHeight(50)
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #27AE60;
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
                padding: 12px 16px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
            QPushButton:disabled {
                background-color: #555;
                color: #888;
            }
        """)
        
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
                font-size: 14px;
                padding: 12px 16px;
            }
            QPushButton:hover {
                background-color: #C0392B;
            }
            QPushButton:disabled {
                background-color: #555;
                color: #888;
            }
        """)
        
        control_layout.addWidget(self.start_btn)
        control_layout.addWidget(self.stop_btn)
        layout.addLayout(control_layout)
        
        # 状态显示
        self.status_label = QLabel("💤 就绪")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: #00D4AA; font-size: 16px; padding: 12px; font-weight: bold;")
        layout.addWidget(self.status_label)
    
    def set_data(self, data):
        """设置执行数据"""
        self.current_data = data
        # 添加日志确认数据接收
        if data and "data" in data:
            cmd_count = len(data["data"])
            self.log_signal.emit(f"📊 已接收执行数据: {cmd_count} 个命令")
        else:
            self.log_signal.emit("❌ 接收到无效的执行数据")
    
    def start_execution(self):
        """开始执行"""
        if not self.current_data:
            QMessageBox.warning(self, "执行错误", "没有设置执行数据，请先加载或编辑JSON数据")
            self.log_signal.emit("❌ 没有设置执行数据")
            return
            
        if "data" not in self.current_data:
            QMessageBox.warning(self, "执行错误", "执行数据格式错误，缺少'data'字段")
            self.log_signal.emit("❌ 执行数据格式错误，缺少'data'字段")
            return
        
        if not self.current_data["data"]:
            QMessageBox.warning(self, "执行错误", "执行数据为空，没有可执行的命令")
            self.log_signal.emit("❌ 执行数据为空")
            return
        
        try:
            # 创建RPA命令对象
            self.rpa_command = RPACommand(callback=self.log_signal.emit)
            
            # 确定执行模式
            is_loop = self.loop_radio.isChecked()
            mode_text = "循环执行" if is_loop else "单次执行"
            
            # 输出执行信息
            cmd_count = len(self.current_data["data"])
            self.log_signal.emit(f"🚀 准备执行 {cmd_count} 个命令 ({mode_text})")
            
            # 创建工作线程
            self.worker_thread = RPAWorkerThread(
                self.rpa_command, 
                self.current_data["data"], 
                is_loop
            )
            self.worker_thread.finished_signal.connect(self.on_execution_finished)
            
            # 更新UI状态
            self.start_btn.setEnabled(False)
            self.stop_btn.setEnabled(True)
            self.status_label.setText(f"🚀 {mode_text}中...")
            self.status_label.setStyleSheet("color: #E67E22; font-size: 16px; padding: 12px; font-weight: bold;")
            
            # 开始执行
            self.worker_thread.start()
            self.log_signal.emit(f"🚀 开始{mode_text}")
            
        except Exception as e:
            QMessageBox.critical(self, "执行错误", f"启动执行时出错:\n{str(e)}")
            self.log_signal.emit(f"❌ 启动执行错误: {str(e)}")
    
    def stop_execution(self):
        """停止执行"""
        self.log_signal.emit("⏹️ 正在停止执行...")
        self.status_label.setText("⏹️ 正在停止...")
        self.status_label.setStyleSheet("color: #E67E22; font-size: 16px; padding: 12px; font-weight: bold;")
        
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
        self.status_label.setStyleSheet("color: #00D4AA; font-size: 16px; padding: 12px; font-weight: bold;")
        
        # 清理资源
        if hasattr(self, 'stop_timer'):
            self.stop_timer.stop()
        
        if self.worker_thread:
            self.worker_thread.quit()
            self.worker_thread.wait(1000)  # 等待1秒
            self.worker_thread = None
            
        self.log_signal.emit("✅ 执行已完成/停止")
    
    def cleanup(self):
        """清理资源"""
        if self.worker_thread and self.worker_thread.isRunning():
            self.stop_execution() 