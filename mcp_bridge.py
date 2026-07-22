# mcp_bridge.py
import asyncio
from autogen import register_function

# MCP & AG2 Imports
from mcp import StdioServerParameters, ClientSession
from mcp.client.stdio import stdio_client
from autogen.tools.mcp import StdioMcpToolAdapter

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
    """Spawns OpenClaw MCP stdio server and binds tools to Onyx and Sora."""
    try:
        # Define connection parameters for OpenClaw stdio process
        server_params = StdioServerParameters(
            command="openclaw",
            args=["mcp", "serve"]
        )

        # Establish stdio client connection
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                # Retrieve available tools from OpenClaw MCP
                mcp_tools = await session.list_tools()

                # Register each tool returned by OpenClaw to Onyx and Sora
                for tool in mcp_tools.tools:
                    adapter = StdioMcpToolAdapter(
                        server_params=server_params,
                        tool=tool,
                        session=session
                    )
                    # Register adapter to AG2 agents
                    for agent in [onyx, sora]:
                        adapter.register_for_llm(agent)
                    adapter.register_for_execution(user_proxy)

                print("✅ [MCP] OpenClaw MCP Server tools successfully registered.")

    except Exception as e:
        print(f"⚠️ [MCP Warning] OpenClaw MCP initialization skipped: {e}")