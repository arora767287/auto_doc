from datetime import datetime, timedelta
from cryptography.fernet import Fernet
import json

class EncryptionHandler:
    def __init__(self, key):
        self.fernet = Fernet(key)
    
    def encrypt(self, data):
        return self.fernet.encrypt(data.encode()).decode()
    
    def decrypt(self, encrypted_data):
        return self.fernet.decrypt(encrypted_data.encode()).decode()

def format_date(date_str):
    """Format date string to consistent format"""
    return datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m-%d")

def get_date_range(days=7):
    """Get date range for queries"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    return start_date, end_date

def is_relevant_url(url):
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

def sanitize_content(content):
    """Sanitize content for safe storage"""
    if isinstance(content, dict):
        return json.dumps(content)
    return str(content)

def parse_json_safely(json_str):
    """Safely parse JSON string"""
    try:
        return json.loads(json_str) if json_str else {}
    except:
        return {}
