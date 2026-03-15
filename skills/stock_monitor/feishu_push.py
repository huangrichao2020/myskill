#!/usr/local/opt/python@3.12/bin/python3.12
# -*- coding: utf-8 -*-
"""
飞书消息推送工具
使用飞书开放平台 API 发送消息
"""

import requests
import json
import time
import hashlib
import hmac
import base64
from datetime import datetime

# 飞书应用配置
APP_ID = "cli_a92c559deaf81bc8"
APP_SECRET = "F5wh32gKae72aa5ucEAGTfxnIuOPkGjq"

# 缓存 tenant_access_token
TOKEN_CACHE = {
    "token": None,
    "expire_time": 0
}

def get_tenant_access_token():
    """获取飞书 tenant_access_token"""
    now = time.time()
    
    # 检查缓存
    if TOKEN_CACHE["token"] and now < TOKEN_CACHE["expire_time"]:
        return TOKEN_CACHE["token"]
    
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    payload = {
        "app_id": APP_ID,
        "app_secret": APP_SECRET
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        data = response.json()
        
        if data.get("code") == 0:
            token = data.get("tenant_access_token")
            # 缓存 2 小时 (飞书 token 有效期 2 小时)
            TOKEN_CACHE["token"] = token
            TOKEN_CACHE["expire_time"] = now + 7000
            return token
        else:
            print(f"获取 token 失败：{data}")
            return None
    except Exception as e:
        print(f"获取 token 异常：{e}")
        return None

def send_message(user_id, message, msg_type="text"):
    """发送消息到飞书"""
    token = get_tenant_access_token()
    if not token:
        return False
    
    # receive_id_type 需要作为 query 参数
    url = f"https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # 飞书消息格式
    if msg_type == "text":
        content = {
            "text": message
        }
    elif msg_type == "post":
        content = {
            "zh_cn": {
                "title": "📊 A 股异动监控",
                "content": [
                    [{"tag": "text", "text": message}]
                ]
            }
        }
    else:
        content = {"text": message}
    
    payload = {
        "receive_id": user_id,
        "msg_type": msg_type,
        "content": json.dumps(content, ensure_ascii=False),
        "receive_id_type": "open_id"
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        data = response.json()
        
        if data.get("code") == 0:
            print(f"消息发送成功")
            return True
        else:
            print(f"消息发送失败：{data}")
            return False
    except Exception as e:
        print(f"发送消息异常：{e}")
        return False

def send_to_user(message):
    """发送消息给用户 (超哥)"""
    # 超哥的 open_id (从 memory 中获取)
    user_open_id = "ou_872241e9e24c06e452befa9cb27c35c1"
    return send_message(user_open_id, message, msg_type="text")

if __name__ == "__main__":
    # 测试
    test_msg = f"测试消息 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    success = send_to_user(test_msg)
    print(f"测试结果：{'成功' if success else '失败'}")
