import pandas as pd
import json
import os
from datetime import datetime


# JSON转换工具函数
def json_to_string(json_obj):
    """将JSON对象转换为紧凑的字符串格式，用于Excel中的cmdParam字段"""
    return json.dumps(json_obj, ensure_ascii=False, separators=(',', ':'))

def json_to_excel(json_data, output_excel_path=None):
    """
    将JSON数据导出为Excel文件
    
    Args:
        json_data: JSON数据(字典或文件路径)
        output_excel_path: 输出Excel文件路径，如果为None则自动生成
        
    Returns:
        str: 生成的Excel文件路径
    """
    try:
        # 如果输入是文件路径，先读取JSON文件
        if isinstance(json_data, str):
            if os.path.isfile(json_data):
                with open(json_data, 'r', encoding='utf-8') as f:
                    json_data = json.load(f)
            else:
                raise ValueError(f"找不到JSON文件: {json_data}")
        
        # 确保json_data是字典格式
        if not isinstance(json_data, dict):
            raise ValueError("JSON数据必须是字典格式")
        
        # 确保包含"data"字段
        if "data" not in json_data:
            if isinstance(json_data, list):
                # 如果是列表，直接使用
                actions = json_data
            else:
                raise ValueError("JSON数据格式不正确，缺少'data'字段")
        else:
            # 从JSON数据中提取actions列表
            actions = json_data["data"]
        
        # 创建Excel数据
        excel_data = []
        for action in actions:
            if not isinstance(action, dict):
                continue
                
            cmd_type = action.get("cmdType", "")
            cmd_param = action.get("cmdParam", {})
            
            # 将cmdParam转换为字符串格式
            if isinstance(cmd_param, (dict, list)):
                cmd_param_str = json.dumps(cmd_param, ensure_ascii=False, indent=2)
            else:
                cmd_param_str = str(cmd_param)
            
            excel_data.append({
                "cmdType": cmd_type,
                "cmdParam": cmd_param_str,
                "说明": ""  # 添加一个空的说明列
            })
        
        # 创建DataFrame
        df = pd.DataFrame(excel_data)
        
        # 如果没有指定输出路径，生成一个默认路径
        if output_excel_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_excel_path = f"rpa_export_{timestamp}.xlsx"
        
        # 保存为Excel文件
        with pd.ExcelWriter(output_excel_path, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='RPA命令', index=False)
            
            # 获取工作表对象以设置列宽和行高
            worksheet = writer.sheets['RPA命令']
            worksheet.column_dimensions['A'].width = 15  # cmdType列
            worksheet.column_dimensions['B'].width = 100  # cmdParam列 - 增加宽度以容纳多行JSON
            worksheet.column_dimensions['C'].width = 35  # 说明列
            
            # 设置文本换行
            from openpyxl.styles import Alignment
            for row_num in range(2, len(excel_data) + 2):
                cell = worksheet[f'B{row_num}']  # cmdParam列
                cell.alignment = Alignment(wrap_text=True, vertical='top')
        
        print(f"✅ JSON数据已成功导出为Excel: {output_excel_path}")
        print(f"📊 共导出了 {len(excel_data)} 个操作")
        
        return output_excel_path
        
    except Exception as e:
        print(f"❌ 导出Excel失败: {str(e)}")
        raise

