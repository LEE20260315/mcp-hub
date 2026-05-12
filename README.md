# 🚀 MCP Hub — AI Agent 超级工具箱

**12 个精选 MCP 服务器，一键安装到 Trae / Claude Desktop / Cursor / VS Code / Windsurf。**

[![MCP Servers](https://img.shields.io/badge/MCP%20Servers-12-blue)](mcp.json)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📦 MCP 工具详解

---

### 1. 📁 Filesystem — 安全文件系统操作

> **官方 MCP 文件系统服务器，赋予 AI 安全读写本地文件的能力。**

| 属性 | 详情 |
|------|------|
| 包名 | `@modelcontextprotocol/server-filesystem` |
| 运行环境 | Node.js (npx) |
| 配置路径 | 需指定允许访问的目录 (如 `~/Desktop`) |

**核心能力：**
- 读取文本文件内容
- 写入/创建/编辑文件
- 列出目录结构
- 搜索文件（支持通配符）
- 获取文件元信息（大小、修改时间、权限）
- 移动/重命名文件
- 创建目录

**安全机制：**
只能在配置时指定的目录范围内操作，无法越权访问系统敏感路径。

**典型用法：**
```
"帮我读取桌面上 project/readme.md 的内容"
"把 data.csv 的前10行提取出来写到 summary.txt"
"在 docs 目录下搜索所有包含 'API' 关键词的 .md 文件"
```

---

### 2. 🖥️ Desktop Commander — 桌面终端总控

> **强大的桌面命令执行器，让 AI 可以操控终端、管理文件和进程。**

| 属性 | 详情 |
|------|------|
| 包名 | `@wonderwhy-er/desktop-commander` |
| 运行环境 | Node.js (npx) |

**核心能力：**
- 执行任意 Shell/终端命令（受安全策略限制）
- 读取/写入/创建/删除文件和目录
- 管理进程（启动、查看、终止）
- 多终端会话管理
- 支持在指定工作目录执行命令
- 长命令状态追踪（异步执行 + 结果轮询）

**典型用法：**
```
"帮我运行 npm install 安装依赖"
"查看当前正在运行的 Node.js 进程"
"在 /project 目录下执行 git log --oneline -10"
"递归删除 node_modules 文件夹"
```

---

### 3. 🧠 Sequential Thinking — 链式深度推理

> **结构化思考引擎，帮助 AI 将复杂问题拆解为循序渐进的推理步骤。**

| 属性 | 详情 |
|------|------|
| 包名 | `@modelcontextprotocol/server-sequential-thinking` |
| 运行环境 | Node.js (npx) |

**核心能力：**
- 将复杂问题分解为多步推理链
- 每步思考可修正/推翻前一步的结论
- 支持分支推理（探索多种思路）
- 生成思考总结与最终结论
- 适合数学证明、逻辑推理、架构设计、Bug 定位

**典型用法：**
```
"帮我推演这个递归算法的时间复杂度"
"分析为什么这个 API 在高并发下会出现竞态条件"
"设计一个分布式锁方案，逐步推演其正确性"
```

---

### 4. 🗂️ Memory — 持久化知识图谱记忆

> **基于知识图谱的长期记忆系统，让 AI 在多次对话间保持上下文。**

| 属性 | 详情 |
|------|------|
| 包名 | `@modelcontextprotocol/server-memory` |
| 运行环境 | Node.js (npx) |

**核心能力：**
- 创建/更新/删除知识实体（Entity）
- 建立实体之间的关系（Relation）
- 对实体添加观察笔记（Observation）
- 全文搜索已存储的知识
- 跨会话持久化记忆

**典型用法：**
```
"记住我的项目 test-app 用的是 PostgreSQL 数据库，端口 5432"
"我之前跟你讨论过的那个用户认证方案是什么来着？"
"搜索所有与 '微服务' 相关的记忆"
```

---

### 5. 📚 context7 — 实时文档上下文注入

> **在代码生成时自动注入最新的第三方库文档，避免 AI 使用过时的 API。**

| 属性 | 详情 |
|------|------|
| 包名 | `@upstash/context7-mcp@latest` |
| 运行环境 | Node.js (npx) |

**核心能力：**
- 查询主流开源库的最新 API 文档
- 自动获取函数签名、参数说明、示例代码
- 覆盖 npm、PyPI 等生态的主流库
- 让 AI 写代码时不再「编造」不存在的 API

**典型用法：**
```
"用 Next.js 14 的 App Router 怎么写 API 路由？查一下最新文档"
"React 19 的 useOptimistic hook 怎么用？"
"Python 的 Pydantic v2 数据校验怎么写？查文档"
```

---

### 6. 🌐 Puppeteer — 无头浏览器自动化

> **通过 Puppeteer 操控无头 Chrome，实现网页截图、爬虫、表单填充等。**

| 属性 | 详情 |
|------|------|
| 包名 | `@modelcontextprotocol/server-puppeteer` |
| 运行环境 | Node.js (npx) + Chrome |

**核心能力：**
- 导航到任意 URL
- 页面截图（全页/元素级）
- 点击元素、填写表单
- 在页面中执行 JavaScript
- 获取页面内容（HTML/文本）
- 模拟用户交互流程

**典型用法：**
```
"打开 https://example.com 并截个全页截图"
"帮我把这个网页的标题和所有链接提取出来"
"自动填写这个注册表单：用户名 test, 邮箱 test@test.com"
```

---

### 7. 🔍 DuckDuckGo Search — 隐私网络搜索

> **通过 DuckDuckGo 进行网络搜索，不追踪、不记录，隐私优先。**

| 属性 | 详情 |
|------|------|
| 包名 | `duckduckgo-mcp-server` |
| 运行环境 | Python (uvx) |
| 镜像加速 | `https://pypi.tuna.tsinghua.edu.cn/simple` |

**核心能力：**
- 网页关键词搜索
- 获取搜索结果摘要和链接
- 隐私保护（DuckDuckGo 不追踪用户）
- 适合实时信息查询、技术问题搜索

**典型用法：**
```
"帮我搜索一下 React 19 的最新特性"
"查一下今天北京的天气"
"搜索 'Golang 泛型最佳实践' 看看有什么好文章"
```

---

### 8. 🕊️ lark-mcp — 飞书/Lark 深度集成

> **连接飞书开放平台，让 AI 可以读写飞书文档、消息、表格等。**

| 属性 | 详情 |
|------|------|
| 包名 | `@larksuiteoapi/lark-mcp` |
| 运行环境 | Node.js (npx) |
| 认证方式 | 需要 APP_ID + APP_SECRET（环境变量配置） |

**核心能力：**
- 读取/创建/编辑飞书文档
- 发送和接收飞书消息
- 操作飞书多维表格/电子表格
- 管理飞书日历和日程
- 飞书审批/任务操作

**配置方法：**
1. 前往 [飞书开放平台](https://open.feishu.cn/app) 创建企业自建应用
2. 获取 App ID 和 App Secret
3. 设置环境变量或通过安装脚本参数传入

**典型用法：**
```
"帮我把这段内容写入飞书文档"
"查看飞书上「项目周报」多维表格的最新数据"
"给飞书群发一条消息：今晚8点开会"
```

---

### 9. 📊 Excel — Excel 文件专业处理

> **直接读写 .xlsx 文件，支持大文件分页读取，避免内存溢出。**

| 属性 | 详情 |
|------|------|
| 包名 | `@negokaz/excel-mcp-server` |
| 运行环境 | Node.js (npx) |
| 分页限制 | 默认每页 4000 单元格（可调整） |

**核心能力：**
- 读取 .xlsx 文件的指定 Sheet 和单元格范围
- 写入数据到 Excel 文件
- 支持大文件分页读取（防止上下文溢出）
- 获取 Sheet 名称列表、行列信息
- 创建新的 Excel 文件

**典型用法：**
```
"帮我读取 data.xlsx 的 Sheet1 中 A1:D100 的数据"
"把这个 JSON 数据导出为 Excel 文件"
"分析 sales.xlsx 中 'Q4销售额' 列的平均值和最大值"
```

---

### 10. 🛠️ Chrome DevTools MCP — 浏览器调试利器

> **接入 Chrome DevTools Protocol，实现性能分析、DOM 检查、网络监控等。**

| 属性 | 详情 |
|------|------|
| 包名 | `chrome-devtools-mcp@latest` |
| 运行环境 | Node.js (npx) + Chrome |

**核心能力：**
- 性能追踪与分析（Core Web Vitals：LCP、INP、CLS）
- Lighthouse 审计（SEO、可访问性、最佳实践）
- 页面 DOM 快照分析
- 网络请求监控与检查
- 控制台消息查看
- 内存堆快照分析
- 模拟设备/网络/地理位置
- 元素点击、悬停、拖拽

**典型用法：**
```
"帮我分析这个网页的 LCP (最大内容绘制) 性能瓶颈"
"对这个网页做一次 Lighthouse SEO 审计"
"检查页面加载时的所有网络请求，看哪个最慢"
"截取这个按钮元素的截图"
```

---

### 11. 📋 发现报告 — FX 报告生成器

> **自动生成发现报告的 MCP 服务。**

| 属性 | 详情 |
|------|------|
| 包名 | `fxbaogao-mcp@latest` |
| 运行环境 | Python (uvx) |
| 镜像加速 | `https://pypi.tuna.tsinghua.edu.cn/simple` |

**核心能力：**
- 生成结构化的发现报告
- 支持多种报告模板
- 自动化数据汇总和分析

**典型用法：**
```
"帮我生成一份关于 XX 问题的发现报告"
"基于这些数据生成分析总结报告"
```

---

### 12. 🎭 Playwright — 跨浏览器自动化测试

> **支持 Chromium / Firefox / WebKit 的浏览器自动化，比 Puppeteer 支持更多浏览器。**

| 属性 | 详情 |
|------|------|
| 包名 | `@playwright/mcp` |
| 运行环境 | Node.js (npx) |

**核心能力：**
- 多浏览器支持（Chromium / Firefox / WebKit）
- 页面导航和截图
- 元素定位与交互（点击、输入、选择）
- 网络请求拦截与 mock
- 移动设备模拟
- 文件上传/下载
- 跨页面/跨域操作
- 浏览器控制台消息读取

**典型用法：**
```
"用 Firefox 打开这个网页看看渲染是否正常"
"模拟 iPhone 14 访问这个页面并截图"
"自动化测试这个登录流程，填写用户名和密码并点击登录"
"拦截页面中所有对 /api/ 的请求并记录响应时间"
```---
## ⚡ 快速安装

### Windows (PowerShell)
```powershell
git clone https://github.com/LEE20260315/mcp-hub.git
cd mcp-hub
.\install.ps1                  # 安装到所有客户端
.\install.ps1 -Client trae     # 只安装到 Trae
.\install.ps1 -LarkAppId "your_id" -LarkAppSecret "your_secret"
```

### macOS / Linux
```bash
git clone https://github.com/LEE20260315/mcp-hub.git
cd mcp-hub
chmod +x install.sh
./install.sh                   # 安装到所有客户端
./install.sh claude            # 只安装到 Claude Desktop
./install.sh all "your_id" "your_secret"
```

---
## 🎯 客户端支持矩阵

| 客户端 | Windows | macOS | Linux | 配置路径 |
|--------|:-------:|:-----:|:-----:|---------|
| **Trae IDE** | ✅ | — | — | `%APPDATA%\Trae CN\User\mcp.json` |
| **Claude Desktop** | ✅ | ✅ | ✅ | `~/...Claude/claude_desktop_config.json` |
| **Cursor** | ✅ | ✅ | ✅ | `~/.cursor/mcp.json` |
| **VS Code (Cline)** | ✅ | ✅ | ✅ | `~/.config/Code/.../mcp_settings.json` |
| **Windsurf** | ✅ | ✅ | ✅ | `~/.windsurf/mcp.json` |

---
## 📋 前置依赖

| 依赖 | 需要的服务器 | 安装方式 |
|------|------------|---------|
| **Node.js** (>=18 LTS) | 1-6, 8-10, 12 | [nodejs.org](https://nodejs.org) |
| **Python 3.9+ + uv** | 7, 11 | `pip install uv` |
| **Chrome 浏览器** | 6, 10 | [google.com/chrome](https://google.com/chrome) |

---
## 🔐 环境变量配置

| 变量名 | 所属服务器 | 说明 |
|--------|----------|------|
| `LARK_APP_ID` | lark-mcp | 飞书开放平台应用 ID |
| `LARK_APP_SECRET` | lark-mcp | 飞书开放平台应用密钥 |
| `UV_INDEX_URL` | DuckDuckGo / 发现报告 | PyPI 镜像加速（清华源） |

复制 `.env.example` 填入凭证：
```bash
cp .env.example .env
```

> ⚠️ `.env` 已加入 `.gitignore`，切勿提交真实密钥。

---
## 🛠️ 自定义

**修改 Filesystem 允许的目录** — 编辑 [mcp.json](mcp.json) 中 `Filesystem.args`

**禁用某个服务器** — 在 [mcp.json](mcp.json) 中删除对应条目

**添加新 MCP** — 在 `mcpServers` 中添加：
```json
"你的服务器名": {
  "command": "npx",
  "args": ["-y", "你的-npm-包名"],
  "env": {}
}
```

---
## 📁 项目结构
```
mcp-hub/
├── mcp.json                      ← 核心 MCP 配置（12个服务器）
├── install.ps1                   ← Windows 一键安装
├── install.sh                    ← macOS/Linux 一键安装
├── .env.example / .gitignore
├── README.md
└── clients/                      ← 各客户端专属配置
    ├── trae/         → Trae IDE
    ├── claude-desktop/ → Claude Desktop
    ├── cursor/       → Cursor
    ├── vscode/       → VS Code (Cline)
    └── windsurf/     → Windsurf
```

---
## ❓ FAQ

**Q: 安装后 MCP 启动失败？**
A: 确保 Node.js >=18 已安装。首次 `npx` 需下载包。部分工具需 `pip install uv`。

**Q: Puppeteer / Playwright 提示无浏览器？**
A: 首次运行自动下载 Chrome/Chromium。网络不畅可设 `PUPPETEER_DOWNLOAD_BASE_URL` 镜像。

**Q: Lark 飞书报 401？**
A: 检查 APP_ID / APP_SECRET，确认飞书开放平台已开启应用权限。

**Q: Filesystem 无法访问目录？**
A: 编辑 mcp.json 的 Filesystem args，添加允许目录。支持多个路径参数。

---
## 📄 License
MIT