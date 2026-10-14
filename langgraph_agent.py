"""LangGraph agent powering the AI Product Manager Assistant.

Defines the conversational graph (LLM node + tool node), the system
prompt that scopes the assistant to product-management topics, and the
``ask_agent`` entry point used by the Streamlit UI.
"""

import sqlite3
from typing import TypedDict

from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from tools import calculator, text_length

load_dotenv()

MODEL_NAME = "gpt-4o-mini"
MEMORY_DB_PATH = "agent_memory.db"
MAX_HISTORY_MESSAGES = 10
DEFAULT_THREAD_ID = "default-thread"

SYSTEM_PROMPT = SystemMessage(
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


class ToolCall(TypedDict):
    name: str
    args: dict


class AgentResponse(TypedDict):
    answer: str
    tool_calls: list[ToolCall]


tools = [calculator, text_length]

llm = ChatOpenAI(model=MODEL_NAME, temperature=0)
llm_with_tools = llm.bind_tools(tools)


def call_model(state: MessagesState) -> dict:
    """LLM node: answers using the system prompt plus recent history."""
    recent_messages = state["messages"][-MAX_HISTORY_MESSAGES:]
    messages = [SYSTEM_PROMPT] + recent_messages
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}


def _build_graph(checkpointer: SqliteSaver):
    builder = StateGraph(MessagesState)

    builder.add_node("llm", call_model)
    builder.add_node("tools", ToolNode(tools))

    builder.add_edge(START, "llm")
    builder.add_conditional_edges("llm", tools_condition)
    builder.add_edge("tools", "llm")

    return builder.compile(checkpointer=checkpointer)


# A single, long-lived SQLite connection backs conversational memory so
# that chat history survives across Streamlit re-runs and app restarts.
_connection = sqlite3.connect(MEMORY_DB_PATH, check_same_thread=False)
_memory = SqliteSaver(_connection)
graph = _build_graph(_memory)


def _extract_tool_calls(messages: list[BaseMessage]) -> list[ToolCall]:
    """Collect every tool call made by the assistant during this turn."""
    tool_calls: list[ToolCall] = []

    for message in messages:
        for tool_call in getattr(message, "tool_calls", None) or []:
            tool_calls.append(
                {
                    "name": tool_call.get("name", "Unknown tool"),
                    "args": tool_call.get("args", {}),
                }
            )

    return tool_calls


def ask_agent(user_input: str, thread_id: str = DEFAULT_THREAD_ID) -> AgentResponse:
    """Run one turn of the conversation and return the answer + tool calls.

    ``thread_id`` scopes conversational memory: messages sharing the same
    thread id are treated as one continuous conversation.
    """
    result = graph.invoke(
        {"messages": [HumanMessage(content=user_input)]},
        config={"configurable": {"thread_id": thread_id}},
    )

    messages = result["messages"]

    return {
        "answer": messages[-1].content,
        "tool_calls": _extract_tool_calls(messages),
    }
