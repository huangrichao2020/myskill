# Agent-Reach 快速上手指南

## 🎯 一句话介绍

**给 AI Agent 装上互联网眼睛** — 让 Agent 能直接访问 Twitter、YouTube、Reddit、B 站、小红书等 16+ 平台。

## ⚡ 5 分钟快速开始

### 1. 安装（已完成）

```bash
# 已安装到系统
agent-reach --version  # v1.3.0

# 查看状态
agent-reach doctor
```

### 2. 当前可用渠道（9/15）

✅ **无需配置即用**：
- 🌐 网页阅读（Jina Reader）
- 🔍 全网搜索（Exa，免费）
- 🐦 Twitter/X（搜索 + 阅读）
- 📺 YouTube（字幕提取）
- 📺 B 站（字幕提取）
- 📖 Reddit（帖子 + 评论）
- 💻 V2EX（公开 API）
- 📡 RSS（订阅源）
- 💬 微信公众号（搜索 + 阅读）

### 3. 立即体验

#### 读取任意网页
```bash
curl -s "https://r.jina.ai/https://example.com"
```

#### 搜索全网（Exa）
```bash
mcporter call 'exa.web_search_exa(query: "AI agent framework", numResults: 5)'
```

#### 提取 YouTube 字幕
```bash
yt-dlp --dump-json "https://www.youtube.com/watch?v=VIDEO_ID"
```

#### 读取 RSS 订阅
```bash
/usr/local/opt/python@3.12/bin/python3.12 -c "
import feedparser
f = feedparser.parse('https://github.com/Panniantong/Agent-Reach/releases.atom')
print(f'Feed: {f.feed.title}')
for e in f.entries[:3]:
    print(f'  - {e.title}')
"
```

## 🔐 配置可选渠道

### Twitter 完整功能（搜索 + 发推）

1. 浏览器登录 https://twitter.com
2. 安装 [Cookie-Editor](https://chromewebstore.google.com/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm)
3. 导出 Cookie（Header String 格式）
4. 运行：
```bash
agent-reach configure twitter-cookies "PASTE_YOUR_COOKIE"
```

### 小宇宙播客转录

1. 获取免费 Groq API Key：https://console.groq.com
2. 安装 ffmpeg：`brew install ffmpeg`
3. 配置：
```bash
agent-reach configure groq-key gsk_xxxxx
```

### 小红书（需要 Docker）

```bash
docker run -d --name xiaohongshu-mcp -p 18060:18060 xpzouying/xiaohongshu-mcp
mcporter config add xiaohongshu http://localhost:18060/mcp
```

## 🛠️ 常用命令

```bash
# 健康检查
agent-reach doctor

# 快速检查（适合定时任务）
agent-reach watch

# 配置代理（解锁服务器访问）
agent-reach configure proxy http://user:pass@ip:port

# 从浏览器导入 Cookie
agent-reach configure --from-browser chrome

# 更新
pip install --upgrade https://github.com/Panniantong/agent-reach/archive/main.zip

# 卸载
agent-reach uninstall
```

## 📊 渠道状态总览

| 渠道 | 状态 | 备注 |
|------|------|------|
| 网页阅读 | ✅ | Jina Reader |
| 全网搜索 | ✅ | Exa 免费 |
| Twitter | ✅ | 基础功能可用 |
| YouTube | ✅ | yt-dlp |
| B 站 | ✅ | 本地环境可用 |
| Reddit | ✅ | JSON API |
| V2EX | ✅ | 公开 API |
| RSS | ✅ | feedparser |
| 微信公众号 | ✅ | Camoufox |
| 微博 | ⚠️ | 需配置 MCP |
| 小宇宙 | ⚠️ | 需 ffmpeg + Groq Key |
| 小红书 | ❌ | 需 Docker |
| 抖音 | ❌ | 需 MCP 服务 |
| LinkedIn | ❌ | 需 MCP 服务 |
| GitHub | ❌ | 需 gh CLI |

## 🔒 安全提醒

1. **使用小号**：Twitter、小红书等平台使用专用小号，避免主账号被封
2. **本地存储**：所有配置保存在 `~/.agent-reach/config.yaml`，权限 600
3. **不上传数据**：Cookie 和 Token 只存在本地

## 📚 更多资源

- **完整文档**：https://github.com/Panniantong/Agent-Reach
- **安装指南**：https://raw.githubusercontent.com/Panniantong/agent-reach/main/docs/install.md
- **故障排查**：https://github.com/Panniantong/Agent-Reach/blob/main/docs/troubleshooting.md

## 💡 使用场景

### 股市研究
- 搜索 Twitter 上的行业讨论
- 读取微信公众号的行业分析
- 监控 V2EX 技术讨论

### 技术学习
- 提取 YouTube 教程字幕
- 搜索 GitHub 上的开源项目
- 阅读 Reddit 技术板块

### 市场调研
- 小红书产品口碑
- 微博热搜趋势
- 全网语义搜索

---

**已集成到 myskill 项目**：https://github.com/huangrichao2020/myskill
