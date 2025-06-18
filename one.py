from typing import Optional, TypedDict
from langgraph.graph import END, START, StateGraph


class AgentState(TypedDict):
    name: Optional[str]
    result: Optional[str]


def node(state: AgentState):
    state["result"] = f"hello {state['name']}, how are you?"
    return state


graph = StateGraph(AgentState)
graph.add_node("node", node)
graph.add_edge(START, "node")
graph.add_edge("node", END)


runner = graph.compile()
result = runner.invoke({"name": "Bob"})
print(result)

