import json
import os
from PyQt5.QtWidgets import (QVBoxLayout, QWidget, QLabel, QFrame, QGroupBox, 
                             QHBoxLayout, QPushButton, QTextEdit, QRadioButton, 
                             QButtonGroup, QFileDialog, QMessageBox)
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QFont

from .recorder_widget import RecorderWidget
from .execution_widget import ExecutionWidget
from .data_source_widget import DataSourceWidget

class ControlPanel(QFrame):
    log_signal = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.setFrameStyle(QFrame.StyledPanel)
        self.setMaximumWidth(700)
        self.setMinimumWidth(500)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # 标题 - 进一步增大
        title = QLabel("🤖 RPA 控制中心")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Microsoft YaHei", 24, QFont.Bold))
        title.setStyleSheet("font-size: 24px; color: #00D4AA; margin: 15px; padding: 15px;")
        layout.addWidget(title)
        
        # 录制功能组件
        self.recorder_widget = RecorderWidget()
        self.recorder_widget.log_signal.connect(self.log_signal)
        layout.addWidget(self.recorder_widget)
        
        # 数据源配置组件
        self.data_source_widget = DataSourceWidget()
        self.data_source_widget.log_signal.connect(self.log_signal)
        layout.addWidget(self.data_source_widget)
        
        # 执行控制组件
        self.execution_widget = ExecutionWidget()
        self.execution_widget.log_signal.connect(self.log_signal)
        layout.addWidget(self.execution_widget)
        
        # 连接数据源和执行组件 - 在加载默认数据之前建立连接
        self.data_source_widget.data_changed.connect(self.execution_widget.set_data)
        
        # 使用定时器延迟初始化默认数据，确保所有信号连接都已建立
        self.init_timer = QTimer()
        self.init_timer.setSingleShot(True)
        self.init_timer.timeout.connect(self.data_source_widget.initialize_default_data)
        self.init_timer.start(100)  # 100ms延迟
        
        layout.addStretch()
    
    def cleanup(self):
        """清理资源"""
        # 停止初始化定时器
        if hasattr(self, 'init_timer'):
            self.init_timer.stop()
        
        self.recorder_widget.cleanup()
        self.execution_widget.cleanup() 