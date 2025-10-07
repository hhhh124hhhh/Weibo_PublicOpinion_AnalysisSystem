# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

"微舆"是一个多智能体舆情分析系统，包含4个核心Agent和1个论坛协作机制：
- **QueryEngine**: 新闻搜索Agent (使用TavilyNewsAgency工具)
- **MediaEngine**: 多模态内容分析Agent (使用BochaMultimodalSearch工具)
- **InsightEngine**: 私有数据库挖掘Agent (使用MediaCrawlerDB工具 + 情感分析)
- **ReportEngine**: 智能报告生成Agent (动态模板选择和HTML生成)
- **ForumEngine**: Agent间论坛协作机制 (LLM主持人 + 实时日志监控)

## 常用命令

### 系统启动
```bash
# 启动完整系统 (自动启动所有Agent + ForumEngine + ReportEngine)
python app.py

# 单独启动Agent (用于开发调试)
streamlit run SingleEngineApp/insight_engine_streamlit_app.py --server.port 8501
streamlit run SingleEngineApp/media_engine_streamlit_app.py --server.port 8502
streamlit run SingleEngineApp/query_engine_streamlit_app.py --server.port 8503
```

### 爬虫系统
```bash
cd MindSpider

# 项目初始化 (数据库表结构创建)
python main.py --setup

# 完整爬虫流程 (话题提取 + 深度爬取)
python main.py --complete --date 2024-01-20

# 仅话题提取 (从热点新闻提取话题)
python main.py --broad-topic --date 2024-01-20

# 仅深度爬取 (基于话题的平台内容爬取)
python main.py --deep-sentiment --platforms xhs dy wb

# 支持平台: xhs(小红书), dy(抖音), ks(快手), bili(B站), wb(微博), tieba(贴吧), zhihu(知乎)
```

### 数据库初始化
```bash
cd MindSpider
python schema/init_database.py  # 创建数据库表结构
```

### 环境设置
```bash
# 创建conda环境
conda create -n weibo_analysis python=3.11
conda activate weibo_analysis

# 安装基础依赖
pip install -r requirements.txt

# 安装浏览器驱动 (爬虫必需)
playwright install chromium

# 可选: 安装情感分析PyTorch依赖
pip install torch torchvision torchaudio  # CPU版本
# 或GPU版本: pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

## 系统架构

### Agent核心架构
每个Agent都采用相同的节点式处理架构:
- **FirstSearchNode**: 初步搜索和分析
- **ReflectionNode**: 反思和策略调整
- **FirstSummaryNode**: 初步总结生成
- **ReflectionSummaryNode**: 反思后的深度总结
- **ReportFormattingNode**: 报告格式化输出

### 配置文件层次
```
config.py                                    # 全局配置 (API密钥、数据库)
├── InsightEngine/utils/config.py           # InsightAgent (搜索限制、LLM配置)
├── MediaEngine/utils/config.py             # MediaAgent (多模态搜索配置)
├── QueryEngine/utils/config.py             # QueryAgent (新闻搜索配置)
├── ReportEngine/utils/config.py            # ReportAgent (报告生成配置)
└── MindSpider/config.py                    # 爬虫系统配置 (平台配置、代理设置)
```

### 核心工具集
- **TavilyNewsAgency**: 6种新闻搜索工具 (QueryEngine)
- **BochaMultimodalSearch**: 5种多模态搜索工具 (MediaEngine)
- **MediaCrawlerDB**: 5种本地数据库查询工具 (InsightEngine)
- **WeiboMultilingualSentiment**: 22种语言情感分析 (InsightEngine)
- **ForumEngine**: LLM主持人 + 实时日志监控

### 数据库设计
**MindSpider数据库结构**:
- `daily_news`: 每日热点新闻 (多平台)
- `daily_topics`: AI提取的话题信息
- `topic_news_relation`: 话题-新闻关联
- `crawling_tasks`: 爬取任务管理
- 平台内容表: `xhs_note`, `douyin_aweme`, `kuaishou_video`, `bilibili_video`, `weibo_note`, `tieba_note`, `zhihu_content`

### Agent协作流程
1. **并行启动**: Flask同时启动三个Agent，各自使用专属工具
2. **初步分析**: Agent进行初步搜索和策略制定
3. **论坛协作**: ForumEngine监控日志，LLM主持人每5条Agent发言生成总结
4. **深度循环**: Agent根据主持人引导调整研究方向，多轮迭代
5. **报告生成**: ReportEngine检测所有Agent完成，动态选择模板生成HTML报告

## 开发指南

### 情感分析模型集成
系统集成了5种情感分析方法:
```python
# 1. 多语言情感分析 (推荐，支持22种语言)
cd SentimentAnalysisModel/WeiboMultilingualSentiment
python predict.py --text "This product is amazing!" --lang "en"

# 2. 小参数Qwen3微调 (中文优化)
cd SentimentAnalysisModel/WeiboSentiment_SmallQwen
python predict_universal.py --text "这次活动办得很成功"

