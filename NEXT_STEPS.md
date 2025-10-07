# 下一步测试指南

## 系统修复确认

我们已经成功修复了之前出现的"Field 'topic_id' doesn't have a default value"错误。主要修改包括：

1. 在[database_manager.py](file:///D:/Weibo_PublicOpinion_AnalysisSystem/MindSpider/BroadTopicExtraction/database_manager.py)中添加了topic_id字段的生成逻辑
2. 修改了数据库INSERT和UPDATE语句，确保包含所有必需的字段
3. 验证了数据库表结构的正确性

## 开始测试下一个平台

根据项目架构，下一步是测试DeepSentimentCrawling模块。以下是推荐的测试步骤：

### 1. 确保环境准备就绪

```bash
# 激活conda环境
conda activate your_conda_name

# 确保Playwright浏览器驱动已安装
playwright install chromium
```

### 2. 测试单个平台（推荐从简单开始）

```bash
# 进入MindSpider目录
cd MindSpider

# 测试小红书平台（使用测试模式，数据量较小）
python main.py --deep-sentiment --platforms xhs --test

# 或者测试微博平台
python main.py --deep-sentiment --platforms wb --test
```

### 3. 首次使用平台需要登录

首次使用每个平台时都需要扫码登录：

1. 运行上述命令后，会弹出浏览器窗口
2. 使用对应平台的APP扫码登录
3. 登录成功后，状态会自动保存

### 4. 如果遇到登录问题

可以关闭无头模式以便查看浏览器界面：

编辑文件：`MindSpider/DeepSentimentCrawling/MediaCrawler/config/base_config.py`
```python
# 将以下行改为False
HEADLESS = False
```

### 5. 测试多个平台

```bash
# 测试多个平台
python main.py --deep-sentiment --platforms xhs dy wb --test
```

### 6. 查看帮助信息

```bash
# 查看所有可用选项
python main.py --deep-sentiment --help
```

## 推荐的测试顺序

建议按照以下顺序测试平台：

1. **小红书 (xhs)** - 通常最容易登录和爬取
2. **微博 (wb)** - 用户基数大，内容丰富
3. **抖音 (dy)** - 视频内容平台
4. **B站 (bili)** - 年轻用户群体，内容质量高
5. **快手 (ks)** - 生活化内容较多
6. **贴吧 (tieba)** - 讨论性内容丰富
7. **知乎 (zhihu)** - 深度内容和专业讨论

## 注意事项

1. **首次登录**：每个平台首次使用都需要扫码登录
2. **测试模式**：建议先使用`--test`参数进行小规模测试
3. **遵守规则**：请遵守各平台的使用规则和爬取频率限制
4. **数据查看**：爬取的数据会保存在MySQL数据库中

## 数据库查看

可以使用以下SQL查询查看爬取的数据：

```sql
-- 查看小红书笔记
SELECT * FROM xhs_note LIMIT 10;

-- 查看微博帖子
SELECT * FROM weibo_note LIMIT 10;

-- 查看话题数据
SELECT * FROM daily_topics;
```

## 常见问题解决

1. **登录失败**：关闭无头模式，手动处理验证码
2. **数据为空**：确保已运行BroadTopicExtraction模块生成关键词
3. **数据库连接失败**：检查config.py中的数据库配置
4. **浏览器驱动问题**：重新安装playwright浏览器驱动

现在可以开始测试下一个平台了！建议从最简单的平台开始，逐步验证系统的完整功能。