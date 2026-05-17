#!/bin/bash
# MCP Hub - 一键安装脚本 (macOS/Linux)
# 支持: Claude Desktop / Cursor / VS Code / Windsurf / Trae / Hermes Agent

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="$SCRIPT_DIR/mcp.json"
CLIENT="${1:-all}"
LARK_APP_ID="${2:-}"
LARK_APP_SECRET="${3:-}"
OPENHUMAN_JWT_TOKEN="${4:-}"

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}========================================${NC}"
echo -e "${CYAN}  MCP Hub - AI Agent MCP 一键安装器${NC}"
echo -e "${CYAN}========================================${NC}"
echo ""

# 检查依赖
echo -e "${YELLOW}[1/4] 检查依赖...${NC}"

if command -v node &> /dev/null; then
    echo -e "  ${GREEN}[OK]${NC} Node.js $(node --version)"
else
    echo -e "  ${RED}[WARN]${NC} Node.js 未安装。请从 https://nodejs.org 安装"
fi

if command -v uvx &> /dev/null; then
    echo -e "  ${GREEN}[OK]${NC} uvx 已安装"
else
    echo -e "  ${RED}[WARN]${NC} uvx 未安装。安装命令: pip install uv"
fi

# 读取配置
echo ""
echo -e "${YELLOW}[2/4] 读取 MCP 配置...${NC}"

CONFIG_JSON=$(cat "$CONFIG_FILE")

if [ -n "$LARK_APP_ID" ] && [ -n "$LARK_APP_SECRET" ]; then
    CONFIG_JSON=$(echo "$CONFIG_JSON" | sed "s/\${LARK_APP_ID}/$LARK_APP_ID/g" | sed "s/\${LARK_APP_SECRET}/$LARK_APP_SECRET/g")
    echo -e "  ${GREEN}[OK]${NC} Lark 凭证已配置"
else
    echo -e "  ${YELLOW}[INFO]${NC} Lark 凭证未提供，保留占位符"
fi

if [ -n "$OPENHUMAN_JWT_TOKEN" ]; then
    CONFIG_JSON=$(echo "$CONFIG_JSON" | sed "s/\${OPENHUMAN_JWT_TOKEN}/$OPENHUMAN_JWT_TOKEN/g")
    echo -e "  ${GREEN}[OK]${NC} OpenHuman 凭证已配置"
else
    echo -e "  ${YELLOW}[INFO]${NC} OpenHuman 凭证未提供，保留占位符"
fi

# 安装函数
install_config() {
    local target_path="$1"
    local client_name="$2"

    mkdir -p "$(dirname "$target_path")"
    echo "$CONFIG_JSON" > "$target_path"
    echo -e "  ${GREEN}[OK]${NC} $client_name -> $target_path"
}

