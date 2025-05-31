import pandas as pd
import json
import os
from datetime import datetime

class ExcelParser:
    def __init__(self):
        self.supported_cmd_types = [
            "Click", "MoveTo", "DragTo", "ImgClick", "Write", "ChineseWrite",
            "Sleep", "Scroll", "KeyDown", "KeyUp", "Press", "ShutDown",
            "OCR", "ClickAfterOCR", "MoveToAfterOCR", "DragToAfterOCR"
        ]
    
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
        
        try:
            # 尝试解析为JSON
            if param_str.startswith('{') and param_str.endswith('}'):
                return json.loads(param_str)
            
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
            
            elif cmd_type == "ImgClick":
                # 图片点击参数
                return {
                    "imgPath": param_str,
                    "button": "left",
                    "reTry": 1
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
                    target_list = json.loads(param_str)
                    return {"target": target_list, "then": []}
                else:
                    return {"target": [param_str], "then": []}
            
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
            
        except json.JSONDecodeError:
            print(f"警告: 第{row_num}行参数JSON格式错误，使用原始字符串: {param_str}")
            return param_str
        except Exception as e:
            print(f"警告: 第{row_num}行参数解析失败: {str(e)}")
            return param_str
    
    def create_excel_template(self, output_path="rpa_template.xlsx"):
        """创建Excel模板文件"""
        try:
            # 创建示例数据
            template_data = [
                {
                    "cmdType": "Click",
                    "cmdParam": '{"x": 100, "y": 200, "clicks": 1, "button": "left"}',
                    "说明": "点击坐标(100,200)"
                },
                {
                    "cmdType": "Sleep",
                    "cmdParam": "2",
                    "说明": "等待2秒"
                },
                {
                    "cmdType": "Write",
                    "cmdParam": '{"message": "Hello World", "interval": 0.01}',
                    "说明": "输入文本"
                },
                {
                    "cmdType": "ChineseWrite",
                    "cmdParam": "你好世界",
                    "说明": "输入中文文本"
                },
                {
                    "cmdType": "Press",
                    "cmdParam": '{"keys": "enter", "presses": 1}',
                    "说明": "按回车键"
                },
                {
                    "cmdType": "ImgClick",
                    "cmdParam": '{"imgPath": "button.jpg", "button": "left", "reTry": 3}',
                    "说明": "点击图片按钮"
                },
                {
                    "cmdType": "Scroll",
                    "cmdParam": "3",
                    "说明": "向上滚动3格"
                },
                {
                    "cmdType": "MoveTo",
                    "cmdParam": '{"x": 300, "y": 400, "duration": 0.5}',
                    "说明": "移动鼠标到指定位置"
                },
                {
                    "cmdType": "DragTo",
                    "cmdParam": '{"x": 500, "y": 600, "duration": 1.0, "button": "left"}',
                    "说明": "拖拽到指定位置"
                },
                {
                    "cmdType": "OCR",
                    "cmdParam": '{"target": ["File", "文件"], "then": []}',
                    "说明": "OCR识别文本"
                },
                {
                    "cmdType": "ClickAfterOCR",
                    "cmdParam": '{"x": 10, "y": 20, "clicks": 1, "button": "left"}',
                    "说明": "基于OCR结果点击(相对偏移)"
                }
            ]
            
            # 创建DataFrame
            df = pd.DataFrame(template_data)
            
            # 保存为Excel文件
            with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='RPA命令', index=False)
                
                # 获取工作表对象以设置列宽
                worksheet = writer.sheets['RPA命令']
                worksheet.column_dimensions['A'].width = 15  # cmdType列
                worksheet.column_dimensions['B'].width = 50  # cmdParam列
                worksheet.column_dimensions['C'].width = 30  # 说明列
            
            print(f"✅ Excel模板已创建: {output_path}")
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