from langchain_core.tools import tool


@tool
def calculator(expression: str) -> str:
    """Calculate a mathematical expression."""
    try:
        result = eval(expression)
        return str(result)
    except Exception:
        return "Sorry, I could not calculate that."
    
    
@tool
def text_length(text: str) -> str:
    """Count the number of characters in a text."""
    return str(len(text))