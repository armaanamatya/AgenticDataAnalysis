from langchain_core.messages import HumanMessage, AIMessage
from typing import List
from dataclasses import dataclass
import google.generativeai as genai
import requests
from langgraph.graph import StateGraph, START, END
from .graph.state import AgentState
from .graph.nodes import call_model, call_tools, route_to_tools
from Pages.data_models import InputData
# from IPython.display import Image, display

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
        # Format the prompt as a list of messages for the Gemini API
        prompt_messages = []
        for msg in self.chat_history:
            if isinstance(msg, HumanMessage):
                prompt_messages.append({"role": "user", "parts": [msg.content]})
            else:
                prompt_messages.append({"role": "model", "parts": [msg.content]})
        prompt_messages.append({"role": "user", "parts": [user_query]})

        # Convert InputData objects to a string and append to the last user message
        input_data_str = ""
        if input_data:
            input_data_lines = [
                f"- Variable: {data.variable_name}, Path: {data.data_path}, Description: {data.data_description}"
                for data in input_data
            ]
            input_data_str = "Available input data:\n" + "\n".join(input_data_lines)

            if prompt_messages:
                # Append input_data_str to the parts of the last user message
                prompt_messages[-1]["parts"].append(input_data_str)
            else:
                # If no previous messages, create a new user message with input_data_str
                prompt_messages.append({"role": "user", "parts": [input_data_str]})


        # Send request to Gemini
        try:
            # Use the model's generate_content method for conversational turn
            response = self.model.generate_content(prompt_messages)
        except Exception as e:
            print(f"Google Generative AI API Error: {e}")
            return

        if not response.parts: # Check if response has content
            print(f"Unexpected response from Gemini: {response}")
            return

        # Extract the response text
        assistant_response = response.text.strip()

        # Update chat history
        self.chat_history.append(HumanMessage(content=user_query))
        self.chat_history.append(AIMessage(content=assistant_response))
        
        print(f"User query: {user_query}")
        print(f"Assistant response: {assistant_response}")
        
        # starting_image_paths_set = set(sum(self.output_image_paths.values(), []))
        # input_state = {
        #     "messages": self.chat_history + [HumanMessage(content=user_query)],
        #     "output_image_paths": list(starting_image_paths_set),
        #     "input_data": input_data,
        # }

        # result = self.graph.invoke(input_state, {"recursion_limit": 25})
        # self.chat_history = result["messages"]
        # new_image_paths = set(result["output_image_paths"]) - starting_image_paths_set
        # self.output_image_paths[len(self.chat_history) - 1] = list(new_image_paths)
        # if "intermediate_outputs" in result:
        #     self.intermediate_outputs.extend(result["intermediate_outputs"])

    def reset_chat(self):
        self.chat_history = []
        self.intermediate_outputs = []
        self.output_image_paths = {}
