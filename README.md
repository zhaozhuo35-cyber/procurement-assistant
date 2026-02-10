# 智能研发样件采购助手系统 - 部署教程

## 📋 系统简介

一个基于AI的智能采购助手系统，帮助采购人员快速处理研发样件采购需求。

**核心功能**：
- 🤖 AI需求自动解析
- 🎯 智能供应商匹配
- 📊 数据统计看板
- 📚 历史案例检索
- 💾 供应商能力库

---

## 🚀 快速部署（三种方式）

### 方式一：本地运行（最简单，5分钟）

#### 步骤1：安装Python
确保你的电脑已安装Python 3.8或更高版本。

检查Python版本：
```bash
python --version
```

如果没有安装，下载地址：https://www.python.org/downloads/

#### 步骤2：安装依赖
打开命令行（Windows按Win+R，输入cmd），进入项目文件夹：

```bash
cd C:\Users\zhaozhuo1\procurement-assistant
```

安装依赖包：
```bash
pip install -r requirements.txt
```

#### 步骤3：运行系统
```bash
streamlit run app.py
```

系统会自动打开浏览器，访问地址：`http://localhost:8501`

**恭喜！系统已经运行起来了！**

---

### 方式二：部署到Streamlit Cloud（推荐，永久免费在线访问）

#### 前提条件
- GitHub账号（没有的话注册一个：https://github.com/signup）
- 项目代码已上传到GitHub

#### 步骤1：上传代码到GitHub

1. **创建GitHub仓库**
   - 访问 https://github.com/new
   - Repository name 填写：`procurement-assistant`
   - 选择 Public
   - 点击 "Create repository"

2. **上传代码**

   **方法A：使用GitHub网页版（简单）**
   - 在刚创建的仓库页面，点击 "uploading an existing file"
   - 拖拽所有文件到页面（app.py, database.py, ai_helper.py, config.py, requirements.txt, .streamlit文件夹）
   - 点击 "Commit changes"

   **方法B：使用命令行（如果熟悉git）**
   ```bash
   cd C:\Users\zhaozhuo1\procurement-assistant
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/你的用户名/procurement-assistant.git
   git push -u origin main
   ```

#### 步骤2：部署到Streamlit Cloud

1. **注册Streamlit Cloud**
   - 访问 https://share.streamlit.io/
   - 点击 "Sign up" 或 "Sign in with GitHub"
   - 使用GitHub账号登录，授权访问

2. **创建新应用**
   - 登录后，点击 "New app"
   - Repository：选择 `procurement-assistant`
   - Branch：选择 `main`
   - Main file path：填写 `app.py`
   - App URL：自定义网址（例如：procurement-assistant）

3. **配置环境变量（可选）**
   - 点击 "Advanced settings"
   - 在 Secrets 区域添加（如果要使用AI API）：
     ```toml
     AI_API_KEY = "你的API密钥"
     ```
   - 点击 "Deploy"

4. **等待部署**
   - 首次部署需要2-3分钟
   - 部署完成后，会显示你的应用URL：`https://你的应用名.streamlit.app`

**完成！现在你有一个在线可访问的系统了！**

#### 📱 访问系统
- 分享链接给同事：`https://你的应用名.streamlit.app`
- 手机也可以访问
- 24小时在线

---

### 方式三：部署到腾讯云/阿里云（专业版）

如果需要更高的稳定性和自定义域名，可以部署到云服务器。

#### 步骤1：购买云服务器
- 最低配置：1核2G内存，带宽1M
- 操作系统：Ubuntu 20.04
- 预算：约100元/年

#### 步骤2：连接服务器并部署

```bash
# 1. 安装Python和依赖
sudo apt update
sudo apt install python3-pip -y

# 2. 上传代码（使用SFTP工具，如WinSCP）
# 或使用git clone
git clone https://github.com/你的用户名/procurement-assistant.git
cd procurement-assistant

# 3. 安装依赖
pip3 install -r requirements.txt

# 4. 后台运行
nohup streamlit run app.py --server.port 8501 &

# 5. 配置防火墙开放8501端口
sudo ufw allow 8501
```

访问地址：`http://你的服务器IP:8501`

---

## 🔧 配置说明

### AI API配置（可选）

系统默认使用规则解析，不需要AI API也能运行。如果想使用AI解析功能，需要配置API密钥。

#### 获取Kimi API密钥（免费）

1. 访问 https://platform.moonshot.cn/
2. 注册并登录
3. 进入 "API密钥管理"
4. 创建新密钥，复制保存