class ExcelParser:
    def __init__(self):
        self.supported_cmd_types = [
            "Click", "MoveTo", "DragTo", "ImgClick", "Write", "ChineseWrite",
            "Sleep", "Scroll", "KeyDown", "KeyUp", "Press", "ShutDown",
            "OCR", "ClickAfterOCR", "MoveToAfterOCR", "DragToAfterOCR",
            "SearchImage", "ClickAfterImg", "MoveToAfterImg", "DragToAfterImg"
        ]
    
    def json_to_excel(self, json_data, output_excel_path=None):
        """
        将JSON数据导出为Excel文件 (类方法)
        
        Args:
            json_data: JSON数据(字典或文件路径)
            output_excel_path: 输出Excel文件路径，如果为None则自动生成
            
        Returns:
            str: 生成的Excel文件路径
        """
        return json_to_excel(json_data, output_excel_path)
    
    def excel_to_json(self, excel_file_path, output_json_path=None):
        """
        将Excel文件转换为JSON格式
        
        Args:
            excel_file_path: Excel文件路径
            output_json_path: 输出JSON文件路径，如果为None则自动生成
            
        Returns:
            dict: 转换后的JSON数据
        """
        try:
            # 读取Excel文件
            df = pd.read_excel(excel_file_path, sheet_name=0)
            
            # 验证必要的列
            required_columns = ['cmdType', 'cmdParam']
            for col in required_columns:
                if col not in df.columns:
                    raise ValueError(f"Excel文件缺少必要的列: {col}")
            
            # 转换数据
            actions = []
            for index, row in df.iterrows():
                try:
                    cmd_type = str(row['cmdType']).strip()
                    cmd_param_str = str(row['cmdParam']).strip()
                    
                    # 跳过空行
                    if pd.isna(row['cmdType']) or cmd_type == '' or cmd_type == 'nan':
                        continue
                    
                    # 验证命令类型
                    if cmd_type not in self.supported_cmd_types:
                        print(f"警告: 第{index+2}行包含不支持的命令类型: {cmd_type}")
                        continue
                    
                    # 解析参数
                    cmd_param = self._parse_cmd_param(cmd_type, cmd_param_str, index + 2)
                    
                    action = {
                        "cmdType": cmd_type,
                        "cmdParam": cmd_param
                    }
                    
                    actions.append(action)
                    
                except Exception as e:
                    print(f"警告: 第{index+2}行数据解析失败: {str(e)}")
                    continue
            
            # 构建最终的JSON结构
            json_data = {
                "data": actions,
                "metadata": {
                    "source": "excel",
                    "source_file": os.path.basename(excel_file_path),
                    "converted_at": datetime.now().isoformat(),
                    "total_actions": len(actions)
                }
            }
            
            # 保存JSON文件
            if output_json_path is None:
                base_name = os.path.splitext(excel_file_path)[0]
                output_json_path = f"{base_name}_converted.json"
            
            with open(output_json_path, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ Excel文件已成功转换为JSON: {output_json_path}")
            print(f"📊 共转换了 {len(actions)} 个操作")
            
            return json_data
            
        except Exception as e:
            print(f"❌ Excel转换失败: {str(e)}")
            raise
    
    def _parse_cmd_param(self, cmd_type, param_str, row_num):
        """解析命令参数"""
        if pd.isna(param_str) or param_str == '' or param_str == 'nan':
            param_str = '{}'
        
        # 转换为字符串并进行初步清理
        param_str = str(param_str).strip()
        
        # 处理三引号字符串格式 - 移除三引号标记
        if param_str.startswith("'''") and param_str.endswith("'''"):
            param_str = param_str[3:-3].strip()
        elif param_str.startswith('"""') and param_str.endswith('"""'):
            param_str = param_str[3:-3].strip()
        
        # 对于JSON格式，智能处理换行符和空白字符
        if param_str.startswith('{') and param_str.endswith('}'):
            # 对于多行JSON，保留结构但规范化空白字符
            # 移除Excel单元格中的\r字符，但保留\n用于JSON结构
            param_str = param_str.replace('\r', '')
            # 不要简单地移除所有\n，因为这会破坏多行JSON的可读性
            # 只在必要时进行JSON压缩
        else:
            # 对于非JSON格式，清理所有换行符
            param_str = param_str.replace('\r', '').replace('\n', ' ').strip()
        
        # 如果清理后为空，设置默认值
        if not param_str:
            param_str = '{}'
        
        try:
            # 尝试解析为JSON
            if param_str.startswith('{') and param_str.endswith('}'):
                try:
                    return json.loads(param_str)
                except json.JSONDecodeError as e:
                    print(f"警告: 第{row_num}行JSON解析失败: {str(e)}")
                    print(f"原始参数: {repr(param_str[:200])}...")  # 只显示前200个字符
                    # JSON解析失败时，尝试修复常见问题
                    fixed_param = self._try_fix_json(param_str)
                    if fixed_param:
                        try:
                            return json.loads(fixed_param)
                        except:
                            pass
                    # 如果修复失败，返回原始字符串
                    return param_str
            
            # 根据命令类型进行特殊处理
            if cmd_type == "Sleep":
                return float(param_str)
            
            elif cmd_type == "Scroll":
                return int(param_str)
            
            elif cmd_type == "ChineseWrite":
                return param_str
            
            elif cmd_type in ["Click", "MoveTo", "DragTo"]:
                # 尝试解析坐标格式: "100,200" 或 "x:100,y:200"
                if ',' in param_str:
                    parts = param_str.split(',')
                    if len(parts) >= 2:
                        try:
                            x = int(parts[0].split(':')[-1].strip())
                            y = int(parts[1].split(':')[-1].strip())
                            result = {"x": x, "y": y}
                            
                            # 添加其他可能的参数
                            if cmd_type == "Click":
                                result.update({"clicks": 1, "interval": 0, "button": "left"})
                            elif cmd_type == "DragTo":
                                result.update({"duration": 0.25, "button": "left"})
                            elif cmd_type == "MoveTo":
                                result.update({"duration": 0.25})
                            
                            return result
                        except ValueError:
                            pass
            
            elif cmd_type == "SearchImage":
                # 图片搜索参数，支持新的target格式
                if param_str.startswith('[') and param_str.endswith(']'):
                    # 简单的target数组格式: ["button.jpg", "button_alt.jpg"]
                    try:
                        target_list = json.loads(param_str)
                        return {
                            "target": target_list,
                            "waitForTarget": False,
                            "detecttime": 0.5,
                            "maxWaitTime": 30
                        }
                    except json.JSONDecodeError:
                        # 解析失败，作为简单文本处理
                        return {
                            "target": [param_str],
                            "waitForTarget": False,
                            "detecttime": 0.5,
                            "maxWaitTime": 30
                        }
                elif param_str.startswith('{') and param_str.endswith('}'):
                    # 完整的JSON格式，直接解析
                    try:
                        search_params = json.loads(param_str)
                        # 确保包含默认值
                        if "waitForTarget" not in search_params:
                            search_params["waitForTarget"] = False
                        if "detecttime" not in search_params:
                            search_params["detecttime"] = 0.5
                        if "maxWaitTime" not in search_params:
                            search_params["maxWaitTime"] = 30
                        return search_params
                    except json.JSONDecodeError:
                        # JSON解析失败，作为简单文本处理
                        return {
                            "target": [param_str],
                            "waitForTarget": False,
                            "detecttime": 0.5,
                            "maxWaitTime": 30
                        }
                else:
                    # 简单文本格式，单个图片路径
                    return {
                        "target": [param_str],
                        "waitForTarget": False,
                        "detecttime": 0.5,
                        "maxWaitTime": 30
                    }
            
            elif cmd_type == "ImgClick":
                # 图片点击参数，支持新的target格式和旧的imgPath格式
                if param_str.startswith('[') and param_str.endswith(']'):
                    # 简单的target数组格式: ["button.jpg", "button_alt.jpg"]
                    try:
                        target_list = json.loads(param_str)
                        return {
                            "target": target_list,
                            "waitForTarget": False,
                            "detecttime": 0.5,
                            "maxWaitTime": 30,
                            "clicks": 1,
                            "button": "left",
                            "then": []
                        }
                    except json.JSONDecodeError:
                        # 解析失败，作为旧格式处理
                        return {
                            "imgPath": param_str,
                            "button": "left",
                            "reTry": 1
                        }
                elif param_str.startswith('{') and param_str.endswith('}'):
                    # 完整的JSON格式，直接解析
                    try:
                        img_params = json.loads(param_str)
                        # 如果包含target参数，则使用新格式
                        if "target" in img_params:
                            # 确保包含默认值
                            if "waitForTarget" not in img_params:
                                img_params["waitForTarget"] = False
                            if "detecttime" not in img_params:
                                img_params["detecttime"] = 0.5
                            if "maxWaitTime" not in img_params:
                                img_params["maxWaitTime"] = 30
                            if "clicks" not in img_params:
                                img_params["clicks"] = 1
                            if "button" not in img_params:
                                img_params["button"] = "left"
                            if "then" not in img_params:
                                img_params["then"] = []
                            return img_params
                        else:
                            # 旧格式，包含imgPath参数
                            if "button" not in img_params:
                                img_params["button"] = "left"
                            if "reTry" not in img_params:
                                img_params["reTry"] = 1
                            return img_params
                    except json.JSONDecodeError:
                        # JSON解析失败，作为简单文本处理（旧格式）
                        return {
                            "imgPath": param_str,
                            "button": "left",
                            "reTry": 1
                        }
                else:
                    # 简单文本格式，可能是图片路径或新格式target
                    # 优先使用新格式
                    return {
                        "target": [param_str],
                        "waitForTarget": False,
                        "detecttime": 0.5,
                        "maxWaitTime": 30,
                        "clicks": 1,
                        "button": "left",
                        "then": []
                    }
            
            elif cmd_type == "Write":
                return {
                    "message": param_str,
                    "interval": 0.01
                }
            
            elif cmd_type in ["KeyDown", "KeyUp"]:
                return param_str
            
            elif cmd_type == "Press":
                return {
                    "keys": param_str,
                    "presses": 1,
                    "interval": 0
                }
            
            elif cmd_type == "ShutDown":
                try:
                    timeout = int(param_str) if param_str.isdigit() else 10
                    return {"timeout": timeout}
                except:
                    return {"timeout": 10}
            
            elif cmd_type == "OCR":
                # OCR参数需要特殊处理
                if param_str.startswith('[') and param_str.endswith(']'):
                    # 简单的target数组格式: ["File", "文件"]
                    target_list = json.loads(param_str)
                    return {
                        "target": target_list, 
                        "then": [],
                        "waitForTarget": False,
                        "detecttime": 0.5,
                        "maxWaitTime": 30
                    }
                elif param_str.startswith('{') and param_str.endswith('}'):
                    # 完整的JSON格式，直接解析
                    try:
                        ocr_params = json.loads(param_str)
                        # 确保包含默认值
                        if "waitForTarget" not in ocr_params:
                            ocr_params["waitForTarget"] = False
                        if "detecttime" not in ocr_params:
                            ocr_params["detecttime"] = 0.5
                        if "maxWaitTime" not in ocr_params:
                            ocr_params["maxWaitTime"] = 30
                        if "then" not in ocr_params:
                            ocr_params["then"] = []
                        return ocr_params
                    except json.JSONDecodeError:
                        # JSON解析失败，作为简单文本处理
                        return {
                            "target": [param_str], 
                            "then": [],
                            "waitForTarget": False,
                            "detecttime": 0.5,
                            "maxWaitTime": 30
                        }
                else:
                    # 简单文本格式
                    return {
                        "target": [param_str], 
                        "then": [],
                        "waitForTarget": False,
                        "detecttime": 0.5,
                        "maxWaitTime": 30
                    }
            
            elif cmd_type in ["ClickAfterImg", "MoveToAfterImg", "DragToAfterImg"]:
                # 解析基于图片的偏移坐标
                if ',' in param_str:
                    parts = param_str.split(',')
                    if len(parts) >= 2:
                        try:
                            x = int(parts[0].split(':')[-1].strip())
                            y = int(parts[1].split(':')[-1].strip())
                            result = {"x": x, "y": y}
                            
                            if cmd_type == "ClickAfterImg":
                                result.update({"clicks": 1, "interval": 0, "button": "left"})
                            elif cmd_type in ["MoveToAfterImg", "DragToAfterImg"]:
                                result.update({"duration": 0.25})
                                if cmd_type == "DragToAfterImg":
                                    result.update({"button": "left"})
                            
                            return result
                        except ValueError:
                            pass
            
            elif cmd_type in ["ClickAfterOCR", "MoveToAfterOCR", "DragToAfterOCR"]:
                # 解析偏移坐标
                if ',' in param_str:
                    parts = param_str.split(',')
                    if len(parts) >= 2:
                        try:
                            x = int(parts[0].split(':')[-1].strip())
                            y = int(parts[1].split(':')[-1].strip())
                            result = {"x": x, "y": y}
                            
                            if cmd_type == "ClickAfterOCR":
                                result.update({"clicks": 1, "interval": 0, "button": "left"})
                            elif cmd_type in ["MoveToAfterOCR", "DragToAfterOCR"]:
                                result.update({"duration": 0.25})
                                if cmd_type == "DragToAfterOCR":
                                    result.update({"button": "left"})
                            
                            return result
                        except ValueError:
                            pass
            
            # 默认返回字符串参数
            return param_str
            
        except Exception as e:
            print(f"警告: 第{row_num}行参数解析失败: {str(e)}")
            return param_str
    
    def _try_fix_json(self, json_str):
        """尝试修复常见的JSON格式问题"""
        try:
            import re
            
            # 移除首尾空白
            fixed = json_str.strip()
            
            # 修复数组末尾的多余逗号: [item1, item2, ] -> [item1, item2]
            fixed = re.sub(r',\s*]', ']', fixed)
            
            # 修复对象末尾的多余逗号: {key1: value1, key2: value2, } -> {key1: value1, key2: value2}
            fixed = re.sub(r',\s*}', '}', fixed)
            
            # 修复属性名没有引号的问题: {key: value} -> {"key": value}
            # 但要小心不要影响已经有引号的属性名
            fixed = re.sub(r'(\w+)(\s*:\s*)', r'"\1"\2', fixed)
            
            # 修复字符串值没有引号的问题（只处理简单情况）
            # 这个比较复杂，暂时跳过，因为可能误判数字和布尔值
            
            return fixed
        except Exception as e:
            print(f"JSON修复失败: {e}")
            return None
    
    def create_excel_template(self, output_path="rpa_template.xlsx"):
        """创建Excel模板文件"""
        try:
            # 创建示例数据
            template_data = [
                {
                    "cmdType": "Click",
                    "cmdParam": '''{"x": 100, "y": 200, "clicks": 1, "button": "left"}''',
                    "说明": "点击坐标(100,200)"
                },
                {
                    "cmdType": "Sleep",
                    "cmdParam": "2",
                    "说明": "等待2秒"
                },
                {
                    "cmdType": "Write",
                    "cmdParam": '''{"message": "Hello World", "interval": 0.01}''',
                    "说明": "输入文本"
                },
                {
                    "cmdType": "ChineseWrite",
                    "cmdParam": "你好世界",
                    "说明": "输入中文文本"
                },
                {
                    "cmdType": "Press",
                    "cmdParam": '''{"keys": "enter", "presses": 1}''',
                    "说明": "按回车键"
                },
                {
                    "cmdType": "SearchImage",
                    "cmdParam": '''{
    "target": ["test.png"],
    "waitForTarget": true,
    "detecttime": 0.5,
    "maxWaitTime": 30,
    "then": [
        {
            "cmdType": "ClickAfterImg",
            "cmdParam": {"x": 0, "y": 0}
        }
    ]
}''',
                    "说明": "搜索图片"
                },
                {
                    "cmdType": "Scroll",
                    "cmdParam": "3",
                    "说明": "向上滚动3格"
                },
                {
                    "cmdType": "MoveTo",
                    "cmdParam": '''{"x": 300, "y": 400, "duration": 0.5}''',
                    "说明": "移动鼠标到指定位置"
                },
                {
                    "cmdType": "DragTo",
                    "cmdParam": '''{"x": 500, "y": 600, "duration": 1.0, "button": "left"}''',
                    "说明": "拖拽到指定位置"
                },
                {
                    "cmdType": "OCR",
                    "cmdParam": '''{
    "target": ["File", "文件"], 
    "waitForTarget": true, 
    "detecttime": 0.5, 
    "maxWaitTime": 30, 
    "then": [
        {
            "cmdType": "ClickAfterOCR", 
            "cmdParam": {"x": 10, "y": 20}
        }
    ]
}''',
                    "说明": "OCR等待检测模式：持续检测直到找到目标文本"
                    },
                {
                    "cmdType": "OCR", 
                    "cmdParam": '''{
    "target": ["确定", "OK"], 
    "waitForTarget": false, 
    "then": [
        {
            "cmdType": "ClickAfterOCR", 
            "cmdParam": {"x": 0, "y": 0}
        }
    ]
}''',
                    "说明": "OCR单次检测模式：检测一次后继续"
                },
                {
                    "cmdType": "ClickAfterImg",
                    "cmdParam": '''{"x": 0, "y": 0, "clicks": 1, "button": "left"}''',
                    "说明": "基于找到的图片进行点击"
                },
                {
                    "cmdType": "ImgClick",
                    "cmdParam": '''{
    "target": ["test.jpg"], 
    "waitForTarget": true, 
    "detecttime": 0.5, 
    "maxWaitTime": 30
}''',
                    "说明": "点击图片按钮(兼容模式)"
                },
            ]
            
            # 创建DataFrame
            df = pd.DataFrame(template_data)
            
            # 保存为Excel文件
            with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='RPA命令', index=False)
                
                # 获取工作表对象以设置列宽和行高
                worksheet = writer.sheets['RPA命令']
                worksheet.column_dimensions['A'].width = 15  # cmdType列
                worksheet.column_dimensions['B'].width = 100  # cmdParam列 - 增加宽度以容纳多行JSON
                worksheet.column_dimensions['C'].width = 35  # 说明列
                
                
                # 设置文本换行
                from openpyxl.styles import Alignment
                for row_num in range(2, len(template_data) + 2):
                    cell = worksheet[f'B{row_num}']  # cmdParam列
                    cell.alignment = Alignment(wrap_text=True, vertical='top')
            
            print(f"✅ Excel模板已创建: {output_path}")
            print("📝 复杂的JSON参数已格式化为多行显示，提高可读性")
            return output_path
            
        except Exception as e:
            print(f"❌ 创建Excel模板失败: {str(e)}")
            raise
    
    def validate_excel_format(self, excel_file_path):
        """验证Excel文件格式"""
        try:
            df = pd.read_excel(excel_file_path, sheet_name=0)
            
            # 检查必要的列
            required_columns = ['cmdType', 'cmdParam']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                return False, f"缺少必要的列: {', '.join(missing_columns)}"
            
            # 检查是否有有效数据
            valid_rows = 0
            for index, row in df.iterrows():
                if not pd.isna(row['cmdType']) and str(row['cmdType']).strip() != '':
                    valid_rows += 1
            
            if valid_rows == 0:
                return False, "Excel文件中没有有效的命令数据"
            
            return True, f"格式正确，包含 {valid_rows} 个有效命令"
            
        except Exception as e:
            return False, f"文件读取失败: {str(e)}"

# 创建全局实例
excel_parser = ExcelParser() 