# 如何获取和设置小红书Cookie

当小红书要求手机验证码验证时，我们可以使用Cookie登录方式来避免这个问题。

## 获取小红书Cookie的步骤

### 方法一：从浏览器开发者工具获取

1. **打开Chrome浏览器**并访问小红书官网 https://www.xiaohongshu.com
2. **登录你的小红书账号**（使用用户名密码登录，不要扫码）
3. **按F12打开开发者工具**或右键点击页面选择"检查"
4. **切换到Network（网络）标签**
5. **刷新页面**（按F5）
6. **在请求列表中找到任意一个请求**，点击它
7. **在Headers部分找到Cookie字段**
8. **复制完整的Cookie值**

### 方法二：使用浏览器扩展（推荐）

1. **安装Chrome扩展**"EditThisCookie"或"Cookie-Editor"
2. **访问小红书并登录**
3. **点击浏览器上的Cookie扩展图标**
4. **导出所有Cookie**
5. **保存为JSON格式**

## 设置Cookie

获取到Cookie后，需要在配置文件中设置：

1. **打开配置文件**：
   ```
   D:\Weibo_PublicOpinion_AnalysisSystem\MindSpider\DeepSentimentCrawling\MediaCrawler\config\base_config.py
   ```

2. **找到COOKIES配置项**：
   ```python
   COOKIES = ""
   ```

3. **将获取到的Cookie粘贴到引号中**：
   ```python
   COOKIES = "这里粘贴你获取到的Cookie"
   ```

## 注意事项

1. **Cookie有效期**：Cookie通常有有效期，过期后需要重新获取
2. **账号安全**：不要将Cookie分享给他人，它相当于你的登录凭证
3. **平台限制**：即使使用Cookie，平台仍可能有访问频率限制
4. **遵守规则**：请遵守小红书的使用条款和robots.txt规则

## 测试Cookie是否有效

设置好Cookie后，可以运行以下命令测试：
```bash
cd /d D:\Weibo_PublicOpinion_AnalysisSystem\MindSpider\DeepSentimentCrawling
python main.py --platforms xhs --test
```

如果配置正确，系统将直接使用Cookie登录，无需扫码和手机验证。