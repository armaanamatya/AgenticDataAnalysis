from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, ToolMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from .state import AgentState
import json
from typing import Literal
from .tools import complete_python_task
#from langgraph.tools import ToolInvocation, ToolExecutor
from langgraph.prebuilt import ToolNode

import os
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI

# Configure the ChatOpenAI with Google Gemini model and API key
llm = ChatGoogleGenerativeAI(
    model="google/gemini-2.5-flash-preview-05-20",
    temperature=0,
    google_api_key="AIzaSyAGHny8arM_Q6JpiLmtwmoGRNIbhOuzP0I"
)

tools = [complete_python_task]

model = llm.bind_tools(tools)

#tool_executor = ToolExecutor(tools)

tool_node = ToolNode(tools)

with open(os.path.join(os.path.dirname(__file__), "../prompts/main_prompt.md"), "r") as file:
    prompt = file.read()

chat_template = ChatPromptTemplate.from_messages([
    ("system", prompt),
    ("placeholder", "{messages}"),
])
model = chat_template | model

def create_data_summary(state: AgentState) -> str:
    summary = ""
    for data in state["input_data"]:
        try:
            # Read the file content
            with open(data.data_path, "r") as file:
                content = file.read()
            summary += (
                f"\n\nVariable: {data.variable_name}\n"
                f"Description: {data.data_description}\n"
                f"Data:\n{content}\n"
            )
        except Exception as e:
            summary += f"\n\nError reading {data.variable_name}: {str(e)}"
    return summary

def route_to_tools(
    state: AgentState,
) -> Literal["tools", "__end__"]:
    """
    Use in the conditional_edge to route to the ToolNode if the last message
    has tool calls. Otherwise, route back to the agent.
    """

    if messages := state.get("messages", []):
        ai_message = messages[-1]
    else:
        raise ValueError(f"No messages found in input state to tool_edge: {state}")
    
    if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
        return "tools"
    return "__end__"

def call_model(state: AgentState):

    current_data_template  = """The following data is available:\n{data_summary}"""
    current_data_message = HumanMessage(content=current_data_template.format(data_summary=create_data_summary(state)))
    state["messages"] = [current_data_message] + state["messages"]

    llm_outputs = model.invoke(state)

    return {"messages": [llm_outputs], "intermediate_outputs": [current_data_message.content]}

def call_tools(state: AgentState):
    """Call the tools using the updated ToolNode approach"""
    return tool_node.invoke(state)

    # last_message = state["messages"][-1]
    # tool_invocations = []
    # if isinstance(last_message, AIMessage) and hasattr(last_message, 'tool_calls'):
    #     tool_invocations = [
    #         ToolInvocation(
    #             tool=tool_call["name"],
    #             tool_input={**tool_call["args"], "graph_state": state}
    #         ) for tool_call in last_message.tool_calls
    #     ]

    # responses = tool_executor.batch(tool_invocations, return_exceptions=True)
    # tool_messages = []
    # state_updates = {}

    # for tc, response in zip(last_message.tool_calls, responses):
    #     if isinstance(response, Exception):
    #         raise response
    #     message, updates = response
    #     tool_messages.append(ToolMessage(
    #         content=str(message),
    #         name=tc["name"],
    #         tool_call_id=tc["id"]
    #     ))
    #     state_updates.update(updates)

    # if 'messages' not in state_updates:
    #     state_updates["messages"] = []

    # state_updates["messages"] = tool_messages 
    # return state_updates

