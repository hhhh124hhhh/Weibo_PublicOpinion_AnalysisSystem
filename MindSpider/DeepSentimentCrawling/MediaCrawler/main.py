# 声明：本代码仅供学习和研究目的使用。使用者应遵守以下原则：
# 1. 不得用于任何商业用途。
# 2. 使用时应遵守目标平台的使用条款和robots.txt规则。
# 3. 不得进行大规模爬取或对平台造成运营干扰。
# 4. 应合理控制请求频率，避免给目标平台带来不必要的负担。
# 5. 不得用于任何非法或不当的用途。
#
# 详细许可条款请参阅项目根目录下的LICENSE文件。
# 使用本代码即表示您同意遵守上述原则和LICENSE中的所有条款。


import asyncio
import sys
from typing import Optional

import cmd_arg
import config
from base.base_crawler import AbstractCrawler
from media_platform.bilibili import BilibiliCrawler
from media_platform.douyin import DouYinCrawler
from media_platform.kuaishou import KuaishouCrawler
from media_platform.tieba import TieBaCrawler
from media_platform.weibo import WeiboCrawler
from media_platform.xhs import XiaoHongShuCrawler
from media_platform.zhihu import ZhihuCrawler


class CrawlerFactory:
    CRAWLERS = {
        "xhs": XiaoHongShuCrawler,
        "dy": DouYinCrawler,
        "ks": KuaishouCrawler,
        "bili": BilibiliCrawler,
        "wb": WeiboCrawler,
        "tieba": TieBaCrawler,
        "zhihu": ZhihuCrawler,
    }

    @staticmethod
    def create_crawler(platform: str) -> AbstractCrawler:
        crawler_class = CrawlerFactory.CRAWLERS.get(platform)
        if not crawler_class:
            raise ValueError(
                "Invalid Media Platform Currently only supported xhs or dy or ks or bili ..."
            )
        return crawler_class()


crawler: Optional[AbstractCrawler] = None


async def main():
    # Init crawler
    global crawler

    # parse cmd
    await cmd_arg.parse_cmd()

    # init db
    if getattr(config, 'SAVE_DATA_OPTION', 'db') in ["db", "sqlite"]:
        import db
        await db.init_db()

    crawler = CrawlerFactory.create_crawler(platform=getattr(config, 'PLATFORM', 'wb'))
    await crawler.start()


def cleanup():
    global crawler
    if crawler:
        # asyncio.run(crawler.close())
        pass
    try:
        # 尝试安全地关闭数据库连接
        if getattr(config, 'SAVE_DATA_OPTION', 'db') in ["db", "sqlite"]:
            import db
            try:
                # 检查是否有运行中的事件循环
                try:
                    loop = asyncio.get_running_loop()
                    # 在运行中的事件循环中，安排关闭任务
                    loop.call_soon(db.close)
                except RuntimeError:
                    # 如果没有运行中的事件循环，使用asyncio.run
                    asyncio.run(db.close())
                except Exception:
                    # 如果出现其他异常，忽略它以避免程序崩溃
                    pass
            except Exception as e:
                # 如果出现其他异常，忽略它以避免程序崩溃
                pass
    except (ImportError, AttributeError):
        # 如果出现导入或属性错误，忽略它以避免程序崩溃
        pass

if __name__ == "__main__":
    try:
        asyncio.get_event_loop().run_until_complete(main())
    except KeyboardInterrupt:
        print("用户中断操作")
    finally:
        try:
            cleanup()
        except:
            # 忽略清理过程中的任何异常
            pass