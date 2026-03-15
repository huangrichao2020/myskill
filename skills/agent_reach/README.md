# 🌐 Agent-Reach — AI Agent 互联网访问能力

> 给 AI Agent 装上互联网眼睛，一键访问 16+ 平台

## 📦 安装

### 快速安装（推荐）

```bash
# 使用 Python 3.12+
python3 -m pip install https://github.com/Panniantong/agent-reach/archive/main.zip

# 运行安装脚本
agent-reach install --env=auto
```

### 安全模式（不自动安装系统依赖）

```bash
agent-reach install --env=auto --safe
```

### 预览模式（先看会做什么）

```bash
agent-reach install --env=auto --dry-run
```

## ✅ 支持的平台

### 装好即用（无需配置）

| 平台 | 功能 | 命令示例 |
|------|------|----------|
| 🌐 网页 | 阅读任意网页 | `curl https://r.jina.ai/URL` |
| 🔍 全网搜索 | Exa 语义搜索 | `mcporter call 'exa.web_search_exa(query: "query")'` |
| 🐦 Twitter/X | 搜索推文、阅读 | `xreach search "query" --json` |
| 📺 YouTube | 字幕提取 + 搜索 | `yt-dlp --dump-json URL` |
| 📺 B 站 | 字幕提取 | `yt-dlp --dump-json "BV 号"` |
| 📖 Reddit | 帖子 + 评论 | `curl reddit.com/r/xxx.json` |
| 💻 V2EX | 热门帖子、节点 | `curl v2ex.com/api/topics/hot.json` |
| 📡 RSS | 订阅源阅读 | `python -c "import feedparser"` |
| 💬 微信公众号 | 搜索 + 阅读 | `agent-reach configure wechat` |

### 配置后可用

| 平台 | 需要 | 配置命令 |
|------|------|----------|
| 📕 小红书 | Docker | `docker run -d --name xiaohongshu-mcp -p 18060:18060 xpzouying/xiaohongshu-mcp` |
| 🎵 抖音 | MCP 服务 | `pip install douyin-mcp-server` |
| 💼 LinkedIn | MCP 服务 | `pip install linkedin-scraper-mcp` |
| 📰 微博 | MCP 配置 | `mcporter config add weibo --command 'mcp-server-weibo'` |
| 🎙️ 小宇宙播客 | ffmpeg + Groq Key | `agent-reach configure groq-key gsk_xxx` |
| 📦 GitHub | gh CLI | `brew install gh` |

## 🔧 常用命令

### 健康检查

```bash
# 检查所有渠道状态
agent-reach doctor

# 快速检查（适合定时任务）
agent-reach watch
```

### 配置渠道

```bash
# 配置代理（解锁 Reddit/B 站服务器访问）
agent-reach configure proxy http://user:pass@ip:port

# 配置 Twitter Cookie（解锁搜索 + 发推）
agent-reach configure twitter-cookies "COOKIE_STRING"

# 配置小红书 Cookie
agent-reach configure xhs-cookies "COOKIE_STRING"

# 配置 Groq API Key（小宇宙播客转录）
agent-reach configure groq-key gsk_xxxxx

# 从浏览器自动导入 Cookie
agent-reach configure --from-browser chrome
```

### 卸载

```bash
# 完全卸载
agent-reach uninstall

# 只删除 skill 文件，保留配置
agent-reach uninstall --keep-config

# 预览删除操作
agent-reach uninstall --dry-run
```

## 📖 使用示例

### 搜索 Twitter

```bash
xreach search "AI agent" -n 10 --json
```

### 提取 YouTube 字幕

```bash
yt-dlp --write-sub --skip-download -o "/tmp/%(id)s" "URL"
```

### 读取任意网页

```bash
curl -s "https://r.jina.ai/https://example.com"
```

### 搜索 GitHub 仓库

```bash
gh search repos "LLM framework" --sort stars --limit 10
```

### 读取 V2EX 热门帖子

```bash
curl -s "https://www.v2ex.com/api/topics/hot.json" | python3 -m json.tool
```

### 搜索微信公众号文章

```python
python3 -c "
import asyncio
from miku_ai import get_wexin_article
async def s():
    for a in await get_wexin_article('AI', 5):
        print(f'{a[\"title\"]} | {a[\"url\"]}')
asyncio.run(s())
"
```

## 🔒 安全说明

1. **Cookie 安全**：使用专用小号，不要用主账号
2. **本地存储**：所有配置保存在 `~/.agent-reach/config.yaml`，权限 600
3. **不上传数据**：Cookie 和 Token 只存在本地，不上传不外传
4. **安全模式**：生产环境使用 `--safe` 参数，不自动修改系统

## 🛠️ 故障排查

### Twitter 无法访问

```bash
# 检查 undici 是否安装
npm list -g undici

# 安装 undici（支持代理）
npm install -g undici

# 配置代理
agent-reach configure proxy http://user:pass@ip:port
```

### 小宇宙播客无法转录

```bash
# 安装 ffmpeg
brew install ffmpeg

# 配置 Groq API Key（免费）
agent-reach configure groq-key gsk_xxxxx
```

### 微博 MCP 未配置

```bash
pip install git+https://github.com/Panniantong/mcp-server-weibo.git
mcporter config add weibo --command 'mcp-server-weibo'
```

## 📚 资源链接

- **GitHub**: https://github.com/Panniantong/Agent-Reach
- **安装指南**: https://raw.githubusercontent.com/Panniantong/agent-reach/main/docs/install.md
- **更新指南**: https://raw.githubusercontent.com/Panniantong/agent-reach/main/docs/update.md
- **故障排查**: https://github.com/Panniantong/Agent-Reach/blob/main/docs/troubleshooting.md

## 🎯 设计理念

Agent Reach 是**脚手架**而非框架：
- 直接调用上游工具（xreach、yt-dlp、gh CLI 等）
- 每个渠道都是可插拔的独立模块
- 不满意可以替换对应渠道文件

## 📄 License

MIT
