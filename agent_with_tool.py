"""Minimal demo of manual tool calling with an LLM (no LangGraph).

Shows the raw request/response loop behind tool calling: ask the model,
execute the tool it picks, then feed the result back for a final answer.

Run with: python agent_with_tool.py
"""

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from tools import calculator

load_dotenv()

MODEL_NAME = "gpt-4o-mini"
QUESTION = "What is 125 multiplied by 48?"


def run_demo() -> None:
    llm = ChatOpenAI(model=MODEL_NAME, temperature=0)
    llm_with_tools = llm.bind_tools([calculator])

    messages = [("user", QUESTION)]

    # Step 1: Ask the AI
    response = llm_with_tools.invoke(messages)
    print("AI decided to use:")
    print(response.tool_calls)
    messages.append(response)

    # Step 2: Execute the tool the AI chose
    tool_call = response.tool_calls[0]
    tool_result = calculator.invoke(tool_call["args"])
    print("Calculator result:")
    print(tool_result)

    # Step 3: Give the tool result back to the AI
    messages.append(
        {
            "role": "tool",
            "content": tool_result,
            "tool_call_id": tool_call["id"],
        }
    )

    # Step 4: Ask the AI for its final answer
    final_response = llm_with_tools.invoke(messages)
    print("Final AI answer:")
    print(final_response.content)


if __name__ == "__main__":
    run_demo()
