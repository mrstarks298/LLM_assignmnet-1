

import os
from flask import Flask, render_template, request, jsonify
from college_chatbot import CollegeChatbot
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def get_db_config():
    """
    Retrieve database configuration from environment variables or predefined config.
    Provides a flexible way to manage database credentials.
    """
    # Priority 1: Environment variables
    db_host = os.environ.get('DB_HOST')
    db_name = os.environ.get('DB_NAME')
    db_user = os.environ.get('DB_USER')
    db_password = os.environ.get('DB_PASSWORD')
    db_port = os.environ.get('DB_PORT')

    # Priority 2: Fallback to predefined configuration if env vars are not set
    if not all([db_host, db_name, db_user, db_password, db_port]):
        logger.warning("Using fallback database configuration. Consider setting environment variables.")
        return {
            'host': 'localhost',
            'database': 'postgres',
            'user': 'postgres',
            'password': 'Saurabh_Agrahari',  # IMPORTANT: Change this!
            'port': '5432'
        }

    return {
        'host': db_host,
        'database': db_name,
        'user': db_user,
        'password': db_password,
        'port': db_port
    }

def create_app():
    """
    Create and configure the Flask application.
    """
    app = Flask(__name__)

    # Secure API key retrieval
    # IMPORTANT: Replace this with a secure method of storing your API key
    groq_api_key = os.environ.get('GROQ_API_KEY', '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')
    
    if not groq_api_key:
        logger.error("GROQ API Key is missing!")
        raise ValueError("GROQ_API_KEY must be set")

    # Initialize chatbot instance
    try:
        db_params = get_db_config()
        chatbot = CollegeChatbot(db_params, groq_api_key)
    except Exception as e:
        logger.error(f"Failed to initialize chatbot: {e}")
        raise

    @app.route('/')
    def home():
        """Render the home page where the user can input their question."""
        return render_template('index.html')

    @app.route('/ask', methods=['POST'])
    def ask():
        """
        Handle user queries and return chatbot responses.
        Provides standardized error handling and response formatting.
        """
        try:
            data = request.get_json()
            user_query = data.get('user_query', '').strip()
            
            if not user_query:
                return jsonify({
                    'error': 'No query provided',
                    'status': 'error'
                }), 400
            
            # Get the answer from the chatbot
            response = chatbot.get_answer(user_query)
            
            # Standardize response format
            formatted_response = {
                'status': 'success',
                'answer': response.get('answer', 'No answer found'),
                'original_question': response.get('original_question', user_query),
                'similar_questions': response.get('similar_questions', []),
                'similarity_score': response.get('similarity_score', 0.0)
            }
            
            return jsonify(formatted_response)
        
        except Exception as e:
            logger.exception("Unexpected error processing query")
            return jsonify({
                'status': 'error',
                'error': str(e),
                'message': 'An unexpected error occurred while processing your query'
            }), 500

    return app

def main():
    """
    Main entry point for the application.
    """
    app = create_app()
    
    # Use environment variable for port with default
    port = int(os.environ.get('PORT', 5001))
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    app.run(
        host='0.0.0.0', 
        port=port, 
        debug=debug_mode
    )

if __name__ == '__main__':
    main()


