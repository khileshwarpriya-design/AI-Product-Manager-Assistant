"""Minimal single-turn "explain it simply" demo agent.

Run with: python agents/travel_agent.py
"""

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

MODEL_NAME = "gpt-4o-mini"

PROMPT_TEMPLATE = """
You are a helpful AI assistant.

Answer the user's question in simple layman language.
Avoid unnecessary technical jargon.
If you use a technical term, explain it briefly.

User question:
{question}
"""


def answer(question: str) -> str:
    llm = ChatOpenAI(model=MODEL_NAME, temperature=0)
    response = llm.invoke(PROMPT_TEMPLATE.format(question=question))
    return response.content


if __name__ == "__main__":
    user_question = input("Ask a question: ")
    print(answer(user_question))
