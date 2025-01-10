from flask import Flask, render_template, request, jsonify, session
from flask_login import LoginManager, login_required, current_user
from models import db, User, Documentation
from config import Config
from data_collector import DataCollector
from ai_processor import AIDocumentationProcessor
from chatgpt_handler import ChatGPTHandler

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/generate_documentation', methods=['POST'])
@login_required
def generate_documentation():
    try:
        # Initialize collectors and processors
        data_collector = DataCollector(session)
        ai_processor = AIDocumentationProcessor(current_user.openai_key)
        
        # Fetch data from all sources
        jira_data = data_collector.fetch_jira_data()
        confluence_data = data_collector.fetch_confluence_data()
        browser_history = data_collector.fetch_browser_history()
        chatgpt_handler = ChatGPTHandler(current_user.openai_key)
        chatgpt_history = chatgpt_handler.get_conversation_history()
        
        # Process data and generate documentation
        documentation = ai_processor.process_data_sources(
            jira_data,
            confluence_data,
            browser_history,
            chatgpt_history
        )
        
        # Save documentation
        new_doc = Documentation(
            user_id=current_user.id,
            content=documentation,
            jira_tickets=json.dumps(jira_data),
            browser_history=json.dumps(browser_history),
            chatgpt_conversations=json.dumps(chatgpt_history)
        )
        db.session.add(new_doc)
        db.session.commit()
        
        return jsonify({'status': 'success', 'documentation': documentation})
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
