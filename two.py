from functools import reduce
from typing import Callable, List, Optional, TypedDict
from langgraph.graph import END, START, StateGraph


class AgentState(TypedDict):
    name: str
    values: List[int]
    operation: Callable[[List[int]], int]
    output: Optional[str]


def node(state: AgentState) -> AgentState:
    value = state["operation"](state["values"])
    state["output"] = f"Hi {state['name']}, the answer is {value}"
    return state


def mul(x: List[int]) -> int:
    return reduce(lambda a, b: a * b, x, 1)


graph = StateGraph(AgentState)
graph.add_node("node", node)
graph.add_edge(START, "node")
graph.add_edge("node", END)

runner = graph.compile()
res = runner.invoke({"name": "john", "values": [1, 2, 5], "operation": mul})
print(res)
