#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建新的Excel模板并测试解析
"""

import sys
import os
import json
sys.path.append(os.path.dirname(__file__))

from excel_parser import excel_parser

def main():
    print("🔧 创建新的Excel模板...")
    
    # 创建新模板
    template_path = "new_rpa_template.xlsx"
    excel_parser.create_excel_template(template_path)
    
    print(f"\n📊 测试解析新模板: {template_path}")
    
    # 测试解析新模板
    try:
        json_data = excel_parser.excel_to_json(template_path, "new_template_converted.json")
        
        if json_data:
            print("✅ 模板解析成功")
            print(f"📋 共解析 {len(json_data['data'])} 个命令")
            
            # 检查OCR命令是否正确解析
            for i, action in enumerate(json_data["data"]):
                cmd_type = action.get("cmdType", "")
                cmd_param = action.get("cmdParam", {})
                
                print(f"\n{i+1}. {cmd_type}:")
                print(f"   参数类型: {type(cmd_param).__name__}")
                
                if cmd_type == "OCR":
                    print(f"   参数内容: {cmd_param}")
                    if isinstance(cmd_param, dict):
                        if "target" in cmd_param and "then" in cmd_param:
                            print("   ✅ OCR结构正确")
                            if isinstance(cmd_param["then"], list):
                                print(f"   ✅ then字段是列表，包含 {len(cmd_param['then'])} 个后续操作")
                                for j, then_action in enumerate(cmd_param["then"]):
                                    if isinstance(then_action, dict):
                                        print(f"      {j+1}. {then_action.get('cmdType', 'Unknown')}")
                                    else:
                                        print(f"      {j+1}. 无效的后续操作: {then_action}")
                            else:
                                print("   ❌ then字段不是列表")
                        else:
                            print("   ❌ OCR结构不完整")
                    else:
                        print("   ❌ OCR参数不是字典")
                elif isinstance(cmd_param, dict):
                    print(f"   ✅ 参数解析为字典")
                elif isinstance(cmd_param, (int, float, str)):
                    print(f"   ✅ 参数解析为基本类型: {cmd_param}")
                else:
                    print(f"   ⚠️ 未知参数类型: {type(cmd_param)}")
            
            # 保存美化的JSON结果
            with open("template_result_pretty.json", 'w', encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=2)
            print(f"\n📄 美化的解析结果已保存到: template_result_pretty.json")
            
        else:
            print("❌ 模板解析失败")
            
    except Exception as e:
        print(f"❌ 解析过程中出错: {e}")
        import traceback
        traceback.print_exc()
    
    # 清理文件
    cleanup_files = [template_path, "new_template_converted.json"]
    print(f"\n🧹 清理临时文件...")
    for file_path in cleanup_files:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"🗑️ 已删除: {file_path}")
            except Exception as e:
                print(f"⚠️ 删除失败 {file_path}: {e}")

if __name__ == "__main__":
    main() 