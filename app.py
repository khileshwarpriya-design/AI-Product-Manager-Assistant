import streamlit as st
import uuid

from langgraph_agent import ask_agent


# Page configuration

st.set_page_config(
    page_title="AI Product Manager Assistant",
    page_icon="🤖",
    layout="wide"
)


st.title("🤖 AI Product Manager Assistant")

st.markdown(
    "Your AI workspace for **product discovery, requirements, "
    "prioritization, and product analytics.**"
)

st.caption(
    "Powered by LangGraph + Groq | Built as an AI Product Management project"
)

st.markdown("---")


# -----------------------------
# Conversation setup
# -----------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

if "chat_title" not in st.session_state:
    st.session_state.chat_title = "New Chat"

if "run_quick_action" not in st.session_state:
    st.session_state.run_quick_action = False


# -----------------------------
# Sidebar
# -----------------------------

st.sidebar.title("🤖 PM Workspace")

st.sidebar.caption(
    "Your AI-powered product management companion"
)

st.sidebar.markdown("---")

if st.sidebar.button("➕ New Chat"):

    st.session_state.messages = []

    st.session_state.thread_id = str(uuid.uuid4())

    st.session_state.chat_title = "New Chat"

    st.experimental_rerun()


if "chat_title" not in st.session_state:
    st.session_state.chat_title = "New Chat"


st.sidebar.markdown("### 🗂️ Current Chat")

st.sidebar.write(
    st.session_state.chat_title
)



st.sidebar.markdown("### ⚡ PM Quick Actions")

if st.sidebar.button("📋 Create PRD"):
    st.session_state.user_input = (
        "Create a detailed Product Requirements Document (PRD) "
        "for an employee attendance tracking feature."
    )
    st.session_state.run_quick_action = True

if st.sidebar.button("👤 Create User Story"):
    st.session_state.user_input = (
        "Create a user story for an employee applying for leave "
        "through an HRMS application. Include acceptance criteria "
        "in Given-When-Then format."
    )
    st.session_state.run_quick_action = True

if st.sidebar.button("🎯 Prioritize Features"):
    st.session_state.user_input = (
        "Prioritize these HRMS features using the RICE framework: "
        "employee self-service portal, AI HR chatbot, attendance "
        "tracking, and payroll automation. State your assumptions "
        "and explain the scores."
    )
    st.session_state.run_quick_action = True

if st.sidebar.button("📊 Define Product Metrics"):
    st.session_state.user_input = (
        "Define the North Star Metric and 5 supporting KPIs for "
        "an employee self-service HRMS application. Explain each "
        "metric, its formula, and why it matters."
    )
    st.session_state.run_quick_action = True
    

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

    st.caption(
        "Python · Streamlit · LangGraph · Groq"
    )

# -----------------------------
# Display conversation
# -----------------------------



for message in st.session_state.messages:

    if message["role"] == "user":

        st.markdown("### 👤 You")
        st.markdown(message["content"])

    else:

        st.markdown("### 🤖 AI Product Manager")
        st.markdown(message["content"])

        tool_calls = message.get("tool_calls", [])

        if tool_calls:
            with st.expander("🔧 View tool execution details"):

                for tool_call in tool_calls:

                    st.markdown(
                        "**Tool:** `" + tool_call["name"] + "`"
                    )

                    st.markdown("**Arguments passed to the tool:**")
                    st.json(tool_call["args"])

        st.markdown("---")

# -----------------------------
# User input
# -----------------------------

user_input = st.text_input(
    "Ask your product management question:",
    key="user_input"
)


# -----------------------------
# Send button
# -----------------------------


if st.button("Send") or st.session_state.get(
    "run_quick_action", False
):

    st.session_state.run_quick_action = False

    if user_input.strip():

        # Create chat title from first user question
        if len(st.session_state.messages) == 0:

            title = user_input.strip()

            if len(title) > 35:
                title = title[:35] + "..."

            st.session_state.chat_title = title
        
        # Store user message
        st.session_state.messages.append(
            {
                "role": "user",
                "content": user_input
            }
        )

        # Get AI response
        with st.spinner("🤖 AI Product Manager is thinking..."):

            response = ask_agent(
                user_input,
                thread_id=st.session_state.thread_id
            )

        # Store AI response
        
# Store AI answer
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response["answer"],
                "tool_calls": response["tool_calls"]
            }
        )

        # Refresh page
        st.experimental_rerun()