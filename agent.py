import os
from typing import TypedDict

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)
# 1. Define the state
class AgentState(TypedDict):
    question: str
    answer: str


# 2. Create the agent node
def answer_question(state: AgentState):
    print("Agent is thinking...")

    response = llm.invoke(state["question"])

    return {
        "answer": response.content
    }


# 3. Create the graph
graph = StateGraph(AgentState)

# Add our node
graph.add_node("answer_question", answer_question)

# Connect START → answer_question → END
graph.add_edge(START, "answer_question")
graph.add_edge("answer_question", END)

# Compile the graph
app = graph.compile()


# 4. Run the agent
while True:
    question = input("You: ")

    if question.lower() == "exit":
        print("Goodbye!")
        break

    result = app.invoke({
        "question": question,
        "answer": ""
    })

    print("Agent response:", result["answer"])