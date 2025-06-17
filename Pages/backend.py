from langchain_core.messages import HumanMessage, AIMessage
from typing import List
from dataclasses import dataclass
import google.generativeai as genai
import requests
from langgraph.graph import StateGraph, START, END
from .graph.state import AgentState
from .graph.nodes import call_model, call_tools, route_to_tools
from Pages.data_models import InputData
#from IPython.display import Image, display

class PythonChatbot:
    def __init__(self):
        super().__init__()
        # self.api_url = "http://localhost:8000/v1/completions"  # Remove this line
        self.google_api_key = "AIzaSyAGHny8arM_Q6JpiLmtwmoGRNIbhOuzP0I"  # Your API key
        genai.configure(api_key=self.google_api_key)  # Configure the Google Generative AI client
        self.model = genai.GenerativeModel('gemini-2.5-flash-preview-05-20') # Initialize the Gemini model
        self.reset_chat()
        self.graph = self.create_graph()
        
    def create_graph(self):
        workflow = StateGraph(AgentState)
        workflow.add_node('agent', call_model)
        workflow.add_node('tools', call_tools)

        workflow.add_conditional_edges('agent', route_to_tools)

        workflow.add_edge('tools', 'agent')
        # Set entry point
        workflow.add_edge(START, 'agent')

        app = workflow.compile()
        # img = display(Image(app.get_graph().draw_mermaid_png()))
        # img.save('graph_image.png')
        return app
    
    def user_sent_message(self, user_query, input_data: List[InputData]):
        try:
            starting_image_paths_set = set(sum(self.output_image_paths.values(), []))
            input_state = {
                "messages": self.chat_history + [HumanMessage(content=user_query)],
                "output_image_paths": list(starting_image_paths_set),
                "input_data": input_data,
                "current_variables": {},
                "intermediate_outputs": []
            }

            result = self.graph.invoke(input_state, {"recursion_limit": 25})
            self.chat_history = result["messages"]
            new_image_paths = set(result["output_image_paths"]) - starting_image_paths_set
            self.output_image_paths[len(self.chat_history) - 1] = list(new_image_paths)
            if "intermediate_outputs" in result:
                self.intermediate_outputs.extend(result["intermediate_outputs"])
        except Exception as e:
            # Add error handling
            error_message = f"An error occurred: {str(e)}"
            self.chat_history.append(AIMessage(content=error_message))
            raise  # Re-raise the exception for Streamlit to handle

    def reset_chat(self):
        self.chat_history = []
        self.intermediate_outputs = []
        self.output_image_paths = {}
