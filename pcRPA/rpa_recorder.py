import pyautogui
import pynput
from pynput import mouse, keyboard
import time
import json
import threading
from datetime import datetime

# 导入Excel解析器
try:
    from .excel_parser import excel_parser
except ImportError:
    try:
        from excel_parser import excel_parser
    except ImportError:
        print("警告: Excel解析模块导入失败，Excel保存功能将不可用")
        excel_parser = None

class RPARecorder:
    def __init__(self, callback=None):
        self.callback = callback  # 用于向界面发送状态更新
        self.is_recording = False
        self.recorded_actions = []
        self.start_time = None
        self.mouse_listener = None
        self.keyboard_listener = None
        self.last_action_time = None
        
        # 拖拽相关状态
        self.is_dragging = False
        self.drag_start_pos = None
        self.drag_start_time = None
        self.drag_button = None
        
    def log(self, message):
        """发送日志消息到界面"""
        if self.callback:
            self.callback(message)
        print(message)
    
    def start_recording(self):
        """开始录制"""
        if self.is_recording:
            return False
            
        self.is_recording = True
        self.recorded_actions = []
        self.start_time = time.time()
        self.last_action_time = self.start_time
        
        # 重置拖拽状态
        self.is_dragging = False
        self.drag_start_pos = None
        self.drag_start_time = None
        self.drag_button = None
        
        # 启动鼠标监听器
        self.mouse_listener = mouse.Listener(
            on_click=self.on_mouse_click,
            on_scroll=self.on_mouse_scroll,
            on_move=self.on_mouse_move
        )
        
        # 启动键盘监听器
        self.keyboard_listener = keyboard.Listener(
            on_press=self.on_key_press,
            on_release=self.on_key_release
        )
        
        self.mouse_listener.start()
        self.keyboard_listener.start()
        
        self.log("开始录制操作... (按F9停止录制)")
        return True
    
    def stop_recording(self):
        """停止录制"""
        if not self.is_recording:
            return []
            
        self.is_recording = False
        
        # 停止监听器
        if self.mouse_listener:
            self.mouse_listener.stop()
            self.mouse_listener = None
            
        if self.keyboard_listener:
            self.keyboard_listener.stop()
            self.keyboard_listener = None
        
        self.log(f"⏹️ 录制结束，共录制 {len(self.recorded_actions)} 个操作")
        return self.recorded_actions.copy()
    
    def add_sleep_if_needed(self):
        """如果需要的话添加睡眠时间"""
        current_time = time.time()
        if self.last_action_time:
            sleep_duration = current_time - self.last_action_time
            # 如果间隔超过0.5秒，添加睡眠
            if sleep_duration > 0.5:
                sleep_action = {
                    "cmdType": "Sleep",
                    "cmdParam": round(sleep_duration, 2)
                }
                self.recorded_actions.append(sleep_action)
                self.log(f"添加睡眠: {round(sleep_duration, 2)} 秒")
        
        self.last_action_time = current_time
    
    def on_mouse_click(self, x, y, button, pressed):
        """鼠标点击事件"""
        if not self.is_recording:
            return
        
        if pressed:  # 鼠标按下
            # 开始可能的拖拽操作
            self.drag_start_pos = (x, y)
            self.drag_start_time = time.time()
            self.drag_button = button
            self.is_dragging = False  # 还不确定是否是拖拽
            
        else:  # 鼠标释放
            if self.drag_start_pos:
                start_x, start_y = self.drag_start_pos
                
                # 计算移动距离
                distance = ((x - start_x) ** 2 + (y - start_y) ** 2) ** 0.5
                duration = time.time() - self.drag_start_time if self.drag_start_time else 0
                
                # 如果移动距离大于10像素且持续时间大于0.1秒，认为是拖拽
                if distance > 10 and duration > 0.1:
                    self.add_sleep_if_needed()
                    
                    button_name = "left" if self.drag_button == mouse.Button.left else "right"
                    
                    action = {
                        "cmdType": "DragTo",
                        "cmdParam": {
                            "x": x,
                            "y": y,
                            "duration": round(duration, 2),
                            "button": button_name
                        }
                    }
                    
                    self.recorded_actions.append(action)
                    self.log(f"录制拖拽: 从({start_x}, {start_y}) 到 ({x}, {y}) - {button_name} - 耗时{round(duration, 2)}秒")
                    
                else:
                    # 如果不是拖拽，记录为普通点击
                    self.add_sleep_if_needed()
                    
                    button_name = "left" if self.drag_button == mouse.Button.left else "right"
                    
                    action = {
                        "cmdType": "Click",
                        "cmdParam": {
                            "x": start_x,
                            "y": start_y,
                            "clicks": 1,
                            "interval": 0,
                            "button": button_name
                        }
                    }
                    
                    self.recorded_actions.append(action)
                    self.log(f"录制点击: ({start_x}, {start_y}) - {button_name}")
                
                # 重置拖拽状态
                self.drag_start_pos = None
                self.drag_start_time = None
                self.drag_button = None
                self.is_dragging = False
    
    def on_mouse_scroll(self, x, y, dx, dy):
        """鼠标滚轮事件"""
        if not self.is_recording:
            return
            
        self.add_sleep_if_needed()
        
        action = {
            "cmdType": "Scroll",
            "cmdParam": int(dy)
        }
        
        self.recorded_actions.append(action)
        self.log(f"录制滚轮: {int(dy)}")
    
    def on_mouse_move(self, x, y):
        """鼠标移动事件"""
        if not self.is_recording:
            return
            
        # 如果正在按住鼠标按钮且移动距离足够大，标记为拖拽
        if self.drag_start_pos and not self.is_dragging:
            start_x, start_y = self.drag_start_pos
            distance = ((x - start_x) ** 2 + (y - start_y) ** 2) ** 0.5
            
            # 如果移动距离超过5像素，开始认为是拖拽
            if distance > 5:
                self.is_dragging = True
                self.log(f"检测到拖拽开始: 从({start_x}, {start_y})")
    
    def on_key_press(self, key):
        """按键按下事件"""
        if not self.is_recording:
            return
            
        # 检查是否是停止录制的快捷键 (F9)
        if key == keyboard.Key.f9:
            self.log("检测到F9键，停止录制")
            self.stop_recording()
            return
        
        # 忽略F10键，因为它被用作全局停止热键
        if key == keyboard.Key.f10:
            self.log("F10键被保留用于停止脚本执行，不录制此按键")
            return
            
        self.add_sleep_if_needed()
        
        try:
            # 处理特殊键
            if hasattr(key, 'char') and key.char is not None:
                # 普通字符键
                if key.char.isprintable():
                    # 累积文本输入
                    self.accumulate_text(key.char)
                    return
            
            # 处理特殊按键
            key_name = self.get_key_name(key)
            if key_name:
                action = {
                    "cmdType": "Press",
                    "cmdParam": {
                        "keys": key_name,
                        "presses": 1,
                        "interval": 0
                    }
                }
                
                self.recorded_actions.append(action)
                self.log(f"录制按键: {key_name}")
                
        except Exception as e:
            self.log(f"录制按键时出错: {str(e)}")
    
    def on_key_release(self, key):
        """按键释放事件（暂时不处理）"""
        pass
    
    def accumulate_text(self, char):
        """累积文本输入"""
        # 检查最后一个动作是否是文本输入
        if (self.recorded_actions and 
            self.recorded_actions[-1]["cmdType"] in ["Write", "ChineseWrite"]):
            # 追加到现有文本
            if self.recorded_actions[-1]["cmdType"] == "Write":
                self.recorded_actions[-1]["cmdParam"]["message"] += char
            else:  # ChineseWrite
                self.recorded_actions[-1]["cmdParam"] += char
            self.log(f"追加文本: {char}")
        else:
            # 创建新的文本输入动作
            # 判断是否包含中文字符
            if self.contains_chinese(char):
                action = {
                    "cmdType": "ChineseWrite",
                    "cmdParam": char
                }
            else:
                action = {
                    "cmdType": "Write",
                    "cmdParam": {
                        "message": char,
                        "interval": 0.01
                    }
                }
            
            self.recorded_actions.append(action)
            self.log(f"录制文本: {char}")
    
    def contains_chinese(self, text):
        """检查文本是否包含中文字符"""
        for char in text:
            if '\u4e00' <= char <= '\u9fff':
                return True
        return False
    
    def get_key_name(self, key):
        """获取按键名称"""
        key_mapping = {
            keyboard.Key.enter: 'enter',
            keyboard.Key.tab: 'tab',
            keyboard.Key.space: 'space',
            keyboard.Key.backspace: 'backspace',
            keyboard.Key.delete: 'delete',
            keyboard.Key.esc: 'escape',
            keyboard.Key.ctrl_l: 'ctrl',
            keyboard.Key.ctrl_r: 'ctrl',
            keyboard.Key.alt_l: 'alt',
            keyboard.Key.alt_r: 'alt',
            keyboard.Key.shift_l: 'shift',
            keyboard.Key.shift_r: 'shift',
            keyboard.Key.up: 'up',
            keyboard.Key.down: 'down',
            keyboard.Key.left: 'left',
            keyboard.Key.right: 'right',
            keyboard.Key.home: 'home',
            keyboard.Key.end: 'end',
            keyboard.Key.page_up: 'pageup',
            keyboard.Key.page_down: 'pagedown',
        }
        
        # 功能键
        if hasattr(key, 'name') and key.name.startswith('f') and key.name[1:].isdigit():
            return key.name
            
        return key_mapping.get(key, None)
    
    def generate_json(self):
        """生成JSON格式的录制数据"""
        json_data = {
            "data": self.recorded_actions,
            "metadata": {
                "recorded_at": datetime.now().isoformat(),
                "total_actions": len(self.recorded_actions),
                "recording_duration": time.time() - self.start_time if self.start_time else 0
            }
        }
        return json_data
    
    def save_to_file(self, file_path):
        """保存录制数据到文件"""
        try:
            json_data = self.generate_json()
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=2)
            self.log(f"✅ 录制数据已保存到: {file_path}")
            return True
        except Exception as e:
            self.log(f"❌ 保存文件时出错: {str(e)}")
            return False
    
    def save_to_excel(self, file_path):
        """保存录制数据到Excel文件"""
        if not excel_parser:
            self.log("❌ Excel解析模块不可用，无法保存为Excel格式")
            return False
        
        try:
            # 生成JSON数据
            json_data = self.generate_json()
            
            # 转换为Excel格式
            self.log("📊 正在转换录制数据为Excel格式...")
            success = self._convert_to_excel(json_data, file_path)
            
            if success:
                self.log(f"✅ 录制数据已保存为Excel文件: {file_path}")
                return True
            else:
                self.log("❌ 转换为Excel格式失败")
                return False
                
        except Exception as e:
            self.log(f"❌ 保存Excel文件时出错: {str(e)}")
            return False
    
    def _convert_to_excel(self, json_data, excel_path):
        """将JSON数据转换为Excel格式"""
        try:
            import pandas as pd
            
            # 准备Excel数据
            excel_data = []
            
            for i, action in enumerate(json_data["data"]):
                cmd_type = action.get("cmdType", "")
                cmd_param = action.get("cmdParam", {})
                
                # 将参数转换为字符串格式
                if isinstance(cmd_param, dict):
                    param_str = json.dumps(cmd_param, ensure_ascii=False)
                else:
                    param_str = str(cmd_param)
                
                # 清理参数字符串中的换行符，确保Excel单元格显示正常
                param_str = param_str.replace('\n', '').replace('\r', '').strip()
                
                # 生成说明
                description = self._generate_description(cmd_type, cmd_param)
                # 同样清理说明中的换行符
                description = description.replace('\n', '').replace('\r', '').strip()
                
                excel_data.append({
                    "cmdType": cmd_type,
                    "cmdParam": param_str,
                    "说明": description
                })
            
            # 创建DataFrame
            df = pd.DataFrame(excel_data)
            
            # 保存为Excel文件
            with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='录制的RPA命令', index=False)
                
                # 获取工作表对象以设置列宽
                worksheet = writer.sheets['录制的RPA命令']
                worksheet.column_dimensions['A'].width = 15  # cmdType列
                worksheet.column_dimensions['B'].width = 60  # cmdParam列
                worksheet.column_dimensions['C'].width = 40  # 说明列
                
                # 添加元数据工作表
                metadata = json_data.get("metadata", {})
                metadata_df = pd.DataFrame([
                    {"属性": "录制时间", "值": metadata.get("recorded_at", "")},
                    {"属性": "总命令数", "值": metadata.get("total_actions", 0)},
                    {"属性": "录制时长(秒)", "值": round(metadata.get("recording_duration", 0), 2)},
                    {"属性": "生成工具", "值": "RPA录制器"},
                    {"属性": "文件格式", "值": "Excel (.xlsx)"}
                ])
                metadata_df.to_excel(writer, sheet_name='录制信息', index=False)
                
                # 设置元数据工作表列宽
                metadata_worksheet = writer.sheets['录制信息']
                metadata_worksheet.column_dimensions['A'].width = 20
                metadata_worksheet.column_dimensions['B'].width = 30
            
            return True
            
        except ImportError:
            self.log("❌ 缺少pandas或openpyxl依赖，无法保存Excel文件")
            self.log("请运行: pip install pandas openpyxl")
            return False
        except Exception as e:
            self.log(f"❌ 转换Excel时出错: {str(e)}")
            return False
    
    def _generate_description(self, cmd_type, cmd_param):
        """为命令生成中文描述"""
        descriptions = {
            "Click": lambda p: f"点击坐标({p.get('x', 0)}, {p.get('y', 0)}) - {p.get('button', 'left')}键",
            "MoveTo": lambda p: f"移动鼠标到({p.get('x', 0)}, {p.get('y', 0)})",
            "DragTo": lambda p: f"拖拽到({p.get('x', 0)}, {p.get('y', 0)}) - 耗时{p.get('duration', 0)}秒",
            "Scroll": lambda p: f"滚轮操作 - 方向{p}",
            "Write": lambda p: f"输入文本: {p.get('message', '') if isinstance(p, dict) else str(p)}",
            "ChineseWrite": lambda p: f"输入中文: {p}",
            "Press": lambda p: f"按键: {p.get('keys', '') if isinstance(p, dict) else str(p)}",
            "Sleep": lambda p: f"等待 {p} 秒"
        }
        
        try:
            if cmd_type in descriptions:
                return descriptions[cmd_type](cmd_param)
            else:
                return f"{cmd_type} 操作"
        except:
            return f"{cmd_type} 操作"
    
    def save_with_format_choice(self, base_path, save_format="both"):
        """根据格式选择保存文件
        
        Args:
            base_path: 基础文件路径（不含扩展名）
            save_format: 保存格式 ("json", "excel", "both")
        
        Returns:
            dict: 保存结果 {"json": bool, "excel": bool}
        """
        results = {"json": False, "excel": False}
        
        if save_format in ["json", "both"]:
            json_path = f"{base_path}.json"
            results["json"] = self.save_to_file(json_path)
        
        if save_format in ["excel", "both"]:
            excel_path = f"{base_path}.xlsx"
            results["excel"] = self.save_to_excel(excel_path)
        
        return results 