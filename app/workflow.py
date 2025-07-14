from langgraph.graph import END, START, StateGraph

from app.agents import intent_agent
from app.models import ASK_ABOUT_WEATHER, GENERIC_QUESTION, MATH, QueryState
from app.tools import llm_tool, math_tool, weather_tool


async def intent_classifier(state: QueryState) -> QueryState:
    """Classify the intent of the user query."""
    result = await intent_agent.run(state.query)
    return QueryState(query=state.query, intent=result.data.intent)


def route_task(state: QueryState) -> str | None:
    """Route the task based on the classified intent."""
    return state.intent


def create_workflow_graph(intent_agent):
    """Create and configure the LangGraph workflow."""
    graph = StateGraph(QueryState)

    # Add nodes - use the async function directly
    graph.add_node("intent_classifier", intent_classifier)
    graph.add_node(MATH, math_tool)
    graph.add_node(ASK_ABOUT_WEATHER, weather_tool)
    graph.add_node(GENERIC_QUESTION, llm_tool)

    # Add edges
    graph.add_edge(START, "intent_classifier")
    graph.add_conditional_edges(
        "intent_classifier",
        route_task,
        [MATH, ASK_ABOUT_WEATHER, GENERIC_QUESTION],
    )
    graph.add_edge(MATH, END)
    graph.add_edge(ASK_ABOUT_WEATHER, END)
    graph.add_edge(GENERIC_QUESTION, END)

    return graph.compile()


# Create the workflow router
tool_router = create_workflow_graph(intent_agent)


# Query routing function
async def route_query(query: str):
    """
    Route a natural language query to the appropriate tool using the LangGraph workflow.

    Args:
        query: The user's natural language query

    Returns:
        QueryState: The final state containing the query, intent, and result
    """

    # Initialize the query state
    initial_state = QueryState(query=query)

    # Run the workflow (use ainvoke for async workflows)
    final_state = await tool_router.ainvoke(initial_state)

    return final_state
