# Actual Gemini wrapper, sliding window to keep track of last 10 messages and responses
# Requires dotenv and genai, run on pi:
# pip install google-generativeai
# pip install python-dotenv

import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

class GeminiBrain:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        
        if not self.api_key:
            raise ValueError("Please provide a Gemini API key in the .env file.")

        genai.configure(api_key=self.api_key)

        self.model = genai.GenerativeModel('gemini-1.5-flash')

        # start_chat() automatically keeps track of the conversation history
        self.chat_session = self.model.start_chat(history=[])
        
        # 10 turns = 10 user messages + 10 model responses = 20 total items
        self.max_history_items = 20 

    def generate_response(self, user_text):
        print("Thinking...")
        try:
            # Prompt injection
            instruction = f"Reply conversationally and concisely to: {user_text}"
            
            # Send prompt to Gemini
            response = self.chat_session.send_message(instruction)
            
            # Manage message history cache, keeps most recent
            if len(self.chat_session.history) > self.max_history_items:
                self.chat_session.history = self.chat_session.history[-self.max_history_items:]
                
            return response.text
            
        except Exception as e:
            print(f"API Error: {e}")
            return "I'm sorry, I am having trouble connecting to Gemini right now."

# Testing
if __name__ == "__main__":
    ai = GeminiBrain() 
    
    print("Gemini Initialized. Type 'quit' to exit.")
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ['quit', 'exit']:
            break
            
        answer = ai.generate_response(user_input)
        print(f"\nGemini: {answer}")
        print(f"[Debug: Currently remembering {len(ai.chat_session.history)} messages]")