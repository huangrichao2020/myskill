#!/usr/local/opt/python@3.12/bin/python3.12
# -*- coding: utf-8 -*-
"""
A 股短线精灵监控 - 统一版
监控进攻板块 + 防御板块 + 我的自选
"""

import requests
import json
import time
from datetime import datetime
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STOCK_POOL_FILE = os.path.join(SCRIPT_DIR, "stock_pool.json")
LAST_PUSH_FILE = os.path.join(SCRIPT_DIR, "last_push.json")

# 异动阈值配置
THRESHOLDS = {
    "rapid_rise": 3.0,
    "rapid_fall": -3.0,
    "limit_up": 9.5,
}

# 板块映射 (用于显示)
SECTOR_MAP = {
    # 进攻板块
    "新能源": ["sh601012", "sh600438", "sh600406", "sh601877", "sh600089", "sz300750", "sz300274", "sz002594"],
    "新材料": ["sh600516", "sh603799", "sz002460", "sz002466", "sz300073"],
    "生物医药": ["sh603259", "sh600276", "sh600085", "sz000661", "sz300760"],
    "高端装备": ["sz300124", "sh600031", "sh600760", "sh600893", "sz000157"],
    "数字经济/AI": ["sz002230", "sz002415", "sh688981", "sz000063", "sh600588"],
    "绿色环保": ["sh600900", "sh601985", "sh600795", "sh600023", "sh600578"],
    # 防御板块
    "基建": ["sh601668", "sh601390", "sh601186", "sh601800", "sh601669", "sh601618", "sh600170", "sh600820"],
    "影视传媒": ["sz002739", "sz300251", "sz300027", "sh600977", "sz300413", "sz002027"],
    "石油石化": ["sh601857", "sh600028", "sh600938", "sh601808", "sh600871"],
    "煤炭": ["sh601088", "sh601225", "sh600188", "sh601898", "sz000983", "sh601699"],
    "电力": ["sh600900", "sh600011", "sh600795", "sh601991", "sh600027", "sh600886", "sh600905", "sh600642"],
    "贵金属": ["sh600547", "sh600489", "sh601899", "sz000975", "sh600988", "sz002155", "sh600531"],
}

