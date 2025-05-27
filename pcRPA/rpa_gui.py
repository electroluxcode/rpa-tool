# 简化的主入口文件，导入新的模块化GUI
from gui.main_window import main

def main_with_hotkey():
    """带全局热键的主函数"""
    try:
        # 导入全局热键管理器
        from global_hotkey import global_hotkey_manager
        
        # 启动GUI
        result = main()
        
        # 程序退出时停止全局热键监听
        global_hotkey_manager.stop()
        
        return result
    except ImportError:
        print("警告: 全局热键功能不可用")
        return main()

if __name__ == '__main__':
    main_with_hotkey() 