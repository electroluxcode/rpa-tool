from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt

def apply_dark_theme(app_or_widget):
    """应用暗黑主题"""
    # 设置暗黑调色板
    palette = QPalette()
    
    # 窗口颜色
    palette.setColor(QPalette.Window, QColor(45, 45, 45))
    palette.setColor(QPalette.WindowText, QColor(212, 212, 212))
    
    # 基础颜色
    palette.setColor(QPalette.Base, QColor(30, 30, 30))
    palette.setColor(QPalette.AlternateBase, QColor(60, 60, 60))
    
    # 文本颜色
    palette.setColor(QPalette.Text, QColor(212, 212, 212))
    palette.setColor(QPalette.BrightText, QColor(255, 255, 255))
    
    # 按钮颜色
    palette.setColor(QPalette.Button, QColor(60, 60, 60))
    palette.setColor(QPalette.ButtonText, QColor(212, 212, 212))
    
    # 高亮颜色
    palette.setColor(QPalette.Highlight, QColor(0, 212, 170))
    palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
    
    # 应用调色板
    app_or_widget.setPalette(palette)
    
    # 设置样式表 - 进一步增大字体，修复QMessageBox颜色，优化QSplitter
    app_or_widget.setStyleSheet("""
        QMainWindow {
            background-color: #2D2D2D;
            color: #D4D4D4;
            font-size: 16px;
        }
        
        QGroupBox {
            font-weight: bold;
            font-size: 16px;
            border: 2px solid #555;
            border-radius: 8px;
            margin-top: 1ex;
            padding-top: 18px;
            background-color: #3A3A3A;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 10px 0 10px;
            color: #00D4AA;
            font-size: 17px;
            font-weight: bold;
        }
        
        QLabel {
            font-size: 15px;
            color: #D4D4D4;
        }
        
        QPushButton {
            font-size: 15px;
            font-weight: bold;
            padding: 10px 15px;
        }
        
        QRadioButton {
            font-size: 15px;
            color: #D4D4D4;
        }
        
        QTextEdit {
            font-size: 15px;
            line-height: 1.8;
        }
        
        QMenuBar {
            font-size: 14px;
            background-color: #3A3A3A;
            color: #D4D4D4;
        }
        
        QMenuBar::item {
            padding: 8px 12px;
            font-size: 14px;
        }
        
        QMenu {
            font-size: 14px;
            background-color: #3A3A3A;
            color: #D4D4D4;
            border: 1px solid #555;
        }
        
        QMenu::item {
            padding: 8px 20px;
            font-size: 14px;
        }
        
        /* 优化QSplitter样式 */
        QSplitter {
            background-color: #2D2D2D;
        }
        
        QSplitter::handle {
            background-color: #555;
            border: none;
        }
        
        QSplitter::handle:horizontal {
            width: 3px;
            background-color: #555;
            border-left: 1px solid #666;
            border-right: 1px solid #444;
        }
        
        QSplitter::handle:vertical {
            height: 3px;
            background-color: #555;
            border-top: 1px solid #666;
            border-bottom: 1px solid #444;
        }
        
        QSplitter::handle:hover {
            background-color: #00D4AA;
        }
        
        QSplitter::handle:pressed {
            background-color: #00B894;
        }
        
        /* 修复QMessageBox样式 */
        QMessageBox {
            background-color: #3A3A3A;
            color: #D4D4D4;
            font-size: 14px;
        }
        
        QMessageBox QLabel {
            color: #D4D4D4;
            font-size: 14px;
            padding: 10px;
        }
        
        QMessageBox QPushButton {
            background-color: #4A4A4A;
            color: #D4D4D4;
            border: 1px solid #666;
            border-radius: 6px;
            padding: 8px 16px;
            font-size: 13px;
            font-weight: bold;
            min-width: 80px;
        }
        
        QMessageBox QPushButton:hover {
            background-color: #5A5A5A;
            border-color: #00D4AA;
        }
        
        QMessageBox QPushButton:pressed {
            background-color: #00D4AA;
            color: #000;
        }
        
        QMessageBox QPushButton:default {
            background-color: #00D4AA;
            color: #000;
        }
        
        /* 修复QDialog样式 */
        QDialog {
            background-color: #3A3A3A;
            color: #D4D4D4;
            font-size: 14px;
        }
        
        QDialog QLabel {
            color: #D4D4D4;
            font-size: 14px;
        }
        
        QDialog QPushButton {
            background-color: #4A4A4A;
            color: #D4D4D4;
            border: 1px solid #666;
            border-radius: 6px;
            padding: 8px 16px;
            font-size: 13px;
            font-weight: bold;
            min-width: 80px;
        }
        
        QDialog QPushButton:hover {
            background-color: #5A5A5A;
            border-color: #00D4AA;
        }
        
        /* 修复QFileDialog样式 */
        QFileDialog {
            background-color: #3A3A3A;
            color: #D4D4D4;
        }
        
        QFileDialog QListView {
            background-color: #2D2D2D;
            color: #D4D4D4;
            border: 1px solid #555;
        }
        
        QFileDialog QTreeView {
            background-color: #2D2D2D;
            color: #D4D4D4;
            border: 1px solid #555;
        }
        
        QFileDialog QLineEdit {
            background-color: #2D2D2D;
            color: #D4D4D4;
            border: 1px solid #555;
            padding: 5px;
        }
        
        QFileDialog QComboBox {
            background-color: #2D2D2D;
            color: #D4D4D4;
            border: 1px solid #555;
            padding: 5px;
        }
        
        QScrollBar:vertical {
            background-color: #2D2D2D;
            width: 18px;
            border-radius: 9px;
        }
        
        QScrollBar::handle:vertical {
            background-color: #555;
            border-radius: 9px;
            min-height: 30px;
        }
        
        QScrollBar::handle:vertical:hover {
            background-color: #666;
        }
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            border: none;
            background: none;
        }
    """) 