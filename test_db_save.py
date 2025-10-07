import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from MindSpider.BroadTopicExtraction.database_manager import DatabaseManager
from datetime import date

def test_db_save():
    """测试数据库保存功能"""
    print("测试数据库保存功能...")
    
    # 测试数据
    test_keywords = ["测试关键词1", "测试关键词2", "测试关键词3"]
    test_summary = "这是一个测试总结，用于验证数据库保存功能是否正常工作。"
    
    try:
        # 创建数据库管理器实例
        db = DatabaseManager()
        
        # 保存测试数据
        print("正在保存测试数据...")
        success = db.save_daily_topics(test_keywords, test_summary, date.today())
        
        if success:
            print("✅ 数据保存成功!")
            
            # 验证数据是否保存
            print("正在验证保存的数据...")
            result = db.get_daily_topics(date.today())
            if result:
                print(f"✅ 数据验证成功!")
                print(f"   关键词: {result['keywords']}")
                print(f"   总结: {result['summary']}")
                print(f"   话题ID: {result['topic_id']}")
            else:
                print("❌ 数据验证失败: 无法查询到保存的数据")
        else:
            print("❌ 数据保存失败!")
            
        # 关闭数据库连接
        db.close()
        
    except Exception as e:
        print(f"❌ 测试过程中发生错误: {e}")

if __name__ == "__main__":
    test_db_save()