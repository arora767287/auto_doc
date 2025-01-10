# Browser History Analyzer

A Flask-based web application that analyzes browser history using AI to provide insights and patterns.

## Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd browser-history-analyzer
Create and activate a virtual environment:

bash
Copy code
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Create a .env file in the root directory with the following variables:

plaintext
Copy code
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///site.db
OPENAI_API_KEY=your-openai-api-key
Initialize the database:

bash
Copy code
flask db init
flask db migrate
flask db upgrade
Running the Application
Ensure your virtual environment is activated.

Run the Flask application:

bash
Copy code
flask run
Access the application at http://localhost:5000.

Features
Browser history collection from Chrome and Safari
AI-powered analysis of browsing patterns
User authentication
Detailed insights dashboard
Export functionality for analysis results
Requirements
Python 3.8+
Flask
SQLAlchemy
OpenAI API key
Notes
After adding these files, your application should be complete. Make sure to:

Create the necessary directories if they don't exist.
Set up your environment variables in the .env file.
Install all required dependencies.
Initialize and migrate the database before running the application.
The application should now be fully functional with all necessary components in place.


This ensures it is all in one block. You can directly use this as your `README.md`.












