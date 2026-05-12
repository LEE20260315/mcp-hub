#!/bin/bash
# MCP Hub - 一键安装脚本 (macOS/Linux)
# 支持: Claude Desktop / Cursor / VS Code / Windsurf

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="$SCRIPT_DIR/mcp.json"
CLIENT="${1:-all}"
LARK_APP_ID="${2:-}"
LARK_APP_SECRET="${3:-}"

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

# 安装函数
install_config() {
    local target_path="$1"
    local client_name="$2"
    
    mkdir -p "$(dirname "$target_path")"
    echo "$CONFIG_JSON" > "$target_path"
    echo -e "  ${GREEN}[OK]${NC} $client_name -> $target_path"
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
echo ""
echo -e "${GREEN}重启你的 AI Agent 客户端即可使用!${NC}"