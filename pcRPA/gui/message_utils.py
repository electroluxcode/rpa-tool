from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

def show_info_message(parent, title, message):
    """显示信息消息框"""
    msg_box = QMessageBox(parent)
    msg_box.setIcon(QMessageBox.Information)
    msg_box.setWindowTitle(title)
    msg_box.setText(message)
    msg_box.setFont(QFont("Microsoft YaHei", 12))
    
    # 应用暗黑主题样式
    msg_box.setStyleSheet("""
        QMessageBox {
            background-color: #3A3A3A;
            color: #D4D4D4;
            font-size: 14px;
        }
        QMessageBox QLabel {
            color: #D4D4D4;
            font-size: 14px;
            padding: 15px;
        }
        QMessageBox QPushButton {
            background-color: #4A4A4A;
            color: #D4D4D4;
            border: 1px solid #666;
            border-radius: 6px;
            padding: 8px 20px;
            font-size: 13px;
            font-weight: bold;
            min-width: 80px;
        }
        QMessageBox QPushButton:hover {
            background-color: #5A5A5A;
            border-color: #00D4AA;
        }
        QMessageBox QPushButton:default {
            background-color: #00D4AA;
            color: #000;
        }
    """)
    
    return msg_box.exec_()

def show_warning_message(parent, title, message):
    """显示警告消息框"""
    msg_box = QMessageBox(parent)
    msg_box.setIcon(QMessageBox.Warning)
    msg_box.setWindowTitle(title)
    msg_box.setText(message)
    msg_box.setFont(QFont("Microsoft YaHei", 12))
    
    # 应用暗黑主题样式
    msg_box.setStyleSheet("""
        QMessageBox {
            background-color: #3A3A3A;
            color: #D4D4D4;
            font-size: 14px;
        }
        QMessageBox QLabel {
            color: #D4D4D4;
            font-size: 14px;
            padding: 15px;
        }
        QMessageBox QPushButton {
            background-color: #E67E22;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 8px 20px;
            font-size: 13px;
            font-weight: bold;
            min-width: 80px;
        }
        QMessageBox QPushButton:hover {
            background-color: #D35400;
        }
    """)
    
    return msg_box.exec_()

def show_error_message(parent, title, message):
    """显示错误消息框"""
    msg_box = QMessageBox(parent)
    msg_box.setIcon(QMessageBox.Critical)
    msg_box.setWindowTitle(title)
    msg_box.setText(message)
    msg_box.setFont(QFont("Microsoft YaHei", 12))
    
    # 应用暗黑主题样式
    msg_box.setStyleSheet("""
        QMessageBox {
            background-color: #3A3A3A;
            color: #D4D4D4;
            font-size: 14px;
        }
        QMessageBox QLabel {
            color: #D4D4D4;
            font-size: 14px;
            padding: 15px;
        }
        QMessageBox QPushButton {
            background-color: #E74C3C;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 8px 20px;
            font-size: 13px;
            font-weight: bold;
            min-width: 80px;
        }
        QMessageBox QPushButton:hover {
            background-color: #C0392B;
        }
    """)
    
    return msg_box.exec_()

def show_question_message(parent, title, message):
    """显示询问消息框"""
    msg_box = QMessageBox(parent)
    msg_box.setIcon(QMessageBox.Question)
    msg_box.setWindowTitle(title)
    msg_box.setText(message)
    msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    msg_box.setDefaultButton(QMessageBox.Yes)
    msg_box.setFont(QFont("Microsoft YaHei", 12))
    
    # 应用暗黑主题样式
    msg_box.setStyleSheet("""
        QMessageBox {
            background-color: #3A3A3A;
            color: #D4D4D4;
            font-size: 14px;
        }
        QMessageBox QLabel {
            color: #D4D4D4;
            font-size: 14px;
            padding: 15px;
        }
        QMessageBox QPushButton {
            background-color: #4A4A4A;
            color: #D4D4D4;
            border: 1px solid #666;
            border-radius: 6px;
            padding: 8px 20px;
            font-size: 13px;
            font-weight: bold;
            min-width: 80px;
        }
        QMessageBox QPushButton:hover {
            background-color: #5A5A5A;
            border-color: #00D4AA;
        }
        QMessageBox QPushButton:default {
            background-color: #00D4AA;
            color: #000;
        }
    """)
    
    return msg_box.exec_() 