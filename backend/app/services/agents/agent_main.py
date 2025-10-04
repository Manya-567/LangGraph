
from app.services.agents.core.report_factcheck_agent import compiled_workflow

def run_report_and_factcheck(user_query: str):
    """
    Runs the combined report generation + fact-check workflow.
    """
    initial_state = {
        "query": user_query,
        "report": "",
        "final_report": ""
    }

    # Invoke the LangGraph workflow
    result_state = compiled_workflow.invoke(initial_state)
    return result_state["final_report"]

# ---------------- Test ----------------
# if __name__ == "__main__":
#     sample_query = "Tell me about the Solar System."
#     output = run_report_and_factcheck(sample_query)
#     print(output)




