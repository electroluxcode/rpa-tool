import sys
import json
from rpa_command import RPACommand

def command_line_mode():
    """命令行模式"""
    print('Electrolux_PC_RPA欢迎使用')
    
    # 创建RPA命令对象
    rpa_command = RPACommand()
    
    # 加载数据
    try:
        with open('pcRPAResouece.json', encoding='UTF-8') as f:
            allDataA = json.load(f)
    except FileNotFoundError:
        print("错误: 找不到 pcRPAResouece.json 文件")
        return
    except json.JSONDecodeError:
        print("错误: JSON文件格式不正确")
        return
    
    # 选择功能
    key = input('选择功能: 1.做一次 2.循环到死 3.启动GUI界面\n')
    
    if key == '1':
        rpa_command.execute_once(allDataA["data"])
    elif key == '2':
        rpa_command.execute_loop(allDataA["data"])
    elif key == '3':
        # 启动GUI界面
        try:
            from rpa_gui import main as gui_main
            gui_main()
        except ImportError:
            print("错误: 无法导入GUI模块，请确保已安装PyQt5")
            print("安装命令: pip install PyQt5")
    else:
        print("无效选择")

if __name__ == '__main__':
    # 默认gui
    gui = True

    # 检查命令行参数
    if (len(sys.argv) > 1 and (sys.argv[1] == '--gui') or gui):
        # 直接启动GUI
        try:
            from rpa_gui import main as gui_main
            gui_main()
        except ImportError as e:
            # 打印错误信息
            print(e.msg)
    else:
        # 命令行模式
        command_line_mode()    