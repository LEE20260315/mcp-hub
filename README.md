# MCP Hub

一个MCP（Model Context Protocol）服务器集合，支持一键安装到各种AI Agent客户端。

## 功能特性

- 📦 **统一管理** - 集中管理多个MCP服务器配置
- 🚀 **一键安装** - 一条命令安装所有或指定MCP
- 🛠️ **多客户端支持** - 支持Claude Desktop、Cursor、Windsurf等
- 📋 **自动配置** - 自动写入客户端配置文件
- 🔍 **信息查看** - 查看MCP详细信息和可用工具

## 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/yourusername/mcp-hub.git
cd mcp-hub
```

### 2. 一键安装所有MCP

```bash
python install.py
```

### 3. 重启你的AI Agent客户端

安装完成后，重启Claude Desktop/Cursor/Windsurf即可使用。

---

## 可用MCP列表

| MCP | 描述 | 安装类型 |
|-----|------|---------|
| [cloakbrowser](./configs/cloakbrowser.json) | 隐形浏览器自动化，绕过机器人检测 | pip |
| [filesystem](./configs/filesystem.json) | 安全的文件系统操作 | npx |
| [github](./configs/github.json) | GitHub API操作 | npx |
| [fetch](./configs/fetch.json) | 网页内容获取 | npx |

---

## 安装脚本使用指南

### 查看所有可用MCP

```bash
python install.py --list
```

### 安装指定MCP

```bash
python install.py cloakbrowser
```

### 安装到指定客户端

```bash
# 安装到Cursor
python install.py --client cursor

# 安装到Windsurf
python install.py --client windsurf
```

### 查看MCP详细信息

```bash
python install.py --info cloakbrowser
```

---

## 支持的客户端

| 客户端 | 配置路径 | 状态 |
|--------|---------|------|
| Claude Desktop | `~/Library/Application Support/Claude/claude_desktop_config.json` | ✅ 支持 |
| Cursor | `~/.cursor/mcp.json` | ✅ 支持 |
| Windsurf | `~/.windsurf/mcp.json` | ✅ 支持 |

---

## 添加新的MCP

1. 在 `configs/` 目录下创建新的JSON配置文件
2. 参考现有配置格式，填写MCP信息
3. 重新运行 `python install.py` 即可安装

### 配置文件格式示例

```json
{
  "name": "your-mcp",
  "displayName": "Your MCP",
  "description": "描述你的MCP功能",
  "version": "1.0.0",
  "author": "Your Name",
  "homepage": "https://github.com/yourname/your-mcp",
  "license": "MIT",
  "install": {
    "type": "pip",
    "package": "your-mcp-package",
    "version": ">=1.0.0"
  },
  "server": {
    "type": "stdio",
    "command": "python",
    "args": ["-m", "your_mcp"]
  },
  "tools": [
    {
      "name": "tool_name",
      "description": "工具描述"
    }
  ],
  "env": {},
  "configurable": {}
}
```

---

## 目录结构

```
mcp-hub/
├── configs/                    # MCP配置文件目录
│   ├── cloakbrowser.json      # CloakBrowser配置
│   ├── filesystem.json        # 文件系统配置
│   ├── github.json            # GitHub配置
│   └── fetch.json             # 网页获取配置
├── install.py                 # 一键安装脚本
└── README.md                  # 本文件
```

---

## 工作原理

1. **配置读取** - 从 `configs/` 目录读取所有MCP配置
2. **包安装** - 根据配置自动安装pip包或准备npx命令
3. **配置生成** - 生成客户端需要的MCP服务器配置
4. **配置写入** - 自动写入到客户端的配置文件

---

## 注意事项

1. **环境要求**
   - Python 3.9+
   - Node.js 16+（用于npx安装的MCP）

2. **权限问题**
   - 脚本需要写入客户端配置目录的权限
   - 首次运行可能需要管理员权限

3. **配置备份**
   - 脚本会自动合并现有配置，不会覆盖
   - 建议定期备份客户端配置文件

---

## 许可证

MIT License

---

## 贡献

欢迎提交Issue和PR，添加更多MCP配置！
