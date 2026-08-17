from fastapi import FastAPI

from app.api.schemas import QueryRequest, QueryResponse
from app.llm.llm_client import ask_database


app = FastAPI(
    title="Text-to-SQL API",
    description="Natural language to MySQL query system",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Text-to-SQL API is running"
    }


@app.post("/query", response_model=QueryResponse)
def query_database(request: QueryRequest):

    result = ask_database(
        request.question
    )

    return {
        "question": request.question,
        "sql": result["sql"],
        "results": result["results"]
    }