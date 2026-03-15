# 🚀 推送到 GitHub - 3 步完成

## 方式一：一键推送脚本（推荐）

```bash
cd /Users/tingchi/myskill
./push.sh
```

脚本会自动：
1. 检查 Git 配置
2. 引导你输入仓库地址
3. 推送到 GitHub

---

## 方式二：手动推送

### 第 1 步：在 GitHub 创建仓库

1. 访问 https://github.com/new
2. 填写：
   - **Repository name**: `myskill`
   - **Description**: `Personal automation skills collection`
   - **Public** ✅ (公开)
   - **Initialize with README**: ❌ (不要勾选)
3. 点击 **Create repository**

### 第 2 步：关联远程仓库

```bash
cd /Users/tingchi/myskill

# 替换 YOUR_USERNAME 为你的 GitHub 用户名
git remote add origin https://github.com/YOUR_USERNAME/myskill.git

# 或 SSH 方式 (如果配置了 SSH 密钥)
# git remote add origin git@github.com:YOUR_USERNAME/myskill.git
```

### 第 3 步：推送代码

```bash
# 确保分支名为 main
git branch -M main

# 推送
git push -u origin main
```

---

## 🔐 认证方式

### HTTPS 方式

如果提示输入密码，需要使用 **Personal Access Token**：

1. 访问 https://github.com/settings/tokens
2. 点击 **Generate new token (classic)**
3. 勾选 `repo` 权限
4. 生成后复制 token
5. 推送时使用 token 作为密码

### SSH 方式（推荐）

1. 生成 SSH 密钥：
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   ```

2. 添加公钥到 GitHub：
   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```
   复制输出，访问 https://github.com/settings/keys 添加

3. 测试连接：
   ```bash
   ssh -T git@github.com
   ```

---

## ✅ 验证推送

推送成功后，访问：
```
https://github.com/YOUR_USERNAME/myskill
```

应该能看到：
- ✅ README.md
- ✅ skills/stock_monitor/ 目录
- ✅ 所有代码文件

---

## 📝 后续更新

添加新技能后：

```bash
cd /Users/tingchi/myskill
git add -A
git commit -m "Add <skill_name> skill"
git push
```

---

## 🆘 常见问题

### 1. 提示 "repository not found"

确保已在 GitHub 创建仓库，并且仓库地址正确。

### 2. 提示 "Permission denied"

- HTTPS: 使用 Personal Access Token 代替密码
- SSH: 检查 SSH 密钥是否已添加到 GitHub

### 3. 推送被拒绝

```bash
# 如果是首次推送
git push -u origin main --force
```

---

## 📞 需要帮助？

运行一键脚本会自动引导你完成：

```bash
cd /Users/tingchi/myskill
./push.sh
```
