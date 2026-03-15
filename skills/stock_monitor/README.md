# 📊 A 股监控技能

实时监控 A 股龙头股异动，自动推送飞书提醒。

## 🎯 功能特性

- **86 只龙头股监控**: 进攻板块 (33 只) + 防御板块 (40 只) + 自选股 (13 只)
- **自动飞书推送**: 检测到异动立即推送
- **交易时段监控**: 周一至周五 9:15-15:00
- **动态自选股**: 随时添加/删除股票
- **异动类型**: 快速拉升 (≥3%)、快速下跌 (≥-3%)、涨停 (≥9.5%)

## 📁 模块结构

```
stock_monitor/
├── stock_monitor_all.py    # 主监控脚本
├── feishu_push.py          # 飞书推送模块
├── stock_manager.py        # 股票管理工具
├── stock_pool.json         # 股票池配置
└── README.md               # 本模块文档
```

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install requests flask apscheduler
```

### 2. 配置飞书

编辑 `feishu_push.py`，填入你的飞书应用凭证：

```python
APP_ID = "your_app_id"
APP_SECRET = "your_app_secret"
```

### 3. 启动监控服务

```bash
# 启动后端服务
python3 stock_monitor_server.py

# 或使用管理脚本
./server.sh start
```

### 4. 访问 Web 界面

打开浏览器访问：`http://localhost:5050`

## 📡 API 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/status` | GET | 查看监控状态 |
| `/monitor/run` | POST | 手动执行监控 |
| `/monitor/enable` | POST | 启用监控 |
| `/monitor/disable` | POST | 禁用监控 |
| `/stocks` | GET | 查看股票池 |
| `/stocks/add` | POST | 添加股票 |
| `/logs` | GET | 查看日志 |

### 使用示例

```bash
# 查看状态
curl http://localhost:5050/status

# 手动执行
curl -X POST http://localhost:5050/monitor/run

# 添加自选股
curl -X POST http://localhost:5050/stocks/add \
  -H "Content-Type: application/json" \
  -d '{"pool":"我的自选","code":"600519","name":"贵州茅台"}'
```

## 🛠️ 命令行工具

```bash
# 添加股票
python3 stock_manager.py add 我的自选 600519 贵州茅台

# 查看股票池
python3 stock_manager.py list

# 删除股票
python3 stock_manager.py remove 我的自选 sh600519
```

## ⏰ 监控时间

| 时间 | 行为 |
|------|------|
| 周一 - 周五 9:15-15:00 | ✅ 自动监控 |
| 周一 - 周五 9:00-9:14 | ⏭️ 跳过 (集合竞价) |
| 周一 - 周五 15:00 后 | ⏭️ 跳过 (已收盘) |
| 周六、周日 | ⏭️ 跳过 (休市) |

## 📊 股票池

| 股票池 | 股票数 | 说明 |
|--------|--------|------|
| 进攻板块 | 33 只 | 十五五规划 6 大龙头 |
| 防御板块 | 40 只 | 6 大防御板块龙头 |
| 我的自选 | ∞ | 自定义股票 |

## 🔧 配置说明

### 添加/删除股票

编辑 `stock_pool.json`：

```json
{
  "我的自选": {
    "enabled": true,
    "stocks": {
      "sh600519": "贵州茅台",
      "sz000858": "五粮液"
    }
  }
}
```

### 调整异动阈值

编辑 `stock_monitor_all.py`：

```python
THRESHOLDS = {
    "rapid_rise": 3.0,    # 快速拉升阈值 (%)
    "rapid_fall": -3.0,   # 快速下跌阈值 (%)
    "limit_up": 9.5,      # 涨停阈值 (%)
}
```

## 📝 日志查看

```bash
# 查看服务日志
tail -f monitor_server.log

# API 查看日志
curl http://localhost:5050/logs?limit=50
```

## 🚨 故障排查

### 服务启动失败

```bash
# 检查端口占用
lsof -i :5050

# 手动启动测试
python3 stock_monitor_server.py
```

### 飞书推送失败

```bash
# 测试推送
python3 feishu_push.py
```

### 数据获取失败

```bash
# 测试腾讯 API
curl -s "http://qt.gtimg.cn/q=s_sh601012"
```

## 📅 更新记录

- **2026-03-15**: 初始版本
  - 86 只龙头股监控
  - 飞书实时推送
  - Web 管理界面
  - 动态自选股管理

## 📄 License

MIT
