from flask import Flask, render_template, request, jsonify
from college_chatbot import CollegeChatbot
import os

app = Flask(__name__)

# Setup database connection parameters
db_params = {
    'host': 'localhost',
    'database': 'postgres',
    'user': 'postgres',
    'password': "Saurabh_Agrahari",  # Consider using environment variables for sensitive info
    'port': '5432'
}

# Ensure that the Groq API key is available
groq_api_key = "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"  # Directly set the API key here
  # Or provide explicitly as a string

if not groq_api_key:
    raise ValueError("GROQ_API_KEY environment variable not set!")

# Initialize chatbot instance
chatbot = CollegeChatbot(db_params, groq_api_key)

@app.route('/')
def home():
    """Render the home page where the user can input their question."""
    return render_template('index.html')
@app.route('/ask', methods=['POST'])
def ask():
    """Handle user input and return the chatbot response."""
    try:
        # Get JSON data from the request
        data = request.get_json()
        user_query = data.get('user_query')

        if not user_query:
            return jsonify({'error': 'No query provided'}), 400

        # Get the answer from the chatbot
        response = chatbot.get_answer(user_query)
        return jsonify(response)  # Return chatbot response as JSON

    except Exception as e:
        # Catch any errors and return them as JSON
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