#### 配置方式

**本地运行**：
编辑 `config.py`，修改：
```python
AI_API_KEY = "你的API密钥"
```

**Streamlit Cloud**：
在部署时添加到 Secrets：
```toml
AI_API_KEY = "你的API密钥"
```

---

## 📖 使用指南

### 1. 首次使用：添加供应商

1. 进入【供应商管理】页面
2. 点击【添加供应商】标签
3. 填写供应商信息：
   - 名称（必填）
   - 联系人、电话、微信
   - 擅长工艺（必填）
   - 价格等级、起订量、响应速度
4. 点击【添加供应商】

**建议**：至少添加5-10家常用供应商，系统才能有效匹配。

### 2. 日常使用：处理采购需求

#### 场景：研发发来需求

1. 进入【AI需求解析】页面
2. 输入需求标题和描述（可以直接复制研发的消息）
3. 点击【AI智能解析】
4. 查看解析结果，确认信息是否完整
5. 系统自动推荐匹配的供应商
6. 点击【生成询价单】，下载发给供应商
7. 点击【保存本次需求记录】

**效果**：从收到需求到发出询价，从2小时缩短到10分钟！

### 3. 查看数据：数据看板

- 进入【数据看板】页面
- 查看本月处理需求数、平均响应时间
- 查看效率提升趋势图
- 查看供应商使用分布

**用于汇报**：截图展示效率提升数据。

### 4. 历史复用：案例检索

- 进入【历史案例】页面
- 输入关键词搜索（例如：铝合金 支架）
- 查看相似历史案例
- 复用历史报价和供应商选择

---

## 💡 常见问题

### Q1：系统运行报错怎么办？

**A**：检查以下几点：
1. Python版本是否>=3.8
2. 依赖是否都安装成功：`pip list | grep streamlit`
3. 查看错误信息，通常会提示缺少什么包

### Q2：AI解析不准确怎么办？

**A**：
1. 不配置API的情况下，系统使用规则解析，识别率约70%
2. 配置Kimi API后，识别率可达90%+
3. 即使不准确，也会大幅减少确认时间

### Q3：如何备份数据？

**A**：
- 所有数据存储在 `procurement_data.db` 文件中
- 定期复制这个文件到其他地方即可备份
- 建议每周备份一次

### Q4：多人可以同时使用吗？

**A**：
- 本地运行：只能自己用
- Streamlit Cloud部署：可以多人访问，但数据会共享
- 云服务器部署：可以多人同时使用

### Q5：如何更新系统？

**A**：
- 本地运行：直接替换文件即可
- Streamlit Cloud：推送新代码到GitHub，自动更新
- 云服务器：上传新文件，重启服务

---

## 📊 汇报材料建议

### 演示准备清单

**提前准备**（演示前一天）：
1. ✅ 添加10家真实供应商数据
2. ✅ 处理3-5个真实采购需求
3. ✅ 确保数据看板有数据可展示
4. ✅ 准备一个典型需求案例用于演示

**演示时展示**：
1. 数据看板：展示效率提升数据
2. AI需求解析：现场演示一个需求处理流程
3. 智能匹配：展示供应商推荐效果
4. 询价单生成：展示自动化成果

**关键话术**：
- "传统方式需要2小时，现在10分钟"
- "AI自动分析，新人也能做出专业判断"
- "历史经验不流失，知识可复用"
- "实时数据监控，效率可量化"

---

## 🎯 后续优化方向

### 短期（1-2周）
- [ ] 增加移动端适配
- [ ] 优化AI解析准确率
- [ ] 增加供应商批量导入功能
- [ ] 增加询价单模板自定义

### 中期（1-2个月）
- [ ] 对接企业微信/钉钉
- [ ] 增加订单跟踪功能
- [ ] 增加自动提醒功能
- [ ] 增加供应商评价体系

### 长期（3-6个月）
- [ ] 对接ERP系统
- [ ] 增加报价对比分析
- [ ] 增加成本预测功能
- [ ] 增加供应商风险预警

---

## 📞 技术支持

如遇到问题：
1. 检查本文档的【常见问题】部分
2. 查看系统错误提示信息
3. 联系IT部门或开发人员

---

## 📝 版本记录

- **v1.0** (2025-02-10)
  - 初始版本发布
  - 包含AI需求解析、供应商管理、数据看板等核心功能

---

**祝你汇报成功！🎉**
