import config
import pymysql

def check_table_structure():
    try:
        conn = pymysql.connect(
            host=config.DB_HOST,
            port=config.DB_PORT,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            database=config.DB_NAME
        )
        cursor = conn.cursor()
        cursor.execute("DESCRIBE daily_topics")
        result = cursor.fetchall()
        print('daily_topics表结构:')
        for row in result:
            print(row)
        conn.close()
    except Exception as e:
        print(f"检查表结构失败: {e}")

if __name__ == "__main__":
    check_table_structure()