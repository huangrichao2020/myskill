#!/usr/local/opt/python@3.12/bin/python3.12
# -*- coding: utf-8 -*-
"""
自选股管理工具
添加、删除、查看自选股票
"""

import json
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STOCK_POOL_FILE = os.path.join(SCRIPT_DIR, "stock_pool.json")

def load_pool():
    """加载股票池"""
    if os.path.exists(STOCK_POOL_FILE):
        with open(STOCK_POOL_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_pool(pool):
    """保存股票池"""
    with open(STOCK_POOL_FILE, 'w', encoding='utf-8') as f:
        json.dump(pool, f, ensure_ascii=False, indent=2)

def list_pools():
    """列出所有股票池"""
    pool = load_pool()
    print("\n📊 股票池列表:\n")
    for name, data in pool.items():
        status = "✅" if data.get("enabled", True) else "❌"
        count = len(data.get("stocks", {}))
        print(f"  {status} {name}: {count} 只股票")
    print()

def list_stocks(pool_name):
    """列出指定股票池的股票"""
    pool = load_pool()
    if pool_name not in pool:
        print(f"❌ 股票池 '{pool_name}' 不存在")
        return
    
    stocks = pool[pool_name].get("stocks", {})
    print(f"\n📈 {pool_name} ({len(stocks)}只):\n")
    for code, name in sorted(stocks.items()):
        market = "沪市" if code.startswith("sh") else "深市"
        print(f"  {code} - {name} ({market})")
    print()

def add_stock(pool_name, code, name):
    """添加股票到指定股票池"""
    pool = load_pool()
    
    if pool_name not in pool:
        print(f"❌ 股票池 '{pool_name}' 不存在")
        print("   可用股票池:", list(pool.keys()))
        return False
    
    # 标准化代码格式
    if code.startswith("sh") or code.startswith("sz"):
        pass
    elif code.startswith("6") or code.startswith("9"):
        code = "sh" + code
    elif code.startswith("0") or code.startswith("3"):
        code = "sz" + code
    else:
        print(f"❌ 代码格式错误：{code}")
        return False
    
    # 添加到股票池
    if "stocks" not in pool[pool_name]:
        pool[pool_name]["stocks"] = {}
    
    pool[pool_name]["stocks"][code] = name
    save_pool(pool)
    
    print(f"✅ 已添加：{code} - {name} 到 '{pool_name}'")
    return True

def remove_stock(pool_name, code):
    """从股票池删除股票"""
    pool = load_pool()
    
    if pool_name not in pool:
        print(f"❌ 股票池 '{pool_name}' 不存在")
        return False
    
    # 标准化代码格式
    if not code.startswith("sh") and not code.startswith("sz"):
        # 尝试自动匹配
        for full_code in pool[pool_name].get("stocks", {}).keys():
            if full_code.endswith(code):
                code = full_code
                break
    
    if code not in pool[pool_name].get("stocks", {}):
        print(f"❌ 股票 '{code}' 不在 '{pool_name}' 中")
        return False
    
    name = pool[pool_name]["stocks"].pop(code)
    save_pool(pool)
    
    print(f"✅ 已删除：{code} - {name} 从 '{pool_name}'")
    return True

def toggle_pool(pool_name):
    """启用/禁用股票池"""
    pool = load_pool()
    
    if pool_name not in pool:
        print(f"❌ 股票池 '{pool_name}' 不存在")
        return False
    
    current = pool[pool_name].get("enabled", True)
    pool[pool_name]["enabled"] = not current
    save_pool(pool)
    
    status = "启用" if not current else "禁用"
    print(f"✅ 已{status}股票池 '{pool_name}'")
    return True

def create_pool(pool_name):
    """创建新股票池"""
    pool = load_pool()
    
    if pool_name in pool:
        print(f"⚠️  股票池 '{pool_name}' 已存在")
        return False
    
    pool[pool_name] = {
        "enabled": True,
        "stocks": {}
    }
    save_pool(pool)
    
    print(f"✅ 已创建股票池 '{pool_name}'")
    return True

def delete_pool(pool_name):
    """删除股票池"""
    pool = load_pool()
    
    if pool_name not in pool:
        print(f"❌ 股票池 '{pool_name}' 不存在")
        return False
    
    if pool_name in ["进攻板块", "防御板块"]:
        print(f"⚠️  不能删除系统股票池 '{pool_name}'")
        return False
    
    del pool[pool_name]
    save_pool(pool)
    
    print(f"✅ 已删除股票池 '{pool_name}'")
    return True

def print_help():
    """打印帮助信息"""
    help_text = """
📊 自选股管理工具

用法:
  python3.12 stock_manager.py <命令> [参数]

命令:
  list                          列出所有股票池
  show <股票池名>               显示股票池中的所有股票
  add <股票池名> <代码> <名称>   添加股票
  remove <股票池名> <代码>       删除股票
  enable <股票池名>             启用股票池
  disable <股票池名>            禁用股票池
  create <股票池名>             创建新股票池
  delete <股票池名>             删除股票池

示例:
  python3.12 stock_manager.py list
  python3.12 stock_manager.py show 我的自选
  python3.12 stock_manager.py add 我的自选 600519 贵州茅台
  python3.12 stock_manager.py add 我的自选 sz000858 五粮液
  python3.12 stock_manager.py remove 我的自选 sh600519
  python3.12 stock_manager.py disable 防御板块
  python3.12 stock_manager.py create 科技股

股票池说明:
  - 进攻板块：十五五规划龙头股 (33 只)
  - 防御板块：基建/影视/石油/煤炭/电力/贵金属 (40 只)
  - 我的自选：自定义股票 (可自由添加)
"""
    print(help_text)

def main():
    if len(sys.argv) < 2:
        print_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == "list":
        list_pools()
    
    elif command == "show" and len(sys.argv) >= 3:
        list_stocks(sys.argv[2])
    
    elif command == "add" and len(sys.argv) >= 5:
        pool_name = sys.argv[2]
        code = sys.argv[3]
        name = sys.argv[4]
        add_stock(pool_name, code, name)
    
    elif command == "remove" and len(sys.argv) >= 4:
        pool_name = sys.argv[2]
        code = sys.argv[3]
        remove_stock(pool_name, code)
    
    elif command == "enable" and len(sys.argv) >= 3:
        toggle_pool(sys.argv[2])
    
    elif command == "disable" and len(sys.argv) >= 3:
        toggle_pool(sys.argv[2])
    
    elif command == "create" and len(sys.argv) >= 3:
        create_pool(sys.argv[2])
    
    elif command == "delete" and len(sys.argv) >= 3:
        delete_pool(sys.argv[2])
    
    else:
        print(f"❌ 未知命令：{command}")
        print_help()

if __name__ == "__main__":
    main()
