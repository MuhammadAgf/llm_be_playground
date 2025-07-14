import math

import numexpr

from app.agents import extractor_agent
from app.models import QueryState


async def extract_math_expr(query: str) -> str:
    """Extract arithmetic expression from user query for Python eval."""
    prompt = (
        "Extract the arithmetic expression from the user's query so it's runnable by "
        f"python eval. If none found, return an empty string. Query: '{query}'"
    )
    resp = await extractor_agent.run(prompt)
    return resp.output.strip()


def calculate_math_expression(expression: str) -> str:
    """Calculate expression using Python's numexpr library.

    Expression should be a single line mathematical expression
    that solves the problem.

    Examples:
        "37593 * 67" for "37593 times 67"
        "37593**(1/5)" for "37593^(1/5)"
    """
    local_dict = {"pi": math.pi, "e": math.e}
    return str(
        numexpr.evaluate(
            expression.strip(),
            global_dict={},
            local_dict=local_dict,
        )
    )


async def math_tool(state: QueryState) -> QueryState:
    """Process mathematical expressions."""
    expr = await extract_math_expr(query=state.query)
    if not expr:
        state.result = "No valid arithmetic expression found."
        return state
    try:
        state.result = calculate_math_expression(expr)
    except Exception as e:
        state.result = f"Error evaluating '{expr}': {e}"
    return state
