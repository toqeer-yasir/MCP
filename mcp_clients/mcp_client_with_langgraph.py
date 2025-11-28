# basic libraries:
import os
import math
import asyncio

from langchain_openai import ChatOpenAI

# library to create state_class
from typing import TypedDict, Annotated
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START
from dotenv import load_dotenv

# libraries to add tools:
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_tavily import TavilySearch

from langchain_mcp_adapters.client import MultiServerMCPClient

load_dotenv()

llm = ChatOpenAI(
     model= "x-ai/grok-4.1-fast:free",
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1",
    temperature=0.1
)


client = MultiServerMCPClient(
    {
        'Calculator': {
            'transport': 'stdio',
            'command': 'python',
            'args': ["/home/toqeer-yasir/Documents/repos/ai-agents-with-langgraph/agentic_chatbot/mcp_calculator_server.py"]
        },

        'Audio Control Server': {
            'transport': 'stdio',
            'command': 'python',
            'args': ["/home/toqeer-yasir/Documents/repos/ai-agents-with-langgraph/agentic_chatbot/music_player.py"]
        }
    }
)

search_tool = TavilySearch(
    max_results=3,
    include_answer=True,
    search_depth="advanced",
    tavily_api_key=os.getenv("TAVILY_API_KEY")
)


class ChatState(TypedDict):
    messages: Annotated[list, add_messages]

async def build_graph():
    calc_tools = await client.get_tools()
    
    tools = [search_tool]
    tools.extend(calc_tools)
    llm_with_tools = llm.bind_tools(tools=tools)

    print(tools)


    
    # Define the async chat_node function
    async def chat_node(state: ChatState):
        message = state['messages']
        response = await llm_with_tools.ainvoke(message)
        return {'messages': [response]}

    # Initialize the graph components
    tool_node = ToolNode(tools=tools)

    # define graph:
    graph = StateGraph(ChatState)

    # add nodes:
    graph.add_node('chat_node', chat_node)
    graph.add_node('tools', tool_node)

    # add edges:
    graph.add_edge(START, 'chat_node')
    graph.add_conditional_edges('chat_node', tools_condition)
    graph.add_edge('tools', 'chat_node')

    # Compile without checkpointer for async
    chatbot = graph.compile()

    return chatbot

async def main():
    chatbot = await build_graph()

    result = await chatbot.ainvoke(
        {'messages': [HumanMessage(content="how many songs are there in my music folder?")]}
    )
    print(result['messages'][-1].content)

if __name__ == "__main__":
    asyncio.run(main())