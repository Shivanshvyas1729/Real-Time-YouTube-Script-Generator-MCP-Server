from asyncio import transports

from app import get_realtime_info,generate_video_script
from mcp.server.fastmcp import FastMCP
mcp = FastMCP("This is for video script genrator")
@mcp.tool()
def get_latest_info_mcp(query:str):
    return get_realtime_info(query)


@mcp.tool()
def get_video_script_mcp(query:str):
    info = get_realtime_info(query)
    return generate_video_script(info)


if __name__ =="__main__":
    mcp.run(transport ="stdio")