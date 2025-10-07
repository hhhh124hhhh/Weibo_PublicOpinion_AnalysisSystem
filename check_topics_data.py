import config
import pymysql
import json

def check_topics_data():
    try:
        conn = pymysql.connect(
            host=config.DB_HOST,
            port=config.DB_PORT,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            database=config.DB_NAME
        )
        cursor = conn.cursor()
        cursor.execute("SELECT topic_id, topic_name, extract_date, keywords FROM daily_topics LIMIT 1")
        result = cursor.fetchone()
        
        if result:
            print('话题ID:', result[0])
            print('话题名称:', result[1])
            print('提取日期:', result[2])
            keywords = json.loads(result[3]) if result[3] else []
            print('关键词数量:', len(keywords))
            print('部分关键词:', keywords[:5])
        else:
            print('暂无话题数据')
            
        conn.close()
    except Exception as e:
        print(f"检查话题数据失败: {e}")

if __name__ == "__main__":
    check_topics_data()