# Hermes Agent YAML 安装函数
install_hermes_config() {
    local target_path="$HOME/.hermes/config.yaml"
    local env_path="$HOME/.hermes/.env"
    local client_name="Hermes Agent"

    mkdir -p "$(dirname "$target_path")"

    # 使用 Node.js 将 JSON mcp.json 转换为 YAML mcp_servers 格式
    local mcp_servers_yaml
    mcp_servers_yaml=$(node -e "
const config = JSON.parse(process.argv[1]);
const servers = config.mcpServers || {};

function yamlValue(val, indent) {
    if (val === null || val === undefined) return 'null';
    if (typeof val === 'boolean') return val ? 'true' : 'false';
    if (typeof val === 'number') return String(val);
    if (typeof val === 'string') {
        if (/[:#{}\[\],&*?|>!\"'%\`@\\\\]/.test(val) || val === '' || val === 'true' || val === 'false' || val === 'null' || /^\d/.test(val)) {
            return '\"' + val.replace(/\\\\/g, '\\\\\\\\').replace(/\"/g, '\\\\\"') + '\"';
        }
        return val;
    }
    if (Array.isArray(val)) {
        if (val.length === 0) return '[]';
        const items = val.map(item => {
            const v = yamlValue(item, indent + 2);
            return ' '.repeat(indent + 2) + '- ' + v.trimStart();
        }).join('\n');
        return '\n' + items;
    }
    if (typeof val === 'object') {
        const keys = Object.keys(val);
        if (keys.length === 0) return '{}';
        const entries = keys.map(key => {
            const v = yamlValue(val[key], indent + 2);
            return ' '.repeat(indent + 2) + key + ': ' + v;
        }).join('\n');
        return '\n' + entries;
    }
    return String(val);
}

let output = 'mcp_servers:\n';
for (const [name, server] of Object.entries(servers)) {
    output += '  ' + name + ':\n';
    if (server.command) {
        output += '    command: ' + yamlValue(server.command, 6) + '\n';
    }
    if (server.args && server.args.length > 0) {
        output += '    args:' + yamlValue(server.args, 6) + '\n';
    }
    if (server.env && typeof server.env === 'object' && Object.keys(server.env).length > 0) {
        output += '    env:' + yamlValue(server.env, 6) + '\n';
    }
}
process.stdout.write(output);
" "$CONFIG_JSON")

    # 检查是否已有 config.yaml，如有则合并
    if [ -f "$target_path" ]; then
        echo -e "  ${YELLOW}[INFO]${NC} 检测到已有 Hermes 配置，执行合并..."

        local merged_yaml
        merged_yaml=$(node -e "
const fs = require('fs');
const targetPath = process.argv[1];
const newMcpBlock = process.argv[2];

const existing = fs.readFileSync(targetPath, 'utf-8');

const mcpMarker = /^mcp_servers:\s*$/m;
const lines = existing.split('\n');

let beforeMcp = [];
let afterMcp = [];
let inMcpBlock = false;
let foundMcp = false;

for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    if (mcpMarker.test(line)) {
        foundMcp = true;
        inMcpBlock = true;
        continue;
    }
    if (inMcpBlock) {
        if (line.match(/^  \S/) || line.trim() === '') {
            if (line.trim() === '' && i + 1 < lines.length && !lines[i + 1].match(/^  \S/)) {
                inMcpBlock = false;
                afterMcp.push(line);
            }
            continue;
        } else {
            inMcpBlock = false;
            afterMcp.push(line);
        }
    } else {
        beforeMcp.push(line);
    }
}

let result = '';
if (foundMcp) {
    while (beforeMcp.length > 0 && beforeMcp[beforeMcp.length - 1].trim() === '') {
        beforeMcp.pop();
    }
    result = beforeMcp.join('\n') + '\n\n' + newMcpBlock.trimEnd() + '\n';
    while (afterMcp.length > 0 && afterMcp[0].trim() === '') {
        afterMcp.shift();
    }
    if (afterMcp.length > 0) {
        result += '\n' + afterMcp.join('\n');
    }
} else {
    result = existing.trimEnd() + '\n\n' + newMcpBlock.trimEnd() + '\n';
}

process.stdout.write(result);
" "$target_path" "$mcp_servers_yaml")

        echo "$merged_yaml" > "$target_path"
        echo -e "  ${GREEN}[OK]${NC} $client_name -> $target_path (已合并)"
    else
        echo "$mcp_servers_yaml" > "$target_path"
        echo -e "  ${GREEN}[OK]${NC} $client_name -> $target_path (新建)"
    fi
}

# 安装到各客户端
echo ""
echo -e "${YELLOW}[3/4] 安装到 AI Agent 客户端...${NC}"

if [ "$CLIENT" = "all" ] || [ "$CLIENT" = "claude" ]; then
    if [[ "$OSTYPE" == "darwin"* ]]; then
        install_config "$HOME/Library/Application Support/Claude/claude_desktop_config.json" "Claude Desktop"
    else
        install_config "$HOME/.config/Claude/claude_desktop_config.json" "Claude Desktop"
    fi
fi

if [ "$CLIENT" = "all" ] || [ "$CLIENT" = "cursor" ]; then
    install_config "$HOME/.cursor/mcp.json" "Cursor"
fi

if [ "$CLIENT" = "all" ] || [ "$CLIENT" = "vscode" ]; then
    install_config "$HOME/.config/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json" "VS Code (Cline)"
fi

if [ "$CLIENT" = "all" ] || [ "$CLIENT" = "windsurf" ]; then
    install_config "$HOME/.windsurf/mcp.json" "Windsurf"
fi

if [ "$CLIENT" = "all" ] || [ "$CLIENT" = "trae" ]; then
    if [[ "$OSTYPE" == "darwin"* ]]; then
        install_config "$HOME/Library/Application Support/Trae CN/User/mcp.json" "Trae IDE"
    else
        install_config "$HOME/.config/Trae CN/User/mcp.json" "Trae IDE"
    fi
fi

if [ "$CLIENT" = "all" ] || [ "$CLIENT" = "hermes" ]; then
    install_hermes_config
fi

# 完成
echo ""
echo -e "${GREEN}[4/4] 安装完成!${NC}"
echo ""
echo -e "${CYAN}已安装的 MCP 服务器:${NC}"
echo "  1. Filesystem          - 文件系统操作"
echo "  2. Desktop Commander   - 桌面终端控制"
echo "  3. Sequential Thinking - 链式思考推理"
echo "  4. Memory              - 持久化记忆"
echo "  5. context7            - 上下文增强"
echo "  6. Puppeteer           - 浏览器自动化"
echo "  7. DuckDuckGo Search   - 网络搜索"
echo "  8. lark-mcp            - 飞书集成"
echo "  9. Excel               - Excel 文件处理"
echo "  10. Chrome DevTools    - Chrome 开发者工具"
echo "  11. 发现报告            - 发现报告"
echo "  12. Playwright         - 浏览器自动化测试"
echo "  13. OpenHuman           - 个人AI记忆与集成"
echo ""
echo -e "${GREEN}重启你的 AI Agent 客户端即可使用!${NC}"
