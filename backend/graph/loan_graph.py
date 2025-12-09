from langgraph.graph import StateGraph, END
from agents.master import master_agent

class LoanState(dict):
    query: str
    memory: dict
    response: dict

def process_query(state: LoanState):
    reply, updated_memory = master_agent(state["query"], state["memory"])
    
    state["response"] = reply
    state["memory"] = updated_memory
    return state

workflow = StateGraph(LoanState)
workflow.add_node("process_query", process_query)
workflow.set_entry_point("process_query")
workflow.add_edge("process_query", END)

loan_graph = workflow.compile()
