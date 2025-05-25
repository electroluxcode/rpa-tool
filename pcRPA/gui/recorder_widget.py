import json
import time
from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QLabel, QGroupBox, 
                             QPushButton, QFileDialog, QMessageBox)
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont

from rpa_recorder import RPARecorder
from .message_utils import show_info_message, show_warning_message, show_error_message, show_question_message

class RecorderWidget(QGroupBox):
    log_signal = pyqtSignal(str)
    
    def __init__(self):
        super().__init__("🎬 操作录制")
        self.setFont(QFont("Microsoft YaHei", 14, QFont.Bold))
        self.recorder = None
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # 录制说明 - 进一步增大字体
        record_info = QLabel("💡 提示:\n• 按 F9 键停止录制\n• 按住鼠标拖拽超过10像素会录制为DragTo\n• 短距离移动会录制为Click")
        record_info.setStyleSheet("padding:0px 5px 15px 5px; font-size: 14px; line-height: 1;")
        record_info.setWordWrap(True)
        layout.addWidget(record_info)
        
        # 录制控制按钮
        record_control_layout = QHBoxLayout()
        
        self.start_record_btn = QPushButton("开始录制")
        self.start_record_btn.clicked.connect(self.start_recording)
        self.start_record_btn.setMinimumHeight(50)
        self.start_record_btn.setStyleSheet("""
            QPushButton {
                background-color: #E74C3C;
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 16px;
                padding: 12px 18px;
            }
            QPushButton:hover {
                background-color: #C0392B;
            }
            QPushButton:disabled {
                background-color: #555;
                color: #888;
            }
        """)
        
        self.stop_record_btn = QPushButton("停止录制")
        self.stop_record_btn.clicked.connect(self.stop_recording)
        self.stop_record_btn.setEnabled(False)
        self.stop_record_btn.setMinimumHeight(50)
        self.stop_record_btn.setStyleSheet("""
            QPushButton {
                background-color: #95A5A6;
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 16px;
                padding: 12px 18px;
            }
            QPushButton:hover {
                background-color: #7F8C8D;
            }
            QPushButton:disabled {
                background-color: #555;
                color: #888;
            }
        """)
        
        record_control_layout.addWidget(self.start_record_btn)
        record_control_layout.addWidget(self.stop_record_btn)
        layout.addLayout(record_control_layout)
        
        # 录制状态 - 进一步增大字体
        self.record_status = QLabel("⭕ 未录制")
        self.record_status.setAlignment(Qt.AlignCenter)
        self.record_status.setStyleSheet("color: #888; font-size: 16px; padding: 10px; font-weight: bold;")
        layout.addWidget(self.record_status)
    
    def start_recording(self):
        """开始录制"""
        try:
            self.recorder = RPARecorder(callback=self.log_signal.emit)
            
            if self.recorder.start_recording():
                self.start_record_btn.setEnabled(False)
                self.stop_record_btn.setEnabled(True)
                self.record_status.setText("🔴 录制中...")
                self.record_status.setStyleSheet("color: #E74C3C; font-size: 16px; padding: 10px; font-weight: bold;")
                self.log_signal.emit("🎬 开始录制操作")
            else:
                show_warning_message(self, "录制失败", "无法开始录制，请检查权限设置")
                
        except Exception as e:
            show_error_message(self, "录制错误", f"启动录制时出错:\n{str(e)}")
            self.log_signal.emit(f"❌ 录制启动错误: {str(e)}")
    
    def stop_recording(self):
        """停止录制"""
        if not self.recorder:
            return
            
        try:
            recorded_actions = self.recorder.stop_recording()
            
            self.start_record_btn.setEnabled(True)
            self.stop_record_btn.setEnabled(False)
            self.record_status.setText("⭕ 未录制")
            self.record_status.setStyleSheet("color: #888; font-size: 16px; padding: 10px; font-weight: bold;")
            
            if recorded_actions:
                # 询问是否保存
                reply = show_question_message(
                    self, "保存录制", 
                    f"录制完成，共 {len(recorded_actions)} 个操作。\n是否保存录制结果？"
                )
                
                if reply == QMessageBox.Yes:
                    self.save_recording()
            else:
                self.log_signal.emit("⚠️ 没有录制到任何操作")
                
        except Exception as e:
            show_error_message(self, "停止录制错误", f"停止录制时出错:\n{str(e)}")
            self.log_signal.emit(f"❌ 停止录制错误: {str(e)}")
    
    def save_recording(self):
        """保存录制结果"""
        if not self.recorder:
            return
            
        # 生成默认文件名
        timestamp = int(time.time())
        default_filename = f"recorded_actions_{timestamp}.json"
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, "保存录制结果", default_filename, 
            "JSON Files (*.json);;All Files (*)"
        )
        
        if file_path:
            if self.recorder.save_to_file(file_path):
                show_info_message(self, "保存成功", f"录制结果已保存到:\n{file_path}")
                
                # 询问是否加载到编辑器
                reply = show_question_message(
                    self, "加载到编辑器", 
                    "是否将录制结果加载到JSON编辑器中？"
                )
                
                if reply == QMessageBox.Yes:
                    self.load_recorded_data(file_path)
            else:
                show_error_message(self, "保存失败", "保存录制结果时出错")
    
    def load_recorded_data(self, file_path):
        """加载录制数据到编辑器"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 发送信号给数据源组件
            self.parent().data_source_widget.load_json_data(data)
            self.log_signal.emit(f"📁 录制数据已加载到编辑器")
            
        except Exception as e:
            self.log_signal.emit(f"❌ 加载录制数据错误: {str(e)}")
    
    def cleanup(self):
        """清理资源"""
        if self.recorder and self.recorder.is_recording:
            self.recorder.stop_recording() 