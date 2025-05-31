import json
import os
from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QLabel, QGroupBox, 
                             QPushButton, QTextEdit, QFileDialog, QMessageBox,
                             QTabWidget, QWidget, QTableWidget, QTableWidgetItem,
                             QHeaderView, QSplitter, QFrame)
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont

# 导入Excel解析器
try:
    from ..excel_parser import excel_parser
except ImportError:
    try:
        import sys
        sys.path.append(os.path.dirname(os.path.dirname(__file__)))
        from excel_parser import excel_parser
    except ImportError:
        excel_parser = None

class DataSourceWidget(QGroupBox):
    log_signal = pyqtSignal(str)
    data_changed = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__("📁 数据源配置")
        self.setFont(QFont("Microsoft YaHei", 12, QFont.Bold))
        self.current_data = None
        self.init_ui()
        # 将默认数据加载移到最后，确保所有UI元素都已初始化
        # 注意：实际的data_changed信号触发需要在父控件连接后进行
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # 创建标签页
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 2px solid #444;
                border-radius: 8px;
                background-color: #2B2B2B;
            }
            QTabWidget::tab-bar {
                alignment: center;
            }
            QTabBar::tab {
                background-color: #3C3C3C;
                color: white;
                padding: 12px 20px;
                margin-right: 2px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                font-weight: bold;
                font-size: 13px;
            }
            QTabBar::tab:selected {
                background-color: #00D4AA;
                color: #1E1E1E;
            }
            QTabBar::tab:hover {
                background-color: #4A4A4A;
            }
        """)
        
        # JSON标签页
        self.json_tab = self.create_json_tab()
        self.tab_widget.addTab(self.json_tab, "📝 JSON编辑器")
        
        # Excel标签页
        self.excel_tab = self.create_excel_tab()
        self.tab_widget.addTab(self.excel_tab, "📊 Excel管理")
        
        # 预览标签页
        self.preview_tab = self.create_preview_tab()
        self.tab_widget.addTab(self.preview_tab, "👁️ 数据预览")
        
        layout.addWidget(self.tab_widget)
        
        # 标签页切换事件
        self.tab_widget.currentChanged.connect(self.on_tab_changed)
    
    def create_json_tab(self):
        """创建JSON编辑标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # JSON操作按钮
        json_buttons_layout = QHBoxLayout()
        
        upload_json_btn = QPushButton("📂 上传JSON文件")
        upload_json_btn.clicked.connect(self.upload_json)
        upload_json_btn.setMinimumHeight(40)
        upload_json_btn.setStyleSheet(self.get_button_style("#3498DB", "#2980B9"))
        
        validate_json_btn = QPushButton("✅ 验证JSON格式")
        validate_json_btn.clicked.connect(self.validate_json)
        validate_json_btn.setMinimumHeight(40)
        validate_json_btn.setStyleSheet(self.get_button_style("#27AE60", "#229954"))
        
        export_json_btn = QPushButton("💾 导出JSON文件")
        export_json_btn.clicked.connect(self.export_json)
        export_json_btn.setMinimumHeight(40)
        export_json_btn.setStyleSheet(self.get_button_style("#34495E", "#2C3E50"))
        
        json_buttons_layout.addWidget(upload_json_btn)
        json_buttons_layout.addWidget(validate_json_btn)
        json_buttons_layout.addWidget(export_json_btn)
        layout.addLayout(json_buttons_layout)
        
        # JSON编辑器
        editor_label = QLabel("📝 JSON 编辑器:")
        editor_label.setFont(QFont("Microsoft YaHei", 11, QFont.Bold))
        editor_label.setStyleSheet("color: white; margin-top: 10px;")
        layout.addWidget(editor_label)
        
        self.json_editor = QTextEdit()
        self.json_editor.setMinimumHeight(300)
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
        
        return tab
    
    def create_excel_tab(self):
        """创建Excel管理标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Excel操作按钮
        excel_buttons_layout = QHBoxLayout()
        
        upload_excel_btn = QPushButton("📊 上传Excel文件")
        upload_excel_btn.clicked.connect(self.upload_excel)
        upload_excel_btn.setMinimumHeight(40)
        upload_excel_btn.setStyleSheet(self.get_button_style("#E67E22", "#D35400"))
        
        download_template_btn = QPushButton("📥 下载Excel模板")
        download_template_btn.clicked.connect(self.download_excel_template)
        download_template_btn.setMinimumHeight(40)
        download_template_btn.setStyleSheet(self.get_button_style("#9B59B6", "#8E44AD"))
        
        excel_buttons_layout.addWidget(upload_excel_btn)
        excel_buttons_layout.addWidget(download_template_btn)
        excel_buttons_layout.addStretch()
        layout.addLayout(excel_buttons_layout)
        
        # Excel功能说明
        info_frame = QFrame()
        info_frame.setStyleSheet("""
            QFrame {
                background-color: #3C3C3C;
                border: 1px solid #555;
                border-radius: 8px;
                padding: 15px;
                margin: 10px 0;
            }
        """)
        info_layout = QVBoxLayout(info_frame)
        
        info_title = QLabel("📊 Excel功能说明")
        info_title.setFont(QFont("Microsoft YaHei", 12, QFont.Bold))
        info_title.setStyleSheet("color: #00D4AA; margin-bottom: 10px;")
        info_layout.addWidget(info_title)
        
        info_text = QLabel("""
