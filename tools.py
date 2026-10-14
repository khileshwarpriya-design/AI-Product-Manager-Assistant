"""Tools the AI Product Manager Assistant can call during reasoning."""

import ast
import operator

from langchain_core.tools import tool

# Only these AST node/operator types are permitted, so `calculator` can
# never execute arbitrary code (unlike a raw `eval`).
_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.FloorDiv: operator.floordiv,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def _safe_eval(node: ast.AST) -> float:
    """Recursively evaluate an arithmetic AST node.

    Raises ``ValueError`` for anything other than numeric literals and
    the operators listed in ``_ALLOWED_OPERATORS``.
    """
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value

    if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_OPERATORS:
        left = _safe_eval(node.left)
        right = _safe_eval(node.right)
        return _ALLOWED_OPERATORS[type(node.op)](left, right)

    if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_OPERATORS:
        return _ALLOWED_OPERATORS[type(node.op)](_safe_eval(node.operand))

    raise ValueError("Unsupported expression")


@tool
def calculator(expression: str) -> str:
    """Calculate a mathematical expression (e.g. "125 * 48")."""
    try:
        tree = ast.parse(expression, mode="eval")
        result = _safe_eval(tree.body)
        return str(result)
    except Exception:
        return "Sorry, I could not calculate that."


@tool
def text_length(text: str) -> str:
    """Count the number of characters in a text."""
    return str(len(text))
