import asyncio
import httpx
import json
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
from pydantic import AnyUrl
import mcp.server.stdio
import logging

# Store notes as a simple key-value dict to demonstrate state management
notes: dict[str, str] = {}

# Configure logging
logging.basicConfig(level=logging.INFO)
#logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("ABiCMCPServer")
server = Server("ABiCMCPServer")

#呼び出すREST APIのエンドポイント(WSGI利用)
API_BASE_URL = "https://localhost:7443/info"

#OpenAI利用時(/mdx)
async def create_dashboard(user_input: str) -> str:
    headers={
        "Content-Type":"application/json;charset=utf-8"
    }
    # 送信するJSONボディを組み立て
    body = {
        "UserInput": user_input,
    }
    async with httpx.AsyncClient(timeout=80.0,verify=False) as client:
        response = await client.post(
            f"{API_BASE_URL}/mdx",
            headers=headers,
            json=body
        )
        response.raise_for_status()
        data = response.json()
        return data

@server.list_resources()
async def handle_list_resources() -> list[types.Resource]:
    """
    List available note resources.
    Each note is exposed as a resource with a custom note:// URI scheme.
    """
    return [
        types.Resource(
            uri=AnyUrl("ABiCMCPServer://dashboard"),
            name="IRIS BIの分析用キューブを使った分析用ダッシュボード作成ツール",
            description="分析したい内容を自然言語で入力すると生成AIを介して分析用ダッシュボードを作成します",
            mimeType="application/json",
        )
    ]

@server.read_resource()
async def handle_read_resource(uri: AnyUrl) -> str:
    """
    Read a specific note's content by its URI.
    The note name is extracted from the URI host component.
    """
    if str(uri).startswith("ABiCMCPServer://dashboard"):
        try:
            iris_data = await create_dashboard()
            #return iris_data
            return json.dumps(iris_data, ensure_ascii=False,indent=2)
        except httpx.HTTPError as e:
            raise RuntimeError(f"IRIS API error: {str(e)}")

    else:
        raise ValueError(f"Unknown resource: {uri}")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """
    List available tools.
    Each tool specifies its arguments using JSON Schema validation.
    """
    return [
        types.Tool(
            name="dashboard",
            description="IRIS BIの分析用キューブを使った分析用ダッシュボード作成ツール",
            inputSchema={
                "type": "object",
                "properties": {
                    "UserInput": {
                        "type": "string",
                        "description": "ダッシュボードで分析したい内容を自然言語で入力します。例）2024年4月の障害レベル別、継続度別、インシデントレポート件数を教えて"
                    }
                },
                "required": ["UserInput"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """
    Handle tool execution requests.
    Tools can modify server state and notify clients of changes.
    """
    if name == "dashboard":
    
        if not isinstance(arguments, dict):
            raise ValueError("Invalid forecast arguments")
        
        userinput=arguments["UserInput"]
        try:
            answer= await create_dashboard(userinput)
            return [
                types.TextContent(
                    type="text",
                    text=json.dumps(answer,ensure_ascii=False, indent=2)
                    #text=f"🎉 IRIS接続成功！\n📥 応答:：{msg}"
                )
            ]
        
        except Exception as e:
            error_details = {
                "error_type": type(e).__name__,
                "error_message": str(e),
            }
            return [
                types.TextContent(
                    type="text",
                    text=f"エラーが発生しました(ダッシュボード作成): {json.dumps(error_details, ensure_ascii=False, indent=2)}"
                )
            ]
        except httpx.HTTPError as e:
            logger.error(f"IRIS API error: {str(e)}")
            return [
                types.TextContent(
                    type="text",
                    text=f"エラーが発生しました(ダッシュボード作成): {str(e)}"
                )
            ]


async def main():
    # Run the server using stdin/stdout streams
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="ABiCMCPServer",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )