import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QSplitter, QTreeWidget, QTreeWidgetItem, QLabel
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont

class QtInspector(QWidget):
    def __init__(self, target_widget=None):
        super().__init__()
        self.target_widget = target_widget
        self.setWindowTitle("Qt Inspector - 元素查看器")
        self.setGeometry(200, 200, 1200, 800)
        self.init_ui()
        
    def init_ui(self):
        layout = QHBoxLayout(self)
        
        # 创建分割器
        splitter = QSplitter(Qt.Horizontal)
        layout.addWidget(splitter)
        
        # 左侧：元素树
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        
        # 刷新按钮
        refresh_btn = QPushButton("🔄 刷新元素树")
        refresh_btn.clicked.connect(self.refresh_tree)
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498DB;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                font-size: 12px;
                padding: 8px 12px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #2980B9;
            }
        """)
        left_layout.addWidget(refresh_btn)
        
        # 元素树
        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderLabel("Qt 元素树")
        self.tree_widget.itemClicked.connect(self.on_item_clicked)
        self.tree_widget.setStyleSheet("""
            QTreeWidget {
                background-color: #2D2D2D;
                color: #D4D4D4;
                border: 1px solid #555;
                font-size: 12px;
            }
            QTreeWidget::item {
                padding: 4px;
            }
            QTreeWidget::item:selected {
                background-color: #00D4AA;
                color: black;
            }
        """)
        left_layout.addWidget(self.tree_widget)
        
        # 右侧：属性面板
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        
        # 属性标题
        props_title = QLabel("📋 元素属性")
        props_title.setFont(QFont("Microsoft YaHei", 14, QFont.Bold))
        props_title.setStyleSheet("color: #00D4AA; padding: 10px;")
        right_layout.addWidget(props_title)
        
        # 属性显示区域
        self.props_display = QTextEdit()
        self.props_display.setReadOnly(True)
        self.props_display.setStyleSheet("""
            QTextEdit {
                background-color: #1A1A1A;
                color: #E0E0E0;
                border: 1px solid #555;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 11px;
                line-height: 1.4;
            }
        """)
        right_layout.addWidget(self.props_display)
        
        # 样式显示区域
        style_title = QLabel("🎨 样式信息")
        style_title.setFont(QFont("Microsoft YaHei", 14, QFont.Bold))
        style_title.setStyleSheet("color: #00D4AA; padding: 10px;")
        right_layout.addWidget(style_title)
        
        self.style_display = QTextEdit()
        self.style_display.setReadOnly(True)
        self.style_display.setStyleSheet("""
            QTextEdit {
                background-color: #1A1A1A;
                color: #E0E0E0;
                border: 1px solid #555;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 11px;
                line-height: 1.4;
            }
        """)
        right_layout.addWidget(self.style_display)
        
        # 添加到分割器
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([400, 800])
        
        # 初始化树
        self.refresh_tree()
        
    def refresh_tree(self):
        """刷新元素树"""
        self.tree_widget.clear()
        
        if self.target_widget:
            root_item = QTreeWidgetItem([f"{self.target_widget.__class__.__name__} (Root)"])
            root_item.setData(0, Qt.UserRole, self.target_widget)
            self.tree_widget.addTopLevelItem(root_item)
            self.build_tree(self.target_widget, root_item)
            root_item.setExpanded(True)
        else:
            # 如果没有指定目标，遍历所有顶级窗口
            app = QApplication.instance()
            for widget in app.topLevelWidgets():
                if widget != self and widget.isVisible():
                    root_item = QTreeWidgetItem([f"{widget.__class__.__name__} (TopLevel)"])
                    root_item.setData(0, Qt.UserRole, widget)
                    self.tree_widget.addTopLevelItem(root_item)
                    self.build_tree(widget, root_item)
    
    def build_tree(self, widget, parent_item):
        """递归构建元素树"""
        for child in widget.findChildren(QWidget):
            if child.parent() == widget:  # 只添加直接子元素
                child_name = f"{child.__class__.__name__}"
                if hasattr(child, 'text') and child.text():
                    child_name += f" '{child.text()[:20]}'"
                elif hasattr(child, 'objectName') and child.objectName():
                    child_name += f" #{child.objectName()}"
                
                child_item = QTreeWidgetItem([child_name])
                child_item.setData(0, Qt.UserRole, child)
                parent_item.addChild(child_item)
                
                # 递归添加子元素
                self.build_tree(child, child_item)
    
    def on_item_clicked(self, item):
        """点击元素时显示属性"""
        widget = item.data(0, Qt.UserRole)
        if widget:
            self.show_widget_properties(widget)
            self.highlight_widget(widget)
    
    def show_widget_properties(self, widget):
        """显示控件属性"""
        props_text = f"=== {widget.__class__.__name__} 属性 ===\n\n"
        
        # 基本属性
        props_text += "📍 基本信息:\n"
        props_text += f"  类名: {widget.__class__.__name__}\n"
        props_text += f"  对象名: {widget.objectName() or '(未设置)'}\n"
        props_text += f"  可见: {widget.isVisible()}\n"
        props_text += f"  启用: {widget.isEnabled()}\n"
        
        # 几何属性
        props_text += f"\n📐 几何属性:\n"
        props_text += f"  位置: ({widget.x()}, {widget.y()})\n"
        props_text += f"  大小: {widget.width()} x {widget.height()}\n"
        props_text += f"  最小大小: {widget.minimumSize().width()} x {widget.minimumSize().height()}\n"
        props_text += f"  最大大小: {widget.maximumSize().width()} x {widget.maximumSize().height()}\n"
        
        # 文本属性
        if hasattr(widget, 'text'):
            props_text += f"\n📝 文本属性:\n"
            props_text += f"  文本: '{widget.text()}'\n"
        
        if hasattr(widget, 'font'):
            font = widget.font()
            props_text += f"  字体: {font.family()}, {font.pointSize()}pt\n"
        
        # 父子关系
        props_text += f"\n👨‍👩‍👧‍👦 层级关系:\n"
        props_text += f"  父控件: {widget.parent().__class__.__name__ if widget.parent() else 'None'}\n"
        props_text += f"  子控件数量: {len(widget.findChildren(QWidget, options=Qt.FindDirectChildrenOnly))}\n"
        
        # 样式表
        style_text = "=== 样式表 ===\n\n"
        if widget.styleSheet():
            style_text += widget.styleSheet()
        else:
            style_text += "(无自定义样式)"
        
        self.props_display.setPlainText(props_text)
        self.style_display.setPlainText(style_text)
    
    def highlight_widget(self, widget):
        """高亮显示选中的控件"""
        # 这里可以添加高亮效果，比如改变边框颜色
        pass

def show_qt_inspector(target_widget=None):
    """显示Qt检查器"""
    inspector = QtInspector(target_widget)
    inspector.show()
    return inspector 