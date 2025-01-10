import openai
from typing import List, Dict
import json
from datetime import datetime

class ChatGPTHandler:
    def __init__(self, api_key: str):
        self.api_key = api_key
        openai.api_key = api_key
        
    def get_conversation_history(self, days: int = 7) -> List[Dict]:
        """Get ChatGPT conversation history"""
        try:
            # Note: OpenAI API doesn't provide conversation history
            # This is a placeholder for future implementation or alternative approaches
            return []
            
        except Exception as e:
            print(f"Error accessing ChatGPT history: {str(e)}")
            return []
            
    def generate_documentation(self, context: str) -> str:
        """Generate documentation using ChatGPT"""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a technical documentation expert."},
                    {"role": "user", "content": f"Generate technical documentation for: {context}"}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error generating documentation: {str(e)}")
            return ""
            
    def summarize_content(self, content: str) -> str:
        """Summarize content using ChatGPT"""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Summarize the following content concisely:"},
                    {"role": "user", "content": content}
                ],
                temperature=0.5,
                max_tokens=500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error summarizing content: {str(e)}")
            return ""
