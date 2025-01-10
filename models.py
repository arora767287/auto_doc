from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    
    # Integration credentials
    jira_token = db.Column(db.String(256))
    confluence_token = db.Column(db.String(256))
    openai_key = db.Column(db.String(256))
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Documentation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text)
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)
    confluence_url = db.Column(db.String(256))
    
    # Metadata
    jira_tickets = db.Column(db.Text)  # JSON string of related tickets
    browser_history = db.Column(db.Text)  # JSON string of relevant history
    chatgpt_conversations = db.Column(db.Text)  # JSON string of relevant conversations
