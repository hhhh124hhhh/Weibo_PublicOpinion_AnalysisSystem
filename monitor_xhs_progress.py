#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
监控小红书爬取进度
"""

import time
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.append(str(project_root))

try:
    import config
    import pymysql
    print("✅ 监控脚本启动...")
    
    # 连接数据库
    connection = pymysql.connect(
        host=config.DB_HOST,
        port=config.DB_PORT,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        database=config.DB_NAME,
        charset=config.DB_CHARSET
    )
    
    cursor = connection.cursor()
    
    print("开始监控小红书数据爬取进度...")
    print("按 Ctrl+C 停止监控")
    print("-" * 50)
    
    while True:
        try:
            # 检查小红书笔记数量
            cursor.execute("SELECT COUNT(*) FROM xhs_note")
            result = cursor.fetchone()
            note_count = result[0] if result else 0
            
            # 检查小红书评论数量
            cursor.execute("SELECT COUNT(*) FROM xhs_note_comment")
            result = cursor.fetchone()
            comment_count = result[0] if result else 0
            
            print(f"小红书笔记数量: {note_count} | 评论数量: {comment_count}")
            
            # 每5秒检查一次
            time.sleep(5)
            
        except KeyboardInterrupt:
            print("\n停止监控...")
            break
        except Exception as e:
            print(f"监控过程中发生错误: {e}")
            time.sleep(5)
    
    connection.close()
    print("监控结束")
    
except Exception as e:
    print(f"❌ 启动监控失败: {e}")