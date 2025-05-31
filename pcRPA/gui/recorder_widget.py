import json
import time
from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QLabel, QGroupBox, 
                             QPushButton, QFileDialog, QMessageBox, QDialog)
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
        
        # 询问保存格式
        format_choice = self.ask_save_format()
        if not format_choice:
            return
        
        # 生成默认文件名（不含扩展名）
        timestamp = int(time.time())
        default_filename = f"recorded_actions_{timestamp}"
        
        # 根据格式选择文件对话框
        if format_choice == "json":
            file_path, _ = QFileDialog.getSaveFileName(
                self, "保存录制结果 (JSON格式)", f"{default_filename}.json", 
                "JSON Files (*.json);;All Files (*)"
            )
            if file_path:
                self.save_single_format(file_path, "json")
                
        elif format_choice == "excel":
            file_path, _ = QFileDialog.getSaveFileName(
                self, "保存录制结果 (Excel格式)", f"{default_filename}.xlsx", 
                "Excel Files (*.xlsx);;All Files (*)"
            )
            if file_path:
                self.save_single_format(file_path, "excel")
                
        elif format_choice == "both":
            # 选择基础路径
            file_path, _ = QFileDialog.getSaveFileName(
                self, "保存录制结果 (选择基础文件名)", f"{default_filename}.json", 
                "JSON Files (*.json);;All Files (*)"
            )
            if file_path:
                # 移除扩展名作为基础路径
                base_path = file_path.rsplit('.', 1)[0] if '.' in file_path else file_path
                self.save_both_formats(base_path)
    
    def ask_save_format(self):
        """询问保存格式"""
        from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QRadioButton, QPushButton, QLabel, QButtonGroup
        
        dialog = QDialog(self)
        dialog.setWindowTitle("选择保存格式")
        dialog.setFixedSize(400, 250)
        dialog.setStyleSheet("""
            QDialog {
                background-color: #2B2B2B;
                color: white;
            }
            QLabel {
                color: white;
                font-size: 14px;
                font-weight: bold;
                margin-bottom: 15px;
            }
            QRadioButton {
                color: white;
                font-size: 13px;
                padding: 8px;
                margin: 5px 0;
            }
            QRadioButton::indicator {
                width: 18px;
                height: 18px;
            }
            QRadioButton::indicator:unchecked {
                border: 2px solid #555;
                border-radius: 9px;
                background-color: #2B2B2B;
            }
            QRadioButton::indicator:checked {
                border: 2px solid #00D4AA;
                border-radius: 9px;
                background-color: #00D4AA;
            }
            QPushButton {
                background-color: #3498DB;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                font-size: 13px;
                padding: 10px 20px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #2980B9;
            }
            QPushButton:pressed {
                background-color: #21618C;
            }
        """)
        
        layout = QVBoxLayout(dialog)
        
        # 标题
        title_label = QLabel("📁 选择录制结果的保存格式:")
        layout.addWidget(title_label)
        
        # 单选按钮组
        button_group = QButtonGroup(dialog)
        
        json_radio = QRadioButton("📝 JSON格式 (.json)")
        json_radio.setToolTip("标准JSON格式，可直接用于RPA执行")
        
        excel_radio = QRadioButton("📊 Excel格式 (.xlsx)")
        excel_radio.setToolTip("Excel表格格式，便于查看和编辑")
        
        both_radio = QRadioButton("📋 同时保存两种格式")
        both_radio.setToolTip("同时生成JSON和Excel两个文件")
        both_radio.setChecked(True)  # 默认选择
        
        button_group.addButton(json_radio)
        button_group.addButton(excel_radio)
        button_group.addButton(both_radio)
        
        layout.addWidget(json_radio)
        layout.addWidget(excel_radio)
        layout.addWidget(both_radio)
        
        # 按钮
        button_layout = QHBoxLayout()
        
        ok_button = QPushButton("确定")
        cancel_button = QPushButton("取消")
        
        ok_button.clicked.connect(dialog.accept)
        cancel_button.clicked.connect(dialog.reject)
        
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)
        
        # 显示对话框
        if dialog.exec_() == QDialog.Accepted:
            if json_radio.isChecked():
                return "json"
            elif excel_radio.isChecked():
                return "excel"
            elif both_radio.isChecked():
                return "both"
        
        return None
    
    def save_single_format(self, file_path, format_type):
        """保存单一格式"""
        success = False
        
        if format_type == "json":
            success = self.recorder.save_to_file(file_path)
        elif format_type == "excel":
            success = self.recorder.save_to_excel(file_path)
        
        if success:
            format_name = "JSON" if format_type == "json" else "Excel"
            show_info_message(self, "保存成功", f"录制结果已保存为{format_name}格式:\n{file_path}")
            
            # 询问是否加载到编辑器（仅JSON格式）
            if format_type == "json":
                reply = show_question_message(
                    self, "加载到编辑器", 
                    "是否将录制结果加载到JSON编辑器中？"
                )
                
                if reply == QMessageBox.Yes:
                    self.load_recorded_data(file_path)
        else:
            show_error_message(self, "保存失败", f"保存{format_type.upper()}格式时出错")
    
    def save_both_formats(self, base_path):
        """保存两种格式"""
        results = self.recorder.save_with_format_choice(base_path, "both")
        
        success_count = sum(results.values())
        total_count = len(results)
        
        if success_count == total_count:
            show_info_message(
                self, "保存成功", 
                f"录制结果已保存为两种格式:\n"
                f"• JSON: {base_path}.json\n"
                f"• Excel: {base_path}.xlsx"
            )
            
            # 询问是否加载JSON到编辑器
            reply = show_question_message(
                self, "加载到编辑器", 
                "是否将录制结果加载到JSON编辑器中？"
            )
            
            if reply == QMessageBox.Yes:
                self.load_recorded_data(f"{base_path}.json")
                
        elif success_count > 0:
            # 部分成功
            success_formats = [fmt for fmt, success in results.items() if success]
            failed_formats = [fmt for fmt, success in results.items() if not success]
            
            show_warning_message(
                self, "部分保存成功", 
                f"成功保存: {', '.join(success_formats).upper()}\n"
                f"保存失败: {', '.join(failed_formats).upper()}"
            )
        else:
            show_error_message(self, "保存失败", "所有格式保存都失败了")
    
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