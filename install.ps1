# MCP Hub - 一键安装脚本 (Windows PowerShell)
# 支持: Trae / Claude Desktop / Cursor / VS Code / Windsurf / Hermes Agent

param(
    [string]$Client = "all",
    [string]$LarkAppId = "",
    [string]$LarkAppSecret = "",
    [string]$OpenHumanJwtToken = ""
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ConfigFile = Join-Path $ScriptDir "mcp.json"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  MCP Hub - AI Agent MCP 一键安装器" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 检查依赖
Write-Host "[1/4] 检查依赖..." -ForegroundColor Yellow

$nodeInstalled = $null -ne (Get-Command node -ErrorAction SilentlyContinue)
$uvInstalled = $null -ne (Get-Command uvx -ErrorAction SilentlyContinue)

if (-not $nodeInstalled) {
    Write-Host "  [WARN] Node.js 未安装。部分 MCP 服务器需要 Node.js。" -ForegroundColor Red
    Write-Host "  请从 https://nodejs.org 安装 Node.js (推荐 LTS 版本)" -ForegroundColor Yellow
}
else {
    Write-Host "  [OK] Node.js $(node --version)" -ForegroundColor Green
}

if (-not $uvInstalled) {
    Write-Host "  [WARN] uvx 未安装。DuckDuckGo 和 发现报告 需要 uvx。" -ForegroundColor Red
    Write-Host "  安装命令: pip install uv" -ForegroundColor Yellow
}
else {
    Write-Host "  [OK] uvx 已安装" -ForegroundColor Green
}

# 读取配置文件
Write-Host ""
Write-Host "[2/4] 读取 MCP 配置..." -ForegroundColor Yellow
$config = Get-Content $ConfigFile -Raw | ConvertFrom-Json

# 替换 lark 环境变量
if ($LarkAppId -and $LarkAppSecret) {
    $config.mcpServers.'lark-mcp'.env.APP_ID = $LarkAppId
    $config.mcpServers.'lark-mcp'.env.APP_SECRET = $LarkAppSecret
    Write-Host "  [OK] Lark 凭证已配置" -ForegroundColor Green
}
else {
    Write-Host "  [INFO] Lark 凭证未提供，将保留占位符。可通过 -LarkAppId 和 -LarkAppSecret 参数配置" -ForegroundColor Yellow
}

# 替换 OpenHuman 环境变量
if ($OpenHumanJwtToken) {
    $config.mcpServers.'OpenHuman'.env.OPENHUMAN_JWT_TOKEN = $OpenHumanJwtToken
    Write-Host "  [OK] OpenHuman 凭证已配置" -ForegroundColor Green
}
else {
    Write-Host "  [INFO] OpenHuman 凭证未提供，将保留占位符。可通过 -OpenHumanJwtToken 参数配置" -ForegroundColor Yellow
}

$configJson = $config | ConvertTo-Json -Depth 10

# 安装到各客户端
Write-Host ""
Write-Host "[3/4] 安装到 AI Agent 客户端..." -ForegroundColor Yellow

function Install-McpConfig {
    param([string]$TargetPath, [string]$ClientName)

    $TargetDir = Split-Path -Parent $TargetPath
    if (-not (Test-Path $TargetDir)) {
        New-Item -ItemType Directory -Path $TargetDir -Force | Out-Null
    }

    $configJson | Set-Content -Path $TargetPath -Force
    Write-Host "  [OK] $ClientName -> $TargetPath" -ForegroundColor Green
}

function Install-HermesConfig {
    param([string]$TargetPath, [string]$ClientName)

    $TargetDir = Split-Path -Parent $TargetPath
    if (-not (Test-Path $TargetDir)) {
        New-Item -ItemType Directory -Path $TargetDir -Force | Out-Null
    }

    $tempJsonFile = [System.IO.Path]::GetTempFileName()
    try {
        $configJson | Set-Content -Path $tempJsonFile -Encoding UTF8 -Force

        $nodeScript = @'
const fs = require('fs');

const jsonFilePath = process.argv[2];
const targetPath = process.argv[3];

const configJson = fs.readFileSync(jsonFilePath, 'utf8');
const config = JSON.parse(configJson);
const mcpServers = config.mcpServers || {};

function buildYamlFromMcpServers(servers) {
    let lines = ['mcp_servers:'];
    const serverNames = Object.keys(servers);
    for (const name of serverNames) {
        const server = servers[name];
        lines.push('  ' + name + ':');
        if (server.command) {
            lines.push('    command: "' + server.command + '"');
        }
        if (server.args && server.args.length > 0) {
            const argsStr = server.args.map(a => '"' + a + '"').join(', ');
            lines.push('    args: [' + argsStr + ']');
        }
        if (server.env && Object.keys(server.env).length > 0) {
            lines.push('    env:');
            for (const [key, value] of Object.entries(server.env)) {
                lines.push('      ' + key + ': "' + value + '"');
            }
        }
    }
    return lines.join('\n');
}

let existingContent = '';
if (fs.existsSync(targetPath)) {
    existingContent = fs.readFileSync(targetPath, 'utf8');
}

let result = '';

if (existingContent.trim()) {
    const existingLines = existingContent.split('\n');
    let inMcpServers = false;
    let mcpServersIndent = -1;
    const preservedLines = [];

    for (let i = 0; i < existingLines.length; i++) {
        const line = existingLines[i];
        const trimmed = line.trimStart();
        const indent = line.length - trimmed.length;

        if (!inMcpServers && (trimmed === 'mcp_servers:' || trimmed.startsWith('mcp_servers:'))) {
            inMcpServers = true;
            mcpServersIndent = indent;
            continue;
        }

        if (inMcpServers) {
            if (trimmed === '' || indent <= mcpServersIndent) {
                inMcpServers = false;
                if (trimmed !== '') {
                    preservedLines.push(line);
                }
            }
            continue;
        }

        preservedLines.push(line);
    }

    const newMcpServersYaml = buildYamlFromMcpServers(mcpServers);
    const preserved = preservedLines.join('\n').trimEnd();

    if (preserved) {
        result = preserved + '\n\n' + newMcpServersYaml + '\n';
    } else {
        result = newMcpServersYaml + '\n';
    }
} else {
    result = buildYamlFromMcpServers(mcpServers) + '\n';
}

fs.writeFileSync(targetPath, result, 'utf8');
'@

        $result = node -e $nodeScript -- $tempJsonFile $TargetPath 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  [OK] $ClientName -> $TargetPath" -ForegroundColor Green
        }
        else {
            Write-Host "  [ERROR] $ClientName 安装失败: $result" -ForegroundColor Red
        }
    }
    finally {
        if (Test-Path $tempJsonFile) {
            Remove-Item -Path $tempJsonFile -Force | Out-Null
        }
    }
}

