#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BroadTopicExtraction模块 - 新闻获取和收集
整合新闻API调用和数据库存储功能
"""

import sys
import asyncio
import httpx
import json
from datetime import datetime, date
from pathlib import Path
from typing import List, Dict, Optional, Union

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

try:
    from BroadTopicExtraction.database_manager import DatabaseManager
except ImportError as e:
    raise ImportError(f"导入模块失败: {e}")

# 新闻API基础URL
BASE_URL = "https://newsnow.busiyi.world"

# 新闻源中文名称映射
SOURCE_NAMES = {
    "weibo": "微博热搜",
    "zhihu": "知乎热榜",
    "bilibili-hot-search": "B站热搜",
    "toutiao": "今日头条",
    "douyin": "抖音热榜",
    "github-trending-today": "GitHub趋势",
    "coolapk": "酷安热榜",
    "tieba": "百度贴吧",
    "wallstreetcn": "华尔街见闻",
    "thepaper": "澎湃新闻",
    "cls-hot": "财联社",
    "xueqiu": "雪球热榜",
    "kuaishou": "快手热榜"
}

class NewsCollector:
    """新闻收集器 - 整合API调用和数据库存储"""
    
    def __init__(self):
        """初始化新闻收集器"""
        self.db_manager = DatabaseManager()
        self.supported_sources = list(SOURCE_NAMES.keys())
    
    def close(self):
        """关闭资源"""
        if self.db_manager:
            self.db_manager.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.close()
    
    # ==================== 新闻API调用 ====================
    
    async def fetch_news(self, source: str) -> dict:
        """从指定源获取最新新闻"""
        url = f"{BASE_URL}/api/s?id={source}&latest"
        headers = {
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                
                # 解析JSON响应
                data = json.loads(response.text)
                return {
                    "source": source,
                    "status": "success",
                    "data": data,
                    "timestamp": datetime.now().isoformat()
                }
        except httpx.TimeoutException:
            return {
                "source": source,
                "status": "timeout",
                "error": "请求超时",
                "timestamp": datetime.now().isoformat()
            }
        except httpx.HTTPStatusError as e:
            # 特别处理快手热榜的500错误
            if source == "kuaishou" and e.response.status_code == 500:
                return {
                    "source": source,
                    "status": "success",
                    "data": {"items": []},  # 返回空数据而不是失败
                    "timestamp": datetime.now().isoformat()
                }
            return {
                "source": source,
                "status": "http_error",
                "error": f"HTTP错误: {e.response.status_code}",
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "source": source,
                "status": "error",
                "error": f"未知错误: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
    
    async def get_popular_news(self, sources: Optional[List[str]] = None) -> List[dict]:
        """获取热门新闻"""
        if sources is None:
            sources = list(SOURCE_NAMES.keys())
        
        print(f"正在获取 {len(sources)} 个新闻源的最新内容...")
        print("=" * 80)
        
        results = []
        for source in sources:
            source_name = SOURCE_NAMES.get(source, source)
            print(f"正在获取 {source_name} 的新闻...")
            result = await self.fetch_news(source)
            results.append(result)
            
            if result["status"] == "success":
                data = result["data"]
                if 'items' in data and isinstance(data['items'], list):
                    count = len(data['items'])
                    print(f"✓ {source_name}: 获取成功，共 {count} 条新闻")
                else:
                    print(f"✓ {source_name}: 获取成功")
            else:
                print(f"✗ {source_name}: {result.get('error', '获取失败')}")
            
            # 避免请求过快
            await asyncio.sleep(0.5)
        
        return results
    
    # ==================== 数据处理和存储 ====================
    
    async def collect_and_save_news(self, sources: Optional[List[str]] = None) -> Dict:
        """
        收集并保存每日热点新闻
        
        Args:
            sources: 指定的新闻源列表，None表示使用所有支持的源
            
        Returns:
            包含收集结果的字典
        """
        print(f"开始收集每日热点新闻...")
        print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 选择新闻源
        if sources is None:
            # 使用所有支持的新闻源
            sources = list(SOURCE_NAMES.keys())
        
        print(f"将从 {len(sources)} 个新闻源收集数据:")
        for source in sources:
            source_name = SOURCE_NAMES.get(source, source)
            print(f"  - {source_name}")
        
        try:
            # 获取新闻数据
            results = await self.get_popular_news(sources)
            
            # 处理结果
            processed_data = self._process_news_results(results)
            
            # 保存到数据库（覆盖模式）
            if processed_data['news_list']:
                saved_count = self.db_manager.save_daily_news(
                    processed_data['news_list'], 
                    date.today()
                )
                processed_data['saved_count'] = saved_count
            
            # 打印统计信息
            self._print_collection_summary(processed_data)
            
            return processed_data
            
        except Exception as e:
            print(f"收集新闻失败: {e}")
            return {
                'success': False,
                'error': str(e),
                'news_list': [],
                'total_news': 0
            }
    
    def _process_news_results(self, results: List[Dict]) -> Dict:
        """处理新闻获取结果"""
        news_list = []
        successful_sources = 0
        total_news = 0
        
        for result in results:
            source = result['source']
            status = result['status']
            
            if status == 'success':
                successful_sources += 1
                data = result['data']
                
                if 'items' in data and isinstance(data['items'], list):
                    source_news_count = len(data['items'])
                    total_news += source_news_count
                    
                    # 处理该源的新闻
                    for i, item in enumerate(data['items'], 1):
                        processed_news = self._process_news_item(item, source, i)
                        if processed_news:
                            news_list.append(processed_news)
        
        return {
            'success': True,
            'news_list': news_list,
            'successful_sources': successful_sources,
            'total_sources': len(results),
            'total_news': total_news,
            'collection_time': datetime.now().isoformat()
        }
    
    def _process_news_item(self, item: Dict, source: str, rank: int) -> Optional[Dict]:
        """处理单条新闻"""
        try:
            if isinstance(item, dict):
                title = item.get('title', '无标题').strip()
                url = item.get('url', '')
                
                # 生成新闻ID
                news_id = f"{source}_{item.get('id', f'rank_{rank}')}"
                
                return {
                    'id': news_id,
                    'title': title,
                    'url': url,
                    'source': source,
                    'rank': rank
                }
            else:
                # 处理字符串类型的新闻
                title = str(item)[:100] if len(str(item)) > 100 else str(item)
                return {
                    'id': f"{source}_rank_{rank}",
                    'title': title,
                    'url': '',
                    'source': source,
                    'rank': rank
                }
                
        except Exception as e:
            print(f"处理新闻项失败: {e}")
            return None
    
    def _print_collection_summary(self, data: Dict):
        """打印收集摘要"""
        print("\n" + "=" * 50)
        print("新闻收集摘要")
        print("=" * 50)
        
        print(f"总新闻源: {data['total_sources']}")
        print(f"成功源数: {data['successful_sources']}")
        print(f"总新闻数: {data['total_news']}")
        
        if 'saved_count' in data:
            print(f"已保存数: {data['saved_count']}")
        
        print("=" * 50)
    
    def get_today_news(self) -> List[Dict]:
        """获取今天的新闻"""
        try:
            return self.db_manager.get_daily_news(date.today())
        except Exception as e:
            print(f"获取今日新闻失败: {e}")
            return []

async def main():
    """测试新闻收集器"""
    print("测试新闻收集器...")
    
    async with NewsCollector() as collector:
        # 收集新闻
        result = await collector.collect_and_save_news(
            sources=["weibo", "zhihu"]  # 测试用，只使用两个源
        )
        
        if result['success']:
            print(f"收集成功！共获取 {result['total_news']} 条新闻")
        else:
            print(f"收集失败: {result.get('error', '未知错误')}")

if __name__ == "__main__":
    asyncio.run(main())
