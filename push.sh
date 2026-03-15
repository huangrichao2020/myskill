#!/bin/bash
# 一键推送到 GitHub 脚本

REPO_DIR="/Users/tingchi/myskill"
REPO_NAME="myskill"

cd "$REPO_DIR"

echo "🔍 检查 Git 配置..."

# 检查是否配置了 Git 用户信息
if ! git config user.name > /dev/null 2>&1; then
    echo "⚠️  未配置 Git 用户名"
    read -p "请输入 Git 用户名: " GIT_USER
    git config user.name "$GIT_USER"
fi

if ! git config user.email > /dev/null 2>&1; then
    echo "⚠️  未配置 Git 邮箱"
    read -p "请输入 Git 邮箱： " GIT_EMAIL
    git config user.email "$GIT_EMAIL"
fi

echo "✅ Git 配置完成"
echo ""

# 检查远程仓库
REMOTE=$(git remote get-url origin 2>/dev/null)
if [ -z "$REMOTE" ]; then
    echo "📝 请输入 GitHub 仓库地址:"
    echo "   格式：https://github.com/YOUR_USERNAME/myskill.git"
    echo "   或：git@github.com:YOUR_USERNAME/myskill.git"
    read -p "> " REPO_URL
    
    git remote add origin "$REPO_URL"
    echo "✅ 远程仓库已添加：$REPO_URL"
else
    echo "✅ 远程仓库已配置：$REMOTE"
fi

echo ""
echo "🚀 开始推送..."

# 确保分支名为 main
git branch -M main 2>/dev/null

# 推送
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 推送成功！"
    echo ""
    echo "📦 仓库地址：$REPO_URL"
    echo "🌐 访问地址：$(echo $REPO_URL | sed 's/.git$//' | sed 's/git@github.com:/https:\/\/github.com\//')"
else
    echo ""
    echo "❌ 推送失败"
    echo ""
    echo "可能的原因:"
    echo "  1. 未配置 SSH 密钥"
    echo "  2. 仓库不存在"
    echo "  3. 认证失败"
    echo ""
    echo "解决方案:"
    echo "  1. 在 GitHub 创建仓库：https://github.com/new"
    echo "     仓库名称：myskill"
    echo "  2. 配置 SSH 密钥：https://docs.github.com/en/authentication/connecting-to-github-with-ssh"
    echo "  3. 或使用 HTTPS + Personal Access Token"
fi
