#!/bin/bash
# A 股监控服务启动脚本

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_FILE="$SCRIPT_DIR/monitor_server.pid"
LOG_FILE="$SCRIPT_DIR/monitor_server.log"

start() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p $PID > /dev/null 2>&1; then
            echo "❌ 服务已在运行中 (PID: $PID)"
            return 1
        fi
        rm -f "$PID_FILE"
    fi
    
    echo "🚀 启动 A 股监控服务..."
    cd "$SCRIPT_DIR"
    nohup /usr/local/opt/python@3.12/bin/python3.12 monitor_server.py > "$LOG_FILE" 2>&1 &
    PID=$!
    echo $PID > "$PID_FILE"
    
    sleep 2
    if ps -p $PID > /dev/null 2>&1; then
        echo "✅ 服务已启动 (PID: $PID)"
        echo "📡 访问地址：http://localhost:5050"
        echo "📋 日志文件：$LOG_FILE"
    else
        echo "❌ 服务启动失败"
        cat "$LOG_FILE"
        return 1
    fi
}

stop() {
    if [ ! -f "$PID_FILE" ]; then
        echo "⚠️  服务未运行"
        return 1
    fi
    
    PID=$(cat "$PID_FILE")
    echo "🛑 停止服务 (PID: $PID)..."
    kill $PID 2>/dev/null
    
    sleep 2
    if ps -p $PID > /dev/null 2>&1; then
        echo "⚠️  强制停止..."
        kill -9 $PID 2>/dev/null
    fi
    
    rm -f "$PID_FILE"
    echo "✅ 服务已停止"
}

restart() {
    stop
    sleep 1
    start
}

status() {
    if [ ! -f "$PID_FILE" ]; then
        echo "❌ 服务未运行"
        return 1
    fi
    
    PID=$(cat "$PID_FILE")
    if ps -p $PID > /dev/null 2>&1; then
        echo "✅ 服务运行中 (PID: $PID)"
        echo "📡 访问地址：http://localhost:5050"
        echo "📋 日志文件：$LOG_FILE"
        
        # 显示最近日志
        echo ""
        echo "📝 最近日志:"
        tail -5 "$LOG_FILE"
    else
        echo "❌ 服务已停止 (PID 文件存在但进程不存在)"
        rm -f "$PID_FILE"
        return 1
    fi
}

logs() {
    if [ ! -f "$LOG_FILE" ]; then
        echo "⚠️  日志文件不存在"
        return 1
    fi
    
    tail -50 "$LOG_FILE"
}

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    status)
        status
        ;;
    logs)
        logs
        ;;
    *)
        echo "用法：$0 {start|stop|restart|status|logs}"
        echo ""
        echo "命令:"
        echo "  start   - 启动服务"
        echo "  stop    - 停止服务"
        echo "  restart - 重启服务"
        echo "  status  - 查看状态"
        echo "  logs    - 查看日志"
        exit 1
        ;;
esac
