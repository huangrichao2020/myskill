#!/usr/local/opt/python@3.12/bin/python3.12
# -*- coding: utf-8 -*-
"""
A 股监控后端服务
使用 Flask + APScheduler 实现定时监控
"""

from flask import Flask, jsonify, request
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime, timedelta
import subprocess
import os
import sys
import json
import threading

# 添加脚本目录到路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from feishu_push import send_to_user

app = Flask(__name__)

# 全局状态
monitor_status = {
    "enabled": True,
    "last_run": None,
    "last_alerts": 0,
    "total_alerts": 0,
    "running": False
}

# 监控日志
monitor_logs = []
MAX_LOGS = 100

def add_log(message, level="info"):
    """添加日志"""
    log_entry = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "level": level,
        "message": message
    }
    monitor_logs.append(log_entry)
    if len(monitor_logs) > MAX_LOGS:
        monitor_logs.pop(0)
    print(f"[{log_entry['time']}] [{level.upper()}] {message}")

def run_monitor():
    """执行监控任务"""
    if not monitor_status["enabled"]:
        add_log("监控已禁用，跳过执行", "info")
        return
    
    if monitor_status["running"]:
        add_log("监控正在运行中，跳过本次执行", "warning")
        return
    
    now = datetime.now()
    
    # 检查是否在交易时间内
    if now.weekday() >= 5:  # 周末
        add_log("周末，跳过监控", "info")
        return
    
    hour = now.hour
    minute = now.minute
    
    # 9:00-9:14 不监控 (集合竞价)
    if hour == 9 and minute < 15:
        add_log("集合竞价时间，跳过监控", "info")
        return
    
    # 15:00 之后不监控
    if hour >= 15:
        add_log("已收盘，跳过监控", "info")
        return
    
    monitor_status["running"] = True
    add_log("开始监控...", "info")
    
    try:
        # 执行监控脚本
        monitor_script = os.path.join(SCRIPT_DIR, "stock_monitor_all.py")
        result = subprocess.run(
            ["python3.12", monitor_script],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        output = result.stdout
        add_log(output, "info")
        
        if result.stderr:
            add_log(result.stderr, "error")
        
        # 解析推送内容
        if "FEISHU_PUSH_START" in output and "FEISHU_PUSH_END" in output:
            start = output.find("FEISHU_PUSH_START") + len("FEISHU_PUSH_START")
            end = output.find("FEISHU_PUSH_END")
            message = output[start:end].strip()
            
            add_log("正在推送到飞书...", "info")
            success = send_to_user(message)
            
            if success:
                add_log("✅ 飞书推送成功", "success")
                monitor_status["last_alerts"] += 1
                monitor_status["total_alerts"] += 1
            else:
                add_log("❌ 飞书推送失败", "error")
        
        # 提取异动数量
        if "发现" in output and "只股票异动" in output:
            for line in output.split('\n'):
                if "发现" in line and "只股票异动" in line:
                    add_log(line, "info")
                    break
        
        monitor_status["last_run"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
    except subprocess.TimeoutExpired:
        add_log("监控执行超时 (60 秒)", "error")
    except Exception as e:
        add_log(f"监控执行失败：{e}", "error")
    finally:
        monitor_status["running"] = False

@app.route('/')
def index():
    """首页"""
    return jsonify({
        "service": "A 股监控服务",
        "version": "1.0.0",
        "status": "running"
    })

@app.route('/health')
def health():
    """健康检查"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "monitor_enabled": monitor_status["enabled"],
        "monitor_running": monitor_status["running"]
    })

@app.route('/status')
def status():
    """监控状态"""
    return jsonify({
        "enabled": monitor_status["enabled"],
        "running": monitor_status["running"],
        "last_run": monitor_status["last_run"],
        "last_alerts": monitor_status["last_alerts"],
        "total_alerts": monitor_status["total_alerts"],
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

@app.route('/logs')
def logs():
    """查看日志"""
    level = request.args.get('level', 'all')
    limit = request.args.get('limit', 50, type=int)
    
    filtered_logs = monitor_logs
    if level != 'all':
        filtered_logs = [log for log in monitor_logs if log['level'] == level]
    
    return jsonify({
        "logs": filtered_logs[-limit:],
        "total": len(filtered_logs)
    })

@app.route('/monitor/enable', methods=['POST'])
def enable_monitor():
    """启用监控"""
    monitor_status["enabled"] = True
    add_log("监控已启用", "success")
    return jsonify({"message": "监控已启用", "enabled": True})

@app.route('/monitor/disable', methods=['POST'])
def disable_monitor():
    """禁用监控"""
    monitor_status["enabled"] = False
    add_log("监控已禁用", "warning")
    return jsonify({"message": "监控已禁用", "enabled": False})

@app.route('/monitor/run', methods=['POST'])
def manual_run():
    """手动执行监控"""
    if monitor_status["running"]:
        return jsonify({"message": "监控正在运行中", "success": False}), 400
    
    # 在新线程中执行
    thread = threading.Thread(target=run_monitor)
    thread.start()
    
    return jsonify({"message": "监控已启动", "success": True})

@app.route('/stocks')
def stocks():
    """查看股票池"""
    pool_file = os.path.join(SCRIPT_DIR, "stock_pool.json")
    if not os.path.exists(pool_file):
        return jsonify({"error": "股票池配置文件不存在"}), 404
    
    with open(pool_file, 'r', encoding='utf-8') as f:
        pool = json.load(f)
    
    # 统计
    stats = {}
    total = 0
    for pool_name, pool_data in pool.items():
        if pool_data.get("enabled", True):
            count = len(pool_data.get("stocks", {}))
            stats[pool_name] = count
            total += count
    
    return jsonify({
        "pools": pool,
        "stats": stats,
        "total": total
    })

@app.route('/stocks/add', methods=['POST'])
def add_stock():
    """添加股票"""
    data = request.json
    pool_name = data.get('pool')
    code = data.get('code')
    name = data.get('name')
    
    if not all([pool_name, code, name]):
        return jsonify({"error": "缺少参数"}), 400
    
    # 调用管理工具
    manager_script = os.path.join(SCRIPT_DIR, "stock_manager.py")
    result = subprocess.run(
        ["python3.12", manager_script, "add", pool_name, code, name],
        capture_output=True,
        text=True
    )
    
    if "✅" in result.stdout:
        add_log(f"添加股票：{code} - {name} 到 {pool_name}", "success")
        return jsonify({"message": result.stdout.strip(), "success": True})
    else:
        return jsonify({"message": result.stdout.strip(), "success": False}), 400

def start_scheduler():
    """启动定时任务"""
    scheduler = BackgroundScheduler()
    
    # 交易日 9:15-15:00，每分钟执行
    scheduler.add_job(
        run_monitor,
        CronTrigger(minute='*', hour='9-15', day_of_week='mon-fri'),
        id='stock_monitor',
        name='A 股监控',
        replace_existing=True
    )
    
    scheduler.start()
    add_log("定时任务已启动 (交易日 9:15-15:00)", "success")
    return scheduler

if __name__ == '__main__':
    print("=" * 60)
    print("A 股监控服务启动中...")
    print("=" * 60)
    
    # 启动定时任务
    scheduler = start_scheduler()
    
    # 启动 Web 服务
    print("Web 服务监听：http://localhost:5050")
    print("API 文档:")
    print("  GET  /          - 服务信息")
    print("  GET  /health    - 健康检查")
    print("  GET  /status    - 监控状态")
    print("  GET  /logs      - 查看日志")
    print("  GET  /stocks    - 股票池")
    print("  POST /monitor/enable  - 启用监控")
    print("  POST /monitor/disable - 禁用监控")
    print("  POST /monitor/run     - 手动执行")
    print("=" * 60)
    
    try:
        app.run(host='0.0.0.0', port=5050, debug=False, threaded=True)
    except KeyboardInterrupt:
        print("\n服务停止中...")
        scheduler.shutdown()
        print("服务已停止")