$installAll = $Client -eq "all"

if ($installAll -or $Client -eq "trae") {
    Install-McpConfig -TargetPath "$env:APPDATA\Trae CN\User\mcp.json" -ClientName "Trae IDE"
}

if ($installAll -or $Client -eq "claude") {
    Install-McpConfig -TargetPath "$env:APPDATA\Claude\claude_desktop_config.json" -ClientName "Claude Desktop"
}

if ($installAll -or $Client -eq "cursor") {
    Install-McpConfig -TargetPath "$env:USERPROFILE\.cursor\mcp.json" -ClientName "Cursor"
}

if ($installAll -or $Client -eq "vscode") {
    Install-McpConfig -TargetPath "$env:APPDATA\Code\User\globalStorage\saoudrizwan.claude-dev\settings\cline_mcp_settings.json" -ClientName "VS Code (Cline)"
}

if ($installAll -or $Client -eq "windsurf") {
    Install-McpConfig -TargetPath "$env:USERPROFILE\.windsurf\mcp.json" -ClientName "Windsurf"
}

if ($installAll -or $Client -eq "hermes") {
    Install-HermesConfig -TargetPath "$env:USERPROFILE\.hermes\config.yaml" -ClientName "Hermes Agent"
}

# 完成
Write-Host ""
Write-Host "[4/4] 安装完成!" -ForegroundColor Green
Write-Host ""
Write-Host "已安装的 MCP 服务器列表:" -ForegroundColor Cyan
Write-Host "  1. Filesystem          - 文件系统操作"
Write-Host "  2. Desktop Commander   - 桌面终端控制"
Write-Host "  3. Sequential Thinking - 链式思考推理"
Write-Host "  4. Memory              - 持久化记忆"
Write-Host "  5. context7            - 上下文增强"
Write-Host "  6. Puppeteer           - 浏览器自动化"
Write-Host "  7. DuckDuckGo Search   - 网络搜索"
Write-Host "  8. lark-mcp            - 飞书集成"
Write-Host "  9. Excel               - Excel 文件处理"
Write-Host "  10. Chrome DevTools    - Chrome 开发者工具"
Write-Host "  11. 发现报告            - 发现报告"
Write-Host "  12. Playwright         - 浏览器自动化测试"
Write-Host "  13. OpenHuman           - 个人AI记忆与集成"
Write-Host ""
Write-Host "重启你的 AI Agent 客户端即可使用!" -ForegroundColor Green
