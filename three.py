from typing import List, Optional, TypedDict
from langchain_ollama.chat_models import ChatOllama
from langgraph.graph import END, START, StateGraph


class AgentState(TypedDict):
    name: str
    age: int
    skills: List[str]
    results: Optional[List[str]]


llm = ChatOllama(model="llama3.2:3b-instruct-q8_0", temperature=0)


def personalize(state: AgentState):
    state["results"] = []
    state["results"].append(
        str(
            llm.invoke(
                f"I need you to personalize a greeting for this name: {state['name']}"
            ).content
        )
    )

    return state


graph = StateGraph(AgentState)
graph.add_node("personalize", personalize)
graph.add_edge(START, "personalize")
graph.add_edge("personalize", END)

runner = graph.compile()
state = runner.invoke(
    {"name": "Mohammed", "age": 22, "skills": ["football", "basketball"]}
)

print(state)
