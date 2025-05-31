import pyautogui
import time
import json
import sys
import pyperclip
import cv2
import numpy as np
import os
import threading
from pynput import keyboard
# 确保 PyScreeze 正确导入
try:
    import pyscreeze
except ImportError:
    print("正在尝试安装 pyscreeze...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyscreeze"])
    import pyscreeze

# 导入OCR相关模块
try:
    from .ocr.PPOCR_api import GetOcrApi
    import subprocess
    from PIL import ImageGrab
except ImportError:
    try:
        from ocr.PPOCR_api import GetOcrApi
        import subprocess
        from PIL import ImageGrab
    except ImportError:
        print("警告: OCR模块导入失败，OCR功能将不可用")
        GetOcrApi = None

# 导入全局热键管理器
try:
    from .global_hotkey import global_hotkey_manager
except ImportError:
    try:
        from global_hotkey import global_hotkey_manager
    except ImportError:
        print("警告: 全局热键模块导入失败")
        global_hotkey_manager = None

# 导入Excel解析器
try:
    from .excel_parser import excel_parser
except ImportError:
    try:
        from excel_parser import excel_parser
    except ImportError:
        print("警告: Excel解析模块导入失败，Excel功能将不可用")
        excel_parser = None

class RPACommand:
    def __init__(self, callback=None):
        self.callback = callback  # 用于向界面发送状态更新
        self.is_running = False
        self.should_stop = False
        self._stop_event = threading.Event()
        self.ocr_api = None
        self._init_ocr()
        self._setup_global_hotkeys()
    
    def _setup_global_hotkeys(self):
        """设置全局热键"""
        if global_hotkey_manager:
            # 注册F10为停止执行热键
            global_hotkey_manager.register_hotkey(keyboard.Key.f10, self._on_f10_pressed)
            global_hotkey_manager.start()
    
    def _on_f10_pressed(self):
        """F10按键回调 - 停止脚本执行"""
        if self.is_running:
            self.log("检测到F10热键，停止脚本执行")
            self.stop_execution()
        else:
            self.log("当前没有脚本在运行")
    
    def _init_ocr(self):
        """初始化OCR引擎"""
        if GetOcrApi is None:
            self.log("OCR模块不可用")
            return
            
        try:
            # 查找PaddleOCR-json.exe路径
            path = self._find_paddleocr_exe()
            if path:
                self.ocr_api = GetOcrApi(path)
                self.log(f"OCR引擎初始化成功，进程号为{self.ocr_api.ret.pid}")
            else:
                self.log("未找到PaddleOCR-json.exe，OCR功能不可用")
        except Exception as e:
            self.log(f"OCR引擎初始化失败: {str(e)}")
    
    def _find_paddleocr_exe(self):
        """查找PaddleOCR-json.exe的路径"""
        try:
            result = subprocess.run(['where', 'PaddleOCR-json.exe'], 
                                  capture_output=True, text=True, check=True)
            paths = result.stdout.strip().split('\n')
            if paths:
                return paths[0]
        except subprocess.CalledProcessError:
            pass
        return None
    
    def _perform_ocr_on_screen(self):
        """对当前屏幕进行OCR识别"""
        if not self.ocr_api:
            self.log("OCR引擎未初始化")
            return None
            
        try:
            # 截取屏幕
            img = ImageGrab.grab()
            temp_path = os.path.join(os.path.dirname(__file__), "temp_screenshot.png")
            img.save(temp_path)
            
            # 进行OCR识别
            result = self.ocr_api.run(temp_path)
            
            # 清理临时文件
            if os.path.exists(temp_path):
                os.remove(temp_path)
                
            if result["code"] == 100:
                return result["data"]
            else:
                self.log(f"OCR识别失败: {result['data']}")
                return None
                
        except Exception as e:
            self.log(f"OCR识别过程出错: {str(e)}")
            return None
    
    def _find_text_in_ocr_results(self, ocr_results, target_texts):
        """在OCR结果中查找目标文本"""
        if not ocr_results:
            return None
            
        for text_block in ocr_results:
            text = text_block.get("text", "")
            for target in target_texts:
                if target in text:
                    # 计算文本块的中心位置
                    box = text_block.get("box", [])
                    if len(box) >= 4:
                        # box格式: [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]
                        x_coords = [point[0] for point in box]
                        y_coords = [point[1] for point in box]
                        center_x = sum(x_coords) // len(x_coords)
                        center_y = sum(y_coords) // len(y_coords)
                        
                        self.log(f"找到目标文本 '{target}' 在位置: ({center_x}, {center_y})")
                        return {
                            "text": text,
                            "target": target,
                            "center_x": center_x,
                            "center_y": center_y,
                            "box": box,
                            "score": text_block.get("score", 0)
                        }
        return None

    def log(self, message):
        """发送日志消息到界面"""
        if self.callback:
            self.callback(message)
        print(message)
    
    def stop_execution(self):
        """停止执行"""
        self.should_stop = True
        self.is_running = False
        self._stop_event.set()
        self.log("收到停止信号")
        
        # 清理OCR引擎
        if self.ocr_api:
            try:
                self.ocr_api.exit()
            except:
                pass
    
    def interruptible_sleep(self, duration):
        """可中断的睡眠函数"""
        if self._stop_event.wait(duration):
            return True  # 被中断
        return False  # 正常完成
    
    def mouseClick(self, clickTimes, lOrR, img, reTry, region=None):
        self.log(f"正在寻找图片：{img}")
        
        # 检查停止信号
        if self.should_stop:
            return False
        
        # 设置查找区域
        if region:
            # 获取屏幕尺寸
            screen_width, screen_height = pyautogui.size()
            
            # 预定义区域
            if region == 'left':
                search_region = (0, 0, screen_width//2, screen_height)
            elif region == 'right':
                search_region = (screen_width//2, 0, screen_width//2, screen_height)
            elif region == 'top':
                search_region = (0, 0, screen_width, screen_height//2)
            elif region == 'bottom':
                search_region = (0, screen_height//2, screen_width, screen_height//2)
            # 添加四个角落区域
            elif region == 'left_top' or region == 'top_left':
                search_region = (0, 0, screen_width//2, screen_height//2)
            elif region == 'right_top' or region == 'top_right':
                search_region = (screen_width//2, 0, screen_width//2, screen_height//2)
            elif region == 'left_bottom' or region == 'bottom_left':
                search_region = (0, screen_height//2, screen_width//2, screen_height//2)
            elif region == 'right_bottom' or region == 'bottom_right':
                search_region = (screen_width//2, screen_height//2, screen_width//2, screen_height//2)
            # 添加中间区域
            elif region == 'center':
                quarter_width = screen_width//4
                quarter_height = screen_height//4
                search_region = (quarter_width, quarter_height, quarter_width*2, quarter_height*2)
            # 自定义区域
            elif isinstance(region, list) and len(region) == 4:
                search_region = tuple(region)  # 自定义区域 [x, y, width, height]
            else:
                search_region = None
                self.log(f"无效的区域参数: {region}，将在全屏查找")
        else:
            search_region = None
        
        if reTry == 1:
            while not self.should_stop:
                try:
                    location=pyautogui.locateCenterOnScreen(img, confidence=0.7, region=search_region)
                    if location is not None:
                        pyautogui.click(location.x,location.y,clicks=clickTimes,interval=0.2,duration=0.2,button=lOrR)
                        self.log(f"找到匹配图片，点击位置: ({location.x}, {location.y})")
                        return True
                    self.log("未找到匹配图片,0.5秒后重试")
                    if self.interruptible_sleep(0.5):
                        break
                except:
                    self.log("未找到匹配图片,0.5秒后重试")
                    if self.interruptible_sleep(0.5):
                        break
                    pass
        elif reTry > 1:
            i = 1
            found = False
            while i < reTry + 1 and not self.should_stop:
                try:
                    location=pyautogui.locateCenterOnScreen(img, confidence=0.7, region=search_region)
                    if location is not None:
                        pyautogui.click(location.x,location.y,clicks=clickTimes,interval=0.2,duration=0.2,button=lOrR)
                        i += 1
                        self.log("恭喜找到图片")
                        found = True
                        break
                    if self.interruptible_sleep(0.1):
                        break
                except Exception as e:
                    self.log(f"查找图片失败: {str(e)}")
                    i += 1
                    pass
            return found
        elif reTry == 0:
            try:
                location=pyautogui.locateCenterOnScreen(img, confidence=0.7, region=search_region)
                if location is not None:
                    self.log("遇到指定图片停止30分钟")
                    # 使用可中断的睡眠
                    if self.interruptible_sleep(30*60):
                        self.log("30分钟等待被中断")
                    return True
                return False
            except:
                return False
        
        # 如果执行到这里，说明没有找到图片
        return False

    def mainWork(self, allData):
        self.is_running = True
        self.log("脚本开始执行 (按F10可随时停止)")
        i = 0
        while i < len(allData) and not self.should_stop:
            # 检查停止信号
            if self._stop_event.is_set():
                self.log("检测到停止信号，退出执行")
                break
                
            cmdType = allData[i]["cmdType"]
            cmdParam = allData[i]["cmdParam"]
            
            self.log(f"执行命令 {i+1}/{len(allData)}: {cmdType}")
            
            if cmdType == "OCR":
                # 执行OCR识别和后续操作
                target_texts = cmdParam.get("target", [])
                then_actions = cmdParam.get("then", [])
                wait_for_target = cmdParam.get("waitForTarget", False)  # 是否等待目标被发现
                detect_time = cmdParam.get("detecttime", 0.5)  # 检测间隔时间，默认0.5秒
                max_wait_time = cmdParam.get("maxWaitTime", 30)  # 最大等待时间，默认30秒
                
                self.log(f"开始OCR识别，查找目标文本: {target_texts}")
                if wait_for_target:
                    self.log(f"等待模式已启用，检测间隔: {detect_time}秒，最大等待时间: {max_wait_time}秒")
                
                found_text = None
                start_time = time.time()
                
                while True:
                    # 检查是否应该停止执行
                    if self.should_stop:
                        self.log("OCR检测被中断")
                        break
                    
                    # 进行OCR识别
                    ocr_results = self._perform_ocr_on_screen()
                    if ocr_results:
                        # 查找目标文本
                        found_text = self._find_text_in_ocr_results(ocr_results, target_texts)
                        
                        if found_text:
                            self.log(f"找到目标文本 '{found_text['target']}'")
                            break
                        elif not wait_for_target:
                            # 如果不是等待模式，一次未找到就退出
                            self.log("未找到目标文本")
                            break
                        else:
                            # 等待模式：检查是否超时
                            elapsed_time = time.time() - start_time
                            if elapsed_time >= max_wait_time:
                                self.log(f"等待超时({max_wait_time}秒)，未找到目标文本")
                                break
                            else:
                                remaining_time = max_wait_time - elapsed_time
                                self.log(f"未找到目标文本，{detect_time}秒后重试 (剩余等待时间: {remaining_time:.1f}秒)")
                                # 可中断的等待
                                if self.interruptible_sleep(detect_time):
                                    self.log("OCR等待被中断")
                                    break
                    else:
                        self.log("OCR识别失败")
                        if not wait_for_target:
                            break
                        else:
                            # 等待模式：检查是否超时
                            elapsed_time = time.time() - start_time
                            if elapsed_time >= max_wait_time:
                                self.log(f"等待超时({max_wait_time}秒)，OCR识别持续失败")
                                break
                            else:
                                remaining_time = max_wait_time - elapsed_time
                                self.log(f"OCR识别失败，{detect_time}秒后重试 (剩余等待时间: {remaining_time:.1f}秒)")
                                # 可中断的等待
                                if self.interruptible_sleep(detect_time):
                                    self.log("OCR等待被中断")
                                    break
                
                # 如果找到目标文本且有后续操作
                if found_text and then_actions and not self.should_stop:
                    self.log(f"找到目标文本 '{found_text['target']}'，执行后续操作")
                    
                    # 设置当前OCR结果为上下文，供后续操作使用
                    self._current_ocr_context = found_text
                    
                    # 执行后续操作
                    self.mainWork(then_actions)
                    
                    # 清理上下文
                    self._current_ocr_context = None
                    
                    self.log("OCR后续操作执行完毕，继续主流程")
                elif not found_text:
                    self.log("未找到目标文本，跳过后续操作")
                elif not then_actions:
                    self.log("无后续操作需要执行")
            
            elif cmdType == "ClickAfterOCR":
                # 基于OCR结果进行点击
                if hasattr(self, '_current_ocr_context') and self._current_ocr_context:
                    base_x = self._current_ocr_context['center_x']
                    base_y = self._current_ocr_context['center_y']
                    offset_x = cmdParam.get("x", 0)
                    offset_y = cmdParam.get("y", 0)
                    
                    target_x = base_x + offset_x
                    target_y = base_y + offset_y
                    
                    pyautogui.click(
                        x=target_x,
                        y=target_y,
                        clicks=cmdParam.get("clicks", 1),
                        interval=cmdParam.get("interval", 0),
                        button=cmdParam.get("button", "left")
                    )
                    self.log(f"基于OCR结果点击位置: ({target_x}, {target_y}) [基准位置: ({base_x}, {base_y}), 偏移: ({offset_x}, {offset_y})]")
                else:
                    self.log("错误: ClickAfterOCR命令需要在OCR命令之后执行")
            
            elif cmdType == "MoveToAfterOCR":
                # 基于OCR结果进行鼠标移动
                if hasattr(self, '_current_ocr_context') and self._current_ocr_context:
                    base_x = self._current_ocr_context['center_x']
                    base_y = self._current_ocr_context['center_y']
                    offset_x = cmdParam.get("x", 0)
                    offset_y = cmdParam.get("y", 0)
                    
                    target_x = base_x + offset_x
                    target_y = base_y + offset_y
                    
                    pyautogui.moveTo(
                        x=target_x,
                        y=target_y,
                        duration=cmdParam.get("duration", 0.25)
                    )
                    self.log(f"基于OCR结果移动鼠标到: ({target_x}, {target_y}) [基准位置: ({base_x}, {base_y}), 偏移: ({offset_x}, {offset_y})]")
                else:
                    self.log("错误: MoveToAfterOCR命令需要在OCR命令之后执行")
            
            elif cmdType == "DragToAfterOCR":
                # 基于OCR结果进行拖拽
                if hasattr(self, '_current_ocr_context') and self._current_ocr_context:
                    base_x = self._current_ocr_context['center_x']
                    base_y = self._current_ocr_context['center_y']
                    offset_x = cmdParam.get("x", 0)
                    offset_y = cmdParam.get("y", 0)
                    
                    target_x = base_x + offset_x
                    target_y = base_y + offset_y
                    
                    pyautogui.dragTo(
                        x=target_x,
                        y=target_y,
                        duration=cmdParam.get("duration", 0.25),
                        button=cmdParam.get("button", "left")
                    )
                    self.log(f"基于OCR结果拖拽到: ({target_x}, {target_y}) [基准位置: ({base_x}, {base_y}), 偏移: ({offset_x}, {offset_y})]")
                else:
                    self.log("错误: DragToAfterOCR命令需要在OCR命令之后执行")
            
            elif cmdType == "ShutDown":
                timeout = cmdParam.get("timeout", 10)
                self.log("电脑将在" + str(timeout) + "秒后关机")
                os.system("shutdown -s -t " + str(timeout))
                if self.interruptible_sleep(timeout+3):
                    break
                break
                
            elif cmdType == "Click":   
                try:
                    x = int(cmdParam.get("x"))
                    y = int(cmdParam.get("y"))
                    pyautogui.click( 
                        x=x, 
                        y=y, 
                        clicks=cmdParam.get("clicks", 1), 
                        interval=cmdParam.get("interval", 0), 
                        button=cmdParam.get("button", "left")
                    )
                    self.log(f"点击坐标 ({x}, {y})")
                except ValueError:
                    self.log(f"错误: 无效的坐标值 x={cmdParam.get('x')}, y={cmdParam.get('y')}")
                except Exception as e:
                    self.log(f"点击操作出错: {str(e)}")

            elif cmdType == "MoveTo":   
                pyautogui.moveTo(
                    x=cmdParam.get("x"), 
                    y=cmdParam.get("y"), 
                    duration=cmdParam.get("duration", 0.25)
                )
                self.log(f"鼠标移动到 {cmdParam}")

            elif cmdType == "DragTo":  
                pyautogui.dragTo(
                    x=cmdParam.get("x"), 
                    y=cmdParam.get("y"), 
                    duration=cmdParam.get("duration", 0.25), 
                    button=cmdParam.get("button", "left")
                )
                self.log(f"鼠标拖拽到 {cmdParam}")

            elif cmdType == "SearchImage":
                # 搜索图片，设置图片上下文
                target_images = cmdParam.get("target", [])
                then_actions = cmdParam.get("then", [])  # 添加then操作支持
                wait_for_target = cmdParam.get("waitForTarget", False)  # 是否等待目标被发现
                detect_time = cmdParam.get("detecttime", 0.5)  # 检测间隔时间，默认0.5秒
                max_wait_time = cmdParam.get("maxWaitTime", 30)  # 最大等待时间，默认30秒
                region = cmdParam.get("region")  # 搜索区域
                
                self.log(f"开始搜索图片，查找目标图片: {target_images}")
                if wait_for_target:
                    self.log(f"等待模式已启用，检测间隔: {detect_time}秒，最大等待时间: {max_wait_time}秒")
                
                found_image = None
                start_time = time.time()
                
                while True:
                    # 检查是否应该停止执行
                    if self.should_stop:
                        self.log("图片搜索被中断")
                        break
                    
                    # 进行图片识别
                    found_image = self.find_image_on_screen(target_images, region)
                    
                    if found_image:
                        self.log(f"找到目标图片 '{found_image['target']}'")
                        # 设置当前图片结果为上下文，供后续操作使用
                        self._current_image_context = found_image
                        break
                    elif not wait_for_target:
                        # 如果不是等待模式，一次未找到就退出
                        self.log("未找到目标图片")
                        break
                    else:
                        # 等待模式：检查是否超时
                        elapsed_time = time.time() - start_time
                        if elapsed_time >= max_wait_time:
                            self.log(f"等待超时({max_wait_time}秒)，未找到目标图片")
                            break
                        else:
                            remaining_time = max_wait_time - elapsed_time
                            self.log(f"未找到目标图片，{detect_time}秒后重试 (剩余等待时间: {remaining_time:.1f}秒)")
                            # 可中断的等待
                            if self.interruptible_sleep(detect_time):
                                self.log("图片搜索等待被中断")
                                break
                
                # 如果找到目标图片且有后续操作
                if found_image and then_actions and not self.should_stop:
                    self.log(f"找到目标图片 '{found_image['target']}'，执行后续操作")
                    
                    # 执行后续操作
                    self.mainWork(then_actions)
                    
                    self.log("SearchImage后续操作执行完毕，继续主流程")
                elif not found_image:
                    self.log("未找到目标图片，跳过后续操作")
                elif not then_actions:
                    self.log("无后续操作需要执行")
            
            elif cmdType == "ImgClick":   
                # 为了向后兼容，保留ImgClick命令，内部转换为SearchImage + ClickAfterImg
                target_images = cmdParam.get("target", [])
                then_actions = cmdParam.get("then", [])
                wait_for_target = cmdParam.get("waitForTarget", False)
                detect_time = cmdParam.get("detecttime", 0.5)
                max_wait_time = cmdParam.get("maxWaitTime", 30)
                region = cmdParam.get("region")
                
                # 兼容旧格式：如果没有target参数但有imgPath参数，则转换为新格式
                if not target_images and "imgPath" in cmdParam:
                    target_images = [cmdParam["imgPath"]]
                    self.log("检测到旧格式imgPath参数，已转换为新格式target参数")
                
                # 先执行SearchImage操作
                search_data = [{
                    "cmdType": "SearchImage",
                    "cmdParam": {
                        "target": target_images,
                        "waitForTarget": wait_for_target,
                        "detecttime": detect_time,
                        "maxWaitTime": max_wait_time,
                        "region": region
                    }
                }]
                
                # 执行搜索
                self.mainWork(search_data)
                
                # 如果找到图片，执行点击操作
                if hasattr(self, '_current_image_context') and self._current_image_context:
                    click_data = [{
                        "cmdType": "ClickAfterImg", 
                        "cmdParam": {
                            "x": 0,
                            "y": 0,
                            "clicks": cmdParam.get("clicks", 1),
                            "button": cmdParam.get("button", "left")
                        }
                    }]
                    
                    # 执行点击
                    self.mainWork(click_data)
                    
                    # 如果有后续操作，执行它们
                    if then_actions and not self.should_stop:
                        self.log("执行ImgClick后续操作")
                        self.mainWork(then_actions)
                        self.log("ImgClick后续操作执行完毕")
                    
                    # 清理上下文
                    self._current_image_context = None
                else:
                    self.log("ImgClick: 未找到目标图片，跳过点击操作")
            
            elif cmdType == "ClickAfterImg":
                # 基于图片结果进行点击
                if hasattr(self, '_current_image_context') and self._current_image_context:
                    base_x = self._current_image_context['center_x']
                    base_y = self._current_image_context['center_y']
                    offset_x = cmdParam.get("x", 0)
                    offset_y = cmdParam.get("y", 0)
                    
                    target_x = base_x + offset_x
                    target_y = base_y + offset_y
                    
                    pyautogui.click(
                        x=target_x,
                        y=target_y,
                        clicks=cmdParam.get("clicks", 1),
                        interval=cmdParam.get("interval", 0),
                        button=cmdParam.get("button", "left")
                    )
                    self.log(f"基于图片结果点击位置: ({target_x}, {target_y}) [基准位置: ({base_x}, {base_y}), 偏移: ({offset_x}, {offset_y})]")
                else:
                    self.log("错误: ClickAfterImg命令需要在ImgClick命令之后执行")
            
            elif cmdType == "MoveToAfterImg":
                # 基于图片结果进行鼠标移动
                if hasattr(self, '_current_image_context') and self._current_image_context:
                    base_x = self._current_image_context['center_x']
                    base_y = self._current_image_context['center_y']
                    offset_x = cmdParam.get("x", 0)
                    offset_y = cmdParam.get("y", 0)
                    
                    target_x = base_x + offset_x
                    target_y = base_y + offset_y
                    
                    pyautogui.moveTo(
                        x=target_x,
                        y=target_y,
                        duration=cmdParam.get("duration", 0.25)
                    )
                    self.log(f"基于图片结果移动鼠标到: ({target_x}, {target_y}) [基准位置: ({base_x}, {base_y}), 偏移: ({offset_x}, {offset_y})]")
                else:
                    self.log("错误: MoveToAfterImg命令需要在ImgClick命令之后执行")
            
            elif cmdType == "DragToAfterImg":
                # 基于图片结果进行拖拽
                if hasattr(self, '_current_image_context') and self._current_image_context:
                    base_x = self._current_image_context['center_x']
                    base_y = self._current_image_context['center_y']
                    offset_x = cmdParam.get("x", 0)
                    offset_y = cmdParam.get("y", 0)
                    
                    target_x = base_x + offset_x
                    target_y = base_y + offset_y
                    
                    pyautogui.dragTo(
                        x=target_x,
                        y=target_y,
                        duration=cmdParam.get("duration", 0.25),
                        button=cmdParam.get("button", "left")
                    )
                    self.log(f"基于图片结果拖拽到: ({target_x}, {target_y}) [基准位置: ({base_x}, {base_y}), 偏移: ({offset_x}, {offset_y})]")
                else:
                    self.log("错误: DragToAfterImg命令需要在ImgClick命令之后执行")
            
            elif cmdType == "Write":
                pyautogui.write(
                    message=cmdParam.get("message"), 
                    interval=cmdParam.get("interval", 0.25)
                )
                self.log(f"输入文本: {cmdParam}")                                        
            
            elif cmdType == "Sleep":
                sleep_time = cmdParam
                self.log(f"等待 {sleep_time} 秒")
                if self.interruptible_sleep(sleep_time):
                    self.log(f"睡眠被中断")
                    break
            
            elif cmdType == "Scroll":
                pyautogui.scroll(cmdParam)
                self.log("滚轮操作")  
            
            elif cmdType == "KeyDown":
                if isinstance(cmdParam, dict):
                    key = cmdParam.get("key")
                    duration = cmdParam.get("duration", 0)
                    pyautogui.keyDown(key)
                    self.log(f"按下按键 {key} 持续 {duration} 秒")
                    if duration > 0:
                        if self.interruptible_sleep(duration):
                            pyautogui.keyUp(key)
                            break
                        pyautogui.keyUp(key)
                        self.log(f"自动释放按键 {key}")
                else:
                    pyautogui.keyDown(cmdParam)
                    self.log(f"按下按键 {cmdParam}")
            
            elif cmdType == "KeyUp":
                if isinstance(cmdParam, dict):
                    key = cmdParam.get("key")
                    pyautogui.keyUp(key)
                    self.log(f"释放按键 {key}")
                else:
                    pyautogui.keyUp(cmdParam)
                    self.log(f"释放按键 {cmdParam}")

            elif cmdType == "Press":
                pyautogui.press(
                    keys=cmdParam.get("keys"),
                    presses=cmdParam.get("presses", 1),
                    interval=cmdParam.get("interval", 0),
                )
                self.log(f"按键操作: {cmdParam}")
            
            elif cmdType == "ChineseWrite":
                pyperclip.copy(cmdParam)
                if self.interruptible_sleep(0.2):
                    break
                pyautogui.hotkey('ctrl', 'v')
                self.log(f"输入中文: {cmdParam}")
                
            i += 1
        
        self.is_running = False
        if self.should_stop:
            self.log("执行已停止")
        else:
            self.log("执行完成")

    def execute_once(self, data):
        """执行一次"""
        self.should_stop = False
        self._stop_event.clear()
        self.mainWork(data)
    
    def execute_loop(self, data):
        """循环执行"""
        self.should_stop = False
        self._stop_event.clear()
        loop_count = 0
        while not self.should_stop:
            loop_count += 1
            self.log(f"开始第 {loop_count} 次循环")
            self.mainWork(data)
            if not self.should_stop:
                if self.interruptible_sleep(0.1):
                    break
                self.log("等待0.1秒后继续下一次循环")
    
    def load_excel_file(self, excel_file_path):
        """加载Excel文件并转换为JSON格式"""
        if not excel_parser:
            self.log("错误: Excel解析模块不可用")
            return None
        
        try:
            self.log(f"正在加载Excel文件: {excel_file_path}")
            
            # 验证Excel文件格式
            is_valid, message = excel_parser.validate_excel_format(excel_file_path)
            if not is_valid:
                self.log(f"Excel文件格式验证失败: {message}")
                return None
            
            self.log(f"Excel文件格式验证通过: {message}")
            
            # 转换Excel为JSON
            json_data = excel_parser.excel_to_json(excel_file_path)
            
            self.log(f"Excel文件加载成功，包含 {len(json_data['data'])} 个命令")
            return json_data
            
        except Exception as e:
            self.log(f"加载Excel文件失败: {str(e)}")
            return None
    
    def execute_excel_once(self, excel_file_path):
        """从Excel文件执行一次"""
        json_data = self.load_excel_file(excel_file_path)
        if json_data:
            self.execute_once(json_data["data"])
        else:
            self.log("无法执行Excel文件：加载失败")
    
    def execute_excel_loop(self, excel_file_path):
        """从Excel文件循环执行"""
        json_data = self.load_excel_file(excel_file_path)
        if json_data:
            self.execute_loop(json_data["data"])
        else:
            self.log("无法执行Excel文件：加载失败")
    
    @staticmethod
    def create_excel_template(output_path="rpa_template.xlsx"):
        """创建Excel模板文件"""
        if not excel_parser:
            print("错误: Excel解析模块不可用")
            return None
        
        try:
            return excel_parser.create_excel_template(output_path)
        except Exception as e:
            print(f"创建Excel模板失败: {str(e)}")
            return None
    
    def __del__(self):
        """析构函数，清理OCR引擎和全局热键"""
        if hasattr(self, 'ocr_api') and self.ocr_api:
            try:
                self.ocr_api.exit()
            except:
                pass
        
        # 清理全局热键
        if global_hotkey_manager:
            global_hotkey_manager.unregister_hotkey(keyboard.Key.f10) 

    def find_image_on_screen(self, target_images, region=None):
        """在屏幕上查找目标图片"""
        if not target_images:
            self.log("错误: 没有指定目标图片")
            return None
            
        # 设置查找区域
        if region:
            # 获取屏幕尺寸
            screen_width, screen_height = pyautogui.size()
            
            # 预定义区域
            if region == 'left':
                search_region = (0, 0, screen_width//2, screen_height)
            elif region == 'right':
                search_region = (screen_width//2, 0, screen_width//2, screen_height)
            elif region == 'top':
                search_region = (0, 0, screen_width, screen_height//2)
            elif region == 'bottom':
                search_region = (0, screen_height//2, screen_width, screen_height//2)
            # 添加四个角落区域
            elif region == 'left_top' or region == 'top_left':
                search_region = (0, 0, screen_width//2, screen_height//2)
            elif region == 'right_top' or region == 'top_right':
                search_region = (screen_width//2, 0, screen_width//2, screen_height//2)
            elif region == 'left_bottom' or region == 'bottom_left':
                search_region = (0, screen_height//2, screen_width//2, screen_height//2)
            elif region == 'right_bottom' or region == 'bottom_right':
                search_region = (screen_width//2, screen_height//2, screen_width//2, screen_height//2)
            # 添加中间区域
            elif region == 'center':
                quarter_width = screen_width//4
                quarter_height = screen_height//4
                search_region = (quarter_width, quarter_height, quarter_width*2, quarter_height*2)
            # 自定义区域
            elif isinstance(region, list) and len(region) == 4:
                search_region = tuple(region)  # 自定义区域 [x, y, width, height]
            else:
                search_region = None
                self.log(f"无效的区域参数: {region}，将在全屏查找")
        else:
            search_region = None
        
        # 尝试查找每个目标图片
        for target_image in target_images:
            self.log(f"正在查找图片: {target_image}")
            try:
                location = pyautogui.locateCenterOnScreen(target_image, confidence=0.7, region=search_region)
                if location is not None:
                    self.log(f"找到目标图片 '{target_image}' 在位置: ({location.x}, {location.y})")
                    return {
                        "target": target_image,
                        "center_x": location.x,
                        "center_y": location.y,
                        "found": True
                    }
            except Exception as e:
                self.log(f"查找图片 '{target_image}' 时出错: {str(e)}")
        
        return None 