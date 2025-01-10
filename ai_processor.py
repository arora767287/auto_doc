import openai
from typing import List, Dict
import json

class AIDocumentationProcessor:
    def __init__(self, api_key: str):
        self.api_key = api_key
        openai.api_key = api_key

    def process_data_sources(self, jira_data: List[Dict], confluence_data: List[Dict], 
                           browser_history: List[Dict], chatgpt_history: List[Dict]) -> str:
        """Process all data sources and generate documentation"""
        
        # Combine all data sources into a structured format
        combined_data = self._combine_data_sources(
            jira_data, confluence_data, browser_history, chatgpt_history
        )
        
        # Generate documentation using GPT
        documentation = self._generate_documentation(combined_data)
        
        return documentation

    def _combine_data_sources(self, jira_data, confluence_data, browser_history, chatgpt_history):
        """Combine and structure all data sources"""
        return {
            'jira_tickets': self._process_jira_data(jira_data),
            'confluence_pages': self._process_confluence_data(confluence_data),
            'relevant_browsing': self._process_browser_history(browser_history),
            'chatgpt_conversations': self._process_chatgpt_history(chatgpt_history)
        }

    def _process_jira_data(self, jira_data):
        """Process Jira tickets into relevant summaries"""
        processed_data = []
        for ticket in jira_data:
            processed_data.append({
                'key': ticket.get('key'),
                'summary': ticket.get('summary'),
                'description': ticket.get('description'),
                'status': ticket.get('status'),
                'updated': ticket.get('updated')
            })
        return processed_data

    def _process_confluence_data(self, confluence_data):
        """Process Confluence pages into relevant summaries"""
        processed_data = []
        for page in confluence_data:
            processed_data.append({
                'title': page.get('title'),
                'content': page.get('content'),
                'last_modified': page.get('last_modified'),
                'url': page.get('url')
            })
        return processed_data

    def _process_browser_history(self, browser_history):
        """Process browser history into relevant summaries"""
        processed_data = []
        for entry in browser_history:
            if self._is_relevant_url(entry['url']):
                processed_data.append({
                    'title': entry.get('title'),
                    'url': entry.get('url'),
                    'timestamp': entry.get('timestamp')
                })
        return processed_data

    def _process_chatgpt_history(self, chatgpt_history):
        """Process ChatGPT conversation history"""
        processed_data = []
        for conv in chatgpt_history:
            processed_data.append({
                'title': conv.get('title'),
                'messages': conv.get('messages'),
                'created_at': conv.get('created_at')
            })
        return processed_data

    def _is_relevant_url(self, url: str) -> bool:
        """Check if URL is relevant for documentation"""
        relevant_domains = [
            'stackoverflow.com',
            'github.com',
            'docs.python.org',
            'confluence.',
            'jira.',
            'chat.openai.com'
        ]
        return any(domain in url.lower() for domain in relevant_domains)

    def _generate_documentation(self, combined_data: Dict) -> str:
        """Generate documentation using GPT-3"""
        try:
            # Create prompt from combined data
            prompt = self._create_prompt(combined_data)
            
            # Call GPT-3 API
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a technical documentation expert. Generate clear, concise documentation based on the provided data sources."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error generating documentation: {str(e)}")
            return ""

    def _create_prompt(self, combined_data: Dict) -> str:
        """Create a prompt for GPT from combined data"""
        prompt = "Generate technical documentation based on the following information:\n\n"
        
        # Add Jira tickets
        prompt += "JIRA TICKETS:\n"
        for ticket in combined_data['jira_tickets']:
            prompt += f"- {ticket['key']}: {ticket['summary']}\n"
        
        # Add Confluence pages
        prompt += "\nCONFLUENCE PAGES:\n"
        for page in combined_data['confluence_pages']:
            prompt += f"- {page['title']}\n"
        
        # Add relevant browser history
        prompt += "\nRELEVANT RESOURCES:\n"
        for entry in combined_data['relevant_browsing']:
            prompt += f"- {entry['title']}: {entry['url']}\n"
        
        # Add ChatGPT conversations
        prompt += "\nRELEVANT DISCUSSIONS:\n"
        for conv in combined_data['chatgpt_conversations']:
            prompt += f"- {conv['title']}\n"
        
        prompt += "\nPlease generate comprehensive documentation that includes:\n"
        prompt += "1. Overview\n2. Technical Details\n3. Implementation Steps\n4. Related Resources\n"
        
        return prompt
