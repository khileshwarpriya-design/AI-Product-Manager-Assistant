from dotenv import load_dotenv

load_dotenv()

from langchain_groq import ChatGroq
from tools import calculator

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)

tools = [calculator]

llm_with_tools = llm.bind_tools(tools)

messages = [
    (
        "user",
        "What is 125 multiplied by 48?"
    )
]

# Step 1: Ask the AI
response = llm_with_tools.invoke(messages)

print("AI decided to use:")
print(response.tool_calls)

# Add AI response to conversation
messages.append(response)

# Step 2: Execute the tool
tool_call = response.tool_calls[0]

tool_result = calculator.invoke(
    tool_call["args"]
)

print("Calculator result:")
print(tool_result)

# Step 3: Give tool result back to AI
messages.append(
    {
        "role": "tool",
        "content": tool_result,
        "tool_call_id": tool_call["id"]
    }
)

# Step 4: Ask AI for final answer
final_response = llm_with_tools.invoke(messages)

print("Final AI answer:")
print(final_response.content)