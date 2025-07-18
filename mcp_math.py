#!/usr/bin/env python3

import asyncio
from typing import Any, Dict, List
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# 创建服务器
app = Server("math-mcp-server")

@app.list_tools()
async def list_tools() -> List[Tool]:
    """返回可用工具列表"""
    return [
        Tool(
            name="add",
            description="两数相加",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "第一个数"},
                    "b": {"type": "number", "description": "第二个数"}
                },
                "required": ["a", "b"]
            }
        ),
        Tool(
            name="subtract",
            description="两数相减",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "被减数"},
                    "b": {"type": "number", "description": "减数"}
                },
                "required": ["a", "b"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """处理工具调用"""
    
    if name == "add":
        a = arguments.get("a", 0)
        b = arguments.get("b", 0)
        result = a + b
        return [TextContent(
            type="text",
            text=f"{a} + {b} = {result}"
        )]
    
    elif name == "subtract":
        a = arguments.get("a", 0)
        b = arguments.get("b", 0)
        result = a - b
        return [TextContent(
            type="text",
            text=f"{a} - {b} = {result}"
        )]
    
    else:
        return [TextContent(
            type="text",
            text=f"未知工具: {name}"
        )]

async def main():
    """启动服务器"""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())