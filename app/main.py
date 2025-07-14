import traceback

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.config import settings
from app.models import OUTPUT_MAP
from app.workflow import route_query

# Load environment variables
load_dotenv()

app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version,
)


class QueryRequest(BaseModel):
    query: str


class QueryResponse(BaseModel):
    query: str
    tool_used: str
    result: str


@app.get("/")
async def root():
    return {"message": "Query Router API is running"}


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """
    Process a natural language query and route it to the appropriate tool.

    Args:
        request: QueryRequest containing the user's query

    Returns:
        QueryResponse with the original query, tool used, and result
    """
    try:
        # Route the query to the appropriate tool
        agent_response = await route_query(request.query)

        return QueryResponse(
            query=request.query,
            tool_used=OUTPUT_MAP[agent_response["intent"]],
            result=agent_response["result"],
        )
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=settings.host, port=settings.port)
