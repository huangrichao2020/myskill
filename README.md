# MySkill - 个人技能库

🚀 个人自动化技能集合，模块化设计，按需使用。

## 📚 技能列表

| 技能 | 说明 | 状态 |
|------|------|------|
| [📊 A 股监控](skills/stock_monitor) | A 股龙头股异动监控，飞书实时推送 | ✅ 可用 |

## 🎯 使用方式

每个技能都是独立的模块，可以单独使用：

```bash
# 进入技能目录
cd skills/<skill_name>

# 查看该技能的文档
cat README.md

# 按照文档说明使用
```

## 📦 添加新技能

1. 在 `skills/` 目录下创建新文件夹
2. 添加技能代码和 `README.md`
3. 更新本文件，添加技能说明

## 🔧 通用依赖

```bash
# Python 3.12+
python3 --version

# 常用依赖
pip install requests flask apscheduler
```

## 📁 项目结构

```
myskill/
├── README.md               # 本文件
├── skills/                 # 技能模块目录
│   ├── stock_monitor/      # A 股监控
│   │   ├── README.md
│   │   ├── stock_monitor_all.py
│   │   ├── feishu_push.py
│   │   └── ...
│   └── <new_skill>/        # 新技能
└── ...
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 License

MIT
