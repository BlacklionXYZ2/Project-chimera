# mcp_bridge.py
import asyncio
from autogen import register_function

# Use the official MCP Python SDK directly
from mcp import StdioServerParameters, ClientSession
from mcp.client.stdio import stdio_client

def register_tool_for_agents(f, caller, executor, name, description):
    """Registers a function tool across one or multiple caller agents."""
    agents = caller if isinstance(caller, list) else [caller]
    for agent in agents:
        register_function(
            f,
            caller=agent,
            executor=executor,
            name=name,
            description=description,
        )

def setup_local_workspace_tools(onyx, sora, atlas, user_proxy):
    """Binds workspace I/O tools with strict caller separation."""
    from tools import write_workspace_file, read_workspace_file, run_python_script
    
    register_tool_for_agents(
        read_workspace_file,
        caller=[onyx, sora, atlas],
        executor=user_proxy,
        name="read_workspace_file",
        description="Reads a file from the local workspace directory.",
    )
    register_tool_for_agents(
        write_workspace_file,
        caller=[sora, atlas],
        executor=user_proxy,
        name="write_workspace_file",
        description="Saves code/config text directly to the local workspace.",
    )
    register_tool_for_agents(
        run_python_script,
        caller=sora,
        executor=user_proxy,
        name="run_python_script",
        description="Executes a Python script in the workspace and returns STDOUT/STDERR.",
    )

async def attach_openclaw_mcp(onyx, sora, user_proxy):
    """Spawns OpenClaw MCP stdio server and binds tools directly to Onyx and Sora."""
    try:
        server_params = StdioServerParameters(
            command="openclaw",
            args=["mcp", "serve"]
        )

        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                mcp_tools = await session.list_tools()

                for tool in mcp_tools.tools:
                    # Dynamically create an execution wrapper for each MCP tool
                    def create_mcp_wrapper(tool_name):
                        async def mcp_wrapper(**kwargs):
                            result = await session.call_tool(tool_name, arguments=kwargs)
                            return str(result.content)
                        return mcp_wrapper

                    wrapper_fn = create_mcp_wrapper(tool.name)

                    # Register the tool natively in AutoGen / AG2
                    register_tool_for_agents(
                        wrapper_fn,
                        caller=[onyx, sora],
                        executor=user_proxy,
                        name=f"openclaw_{tool.name}",
                        description=tool.description or f"OpenClaw tool: {tool.name}",
                    )

                print("✅ [MCP] OpenClaw MCP Server connected and tools registered.")

    except Exception as e:
        print(f"⚠️ [MCP Warning] OpenClaw MCP initialization skipped: {e}")