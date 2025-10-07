#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的数据库连接测试
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.append(str(project_root))

print("当前工作目录:", os.getcwd())
print("项目根目录:", project_root)

try:
    import config
    print("✅ 成功导入config.py")
    print(f"数据库配置: {config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}")
except ImportError as e:
    print(f"❌ 导入config.py失败: {e}")
    sys.exit(1)

try:
    import pymysql
    print("✅ 成功导入pymysql")
except ImportError as e:
    print(f"❌ 导入pymysql失败: {e}")
    sys.exit(1)

try:
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
    cursor.execute("SELECT VERSION()")
    version = cursor.fetchone()
    print(f"数据库版本: {version[0]}")
    
    connection.close()
    print("✅ 数据库测试完成")
    
except Exception as e:
    print(f"❌ 数据库连接失败: {e}")