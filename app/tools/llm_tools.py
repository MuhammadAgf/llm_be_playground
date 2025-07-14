from app.agents import llm_agent
from app.models import QueryState


async def llm_tool(state: QueryState) -> QueryState:
    """Process generic questions using LLM."""
    result = await llm_agent.run(state.query)
    state.result = result.output
    return state
