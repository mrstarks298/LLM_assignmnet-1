
import os
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from sqlalchemy import create_engine, text
from groq import Groq  # Importing the Groq client

class CollegeChatbot:
    def __init__(self, db_params, groq_api_key=None):
        """
        Initialize the chatbot, connecting to the database and setting up Groq client.
        :param db_params: Dictionary containing database connection parameters.
        :param groq_api_key: API key for the Groq client (can be set via environment variable).
        """
        # Initialize the sentence transformer model
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Use environment variable if no key is explicitly passed
        groq_api_key = groq_api_key or os.environ.get("GROQ_API_KEY")
        if not groq_api_key:
            raise ValueError("GROQ_API_KEY must be set as an environment variable or passed explicitly!")

        # Initialize the Groq API client
        self.groq_client = Groq(api_key=groq_api_key)
        print("Groq client initialized successfully!")

        # Connect to the database
        try:
            self.engine = create_engine(
                f"postgresql://{db_params['user']}:{db_params['password']}@{db_params['host']}:{db_params['port']}/{db_params['database']}"
            )
            with self.engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            print("Database connection successful!")
        except Exception as e:
            print(f"Error connecting to the database: {e}")
            raise

    def embed_query(self, query):
        """Generate an embedding for the given query."""
        try:
            return self.model.encode(query)
        except Exception as e:
            print(f"Error generating embedding: {e}")
            raise
#it will search answer in dataabse which has been created by the code which will be in notebook in repo.

    def find_similar_questions(self, query_embedding):
        """Retrieve the most similar questions from the database."""
        try:
            with self.engine.connect() as connection:
                sql_query = text("""
                    SELECT id, question, answer, 
                           (embedding <=> CAST(:query_embedding AS vector)) AS cosine_distance
                    FROM qa1_embeddings
                    ORDER BY cosine_distance
                    LIMIT 5;
                """)
                result = connection.execute(sql_query, {'query_embedding': query_embedding.tolist()})
                return pd.DataFrame(result.fetchall(), columns=['id', 'question', 'answer', 'cosine_distance'])
        except Exception as e:
            print(f"Error finding similar questions: {e}")
            raise

    def groq_enhance_response(self, base_answer):
        """Enhance the answer using Groq API."""
        try:
            chat_completion = self.groq_client.chat.completions.create(
                messages=[
                  {
                    "role": "user",
                    "content": f"""
                    Context: {base_answer}
                    Provide a clear and direct answer based ONLY on the given context. 
                    Do NOT include the original question in your response.
                    If the context does not provide a clear answer, respond with: "I don't have an appropriate answer."
                    """
                }
                ],
                model="llama3-8b-8192",  # Use the desired Groq LLaMA model
                stream=False
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return f"Error enhancing response with Groq: {e}"
    
    def handle_greeting(self, user_query):
        """Respond to greetings like 'hey', 'hello', etc."""
        greetings = ['hey', 'hello', 'hi',  'good morning', 'good evening']
        # Convert the user query to lowercase and check if it contains any greeting words
        user_query_lower = user_query.lower()
        for greeting in greetings:
            if greeting in user_query_lower:
                return "Hey! What do you want to know about Sitare University?"
        return None

    def get_answer(self, user_query, similarity_threshold=0.7):
        """Get the answer to a user's query."""
        try:
            # Check if the user is greeting the bot
            greeting_response = self.handle_greeting(user_query)
            if greeting_response:
                return {'answer': greeting_response}

            query_embedding = self.embed_query(user_query)
            similar_questions = self.find_similar_questions(query_embedding)
            
            if not similar_questions.empty:
                top_match = similar_questions.iloc[0]
                similarity_score = 1 - top_match['cosine_distance']
                base_answer = top_match['answer']
                enhanced_answer = self.groq_enhance_response(base_answer)
                
                if similarity_score >= similarity_threshold:
                    return {
                        'answer': enhanced_answer,
                        'original_question': top_match['question'],
                        'similarity_score': similarity_score,
                        'similar_questions': similar_questions.to_dict('records')
                    }
                else:
                    return {
                        'answer': "Sorry, I couldn't find a confidently matching answer.",
                        'similarity_score': similarity_score,
                        'similar_questions': similar_questions.to_dict('records')
                    }
            else:
                return {'answer': "Sorry, no similar questions were found."}
        except Exception as e:
            print(f"Error getting answer: {e}")
            return {'answer': f"An error occurred: {e}"}
#eaxple like 
if __name__ == "__main__":
    # Setup database connection parameters
    db_params = {
        'host': 'localhost',
        'database': 'postgres',
        'user': 'postgres',
        'password': "your password ",
        'port': '5432'
    }

    # Set up Groq API key (or set as environment variable)
    groq_api_key = "your GRoq API"

    # Initialize chatbot instance
    chatbot = CollegeChatbot(db_params, groq_api_key)

    # Example query
    user_query = input("Ask your question: ")
    response = chatbot.get_answer(user_query)

    # Print the response
    print(f"\nYour Question: {user_query}")
    print(f"\nAnswer: {response['answer']}")
    
    if 'original_question' in response:
        print(f"\nOriginal Question in Database: {response['original_question']}")

    if 'similar_questions' in response:
        print("\nSimilar Questions:")
        for q in response['similar_questions']:
            print(f"- {q['question']} (Distance: {q['cosine_distance']:.4f})")

    if 'similarity_score' in response:
        print(f"\nSimilarity Score: {response['similarity_score']:.4f}")
