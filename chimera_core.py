import discord
import asyncio
import queue
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
from config import LLM_CONFIG, CHANNEL_HISTORY
from mcp_bridge import setup_local_workspace_tools, attach_openclaw_mcp

DISCORD_TOKEN = "MTQ5NDc3NjUxMTg4NDk1NTY2OA.GRqqE9.LRBuYTWa3hbKGE133K32xyQgLILJ6ORyVxwIj0"

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Project Chimera Engine live as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if client.user.mentioned_in(message):
        channel_id = message.channel.id
        user_prompt = message.content.replace(f'<@{client.user.id}>', '').strip()

        if channel_id not in CHANNEL_HISTORY:
            CHANNEL_HISTORY[channel_id] = []

        status_msg = await message.channel.send("⏳ **Project Chimera Swarm Initializing...**")
        msg_queue = queue.Queue()
        current_run_transcript = []

        # --- SWARM EXECUTION WORKER ---
        def run_swarm_thread():
            def agent_hook(sender, recipient, message=None, silent=False, **kwargs):
                if message:
                    content = message.get("content", "") if isinstance(message, dict) else str(message)
                    name = message.get("name", getattr(sender, "name", "Agent")) if isinstance(message, dict) else getattr(sender, "name", "Agent")

                    if content and name != "User_Controller":
                        msg_queue.put((name, content))
                return message

            # 1. Instantiation
            onyx = AssistantAgent(
                name="Onyx",
                system_message=(
                    "You are Onyx, Lead System Orchestrator.\n"
                    "RULES:\n"
                    "1. DO NOT write or output raw code blocks into chat. Coordinate Sora and Atlas.\n"
                    "2. Keep chat responses concise and strategic."
                ),
                llm_config=LLM_CONFIG,
            )
            sora = AssistantAgent(
                name="Sora",
                system_message=(
                    "You are Sora, Lead Coder.\n"
                    "RULES:\n"
                    "1. DO NOT output code directly into chat text.\n"
                    "2. You MUST use `write_workspace_file` to save all code to disk.\n"
                    "3. You MUST use `run_python_script` to test code after writing it."
                ),
                llm_config=LLM_CONFIG,
            )
            atlas = AssistantAgent(
                name="Atlas",
                system_message=(
                    "You are Atlas, Performance Auditor.\n"
                    "RULES:\n"
                    "1. Use `read_workspace_file` to inspect code written by Sora.\n"
                    "2. Point out logic bugs for Sora to fix."
                ),
                llm_config=LLM_CONFIG,
            )
            user_proxy = UserProxyAgent(
                name="User_Controller",
                human_input_mode="NEVER",
                max_consecutive_auto_reply=1,
                code_execution_config=False,
            )

            # 2. Attach Hooks & Tools
            for agent in [onyx, sora, atlas]:
                agent.register_hook("process_message_before_send", agent_hook)

            setup_local_workspace_tools(onyx, sora, atlas, user_proxy)

            # OpenClaw MCP Attachment (Run within thread loop)
            asyncio.run(attach_openclaw_mcp(onyx, sora, user_proxy))

            # 3. Setup Context & Execute
            existing_messages = list(CHANNEL_HISTORY[channel_id])
            groupchat = GroupChat(
                agents=[user_proxy, onyx, sora, atlas],
                messages=existing_messages,
                max_round=len(existing_messages) + 4,
                speaker_selection_method="round_robin",
            )
            manager = GroupChatManager(groupchat=groupchat, llm_config=LLM_CONFIG)

            user_proxy.initiate_chat(manager, message=user_prompt)

            # 4. History Memory Cleanup
            filtered_history = [
                msg for msg in groupchat.messages 
                if (isinstance(msg.get("content"), str) and msg.get("content").strip()) 
                or msg.get("tool_calls")
            ]
            CHANNEL_HISTORY[channel_id] = filtered_history[-12:]
            msg_queue.put(None)

        # --- ASYNC QUEUE CONSUMER ---
        loop = asyncio.get_running_loop()
        swarm_future = loop.run_in_executor(None, run_swarm_thread)

        while True:
            await asyncio.sleep(0.5)
            has_new = False
            while not msg_queue.empty():
                item = msg_queue.get_nowait()
                if item is None:
                    break
                name, content = item
                current_run_transcript.append(f"**[{name}]**:\n{content}\n")
                has_new = True

            if has_new and current_run_transcript:
                full_text = "\n---\n".join(current_run_transcript)
                if len(full_text) > 1900:
                    full_text = full_text[-1900:]
                try:
                    await status_msg.edit(content=full_text)
                except Exception as e:
                    print(f"Discord Edit Error: {e}")

            if swarm_future.done() and msg_queue.empty():
                break

        await swarm_future

        final_text = "\n---\n".join(current_run_transcript) if current_run_transcript else "⚠️ Task complete with no text output."
        
        # Chunk text into <= 1900 character slices to respect Discord limits
        chunk_size = 1900
        chunks = [final_text[i : i + chunk_size] for i in range(0, len(final_text), chunk_size)]

        if chunks:
            # Edit the placeholder message with the first chunk
            await status_msg.edit(content=chunks[0])
            
            # Send any remaining chunks as follow-up messages in the channel
            for extra_chunk in chunks[1:]:
                await message.channel.send(extra_chunk)

if __name__ == "__main__":
    client.run(DISCORD_TOKEN)