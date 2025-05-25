from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, 
                             QPushButton, QLabel, QComboBox, QSplitter)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class StyleEditor(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("🎨 样式表编辑器")
        self.setGeometry(300, 300, 1000, 600)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # 标题
        title = QLabel("🎨 实时样式表编辑器")
        title.setFont(QFont("Microsoft YaHei", 16, QFont.Bold))
        title.setStyleSheet("color: #00D4AA; padding: 10px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # 控件选择器
        selector_layout = QHBoxLayout()
        selector_label = QLabel("选择控件:")
        selector_label.setStyleSheet("color: #D4D4D4; font-size: 12px;")
        
        self.widget_selector = QComboBox()
        self.widget_selector.addItems([
            "主窗口 (QMainWindow)",
            "控制面板 (ControlPanel)", 
            "录制组件 (RecorderWidget)",
            "数据源组件 (DataSourceWidget)",
            "执行组件 (ExecutionWidget)",
            "日志面板 (LogPanel)"
        ])
        self.widget_selector.currentTextChanged.connect(self.load_current_style)
        
        selector_layout.addWidget(selector_label)
        selector_layout.addWidget(self.widget_selector)
        selector_layout.addStretch()
        layout.addLayout(selector_layout)
        
        # 分割器
        splitter = QSplitter(Qt.Horizontal)
        layout.addWidget(splitter)
        
        # 样式编辑区
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        
        editor_label = QLabel("📝 CSS 样式编辑:")
        editor_label.setStyleSheet("color: #D4D4D4; font-size: 12px; font-weight: bold;")
        left_layout.addWidget(editor_label)
        
        self.style_editor = QTextEdit()
        self.style_editor.setStyleSheet("""
            QTextEdit {
                background-color: #1E1E1E;
                color: #D4D4D4;
                border: 1px solid #555;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 12px;
                line-height: 1.4;
            }
        """)
        left_layout.addWidget(self.style_editor)
        
        # 按钮区
        button_layout = QHBoxLayout()
        
        apply_btn = QPushButton("✅ 应用样式")
        apply_btn.clicked.connect(self.apply_style)
        apply_btn.setStyleSheet("""
            QPushButton {
                background-color: #27AE60;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                font-size: 12px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        
        reset_btn = QPushButton("🔄 重置样式")
        reset_btn.clicked.connect(self.reset_style)
        reset_btn.setStyleSheet("""
            QPushButton {
                background-color: #E67E22;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                font-size: 12px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #D35400;
            }
        """)
        
        button_layout.addWidget(apply_btn)
        button_layout.addWidget(reset_btn)
        button_layout.addStretch()
        left_layout.addLayout(button_layout)
        
        # 预设样式区
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        
        presets_label = QLabel("🎨 预设样式:")
        presets_label.setStyleSheet("color: #D4D4D4; font-size: 12px; font-weight: bold;")
        right_layout.addWidget(presets_label)
        
        self.presets_list = QTextEdit()
        self.presets_list.setReadOnly(True)
        self.presets_list.setStyleSheet("""
            QTextEdit {
                background-color: #2D2D2D;
                color: #D4D4D4;
                border: 1px solid #555;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 11px;
            }
        """)
        self.load_presets()
        right_layout.addWidget(self.presets_list)
        
        # 添加到分割器
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([600, 400])
        
        # 加载当前样式
        self.load_current_style()
    
    def load_current_style(self):
        """加载当前选中控件的样式"""
        current_text = self.widget_selector.currentText()
        
        if "主窗口" in current_text:
            style = self.main_window.styleSheet()
        elif "控制面板" in current_text:
            style = self.main_window.control_panel.styleSheet()
        elif "录制组件" in current_text:
            style = self.main_window.control_panel.recorder_widget.styleSheet()
        elif "数据源组件" in current_text:
            style = self.main_window.control_panel.data_source_widget.styleSheet()
        elif "执行组件" in current_text:
            style = self.main_window.control_panel.execution_widget.styleSheet()
        elif "日志面板" in current_text:
            style = self.main_window.log_panel.styleSheet()
        else:
            style = ""
        
        self.style_editor.setPlainText(style)
    
    def apply_style(self):
        """应用样式"""
        style = self.style_editor.toPlainText()
        current_text = self.widget_selector.currentText()
        
        try:
            if "主窗口" in current_text:
                self.main_window.setStyleSheet(style)
            elif "控制面板" in current_text:
                self.main_window.control_panel.setStyleSheet(style)
            elif "录制组件" in current_text:
                self.main_window.control_panel.recorder_widget.setStyleSheet(style)
            elif "数据源组件" in current_text:
                self.main_window.control_panel.data_source_widget.setStyleSheet(style)
            elif "执行组件" in current_text:
                self.main_window.control_panel.execution_widget.setStyleSheet(style)
            elif "日志面板" in current_text:
                self.main_window.log_panel.setStyleSheet(style)
            
            self.main_window.log_panel.add_log(f"✅ 样式已应用到 {current_text}")
            
        except Exception as e:
            self.main_window.log_panel.add_log(f"❌ 样式应用失败: {str(e)}")
    
    def reset_style(self):
        """重置样式"""
        from .theme import apply_dark_theme
        apply_dark_theme(self.main_window)
        self.load_current_style()
        self.main_window.log_panel.add_log("🔄 样式已重置为默认主题")
    
    def load_presets(self):
        """加载预设样式"""
        presets = """
=== 常用样式预设 ===

🔘 按钮样式:
QPushButton {
    background-color: #3498DB;
    color: white;
    border: none;
    border-radius: 6px;
    font-weight: bold;
    padding: 8px 16px;
}
QPushButton:hover {
    background-color: #2980B9;
}

📝 文本框样式:
QTextEdit {
    background-color: #1E1E1E;
    color: #D4D4D4;
    border: 2px solid #444;
    border-radius: 8px;
    padding: 10px;
    font-size: 12px;
}

📦 组框样式:
QGroupBox {
    font-weight: bold;
    border: 2px solid #555;
    border-radius: 8px;
    margin-top: 1ex;
    padding-top: 10px;
    background-color: #3A3A3A;
}

🏷️ 标签样式:
QLabel {
    color: #D4D4D4;
    font-size: 12px;
    padding: 4px;
}
        """
        self.presets_list.setPlainText(presets) 