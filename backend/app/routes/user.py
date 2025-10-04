

from fastapi import APIRouter
from pydantic import BaseModel
from app.services.agents.agent_main import run_report_and_factcheck

router = APIRouter()

# Request model
class QueryRequest(BaseModel):
    query: str

# Endpoint for report + fact-check
@router.post("/report-factcheck")
def report_factcheck(req: QueryRequest):
    """
    Accepts a user query, runs the report agent, then fact-check agent,
    and returns a structured JSON with the report and fact-check result.
    """
    result = run_report_and_factcheck(req.query)
    return result
