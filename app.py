"""Streamlit UI for the AI Product Manager Assistant."""

import uuid

import streamlit as st

from langgraph_agent import ask_agent

PAGE_TITLE = "AI Product Manager Assistant"
CHAT_TITLE_MAX_LENGTH = 35

QUICK_ACTIONS = [
    (
        "📋 Create PRD",
        "Create a detailed Product Requirements Document (PRD) "
        "for an employee attendance tracking feature.",
    ),
    (
        "👤 Create User Story",
        "Create a user story for an employee applying for leave "
        "through an HRMS application. Include acceptance criteria "
        "in Given-When-Then format.",
    ),
    (
        "🎯 Prioritize Features",
        "Prioritize these HRMS features using the RICE framework: "
        "employee self-service portal, AI HR chatbot, attendance "
        "tracking, and payroll automation. State your assumptions "
        "and explain the scores.",
    ),
    (
        "📊 Define Product Metrics",
        "Define the North Star Metric and 5 supporting KPIs for "
        "an employee self-service HRMS application. Explain each "
        "metric, its formula, and why it matters.",
    ),
]


def init_session_state() -> None:
    """Set up the per-session chat state on first load."""
    defaults = {
        "messages": [],
        "thread_id": str(uuid.uuid4()),
        "chat_title": "New Chat",
        "run_quick_action": False,
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


def start_new_chat() -> None:
    st.session_state.messages = []
    st.session_state.thread_id = str(uuid.uuid4())
    st.session_state.chat_title = "New Chat"
    st.rerun()


def queue_quick_action(prompt: str) -> None:
    st.session_state.user_input = prompt
    st.session_state.run_quick_action = True


def render_header() -> None:
    st.set_page_config(page_title=PAGE_TITLE, page_icon="🤖", layout="wide")
    st.title(f"🤖 {PAGE_TITLE}")
    st.markdown(
        "Your AI workspace for **product discovery, requirements, "
        "prioritization, and product analytics.**"
    )
    st.caption("Powered by LangGraph + OpenAI | Built as an AI Product Management project")
    st.markdown("---")


def render_sidebar() -> None:
    st.sidebar.title("🤖 PM Workspace")
    st.sidebar.caption("Your AI-powered product management companion")
    st.sidebar.markdown("---")

    if st.sidebar.button("➕ New Chat"):
        start_new_chat()

    st.sidebar.markdown("### 🗂️ Current Chat")
    st.sidebar.write(st.session_state.chat_title)

    st.sidebar.markdown("### ⚡ PM Quick Actions")
    for label, prompt in QUICK_ACTIONS:
        if st.sidebar.button(label):
            queue_quick_action(prompt)

    st.sidebar.markdown("---")
    with st.sidebar.expander("ℹ️ About this Assistant"):
        st.write(
            "An AI-powered workspace designed to support "
            "everyday Product Management tasks."
        )
        st.markdown("**Capabilities**")
        st.markdown(
            "- Product Requirements Documents (PRDs)\n"
            "- Agile user stories and acceptance criteria\n"
            "- Feature prioritization using RICE\n"
            "- Product metrics and KPIs\n"
            "- Tool calling through LangGraph"
        )
        st.markdown("**Technology Stack**")
        st.caption("Python · Streamlit · LangGraph · OpenAI")


def render_tool_calls(tool_calls: list[dict]) -> None:
    if not tool_calls:
        return

    with st.expander("🔧 View tool execution details"):
        for tool_call in tool_calls:
            st.markdown(f"**Tool:** `{tool_call['name']}`")
            st.markdown("**Arguments passed to the tool:**")
            st.json(tool_call["args"])


def render_conversation() -> None:
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown("### 👤 You")
            st.markdown(message["content"])
        else:
            st.markdown("### 🤖 AI Product Manager")
            st.markdown(message["content"])
            render_tool_calls(message.get("tool_calls", []))

        st.markdown("---")


def chat_title_from(user_input: str) -> str:
    title = user_input.strip()
    if len(title) > CHAT_TITLE_MAX_LENGTH:
        title = title[:CHAT_TITLE_MAX_LENGTH] + "..."
    return title


def handle_user_message(user_input: str) -> None:
    if not user_input.strip():
        return

    if not st.session_state.messages:
        st.session_state.chat_title = chat_title_from(user_input)

    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.spinner("🤖 AI Product Manager is thinking..."):
        response = ask_agent(user_input, thread_id=st.session_state.thread_id)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response["answer"],
            "tool_calls": response["tool_calls"],
        }
    )

    st.rerun()


def render_input_area() -> None:
    user_input = st.text_input(
        "Ask your product management question:", key="user_input"
    )

    should_send = st.button("Send") or st.session_state.run_quick_action
    st.session_state.run_quick_action = False

    if should_send:
        handle_user_message(user_input)


def main() -> None:
    init_session_state()
    render_header()
    render_sidebar()
    render_conversation()
    render_input_area()


if __name__ == "__main__":
    main()
