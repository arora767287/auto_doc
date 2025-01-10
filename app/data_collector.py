from typing import Dict, List
from datetime import datetime, timedelta
from .browser_history.chrome import ChromeHistory
from .browser_history.safari import SafariHistory
import os

class DataCollector:
    def __init__(self, session):
        self.session = session
        self.chrome_history = ChromeHistory()
        self.safari_history = SafariHistory()

    def fetch_jira_data(self, days: int = 7) -> List[Dict]:
        """Fetch relevant Jira tickets"""
        try:
            from jira import JIRA
            
            jira = JIRA(
                server=self.session.get('jira_url'),
                basic_auth=(
                    self.session.get('jira_username'),
                    self.session.get('jira_token')
                )
            )
            
            # Calculate date range
            date_from = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
            
            # JQL query
            jql_str = f'updated >= "{date_from}" ORDER BY updated DESC'
            
            # Fetch issues
            issues = jira.search_issues(jql_str, maxResults=100)
            
            return [{
                'key': issue.key,
                'summary': issue.fields.summary,
                'description': issue.fields.description,
                'status': str(issue.fields.status),
                'updated': issue.fields.updated
            } for issue in issues]
            
        except Exception as e:
            print(f"Error fetching Jira data: {str(e)}")
            return []

    def fetch_confluence_data(self, days: int = 7) -> List[Dict]:
        """Fetch relevant Confluence pages"""
        try:
            from atlassian import Confluence
            
            confluence = Confluence(
                url=self.session.get('confluence_url'),
                username=self.session.get('confluence_username'),
                password=self.session.get('confluence_token')
            )
            
            # Calculate date range
            date_from = datetime.now() - timedelta(days=days)
            
            # Get recently updated pages
            pages = confluence.get_all_pages_from_space(
                space='TEAM',
                start=0,
                limit=100
            )
            
            results = []
            for page in pages:
                page_info = confluence.get_page_by_id(page['id'])
                updated = datetime.strptime(page_info['version']['when'], '%Y-%m-%dT%H:%M:%S.%fZ')
                
                if updated >= date_from:
                    results.append({
                        'title': page['title'],
                        'content': confluence.get_page_content(page['id']),
                        'last_modified': updated,
                        'url': f"{self.session.get('confluence_url')}{page['_links']['webui']}"
                    })
            
            return results
            
        except Exception as e:
            print(f"Error fetching Confluence data: {str(e)}")
            return []

    def fetch_browser_history(self, days: int = 7) -> List[Dict]:
        """Fetch relevant browser history from Chrome and Safari"""
        try:
            # Get history from both browsers
            chrome_history = self.chrome_history.get_history(days)
            safari_history = self.safari_history.get_history(days)
            
            # Combine and sort by timestamp
            combined_history = chrome_history + safari_history
            combined_history.sort(key=lambda x: x['timestamp'], reverse=True)
            
            return combined_history
            
        except Exception as e:
            print(f"Error fetching browser history: {str(e)}")
            return []
