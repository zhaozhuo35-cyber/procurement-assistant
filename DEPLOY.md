# 部署到 Streamlit Cloud 指南

## 前置准备

1. **GitHub 账号**：确保有 GitHub 账号
2. **AI API 密钥**：从 [Kimi开放平台](https://platform.moonshot.cn/) 获取 API Key

## 部署步骤

### 1. 推送代码到 GitHub

```bash
# 如果还没有推送到远程仓库
git remote add origin https://github.com/你的用户名/procurement-assistant.git
git add .
git commit -m "准备部署到 Streamlit Cloud"
git push -u origin main
```

### 2. 登录 Streamlit Cloud

1. 访问 [share.streamlit.io](https://share.streamlit.io/)
2. 使用 GitHub 账号登录
3. 授权 Streamlit Cloud 访问你的 GitHub 仓库

### 3. 创建新应用

1. 点击 "New app" 按钮
2. 选择你的仓库：`你的用户名/procurement-assistant`
3. 选择分支：`main`
4. 主文件路径：`app.py`
5. 点击 "Deploy!" 按钮

### 4. 配置 Secrets（重要）

部署开始后，点击 "Advanced settings" 或应用右下角的设置按钮：

1. 找到 "Secrets" 部分
2. 添加以下内容：

```toml
AI_API_KEY = "你的Kimi API密钥"
```

3. 保存配置

### 5. 等待部署完成

- 首次部署需要 3-5 分钟
- 部署完成后会得到一个公开访问链接
- 链接格式：`https://你的应用名.streamlit.app`

## 配置说明

### 颜色主题
已配置包豪斯风格墨绿色主题：
- 主色：#1e4f4b (墨绿色)
- 背景：#fafaf8 (米白色)

### 数据库
- 使用 SQLite 数据库
- 数据会在每次重启后重置（免费版限制）
- 如需持久化数据，考虑升级到付费版或使用外部数据库

## 常见问题

### Q: 应用无法启动？
A: 检查 Secrets 是否正确配置了 AI_API_KEY

### Q: 数据丢失了？
A: Streamlit Cloud 免费版重启后会清空数据库，建议定期导出重要数据

### Q: 如何更新应用？
A: 推送代码到 GitHub，Streamlit Cloud 会自动重新部署

```bash
git add .
git commit -m "更新说明"
git push
```

## 技术栈

- Streamlit >= 1.28.0
- Pandas >= 2.0.0
- Plotly >= 5.17.0
- Requests >= 2.31.0

## 链接

- [Streamlit Cloud 文档](https://docs.streamlit.io/streamlit-community-cloud)
- [Kimi API 文档](https://platform.moonshot.cn/docs)
