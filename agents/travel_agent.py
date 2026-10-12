import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)

prompt = f"""
You are a helpful AI assistant.

Answer the user's question in simple layman language.
Avoid unnecessary technical jargon.
If you use a technical term, explain it briefly.

User question:
{state["question"]}
"""

response = llm.invoke(prompt)

print(response.content)