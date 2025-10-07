#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查小红书爬取数据
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
    
    # 检查小红书相关表
    cursor.execute("SHOW TABLES LIKE 'xhs_%'")
    results = cursor.fetchall()
    print("小红书相关数据表:")
    for table in results:
        print(f"  - {table[0]}")
    
    # 检查小红书笔记数量
    try:
        cursor.execute("SELECT COUNT(*) FROM xhs_note")
        count = cursor.fetchone()[0]
        print(f"小红书笔记数量: {count}")
    except Exception as e:
        print(f"查询小红书笔记数量失败: {e}")
    
    # 检查小红书评论数量
    try:
        cursor.execute("SELECT COUNT(*) FROM xhs_note_comment")
        count = cursor.fetchone()[0]
        print(f"小红书评论数量: {count}")
    except Exception as e:
        print(f"查询小红书评论数量失败: {e}")
    
    connection.close()
    print("✅ 数据库连接已关闭")
    
except Exception as e:
    print(f"❌ 发生错误: {e}")
    import traceback
    traceback.print_exc()