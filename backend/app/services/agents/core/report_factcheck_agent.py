# backend/app/services/agents/core/report_factcheck_agent.py

from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
import json

# Load Gemini API key from .env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize Gemini 2.0
gemini_llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=GEMINI_API_KEY)

# State for LangGraph workflow
class ReportFactCheckState(TypedDict):
    query: str
    report: str
    final_report: str

# ---------------- Report Node ----------------
def generate_report(state: ReportFactCheckState) -> ReportFactCheckState:
    query = state.get("query", "").strip()
    if not query:
        state["report"] = "No query provided."
        return state

    # LLM prompt for report generation
    report_prompt = f"""
You are a helpful assistant. Generate a concise report based on the query:
{query}

Provide the output in 2-3 lines.
"""
    try:
        state["report"] = gemini_llm.invoke(report_prompt)
    except Exception as e:
        state["report"] = f"Failed to generate report: {e}"
    return state

# ---------------- FactCheck Node ----------------
def fact_check(state: ReportFactCheckState) -> ReportFactCheckState:
    # Extract text from AIMessage object
    text_obj = state.get("report", "")
    
    # If Gemini returns AIMessage, get its .content
    if hasattr(text_obj, "content"):
        text = text_obj.content.strip()
    else:
        text = str(text_obj).strip()

    if not text:
        state["final_report"] = "No report to fact-check."
        return state

    # Prompt for fact-checking
    fact_prompt = f"""
You are a fact-checking assistant. Verify the following report:
{text}

1. Is the content factually correct? 
2. If there are errors, provide the corrected version.
3. Give a short explanation if corrections were needed.

Return in JSON format:
{{
  "is_correct": true/false,
  "corrected_report": "...",
  "explanation": "..."
}}
"""
    try:
        llm_response = gemini_llm.invoke(fact_prompt)

        # Extract content if llm_response is AIMessage
        if hasattr(llm_response, "content"):
            llm_response_text = llm_response.content
        else:
            llm_response_text = str(llm_response)

        result = json.loads(llm_response_text)
        corrected_report = result.get("corrected_report", text)
        explanation = result.get("explanation", "Verified")
        state["final_report"] = f"According to the user query: {state['query']}\n\nReport: {corrected_report}\n\nFact-check: {explanation}"

    except Exception as e:
        state["final_report"] = f"According to the user query: {state['query']}\n\nReport: {text}\n\nFact-check failed: {e}"

    return state


# ---------------- LangGraph Workflow ----------------
workflow_graph = StateGraph(ReportFactCheckState)
workflow_graph.add_node("generate_report", generate_report)
workflow_graph.add_node("fact_check", fact_check)
workflow_graph.add_edge(START, "generate_report")
workflow_graph.add_edge("generate_report", "fact_check")
workflow_graph.add_edge("fact_check", END)

compiled_workflow = workflow_graph.compile()

# ---------------- Test Run ----------------
# if __name__ == "__main__":
#     sample_state = {"query": "Tell me about the Solar System.", "report": "", "final_report": ""}
#     result = compiled_workflow.invoke(sample_state)
#     print(result["final_report"])
