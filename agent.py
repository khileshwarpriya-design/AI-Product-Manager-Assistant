"""Minimal CLI demo: a single-node LangGraph agent with no tools or memory.

Run with: python agent.py
"""

from typing import TypedDict

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph

load_dotenv()

MODEL_NAME = "gpt-4o-mini"

llm = ChatOpenAI(model=MODEL_NAME, temperature=0)


class AgentState(TypedDict):
    question: str
    answer: str


def answer_question(state: AgentState) -> dict:
    response = llm.invoke(state["question"])
    return {"answer": response.content}


def build_graph():
    graph = StateGraph(AgentState)
    graph.add_node("answer_question", answer_question)
    graph.add_edge(START, "answer_question")
    graph.add_edge("answer_question", END)
    return graph.compile()


def run_cli() -> None:
    app = build_graph()

    print("AI Product Manager Assistant (type 'exit' to quit)")

    while True:
        question = input("You: ")

        if question.lower() == "exit":
            print("Goodbye!")
            break

        result = app.invoke({"question": question, "answer": ""})
        print("Agent response:", result["answer"])


if __name__ == "__main__":
    run_cli()
