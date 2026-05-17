#!/usr/bin/env python3
"""
MCP Hub 一键安装脚本
自动安装和配置多个MCP服务器

使用方法:
    python install.py                    # 安装所有MCP
    python install.py cloakbrowser       # 安装指定MCP
    python install.py --list             # 列出可用MCP
    python install.py --client all       # 安装到所有客户端（默认）
    python install.py --client claude    # 指定客户端配置
    python install.py --client hermes    # 安装到Hermes Agent（YAML格式）

"""

import argparse
import json
import os
import platform
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional

# 尝试导入 PyYAML，用于 Hermes Agent 的 YAML 配置
try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


# MCP Hub 配置目录
HUB_DIR = Path(__file__).parent
CONFIGS_DIR = HUB_DIR / "configs"

# 支持的客户端配置路径
# 注意: hermes 使用 YAML 格式，与其他 JSON 格式客户端不同，需要特殊处理
CLIENT_CONFIGS = {
    "claude": {
        "darwin": Path.home() / "Library/Application Support/Claude/claude_desktop_config.json",
        "win32": Path(os.environ.get("APPDATA", "")) / "Claude/claude_desktop_config.json",
        "linux": Path.home() / ".config/Claude/claude_desktop_config.json",
    },
    "cursor": {
        "darwin": Path.home() / ".cursor/mcp.json",
        "win32": Path(os.environ.get("APPDATA", "")) / "Cursor/mcp.json",
        "linux": Path.home() / ".cursor/mcp.json",
    },
    "windsurf": {
        "darwin": Path.home() / ".windsurf/mcp.json",
        "win32": Path(os.environ.get("APPDATA", "")) / "Windsurf/mcp.json",
        "linux": Path.home() / ".windsurf/mcp.json",
    },
    "trae": {
        "darwin": Path.home() / "Library/Application Support/Trae CN/User/mcp.json",
        "win32": Path(os.environ.get("APPDATA", "")) / "Trae CN/User/mcp.json",
        "linux": Path.home() / ".config/Trae CN/User/mcp.json",
    },
    "vscode": {
        "darwin": Path.home() / "Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json",
        "win32": Path(os.environ.get("APPDATA", "")) / "Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json",
        "linux": Path.home() / ".config/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json",
    },
    "hermes": {
        "darwin": Path.home() / ".hermes/config.yaml",
        "win32": Path.home() / ".hermes/config.yaml",
        "linux": Path.home() / ".hermes/config.yaml",
    },
}


def get_system() -> str:
    """获取当前系统平台"""
    system = platform.system().lower()
    if system == "darwin":
        return "darwin"
    elif system == "windows" or sys.platform == "win32":
        return "win32"
    else:
        return "linux"


def load_mcp_config(name: str) -> Optional[Dict]:
    """加载MCP配置文件"""
    config_file = CONFIGS_DIR / f"{name}.json"
    if not config_file.exists():
        return None

    with open(config_file, "r", encoding="utf-8") as f:
        return json.load(f)


def list_available_mcps() -> List[str]:
    """列出所有可用的MCP"""
    configs = []
    if CONFIGS_DIR.exists():
        for config_file in CONFIGS_DIR.glob("*.json"):
            configs.append(config_file.stem)
    return sorted(configs)


def install_mcp_package(config: Dict) -> bool:
    """安装MCP包"""
    install_config = config.get("install", {})
    install_type = install_config.get("type", "")
    package = install_config.get("package", "")
    version = install_config.get("version", "")

    if not package:
        print(f"  ⚠️  {config['name']}: 未配置安装包")
        return False

    try:
        if install_type == "pip":
            cmd = [sys.executable, "-m", "pip", "install", package]
            if version:
                cmd[-1] = f"{package}{version}"
            print(f"  📦 pip install {cmd[-1]}...")
            subprocess.run(cmd, check=True, capture_output=True)
            return True

        elif install_type == "npx":
            print(f"  📦 npx安装 {package}...")
            return True

        else:
            print(f"  ⚠️  {config['name']}: 未知的安装类型 {install_type}")
            return False

    except subprocess.CalledProcessError as e:
        print(f"  ❌ {config['name']}: 安装失败 - {e}")
        return False


def generate_mcp_server_config(config: Dict, custom_args: Dict = None) -> Dict:
    """生成MCP服务器配置"""
    server_config = config.get("server", {}).copy()

    args = server_config.get("args", [])
    processed_args = []
    for arg in args:
        if isinstance(arg, str) and "{{" in arg and "}}" in arg:
            var_name = arg.strip("{} ")
            if custom_args and var_name in custom_args:
                processed_args.append(custom_args[var_name])
            else:
                continue
        else:
            processed_args.append(arg)

    server_config["args"] = processed_args
    return server_config


