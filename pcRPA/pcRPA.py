import sys
import json
import os
from rpa_command import RPACommand

def command_line_mode():
    """命令行模式"""
    print('Electrolux_PC_RPA欢迎使用')
    print('提示: 脚本执行时按F10可随时停止')
    
    # 创建RPA命令对象
    rpa_command = RPACommand()
    
    # 选择功能
    print('选择功能:')
    print('1. 从JSON文件执行一次')
    print('2. 从JSON文件循环执行')
    print('3. 从Excel文件执行一次')
    print('4. 从Excel文件循环执行')
    print('5. 创建Excel模板')
    print('6. 启动GUI界面')
    
    key = input('请输入选项 (1-6): ')
    
    if key == '1':
        # 从JSON文件执行一次
        try:
            with open('pcRPAResouece.json', encoding='UTF-8') as f:
                allDataA = json.load(f)
            rpa_command.execute_once(allDataA["data"])
        except FileNotFoundError:
            print("错误: 找不到 pcRPAResouece.json 文件")
        except json.JSONDecodeError:
            print("错误: JSON文件格式不正确")
            
    elif key == '2':
        # 从JSON文件循环执行
        try:
            with open('pcRPAResouece.json', encoding='UTF-8') as f:
                allDataA = json.load(f)
            rpa_command.execute_loop(allDataA["data"])
        except FileNotFoundError:
            print("错误: 找不到 pcRPAResouece.json 文件")
        except json.JSONDecodeError:
            print("错误: JSON文件格式不正确")
            
    elif key == '3':
        # 从Excel文件执行一次
        excel_file = input('请输入Excel文件路径 (默认: rpa_commands.xlsx): ').strip()
        if not excel_file:
            excel_file = 'rpa_commands.xlsx'
        
        if not os.path.exists(excel_file):
            print(f"错误: 找不到Excel文件 {excel_file}")
        else:
            rpa_command.execute_excel_once(excel_file)
            
    elif key == '4':
        # 从Excel文件循环执行
        excel_file = input('请输入Excel文件路径 (默认: rpa_commands.xlsx): ').strip()
        if not excel_file:
            excel_file = 'rpa_commands.xlsx'
        
        if not os.path.exists(excel_file):
            print(f"错误: 找不到Excel文件 {excel_file}")
        else:
            rpa_command.execute_excel_loop(excel_file)
            
    elif key == '5':
        # 创建Excel模板
        template_file = input('请输入模板文件名 (默认: rpa_template.xlsx): ').strip()
        if not template_file:
            template_file = 'rpa_template.xlsx'
        
        result = RPACommand.create_excel_template(template_file)
        if result:
            print(f"✅ Excel模板已创建: {result}")
        else:
            print("❌ 创建Excel模板失败")
            
    elif key == '6':
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