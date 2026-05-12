# 🚀 MCP Hub - AI Agent 超级工具箱

**12 个精选 MCP 服务器，一键安装到所有主流 AI Agent 客户端。**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![MCP Servers](https://img.shields.io/badge/MCP%20Servers-12-blue)](mcp.json)

---

## 📦 包含的 MCP 服务器

| # | MCP 服务器 | 功能 | 运行环境 |
|---|-----------|------|---------|
| 1 | **Filesystem** | 安全的文件系统读写操作 | Node.js |
| 2 | **Desktop Commander** | 终端命令执行、文件管理、进程控制 | Node.js |
| 3 | **Sequential Thinking** | 链式思考推理引擎 | Node.js |
| 4 | **Memory** | 知识图谱持久化记忆系统 | Node.js |
| 5 | **context7** | 第三方库文档上下文增强 | Node.js |
| 6 | **Puppeteer** | 无头浏览器自动化操作 | Node.js |
| 7 | **DuckDuckGo Search** | 隐私保护的网络搜索 | Python (uvx) |
| 8 | **lark-mcp** | 飞书/Lark 文档与消息集成 | Node.js |
| 9 | **Excel** | Excel 文件读写与处理 | Node.js |
| 10 | **Chrome DevTools** | Chrome 浏览器调试与性能分析 | Node.js |
| 11 | **发现报告** | 发现报告生成 | Python (uvx) |
| 12 | **Playwright** | 跨浏览器自动化测试 | Node.js |

---

## 🎯 支持的 AI Agent 客户端

| 客户端 | 平台 | 配置路径 |
|--------|------|---------|
| **Trae IDE** | Windows | `%APPDATA%\Trae CN\User\mcp.json` |
| **Claude Desktop** | Windows | `%APPDATA%\Claude\claude_desktop_config.json` |
| **Claude Desktop** | macOS | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| **Cursor** | 全平台 | `~/.cursor/mcp.json` |
| **VS Code (Cline)** | 全平台 | `~/.config/Code/User/globalStorage/.../mcp_settings.json` |
| **Windsurf** | 全平台 | `~/.windsurf/mcp.json` |

---

## ⚡ 快速安装

### 方式一：一键安装（推荐）

**Windows (PowerShell):**
```powershell
# 安装到所有客户端
.\install.ps1

# 只安装到指定客户端
.\install.ps1 -Client trae
.\install.ps1 -Client claude

# 同时配置 Lark 飞书凭证
.\install.ps1 -LarkAppId "your_app_id" -LarkAppSecret "your_secret"
```

**macOS / Linux:**
```bash
# 安装到所有支持的客户端
chmod +x install.sh
./install.sh

# 只安装到指定客户端
./install.sh claude
./install.sh cursor

# 同时配置 Lark 飞书凭证
./install.sh all "your_app_id" "your_app_secret"
```

### 方式二：手动安装

1. 复制 `mcp.json` 内容
2. 粘贴到对应客户端的 MCP 配置文件中
3. 重启客户端

### 方式三：仅用特定服务器

从 `mcp.json` 中选择你需要的条目，添加到你的客户端配置中。

---

## 📋 前置依赖

| 依赖 | 需要它的服务器 | 安装方式 |
|------|-------------|---------|
| **Node.js** (>=18) | Filesystem, Commander, Thinking, Memory, Puppeteer, Lark, Excel, Chrome, Playwright | [nodejs.org](https://nodejs.org) |
| **Python + uv** | DuckDuckGo, 发现报告 | `pip install uv` |
| **Chrome** | Puppeteer, Chrome DevTools | [google.com/chrome](https://google.com/chrome) |

---

## 🔐 环境变量配置

部分 MCP 服务器需要通过环境变量配置密钥：

| 服务器 | 环境变量 | 说明 |
|--------|---------|------|
| lark-mcp | `LARK_APP_ID` | 飞书应用 ID |
| lark-mcp | `LARK_APP_SECRET` | 飞书应用密钥 |

复制 `.env.example` 并填入你的凭证：
```bash
cp .env.example .env
# 编辑 .env 填入你的 Lark 凭证
```

> ⚠️ **安全提醒**: `.env` 文件已加入 `.gitignore`，切勿将包含真实密钥的文件提交到仓库。

---

## 🛠️ 自定义

### 调整 Filesystem 允许的目录

编辑 `mcp.json` 中 Filesystem 的 `args`：
```json
"args": ["-y", "@modelcontextprotocol/server-filesystem", "/your/custom/path"]
```

### 禁用某个服务器

直接删除 `mcp.json` 中对应条目即可。

### 添加新服务器

在 `mcp.json` 的 `mcpServers` 中添加：
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
├── mcp.json                  # 通用 MCP 配置（主文件）
├── install.ps1               # Windows 一键安装脚本
├── install.sh                # macOS/Linux 一键安装脚本
├── .env.example              # 环境变量模板
├── .gitignore
├── clients/
│   ├── trae/
│   │   └── mcp.json          # Trae IDE 配置
│   ├── claude-desktop/
│   │   └── claude_desktop_config.json  # Claude Desktop 配置
│   ├── cursor/
│   │   └── mcp.json          # Cursor 配置
│   ├── vscode/
│   │   └── mcp.json          # VS Code 配置
│   └── windsurf/
│       └── mcp.json          # Windsurf 配置
└── README.md
```

---

## ❓ 常见问题

**Q: 安装后 MCP 服务器无法启动？**
A: 确保 Node.js (>=18) 已安装且 `npx` 可用。首次启动可能需要下载 npm 包，请耐心等待。

**Q: uvx 命令不存在？**
A: 安装 `pip install uv`，然后确保 Python 的 Scripts 目录在 PATH 中。

**Q: Lark 飞书集成如何配置？**
A: 前往 [飞书开放平台](https://open.feishu.cn/app) 创建应用，获取 App ID 和 App Secret。

**Q: Puppeteer 或 Playwright 需要额外安装浏览器吗？**
A: 首次运行时会自动下载 Chrome/Chromium 浏览器。

---

## 📄 License

MIT © 2025