def get_client_config_path(client: str) -> Optional[Path]:
    """获取客户端配置文件路径"""
    system = get_system()
    if client not in CLIENT_CONFIGS:
        return None

    config_paths = CLIENT_CONFIGS[client]
    if system not in config_paths:
        print(f"  ⚠️  不支持的操作系统: {system}")
        return None

    return config_paths[system]


def load_client_config(client: str) -> Dict:
    """加载客户端现有配置"""
    config_path = get_client_config_path(client)
    if not config_path:
        return {}

    if config_path.exists():
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}


def save_client_config(client: str, config: Dict) -> bool:
    """保存客户端配置"""
    config_path = get_client_config_path(client)
    if not config_path:
        return False

    config_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        return True
    except IOError as e:
        print(f"  ❌ 保存配置失败: {e}")
        return False


# ==================== Hermes Agent YAML 配置处理 ====================


def load_hermes_config() -> Dict:
    """读取 Hermes Agent 的 YAML 配置文件

    Returns:
        解析后的配置字典，如果文件不存在或读取失败则返回空字典
    """
    if not HAS_YAML:
        return {}

    config_path = get_client_config_path("hermes")
    if not config_path:
        return {}

    if config_path.exists():
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        except (yaml.YAMLError, IOError):
            print(f"  ⚠️  读取 Hermes 配置文件失败: {config_path}")
            return {}
    return {}


