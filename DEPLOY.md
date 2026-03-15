# 推送到 GitHub

## 第一步：创建 GitHub 仓库

1. 访问 https://github.com/new
2. 仓库名称：`myskill`
3. 描述：`Personal automation skills collection`
4. 公开仓库 ✅
5. 点击 **Create repository**

## 第二步：关联远程仓库

```bash
cd /Users/tingchi/myskill

# 替换 <your_username> 为你的 GitHub 用户名
git remote add origin https://github.com/<your_username>/myskill.git

# 验证
git remote -v
```

## 第三步：推送代码

```bash
# 推送到 main 分支
git branch -M main
git push -u origin main
```

## 第四步：验证

访问 `https://github.com/<your_username>/myskill` 查看代码

---

## 后续更新

```bash
cd /Users/tingchi/myskill

# 添加新技能后
git add -A
git commit -m "Add <skill_name> skill"
git push
```
