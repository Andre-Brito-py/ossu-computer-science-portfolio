import json
import logging
import os
import google.generativeai as genai
from tools import AVAILABLE_TOOLS
from verification import verify_action

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("ReAct_Agent")

class AutonomousAgent:
    def __init__(self):
        # Configure Gemini API
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is missing.")
            
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-pro')
        
        self.system_prompt = """
        You are an Autonomous Agent capable of thinking and taking actions.
        You have access to the following tools:
        1. send_email(to_email: str, subject: str, body: str)
        2. generate_boleto(customer_cpf: str, value: float, due_date: str)
        
        Use the ReAct format:
        Thought: Explain your reasoning step-by-step.
        Action: ToolName
        Action Input: {"param1": "value", "param2": "value"}
        
        Once you have the final answer, output:
        Final Answer: <your final response to the user>
        """

    def run(self, user_prompt: str, max_steps: int = 5):
        logger.info(f"Starting agent loop with prompt: '{user_prompt}'")
        
        chat = self.model.start_chat(history=[])
        chat.send_message(self.system_prompt)
        
        current_prompt = user_prompt
        
        for step in range(max_steps):
            logger.info(f"--- Step {step + 1} ---")
            
            response = chat.send_message(current_prompt)
            text = response.text
            print(f"\n[Agent output]\n{text}\n")
            
            if "Final Answer:" in text:
                logger.info("Agent has reached a final answer.")
                return text.split("Final Answer:")[-1].strip()
                
            if "Action:" in text and "Action Input:" in text:
                try:
                    action_line = [line for line in text.split('\n') if line.startswith("Action:")][0]
                    input_line = [line for line in text.split('\n') if line.startswith("Action Input:")][0]
                    
                    tool_name = action_line.replace("Action:", "").strip()
                    tool_input_str = input_line.replace("Action Input:", "").strip()
                    tool_input = json.loads(tool_input_str)
                    
                    logger.info(f"Agent requested tool: {tool_name} with params: {tool_input}")
                    
                    if tool_name in AVAILABLE_TOOLS:
                        # 1. Human in the loop verification
                        if verify_action(tool_name, tool_input):
                            # 2. Execute Action
                            tool_func = AVAILABLE_TOOLS[tool_name]
                            tool_result = tool_func(**tool_input)
                            logger.info(f"Tool execution result: {tool_result}")
                            current_prompt = f"Observation: {tool_result}"
                        else:
                            current_prompt = "Observation: [Error] Human denied permission to run this tool. Think of an alternative or inform the user."
                    else:
                        current_prompt = f"Observation: Tool {tool_name} does not exist."
                        
                except Exception as e:
                    logger.error(f"Failed to parse or execute action: {e}")
                    current_prompt = f"Observation: [Error] {str(e)}. Make sure Action Input is valid JSON."
            else:
                current_prompt = "Observation: Please output 'Action:' and 'Action Input:' or 'Final Answer:'"
                
        return "Agent stopped. Max steps reached."