def save_hermes_config(config: Dict) -> bool:
    """保存 Hermes Agent 的 YAML 配置文件

    将配置字典写入 ~/.hermes/config.yaml，保留文件中已有的所有其他设置。

    Args:
        config: 完整的配置字典（包含 mcp_servers 及其他所有设置）

    Returns:
        保存是否成功
    """
    if not HAS_YAML:
        return False

    config_path = get_client_config_path("hermes")
    if not config_path:
        return False

    config_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with open(config_path, "w", encoding="utf-8") as f:
            yaml.dump(config, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        return True
    except IOError as e:
        print(f"  ❌ 保存 Hermes 配置失败: {e}")
        return False


def install_mcp_to_hermes(name: str, server_config: Dict) -> bool:
    """将单个 MCP 服务器配置合并到 Hermes Agent 的 config.yaml 中

    Hermes 使用 YAML 格式，MCP 服务器配置在 mcp_servers 键下。
    此函数会：
    1. 读取现有的 config.yaml（如果存在）
    2. 将新的 MCP 服务器配置合并到 mcp_servers 中
    3. 保留所有其他现有设置（model、terminal、TTS 等）
    4. 如果文件不存在则创建

    Args:
        name: MCP 服务器名称（用作 mcp_servers 下的键）
        server_config: MCP 服务器配置字典，包含 command、args、env 等字段

    Returns:
        安装是否成功
    """
    if not HAS_YAML:
        print(f"  ⚠️  跳过 Hermes Agent: 未安装 PyYAML")
        print(f"     请运行: pip install pyyaml")
        return False

    # 读取现有配置（保留所有非 MCP 设置）
    hermes_config = load_hermes_config()

    # 确保 mcp_servers 键存在
    if "mcp_servers" not in hermes_config:
        hermes_config["mcp_servers"] = {}

    # 转换 JSON 格式的 server_config 为 Hermes YAML 格式
    hermes_server = {}
    if "command" in server_config:
        hermes_server["command"] = server_config["command"]
    if "args" in server_config:
        hermes_server["args"] = server_config["args"]
    if "env" in server_config:
        hermes_server["env"] = server_config["env"]

    # 合并到配置中（同名服务器会被覆盖）
    hermes_config["mcp_servers"][name] = hermes_server

    # 保存完整配置
    if save_hermes_config(hermes_config):
        print(f"  ✅ {name} -> hermes")
        return True
    else:
        print(f"  ❌ {name} -> hermes 失败")
        return False


# ==================== 通用安装逻辑 ====================


def install_mcp(name: str, client: str = "all", custom_args: Dict = None) -> bool:
    """安装单个MCP"""
    print(f"\n🔧 安装 MCP: {name}")

    config = load_mcp_config(name)
    if not config:
        print(f"  ❌ 未找到MCP配置: {name}")
        return False

    display_name = config.get("displayName", name)
    print(f"  📋 {display_name}: {config.get('description', '')}")

    if not install_mcp_package(config):
        return False

    server_config = generate_mcp_server_config(config, custom_args)

    if client == "all":
        clients_to_install = list(CLIENT_CONFIGS.keys())
    else:
        clients_to_install = [client]

    success = False
    for target_client in clients_to_install:
        # Hermes 使用特殊的 YAML 合并逻辑
        if target_client == "hermes":
            if install_mcp_to_hermes(name, server_config):
                success = True
            continue

        # 其他客户端使用标准 JSON 逻辑
        client_config = load_client_config(target_client)

        if "mcpServers" not in client_config:
            client_config["mcpServers"] = {}
        client_config["mcpServers"][name] = server_config

        if save_client_config(target_client, client_config):
            print(f"  ✅ {display_name} -> {target_client}")
            success = True
        else:
            print(f"  ❌ {display_name} -> {target_client} 失败")

    return success


def install_all(client: str = "all") -> None:
    """安装所有可用的MCP"""
    available = list_available_mcps()
    if not available:
        print("❌ 没有找到可用的MCP配置")
        return

    if client == "all":
        print(f"\n🚀 开始安装 {len(available)} 个MCP 到所有客户端")
    else:
        print(f"\n🚀 开始安装 {len(available)} 个MCP 到 {client}")
    print(f"   可用MCP: {', '.join(available)}")

    # 如果目标包含 hermes 且没有 PyYAML，提前警告
    if (client == "all" or client == "hermes") and not HAS_YAML:
        print(f"\n  ⚠️  Hermes Agent 需要 PyYAML 支持")
        print(f"     请先运行: pip install pyyaml")
        print(f"     Hermes 配置将被跳过\n")

    success_count = 0
    for mcp_name in available:
        if install_mcp(mcp_name, client):
            success_count += 1

    print(f"\n✨ 安装完成: {success_count}/{len(available)} 个MCP安装成功")

    if success_count > 0:
        print(f"\n💡 请重启 AI Agent 客户端以加载新的MCP配置")


def show_mcp_info(name: str) -> None:
    """显示MCP详细信息"""
    config = load_mcp_config(name)
    if not config:
        print(f"❌ 未找到MCP: {name}")
        return

    print(f"\n📋 MCP: {config.get('displayName', name)}")
    print(f"   名称: {name}")
    print(f"   描述: {config.get('description', 'N/A')}")
    print(f"   版本: {config.get('version', 'N/A')}")
    print(f"   作者: {config.get('author', 'N/A')}")
    print(f"   主页: {config.get('homepage', 'N/A')}")

    print(f"\n   工具列表:")
    for tool in config.get('tools', []):
        print(f"     - {tool['name']}: {tool['description']}")

    env = config.get('env', {})
    if env:
        print(f"\n   环境变量要求:")
        for var_name, var_config in env.items():
            required = "必需" if var_config.get('required') else "可选"
            print(f"     - {var_name}: {var_config.get('description', '')} ({required})")

    configurable = config.get('configurable', {})
    if configurable:
        print(f"\n   可配置项:")
        for key, conf in configurable.items():
            default = conf.get('default', '无')
            print(f"     - {key}: {conf.get('description', '')} (默认: {default})")


def main():
    parser = argparse.ArgumentParser(
        description="MCP Hub - 一键安装和管理MCP服务器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python install.py                    # 安装所有MCP到所有客户端
  python install.py cloakbrowser       # 安装CloakBrowser
  python install.py --list             # 列出所有可用MCP
  python install.py --info cloakbrowser # 查看MCP详情
  python install.py --client cursor    # 仅安装到Cursor
  python install.py --client hermes    # 仅安装到Hermes Agent
  python install.py --client all       # 安装到所有客户端（默认）
        """
    )

    parser.add_argument(
        "mcp",
        nargs="?",
        help="要安装的MCP名称（不指定则安装全部）"
    )

    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="列出所有可用的MCP"
    )

    parser.add_argument(
        "--info", "-i",
        metavar="NAME",
        help="显示指定MCP的详细信息"
    )

    parser.add_argument(
        "--client", "-c",
        default="all",
        choices=["all", "claude", "cursor", "windsurf", "trae", "vscode", "hermes"],
        help="目标客户端（默认: all）"
    )

    args = parser.parse_args()

    if args.list:
        available = list_available_mcps()
        print("\n📦 可用的MCP:")
        for name in available:
            config = load_mcp_config(name)
            display_name = config.get("displayName", name) if config else name
            desc = config.get("description", "") if config else ''
            print(f"  - {name}: {display_name}")
            if desc:
                print(f"    {desc}")
        return

    if args.info:
        show_mcp_info(args.info)
        return

    if args.mcp:
        install_mcp(args.mcp, args.client)
    else:
        install_all(args.client)


if __name__ == "__main__":
    main()
