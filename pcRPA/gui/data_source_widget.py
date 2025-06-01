import json
import os
from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QLabel, QGroupBox, 
                             QPushButton, QTextEdit, QFileDialog, QMessageBox,
                             QTabWidget, QWidget, QTableWidget, QTableWidgetItem,
                             QHeaderView, QSplitter, QFrame, QScrollArea, QSizePolicy)
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
        layout.setContentsMargins(5, 10, 5, 5)  # 减少整体边距
        layout.setSpacing(5)  # 减少控件间距
        
        # 创建标签页
        self.tab_widget = QTabWidget()
        # 设置一个最小高度，增加20%的高度
        self.tab_widget.setMinimumHeight(320)  # 增加整体高度
        # 修改tab widget的sizePolicy，使其不强制同步所有页面高度
        size_policy = self.tab_widget.sizePolicy()
        size_policy.setVerticalPolicy(QSizePolicy.Preferred)
        self.tab_widget.setSizePolicy(size_policy)
        
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #444;
                border-radius: 6px;
                background-color: #2B2B2B;
            }
            QTabWidget::tab-bar {
                alignment: center;
            }
            QTabBar::tab {
                background-color: #3C3C3C;
                color: white;
                padding: 10px 16px;
                margin-right: 2px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
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
        
        # JSON标签页 - 使用QScrollArea包装，确保滚动而不影响其他标签页
        self.json_tab = QWidget()
        self.json_tab.setStyleSheet("background-color: #2B2B2B;")
        json_scroll = QScrollArea()
        json_scroll.setStyleSheet("""
            QScrollArea {
                background-color: #2B2B2B;
                border: none;
            }
            QScrollBar:vertical {
                background-color: #2B2B2B;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background-color: #555;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        json_scroll.setWidget(self.json_tab)
        json_scroll.setWidgetResizable(True)
        json_scroll.setFrameShape(QFrame.NoFrame)
        self.create_json_tab(self.json_tab)
        self.tab_widget.addTab(json_scroll, "📝 JSON管理")
        
        # Excel标签页 - 使用QScrollArea包装，确保滚动而不影响其他标签页
        self.excel_tab = QWidget()
        self.excel_tab.setStyleSheet("background-color: #2B2B2B;")
        excel_scroll = QScrollArea()
        excel_scroll.setStyleSheet("""
            QScrollArea {
                background-color: #2B2B2B;
                border: none;
            }
            QScrollBar:vertical {
                background-color: #2B2B2B;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background-color: #555;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        excel_scroll.setWidget(self.excel_tab)
        excel_scroll.setWidgetResizable(True)
        excel_scroll.setFrameShape(QFrame.NoFrame)
        self.create_excel_tab(self.excel_tab)
        self.tab_widget.addTab(excel_scroll, "📊 Excel管理")
        
        layout.addWidget(self.tab_widget)
        
        # 设置整体GroupBox的暗色主题样式
        self.setStyleSheet("""
            QGroupBox {
                background-color: #2B2B2B;
                color: white;
                border: 1px solid #444;
                border-radius: 6px;
                margin-top: 12px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 5px;
                color: #00D4AA;
            }
        """)
    
    def create_json_tab(self, tab):
        """创建JSON编辑标签页"""
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(10, 10, 10, 10)  # 设置边距更小
        layout.setSpacing(8)  # 设置控件间距更小
        layout.setAlignment(Qt.AlignTop)  # 设置顶部对齐
        
        # JSON操作按钮 - 一行显示所有按钮
        json_buttons_layout = QHBoxLayout()
        json_buttons_layout.setSpacing(8)  # 设置按钮间距
        
        upload_json_btn = QPushButton("📂 上传JSON文件")
        upload_json_btn.clicked.connect(self.upload_json)
        upload_json_btn.setMinimumHeight(36)  # 稍微减小高度
        upload_json_btn.setStyleSheet(self.get_button_style("#3498DB", "#2980B9"))
        
        validate_json_btn = QPushButton("✅ 验证JSON格式")
        validate_json_btn.clicked.connect(self.validate_json)
        validate_json_btn.setMinimumHeight(36)  # 稍微减小高度
        validate_json_btn.setStyleSheet(self.get_button_style("#27AE60", "#229954"))
        
        export_json_btn = QPushButton("💾 导出JSON文件")
        export_json_btn.clicked.connect(self.export_json)
        export_json_btn.setMinimumHeight(36)  # 稍微减小高度
        export_json_btn.setStyleSheet(self.get_button_style("#34495E", "#2C3E50"))
        
        json_buttons_layout.addWidget(upload_json_btn)
        json_buttons_layout.addWidget(validate_json_btn)
        json_buttons_layout.addWidget(export_json_btn)
        json_buttons_layout.addStretch()
        layout.addLayout(json_buttons_layout)
        
        # JSON编辑器
        editor_label = QLabel("📝 JSON 编辑器:")
        editor_label.setFont(QFont("Microsoft YaHei", 11, QFont.Bold))
        editor_label.setStyleSheet("color: white;")
        layout.addWidget(editor_label)
        
        self.json_editor = QTextEdit()
        self.json_editor.setMinimumHeight(144)  # 增加20%高度，从120增加到144
        self.json_editor.setMaximumHeight(180)  # 增加20%高度，从150增加到180
        self.json_editor.setStyleSheet("""
            QTextEdit {
                background-color: #1E1E1E;
                color: #D4D4D4;
                border: 1px solid #444;
                border-radius: 6px;
                padding: 8px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 12px;
                line-height: 1.4;
            }
            QTextEdit:focus {
                border-color: #00D4AA;
            }
        """)
        self.json_editor.textChanged.connect(self.on_json_changed)
        layout.addWidget(self.json_editor)
    
    def create_excel_tab(self, tab):
        """创建Excel管理标签页"""
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(10, 10, 10, 10)  # 设置边距更小
        layout.setSpacing(8)  # 设置控件间距更小
        layout.setAlignment(Qt.AlignTop)  # 设置顶部对齐
        
        # Excel操作按钮
        excel_buttons_layout = QHBoxLayout()
        excel_buttons_layout.setSpacing(8)  # 设置按钮间距
        
        upload_excel_btn = QPushButton("📊 上传Excel文件")
        upload_excel_btn.clicked.connect(self.upload_excel)
        upload_excel_btn.setMinimumHeight(36)  # 稍微减小高度
        upload_excel_btn.setStyleSheet(self.get_button_style("#E67E22", "#D35400"))
        
        download_template_btn = QPushButton("📥 下载Excel模板")
        download_template_btn.clicked.connect(self.download_excel_template)
        download_template_btn.setMinimumHeight(36)  # 稍微减小高度
        download_template_btn.setStyleSheet(self.get_button_style("#9B59B6", "#8E44AD"))
        
        export_to_excel_btn = QPushButton("📊 导出为Excel")
        export_to_excel_btn.clicked.connect(self.export_to_excel)
        export_to_excel_btn.setMinimumHeight(36)  # 稍微减小高度
        export_to_excel_btn.setStyleSheet(self.get_button_style("#27AE60", "#229954"))
        
        excel_buttons_layout.addWidget(upload_excel_btn)
        excel_buttons_layout.addWidget(download_template_btn)
        excel_buttons_layout.addWidget(export_to_excel_btn)
        excel_buttons_layout.addStretch()
        layout.addLayout(excel_buttons_layout)
        
        # Excel功能说明
        info_frame = QFrame()
        info_frame.setStyleSheet("""
            QFrame {
                background-color: #3C3C3C;
                border: 1px solid #555;
                border-radius: 6px;
                padding: 8px;
                margin: 5px 0;
            }
        """)
        info_layout = QVBoxLayout(info_frame)
        info_layout.setContentsMargins(8, 8, 8, 8)  # 减小内边距
        info_layout.setSpacing(3)  # 减小间距
        
        info_title = QLabel("📊 Excel功能说明")
        info_title.setFont(QFont("Microsoft YaHei", 10, QFont.Bold))
        info_title.setStyleSheet("color: #00D4AA;")
        info_layout.addWidget(info_title)
        
        info_text = QLabel("""
• 支持 .xlsx 和 .xls 格式的Excel文件
• Excel文件必须包含 'cmdType' 和 'cmdParam' 列
• 可以下载模板文件作为参考
• 上传后会自动转换为JSON格式
• 支持所有RPA命令类型，包括OCR功能
• 可以将当前JSON数据导出为Excel格式
        """)
        info_text.setStyleSheet("color: #CCCCCC; line-height: 1.3;")
        info_text.setWordWrap(True)
        info_layout.addWidget(info_text)
        
        layout.addWidget(info_frame)
        
        # Excel状态信息
        self.excel_status_label = QLabel("📋 状态: 等待上传Excel文件")
        self.excel_status_label.setStyleSheet("""
            QLabel {
                background-color: #2C3E50;
                color: white;
                padding: 6px;
                border-radius: 4px;
                font-weight: bold;
            }
        """)
        layout.addWidget(self.excel_status_label)
        
        # 在Excel标签页中添加JSON编辑器
        json_editor_label = QLabel("📝 JSON 编辑器:")
        json_editor_label.setFont(QFont("Microsoft YaHei", 11, QFont.Bold))
        json_editor_label.setStyleSheet("color: white;")
        layout.addWidget(json_editor_label)
        
        self.excel_json_editor = QTextEdit()
        self.excel_json_editor.setMinimumHeight(144)  # 增加20%高度，从120增加到144
        self.excel_json_editor.setMaximumHeight(180)  # 增加20%高度，从150增加到180
        self.excel_json_editor.setStyleSheet("""
            QTextEdit {
                background-color: #1E1E1E;
                color: #D4D4D4;
                border: 1px solid #444;
                border-radius: 6px;
                padding: 8px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 12px;
                line-height: 1.4;
            }
            QTextEdit:focus {
                border-color: #00D4AA;
            }
        """)
        self.excel_json_editor.textChanged.connect(self.on_excel_json_changed)
        layout.addWidget(self.excel_json_editor)
    
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
                    
                    # 不再自动切换到JSON编辑器标签页，留在Excel标签页
                    # self.tab_widget.setCurrentIndex(0)
                    
                    # 显示转换成功信息
                    QMessageBox.information(
                        self, 
                        "转换成功", 
                        f"Excel文件已成功转换为JSON格式\n"
                        f"文件: {os.path.basename(file_path)}\n"
                        f"命令数量: {len(json_data['data'])}\n\n"
                        f"JSON数据已在当前页面更新"
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
        try:
            data = self.get_current_data()
            if not data:
                QMessageBox.warning(self, "导出失败", "当前没有有效的JSON数据可导出")
                return
            
            file_path, _ = QFileDialog.getSaveFileName(
                self, "保存JSON文件", "", "JSON Files (*.json);;All Files (*)"
            )
            
            if not file_path:
                return
                
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                
            QMessageBox.information(
                self, "导出成功", 
                f"JSON数据已成功导出到:\n{file_path}"
            )
            self.log_signal.emit(f"✅ JSON数据已成功导出到: {file_path}")
        
        except Exception as e:
            QMessageBox.critical(self, "导出失败", f"导出JSON文件时出错:\n{str(e)}")
            self.log_signal.emit(f"❌ JSON导出失败: {str(e)}")
            
    def export_to_excel(self):
        """导出当前JSON数据为Excel文件"""
        try:
            # 检查是否有excel_parser可用
            if excel_parser is None:
                QMessageBox.critical(
                    self, "功能不可用", 
                    "导出Excel功能需要Excel解析模块，但该模块未能正确加载。"
                )
                return
            
            # 获取当前JSON数据
            data = self.get_current_data()
            if not data:
                QMessageBox.warning(self, "导出失败", "当前没有有效的JSON数据可导出")
                return
            
            # 选择保存路径
            file_path, _ = QFileDialog.getSaveFileName(
                self, "保存Excel文件", "", "Excel Files (*.xlsx);;All Files (*)"
            )
            
            if not file_path:
                return
            
            # 如果文件名没有.xlsx后缀，添加它
            if not file_path.lower().endswith('.xlsx'):
                file_path += '.xlsx'
            
            # 导出到Excel
            output_path = excel_parser.json_to_excel(data, file_path)
            
            QMessageBox.information(
                self, "导出成功", 
                f"JSON数据已成功导出为Excel文件:\n{output_path}"
            )
            self.log_signal.emit(f"✅ JSON数据已成功导出为Excel: {output_path}")
        
        except Exception as e:
            QMessageBox.critical(self, "导出失败", f"导出Excel文件时出错:\n{str(e)}")
            self.log_signal.emit(f"❌ 导出Excel失败: {str(e)}")
    
    def load_json_data(self, data):
        """加载JSON数据到编辑器"""
        self.current_data = data
        formatted_json = json.dumps(data, ensure_ascii=False, indent=2)
        
        # 更新两个编辑器
        self.json_editor.setPlainText(formatted_json)
        if hasattr(self, 'excel_json_editor'):
            self.excel_json_editor.setPlainText(formatted_json)
        
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
                
                # 同步更新Excel标签页中的JSON编辑器，避免循环触发
                if hasattr(self, 'excel_json_editor') and self.excel_json_editor.toPlainText() != content:
                    self.excel_json_editor.blockSignals(True)
                    self.excel_json_editor.setPlainText(content)
                    self.excel_json_editor.blockSignals(False)
        except:
            pass  # 忽略格式错误，用户可能正在编辑
    
    def on_excel_json_changed(self):
        """Excel标签页中的JSON内容改变时触发"""
        try:
            content = self.excel_json_editor.toPlainText().strip()
            if content:
                data = json.loads(content)
                self.current_data = data
                self.data_changed.emit(data)
                
                # 同步更新JSON标签页中的编辑器，避免循环触发
                if self.json_editor.toPlainText() != content:
                    self.json_editor.blockSignals(True)
                    self.json_editor.setPlainText(content)
                    self.json_editor.blockSignals(False)
        except:
            pass  # 忽略格式错误，用户可能正在编辑
    
    def get_current_data(self):
        """获取当前JSON数据"""
        return self.current_data 

    def initialize_default_data(self):
        """初始化默认数据 - 由父控件在建立连接后调用"""
        self.load_default_data() 