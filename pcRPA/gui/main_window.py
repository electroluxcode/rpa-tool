import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget, QSplitter, QMenuBar, QAction
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QKeySequence

from .control_panel import ControlPanel
from .log_panel import LogPanel
from .theme import apply_dark_theme
from .debug_tools import show_qt_inspector

class RPAMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.inspector = None
        self.init_ui()
        apply_dark_theme(self)
        
    def init_ui(self):
        self.setWindowTitle("Electrolux PC RPA - 可视化界面")
        self.setGeometry(100, 100, 1400, 900)
        
        # 创建菜单栏
        self.create_menu_bar()
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QHBoxLayout(central_widget)
        
        # 创建分割器
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # 创建控制面板和日志面板
        self.control_panel = ControlPanel()
        self.log_panel = LogPanel()
        
        # 连接信号
        self.control_panel.log_signal.connect(self.log_panel.add_log)
        
        splitter.addWidget(self.control_panel)
        splitter.addWidget(self.log_panel)
        
        # 设置分割器比例 - 增大左侧控制面板的宽度
        splitter.setSizes([400, 800])  # 左侧400px，右侧800px，更平衡的分配
        
        # 设置最小宽度，防止面板被压缩得太小
        self.control_panel.setMinimumWidth(500)
        self.log_panel.setMinimumWidth(400)
    
    def create_menu_bar(self):
        """创建菜单栏"""
        menubar = self.menuBar()
        
        # 调试菜单
        debug_menu = menubar.addMenu('🔧 调试')
        
        # Qt Inspector
        inspector_action = QAction('🔍 Qt Inspector', self)
        inspector_action.setShortcut(QKeySequence('F12'))
        inspector_action.setStatusTip('打开Qt元素检查器 (F12)')
        inspector_action.triggered.connect(self.show_inspector)
        debug_menu.addAction(inspector_action)
        
        # 刷新界面
        refresh_action = QAction('🔄 刷新界面', self)
        refresh_action.setShortcut(QKeySequence('F5'))
        refresh_action.setStatusTip('刷新界面 (F5)')
        refresh_action.triggered.connect(self.refresh_ui)
        debug_menu.addAction(refresh_action)
        
        debug_menu.addSeparator()
        
        # 显示所有控件
        show_all_action = QAction('👁️ 显示所有控件', self)
        show_all_action.triggered.connect(self.show_all_widgets)
        debug_menu.addAction(show_all_action)
        
        # 样式表编辑器
        style_editor_action = QAction('🎨 样式表编辑器', self)
        style_editor_action.triggered.connect(self.show_style_editor)
        debug_menu.addAction(style_editor_action)
    
    def show_inspector(self):
        """显示Qt检查器"""
        if self.inspector is None or not self.inspector.isVisible():
            self.inspector = show_qt_inspector(self)
            self.log_panel.add_log("🔍 Qt Inspector 已打开 (F12)")
        else:
            self.inspector.raise_()
            self.inspector.activateWindow()
    
    def refresh_ui(self):
        """刷新界面"""
        self.update()
        if self.inspector and self.inspector.isVisible():
            self.inspector.refresh_tree()
        self.log_panel.add_log("🔄 界面已刷新")
    
    def show_all_widgets(self):
        """显示所有控件信息"""
        widgets_info = self.get_all_widgets_info(self)
        self.log_panel.add_log("👁️ 控件信息:")
        for info in widgets_info:
            self.log_panel.add_log(f"  {info}")
    
    def get_all_widgets_info(self, parent, level=0):
        """递归获取所有控件信息"""
        info_list = []
        indent = "  " * level
        
        widget_info = f"{indent}{parent.__class__.__name__}"
        if hasattr(parent, 'text') and parent.text():
            widget_info += f" '{parent.text()[:20]}'"
        elif hasattr(parent, 'objectName') and parent.objectName():
            widget_info += f" #{parent.objectName()}"
        
        info_list.append(widget_info)
        
        for child in parent.findChildren(QWidget):
            if child.parent() == parent:
                info_list.extend(self.get_all_widgets_info(child, level + 1))
        
        return info_list
    
    def show_style_editor(self):
        """显示样式表编辑器"""
        from .style_editor import StyleEditor
        self.style_editor = StyleEditor(self)
        self.style_editor.show()
        self.log_panel.add_log("🎨 样式表编辑器已打开")
    
    def keyPressEvent(self, event):
        """键盘事件处理"""
        if event.key() == Qt.Key_F12:
            self.show_inspector()
        elif event.key() == Qt.Key_F5:
            self.refresh_ui()
        else:
            super().keyPressEvent(event)
    
    def closeEvent(self, event):
        """关闭事件"""
        self.control_panel.cleanup()
        if self.inspector:
            self.inspector.close()
        event.accept()

def main():
    app = QApplication(sys.argv)
    
    # 设置应用程序信息
    app.setApplicationName("Electrolux PC RPA")
    app.setApplicationVersion("2.0")
    app.setOrganizationName("Electrolux")
    
    window = RPAMainWindow()
    window.show()
    
    sys.exit(app.exec_()) 