def load_stock_pool():
    """从配置文件加载股票池"""
    if not os.path.exists(STOCK_POOL_FILE):
        print(f"⚠️  股票池配置文件不存在：{STOCK_POOL_FILE}")
        return {}
    
    with open(STOCK_POOL_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_monitor_stocks():
    """获取所有需要监控的股票"""
    pool = load_stock_pool()
    stocks = {}
    
    for pool_name, pool_data in pool.items():
        if pool_data.get("enabled", True):
            stocks.update(pool_data.get("stocks", {}))
    
    return stocks, pool

def load_last_push():
    if os.path.exists(LAST_PUSH_FILE):
        with open(LAST_PUSH_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_last_push(data):
    os.makedirs(os.path.dirname(LAST_PUSH_FILE), exist_ok=True)
    with open(LAST_PUSH_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_stock_data(stock_codes):
    """获取腾讯财经实时行情数据"""
    codes = ",".join([f"s_{code}" for code in stock_codes])
    url = f"http://qt.gtimg.cn/q={codes}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "http://quote.eastmoney.com/"
    }
    
    for i in range(3):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            text = response.text
            
            if not text or len(text) < 50:
                print(f"尝试 {i+1}/3: 响应数据过短")
                time.sleep(1)
                continue
            
            stocks = []
            for line in text.strip().split('\n'):
                if '=' not in line:
                    continue
                try:
                    code_part, data_part = line.split('=', 1)
                    code = code_part.replace('v_s_', '')
                    data_part = data_part.strip().strip('"').rstrip(';')
                    fields = data_part.split('~')
                    
                    if len(fields) >= 6:
                        stocks.append({
                            "code": code,
                            "name": fields[1],
                            "price": float(fields[3]) if fields[3] else 0,
                            "change_amt": float(fields[4]) if fields[4] else 0,
                            "change_pct": float(fields[5]) if fields[5] else 0,
                            "volume": int(fields[6]) if fields[6] else 0,
                            "turnover": float(fields[37]) if len(fields) > 37 and fields[37] else 0,
                        })
                except Exception as e:
                    print(f"解析行失败：{line}, 错误：{e}")
                    continue
            
            return stocks
        except Exception as e:
            print(f"获取行情失败 (尝试 {i+1}/3): {e}")
            time.sleep(1)
    
    return []

def get_sector(code, pool):
    """获取股票所属板块"""
    # 先从板块映射查找
    for sector_name, sector_stocks in SECTOR_MAP.items():
        if code in sector_stocks:
            return sector_name
    
    # 查找股票在哪个股票池
    for pool_name, pool_data in pool.items():
        if code in pool_data.get("stocks", {}):
            return pool_name
    
    return "其他"

def check_alerts(stock_list, monitor_stocks, pool):
    """检查异动股票"""
    alerts = []
    
    for stock in stock_list:
        code = stock.get("code", "")
        if code not in monitor_stocks:
            continue
        
        name = stock.get("name", "")
        price = stock.get("price", 0)
        change_pct = stock.get("change_pct", 0)
        change_amt = stock.get("change_amt", 0)
        turnover = stock.get("turnover", 0)
        
        if price == 0:
            continue
            
        alert_types = []
        
        if change_pct >= THRESHOLDS["rapid_rise"]:
            alert_types.append(f"🚀 快速拉升 {change_pct:+.2f}%")
        
        if change_pct <= THRESHOLDS["rapid_fall"]:
            alert_types.append(f"📉 快速下跌 {change_pct:+.2f}%")
        
        if change_pct >= THRESHOLDS["limit_up"]:
            alert_types.append(f"🔥 涨停 {change_pct:.2f}%")
        
        if alert_types:
            sector = get_sector(code, pool)
            alerts.append({
                "code": code,
                "name": name,
                "price": price,
                "change_pct": change_pct,
                "change_amt": change_amt,
                "turnover": turnover,
                "sector": sector,
                "alert_types": alert_types
            })
    
    return alerts

def format_alert_message(alerts):
    """格式化飞书消息"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 按板块分组
    sector_alerts = {}
    for alert in alerts:
        sector = alert["sector"]
        if sector not in sector_alerts:
            sector_alerts[sector] = []
        sector_alerts[sector].append(alert)
    
    # 统计进攻/防御/自选
    attack_count = 0
    defense_count = 0
    custom_count = 0
    
    attack_sectors = ["新能源", "新材料", "生物医药", "高端装备", "数字经济/AI", "绿色环保"]
    defense_sectors = ["基建", "影视传媒", "石油石化", "煤炭", "电力", "贵金属"]
    
    for alert in alerts:
        if alert["sector"] in attack_sectors or alert["sector"] == "进攻板块":
            attack_count += 1
        elif alert["sector"] in defense_sectors or alert["sector"] == "防御板块":
            defense_count += 1
        else:
            custom_count += 1
    
    content = f"""📊 **A 股异动监控**
⏰ {now}
📌 进攻：{attack_count} | 防御：{defense_count} | 自选：{custom_count}

"""
    
    # 板块图标
    sector_icons = {
        "新能源": "🌞",
        "新材料": "🔬",
        "生物医药": "💊",
        "高端装备": "⚙️",
        "数字经济/AI": "💻",
        "绿色环保": "🌿",
        "基建": "🏗️",
        "影视传媒": "🎬",
        "石油石化": "🛢️",
        "煤炭": "⚫",
        "电力": "⚡",
        "贵金属": "🥇",
        "我的自选": "⭐",
    }
    
    # 排序：进攻板块 → 防御板块 → 自选
    sector_order = attack_sectors + defense_sectors + ["我的自选", "其他"]
    sorted_sectors = [s for s in sector_order if s in sector_alerts]
    
    for sector in sorted_sectors:
        sector_alert_list = sector_alerts[sector]
        icon = sector_icons.get(sector, "📌")
        content += f"\n{icon} **{sector}** ({len(sector_alert_list)}只异动)\n"
        content += "├" + "─" * 30 + "\n"
        
        for alert in sector_alert_list:
            content += f"│  {alert['name']} ({alert['code']})\n"
            content += f"│    💹 ¥{alert['price']:.2f}  ({alert['change_pct']:+.2f}%)\n"
            content += f"│    {'  '.join(alert['alert_types'])}\n"
            content += "├" + "─" * 30 + "\n"
    
    content += f"\n合计：{len(alerts)} 只股票异动"
    
    return content

def push_to_feishu(message):
    print("FEISHU_PUSH_START")
    print(message)
    print("FEISHU_PUSH_END")

def main():
    """主函数"""
    now = datetime.now()
    
    # 检查是否在交易时间内
    # 周一至周五 9:15-15:00
    if now.weekday() >= 5:  # 周末不监控
        print(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] 周末，跳过监控")
        return
    
    hour = now.hour
    minute = now.minute
    
    # 9:00-9:14 不监控 (集合竞价时间)
    if hour == 9 and minute < 15:
        print(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] 集合竞价时间，跳过监控")
        return
    
    # 15:00 之后不监控
    if hour >= 15:
        print(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] 已收盘，跳过监控")
        return
    
    print(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] 开始监控...")
    
    # 加载股票池
    monitor_stocks, pool = get_monitor_stocks()
    print(f"监控股票数：{len(monitor_stocks)}")
    
    # 统计各股票池数量
    pool_stats = {}
    for pool_name, pool_data in pool.items():
        if pool_data.get("enabled", True):
            pool_stats[pool_name] = len(pool_data.get("stocks", {}))
    print(f"股票池分布：{pool_stats}")
    
    if not monitor_stocks:
        print("⚠️  没有启用的股票池")
        return
    
    stock_data = get_stock_data(monitor_stocks.keys())
    if not stock_data:
        print("获取行情数据失败")
        return
    
    print(f"获取到 {len(stock_data)} 只股票数据")
    
    alerts = check_alerts(stock_data, monitor_stocks, pool)
    
    if not alerts:
        print("无异动股票")
        return
    
    print(f"发现 {len(alerts)} 只股票异动")
    
    # 去重检查
    last_push = load_last_push()
    new_alerts = []
    
    for alert in alerts:
        key = f"{alert['code']}_{alert['change_pct']:.1f}"
        last_time = last_push.get(key, 0)
        now = time.time()
        
        if now - last_time > 600:
            new_alerts.append(alert)
            last_push[key] = now
    
    if not new_alerts:
        print("无新异动 (已推送过)")
        return
    
    message = format_alert_message(new_alerts)
    push_to_feishu(message)
    save_last_push(last_push)
    
    print(f"已推送 {len(new_alerts)} 条异动提醒")

if __name__ == "__main__":
    main()
