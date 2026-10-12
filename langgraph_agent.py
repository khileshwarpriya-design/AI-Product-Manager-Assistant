from dotenv import load_dotenv

load_dotenv()

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, MessagesState, START
from langgraph.prebuilt import ToolNode, tools_condition

import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver

from tools import calculator, text_length


# 1. Create the LLM
llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)


# 2. Give tools to the LLM
tools = [calculator, text_length]

llm_with_tools = llm.bind_tools(tools)

#system message
system_message = SystemMessage(
    content="""
You are an AI Product Manager Assistant.

Your primary role is to help with:

1. Product Management
   - PRDs
   - User stories
   - Product requirements
   - Feature prioritization
   - Product strategy
   - Roadmaps
   - Product metrics

2. Technical Product Management
   - APIs
   - API integrations
   - Technical requirements
   - System workflows
   - AI and GenAI concepts
   - Technical documentation

3. AI Product Management
   - AI agents
   - LLM applications
   - Tool calling
   - AI product use cases
   - AI feature requirements

Behavior:
- Be practical and concise.
- Explain technical concepts in simple language.
- Use examples when helpful.
- Structure answers with bullets or tables when appropriate.
- Ask clarifying questions when requirements are unclear.

Boundaries:
- Stay focused on Product Management, Technology, and AI Product Management.
- If a request is unrelated to these areas, politely explain that your primary role is as an AI Product Manager Assistant.
"""
)
# 3. Create the LLM node
def call_model(state: MessagesState):
    recent_messages = state["messages"][-10:]

    messages = [
        system_message
    ] + recent_messages

    response = llm_with_tools.invoke(messages)

    return {
        "messages": [response]
    }


# 4. Create the graph
builder = StateGraph(MessagesState)


# 5. Add the LLM node
builder.add_node("llm", call_model)


# 6. Add the tool node
builder.add_node("tools", ToolNode(tools))


# 7. Start → LLM
builder.add_edge(START, "llm")


# 8. Decide whether to use a tool
builder.add_conditional_edges(
    "llm",
    tools_condition,
)


# 9. Tool → LLM
builder.add_edge("tools", "llm")


# 10. Create persistent memory
conn = sqlite3.connect(
    "agent_memory.db",
    check_same_thread=False
)

memory = SqliteSaver(conn)


# 11. Compile graph with memory
graph = builder.compile(
    checkpointer=memory
)


# 12. Start conversation


def ask_agent(user_input, thread_id="khileshwar-1"):
    result = graph.invoke(
        {
            "messages": [
                HumanMessage(content=user_input)
            ]
        },
        config={
            "configurable": {
                "thread_id": thread_id
            }
        }
    )

    messages = result["messages"]

    # Find tool calls made by the AI
    tool_calls = []

    for message in messages:
        if getattr(message, "tool_calls", None):
            for tool_call in message.tool_calls:
                tool_calls.append({
                    "name": tool_call.get("name", "Unknown tool"),
                    "args": tool_call.get("args", {})
                })

    # Return the answer and tool-call details
    return {
        "answer": messages[-1].content,
        "tool_calls": tool_calls
    }

