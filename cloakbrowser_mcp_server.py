"""
CloakBrowser MCP Server
将CloakBrowser封装为MCP工具，供AI Agent调用
"""

import asyncio
import base64
import json
from typing import Optional, Dict, Any, List
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# 全局浏览器实例管理
_browser_instance = None
_page_instance = None
_context_instance = None


async def get_async_browser():
    """异步获取或创建浏览器实例"""
    global _browser_instance
    if _browser_instance is None:
        try:
            from cloakbrowser import launch_async
            _browser_instance = await launch_async(headless=True)
        except ImportError:
            raise RuntimeError("请先安装cloakbrowser: pip install cloakbrowser")
    return _browser_instance


async def get_async_page():
    """异步获取或创建页面实例"""
    global _page_instance
    if _page_instance is None:
        browser = await get_async_browser()
        _page_instance = await browser.new_page()
    return _page_instance


# 创建MCP服务器
server = Server("cloakbrowser-mcp")


@server.list_tools()
async def list_tools() -> List[Tool]:
    """列出所有可用的工具"""
    return [
        Tool(
            name="browser_launch",
            description="启动CloakBrowser浏览器实例。可选参数：headless(是否无头模式), proxy(代理地址), humanize(是否启用人类行为模拟)",
            inputSchema={
                "type": "object",
                "properties": {
                    "headless": {
                        "type": "boolean",
                        "description": "是否使用无头模式，默认True",
                        "default": True
                    },
                    "proxy": {
                        "type": "string",
                        "description": "代理地址，格式：http://user:pass@host:port 或 socks5://user:pass@host:port"
                    },
                    "humanize": {
                        "type": "boolean",
                        "description": "是否启用人类行为模拟（鼠标轨迹、键盘延迟等）",
                        "default": False
                    },
                    "geoip": {
                        "type": "boolean",
                        "description": "是否根据代理IP自动检测时区和语言",
                        "default": False
                    }
                }
            }
        ),
        Tool(
            name="browser_close",
            description="关闭浏览器实例并释放资源",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="page_new",
            description="创建新的浏览器页面/标签页",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="page_goto",
            description="导航到指定URL",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "要访问的URL地址"
                    },
                    "wait_until": {
                        "type": "string",
                        "description": "等待条件：load, domcontentloaded, networkidle",
                        "enum": ["load", "domcontentloaded", "networkidle"],
                        "default": "load"
                    },
                    "timeout": {
                        "type": "integer",
                        "description": "超时时间（毫秒），默认30000",
                        "default": 30000
                    }
                },
                "required": ["url"]
            }
        ),
        Tool(
            name="page_screenshot",
            description="截取当前页面的屏幕截图",
            inputSchema={
                "type": "object",
                "properties": {
                    "full_page": {
                        "type": "boolean",
                        "description": "是否截取整个页面，默认False只截取可见区域",
                        "default": False
                    },
                    "selector": {
                        "type": "string",
                        "description": "可选，截取特定元素的CSS选择器"
                    }
                }
            }
        ),
        Tool(
            name="page_click",
            description="点击页面上的元素",
            inputSchema={
                "type": "object",
                "properties": {
                    "selector": {
                        "type": "string",
                        "description": "要点击元素的CSS选择器"
                    },
                    "timeout": {
                        "type": "integer",
                        "description": "等待元素出现的超时时间（毫秒）",
                        "default": 30000
                    }
                },
                "required": ["selector"]
            }
        ),
        Tool(
            name="page_fill",
            description="在输入框中填写文本",
            inputSchema={
                "type": "object",
                "properties": {
                    "selector": {
                        "type": "string",
                        "description": "输入框的CSS选择器"
                    },
                    "text": {
                        "type": "string",
                        "description": "要填写的文本"
                    },
                    "clear_first": {
                        "type": "boolean",
                        "description": "是否先清空输入框，默认True",
                        "default": True
                    }
                },
                "required": ["selector", "text"]
            }
        ),
        Tool(
            name="page_evaluate",
            description="在页面中执行JavaScript代码",
            inputSchema={
                "type": "object",
                "properties": {
                    "script": {
                        "type": "string",
                        "description": "要执行的JavaScript代码"
                    }
                },
                "required": ["script"]
            }
        ),
        Tool(
            name="page_content",
            description="获取当前页面的HTML内容",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="page_text",
            description="获取当前页面的纯文本内容",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="page_title",
            description="获取当前页面的标题",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="page_url",
            description="获取当前页面的URL",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="page_wait_for_selector",
            description="等待指定选择器的元素出现",
            inputSchema={
                "type": "object",
                "properties": {
                    "selector": {
                        "type": "string",
                        "description": "CSS选择器"
                    },
                    "timeout": {
                        "type": "integer",
                        "description": "超时时间（毫秒）",
                        "default": 30000
                    }
                },
                "required": ["selector"]
            }
        ),
        Tool(
            name="page_query_selector",
            description="查询页面上的元素信息",
            inputSchema={
                "type": "object",
                "properties": {
                    "selector": {
                        "type": "string",
                        "description": "CSS选择器"
                    }
                },
                "required": ["selector"]
            }
        ),
        Tool(
            name="page_query_selector_all",
            description="查询页面上所有匹配的元素信息",
            inputSchema={
                "type": "object",
                "properties": {
                    "selector": {
                        "type": "string",
                        "description": "CSS选择器"
                    }
                },
                "required": ["selector"]
            }
        ),
        Tool(
            name="page_press",
            description="在页面上按下键盘按键",
            inputSchema={
                "type": "object",
                "properties": {
                    "key": {
                        "type": "string",
                        "description": "要按下的键，如 Enter, Escape, Tab, ArrowDown 等"
                    }
                },
                "required": ["key"]
            }
        ),
        Tool(
            name="page_scroll",
            description="滚动页面",
            inputSchema={
                "type": "object",
                "properties": {
                    "direction": {
                        "type": "string",
                        "description": "滚动方向",
                        "enum": ["up", "down"],
                        "default": "down"
                    },
                    "amount": {
                        "type": "integer",
                        "description": "滚动像素数",
                        "default": 500
                    }
                }
            }
        ),
        Tool(
            name="page_go_back",
            description="浏览器后退",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="page_go_forward",
            description="浏览器前进",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="page_reload",
            description="刷新当前页面",
            inputSchema={
                "type": "object",
                "properties": {
                    "wait_until": {
                        "type": "string",
                        "description": "等待条件",
                        "enum": ["load", "domcontentloaded", "networkidle"],
                        "default": "load"
                    }
                }
            }
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """执行工具调用"""
    global _browser_instance, _page_instance
    
    try:
        if name == "browser_launch":
            from cloakbrowser import launch_async
            
            headless = arguments.get("headless", True)
            proxy = arguments.get("proxy")
            humanize = arguments.get("humanize", False)
            geoip = arguments.get("geoip", False)
            
            launch_kwargs = {"headless": headless}
            if proxy:
                launch_kwargs["proxy"] = proxy
            if humanize:
                launch_kwargs["humanize"] = True
            if geoip:
                launch_kwargs["geoip"] = True
            
            _browser_instance = await launch_async(**launch_kwargs)
            return [TextContent(type="text", text="✅ 浏览器启动成功")]
        
        elif name == "browser_close":
            if _browser_instance:
                await _browser_instance.close()
                _browser_instance = None
                _page_instance = None
                return [TextContent(type="text", text="✅ 浏览器已关闭")]
            return [TextContent(type="text", text="⚠️ 没有运行中的浏览器实例")]
        
        elif name == "page_new":
            if not _browser_instance:
                await get_async_browser()
            _page_instance = await _browser_instance.new_page()
            return [TextContent(type="text", text="✅ 新页面已创建")]
        
        elif name == "page_goto":
            page = await get_async_page()
            url = arguments["url"]
            wait_until = arguments.get("wait_until", "load")
            timeout = arguments.get("timeout", 30000)
            
            await page.goto(url, wait_until=wait_until, timeout=timeout)
            return [TextContent(type="text", text=f"✅ 已导航到: {url}")]
        
        elif name == "page_screenshot":
            page = await get_async_page()
            full_page = arguments.get("full_page", False)
            selector = arguments.get("selector")
            
            if selector:
                element = await page.query_selector(selector)
                if element:
                    screenshot_bytes = await element.screenshot()
                else:
                    return [TextContent(type="text", text=f"❌ 未找到元素: {selector}")]
            else:
                screenshot_bytes = await page.screenshot(full_page=full_page)
            
            # 转换为base64
            screenshot_base64 = base64.b64encode(screenshot_bytes).decode('utf-8')
            return [TextContent(
                type="text", 
                text=f"✅ 截图成功\n\nbase64图片数据:\n{screenshot_base64[:100]}...\n(完整数据已生成，共{len(screenshot_base64)}字符)"
            )]
        
        elif name == "page_click":
            page = await get_async_page()
            selector = arguments["selector"]
            timeout = arguments.get("timeout", 30000)
            
            await page.click(selector, timeout=timeout)
            return [TextContent(type="text", text=f"✅ 已点击元素: {selector}")]
        
        elif name == "page_fill":
            page = await get_async_page()
            selector = arguments["selector"]
            text = arguments["text"]
            clear_first = arguments.get("clear_first", True)
            
            if clear_first:
                await page.fill(selector, text)
            else:
                await page.type(selector, text)
            return [TextContent(type="text", text=f"✅ 已填写文本到: {selector}")]
        
        elif name == "page_evaluate":
            page = await get_async_page()
            script = arguments["script"]
            result = await page.evaluate(script)
            return [TextContent(type="text", text=f"✅ 执行结果:\n{json.dumps(result, ensure_ascii=False, indent=2) if result else 'null'}")]
        
        elif name == "page_content":
            page = await get_async_page()
            content = await page.content()
            return [TextContent(type="text", text=f"✅ 页面HTML内容:\n{content[:5000]}{'...' if len(content) > 5000 else ''}")]
        
        elif name == "page_text":
            page = await get_async_page()
            text = await page.text_content('body')
            return [TextContent(type="text", text=f"✅ 页面文本内容:\n{text[:5000]}{'...' if len(text) > 5000 else ''}")]
        
        elif name == "page_title":
            page = await get_async_page()
            title = await page.title()
            return [TextContent(type="text", text=f"✅ 页面标题: {title}")]
        
        elif name == "page_url":
            page = await get_async_page()
            url = page.url
            return [TextContent(type="text", text=f"✅ 当前URL: {url}")]
        
        elif name == "page_wait_for_selector":
            page = await get_async_page()
            selector = arguments["selector"]
            timeout = arguments.get("timeout", 30000)
            
            await page.wait_for_selector(selector, timeout=timeout)
            return [TextContent(type="text", text=f"✅ 元素已出现: {selector}")]
        
        elif name == "page_query_selector":
            page = await get_async_page()
            selector = arguments["selector"]
            
            element = await page.query_selector(selector)
            if element:
                text = await element.text_content()
                return [TextContent(type="text", text=f"✅ 找到元素: {selector}\n文本内容: {text}")]
            return [TextContent(type="text", text=f"❌ 未找到元素: {selector}")]
        
        elif name == "page_query_selector_all":
            page = await get_async_page()
            selector = arguments["selector"]
            
            elements = await page.query_selector_all(selector)
            results = []
            for i, el in enumerate(elements[:10]):  # 限制返回前10个
                text = await el.text_content()
                results.append(f"{i+1}. {text[:200] if text else '(空)'}")
            
            return [TextContent(type="text", text=f"✅ 找到 {len(elements)} 个元素:\n" + "\n".join(results))]
        
        elif name == "page_press":
            page = await get_async_page()
            key = arguments["key"]
            await page.keyboard.press(key)
            return [TextContent(type="text", text=f"✅ 已按下键: {key}")]
        
        elif name == "page_scroll":
            page = await get_async_page()
            direction = arguments.get("direction", "down")
            amount = arguments.get("amount", 500)
            
            if direction == "down":
                await page.evaluate(f"window.scrollBy(0, {amount})")
            else:
                await page.evaluate(f"window.scrollBy(0, -{amount})")
            return [TextContent(type="text", text=f"✅ 已向{direction}滚动 {amount} 像素")]
        
        elif name == "page_go_back":
            page = await get_async_page()
            await page.go_back()
            return [TextContent(type="text", text="✅ 已后退")]
        
        elif name == "page_go_forward":
            page = await get_async_page()
            await page.go_forward()
            return [TextContent(type="text", text="✅ 已前进")]
        
        elif name == "page_reload":
            page = await get_async_page()
            wait_until = arguments.get("wait_until", "load")
            await page.reload(wait_until=wait_until)
            return [TextContent(type="text", text="✅ 页面已刷新")]
        
        else:
            return [TextContent(type="text", text=f"❌ 未知工具: {name}")]
    
    except Exception as e:
        return [TextContent(type="text", text=f"❌ 执行失败: {str(e)}")]


async def main():
    """启动MCP服务器"""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
