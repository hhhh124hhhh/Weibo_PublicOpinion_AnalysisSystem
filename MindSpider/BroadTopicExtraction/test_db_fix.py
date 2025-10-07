#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试BroadTopicExtraction数据库修复
"""

import sys
from datetime import date
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

try:
    from BroadTopicExtraction.database_manager import DatabaseManager
except ImportError as e:
    print(f"导入模块失败: {e}")
    sys.exit(1)

def test_database_save():
    """测试数据库保存功能"""
    print("测试BroadTopicExtraction数据库保存功能...")
    
    try:
        # 初始化数据库管理器
        db = DatabaseManager()
        
        # 测试数据
        test_keywords = ["人工智能", "机器学习", "深度学习", "自然语言处理", "计算机视觉"]
        test_summary = "今日热点话题主要集中在人工智能技术发展及其应用领域。"
        
        # 测试保存功能
        print("正在保存测试数据...")
        result = db.save_daily_topics(test_keywords, test_summary, date.today())
        
        if result:
            print("✅ 数据库保存功能正常")
            
            # 验证数据是否正确保存
            saved_data = db.get_daily_topics(date.today())
            if saved_data and saved_data['keywords'] == test_keywords:
                print("✅ 数据正确保存并可查询")
                print(f"保存的关键词: {saved_data['keywords']}")
                print(f"保存的总结: {saved_data['summary']}")
            else:
                print("❌ 数据保存后查询失败")
        else:
            print("❌ 数据库保存功能异常")
            
        # 关闭数据库连接
        db.close()
        
    except Exception as e:
        print(f"❌ 测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_database_save()