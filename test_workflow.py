#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试MindSpider完整工作流程
"""

import sys
from datetime import date
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.append(str(project_root))

def test_broad_topic_extraction():
    """测试话题提取模块"""
    print("测试BroadTopicExtraction模块...")
    
    try:
        # 导入BroadTopicExtraction模块
        from MindSpider.BroadTopicExtraction.main import BroadTopicExtraction
        
        # 创建实例并测试
        extractor = BroadTopicExtraction()
        print("✅ BroadTopicExtraction模块导入成功")
        
        # 测试数据库连接
        if extractor.db_manager.connection:
            print("✅ 数据库连接正常")
        else:
            print("❌ 数据库连接异常")
            return False
            
        extractor.close()
        return True
        
    except Exception as e:
        print(f"❌ 测试BroadTopicExtraction模块时发生错误: {e}")
        return False

def test_deep_sentiment_crawling():
    """测试深度情感爬取模块"""
    print("测试DeepSentimentCrawling模块...")
    
    try:
        # 导入DeepSentimentCrawling模块
        from MindSpider.DeepSentimentCrawling.main import DeepSentimentCrawling
        
        # 创建实例并测试
        crawler = DeepSentimentCrawling()
        print("✅ DeepSentimentCrawling模块导入成功")
        
        # 测试数据库连接
        if crawler.keyword_manager.connection:
            print("✅ 关键词管理器数据库连接正常")
        else:
            print("❌ 关键词管理器数据库连接异常")
            return False
            
        crawler.close()
        return True
        
    except Exception as e:
        print(f"❌ 测试DeepSentimentCrawling模块时发生错误: {e}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("MindSpider工作流程测试")
    print("=" * 60)
    
    # 测试BroadTopicExtraction模块
    if test_broad_topic_extraction():
        print("✅ BroadTopicExtraction模块测试通过\n")
    else:
        print("❌ BroadTopicExtraction模块测试失败\n")
        return
    
    # 测试DeepSentimentCrawling模块
    if test_deep_sentiment_crawling():
        print("✅ DeepSentimentCrawling模块测试通过\n")
    else:
        print("❌ DeepSentimentCrawling模块测试失败\n")
        return
    
    print("=" * 60)
    print("所有模块测试通过！")
    print("现在可以开始测试平台爬取了。")
    print("例如：")
    print("  cd MindSpider")
    print("  python main.py --deep-sentiment --platforms xhs --test")
    print("=" * 60)

if __name__ == "__main__":
    main()