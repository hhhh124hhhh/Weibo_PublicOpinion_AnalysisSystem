#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查数据库状态和话题数据
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.append(str(project_root))

try:
    import config
    import pymysql
    print("✅ 成功导入配置和数据库模块")
    
    # 连接数据库
    connection = pymysql.connect(
        host=config.DB_HOST,
        port=config.DB_PORT,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        database=config.DB_NAME,
        charset=config.DB_CHARSET
    )
    print("✅ 数据库连接成功")
    
    cursor = connection.cursor()
    
    # 检查表是否存在
    cursor.execute("SHOW TABLES LIKE 'daily_topics'")
    result = cursor.fetchone()
    if result:
        print("✅ daily_topics表存在")
        
        # 检查话题数据
        cursor.execute("SELECT COUNT(*) FROM daily_topics")
        count = cursor.fetchone()[0]
        print(f"📊 话题数据数量: {count}")
        
        if count > 0:
            # 显示最近的话题数据
            cursor.execute("SELECT topic_id, extract_date FROM daily_topics ORDER BY extract_date DESC LIMIT 5")
            results = cursor.fetchall()
            print("📅 最近的话题数据:")
            for row in results:
                print(f"   {row[0]} - {row[1]}")
        else:
            print("⚠️  暂无话题数据，请先运行BroadTopicExtraction模块")
    else:
        print("❌ daily_topics表不存在，请初始化数据库")
    
    # 检查其他关键表
    cursor.execute("SHOW TABLES LIKE 'daily_news'")
    result = cursor.fetchone()
    if result:
        print("✅ daily_news表存在")
        
        cursor.execute("SELECT COUNT(*) FROM daily_news")
        count = cursor.fetchone()[0]
        print(f"📊 新闻数据数量: {count}")
    else:
        print("❌ daily_news表不存在")
    
    connection.close()
    print("✅ 数据库连接已关闭")
    
except Exception as e:
    print(f"❌ 发生错误: {e}")