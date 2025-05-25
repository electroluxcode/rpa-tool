import json
import os
from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QLabel, QGroupBox, 
                             QPushButton, QTextEdit, QFileDialog, QMessageBox)
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFont

class DataSourceWidget(QGroupBox):
    log_signal = pyqtSignal(str)
    data_changed = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__("📁 数据源配置")
        self.setFont(QFont("Microsoft YaHei", 12, QFont.Bold))
        self.init_ui()
        self.load_default_data()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # 文件操作按钮
        file_layout = QHBoxLayout()
        
        upload_btn = QPushButton("📂 上传JSON")
        upload_btn.clicked.connect(self.upload_json)
        upload_btn.setMinimumHeight(40)
        upload_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498DB;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                font-size: 13px;
                padding: 8px 12px;
            }
            QPushButton:hover {
                background-color: #2980B9;
            }
        """)
        
        validate_btn = QPushButton("✅ 验证格式")
        validate_btn.clicked.connect(self.validate_json)
        validate_btn.setMinimumHeight(40)
        validate_btn.setStyleSheet("""
            QPushButton {
                background-color: #27AE60;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                font-size: 13px;
                padding: 8px 12px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        
        file_layout.addWidget(upload_btn)
        file_layout.addWidget(validate_btn)
        layout.addLayout(file_layout)
        
        # JSON编辑器
        editor_label = QLabel("📝 JSON 编辑器:")
        editor_label.setFont(QFont("Microsoft YaHei", 11, QFont.Bold))
        layout.addWidget(editor_label)
        
        self.json_editor = QTextEdit()
        self.json_editor.setMinimumHeight(200)
        self.json_editor.setMaximumHeight(300)
        self.json_editor.setStyleSheet("""
            QTextEdit {
                background-color: #1E1E1E;
                color: #D4D4D4;
                border: 2px solid #444;
                border-radius: 8px;
                padding: 12px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 13px;
                line-height: 1.5;
            }
            QTextEdit:focus {
                border-color: #00D4AA;
            }
        """)
        self.json_editor.textChanged.connect(self.on_json_changed)
        layout.addWidget(self.json_editor)
    
    def load_default_data(self):
        """加载默认数据"""
        default_json = {
            "data": [
                {
                    "cmdType": "Click",
                    "cmdParam": {
                        "x": 100,
                        "y": 100,
                        "clicks": 1,
                        "button": "left"
                    }
                }
            ]
        }
        
        # 尝试加载现有的配置文件
        try:
            if os.path.exists('pcRPAResouece.json'):
                with open('pcRPAResouece.json', encoding='UTF-8') as f:
                    default_json = json.load(f)
        except:
            pass
        
        self.load_json_data(default_json)
    
    def upload_json(self):
        """上传JSON文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择JSON文件", "", "JSON Files (*.json);;All Files (*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                self.load_json_data(data)
                self.log_signal.emit(f"📁 已加载文件: {os.path.basename(file_path)}")
                
            except json.JSONDecodeError as e:
                QMessageBox.critical(self, "文件格式错误", f"JSON格式不正确:\n{str(e)}")
                self.log_signal.emit(f"❌ JSON格式错误: {str(e)}")
            except Exception as e:
                QMessageBox.critical(self, "文件读取错误", f"读取文件时出错:\n{str(e)}")
                self.log_signal.emit(f"❌ 文件读取错误: {str(e)}")
    
    def load_json_data(self, data):
        """加载JSON数据到编辑器"""
        formatted_json = json.dumps(data, ensure_ascii=False, indent=2)
        self.json_editor.setPlainText(formatted_json)
    
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
            self.log_signal.emit("✅ JSON格式验证通过")
            return True
            
        except json.JSONDecodeError as e:
            QMessageBox.warning(self, "JSON 格式错误", f"格式不正确:\n{str(e)}")
            self.log_signal.emit(f"❌ JSON格式错误: {str(e)}")
            return False
    
    def on_json_changed(self):
        """JSON内容改变时触发"""
        try:
            content = self.json_editor.toPlainText().strip()
            if content:
                data = json.loads(content)
                self.data_changed.emit(data)
        except:
            pass  # 忽略格式错误，用户可能正在编辑
    
    def get_current_data(self):
        """获取当前JSON数据"""
        try:
            content = self.json_editor.toPlainText().strip()
            return json.loads(content) if content else None
        except:
            return None 