• 支持 .xlsx 和 .xls 格式的Excel文件
• Excel文件必须包含 'cmdType' 和 'cmdParam' 列
• 可以下载模板文件作为参考
• 上传后会自动转换为JSON格式
• 支持所有RPA命令类型，包括OCR功能
        """)
        info_text.setStyleSheet("color: #CCCCCC; line-height: 1.6;")
        info_text.setWordWrap(True)
        info_layout.addWidget(info_text)
        
        layout.addWidget(info_frame)
        
        # Excel状态信息
        self.excel_status_label = QLabel("📋 状态: 等待上传Excel文件")
        self.excel_status_label.setStyleSheet("""
            QLabel {
                background-color: #2C3E50;
                color: white;
                padding: 10px;
                border-radius: 6px;
                font-weight: bold;
            }
        """)
        layout.addWidget(self.excel_status_label)
        
        layout.addStretch()
        return tab
    
    def create_preview_tab(self):
        """创建数据预览标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 预览标题
        preview_title = QLabel("👁️ 当前数据预览")
        preview_title.setFont(QFont("Microsoft YaHei", 12, QFont.Bold))
        preview_title.setStyleSheet("color: #00D4AA; margin-bottom: 10px;")
        layout.addWidget(preview_title)
        
        # 数据统计
        self.stats_label = QLabel("📊 统计信息: 0 个命令")
        self.stats_label.setStyleSheet("""
            QLabel {
                background-color: #3C3C3C;
                color: white;
                padding: 8px 12px;
                border-radius: 6px;
                font-weight: bold;
                margin-bottom: 10px;
            }
        """)
        layout.addWidget(self.stats_label)
        
        # 数据表格
        self.preview_table = QTableWidget()
        self.preview_table.setColumnCount(3)
        self.preview_table.setHorizontalHeaderLabels(["序号", "命令类型", "参数预览"])
        
        # 设置表格样式
        self.preview_table.setStyleSheet("""
            QTableWidget {
                background-color: #2B2B2B;
                color: white;
                border: 1px solid #444;
                border-radius: 8px;
                gridline-color: #444;
                font-size: 12px;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #444;
            }
            QTableWidget::item:selected {
                background-color: #00D4AA;
                color: #1E1E1E;
            }
            QHeaderView::section {
                background-color: #3C3C3C;
                color: white;
                padding: 10px;
                border: none;
                font-weight: bold;
            }
        """)
        
        # 设置列宽
        header = self.preview_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Fixed)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        self.preview_table.setColumnWidth(0, 60)
        
        layout.addWidget(self.preview_table)
        
        return tab
    
    def get_button_style(self, bg_color, hover_color):
        """获取按钮样式"""
        return f"""
            QPushButton {{
                background-color: {bg_color};
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                font-size: 13px;
                padding: 8px 12px;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
            QPushButton:pressed {{
                background-color: {hover_color};
            }}
        """
    
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
                    existing_data = json.load(f)
                    # 只有当文件存在且有有效数据时才使用，否则使用默认的简单Click命令
                    if existing_data and "data" in existing_data and existing_data["data"]:
                        default_json = existing_data
        except:
            # 如果读取配置文件失败，使用默认的简单Click命令
            pass
        
        self.load_json_data(default_json)
    
    def on_tab_changed(self, index):
        """标签页切换事件"""
        if index == 2:  # 预览标签页
            self.update_preview_table()
    
    def update_preview_table(self):
        """更新预览表格"""
        if not self.current_data or "data" not in self.current_data:
            self.preview_table.setRowCount(0)
            self.stats_label.setText("📊 统计信息: 0 个命令")
            return
        
        commands = self.current_data["data"]
        self.preview_table.setRowCount(len(commands))
        
        for i, cmd in enumerate(commands):
            # 序号
            self.preview_table.setItem(i, 0, QTableWidgetItem(str(i + 1)))
            
            # 命令类型
            cmd_type = cmd.get("cmdType", "Unknown")
            self.preview_table.setItem(i, 1, QTableWidgetItem(cmd_type))
            
            # 参数预览
            cmd_param = cmd.get("cmdParam", {})
            if isinstance(cmd_param, dict):
                param_preview = ", ".join([f"{k}:{v}" for k, v in list(cmd_param.items())[:3]])
                if len(cmd_param) > 3:
                    param_preview += "..."
            else:
                param_preview = str(cmd_param)[:50]
                if len(str(cmd_param)) > 50:
                    param_preview += "..."
            
            self.preview_table.setItem(i, 2, QTableWidgetItem(param_preview))
        
        # 更新统计信息
        cmd_types = {}
        for cmd in commands:
            cmd_type = cmd.get("cmdType", "Unknown")
            cmd_types[cmd_type] = cmd_types.get(cmd_type, 0) + 1
        
        stats_text = f"📊 统计信息: {len(commands)} 个命令"
        if cmd_types:
            top_types = sorted(cmd_types.items(), key=lambda x: x[1], reverse=True)[:3]
            type_summary = ", ".join([f"{t}({c})" for t, c in top_types])
            stats_text += f" | 主要类型: {type_summary}"
        
        self.stats_label.setText(stats_text)
    
    def update_excel_status(self, message, is_success=True):
        """更新Excel状态"""
        color = "#27AE60" if is_success else "#E74C3C"
        self.excel_status_label.setText(f"📋 状态: {message}")
        self.excel_status_label.setStyleSheet(f"""
            QLabel {{
                background-color: {color};
                color: white;
                padding: 10px;
                border-radius: 6px;
                font-weight: bold;
            }}
        """)
    
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
                self.log_signal.emit(f"📁 已加载JSON文件: {os.path.basename(file_path)}")
                
            except json.JSONDecodeError as e:
                QMessageBox.critical(self, "文件格式错误", f"JSON格式不正确:\n{str(e)}")
                self.log_signal.emit(f"❌ JSON格式错误: {str(e)}")
            except Exception as e:
                QMessageBox.critical(self, "文件读取错误", f"读取文件时出错:\n{str(e)}")
                self.log_signal.emit(f"❌ 文件读取错误: {str(e)}")
    
    def upload_excel(self):
        """上传Excel文件"""
        if not excel_parser:
            QMessageBox.warning(self, "功能不可用", "Excel解析模块不可用，请安装pandas和openpyxl")
            self.log_signal.emit("❌ Excel功能不可用：缺少依赖模块")
            self.update_excel_status("Excel功能不可用：缺少依赖模块", False)
            return
        
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择Excel文件", "", "Excel Files (*.xlsx *.xls);;All Files (*)"
        )
        
        if file_path:
            try:
                self.update_excel_status("正在验证Excel文件格式...")
                
                # 验证Excel文件格式
                is_valid, message = excel_parser.validate_excel_format(file_path)
                if not is_valid:
                    QMessageBox.warning(self, "Excel格式错误", f"文件格式不正确:\n{message}")
                    self.log_signal.emit(f"❌ Excel格式错误: {message}")
                    self.update_excel_status(f"格式错误: {message}", False)
                    return
                
                # 转换Excel为JSON
                self.update_excel_status("正在转换Excel文件...")
                self.log_signal.emit("📊 正在转换Excel文件...")
                json_data = excel_parser.excel_to_json(file_path)
                
                if json_data:
                    self.load_json_data(json_data)
                    self.log_signal.emit(f"📊 已加载Excel文件: {os.path.basename(file_path)}")
                    self.log_signal.emit(f"✅ 成功转换 {len(json_data['data'])} 个命令")
                    
                    # 更新Excel状态
                    self.update_excel_status(f"成功加载 {len(json_data['data'])} 个命令")
                    
                    # 自动切换到JSON编辑器标签页显示结果
                    self.tab_widget.setCurrentIndex(0)
                    
                    # 显示转换成功信息
                    QMessageBox.information(
                        self, 
                        "转换成功", 
                        f"Excel文件已成功转换为JSON格式\n"
                        f"文件: {os.path.basename(file_path)}\n"
                        f"命令数量: {len(json_data['data'])}\n\n"
                        f"已自动切换到JSON编辑器查看结果"
                    )
                else:
                    QMessageBox.critical(self, "转换失败", "Excel文件转换失败")
                    self.log_signal.emit("❌ Excel文件转换失败")
                    self.update_excel_status("Excel文件转换失败", False)
                    
            except Exception as e:
                QMessageBox.critical(self, "文件处理错误", f"处理Excel文件时出错:\n{str(e)}")
                self.log_signal.emit(f"❌ Excel文件处理错误: {str(e)}")
                self.update_excel_status(f"处理错误: {str(e)}", False)
    
    def download_excel_template(self):
        """下载Excel模板"""
        if not excel_parser:
            QMessageBox.warning(self, "功能不可用", "Excel解析模块不可用，请安装pandas和openpyxl")
            self.log_signal.emit("❌ Excel功能不可用：缺少依赖模块")
            return
        
        # 选择保存位置
        file_path, _ = QFileDialog.getSaveFileName(
            self, 
            "保存Excel模板", 
            "rpa_template.xlsx", 
            "Excel Files (*.xlsx);;All Files (*)"
        )
        
        if file_path:
            try:
                result = excel_parser.create_excel_template(file_path)
                if result:
                    QMessageBox.information(
                        self, 
                        "模板创建成功", 
                        f"Excel模板已创建:\n{file_path}\n\n"
                        f"模板包含了所有支持的命令类型和示例参数，"
                        f"您可以参考模板格式来创建自己的RPA命令。"
                    )
                    self.log_signal.emit(f"📥 Excel模板已创建: {os.path.basename(file_path)}")
                else:
                    QMessageBox.critical(self, "创建失败", "Excel模板创建失败")
                    self.log_signal.emit("❌ Excel模板创建失败")
                    
            except Exception as e:
                QMessageBox.critical(self, "创建错误", f"创建Excel模板时出错:\n{str(e)}")
                self.log_signal.emit(f"❌ Excel模板创建错误: {str(e)}")
    
    def export_json(self):
        """导出JSON文件"""
        current_data = self.get_current_data()
        if not current_data:
            QMessageBox.warning(self, "导出失败", "当前没有有效的JSON数据")
            return
        
        # 选择保存位置
        file_path, _ = QFileDialog.getSaveFileName(
            self, 
            "导出JSON文件", 
            "rpa_commands.json", 
            "JSON Files (*.json);;All Files (*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(current_data, f, ensure_ascii=False, indent=2)
                
                QMessageBox.information(self, "导出成功", f"JSON文件已导出:\n{file_path}")
                self.log_signal.emit(f"💾 JSON文件已导出: {os.path.basename(file_path)}")
                
            except Exception as e:
                QMessageBox.critical(self, "导出错误", f"导出JSON文件时出错:\n{str(e)}")
                self.log_signal.emit(f"❌ JSON导出错误: {str(e)}")
    
    def load_json_data(self, data):
        """加载JSON数据到编辑器"""
        self.current_data = data
        formatted_json = json.dumps(data, ensure_ascii=False, indent=2)
        self.json_editor.setPlainText(formatted_json)
        
        # 触发数据变更信号，确保执行组件能接收到数据
        self.data_changed.emit(data)
        
        # 更新预览表格（如果当前在预览标签页）
        if self.tab_widget.currentIndex() == 2:
            self.update_preview_table()
    
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
            
            # 更新当前数据
            self.current_data = data
            
            QMessageBox.information(self, "验证成功", "✅ JSON格式正确!")
            self.log_signal.emit("✅ JSON格式验证通过")
            
            # 更新预览表格
            if self.tab_widget.currentIndex() == 2:
                self.update_preview_table()
            
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
                self.current_data = data
                self.data_changed.emit(data)
                
                # 如果当前在预览标签页，更新预览
                if self.tab_widget.currentIndex() == 2:
                    self.update_preview_table()
        except:
            pass  # 忽略格式错误，用户可能正在编辑
    
    def get_current_data(self):
        """获取当前JSON数据"""
        return self.current_data 

    def initialize_default_data(self):
        """初始化默认数据 - 由父控件在建立连接后调用"""
        self.load_default_data() 