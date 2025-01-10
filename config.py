import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    JIRA_URL = os.getenv('JIRA_URL')
    JIRA_USERNAME = os.getenv('JIRA_USERNAME')
    JIRA_API_TOKEN = os.getenv('JIRA_API_TOKEN')
    CONFLUENCE_URL = os.getenv('CONFLUENCE_URL')
    CONFLUENCE_USERNAME = os.getenv('CONFLUENCE_USERNAME')
    CONFLUENCE_API_TOKEN = os.getenv('CONFLUENCE_API_TOKEN')
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    
    # Additional configuration
    CONFLUENCE_SPACE = "TEAM"
    CONFLUENCE_PAGE_TITLE = "Work Documentation"
    JIRA_PROJECT = "PROJ"
    BROWSER_HISTORY_LIMIT_DAYS = 7
