# Browser History Analyzer

A Flask-based web application that analyzes browser history using AI to provide insights and patterns.

## Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd browser-history-analyzer
   
2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies:

```bash
pip install -r requirements.txt

4. Create a .env file in the root directory with the following variables:

FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///site.db
OPENAI_API_KEY=your-openai-api-key

5. Initialize the database:

   ```bash
flask db init
flask db migrate
flask db upgrade

6. Running the Application

### Ensure your virtual environment is activated.
7. Run the Flask application:

```bash
flask run
Access the application at http://localhost:5000.

### Features
Browser history collection from Chrome and Safari
AI-powered analysis of browsing patterns
User authentication
Detailed insights dashboard
Export functionality for analysis results

Create the necessary directories if they don't exist.
Set up your environment variables in the .env file.
Install all required dependencies.
Initialize and migrate the database before running the application.
The application should now be fully functional with all necessary components in place.


