#!/usr/bin/env python3
import asyncio
from typing import Any, Dict, List
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from llmada.core import BianXieAdapter
# 创建服务器
app = Server("api_documents_experts_mcp_server")

@app.list_tools()
async def list_tools() -> List[Tool]:
    """返回可用工具列表"""
    return [
        Tool(
            name="full_function_use_packages",
            description="主要用来填充mock类函数修改为真正函数, 内涵大量自定义的三方包, 拥有强大能力的python专家",
            inputSchema={
                "type": "object",
                "properties": {
                    "prompt": {"type": "string", "description": "对于函数的实现需求"},
                    "code": {"type": "string", "description": "当前的fack函数"}
                },
                "required": ["prompt", "code"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """处理工具调用"""
    
    if name == "full_function_use_packages":
        prompt = arguments.get("prompt", '')
        code = arguments.get("code", '')

        bx = BianXieAdapter(api_key = "12341234",api_base = "http://127.0.0.1:8108/v1/chat/completions")

        bx.model_pool.append('ReactAgent_API_Expert')
        bx.set_model('ReactAgent_API_Expert')
        result = ''
        for i in bx.product_stream(prompt + code):
            print(i)
            result += i
        return [TextContent(
            type="text",
            text= result
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