# 3. BERT中文LoRA微调
cd SentimentAnalysisModel/WeiboSentiment_Finetuned/BertChinese-Lora
python predict.py --text "这个产品真的很不错"

# 4. 传统机器学习方法
cd SentimentAnalysisModel/WeiboSentiment_MachineLearning
python predict.py --model_type "svm" --text "服务态度需要改进"
```

### 添加新Agent
1. 参考现有Engine目录结构创建新Agent
2. 实现`agent.py`主类，继承相同的节点架构
3. 在`tools/`目录实现专用工具集
4. 在`utils/config.py`中添加配置参数
5. 在`app.py`中添加启动逻辑

### 自定义报告模板
1. 在`ReportEngine/report_template/`目录添加.md模板文件
2. 系统会自动识别并选择最合适的模板
3. 支持通过Web界面上传自定义模板

### 业务数据库集成
```python
# 1. 在config.py添加业务数据库配置
BUSINESS_DB_HOST = "your_host"
BUSINESS_DB_USER = "your_user"
# ...其他配置

# 2. 在InsightEngine/tools/创建自定义工具
class CustomBusinessDBTool:
    def search_business_data(self, query: str):
        # 实现业务逻辑
        pass

# 3. 集成到InsightAgent
from .tools.custom_db_tool import CustomBusinessDBTool
```

## 重要配置参数

### Agent配置 (各Engine的utils/config.py)
```python
# 搜索限制配置
max_search_results = 15          # 最大搜索结果数
max_content_length = 8000        # 最大内容长度
max_reflections = 2              # 反思轮次

# InsightEngine特有配置
default_search_topic_globally_limit = 200    # 全局搜索限制
default_get_comments_limit = 500             # 评论获取限制
max_search_results_for_llm = 50              # 传给LLM的最大结果数
```

### 情感分析配置
```python
# InsightEngine/tools/sentiment_analyzer.py
SENTIMENT_CONFIG = {
    'model_type': 'multilingual',     # 模型类型
    'confidence_threshold': 0.8,      # 置信度阈值
    'batch_size': 32,                 # 批处理大小
}
```

### 爬虫平台配置
- 支持平台: 微博、小红书、抖音、快手、B站、知乎、贴吧
- 代理配置: 支持多种代理服务商
- 反爬策略: User-Agent轮换、请求间隔、验证码处理

## 调试和监控

### 日志系统
```
logs/
├── forum.log              # ForumEngine论坛讨论记录
├── insight.log            # InsightEngine运行日志
├── media.log              # MediaEngine运行日志
├── query.log              # QueryEngine运行日志
└── report.log             # ReportEngine运行日志
```

### 实时监控
- 访问 http://localhost:5000 查看统一的Web界面
- 实时查看各Agent运行状态和日志输出
- ForumEngine讨论内容实时更新
- 支持手动启动/停止各Agent

### 常见问题排查
1. **Agent启动失败**: 检查端口占用 (8501/8502/8503)
2. **数据库连接失败**: 检查config.py中的数据库配置
3. **API调用失败**: 检查API密钥配置和网络连接
4. **爬虫功能异常**: 检查playwright驱动安装 `playwright install chromium`

## 部署要求

### 系统要求
- **操作系统**: Windows/Linux/MacOS
- **Python**: 3.9+ (推荐3.11)
- **内存**: 2GB+ (推荐4GB+)
- **数据库**: MySQL 5.7+ 或 云数据库服务

### 端口分配
- **5000**: Flask主应用 (Web界面)
- **8501**: InsightEngine Streamlit应用
- **8502**: MediaEngine Streamlit应用
- **8503**: QueryEngine Streamlit应用

### API服务配置
系统支持多种LLM和搜索API:
```python
# LLM服务商
DEEPSEEK_API_KEY = "your_key"      # DeepSeek (推荐)
OPENAI_API_KEY = "your_key"        # OpenAI兼容
KIMI_API_KEY = "your_key"          # Kimi (长文本)
GEMINI_API_KEY = "your_key"        # Gemini (多模态)

# 搜索服务商
TAVILY_API_KEY = "your_key"        # Tavily新闻搜索
BOCHA_Web_Search_API_KEY = "your_key"  # 博查多模态搜索
```

### 云数据库服务
- 项目提供免费云数据库服务 (日均10万+真实舆情数据)
- 联系邮箱: 670939375@qq.com
- 包含多维度标签分类，实时更新

## 开发最佳实践

1. **模块化开发**: 每个Agent独立开发测试，避免相互依赖
2. **配置管理**: 使用环境变量或配置文件管理敏感信息
3. **错误处理**: 实现完善的异常处理和重试机制
4. **日志记录**: 详细记录运行过程，便于调试和监控
5. **性能优化**: 合理设置搜索限制和批处理大小
6. **扩展性**: 预留接口用于添加新工具和模型