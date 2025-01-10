from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    
    # Integration credentials and status
    jira_token = db.Column(db.String(256))
    jira_url = db.Column(db.String(256))  # Added
    jira_username = db.Column(db.String(120))  # Added
    jira_enabled = db.Column(db.Boolean, default=False)  # Added
    
    confluence_token = db.Column(db.String(256))
    confluence_url = db.Column(db.String(256))  # Added
    confluence_username = db.Column(db.String(120))  # Added
    confluence_enabled = db.Column(db.Boolean, default=False)  # Added
    
    openai_key = db.Column(db.String(256))
    openai_enabled = db.Column(db.Boolean, default=False)  # Added
    
    # User preferences
    browser_history_enabled = db.Column(db.Boolean, default=True)  # Added
    update_frequency = db.Column(db.Integer, default=4)  # Hours between updates
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_documentation_update = db.Column(db.DateTime)  # Added
    
    # Password handling
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    # Documentation relationship
    documentations = db.relationship('Documentation', backref='user', lazy=True)

class Documentation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text)
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)
    confluence_url = db.Column(db.String(256))
    confluence_page_id = db.Column(db.String(256))  # Added
    
    # Status tracking
    status = db.Column(db.String(50), default='pending')  # Added
    error_message = db.Column(db.Text)  # Added
    
    # Metadata
    jira_tickets = db.Column(db.Text)  # JSON string of related tickets
    browser_history = db.Column(db.Text)  # JSON string of relevant history
    chatgpt_conversations = db.Column(db.Text)  # JSON string of relevant conversations
    
    # Version tracking
    version = db.Column(db.Integer, default=1)  # Added
    previous_version_id = db.Column(db.Integer, db.ForeignKey('documentation.id'))  # Added
