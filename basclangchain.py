from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI

# LangGraph core imports
from langgraph.graph import Graph
from langgraph.schema import Node, Edge
# Node implementations in latest LangGraph layout
from langgraph.nodes.llm import LLMNode
from langgraph.nodes.execution import PythonExecutionNode
from langgraph.nodes.output import OutputNode
from langgraph.utils import connect_nodes

# Initialize the LLM
llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

# Agent factories for Python or Pandas workflows
from agents.agent_toolkits.python.base import create_python_agent
from agents.agent_toolkits.pandas.base import create_pandas_dataframe_agent

# Build the directed graph
graph = Graph(name="DataAnalysisAgent")

# Input: user query
user_query = Node(name="UserQuery", node_type="input")

# Reasoning (pre-execution)
reasoning_pre = LLMNode(name="ReasoningPre", llm=llm)

# Python execution node (swap agent_factory for Pandas if desired)
python_exec = PythonExecutionNode(
    name="PythonExec",
    agent_factory=lambda: create_python_agent(llm=llm)
)

# Reasoning (post-execution)
reasoning_post = LLMNode(name="ReasoningPost", llm=llm)

# Final output node
output = OutputNode(name="Output")

# Define edges according to directed workflow
graph.add_edge(Edge(user_query, reasoning_pre))
graph.add_edge(Edge(reasoning_pre, python_exec))
graph.add_edge(Edge(python_exec, reasoning_post))
# Loop back for additional code execution when needed
graph.add_edge(Edge(reasoning_post, python_exec, condition="needs_more_exec"))
# Complete the flow when done
graph.add_edge(Edge(reasoning_post, output, condition="done"))

# Auto-connect any remaining ports
connect_nodes(graph)

# Runner utility

def run_agent(query, dataframe=None):
    graph.context["UserQuery"] = query
    if dataframe is not None:
        graph.context["dataframe"] = dataframe
    return graph.run(start_node="UserQuery")

# Usage example
if __name__ == "__main__":
    import pandas as pd
    df = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})
    result = run_agent("Show the correlation between x and y", dataframe=df)
    print(result)
